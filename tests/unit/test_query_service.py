from src.mcg.gateway import GenerationGateway
from src.mrec.embeddings import LocalEmbeddingProvider
from src.mrec.retriever import QdrantRetriever
from src.mrm.logger import MRMLogger
from src.service.query_service import QueryService


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
                    0.5,
                    {
                        "udv_id": "integration-001:v1:0",
                        "content": "Partial documentary evidence.",
                        "source_doc": "integration-001",
                        "source_type": "test",
                        "icd": 0.8,
                        "metadata": {"source_version": "v1"},
                    },
                ),
                FakePoint(
                    2,
                    0.4,
                    {
                        "udv_id": "integration-002:v1:0",
                        "content": "Additional documentary evidence.",
                        "source_doc": "integration-002",
                        "source_type": "test",
                        "icd": 0.8,
                        "metadata": {"source_version": "v1"},
                    },
                ),
            ]
        )


class FakeLLM:
    def __init__(self):
        self.calls = 0

    def generate(self, prompt: str) -> str:
        self.calls += 1
        return "integration response"


def test_query_service_connects_retrieval_gateway_and_mrm():
    llm = FakeLLM()
    mrm = MRMLogger()

    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=mrm,
        theta_a=0.80,
        theta_b=0.30,
        top_k=10,
    )

    service = QueryService(
        retriever=QdrantRetriever(
            qdrant_client=FakeQdrant(),
            collection_name="veridical_udv",
            embedding_provider=FakeEmbeddingProvider(),
        ),
        gateway=gateway,
        embedding_provider=FakeEmbeddingProvider(),
    )

    result = service.handle(
        query="historical query",
        prompt="answer using documentary evidence",
    )

    assert result.category == "B"
    assert result.llm_invoked is True
    assert llm.calls == 1

    assert len(mrm.records) == 1
    trace = mrm.records[0]

    assert trace.category == "B"
    assert trace.llm_invoked is True
    assert trace.source_ids == [
        "integration-001:v1:0",
        "integration-002:v1:0",
    ]
    assert abs(trace.ir_max - 0.4) < 1e-9
    assert abs(trace.ir_avg - 0.36) < 1e-9
    assert trace.query_vector == [1.0, 0.0, 0.0]
