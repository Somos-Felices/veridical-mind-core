from dataclasses import dataclass
from typing import Literal


Category = Literal["A", "B", "C"]


@dataclass(frozen=True)
class MCGDecision:
    category: Category
    ir_max: float
    ir_avg: float
    icr: float | None
    llm_allowed: bool


def calculate_icr(ir_values: list[float]) -> float | None:
    if not ir_values:
        return None

    denominator = sum(ir_values)

    if denominator == 0:
        return None

    numerator = sum(ir_value ** 2 for ir_value in ir_values)

    return numerator / denominator


def classify(
    ir_values: list[float],
    theta_a: float,
    theta_b: float,
    top_k: int = 10,
) -> MCGDecision:

    if not ir_values:
        return MCGDecision(
            category="C",
            ir_max=0.0,
            ir_avg=0.0,
            icr=None,
            llm_allowed=False,
        )

    selected = sorted(ir_values, reverse=True)[:top_k]

    ir_max = max(selected)
    ir_avg = sum(selected) / len(selected)

    if ir_max >= theta_a:
        return MCGDecision(
            category="A",
            ir_max=ir_max,
            ir_avg=ir_avg,
            icr=None,
            llm_allowed=True,
        )

    if ir_avg >= theta_b:
        return MCGDecision(
            category="B",
            ir_max=ir_max,
            ir_avg=ir_avg,
            icr=calculate_icr(selected),
            llm_allowed=True,
        )

    return MCGDecision(
        category="C",
        ir_max=ir_max,
        ir_avg=ir_avg,
        icr=None,
        llm_allowed=False,
    )
