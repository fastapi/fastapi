# Додаткова конфігурація операцій шляху { #path-operation-advanced-configuration }

## OpenAPI operationId { #openapi-operationid }

/// warning | Попередження

Якщо ви не «експерт» з OpenAPI, імовірно, вам це не потрібно.

///

Ви можете встановити OpenAPI `operationId`, який буде використано у вашій *операції шляху*, за допомогою параметра `operation_id`.

Потрібно переконатися, що він унікальний для кожної операції.

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py310.py hl[6] *}

### Використання назви *функції операції шляху* як operationId { #using-the-path-operation-function-name-as-the-operationid }

Якщо ви хочете використовувати назви функцій ваших API як `operationId`, ви можете пройтися по всіх них і переписати `operation_id` кожної *операції шляху*, використовуючи їхній `APIRoute.name`.

Зробіть це після додавання всіх *операцій шляху*.

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py310.py hl[2, 12:21, 24] *}

/// tip | Порада

Якщо ви вручну викликаєте `app.openapi()`, оновіть значення `operationId` до цього.

///

/// warning | Попередження

Якщо ви робите це, переконайтеся, що кожна з ваших *функцій операцій шляху* має унікальну назву.

Навіть якщо вони в різних модулях (файлах Python).

///

## Виключення з OpenAPI { #exclude-from-openapi }

Щоб виключити *операцію шляху* зі згенерованої Схеми OpenAPI (а отже, і з автоматичних систем документації), використайте параметр `include_in_schema` і встановіть його в `False`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py310.py hl[6] *}

## Розширений опис із docstring { #advanced-description-from-docstring }

Ви можете обмежити кількість рядків із docstring *функції операції шляху*, що використовуються для OpenAPI.

Додавання `\f` (екранованого символу «form feed») змусить **FastAPI** обрізати вивід для OpenAPI в цій точці.

Це не з’явиться в документації, але інші інструменти (такі як Sphinx) зможуть використати решту.

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## Додаткові відповіді { #additional-responses }

Ймовірно, ви вже бачили, як оголошувати `response_model` і `status_code` для *операції шляху*.

Це визначає метадані про основну відповідь *операції шляху*.

Також можна оголосити додаткові відповіді з їхніми моделями, кодами статусу тощо.

У документації є цілий розділ про це, ви можете прочитати його тут: [Додаткові відповіді в OpenAPI](additional-responses.md){.internal-link target=_blank}.

## Додатково в OpenAPI { #openapi-extra }

Коли ви оголошуєте *операцію шляху* у своєму застосунку, **FastAPI** автоматично генерує відповідні метадані про цю *операцію шляху* для включення в Схему OpenAPI.

/// note | Технічні деталі

У специфікації OpenAPI це називається <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Об'єкт Operation</a>.

///

Він містить усю інформацію про *операцію шляху* і використовується для побудови автоматичної документації.

Він включає `tags`, `parameters`, `requestBody`, `responses` тощо.

Цю OpenAPI-схему, специфічну для *операції шляху*, зазвичай генерує **FastAPI** автоматично, але ви також можете її розширити.

/// tip | Порада

Це низькорівнева точка розширення.

Якщо вам потрібно лише оголосити додаткові відповіді, зручніше зробити це через [Додаткові відповіді в OpenAPI](additional-responses.md){.internal-link target=_blank}.

///

Ви можете розширити OpenAPI-схему для *операції шляху*, використовуючи параметр `openapi_extra`.

### Розширення OpenAPI { #openapi-extensions }

`openapi_extra` може бути корисним, наприклад, для оголошення [OpenAPI Extensions](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions):

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py310.py hl[6] *}

Якщо ви відкриєте автоматичну документацію API, ваше розширення з’явиться внизу конкретної *операції шляху*.

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

І якщо ви відкриєте згенерований OpenAPI (за адресою `/openapi.json` у вашому API), ви також побачите своє розширення як частину конкретної *операції шляху*:

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

### Власна схема OpenAPI для *операції шляху* { #custom-openapi-path-operation-schema }

Словник у `openapi_extra` буде глибоко об’єднано з автоматично згенерованою OpenAPI-схемою для *операції шляху*.

Тож ви можете додати додаткові дані до автоматично згенерованої схеми.

Наприклад, ви можете вирішити читати та перевіряти запит власним кодом, не використовуючи автоматичні можливості FastAPI з Pydantic, але все ж захотіти визначити запит у Схемі OpenAPI.

Ви можете зробити це за допомогою `openapi_extra`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py310.py hl[19:36, 39:40] *}

У цьому прикладі ми не оголошували жодної моделі Pydantic. Насправді тіло запиту навіть не <dfn title="перетворено з простого формату, як-от bytes, у об'єкти Python">розібрано</dfn> як JSON, воно читається безпосередньо як `bytes`, а функція `magic_data_reader()` відповідатиме за його розбір певним чином.

Водночас ми можемо оголосити очікувану схему для тіла запиту.

### Власний тип вмісту OpenAPI { #custom-openapi-content-type }

Використовуючи той самий прийом, ви можете застосувати модель Pydantic, щоб визначити Схему JSON, яка потім включається в користувацький розділ OpenAPI-схеми для *операції шляху*.

І ви можете зробити це, навіть якщо тип даних у запиті - не JSON.

Наприклад, у цьому застосунку ми не використовуємо вбудовану функціональність FastAPI для отримання Схеми JSON з моделей Pydantic і не використовуємо автоматичну валідацію для JSON. Насправді ми оголошуємо тип вмісту запиту як YAML, а не JSON:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[15:20, 22] *}

Попри те, що ми не використовуємо типову вбудовану функціональність, ми все одно використовуємо модель Pydantic, щоб вручну згенерувати Схему JSON для даних, які хочемо отримати у форматі YAML.

Потім ми працюємо із запитом безпосередньо і отримуємо тіло як `bytes`. Це означає, що FastAPI навіть не намагатиметься розібрати корисне навантаження запиту як JSON.

Далі у нашому коді ми безпосередньо розбираємо цей YAML-вміст і знову використовуємо ту саму модель Pydantic, щоб перевірити YAML-вміст:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[24:31] *}

/// tip | Порада

Тут ми перевикористовуємо ту саму модель Pydantic.

Але так само ми могли б перевіряти дані іншим способом.

///
