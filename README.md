# skills-copilot-codespaces-vscode

Repositorio base para usar GitHub Copilot, GitHub Copilot CLI, VS Code y Codespaces como entorno de trabajo para BetIntel AI.

## Base de BetIntel AI

Este repo ya incluye un MVP tecnico inicial:

- API FastAPI con `GET /health`, `POST /predict` y `GET /value-signals`.
- Dashboard Streamlit minimo para explorar probabilidad, cuota y EV.
- Paquete Python bajo `src/betintel/`.
- CI con `ruff`, `pytest`, import de API y smoketest de backtest.
- Dockerfiles para API y dashboard.
- `docker-compose.yml` con API, dashboard y Postgres.
- Documentacion inicial de API, modelado, datos y modelo operativo.
- Dev Container con Python 3.12 y extensiones recomendadas.

## Primer uso

1. Abre una terminal nueva para que Windows recargue el `PATH`.
2. Entra al repositorio:

   ```powershell
   cd C:\Users\isra9\Documents\GitHub\skills-copilot-codespaces-vscode
   ```

3. Instala dependencias de desarrollo:

   ```powershell
   python -m pip install -e ".[dev]"
   ```

4. Ejecuta validacion local:

   ```powershell
   ruff check .
   pytest -q
   python scripts\backtest_smoke.py
   ```

## Ejecutar la API

```powershell
uvicorn betintel.api:app --reload
```

Abrir:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

Ejemplo:

```powershell
$body = @{
  event_id = "match-001"
  market = "match_winner"
  selection = "home"
  model_probability = 0.58
  decimal_odds = 2.05
  min_edge = 0.02
} | ConvertTo-Json -Compress

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/predict" -ContentType "application/json" -Body $body
```

## Ejecutar el dashboard

```powershell
streamlit run apps\dashboard\app.py
```

## Docker Compose

```powershell
docker compose up --build
```

Servicios esperados:

- API: http://127.0.0.1:8000
- Dashboard: http://127.0.0.1:8501
- Postgres: localhost:5432

## Copilot CLI

```powershell
copilot
copilot -i "lee AGENTS.md y docs/modelo-betintel-ai-github-education.md y dime el siguiente paso tecnico"
copilot -i "implementa el siguiente endpoint manteniendo tests y docs actualizados"
```

Usa `--allow-all` o `--yolo` solo en tareas acotadas y revisables.

## Archivos incluidos

- `.github/copilot-instructions.md`: instrucciones generales para Copilot en este repositorio.
- `.github/instructions/markdown.instructions.md`: reglas para archivos Markdown.
- `.github/workflows/ci.yml`: validacion automatica para lint, pruebas, API y smoketest.
- `.github/prompts/review-repo.prompt.md`: prompt reutilizable para revisar un repo.
- `.github/prompts/create-plan.prompt.md`: prompt reutilizable para generar un plan de trabajo.
- `.devcontainer/devcontainer.json`: entorno base para GitHub Codespaces y Dev Containers.
- `.vscode/extensions.json`: extensiones recomendadas.
- `.vscode/settings.json`: ajustes del workspace.
- `AGENTS.md`: reglas para agentes CLI que trabajen en el repositorio.
- `apps/api/Dockerfile`: imagen runtime para la API.
- `apps/dashboard/app.py`: dashboard Streamlit inicial.
- `docs/api.md`: contrato actual de la API.
- `docs/data-policy.md`: reglas de uso y origen de datos.
- `docs/modeling.md`: principios iniciales de modelado y metricas.
- `docs/modelo-betintel-ai-github-education.md`: modelo operativo derivado de la investigacion PDF.
- `.codex/config.toml`: configuracion local sugerida para agentes tipo Codex.

## Publicar cambios

```powershell
git status
git add .
git commit -m "Create BetIntel AI MVP scaffold"
git push origin main
```