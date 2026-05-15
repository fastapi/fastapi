# Більші застосунки - кілька файлів { #bigger-applications-multiple-files }

Якщо ви створюєте застосунок або веб-API, рідко вдається вмістити все в один файл.

**FastAPI** надає зручний інструмент для структурування вашого застосунку, зберігаючи всю гнучкість.

/// info | Інформація

Якщо ви прийшли з Flask, це еквівалент «Blueprints» у Flask.

///

## Приклад структури файлів { #an-example-file-structure }

Припустімо, у вас така структура файлів:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

/// tip | Порада

Тут кілька файлів `__init__.py`: по одному в кожному каталозі та підкаталозі.

Саме це дозволяє імпортувати код з одного файлу в інший.

Наприклад, у `app/main.py` ви можете мати рядок:

```
from app.routers import items
```

///

* Каталог `app` містить усе. І він має порожній файл `app/__init__.py`, тож це «пакет Python» (збірка «модулів Python»): `app`.
* Він містить файл `app/main.py`. Оскільки він усередині пакета Python (каталог з файлом `__init__.py`), це «модуль» цього пакета: `app.main`.
* Є також файл `app/dependencies.py`, так само як `app/main.py`, це «модуль»: `app.dependencies`.
* Є підкаталог `app/routers/` з іншим файлом `__init__.py`, отже це «підпакет Python»: `app.routers`.
* Файл `app/routers/items.py` знаходиться в пакеті `app/routers/`, отже це підмодуль: `app.routers.items`.
* Так само і `app/routers/users.py`, це інший підмодуль: `app.routers.users`.
* Є також підкаталог `app/internal/` з іншим файлом `__init__.py`, отже це інший «підпакет Python»: `app.internal`.
* І файл `app/internal/admin.py` - ще один підмодуль: `app.internal.admin`.

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

Та сама структура файлів з коментарями:

```bash
.
├── app                  # «app» - це пакет Python
│   ├── __init__.py      # цей файл робить «app» «пакетом Python»
│   ├── main.py          # модуль «main», напр. import app.main
│   ├── dependencies.py  # модуль «dependencies», напр. import app.dependencies
│   └── routers          # «routers» - це «підпакет Python»
│   │   ├── __init__.py  # робить «routers» «підпакетом Python»
│   │   ├── items.py     # підмодуль «items», напр. import app.routers.items
│   │   └── users.py     # підмодуль «users», напр. import app.routers.users
│   └── internal         # «internal» - це «підпакет Python»
│       ├── __init__.py  # робить «internal» «підпакетом Python»
│       └── admin.py     # підмодуль «admin», напр. import app.internal.admin
```

## `APIRouter` { #apirouter }

Припустімо, файл, присвячений обробці лише користувачів, - це підмодуль у `/app/routers/users.py`.

Ви хочете мати *операції шляху*, пов'язані з користувачами, відокремлено від решти коду, щоб зберегти порядок.

Але це все одно частина того самого застосунку/веб-API **FastAPI** (це частина того самого «пакета Python»).

Ви можете створювати *операції шляху* для цього модуля, використовуючи `APIRouter`.

### Імпортуйте `APIRouter` { #import-apirouter }

Імпортуйте його та створіть «екземпляр» так само, як ви б робили з класом `FastAPI`:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[1,3] title["app/routers/users.py"] *}

### *Операції шляху* з `APIRouter` { #path-operations-with-apirouter }

Потім використовуйте його для оголошення *операцій шляху*.

Використовуйте його так само, як і клас `FastAPI`:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[6,11,16] title["app/routers/users.py"] *}

Можете думати про `APIRouter` як про «міні `FastAPI`».

Підтримуються ті самі опції.

Ті самі `parameters`, `responses`, `dependencies`, `tags` тощо.

/// tip | Порада

У цьому прикладі змінна називається `router`, але ви можете назвати її як завгодно.

///

Ми включимо цей `APIRouter` у основний застосунок `FastAPI`, але спочатку розгляньмо залежності та інший `APIRouter`.

## Залежності { #dependencies }

Бачимо, що нам знадобляться кілька залежностей, які використовуються в різних місцях застосунку.

Тож помістимо їх у власний модуль `dependencies` (`app/dependencies.py`).

Тепер використаємо просту залежність для читання користувацького заголовка `X-Token`:

{* ../../docs_src/bigger_applications/app_an_py310/dependencies.py hl[3,6:8] title["app/dependencies.py"] *}

/// tip | Порада

Ми використовуємо вигаданий заголовок, щоб спростити приклад.

Але в реальних випадках ви отримаєте кращі результати, використовуючи інтегровані [засоби безпеки](security/index.md).

///

## Інший модуль з `APIRouter` { #another-module-with-apirouter }

Припустімо, у вас також є кінцеві точки для обробки «items» у модулі `app/routers/items.py`.

