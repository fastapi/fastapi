# Використання dataclasses { #using-dataclasses }

FastAPI побудовано поверх **Pydantic**, і я показував вам, як використовувати моделі Pydantic для оголошення запитів і відповідей.

Але FastAPI також підтримує використання [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) таким самим чином:

{* ../../docs_src/dataclasses_/tutorial001_py310.py hl[1,6:11,18:19] *}

Це підтримується завдяки **Pydantic**, адже він має [внутрішню підтримку `dataclasses`](https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel).

Тож навіть із наведеним вище кодом, який явно не використовує Pydantic, FastAPI використовує Pydantic, щоб перетворити стандартні dataclasses у власний варіант dataclasses Pydantic.

І, звісно, підтримується те саме:

* валідація даних
* серіалізація даних
* документація даних тощо

Це працює так само, як із моделями Pydantic. Насправді під капотом це також досягається за допомогою Pydantic.

/// info

Майте на увазі, що dataclasses не можуть робити все те, що можуть моделі Pydantic.

Тож вам усе ще може знадобитися використовувати моделі Pydantic.

Але якщо у вас вже є чимало dataclasses, це зручний трюк, щоб задіяти їх для веб-API на FastAPI. 🤓

///

## Dataclasses у `response_model` { #dataclasses-in-response-model }

Ви також можете використовувати `dataclasses` у параметрі `response_model`:

{* ../../docs_src/dataclasses_/tutorial002_py310.py hl[1,6:12,18] *}

Dataclass буде автоматично перетворено на dataclass Pydantic.

Таким чином його схема з'явиться в інтерфейсі користувача документації API:

<img src="/img/tutorial/dataclasses/image01.png">

## Dataclasses у вкладених структурах даних { #dataclasses-in-nested-data-structures }

Можна поєднувати `dataclasses` з іншими анотаціями типів, щоб створювати вкладені структури даних.

У деяких випадках вам усе ж доведеться використовувати варіант `dataclasses` від Pydantic. Наприклад, якщо виникають помилки з автоматично згенерованою документацією API.

У такому разі ви можете просто замінити стандартні `dataclasses` на `pydantic.dataclasses`, що є взаємозамінником:

{* ../../docs_src/dataclasses_/tutorial003_py310.py hl[1,4,7:10,13:16,22:24,27] *}

1. Ми все ще імпортуємо `field` зі стандартних `dataclasses`.

2. `pydantic.dataclasses` - це взаємозамінник для `dataclasses`.

3. Dataclass `Author` містить список dataclass `Item`.

4. Dataclass `Author` використовується як параметр `response_model`.

5. Ви можете використовувати інші стандартні анотації типів із dataclasses як тіло запиту.

    У цьому випадку це список dataclass `Item`.

6. Тут ми повертаємо словник, що містить `items`, який є списком dataclass.

    FastAPI усе ще здатний <dfn title="перетворення даних у формат, який можна передати">серіалізувати</dfн> дані до JSON.

7. Тут у `response_model` використано анотацію типу список dataclass `Author`.

    Знову ж, ви можете поєднувати `dataclasses` зі стандартними анотаціями типів.

8. Зверніть увагу, що ця *функція операції шляху* використовує звичайний `def` замість `async def`.

    Як завжди, у FastAPI ви можете поєднувати `def` і `async def` за потреби.

    Якщо вам потрібне коротке нагадування, коли що використовувати, перегляньте розділ _«Поспішаєте?»_ у документації про [`async` та `await`](../async.md#in-a-hurry).

9. Ця *функція операції шляху* не повертає dataclasses (хоча могла б), а список словників із внутрішніми даними.

    FastAPI використає параметр `response_model` (що включає dataclasses), щоб перетворити відповідь.

Ви можете поєднувати `dataclasses` з іншими анотаціями типів у багатьох поєднаннях, щоб формувати складні структури даних.

Перегляньте підказки щодо анотацій у коді вище, щоб побачити більше деталей.

## Дізнатися більше { #learn-more }

Можна поєднувати `dataclasses` з іншими моделями Pydantic, наслідувати їх, включати у власні моделі тощо.

Щоб дізнатися більше, перегляньте [документацію Pydantic про dataclasses](https://docs.pydantic.dev/latest/concepts/dataclasses/).

## Версія { #version }

Доступно починаючи з версії FastAPI `0.67.0`. 🔖
