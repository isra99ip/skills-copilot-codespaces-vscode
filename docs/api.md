# API

## Estado actual

La API minima esta implementada con FastAPI en `src/betintel/api.py`.

## Ejecutar localmente

```powershell
python -m pip install -e ".[dev]"
uvicorn betintel.api:app --reload
```

Abrir:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

## Endpoints

### `GET /health`

Verifica que el servicio esta vivo.

Respuesta:

```json
{
  "status": "ok",
  "service": "betintel-ai",
  "version": "0.1.0"
}
```

### `POST /predict`

Calcula probabilidad implicita, edge, EV y si existe valor segun una probabilidad del modelo y una cuota decimal.

Request:

```json
{
  "event_id": "match-001",
  "market": "match_winner",
  "selection": "home",
  "model_probability": 0.58,
  "decimal_odds": 2.05,
  "min_edge": 0.02,
  "model_name": "baseline-smoke"
}
```

Response:

```json
{
  "event_id": "match-001",
  "market": "match_winner",
  "selection": "home",
  "model_name": "baseline-smoke",
  "model_probability": 0.58,
  "decimal_odds": 2.05,
  "implied_probability": 0.48780487804878053,
  "edge": 0.09219512195121944,
  "expected_value": 0.189,
  "is_value": true
}
```

### `GET /value-signals`

Devuelve una lista vacia por ahora. Se deja como contrato inicial para conectar ingesta y persistencia despues.

## Regla

Cuando se implemente un endpoint publico, este documento debe reflejar su contrato, validacion, respuesta y errores esperados.