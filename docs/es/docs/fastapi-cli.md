# FastAPI CLI { #fastapi-cli }

**FastAPI <abbr title="command line interface - interfaz de línea de comandos">CLI</abbr>** es un programa de línea de comandos que puedes usar para servir tu aplicación FastAPI, gestionar tu proyecto FastAPI, y más.

Cuando instalas FastAPI (por ejemplo, con `pip install "fastapi[standard]"`), viene con un programa de línea de comandos que puedes ejecutar en la terminal.

Para ejecutar tu aplicación FastAPI en modo de desarrollo, puedes usar el comando `fastapi dev`:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

/// tip | Consejo

Para producción usarías `fastapi run` en lugar de `fastapi dev`. 🚀

///

Internamente, **FastAPI CLI** usa [Uvicorn](https://www.uvicorn.dev), un servidor ASGI de alto rendimiento y listo para producción. 😎

El CLI `fastapi` intentará detectar automáticamente la app de FastAPI que debe ejecutar, asumiendo que es un objeto llamado `app` en un archivo `main.py` (o un par de variantes más).

Pero puedes configurar explícitamente la app a usar.

## Configura el `entrypoint` de la app en `pyproject.toml` { #configure-the-app-entrypoint-in-pyproject-toml }

Puedes configurar dónde está tu app en un archivo `pyproject.toml` así:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Ese `entrypoint` le dirá al comando `fastapi` que debe importar la app así:

```python
from main import app
```

Si tu código estuviera estructurado así:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

Entonces establecerías el `entrypoint` como:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

lo cual sería equivalente a:

```python
from backend.main import app
```

### `fastapi dev` con path { #fastapi-dev-with-path }

También puedes pasar el path del archivo al comando `fastapi dev`, y adivinará el objeto app de FastAPI a usar:

```console
$ fastapi dev main.py
```

Pero tendrías que recordar pasar el path correcto cada vez que llames al comando `fastapi`.

Adicionalmente, otras herramientas podrían no ser capaces de encontrarla, por ejemplo la [Extensión de VS Code](editor-support.md) o [FastAPI Cloud](https://fastapicloud.com), así que se recomienda usar el `entrypoint` en `pyproject.toml`.

## `fastapi dev` { #fastapi-dev }

Ejecutar `fastapi dev` inicia el modo de desarrollo.

Por defecto, **auto-reload** está habilitado, recargando automáticamente el servidor cuando realizas cambios en tu código. Esto consume muchos recursos y podría ser menos estable que cuando está deshabilitado. Deberías usarlo solo para desarrollo. También escucha en la dirección IP `127.0.0.1`, que es la IP para que tu máquina se comunique solo consigo misma (`localhost`).

## `fastapi run` { #fastapi-run }

Ejecutar `fastapi run` inicia FastAPI en modo de producción por defecto.

Por defecto, **auto-reload** está deshabilitado. También escucha en la dirección IP `0.0.0.0`, lo que significa todas las direcciones IP disponibles, de esta manera será accesible públicamente por cualquiera que pueda comunicarse con la máquina. Esta es la manera en la que normalmente lo ejecutarías en producción, por ejemplo, en un contenedor.

En la mayoría de los casos tendrías (y deberías) tener un "proxy de terminación" manejando HTTPS por ti, esto dependerá de cómo despliegues tu aplicación, tu proveedor podría hacer esto por ti, o podrías necesitar configurarlo tú mismo.

/// tip | Consejo

Puedes aprender más al respecto en la [documentación de despliegue](deployment/index.md).

///
