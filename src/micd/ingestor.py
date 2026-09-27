from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import NAMESPACE_URL, uuid5

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from src.micd.chunker import chunk_document
from src.micd.models import DocumentVersion, ICD, UDV


@dataclass(frozen=True)
class IngestionResult:
    document_id: str
    source_version: str
    icd: float
    ingestion_timestamp: str
    udvs: list[UDV]


class DocumentIngestor:
    """
    MICD Sprint 1 ingestion component.

    Source document/version
        ↓
    human-assigned ICD
        ↓
    semantic/propositional chunks
        ↓
    UDV + immutable provenance
        ↓
    embedding
        ↓
    Qdrant
    """

    def __init__(
        self,
        qdrant_client: QdrantClient,
        collection_name: str,
        embedding_provider,
    ):
        self.qdrant = qdrant_client
        self.collection_name = collection_name
        self.embedding_provider = embedding_provider

    def ingest(
        self,
        *,
        document_id: str,
        source_version: str,
        content: str,
        source_type: str,
        icd: ICD,
        metadata: dict | None = None,
    ) -> IngestionResult:

        if not document_id.strip():
            raise ValueError("document_id must not be empty")

        if not source_version.strip():
            raise ValueError("source_version must not be empty")

        if not content.strip():
            raise ValueError("content must not be empty")

        chunks = chunk_document(content)

        if not chunks:
            raise ValueError("document produced no UDV chunks")

        ingestion_timestamp = datetime.now(timezone.utc).isoformat()
        base_metadata = dict(metadata or {})
        icd_value = icd.value

        document_version = DocumentVersion(
            document_id=document_id,
            source_version=source_version,
            source_type=source_type,
            icd=icd_value,
            icd_authenticity=icd.authenticity,
            icd_completeness=icd.completeness,
            icd_consensus=icd.consensus,
            ingestion_timestamp=ingestion_timestamp,
            metadata=base_metadata,
        )

        udvs: list[UDV] = []
        points: list[PointStruct] = []

        for index, chunk in enumerate(chunks):
            udv_id = f"{document_id}:{source_version}:{index}"

            vector = self.embedding_provider.embed(chunk)

            udv_metadata = {
                **document_version.metadata,
                "document_id": document_version.document_id,
                "source_version": document_version.source_version,
                "chunk_index": index,
                "icd_authenticity": document_version.icd_authenticity,
                "icd_completeness": document_version.icd_completeness,
                "icd_consensus": document_version.icd_consensus,
            }

            udv = UDV(
                id=udv_id,
                content=chunk,
                vector=vector,
                source_doc=document_id,
                source_type=source_type,
                icd=icd_value,
                ingestion_timestamp=ingestion_timestamp,
                metadata=udv_metadata,
            )

            point_id = str(uuid5(NAMESPACE_URL, udv_id))

            points.append(
                PointStruct(
                    id=point_id,
                    vector=udv.vector,
                    payload={
                        "udv_id": udv.id,
                        "content": udv.content,
                        "source_doc": udv.source_doc,
                        "source_type": udv.source_type,
                        "icd": udv.icd,
                        "ingestion_timestamp": udv.ingestion_timestamp,
                        "metadata": udv.metadata,
                    },
                )
            )

            udvs.append(udv)

        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )

        return IngestionResult(
            document_id=document_id,
            source_version=source_version,
            icd=icd_value,
            ingestion_timestamp=ingestion_timestamp,
            udvs=udvs,
        )
