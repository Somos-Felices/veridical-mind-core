from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from src.micd.ingestor import DocumentIngestor
from src.micd.models import ICD
from src.mrec.retriever import QdrantRetriever


class FakeEmbeddingProvider:
    dimension = 3

    def embed(self, text: str) -> list[float]:
        text_lower = text.lower()

        if "isidora" in text_lower or "goyenechea" in text_lower:
            return [1.0, 0.0, 0.0]

        return [0.0, 1.0, 0.0]


def main():
    collection = "micd_retrieval_integration"

    client = QdrantClient("http://localhost:6333")

    if client.collection_exists(collection):
        client.delete_collection(collection)

    client.create_collection(
        collection_name=collection,
        vectors_config=VectorParams(
            size=3,
            distance=Distance.COSINE,
        ),
    )

    embeddings = FakeEmbeddingProvider()

    ingestor = DocumentIngestor(
        qdrant_client=client,
        collection_name=collection,
        embedding_provider=embeddings,
    )

    result = ingestor.ingest(
        document_id="isidora-integration-001",
        source_version="v1",
        content=(
            "Isidora Goyenechea was an important historical figure "
            "associated with documentary evidence.\n\n"
            "This second proposition provides additional historical context."
        ),
        source_type="historical_document",
        icd=ICD(
            authenticity=0.95,
            completeness=0.90,
            consensus=0.85,
        ),
        metadata={
            "integration_test": True,
            "catalogue_reference": "TEST-001",
        },
    )

    assert len(result.udvs) == 2
    assert result.source_version == "v1"
    assert result.icd > 0.0

    print("=== MICD INGESTION ===")
    print(f"document_id={result.document_id}")
    print(f"source_version={result.source_version}")
    print(f"icd={result.icd:.6f}")
    print(f"udv_count={len(result.udvs)}")

    for udv in result.udvs:
        assert udv.vector
        assert udv.icd == result.icd
        assert udv.source_doc == result.document_id
        assert udv.metadata["source_version"] == "v1"
        assert udv.metadata["document_id"] == result.document_id

    print("UDV provenance: OK")

    retriever = QdrantRetriever(
        qdrant_client=client,
        collection_name=collection,
        embedding_provider=embeddings,
    )

    retrieval = retriever.retrieve(
        "What documentary information is available about Isidora Goyenechea?"
    )

    assert retrieval.results
    assert retrieval.results[0].id.startswith(
        "isidora-integration-001:v1:"
    )

    first = retrieval.results[0]

    assert first.icd == result.icd
    assert first.ir >= 0.0
    assert first.similarity >= 0.0
    assert first.metadata["source_version"] == "v1"
    assert first.metadata["document_id"] == result.document_id

    print()
    print("=== RETRIEVAL → IR ===")
    print(f"UDV={first.id}")
    print(f"similarity={first.similarity:.6f}")
    print(f"ICD={first.icd:.6f}")
    print(f"IR={first.ir:.6f}")
    print(f"source_version={first.metadata['source_version']}")

    # Verify the original source-version payload still exists in Qdrant.
    points = client.scroll(
        collection_name=collection,
        limit=10,
        with_payload=True,
        with_vectors=False,
    )[0]

    assert points

    for point in points:
        payload = point.payload

        assert payload["source_doc"] == result.document_id
        assert payload["icd"] == result.icd
        assert payload["ingestion_timestamp"] == result.ingestion_timestamp
        assert payload["metadata"]["source_version"] == "v1"
        assert payload["metadata"]["document_id"] == result.document_id

    print()
    print("=== QDRANT PROVENANCE ===")
    print(f"stored_points={len(points)}")
    print("ICD preserved: OK")
    print("source version preserved: OK")
    print("ingestion timestamp preserved: OK")
    print("metadata preserved: OK")

    # Create a second source version.
    result_v2 = ingestor.ingest(
        document_id="isidora-integration-001",
        source_version="v2",
        content=(
            "Isidora Goyenechea documentary record, revised source version."
        ),
        source_type="historical_document",
        icd=ICD(
            authenticity=0.70,
            completeness=0.70,
            consensus=0.70,
        ),
        metadata={
            "integration_test": True,
            "catalogue_reference": "TEST-001",
        },
    )

    assert result_v2.source_version == "v2"
    assert result_v2.icd != result.icd
    assert result_v2.udvs[0].id != result.udvs[0].id

    points_after_v2 = client.scroll(
        collection_name=collection,
        limit=20,
        with_payload=True,
        with_vectors=False,
    )[0]

    versions = {
        point.payload["metadata"]["source_version"]
        for point in points_after_v2
    }

    assert "v1" in versions
    assert "v2" in versions

    print()
    print("=== VERSION IMMUTABILITY ===")
    print(f"versions_present={sorted(versions)}")
    print(f"v1_icd={result.icd:.6f}")
    print(f"v2_icd={result_v2.icd:.6f}")
    print("Historical v1 preserved: OK")
    print("New v2 created: OK")

    client.delete_collection(collection)

    print()
    print("==============================================")
    print("MICD → QDRANT → RETRIEVAL → IR VALIDATION OK")
    print("VERSION IMMUTABILITY VALIDATION OK")
    print("==============================================")


if __name__ == "__main__":
    main()
