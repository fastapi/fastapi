# Respuestas Adicionales en OpenAPI

/// warning | Advertencia

Este es un tema bastante avanzado.

Si estás comenzando con **FastAPI**, puede que no lo necesites.

///

Puedes declarar respuestas adicionales, con códigos de estado adicionales, tipos de medios, descripciones, etc.

Esas respuestas adicionales se incluirán en el schema de OpenAPI, por lo que también aparecerán en la documentación de la API.

Pero para esas respuestas adicionales tienes que asegurarte de devolver un `Response` como `JSONResponse` directamente, con tu código de estado y contenido.

## Respuesta Adicional con `model`

Puedes pasar a tus *decoradores de path operation* un parámetro `responses`.

Recibe un `dict`: las claves son los códigos de estado para cada respuesta (como `200`), y los valores son otros `dict`s con la información para cada uno de ellos.

Cada uno de esos `dict`s de respuesta puede tener una clave `model`, conteniendo un modelo de Pydantic, así como `response_model`.

**FastAPI** tomará ese modelo, generará su JSON Schema y lo incluirá en el lugar correcto en OpenAPI.

Por ejemplo, para declarar otra respuesta con un código de estado `404` y un modelo Pydantic `Message`, puedes escribir:

{* ../../docs_src/additional_responses/tutorial001.py hl[18,22] *}

/// note | Nota

Ten en cuenta que debes devolver el `JSONResponse` directamente.

///

/// info | Información

La clave `model` no es parte de OpenAPI.

**FastAPI** tomará el modelo de Pydantic de allí, generará el JSON Schema y lo colocará en el lugar correcto.

El lugar correcto es:

* En la clave `content`, que tiene como valor otro objeto JSON (`dict`) que contiene:
  * Una clave con el tipo de medio, por ejemplo, `application/json`, que contiene como valor otro objeto JSON, que contiene:
    * Una clave `schema`, que tiene como valor el JSON Schema del modelo, aquí es el lugar correcto.
        * **FastAPI** agrega una referencia aquí a los JSON Schemas globales en otro lugar de tu OpenAPI en lugar de incluirlo directamente. De este modo, otras aplicaciones y clientes pueden usar esos JSON Schemas directamente, proporcionar mejores herramientas de generación de código, etc.

///

Las respuestas generadas en el OpenAPI para esta *path operation* serán:

```JSON hl_lines="3-12"
{
    "responses": {
        "404": {
            "description": "Additional Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Message"
                    }
                }
            }
        },
        "200": {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Item"
                    }
                }
            }
        },
        "422": {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        }
    }
}
```

Los schemas se referencian a otro lugar dentro del schema de OpenAPI:

```JSON hl_lines="4-16"
{
    "components": {
        "schemas": {
            "Message": {
                "title": "Message",
                "required": [
                    "message"
                ],
                "type": "object",
                "properties": {
                    "message": {
                        "title": "Message",
                        "type": "string"
                    }
                }
            },
            "Item": {
                "title": "Item",
                "required": [
                    "id",
                    "value"
                ],
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Id",
                        "type": "string"
                    },
                    "value": {
                        "title": "Value",
                        "type": "string"
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            }
        }
    }
}
```

## Tipos de medios adicionales para la respuesta principal

Puedes usar este mismo parámetro `responses` para agregar diferentes tipos de medios para la misma respuesta principal.

Por ejemplo, puedes agregar un tipo de medio adicional de `image/png`, declarando que tu *path operation* puede devolver un objeto JSON (con tipo de medio `application/json`) o una imagen PNG:

{* ../../docs_src/additional_responses/tutorial002.py hl[19:24,28] *}

/// note | Nota

Nota que debes devolver la imagen usando un `FileResponse` directamente.

///

/// info | Información

A menos que especifiques un tipo de medio diferente explícitamente en tu parámetro `responses`, FastAPI asumirá que la respuesta tiene el mismo tipo de medio que la clase de respuesta principal (por defecto `application/json`).

Pero si has especificado una clase de respuesta personalizada con `None` como su tipo de medio, FastAPI usará `application/json` para cualquier respuesta adicional que tenga un modelo asociado.

///

## Combinando información

También puedes combinar información de respuesta de múltiples lugares, incluyendo los parámetros `response_model`, `status_code`, y `responses`.

Puedes declarar un `response_model`, usando el código de estado predeterminado `200` (o uno personalizado si lo necesitas), y luego declarar información adicional para esa misma respuesta en `responses`, directamente en el schema de OpenAPI.

**FastAPI** manterá la información adicional de `responses` y la combinará con el JSON Schema de tu modelo.

Por ejemplo, puedes declarar una respuesta con un código de estado `404` que usa un modelo Pydantic y tiene una `description` personalizada.

Y una respuesta con un código de estado `200` que usa tu `response_model`, pero incluye un `example` personalizado:

{* ../../docs_src/additional_responses/tutorial003.py hl[20:31] *}

Todo se combinará e incluirá en tu OpenAPI, y se mostrará en la documentación de la API:

<img src="/img/tutorial/additional-responses/image01.png">

## Combina respuestas predefinidas y personalizadas

Es posible que desees tener algunas respuestas predefinidas que se apliquen a muchas *path operations*, pero que quieras combinarlas con respuestas personalizadas necesarias por cada *path operation*.

Para esos casos, puedes usar la técnica de Python de "desempaquetar" un `dict` con `**dict_to_unpack`:

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

Aquí, `new_dict` contendrá todos los pares clave-valor de `old_dict` más el nuevo par clave-valor:

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

Puedes usar esa técnica para reutilizar algunas respuestas predefinidas en tus *path operations* y combinarlas con otras personalizadas adicionales.

Por ejemplo:

{* ../../docs_src/additional_responses/tutorial004.py hl[13:17,26] *}

## Más información sobre respuestas OpenAPI

Para ver exactamente qué puedes incluir en las respuestas, puedes revisar estas secciones en la especificación OpenAPI:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object" class="external-link" target="_blank">Objeto de Respuestas de OpenAPI</a>, incluye el `Response Object`.
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object" class="external-link" target="_blank">Objeto de Respuesta de OpenAPI</a>, puedes incluir cualquier cosa de esto directamente en cada respuesta dentro de tu parámetro `responses`. Incluyendo `description`, `headers`, `content` (dentro de este es que declaras diferentes tipos de medios y JSON Schemas), y `links`.
