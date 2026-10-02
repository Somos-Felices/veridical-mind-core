from pathlib import Path
from tempfile import TemporaryDirectory

from src.micd.corpus import (
    CorpusManifest,
    CorpusSource,
    SourceAssessment,
    SourceGovernance,
)
from src.micd.corpus_ingestor import CorpusIngestor
from src.micd.models import ICD


def test_manifest_validation():
    source = CorpusSource(
        document_id="TEST-001",
        source_version="v1",
        title="Test Source",
        source_type="historical_document",
        governance=SourceGovernance(
            authenticity=SourceAssessment(value=0.9),
            completeness=SourceAssessment(value=0.8),
            consensus=SourceAssessment(value=0.7),
        ),
        approved=True,
    )

    manifest = CorpusManifest(
        corpus_id="test-corpus",
        corpus_version="v1",
        description="Synthetic validation corpus",
        sources=[source],
    )

    manifest.validate()

    assert source.governance is not None

    icd = ICD(
        authenticity=0.9,
        completeness=0.8,
        consensus=0.7,
    )

    assert abs(icd.value - 0.8) < 1e-9


def test_metadata_mapping():
    source = CorpusSource(
        document_id="TEST-002",
        source_version="v3",
        title="Historical Test",
        author="Test Author",
        date_or_date_range="1900",
        source_type="archive",
        archive_or_repository="Test Archive",
        catalogue_reference_id="CAT-002",
        language="es",
        representation_type="transcription",
        edition_history=["v1", "v2", "v3"],
        source_relationships=["TEST-001"],
        provenance="Synthetic provenance",
        completeness_notes="Synthetic completeness note",
        governance=SourceGovernance(
            authenticity=SourceAssessment(value=1.0),
            completeness=SourceAssessment(value=0.9),
            consensus=SourceAssessment(value=0.8),
        ),
        approved=True,
    )

    metadata = CorpusIngestor._source_metadata(source)

    assert metadata["title"] == "Historical Test"
    assert metadata["author"] == "Test Author"
    assert metadata["language"] == "es"
    assert metadata["representation_type"] == "transcription"
    assert metadata["edition_history"] == ["v1", "v2", "v3"]
    assert metadata["source_relationships"] == ["TEST-001"]
    assert metadata["provenance"] == "Synthetic provenance"


def test_missing_document_fails():
    source = CorpusSource(
        document_id="MISSING",
        source_version="v1",
        title="Missing",
        source_type="archive",
        governance=SourceGovernance(
            authenticity=SourceAssessment(value=1.0),
            completeness=SourceAssessment(value=1.0),
            consensus=SourceAssessment(value=1.0),
        ),
        approved=True,
    )

    manifest = CorpusManifest(
        corpus_id="test-corpus",
        corpus_version="v1",
        description="Synthetic",
        sources=[source],
    )

    runner = CorpusIngestor(
        qdrant_client=None,
        collection_name="unused",
        embedding_provider=None,
    )

    with TemporaryDirectory() as tmp:
        try:
            runner.ingest_manifest(
                manifest=manifest,
                corpus_dir=tmp,
            )
        except FileNotFoundError as exc:
            assert "MISSING:v1" in str(exc)
        else:
            raise AssertionError("missing document must fail")


test_manifest_validation()
test_metadata_mapping()
test_missing_document_fails()

print("Corpus ingestion validation: OK")
