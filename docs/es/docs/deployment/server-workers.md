# Servidores Workers - Uvicorn con Workers { #server-workers-uvicorn-with-workers }

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

## Múltiples Workers { #multiple-workers }

Puedes iniciar múltiples workers con la opción de línea de comando `--workers`:

//// tab | `fastapi`

Si usas el comando `fastapi`:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started parent process <b>[</b><font color="#34E2E2"><b>27365</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27368</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27369</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27370</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27367</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
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

## Conceptos de Despliegue { #deployment-concepts }

Aquí viste cómo usar múltiples **workers** para **paralelizar** la ejecución de la aplicación, aprovechar los **múltiples núcleos** del CPU, y poder servir **más requests**.

De la lista de conceptos de despliegue de antes, usar workers ayudaría principalmente con la parte de **replicación**, y un poquito con los **reinicios**, pero aún necesitas encargarte de los otros:

* **Seguridad - HTTPS**
* **Ejecución al inicio**
* ***Reinicios***
* Replicación (el número de procesos en ejecución)
* **Memoria**
* **Pasos previos antes de empezar**

## Contenedores y Docker { #containers-and-docker }

En el próximo capítulo sobre [FastAPI en Contenedores - Docker](docker.md){.internal-link target=_blank} te explicaré algunas estrategias que podrías usar para manejar los otros **conceptos de despliegue**.

Te mostraré cómo **construir tu propia imagen desde cero** para ejecutar un solo proceso de Uvicorn. Es un proceso sencillo y probablemente es lo que querrías hacer al usar un sistema de gestión de contenedores distribuido como **Kubernetes**.

## Resumen { #recap }

Puedes usar múltiples worker processes con la opción CLI `--workers` con los comandos `fastapi` o `uvicorn` para aprovechar los **CPUs de múltiples núcleos**, para ejecutar **múltiples procesos en paralelo**.

Podrías usar estas herramientas e ideas si estás instalando **tu propio sistema de despliegue** mientras te encargas tú mismo de los otros conceptos de despliegue.

Revisa el próximo capítulo para aprender sobre **FastAPI** con contenedores (por ejemplo, Docker y Kubernetes). Verás que esas herramientas tienen formas sencillas de resolver los otros **conceptos de despliegue** también. ✨