У вас є *операції шляху* для:

* `/items/`
* `/items/{item_id}`

Структура така сама, як у `app/routers/users.py`.

Але ми хочемо бути розумнішими й трохи спростити код.

Ми знаємо, що всі *операції шляху* в цьому модулі мають однакові:

* Префікс шляху `prefix`: `/items`.
* `tags`: (лише одна мітка: `items`).
* Додаткові `responses`.
* `dependencies`: усім потрібна залежність `X-Token`, яку ми створили.

Тож замість додавання цього до кожної *операції шляху*, ми можемо додати це до `APIRouter`.

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[5:10,16,21] title["app/routers/items.py"] *}

Оскільки шлях кожної *операції шляху* має починатися з `/`, як у:

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...префікс не має містити кінцевий `/`.

Отже, у цьому випадку префікс - це `/items`.

Ми також можемо додати список `tags` та додаткові `responses`, які застосовуватимуться до всіх *операцій шляху*, включених у цей router.

І ми можемо додати список `dependencies`, які буде додано до всіх *операцій шляху* у router і які виконуватимуться/вирішуватимуться для кожного запиту до них.

/// tip | Порада

Зверніть увагу, що так само як і для [залежностей у декораторах *операцій шляху*](dependencies/dependencies-in-path-operation-decorators.md), жодне значення не буде передано вашій *функції операції шляху*.

///

У підсумку шляхи предметів тепер:

* `/items/`
* `/items/{item_id}`

...як ми і планували.

* Вони будуть позначені списком міток, що містить один рядок `"items"`.
    * Ці «мітки» особливо корисні для автоматичної інтерактивної документації (за допомогою OpenAPI).
* Усі вони включатимуть наперед визначені `responses`.
* Для всіх цих *операцій шляху* список `dependencies` буде оцінений/виконаний перед ними.
    * Якщо ви також оголосите залежності в конкретній *операції шляху*, **вони також будуть виконані**.
    * Спочатку виконуються залежності router'а, потім [`dependencies` у декораторі](dependencies/dependencies-in-path-operation-decorators.md), а потім звичайні параметричні залежності.
    * Ви також можете додати [`Security` залежності з `scopes`](../advanced/security/oauth2-scopes.md).

/// tip | Порада

Наявність `dependencies` у `APIRouter` можна використати, наприклад, щоб вимагати автентифікацію для всієї групи *операцій шляху*. Навіть якщо залежності не додані до кожної з них окремо.

///

/// check | Перевірте

Параметри `prefix`, `tags`, `responses` і `dependencies` - це (як і в багатьох інших випадках) просто можливість **FastAPI**, яка допомагає уникати дублювання коду.

///

### Імпортуйте залежності { #import-the-dependencies }

Цей код живе в модулі `app.routers.items`, у файлі `app/routers/items.py`.

І нам потрібно отримати функцію залежності з модуля `app.dependencies`, файлу `app/dependencies.py`.

Тож ми використовуємо відносний імпорт з `..` для залежностей:

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[3] title["app/routers/items.py"] *}

#### Як працюють відносні імпорти { #how-relative-imports-work }

/// tip | Порада

Якщо ви досконало знаєте, як працюють імпорти, перейдіть до наступного розділу нижче.

///

Одна крапка `.`, як у:

```Python
from .dependencies import get_token_header
```

означає:

* Починаючи в тому самому пакеті, де знаходиться цей модуль (файл `app/routers/items.py`) (каталог `app/routers/`)...
* знайти модуль `dependencies` (уявний файл `app/routers/dependencies.py`)...
* і з нього імпортувати функцію `get_token_header`.

Але такого файлу не існує, наші залежності у файлі `app/dependencies.py`.

Згадайте, як виглядає структура нашого застосунку/файлів:

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

---

Дві крапки `..`, як у:

```Python
from ..dependencies import get_token_header
```

означають:

* Починаючи в тому самому пакеті, де знаходиться цей модуль (файл `app/routers/items.py`) (каталог `app/routers/`)...
* перейти до батьківського пакета (каталог `app/`)...
* і там знайти модуль `dependencies` (файл `app/dependencies.py`)...
* і з нього імпортувати функцію `get_token_header`.

Це працює правильно! 🎉

---

Так само, якби ми використали три крапки `...`, як у:

```Python
from ...dependencies import get_token_header
```

це б означало:

* Починаючи в тому самому пакеті, де знаходиться цей модуль (файл `app/routers/items.py`) (каталог `app/routers/`)...
* перейти до батьківського пакета (каталог `app/`)...
* потім перейти до батьківського пакета від того (немає батьківського пакета, `app` - верхній рівень 😱)...
* і там знайти модуль `dependencies` (файл `app/dependencies.py`)...
* і з нього імпортувати функцію `get_token_header`.

