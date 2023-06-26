# Características

## Características de FastAPI

**FastAPI** te provee lo siguiente:

### Basado en estándares abiertos

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> para la creación de APIs, incluyendo declaraciones de  <abbr title="en español: ruta. En inglés también conocido cómo: endpoints, routes">path</abbr> <abbr title="también conocido como HTTP methods, cómo POST, GET, PUT, DELETE">operations</abbr>, parámetros, <abbr title="cuerpo del mensaje HTTP">body</abbr> requests, seguridad, etc.
* Documentación automática del modelo de datos con <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (dado que OpenAPI mismo está basado en JSON Schema).
* Diseñado alrededor de estos estándares después de un estudio meticuloso. En vez de ser una capa añadida a último momento.
* Esto también permite la **generación automática de código de cliente** para muchos lenguajes.

### Documentación automática

Documentación interactiva de la API e interfaces web de exploración. Hay múltiples opciones, dos incluídas por defecto, porque el framework está basado en OpenAPI.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, con exploración interactiva, llama y prueba tu API directamente desde tu navegador.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Documentación alternativa de la API con <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Simplemente Python moderno

Todo está basado en las declaraciones de tipo de **Python 3.6** estándar (gracias a Pydantic). No necesitas aprender una sintáxis nueva, solo Python moderno.

Si necesitas un repaso de 2 minutos de cómo usar los tipos de Python (así no uses FastAPI) prueba el tutorial corto: [Python Types](python-types.md){.internal-link target=_blank}.

Escribes Python estándar con tipos así:

