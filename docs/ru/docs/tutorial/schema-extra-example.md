# Объявление примеров данных запроса { #declare-request-example-data }

Вы можете объявлять примеры данных, которые ваше приложение может получать.

Вот несколько способов, как это сделать.

## Дополнительные данные JSON Schema в моделях Pydantic { #extra-json-schema-data-in-pydantic-models }

Вы можете объявить `examples` для модели Pydantic, которые будут добавлены в сгенерированную JSON Schema.

//// tab | Pydantic v2

{* ../../docs_src/schema_extra_example/tutorial001_py310.py hl[13:24] *}

////

//// tab | Pydantic v1

{* ../../docs_src/schema_extra_example/tutorial001_pv1_py310.py hl[13:23] *}

////

Эта дополнительная информация будет добавлена как есть в выходную **JSON Schema** этой модели и будет использоваться в документации API.

//// tab | Pydantic v2

В Pydantic версии 2 вы будете использовать атрибут `model_config`, который принимает `dict`, как описано в <a href="https://docs.pydantic.dev/latest/api/config/" class="external-link" target="_blank">Документации Pydantic: Конфигурация</a>.

Вы можете задать `"json_schema_extra"` с `dict`, содержащим любые дополнительные данные, которые вы хотите видеть в сгенерированной JSON Schema, включая `examples`.

////

//// tab | Pydantic v1

В Pydantic версии 1 вы будете использовать внутренний класс `Config` и `schema_extra`, как описано в <a href="https://docs.pydantic.dev/1.10/usage/schema/#schema-customization" class="external-link" target="_blank">Документации Pydantic: Настройка схемы</a>.

Вы можете задать `schema_extra` со `dict`, содержащим любые дополнительные данные, которые вы хотите видеть в сгенерированной JSON Schema, включая `examples`.

////

/// tip | Подсказка

Вы можете использовать тот же приём, чтобы расширить JSON Schema и добавить свою собственную дополнительную информацию.

Например, вы можете использовать это, чтобы добавить метаданные для фронтенд‑пользовательского интерфейса и т.д.

///

/// info | Информация

OpenAPI 3.1.0 (используется начиная с FastAPI 0.99.0) добавил поддержку `examples`, который является частью стандарта **JSON Schema**.

До этого поддерживалось только ключевое слово `example` с одним примером. Оно всё ещё поддерживается в OpenAPI 3.1.0, но помечено как устаревшее и не является частью стандарта JSON Schema. Поэтому рекомендуется мигрировать `example` на `examples`. 🤓

Подробнее — в конце этой страницы.

///

## Дополнительные аргументы `Field` { #field-additional-arguments }

При использовании `Field()` с моделями Pydantic вы также можете объявлять дополнительные `examples`:

{* ../../docs_src/schema_extra_example/tutorial002_py310.py hl[2,8:11] *}

## `examples` в JSON Schema — OpenAPI { #examples-in-json-schema-openapi }

При использовании любой из функций:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

вы также можете объявить набор `examples` с дополнительной информацией, которая будет добавлена в их **JSON Schema** внутри **OpenAPI**.

### `Body` с `examples` { #body-with-examples }

Здесь мы передаём `examples`, содержащий один пример данных, ожидаемых в `Body()`:

{* ../../docs_src/schema_extra_example/tutorial003_an_py310.py hl[22:29] *}

### Пример в UI документации { #example-in-the-docs-ui }

С любым из перечисленных выше методов это будет выглядеть так в `/docs`:

<img src="/img/tutorial/body-fields/image01.png">

### `Body` с несколькими `examples` { #body-with-multiple-examples }

Конечно, вы можете передать и несколько `examples`:

{* ../../docs_src/schema_extra_example/tutorial004_an_py310.py hl[23:38] *}

Когда вы делаете это, примеры становятся частью внутренней **JSON Schema** для данных тела запроса.

Тем не менее, на <abbr title="2023-08-26">момент написания этого</abbr> Swagger UI, инструмент, отвечающий за отображение UI документации, не поддерживает показ нескольких примеров для данных в **JSON Schema**. Но ниже есть обходной путь.

### Специфические для OpenAPI `examples` { #openapi-specific-examples }

Ещё до того как **JSON Schema** поддержала `examples`, в OpenAPI была поддержка другого поля, также называемого `examples`.

Эти **специфические для OpenAPI** `examples` находятся в другой секции спецификации OpenAPI. Они находятся в **подробностях для каждой операции пути (обработчика пути)**, а не внутри каждого объекта Schema.

И Swagger UI уже какое‑то время поддерживает именно это поле `examples`. Поэтому вы можете использовать его, чтобы **отобразить** разные **примеры в UI документации**.

Структура этого специфичного для OpenAPI поля `examples` — это `dict` с **несколькими примерами** (вместо `list`), каждый с дополнительной информацией, которая также будет добавлена в **OpenAPI**.

Это не помещается внутрь каждого объекта Schema в OpenAPI, это находится снаружи, непосредственно на уровне самой *операции пути*.

### Использование параметра `openapi_examples` { #using-the-openapi-examples-parameter }

Вы можете объявлять специфические для OpenAPI `examples` в FastAPI с помощью параметра `openapi_examples` для:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

Ключи `dict` идентифицируют каждый пример, а каждое значение — это ещё один `dict`.

