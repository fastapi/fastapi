# Header-параметры

Вы можете определить параметры заголовка таким же образом, как вы определяете параметры `Query`, `Path` и `Cookie`.

## Импорт `Header`

Сперва импортируйте `Header`:

=== "Python 3.10+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/header_params/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/header_params/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/header_params/tutorial001_an.py!}
    ```

=== "Python 3.10+ без Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="1"
    {!> ../../../docs_src/header_params/tutorial001_py310.py!}
    ```

=== "Python 3.6+ без Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="3"
    {!> ../../../docs_src/header_params/tutorial001.py!}
    ```

## Объявление параметров `Header`

Затем объявите параметры заголовка, используя ту же структуру, что и с `Path`, `Query` и `Cookie`.

Первое значение является значением по умолчанию, вы можете передать все дополнительные параметры валидации или аннотации:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/header_params/tutorial001_an.py!}
    ```

=== "Python 3.10+ без Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="7"
    {!> ../../../docs_src/header_params/tutorial001_py310.py!}
    ```

=== "Python 3.6+ без Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial001.py!}
    ```

!!! note "Технические детали"
    `Header` - это "родственный" класс `Path`, `Query` и `Cookie`. Он также наследуется от того же общего класса `Param`.

    Но помните, что когда вы импортируете `Query`, `Path`, `Header` и другие из `fastapi`, на самом деле это функции, которые возвращают специальные классы.

!!! Дополнительная информация
    Чтобы объявить заголовки, вам нужно использовать `Header`, потому что в противном случае параметры были бы интерпретированы как query-параметры.

## Автоматическое преобразование

`Header` обладает небольшой дополнительной функциональностью в дополнение к тому, что предоставляют `Path`, `Query` и `Cookie`.

Большинство стандартных заголовков разделены символом "дефис", также известным как "символ минуса" (`-`).

Но переменная типа `user-agent` недопустима в Python.

По умолчанию `Header` преобразует символы имен параметров из символа подчеркивания (`_`) в дефис (`-`) для извлечения и документирования заголовков.

Кроме того, HTTP-заголовки не чувствительны к регистру, поэтому вы можете объявить их в стандартном стиле Python (также известном как "snake_case").

Итак, вы можете использовать `user_agent`, как обычно, в коде Python, вместо того, чтобы вводить заглавные буквы как `User_Agent` или что-то подобное.

Если по какой-либо причине вам необходимо отключить автоматическое преобразование подчеркиваний в дефисы, установите для параметра `convert_underscores` в `Header` значение `False':

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/header_params/tutorial002_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/header_params/tutorial002_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="12"
    {!> ../../../docs_src/header_params/tutorial002_an.py!}
    ```

=== "Python 3.10+ без Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="8"
    {!> ../../../docs_src/header_params/tutorial002_py310.py!}
    ```

=== "Python 3.6+ без Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="10"
    {!> ../../../docs_src/header_params/tutorial002.py!}
    ```

!!! Внимание
    Прежде чем установить для `convert_underscores` значение `False`, имейте в виду, что некоторые HTTP-прокси и серверы запрещают использование заголовков с подчеркиванием.

## Повторяющиеся заголовки

Есть возможность получать повторяющиеся заголовки. Это означает один и тот же заголовок с множеством значений.

Вы можете определить эти случаи, используя список в объявлении типа.

Вы получите все значения из повторяющегося заголовка в виде `list` Python.

Например, чтобы объявить заголовок `X-Token`, который может появляться более одного раза, вы можете написать:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial003_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial003_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/header_params/tutorial003_an.py!}
    ```

=== "Python 3.10+ без Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="7"
    {!> ../../../docs_src/header_params/tutorial003_py310.py!}
    ```

=== "Python 3.9+ без Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial003_py39.py!}
    ```

=== "Python 3.6+ без Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial003.py!}
    ```

Если вы взаимодействуете с этой *операцией пути*, отправляя два HTTP-заголовка, таких как:

```
X-Token: foo
X-Token: bar
```

Ответ был бы таким:

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## Резюме

Объявляйте заголовки с помощью `Header`, используя тот же общий шаблон, как при `Query`, `Path` и `Cookie`.

И не беспокойтесь о символах подчеркивания в ваших переменных, **FastAPI** позаботится об их преобразовании.
