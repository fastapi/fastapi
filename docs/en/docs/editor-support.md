# Editor Support { #editor-support }

The official <a href="https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode" class="external-link" target="_blank">FastAPI Extension</a> enhances your FastAPI development workflow with *path operation* discovery, navigation, as well as FastAPI Cloud deployment, and live log streaming.

For more details about the extension, refer to the README on the <a href="https://github.com/fastapi/fastapi-vscode" class="external-link" target="_blank">GitHub repository</a>.

## Setup and Installation { #setup-and-installation }

The **FastAPI Extension** is available for both <a href="https://code.visualstudio.com/" class="external-link" target="_blank">VS Code</a> and <a href="https://www.cursor.com/" class="external-link" target="_blank">Cursor</a>. It can be installed directly from the Extensions panel in each editor by searching for "FastAPI" and selecting the extension published by **FastAPI Labs**. The extension also works in browser-based editors such as <a href="https://vscode.dev" class="external-link" target="_blank">vscode.dev</a> and <a href="https://github.dev" class="external-link" target="_blank">github.dev</a>.

### Application Discovery { #application-discovery }

By default, the extension will automatically discover FastAPI applications in your workspace by scanning for files that instantiate `FastAPI()`. If auto-detection doesn't work for your project structure, you can specify an entrypoint via `[tool.fastapi]` in `pyproject.toml` or the `fastapi.entryPoint` VS Code setting using module notation (e.g. `myapp.main:app`).

## Features { #features }

- **Path Operation Explorer** - A sidebar tree view of all <dfn title="routes, endpoints">*path operations*</dfn> in your application. Click to jump to any route or router definition.
- **Route Search** - Search by path, method, or name with <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd> (on macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>).
- **CodeLens Navigation** - Clickable links above test client calls (e.g. `client.get('/items')`) that jump to the matching *path operation* for quick navigation between tests and implementation.
- **Deploy to FastAPI Cloud** - One-click deployment of your app to <a href="https://fastapicloud.com/" class="external-link" target="_blank">FastAPI Cloud</a>.
- **Stream Application Logs** - Real-time log streaming from your FastAPI Cloud-deployed application with level filtering and text search.

If you'd like to familiarize yourself with the extension's features, you can checkout the extension walkthrough by opening the Command Palette (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> or on macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>) and selecting "Welcome: Open walkthrough..." and then choosing the "Get started with FastAPI" walkthrough.
