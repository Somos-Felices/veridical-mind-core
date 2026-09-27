from src.mcg.classifier import classify, calculate_icr


def test_category_a_high_support():
    decision = classify(
        [0.95, 0.90, 0.85],
        theta_a=0.80,
        theta_b=0.30,
        top_k=10,
    )

    assert decision.category == "A"
    assert decision.llm_allowed is True
    assert decision.ir_max == 0.95


def test_category_b_partial_support():
    decision = classify(
        [0.55, 0.50, 0.45],
        theta_a=0.80,
        theta_b=0.30,
        top_k=10,
    )

    assert decision.category == "B"
    assert decision.llm_allowed is True
    assert decision.icr is not None


def test_category_c_insufficient_support():
    decision = classify(
        [0.20, 0.15, 0.10],
        theta_a=0.80,
        theta_b=0.30,
        top_k=10,
    )

    assert decision.category == "C"
    assert decision.llm_allowed is False
    assert decision.icr is None


def test_icr_formula():
    values = [0.5, 0.25, 0.25]

    expected = (
        (0.5 ** 2)
        + (0.25 ** 2)
        + (0.25 ** 2)
    ) / sum(values)

    assert calculate_icr(values) == expected


def test_top_k_applied_before_average():
    decision = classify(
        [0.50, 0.40, 0.35, 0.01],
        theta_a=0.80,
        theta_b=0.30,
        top_k=3,
    )

    assert decision.ir_avg == (0.50 + 0.40 + 0.35) / 3
