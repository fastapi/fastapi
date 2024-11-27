# Модели Query-Параметров

Если у вас есть группа связанных **query-параметров**, то вы можете объединить их в одну **Pydantic-модель**.

Это позволит вам **переиспользовать модель** в **разных местах**, устанавливать валидаторы и метаданные, в том числе для сразу всех параметров, в одном месте. 😎

/// note | Заметка

Этот функционал доступен с версии `0.115.0`. 🤓

///

## Pydantic-Модель для Query-Параметров

Объявите нужные **query-параметры** в **Pydantic-модели**, а после аннотируйте параметр как `Query`:

//// tab | Python 3.10+

```Python hl_lines="9-13  17"
{!> ../../docs_src/query_param_models/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="8-12  16"
{!> ../../docs_src/query_param_models/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10-14  18"
{!> ../../docs_src/query_param_models/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ без Annotated

/// tip | Совет

При возможности используйте версию с `Annotated`.

///

```Python hl_lines="9-13  17"
{!> ../../docs_src/query_param_models/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+ без Annotated

/// tip | Совет

При возможности используйте версию с `Annotated`.

///

```Python hl_lines="8-12 16"
{!> ../../docs_src/query_param_models/tutorial001_py39.py!}
```

////

//// tab | Python 3.8+ без Annotated

/// tip | Совет

При возможности используйте версию с `Annotated`.

///

```Python hl_lines="9-13  17"
{!> ../../docs_src/query_param_models/tutorial001_py310.py!}
```

////

**FastAPI извлечёт** данные соответствующие **каждому полю модели** из **query-параметров** запроса и выдаст вам объявленную Pydantic-модель заполненную ими.

## Проверьте Сгенерированную Документацию

Вы можете посмотреть query-параметры в графическом интерфейсе сгенерированной документации по пути `/docs`:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Запретить Дополнительные Query-Параметры

В некоторых случаях (не особо часто встречающихся) вам может понадобиться **ограничить** query-параметры, которые вы хотите получить.

Вы можете сконфигурировать Pydantic-модель так, чтобы запретить (`forbid`) все дополнительные (`extra`) поля.

//// tab | Python 3.10+

```Python hl_lines="10"
{!> ../../docs_src/query_param_models/tutorial002_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../docs_src/query_param_models/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11"
{!> ../../docs_src/query_param_models/tutorial002_an.py!}
```

////

//// tab | Python 3.10+ без Annotated

/// tip | Совет

При возможности используйте версию с `Annotated`.

///

```Python hl_lines="10"
{!> ../../docs_src/query_param_models/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+ без Annotated

/// tip | Совет

При возможности используйте версию с `Annotated`.

///

```Python hl_lines="9"
{!> ../../docs_src/query_param_models/tutorial002_py39.py!}
```

////

//// tab | Python 3.8+ без Annotated

/// tip | Совет

При возможности используйте версию с `Annotated`.

///

```Python hl_lines="11"
{!> ../../docs_src/query_param_models/tutorial002.py!}
```

////

Если клиент попробует отправить **дополнительные** данные в **query-параметрах**, то в ответ он получит **ошибку**.

Например, если клиент попытается отправить query-параметр `tool` с значением `plumbus`, в виде:

```http
https://example.com/items/?limit=10&tool=plumbus
```

То в ответ он получит **ошибку**, сообщающую ему, что query-параметр `tool` не разрешен:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## Заключение

Вы можете использовать **Pydantic-модели** для объявления **query-параметров** в **FastAPI**. 😎

/// tip | Совет

Спойлер: вы также можете использовать Pydantic-модели для группировки кук (cookies) и заголовков (headers), но об этом вы прочитаете позже. 🤫

///
