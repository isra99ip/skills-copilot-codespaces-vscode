from __future__ import annotations

import json

from betintel.smoke import BacktestPoint, build_smoke_backtest, run_smoke_backtest


def test_build_smoke_backtest_returns_expected_metrics() -> None:
    summary = build_smoke_backtest()

    assert summary.samples == 4
    assert 0.0 < summary.log_loss < 1.0
    assert 0.0 < summary.brier_score < 1.0
    assert summary.average_expected_value > 0.0
    assert 0.0 <= summary.positive_value_rate <= 1.0
    assert summary.calibration_gap >= 0.0


def test_run_smoke_backtest_writes_json(tmp_path) -> None:
    output = tmp_path / "backtest_summary.json"

    summary = run_smoke_backtest(output)

    assert output.exists()
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["samples"] == summary.samples
    assert payload["calibration_gap"] == summary.calibration_gap


def test_build_smoke_backtest_rejects_empty_input() -> None:
    try:
        build_smoke_backtest([])
    except ValueError as exc:
        assert "smoketest" in str(exc)
    else:
        raise AssertionError("Se esperaba ValueError")


def test_build_smoke_backtest_accepts_custom_points() -> None:
    summary = build_smoke_backtest(
        [BacktestPoint(probability=0.7, outcome=1, decimal_odds=1.8)]
    )

    assert summary.samples == 1
    assert summary.average_expected_value > 0.0
