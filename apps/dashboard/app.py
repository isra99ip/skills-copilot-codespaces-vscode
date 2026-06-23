"""Dashboard Streamlit minimo para explorar senales de valor."""

from __future__ import annotations

import streamlit as st

from betintel.odds import evaluate_value_signal

st.set_page_config(page_title="BetIntel AI", page_icon="BI", layout="wide")

st.title("BetIntel AI")
st.caption("MVP para evaluar probabilidad, cuota decimal y valor esperado.")

left, right = st.columns(2)
with left:
    model_probability = st.slider(
        "Probabilidad del modelo",
        min_value=0.0,
        max_value=1.0,
        value=0.58,
        step=0.01,
    )
    decimal_odds = st.number_input(
        "Cuota decimal",
        min_value=1.01,
        value=2.05,
        step=0.01,
    )
with right:
    min_edge = st.slider(
        "Edge minimo",
        min_value=0.0,
        max_value=0.25,
        value=0.02,
        step=0.01,
    )

signal = evaluate_value_signal(
    model_probability,
    decimal_odds,
    min_edge=min_edge,
)

metric_cols = st.columns(4)
metric_cols[0].metric("Prob. implicita", f"{signal.implied_probability:.2%}")
metric_cols[1].metric("Edge", f"{signal.edge:.2%}")
metric_cols[2].metric("EV", f"{signal.expected_value:.3f}")
metric_cols[3].metric("Valor", "Si" if signal.is_value else "No")

st.json(
    {
        "model_probability": signal.model_probability,
        "decimal_odds": signal.decimal_odds,
        "implied_probability": signal.implied_probability,
        "edge": signal.edge,
        "expected_value": signal.expected_value,
        "is_value": signal.is_value,
    }
)