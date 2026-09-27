from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Protocol

from src.mcg.classifier import MCGDecision, classify
from src.mrec.ir import RankedUDV
from src.mrm.logger import MRMLogger


class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...


@dataclass(frozen=True)
class GatewayResponse:
    category: str
    response: str
    llm_invoked: bool
    icr: float | None
    trace: object


class RPA:
    @staticmethod
    def respond() -> str:
        return "I don't have sufficient documentary evidence to answer that."


class GenerationGateway:
    def __init__(
        self,
        llm_client: LLMClient,
        mrm_logger: MRMLogger,
        theta_a: float,
        theta_b: float,
        top_k: int = 10,
    ):
        self.llm_client = llm_client
        self.mrm_logger = mrm_logger
        self.theta_a = theta_a
        self.theta_b = theta_b
        self.top_k = top_k

    def handle(
        self,
        *,
        query: str,
        ranked_udvs: list[RankedUDV],
        prompt: str,
        query_vector: list[float] | None = None,
    ) -> GatewayResponse:

        ir_values = [udv.ir for udv in ranked_udvs]

        decision_start = perf_counter()

        decision: MCGDecision = classify(
            ir_values,
            theta_a=self.theta_a,
            theta_b=self.theta_b,
            top_k=self.top_k,
        )

        decision_latency_ms = (perf_counter() - decision_start) * 1000.0

        source_ids = [
            udv.id
            for udv in sorted(
                ranked_udvs,
                key=lambda item: item.ir,
                reverse=True,
            )[: self.top_k]
        ]

        if decision.category == "C":
            trace = self.mrm_logger.record(
                query_vector=query_vector,
                category="C",
                source_ids=source_ids,
                ir_max=decision.ir_max,
                ir_avg=decision.ir_avg,
                icr=None,
                latency_ms=decision_latency_ms,
                llm_invoked=False,
            )

            return GatewayResponse(
                category="C",
                response=RPA.respond(),
                llm_invoked=False,
                icr=None,
                trace=trace,
            )

        generation_prompt = prompt

        if decision.category == "B":
            generation_prompt = (
                "[EPISTEMIC QUALIFICATION] The available documentary evidence "
                "is partial or non-conclusive. Clearly distinguish documented "
                "evidence from inference and avoid presenting inference as fact. "
                f"ICR={decision.icr}\n\n{prompt}"
            )

        response = self.llm_client.generate(generation_prompt)

        trace = self.mrm_logger.record(
            query_vector=query_vector,
            category=decision.category,
            source_ids=source_ids,
            ir_max=decision.ir_max,
            ir_avg=decision.ir_avg,
            icr=decision.icr,
            latency_ms=decision_latency_ms,
            llm_invoked=True,
        )

        return GatewayResponse(
            category=decision.category,
            response=response,
            llm_invoked=True,
            icr=decision.icr,
            trace=trace,
        )
