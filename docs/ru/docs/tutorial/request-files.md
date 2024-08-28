# Загрузка файлов

Используя класс `File`, мы можем позволить клиентам загружать файлы.

/// info | "Дополнительная информация"

Чтобы получать загруженные файлы, сначала установите <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Например: `pip install python-multipart`.

Это связано с тем, что загружаемые файлы передаются как данные формы.

///

## Импорт `File`

Импортируйте `File` и `UploadFile` из модуля `fastapi`:

//// tab | Python 3.9+

```Python hl_lines="3"
{!> ../../../docs_src/request_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.6+

```Python hl_lines="1"
{!> ../../../docs_src/request_files/tutorial001_an.py!}
```

////

//// tab | Python 3.6+ без Annotated

/// tip | "Подсказка"

Предпочтительнее использовать версию с аннотацией, если это возможно.

///

```Python hl_lines="1"
{!> ../../../docs_src/request_files/tutorial001.py!}
```

////

## Определите параметры `File`

Создайте параметры `File` так же, как вы это делаете для `Body` или `Form`:

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/request_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.6+

```Python hl_lines="8"
{!> ../../../docs_src/request_files/tutorial001_an.py!}
```

////

//// tab | Python 3.6+ без Annotated

/// tip | "Подсказка"

Предпочтительнее использовать версию с аннотацией, если это возможно.

///

```Python hl_lines="7"
{!> ../../../docs_src/request_files/tutorial001.py!}
```

////

/// info | "Дополнительная информация"

`File` - это класс, который наследуется непосредственно от `Form`.

Но помните, что когда вы импортируете `Query`, `Path`, `File` и другие из `fastapi`, на самом деле это функции, которые возвращают специальные классы.

///

/// tip | "Подсказка"

Для объявления тела файла необходимо использовать `File`, поскольку в противном случае параметры будут интерпретироваться как параметры запроса или параметры тела (JSON).

///

Файлы будут загружены как данные формы.

Если вы объявите тип параметра у *функции операции пути* как `bytes`, то **FastAPI** прочитает файл за вас, и вы получите его содержимое в виде `bytes`.

Следует иметь в виду, что все содержимое будет храниться в памяти. Это хорошо подходит для небольших файлов.

Однако возможны случаи, когда использование `UploadFile` может оказаться полезным.

## Загрузка файла с помощью `UploadFile`

Определите параметр файла с типом `UploadFile`:

//// tab | Python 3.9+

```Python hl_lines="14"
{!> ../../../docs_src/request_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.6+

```Python hl_lines="13"
{!> ../../../docs_src/request_files/tutorial001_an.py!}
```

////

//// tab | Python 3.6+ без Annotated

/// tip | "Подсказка"

Предпочтительнее использовать версию с аннотацией, если это возможно.

///

```Python hl_lines="12"
{!> ../../../docs_src/request_files/tutorial001.py!}
```

////

Использование `UploadFile` имеет ряд преимуществ перед `bytes`:

* Использовать `File()` в значении параметра по умолчанию не обязательно.
* При этом используется "буферный" файл:
    * Файл, хранящийся в памяти до максимального предела размера, после преодоления которого он будет храниться на диске.
* Это означает, что он будет хорошо работать с большими файлами, такими как изображения, видео, большие бинарные файлы и т.д., не потребляя при этом всю память.
* Из загруженного файла можно получить метаданные.
* Он реализует <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> `async` интерфейс.
* Он предоставляет реальный объект Python <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> который вы можете передать непосредственно другим библиотекам, которые ожидают файл в качестве объекта.

### `UploadFile`

`UploadFile` имеет следующие атрибуты:

* `filename`: Строка `str` с исходным именем файла, который был загружен (например, `myimage.jpg`).
* `content_type`: Строка `str` с типом содержимого (MIME type / media type) (например, `image/jpeg`).
* `file`: <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> (a <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> объект). Это фактический файл Python, который можно передавать непосредственно другим функциям или библиотекам, ожидающим файл в качестве объекта.

`UploadFile` имеет следующие методы `async`. Все они вызывают соответствующие файловые методы (используя внутренний SpooledTemporaryFile).

* `write(data)`: Записать данные `data` (`str` или `bytes`) в файл.
* `read(size)`: Прочитать количество `size` (`int`) байт/символов из файла.
* `seek(offset)`: Перейти к байту на позиции `offset` (`int`) в файле.
    * Наример, `await myfile.seek(0)` перейдет к началу файла.
    * Это особенно удобно, если вы один раз выполнили команду `await myfile.read()`, а затем вам нужно прочитать содержимое файла еще раз.
* `close()`: Закрыть файл.

Поскольку все эти методы являются `async` методами, вам следует использовать "await" вместе с ними.

Например, внутри `async` *функции операции пути* можно получить содержимое с помощью:

```Python
contents = await myfile.read()
```

Если вы находитесь внутри обычной `def` *функции операции пути*, можно получить прямой доступ к файлу `UploadFile.file`, например:

```Python
contents = myfile.file.read()
```

/// note | "Технические детали `async`"

При использовании методов `async` **FastAPI** запускает файловые методы в пуле потоков и ожидает их.

///

/// note | "Технические детали Starlette"

**FastAPI** наследует `UploadFile` непосредственно из **Starlette**, но добавляет некоторые детали для совместимости с **Pydantic** и другими частями FastAPI.

///

## Про данные формы ("Form Data")

Способ, которым HTML-формы (`<form></form>`) отправляют данные на сервер, обычно использует "специальную" кодировку для этих данных, отличную от JSON.

**FastAPI** позаботится о том, чтобы считать эти данные из нужного места, а не из JSON.

/// note | "Технические детали"

Данные из форм обычно кодируются с использованием "media type" `application/x-www-form-urlencoded` когда он не включает файлы.

Но когда форма включает файлы, она кодируется как multipart/form-data. Если вы используете `File`, **FastAPI** будет знать, что ему нужно получить файлы из нужной части тела.

Если вы хотите узнать больше об этих кодировках и полях форм, перейдите по ссылке <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> web docs for <code>POST</code></a>.

///

/// warning | "Внимание"

В операции *функции операции пути* можно объявить несколько параметров `File` и `Form`, но нельзя также объявлять поля `Body`, которые предполагается получить в виде JSON, поскольку тело запроса будет закодировано с помощью `multipart/form-data`, а не `application/json`.

Это не является ограничением **FastAPI**, это часть протокола HTTP.

///

## Необязательная загрузка файлов

Вы можете сделать загрузку файла необязательной, используя стандартные аннотации типов и установив значение по умолчанию `None`:

//// tab | Python 3.10+

```Python hl_lines="9  17"
{!> ../../../docs_src/request_files/tutorial001_02_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9  17"
{!> ../../../docs_src/request_files/tutorial001_02_an_py39.py!}
```

////

//// tab | Python 3.6+

```Python hl_lines="10  18"
{!> ../../../docs_src/request_files/tutorial001_02_an.py!}
```

////

//// tab | Python 3.10+ без Annotated

/// tip | "Подсказка"

Предпочтительнее использовать версию с аннотацией, если это возможно.

///

```Python hl_lines="7  15"
{!> ../../../docs_src/request_files/tutorial001_02_py310.py!}
```

////

//// tab | Python 3.6+ без Annotated

/// tip | "Подсказка"

Предпочтительнее использовать версию с аннотацией, если это возможно.

///

```Python hl_lines="9  17"
{!> ../../../docs_src/request_files/tutorial001_02.py!}
```

////

## `UploadFile` с дополнительными метаданными

Вы также можете использовать `File()` вместе с `UploadFile`, например, для установки дополнительных метаданных:

//// tab | Python 3.9+

```Python hl_lines="9  15"
{!> ../../../docs_src/request_files/tutorial001_03_an_py39.py!}
```

////

//// tab | Python 3.6+

```Python hl_lines="8  14"
{!> ../../../docs_src/request_files/tutorial001_03_an.py!}
```

////

//// tab | Python 3.6+ без Annotated

/// tip | "Подсказка"

Предпочтительнее использовать версию с аннотацией, если это возможно.

///

```Python hl_lines="7  13"
{!> ../../../docs_src/request_files/tutorial001_03.py!}
```

////

## Загрузка нескольких файлов

Можно одновременно загружать несколько файлов.

Они будут связаны с одним и тем же "полем формы", отправляемым с помощью данных формы.

Для этого необходимо объявить список `bytes` или `UploadFile`:

//// tab | Python 3.9+

```Python hl_lines="10  15"
{!> ../../../docs_src/request_files/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.6+

```Python hl_lines="11  16"
{!> ../../../docs_src/request_files/tutorial002_an.py!}
```

////

//// tab | Python 3.9+ без Annotated

/// tip | "Подсказка"

Предпочтительнее использовать версию с аннотацией, если это возможно.

///

```Python hl_lines="8  13"
{!> ../../../docs_src/request_files/tutorial002_py39.py!}
```

////

//// tab | Python 3.6+ без Annotated

/// tip | "Подсказка"

Предпочтительнее использовать версию с аннотацией, если это возможно.

///

```Python hl_lines="10  15"
{!> ../../../docs_src/request_files/tutorial002.py!}
```

////

Вы получите, как и было объявлено, список `list` из `bytes` или `UploadFile`.

/// note | "Technical Details"

Можно также использовать `from starlette.responses import HTMLResponse`.

**FastAPI** предоставляет тот же `starlette.responses`, что и `fastapi.responses`, просто для удобства разработчика. Однако большинство доступных ответов поступает непосредственно из Starlette.

///

### Загрузка нескольких файлов с дополнительными метаданными

Так же, как и раньше, вы можете использовать `File()` для задания дополнительных параметров, даже для `UploadFile`:

//// tab | Python 3.9+

```Python hl_lines="11  18-20"
{!> ../../../docs_src/request_files/tutorial003_an_py39.py!}
```

////

//// tab | Python 3.6+

```Python hl_lines="12  19-21"
{!> ../../../docs_src/request_files/tutorial003_an.py!}
```

////

//// tab | Python 3.9+ без Annotated

/// tip | "Подсказка"

Предпочтительнее использовать версию с аннотацией, если это возможно.

///

```Python hl_lines="9  16"
{!> ../../../docs_src/request_files/tutorial003_py39.py!}
```

////

//// tab | Python 3.6+ без Annotated

/// tip | "Подсказка"

Предпочтительнее использовать версию с аннотацией, если это возможно.

///

```Python hl_lines="11  18"
{!> ../../../docs_src/request_files/tutorial003.py!}
```

////

## Резюме

Используйте `File`, `bytes` и `UploadFile` для работы с файлами, которые будут загружаться и передаваться в виде данных формы.
