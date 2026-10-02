from src.config.mcg import MCGConfig


def test_valid_config():
    config = MCGConfig(
        theta_a=0.80,
        theta_b=0.30,
        top_k=10,
    )

    assert config.theta_a == 0.80
    assert config.theta_b == 0.30
    assert config.top_k == 10


def test_rejects_theta_a_below_theta_b():
    try:
        MCGConfig(theta_a=0.20, theta_b=0.30)
    except ValueError as exc:
        assert "theta_a must be >= theta_b" in str(exc)
    else:
        raise AssertionError("invalid threshold ordering must fail")


def test_rejects_threshold_above_one():
    try:
        MCGConfig(theta_a=1.01, theta_b=0.30)
    except ValueError as exc:
        assert "between 0 and 1" in str(exc)
    else:
        raise AssertionError("theta_a > 1 must fail")


def test_rejects_negative_threshold():
    try:
        MCGConfig(theta_a=0.80, theta_b=-0.01)
    except ValueError as exc:
        assert "between 0 and 1" in str(exc)
    else:
        raise AssertionError("negative theta_b must fail")


def test_rejects_invalid_top_k():
    try:
        MCGConfig(theta_a=0.80, theta_b=0.30, top_k=0)
    except ValueError as exc:
        assert "top_k must be >= 1" in str(exc)
    else:
        raise AssertionError("top_k < 1 must fail")
