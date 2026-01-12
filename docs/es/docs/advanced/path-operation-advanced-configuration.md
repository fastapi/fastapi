# Configuración Avanzada de Path Operation { #path-operation-advanced-configuration }

## operationId de OpenAPI { #openapi-operationid }

/// warning | Advertencia

Si no eres un "experto" en OpenAPI, probablemente no necesites esto.

///

Puedes establecer el `operationId` de OpenAPI para ser usado en tu *path operation* con el parámetro `operation_id`.

Tendrías que asegurarte de que sea único para cada operación.

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py39.py hl[6] *}

### Usar el nombre de la *path operation function* como el operationId { #using-the-path-operation-function-name-as-the-operationid }

Si quieres usar los nombres de las funciones de tus APIs como `operationId`s, puedes iterar sobre todas ellas y sobrescribir el `operation_id` de cada *path operation* usando su `APIRoute.name`.

Deberías hacerlo después de agregar todas tus *path operations*.

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py39.py hl[2, 12:21, 24] *}

/// tip | Consejo

Si llamas manualmente a `app.openapi()`, deberías actualizar los `operationId`s antes de eso.

///

/// warning | Advertencia

Si haces esto, tienes que asegurarte de que cada una de tus *path operation functions* tenga un nombre único.

Incluso si están en diferentes módulos (archivos de Python).

///

## Excluir de OpenAPI { #exclude-from-openapi }

Para excluir una *path operation* del esquema OpenAPI generado (y por lo tanto, de los sistemas de documentación automática), utiliza el parámetro `include_in_schema` y configúralo en `False`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py39.py hl[6] *}

## Descripción avanzada desde el docstring { #advanced-description-from-docstring }

Puedes limitar las líneas usadas del docstring de una *path operation function* para OpenAPI.

Añadir un `\f` (un carácter "form feed" escapado) hace que **FastAPI** trunque la salida usada para OpenAPI en este punto.

No aparecerá en la documentación, pero otras herramientas (como Sphinx) podrán usar el resto.

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## Responses Adicionales { #additional-responses }

Probablemente has visto cómo declarar el `response_model` y el `status_code` para una *path operation*.

Eso define los metadatos sobre el response principal de una *path operation*.

También puedes declarar responses adicionales con sus modelos, códigos de estado, etc.

Hay un capítulo entero en la documentación sobre ello, puedes leerlo en [Responses Adicionales en OpenAPI](additional-responses.md){.internal-link target=_blank}.

## OpenAPI Extra { #openapi-extra }

Cuando declaras una *path operation* en tu aplicación, **FastAPI** genera automáticamente los metadatos relevantes sobre esa *path operation* para incluirlos en el esquema de OpenAPI.

/// note | Detalles técnicos

En la especificación de OpenAPI se llama el <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Objeto de Operación</a>.

///

Tiene toda la información sobre la *path operation* y se usa para generar la documentación automática.

Incluye los `tags`, `parameters`, `requestBody`, `responses`, etc.

Este esquema de OpenAPI específico de *path operation* normalmente se genera automáticamente por **FastAPI**, pero también puedes extenderlo.

/// tip | Consejo

Este es un punto de extensión de bajo nivel.

Si solo necesitas declarar responses adicionales, una forma más conveniente de hacerlo es con [Responses Adicionales en OpenAPI](additional-responses.md){.internal-link target=_blank}.

///

Puedes extender el esquema de OpenAPI para una *path operation* usando el parámetro `openapi_extra`.

### Extensiones de OpenAPI { #openapi-extensions }

Este `openapi_extra` puede ser útil, por ejemplo, para declarar [Extensiones de OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions):

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py39.py hl[6] *}

Si abres la documentación automática de la API, tu extensión aparecerá en la parte inferior de la *path operation* específica.

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

Y si ves el OpenAPI resultante (en `/openapi.json` en tu API), verás tu extensión como parte de la *path operation* específica también:

```JSON hl_lines="22"
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "x-aperture-labs-portal": "blue"
            }
        }
    }
}
```

### Esquema de *path operation* personalizada de OpenAPI { #custom-openapi-path-operation-schema }

El diccionario en `openapi_extra` se combinará profundamente con el esquema de OpenAPI generado automáticamente para la *path operation*.

Por lo tanto, podrías añadir datos adicionales al esquema generado automáticamente.

Por ejemplo, podrías decidir leer y validar el request con tu propio código, sin usar las funcionalidades automáticas de FastAPI con Pydantic, pero aún podrías querer definir el request en el esquema de OpenAPI.

Podrías hacer eso con `openapi_extra`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py39.py hl[19:36, 39:40] *}

En este ejemplo, no declaramos ningún modelo Pydantic. De hecho, el request body ni siquiera se <abbr title="converted from some plain format, like bytes, into Python objects - convertido de algún formato plano, como bytes, a objetos de Python">parse</abbr> como JSON, se lee directamente como `bytes`, y la función `magic_data_reader()` sería la encargada de parsearlo de alguna manera.

Sin embargo, podemos declarar el esquema esperado para el request body.

### Tipo de contenido personalizado de OpenAPI { #custom-openapi-content-type }

Usando este mismo truco, podrías usar un modelo Pydantic para definir el JSON Schema que luego se incluye en la sección personalizada del esquema OpenAPI para la *path operation*.

Y podrías hacer esto incluso si el tipo de datos en el request no es JSON.

Por ejemplo, en esta aplicación no usamos la funcionalidad integrada de FastAPI para extraer el JSON Schema de los modelos Pydantic ni la validación automática para JSON. De hecho, estamos declarando el tipo de contenido del request como YAML, no JSON:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[15:20, 22] *}

Sin embargo, aunque no estamos usando la funcionalidad integrada por defecto, aún estamos usando un modelo Pydantic para generar manualmente el JSON Schema para los datos que queremos recibir en YAML.

Luego usamos el request directamente, y extraemos el cuerpo como `bytes`. Esto significa que FastAPI ni siquiera intentará parsear la carga útil del request como JSON.

Y luego en nuestro código, parseamos ese contenido YAML directamente, y nuevamente estamos usando el mismo modelo Pydantic para validar el contenido YAML:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[24:31] *}

/// tip | Consejo

Aquí reutilizamos el mismo modelo Pydantic.

Pero de la misma manera, podríamos haberlo validado de alguna otra forma.

///
