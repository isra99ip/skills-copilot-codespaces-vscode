# API

## Estado actual

La API minima esta implementada con FastAPI en `src/betintel/api.py`.

Puede correr sin base de datos para calculos locales, o con `DATABASE_URL` para persistir predicciones y consultar senales de valor.

## Ejecutar localmente

```powershell
python -m pip install -e ".[dev]"
uvicorn betintel.api:app --reload
```

Con Postgres local:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://betintel:betintel@localhost:5432/betintel"
uvicorn betintel.api:app --reload
```

Con Docker en WSL:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_docker_wsl.ps1
```

Abrir:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

## Endpoints

### `GET /health`

Verifica que el servicio esta vivo y reporta el estado de la base de datos.

Respuesta sin `DATABASE_URL`:

```json
{
  "status": "ok",
  "service": "betintel-ai",
  "version": "0.1.0",
  "database": "not_configured"
}
```

Respuesta con base de datos disponible:

```json
{
  "status": "ok",
  "service": "betintel-ai",
  "version": "0.1.0",
  "database": "ok"
}
```

`database` puede ser `ok`, `not_configured` o `error`.

### `POST /predict`

Calcula probabilidad implicita, edge, EV y si existe valor segun una probabilidad del modelo y una cuota decimal. Si la API tiene `DATABASE_URL`, tambien guarda el registro.

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
  "is_value": true,
  "record_id": 1
}
```

`record_id` es `null` cuando la base de datos no esta configurada.

### `GET /value-signals`

Devuelve las ultimas senales donde `is_value = true` desde la base de datos.

Query params:

- `limit`: cantidad maxima de senales, entre 1 y 500. Valor por defecto: 50.

Response con datos:

```json
{
  "status": "ok",
  "signals": [
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
      "is_value": true,
      "record_id": 1
    }
  ],
  "note": "Senales persistidas desde /predict."
}
```

Si no hay base de datos configurada, devuelve `status: "not_configured"`. Si la base existe pero no hay senales, devuelve `status: "empty"`.

## Regla

Cuando se implemente un endpoint publico, este documento debe reflejar su contrato, validacion, respuesta y errores esperados.
