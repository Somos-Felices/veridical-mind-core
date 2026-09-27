from time import perf_counter


def measure_classification_latency(classifier_call):
    """
    Measures only the MCG classification decision.

    Timing begins immediately before classification receives
    the ranked IR values and ends immediately after the decision.
    """

    start = perf_counter()
    decision = classifier_call()
    elapsed_ms = (perf_counter() - start) * 1000

    return decision, elapsed_ms
