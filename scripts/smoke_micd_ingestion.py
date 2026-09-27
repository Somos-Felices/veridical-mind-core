from __future__ import annotations

import os

from qdrant_client import QdrantClient

from src.micd.ingestor import DocumentIngestor
from src.micd.models import ICD
from src.mrec.embeddings import LocalEmbeddingProvider


COLLECTION = os.getenv("QDRANT_COLLECTION", "veridical_udv")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")


def main():
    client = QdrantClient(url=QDRANT_URL)

    embedding_provider = LocalEmbeddingProvider()

    ingestor = DocumentIngestor(
        qdrant_client=client,
        collection_name=COLLECTION,
        embedding_provider=embedding_provider,
    )

    icd = ICD(
        authenticity=0.95,
        completeness=0.90,
        consensus=0.85,
    )

    result = ingestor.ingest(
        document_id="micd-smoke-001",
        source_version="v1",
        content=(
            "Isidora Goyenechea was a Chilean industrialist and philanthropist. "
            "This synthetic smoke-test document is not part of the protected corpus.\n\n"
            "The purpose of this document is to verify MICD ingestion, UDV creation, "
            "embedding generation, ICD propagation, and Qdrant persistence."
        ),
        source_type="synthetic_test",
        icd=icd,
        metadata={"test": True},
    )

    print("MICD ingestion successful")
    print(f"document_id={result.document_id}")
    print(f"source_version={result.source_version}")
    print(f"icd={result.icd:.6f}")
    print(f"udv_count={len(result.udvs)}")

    for udv in result.udvs:
        print(
            f"UDV={udv.id} | "
            f"ICD={udv.icd:.6f} | "
            f"chars={len(udv.content)}"
        )


if __name__ == "__main__":
    main()
