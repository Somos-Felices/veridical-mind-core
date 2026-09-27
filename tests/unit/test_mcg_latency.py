from src.mcg.classifier import classify
from src.mcg.latency import measure_classification_latency


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
    """
    Local smoke-level check.

    This does NOT constitute the final production <50 ms
    benchmark. Final acceptance must be measured on the
    agreed runtime/environment and corpus.
    """

    _, latency_ms = measure_classification_latency(
        lambda: classify(
            [0.55, 0.50, 0.45, 0.40, 0.35],
            theta_a=0.80,
            theta_b=0.30,
            top_k=10,
        )
    )

    assert latency_ms < 50
