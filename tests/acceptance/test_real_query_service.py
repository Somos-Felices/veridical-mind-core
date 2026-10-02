from qdrant_client import QdrantClient

from src.config.mcg import MCGConfig
from src.mcg.gateway import GenerationGateway
from src.mrec.embeddings import LocalEmbeddingProvider
from src.mrec.retriever import QdrantRetriever
from src.mrm.logger import MRMLogger
from src.service.query_service import QueryService


class RecordingLLM:
    def __init__(self):
        self.calls = []

    def generate(self, prompt: str, *, temperature: float = 0.0) -> str:
        self.calls.append(
            {
                "prompt": prompt,
                "temperature": temperature,
            }
        )
        return "integration response"


def build_service(llm):
    embedding_provider = LocalEmbeddingProvider()

    qdrant = QdrantClient(
        url="http://localhost:6333",
    )

    retriever = QdrantRetriever(
        qdrant_client=qdrant,
        collection_name="veridical_udv",
        embedding_provider=embedding_provider,
    )

    mrm = MRMLogger()

    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=mrm,
        config=MCGConfig(
            theta_a=0.80,
            theta_b=0.30,
            top_k=10,
        ),
    )

    service = QueryService(
        retriever=retriever,
        gateway=gateway,
        embedding_provider=embedding_provider,
    )

    return service, mrm


def test_real_qdrant_query_service_reaches_gateway_and_mrm():
    llm = RecordingLLM()
    service, mrm = build_service(llm)

    result = service.handle(
        query="What documentary information is available about Isidora Goyenechea?",
        prompt="Answer using documentary evidence.",
    )

    assert result.category in {"A", "B", "C"}

    assert len(mrm.records) == 1
    trace = mrm.records[0]

    assert trace.category == result.category
    assert trace.query_vector
    assert trace.source_ids
    assert trace.ir_max is not None
    assert trace.ir_avg is not None
    assert trace.latency_ms >= 0

    if result.category == "C":
        assert llm.calls == []
        assert result.llm_invoked is False
        assert trace.llm_invoked is False
    else:
        assert len(llm.calls) == 1
        assert result.llm_invoked is True
        assert trace.llm_invoked is True
        assert llm.calls[0]["temperature"] == 0.0
