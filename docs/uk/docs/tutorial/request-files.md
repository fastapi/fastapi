# Запит файлів { #request-files }

Ви можете визначити файли, які будуть завантажуватися клієнтом, використовуючи `File`.

/// info | Інформація

Щоб отримувати завантажені файли, спочатку встановіть <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Переконайтеся, що ви створили [віртуальне середовище](../virtual-environments.md){.internal-link target=_blank}, активували його, а потім встановили пакет, наприклад:

```console
$ pip install python-multipart
```

Це необхідно, оскільки завантажені файли передаються у вигляді «form data».

///

## Імпорт `File` { #import-file }

Імпортуйте `File` та `UploadFile` з `fastapi`:

{* ../../docs_src/request_files/tutorial001_an_py39.py hl[3] *}

## Визначення параметрів `File` { #define-file-parameters }

Створіть параметри файлів так само як ви б створювали `Body` або `Form`:

{* ../../docs_src/request_files/tutorial001_an_py39.py hl[9] *}

/// info | Інформація

`File` — це клас, який безпосередньо успадковує `Form`.

Але пам’ятайте, що коли ви імпортуєте `Query`, `Path`, `File` та інші з `fastapi`, це насправді функції, які повертають спеціальні класи.

///

/// tip | Порада

Щоб оголосити тіла файлів, вам потрібно використовувати `File`, тому що інакше параметри будуть інтерпретовані як параметри запиту або параметри тіла (JSON).

///

Файли будуть завантажені у вигляді «form data».

Якщо ви оголосите тип параметра *функції операції шляху* як `bytes`, **FastAPI** прочитає файл за вас, і ви отримаєте його вміст у вигляді `bytes`.

Майте на увазі, що це означає, що весь вміст буде збережено в пам'яті. Це працюватиме добре для малих файлів.

Але є кілька випадків, у яких вам може бути корисно використовувати `UploadFile`.

## Параметри файлу з `UploadFile` { #file-parameters-with-uploadfile }

Визначте параметр файлу з типом `UploadFile`:

{* ../../docs_src/request_files/tutorial001_an_py39.py hl[14] *}

Використання `UploadFile` має кілька переваг перед `bytes`:

* Вам не потрібно використовувати `File()` у значенні за замовчуванням параметра.
* Використовується «spooled» файл:
    * Файл зберігається в пам'яті до досягнення максимального обмеження розміру, після чого він буде збережений на диску.
* Це означає, що він добре працюватиме для великих файлів, таких як зображення, відео, великі двійкові файли тощо, не споживаючи всю пам'ять.
* Ви можете отримати метадані про завантажений файл.
* Він має <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> `async` інтерфейс.
* Він надає фактичний об'єкт Python <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a>, який можна передавати безпосередньо іншим бібліотекам, що очікують file-like об'єкт.

### `UploadFile` { #uploadfile }

`UploadFile` має такі атрибути:

