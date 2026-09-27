from src.micd.ingestor import DocumentIngestor
from src.micd.models import ICD


class FakeEmbeddingProvider:
    def embed(self, text: str) -> list[float]:
        return [float(len(text)), 1.0, 2.0]


class FakeQdrant:
    def __init__(self):
        self.calls = []

    def upsert(self, *, collection_name, points, wait):
        self.calls.append(
            {
                "collection_name": collection_name,
                "points": points,
                "wait": wait,
            }
        )


def test_ingestion_propagates_single_icd_to_all_udvs():
    qdrant = FakeQdrant()

    ingestor = DocumentIngestor(
        qdrant_client=qdrant,
        collection_name="veridical_udv",
        embedding_provider=FakeEmbeddingProvider(),
    )

    icd = ICD(
        authenticity=0.9,
        completeness=0.8,
        consensus=0.7,
    )

    result = ingestor.ingest(
        document_id="doc-001",
        source_version="v1",
        content=(
            "This is the first historical proposition. "
            "It contains documentary information.\n\n"
            "This is a second historical proposition."
        ),
        source_type="historical_document",
        icd=icd,
        metadata={"origin": "synthetic-test"},
    )

    assert result.document_id == "doc-001"
    assert result.source_version == "v1"
    assert result.icd == icd.value
    assert len(result.udvs) == 2

    assert all(udv.icd == icd.value for udv in result.udvs)
    assert all(udv.source_doc == "doc-001" for udv in result.udvs)
    assert all(udv.metadata["source_version"] == "v1" for udv in result.udvs)

    assert len(qdrant.calls) == 1
    assert len(qdrant.calls[0]["points"]) == 2


def test_new_document_version_has_independent_ingestion_identity():
    qdrant = FakeQdrant()

    ingestor = DocumentIngestor(
        qdrant_client=qdrant,
        collection_name="veridical_udv",
        embedding_provider=FakeEmbeddingProvider(),
    )

    icd_v1 = ICD(
        authenticity=1.0,
        completeness=1.0,
        consensus=1.0,
    )

    icd_v2 = ICD(
        authenticity=0.5,
        completeness=0.5,
        consensus=0.5,
    )

    result_v1 = ingestor.ingest(
        document_id="doc-002",
        source_version="v1",
        content="Original source statement.",
        source_type="historical_document",
        icd=icd_v1,
    )

    result_v2 = ingestor.ingest(
        document_id="doc-002",
        source_version="v2",
        content="Updated source statement.",
        source_type="historical_document",
        icd=icd_v2,
    )

    assert result_v1.udvs[0].id != result_v2.udvs[0].id
    assert result_v1.icd != result_v2.icd
    assert result_v1.udvs[0].icd == icd_v1.value
    assert result_v2.udvs[0].icd == icd_v2.value
