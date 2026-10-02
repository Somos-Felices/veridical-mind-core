from src.mrm.logger import MRMLogger, MRMTrace


def test_trace_contains_required_fields():
    logger = MRMLogger()

    trace = logger.record(
        query_vector=[0.1, 0.2, 0.3],
        category="C",
        source_ids=["doc1:v1:0", "doc1:v1:1"],
        ir_max=0.42,
        ir_avg=0.31,
        icr=None,
        latency_ms=0.01,
        llm_invoked=False,
    )

    assert isinstance(trace, MRMTrace)
    assert trace.timestamp
    assert trace.query_vector == [0.1, 0.2, 0.3]
    assert trace.category == "C"
    assert trace.source_ids == ["doc1:v1:0", "doc1:v1:1"]
    assert trace.ir_max == 0.42
    assert trace.ir_avg == 0.31
    assert trace.icr is None
    assert trace.latency_ms == 0.01
    assert trace.llm_invoked is False


def test_trace_does_not_store_raw_query():
    logger = MRMLogger()

    trace = logger.record(
        query_vector=[0.1, 0.2],
        category="C",
        source_ids=[],
        ir_max=0.1,
        ir_avg=0.1,
        icr=None,
        latency_ms=0.02,
        llm_invoked=False,
    )

    assert not hasattr(trace, "query")
    assert not hasattr(trace, "raw_query")


def test_trace_is_immutable():
    logger = MRMLogger()

    trace = logger.record(
        query_vector=[0.1],
        category="A",
        source_ids=["doc:v1:0"],
        ir_max=0.9,
        ir_avg=0.9,
        icr=None,
        latency_ms=0.01,
        llm_invoked=True,
    )

    try:
        trace.category = "C"
    except AttributeError:
        pass
    else:
        raise AssertionError("MRMTrace must be immutable")


def test_logger_keeps_trace_history():
    logger = MRMLogger()

    first = logger.record(
        query_vector=[0.1],
        category="C",
        source_ids=[],
        ir_max=0.1,
        ir_avg=0.1,
        icr=None,
        latency_ms=0.01,
        llm_invoked=False,
    )

    second = logger.record(
        query_vector=[0.2],
        category="A",
        source_ids=["doc:v1:0"],
        ir_max=0.9,
        ir_avg=0.9,
        icr=None,
        latency_ms=0.01,
        llm_invoked=True,
    )

    assert logger.records == [first, second]
