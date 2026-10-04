from __future__ import annotations

import os

from src.mrm.logger import MRMTrace


class LangfuseObserver:
    def __init__(self, client):
        self.client = client

    def record(self, trace: MRMTrace) -> None:
        with self.client.start_as_current_observation(
            as_type="span",
            name="mrm-decision",
            input={
                "query_vector_dimension": len(trace.query_vector),
            },
        ) as observation:
            observation.update(
                output={
                    "category": trace.category,
                    "ir_max": trace.ir_max,
                    "ir_avg": trace.ir_avg,
                    "icr": trace.icr,
                    "latency_ms": trace.latency_ms,
                    "llm_invoked": trace.llm_invoked,
                    "source_count": len(trace.source_ids),
                },
                metadata={
                    "source_ids": ",".join(trace.source_ids),
                    "llm_invoked": str(trace.llm_invoked),
                },
            )


def create_langfuse_observer():
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")

    if not public_key or not secret_key:
        return None

    try:
        from langfuse import get_client

        return LangfuseObserver(get_client())
    except Exception:
        return None