```Python
from datetime import date

from pydantic import BaseModel

# Declaras la variable como un str
# y obtienes soporte del editor dentro de la función
def main(user_id: str):
    return user_id


# Un modelo de Pydantic
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Este puede ser usado como:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! info
    `**second_user_data` significa:

    Pasa las <abbr title="en español key se refiere a la guía de un diccionario">keys</abbr> y los valores del dict `second_user_data` directamente como argumentos de key-value, equivalente a: `User(id=4, name="Mary", joined="2018-11-30")`

### Soporte del editor

El framework fue diseñado en su totalidad para ser fácil e intuitivo de usar. Todas las decisiones fueron probadas en múltiples editores antes de comenzar el desarrollo para asegurar la mejor experiencia de desarrollo.

En la última encuesta a desarrolladores de Python fue claro que <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">la característica más usada es el "autocompletado"</a>.

El framework **FastAPI** está creado para satisfacer eso. El autocompletado funciona en todas partes.

No vas a tener que volver a la documentación seguido.

Así es como tu editor te puede ayudar:

* en <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* en <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Obtendrás completado para tu código que podrías haber considerado imposible antes. Por ejemplo, el key `price` dentro del JSON body (que podría haber estado anidado) que viene de un request.

Ya no pasará que escribas los nombres de key equivocados, o que tengas que revisar constantemente la documentación o desplazarte arriba y abajo para saber si usaste `username` o `user_name`.

### Corto

Tiene **configuraciones por defecto** razonables para todo, con configuraciones opcionales en todas partes. Todos los parámetros pueden ser ajustados para tus necesidades y las de tu API.

Pero, todo **simplemente funciona** por defecto.

### Validación

* Validación para la mayoría (¿o todos?) los **tipos de datos** de Python incluyendo:
    * Objetos JSON (`dict`).
    * JSON array (`list`) definiendo tipos de ítem.
    * Campos de texto (`str`) definiendo longitudes mínimas y máximas.
    * Números (`int`, `float`) con valores mínimos y máximos, etc.

* Validación para tipos más exóticos como:
    * URL.
    * Email.
    * UUID.
    * ...y otros.

Toda la validación es manejada por **Pydantic**, que es robusto y sólidamente establecido.

### Seguridad y autenticación

La seguridad y la autenticación están integradas. Sin ningún compromiso con bases de datos ni modelos de datos.

Todos los schemes de seguridad están definidos en OpenAPI incluyendo:

* HTTP Basic.
* **OAuth2** (también con **JWT tokens**). Prueba el tutorial en [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* API keys en:
    * Headers.
    * Parámetros de Query.
    * Cookies, etc.

Más todas las características de seguridad de Starlette (incluyendo **session cookies**).

Todo ha sido construido como herramientas y componentes reutilizables que son fácilmente integrados con tus sistemas, almacenamiento de datos, bases de datos relacionales y no relacionales, etc.

### Dependency Injection

FastAPI incluye un sistema de <abbr title='En español: Inyección de Dependencias. También conocido en inglés cómo: "components", "resources", "services", "providers"'><strong>Dependency Injection</strong></abbr> extremadamente poderoso y fácil de usar.

* Inclusive las dependencias pueden tener dependencias creando una jerarquía o un **"grafo" de dependencias**.
* Todas son **manejadas automáticamente** por el framework.
* Todas las dependencias pueden requerir datos de los requests y aumentar las restricciones del *path operation* y la documentación automática.
* **Validación automática** inclusive para parámetros del *path operation* definidos en las dependencias.
* Soporte para sistemas complejos de autenticación de usuarios, **conexiones con bases de datos**, etc.
* **Sin comprometerse** con bases de datos, frontends, etc. Pero permitiendo integración fácil con todos ellos.

### "Plug-ins" ilimitados

O dicho de otra manera, no hay necesidad para "plug-ins". Importa y usa el código que necesites.

Cualquier integración está diseñada para que sea tan sencilla de usar (con dependencias) que puedas crear un "plug-in" para tu aplicación en dos líneas de código usando la misma estructura y sintáxis que usaste para tus *path operations*.

### Probado

* <abbr title="La cantidad de código que es probado automáticamente">Cobertura de pruebas</abbr> al 100%.
*  Base de código 100% <abbr title="Type annotations de Python, con esto tu editor y otras herramientas externas pueden darte mejor soporte">anotada con tipos</abbr>.
* Usado en aplicaciones en producción.

## Características de Starlette

**FastAPI** está basado y es completamente compatible con <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong></a>. Tanto así, que cualquier código de Starlette que tengas también funcionará.

`FastAPI` es realmente una sub-clase de `Starlette`. Así que, si ya conoces o usas Starlette, muchas de las características funcionarán de la misma manera.

Con **FastAPI** obtienes todas las características de **Starlette** (porque FastAPI es simplemente Starlette en esteroides):

* Desempeño realmente impresionante. Es uno <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank"> de los frameworks de Python más rápidos, a la par con **NodeJS** y **Go**</a>.
* Soporte para **WebSocket**.
* Soporte para **GraphQL**.
* <abbr title="En español: tareas que se ejecutan en el fondo, sin frenar requests, en el mismo proceso. En ingles: In-process background tasks">Tareas en background</abbr>.
* Eventos de startup y shutdown.
* Cliente de pruebas construido con HTTPX.
* **CORS**, GZip, Static Files, Streaming responses.
* Soporte para **Session and Cookie**.
* Cobertura de pruebas al 100%.
* Base de código 100% anotada con tipos.

## Características de Pydantic

**FastAPI** está basado y es completamente compatible con <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a>. Tanto así, que cualquier código de Pydantic que tengas también funcionará.

Esto incluye a librerías externas basadas en Pydantic como <abbr title="Object-Relational Mapper">ORM</abbr>s y <abbr title="Object-Document Mapper">ODM</abbr>s para bases de datos.

Esto también significa que en muchos casos puedes pasar el mismo objeto que obtuviste de un request **directamente a la base de datos**, dado que todo es validado automáticamente.

Lo mismo aplica para el sentido contrario. En muchos casos puedes pasarle el objeto que obtienes de la base de datos **directamente al cliente**.

Con **FastAPI** obtienes todas las características de **Pydantic** (dado que FastAPI está basado en Pydantic para todo el manejo de datos):

* **Sin dificultades para entender**:
    * No necesitas aprender un nuevo micro-lenguaje de definición de schemas.
    * Si sabes tipos de Python, sabes cómo usar Pydantic.
* Interactúa bien con tu **<abbr title="en inglés: Integrated Development Environment, similar a editor de código">IDE</abbr>/<abbr title="Un programa que chequea errores en el código">linter</abbr>/cerebro**:
    * Porque las estructuras de datos de Pydantic son solo <abbr title='En español: ejemplares. Aunque a veces los llaman incorrectamente "instancias"'>instances</abbr> de clases que tu defines, el auto-completado, el linting, mypy y tu intuición deberían funcionar bien con tus datos validados.
* **Rápido**:
    * En <a href="https://pydantic-docs.helpmanual.io/benchmarks/" class="external-link" target="_blank">benchmarks</a> Pydantic es más rápido que todas las otras <abbr title='Herramienta, paquete. A veces llamado "librería"'>libraries</abbr> probadas.
* Valida **estructuras complejas**:
    * Usa modelos jerárquicos de modelos de Pydantic, `typing` de Python,  `List` y `Dict`, etc.
    * Los validadores también permiten que se definan fácil y claramente schemas complejos de datos. Estos son chequeados y documentados como JSON Schema.
    * Puedes tener objetos de **JSON profundamente anidados** y que todos sean validados y anotados.
* **Extensible**:
    * Pydantic permite que se definan tipos de datos a la medida o puedes extender la validación con métodos en un modelo decorado con el <abbr title="en inglés: validator decorator"> decorador de validación</abbr>.
* Cobertura de pruebas al 100%.
