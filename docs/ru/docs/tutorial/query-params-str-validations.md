# Query-параметры и валидация строк

**FastAPI** позволяет определять дополнительную информацию и валидацию для ваших параметров.

Давайте рассмотрим следующий пример:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial001_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial001.py!}
    ```

Query-параметр `q` имеет тип `Union[str, None]` (или `str | None` в Python 3.10). Это означает, что входной параметр будет типа `str`, но может быть и `None`. Ещё параметр имеет значение по умолчанию `None`, из-за чего FastAPI определит параметр как необязательный.

!!! note "Технические детали"
    FastAPI определит параметр `q` как необязательный, потому что его значение по умолчанию `= None`.

    `Union` в `Union[str, None]` позволит редактору кода оказать вам лучшую поддержку и найти ошибки.

## Расширенная валидация

Добавим дополнительное условие валидации параметра `q` - **длина строки не более 50 символов** (условие проверяется всякий раз, когда параметр `q` не является `None`).

### Импорт `Query` и `Annotated`

Чтобы достичь этого, первым делом нам нужно импортировать:

* `Query` из пакета `fastapi`:
* `Annotated` из пакета `typing` (или из `typing_extensions` для Python ниже 3.9)

=== "Python 3.10+"

    В Python 3.9 или выше, `Annotated` является частью стандартной библиотеки, таким образом вы можете импортировать его из `typing`.

    ```Python hl_lines="1  3"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an_py310.py!}
    ```

=== "Python 3.8+"

    В версиях Python ниже Python 3.9 `Annotation` импортируется из `typing_extensions`.

    Эта библиотека будет установлена вместе с FastAPI.

    ```Python hl_lines="3-4"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an.py!}
    ```

## `Annotated` как тип для query-параметра `q`

Помните, как ранее я говорил об Annotated? Он может быть использован для добавления метаданных для ваших параметров в разделе [Введение в аннотации типов Python](../python-types.md#type-hints-with-metadata-annotations){.internal-link target=_blank}?

Пришло время использовать их в FastAPI. 🚀

У нас была аннотация следующего типа:

=== "Python 3.10+"

    ```Python
    q: str | None = None
    ```

=== "Python 3.8+"

    ```Python
    q: Union[str, None] = None
    ```

Вот что мы получим, если обернём это в `Annotated`:

=== "Python 3.10+"

    ```Python
    q: Annotated[str | None] = None
    ```

=== "Python 3.8+"

    ```Python
    q: Annotated[Union[str, None]] = None
    ```

Обе эти версии означают одно и тоже. `q` - это параметр, который может быть `str` или `None`, и по умолчанию он будет принимать `None`.

Давайте повеселимся. 🎉

## Добавим `Query` в `Annotated` для query-параметра `q`

Теперь, когда у нас есть `Annotated`, где мы можем добавить больше метаданных, добавим `Query` со значением параметра `max_length` равным 50:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an.py!}
    ```

Обратите внимание, что значение по умолчанию всё ещё `None`, так что параметр остаётся необязательным.

Однако теперь, имея `Query(max_length=50)` внутри `Annotated`, мы говорим FastAPI, что мы хотим извлечь это значение из параметров query-запроса (что произойдёт в любом случае 🤷), и что мы хотим иметь **дополнительные условия валидации** для этого значения (для чего мы и делаем это - чтобы получить дополнительную валидацию). 😎

Теперь FastAPI:

* **Валидирует** (проверяет), что полученные данные состоят максимум из 50 символов
* Показывает **исчерпывающую ошибку** (будет описание местонахождения ошибки и её причины) для клиента в случаях, когда данные не валидны
* **Задокументирует** параметр в схему OpenAPI *операции пути* (что будет отображено в **UI автоматической документации**)

## Альтернативный (устаревший) способ задать `Query` как значение по умолчанию

В предыдущих версиях FastAPI (ниже <abbr title="ранее 2023-03">0.95.0</abbr>) необходимо было использовать `Query` как значение по умолчанию для query-параметра. Так было вместо размещения его в `Annotated`, так что велика вероятность, что вам встретится такой код. Сейчас объясню.

!!! tip "Подсказка"
    При написании нового кода и везде где это возможно, используйте `Annotated`, как было описано ранее. У этого способа есть несколько преимуществ (о них дальше) и никаких недостатков. 🍰

