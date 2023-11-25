# Додаткові типи даних

До цього часу, ви використовували загальнопоширені типи даних, такі як:

* `int`
* `float`
* `str`
* `bool`

Але можна також використовувати більш складні типи даних.

І ви все ще матимете ті ж можливості, які були показані до цього:

* Чудова підтримка редактора.
* Конвертація даних з вхідних запитів.
* Конвертація даних для відповіді.
* Валідація даних.
* Автоматична анотація та документація.

## Інші типи даних

Ось додаткові типи даних для використання:

* `UUID`:
    * Стандартний "Універсальний Унікальний Ідентифікатор", який часто використовується як ідентифікатор у багатьох базах даних та системах.
    * У запитах та відповідях буде представлений як `str`.
* `datetime.datetime`:
    * Пайтонівський `datetime.datetime`.
    * У запитах та відповідях буде представлений як `str` в форматі ISO 8601, як: `2008-09-15T15:53:00+05:00`.
* `datetime.date`:
    * Пайтонівський `datetime.date`.
    * У запитах та відповідях буде представлений як `str` в форматі ISO 8601, як: `2008-09-15`.
* `datetime.time`:
    * Пайтонівський `datetime.time`.
    * У запитах та відповідях буде представлений як `str` в форматі ISO 8601, як: `14:23:55.003`.
* `datetime.timedelta`:
    * Пайтонівський `datetime.timedelta`.
    * У запитах та відповідях буде представлений як `float` загальної кількості секунд.
    * Pydantic також дозволяє представляти це як "ISO 8601 time diff encoding", <a href="https://pydantic-docs.helpmanual.io/usage/exporting_models/#json_encoders" class="external-link" target="_blank">більше інформації дивись у документації</a>.
* `frozenset`:
    * У запитах і відповідях це буде оброблено так само, як і `set`:
        * У запитах список буде зчитано, дублікати будуть видалені та він буде перетворений на `set`.
        * У відповідях, `set` буде перетворений на `list`.
        * Згенерована схема буде вказувати, що значення `set` є унікальними (з використанням JSON Schema's `uniqueItems`).
* `bytes`:
    * Стандартний Пайтонівський `bytes`.
    * У запитах і відповідях це буде оброблено як `str`.
    * Згенерована схема буде вказувати, що це `str` з "форматом" `binary`.
* `Decimal`:
    * Стандартний Пайтонівський `Decimal`.
    * У запитах і відповідях це буде оброблено так само, як і `float`.
* Ви можете перевірити всі дійсні типи даних Pydantic тут: <a href="https://pydantic-docs.helpmanual.io/usage/types" class="external-link" target="_blank">типи даних Pydantic</a>.

## Приклад

Ось приклад *path operation* з параметрами, використовуючи деякі з вищезазначених типів.

=== "Python 3.10+"

    ```Python hl_lines="1  3  12-16"
    {!> ../../../docs_src/extra_data_types/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="1  3  12-16"
    {!> ../../../docs_src/extra_data_types/tutorial001_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="1  3  13-17"
    {!> ../../../docs_src/extra_data_types/tutorial001_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Бажано використовувати `Annotated` версію, якщо це можливо.

    ```Python hl_lines="1  2  11-15"
    {!> ../../../docs_src/extra_data_types/tutorial001_py310.py!}
    ```

=== "Python 3.8+ non-Annotated"

    !!! tip
        Бажано використовувати `Annotated` версію, якщо це можливо.

    ```Python hl_lines="1  2  12-16"
    {!> ../../../docs_src/extra_data_types/tutorial001.py!}
    ```

Зверніть увагу, що параметри всередині функції мають свій звичайний тип даних, і ви можете, наприклад, виконувати звичайні маніпуляції з датами, такі як:

=== "Python 3.10+"

    ```Python hl_lines="18-19"
    {!> ../../../docs_src/extra_data_types/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="18-19"
    {!> ../../../docs_src/extra_data_types/tutorial001_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="19-20"
    {!> ../../../docs_src/extra_data_types/tutorial001_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Бажано використовувати `Annotated` версію, якщо це можливо.

    ```Python hl_lines="17-18"
    {!> ../../../docs_src/extra_data_types/tutorial001_py310.py!}
    ```

=== "Python 3.8+ non-Annotated"

    !!! tip
        Бажано використовувати `Annotated` версію, якщо це можливо.

    ```Python hl_lines="18-19"
    {!> ../../../docs_src/extra_data_types/tutorial001.py!}
    ```
