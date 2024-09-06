# Respuestas adicionales en OpenAPI

/// warning

Este es un tema bastante avanzado.

Si apenas estas empezando con **FastAPI**, Puede que no necesites esto.

///


Tú puedes declarar respuestas adicionales, que contengan códigos de estado, tipos de medio, descripciones y varias cosas adicionales.

Ten en cuenta que estas respuestas adicionales se incluirán en el esquema OpenAPI, por lo que también aparecerán en la documentación de la API.

Pero para que esas respuestas adicionales funcionen tienes que asegurarte de que devuelves un `Response` como un objeto`JSONResponse` directamente, el cual debe incluir código de estado y contenido.

## Respuesta Adicional con un `model`

Puedes pasar un parámetro `responses` a los *path operation decorators*

Este parámetro recibe un objeto `dict`, cuyas keys son los códigos de estado para cada respuesta, por ejemplo 200, y  sus valores son otro `dict` con la información necesaria para cada una de las respuestas.

Cada uno de estos `dict`s soporta una key `model`, la cual contenga un modelo de Pydantic, de forma similar al parámetro `response_model`.

**FastAPI** utilizará ese modelo, para generar su propio JSON Schema y lo incluirá en el lugar correcto dentro de OpenAPI.

Por ejemplo, al declarar otra respuesta con un código de estado `404` y un modelo de Pydantic `Message`, lo puedes escribir de esta forma:

```Python hl_lines="18  22"
{!../../../docs_src/additional_responses/tutorial001.py!}
```

/// note

Mantén en mente debes retornar el objeto `JSONResponse` directamente.

///

/// info

La key `model no es parte de OpenAPI.

**FastAPI** lo tomará desde el modelo de Pydantic para generar el JSON Schema, y colocarlo en el lugar correcto.

El lugar correcto es:

* Dentro de la key `content`, cuyo valor es otro objeto tipo JSON (`dict`), compuesto de:
    * Una key con el tipo de medio, e.j. `application/json`, el cual contenga como valor otro objeto JSON, con la siguiente estructura:
        * Una key `schema`, cuyo valor es el esquema JSON para el modelo, este es el lugar correcto.
            *  **FastAPI** añade una referencia en este lugar hacia el esquema global JSON ubicado en otro sitio dentro de tu OpenAPI en lugar de incluirlo directamente, proveyendo una mejor herramienta de generación de código.

/// 

Las respuestas generadas en OpenAPI para este *path operation* serán:

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

Los schemas están referenciados a otro lugar dentro del esquema de Open Api.

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

## Tipos de medio adicionales para la respuesta principal

Puedes utilizar los mismos parámetros en tus `responses` para añadir diferentes tipos de medio en la misma respuesta principal.

Por ejemplo, Puedes añadir un tipo de medio adicional de `image/png`, declarando que tu *path operation* pueda retornar un objeto JSON (con el tipo de medio `application/json`) or una imagen PNG:

```Python hl_lines="19-24  28"
{!../../../docs_src/additional_responses/tutorial002.py!}
```

/// note

Nota que debes retornar la imagen usando una `FileResponse` directamente.

///


/// info

Amenos que especifiques explícitamente en tu parámetro `responses` un tipo de medio diferente, FastAPI asumirá que la respuesta tiene el mismo tipo de medio que las clase de respuesta principal (por defecto `application/json`).

Pero si as especificado una clase de respuesta personalizada with `None` como su tipo de medio, FastAPI usará `application/json` para cualquier respuesta adicional que tenga un modelo asociado.

///

## Combinando información

También puedes combinar la información de la respuesta de multiples lugares, incluyendo los parámetros `response_model`, `status_code`y `responses`.

Puedes declarar un `response_model`, utilizando el código de estado `200` por defecto (o uno personalizado si lo necesitas), y después declarar información adicional para la misma respuesta en `responses`, directamente dentro del schema de OpenAPI.

**FastAPI** mantendrá la información adicional desde `responses`, y la combinará con el esquema JSON desde tu modelo.

Por ejemplo, puedes declarar una respuesta con un código de estado `404` que use un modelo de Pydantic y tenga un descripción personalizada.

Y una respuesta con un código de estado `200` que use tu `response_model`, pero incluya un ejemplo personalizado dentro de la key `example`:

```Python hl_lines="20-31"
{!../../../docs_src/additional_responses/tutorial003.py!}
```

Todo esto sera combinado e incluido dentro de tu OpenAPI, y presentado en la documentación de la API.

<img src="/img/tutorial/additional-responses/image01.png">

## Combinar respuestas predefinidas y personalizadas

Es posible que desees tener algunas respuestas predefinidas que se apliquen a varios *path operations*, pero quieras combinarlas con respuestas personalizadas que sean necesarias para cada *path operation*.

Para estos casos, puedes usar la técnica de python de "desempaquetar" un  `dict` con `**dict_to_unpack`:

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

Aquí, `new_dict` contendrá todos los pares key-value de `old_dict` más el nuevo par key-value:

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

Puedes usar esta técnica para rehusar algunas respuestas predefinidas en tus *path operations* y combinarlas con algunas personalizadas.

Por ejemplo:

```Python hl_lines="13-17  26"
{!../../../docs_src/additional_responses/tutorial004.py!}
```

## Mas información sobre las respuestas de OpenAPI

Para mirar que exactamente puedes incluir en las respuestas, puedes chequear estas secciones dentro de la especificación de OpenAPI:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object" class="external-link" target="_blank">OpenAPI Responses Object</a>, esto incluye el `Response Object`.
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object" class="external-link" target="_blank">OpenAPI Response Object</a>, Puedes incluir cualquier cosa de esta directiva directamente en cada respuesta dentro de tu parámetro `responses`. Incluyendo `description`, `headers`, `content` (dentro de este es que declaras diferentes tipos de medio y esquemas JSON), y `links`.
