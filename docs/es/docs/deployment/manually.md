# Ejecutar un Servidor Manualmente

## Usa el Comando `fastapi run`

En resumen, usa `fastapi run` para servir tu aplicación FastAPI:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:single">main.py</u>
<font color="#3465A4">INFO    </font> Usando path <font color="#3465A4">main.py</font>
<font color="#3465A4">INFO    </font> Path absoluto resuelto <font color="#75507B">/home/user/code/awesomeapp/</font><font color="#AD7FA8">main.py</font>
<font color="#3465A4">INFO    </font> Buscando una estructura de archivos de paquete desde directorios con archivos <font color="#3465A4">__init__.py</font>
<font color="#3465A4">INFO    </font> Importando desde <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

 ╭─ <font color="#8AE234"><b>Archivo de módulo de Python</b></font> ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

<font color="#3465A4">INFO    </font> Importando módulo <font color="#4E9A06">main</font>
<font color="#3465A4">INFO    </font> Encontrada aplicación FastAPI importable

 ╭─ <font color="#8AE234"><b>Aplicación FastAPI importable</b></font> ─╮
 │                          │
 │  <span style="background-color:#272822"><font color="#FF4689">from</font></span><span style="background-color:#272822"><font color="#F8F8F2"> main </font></span><span style="background-color:#272822"><font color="#FF4689">import</font></span><span style="background-color:#272822"><font color="#F8F8F2"> app</font></span><span style="background-color:#272822">  </span>  │
 │                          │
 ╰──────────────────────────╯

<font color="#3465A4">INFO    </font> Usando la cadena de import <font color="#8AE234"><b>main:app</b></font>

 <font color="#4E9A06">╭─────────── CLI de FastAPI - Modo Producción ───────────╮</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  Sirviendo en: http://0.0.0.0:8000                    │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  Docs de API: http://0.0.0.0:8000/docs               │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  Corriendo en modo producción, para desarrollo usa:  │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  </font><font color="#8AE234"><b>fastapi dev</b></font><font color="#4E9A06">                                        │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">╰─────────────────────────────────────────────────────╯</font>

<font color="#4E9A06">INFO</font>:     Iniciado el proceso del servidor [<font color="#06989A">2306215</font>]
<font color="#4E9A06">INFO</font>:     Esperando el inicio de la aplicación.
<font color="#4E9A06">INFO</font>:     Inicio de la aplicación completado.
<font color="#4E9A06">INFO</font>:     Uvicorn corriendo en <b>http://0.0.0.0:8000</b> (Presiona CTRL+C para salir)
```

</div>

Eso funcionaría para la mayoría de los casos. 😎

Podrías usar ese comando, por ejemplo, para iniciar tu app **FastAPI** en un contenedor, en un servidor, etc.

## Servidores ASGI

Vamos a profundizar un poquito en los detalles.

FastAPI usa un estándar para construir frameworks de web y servidores de Python llamado <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr>. FastAPI es un framework web ASGI.

Lo principal que necesitas para ejecutar una aplicación **FastAPI** (o cualquier otra aplicación ASGI) en una máquina de servidor remota es un programa de servidor ASGI como **Uvicorn**, que es el que viene por defecto en el comando `fastapi`.

Hay varias alternativas, incluyendo:

* <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a>: un servidor ASGI de alto rendimiento.
* <a href="https://hypercorn.readthedocs.io/" class="external-link" target="_blank">Hypercorn</a>: un servidor ASGI compatible con HTTP/2 y Trio entre otras funcionalidades.
* <a href="https://github.com/django/daphne" class="external-link" target="_blank">Daphne</a>: el servidor ASGI construido para Django Channels.
* <a href="https://github.com/emmett-framework/granian" class="external-link" target="_blank">Granian</a>: Un servidor HTTP Rust para aplicaciones en Python.
* <a href="https://unit.nginx.org/howto/fastapi/" class="external-link" target="_blank">NGINX Unit</a>: NGINX Unit es un runtime para aplicaciones web ligero y versátil.

## Máquina Servidor y Programa Servidor

Hay un pequeño detalle sobre los nombres que hay que tener en cuenta. 💡

La palabra "**servidor**" se utiliza comúnmente para referirse tanto al computador remoto/en la nube (la máquina física o virtual) como al programa que se está ejecutando en esa máquina (por ejemplo, Uvicorn).

Solo ten en cuenta que cuando leas "servidor" en general, podría referirse a una de esas dos cosas.

Al referirse a la máquina remota, es común llamarla **servidor**, pero también **máquina**, **VM** (máquina virtual), **nodo**. Todos esos se refieren a algún tipo de máquina remota, generalmente con Linux, donde ejecutas programas.

## Instala el Programa del Servidor

Cuando instalas FastAPI, viene con un servidor de producción, Uvicorn, y puedes iniciarlo con el comando `fastapi run`.

Pero también puedes instalar un servidor ASGI manualmente.

Asegúrate de crear un [entorno virtual](../virtual-environments.md){.internal-link target=_blank}, actívalo, y luego puedes instalar la aplicación del servidor.

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

## Ejecuta el Programa del Servidor

Si instalaste un servidor ASGI manualmente, normalmente necesitarías pasar una cadena de import en un formato especial para que importe tu aplicación FastAPI:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn corriendo en http://0.0.0.0:80 (Presiona CTRL+C para salir)
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

## Conceptos de Despliegue

Estos ejemplos ejecutan el programa del servidor (por ejemplo, Uvicorn), iniciando **un solo proceso**, escuchando en todas las IPs (`0.0.0.0`) en un puerto predefinido (por ejemplo, `80`).

Esta es la idea básica. Pero probablemente querrás encargarte de algunas cosas adicionales, como:

* Seguridad - HTTPS
* Ejecución en el arranque
* Reinicios
* Replicación (el número de procesos ejecutándose)
* Memoria
* Pasos previos antes de comenzar

Te contaré más sobre cada uno de estos conceptos, cómo pensarlos, y algunos ejemplos concretos con estrategias para manejarlos en los próximos capítulos. 🚀
