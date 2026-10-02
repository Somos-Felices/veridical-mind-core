from dataclasses import dataclass

from src.config.mcg import MCGConfig
from src.mcg.gateway import GenerationGateway
from src.mrec.ir import RankedUDV
from src.mrm.logger import MRMLogger


@dataclass
class SpyLLM:
    calls: list[tuple[str, float]]

    def generate(self, prompt: str, *, temperature: float = 0.0) -> str:
        self.calls.append((prompt, temperature))
        return "generated response"


def make_udv(identifier: str, ir: float) -> RankedUDV:
    return RankedUDV(
        id=identifier,
        content=f"synthetic evidence {identifier}",
        source_doc=f"source-{identifier}",
        source_type="acceptance_test",
        icd=1.0,
        similarity=ir,
        ir=ir,
        metadata={},
    )


def make_gateway():
    llm = SpyLLM(calls=[])
    mrm = MRMLogger()
    config = MCGConfig(theta_a=0.70, theta_b=0.25, top_k=10)
    gateway = GenerationGateway(
        llm_client=llm,
        mrm_logger=mrm,
        config=config,
    )
    return gateway, llm, mrm


def test_t1_category_a_generation_allowed_at_zero_temperature():
    gateway, llm, mrm = make_gateway()

    result = gateway.handle(
        query="supported question",
        ranked_udvs=[
            make_udv("a-1", 0.90),
            make_udv("a-2", 0.55),
        ],
        prompt="answer using documentary evidence",
        query_vector=[0.1, 0.2, 0.3],
    )

    assert result.category == "A"
    assert result.llm_invoked is True
    assert len(llm.calls) == 1
    assert llm.calls[0][1] == 0.0
    assert result.trace.category == "A"
    assert result.trace.llm_invoked is True
    assert result.trace.source_ids == ["a-1", "a-2"]


def test_t2_category_b_is_qualified_and_records_icr():
    gateway, llm, mrm = make_gateway()

    result = gateway.handle(
        query="partially supported question",
        ranked_udvs=[
            make_udv("b-1", 0.60),
            make_udv("b-2", 0.50),
            make_udv("b-3", 0.40),
        ],
        prompt="answer with available evidence",
        query_vector=[0.4, 0.5, 0.6],
    )

    assert result.category == "B"
    assert result.llm_invoked is True
    assert len(llm.calls) == 1
    assert llm.calls[0][1] == 0.0

    generated_prompt = llm.calls[0][0]
    assert "EPISTEMIC QUALIFICATION" in generated_prompt
    assert "partial or non-conclusive" in generated_prompt
    assert "ICR=" in generated_prompt

    assert result.icr is not None
    assert result.trace.category == "B"
    assert result.trace.llm_invoked is True
    assert result.trace.icr == result.icr


def test_t3_category_c_physically_suppresses_llm():
    gateway, llm, mrm = make_gateway()

    result = gateway.handle(
        query="unsupported question",
        ranked_udvs=[
            make_udv("c-1", 0.20),
            make_udv("c-2", 0.15),
            make_udv("c-3", 0.10),
        ],
        prompt="THIS MUST NEVER REACH THE LLM",
        query_vector=[0.7, 0.8, 0.9],
    )

    assert result.category == "C"
    assert result.llm_invoked is False
    assert len(llm.calls) == 0
    assert result.response == (
        "I don't have sufficient documentary evidence to answer that."
    )

    trace = result.trace
    assert trace.category == "C"
    assert trace.llm_invoked is False
    assert trace.icr is None
    assert trace.latency_ms < 50.0


def test_t4_mrm_contains_required_trace_fields_without_raw_query():
    gateway, llm, mrm = make_gateway()

    result = gateway.handle(
        query="private raw query must not appear in MRM",
        ranked_udvs=[
            make_udv("t4-1", 0.20),
            make_udv("t4-2", 0.10),
        ],
        prompt="must not reach LLM",
        query_vector=[0.11, 0.22, 0.33],
    )

    trace = result.trace

    assert trace.timestamp
    assert trace.query_vector == [0.11, 0.22, 0.33]
    assert trace.category == "C"
    assert trace.source_ids == ["t4-1", "t4-2"]
    assert trace.ir_max == 0.20
    assert abs(trace.ir_avg - 0.15) < 1e-12
    assert trace.icr is None
    assert trace.latency_ms >= 0.0
    assert trace.llm_invoked is False

    assert not hasattr(trace, "query")
    assert "private raw query must not appear in MRM" not in trace.__dict__
