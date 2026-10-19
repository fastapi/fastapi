# Tutorial - Guía del Usuario { #tutorial-user-guide }

Este tutorial te muestra cómo usar **FastAPI** con la mayoría de sus funcionalidades, paso a paso.

Cada sección se basa gradualmente en las anteriores, pero está estructurada para separar temas, de manera que puedas ir directamente a cualquier sección específica para resolver tus necesidades específicas de API.

También está diseñado para funcionar como una referencia futura para que puedas volver y ver exactamente lo que necesitas.

## Ejecuta el código { #run-the-code }

Todos los bloques de código pueden ser copiados y usados directamente (de hecho, son archivos Python probados).

Para ejecutar cualquiera de los ejemplos, copia el código a un archivo `main.py`, y comienza `fastapi dev` con `uv run`:

<div class="termy">

```console
$ <font color="#4E9A06">uv run fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

Es **ALTAMENTE recomendable** que escribas o copies el código, lo edites y lo ejecutes localmente.

Usarlo en tu editor es lo que realmente te muestra los beneficios de FastAPI, al ver cuán poco código tienes que escribir, todo el chequeo de tipos, autocompletado, etc.

---

## Instalar FastAPI { #install-fastapi }

El primer paso es configurar tu proyecto y añadir FastAPI.

Instala [`uv`](https://docs.astral.sh/uv/getting-started/installation/), luego crea un proyecto y añade FastAPI:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"

---> 100%
```

</div>

`uv add` crea el entorno virtual del proyecto en `.venv`, añade FastAPI a `pyproject.toml`, y crea `uv.lock` para que se puedan instalar las mismas versiones de paquetes más adelante.

/// details | Qué hacen estos comandos

* `uv init`: crea un nuevo proyecto Python.
* `awesome-project`: crea el proyecto en un nuevo directorio con este nombre.
* `--bare`: crea solo el archivo mínimo `pyproject.toml`, sin generar un `main.py`, `README.md`, u otros archivos de ejemplo. Tú crearás los archivos de la aplicación en los siguientes pasos de este tutorial.

Luego `cd awesome-project` entra al nuevo directorio del proyecto antes de añadir FastAPI.

`uv` usará una versión compatible de Python ya instalada en tu sistema, o descargará una si es necesario.

Cuando ejecutas `uv add`, selecciona versiones compatibles de FastAPI y todos los paquetes de los que depende FastAPI. Registra las versiones exactas en `uv.lock`, haciendo posible instalar las mismas versiones de paquetes más adelante en otra computadora o al hacer deploy de la aplicación.

Crear o actualizar este archivo se llama hacer [**locking** de las dependencias del proyecto](https://docs.astral.sh/uv/concepts/projects/sync/). `uv` hace esto automáticamente cuando añades un paquete.

///

/// details | Opciones de instalación de FastAPI

Cuando instalas con `uv add "fastapi[standard]"` viene con algunas dependencias opcionales estándar por defecto, incluyendo `fastapi-cloud-cli`, que te permite hacer deploy a [FastAPI Cloud](https://fastapicloud.com).

Si no quieres tener esas dependencias opcionales, en su lugar puedes instalar `uv add fastapi`.

Si quieres instalar las dependencias estándar pero sin `fastapi-cloud-cli`, puedes instalar con `uv add "fastapi[standard-no-fastapi-cloud-cli]"`.

///

/// details | Usar `pip` en su lugar

Si prefieres gestionar un entorno virtual y paquetes manualmente, crea y activa un entorno virtual y luego instala FastAPI con `pip install "fastapi[standard]"`.

Lee la [guía de Entornos Virtuales](https://tiangolo.com/guides/virtual-environments/) para ver los pasos detallados.

///

## Habilidades de agentes de IA { #ai-agent-skills }

FastAPI incluye una habilidad oficial para agentes de programación con IA. Viene incluida con el paquete, por lo que su guía se mantiene alineada con la versión de FastAPI instalada en tu proyecto y se actualiza cuando actualizas FastAPI.

Después de instalar FastAPI en tu proyecto, puedes instalar la habilidad con <a href="https://library-skills.io">Library Skills</a>:

```bash
uvx library-skills
```

/// note | Nota

`uvx` es un alias de `uv tool run`. Ejecuta Library Skills en un entorno temporal y aislado mientras Library Skills escanea los paquetes instalados en tu proyecto.

///

La habilidad es compatible con Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, Pi, OpenCode, y la mayoría de otros agentes de programación. Para Claude Code, selecciona `.claude/skills` cuando se te pregunte dónde instalar la habilidad.

## Guía Avanzada del Usuario { #advanced-user-guide }

También hay una **Guía Avanzada del Usuario** que puedes leer después de esta **Tutorial - Guía del Usuario**.

La **Guía Avanzada del Usuario** se basa en esta, utiliza los mismos conceptos y te enseña algunas funcionalidades adicionales.

Pero primero deberías leer la **Tutorial - Guía del Usuario** (lo que estás leyendo ahora mismo).

Está diseñada para que puedas construir una aplicación completa solo con la **Tutorial - Guía del Usuario**, y luego extenderla de diferentes maneras, dependiendo de tus necesidades, utilizando algunas de las ideas adicionales de la **Guía Avanzada del Usuario**.
