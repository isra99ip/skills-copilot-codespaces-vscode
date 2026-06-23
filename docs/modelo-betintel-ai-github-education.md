# Modelo operativo: BetIntel AI con GitHub Education Pack

Este documento convierte la investigacion del PDF `Como aprovechar GitHub Education Pack para BetIntel AI` en un modelo de trabajo accionable para el repositorio y para el uso de GitHub Copilot CLI, Codespaces y servicios del GitHub Student Developer Pack.

## Objetivo

Construir un MVP de BetIntel AI: un sistema de prediccion probabilistica y deteccion de valor en cuotas deportivas, con desarrollo reproducible, CI/CD, despliegue simple, observabilidad basica y control de riesgos legales de datos.

El Pack no debe usarse activando todo a la vez. La estrategia recomendada es usar primero lo que reduce friccion real del MVP:

1. GitHub Pro para repositorio, ramas protegidas, environments, Actions, Packages y Codespaces.
2. GitHub Actions para calidad, pruebas y backtesting liviano.
3. GitHub Codespaces para entorno reproducible.
4. GHCR/GitHub Packages para imagenes Docker delgadas.
5. DigitalOcean o Heroku para despliegue.
6. Sentry para errores y trazas basicas.
7. Deepnote, Datadog, MongoDB, Zyte o Azure solo cuando el MVP lo justifique.

## Arquitectura minima recomendada

```text
Desarrollo
  VS Code / Codespaces / Copilot CLI
  .github/copilot-instructions.md
  AGENTS.md

Repositorio
  main protegida
  staging protegida
  pull requests obligatorias
  CODEOWNERS
  environments: staging, production
  secrets por environment

CI/CD
  GitHub Actions
  ruff / pytest / mypy
  backtest_smoke
  build Docker
  publish GHCR

Runtime MVP
  FastAPI: API de probabilidades y senales
  Streamlit: dashboard interno o demo
  Postgres: datos estructurados y resultados
  Sentry: errores y trazas
  Heroku: staging rapido
  DigitalOcean: produccion ligera o runner propio
```

## Pila inicial

| Capa | Eleccion inicial | Razon |
| --- | --- | --- |
| Repo | GitHub privado personal | GitHub Pro via Education cubre mejor el MVP personal. |
| IDE | VS Code + Copilot + Codespaces | Misma experiencia local y cloud. |
| Agente CLI | GitHub Copilot CLI | Tareas desde terminal, edicion, explicacion y revision. |
| Backend | FastAPI | API ligera para probabilidades, backtests y senales. |
| Dashboard | Streamlit | Rapido para demo interna y lectura de resultados. |
| DB | Postgres | Base solida para eventos, odds, resultados y features. |
| CI | GitHub Actions | Pruebas, lint, smoke backtests y artefactos. |
| Contenedores | Docker + GHCR | Imagenes versionadas por commit y rama. |
| Staging | Heroku | Despliegue rapido con credito mensual. |
| Produccion ligera | DigitalOcean | Mas control para API, worker, DB o runner propio. |
| Observabilidad | Sentry primero | Mejor retorno temprano que observabilidad completa. |

## Prioridad de beneficios

| Recurso | Prioridad | Uso en BetIntel AI | Activar ahora |
| --- | --- | --- | --- |
| GitHub Pro | Muy alta | Repo privado, Actions, Packages, Codespaces, protections. | Si |
| GitHub Actions | Muy alta | CI, smoke tests, backtests cortos, deploy. | Si |
| GitHub Codespaces | Muy alta | Entorno reproducible para desarrollo. | Si |
| GHCR/Packages | Alta | Imagenes Docker delgadas. | Si |
| DigitalOcean | Alta | Produccion ligera, runner, DB, jobs. | Si |
| Heroku | Alta | Staging/demo rapido. | Si |
| Sentry | Alta | Errores, trazas y releases por commit. | Si |
| Deepnote | Media | Analisis y notebooks colaborativos. | Despues |
| Datadog | Media | Host metrics, CI Visibility, deploy gates. | Despues |
| MongoDB Atlas | Media | Snapshots JSON si Postgres no basta. | Evaluar |
| Zyte | Baja | Scraping cloud solo con fuente permitida. | No sin validar TOS |
| Azure | Baja | Respaldo de cloud. | No si DO/Heroku bastan |

## Estructura de repositorio recomendada

```text
betintel-ai/
  .devcontainer/
    devcontainer.json
  .github/
    workflows/
      ci.yml
      deploy.yml
    copilot-instructions.md
  apps/
    api/
      app/
      Dockerfile
    dashboard/
      app.py
      Dockerfile
  src/
    betintel/
      data/
      features/
      modeling/
      value/
  scripts/
    backtest_smoke.py
    ingest_sample.py
  tests/
  docs/
    api.md
    modeling.md
    data-policy.md
  AGENTS.md
  docker-compose.yml
  pyproject.toml
```

## Workflow de trabajo con Copilot CLI

Trabaja desde el directorio del repo:

```powershell
cd C:\Users\isra9\Documents\GitHub\skills-copilot-codespaces-vscode
copilot
```

Prompts iniciales utiles:

```powershell
copilot -i "lee AGENTS.md y revisa si la estructura del repo cumple el modelo operativo"
copilot -i "crea un plan para convertir este repo en betintel-ai siguiendo docs/modelo-betintel-ai-github-education.md"
copilot -i "genera los workflows ci.yml y deploy.yml para FastAPI, Streamlit, Docker y GHCR"
copilot -i "revisa riesgos de seguridad y secretos en este repositorio"
```

