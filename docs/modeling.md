# Modelado

## Principio base

BetIntel AI debe optimizar probabilidades y deteccion de valor, no solo aciertos binarios.

## Formulas iniciales

Probabilidad implicita de una cuota decimal:

```text
implied_probability = 1 / decimal_odds
```

Valor esperado por unidad apostada:

```text
expected_value = model_probability * decimal_odds - 1
```

Edge frente al mercado:

```text
edge = model_probability - implied_probability
```

Una senal se marca como valor cuando:

```text
edge >= min_edge and expected_value > 0
```

## Metricas iniciales

- Calibration gap.
- Log loss.
- Brier score.
- EV esperado.

## Reglas de modelado

- Usar cortes temporales para evitar leakage.
- Comparar siempre contra un baseline simple.
- No mezclar datos futuros en features o targets.
- Separar datos exploratorios de datos usados en evaluacion.
- No asumir que EV positivo en un dataset pequeno implica ventaja real.

## Smoketest

Ejecutar:

```powershell
python scripts/backtest_smoke.py
```

El smoketest valida que el pipeline base produce metricas finitas. No es una prueba de rentabilidad real.