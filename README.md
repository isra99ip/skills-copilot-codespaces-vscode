# skills-copilot-codespaces-vscode

Repositorio base para usar GitHub Copilot, VS Code y GitHub Codespaces con instrucciones y prompts reutilizables.

## Estado del entorno local

- VS Code instalado.
- GitHub Copilot instalado en VS Code.
- GitHub Codespaces instalado en VS Code.
- GitHub Pull Requests instalado en VS Code.
- Dev Containers instalado en VS Code.
- Git instalado.
- GitHub CLI instalado.

## Primer uso

1. Abre una terminal nueva para que Windows recargue el `PATH`.
2. Inicia sesion en GitHub:

   ```powershell
   gh auth login
   ```

3. Abre este repositorio en VS Code:

   ```powershell
   code C:\Users\isra9\Documents\GitHub\skills-copilot-codespaces-vscode
   ```

4. En VS Code, inicia sesion cuando Copilot o Codespaces lo pidan.
5. Para crear un Codespace, abre la paleta con `Ctrl+Shift+P` y ejecuta:

   ```text
   Codespaces: Create New Codespace
   ```

## Archivos incluidos

- `.github/copilot-instructions.md`: instrucciones generales para Copilot en este repositorio.
- `.github/instructions/markdown.instructions.md`: reglas para archivos Markdown.
- `.github/prompts/review-repo.prompt.md`: prompt reutilizable para revisar un repo.
- `.github/prompts/create-plan.prompt.md`: prompt reutilizable para generar un plan de trabajo.
- `.devcontainer/devcontainer.json`: entorno base para GitHub Codespaces y Dev Containers.
- `.vscode/extensions.json`: extensiones recomendadas.
- `.vscode/settings.json`: ajustes del workspace.

## Publicar cambios

Despues de iniciar sesion con `gh auth login`, ejecuta:

```powershell
git add .
git commit -m "Initial Copilot Codespaces setup"
git push -u origin main
```
