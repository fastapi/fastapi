# Declarar Datos de Ejemplo de Request { #declare-request-example-data }

Puedes declarar ejemplos de los datos que tu aplicación puede recibir.

Aquí tienes varias formas de hacerlo.

## Datos extra de JSON Schema en modelos de Pydantic { #extra-json-schema-data-in-pydantic-models }

Puedes declarar `examples` para un modelo de Pydantic que se añadirá al JSON Schema generado.

{* ../../docs_src/schema_extra_example/tutorial001_py310.py hl[13:24] *}

Esa información extra se añadirá tal cual al **JSON Schema** resultante para ese modelo, y se usará en la documentación de la API.

Puedes usar el atributo `model_config` que toma un `dict` como se describe en [Documentación de Pydantic: Configuración](https://docs.pydantic.dev/latest/api/config/).

Puedes establecer `"json_schema_extra"` con un `dict` que contenga cualquier dato adicional que te gustaría que aparezca en el JSON Schema generado, incluyendo `examples`.

/// tip | Consejo

Podrías usar la misma técnica para extender el JSON Schema y añadir tu propia información extra personalizada.

Por ejemplo, podrías usarlo para añadir metadatos para una interfaz de usuario frontend, etc.

///

/// info | Información

OpenAPI 3.1.0 (usado desde FastAPI 0.99.0) añadió soporte para `examples`, que es parte del estándar de **JSON Schema**.

Antes de eso, solo soportaba la palabra clave `example` con un solo ejemplo. Eso aún es soportado por OpenAPI 3.1.0, pero está obsoleto y no es parte del estándar de JSON Schema. Así que se te anima a migrar `example` a `examples`. 🤓

Puedes leer más al final de esta página.

///

## Argumentos adicionales en `Field` { #field-additional-arguments }

Cuando usas `Field()` con modelos de Pydantic, también puedes declarar `examples` adicionales:

{* ../../docs_src/schema_extra_example/tutorial002_py310.py hl[2,8:11] *}

## `examples` en JSON Schema - OpenAPI { #examples-in-json-schema-openapi }

Cuando usas cualquiera de:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

también puedes declarar un grupo de `examples` con información adicional que se añadirá a sus **JSON Schemas** dentro de **OpenAPI**.

### `Body` con `examples` { #body-with-examples }

Aquí pasamos `examples` que contiene un ejemplo de los datos esperados en `Body()`:

{* ../../docs_src/schema_extra_example/tutorial003_an_py310.py hl[22:29] *}

### Ejemplo en la interfaz de documentación { #example-in-the-docs-ui }

Con cualquiera de los métodos anteriores se vería así en los `/docs`:

<img src="/img/tutorial/body-fields/image01.png">

### `Body` con múltiples `examples` { #body-with-multiple-examples }

Por supuesto, también puedes pasar múltiples `examples`:

{* ../../docs_src/schema_extra_example/tutorial004_an_py310.py hl[23:38] *}

Cuando haces esto, los ejemplos serán parte del **JSON Schema** interno para esos datos del body.

Sin embargo, al <dfn title="2023-08-26">momento de escribir esto</dfn>, Swagger UI, la herramienta encargada de mostrar la interfaz de documentación, no soporta mostrar múltiples ejemplos para los datos en **JSON Schema**. Pero lee más abajo para una solución alternativa.

### `examples` específicos de OpenAPI { #openapi-specific-examples }

Desde antes de que **JSON Schema** soportara `examples`, OpenAPI tenía soporte para un campo diferente también llamado `examples`.

Estos `examples` específicos de **OpenAPI** van en otra sección en la especificación de OpenAPI. Van en los **detalles para cada *path operation***, no dentro de cada JSON Schema.

Y Swagger UI ha soportado este campo particular de `examples` por un tiempo. Así que, puedes usarlo para **mostrar** diferentes **ejemplos en la interfaz de documentación**.

La forma de este campo específico de OpenAPI `examples` es un `dict` con **múltiples ejemplos** (en lugar de una `list`), cada uno con información adicional que también se añadirá a **OpenAPI**.

Esto no va dentro de cada JSON Schema contenido en OpenAPI, esto va afuera, directamente en la *path operation*.

### Usando el Parámetro `openapi_examples` { #using-the-openapi-examples-parameter }

Puedes declarar los `examples` específicos de OpenAPI en FastAPI con el parámetro `openapi_examples` para:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

Las claves del `dict` identifican cada ejemplo, y cada valor es otro `dict`.

Cada `dict` específico del ejemplo en los `examples` puede contener:

* `summary`: Descripción corta del ejemplo.
* `description`: Una descripción larga que puede contener texto Markdown.
* `value`: Este es el ejemplo real mostrado, e.g. un `dict`.
* `externalValue`: alternativa a `value`, una URL que apunta al ejemplo. Aunque esto puede no ser soportado por tantas herramientas como `value`.

Puedes usarlo así:

{* ../../docs_src/schema_extra_example/tutorial005_an_py310.py hl[23:49] *}

### Ejemplos de OpenAPI en la Interfaz de Documentación { #openapi-examples-in-the-docs-ui }

Con `openapi_examples` añadido a `Body()`, los `/docs` se verían así:

<img src="/img/tutorial/body-fields/image02.png">

## Detalles Técnicos { #technical-details }

/// tip | Consejo

Si ya estás usando la versión **0.99.0 o superior** de **FastAPI**, probablemente puedes **omitir** estos detalles.

Son más relevantes para versiones más antiguas, antes de que OpenAPI 3.1.0 estuviera disponible.

Puedes considerar esto una breve lección de **historia** de OpenAPI y JSON Schema. 🤓

///

/// warning | Advertencia

Estos son detalles muy técnicos sobre los estándares **JSON Schema** y **OpenAPI**.

Si las ideas anteriores ya funcionan para ti, eso podría ser suficiente, y probablemente no necesites estos detalles, siéntete libre de omitirlos.

///

Antes de OpenAPI 3.1.0, OpenAPI usaba una versión más antigua y modificada de **JSON Schema**.

JSON Schema no tenía `examples`, así que OpenAPI añadió su propio campo `example` a su versión modificada.

OpenAPI también añadió los campos `example` y `examples` a otras partes de la especificación:

* [`Parameter Object` (en la especificación)](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object) que era usado por FastAPI:
    * `Path()`
    * `Query()`
    * `Header()`
    * `Cookie()`
* [`Request Body Object`, en el campo `content`, sobre el `Media Type Object` (en la especificación)](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object) que era usado por FastAPI:
    * `Body()`
    * `File()`
    * `Form()`

/// info | Información

Este viejo parámetro `examples` específico de OpenAPI ahora es `openapi_examples` desde FastAPI `0.103.0`.

///

### Campo `examples` de JSON Schema { #json-schemas-examples-field }

Pero luego JSON Schema añadió un [campo `examples`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5) a una nueva versión de la especificación.

Y entonces el nuevo OpenAPI 3.1.0 se basó en la última versión (JSON Schema 2020-12) que incluía este nuevo campo `examples`.

Y ahora este nuevo campo `examples` tiene precedencia sobre el viejo campo único (y personalizado) `example`, que ahora está obsoleto.

Este nuevo campo `examples` en JSON Schema es **solo una `list`** de ejemplos, no un dict con metadatos adicionales como en los otros lugares en OpenAPI (descritos arriba).

/// info | Información

Incluso después de que OpenAPI 3.1.0 fue lanzado con esta nueva integración más sencilla con JSON Schema, por un tiempo, Swagger UI, la herramienta que proporciona la documentación automática, no soportaba OpenAPI 3.1.0 (lo hace desde la versión 5.0.0 🎉).

Debido a eso, las versiones de FastAPI anteriores a 0.99.0 todavía usaban versiones de OpenAPI menores a 3.1.0.

///

### `examples` de Pydantic y FastAPI { #pydantic-and-fastapi-examples }

Cuando añades `examples` dentro de un modelo de Pydantic, usando `schema_extra` o `Field(examples=["something"])`, ese ejemplo se añade al **JSON Schema** para ese modelo de Pydantic.

Y ese **JSON Schema** del modelo de Pydantic se incluye en el **OpenAPI** de tu API, y luego se usa en la interfaz de documentación.

En las versiones de FastAPI antes de 0.99.0 (0.99.0 y superiores usan el nuevo OpenAPI 3.1.0) cuando usabas `example` o `examples` con cualquiera de las otras utilidades (`Query()`, `Body()`, etc.) esos ejemplos no se añadían al JSON Schema que describe esos datos (ni siquiera a la propia versión de JSON Schema de OpenAPI), se añadían directamente a la declaración de la *path operation* en OpenAPI (fuera de las partes de OpenAPI que usan JSON Schema).

Pero ahora que FastAPI 0.99.0 y superiores usa OpenAPI 3.1.0, que usa JSON Schema 2020-12, y Swagger UI 5.0.0 y superiores, todo es más consistente y los ejemplos se incluyen en JSON Schema.

### Swagger UI y `examples` específicos de OpenAPI { #swagger-ui-and-openapi-specific-examples }

Ahora, como Swagger UI no soportaba múltiples ejemplos de JSON Schema (a fecha de 2023-08-26), los usuarios no tenían una forma de mostrar múltiples ejemplos en la documentación.

Para resolver eso, FastAPI `0.103.0` **añadió soporte** para declarar el mismo viejo campo **específico de OpenAPI** `examples` con el nuevo parámetro `openapi_examples`. 🤓

### Resumen { #summary }

Solía decir que no me gustaba mucho la historia... y mírame ahora dando lecciones de "historia tecnológica". 😅

En resumen, **actualiza a FastAPI 0.99.0 o superior**, y las cosas son mucho **más simples, consistentes e intuitivas**, y no necesitas conocer todos estos detalles históricos. 😎
