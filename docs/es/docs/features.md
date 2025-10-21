# Funcionalidades

## Funcionalidades de FastAPI

**FastAPI** te ofrece lo siguiente:

### Basado en estándares abiertos

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> para la creación de APIs, incluyendo declaraciones de <abbr title="también conocido como: endpoints, rutas">path</abbr> <abbr title="también conocido como métodos HTTP, como POST, GET, PUT, DELETE">operations</abbr>, parámetros, request bodies, seguridad, etc.
* Documentación automática de modelos de datos con <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (ya que OpenAPI en sí mismo está basado en JSON Schema).
* Diseñado alrededor de estos estándares, tras un estudio meticuloso. En lugar de ser una capa adicional.
* Esto también permite el uso de **generación de código cliente automática** en muchos idiomas.

### Documentación automática

Interfaces web de documentación y exploración de APIs interactivas. Como el framework está basado en OpenAPI, hay múltiples opciones, 2 incluidas por defecto.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, con exploración interactiva, llama y prueba tu API directamente desde el navegador.

![Interacción Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Documentación alternativa de API con <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Solo Python moderno

Todo está basado en declaraciones estándar de **tipos en Python** (gracias a Pydantic). Sin nueva sintaxis que aprender. Solo Python moderno estándar.

Si necesitas un repaso de 2 minutos sobre cómo usar tipos en Python (aunque no uses FastAPI), revisa el tutorial corto: [Tipos en Python](python-types.md){.internal-link target=_blank}.

Escribes Python estándar con tipos:

```Python
from datetime import date

from pydantic import BaseModel

# Declara una variable como un str
# y obtiene soporte del editor dentro de la función
def main(user_id: str):
    return user_id


# Un modelo de Pydantic
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Que luego puede ser usado como:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

/// info | Información

`**second_user_data` significa:

Pasa las claves y valores del dict `second_user_data` directamente como argumentos de clave-valor, equivalente a: `User(id=4, name="Mary", joined="2018-11-30")`

///

### Soporte del editor

Todo el framework fue diseñado para ser fácil e intuitivo de usar, todas las decisiones fueron probadas en múltiples editores incluso antes de comenzar el desarrollo, para asegurar la mejor experiencia de desarrollo.

En las encuestas a desarrolladores de Python, es claro <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">que una de las funcionalidades más usadas es el "autocompletado"</a>.

Todo el framework **FastAPI** está basado para satisfacer eso. El autocompletado funciona en todas partes.

Rara vez necesitarás regresar a la documentación.

Aquí está cómo tu editor podría ayudarte:

* en <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

![soporte del editor](https://fastapi.tiangolo.com/img/vscode-completion.png)

* en <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![soporte del editor](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Obtendrás autocompletado en código que podrías considerar imposible antes. Por ejemplo, la clave `price` dentro de un cuerpo JSON (que podría haber estado anidado) que proviene de un request.

No más escribir nombres de claves incorrectos, yendo de un lado a otro entre la documentación, o desplazándote hacia arriba y abajo para encontrar si finalmente usaste `username` o `user_name`.

### Breve

Tiene **valores predeterminados** sensatos para todo, con configuraciones opcionales en todas partes. Todos los parámetros se pueden ajustar finamente para hacer lo que necesitas y para definir el API que necesitas.

Pero por defecto, todo **"simplemente funciona"**.

### Validación

* Validación para la mayoría (¿o todas?) de los **tipos de datos** de Python, incluyendo:
    * Objetos JSON (`dict`).
    * Array JSON (`list`) definiendo tipos de elementos.
    * Campos de cadena de caracteres (`str`), definiendo longitudes mínimas y máximas.
    * Números (`int`, `float`) con valores mínimos y máximos, etc.

* Validación para tipos más exóticos, como:
    * URL.
    * Email.
    * UUID.
    * ...y otros.

Toda la validación es manejada por **Pydantic**, una herramienta bien establecida y robusta.

### Seguridad y autenticación

Seguridad y autenticación integradas. Sin ningún compromiso con bases de datos o modelos de datos.

Todos los esquemas de seguridad definidos en OpenAPI, incluyendo:

* HTTP Básico.
* **OAuth2** (también con **tokens JWT**). Revisa el tutorial sobre [OAuth2 con JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* API keys en:
    * Headers.
    * Parámetros de query.
    * Cookies, etc.

Además de todas las características de seguridad de Starlette (incluyendo **cookies de sesión**).

Todo construido como herramientas y componentes reutilizables que son fáciles de integrar con tus sistemas, almacenes de datos, bases de datos relacionales y NoSQL, etc.

### Inyección de dependencias

FastAPI incluye un sistema de <abbr title='también conocido como "componentes", "recursos", "servicios", "proveedores"'><strong>Inyección de Dependencias</strong></abbr> extremadamente fácil de usar, pero extremadamente potente.

* Incluso las dependencias pueden tener dependencias, creando una jerarquía o **"gráfico de dependencias"**.
* Todo **manejado automáticamente** por el framework.
* Todas las dependencias pueden requerir datos de los requests y **aumentar las restricciones de la path operation** y la documentación automática.
* **Validación automática** incluso para los parámetros de *path operation* definidos en las dependencias.
* Soporte para sistemas de autenticación de usuario complejos, **conexiones a bases de datos**, etc.
* **Sin compromisos** con bases de datos, frontends, etc. Pero fácil integración con todos ellos.

### "Plug-ins" ilimitados

O de otra manera, no hay necesidad de ellos, importa y usa el código que necesitas.

Cualquier integración está diseñada para ser tan simple de usar (con dependencias) que puedes crear un "plug-in" para tu aplicación en 2 líneas de código usando la misma estructura y sintaxis utilizada para tus *path operations*.

### Probado

* 100% de <abbr title="La cantidad de código que se prueba automáticamente">cobertura de tests</abbr>.
* Código completamente <abbr title="Anotaciones de tipos en Python, con esto tu editor y herramientas externas pueden ofrecerte mejor soporte">anotado con tipos</abbr>.
* Usado en aplicaciones en producción.

## Funcionalidades de Starlette

**FastAPI** es totalmente compatible con (y está basado en) <a href="https://www.starlette.dev/" class="external-link" target="_blank"><strong>Starlette</strong></a>. Así que, cualquier código adicional de Starlette que tengas, también funcionará.

`FastAPI` es en realidad una subclase de `Starlette`. Así que, si ya conoces o usas Starlette, la mayoría de las funcionalidades funcionarán de la misma manera.

Con **FastAPI** obtienes todas las funcionalidades de **Starlette** (ya que FastAPI es simplemente Starlette potenciado):

* Rendimiento seriamente impresionante. Es <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">uno de los frameworks de Python más rápidos disponibles, a la par de **NodeJS** y **Go**</a>.
* Soporte para **WebSocket**.
* Tareas en segundo plano en el mismo proceso.
* Eventos de inicio y apagado.
* Cliente de prueba basado en HTTPX.
* **CORS**, GZip, archivos estáticos, responses en streaming.
* Soporte para **Session y Cookie**.
* Cobertura de tests del 100%.
* Código completamente anotado con tipos.

## Funcionalidades de Pydantic

**FastAPI** es totalmente compatible con (y está basado en) <a href="https://docs.pydantic.dev/" class="external-link" target="_blank"><strong>Pydantic</strong></a>. Por lo tanto, cualquier código adicional de Pydantic que tengas, también funcionará.

Incluyendo paquetes externos también basados en Pydantic, como <abbr title="Object-Relational Mapper">ORM</abbr>s, <abbr title="Object-Document Mapper">ODM</abbr>s para bases de datos.

Esto también significa que, en muchos casos, puedes pasar el mismo objeto que obtienes de un request **directamente a la base de datos**, ya que todo se valida automáticamente.

Lo mismo aplica al revés, en muchos casos puedes simplemente pasar el objeto que obtienes de la base de datos **directamente al cliente**.

Con **FastAPI** obtienes todas las funcionalidades de **Pydantic** (ya que FastAPI está basado en Pydantic para todo el manejo de datos):

* **Sin complicaciones**:
    * Sin micro-lenguaje de definición de esquemas nuevo que aprender.
    * Si conoces los tipos en Python sabes cómo usar Pydantic.
* Se lleva bien con tu **<abbr title="Entorno de Desarrollo Integrado, similar a un editor de código">IDE</abbr>/<abbr title="Un programa que verifica errores de código">linter</abbr>/cerebro**:
    * Porque las estructuras de datos de pydantic son solo instances de clases que defines; autocompletado, linting, mypy y tu intuición deberían funcionar correctamente con tus datos validados.
* Valida **estructuras complejas**:
    * Uso de modelos jerárquicos de Pydantic, `List` y `Dict` de `typing` de Python, etc.
    * Y los validadores permiten definir, verificar y documentar de manera clara y fácil esquemas de datos complejos como JSON Schema.
    * Puedes tener objetos JSON profundamente **anidados** y validarlos todos y anotarlos.
* **Extensible**:
    * Pydantic permite definir tipos de datos personalizados o puedes extender la validación con métodos en un modelo decorados con el decorador validator.
* Cobertura de tests del 100%.
