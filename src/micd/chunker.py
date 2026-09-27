from __future__ import annotations

import re


def chunk_document(text: str, max_chars: int = 1200) -> list[str]:
    """
    Deterministic semantic/propositional chunking for Sprint 1.

    Strategy:
    1. Normalize whitespace.
    2. Preserve paragraph boundaries.
    3. Split oversized paragraphs at sentence boundaries.
    4. Combine short adjacent sentences until max_chars is reached.

    This is intentionally deterministic and corpus-agnostic.
    """

    if not text or not text.strip():
        return []

    paragraphs = [
        re.sub(r"\s+", " ", paragraph).strip()
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
    ]

    chunks: list[str] = []

    for paragraph in paragraphs:
        if len(paragraph) <= max_chars:
            chunks.append(paragraph)
            continue

        sentences = re.split(r"(?<=[.!?])\s+", paragraph)
        current = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            candidate = f"{current} {sentence}".strip()

            if current and len(candidate) > max_chars:
                chunks.append(current)
                current = sentence
            else:
                current = candidate

        if current:
            chunks.append(current)

    return chunks
