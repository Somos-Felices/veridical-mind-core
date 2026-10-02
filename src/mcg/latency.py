from dataclasses import dataclass
from time import perf_counter
from typing import Callable


@dataclass(frozen=True)
class LatencyBenchmark:
    iterations: int
    samples_ms: tuple[float, ...]
    minimum_ms: float
    mean_ms: float
    p95_ms: float
    maximum_ms: float


def measure_classification_latency(classifier_call):
    """
    Measures only the MCG classification decision.

    Timing begins immediately before classification receives
    the ranked IR values and ends immediately after the decision.
    """

    start = perf_counter()
    decision = classifier_call()
    elapsed_ms = (perf_counter() - start) * 1000.0

    return decision, elapsed_ms


def benchmark_classification_latency(
    classifier_call: Callable[[], object],
    *,
    iterations: int = 1000,
) -> LatencyBenchmark:
    if iterations < 1:
        raise ValueError("iterations must be >= 1")

    samples = []

    for _ in range(iterations):
        _, latency_ms = measure_classification_latency(classifier_call)
        samples.append(latency_ms)

    ordered = sorted(samples)
    p95_index = min(
        len(ordered) - 1,
        max(0, int(len(ordered) * 0.95) - 1),
    )

    return LatencyBenchmark(
        iterations=iterations,
        samples_ms=tuple(samples),
        minimum_ms=min(samples),
        mean_ms=sum(samples) / len(samples),
        p95_ms=ordered[p95_index],
        maximum_ms=max(samples),
    )
