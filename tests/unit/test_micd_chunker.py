from src.micd.chunker import chunk_document


def test_empty_document_returns_no_chunks():
    assert chunk_document("") == []


def test_paragraphs_are_preserved_as_chunks():
    text = "First historical paragraph.\n\nSecond historical paragraph."
    chunks = chunk_document(text)

    assert chunks == [
        "First historical paragraph.",
        "Second historical paragraph.",
    ]


def test_oversized_paragraph_is_split():
    text = (
        "Sentence one contains historical information. "
        "Sentence two contains additional historical information. "
        "Sentence three contains more historical information."
    )

    chunks = chunk_document(text, max_chars=70)

    assert len(chunks) > 1
    assert all(chunk for chunk in chunks)
    assert all(len(chunk) <= 100 for chunk in chunks)


def test_whitespace_is_normalized():
    text = "First   sentence.\nSecond   sentence."
    chunks = chunk_document(text)

    assert chunks == ["First sentence. Second sentence."]
