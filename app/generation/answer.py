import os
import re

from openai import OpenAI

SUMMARY_TERMS = ("summarize", "summary", "overview")


def _extractive_answer(question: str, chunks: list[dict[str, float | str]]) -> str:
    if not chunks:
        return "I do not know. Not enough context to answer that question."

    stopwords = {
        "the",
        "is",
        "are",
        "a",
        "an",
        "of",
        "to",
        "for",
        "and",
        "or",
        "what",
        "which",
        "who",
        "when",
        "where",
        "why",
        "how",
        "does",
        "do",
        "did",
        "it",
        "in",
        "on",
        "with",
        "by",
        "about",
        "from",
        "be",
        "as",
        "at",
        "this",
        "that",
        "these",
        "those",
    }
    tokens = re.findall(r"[A-Za-z0-9']+", question.lower())
    keywords = [token for token in tokens if token not in stopwords]

    matched_sentences = []
    for chunk in chunks:
        text = str(chunk.get("text", ""))
        raw_sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        sentences = []
        i = 0
        while i < len(raw_sentences):
            current = raw_sentences[i]
            if current.endswith("Inc.") and i + 1 < len(raw_sentences):
                current = f"{current} {raw_sentences[i + 1]}"
                i += 1
            sentences.append(current)
            i += 1

        for sentence in sentences:
            sentence_lower = sentence.lower()
            if keywords and any(term in sentence_lower for term in keywords):
                matched_sentences.append(sentence)
        if matched_sentences:
            break

    if matched_sentences:
        return " ".join(matched_sentences[:3])

    question_lower = question.lower()
    if any(term in question_lower for term in SUMMARY_TERMS):
        summary_sentences = []
        for chunk in chunks:
            text = str(chunk.get("text", ""))
            raw_sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
            for sentence in raw_sentences:
                summary_sentences.append(sentence)
                if len(summary_sentences) >= 3:
                    break
            if len(summary_sentences) >= 3:
                break
        if summary_sentences:
            return " ".join(summary_sentences)

    return "I do not know. Not enough context to answer that question."


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _normalize(text: str) -> str:
    return " ".join(_tokenize(text))


def _upper_ratio(text: str) -> float:
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return 0.0
    upper = sum(1 for ch in letters if ch.isupper())
    return upper / len(letters)


