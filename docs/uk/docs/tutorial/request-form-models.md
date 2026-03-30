# Моделі форм { #form-models }

У FastAPI ви можете використовувати **Pydantic-моделі** для оголошення **полів форми**.

/// info

Щоб використовувати форми, спочатку встановіть [`python-multipart`](https://github.com/Kludex/python-multipart).

Переконайтеся, що ви створили [віртуальне середовище](../virtual-environments.md), активували його, а потім встановили його, наприклад:

```console
$ pip install python-multipart
```

///

/// note

Це підтримується, починаючи з FastAPI версії `0.113.0`. 🤓

///

## Pydantic-моделі для форм { #pydantic-models-for-forms }

Вам просто потрібно оголосити **Pydantic-модель** з полями, які ви хочете отримати як **поля форми**, а потім оголосити параметр як `Form`:

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI**  **витягне** дані для **кожного поля** з **формових даних** у запиті та надасть вам Pydantic-модель, яку ви визначили.

## Перевірте документацію { #check-the-docs }

Ви можете перевірити це в UI документації за `/docs`:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Забороніть додаткові поля форми { #forbid-extra-form-fields }

У деяких особливих випадках (ймовірно, не дуже поширених) ви можете **обмежити** поля форми лише тими, які були оголошені в Pydantic-моделі. І **заборонити** будь-які **додаткові** поля.

/// note

Це підтримується, починаючи з FastAPI версії `0.114.0`. 🤓

///

Ви можете використати конфігурацію Pydantic-моделі, щоб заборонити `forbid` будь-які додаткові `extra` поля:

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

Якщо клієнт спробує надіслати додаткові дані, він отримає **відповідь з помилкою**.

Наприклад, якщо клієнт спробує надіслати поля форми:

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

Він отримає відповідь із помилкою, яка повідомляє, що поле `extra` не дозволено:

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

## Підсумок { #summary }

У FastAPI ви можете використовувати Pydantic-моделі для оголошення полів форми. 😎
