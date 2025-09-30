# Использование dataclasses { #using-dataclasses }

FastAPI построен поверх **Pydantic**, и я показывал вам, как использовать Pydantic-модели для объявления HTTP-запросов и HTTP-ответов.

Но FastAPI также поддерживает использование <a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a> тем же способом:

{* ../../docs_src/dataclasses/tutorial001.py hl[1,7:12,19:20] *}

Это по-прежнему поддерживается благодаря **Pydantic**, так как в нём есть <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">встроенная поддержка `dataclasses`</a>.

Так что даже если в коде выше Pydantic не используется явно, FastAPI использует Pydantic, чтобы конвертировать стандартные dataclasses в собственный вариант dataclasses от Pydantic.

И, конечно, поддерживаются те же возможности:

- валидация данных
- сериализация данных
- документирование данных и т.д.

Это работает так же, как с Pydantic-моделями. И на самом деле под капотом это достигается тем же образом, с использованием Pydantic.

/// info | Информация

Помните, что dataclasses не умеют всего того, что умеют Pydantic-модели.

Поэтому вам всё ещё может потребоваться использовать Pydantic-модели.

Но если у вас уже есть набор dataclasses, это полезный приём — задействовать их для веб-API на FastAPI. 🤓

///

## Dataclasses в `response_model` { #dataclasses-in-response-model }

Вы также можете использовать `dataclasses` в параметре `response_model`:

{* ../../docs_src/dataclasses/tutorial002.py hl[1,7:13,19] *}

Этот dataclass будет автоматически преобразован в Pydantic dataclass.

Таким образом, его схема появится в интерфейсе документации API:

<img src="/img/tutorial/dataclasses/image01.png">

## Dataclasses во вложенных структурах данных { #dataclasses-in-nested-data-structures }

Вы также можете комбинировать `dataclasses` с другими аннотациями типов, чтобы создавать вложенные структуры данных.

В некоторых случаях вам всё же может понадобиться использовать версию `dataclasses` из Pydantic. Например, если у вас возникают ошибки с автоматически генерируемой документацией API.

В таком случае вы можете просто заменить стандартные `dataclasses` на `pydantic.dataclasses`, которая является полностью совместимой заменой (drop-in replacement):

{* ../../docs_src/dataclasses/tutorial003.py hl[1,5,8:11,14:17,23:25,28] *}

1. Мы по-прежнему импортируем `field` из стандартных `dataclasses`.

2. `pydantic.dataclasses` — полностью совместимая замена (drop-in replacement) для `dataclasses`.

3. Dataclass `Author` содержит список dataclass `Item`.

4. Dataclass `Author` используется в параметре `response_model`.

5. Вы можете использовать и другие стандартные аннотации типов вместе с dataclasses в качестве тела запроса.

    В этом случае это список dataclass `Item`.

6. Здесь мы возвращаем словарь, содержащий `items`, который является списком dataclass.

    FastAPI по-прежнему способен <abbr title="преобразование данных в формат, который можно передавать">сериализовать</abbr> данные в JSON.

7. Здесь `response_model` использует аннотацию типа — список dataclass `Author`.

    Снова, вы можете комбинировать `dataclasses` со стандартными аннотациями типов.

8. Обратите внимание, что эта *функция-обработчик пути* использует обычный `def` вместо `async def`.

    Как и всегда в FastAPI, вы можете сочетать `def` и `async def` по необходимости.

    Если хотите освежить в памяти, когда что использовать, посмотрите раздел _"Нет времени?"_ в документации про [`async` и `await`](../async.md#in-a-hurry){.internal-link target=_blank}.

9. Эта *функция-обработчик пути* возвращает не dataclasses (хотя могла бы), а список словарей с внутренними данными.

    FastAPI использует параметр `response_model` (в котором заданы dataclasses), чтобы преобразовать HTTP-ответ.

Вы можете комбинировать `dataclasses` с другими аннотациями типов множеством способов, чтобы формировать сложные структуры данных.

Смотрите подсказки в коде выше, чтобы увидеть более конкретные детали.

## Узнать больше { #learn-more }

Вы также можете комбинировать `dataclasses` с другими Pydantic-моделями, наследоваться от них, включать их в свои модели и т.д.

Чтобы узнать больше, посмотрите <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/" class="external-link" target="_blank">документацию Pydantic о dataclasses</a>.

## Версия { #version }

Доступно начиная с версии FastAPI `0.67.0`. 🔖
