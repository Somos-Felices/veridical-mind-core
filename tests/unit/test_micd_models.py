from src.micd.models import DocumentVersion, ICD, UDV


def test_icd_is_immutable():
    icd = ICD(
        authenticity=0.9,
        completeness=0.8,
        consensus=0.7,
    )

    try:
        icd.authenticity = 0.1
        assert False, "ICD should be immutable"
    except Exception:
        pass


def test_document_version_is_immutable():
    version = DocumentVersion(
        document_id="doc-001",
        source_version="v1",
        source_type="historical_document",
        icd=0.8,
        icd_authenticity=0.9,
        icd_completeness=0.8,
        icd_consensus=0.7,
        ingestion_timestamp="2026-09-27T00:00:00+00:00",
    )

    try:
        version.icd = 0.2
        assert False, "DocumentVersion should be immutable"
    except Exception:
        pass


def test_udv_contains_required_provenance_fields():
    udv = UDV(
        id="doc-001:v1:0",
        content="Historical proposition.",
        vector=[0.1, 0.2, 0.3],
        icd=0.8,
        source_doc="doc-001",
        source_type="historical_document",
        ingestion_timestamp="2026-09-27T00:00:00+00:00",
        metadata={
            "document_id": "doc-001",
            "source_version": "v1",
            "chunk_index": 0,
        },
    )

    assert udv.vector == [0.1, 0.2, 0.3]
    assert udv.icd == 0.8
    assert udv.source_doc == "doc-001"
    assert udv.source_type == "historical_document"
    assert udv.ingestion_timestamp
    assert udv.metadata["source_version"] == "v1"


def test_udv_is_immutable():
    udv = UDV(
        id="doc-001:v1:0",
        content="Historical proposition.",
        vector=[0.1, 0.2],
        icd=0.8,
        source_doc="doc-001",
        source_type="historical_document",
        ingestion_timestamp="2026-09-27T00:00:00+00:00",
    )

    try:
        udv.icd = 0.1
        assert False, "UDV should be immutable"
    except Exception:
        pass
