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
        return "grounded integration response"


def build_poc_service():
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
    llm = RecordingLLM()

    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=mrm,
        config=MCGConfig(
            theta_a=0.80,
            theta_b=0.30,
            top_k=10,
        ),
        answerability_enabled=True,
    )

    service = QueryService(
        retriever=retriever,
        gateway=gateway,
        embedding_provider=embedding_provider,
    )

    return service, llm, mrm


def test_strong_evidence_produces_grounded_answer():
    service, llm, mrm = build_poc_service()

    result = service.handle(
        query="Who designed Palacio Cousino?",
        prompt="Answer using only the supplied documentary evidence.",
    )

    assert result.category in {"A", "B"}
    assert result.llm_invoked is True
    assert len(llm.calls) == 1

    prompt = llm.calls[0]["prompt"]

    assert "DOCUMENTARY EVIDENCE:" in prompt
    assert "[UDV " in prompt
    assert "[SOURCE " in prompt
    assert "Palacio Cousino" in prompt

    assert len(mrm.records) == 1
    assert mrm.records[0].llm_invoked is True


def test_multiple_sources_are_present_in_grounded_prompt():
    service, llm, mrm = build_poc_service()

    result = service.handle(
        query="What did Isidora Goyenechea do with Parque de Lota?",
        prompt="Answer using only the supplied documentary evidence.",
    )

    assert result.category in {"A", "B"}
    assert result.llm_invoked is True
    assert len(llm.calls) == 1

    prompt = llm.calls[0]["prompt"]

    assert "DOCUMENTARY EVIDENCE:" in prompt
    assert "[UDV " in prompt
    assert "[SOURCE " in prompt

    source_count = prompt.count("[SOURCE ")
    assert source_count >= 2

    assert len(mrm.records) == 1
    assert mrm.records[0].llm_invoked is True


def test_unsupported_question_is_refused_without_llm():
    service, llm, mrm = build_poc_service()

    result = service.handle(
        query="What was Isidora Goyenechea's favorite color?",
        prompt="Answer using only the supplied documentary evidence.",
    )

    assert result.category == "C"
    assert result.llm_invoked is False
    assert llm.calls == []

    assert "sufficient documentary evidence" in result.response.lower()

    assert len(mrm.records) == 1
    assert mrm.records[0].category == "C"
    assert mrm.records[0].llm_invoked is False