def _sanitize_context(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if _upper_ratio(stripped) > 0.7 and len(stripped) < 140:
            continue
        lines.append(stripped)
    return "\n".join(lines)


def _build_context(chunks: list[dict[str, float | str]], summary_mode: bool) -> str:
    if summary_mode:
        sanitized_chunks = [
            f"Chunk {i + 1}:\n{_sanitize_context(str(item.get('text', '')))}"
            for i, item in enumerate(chunks)
        ]
        return "\n\n".join(sanitized_chunks)
    return "\n\n".join([f"Chunk {i + 1}:\n{item['text']}" for i, item in enumerate(chunks)])


def _looks_quoted(answer_text: str, chunks: list[dict[str, float | str]]) -> bool:
    normalized_answer = _normalize(answer_text)
    if len(normalized_answer) < 80:
        return False
    for item in chunks:
        chunk_text = _normalize(str(item.get("text", "")))
        if normalized_answer in chunk_text or chunk_text in normalized_answer:
            return True
    return False


def _has_ngram_overlap(answer_text: str, chunks: list[dict[str, float | str]], n: int = 6) -> bool:
    answer_tokens = _tokenize(answer_text)
    if len(answer_tokens) < n:
        return False
    answer_ngrams = {tuple(answer_tokens[i : i + n]) for i in range(len(answer_tokens) - n + 1)}
    for item in chunks:
        chunk_tokens = _tokenize(str(item.get("text", "")))
        if len(chunk_tokens) < n:
            continue
        chunk_ngrams = {tuple(chunk_tokens[i : i + n]) for i in range(len(chunk_tokens) - n + 1)}
        if answer_ngrams & chunk_ngrams:
            return True
    return False


def _needs_summary_rewrite(
    answer_text: str,
    summary_mode: bool,
    chunks: list[dict[str, float | str]],
) -> bool:
    word_count = len(answer_text.split())
    sentence_count = len([s for s in re.split(r"[.!?]+", answer_text) if s.strip()])
    return (
        summary_mode
        and (
            word_count < 30
            or sentence_count < 2
            or _upper_ratio(answer_text) > 0.6
            or _looks_quoted(answer_text, chunks)
            or _has_ngram_overlap(answer_text, chunks)
        )
    )


def _too_verbose(answer_text: str) -> bool:
    sentence_count = len([s for s in re.split(r"[.!?]+", answer_text) if s.strip()])
    word_count = len(answer_text.split())
    return sentence_count > 6 or word_count > 160


def _call_model(
    client: OpenAI,
    model_name: str,
    messages: list[dict[str, str]],
    temperature: float,
) -> str:
    if hasattr(client, "responses"):
        response = client.responses.create(
            model=model_name,
            input=messages,
            temperature=temperature,
        )
        return response.output_text.strip()
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()


def generate_answer(
    question: str,
    chunks: list[dict[str, float | str]],
    model: str | None = None,
    api_key: str | None = None,
) -> tuple[str, list[dict[str, float | str]]]:
    if not chunks:
        return "I do not know. Not enough context to answer that question.", []

    api_key = api_key or os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return "Missing OPENAI_API_KEY. Set it and try again.", []

    model = model or os.getenv("OPENAI_MODEL", "gpt-5.2")
    fallback_model = os.getenv("OPENAI_FALLBACK_MODEL", "gpt-4o-mini")
    summary_mode = any(term in question.lower() for term in SUMMARY_TERMS)

    context = _build_context(chunks, summary_mode)
    effective_model = fallback_model if summary_mode and fallback_model else model

    system_prompt = (
        "You are a document assistant. Provide a clear, user-friendly answer in your own words "
        "based only on the provided context. Do not quote or copy sentences verbatim from the "
        "context and do not list raw chunks. If the answer is not in the context, say you do "
        "not know."
    )
    user_prompt = f"Question: {question}\n\nContext:\n{context}"
    if summary_mode:
        user_prompt = (
            f"Question: {question}\n\nContext:\n{context}\n\n"
            "Write a plain-English summary of the document's main ideas. "
            "Do not quote or copy sentences from the context."
        )

    client = OpenAI(api_key=api_key)

    try:
        answer = _call_model(
            client,
            effective_model,
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        if _needs_summary_rewrite(answer, summary_mode, chunks) or _too_verbose(answer):
            rewrite_model = fallback_model if fallback_model and fallback_model != model else model
            rewrite_prompt = (
                "Rewrite as a concise, user-friendly summary. "
                "Use plain language and do not quote or copy sentences verbatim from the context. "
                "Avoid reusing any 6-word sequence from the context. Focus on the main topic, key "
                "points, and outcome or conclusion."
            )
            answer = _call_model(
                client,
                rewrite_model,
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                    {"role": "user", "content": rewrite_prompt},
                ],
                temperature=0.3,
            )
            if summary_mode and _needs_summary_rewrite(answer, summary_mode, chunks):
                final_prompt = (
                    "Summarize the document using plain language. "
                    "Do not use quotations or headings. Include the main subject, key points, "
                    "and the overall conclusion."
                )
                answer = _call_model(
                    client,
                    rewrite_model,
                    [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                        {"role": "user", "content": final_prompt},
                    ],
                    temperature=0.4,
                )
        return answer, chunks
    except Exception:
        if fallback_model and fallback_model != model:
            try:
                answer = _call_model(
                    client,
                    fallback_model,
                    [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.2,
                )
                return answer, chunks
            except Exception:
                pass
        return _extractive_answer(question, chunks), chunks