Вот как вы могли бы использовать `Query()` в качестве значения по умолчанию параметра вашей функции, установив для параметра `max_length` значение 50:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial002.py!}
    ```

В таком случае (без использования `Annotated`), мы заменили значение по умолчанию с `None` на `Query()` в функции. Теперь нам нужно установить значение по умолчанию для query-параметра `Query(default=None)`, что необходимо для тех же целей, как когда ранее просто указывалось значение по умолчанию (по крайней мере, для FastAPI).

Таким образом:

```Python
q: Union[str, None] = Query(default=None)
```

...делает параметр необязательным со значением по умолчанию `None`, также как это делает:

```Python
q: Union[str, None] = None
```

И для Python 3.10 и выше:

```Python
q: str | None = Query(default=None)
```

...делает параметр необязательным со значением по умолчанию `None`, также как это делает:

```Python
q: str | None = None
```

Но он явно объявляет его как query-параметр.

!!! info "Дополнительная информация"
    Запомните, важной частью объявления параметра как необязательного является:

    ```Python
    = None
    ```

    или:

    ```Python
    = Query(default=None)
    ```

    так как `None` указан в качестве значения по умолчанию, параметр будет **необязательным**.

    `Union[str, None]` позволит редактору кода оказать вам лучшую поддержку. Но это не то, на что обращает внимание FastAPI для определения необязательности параметра.

Теперь, мы можем указать больше параметров для `Query`. В данном случае, параметр `max_length` применяется к строкам:

```Python
q: Union[str, None] = Query(default=None, max_length=50)
```

Входные данные будут проверены. Если данные недействительны, тогда будет указано на ошибку в запросе (будет описание местонахождения ошибки и её причины). Кроме того, параметр задокументируется в схеме OpenAPI данной *операции пути*.

### Использовать `Query` как значение по умолчанию или добавить в `Annotated`

Когда `Query` используется внутри `Annotated`, вы не можете использовать параметр `default` у `Query`.

Вместо этого, используйте обычное указание значения по умолчанию для параметра функции. Иначе, это будет несовместимо.

Следующий пример не рабочий:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

...потому что нельзя однозначно определить, что именно должно быть значением по умолчанию: `"rick"` или `"morty"`.

Вам следует использовать (предпочтительно):

```Python
q: Annotated[str, Query()] = "rick"
```

...или как в старом коде, который вам может попасться:

```Python
q: str = Query(default="rick")
```

### Преимущества `Annotated`

**Рекомендуется использовать `Annotated`** вместо значения по умолчанию в параметрах функции, потому что так **лучше** по нескольким причинам. 🤓

Значение **по умолчанию** у **параметров функции** - это **действительно значение по умолчанию**, что более интуитивно понятно для пользователей Python. 😌

Вы можете **вызвать** ту же функцию в **иных местах** без FastAPI, и она **сработает как ожидается**. Если это **обязательный** параметр (без значения по умолчанию), ваш **редактор кода** сообщит об ошибке. **Python** также укажет на ошибку, если вы вызовете функцию без передачи ей обязательного параметра.

Если вы вместо `Annotated` используете **(устаревший) стиль значений по умолчанию**, тогда при вызове этой функции без FastAPI в **другом месте** вам необходимо **помнить** о передаче аргументов функции, чтобы она работала корректно. В противном случае, значения будут отличаться от тех, что вы ожидаете (например, `QueryInfo` или что-то подобное вместо `str`). И ни ваш редактор кода, ни Python не будут жаловаться на работу этой функции, только когда вычисления внутри дадут сбой.

Так как `Annotated` может принимать более одной аннотации метаданных, то теперь вы можете использовать ту же функцию с другими инструментами, например <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a>. 🚀

## Больше валидации

Вы также можете добавить параметр `min_length`:

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_an.py!}
    ```

=== "Python 3.10+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_py310.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003.py!}
    ```

## Регулярные выражения

Вы можете определить <abbr title="Регулярное выражение, regex или regexp - это последовательность символов, определяющая шаблон для строк.">регулярное выражение</abbr>, которому должен соответствовать параметр:

=== "Python 3.10+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="12"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an.py!}
    ```

