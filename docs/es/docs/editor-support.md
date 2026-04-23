# Soporte del editor { #editor-support }

La [Extensión de FastAPI](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode) oficial mejora tu flujo de trabajo de desarrollo con FastAPI con descubrimiento de *path operation*, navegación, además de deployment a FastAPI Cloud y streaming en vivo de logs.

Para más detalles sobre la extensión, consulta el README en el [repositorio de GitHub](https://github.com/fastapi/fastapi-vscode).

## Configuración e instalación { #setup-and-installation }

La **Extensión de FastAPI** está disponible tanto para [VS Code](https://code.visualstudio.com/) como para [Cursor](https://www.cursor.com/). Se puede instalar directamente desde el panel de Extensiones en cada editor buscando "FastAPI" y seleccionando la extensión publicada por **FastAPI Labs**. La extensión también funciona en editores basados en navegador como [vscode.dev](https://vscode.dev) y [github.dev](https://github.dev).

### Descubrimiento de la aplicación { #application-discovery }

Por defecto, la extensión descubrirá automáticamente aplicaciones FastAPI en tu espacio de trabajo escaneando archivos que creen un instance de `FastAPI()`. Si la detección automática no funciona con la estructura de tu proyecto, puedes especificar un punto de entrada mediante `[tool.fastapi]` en `pyproject.toml` o la configuración de VS Code `fastapi.entryPoint` usando notación de módulo (p. ej. `myapp.main:app`).

## Funcionalidades { #features }

- **Explorador de Path Operations** - Una vista en árbol en la barra lateral de todas las <dfn title="rutas, endpoints">*path operations*</dfn> de tu aplicación. Haz clic para saltar a cualquier definición de ruta o de router.
- **Búsqueda de rutas** - Busca por path, método o nombre con <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd> (en macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>).
- **Navegación con CodeLens** - Enlaces clicables encima de llamadas del cliente de tests (p. ej. `client.get('/items')`) que saltan a la *path operation* correspondiente para navegar rápidamente entre tests e implementación.
- **Desplegar en FastAPI Cloud** - Deployment con un clic de tu app a [FastAPI Cloud](https://fastapicloud.com/).
- **Streaming de logs de la aplicación** - Streaming en tiempo real de logs desde tu aplicación desplegada en FastAPI Cloud, con filtrado por nivel y búsqueda de texto.

Si quieres familiarizarte con las funcionalidades de la extensión, puedes revisar el recorrido guiado de la extensión abriendo la Paleta de Comandos (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> o en macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>) y seleccionando "Welcome: Open walkthrough..." y luego eligiendo el recorrido "Get started with FastAPI".
