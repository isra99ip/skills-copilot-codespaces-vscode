from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from betintel.api import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


@pytest.fixture()
def db_client() -> TestClient:
    return TestClient(create_app("sqlite+pysqlite:///:memory:"))


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["database"] == "not_configured"


def test_health_with_database(db_client: TestClient) -> None:
    response = db_client.get("/health")

    assert response.status_code == 200
    assert response.json()["database"] == "ok"


def test_predict_returns_value_metrics(client: TestClient) -> None:
    response = client.post(
        "/predict",
        json={
            "event_id": "match-001",
            "market": "match_winner",
            "selection": "home",
            "model_probability": 0.58,
            "decimal_odds": 2.05,
            "min_edge": 0.02,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["event_id"] == "match-001"
    assert payload["implied_probability"] == pytest.approx(1 / 2.05)
    assert payload["expected_value"] == pytest.approx(0.189)
    assert payload["is_value"] is True
    assert payload["record_id"] is None


def test_predict_persists_when_database_is_configured(db_client: TestClient) -> None:
    response = db_client.post(
        "/predict",
        json={
            "event_id": "match-001",
            "market": "match_winner",
            "selection": "home",
            "model_probability": 0.58,
            "decimal_odds": 2.05,
            "min_edge": 0.02,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["record_id"] == 1

    signals = db_client.get("/value-signals")
    assert signals.status_code == 200
    signal_payload = signals.json()
    assert signal_payload["status"] == "ok"
    assert signal_payload["signals"][0]["event_id"] == "match-001"


def test_predict_validates_payload(client: TestClient) -> None:
    response = client.post(
        "/predict",
        json={
            "event_id": "match-001",
            "market": "match_winner",
            "selection": "home",
            "model_probability": 1.5,
            "decimal_odds": 2.05,
        },
    )

    assert response.status_code == 422


def test_value_signals_requires_database(client: TestClient) -> None:
    response = client.get("/value-signals")

    assert response.status_code == 200
    assert response.json()["status"] == "not_configured"