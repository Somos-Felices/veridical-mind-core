from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from src.mrec.embeddings import LocalEmbeddingProvider

COLLECTION = "veridical_udv"

client = QdrantClient(url="http://localhost:6333")
embedder = LocalEmbeddingProvider()

documents = [
    {
        "point_id": 1001,
        "id": "test-001",
        "content": "Isidora Goyenechea was a Chilean businesswoman.",
        "source_doc": "synthetic-source-a",
        "source_type": "test",
        "icd": 0.95,
    },
    {
        "point_id": 1002,
        "id": "test-002",
        "content": "Santiago is the capital city of Chile.",
        "source_doc": "synthetic-source-b",
        "source_type": "test",
        "icd": 0.80,
    },
    {
        "point_id": 1003,
        "id": "test-003",
        "content": "This document contains unrelated information about astronomy.",
        "source_doc": "synthetic-source-c",
        "source_type": "test",
        "icd": 0.40,
    },
]

points = []

for doc in documents:
    vector = embedder.embed(doc["content"])

    points.append(
        PointStruct(
            id=doc["point_id"],
            vector=vector,
            payload={
                "id": doc["id"],
                "content": doc["content"],
                "source_doc": doc["source_doc"],
                "source_type": doc["source_type"],
                "icd": doc["icd"],
            },
        )
    )

client.upsert(
    collection_name=COLLECTION,
    points=points,
)

query = "Who was Isidora Goyenechea?"

query_vector = embedder.embed(query)

results = client.query_points(
    collection_name=COLLECTION,
    query=query_vector,
    limit=10,
    with_payload=True,
).points

print("\nQdrant retrieval:")

for r in results:
    print(
        f"id={r.payload['id']} | "
        f"similarity={r.score:.4f} | "
        f"ICD={r.payload['icd']} | "
        f"source={r.payload['source_doc']}"
    )

print("\nQdrant retrieval: OK")
