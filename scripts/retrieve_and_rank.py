from dataclasses import asdict

from qdrant_client import QdrantClient

from src.mrec.embeddings import LocalEmbeddingProvider
from src.mrec.ir import rank_results


COLLECTION = "veridical_udv"


def retrieve_and_rank(query: str, top_k: int = 10):
    client = QdrantClient(url="http://localhost:6333")
    embedder = LocalEmbeddingProvider()

    query_vector = embedder.embed(query)

    results = client.query_points(
        collection_name=COLLECTION,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    ).points

    candidates = []

    for result in results:
        payload = result.payload

        candidates.append(
            {
                "id": payload["id"],
                "content": payload["content"],
                "source_doc": payload["source_doc"],
                "source_type": payload["source_type"],
                "icd": float(payload["icd"]),
                "similarity": float(result.score),
                "metadata": {
                    key: value
                    for key, value in payload.items()
                    if key not in {
                        "id",
                        "content",
                        "source_doc",
                        "source_type",
                        "icd",
                    }
                },
            }
        )

    ranked = rank_results(candidates, top_k=top_k)

    return ranked


if __name__ == "__main__":
    query = "Who was Isidora Goyenechea?"

    ranked = retrieve_and_rank(query)

    print("\nIR-ranked evidence:")

    for item in ranked:
        print(
            f"id={item.id} | "
            f"similarity={item.similarity:.4f} | "
            f"ICD={item.icd:.4f} | "
            f"IR={item.ir:.4f}"
        )

    print("\nQdrant ? IR pipeline: OK")
