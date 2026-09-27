from pydantic import BaseModel, Field
from typing import Any

class ICD(BaseModel):
    authenticity: float = Field(ge=0, le=1)
    completeness: float = Field(ge=0, le=1)
    consensus: float = Field(ge=0, le=1)
    weight_authenticity: float = 1/3
    weight_completeness: float = 1/3
    weight_consensus: float = 1/3

    @property
    def value(self) -> float:
        return (
            self.authenticity * self.weight_authenticity
            + self.completeness * self.weight_completeness
            + self.consensus * self.weight_consensus
        )


class UDV(BaseModel):
    id: str
    content: str
    source_doc: str
    source_type: str
    icd: float
    metadata: dict[str, Any] = Field(default_factory=dict)
