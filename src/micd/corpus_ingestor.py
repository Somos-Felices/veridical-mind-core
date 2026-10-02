from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient

from src.micd.corpus import CorpusManifest
from src.micd.ingestor import DocumentIngestor
from src.micd.models import ICD
from src.mrec.embeddings import LocalEmbeddingProvider


class CorpusIngestor:
    def __init__(
        self,
        *,
        qdrant_client: QdrantClient,
        collection_name: str,
        embedding_provider: Any,
    ) -> None:
        self.ingestor = DocumentIngestor(
            qdrant_client=qdrant_client,
            collection_name=collection_name,
            embedding_provider=embedding_provider,
        )

    @staticmethod
    def load_manifest(path: str | Path) -> CorpusManifest:
        manifest_path = Path(path)

        if not manifest_path.is_file():
            raise FileNotFoundError(
                f"corpus manifest not found: {manifest_path}"
            )

        with manifest_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        manifest = CorpusManifest.model_validate(data)
        manifest.validate()
        return manifest

    @staticmethod
    def _source_metadata(source) -> dict[str, Any]:
        return {
            "corpus_id": None,
            "corpus_version": None,
            "title": source.title,
            "author": source.author,
            "date_or_date_range": source.date_or_date_range,
            "archive_or_repository": source.archive_or_repository,
            "catalogue_reference_id": source.catalogue_reference_id,
            "language": source.language,
            "representation_type": source.representation_type,
            "edition_history": list(source.edition_history),
            "source_relationships": list(source.source_relationships),
            "provenance": source.provenance,
            "completeness_notes": source.completeness_notes,
        }

    def ingest_manifest(
        self,
        *,
        manifest: CorpusManifest,
        corpus_dir: str | Path,
    ) -> list:
        manifest.validate()

        root = Path(corpus_dir)

        if not root.is_dir():
            raise FileNotFoundError(
                f"corpus directory not found: {root}"
            )

        results = []

        for source in manifest.sources:
            document_path = root / f"{source.document_id}.txt"

            if not document_path.is_file():
                raise FileNotFoundError(
                    f"document file not found for "
                    f"{source.document_id}:{source.source_version}: "
                    f"{document_path}"
                )

            if source.governance is None:
                raise ValueError(
                    f"source governance missing: "
                    f"{source.document_id}:{source.source_version}"
                )

            assessments = source.governance

            if any(
                assessment.value is None
                for assessment in (
                    assessments.authenticity,
                    assessments.completeness,
                    assessments.consensus,
                )
            ):
                raise ValueError(
                    f"incomplete A/C/K assessment: "
                    f"{source.document_id}:{source.source_version}"
                )

            icd = ICD(
                authenticity=assessments.authenticity.value,
                completeness=assessments.completeness.value,
                consensus=assessments.consensus.value,
            )

            metadata = self._source_metadata(source)
            metadata["corpus_id"] = manifest.corpus_id
            metadata["corpus_version"] = manifest.corpus_version

            content = document_path.read_text(encoding="utf-8")

            result = self.ingestor.ingest(
                document_id=source.document_id,
                source_version=source.source_version,
                content=content,
                source_type=source.source_type,
                icd=icd,
                metadata=metadata,
            )

            results.append(result)

        return results