* `filename`: Рядок `str` з оригінальною назвою файлу, який був завантажений (наприклад, `myimage.jpg`).
* `content_type`: Рядок `str` з типом вмісту (MIME type / media type) (наприклад, `image/jpeg`).
* `file`: <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> (<a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> об'єкт). Це фактичний файловий об'єкт Python, який ви можете передавати безпосередньо іншим функціям або бібліотекам, що очікують «file-like» об'єкт.

`UploadFile` має такі асинхронні `async` методи. Вони всі викликають відповідні методи файлу під капотом (використовуючи внутрішній `SpooledTemporaryFile`).

* `write(data)`: Записує `data` (`str` або `bytes`) у файл.
* `read(size)`: Читає `size` (`int`) байтів/символів з файлу.
* `seek(offset)`: Переходить до байтової позиції `offset` (`int`) у файлі.
    * Наприклад, `await myfile.seek(0)` перейде на початок файлу.
    * Це особливо корисно, якщо ви виконаєте `await myfile.read()` один раз, а потім потрібно знову прочитати вміст.
* `close()`: Закриває файл.

Оскільки всі ці методи є асинхронними `async` методами, вам потрібно їх «await»-ити.

Наприклад, всередині `async` *функції операції шляху* ви можете отримати вміст за допомогою:

```Python
contents = await myfile.read()
```

Якщо ви знаходитесь у звичайній `def` *функції операції шляху*, ви можете отримати доступ до `UploadFile.file` безпосередньо, наприклад:

```Python
contents = myfile.file.read()
```

/// note | Технічні деталі `async`

Коли ви використовуєте `async` методи, **FastAPI** виконує файлові методи у пулі потоків і очікує на них.

///

/// note | Технічні деталі Starlette

`UploadFile` у **FastAPI** успадковується безпосередньо від `UploadFile` у **Starlette**, але додає деякі необхідні частини, щоб зробити його сумісним із **Pydantic** та іншими частинами FastAPI.

///

## Що таке «Form Data» { #what-is-form-data }

Спосіб, у який HTML-форми (`<form></form>`) надсилають дані на сервер, зазвичай використовує «спеціальне» кодування для цих даних, відмінне від JSON.

**FastAPI** забезпечить зчитування цих даних з правильного місця, а не з JSON.

/// note | Технічні деталі

Дані з форм зазвичай кодуються за допомогою «media type» `application/x-www-form-urlencoded`, якщо вони не містять файлів.

Але якщо форма містить файли, вона кодується як `multipart/form-data`. Якщо ви використовуєте `File`, **FastAPI** знатиме, що потрібно отримати файли з правильної частини тіла.

Якщо ви хочете дізнатися більше про ці типи кодування та формові поля, ознайомтеся з <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> web docs для <code>POST</code></a>.

///

/// warning | Попередження

Ви можете оголосити кілька параметрів `File` і `Form` в *операції шляху*, але ви не можете одночасно оголошувати поля `Body`, які ви очікуєте отримати як JSON, оскільки запит матиме тіло, закодоване як `multipart/form-data`, а не `application/json`.

Це не обмеження **FastAPI**, а частина протоколу HTTP.

///

## Необов’язкове завантаження файлу { #optional-file-upload }

Ви можете зробити файл необов’язковим, використовуючи стандартні анотації типів і встановивши значення за замовчуванням `None`:

{* ../../docs_src/request_files/tutorial001_02_an_py310.py hl[9,17] *}

## `UploadFile` із додатковими метаданими { #uploadfile-with-additional-metadata }

Ви також можете використовувати `File()` разом із `UploadFile`, наприклад, щоб встановити додаткові метадані:

{* ../../docs_src/request_files/tutorial001_03_an_py39.py hl[9,15] *}

## Завантаження кількох файлів { #multiple-file-uploads }

Можна завантажувати кілька файлів одночасно.

Вони будуть пов’язані з одним і тим самим «form field», який передається у вигляді «form data».

Щоб це реалізувати, потрібно оголосити список `bytes` або `UploadFile`:

{* ../../docs_src/request_files/tutorial002_an_py39.py hl[10,15] *}

Ви отримаєте, як і було оголошено, `list` із `bytes` або `UploadFile`.

/// note | Технічні деталі

Ви також можете використати `from starlette.responses import HTMLResponse`.

**FastAPI** надає ті ж самі `starlette.responses`, що й `fastapi.responses`, просто для зручності для вас, розробника. Але більшість доступних відповідей надходять безпосередньо від Starlette.

///

### Завантаження кількох файлів із додатковими метаданими { #multiple-file-uploads-with-additional-metadata }

Так само як і раніше, ви можете використовувати `File()`, щоб встановити додаткові параметри навіть для `UploadFile`:

{* ../../docs_src/request_files/tutorial003_an_py39.py hl[11,18:20] *}

## Підсумок { #recap }

Використовуйте `File`, `bytes` та `UploadFile`, щоб оголошувати файли для завантаження в запиті, надіслані у вигляді form data.
