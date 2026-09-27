import pytest
from src.config.mcg import MCGConfig

def test_defaults():
    config = MCGConfig(theta_a=0.80, theta_b=0.30)
    assert config.theta_a == 0.80
    assert config.theta_b == 0.30
    assert config.top_k == 10

def test_invalid_threshold_order():
    with pytest.raises(ValueError):
        MCGConfig(theta_a=0.20, theta_b=0.30)

def test_invalid_top_k():
    with pytest.raises(ValueError):
        MCGConfig(theta_a=0.80, theta_b=0.30, top_k=0)
