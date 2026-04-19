import os
import re

from openai import OpenAI


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
    if any(term in question_lower for term in ["summarize", "summary", "overview"]):
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
    context = "\n\n".join([f"Chunk {i + 1}:\n{item['text']}" for i, item in enumerate(chunks)])

    system_prompt = (
        "You are a document assistant. Answer only with the provided context. "
        "If the answer is not in the context, say you do not know."
    )
    user_prompt = f"Question: {question}\n\nContext:\n{context}"

    client = OpenAI(api_key=api_key)
    try:
        response = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        answer = response.output_text.strip()
        return answer, chunks
    except Exception:
        if fallback_model and fallback_model != model:
            try:
                response = client.responses.create(
                    model=fallback_model,
                    input=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.2,
                )
                answer = response.output_text.strip()
                return answer, chunks
            except Exception:
                pass
            return _extractive_answer(question, chunks), chunks