Para una tarea directa sin chat interactivo:

```powershell
copilot -p "resume el modelo operativo y crea una checklist de implementacion" --allow-all-tools
```

Usa `--allow-all` o `--yolo` solo en tareas controladas. Para tareas que puedan tocar despliegues, credenciales o archivos grandes, pide revision antes de aceptar cambios.

## Reglas de calidad

Antes de hacer merge:

```powershell
ruff check .
pytest -q
python scripts/backtest_smoke.py
```

Si el cambio toca modelado, revisar:

- Calibracion.
- Log loss.
- Brier score.
- EV esperado.
- Riesgo de leakage.
- Comparacion contra baseline.

Si el cambio toca API, revisar:

- Contratos de endpoints.
- Manejo de errores.
- Validacion de entrada.
- Documentacion en `docs/api.md`.

## CI recomendado

```yaml
name: ci

on:
  pull_request:
  push:
    branches: [main, staging]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: betintel
          POSTGRES_PASSWORD: betintel
          POSTGRES_DB: betintel_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd="pg_isready -U betintel -d betintel_test"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5
    env:
      DATABASE_URL: postgresql://betintel:betintel@localhost:5432/betintel_test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ runner.os }}-${{ hashFiles('pyproject.toml') }}
      - run: python -m pip install -e ".[dev]"
      - run: ruff check .
      - run: pytest -q --maxfail=1
      - run: python scripts/backtest_smoke.py --output artifacts/backtest_summary.json
      - uses: actions/upload-artifact@v4
        with:
          name: backtest-summary
          path: artifacts/backtest_summary.json
```

## Secrets y environments

Crear environments:

- `staging`
- `production`

Secrets minimos:

- `DATABASE_URL`
- `SENTRY_DSN`
- `HEROKU_API_KEY` o credenciales DigitalOcean
- `GHCR_TOKEN` si no basta `GITHUB_TOKEN`
- tokens de proveedores de datos autorizados

Reglas:

- No poner secretos en `.env` versionado.
- No subir datasets brutos.
- No usar GitHub Packages como storage de historicos.
- Production debe requerir aprobacion manual.

## Docker Compose minimo

```yaml
version: "3.9"

services:
  api:
    image: ghcr.io/YOUR_GITHUB_USER/betintel-api:latest
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  dashboard:
    image: ghcr.io/YOUR_GITHUB_USER/betintel-dashboard:latest
    env_file:
      - .env
    ports:
      - "8501:8501"
    depends_on:
      - api

  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: betintel
      POSTGRES_PASSWORD: betintel
      POSTGRES_DB: betintel
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  pgdata:
```

## Plan de 4 semanas

### Semana 1

- Activar GitHub Education y confirmar GitHub Pro.
- Redimir DigitalOcean, Heroku y Sentry.
- Crear repo privado `betintel-ai`.
- Configurar `main`, `staging`, CODEOWNERS y environments.
- Agregar `AGENTS.md`, `.github/copilot-instructions.md` y `.devcontainer/`.

### Semana 2

- Crear API FastAPI minima.
- Crear dashboard Streamlit minimo.
- Montar Postgres en desarrollo.
- Crear workflow `ci.yml`.
- Publicar primera imagen Docker en GHCR.

### Semana 3

- Implementar `backtest_smoke.py`.
- Guardar artefactos de backtest en GitHub Actions.
- Medir consumo de minutos y decidir si hace falta runner en DigitalOcean.
- Activar Sentry en FastAPI y dashboard.

### Semana 4

- Desplegar staging en Heroku.
- Preparar produccion ligera en DigitalOcean.
- Evaluar Datadog solo si ya hay servicios estables.
- Evaluar MongoDB solo si los snapshots JSON lo justifican.
- Documentar politica de datos y fuentes autorizadas.

## Riesgos principales

### Datos deportivos

El riesgo mayor no es tecnico: es legal y contractual. No automatizar scraping ni extraccion masiva sin revisar terminos de uso de cada fuente. Priorizar:

1. APIs oficiales.
2. Fuentes con licencia.
3. Datos propios.
4. Scraping solo si los terminos lo permiten expresamente.

### Costos y cuotas

GitHub Pro tiene cuotas utiles pero limitadas. No usar:

- GitHub Packages para datasets grandes.
- Actions para backtests largos diarios.
- Codespaces para computo batch pesado.

Usar DigitalOcean o infraestructura externa para procesamiento pesado.

### Dependencia del Pack

Los beneficios pueden cambiar, expirar o no renovarse. Disenar salida:

- Docker para mover servicios.
- Postgres portable.
- CI separada del proveedor de hosting.
- Secrets documentados por environment.

## Fuentes verificadas

- GitHub Student Developer Pack: https://education.github.com/pack
- Uso incluido por plan de GitHub: https://docs.github.com/en/billing/reference/product-usage-included
- GitHub Copilot CLI: https://docs.github.com/en/copilot/how-tos/copilot-cli
- GitHub Actions billing: https://docs.github.com/billing/managing-billing-for-github-actions/about-billing-for-github-actions
- GitHub Codespaces billing: https://docs.github.com/en/billing/concepts/product-billing/github-codespaces
- GitHub Packages billing: https://docs.github.com/en/billing/concepts/product-billing/github-packages
- Deployment environments: https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments
- Secrets: https://docs.github.com/en/actions/concepts/security/secrets
- Sentry FastAPI: https://docs.sentry.io/platforms/python/integrations/fastapi/
- 365Scores Terms: https://www.365scores.com/pages/terms
