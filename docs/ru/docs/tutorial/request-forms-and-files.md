# Файлы и формы в запросе

Вы можете определять файлы и поля формы одновременно, используя `File` и `Form`.

/// info | "Дополнительная информация"

Чтобы получать загруженные файлы и/или данные форм, сначала установите <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Например: `pip install python-multipart`.

///

## Импортируйте `File` и `Form`

//// tab | Python 3.9+

```Python hl_lines="3"
{!> ../../../docs_src/request_forms_and_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.6+

```Python hl_lines="1"
{!> ../../../docs_src/request_forms_and_files/tutorial001_an.py!}
```

////

//// tab | Python 3.6+ без Annotated

/// tip | "Подсказка"

Предпочтительнее использовать версию с аннотацией, если это возможно.

///

```Python hl_lines="1"
{!> ../../../docs_src/request_forms_and_files/tutorial001.py!}
```

////

## Определите параметры `File` и `Form`

Создайте параметры файла и формы таким же образом, как для `Body` или `Query`:

//// tab | Python 3.9+

```Python hl_lines="10-12"
{!> ../../../docs_src/request_forms_and_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.6+

```Python hl_lines="9-11"
{!> ../../../docs_src/request_forms_and_files/tutorial001_an.py!}
```

////

//// tab | Python 3.6+ без Annotated

/// tip | "Подсказка"

Предпочтительнее использовать версию с аннотацией, если это возможно.

///

```Python hl_lines="8"
{!> ../../../docs_src/request_forms_and_files/tutorial001.py!}
```

////

Файлы и поля формы будут загружены в виде данных формы, и вы получите файлы и поля формы.

Вы можете объявить некоторые файлы как `bytes`, а некоторые - как `UploadFile`.

/// warning | "Внимание"

Вы можете объявить несколько параметров `File` и `Form` в операции *path*, но вы не можете также объявить поля `Body`, которые вы ожидаете получить в виде JSON, так как запрос будет иметь тело, закодированное с помощью `multipart/form-data` вместо `application/json`.

Это не ограничение **Fast API**, это часть протокола HTTP.

///

## Резюме

Используйте `File` и `Form` вместе, когда необходимо получить данные и файлы в одном запросе.
