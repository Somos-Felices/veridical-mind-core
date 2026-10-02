from dataclasses import dataclass

from src.mcg.gateway import GenerationGateway
from src.mrec.ir import RankedUDV
from src.mrm.logger import MRMLogger


@dataclass
class MockLLM:
    calls: int = 0
    prompts: list[str] | None = None
    temperatures: list[float] | None = None

    def __post_init__(self):
        if self.prompts is None:
            self.prompts = []
        if self.temperatures is None:
            self.temperatures = []

    def generate(self, prompt: str, *, temperature: float = 0.0) -> str:
        self.calls += 1
        self.prompts.append(prompt)
        self.temperatures.append(temperature)
        return "mock generated response"


def udv(identifier: str, ir: float) -> RankedUDV:
    return RankedUDV(
        id=identifier,
        content=f"Evidence {identifier}",
        source_doc=f"doc-{identifier}",
        source_type="test",
        icd=1.0,
        similarity=ir,
        ir=ir,
        metadata={},
    )


def test_gateway_category_a_calls_llm_and_records_mrm():
    llm = MockLLM()
    mrm = MRMLogger()

    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=mrm,
        theta_a=0.70,
        theta_b=0.25,
        top_k=10,
    )

    response = gateway.handle(
        query="test query",
        ranked_udvs=[
            udv("a-1", 0.80),
            udv("a-2", 0.40),
        ],
        prompt="answer using evidence",
    )

    assert response.category == "A"
    assert response.llm_invoked is True
    assert llm.calls == 1
    assert llm.temperatures == [0.0]
    assert response.icr is None

    assert len(mrm.records) == 1

    trace = mrm.records[0]

    assert trace.category == "A"
    assert trace.llm_invoked is True
    assert trace.icr is None
    assert trace.source_ids == ["a-1", "a-2"]
    assert trace.ir_max == 0.80
    assert abs(trace.ir_avg - 0.60) < 1e-9
    assert trace.latency_ms >= 0


def test_gateway_category_b_calls_llm_and_records_icr():
    llm = MockLLM()
    mrm = MRMLogger()

    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=mrm,
        theta_a=0.70,
        theta_b=0.25,
        top_k=10,
    )

    response = gateway.handle(
        query="partial evidence query",
        ranked_udvs=[
            udv("b-1", 0.60),
            udv("b-2", 0.40),
        ],
        prompt="provide a qualified answer",
    )

    assert response.category == "B"
    assert response.llm_invoked is True
    assert llm.calls == 1
    assert llm.temperatures == [0.0]
    assert response.icr is not None

    trace = mrm.records[0]

    assert trace.category == "B"
    assert trace.llm_invoked is True
    assert trace.icr == response.icr
    assert trace.ir_max == 0.60
    assert abs(trace.ir_avg - 0.50) < 1e-9


def test_gateway_category_c_physically_suppresses_llm():
    llm = MockLLM()
    mrm = MRMLogger()

    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=mrm,
        theta_a=0.70,
        theta_b=0.25,
        top_k=10,
    )

    response = gateway.handle(
        query="unsupported query",
        ranked_udvs=[
            udv("c-1", 0.10),
            udv("c-2", 0.08),
            udv("c-3", 0.05),
        ],
        prompt="THIS PROMPT MUST NEVER REACH THE LLM",
    )

    assert response.category == "C"
    assert response.llm_invoked is False
    assert response.icr is None

    assert llm.calls == 0
    assert llm.prompts == []
    assert llm.temperatures == []

    assert "sufficient documentary evidence" in response.response

    assert len(mrm.records) == 1

    trace = mrm.records[0]

    assert trace.category == "C"
    assert trace.llm_invoked is False
    assert trace.icr is None
    assert trace.source_ids == ["c-1", "c-2", "c-3"]
    assert trace.ir_max == 0.10
    assert abs(trace.ir_avg - (0.23 / 3)) < 1e-9
    assert trace.latency_ms >= 0


def test_gateway_category_c_records_decision_latency():
    llm = MockLLM()
    mrm = MRMLogger()

    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=mrm,
        theta_a=0.70,
        theta_b=0.25,
        top_k=10,
    )

    response = gateway.handle(
        query="latency test",
        ranked_udvs=[udv("latency-1", 0.05)],
        prompt="must not be sent",
    )

    assert response.category == "C"
    assert response.trace.latency_ms >= 0
    assert response.trace.latency_ms < 50.0
