from __future__ import annotations

from dataclasses import dataclass

from src.mcg.gateway import GenerationGateway
from src.mrec.embeddings import LocalEmbeddingProvider
from src.mrec.retriever import QdrantRetriever
from src.mrm.logger import MRMLogger
from qdrant_client import QdrantClient


@dataclass
class RecordingLLM:
    calls: int = 0

    def generate(self, prompt: str, *, temperature: float = 0.0) -> str:
        self.calls += 1
        return "validation response"


PUBLIC_DOCS = [f"public-isidora-{i:03d}" for i in range(1, 9)]

QUERIES = [
    "What was Isidora Goyenechea role in Lota?",
    "What did Isidora Goyenechea do with Parque de Lota?",
    "Who designed Palacio Cousino?",
    "When was Palacio Cousino constructed?",
    "What features did Parque de Lota have?",
    "When was Parque de Lota declared a Historic Monument?",
]


def main() -> None:
    embeddings = LocalEmbeddingProvider()
    qdrant = QdrantClient("http://127.0.0.1:6333")
    retriever = QdrantRetriever(qdrant, "veridical_udv", embeddings)

    llm = RecordingLLM()
    mrm = MRMLogger()

    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=mrm,
        theta_a=0.80,
        theta_b=0.30,
        top_k=10,
    )

    print("=== PUBLIC FILTERED VALIDATION ===")

    for query in QUERIES:
        result = retriever.retrieve(
            query,
            top_k=10,
            source_docs=PUBLIC_DOCS,
        )

        response = gateway.handle(
            query=query,
            query_vector=embeddings.embed(query),
            ranked_udvs=result.results,
            prompt=query,
        )

        print(f"\nQUERY: {query}")
        print(f"TOP_K_RETURNED: {len(result.results)}")

        for i, item in enumerate(result.results[:5], 1):
            print(
                f"{i}. {item.source_doc} | {item.id} | "
                f"IR={item.ir:.6f}"
            )

        print(
            f"MCG={response.category} | "
            f"llm_invoked={response.llm_invoked} | "
            f"ICR={response.icr}"
        )

    print("\n=== SUMMARY ===")

    for trace in mrm.records:
        print(
            f"{trace.category} | "
            f"llm={trace.llm_invoked} | "
            f"max={trace.ir_max:.6f} | "
            f"avg={trace.ir_avg:.6f} | "
            f"icr={trace.icr}"
        )

    print(f"LLM_CALLS={llm.calls}")


if __name__ == "__main__":
    main()
