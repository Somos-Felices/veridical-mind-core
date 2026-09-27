from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class MRMTrace:
    timestamp: str
    category: str
    source_ids: list[str]
    ir_max: float
    ir_avg: float
    icr: float | None
    latency_ms: float
    llm_invoked: bool


class MRMLogger:
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
    ) -> MRMTrace:

        trace = MRMTrace(
            timestamp=datetime.now(timezone.utc).isoformat(),
            category=category,
            source_ids=source_ids,
            ir_max=ir_max,
            ir_avg=ir_avg,
            icr=icr,
            latency_ms=latency_ms,
            llm_invoked=llm_invoked,
        )

        self.records.append(trace)

        return trace
