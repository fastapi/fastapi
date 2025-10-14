# Файлы и формы в запросе { #request-forms-and-files }

Вы можете определять файлы и поля формы одновременно, используя `File` и `Form`.

/// info | Информация

Чтобы получать загруженные файлы и/или данные форм, сначала установите <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Убедитесь, что вы создали [виртуальное окружение](../virtual-environments.md){.internal-link target=_blank}, активировали его, а затем установили пакет, например:

```console
$ pip install python-multipart
```

///

## Импортируйте `File` и `Form` { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[3] *}

## Определите параметры `File` и `Form` { #define-file-and-form-parameters }

Создайте параметры файла и формы таким же образом, как для `Body` или `Query`:

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[10:12] *}

Файлы и поля формы будут загружены в виде данных формы, и вы получите файлы и поля формы.

Вы можете объявить некоторые файлы как `bytes`, а некоторые — как `UploadFile`.

/// warning | Внимание

Вы можете объявить несколько параметров `File` и `Form` в операции пути, но вы не можете также объявить поля `Body`, которые вы ожидаете получить в виде JSON, так как запрос будет иметь тело, закодированное с помощью `multipart/form-data` вместо `application/json`.

Это не ограничение **FastAPI**, это часть протокола HTTP.

///

## Резюме { #recap }

Используйте `File` и `Form` вместе, когда необходимо получить данные и файлы в одном запросе.