Це б посилалося на якийсь пакет вище за `app/` з власним файлом `__init__.py` тощо. Але в нас такого немає. Тож у нашому прикладі це спричинить помилку. 🚨

Але тепер ви знаєте, як це працює, тож можете використовувати відносні імпорти у власних застосунках, незалежно від їхньої складності. 🤓

### Додайте користувацькі `tags`, `responses` і `dependencies` { #add-some-custom-tags-responses-and-dependencies }

Ми не додаємо префікс `/items` ані `tags=["items"]` до кожної *операції шляху*, бо додали їх до `APIRouter`.

Але ми все ще можемо додати _ще_ `tags`, які будуть застосовані до конкретної *операції шляху*, а також додаткові `responses`, специфічні для цієї *операції шляху*:

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[30:31] title["app/routers/items.py"] *}

/// tip | Порада

Остання операція шляху матиме комбінацію міток: `["items", "custom"]`.

І вона також матиме в документації обидві відповіді: одну для `404` і одну для `403`.

///

## Основний `FastAPI` { #the-main-fastapi }

Тепер розгляньмо модуль `app/main.py`.

Тут ви імпортуєте і використовуєте клас `FastAPI`.

Це буде головний файл вашого застосунку, який усе поєднує.

І оскільки більшість вашої логіки тепер житиме у власних модулях, головний файл буде досить простим.

### Імпортуйте `FastAPI` { #import-fastapi }

Імпортуйте та створіть клас `FastAPI`, як зазвичай.

І ми навіть можемо оголосити [глобальні залежності](dependencies/global-dependencies.md), які будуть поєднані із залежностями кожного `APIRouter`:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[1,3,7] title["app/main.py"] *}

### Імпортуйте `APIRouter` { #import-the-apirouter }

Тепер імпортуємо інші підмодулі, що мають `APIRouter`:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[4:5] title["app/main.py"] *}

Оскільки файли `app/routers/users.py` та `app/routers/items.py` - це підмодулі, що є частиною того самого пакета Python `app`, ми можемо використати одну крапку `.` для «відносних імпортів».

### Як працює імпорт { #how-the-importing-works }

Розділ:

```Python
from .routers import items, users
```

означає:

* Починаючи в тому самому пакеті, де знаходиться цей модуль (файл `app/main.py`) (каталог `app/`)...
* знайти підпакет `routers` (каталог `app/routers/`)...
* і з нього імпортувати підмодулі `items` (файл `app/routers/items.py`) і `users` (файл `app/routers/users.py`)...

Модуль `items` матиме змінну `router` (`items.router`). Це та сама, що ми створили у файлі `app/routers/items.py`, це об’єкт `APIRouter`.

Потім ми робимо те саме для модуля `users`.

Ми також могли б імпортувати їх так:

```Python
from app.routers import items, users
```

/// info | Інформація

Перша версія - «відносний імпорт»:

```Python
from .routers import items, users
```

Друга версія - «абсолютний імпорт»:

```Python
from app.routers import items, users
```

Щоб дізнатися більше про пакети й модулі Python, прочитайте [офіційну документацію Python про модулі](https://docs.python.org/3/tutorial/modules.html).

///

### Уникайте колізій імен { #avoid-name-collisions }

Ми імпортуємо підмодуль `items` напряму, замість імпорту лише його змінної `router`.

Це тому, що в підмодулі `users` також є змінна з назвою `router`.

Якби ми імпортували один за одним, як:

```Python
from .routers.items import router
from .routers.users import router
```

`router` з `users` перезаписав би той, що з `items`, і ми не змогли б використовувати їх одночасно.

Щоб мати змогу використовувати обидва в одному файлі, ми імпортуємо підмодулі напряму:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[5] title["app/main.py"] *}

### Додайте `APIRouter` для `users` і `items` { #include-the-apirouters-for-users-and-items }

Тепер додаймо `router` з підмодулів `users` і `items`:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[10:11] title["app/main.py"] *}

/// info | Інформація

`users.router` містить `APIRouter` у файлі `app/routers/users.py`.

А `items.router` містить `APIRouter` у файлі `app/routers/items.py`.

///

За допомогою `app.include_router()` ми можемо додати кожен `APIRouter` до основного застосунку `FastAPI`.

Це включить усі маршрути з цього router'а як частину застосунку.

/// note | Технічні деталі

Фактично, всередині для кожної *операції шляху*, оголошеної в `APIRouter`, буде створена окрема *операція шляху*.

Тобто за лаштунками все працюватиме так, ніби це один і той самий застосунок.

///

/// check | Перевірте

Вам не потрібно перейматися продуктивністю під час включення router'ів.

Це займе мікросекунди і відбуватиметься лише під час запуску.

Тож це не вплине на продуктивність. ⚡

///

### Додайте `APIRouter` з власними `prefix`, `tags`, `responses` і `dependencies` { #include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies }

