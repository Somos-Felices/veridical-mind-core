from dataclasses import dataclass

@dataclass
class RankedUDV:
    id: str
    content: str
    source_doc: str
    source_type: str
    icd: float
    similarity: float
    ir: float
    metadata: dict

def calculate_ir(icd: float, similarity: float) -> float:
    return icd * similarity

def rank_results(results: list[dict], top_k: int = 10) -> list[RankedUDV]:
    ranked = []

    for r in results:
        ir = calculate_ir(r["icd"], r["similarity"])
        ranked.append(
            RankedUDV(
                id=r["id"],
                content=r["content"],
                source_doc=r["source_doc"],
                source_type=r["source_type"],
                icd=r["icd"],
                similarity=r["similarity"],
                ir=ir,
                metadata=r.get("metadata", {}),
            )
        )

    return sorted(ranked, key=lambda x: x.ir, reverse=True)[:top_k]
