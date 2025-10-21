# Модели форм { #form-models }

Вы можете использовать **Pydantic-модели** для объявления **полей формы** в FastAPI.

/// info | Дополнительная информация

Чтобы использовать формы, сначала установите <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Убедитесь, что вы создали и активировали [виртуальное окружение](../virtual-environments.md){.internal-link target=_blank}, а затем установите пакет, например:

```console
$ pip install python-multipart
```

///

/// note | Заметка

Этот функционал доступен начиная с версии FastAPI `0.113.0`. 🤓

///

## Pydantic-модели для форм { #pydantic-models-for-forms }

Вам просто нужно объявить **Pydantic-модель** с полями, которые вы хотите получить как **поля формы**, а затем объявить параметр как `Form`:

{* ../../docs_src/request_form_models/tutorial001_an_py39.py hl[9:11,15] *}

**FastAPI** **извлечёт** данные для **каждого поля** из **данных формы** в запросе и выдаст вам объявленную Pydantic-модель.

## Проверьте документацию { #check-the-docs }

Вы можете проверить это в интерфейсе документации по адресу `/docs`:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Запрет дополнительных полей формы { #forbid-extra-form-fields }

В некоторых случаях (не особо часто встречающихся) вам может понадобиться **ограничить** поля формы только теми, которые объявлены в Pydantic-модели. И **запретить** любые **дополнительные** поля.

/// note | Заметка

Этот функционал доступен начиная с версии FastAPI `0.114.0`. 🤓

///

Вы можете сконфигурировать Pydantic-модель так, чтобы запретить (`forbid`) все дополнительные (`extra`) поля:

{* ../../docs_src/request_form_models/tutorial002_an_py39.py hl[12] *}

Если клиент попробует отправить дополнительные данные, то в ответ он получит **ошибку**.

Например, если клиент попытается отправить поля формы:

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

То в ответ он получит **ошибку**, сообщающую ему, что поле `extra` не разрешено:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## Итоги { #summary }

Вы можете использовать Pydantic-модели для объявления полей форм в FastAPI. 😎
