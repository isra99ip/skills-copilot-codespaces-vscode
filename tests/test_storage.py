from __future__ import annotations

from betintel.odds import evaluate_value_signal
from betintel.storage import build_engine, ensure_schema, list_value_signals, save_prediction


def test_save_and_list_value_signal() -> None:
    engine = build_engine("sqlite+pysqlite:///:memory:")
    ensure_schema(engine)
    signal = evaluate_value_signal(0.58, 2.05, min_edge=0.02)

    record_id = save_prediction(
        engine,
        event_id="match-001",
        market="match_winner",
        selection="home",
        model_name="baseline-smoke",
        signal=signal,
    )

    assert record_id == 1
    rows = list_value_signals(engine)
    assert len(rows) == 1
    assert rows[0]["event_id"] == "match-001"
    assert rows[0]["is_value"] is True