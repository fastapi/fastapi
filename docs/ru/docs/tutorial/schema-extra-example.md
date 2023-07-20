# Объявление примера запроса данных

Вы можете объявлять примеры данных, которые ваше приложение может получать.

Вот несколько способов, как это можно сделать.

## Дополнительные данные JSON Schema в моделях Pydantic

Вы можете объявить ключ `examples` для модели Pydantic, которые будут добавлены в сгенерированную JSON Schema.

=== "Python 3.10+ Pydantic v2"

    ```Python hl_lines="13-24"
    {!> ../../../docs_src/schema_extra_example/tutorial001_py310.py!}
    ```

=== "Python 3.10+ Pydantic v1"

    ```Python hl_lines="13-23"
    {!> ../../../docs_src/schema_extra_example/tutorial001_py310_pv1.py!}
    ```

=== "Python 3.6+ Pydantic v2"

    ```Python hl_lines="15-26"
    {!> ../../../docs_src/schema_extra_example/tutorial001.py!}
    ```

=== "Python 3.6+ Pydantic v1"

    ```Python hl_lines="15-25"
    {!> ../../../docs_src/schema_extra_example/tutorial001_pv1.py!}
    ```

Эта дополнительная информация будет включена в **JSON Schema** выходных данных для этой модели, и она будет использоваться в документации к API.

=== "Pydantic v2"

    В Pydantic версии 2 вы бы использовали атрибут `model_config`, который принимает `dict`, как описано в <a href="https://docs.pydantic.dev/latest/usage/model_config/" class="external-link" target="_blank">Документации Pydantic: Конфигурация модели</a>.
    Вы можете установить `"json_schema_extra"` с помощью `dict`, содержащего любые дополнительные данные, которые вы хотели бы отобразить в сгенерированной JSON Schema, включая `examples`.

=== "Pydantic v1"

    В Pydantic версии 1 вы бы использовали внутренний класс `Config` и `schema_extra`, как описано в <a href="https://docs.pydantic.dev/1.10/usage/schema/#schema-customization" class="external-link" target="_blank">Документации Pydantic: Настройка схемы</a>.

    Вы можете установить `schema_extra` с помощью `dict`, содержащего любые дополнительные данные, которые вы хотели бы отобразить в сгенерированной JSON Schema, включая `examples`.

!!! Подсказка
    Вы могли бы использовать ту же технику, чтобы расширить JSON Schema и добавить свою собственную пользовательскую дополнительную информацию.

    Например, вы могли бы использовать это для добавления метаданных для внешнего пользовательского интерфейса и т.д.

!!! информация
    В OpenAPI 3.1.0 (используется начиная с FastAPI 0.99.0) добавлена поддержка ключевого слова `examples`, который является частью стандарта **JSON Schema**.
    
    До этого он поддерживал ключевое слово `example` только в одном примере. Это по-прежнему поддерживается OpenAPI 3.1.0, но устарело и не является частью стандарта JSON Schema. Таким образом, вам рекомендуется перенести `example` в `examples`. 🤓
    
    Вы можете прочитать об этом больше в конце этой страницы.

## Дополнительные аргументы `Field`

При использовании `Field()` с моделями Pydantic вы также можете объявить дополнительный аргумент `examples`:

=== "Python 3.10+"

    ```Python hl_lines="2  8-11"
    {!> ../../../docs_src/schema_extra_example/tutorial002_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="4  10-13"
    {!> ../../../docs_src/schema_extra_example/tutorial002.py!}
    ```
    
## `examples` в OpenAPI

При использовании любого из:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

вы также можете объявить группу `examples` с дополнительной информацией, которая будет добавлена в **OpenAPI**.

### `Body` с использованием `examples`

Здесь мы передаем `examples`, содержащие один пример данных, ожидаемых в `Body()`:

