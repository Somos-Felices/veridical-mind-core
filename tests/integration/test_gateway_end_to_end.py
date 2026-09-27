from src.mcg.gateway import GenerationGateway
from src.mrec.ir import RankedUDV
from src.mrm.logger import MRMLogger


class FakeLLM:
    def __init__(self):
        self.calls = []

    def generate(self, prompt: str) -> str:
        self.calls.append(prompt)
        return "generated response"


def make_udv(identifier: str, ir: float) -> RankedUDV:
    return RankedUDV(
        id=identifier,
        content="synthetic evidence",
        source_doc="synthetic-doc",
        source_type="historical_document",
        icd=ir,
        similarity=1.0,
        ir=ir,
        metadata={},
    )


def test_gateway_category_a_invokes_llm_and_records_mrm():
    llm = FakeLLM()
    logger = MRMLogger()

    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=logger,
        theta_a=0.80,
        theta_b=0.30,
    )

    result = gateway.handle(
        query="supported question",
        ranked_udvs=[make_udv("a-1", 0.90)],
        prompt="answer using evidence",
    )

    assert result.category == "A"
    assert result.llm_invoked is True
    assert len(llm.calls) == 1
    assert result.trace.category == "A"
    assert result.trace.llm_invoked is True


def test_gateway_category_b_invokes_llm_and_records_icr():
    llm = FakeLLM()
    logger = MRMLogger()

    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=logger,
        theta_a=0.80,
        theta_b=0.30,
    )

    result = gateway.handle(
        query="partially supported question",
        ranked_udvs=[
            make_udv("b-1", 0.55),
            make_udv("b-2", 0.50),
            make_udv("b-3", 0.45),
        ],
        prompt="answer with qualification",
    )

    assert result.category == "B"
    assert result.llm_invoked is True
    assert result.icr is not None
    assert len(llm.calls) == 1
    assert result.trace.category == "B"
    assert result.trace.llm_invoked is True


def test_gateway_category_c_blocks_llm_and_returns_rpa():
    llm = FakeLLM()
    logger = MRMLogger()

    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=logger,
        theta_a=0.80,
        theta_b=0.30,
    )

    result = gateway.handle(
        query="unsupported question",
        ranked_udvs=[
            make_udv("c-1", 0.20),
            make_udv("c-2", 0.15),
            make_udv("c-3", 0.10),
        ],
        prompt="this must never reach the LLM",
    )

    assert result.category == "C"
    assert result.llm_invoked is False
    assert result.icr is None
    assert len(llm.calls) == 0
    assert result.response == (
        "I don't have sufficient documentary evidence to answer that."
    )
    assert result.trace.category == "C"
    assert result.trace.llm_invoked is False
