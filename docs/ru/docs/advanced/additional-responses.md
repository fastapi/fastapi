# Дополнительные ответы в OpenAPI { #additional-responses-in-openapi }

/// warning | Предупреждение

Это довольно продвинутая тема.

Если вы только начинаете работать с **FastAPI**, возможно, вам это пока не нужно.

///

Вы можете объявлять дополнительные ответы с дополнительными статус-кодами, типами содержимого, описаниями и т.д.

Эти дополнительные ответы будут включены в схему OpenAPI, и поэтому появятся в документации API.

Но для таких дополнительных ответов убедитесь, что вы возвращаете `Response`, например `JSONResponse`, напрямую, со своим статус-кодом и содержимым.

## Дополнительный ответ с `model` { #additional-response-with-model }

Вы можете передать вашим декораторам операции пути параметр `responses`.

Он принимает `dict`: ключи — это статус-коды для каждого ответа (например, `200`), а значения — другие `dict` с информацией для каждого из них.

Каждый из этих `dict` для ответа может иметь ключ `model`, содержащий Pydantic-модель, аналогично `response_model`.

**FastAPI** возьмёт эту модель, сгенерирует для неё JSON‑схему и включит её в нужное место в OpenAPI.

Например, чтобы объявить ещё один ответ со статус-кодом `404` и Pydantic-моделью `Message`, можно написать:

{* ../../docs_src/additional_responses/tutorial001.py hl[18,22] *}

/// note | Примечание

Имейте в виду, что необходимо возвращать `JSONResponse` напрямую.

///

/// info | Информация

Ключ `model` не является частью OpenAPI.

**FastAPI** возьмёт Pydantic-модель оттуда, сгенерирует JSON‑схему и поместит её в нужное место.

Нужное место:

* В ключе `content`, значением которого является другой JSON‑объект (`dict`), содержащий:
    * Ключ с типом содержимого, например `application/json`, значением которого является другой JSON‑объект, содержащий:
        * Ключ `schema`, значением которого является JSON‑схема из модели — вот нужное место.
            * **FastAPI** добавляет здесь ссылку на глобальные JSON‑схемы в другом месте вашего OpenAPI вместо того, чтобы включать схему напрямую. Так другие приложения и клиенты смогут использовать эти JSON‑схемы напрямую, предоставлять лучшие инструменты генерации кода и т.д.

///

Сгенерированные в OpenAPI ответы для этой операции пути будут такими:

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

Схемы даны как ссылки на другое место внутри схемы OpenAPI:

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

## Дополнительные типы содержимого для основного ответа { #additional-media-types-for-the-main-response }

Вы можете использовать этот же параметр `responses`, чтобы добавить разные типы содержимого для того же основного ответа.

Например, вы можете добавить дополнительный тип содержимого `image/png`, объявив, что ваша операция пути может возвращать JSON‑объект (с типом содержимого `application/json`) или PNG‑изображение:

{* ../../docs_src/additional_responses/tutorial002.py hl[19:24,28] *}

/// note | Примечание

Учтите, что изображение нужно возвращать напрямую, используя `FileResponse`.

///

/// info | Информация

Если вы явно не укажете другой тип содержимого в параметре `responses`, FastAPI будет считать, что ответ имеет тот же тип содержимого, что и основной класс ответа (по умолчанию `application/json`).

Но если вы указали пользовательский класс ответа с `None` в качестве его типа содержимого, FastAPI использует `application/json` для любого дополнительного ответа, у которого есть связанная модель.

///

## Комбинирование информации { #combining-information }

Вы также можете комбинировать информацию об ответах из нескольких мест, включая параметры `response_model`, `status_code` и `responses`.

Вы можете объявить `response_model`, используя статус-код по умолчанию `200` (или свой, если нужно), а затем объявить дополнительную информацию для этого же ответа в `responses`, напрямую в схеме OpenAPI.

**FastAPI** сохранит дополнительную информацию из `responses` и объединит её с JSON‑схемой из вашей модели.

Например, вы можете объявить ответ со статус-кодом `404`, который использует Pydantic-модель и имеет пользовательское `description`.

А также ответ со статус-кодом `200`, который использует ваш `response_model`, но включает пользовательский `example`:

{* ../../docs_src/additional_responses/tutorial003.py hl[20:31] *}

Всё это будет объединено и включено в ваш OpenAPI и отображено в документации API:

<img src="/img/tutorial/additional-responses/image01.png">

## Комбинирование предопределённых и пользовательских ответов { #combine-predefined-responses-and-custom-ones }

Возможно, вы хотите иметь некоторые предопределённые ответы, применимые ко многим операциям пути, но при этом комбинировать их с пользовательскими ответами, необходимыми для каждой конкретной операции пути.

В таких случаях вы можете использовать приём Python «распаковки» `dict` с помощью `**dict_to_unpack`:

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

Здесь `new_dict` будет содержать все пары ключ-значение из `old_dict` плюс новую пару ключ-значение:

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

Вы можете использовать этот приём, чтобы переиспользовать некоторые предопределённые ответы в ваших операциях пути и комбинировать их с дополнительными пользовательскими.

Например:

{* ../../docs_src/additional_responses/tutorial004.py hl[13:17,26] *}

## Дополнительная информация об ответах OpenAPI { #more-information-about-openapi-responses }

Чтобы увидеть, что именно можно включать в ответы, посмотрите эти разделы спецификации OpenAPI:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object" class="external-link" target="_blank">Объект Responses OpenAPI</a>, он включает `Response Object`.
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object" class="external-link" target="_blank">Объект Response OpenAPI</a>, вы можете включить всё из этого объекта напрямую в каждый ответ внутри вашего параметра `responses`. Включая `description`, `headers`, `content` (внутри него вы объявляете разные типы содержимого и JSON‑схемы) и `links`.