=== "Python 3.10+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_py310.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004.py!}
    ```

Данное регулярное выражение проверяет, что полученное значение параметра:

* `^`: начало строки.
* `fixedquery`: в точности содержит строку `fixedquery`.
* `$`: конец строки, не имеет символов после `fixedquery`.

Не переживайте, если **"регулярное выражение"** вызывает у вас трудности. Это достаточно сложная тема для многих людей. Вы можете сделать множество вещей без использования регулярных выражений.

Но когда они вам понадобятся, и вы закончите их освоение, то не будет проблемой использовать их в **FastAPI**.

## Значения по умолчанию

Вы точно также можете указать любое значение `по умолчанию`, как ранее указывали `None`.

Например, вы хотите для параметра запроса `q` указать, что он должен состоять минимум из 3 символов (`min_length=3`) и иметь значение по умолчанию `"fixedquery"`:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial005_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial005_an.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial005.py!}
    ```

!!! note "Технические детали"
    Наличие значения по умолчанию делает параметр необязательным.

## Обязательный параметр

Когда вам не требуется дополнительная валидация или дополнительные метаданные для параметра запроса, вы можете сделать параметр `q` обязательным просто не указывая значения по умолчанию. Например:

```Python
q: str
```

вместо:

```Python
q: Union[str, None] = None
```

Но у нас query-параметр определён как `Query`. Например:

=== "Annotated"

    ```Python
    q: Annotated[Union[str, None], Query(min_length=3)] = None
    ```

=== "без Annotated"

    ```Python
    q: Union[str, None] = Query(default=None, min_length=3)
    ```

В таком случае, чтобы сделать query-параметр `Query` обязательным, вы можете просто не указывать значение по умолчанию:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial006_an.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006.py!}
    ```

    !!! tip "Подсказка"
        Обратите внимание, что даже когда `Query()` используется как значение по умолчанию для параметра функции, мы не передаём `default=None` в `Query()`.

        Лучше будет использовать версию с `Annotated`. 😉

### Обязательный параметр с Ellipsis (`...`)

Альтернативный способ указать обязательность параметра запроса - это указать параметр `default` через многоточие `...`:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006b_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial006b_an.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006b.py!}
    ```

!!! info "Дополнительная информация"
    Если вы ранее не сталкивались с `...`: это специальное значение, <a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">часть языка Python и называется "Ellipsis"</a>.

    Используется в Pydantic и FastAPI для определения, что значение требуется обязательно.

Таким образом, **FastAPI** определяет, что параметр является обязательным.

### Обязательный параметр с `None`

Вы можете определить, что параметр может принимать `None`, но всё ещё является обязательным. Это может потребоваться для того, чтобы пользователи явно указали параметр, даже если его значение будет `None`.

Чтобы этого добиться, вам нужно определить `None` как валидный тип для параметра запроса, но также указать `default=...`:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_an.py!}
    ```

=== "Python 3.10+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_py310.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c.py!}
    ```

!!! tip "Подсказка"
    Pydantic, мощь которого используется в FastAPI для валидации и сериализации, имеет специальное поведение для `Optional` или `Union[Something, None]` без значения по умолчанию. Вы можете узнать об этом больше в документации Pydantic, раздел <a href="https://pydantic-docs.helpmanual.io/usage/models/#required-optional-fields" class="external-link" target="_blank">Обязательные Опциональные поля</a>.

### Использование Pydantic's `Required` вместо Ellipsis (`...`)

Если вас смущает `...`, вы можете использовать `Required` из Pydantic:

=== "Python 3.9+"

    ```Python hl_lines="4  10"
    {!> ../../../docs_src/query_params_str_validations/tutorial006d_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="2  9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006d_an.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="2  8"
    {!> ../../../docs_src/query_params_str_validations/tutorial006d.py!}
    ```

!!! tip "Подсказка"
    Запомните, когда вам необходимо объявить query-параметр обязательным, вы можете просто не указывать параметр `default`. Таким образом, вам редко придётся использовать `...` или `Required`.

## Множество значений для query-параметра

Для query-параметра `Query` можно указать, что он принимает список значений (множество значений).

Например, query-параметр `q` может быть указан в URL несколько раз. И если вы ожидаете такой формат запроса, то можете указать это следующим образом:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_an.py!}
    ```

=== "Python 3.10+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_py310.py!}
    ```

