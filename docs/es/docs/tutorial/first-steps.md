# Primeros Pasos

El archivo FastAPI más simple podría verse así:

{* ../../docs_src/first_steps/tutorial001.py *}

Copia eso en un archivo `main.py`.

Ejecuta el servidor en vivo:

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

En el resultado, hay una línea con algo como:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Esa línea muestra la URL donde tu aplicación está siendo servida, en tu máquina local.

### Compruébalo

Abre tu navegador en <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Verás el response JSON como:

```JSON
{"message": "Hello World"}
```

### Documentación interactiva de la API

Ahora ve a <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Verás la documentación interactiva automática de la API (proporcionada por <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentación alternativa de la API

Y ahora, ve a <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Verás la documentación alternativa automática (proporcionada por <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** genera un "esquema" con toda tu API utilizando el estándar **OpenAPI** para definir APIs.

#### "Esquema"

Un "esquema" es una definición o descripción de algo. No el código que lo implementa, sino solo una descripción abstracta.

#### Esquema de la API

En este caso, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> es una especificación que dicta cómo definir un esquema de tu API.

Esta definición de esquema incluye los paths de tu API, los posibles parámetros que toman, etc.

#### Esquema de Datos

El término "esquema" también podría referirse a la forma de algunos datos, como el contenido JSON.

En ese caso, significaría los atributos del JSON, los tipos de datos que tienen, etc.

#### OpenAPI y JSON Schema

OpenAPI define un esquema de API para tu API. Y ese esquema incluye definiciones (o "esquemas") de los datos enviados y recibidos por tu API utilizando **JSON Schema**, el estándar para esquemas de datos JSON.

#### Revisa el `openapi.json`

Si tienes curiosidad por cómo se ve el esquema OpenAPI en bruto, FastAPI automáticamente genera un JSON (esquema) con las descripciones de toda tu API.

Puedes verlo directamente en: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

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

#### Para qué sirve OpenAPI

El esquema OpenAPI es lo que impulsa los dos sistemas de documentación interactiva incluidos.

Y hay docenas de alternativas, todas basadas en OpenAPI. Podrías añadir fácilmente cualquiera de esas alternativas a tu aplicación construida con **FastAPI**.

También podrías usarlo para generar código automáticamente, para clientes que se comuniquen con tu API. Por ejemplo, aplicaciones frontend, móviles o IoT.

## Recapitulación, paso a paso

### Paso 1: importa `FastAPI`

{* ../../docs_src/first_steps/tutorial001.py hl[1] *}

`FastAPI` es una clase de Python que proporciona toda la funcionalidad para tu API.

/// note | Detalles Técnicos

`FastAPI` es una clase que hereda directamente de `Starlette`.

Puedes usar toda la funcionalidad de <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> con `FastAPI` también.

///

### Paso 2: crea una "instance" de `FastAPI`

{* ../../docs_src/first_steps/tutorial001.py hl[3] *}

Aquí la variable `app` será una "instance" de la clase `FastAPI`.

Este será el punto principal de interacción para crear toda tu API.

### Paso 3: crea una *path operation*

#### Path

"Path" aquí se refiere a la última parte de la URL empezando desde la primera `/`.

Así que, en una URL como:

```
https://example.com/items/foo
```

...el path sería:

```
/items/foo
```

/// info

Un "path" también es comúnmente llamado "endpoint" o "ruta".

///

Mientras construyes una API, el "path" es la forma principal de separar "concerns" y "resources".

#### Operación

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

#### Define un *path operation decorator*

{* ../../docs_src/first_steps/tutorial001.py hl[6] *}

El `@app.get("/")` le dice a **FastAPI** que la función justo debajo se encarga de manejar requests que vayan a:

* el path `/`
* usando una <abbr title="un método HTTP GET"><code>get</code> operation</abbr>

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

/// tip

Eres libre de usar cada operación (método HTTP) como quieras.

**FastAPI** no fuerza ningún significado específico.

La información aquí se presenta como una guía, no un requisito.

Por ejemplo, cuando usas GraphQL normalmente realizas todas las acciones usando solo operaciones `POST`.

///

### Paso 4: define la **path operation function**

Esta es nuestra "**path operation function**":

* **path**: es `/`.
* **operation**: es `get`.
* **function**: es la función debajo del "decorador" (debajo de `@app.get("/")`).

{* ../../docs_src/first_steps/tutorial001.py hl[7] *}

Esta es una función de Python.

Será llamada por **FastAPI** cuando reciba un request en la URL "`/`" usando una operación `GET`.

En este caso, es una función `async`.

---

También podrías definirla como una función normal en lugar de `async def`:

{* ../../docs_src/first_steps/tutorial003.py hl[7] *}

/// note | Nota

Si no sabes la diferencia, revisa la sección [Async: *"¿Tienes prisa?"*](../async.md#in-a-hurry){.internal-link target=_blank}.

///

### Paso 5: retorna el contenido

{* ../../docs_src/first_steps/tutorial001.py hl[8] *}

Puedes retornar un `dict`, `list`, valores singulares como `str`, `int`, etc.

También puedes retornar modelos de Pydantic (verás más sobre eso más adelante).

Hay muchos otros objetos y modelos que serán automáticamente convertidos a JSON (incluyendo ORMs, etc). Intenta usar tus favoritos, es altamente probable que ya sean compatibles.

## Recapitulación

* Importa `FastAPI`.
* Crea una instancia `app`.
* Escribe un **path operation decorator** usando decoradores como `@app.get("/")`.
* Define una **path operation function**; por ejemplo, `def root(): ...`.
* Ejecuta el servidor de desarrollo usando el comando `fastapi dev`.
