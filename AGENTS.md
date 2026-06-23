# AGENTS.md

## Objetivo del repositorio

Este repositorio documenta y prepara el flujo de trabajo para BetIntel AI con GitHub Copilot, GitHub Copilot CLI, VS Code, Codespaces y GitHub Education Pack.

BetIntel AI debe tratarse como un sistema de prediccion probabilistica y deteccion de valor. No optimizar solo por acierto binario; priorizar calibracion, log loss, Brier score y EV esperado.

## Reglas obligatorias

- Responder en espanol salvo que se pida otro idioma.
- Nunca subir secretos, tokens, claves privadas, DSN reales ni credenciales.
- Nunca generar ni versionar datasets grandes dentro de Git.
- No automatizar scraping de fuentes deportivas sin validar primero sus terminos de uso.
- Preferir APIs oficiales, datos licenciados o datos propios.
- Antes de sugerir merge para codigo, ejecutar o proponer:
  - `ruff check .`
  - `pytest -q`
  - `python scripts/backtest_smoke.py`
- Si se cambia logica de features, targets o modelado, actualizar `docs/modeling.md`.
- Si se cambia un endpoint publico, actualizar `docs/api.md`.
- Si se agregan dependencias de produccion, explicar por que son necesarias.

## Rutas importantes

- `docs/modelo-betintel-ai-github-education.md`: modelo operativo derivado de la investigacion PDF.
- `.github/copilot-instructions.md`: instrucciones generales para Copilot.
- `.github/prompts/`: prompts reutilizables.
- `.devcontainer/`: configuracion de Codespaces y Dev Containers.
- `.vscode/`: recomendaciones y settings del workspace.

## Seguridad

- Usar variables de entorno para claves y credenciales.
- Mantener `.env` fuera de Git.
- Usar GitHub environments para `staging` y `production`.
- Production debe requerir aprobacion manual.
- Pedir aprobacion antes de ejecutar comandos que publiquen, desplieguen o borren recursos.

## Flujo recomendado con Copilot CLI

```powershell
copilot
copilot -i "revisa este repo siguiendo AGENTS.md"
copilot -i "crea un plan para implementar el modelo operativo de BetIntel AI"
copilot --continue
copilot --resume
```

Usar `--allow-all` o `--yolo` solo en tareas acotadas y revisables.
