# Servidores Workers - Uvicorn con Workers

Vamos a revisar esos conceptos de despliegue de antes:

* Seguridad - HTTPS
* Ejecución al inicio
* Reinicios
* **Replicación (el número de procesos en ejecución)**
* Memoria
* Pasos previos antes de empezar

Hasta este punto, con todos los tutoriales en la documentación, probablemente has estado ejecutando un **programa de servidor**, por ejemplo, usando el comando `fastapi`, que ejecuta Uvicorn, corriendo un **solo proceso**.

Al desplegar aplicaciones probablemente querrás tener algo de **replicación de procesos** para aprovechar **múltiples núcleos** y poder manejar más requests.

Como viste en el capítulo anterior sobre [Conceptos de Despliegue](concepts.md){.internal-link target=_blank}, hay múltiples estrategias que puedes usar.

Aquí te mostraré cómo usar **Uvicorn** con **worker processes** usando el comando `fastapi` o el comando `uvicorn` directamente.

/// info | Información

Si estás usando contenedores, por ejemplo con Docker o Kubernetes, te contaré más sobre eso en el próximo capítulo: [FastAPI en Contenedores - Docker](docker.md){.internal-link target=_blank}.

En particular, cuando corras en **Kubernetes** probablemente **no** querrás usar workers y en cambio correr **un solo proceso de Uvicorn por contenedor**, pero te contaré sobre eso más adelante en ese capítulo.

///

## Múltiples Workers

Puedes iniciar múltiples workers con la opción de línea de comando `--workers`:

//// tab | `fastapi`

Si usas el comando `fastapi`:

<div class="termy">

```console
$ <pre> <font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:single">main.py</u>
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

 <font color="#4E9A06">╭─────────── FastAPI CLI - Production mode ───────────╮</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  Serving at: http://0.0.0.0:8000                    │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  API docs: http://0.0.0.0:8000/docs                 │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  Running in production mode, for development use:   │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  </font><font color="#8AE234"><b>fastapi dev</b></font><font color="#4E9A06">                                        │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">╰─────────────────────────────────────────────────────╯</font>

<font color="#4E9A06">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8000</b> (Press CTRL+C to quit)
<font color="#4E9A06">INFO</font>:     Started parent process [<font color="#34E2E2"><b>27365</b></font>]
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">27368</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">27369</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">27370</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">27367</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
</pre>
```

</div>

////

//// tab | `uvicorn`

Si prefieres usar el comando `uvicorn` directamente:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

</div>

////

La única opción nueva aquí es `--workers` indicando a Uvicorn que inicie 4 worker processes.

También puedes ver que muestra el **PID** de cada proceso, `27365` para el proceso padre (este es el **gestor de procesos**) y uno para cada worker process: `27368`, `27369`, `27370`, y `27367`.

## Conceptos de Despliegue

Aquí viste cómo usar múltiples **workers** para **paralelizar** la ejecución de la aplicación, aprovechar los **múltiples núcleos** del CPU, y poder servir **más requests**.

De la lista de conceptos de despliegue de antes, usar workers ayudaría principalmente con la parte de **replicación**, y un poquito con los **reinicios**, pero aún necesitas encargarte de los otros:

* **Seguridad - HTTPS**
* **Ejecución al inicio**
* ***Reinicios***
* Replicación (el número de procesos en ejecución)
* **Memoria**
* **Pasos previos antes de empezar**

## Contenedores y Docker

En el próximo capítulo sobre [FastAPI en Contenedores - Docker](docker.md){.internal-link target=_blank} te explicaré algunas estrategias que podrías usar para manejar los otros **conceptos de despliegue**.

Te mostraré cómo **construir tu propia imagen desde cero** para ejecutar un solo proceso de Uvicorn. Es un proceso sencillo y probablemente es lo que querrías hacer al usar un sistema de gestión de contenedores distribuido como **Kubernetes**.

## Resumen

Puedes usar múltiples worker processes con la opción CLI `--workers` con los comandos `fastapi` o `uvicorn` para aprovechar los **CPUs de múltiples núcleos**, para ejecutar **múltiples procesos en paralelo**.

Podrías usar estas herramientas e ideas si estás instalando **tu propio sistema de despliegue** mientras te encargas tú mismo de los otros conceptos de despliegue.

Revisa el próximo capítulo para aprender sobre **FastAPI** con contenedores (por ejemplo, Docker y Kubernetes). Verás que esas herramientas tienen formas sencillas de resolver los otros **conceptos de despliegue** también. ✨
