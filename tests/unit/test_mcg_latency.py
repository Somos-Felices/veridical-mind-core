from src.mcg.classifier import classify
from src.mcg.latency import (
    benchmark_classification_latency,
    measure_classification_latency,
)


def test_classification_latency_is_measurable():
    decision, latency_ms = measure_classification_latency(
        lambda: classify(
            [0.55, 0.50, 0.45, 0.40, 0.35],
            theta_a=0.80,
            theta_b=0.30,
            top_k=10,
        )
    )

    assert decision.category == "B"
    assert latency_ms >= 0


def test_local_classification_latency_target():
    _, latency_ms = measure_classification_latency(
        lambda: classify(
            [0.55, 0.50, 0.45, 0.40, 0.35],
            theta_a=0.80,
            theta_b=0.30,
            top_k=10,
        )
    )

    assert latency_ms < 50


def test_latency_benchmark_is_repeatable():
    benchmark = benchmark_classification_latency(
        lambda: classify(
            [0.55, 0.50, 0.45, 0.40, 0.35],
            theta_a=0.80,
            theta_b=0.30,
            top_k=10,
        ),
        iterations=100,
    )

    assert benchmark.iterations == 100
    assert len(benchmark.samples_ms) == 100
    assert benchmark.minimum_ms >= 0
    assert benchmark.minimum_ms <= benchmark.mean_ms
    assert benchmark.mean_ms <= benchmark.maximum_ms
    assert benchmark.p95_ms <= benchmark.maximum_ms
