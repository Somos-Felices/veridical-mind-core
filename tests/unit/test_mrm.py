from src.mrm import MRMLogger


def test_mrm_records_category_c():
    logger = MRMLogger()

    trace = logger.record(
        category="C",
        source_ids=["test-001", "test-002"],
        ir_max=0.20,
        ir_avg=0.12,
        icr=None,
        latency_ms=1.5,
        llm_invoked=False,
    )

    assert trace.category == "C"
    assert trace.source_ids == ["test-001", "test-002"]
    assert trace.ir_max == 0.20
    assert trace.ir_avg == 0.12
    assert trace.icr is None
    assert trace.latency_ms == 1.5
    assert trace.llm_invoked is False
    assert len(logger.records) == 1


def test_mrm_records_category_a():
    logger = MRMLogger()

    trace = logger.record(
        category="A",
        source_ids=["test-001"],
        ir_max=0.80,
        ir_avg=0.50,
        icr=None,
        latency_ms=2.0,
        llm_invoked=True,
    )

    assert trace.category == "A"
    assert trace.llm_invoked is True


def test_mrm_records_category_b_with_icr():
    logger = MRMLogger()

    trace = logger.record(
        category="B",
        source_ids=["test-001", "test-002", "test-003"],
        ir_max=0.60,
        ir_avg=0.50,
        icr=0.53,
        latency_ms=1.8,
        llm_invoked=True,
    )

    assert trace.category == "B"
    assert trace.icr == 0.53
    assert trace.llm_invoked is True
