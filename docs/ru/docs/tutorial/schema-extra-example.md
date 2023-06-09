# Объявление примера запроса данных

Вы можете объявлять примеры данных, которые ваше приложение может получать.

Вот несколько способов, как это можно сделать.

## Pydantic `schema_extra`

Вы можете объявить ключ `example` для модели Pydantic, используя класс `Config` и переменную `schema_extra`, как описано в <a href="https://pydantic-docs.helpmanual.io/usage/schema/#schema-customization" class="external-link" target="_blank">Pydantic документации: Настройка схемы</a>:

=== "Python 3.10+"

    ```Python hl_lines="13-21"
    {!> ../../../docs_src/schema_extra_example/tutorial001_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="15-23"
    {!> ../../../docs_src/schema_extra_example/tutorial001.py!}
    ```

Эта дополнительная информация будет включена в **JSON Schema** выходных данных для этой модели, и она будет использоваться в документации к API.

!!! tip Подсказка
    Вы можете использовать тот же метод для расширения JSON-схемы и добавления своей собственной дополнительной информации.

    Например, вы можете использовать это для добавления дополнительной информации для пользовательского интерфейса в вашем веб-приложении и т.д.

## Дополнительные аргументы поля `Field`

При использовании `Field()` с моделями Pydantic, вы также можете объявлять дополнительную информацию для **JSON Schema**, передавая любые другие произвольные аргументы в функцию.

Вы можете использовать это, чтобы добавить аргумент `example` для каждого поля:

=== "Python 3.10+"

    ```Python hl_lines="2  8-11"
    {!> ../../../docs_src/schema_extra_example/tutorial002_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="4  10-13"
    {!> ../../../docs_src/schema_extra_example/tutorial002.py!}
    ```

!!! warning Внимание
    Имейте в виду, что эти дополнительные переданные аргументы не добавляют никакой валидации, только дополнительную информацию для документации.

## Использование `example` и `examples` в OpenAPI

При использовании любой из этих функций:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

вы также можете добавить аргумент, содержащий `example` или группу `examples` с дополнительной информацией, которая будет добавлена в **OpenAPI**.

### Параметр `Body` с аргументом `example`

Здесь мы передаём аргумент `example`, как пример данных ожидаемых в параметре `Body()`:

=== "Python 3.10+"

    ```Python hl_lines="22-27"
    {!> ../../../docs_src/schema_extra_example/tutorial003_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="22-27"
    {!> ../../../docs_src/schema_extra_example/tutorial003_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="23-28"
    {!> ../../../docs_src/schema_extra_example/tutorial003_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip Заметка
        Рекомендуется использовать версию с `Annotated`, если это возможно.

    ```Python hl_lines="18-23"
    {!> ../../../docs_src/schema_extra_example/tutorial003_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip Заметка
        Рекомендуется использовать версию с `Annotated`, если это возможно.

    ```Python hl_lines="20-25"
    {!> ../../../docs_src/schema_extra_example/tutorial003.py!}
    ```

### Аргумент "example" в UI документации

С любым из вышеуказанных методов это будет выглядеть так в `/docs`:

<img src="/img/tutorial/body-fields/image01.png">

### `Body` с аргументом `examples`

В качестве альтернативы одному аргументу `example`, вы можете передавать `examples` используя тип данных `dict` с **несколькими примерами**, каждый из которых содержит дополнительную информацию, которая также будет добавлена в **OpenAPI**.

Ключи `dict` указывают на каждый пример, а значения для каждого из них - на еще один тип `dict` с дополнительной информацией.

Каждый конкретный пример типа `dict` в аргументе `examples` может содержать:

* `summary`: Краткое описание для примера.
* `description`: Полное описание, которое может содержать текст в формате Markdown.
* `value`: Это конкретный пример, который отображается, например, в виде типа `dict`.
* `externalValue`: альтернатива параметру `value`, URL-адрес, указывающий на пример. Хотя это может не поддерживаться таким же количеством инструментов разработки и тестирования API, как параметр `value`.

=== "Python 3.10+"

    ```Python hl_lines="23-49"
    {!> ../../../docs_src/schema_extra_example/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="23-49"
    {!> ../../../docs_src/schema_extra_example/tutorial004_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="24-50"
    {!> ../../../docs_src/schema_extra_example/tutorial004_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip Заметка
        Рекомендуется использовать версию с `Annotated`, если это возможно.

    ```Python hl_lines="19-45"
    {!> ../../../docs_src/schema_extra_example/tutorial004_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip Заметка
        Рекомендуется использовать версию с `Annotated`, если это возможно.

    ```Python hl_lines="21-47"
    {!> ../../../docs_src/schema_extra_example/tutorial004.py!}
    ```

### Аргумент "examples" в UI документации

С аргументом `examples`, добавленным в `Body()`, страница документации `/docs` будет выглядеть так:

<img src="/img/tutorial/body-fields/image02.png">

## Технические Детали

!!! warning Внимание
    Эти технические детали относятся к стандартам  **JSON Schema** и **OpenAPI**.

    Если предложенные выше идеи уже работают для вас, возможно этого будет достаточно и эти детали вам не потребуются, можете спокойно их пропустить.

Когда вы добавляете пример внутрь модели Pydantic, используя `schema_extra` или `Field(example="something")`, этот пример добавляется в **JSON Schema** для данной модели Pydantic.

И эта **JSON Schema** модели Pydantic включается в **OpenAPI** вашего API, а затем используется в UI документации.

Поля `example` как такового не существует в стандартах **JSON Schema**. В последних версиях JSON-схемы определено поле <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a>, но OpenAPI 3.0.3 основан на более старой версии JSON-схемы, которая не имела поля `examples`.

Таким образом, OpenAPI 3.0.3 определяет своё собственное поле <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#fixed-fields-20" class="external-link" target="_blank">`example`</a> для модифицированной версии **JSON Schema**, которую он использует чтобы достичь той же цели (однако это именно поле `example`, а не `examples`), и именно это используется API в UI документации (с интеграцией Swagger UI).

Итак, хотя поле `example` не является частью JSON-схемы, оно является частью настраиваемой версии JSON-схемы в OpenAPI, и именно это поле будет использоваться в UI документации.

Однако, когда вы используете  поле `example` или `examples` с любой другой функцией (`Query()`, `Body()`, и т.д.), эти примеры не добавляются в JSON-схему, которая описывает эти данные (даже в собственную версию JSON-схемы OpenAPI), они добавляются непосредственно в объявление *операции пути* в OpenAPI (вне частей OpenAPI, которые используют JSON-схему).

Для функций `Path()`, `Query()`, `Header()`, и `Cookie()`, аргументы `example` или `examples` добавляются в <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#parameter-object" class="external-link" target="_blank">определение OpenAPI, к объекту `Parameter Object` (в спецификации)</a>.

И для функций `Body()`, `File()` и `Form()` аргументы `example` или `examples` аналогично добавляются в <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#mediaTypeObject" class="external-link" target="_blank"> определение OpenAPI, к объекту `Request Body Object`, в поле `content` в объекте `Media Type Object` (в спецификации)</a>.

С другой стороны, существует более новая версия OpenAPI: **3.1.0**, недавно выпущенная. Она основана на последней версии JSON-схемы и большинство модификаций из OpenAPI JSON-схемы удалены в обмен на новые возможности из последней версии JSON-схемы, так что все эти мелкие отличия устранены. Тем не менее, Swagger UI в настоящее время не поддерживает OpenAPI 3.1.0, поэтому пока лучше продолжать использовать вышеупомянутые методы.
