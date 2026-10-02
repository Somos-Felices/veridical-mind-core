import json


def test_mrm_writes_structured_jsonl_without_raw_query(tmp_path):
    from src.mrm.logger import MRMLogger

    log_path = tmp_path / "mrm.jsonl"
    logger = MRMLogger(log_path=log_path)

    logger.record(
        category="C",
        source_ids=["source-001", "source-002"],
        ir_max=0.20,
        ir_avg=0.12,
        icr=None,
        latency_ms=1.5,
        llm_invoked=False,
        query_vector=[0.1, 0.2, 0.3],
    )

    lines = log_path.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 1

    record = json.loads(lines[0])

    assert record["category"] == "C"
    assert record["source_ids"] == ["source-001", "source-002"]
    assert record["query_vector"] == [0.1, 0.2, 0.3]
    assert record["ir_max"] == 0.20
    assert record["ir_avg"] == 0.12
    assert record["icr"] is None
    assert record["latency_ms"] == 1.5
    assert record["llm_invoked"] is False
    assert "query" not in record
    assert "raw_query" not in record
