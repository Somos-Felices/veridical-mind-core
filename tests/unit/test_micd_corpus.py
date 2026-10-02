import pytest

from src.micd.corpus import (
    CorpusManifest,
    CorpusSource,
    SourceAssessment,
    SourceGovernance,
)


def governance():
    assessment = SourceAssessment(
        value=0.8,
        justification="test basis",
        uncertainty="test uncertainty",
    )

    return SourceGovernance(
        authenticity=assessment,
        completeness=assessment,
        consensus=assessment,
    )


def source(
    document_id="doc-001",
    version="v1",
    approved=False,
    with_governance=False,
):
    return CorpusSource(
        document_id=document_id,
        source_version=version,
        title="Test source",
        source_type="historical_document",
        representation_type="original",
        approved=approved,
        governance=governance() if with_governance else None,
    )


def test_manifest_accepts_unapproved_source_without_governance():
    manifest = CorpusManifest(
        corpus_id="isidora-goyenechea",
        corpus_version="v1",
        description="Test corpus",
        sources=[source()],
    )

    manifest.validate()


def test_approved_source_requires_governance():
    manifest = CorpusManifest(
        corpus_id="isidora-goyenechea",
        corpus_version="v1",
        description="Test corpus",
        sources=[source(approved=True)],
    )

    with pytest.raises(
        ValueError,
        match="approved source requires source governance",
    ):
        manifest.validate()


def test_approved_source_requires_all_assessment_values():
    incomplete_governance = SourceGovernance(
        authenticity=SourceAssessment(value=0.8),
        completeness=SourceAssessment(value=None),
        consensus=SourceAssessment(value=0.8),
    )

    manifest = CorpusManifest(
        corpus_id="isidora-goyenechea",
        corpus_version="v1",
        description="Test corpus",
        sources=[
            CorpusSource(
                document_id="doc-001",
                source_version="v1",
                title="Test source",
                source_type="historical_document",
                approved=True,
                governance=incomplete_governance,
            )
        ],
    )

    with pytest.raises(
        ValueError,
        match="approved source requires completeness assessment value",
    ):
        manifest.validate()


def test_approved_source_with_governance_is_valid():
    manifest = CorpusManifest(
        corpus_id="isidora-goyenechea",
        corpus_version="v1",
        description="Test corpus",
        sources=[source(approved=True, with_governance=True)],
    )

    manifest.validate()


def test_duplicate_document_version_is_rejected():
    manifest = CorpusManifest(
        corpus_id="isidora-goyenechea",
        corpus_version="v1",
        description="Test corpus",
        sources=[source(), source()],
    )

    with pytest.raises(
        ValueError,
        match="duplicate document_id/source_version identity",
    ):
        manifest.validate()
