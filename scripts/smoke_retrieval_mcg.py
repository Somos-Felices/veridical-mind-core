from __future__ import annotations

import os

from qdrant_client import QdrantClient

from src.mcg.classifier import classify
from src.mrec.embeddings import LocalEmbeddingProvider
from src.mrec.retriever import QdrantRetriever


COLLECTION = os.getenv("QDRANT_COLLECTION", "veridical_udv")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

# Development thresholds only.
# Final thresholds are to be validated with Cristian's approved test queries.
THETA_A = 0.70
THETA_B = 0.25


def main():
    client = QdrantClient(url=QDRANT_URL)
    embeddings = LocalEmbeddingProvider()

    retriever = QdrantRetriever(
        qdrant_client=client,
        collection_name=COLLECTION,
        embedding_provider=embeddings,
    )

    query = "What documentary information is available about Isidora Goyenechea?"

    retrieval = retriever.retrieve(query, top_k=10)

    ir_values = [result.ir for result in retrieval.results]

    decision = classify(
        ir_values,
        theta_a=THETA_A,
        theta_b=THETA_B,
        top_k=10,
    )

    print("\n=== REAL RETRIEVAL → IR → MCG SMOKE TEST ===")
    print(f"query: {query}")
    print(f"retrieved: {len(retrieval.results)}")

    for index, result in enumerate(retrieval.results, start=1):
        print(
            f"{index:02d}. "
            f"UDV={result.id} | "
            f"similarity={result.similarity:.6f} | "
            f"ICD={result.icd:.6f} | "
            f"IR={result.ir:.6f}"
        )

    print("\n=== MCG ===")
    print(f"category={decision.category}")
    print(f"ir_max={decision.ir_max:.6f}")
    print(f"ir_avg={decision.ir_avg:.6f}")
    print(f"icr={decision.icr}")
    print(f"llm_allowed={decision.llm_allowed}")


if __name__ == "__main__":
    main()
