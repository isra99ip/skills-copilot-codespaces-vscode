"""Calculos basicos de probabilidad, cuota y valor esperado."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValueSignal:
    """Resultado normalizado de una evaluacion de valor."""

    model_probability: float
    decimal_odds: float
    implied_probability: float
    edge: float
    expected_value: float
    is_value: bool


def validate_probability(probability: float) -> None:
    if not 0.0 <= probability <= 1.0:
        raise ValueError(f"probability fuera de rango: {probability!r}")


def validate_decimal_odds(decimal_odds: float) -> None:
    if decimal_odds <= 1.0:
        raise ValueError(f"decimal_odds debe ser mayor que 1.0: {decimal_odds!r}")


def implied_probability(decimal_odds: float) -> float:
    """Devuelve la probabilidad implicita de una cuota decimal."""

    validate_decimal_odds(decimal_odds)
    return 1.0 / decimal_odds


def expected_value(probability: float, decimal_odds: float) -> float:
    """Calcula EV por unidad apostada usando cuota decimal."""

    validate_probability(probability)
    validate_decimal_odds(decimal_odds)
    return probability * decimal_odds - 1.0


def evaluate_value_signal(
    model_probability: float,
    decimal_odds: float,
    *,
    min_edge: float = 0.0,
) -> ValueSignal:
    """Evalua si una prediccion supera la probabilidad implicita de mercado."""

    validate_probability(model_probability)
    validate_decimal_odds(decimal_odds)
    market_probability = implied_probability(decimal_odds)
    edge = model_probability - market_probability
    ev = expected_value(model_probability, decimal_odds)
    return ValueSignal(
        model_probability=model_probability,
        decimal_odds=decimal_odds,
        implied_probability=market_probability,
        edge=edge,
        expected_value=ev,
        is_value=edge >= min_edge and ev > 0.0,
    )