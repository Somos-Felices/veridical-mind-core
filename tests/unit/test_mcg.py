from src.mcg import calculate_icr, classify


def test_icr():
    values = [0.8, 0.4]

    expected = (0.8**2 + 0.4**2) / (0.8 + 0.4)

    assert calculate_icr(values) == expected


def test_category_a():
    decision = classify(
        ir_values=[0.80, 0.20],
        theta_a=0.75,
        theta_b=0.30,
    )

    assert decision.category == "A"
    assert decision.llm_allowed is True
    assert decision.icr is None


def test_category_b():
    decision = classify(
        ir_values=[0.60, 0.50, 0.40],
        theta_a=0.75,
        theta_b=0.45,
    )

    assert decision.category == "B"
    assert decision.llm_allowed is True
    assert decision.icr is not None


def test_category_c():
    decision = classify(
        ir_values=[0.20, 0.10, 0.05],
        theta_a=0.75,
        theta_b=0.40,
    )

    assert decision.category == "C"
    assert decision.llm_allowed is False
    assert decision.icr is None


def test_top_k_is_used_for_category_b():
    decision = classify(
        ir_values=[0.60, 0.50, 0.40, 0.01],
        theta_a=0.75,
        theta_b=0.45,
        top_k=3,
    )

    assert decision.category == "B"
    assert decision.ir_avg == 0.50
