# Retornos Adicionais no OpenAPI

!!! warning
    Este é um tema bem avançado.

    Se você está começando com o **FastAPI**, provavelmente você não precisa disso.

Você pode declarar retornos adicionais, com status codes adicionais, media types, descrições, etc.

Essas respostas adicionais serão incluídas no schema do OpenAPI, e também aparecerão na documentação da API.

Porém para as respostas adicionais, você deve garantir que está retornando um `Response` como por exemplo o `JSONResponse` diretamente, junto com o status code e o conteúdo.

## Retorno Adicional com `model`

Você pode fornecer o parâmetro `responses` aos seus *decorators de path*.

Este parâmetro recebe um `dict`, as chaves são os status codes para cada retorno, como por exemplo `200`, e os valores são um outro `dict` com a informação de cada um deles.

Cada um desses `dict` de retorno pode ter uma chave `model`, contendo um modelo do Pydantic, assim como o `response_model`.

O **FastAPI** pegará este modelo, gerará o Schema JSON dele e incluirá no local correto do OpenAPI.

Por exemplo, para declarar um outro retorno com o status code `404` e um modelo do Pydantic chamado `Message`, você pode escrever:

```Python hl_lines="18  22"
{!../../../docs_src/additional_responses/tutorial001.py!}
```

!!! note
    Lembre-se que você deve retornar o `JSONResponse` diretamente.

!!! info
    A chave `model` não é parte do OpenAPI.

    O **FastAPI** pegará o modelo do Pydantic, gerará o `JSON Schema`, e adicionará no logcal correto.

    O local correto é:

    * Na chave `content`, que tem como valor um outro objeto JSON (`dict`) que contém:
        * Uma chave com o media type, como por exemplo `application/json`, que contém como valor um outro objeto JSON, contendo::
            * Uma chave `schema`, que contém como valor o JSON Schema do modelo, from the model, sendo este o local correto.
                * O **FastAPI** adiciona aqui a referência dos JSON Schemas globais que estão localizados em outro lugar, no lugar de incluí-lo diretamente. Deste modo, outras aplicações e clientes podem utilizar estes JSON Schemas diretamente, fornecer melhores ferramentas de geração de código, etc.

O retorno gerado no OpenAI para este *path operation* será:

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

Os schemas são referenciados em outro local dentro do schema OpenAPI:

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

## Media types adicionais para o retorno principal

Você pode utilizar o mesmo parâmetro `responses` para adicionar diferentes media types para o mesmo retorno principal.

Por exemplo, você pode adicionar um media type adicional de `image/png`, declarando que o seu *path operation* pode retornar um objeto JSON (com o media type `application/json`) ou uma imagem PNG:

```Python hl_lines="19-24  28"
{!../../../docs_src/additional_responses/tutorial002.py!}
```

!!! note
    Note que você deve retornar a imagem utilizando um `FileResponse` diretamente.

!!! info
    Unless you specify a different media type explicitly in your `responses` parameter, FastAPI will assume the response has the same media type as the main response class (default `application/json`).

    But if you have specified a custom response class with `None` as its media type, FastAPI will use `application/json` for any additional response that has an associated model.

## Combining information

You can also combine response information from multiple places, including the `response_model`, `status_code`, and `responses` parameters.

You can declare a `response_model`, using the default status code `200` (or a custom one if you need), and then declare additional information for that same response in `responses`, directly in the OpenAPI schema.

**FastAPI** will keep the additional information from `responses`, and combine it with the JSON Schema from your model.

For example, you can declare a response with a status code `404` that uses a Pydantic model and has a custom `description`.

And a response with a status code `200` that uses your `response_model`, but includes a custom `example`:

```Python hl_lines="20-31"
{!../../../docs_src/additional_responses/tutorial003.py!}
```

It will all be combined and included in your OpenAPI, and shown in the API docs:

<img src="/img/tutorial/additional-responses/image01.png">

## Combine predefined responses and custom ones

You might want to have some predefined responses that apply to many *path operations*, but you want to combine them with custom responses needed by each *path operation*.

For those cases, you can use the Python technique of "unpacking" a `dict` with `**dict_to_unpack`:

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

Here, `new_dict` will contain all the key-value pairs from `old_dict` plus the new key-value pair:

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

You can use that technique to reuse some predefined responses in your *path operations* and combine them with additional custom ones.

For example:

```Python hl_lines="13-17  26"
{!../../../docs_src/additional_responses/tutorial004.py!}
```

## More information about OpenAPI responses

To see what exactly you can include in the responses, you can check these sections in the OpenAPI specification:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responsesObject" class="external-link" target="_blank">OpenAPI Responses Object</a>, it includes the `Response Object`.
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responseObject" class="external-link" target="_blank">OpenAPI Response Object</a>, you can include anything from this directly in each response inside your `responses` parameter. Including `description`, `headers`, `content` (inside of this is that you declare different media types and JSON Schemas), and `links`.
