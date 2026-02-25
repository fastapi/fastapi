# Додаткові моделі { #extra-models }

Продовжуючи попередній приклад, часто потрібно мати більше ніж одну пов’язану модель.

Особливо це стосується моделей користувача, тому що:

* **вхідна модель** повинна мати пароль.
* **вихідна модель** не повинна містити пароль.
* **модель бази даних**, ймовірно, повинна містити хеш пароля.

/// danger | Обережно

Ніколи не зберігайте паролі користувачів у відкритому вигляді. Завжди зберігайте «безпечний хеш», який потім можна перевірити.

Якщо ви ще не знаєте, що таке «хеш пароля», ви дізнаєтесь у [розділах про безпеку](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}.

///

## Кілька моделей { #multiple-models }

Ось загальна ідея того, як можуть виглядати моделі з їхніми полями пароля та місцями використання:

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

### Про `**user_in.model_dump()` { #about-user-in-model-dump }

#### `.model_dump()` у Pydantic { #pydantics-model-dump }

`user_in` - це модель Pydantic класу `UserIn`.

Моделі Pydantic мають метод `.model_dump()`, який повертає `dict` з даними моделі.

Отже, якщо ми створимо об’єкт Pydantic `user_in` так:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

і викличемо:

```Python
user_dict = user_in.model_dump()
```

тепер ми маємо `dict` з даними у змінній `user_dict` (це `dict`, а не об’єкт моделі Pydantic).

А якщо викликати:

```Python
print(user_dict)
```

ми отримаємо Python `dict` з:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### Розпакування `dict` { #unpacking-a-dict }

Якщо взяти `dict`, наприклад `user_dict`, і передати його у функцію (або клас) як `**user_dict`, Python «розпакує» його. Ключі та значення `user_dict` будуть передані безпосередньо як іменовані аргументи.

Отже, продовжуючи з `user_dict` вище, запис:

```Python
UserInDB(**user_dict)
```

дасть еквівалентний результат:

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

А точніше, використовуючи безпосередньо `user_dict`, з будь-яким його вмістом у майбутньому:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### Модель Pydantic зі вмісту іншої { #a-pydantic-model-from-the-contents-of-another }

Як у прикладі вище ми отримали `user_dict` з `user_in.model_dump()`, цей код:

```Python
user_dict = user_in.model_dump()
UserInDB(**user_dict)
```

буде еквівалентним:

```Python
UserInDB(**user_in.model_dump())
```

...тому що `user_in.model_dump()` повертає `dict`, а ми змушуємо Python «розпакувати» його, передаючи в `UserInDB` з префіксом `**`.

Тож ми отримуємо модель Pydantic з даних іншої моделі Pydantic.

#### Розпакування `dict` і додаткові ключові аргументи { #unpacking-a-dict-and-extra-keywords }

Додаючи додатковий іменований аргумент `hashed_password=hashed_password`, як тут:

```Python
UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
```

...у підсумку це дорівнює:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning | Попередження

Додаткові допоміжні функції `fake_password_hasher` і `fake_save_user` лише демонструють можливий потік даних і, звісно, не забезпечують реальної безпеки.

///

## Зменшення дублювання { #reduce-duplication }

Зменшення дублювання коду - одна з ключових ідей у **FastAPI**.

Адже дублювання коду підвищує ймовірність помилок, проблем безпеки, розсинхронізації коду (коли ви оновлюєте в одному місці, але не в інших) тощо.

І ці моделі спільно використовують багато даних та дублюють назви і типи атрибутів.

Можна зробити краще.

Можна оголосити модель `UserBase`, яка буде базовою для інших моделей. Потім створити підкласи цієї моделі, що наслідуватимуть її атрибути (оголошення типів, валідацію тощо).

Уся конвертація даних, валідація, документація тощо працюватимуть як зазвичай.

Таким чином, ми оголошуємо лише відмінності між моделями (з відкритим `password`, з `hashed_password` і без пароля):

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` або `anyOf` { #union-or-anyof }

Ви можете оголосити відповідь як `Union` двох або більше типів - це означає, що відповідь може бути будь-якого з них.

В OpenAPI це буде визначено як `anyOf`.

Для цього використайте стандартну підказку типу Python <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>:

/// note | Примітка

Під час визначення <a href="https://docs.pydantic.dev/latest/concepts/types/#unions" class="external-link" target="_blank">`Union`</a> спочатку вказуйте найконкретніший тип, а потім менш конкретний. У прикладі нижче більш конкретний `PlaneItem` стоїть перед `CarItem` у `Union[PlaneItem, CarItem]`.

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}

### `Union` у Python 3.10 { #union-in-python-3-10 }

У цьому прикладі ми передаємо `Union[PlaneItem, CarItem]` як значення аргументу `response_model`.

Оскільки ми передаємо його як значення аргументу, а не в анотації типу, потрібно використовувати `Union` навіть у Python 3.10.

Якби це була анотація типу, можна було б використати вертикальну риску, наприклад:

```Python
some_variable: PlaneItem | CarItem
```

Але якщо записати це як присвоєння `response_model=PlaneItem | CarItem`, отримаємо помилку, тому що Python спробує виконати невалідну операцію між `PlaneItem` і `CarItem`, замість того щоб трактувати це як анотацію типу.

## Список моделей { #list-of-models }

Аналогічно можна оголошувати відповіді як списки об’єктів.

Для цього використайте стандартний Python `list`:

{* ../../docs_src/extra_models/tutorial004_py310.py hl[18] *}

## Відповідь з довільним `dict` { #response-with-arbitrary-dict }

Також можна оголосити відповідь, використовуючи звичайний довільний `dict`, вказавши лише типи ключів і значень, без моделі Pydantic.

Це корисно, якщо ви заздалегідь не знаєте допустимі назви полів/атрибутів (які були б потрібні для моделі Pydantic).

У такому разі можна використати `dict`:

{* ../../docs_src/extra_models/tutorial005_py310.py hl[6] *}

## Підсумок { #recap }

Використовуйте кілька моделей Pydantic і вільно наслідуйте для кожного випадку.

Не обов’язково мати одну модель даних на сутність, якщо ця сутність може мати різні «стани». Як у випадку сутності користувача зі станами: з `password`, з `password_hash` і без пароля.
