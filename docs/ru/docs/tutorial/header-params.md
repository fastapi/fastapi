# Параметры Заголовка

Вы можете определять параметры Заголовка также, как вы определяете параметры `Query`, `Path` и `Cookie`.

## Import `Header`

Сначала импортируйте `Header`:

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

=== "Python 3.10+ non-Annotated"

    !!! tip "Подсказка"
        Предпочтительно использовать версию `Annotated`, если это возможно.

    ```Python hl_lines="1"
    {!> ../../../docs_src/header_params/tutorial001_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip "Подсказка"
        Предпочтительно использовать версию `Annotated`, если это возможно.

    ```Python hl_lines="3"
    {!> ../../../docs_src/header_params/tutorial001.py!}
    ```

## Объявление параметров `Header`

Затем объявите параметры заголовка, используя ту же структуру, что и в случае с `Path`, `Query` и `Cookie`.

Первое значение - это значение по умолчанию, вы можете передать все дополнительные параметры проверки или аннотации:

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

=== "Python 3.10+ non-Annotated"

    !!! tip "Подсказка"
        Предпочтительно использовать версию `Annotated`, если это возможно.

    ```Python hl_lines="7"
    {!> ../../../docs_src/header_params/tutorial001_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip "Подсказка"
        Предпочтительно использовать версию `Annotated`, если это возможно.

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial001.py!}
    ```

!!! note "Технические Детали"
    `Header` это "родственный" класс `Path`, `Query` и `Cookie`. Он также наследут тот же самый общий класс `Param`.

    Но помните, что когда вы импортируете `Query`, `Path`, `Header` и остальное из `fastapi`, на самом деле вы импортируете функции, которые возвращают специальные классы.

!!! info "Информация"
    Для объявления заголовков вам нужно использовать `Header`, потому что иначе параметры будут интерпретироваться как query-параметры.

## Автоматическое преобразование

`Header` обладает небольшой дополнительной функциональностью сверх того, что предоставляют `Path`, `Query` и `Cookie`.

Большинство стандартных заголовков разделены символом "дефис", также известным как "символ минуса" (`-`).

Но имя переменной, например как `user-agent`, недопустимо в Python.

Таким образом, по умолчанию `Header` в именах параметров преобразует символ подчеркивания (`_`) в дефис (`-`) для извлечения и документирования заголовков.

Кроме того, HTTP-заголовки не чувствительны к регистру, поэтому вы можете объявить их в стандартном стиле Python (также известном как "snake_case").

Итак, вы можете использовать `user_agent`, как обычно в коде Python, вместо того, чтобы использовать заглавные буквы как `User_Agent` или что-то подобное.

Если по какой-то причине вам необходимо отключить автоматическое преобразование нижних подчеркиваний в дефисы, установите параметр `convert_underscores` в `Header` в значение `False`:

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

=== "Python 3.10+ non-Annotated"

    !!! tip "Подсказка"
        Предпочтительно использовать версию `Annotated`, если это возможно.

    ```Python hl_lines="8"
    {!> ../../../docs_src/header_params/tutorial002_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip "Подсказка"
        Предпочтительно использовать версию `Annotated`, если это возможно.

    ```Python hl_lines="10"
    {!> ../../../docs_src/header_params/tutorial002.py!}
    ```

!!! warning "Внимание"
    Прежде чем установить `convert_underscores` в значение `False`, имейте в виду, что некоторые HTTP-прокси и серверы запрещают использование заголовков с подчеркиванием.

## Повторяющиеся заголовки

Возможно получение повторяющихся заголовков. Это означает, что один и тот же заголовок содержит несколько значений.

Вы можете определить эти случаи, используя список в объявлении типа.

Вы получите все значения из дублирующегося заголовка в виде `списка` Python.

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

=== "Python 3.10+ non-Annotated"

    tip "Подсказка"
        Предпочтительно использовать версию `Annotated`, если это возможно.

    ```Python hl_lines="7"
    {!> ../../../docs_src/header_params/tutorial003_py310.py!}
    ```

=== "Python 3.9+ non-Annotated"

    tip "Подсказка"
        Предпочтительно использовать версию `Annotated`, если это возможно.

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial003_py39.py!}
    ```

=== "Python 3.6+ non-Annotated"

    tip "Подсказка"
        Предпочтительно использовать версию `Annotated`, если это возможно.

    ```Python hl_lines="9"
    {!> ../../../docs_src/header_params/tutorial003.py!}
    ```

Если вы взаимодействуете с этой *операцией path*, отправляя два HTTP-заголовка, таких как:

```
X-Token: foo
X-Token: bar
```

Ответ будет таким:

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## Резюме

Объявляйте заголовки с помощью `Header`, используя тот же общий шаблон, что и `Query`, `Path` и `Cookie`.

И не беспокойтесь о символах подчеркивания в ваших переменных, **FastAPI** позаботится об их преобразовании.
