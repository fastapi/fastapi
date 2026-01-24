# Розширена конфігурація операцій шляху { #path-operation-advanced-configuration }

## OpenAPI operationId { #openapi-operationid }

/// warning | Попередження

Якщо ви не є «експертом» з OpenAPI, імовірно, вам це не потрібно.

///

Ви можете встановити OpenAPI `operationId`, який буде використано у вашій *операції шляху*, за допомогою параметра `operation_id`.

Потрібно переконатися, що він унікальний для кожної операції.

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py39.py hl[6] *}

### Використання назви *функції операції шляху* як operationId { #using-the-path-operation-function-name-as-the-operationid }

Якщо ви хочете використовувати назви функцій вашого API як `operationId`, ви можете пройтися по всіх них і перевизначити `operation_id` кожної *операції шляху*, використовуючи `APIRoute.name`.

Це слід робити після додавання всіх ваших *операцій шляху*.

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py39.py hl[2, 12:21, 24] *}

/// tip | Порада

Якщо ви викликаєте `app.openapi()` вручну, вам слід оновити `operationId` до цього.

///

/// warning | Попередження

Якщо ви робите це, потрібно переконатися, що кожна з ваших *функцій операції шляху* має унікальне ім’я.

Навіть якщо вони розташовані в різних модулях (файлах Python).

///

## Виключення з OpenAPI { #exclude-from-openapi }

Щоб виключити *операцію шляху* зі згенерованої схеми OpenAPI (а отже, і з автоматичних систем документації), використайте параметр `include_in_schema` і встановіть його в `False`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py39.py hl[6] *}

## Розширений опис із docstring { #advanced-description-from-docstring }

Ви можете обмежити кількість рядків docstring *функції операції шляху*, які використовуються для OpenAPI.

Додавання `\f` (екранованого символу «form feed») змушує **FastAPI** обрізати вивід, що використовується для OpenAPI, у цьому місці.

Це не відображатиметься в документації, але інші інструменти (наприклад, Sphinx) зможуть використати решту.

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## Додаткові відповіді { #additional-responses }

Ви, ймовірно, бачили, як оголошувати `response_model` і `status_code` для *операції шляху*.

Це визначає метадані про основну відповідь *операції шляху*.

Ви також можете оголосити додаткові відповіді з їхніми моделями, кодами стану тощо.

У документації є цілий розділ про це, прочитайте його тут: [Додаткові відповіді в OpenAPI](additional-responses.md){.internal-link target=_blank}.

## OpenAPI Extra { #openapi-extra }

Коли ви оголошуєте *операцію шляху* у вашому застосунку, **FastAPI** автоматично генерує відповідні метадані про цю *операцію шляху* для включення в схему OpenAPI.

/// note | Технічні деталі

У специфікації OpenAPI це називається <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Operation Object</a>.

///

Він містить усю інформацію про *операцію шляху* та використовується для генерації автоматичної документації.

Він включає `tags`, `parameters`, `requestBody`, `responses` тощо.

Ця частина схеми OpenAPI, специфічна для *операції шляху*, зазвичай генерується **FastAPI** автоматично, але ви також можете її розширити.

/// tip | Порада

Це низькорівнева точка розширення.

Якщо вам потрібно лише оголосити додаткові відповіді, зручніший спосіб — через [Додаткові відповіді в OpenAPI](additional-responses.md){.internal-link target=_blank}.

///

Ви можете розширити схему OpenAPI для *операції шляху* за допомогою параметра `openapi_extra`.

### Розширення OpenAPI { #openapi-extensions }

Цей `openapi_extra` може бути корисним, наприклад, щоб оголосити [OpenAPI Extensions](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions):

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py39.py hl[6] *}

Якщо ви відкриєте автоматичну документацію API, ваше розширення з’явиться внизу конкретної *операції шляху*.

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

А якщо ви подивитеся на результуючий OpenAPI (за адресою `/openapi.json` у вашому API), ви також побачите ваше розширення як частину конкретної *операції шляху*:

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

### Власна OpenAPI-схема для *операції шляху* { #custom-openapi-path-operation-schema }

Словник у `openapi_extra` буде глибоко об’єднано з автоматично згенерованою схемою OpenAPI для *операції шляху*.

Тож ви можете додати додаткові дані до автоматично згенерованої схеми.

Наприклад, ви можете вирішити читати й перевіряти запит власним кодом, не використовуючи автоматичні можливості FastAPI з Pydantic, але все одно хотіти визначити запит у схемі OpenAPI.

Це можна зробити за допомогою `openapi_extra`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py39.py hl[19:36, 39:40] *}

У цьому прикладі ми не оголошували жодної моделі Pydantic. Фактично тіло запиту навіть не <abbr title="converted from some plain format, like bytes, into Python objects - перетворення з простого формату, наприклад bytes, у об’єкти Python">parsed</abbr> як JSON — його читають безпосередньо як `bytes`, а функція `magic_data_reader()` відповідала б за його розбір певним способом.

Попри це, ми можемо оголосити очікувану схему для тіла запиту.

### Власний тип вмісту OpenAPI { #custom-openapi-content-type }

Використовуючи цей самий підхід, ви можете застосувати модель Pydantic, щоб визначити JSON Schema, яку потім буде включено до власної секції схеми OpenAPI для *операції шляху*.

І ви можете зробити це навіть тоді, коли тип даних у запиті — не JSON.

Наприклад, у цьому застосунку ми не використовуємо інтегровану функціональність FastAPI для витягування JSON Schema з моделей Pydantic, а також автоматичну валідацію для JSON. Насправді ми оголошуємо тип вмісту запиту як YAML, а не JSON:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[15:20, 22] *}

Попри це, хоча ми не використовуємо стандартну інтегровану функціональність, ми все одно використовуємо модель Pydantic, щоб вручну згенерувати JSON Schema для даних, які ми хочемо отримати в YAML.

Далі ми використовуємо запит безпосередньо й витягаємо тіло як `bytes`. Це означає, що FastAPI навіть не намагатиметься розбирати корисне навантаження запиту як JSON.

А потім у нашому коді ми напряму розбираємо цей YAML-вміст і знову використовуємо ту саму модель Pydantic, щоб валідувати YAML-вміст:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[24:31] *}

/// tip | Порада

Тут ми повторно використовуємо ту саму модель Pydantic.

Але так само ми могли б валідувати це іншим способом.

///
