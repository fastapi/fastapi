# Запити з формами та файлами { #request-forms-and-files }

Ви можете одночасно визначати файли та поля форми, використовуючи `File` і `Form`.

/// info | Інформація

Щоб отримувати завантажені файли та/або дані форми, спочатку встановіть <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Переконайтеся, що Ви створили [віртуальне середовище](../virtual-environments.md){.internal-link target=_blank}, активували його, а потім встановили бібліотеку, наприклад:

```console
$ pip install python-multipart
```

///

## Імпорт `File` та `Form` { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[3] *}

## Оголошення параметрів `File` та `Form` { #define-file-and-form-parameters }

Створіть параметри файлів та форми так само як і для `Body` або `Query`:

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[10:12] *}

Файли та поля форми будуть завантажені як формові дані, і Ви отримаєте файли та поля форми.

Ви також можете оголосити деякі файли як `bytes`, а деякі як `UploadFile`.

/// warning | Попередження

Ви можете оголосити кілька параметрів `File` і `Form` в операції *шляху*, але не можете одночасно оголошувати `Body`-поля, які очікуєте отримати у форматі JSON, оскільки запит матиме тіло, закодоване за допомогою `multipart/form-data`, а не `application/json`.

Це не обмеження **FastAPI**, а частина протоколу HTTP.

///

## Підсумок { #recap }

Використовуйте `File` та `Form` разом, коли вам потрібно отримувати дані та файли в одному запиті.
