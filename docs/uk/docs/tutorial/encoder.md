# JSON Compatible Encoder

Існують випадки, коли вам може знадобитися перетворити тип даних (наприклад, модель Pydantic) в щось сумісне з JSON (наприклад, `dict`, `list`, і т. д.).

Наприклад, якщо вам потрібно зберегти це в базі даних.

Для цього, **FastAPI** надає `jsonable_encoder()` функцію.

## Використання `jsonable_encoder`

Давайте уявимо, що у вас є база даних `fake_db`, яка приймає лише дані, сумісні з JSON.

Наприклад, вона не приймає об'єкти типу `datetime`, оскільки вони не сумісні з JSON.

Отже, об'єкт типу `datetime` потрібно перетворити в рядок `str`, який містить дані в <a href="https://en.wikipedia.org/wiki/ISO_8601" class="external-link" target="_blank">ISO форматі</a>.

Тим самим способом ця база даних не прийматиме об'єкт типу Pydantic model (об'єкт з атрибутами), а лише `dict`.

Ви можете використовувати `jsonable_encoder` для цього.

Вона приймає об'єкт, такий як Pydantic model, і повертає його версію, сумісну з JSON:

=== "Python 3.10+"

    ```Python hl_lines="4  21"
    {!> ../../../docs_src/encoder/tutorial001_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="5  22"
    {!> ../../../docs_src/encoder/tutorial001.py!}
    ```

У цьому прикладі вона конвертує Pydantic model у `dict`, а `datetime` у `str`.

Результат виклику цієї функції - це щось, що можна кодувати з використанням стандарту Python <a href="https://docs.python.org/3/library/json.html#json.dumps" class="external-link" target="_blank">`json.dumps()`</a>.

Вона не повертає велику строку `str`, яка містить дані у форматі JSON (як строка). Вона повертає стандартну структуру даних Python (наприклад `dict`) із значеннями та підзначеннями, які є сумісними з JSON.

!!! Примітка
    `jsonable_encoder` фактично використовується **FastAPI** внутрішньо для перетворення даних. Проте вона корисна в багатьох інших сценаріях.
