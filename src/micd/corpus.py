from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SourceAssessment(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: float | None = Field(default=None, ge=0, le=1)
    justification: str | None = None
    uncertainty: str | None = None


class SourceGovernance(BaseModel):
    model_config = ConfigDict(frozen=True)

    authenticity: SourceAssessment
    completeness: SourceAssessment
    consensus: SourceAssessment


class CorpusSource(BaseModel):
    model_config = ConfigDict(frozen=True)

    document_id: str
    source_version: str
    title: str
    author: str | None = None
    date_or_date_range: str | None = None
    source_type: str
    archive_or_repository: str | None = None
    catalogue_reference_id: str | None = None
    language: str | None = None
    representation_type: Literal[
        "original",
        "transcription",
        "translation",
        "later_edition",
        "unknown",
    ] = "unknown"
    edition_history: list[str] = Field(default_factory=list)
    source_relationships: list[str] = Field(default_factory=list)
    provenance: str | None = None
    completeness_notes: str | None = None
    governance: SourceGovernance | None = None
    approved: bool = False


class CorpusManifest(BaseModel):
    model_config = ConfigDict(frozen=True)

    corpus_id: str
    corpus_version: str
    description: str
    sources: list[CorpusSource]

    def validate_unique_identity(self) -> None:
        identities = [
            (source.document_id, source.source_version)
            for source in self.sources
        ]

        if len(identities) != len(set(identities)):
            raise ValueError(
                "duplicate document_id/source_version identity in corpus manifest"
            )

    def validate_approved_sources(self) -> None:
        for source in self.sources:
            if not source.approved:
                continue

            if source.governance is None:
                raise ValueError(
                    f"approved source requires source governance data: "
                    f"{source.document_id}:{source.source_version}"
                )

            assessments = {
                "authenticity": source.governance.authenticity,
                "completeness": source.governance.completeness,
                "consensus": source.governance.consensus,
            }

            for name, assessment in assessments.items():
                if assessment.value is None:
                    raise ValueError(
                        f"approved source requires {name} assessment value: "
                        f"{source.document_id}:{source.source_version}"
                    )

    def validate(self) -> None:
        self.validate_unique_identity()
        self.validate_approved_sources()
