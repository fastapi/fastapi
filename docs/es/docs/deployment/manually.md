# Ejecutar un Servidor Manualmente { #run-a-server-manually }

## Usa el Comando `fastapi run` { #use-the-fastapi-run-command }

En resumen, usa `fastapi run` para servir tu aplicación FastAPI:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>2306215</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
```

</div>

Eso funcionaría para la mayoría de los casos. 😎

Podrías usar ese comando, por ejemplo, para iniciar tu app **FastAPI** en un contenedor, en un servidor, etc.

## Servidores ASGI { #asgi-servers }

Vamos a profundizar un poquito en los detalles.

FastAPI usa un estándar para construir frameworks de web y servidores de Python llamado <abbr title="Asynchronous Server Gateway Interface - Interfaz de puerta de enlace de servidor asíncrona">ASGI</abbr>. FastAPI es un framework web ASGI.

Lo principal que necesitas para ejecutar una aplicación **FastAPI** (o cualquier otra aplicación ASGI) en una máquina de servidor remota es un programa de servidor ASGI como **Uvicorn**, que es el que viene por defecto en el comando `fastapi`.

Hay varias alternativas, incluyendo:

* [Uvicorn](https://www.uvicorn.dev/): un servidor ASGI de alto rendimiento.
* [Hypercorn](https://hypercorn.readthedocs.io/): un servidor ASGI compatible con HTTP/2 y Trio entre otras funcionalidades.
* [Daphne](https://github.com/django/daphne): el servidor ASGI construido para Django Channels.
* [Granian](https://github.com/emmett-framework/granian): Un servidor HTTP Rust para aplicaciones en Python.
* [NGINX Unit](https://unit.nginx.org/howto/fastapi/): NGINX Unit es un runtime para aplicaciones web ligero y versátil.

## Máquina Servidor y Programa Servidor { #server-machine-and-server-program }

Hay un pequeño detalle sobre los nombres que hay que tener en cuenta. 💡

La palabra "**servidor**" se utiliza comúnmente para referirse tanto al computador remoto/en la nube (la máquina física o virtual) como al programa que se está ejecutando en esa máquina (por ejemplo, Uvicorn).

Solo ten en cuenta que cuando leas "servidor" en general, podría referirse a una de esas dos cosas.

Al referirse a la máquina remota, es común llamarla **servidor**, pero también **máquina**, **VM** (máquina virtual), **nodo**. Todos esos se refieren a algún tipo de máquina remota, generalmente con Linux, donde ejecutas programas.

## Instala el Programa del Servidor { #install-the-server-program }

Cuando instalas FastAPI, viene con un servidor de producción, Uvicorn, y puedes iniciarlo con el comando `fastapi run`.

Pero también puedes instalar un servidor ASGI manualmente.

Asegúrate de crear un [entorno virtual](../virtual-environments.md), actívalo, y luego puedes instalar la aplicación del servidor.

Por ejemplo, para instalar Uvicorn:

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

Un proceso similar se aplicaría a cualquier otro programa de servidor ASGI.

/// tip | Consejo

Al añadir `standard`, Uvicorn instalará y usará algunas dependencias adicionales recomendadas.

Eso incluye `uvloop`, el reemplazo de alto rendimiento para `asyncio`, que proporciona un gran impulso de rendimiento en concurrencia.

Cuando instalas FastAPI con algo como `pip install "fastapi[standard]"` ya obtienes `uvicorn[standard]` también.

///

## Ejecuta el Programa del Servidor { #run-the-server-program }

Si instalaste un servidor ASGI manualmente, normalmente necesitarías pasar una cadena de import en un formato especial para que importe tu aplicación FastAPI:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note | Nota

El comando `uvicorn main:app` se refiere a:

* `main`: el archivo `main.py` (el "módulo" de Python).
* `app`: el objeto creado dentro de `main.py` con la línea `app = FastAPI()`.

Es equivalente a:

```Python
from main import app
```

///

Cada programa alternativo de servidor ASGI tendría un comando similar, puedes leer más en su respectiva documentación.

/// warning | Advertencia

Uvicorn y otros servidores soportan una opción `--reload` que es útil durante el desarrollo.

La opción `--reload` consume muchos más recursos, es más inestable, etc.

Ayuda mucho durante el **desarrollo**, pero **no** deberías usarla en **producción**.

///

## Conceptos de Despliegue { #deployment-concepts }

Estos ejemplos ejecutan el programa del servidor (por ejemplo, Uvicorn), iniciando **un solo proceso**, escuchando en todas las IPs (`0.0.0.0`) en un puerto predefinido (por ejemplo, `80`).

Esta es la idea básica. Pero probablemente querrás encargarte de algunas cosas adicionales, como:

* Seguridad - HTTPS
* Ejecución en el arranque
* Reinicios
* Replicación (el número de procesos ejecutándose)
* Memoria
* Pasos previos antes de comenzar

Te contaré más sobre cada uno de estos conceptos, cómo pensarlos, y algunos ejemplos concretos con estrategias para manejarlos en los próximos capítulos. 🚀