=== "Python 3.10+"

    ```Python hl_lines="22-29"
    {!> ../../../docs_src/schema_extra_example/tutorial003_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="22-29"
    {!> ../../../docs_src/schema_extra_example/tutorial003_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="23-30"
    {!> ../../../docs_src/schema_extra_example/tutorial003_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! Подсказка
        Предпочтительно использовать версию `Annotated`, если это возможно.

    ```Python hl_lines="18-25"
    {!> ../../../docs_src/schema_extra_example/tutorial003_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! Подсказка
        Предпочтительно использовать версию `Annotated`, если это возможно.

    ```Python hl_lines="20-27"
    {!> ../../../docs_src/schema_extra_example/tutorial003.py!}
    ```

### Пример в документации UI

С любым из описанных выше методов это выглядело бы примерно так в `/docs`:

<img src="/img/tutorial/body-fields/image01.png">

### `Body` с несколькими `examples`

Конечно, вы также можете передать несколько `examples`:

=== "Python 3.10+"

    ```Python hl_lines="23-38"
    {!> ../../../docs_src/schema_extra_example/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="23-38"
    {!> ../../../docs_src/schema_extra_example/tutorial004_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="24-39"
    {!> ../../../docs_src/schema_extra_example/tutorial004_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! Подсказка
        Предпочтительно использовать версию `Annotated`, если это возможно.

    ```Python hl_lines="19-34"
    {!> ../../../docs_src/schema_extra_example/tutorial004_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! Подсказка
        Предпочтительно использовать версию `Annotated`, если это возможно.

    ```Python hl_lines="21-36"
    {!> ../../../docs_src/schema_extra_example/tutorial004.py!}
    ```

### Примеры в документации UI

С `examples`, добавленными к `Body()`, `/docs` будет выглядеть следующим образом:

<img src="/img/tutorial/body-fields/image02.png">

## Технические детали

!!! Подсказка
    Если вы уже используете **FastAPI** версии **0.99.0 или выше**, вы можете **пропустить** эти сведения.

    Они более актуальны для более старых версий, до того, как был доступен OpenAPI 3.1.0.

    Вы можете считать это кратким **уроком истории** OpenAPI и JSON Schema. 🤓

!!! Внимание
    Это очень технические подробности о стандартах **JSON Schema** и **OpenAPI**.

    Если вышеприведенные идеи уже работают для вас, этого может быть достаточно, и вам, вероятно, не нужны эти подробности, вы можете спокойно пропустить их.

До [OpenAPI 3.1.0] OpenAPI использовал более старую и модифицированную версию **JSON Schema**.

В JSON Schema не было `examples`, поэтому OpenAPI добавил свое собственное поле `example` в свою собственную модифицированную версию.

OpenAPI также добавил поля `example` и `examples` в другие части спецификации:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object" class="external-link" target="_blank">`Объект Параметра` (в спецификации)</a>, которая использовалась в FastAPI:
    * `Path()`
    * `Query()`
    * `Header()`
    * `Cookie()`
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object" class="external-link" target="_blank">`Объект Тела Запроса`, в поле `content`, в `Media Type Object` (в спецификации)</a>, которая использовалась в FastAPI:
    * `Body()`
    * `File()`
    * `Form()`

### Поле `examples` OpenAPI

Форма этого поля `examples` из OpenAPI представляет собой `dict` с **несколькими примерами**, каждый из которых содержит дополнительную информацию, которая также будет добавлена в **OpenAPI**.

Ключи `dict` идентифицируют каждый пример, и каждое значение является другим `dict`.

Каждый конкретный пример `dict` в разделе `examples` может содержать:

* `summary`: Короткое описание для примера.
* `description`: Полное описание, которое может содержать текст Markdown.
* `value`: Это показанный фактический пример, например, `dict`.
* `externalValue`: альтернатива `value` - URL-адрес, указывающий на пример. Хотя это может поддерживаться не таким количеством инструментов, как `value`.

Это относится и к другим частям спецификации OpenAPI, помимо JSON Schema.

### Поле `examples` в JSON Schema

Но затем JSON Schema добавила поле <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5 " class="external-link" target="_blank">`examples`</a> для новой версии спецификации.

И затем новый OpenAPI 3.1.0 был основан на последней версии (JSON Schema 2020-12), которая включала это новое поле `examples`.

И теперь это новое поле `examples` имеет приоритет над старым единственным (и пользовательским) полем `example`, которое теперь устарело.

Это новое поле `examples` в схеме JSON - это просто **`list`** примеров, а не dict с дополнительными метаданными, как в других местах OpenAPI (описано выше).

!!! Информация
    Даже после того, как OpenAPI 3.1.0 был выпущен с этой новой, более простой интеграцией с JSON Schema, некоторое время Swagger UI, инструмент, который предоставляет автоматическую документацию, не поддерживал OpenAPI 3.1.0 (он поддерживает начиная с версии 5.0.0 🎉).

    Из-за этого версии FastAPI, предшествующие версии 0.99.0, по-прежнему использовали версии OpenAPI ниже 3.1.0.

### Pydantic и FastAPI `examples`

Когда вы добавляете `examples` внутри модели Pydantic, используя `schema_extra` или `Field(examples=["что-то"])`, этот пример добавляется в **JSON Schema** для этой модели Pydantic.

И эта **JSON Schema** модели Pydantic включена в **OpenAPI** вашего API, а затем используется в пользовательском интерфейсе docs.

В версиях FastAPI до 0.99.0 (0.99.0 и выше используют более новый OpenAPI 3.1.0), когда вы использовали `example` или `examples` с любой из других утилит (`Query()`, `Body()` и т.д.), эти примеры не были добавлены в JSON Schema, которая описывает эти данные (даже не в собственную версию JSON Schema OpenAPI), они были добавлены непосредственно в объявление *path operation* в OpenAPI (за пределами частей OpenAPI, которые используют JSON Schema).

Но теперь, когда FastAPI 0.99.0 и выше использует OpenAPI 3.1.0, который использует JSON Schema 2020-12, и Swagger UI 5.0.0 и выше, все стало более последовательным, и примеры включены в JSON Schema.

### Резюме

Раньше я говорил, что мне не очень нравится история... и посмотрите на меня сейчас, когда я даю уроки "истории технологий". 😅

Короче говоря, **обновитесь до FastAPI 0.99.0 или выше**, и все станет намного **проще, последовательнее и интуитивно понятнее**, и вам не обязательно знать все эти исторические подробности. 😎