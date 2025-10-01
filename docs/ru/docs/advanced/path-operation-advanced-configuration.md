# Расширенная конфигурация операций пути { #path-operation-advanced-configuration }

## OpenAPI operationId { #openapi-operationid }

/// warning | Предупреждение

Если вы не «эксперт» по OpenAPI, скорее всего, это вам не нужно.

///

Вы можете задать OpenAPI `operationId`, который будет использоваться в вашей *операции пути*, с помощью параметра `operation_id`.

Нужно убедиться, что он уникален для каждой операции.

{* ../../docs_src/path_operation_advanced_configuration/tutorial001.py hl[6] *}

### Использование имени функции-обработчика пути как operationId { #using-the-path-operation-function-name-as-the-operationid }

Если вы хотите использовать имена функций ваших API в качестве `operationId`, вы можете пройти по всем из них и переопределить `operation_id` каждой *операции пути* с помощью их `APIRoute.name`.

Делать это следует после добавления всех *операций пути*.

{* ../../docs_src/path_operation_advanced_configuration/tutorial002.py hl[2, 12:21, 24] *}

/// tip | Совет

Если вы вызываете `app.openapi()` вручную, обновите `operationId` до этого.

///

/// warning | Предупреждение

Если вы делаете это, убедитесь, что каждая из ваших *функций-обработчиков пути* имеет уникальное имя.

Даже если они находятся в разных модулях (файлах Python).

///

## Исключить из OpenAPI { #exclude-from-openapi }

Чтобы исключить *операцию пути* из генерируемой схемы OpenAPI (а значит, и из автоматической документации), используйте параметр `include_in_schema` и установите его в `False`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial003.py hl[6] *}

## Расширенное описание из docstring { #advanced-description-from-docstring }

Вы можете ограничить количество строк из docstring *функции-обработчика пути*, используемых для OpenAPI.

Добавление `\f` (экранированного символа «form feed») заставит **FastAPI** обрезать текст, используемый для OpenAPI, в этой точке.

Эта часть не попадёт в документацию, но другие инструменты (например, Sphinx) смогут использовать остальное.

{* ../../docs_src/path_operation_advanced_configuration/tutorial004.py hl[19:29] *}

## Дополнительные ответы { #additional-responses }

Вы, вероятно, уже видели, как объявлять `response_model` и `status_code` для *операции пути*.

Это определяет метаданные об основном ответе *операции пути*.

Также можно объявлять дополнительные ответы с их моделями, статус-кодами и т.д.

В документации есть целая глава об этом — [Дополнительные ответы в OpenAPI](additional-responses.md){.internal-link target=_blank}.

## Дополнительные данные OpenAPI { #openapi-extra }

Когда вы объявляете *операцию пути* в своём приложении, **FastAPI** автоматически генерирует соответствующие метаданные об этой *операции пути* для включения в схему OpenAPI.

/// note | Технические детали

В спецификации OpenAPI это называется <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Объект операции</a>.

///

Он содержит всю информацию об *операции пути* и используется для генерации автоматической документации.

Там есть `tags`, `parameters`, `requestBody`, `responses` и т.д.

Эта спецификация OpenAPI, специфичная для *операции пути*, обычно генерируется автоматически **FastAPI**, но вы также можете её расширить.

/// tip | Совет

Это низкоуровневая возможность расширения.

Если вам нужно лишь объявить дополнительные ответы, удобнее сделать это через [Дополнительные ответы в OpenAPI](additional-responses.md){.internal-link target=_blank}.

///

Вы можете расширить схему OpenAPI для *операции пути* с помощью параметра `openapi_extra`.

### Расширения OpenAPI { #openapi-extensions }

`openapi_extra` может пригодиться, например, чтобы объявить [Расширения OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions):

{* ../../docs_src/path_operation_advanced_configuration/tutorial005.py hl[6] *}

Если вы откроете автоматическую документацию API, ваше расширение появится внизу страницы конкретной *операции пути*.

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

И если вы посмотрите на итоговый OpenAPI (по адресу `/openapi.json` вашего API), вы также увидите своё расширение в составе описания соответствующей *операции пути*:

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

### Пользовательская схема OpenAPI для операции пути { #custom-openapi-path-operation-schema }

Словарь в `openapi_extra` будет объединён с автоматически сгенерированной схемой OpenAPI для *операции пути*.

Таким образом, вы можете добавить дополнительные данные к автоматически сгенерированной схеме.

Например, вы можете решить читать и валидировать запрос своим кодом, не используя автоматические возможности FastAPI и Pydantic, но при этом захотите описать запрос в схеме OpenAPI.

Это можно сделать с помощью `openapi_extra`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial006.py hl[19:36, 39:40] *}

В этом примере мы не объявляли никакую Pydantic-модель. Фактически тело запроса даже не <abbr title="преобразовано из простого формата, например байтов, в объекты Python">распарсено</abbr> как JSON, оно читается напрямую как `bytes`, а функция `magic_data_reader()` будет отвечать за его парсинг каким-то способом.

Тем не менее, мы можем объявить ожидаемую схему для тела запроса.

### Пользовательский тип содержимого в OpenAPI { #custom-openapi-content-type }

Используя тот же приём, вы можете воспользоваться Pydantic-моделью, чтобы определить JSON Schema, которая затем будет включена в пользовательский раздел схемы OpenAPI для *операции пути*.

И вы можете сделать это, даже если тип данных в запросе — не JSON.

Например, в этом приложении мы не используем встроенную функциональность FastAPI для извлечения JSON Schema из моделей Pydantic, равно как и автоматическую валидацию JSON. Мы объявляем тип содержимого запроса как YAML, а не JSON:

//// tab | Pydantic v2

{* ../../docs_src/path_operation_advanced_configuration/tutorial007.py hl[17:22, 24] *}

////

//// tab | Pydantic v1

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_pv1.py hl[17:22, 24] *}

////

/// info | Информация

В Pydantic версии 1 метод для получения JSON Schema модели назывался `Item.schema()`, в Pydantic версии 2 метод называется `Item.model_json_schema()`.

///

Тем не менее, хотя мы не используем встроенную функциональность по умолчанию, мы всё равно используем Pydantic-модель, чтобы вручную сгенерировать JSON Schema для данных, которые мы хотим получить в YAML.

Затем мы работаем с запросом напрямую и извлекаем тело как `bytes`. Это означает, что FastAPI даже не попытается распарсить полезную нагрузку запроса как JSON.

А затем в нашем коде мы напрямую парсим этот YAML и снова используем ту же Pydantic-модель для валидации YAML-содержимого:

//// tab | Pydantic v2

{* ../../docs_src/path_operation_advanced_configuration/tutorial007.py hl[26:33] *}

////

//// tab | Pydantic v1

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_pv1.py hl[26:33] *}

////

/// info | Информация

В Pydantic версии 1 метод для парсинга и валидации объекта назывался `Item.parse_obj()`, в Pydantic версии 2 метод называется `Item.model_validate()`.

///

/// tip | Совет

Здесь мы переиспользуем ту же Pydantic-модель.

Но аналогично мы могли бы валидировать данные и каким-то другим способом.

///
