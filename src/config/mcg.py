import os
from dataclasses import dataclass

@dataclass(frozen=True)
class MCGConfig:
    theta_a: float
    theta_b: float
    top_k: int = 10

    def __post_init__(self):
        if self.theta_a < self.theta_b:
            raise ValueError("theta_a must be >= theta_b")
        if self.top_k < 1:
            raise ValueError("top_k must be >= 1")

def load_mcg_config() -> MCGConfig:
    return MCGConfig(
        theta_a=float(os.getenv("MCG_THETA_A", "0.80")),
        theta_b=float(os.getenv("MCG_THETA_B", "0.30")),
        top_k=int(os.getenv("MCG_TOP_K", "10")),
    )
