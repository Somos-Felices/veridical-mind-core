from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


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
    Sprint 1 Model Reliability Monitoring logger.

    Runtime requests provide the query vector.
    Structured JSONL persistence is optional and disabled by default.
    Raw query text is never stored.
    """

    def __init__(self, log_path: str | Path | None = None, observer=None):
        self.records: list[MRMTrace] = []
        self.log_path = Path(log_path) if log_path else None
        self.observer = observer

        if self.log_path:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)

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

        if self.log_path:
            with self.log_path.open("a", encoding="utf-8") as handle:
                handle.write(
                    json.dumps(asdict(trace), separators=(",", ":")) + "\n"
                )

        if self.observer:
            try:
                self.observer.record(trace)
            except Exception:
                pass

        return trace
