from __future__ import annotations

from dataclasses import dataclass
import re

from src.mrec.ir import RankedUDV


STOPWORDS = {
    "what", "was", "were", "is", "are", "the", "a", "an",
    "who", "whom", "which", "when", "where", "why", "how",
    "did", "does", "do", "have", "has", "had",
    "with", "for", "from", "about", "into", "during",
    "and", "or", "of", "to", "in", "on", "at", "by",
    "her", "his", "their", "its", "this", "that",
    "private", "favorite", "favourite",
}

ENTITY_TERMS = {
    "isidora",
    "goyenechea",
    "cousino",
    "cousiño",
}


@dataclass(frozen=True)
class AnswerabilityDecision:
    sufficient: bool
    matched_terms: tuple[str, ...]
    query_terms: tuple[str, ...]
    coverage: float


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-ZÀ-ÿ]+", text.lower()))


def assess_answerability(
    query: str,
    ranked_udvs: list[RankedUDV],
    *,
    evidence_k: int = 5,
    min_matched_terms: int = 1,
) -> AnswerabilityDecision:

    query_tokens = _tokens(query)

    substantive = {
        token
        for token in query_tokens
        if token not in STOPWORDS
        and token not in ENTITY_TERMS
        and len(token) >= 3
    }

    evidence_text = " ".join(
        item.content for item in ranked_udvs[:evidence_k]
    )

    evidence_tokens = _tokens(evidence_text)

    matched = sorted(
        substantive.intersection(evidence_tokens)
    )

    coverage = (
        len(matched) / len(substantive)
        if substantive
        else 0.0
    )

    return AnswerabilityDecision(
        sufficient=len(matched) >= min_matched_terms,
        matched_terms=tuple(matched),
        query_terms=tuple(sorted(substantive)),
        coverage=coverage,
    )
