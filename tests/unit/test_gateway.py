from src.mcg import classify
from src.mcg.gateway import GenerationGateway


class MockLLM:
    def __init__(self):
        self.calls = 0

    def generate(self, prompt: str) -> str:
        self.calls += 1
        return f"generated: {prompt}"


def test_category_c_physically_suppresses_llm():
    llm = MockLLM()
    gateway = GenerationGateway(llm)

    decision = classify(
        ir_values=[0.20, 0.10, 0.05],
        theta_a=0.75,
        theta_b=0.40,
    )

    result = gateway.handle(
        decision=decision,
        prompt="This prompt must never reach the LLM.",
    )

    assert result.category == "C"
    assert result.llm_invoked is False
    assert llm.calls == 0
    assert result.response == (
        "I don't have sufficient documentary evidence to answer that."
    )


def test_category_a_allows_llm():
    llm = MockLLM()
    gateway = GenerationGateway(llm)

    decision = classify(
        ir_values=[0.80, 0.20],
        theta_a=0.75,
        theta_b=0.30,
    )

    result = gateway.handle(
        decision=decision,
        prompt="Who was Isidora Goyenechea?",
    )

    assert result.category == "A"
    assert result.llm_invoked is True
    assert llm.calls == 1
    assert result.response.startswith("generated:")


def test_category_b_allows_llm_and_preserves_icr():
    llm = MockLLM()
    gateway = GenerationGateway(llm)

    decision = classify(
        ir_values=[0.60, 0.50, 0.40],
        theta_a=0.75,
        theta_b=0.45,
    )

    result = gateway.handle(
        decision=decision,
        prompt="Give a qualified answer.",
    )

    assert result.category == "B"
    assert result.llm_invoked is True
    assert llm.calls == 1
    assert result.icr == decision.icr
