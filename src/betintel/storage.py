"""Persistencia minima de predicciones y senales de valor."""

from __future__ import annotations

import os
from collections.abc import Sequence
from typing import Any

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    desc,
    func,
    insert,
    select,
)
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool

from betintel.odds import ValueSignal

metadata = MetaData()

prediction_events = Table(
    "prediction_events",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("event_id", String(128), nullable=False, index=True),
    Column("market", String(128), nullable=False, index=True),
    Column("selection", String(128), nullable=False),
    Column("model_name", String(128), nullable=False),
    Column("model_probability", Float, nullable=False),
    Column("decimal_odds", Float, nullable=False),
    Column("implied_probability", Float, nullable=False),
    Column("edge", Float, nullable=False),
    Column("expected_value", Float, nullable=False),
    Column("is_value", Boolean, nullable=False, index=True),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)


def get_database_url() -> str | None:
    return os.getenv("DATABASE_URL") or None


def build_engine(database_url: str) -> Engine:
    kwargs: dict[str, Any] = {"pool_pre_ping": true_if_not_sqlite_memory(database_url)}
    if database_url == "sqlite+pysqlite:///:memory:":
        kwargs.update(
            {
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,
            }
        )
    return create_engine(database_url, **kwargs)


def true_if_not_sqlite_memory(database_url: str) -> bool:
    return database_url != "sqlite+pysqlite:///:memory:"


def ensure_schema(engine: Engine) -> None:
    metadata.create_all(engine)


def save_prediction(
    engine: Engine,
    *,
    event_id: str,
    market: str,
    selection: str,
    model_name: str,
    signal: ValueSignal,
) -> int | None:
    statement = insert(prediction_events).values(
        event_id=event_id,
        market=market,
        selection=selection,
        model_name=model_name,
        model_probability=signal.model_probability,
        decimal_odds=signal.decimal_odds,
        implied_probability=signal.implied_probability,
        edge=signal.edge,
        expected_value=signal.expected_value,
        is_value=signal.is_value,
    )
    with engine.begin() as connection:
        result = connection.execute(statement)
        inserted = result.inserted_primary_key
        if inserted:
            return int(inserted[0])
    return None


def list_value_signals(engine: Engine, *, limit: int = 50) -> list[dict[str, Any]]:
    statement = (
        select(prediction_events)
        .where(prediction_events.c.is_value.is_(True))
        .order_by(desc(prediction_events.c.created_at), desc(prediction_events.c.id))
        .limit(limit)
    )
    with engine.begin() as connection:
        rows: Sequence[Any] = connection.execute(statement).mappings().all()
    return [dict(row) for row in rows]


def check_database(engine: Engine) -> bool:
    with engine.begin() as connection:
        connection.execute(select(1))
    return True