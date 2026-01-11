# Додаткові моделі { #extra-models }

Продовжуючи попередній приклад, зазвичай буде потрібно мати більше ніж одну пов’язану модель.

Особливо це стосується моделей користувача, тому що:

* **Вхідна модель** має мати можливість містити пароль.
* **Вихідна модель** не повинна містити пароль.
* **Модель бази даних** імовірно має містити хешований пароль.

/// danger | Обережно

Ніколи не зберігайте пароль користувача у відкритому вигляді. Завжди зберігайте «безпечний хеш», який потім можна перевірити.

Якщо ви не знаєте, що таке «хеш пароля», ви дізнаєтесь про це в [розділах про безпеку](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}.

///

## Кілька моделей { #multiple-models }

Ось загальна ідея того, як можуть виглядати моделі з їхніми полями пароля та місцями, де вони використовуються:

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

### Про `**user_in.model_dump()` { #about-user-in-model-dump }

#### `.model_dump()` у Pydantic { #pydantics-model-dump }

`user_in` — це Pydantic-модель класу `UserIn`.

Pydantic-моделі мають метод `.model_dump()`, який повертає `dict` з даними моделі.

Отже, якщо ми створимо Pydantic-об’єкт `user_in`, як:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

а потім викличемо:

```Python
user_dict = user_in.model_dump()
```

то отримаємо `dict` з даними у змінній `user_dict` (це `dict`, а не об’єкт Pydantic-моделі).

І якщо викликати:

```Python
print(user_dict)
```

ми отримаємо Python `dict` із:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### Розпакування `dict` { #unpacking-a-dict }

Якщо взяти `dict`, як-от `user_dict`, і передати його у функцію (або клас) через `**user_dict`, Python «розпакує» його. Він передасть ключі й значення `user_dict` безпосередньо як іменовані аргументи ключ-значення.

Отже, продовжуючи з `user_dict` вище, запис:

```Python
UserInDB(**user_dict)
```

дасть результат, еквівалентний:

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

Або, точніше, використовуючи `user_dict` напряму з будь-яким вмістом, який він може мати в майбутньому:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### Pydantic-модель із вмісту іншої { #a-pydantic-model-from-the-contents-of-another }

Як у прикладі вище, ми отримали `user_dict` з `user_in.model_dump()`, цей код:

```Python
user_dict = user_in.model_dump()
UserInDB(**user_dict)
```

буде еквівалентним:

```Python
UserInDB(**user_in.model_dump())
```

...тому що `user_in.model_dump()` — це `dict`, а потім ми змушуємо Python «розпакувати» його, передаючи в `UserInDB` з префіксом `**`.

Таким чином, ми отримуємо Pydantic-модель з даних іншої Pydantic-моделі.

#### Розпакування `dict` і додаткові ключові слова { #unpacking-a-dict-and-extra-keywords }

А потім, додаючи додатковий іменований аргумент `hashed_password=hashed_password`, як у:

```Python
UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
```

...у підсумку це буде як:

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

Допоміжні додаткові функції `fake_password_hasher` і `fake_save_user` потрібні лише для демонстрації можливого потоку даних, але, звісно, не забезпечують жодної реальної безпеки.

///

## Зменшення дублювання { #reduce-duplication }

Зменшення дублювання коду — одна з ключових ідей **FastAPI**.

Адже дублювання коду збільшує ймовірність багів, проблем безпеки, розсинхронізації коду (коли ви оновлюєте в одному місці, але не в інших) тощо.

І всі ці моделі мають багато спільних даних та дублюють назви атрибутів і типи.

Можна зробити краще.

Ми можемо оголосити модель `UserBase`, що слугуватиме базою для інших моделей. А потім створити підкласи цієї моделі, які успадковуватимуть її атрибути (оголошення типів, валідацію тощо).

Усі перетворення даних, валідація, документація тощо й надалі працюватимуть як зазвичай.

Таким чином, ми зможемо оголошувати лише відмінності між моделями (з відкритим `password`, з `hashed_password` і без пароля):

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` або `anyOf` { #union-or-anyof }

Ви можете оголосити відповідь як `Union` з двох або більше типів, тобто відповідь може бути будь-яким із них.

У OpenAPI це буде визначено як `anyOf`.

Для цього використовуйте стандартну підказку типів Python <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>:

/// note | Примітка

Під час визначення <a href="https://docs.pydantic.dev/latest/concepts/types/#unions" class="external-link" target="_blank">`Union`</a> спочатку вказуйте найбільш специфічний тип, а потім менш специфічний. У прикладі нижче більш специфічний `PlaneItem` іде перед `CarItem` у `Union[PlaneItem, CarItem]`.

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}

### `Union` у Python 3.10 { #union-in-python-3-10 }

У цьому прикладі ми передаємо `Union[PlaneItem, CarItem]` як значення аргументу `response_model`.

Оскільки ми передаємо це як **значення аргументу**, а не розміщуємо у **типовій анотації**, нам потрібно використовувати `Union` навіть у Python 3.10.

Якби це було в типовій анотації, ми могли б використати вертикальну риску:

```Python
some_variable: PlaneItem | CarItem
```

Але якщо записати це в присвоєнні `response_model=PlaneItem | CarItem`, ми отримаємо помилку, тому що Python спробує виконати **некоректну операцію** між `PlaneItem` і `CarItem`, замість того щоб інтерпретувати це як типову анотацію.

## Список моделей { #list-of-models }

Так само ви можете оголошувати відповіді як списки об’єктів.

Для цього використовуйте стандартний Python `typing.List` (або просто `list` у Python 3.9 і вище):

{* ../../docs_src/extra_models/tutorial004_py39.py hl[18] *}

## Відповідь із довільним `dict` { #response-with-arbitrary-dict }

Ви також можете оголосити відповідь, використовуючи звичайний довільний `dict`, вказавши лише тип ключів і значень, без використання Pydantic-моделі.

Це корисно, якщо ви заздалегідь не знаєте коректні назви полів/атрибутів (які були б потрібні для Pydantic-моделі).

У цьому випадку можна використати `typing.Dict` (або просто `dict` у Python 3.9 і вище):

{* ../../docs_src/extra_models/tutorial005_py39.py hl[6] *}

## Підсумок { #recap }

Використовуйте кілька Pydantic-моделей і вільно застосовуйте успадкування для кожного випадку.

Вам не потрібно мати одну-єдину модель даних на сутність, якщо ця сутність може мати різні «стани». Як у випадку з «сутністю» користувача зі станом, що включає `password`, `password_hash` і без пароля.
