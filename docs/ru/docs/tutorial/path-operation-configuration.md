# Конфигурация операций пути

Существует несколько параметров, которые вы можете передать вашему *декоратору операций пути* для его настройки.

!!! warning "Внимание"
    Помните, что эти параметры передаются непосредственно *декоратору операций пути*, а не вашей *функции-обработчику операций пути*.

## Коды состояния

Вы можете определить (HTTP) `status_code`, который будет использован в ответах вашей *операции пути*.

Вы можете передать только `int`-значение кода, например `404`.

Но если вы не помните, для чего нужен каждый числовой код, вы можете использовать сокращенные константы в параметре `status`:

=== "Python 3.10+"

    ```Python hl_lines="1  15"
    {!> ../../../docs_src/path_operation_configuration/tutorial001_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="3  17"
    {!> ../../../docs_src/path_operation_configuration/tutorial001_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="3  17"
    {!> ../../../docs_src/path_operation_configuration/tutorial001.py!}
    ```

Этот код состояния будет использован в ответе и будет добавлен в схему OpenAPI.

!!! note "Технические детали"
    Вы также можете использовать `from starlette import status`.

    **FastAPI** предоставляет тот же `starlette.status` под псевдонимом `fastapi.status` для удобства разработчика. Но его источник - это непосредственно Starlette.

## Теги

Вы можете добавлять теги к вашим *операциям пути*, добавив параметр `tags` с `list` заполненным `str`-значениями (обычно в нём только одна строка):

=== "Python 3.10+"

    ```Python hl_lines="15  20  25"
    {!> ../../../docs_src/path_operation_configuration/tutorial002_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="17  22  27"
    {!> ../../../docs_src/path_operation_configuration/tutorial002_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="17  22  27"
    {!> ../../../docs_src/path_operation_configuration/tutorial002.py!}
    ```

Они будут добавлены в схему OpenAPI и будут использованы в автоматической документации интерфейса:

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Теги с перечислениями

Если у вас большое приложение, вы можете прийти к необходимости добавить **несколько тегов**, и возможно, вы захотите убедиться в том, что всегда используете **один и тот же тег** для связанных *операций пути*.

В этих случаях, имеет смысл хранить теги в классе `Enum`.

**FastAPI** поддерживает это так же, как и в случае с обычными строками:

```Python hl_lines="1  8-10  13  18"
{!../../../docs_src/path_operation_configuration/tutorial002b.py!}
```

## Краткое и развёрнутое содержание

Вы можете добавить параметры `summary` и `description`:

=== "Python 3.10+"

    ```Python hl_lines="18-19"
    {!> ../../../docs_src/path_operation_configuration/tutorial003_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="20-21"
    {!> ../../../docs_src/path_operation_configuration/tutorial003_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="20-21"
    {!> ../../../docs_src/path_operation_configuration/tutorial003.py!}
    ```

## Описание из строк документации

Так как описания обычно длинные и содержат много строк, вы можете объявить описание *операции пути* в функции <abbr title="многострочный текст, первое выражение внутри функции (не присвоенный какой-либо переменной), используемый для документации">строки документации</abbr> и **FastAPI** прочитает её отсюда.

Вы можете использовать <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a> в строке документации, и он будет интерпретирован и отображён корректно (с учетом отступа в строке документации).

=== "Python 3.10+"

    ```Python hl_lines="17-25"
    {!> ../../../docs_src/path_operation_configuration/tutorial004_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="19-27"
    {!> ../../../docs_src/path_operation_configuration/tutorial004_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="19-27"
    {!> ../../../docs_src/path_operation_configuration/tutorial004.py!}
    ```

Он будет использован в интерактивной документации:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## Описание ответа

Вы можете указать описание ответа с помощью параметра `response_description`:

=== "Python 3.10+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/path_operation_configuration/tutorial005_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="21"
    {!> ../../../docs_src/path_operation_configuration/tutorial005_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="21"
    {!> ../../../docs_src/path_operation_configuration/tutorial005.py!}
    ```

!!! info "Дополнительная информация"
    Помните, что `response_description` относится конкретно к ответу, а `description` относится к *операции пути* в целом.

!!! check "Технические детали"
    OpenAPI указывает, что каждой *операции пути* необходимо описание ответа.

    Если вдруг вы не укажете его, то **FastAPI** автоматически сгенерирует это описание с текстом "Successful response".

<img src="/img/tutorial/path-operation-configuration/image03.png">

## Обозначение *операции пути* как устаревшей

Если вам необходимо пометить *операцию пути* как <abbr title="устаревшее, не рекомендовано к использованию">устаревшую</abbr>, при этом не удаляя её, передайте параметр `deprecated`:

```Python hl_lines="16"
{!../../../docs_src/path_operation_configuration/tutorial006.py!}
```

Он будет четко помечен как устаревший в интерактивной документации:

<img src="/img/tutorial/path-operation-configuration/image04.png">

Проверьте, как будут выглядеть устаревшие и не устаревшие *операции пути*:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## Резюме

Вы можете легко конфигурировать и добавлять метаданные в ваши *операции пути*, передавая параметры *декораторам операций пути*.
