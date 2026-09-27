from dataclasses import dataclass

from src.mcg.gateway import GenerationGateway
from src.mrec.ir import RankedUDV
from src.mrm.logger import MRMLogger


@dataclass
class MockLLM:
    calls: int = 0

    def generate(self, prompt: str) -> str:
        self.calls += 1
        return "generated"


def evidence(identifier: str, ir: float) -> RankedUDV:
    return RankedUDV(
        id=identifier,
        content=f"Evidence {identifier}",
        source_doc=f"source-{identifier}",
        source_type="integration_test",
        icd=1.0,
        similarity=ir,
        ir=ir,
        metadata={},
    )


def run_case(ir_values: list[float]):
    llm = MockLLM()
    mrm = MRMLogger()

    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=mrm,
        theta_a=0.70,
        theta_b=0.25,
        top_k=10,
    )

    ranked = [
        evidence(f"udv-{index}", value)
        for index, value in enumerate(ir_values)
    ]

    response = gateway.handle(
        query="integration query",
        ranked_udvs=ranked,
        prompt="integration prompt",
    )

    return response, llm, mrm


def test_end_to_end_category_a():
    response, llm, mrm = run_case([0.80, 0.50])

    assert response.category == "A"
    assert llm.calls == 1
    assert mrm.records[0].llm_invoked is True


def test_end_to_end_category_b():
    response, llm, mrm = run_case([0.60, 0.40])

    assert response.category == "B"
    assert llm.calls == 1
    assert response.icr is not None
    assert mrm.records[0].llm_invoked is True
    assert mrm.records[0].icr == response.icr


def test_end_to_end_category_c_zero_llm_calls():
    response, llm, mrm = run_case([0.10, 0.08, 0.05])

    assert response.category == "C"
    assert response.llm_invoked is False

    # Physical suppression proof.
    assert llm.calls == 0

    trace = mrm.records[0]

    assert trace.category == "C"
    assert trace.llm_invoked is False
    assert trace.icr is None
    assert trace.latency_ms < 50.0