=== "Python 3.9+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_py39.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011.py!}
    ```

Затем, получив такой URL:

```
http://localhost:8000/items/?q=foo&q=bar
```

вы бы получили несколько значений (`foo` и `bar`), которые относятся к параметру `q`, в виде Python `list` внутри вашей *функции обработки пути*, в *параметре функции* `q`.

Таким образом, ответ на этот URL будет:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

!!! tip "Подсказка"
    Чтобы объявить query-параметр типом `list`, как в примере выше, вам нужно явно использовать `Query`, иначе он будет интерпретирован как тело запроса.

Интерактивная документация API будет обновлена соответствующим образом, где будет разрешено множество значений:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### Query-параметр со множеством значений по умолчанию

Вы также можете указать тип `list` со списком значений по умолчанию на случай, если вам их не предоставят:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_an.py!}
    ```

=== "Python 3.9+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_py39.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial012.py!}
    ```

Если вы перейдёте по ссылке:

```
http://localhost:8000/items/
```

значение по умолчанию для `q` будет: `["foo", "bar"]` и ответом для вас будет:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### Использование `list`

Вы также можете использовать `list` напрямую вместо `List[str]` (или `list[str]` в Python 3.9+):

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial013_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial013_an.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial013.py!}
    ```

!!! note "Технические детали"
    Запомните, что в таком случае, FastAPI не будет проверять содержимое списка.

    Например, для List[int] список будет провалидирован (и задокументирован) на содержание только целочисленных элементов. Но для простого `list` такой проверки не будет.

## Больше метаданных

Вы можете добавить больше информации об query-параметре.

Указанная информация будет включена в генерируемую OpenAPI документацию и использована в пользовательском интерфейсе и внешних инструментах.

!!! note "Технические детали"
    Имейте в виду, что разные инструменты могут иметь разные уровни поддержки OpenAPI.

    Некоторые из них могут не отображать (на данный момент) всю заявленную дополнительную информацию, хотя в большинстве случаев отсутствующая функция уже запланирована к разработке.

Вы можете указать название query-параметра, используя параметр `title`:

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_an.py!}
    ```

=== "Python 3.10+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_py310.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007.py!}
    ```

Добавить описание, используя параметр `description`:

=== "Python 3.10+"

    ```Python hl_lines="14"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="14"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="15"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_an.py!}
    ```

=== "Python 3.10+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_py310.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="13"
    {!> ../../../docs_src/query_params_str_validations/tutorial008.py!}
    ```

## Псевдонимы параметров

Представьте, что вы хотите использовать query-параметр с названием `item-query`.

Например:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

Но `item-query` является невалидным именем переменной в Python.

Наиболее похожее валидное имя `item_query`.

Но вам всё равно необходим `item-query`...

Тогда вы можете объявить `псевдоним`, и этот псевдоним будет использоваться для поиска значения параметра запроса:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_an.py!}
    ```

=== "Python 3.10+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_py310.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009.py!}
    ```

## Устаревшие параметры

Предположим, вы больше не хотите использовать какой-либо параметр.

Вы решили оставить его, потому что клиенты всё ещё им пользуются. Но вы хотите отобразить это в документации как <abbr title="устарело, не рекомендуется использовать">устаревший функционал</abbr>.

Тогда для `Query` укажите параметр `deprecated=True`:

=== "Python 3.10+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="20"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_an.py!}
    ```

=== "Python 3.10+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="16"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_py310.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="18"
    {!> ../../../docs_src/query_params_str_validations/tutorial010.py!}
    ```

В документации это будет отображено следующим образом:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## Исключить из OpenAPI

Чтобы исключить query-параметр из генерируемой OpenAPI схемы (а также из системы автоматической генерации документации), укажите в `Query` параметр `include_in_schema=False`:

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_an.py!}
    ```

=== "Python 3.10+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_py310.py!}
    ```

=== "Python 3.8+ без Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать версию с `Annotated` если возможно.

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014.py!}
    ```

## Резюме

Вы можете объявлять дополнительные правила валидации и метаданные для ваших параметров запроса.

Общие метаданные:

* `alias`
* `title`
* `description`
* `deprecated`
* `include_in_schema`

Специфичные правила валидации для строк:

* `min_length`
* `max_length`
* `regex`

В рассмотренных примерах показано объявление правил валидации для строковых значений `str`.

В следующих главах вы увидете, как объявлять правила валидации для других типов (например, чисел).
