from src.mcg.gateway import GenerationGateway
from src.mrec.ir import RankedUDV
from src.mrm.logger import MRMLogger


class FakeLLM:
    def __init__(self):
        self.calls = 0

    def generate(self, prompt: str, *, temperature: float = 0.0) -> str:
        self.calls += 1
        return "SHOULD NOT BE CALLED"


def test_category_c_physically_suppresses_llm():
    llm = FakeLLM()
    mrm_logger = MRMLogger()

    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=mrm_logger,
        theta_a=0.80,
        theta_b=0.30,
    )

    ranked_udvs = [
        RankedUDV(
            id="udv-c-1",
            content="weak evidence",
            source_doc="test-doc",
            source_type="test",
            icd=0.20,
            similarity=1.0,
            ir=0.20,
            metadata={},
        ),
        RankedUDV(
            id="udv-c-2",
            content="weak evidence",
            source_doc="test-doc",
            source_type="test",
            icd=0.15,
            similarity=1.0,
            ir=0.15,
            metadata={},
        ),
        RankedUDV(
            id="udv-c-3",
            content="weak evidence",
            source_doc="test-doc",
            source_type="test",
            icd=0.10,
            similarity=1.0,
            ir=0.10,
            metadata={},
        ),
    ]

    result = gateway.handle(
        query="unsupported question",
        ranked_udvs=ranked_udvs,
        prompt="This prompt must never reach the LLM.",
    )

    assert result.category == "C"
    assert result.llm_invoked is False
    assert result.response == (
        "I don't have sufficient documentary evidence to answer that."
    )

    # Physical suppression proof:
    assert llm.calls == 0

    # MRM proof:
    assert result.trace.llm_invoked is False
    assert result.trace.category == "C"

