"""Smoketest de backtest para la base inicial de BetIntel AI."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from json import dumps
from math import log
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True, slots=True)
class BacktestPoint:
    probability: float
    outcome: int
    decimal_odds: float


@dataclass(frozen=True, slots=True)
class SmokeSummary:
    samples: int
    log_loss: float
    brier_score: float
    average_expected_value: float
    positive_value_rate: float
    predicted_mean: float
    observed_rate: float
    calibration_gap: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


DEFAULT_POINTS: tuple[BacktestPoint, ...] = (
    BacktestPoint(probability=0.62, outcome=1, decimal_odds=1.90),
    BacktestPoint(probability=0.55, outcome=0, decimal_odds=2.05),
    BacktestPoint(probability=0.44, outcome=1, decimal_odds=2.00),
    BacktestPoint(probability=0.72, outcome=1, decimal_odds=1.60),
)


def _clamp_probability(probability: float) -> float:
    epsilon = 1e-15
    return min(max(probability, epsilon), 1.0 - epsilon)


def _validate_point(point: BacktestPoint) -> None:
    if not 0.0 <= point.probability <= 1.0:
        raise ValueError(f"probability fuera de rango: {point.probability!r}")
    if point.outcome not in (0, 1):
        raise ValueError(f"outcome invalido: {point.outcome!r}")
    if point.decimal_odds <= 1.0:
        raise ValueError(f"decimal_odds debe ser mayor que 1.0: {point.decimal_odds!r}")


def build_smoke_backtest(
    points: Iterable[BacktestPoint] = DEFAULT_POINTS,
) -> SmokeSummary:
    items = tuple(points)
    if not items:
        raise ValueError("Se requiere al menos un punto para el smoketest.")

    for point in items:
        _validate_point(point)

    samples = len(items)
    predicted_sum = sum(point.probability for point in items)
    observed_sum = sum(point.outcome for point in items)

    log_loss = 0.0
    brier_score = 0.0
    expected_value_sum = 0.0
    positive_value_count = 0

    for point in items:
        probability = _clamp_probability(point.probability)
        outcome = point.outcome

        log_loss += -(outcome * log(probability) + (1 - outcome) * log(1 - probability))
        brier_score += (point.probability - outcome) ** 2

        expected_value = point.probability * point.decimal_odds - 1.0
        expected_value_sum += expected_value
        if expected_value > 0.0:
            positive_value_count += 1

    predicted_mean = predicted_sum / samples
    observed_rate = observed_sum / samples

    summary = SmokeSummary(
        samples=samples,
        log_loss=log_loss / samples,
        brier_score=brier_score / samples,
        average_expected_value=expected_value_sum / samples,
        positive_value_rate=positive_value_count / samples,
        predicted_mean=predicted_mean,
        observed_rate=observed_rate,
        calibration_gap=abs(predicted_mean - observed_rate),
    )
    return summary


def run_smoke_backtest(output_path: str | Path | None = None) -> SmokeSummary:
    summary = build_smoke_backtest()
    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            dumps(summary.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return summary
