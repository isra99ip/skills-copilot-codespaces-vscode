"""BetIntel AI base package."""

from .odds import ValueSignal, evaluate_value_signal, expected_value, implied_probability
from .smoke import BacktestPoint, SmokeSummary, build_smoke_backtest, run_smoke_backtest

__all__ = [
    "BacktestPoint",
    "SmokeSummary",
    "ValueSignal",
    "build_smoke_backtest",
    "evaluate_value_signal",
    "expected_value",
    "implied_probability",
    "run_smoke_backtest",
]

__version__ = "0.1.0"