Уявімо, що ваша організація надала вам файл `app/internal/admin.py`.

Він містить `APIRouter` з кількома адміністративними *операціями шляху*, які організація спільно використовує між кількома проєктами.

Для цього прикладу він буде дуже простим. Але припустімо, що оскільки його спільно використовують з іншими проєктами організації, ми не можемо модифікувати його та додавати `prefix`, `dependencies`, `tags` тощо прямо до `APIRouter`:

{* ../../docs_src/bigger_applications/app_an_py310/internal/admin.py hl[3] title["app/internal/admin.py"] *}

Але ми все одно хочемо встановити користувацький `prefix` під час включення `APIRouter`, щоб усі його *операції шляху* починалися з `/admin`, хочемо захистити його за допомогою `dependencies`, які вже є в цьому проєкті, і хочемо додати `tags` та `responses`.

Ми можемо оголосити все це, не змінюючи оригінальний `APIRouter`, передавши ці параметри до `app.include_router()`:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[14:17] title["app/main.py"] *}

Таким чином, вихідний `APIRouter` залишиться без змін, тож ми все ще зможемо спільно використовувати той самий файл `app/internal/admin.py` з іншими проєктами в організації.

У результаті в нашому застосунку кожна з *операцій шляху* з модуля `admin` матиме:

* Префікс `/admin`.
* Мітку `admin`.
* Залежність `get_token_header`.
* Відповідь `418`. 🍵

Але це вплине лише на цей `APIRouter` у нашому застосунку, а не на будь-який інший код, який його використовує.

Наприклад, інші проєкти можуть використовувати той самий `APIRouter` з іншим методом автентифікації.

### Додайте *операцію шляху* { #include-a-path-operation }

Ми також можемо додавати *операції шляху* безпосередньо до застосунку `FastAPI`.

Тут ми це робимо... просто щоб показати, що так можна 🤷:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[21:23] title["app/main.py"] *}

і це працюватиме коректно разом з усіма іншими *операціями шляху*, доданими через `app.include_router()`.

/// info | Дуже технічні деталі

Примітка: це дуже технічна деталь, яку ви, ймовірно, можете просто пропустити.

---

`APIRouter` не «монтуються», вони не ізольовані від решти застосунку.

Це тому, що ми хочемо включати їхні *операції шляху* в схему OpenAPI та інтерфейси користувача.

Оскільки ми не можемо просто ізолювати їх і «змонтувати» незалежно від решти, *операції шляху* «клонуються» (створюються заново), а не включаються безпосередньо.

///

## Налаштуйте `entrypoint` у `pyproject.toml` { #configure-the-entrypoint-in-pyproject-toml }

Оскільки ваш об'єкт FastAPI `app` знаходиться в `app/main.py`, ви можете налаштувати `entrypoint` у файлі `pyproject.toml` так:

```toml
[tool.fastapi]
entrypoint = "app.main:app"
```

це еквівалентно імпорту:

```python
from app.main import app
```

Таким чином команда `fastapi` знатиме, де знайти ваш застосунок.

/// Note | Примітка

Ви також могли б передати шлях команді, наприклад:

```console
$ fastapi dev app/main.py
```

Але тоді вам доведеться щоразу пам'ятати, щоб передавати правильний шлях, коли ви викликаєте команду `fastapi`.

Крім того, інші інструменти можуть не знайти його, наприклад [розширення VS Code](../editor-support.md) або [FastAPI Cloud](https://fastapicloud.com), тому рекомендовано використовувати `entrypoint` у `pyproject.toml`.

///

## Перевірте автоматичну документацію API { #check-the-automatic-api-docs }

Тепер запустіть ваш застосунок:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

І відкрийте документацію за адресою [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Ви побачите автоматичну документацію API, що включає шляхи з усіх підмодулів, з правильними шляхами (і префіксами) та правильними мітками:

<img src="/img/tutorial/bigger-applications/image01.png">

## Включайте той самий router кілька разів з різними `prefix` { #include-the-same-router-multiple-times-with-different-prefix }

Ви також можете використовувати `.include_router()` кілька разів з одним і тим самим router'ом, але з різними префіксами.

Це може бути корисно, наприклад, щоб публікувати той самий API під різними префіксами, наприклад `/api/v1` і `/api/latest`.

Це просунуте використання, яке вам може й не знадобитися, але воно є на випадок, якщо потрібно.

## Включіть один `APIRouter` до іншого { #include-an-apirouter-in-another }

Так само як ви можете включити `APIRouter` у застосунок `FastAPI`, ви можете включити `APIRouter` в інший `APIRouter`, використовуючи:

```Python
router.include_router(other_router)
```

Переконайтеся, що ви робите це до включення `router` в застосунок `FastAPI`, щоб *операції шляху* з `other_router` також були включені.
