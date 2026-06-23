from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from betintel.api import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


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


def test_value_signals_is_empty_until_ingestion_exists(client: TestClient) -> None:
    response = client.get("/value-signals")

    assert response.status_code == 200
    assert response.json()["signals"] == []