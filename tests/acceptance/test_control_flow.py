from time import perf_counter

from src.mcg import classify
from src.mcg.gateway import GenerationGateway
from src.mrm import MRMLogger


class MockLLM:
    def __init__(self):
        self.calls = 0
        self.prompts = []

    def generate(self, prompt: str) -> str:
        self.calls += 1
        self.prompts.append(prompt)
        return f"generated: {prompt}"


def run_control_flow(
    ir_values: list[float],
    source_ids: list[str],
    *,
    theta_a: float,
    theta_b: float,
    prompt: str,
):
    llm = MockLLM()
    gateway = GenerationGateway(llm)
    logger = MRMLogger()

    start = perf_counter()

    decision = classify(
        ir_values=ir_values,
        theta_a=theta_a,
        theta_b=theta_b,
        top_k=10,
    )

    result = gateway.handle(
        decision=decision,
        prompt=prompt,
    )

    latency_ms = (perf_counter() - start) * 1000

    trace = logger.record(
        category=decision.category,
        source_ids=source_ids,
        ir_max=decision.ir_max,
        ir_avg=decision.ir_avg,
        icr=decision.icr,
        latency_ms=latency_ms,
        llm_invoked=result.llm_invoked,
    )

    return decision, result, trace, llm


def test_acceptance_category_a():
    decision, result, trace, llm = run_control_flow(
        ir_values=[0.80, 0.20],
        source_ids=["test-001", "test-002"],
        theta_a=0.75,
        theta_b=0.30,
        prompt="Who was Isidora Goyenechea?",
    )

    assert decision.category == "A"
    assert result.category == "A"
    assert result.llm_invoked is True
    assert llm.calls == 1

    assert trace.category == "A"
    assert trace.llm_invoked is True
    assert trace.ir_max == 0.80
    assert trace.icr is None


def test_acceptance_category_b():
    decision, result, trace, llm = run_control_flow(
        ir_values=[0.60, 0.50, 0.40],
        source_ids=["test-001", "test-002", "test-003"],
        theta_a=0.75,
        theta_b=0.45,
        prompt="Give a qualified answer.",
    )

    assert decision.category == "B"
    assert result.category == "B"
    assert result.llm_invoked is True
    assert llm.calls == 1

    assert result.icr is not None
    assert trace.category == "B"
    assert trace.icr == result.icr
    assert trace.llm_invoked is True


def test_acceptance_category_c_zero_llm_calls():
    decision, result, trace, llm = run_control_flow(
        ir_values=[0.20, 0.10, 0.05],
        source_ids=["test-001", "test-002", "test-003"],
        theta_a=0.75,
        theta_b=0.40,
        prompt="This must never reach the LLM.",
    )

    assert decision.category == "C"
    assert result.category == "C"

    # Physical suppression proof.
    assert result.llm_invoked is False
    assert llm.calls == 0
    assert llm.prompts == []

    # RPA path.
    assert result.response == (
        "I don't have sufficient documentary evidence to answer that."
    )

    # MRM proof.
    assert trace.category == "C"
    assert trace.llm_invoked is False
    assert trace.icr is None

    # MCG latency is measured around classification/control here.
    assert trace.latency_ms >= 0.0
