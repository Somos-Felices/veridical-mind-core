from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class MRMTrace:
    timestamp: str
    query_vector: list[float]
    category: str
    source_ids: list[str]
    ir_max: float
    ir_avg: float
    icr: float | None
    latency_ms: float
    llm_invoked: bool


class MRMLogger:
    """
    Minimal Sprint 1 Model Reliability Monitoring logger.

    Runtime requests provide the query vector.
    The optional argument preserves compatibility with existing
    lower-level tests that exercise the logger in isolation.
    """

    def __init__(self):
        self.records: list[MRMTrace] = []

    def record(
        self,
        *,
        category: str,
        source_ids: list[str],
        ir_max: float,
        ir_avg: float,
        icr: float | None,
        latency_ms: float,
        llm_invoked: bool,
        query_vector: list[float] | None = None,
    ) -> MRMTrace:

        trace = MRMTrace(
            timestamp=datetime.now(timezone.utc).isoformat(),
            query_vector=list(query_vector or []),
            category=category,
            source_ids=list(source_ids),
            ir_max=ir_max,
            ir_avg=ir_avg,
            icr=icr,
            latency_ms=latency_ms,
            llm_invoked=llm_invoked,
        )

        self.records.append(trace)
        return trace
