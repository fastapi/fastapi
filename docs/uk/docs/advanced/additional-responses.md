# Додаткові відповіді в OpenAPI { #additional-responses-in-openapi }

/// warning | Попередження

Це доволі просунута тема.

Якщо ви лише починаєте з **FastAPI**, ймовірно, вам це не потрібно.

///

Ви можете оголосити додаткові відповіді з додатковими кодами статусу, типами медіа, описами тощо.

Ці додаткові відповіді буде включено до схеми OpenAPI, тож вони з'являться і в документації API.

Але для таких додаткових відповідей потрібно повертати `Response` на кшталт `JSONResponse` безпосередньо, із потрібним кодом статусу та вмістом.

## Додаткова відповідь з `model` { #additional-response-with-model }

Ви можете передати вашим декораторам операцій шляху параметр `responses`.

Він приймає `dict`: ключі - це коди статусу для кожної відповіді (наприклад, `200`), а значення - інші `dict` з інформацією для кожної з них.

Кожен із цих словників відповіді може мати ключ `model`, що містить Pydantic-модель, подібно до `response_model`.

**FastAPI** візьме цю модель, згенерує її Схему JSON і додасть у відповідне місце в OpenAPI.

Наприклад, щоб оголосити іншу відповідь з кодом статусу `404` і Pydantic-моделлю `Message`, ви можете написати:

{* ../../docs_src/additional_responses/tutorial001_py310.py hl[18,22] *}

/// note | Примітка

Майте на увазі, що потрібно повертати `JSONResponse` безпосередньо.

///

/// info | Інформація

Ключ `model` не є частиною OpenAPI.

**FastAPI** візьме звідти Pydantic-модель, згенерує Схему JSON і помістить у відповідне місце.

Відповідне місце це:

- У ключі `content`, значенням якого є інший JSON-об'єкт (`dict`), що містить:
    - Ключ із типом медіа, напр. `application/json`, значенням якого є інший JSON-об'єкт, що містить:
        - Ключ `schema`, значенням якого є Схема JSON з моделі - ось це і є правильне місце.
            - **FastAPI** додає тут посилання на глобальні Схеми JSON в іншому місці вашого OpenAPI замість прямого включення. Так інші застосунки та клієнти можуть напряму використовувати ці Схеми JSON, надавати кращі інструменти генерації коду тощо.

///

Згенеровані відповіді в OpenAPI для цієї операції шляху будуть такими:

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

Схеми посилаються на інше місце всередині схеми OpenAPI:

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

## Додаткові типи медіа для основної відповіді { #additional-media-types-for-the-main-response }

Можна використати цей самий параметр `responses`, щоб додати різні типи медіа для тієї ж основної відповіді.

Наприклад, можна додати додатковий тип медіа `image/png`, оголосивши, що ваша операція шляху може повертати JSON-об'єкт (з типом медіа `application/json`) або PNG-зображення:

{* ../../docs_src/additional_responses/tutorial002_py310.py hl[17:22,26] *}

/// note | Примітка

Зверніть увагу, що потрібно повертати зображення безпосередньо за допомогою `FileResponse`.

///

/// info | Інформація

Поки ви явно не вкажете інший тип медіа в параметрі `responses`, FastAPI вважатиме, що відповідь має той самий тип медіа, що й основний клас відповіді (типово `application/json`).

Але якщо ви вказали власний клас відповіді з `None` як типом медіа, FastAPI використає `application/json` для будь-якої додаткової відповіді, що має пов'язану модель.

///

## Комбінування інформації { #combining-information }

Ви також можете поєднувати інформацію про відповіді з кількох місць, зокрема з параметрів `response_model`, `status_code` і `responses`.

Ви можете оголосити `response_model`, використовуючи типовий код статусу `200` (або власний за потреби), а потім оголосити додаткову інформацію для цієї ж відповіді в `responses`, безпосередньо в схемі OpenAPI.

**FastAPI** збереже додаткову інформацію з `responses` і поєднає її зі Схемою JSON з вашої моделі.

Наприклад, ви можете оголосити відповідь з кодом статусу `404`, яка використовує Pydantic-модель і має власний `description`.

І відповідь з кодом статусу `200`, яка використовує ваш `response_model`, але містить власний `example`:

{* ../../docs_src/additional_responses/tutorial003_py310.py hl[20:31] *}

Усе це буде поєднано та включено до вашого OpenAPI і показано в документації API:

<img src="/img/tutorial/additional-responses/image01.png">

## Комбінуйте попередньо визначені та власні відповіді { #combine-predefined-responses-and-custom-ones }

Можливо, ви захочете мати кілька попередньо визначених відповідей, що застосовуються до багатьох операцій шляху, але поєднувати їх із власними відповідями, потрібними для кожної операції шляху.

Для таких випадків можна скористатися прийомом Python «розпакування» `dict` за допомогою `**dict_to_unpack`:

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

Тут `new_dict` міститиме всі пари ключ-значення з `old_dict` плюс нову пару ключ-значення:

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

Цей прийом можна використати, щоб перевикористовувати деякі попередньо визначені відповіді у ваших операціях шляху та поєднувати їх із додатковими власними.

Наприклад:

{* ../../docs_src/additional_responses/tutorial004_py310.py hl[11:15,24] *}

## Докладніше про відповіді OpenAPI { #more-information-about-openapi-responses }

Щоб побачити, що саме можна включати у відповіді, ознайомтеся з цими розділами специфікації OpenAPI:

- <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object" class="external-link" target="_blank">Об'єкт відповідей OpenAPI</a>, він включає `Response Object`.
- <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object" class="external-link" target="_blank">Об'єкт відповіді OpenAPI</a>, ви можете включити будь-що з цього безпосередньо в кожну відповідь у параметрі `responses`. Зокрема `description`, `headers`, `content` (усередині нього ви оголошуєте різні типи медіа та Схеми JSON) і `links`.
