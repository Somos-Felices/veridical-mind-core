from src.mcg.classifier import classify
from src.mcg.latency import benchmark_classification_latency


def main():
    benchmark = benchmark_classification_latency(
        lambda: classify(
            [0.55, 0.50, 0.45, 0.40, 0.35],
            theta_a=0.80,
            theta_b=0.30,
            top_k=10,
        ),
        iterations=1000,
    )

    print(f"iterations={benchmark.iterations}")
    print(f"minimum_ms={benchmark.minimum_ms:.6f}")
    print(f"mean_ms={benchmark.mean_ms:.6f}")
    print(f"p95_ms={benchmark.p95_ms:.6f}")
    print(f"maximum_ms={benchmark.maximum_ms:.6f}")
    print(f"target_lt_50ms={benchmark.p95_ms < 50.0}")


if __name__ == "__main__":
    main()
