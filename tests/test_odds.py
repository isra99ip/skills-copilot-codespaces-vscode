from __future__ import annotations

import pytest

from betintel.odds import evaluate_value_signal, expected_value, implied_probability


def test_implied_probability_from_decimal_odds() -> None:
    assert implied_probability(2.0) == pytest.approx(0.5)


def test_expected_value_positive_when_model_beats_market() -> None:
    assert expected_value(0.58, 2.05) == pytest.approx(0.189)


def test_value_signal_respects_min_edge() -> None:
    signal = evaluate_value_signal(0.58, 2.05, min_edge=0.02)

    assert signal.implied_probability == pytest.approx(1 / 2.05)
    assert signal.edge == pytest.approx(0.58 - (1 / 2.05))
    assert signal.expected_value == pytest.approx(0.189)
    assert signal.is_value is True


def test_value_signal_rejects_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        evaluate_value_signal(1.2, 2.0)
    with pytest.raises(ValueError):
        evaluate_value_signal(0.5, 1.0)