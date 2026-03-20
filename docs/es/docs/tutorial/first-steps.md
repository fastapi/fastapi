# Primeros Pasos { #first-steps }

El archivo FastAPI más simple podría verse así:

{* ../../docs_src/first_steps/tutorial001_py310.py *}

Copia eso en un archivo `main.py`.

Ejecuta el servidor en vivo:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

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

En el resultado, hay una línea con algo como:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Esa línea muestra la URL donde tu aplicación está siendo servida, en tu máquina local.

### Revisa { #check-it }

Abre tu navegador en [http://127.0.0.1:8000](http://127.0.0.1:8000).

Verás el response JSON como:

```JSON
{"message": "Hello World"}
```

### Documentación interactiva de la API { #interactive-api-docs }

Ahora ve a [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Verás la documentación interactiva automática de la API (proporcionada por [Swagger UI](https://github.com/swagger-api/swagger-ui)):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentación alternativa de la API { #alternative-api-docs }

Y ahora, ve a [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

Verás la documentación alternativa automática (proporcionada por [ReDoc](https://github.com/Rebilly/ReDoc)):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI** genera un "esquema" con toda tu API utilizando el estándar **OpenAPI** para definir APIs.

#### "Esquema" { #schema }

Un "esquema" es una definición o descripción de algo. No el código que lo implementa, sino solo una descripción abstracta.

#### Esquema de la API { #api-schema }

En este caso, [OpenAPI](https://github.com/OAI/OpenAPI-Specification) es una especificación que dicta cómo definir un esquema de tu API.

Esta definición de esquema incluye los paths de tu API, los posibles parámetros que toman, etc.

#### Esquema de Datos { #data-schema }

El término "esquema" también podría referirse a la forma de algunos datos, como el contenido JSON.

En ese caso, significaría los atributos del JSON, los tipos de datos que tienen, etc.

#### OpenAPI y JSON Schema { #openapi-and-json-schema }

OpenAPI define un esquema de API para tu API. Y ese esquema incluye definiciones (o "esquemas") de los datos enviados y recibidos por tu API utilizando **JSON Schema**, el estándar para esquemas de datos JSON.

#### Revisa el `openapi.json` { #check-the-openapi-json }

Si tienes curiosidad por cómo se ve el esquema OpenAPI en bruto, FastAPI automáticamente genera un JSON (esquema) con las descripciones de toda tu API.

Puedes verlo directamente en: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json).

Mostrará un JSON que empieza con algo como:

```JSON
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### Para qué sirve OpenAPI { #what-is-openapi-for }

El esquema OpenAPI es lo que impulsa los dos sistemas de documentación interactiva incluidos.

Y hay docenas de alternativas, todas basadas en OpenAPI. Podrías añadir fácilmente cualquiera de esas alternativas a tu aplicación construida con **FastAPI**.

También podrías usarlo para generar código automáticamente, para clientes que se comuniquen con tu API. Por ejemplo, aplicaciones frontend, móviles o IoT.

### Configura el `entrypoint` de la app en `pyproject.toml` { #configure-the-app-entrypoint-in-pyproject-toml }

Puedes configurar dónde está tu app en un archivo `pyproject.toml` así:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Ese `entrypoint` le dirá al comando `fastapi` que debe hacer el import de la app así:

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

Entonces pondrías el `entrypoint` como:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

lo cual sería equivalente a:

```python
from backend.main import app
```

### `fastapi dev` con path { #fastapi-dev-with-path }

También puedes pasar el path del archivo al comando `fastapi dev`, y adivinará el objeto app de FastAPI que debe usar:

```console
$ fastapi dev main.py
```

Pero tendrías que recordar pasar el path correcto cada vez que llames al comando `fastapi`.

Además, otras herramientas podrían no ser capaces de encontrarlo, por ejemplo la [Extensión de VS Code](../editor-support.md) o [FastAPI Cloud](https://fastapicloud.com), así que se recomienda usar el `entrypoint` en `pyproject.toml`.

### Despliega tu app (opcional) { #deploy-your-app-optional }

Opcionalmente puedes desplegar tu app de FastAPI en [FastAPI Cloud](https://fastapicloud.com), ve y únete a la lista de espera si aún no lo has hecho. 🚀

Si ya tienes una cuenta de **FastAPI Cloud** (te invitamos desde la lista de espera 😉), puedes desplegar tu aplicación con un solo comando.

Antes de desplegar, asegúrate de haber iniciado sesión:

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

Luego despliega tu app:

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

¡Eso es todo! Ahora puedes acceder a tu app en esa URL. ✨

## Recapitulación, paso a paso { #recap-step-by-step }

### Paso 1: importa `FastAPI` { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[1] *}

`FastAPI` es una clase de Python que proporciona toda la funcionalidad para tu API.

/// note | Detalles técnicos

`FastAPI` es una clase que hereda directamente de `Starlette`.

Puedes usar toda la funcionalidad de [Starlette](https://www.starlette.dev/) con `FastAPI` también.

///

### Paso 2: crea una "instance" de `FastAPI` { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[3] *}

Aquí la variable `app` será una "instance" de la clase `FastAPI`.

Este será el punto principal de interacción para crear toda tu API.

### Paso 3: crea una *path operation* { #step-3-create-a-path-operation }

#### Path { #path }

"Path" aquí se refiere a la última parte de la URL empezando desde la primera `/`.

Así que, en una URL como:

```
https://example.com/items/foo
```

...el path sería:

```
/items/foo
```

/// info | Información

Un "path" también es comúnmente llamado "endpoint" o "ruta".

///

Mientras construyes una API, el "path" es la forma principal de separar "concerns" y "resources".

#### Operación { #operation }

"Operación" aquí se refiere a uno de los "métodos" HTTP.

Uno de:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...y los más exóticos:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

En el protocolo HTTP, puedes comunicarte con cada path usando uno (o más) de estos "métodos".

---

Al construir APIs, normalmente usas estos métodos HTTP específicos para realizar una acción específica.

Normalmente usas:

* `POST`: para crear datos.
* `GET`: para leer datos.
* `PUT`: para actualizar datos.
* `DELETE`: para eliminar datos.

Así que, en OpenAPI, cada uno de los métodos HTTP se llama una "operation".

Vamos a llamarlas "**operaciones**" también.

#### Define un *path operation decorator* { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[6] *}

El `@app.get("/")` le dice a **FastAPI** que la función justo debajo se encarga de manejar requests que vayan a:

* el path `/`
* usando una <dfn title="un método HTTP GET"><code>get</code> operación</dfn>

/// info | Información sobre `@decorator`

Esa sintaxis `@algo` en Python se llama un "decorador".

Lo pones encima de una función. Como un bonito sombrero decorativo (supongo que de ahí viene el término).

Un "decorador" toma la función de abajo y hace algo con ella.

En nuestro caso, este decorador le dice a **FastAPI** que la función de abajo corresponde al **path** `/` con una **operation** `get`.

Es el "**path operation decorator**".

///

También puedes usar las otras operaciones:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

Y los más exóticos:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | Consejo

Eres libre de usar cada operación (método HTTP) como quieras.

**FastAPI** no fuerza ningún significado específico.

La información aquí se presenta como una guía, no un requisito.

Por ejemplo, cuando usas GraphQL normalmente realizas todas las acciones usando solo operaciones `POST`.

///

### Paso 4: define la **path operation function** { #step-4-define-the-path-operation-function }

Esta es nuestra "**path operation function**":

* **path**: es `/`.
* **operation**: es `get`.
* **function**: es la función debajo del "decorador" (debajo de `@app.get("/")`).

{* ../../docs_src/first_steps/tutorial001_py310.py hl[7] *}

Esta es una función de Python.

Será llamada por **FastAPI** cuando reciba un request en la URL "`/`" usando una operación `GET`.

En este caso, es una función `async`.

---

También podrías definirla como una función normal en lugar de `async def`:

{* ../../docs_src/first_steps/tutorial003_py310.py hl[7] *}

/// note | Nota

Si no sabes la diferencia, Revisa la sección [Async: *"¿Tienes prisa?"*](../async.md#in-a-hurry).

///

### Paso 5: retorna el contenido { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[8] *}

Puedes retornar un `dict`, `list`, valores singulares como `str`, `int`, etc.

También puedes retornar modelos de Pydantic (verás más sobre eso más adelante).

Hay muchos otros objetos y modelos que serán automáticamente convertidos a JSON (incluyendo ORMs, etc). Intenta usar tus favoritos, es altamente probable que ya sean compatibles.

### Paso 6: Despliégalo { #step-6-deploy-it }

Despliega tu app en **[FastAPI Cloud](https://fastapicloud.com)** con un solo comando: `fastapi deploy`. 🎉

#### Sobre FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** está construido por el mismo autor y equipo detrás de **FastAPI**.

Agiliza el proceso de **construir**, **desplegar** y **acceder** a una API con el mínimo esfuerzo.

Trae la misma **experiencia de desarrollador** de construir apps con FastAPI a **desplegarlas** en la nube. 🎉

FastAPI Cloud es el sponsor principal y proveedor de financiación para los proyectos open source de *FastAPI and friends*. ✨

#### Despliega en otros proveedores cloud { #deploy-to-other-cloud-providers }

FastAPI es open source y basado en estándares. Puedes desplegar apps de FastAPI en cualquier proveedor cloud que elijas.

Sigue las guías de tu proveedor cloud para desplegar apps de FastAPI con ellos. 🤓

## Recapitulación { #recap }

* Importa `FastAPI`.
* Crea una instance `app`.
* Escribe un **path operation decorator** usando decoradores como `@app.get("/")`.
* Define una **path operation function**; por ejemplo, `def root(): ...`.
* Ejecuta el servidor de desarrollo usando el comando `fastapi dev`.
* Opcionalmente, despliega tu app con `fastapi deploy`.
