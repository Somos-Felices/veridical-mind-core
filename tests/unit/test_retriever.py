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
    def query_points(self, *, collection_name, query, limit, with_payload):
        assert collection_name == "veridical_udv"
        assert query == [1.0, 0.0, 0.0]
        assert limit == 10
        assert with_payload is True

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
            ]
        )


def test_qdrant_retriever_reconstructs_udvs_and_applies_ir():
    retriever = QdrantRetriever(
        qdrant_client=FakeQdrant(),
        collection_name="veridical_udv",
        embedding_provider=FakeEmbeddingProvider(),
    )

    result = retriever.retrieve("historical query")

    assert result.query == "historical query"
    assert len(result.results) == 2

    first = result.results[0]
    second = result.results[1]

    assert first.id == "doc-001:v1:0"
    assert first.similarity == 0.8
    assert first.icd == 0.9
    assert abs(first.ir - 0.72) < 1e-9

    assert second.id == "doc-002:v1:0"
    assert second.similarity == 0.6
    assert second.icd == 0.5
    assert abs(second.ir - 0.30) < 1e-9

    assert first.ir > second.ir


def test_empty_query_is_rejected():
    retriever = QdrantRetriever(
        qdrant_client=FakeQdrant(),
        collection_name="veridical_udv",
        embedding_provider=FakeEmbeddingProvider(),
    )

    try:
        retriever.retrieve("   ")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "query" in str(exc)
