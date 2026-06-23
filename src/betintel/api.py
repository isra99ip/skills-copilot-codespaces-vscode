"""API FastAPI minima para BetIntel AI."""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.engine import Engine

from betintel import __version__
from betintel.odds import evaluate_value_signal
from betintel.storage import (
    build_engine,
    check_database,
    ensure_schema,
    get_database_url,
    list_value_signals,
    save_prediction,
)


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str
    database: Literal["ok", "not_configured", "error"]


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
    record_id: int | None = None


class ValueSignalsResponse(BaseModel):
    status: Literal["ok", "empty", "not_configured"]
    signals: list[PredictionResponse]
    note: str


def _get_engine(app: FastAPI) -> Engine | None:
    engine = getattr(app.state, "engine", None)
    if isinstance(engine, Engine):
        return engine
    return None


def create_app(database_url: str | None = None) -> FastAPI:
    app = FastAPI(
        title="BetIntel AI API",
        version=__version__,
        summary="API minima para prediccion probabilistica y senales de valor.",
    )

    resolved_database_url = database_url if database_url is not None else get_database_url()
    app.state.engine = None
    if resolved_database_url:
        engine = build_engine(resolved_database_url)
        ensure_schema(engine)
        app.state.engine = engine

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        engine = _get_engine(app)
        database_status: Literal["ok", "not_configured", "error"] = "not_configured"
        if engine is not None:
            try:
                check_database(engine)
                database_status = "ok"
            except Exception:
                database_status = "error"
        return HealthResponse(
            status="ok",
            service="betintel-ai",
            version=__version__,
            database=database_status,
        )

    @app.post("/predict", response_model=PredictionResponse)
    def predict(payload: PredictionRequest) -> PredictionResponse:
        signal = evaluate_value_signal(
            payload.model_probability,
            payload.decimal_odds,
            min_edge=payload.min_edge,
        )
        record_id = None
        engine = _get_engine(app)
        if engine is not None:
            record_id = save_prediction(
                engine,
                event_id=payload.event_id,
                market=payload.market,
                selection=payload.selection,
                model_name=payload.model_name,
                signal=signal,
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
            record_id=record_id,
        )

    @app.get("/value-signals", response_model=ValueSignalsResponse)
    def value_signals(limit: int = Query(default=50, ge=1, le=500)) -> ValueSignalsResponse:
        engine = _get_engine(app)
        if engine is None:
            return ValueSignalsResponse(
                status="not_configured",
                signals=[],
                note="DATABASE_URL no esta configurado.",
            )

        rows = list_value_signals(engine, limit=limit)
        signals = [
            PredictionResponse(
                event_id=row["event_id"],
                market=row["market"],
                selection=row["selection"],
                model_name=row["model_name"],
                model_probability=row["model_probability"],
                decimal_odds=row["decimal_odds"],
                implied_probability=row["implied_probability"],
                edge=row["edge"],
                expected_value=row["expected_value"],
                is_value=row["is_value"],
                record_id=row["id"],
            )
            for row in rows
        ]
        return ValueSignalsResponse(
            status="ok" if signals else "empty",
            signals=signals,
            note="Senales persistidas desde /predict.",
        )

    return app


app = create_app()