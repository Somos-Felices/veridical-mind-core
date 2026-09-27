from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ICD(BaseModel):
    model_config = ConfigDict(frozen=True)

    authenticity: float = Field(ge=0, le=1)
    completeness: float = Field(ge=0, le=1)
    consensus: float = Field(ge=0, le=1)

    # Development defaults only.
    # Final p_A / p_C / p_K values must come from project alignment.
    weight_authenticity: float = 1 / 3
    weight_completeness: float = 1 / 3
    weight_consensus: float = 1 / 3

    @property
    def value(self) -> float:
        return (
            self.authenticity * self.weight_authenticity
            + self.completeness * self.weight_completeness
            + self.consensus * self.weight_consensus
        )


class DocumentVersion(BaseModel):
    """
    Immutable identity/provenance record for one source-document version.

    A new version must be created whenever the source's A/C/K assessment
    changes. Historical versions are never mutated.
    """

    model_config = ConfigDict(frozen=True)

    document_id: str
    source_version: str
    source_type: str
    icd: float
    icd_authenticity: float = Field(ge=0, le=1)
    icd_completeness: float = Field(ge=0, le=1)
    icd_consensus: float = Field(ge=0, le=1)
    ingestion_timestamp: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class UDV(BaseModel):
    """
    Verifiable Document Unit.

    Every UDV inherits the ICD and provenance of its source-document
    version at ingestion time.
    """

    model_config = ConfigDict(frozen=True)

    id: str
    content: str
    vector: list[float]
    icd: float
    source_doc: str
    source_type: str
    ingestion_timestamp: str
    metadata: dict[str, Any] = Field(default_factory=dict)
