from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchAny

from src.mrec.ir import RankedUDV, rank_results


@dataclass(frozen=True)
class RetrievalResult:
    query: str
    results: list[RankedUDV]


class QdrantRetriever:
    def __init__(
        self,
        qdrant_client: QdrantClient,
        collection_name: str,
        embedding_provider,
    ):
        self.qdrant = qdrant_client
        self.collection_name = collection_name
        self.embedding_provider = embedding_provider

    def retrieve(
        self,
        query: str,
        *,
        top_k: int = 10,
        source_docs: list[str] | None = None,
    ) -> RetrievalResult:
        if not query.strip():
            raise ValueError("query must not be empty")

        query_vector = self.embedding_provider.embed(query)

        query_filter = None
        if source_docs is not None:
            if not source_docs:
                raise ValueError("source_docs must not be empty when provided")
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="source_doc",
                        match=MatchAny(any=source_docs),
                    )
                ]
            )

        search_results = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
            query_filter=query_filter,
            with_payload=True,
        ).points

        candidates: list[dict[str, Any]] = []

        for point in search_results:
            payload = point.payload or {}

            candidates.append(
                {
                    "id": str(payload.get("udv_id", point.id)),
                    "content": str(payload.get("content", "")),
                    "source_doc": str(payload.get("source_doc", "")),
                    "source_type": str(payload.get("source_type", "")),
                    "icd": float(payload.get("icd", 0.0)),
                    "similarity": float(point.score),
                    "metadata": dict(payload.get("metadata", {})),
                }
            )

        ranked = rank_results(candidates, top_k=top_k)

        return RetrievalResult(
            query=query,
            results=ranked,
        )
