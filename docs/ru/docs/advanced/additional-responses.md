# Дополнительные ответы в OpenAPI

/// warning | Предупреждение

Это довольно сложная тема.

Если вы только начинаете с **FastAPI**, вам это может не понадобиться.

///

Вы можете объявить дополнительные ответы с дополнительными статус-кодами, медиа-типами, описаниями и т.д.

Эти дополнительные ответы будут включены в OpenAPI схему, и они также будут отображаться в документации API.

Но для этих дополнительных ответов вы должны убедиться, что возвращаете `Response`, например `JSONResponse`, напрямую с вашим статус-кодом и содержимым.

## Дополнительный ответ с `model`

Вы можете передать вашим *декораторам операций пути* параметр `responses`.

Он принимает `dict`: ключи - это статус-коды для каждого ответа (такие как `200`), а значения - другие `dict` с информацией для каждого из них.

Каждый из этих `dict` ответов может иметь ключ `model`, содержащий Pydantic модель, так же как и `response_model`.

**FastAPI** возьмет эту модель, сгенерирует ее JSON Schema и включит в нужное место в OpenAPI.

Например, чтобы объявить другой ответ с кодом состояния `404` и Pydantic моделью `Message`, можно написать:

{* ../../docs_src/additional_responses/tutorial001.py hl[18,22] *}

/// note | Примечание

Имейте в виду, что вы должны вернуть `JSONResponse` напрямую.

///

/// info | Информация

Ключ `model` не является частью OpenAPI.

**FastAPI** возьмет Pydantic модель оттуда, сгенерирует JSON Schema и разместит ее в нужном месте.

Правильное место:

* В ключе `content`, который имеет значение другого JSON объекта (`dict`), содержащего:
    * Ключ с медиа-типом, например, `application/json`, который содержит как значение другой JSON объект, который содержит:
        * Ключ `schema`, который имеет как значение JSON Schema из модели, вот это правильное место.
            * **FastAPI** добавляет ссылку здесь на глобальные JSON Schema в другом месте вашего OpenAPI вместо того, чтобы включать её напрямую. Таким образом, другие приложения и клиенты могут использовать эти JSON Schema напрямую, предоставлять лучшие инструменты для генерации кода и т.д.

///

Сгенерированные ответы в OpenAPI для этой *операции пути* будут:

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

Схемы ссылаются на другое место внутри OpenAPI схемы:

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

## Дополнительные медиа-типы для основного ответа

Вы можете использовать тот же параметр `responses` для добавления различных медиа-типов для одного и того же основного ответа.

Например, можно добавить дополнительный медиа-тип `image/png`, объявляя, что ваша *операция пути* может возвращать JSON объект (с медиа-типом `application/json`) или PNG изображение:

{* ../../docs_src/additional_responses/tutorial002.py hl[19:24,28] *}

/// note | Примечание

Обратите внимание, что вы должны вернуть изображение, используя `FileResponse` напрямую.

///

/// info | Информация

Если вы не укажете явный медиа-тип в вашем `responses` параметре, FastAPI будет предполагать, что ответ имеет тот же медиа-тип, что и основной класс ответа (по умолчанию `application/json`).

Но если вы указали пользовательский класс ответа с `None` в качестве его медиа-типа, FastAPI будет использовать `application/json` для любого дополнительного ответа, который связан с моделью.

///

## Комбинирование информации

Вы также можете объединять информацию об ответах из нескольких мест, включая параметры `response_model`, `status_code` и `responses`.

Вы можете объявить `response_model`, используя статус-код по умолчанию `200` (или пользовательский, если вам нужно), а затем объявить дополнительную информацию для этого же ответа в `responses`, напрямую в OpenAPI схеме.

**FastAPI** сохранит дополнительную информацию из `responses` и объединит её с JSON Schema вашей модели.

Например, вы можете объявить ответ с кодом состояния `404`, который использует Pydantic модель и имеет пользовательское `description`.

И ответ с кодом состояния `200`, который использует ваш `response_model`, но включает пользовательский `example`:

{* ../../docs_src/additional_responses/tutorial003.py hl[20:31] *}

Все это будет объединено и включено в ваш OpenAPI и показано в документации API:

<img src="/img/tutorial/additional-responses/image01.png">

## Комбинирование предопределенных ответов и пользовательских

Возможно, вы захотите иметь некоторые предопределенные ответы, которые применяются к многим *операциям пути*, но вы хотите объединить их с пользовательскими ответами, необходимыми для каждой *операции пути*.

В таких случаях вы можете использовать технику Python "распаковки" `dict` с помощью `**dict_to_unpack`:

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

Здесь, `new_dict` будет содержать все пары ключ-значение из `old_dict` плюс новую пару ключ-значение:

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

Вы можете использовать эту технику для повторного использования некоторых предопределенных ответов в ваших *операциях пути* и сочетания их с дополнительными пользовательскими ответами.

Например:

{* ../../docs_src/additional_responses/tutorial004.py hl[13:17,26] *}

## Дополнительная информация об OpenAPI ответах

Чтобы узнать, что именно можно включить в ответы, вы можете проверить эти разделы в спецификации OpenAPI:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object" class="external-link" target="_blank">OpenAPI Responses Object</a>, включает в себя `Response Object`.
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object" class="external-link" target="_blank">OpenAPI Response Object</a>, вы можете включить что угодно из этого напрямую для каждого ответа в вашем параметре `responses`. Включая `description`, `headers`, `content` (внутри этого вы объявляете различные медиа-типы и JSON schemas), и `links`.
