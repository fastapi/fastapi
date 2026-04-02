# Editor-Unterstützung { #editor-support }

Die offizielle [FastAPI-Erweiterung](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode) verbessert Ihren FastAPI-Entwicklungsworkflow mit Pfadoperation-Erkennung und -Navigation sowie FastAPI-Cloud-Deployment und Live-Logstreaming.

Weitere Details zur Erweiterung finden Sie im README im [GitHub-Repository](https://github.com/fastapi/fastapi-vscode).

## Einrichtung und Installation { #setup-and-installation }

Die **FastAPI-Erweiterung** ist sowohl für [VS Code](https://code.visualstudio.com/) als auch für [Cursor](https://www.cursor.com/) verfügbar. Sie kann direkt über das Erweiterungen-Panel in jedem Editor installiert werden, indem Sie nach „FastAPI“ suchen und die von **FastAPI Labs** veröffentlichte Erweiterung auswählen. Die Erweiterung funktioniert auch in browserbasierten Editoren wie [vscode.dev](https://vscode.dev) und [github.dev](https://github.dev).

### Anwendungserkennung { #application-discovery }

Standardmäßig erkennt die Erweiterung FastAPI-Anwendungen in Ihrem Workspace automatisch, indem sie nach Dateien sucht, die `FastAPI()` instanziieren. Falls die automatische Erkennung mit Ihrer Projektstruktur nicht funktioniert, können Sie einen Entry-Point über `[tool.fastapi]` in `pyproject.toml` oder die VS-Code-Einstellung `fastapi.entryPoint` in Modulnotation angeben (z. B. `myapp.main:app`).

## Funktionen { #features }

- Pfadoperation-Explorer – Eine Baumansicht in der Seitenleiste aller <dfn title="Routen, Endpunkte">*Pfadoperationen*</dfn> in Ihrer Anwendung. Klicken Sie, um zu einer beliebigen Route- oder Router-Definition zu springen.
- Routensuche – Suchen Sie nach Pfad, Methode oder Namen mit <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd> (unter macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>).
- CodeLens-Navigation – Anklickbare Links oberhalb von Testclient-Aufrufen (z. B. `client.get('/items')`), die zur passenden Pfadoperation springen und so eine schnelle Navigation zwischen Tests und Implementierung ermöglichen.
- Zu FastAPI Cloud deployen – Deployment Ihrer App mit einem Klick auf [FastAPI Cloud](https://fastapicloud.com/).
- Anwendungslogs streamen – Echtzeit-Logstreaming Ihrer auf FastAPI Cloud deployten Anwendung mit Loglevel-Filterung und Textsuche.

Wenn Sie sich mit den Funktionen der Erweiterung vertraut machen möchten, können Sie den Erweiterungs‑Walkthrough aufrufen, indem Sie die Befehlspalette öffnen (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> oder unter macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>) und „Welcome: Open walkthrough …“ auswählen und anschließend den Walkthrough „Get started with FastAPI“ wählen.