Каждый конкретный пример‑`dict` в `examples` может содержать:

* `summary`: Краткое описание примера.
* `description`: Подробное описание, которое может содержать текст в Markdown.
* `value`: Это фактический пример, который отображается, например, `dict`.
* `externalValue`: альтернатива `value`, URL, указывающий на пример. Хотя это может поддерживаться не так многими инструментами, как `value`.

Использовать это можно так:

{* ../../docs_src/schema_extra_example/tutorial005_an_py310.py hl[23:49] *}

### OpenAPI-примеры  в UI документации { #openapi-examples-in-the-docs-ui }

С `openapi_examples`, добавленным в `Body()`, страница `/docs` будет выглядеть так:

<img src="/img/tutorial/body-fields/image02.png">

## Технические детали { #technical-details }

/// tip | Подсказка

Если вы уже используете **FastAPI** версии **0.99.0 или выше**, вы, вероятно, можете **пропустить** эти подробности.

Они более актуальны для старых версий, до того как стала доступна OpenAPI 3.1.0.

Считайте это кратким **уроком истории** про OpenAPI и JSON Schema. 🤓

///

/// warning | Внимание

Далее идут очень технические подробности о стандартах **JSON Schema** и **OpenAPI**.

Если идеи выше уже работают для вас, этого может быть достаточно, и, вероятно, вам не нужны эти детали — смело пропускайте их.

///

До OpenAPI 3.1.0 OpenAPI использовала более старую и модифицированную версию **JSON Schema**.

В JSON Schema не было `examples`, поэтому OpenAPI добавила собственное поле `example` в свою модифицированную версию.

OpenAPI также добавила поля `example` и `examples` в другие части спецификации:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object" class="external-link" target="_blank">`Parameter Object` (в спецификации)</a>, которое использовалось в FastAPI:
    * `Path()`
    * `Query()`
    * `Header()`
    * `Cookie()`
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object" class="external-link" target="_blank">`Request Body Object`, в поле `content`, в `Media Type Object` (в спецификации)</a>, которое использовалось в FastAPI:
    * `Body()`
    * `File()`
    * `Form()`

/// info | Информация

Этот старый специфичный для OpenAPI параметр `examples` теперь называется `openapi_examples`, начиная с FastAPI `0.103.0`.

///

### Поле `examples` в JSON Schema { #json-schemas-examples-field }

Позже в новой версии спецификации JSON Schema было добавлено поле <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a>.

А затем новый OpenAPI 3.1.0 был основан на последней версии (JSON Schema 2020-12), которая включала это новое поле `examples`.

И теперь это новое поле `examples` имеет приоритет над старым одиночным (и кастомным) полем `example`, которое теперь устарело.

Это новое поле `examples` в JSON Schema — это **просто `list`** примеров, а не dict с дополнительными метаданными, как в других местах OpenAPI (описанных выше).

/// info | Информация

Даже после того как OpenAPI 3.1.0 была выпущена с этой новой, более простой интеграцией с JSON Schema, какое‑то время Swagger UI, инструмент, предоставляющий автоматическую документацию, не поддерживал OpenAPI 3.1.0 (поддержка появилась начиная с версии 5.0.0 🎉).

Из‑за этого версии FastAPI до 0.99.0 всё ещё использовали версии OpenAPI ниже 3.1.0.

///

### `examples` в Pydantic и FastAPI { #pydantic-and-fastapi-examples }

Когда вы добавляете `examples` внутри модели Pydantic, используя `schema_extra` или `Field(examples=["something"])`, этот пример добавляется в **JSON Schema** для этой модели Pydantic.

И эта **JSON Schema** модели Pydantic включается в **OpenAPI** вашего API, а затем используется в UI документации.

В версиях FastAPI до 0.99.0 (0.99.0 и выше используют новый OpenAPI 3.1.0), когда вы использовали `example` или `examples` с любыми другими утилитами (`Query()`, `Body()`, и т.д.), эти примеры не добавлялись в JSON Schema, описывающую эти данные (даже в собственную версию JSON Schema OpenAPI), они добавлялись непосредственно в объявление *операции пути* в OpenAPI (вне частей OpenAPI, использующих JSON Schema).

Но теперь, когда FastAPI 0.99.0 и выше используют OpenAPI 3.1.0, который использует JSON Schema 2020-12, а также Swagger UI 5.0.0 и выше, всё стало более последовательным, и примеры включаются в JSON Schema.

### Swagger UI и специфичные для OpenAPI `examples` { #swagger-ui-and-openapi-specific-examples }

Раньше, поскольку Swagger UI не поддерживал несколько примеров JSON Schema (по состоянию на 2023-08-26), у пользователей не было способа показать несколько примеров в документации.

Чтобы решить это, FastAPI `0.103.0` **добавил поддержку** объявления того же старого, **специфичного для OpenAPI**, поля `examples` с новым параметром `openapi_examples`. 🤓

### Итог { #summary }

Раньше я говорил, что не очень люблю историю... а теперь вот рассказываю «уроки технической истории». 😅

Коротко: **обновитесь до FastAPI 0.99.0 или выше** — так всё будет значительно **проще, последовательнее и интуитивнее**, и вам не придётся знать все эти исторические подробности. 😎
