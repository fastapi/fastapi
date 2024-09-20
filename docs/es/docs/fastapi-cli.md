# FastAPI CLI

**FastAPI CLI** es un programa de línea de comandos que te permite lanzar tu aplicación FastAPI, gestionar tu proyecto y más.

Cuando instalas FastAPI (por ejemplo, con `pip install "fastapi[standard]"`), se incluye un paquete llamado `fastapi-cli`, que te proporciona el comando `fastapi` en la terminal.

Para ejecutar tu aplicación FastAPI en modo desarrollo, puedes usar el comando `fastapi dev`:


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

FastAPI CLI recibe la ruta de tu programa Python (por ejemplo, `main.py`), detecta automáticamente la instancia de `FastAPI` (comúnmente llamada `app`), determina el proceso de importación correcto y luego la lanza.

Para producción, usarías `fastapi run` en su lugar. 🚀

Internamente, **FastAPI CLI** utiliza <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>, un servidor ASGI de alto rendimiento y listo para producción. 😎

## `fastapi dev`

Cuando ejecutas `fastapi dev`, el proyecto se ejecuta en modo de desarrollo.

Por defecto, está habilitada la **recarga automática**, por lo que recargará automáticamente el servidor cuando realices cambios en tu código. Esto consume muchos recursos y podría ser menos estable que cuando está deshabilitada. Debes usarlo solo para desarrollo.
También escucha en la dirección IP `127.0.0.1`, que es la IP que permite que tu máquina se comunique consigo misma (`localhost`).

## `fastapi run`

Al ejecutar `fastapi run`, FastAPI se inicia automáticamente en modo producción.

Por defecto, la **recarga automática** está deshabilitada. También escucha en la dirección IP `0.0.0.0`, lo que significa que estará disponible en todas las direcciones IP, haciéndolo accesible públicamente para cualquiera que pueda comunicarse con la máquina. Esta es la forma en la que normalmente lo ejecutarías en producción, por ejemplo, en un contenedor.

En la mayoría de los casos, deberías (y tendrías que) tener un "proxy de terminación" que maneje HTTPS por ti, dependiendo de cómo despliegues tu aplicación. Tu proveedor podría encargarse de esto, o quizás necesites configurarlo por tu cuenta.


/// tip | Consejo

Puedes aprender más al respecto en la [documentación de despliegue](deployment/index.md){.internal-link target=_blank}.

///
