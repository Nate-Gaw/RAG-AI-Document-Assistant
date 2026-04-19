import os
import tempfile

import pytest

from app.processing.chunker import chunk_text, clean_text
from app.processing.extractor import extract_text


def _extract_from_text(content: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as file:
        file.write(content)
        file_path = file.name

    with open(file_path, "rb") as file:
        data = file.read()
    os.unlink(file_path)

    return extract_text(data, file_path)


# --------------------------------------------------
# 1. TEXT EXTRACTION TESTS
# --------------------------------------------------

@pytest.mark.parametrize(
    "content",
    [
        "The capital of France is Paris.",
        "Python is used for AI and data science.",
        "Short text.",
    ],
)
def test_extraction_basic(content: str) -> None:
    extracted = _extract_from_text(content)

    assert extracted is not None
    assert len(extracted.strip()) > 0
    assert any(word in extracted for word in content.split())


@pytest.mark.parametrize(
    "content",
    [
        "Line1\n\n\nLine2",
        "Weird    spacing   test",
        "Symbols !!! ??? ###",
    ],
)
def test_extraction_edge_cases(content: str) -> None:
    extracted = _extract_from_text(content)

    assert extracted is not None
    assert len(extracted) > 0


# --------------------------------------------------
# 2. TEXT CLEANING TESTS
# --------------------------------------------------

@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Hello\n\nWorld", "Hello\nWorld"),
        ("This    is   messy", "This is messy"),
        ("Text\twith\t tabs", "Text with tabs"),
    ],
)
def test_cleaning_basic(raw: str, expected: str) -> None:
    cleaned = clean_text(raw)

    assert cleaned is not None
    assert "  " not in cleaned
    assert "\n" not in cleaned or cleaned.count("\n") < raw.count("\n")
    normalized_expected = expected.replace(" ", "").replace("\n", "")
    normalized_cleaned = cleaned.replace(" ", "").replace("\n", "")
    assert normalized_expected in normalized_cleaned


@pytest.mark.parametrize(
    "raw",
    [
        "!!! Hello ###",
        "   Leading and trailing spaces   ",
        "\n\nMultiple\n\nLines\n\n",
    ],
)
def test_cleaning_edge_cases(raw: str) -> None:
    cleaned = clean_text(raw)

    assert cleaned is not None
    assert cleaned.strip() == cleaned
    assert len(cleaned) > 0


# --------------------------------------------------
# 3. CHUNKING TESTS
# --------------------------------------------------

@pytest.mark.parametrize("length", [800, 1200, 2000])
def test_chunking_basic(length: int) -> None:
    text = "word " * length

    chunks = chunk_text(text, chunk_size_words=200, overlap_words=50)

    assert isinstance(chunks, list)
    assert len(chunks) > 1

    for chunk in chunks:
        assert 100 <= len(chunk.split()) <= 300


@pytest.mark.parametrize("length", [1000, 1500])
def test_chunking_overlap(length: int) -> None:
    text = "word " * length

    chunks = chunk_text(text, chunk_size_words=200, overlap_words=50)

    for i in range(len(chunks) - 1):
        overlap_words = set(chunks[i].split()) & set(chunks[i + 1].split())
        assert len(overlap_words) > 0


# --------------------------------------------------
# 4. PIPELINE TEST (END-TO-END)
# --------------------------------------------------

@pytest.mark.parametrize(
    "content",
    [
        "This is a simple document about AI and machine learning.",
        "Air traffic control ensures aircraft safety and efficiency.",
    ],
)
def test_full_pipeline(content: str) -> None:
    extracted = _extract_from_text(content)
    cleaned = clean_text(extracted)
    chunks = chunk_text(cleaned, chunk_size_words=100, overlap_words=20)

    assert extracted is not None
    assert cleaned is not None
    assert isinstance(chunks, list)
    assert len(chunks) >= 1

    for chunk in chunks:
        assert len(chunk.strip()) > 0


# --------------------------------------------------
# 5. EDGE CASE TESTS
# --------------------------------------------------


def test_empty_file() -> None:
    extracted = _extract_from_text("")
    cleaned = clean_text(extracted)
    chunks = chunk_text(cleaned, chunk_size_words=100, overlap_words=20)

    assert extracted == "" or extracted is not None
    assert cleaned == "" or cleaned is not None
    assert isinstance(chunks, list)


@pytest.mark.parametrize(
    "content",
    [
        "U.S. is a country. Dr. Smith works there.",
        "Apple Inc. is a company.",
        "e.g. this should not break.",
    ],
)
def test_special_formatting(content: str) -> None:
    cleaned = clean_text(content)
    chunks = chunk_text(cleaned, chunk_size_words=50, overlap_words=10)

    assert len(chunks) >= 1
    assert any("U.S." in chunk or "Inc." in chunk or "e.g." in chunk for chunk in chunks)


@pytest.mark.parametrize(
    "content",
    [
        "你好，这是中文文本。",
        "Texto en español con acentos áéíóú",
        "Mixed English 中文 Español",
    ],
)
def test_multilingual(content: str) -> None:
    cleaned = clean_text(content)
    chunks = chunk_text(cleaned, chunk_size_words=50, overlap_words=10)

    assert len(chunks) >= 1
    assert any(len(chunk) > 0 for chunk in chunks)


@pytest.mark.parametrize("length", [5000, 10000])
def test_large_document(length: int) -> None:
    text = "data " * length

    cleaned = clean_text(text)
    chunks = chunk_text(cleaned, chunk_size_words=300, overlap_words=50)

    assert len(chunks) > 5
