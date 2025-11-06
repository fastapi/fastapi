# FastAPI

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, alto rendimiento, fácil de aprender, rápido de programar, listo para producción</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentación**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Código Fuente**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI es un framework web moderno, rápido (de alto rendimiento), para construir APIs con Python basado en las anotaciones de tipos estándar de Python.

Las características clave son:

* **Rápido**: Muy alto rendimiento, a la par con **NodeJS** y **Go** (gracias a Starlette y Pydantic). [Uno de los frameworks Python más rápidos disponibles](#performance).
* **Rápido de programar**: Aumenta la velocidad para desarrollar funcionalidades en aproximadamente un 200% a 300%. *
* **Menos bugs**: Reduce en aproximadamente un 40% los errores inducidos por humanos (desarrolladores). *
* **Intuitivo**: Gran soporte para editores. <abbr title="también conocido como autocompletado, IntelliSense">Autocompletado</abbr> en todas partes. Menos tiempo depurando.
* **Fácil**: Diseñado para ser fácil de usar y aprender. Menos tiempo leyendo documentación.
* **Corto**: Minimiza la duplicación de código. Múltiples funcionalidades desde cada declaración de parámetro. Menos bugs.
* **Robusto**: Obtén código listo para producción. Con documentación interactiva automática.
* **Basado en estándares**: Basado (y completamente compatible) con los estándares abiertos para APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (anteriormente conocido como Swagger) y <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* estimación basada en pruebas con un equipo de desarrollo interno, construyendo aplicaciones de producción.</small>

## Sponsors

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Otros sponsors</a>

## Opiniones

"_[...] Estoy usando **FastAPI** un montón estos días. [...] De hecho, estoy planeando usarlo para todos los servicios de **ML de mi equipo en Microsoft**. Algunos de ellos se están integrando en el núcleo del producto **Windows** y algunos productos de **Office**._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_Adoptamos el paquete **FastAPI** para crear un servidor **REST** que pueda ser consultado para obtener **predicciones**. [para Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, y Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** se complace en anunciar el lanzamiento de código abierto de nuestro framework de orquestación de **gestión de crisis**: **Dispatch**! [construido con **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Estoy súper emocionado con **FastAPI**. ¡Es tan divertido!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">host del podcast Python Bytes</a></strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Honestamente, lo que has construido parece súper sólido y pulido. En muchos aspectos, es lo que quería que **Hug** fuera; es realmente inspirador ver a alguien construir eso._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">creador de Hug</a></strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Si estás buscando aprender un **framework moderno** para construir APIs REST, échale un vistazo a **FastAPI** [...] Es rápido, fácil de usar y fácil de aprender [...]_"

"_Nos hemos cambiado a **FastAPI** para nuestras **APIs** [...] Creo que te gustará [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">fundadores de Explosion AI</a> - <a href="https://spacy.io" target="_blank">creadores de spaCy</a></strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_Si alguien está buscando construir una API de Python para producción, altamente recomendaría **FastAPI**. Está **hermosamente diseñado**, es **simple de usar** y **altamente escalable**, se ha convertido en un **componente clave** en nuestra estrategia de desarrollo API primero y está impulsando muchas automatizaciones y servicios como nuestro Ingeniero Virtual TAC._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, el FastAPI de las CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Si estás construyendo una aplicación de <abbr title="Interfaz de Línea de Comandos">CLI</abbr> para ser usada en el terminal en lugar de una API web, revisa <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** es el hermano pequeño de FastAPI. Y está destinado a ser el **FastAPI de las CLIs**. ⌨️ 🚀

## Requisitos

FastAPI se apoya en hombros de gigantes:

* <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> para las partes web.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> para las partes de datos.

## Instalación

Crea y activa un <a href="https://fastapi.tiangolo.com/virtual-environments/" class="external-link" target="_blank">entorno virtual</a> y luego instala FastAPI:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Nota**: Asegúrate de poner `"fastapi[standard]"` entre comillas para asegurar que funcione en todas las terminales.

## Ejemplo

### Créalo

* Crea un archivo `main.py` con:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>O usa <code>async def</code>...</summary>

Si tu código usa `async` / `await`, usa `async def`:

```Python hl_lines="9  14"
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

**Nota**:

Si no lo sabes, revisa la sección _"¿Con prisa?"_ sobre <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` y `await` en la documentación</a>.

</details>

### Córrelo

Corre el servidor con:

<div class="termy">

```console
$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>Acerca del comando <code>fastapi dev main.py</code>...</summary>

El comando `fastapi dev` lee tu archivo `main.py`, detecta la app **FastAPI** en él y arranca un servidor usando <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>.

Por defecto, `fastapi dev` comenzará con auto-recarga habilitada para el desarrollo local.

Puedes leer más sobre esto en la <a href="https://fastapi.tiangolo.com/fastapi-cli/" target="_blank">documentación del CLI de FastAPI</a>.

</details>

### Revísalo

Abre tu navegador en <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Verás el response JSON como:

```JSON
{"item_id": 5, "q": "somequery"}
```

Ya creaste una API que:

* Recibe requests HTTP en los _paths_ `/` y `/items/{item_id}`.
* Ambos _paths_ toman _operaciones_ `GET` (también conocidas como métodos HTTP).
* El _path_ `/items/{item_id}` tiene un _parámetro de path_ `item_id` que debe ser un `int`.
* El _path_ `/items/{item_id}` tiene un _parámetro de query_ `q` opcional que es un `str`.

### Documentación interactiva de la API

Ahora ve a <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Verás la documentación interactiva automática de la API (proporcionada por <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentación de API Alternativa

Y ahora, ve a <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Verás la documentación alternativa automática (proporcionada por <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Actualización del Ejemplo

Ahora modifica el archivo `main.py` para recibir un body desde un request `PUT`.

Declara el body usando tipos estándar de Python, gracias a Pydantic.

```Python hl_lines="4  9-12  25-27"
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

El servidor `fastapi dev` debería recargarse automáticamente.

### Actualización de la Documentación Interactiva de la API

Ahora ve a <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* La documentación interactiva de la API se actualizará automáticamente, incluyendo el nuevo body:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Haz clic en el botón "Try it out", te permite llenar los parámetros e interactuar directamente con la API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Luego haz clic en el botón "Execute", la interfaz de usuario se comunicará con tu API, enviará los parámetros, obtendrá los resultados y los mostrará en la pantalla:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Actualización de la Documentación Alternativa de la API

Y ahora, ve a <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* La documentación alternativa también reflejará el nuevo parámetro de query y body:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Resumen

En resumen, declaras **una vez** los tipos de parámetros, body, etc. como parámetros de función.

Lo haces con tipos estándar modernos de Python.

No tienes que aprender una nueva sintaxis, los métodos o clases de un paquete específico, etc.

Solo **Python** estándar.

Por ejemplo, para un `int`:

```Python
item_id: int
```

o para un modelo `Item` más complejo:

```Python
item: Item
```

...y con esa única declaración obtienes:

* Soporte para editores, incluyendo:
    * Autocompletado.
    * Chequeo de tipos.
* Validación de datos:
    * Errores automáticos y claros cuando los datos son inválidos.
    * Validación incluso para objetos JSON profundamente anidados.
* <abbr title="también conocido como: serialización, parsing, marshalling">Conversión</abbr> de datos de entrada: de la red a los datos y tipos de Python. Leyendo desde:
    * JSON.
    * Parámetros de path.
    * Parámetros de query.
    * Cookies.
    * Headers.
    * Forms.
    * Archivos.
* <abbr title="también conocido como: serialización, parsing, marshalling">Conversión</abbr> de datos de salida: convirtiendo de datos y tipos de Python a datos de red (como JSON):
    * Convertir tipos de Python (`str`, `int`, `float`, `bool`, `list`, etc).
    * Objetos `datetime`.
    * Objetos `UUID`.
    * Modelos de base de datos.
    * ...y muchos más.
* Documentación interactiva automática de la API, incluyendo 2 interfaces de usuario alternativas:
    * Swagger UI.
    * ReDoc.

---

Volviendo al ejemplo de código anterior, **FastAPI**:

* Validará que haya un `item_id` en el path para requests `GET` y `PUT`.
* Validará que el `item_id` sea del tipo `int` para requests `GET` y `PUT`.
    * Si no lo es, el cliente verá un error útil y claro.
* Comprobará si hay un parámetro de query opcional llamado `q` (como en `http://127.0.0.1:8000/items/foo?q=somequery`) para requests `GET`.
    * Como el parámetro `q` está declarado con `= None`, es opcional.
    * Sin el `None` sería requerido (como lo es el body en el caso con `PUT`).
* Para requests `PUT` a `/items/{item_id}`, leerá el body como JSON:
    * Comprobará que tiene un atributo requerido `name` que debe ser un `str`.
    * Comprobará que tiene un atributo requerido `price` que debe ser un `float`.
    * Comprobará que tiene un atributo opcional `is_offer`, que debe ser un `bool`, si está presente.
    * Todo esto también funcionaría para objetos JSON profundamente anidados.
* Convertirá de y a JSON automáticamente.
* Documentará todo con OpenAPI, que puede ser usado por:
    * Sistemas de documentación interactiva.
    * Sistemas de generación automática de código cliente, para muchos lenguajes.
* Proporcionará 2 interfaces web de documentación interactiva directamente.

---

Solo tocamos los conceptos básicos, pero ya te haces una idea de cómo funciona todo.

Intenta cambiar la línea con:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...desde:

```Python
        ... "item_name": item.name ...
```

...a:

```Python
        ... "item_price": item.price ...
```

...y observa cómo tu editor autocompleta los atributos y conoce sus tipos:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Para un ejemplo más completo incluyendo más funcionalidades, ve al <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - Guía del Usuario</a>.

**Alerta de spoilers**: el tutorial - guía del usuario incluye:

* Declaración de **parámetros** desde otros lugares diferentes como: **headers**, **cookies**, **campos de formulario** y **archivos**.
* Cómo establecer **restricciones de validación** como `maximum_length` o `regex`.
* Un sistema de **<abbr title="también conocido como componentes, recursos, proveedores, servicios, inyectables">Inyección de Dependencias</abbr>** muy poderoso y fácil de usar.
* Seguridad y autenticación, incluyendo soporte para **OAuth2** con **tokens JWT** y autenticación **HTTP Basic**.
* Técnicas más avanzadas (pero igualmente fáciles) para declarar **modelos JSON profundamente anidados** (gracias a Pydantic).
* Integración con **GraphQL** usando <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> y otros paquetes.
* Muchas funcionalidades extra (gracias a Starlette) como:
    * **WebSockets**
    * pruebas extremadamente fáciles basadas en HTTPX y `pytest`
    * **CORS**
    * **Sesiones de Cookies**
    * ...y más.

## Rendimiento

Benchmarks independientes de TechEmpower muestran aplicaciones **FastAPI** ejecutándose bajo Uvicorn como <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">uno de los frameworks Python más rápidos disponibles</a>, solo por debajo de Starlette y Uvicorn (usados internamente por FastAPI). (*)

Para entender más sobre esto, ve la sección <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Dependencias

FastAPI depende de Pydantic y Starlette.

### Dependencias `standard`

Cuando instalas FastAPI con `pip install "fastapi[standard]"` viene con el grupo `standard` de dependencias opcionales:

Usadas por Pydantic:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - para validación de correos electrónicos.

Usadas por Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Requerido si deseas usar el `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Requerido si deseas usar la configuración de plantilla predeterminada.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - Requerido si deseas soportar <abbr title="convertir el string que viene de un request HTTP en datos de Python">"parsing"</abbr> de forms, con `request.form()`.

Usadas por FastAPI / Starlette:

* <a href="https://www.uvicorn.dev" target="_blank"><code>uvicorn</code></a> - para el servidor que carga y sirve tu aplicación. Esto incluye `uvicorn[standard]`, que incluye algunas dependencias (por ejemplo, `uvloop`) necesarias para servir con alto rendimiento.
* `fastapi-cli` - para proporcionar el comando `fastapi`.

### Sin Dependencias `standard`

Si no deseas incluir las dependencias opcionales `standard`, puedes instalar con `pip install fastapi` en lugar de `pip install "fastapi[standard]"`.

### Dependencias Opcionales Adicionales

Existen algunas dependencias adicionales que podrías querer instalar.

Dependencias opcionales adicionales de Pydantic:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - para la gestión de configuraciones.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - para tipos extra para ser usados con Pydantic.

Dependencias opcionales adicionales de FastAPI:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Requerido si deseas usar `ORJSONResponse`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Requerido si deseas usar `UJSONResponse`.

## Licencia

Este proyecto tiene licencia bajo los términos de la licencia MIT.
