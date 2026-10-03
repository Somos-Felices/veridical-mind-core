from src.mrec.retriever import QdrantRetriever


class FakeEmbeddingProvider:
    def embed(self, text: str) -> list[float]:
        return [1.0, 0.0, 0.0]


class FakePoint:
    def __init__(self, point_id, score, payload):
        self.id = point_id
        self.score = score
        self.payload = payload


class FakeQueryResponse:
    def __init__(self, points):
        self.points = points


class FakeQdrant:
    def __init__(self):
        self.last_query_filter = None

    def query_points(
        self,
        *,
        collection_name,
        query,
        limit,
        query_filter=None,
        with_payload,
    ):
        self.last_query_filter = query_filter

        return FakeQueryResponse(
            [
                FakePoint(
                    1,
                    0.8,
                    {
                        "udv_id": "doc-001:v1:0",
                        "content": "Highly relevant evidence.",
                        "source_doc": "doc-001",
                        "source_type": "historical_document",
                        "icd": 0.9,
                        "metadata": {"source_version": "v1"},
                    },
                ),
                FakePoint(
                    2,
                    0.6,
                    {
                        "udv_id": "doc-002:v1:0",
                        "content": "Moderately relevant evidence.",
                        "source_doc": "doc-002",
                        "source_type": "historical_document",
                        "icd": 0.5,
                        "metadata": {"source_version": "v1"},
                    },
                ),
            ][:limit]
        )


def test_qdrant_retriever_reconstructs_udvs_and_applies_ir():
    retriever = QdrantRetriever(
        qdrant_client=FakeQdrant(),
        collection_name="veridical_udv",
        embedding_provider=FakeEmbeddingProvider(),
    )

    result = retriever.retrieve("historical query")

    assert len(result.results) == 2
    assert result.results[0].id == "doc-001:v1:0"
    assert abs(result.results[0].ir - 0.72) < 1e-9
    assert result.results[1].id == "doc-002:v1:0"
    assert abs(result.results[1].ir - 0.30) < 1e-9


def test_empty_query_is_rejected():
    retriever = QdrantRetriever(
        qdrant_client=FakeQdrant(),
        collection_name="veridical_udv",
        embedding_provider=FakeEmbeddingProvider(),
    )

    try:
        retriever.retrieve("   ")
        assert False
    except ValueError as exc:
        assert "query" in str(exc)


def test_retriever_respects_custom_top_k():
    retriever = QdrantRetriever(
        qdrant_client=FakeQdrant(),
        collection_name="veridical_udv",
        embedding_provider=FakeEmbeddingProvider(),
    )

    result = retriever.retrieve("historical query", top_k=1)

    assert len(result.results) == 1
    assert result.results[0].id == "doc-001:v1:0"


def test_retriever_builds_source_filter():
    qdrant = FakeQdrant()

    retriever = QdrantRetriever(
        qdrant_client=qdrant,
        collection_name="veridical_udv",
        embedding_provider=FakeEmbeddingProvider(),
    )

    retriever.retrieve(
        "historical query",
        source_docs=["public-isidora-005", "public-isidora-006"],
    )

    assert qdrant.last_query_filter is not None
    condition = qdrant.last_query_filter.must[0]
    assert condition.key == "source_doc"
    assert condition.match.any == [
        "public-isidora-005",
        "public-isidora-006",
    ]


def test_empty_source_filter_is_rejected():
    retriever = QdrantRetriever(
        qdrant_client=FakeQdrant(),
        collection_name="veridical_udv",
        embedding_provider=FakeEmbeddingProvider(),
    )

    try:
        retriever.retrieve("historical query", source_docs=[])
        assert False
    except ValueError as exc:
        assert "source_docs" in str(exc)
