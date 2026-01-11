# Додаткові відповіді в OpenAPI { #additional-responses-in-openapi }

/// warning | Попередження

Це доволі просунута тема.

Якщо ви тільки починаєте з **FastAPI**, вам це може бути не потрібно.

///

Ви можете оголошувати додаткові відповіді з додатковими кодами статусу, media types, описами тощо.

Ці додаткові відповіді буде включено до схеми OpenAPI, тож вони також з’являться в документації API.

Але для цих додаткових відповідей вам потрібно переконатися, що ви повертаєте `Response`, як-от `JSONResponse`, безпосередньо, із вашим кодом статусу та вмістом.

## Додаткова відповідь із `model` { #additional-response-with-model }

Ви можете передати в *декоратори операції шляху* параметр `responses`.

Він приймає `dict`: ключі — це коди статусу для кожної відповіді (наприклад, `200`), а значення — інші `dict` з інформацією для кожної з них.

Кожен із цих `dict` відповіді може мати ключ `model`, що містить Pydantic model, так само як `response_model`.

**FastAPI** візьме цю модель, згенерує її JSON Schema та включить у правильне місце в OpenAPI.

Наприклад, щоб оголосити ще одну відповідь із кодом статусу `404` і Pydantic model `Message`, ви можете написати:

{* ../../docs_src/additional_responses/tutorial001_py39.py hl[18,22] *}

/// note | Примітка

Пам’ятайте, що потрібно повертати `JSONResponse` безпосередньо.

///

/// info | Інформація

Ключ `model` не є частиною OpenAPI.

**FastAPI** візьме Pydantic model звідти, згенерує JSON Schema і помістить його в правильне місце.

Правильне місце:

* У ключі `content`, значенням якого є інший JSON-об’єкт (`dict`), що містить:
    * Ключ із media type, наприклад `application/json`, значенням якого є інший JSON-об’єкт, що містить:
        * Ключ `schema`, значенням якого є JSON Schema з моделі — ось правильне місце.
            * **FastAPI** додає тут посилання на глобальні JSON Schemas в іншому місці вашого OpenAPI, замість того щоб включати схему безпосередньо. Так інші застосунки та клієнти можуть використовувати ці JSON Schemas напряму, надавати кращі інструменти генерації коду тощо.

///

Згенеровані відповіді в OpenAPI для цієї *операції шляху* будуть:

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

Схеми мають посилання на інше місце всередині схеми OpenAPI:

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

## Додаткові media types для основної відповіді { #additional-media-types-for-the-main-response }

Ви можете використати цей самий параметр `responses`, щоб додати різні media types для тієї самої основної відповіді.

Наприклад, ви можете додати додатковий media type `image/png`, оголосивши, що ваша *операція шляху* може повертати JSON-об’єкт (із media type `application/json`) або PNG-зображення:

{* ../../docs_src/additional_responses/tutorial002_py310.py hl[17:22,26] *}

/// note | Примітка

Зверніть увагу, що потрібно повертати зображення безпосередньо через `FileResponse`.

///

/// info | Інформація

Якщо ви явно не вкажете інший media type у параметрі `responses`, FastAPI вважатиме, що відповідь має той самий media type, що й основний клас відповіді (типово `application/json`).

Але якщо ви вказали власний клас відповіді з `None` як media type, FastAPI використає `application/json` для будь-якої додаткової відповіді, що має пов’язану модель.

///

## Об’єднання інформації { #combining-information }

Ви також можете об’єднувати інформацію про відповіді з кількох місць, зокрема з параметрів `response_model`, `status_code` і `responses`.

Ви можете оголосити `response_model`, використовуючи типовий код статусу `200` (або власний, якщо потрібно), а потім оголосити додаткову інформацію для цієї ж відповіді в `responses` — безпосередньо в схемі OpenAPI.

**FastAPI** збереже додаткову інформацію з `responses` і об’єднає її з JSON Schema вашої моделі.

Наприклад, ви можете оголосити відповідь із кодом статусу `404`, яка використовує Pydantic model і має власний `description`.

А також відповідь із кодом статусу `200`, яка використовує ваш `response_model`, але містить власний `example`:

{* ../../docs_src/additional_responses/tutorial003_py39.py hl[20:31] *}

Усе це буде об’єднано й включено до вашого OpenAPI та показано в документації API:

<img src="/img/tutorial/additional-responses/image01.png">

## Поєднання попередньо визначених відповідей і власних { #combine-predefined-responses-and-custom-ones }

Можливо, ви хочете мати деякі попередньо визначені відповіді, що застосовуються до багатьох *операцій шляху*, але при цьому поєднати їх із власними відповідями, потрібними для кожної *операції шляху*.

Для таких випадків можна використати Python-техніку «розпакування» `dict` за допомогою `**dict_to_unpack`:

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

Тут `new_dict` міститиме всі пари ключ-значення з `old_dict`, плюс нову пару ключ-значення:

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

Ви можете застосувати цю техніку, щоб повторно використати деякі попередньо визначені відповіді у ваших *операціях шляху* та поєднати їх із додатковими власними.

Наприклад:

{* ../../docs_src/additional_responses/tutorial004_py310.py hl[11:15,24] *}

## Докладніше про відповіді OpenAPI { #more-information-about-openapi-responses }

Щоб побачити, що саме можна включати до відповідей, перегляньте ці розділи специфікації OpenAPI:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object" class="external-link" target="_blank">OpenAPI Responses Object</a> — містить `Response Object`.
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object" class="external-link" target="_blank">OpenAPI Response Object</a> — ви можете включити будь-що з цього безпосередньо в кожну відповідь у параметрі `responses`, зокрема `description`, `headers`, `content` (усередині нього ви оголошуєте різні media types і JSON Schemas) та `links`.
