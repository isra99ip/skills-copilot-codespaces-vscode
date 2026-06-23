"""API FastAPI minima para BetIntel AI."""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

from betintel import __version__
from betintel.odds import evaluate_value_signal


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str


class PredictionRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    event_id: str = Field(..., min_length=1, examples=["match-2026-001"])
    market: str = Field(..., min_length=1, examples=["match_winner"])
    selection: str = Field(..., min_length=1, examples=["home"])
    model_probability: float = Field(..., ge=0.0, le=1.0, examples=[0.58])
    decimal_odds: float = Field(..., gt=1.0, examples=[2.05])
    min_edge: float = Field(default=0.0, ge=0.0, le=1.0)
    model_name: str = Field(default="baseline-smoke", min_length=1)


class PredictionResponse(BaseModel):
    event_id: str
    market: str
    selection: str
    model_name: str
    model_probability: float
    decimal_odds: float
    implied_probability: float
    edge: float
    expected_value: float
    is_value: bool


class ValueSignalsResponse(BaseModel):
    status: Literal["empty"]
    signals: list[PredictionResponse]
    note: str


def create_app() -> FastAPI:
    app = FastAPI(
        title="BetIntel AI API",
        version=__version__,
        summary="API minima para prediccion probabilistica y senales de valor.",
    )

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok", service="betintel-ai", version=__version__)

    @app.post("/predict", response_model=PredictionResponse)
    def predict(payload: PredictionRequest) -> PredictionResponse:
        signal = evaluate_value_signal(
            payload.model_probability,
            payload.decimal_odds,
            min_edge=payload.min_edge,
        )
        return PredictionResponse(
            event_id=payload.event_id,
            market=payload.market,
            selection=payload.selection,
            model_name=payload.model_name,
            model_probability=signal.model_probability,
            decimal_odds=signal.decimal_odds,
            implied_probability=signal.implied_probability,
            edge=signal.edge,
            expected_value=signal.expected_value,
            is_value=signal.is_value,
        )

    @app.get("/value-signals", response_model=ValueSignalsResponse)
    def value_signals() -> ValueSignalsResponse:
        return ValueSignalsResponse(
            status="empty",
            signals=[],
            note="No hay ingesta de datos configurada todavia.",
        )

    return app


app = create_app()