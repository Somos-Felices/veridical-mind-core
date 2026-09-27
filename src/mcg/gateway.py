from dataclasses import dataclass
from typing import Protocol

from src.mcg import MCGDecision


class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...


@dataclass(frozen=True)
class GatewayResponse:
    category: str
    response: str
    llm_invoked: bool
    icr: float | None


class RPA:
    @staticmethod
    def respond() -> str:
        return "I don't have sufficient documentary evidence to answer that."


class GenerationGateway:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def handle(
        self,
        decision: MCGDecision,
        prompt: str,
    ) -> GatewayResponse:

        # Category C: physically terminate before LLM invocation.
        if decision.category == "C":
            return GatewayResponse(
                category="C",
                response=RPA.respond(),
                llm_invoked=False,
                icr=None,
            )

        # Categories A/B are permitted to reach generation.
        response = self.llm_client.generate(prompt)

        return GatewayResponse(
            category=decision.category,
            response=response,
            llm_invoked=True,
            icr=decision.icr,
        )
