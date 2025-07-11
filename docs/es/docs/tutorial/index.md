# Tutorial - Guía del Usuario

Este tutorial te muestra cómo usar **FastAPI** con la mayoría de sus funcionalidades, paso a paso.

Cada sección se basa gradualmente en las anteriores, pero está estructurada para separar temas, de manera que puedas ir directamente a cualquier sección específica para resolver tus necesidades específicas de API.

También está diseñado para funcionar como una referencia futura para que puedas volver y ver exactamente lo que necesitas.

## Ejecuta el código

Todos los bloques de código pueden ser copiados y usados directamente (de hecho, son archivos Python probados).

Para ejecutar cualquiera de los ejemplos, copia el código a un archivo `main.py`, y comienza `fastapi dev` con:

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
</pre>
```

</div>

Es **ALTAMENTE recomendable** que escribas o copies el código, lo edites y lo ejecutes localmente.

Usarlo en tu editor es lo que realmente te muestra los beneficios de FastAPI, al ver cuán poco código tienes que escribir, todos los chequeos de tipos, autocompletado, etc.

---

## Instalar FastAPI

El primer paso es instalar FastAPI.

Asegúrate de crear un [entorno virtual](../virtual-environments.md){.internal-link target=_blank}, actívalo, y luego **instala FastAPI**:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note | Nota

Cuando instalas con `pip install "fastapi[standard]"` viene con algunas dependencias opcionales estándar por defecto.

Si no quieres tener esas dependencias opcionales, en su lugar puedes instalar `pip install fastapi`.

///

## Guía Avanzada del Usuario

También hay una **Guía Avanzada del Usuario** que puedes leer después de esta **Tutorial - Guía del Usuario**.

La **Guía Avanzada del Usuario** se basa en esta, utiliza los mismos conceptos y te enseña algunas funcionalidades adicionales.

Pero primero deberías leer la **Tutorial - Guía del Usuario** (lo que estás leyendo ahora mismo).

Está diseñada para que puedas construir una aplicación completa solo con la **Tutorial - Guía del Usuario**, y luego extenderla de diferentes maneras, dependiendo de tus necesidades, utilizando algunas de las ideas adicionales de la **Guía Avanzada del Usuario**.
