# FastAPI CLI

**FastAPI CLI** es un programa de línea de comandos que puedes usar para servir tu aplicación FastAPI, administrarla y más.

Cuando instalas FastAPI (e.g. `pip install fastapi`), esto incluye un paquete llamado `fastapi-cli`. Este paquete provee el comando `fastapi` en la terminal.

Para ejecutar tu aplicación de FastAPI para desarrollo, puedes usar el comando `fastapi dev`:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:single">main.py</u>
<font color="#3465A4">INFO    </font> Using path <font color="#3465A4">main.py</font>
<font color="#3465A4">INFO    </font> Resolved absolute path <font color="#75507B">/home/user/code/awesomeapp/</font><font color="#AD7FA8">main.py</font>
<font color="#3465A4">INFO    </font> Searching for package file structure from directories with <font color="#3465A4">__init__.py</font> files
<font color="#3465A4">INFO    </font> Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

 ╭─ <font color="#8AE234"><b>Python module file</b></font> ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

<font color="#3465A4">INFO    </font> Importing module <font color="#4E9A06">main</font>
<font color="#3465A4">INFO    </font> Found importable FastAPI app

 ╭─ <font color="#8AE234"><b>Importable FastAPI app</b></font> ─╮
 │                          │
 │  <span style="background-color:#272822"><font color="#FF4689">from</font></span><span style="background-color:#272822"><font color="#F8F8F2"> main </font></span><span style="background-color:#272822"><font color="#FF4689">import</font></span><span style="background-color:#272822"><font color="#F8F8F2"> app</font></span><span style="background-color:#272822">  </span>  │
 │                          │
 ╰──────────────────────────╯

<font color="#3465A4">INFO    </font> Using import string <font color="#8AE234"><b>main:app</b></font>

 <span style="background-color:#C4A000"><font color="#2E3436">╭────────── FastAPI CLI - Development mode ───────────╮</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Serving at: http://127.0.0.1:8000                  │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  API docs: http://127.0.0.1:8000/docs               │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Running in development mode, for production use:   │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  </font></span><span style="background-color:#C4A000"><font color="#555753"><b>fastapi run</b></font></span><span style="background-color:#C4A000"><font color="#2E3436">                                        │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">╰─────────────────────────────────────────────────────╯</font></span>

<font color="#4E9A06">INFO</font>:     Will watch for changes in these directories: [&apos;/home/user/code/awesomeapp&apos;]
<font color="#4E9A06">INFO</font>:     Uvicorn running on <b>http://127.0.0.1:8000</b> (Press CTRL+C to quit)
<font color="#4E9A06">INFO</font>:     Started reloader process [<font color="#34E2E2"><b>2265862</b></font>] using <font color="#34E2E2"><b>WatchFiles</b></font>
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">2265873</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
```

</div>

El programa de línea de comandos llamado `fastapi` es **FastAPI CLI**.

FastAPI CLI toma la ruta de tu programa Python (por ejemplo, `main.py`) y detecta automáticamente la variable de FastAPI (comúnmente llamada `app`),  y la importa para finalmente servir la aplicación.

Para producción usarías `fastapi run` en su lugar. 🚀

Internamente, **FastAPI CLI** usa <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>, un servidor ASGI de alto rendimiento y listo para producción. 😎

## `fastapi dev`

Cuando ejecutas `fastapi dev`, el proyecto se ejecuta en modo de desarrollo.

Por defecto, está habilitada la **recarga automática**, por lo que recargará automáticamente el servidor cuando realices cambios en tu código. Esto consume muchos recursos y podría ser menos estable que sin ella; solo debes usarlo para desarrollo.

Por defecto, escuchará en la dirección IP `127.0.0.1`, que es la IP para que tu máquina se comunique consigo misma (localhost).

## `fastapi run`

Cuando ejecutas `fastapi run`, el proyecto se ejecuta en modo de producción por defecto.

La **recarga automática** está deshabilitada por defecto.

Cuando ejecutas en modo de producción, la aplicación escuchará en la dirección IP `0.0.0.0`, lo que significa todas las direcciones IP disponibles, de esta manera será accesible públicamente para cualquiera que pueda comunicarse con la máquina. Así es como normalmente lo ejecutarías en producción, por ejemplo, en un contenedor.

En la mayoría de los casos, tendrías (y deberías tener) un "proxy de terminación" que maneje HTTPS por ti, esto dependerá de cómo implementes tu aplicación; tu proveedor podría hacerlo por ti o podrías necesitar configurarlo tú mismo.

!!! tip
    Puedes aprender más en la [documentación de despliegue](deployment/index.md){.internal-link target=_blank}.
