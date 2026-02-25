# Розширення OpenAPI { #extending-openapi }

У деяких випадках вам може знадобитися змінити згенеровану схему OpenAPI.

У цьому розділі ви побачите як це зробити.

## Звичайний процес { #the-normal-process }

Звичайний (типовий) процес такий.

Застосунок `FastAPI` (екземпляр) має метод `.openapi()`, який має повертати схему OpenAPI.

Під час створення об'єкта застосунку реєструється *операція шляху* для `/openapi.json` (або для того значення, яке ви встановили в `openapi_url`).

Вона просто повертає відповідь JSON з результатом методу `.openapi()` застосунку.

Типово метод `.openapi()` перевіряє властивість `.openapi_schema`, і якщо там вже є дані, повертає їх.

Якщо ні, він генерує їх за допомогою утилітарної функції `fastapi.openapi.utils.get_openapi`.

Функція `get_openapi()` приймає такі параметри:

- `title`: Заголовок OpenAPI, показується в документації.
- `version`: Версія вашого API, напр. `2.5.0`.
- `openapi_version`: Версія специфікації OpenAPI, що використовується. Типово остання: `3.1.0`.
- `summary`: Короткий підсумок API.
- `description`: Опис вашого API; може містити markdown і буде показаний у документації.
- `routes`: Список маршрутів, це кожна з зареєстрованих *операцій шляху*. Їх беруть з `app.routes`.

/// info | Інформація

Параметр `summary` доступний в OpenAPI 3.1.0 і вище, підтримується FastAPI 0.99.0 і вище.

///

## Переписування типових значень { #overriding-the-defaults }

Використовуючи наведене вище, ви можете скористатися тією ж утилітарною функцією для генерації схеми OpenAPI і переписати потрібні частини.

Наприклад, додаймо <a href="https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo" class="external-link" target="_blank">розширення OpenAPI для ReDoc для додавання власного логотипа</a>.

### Звичайний **FastAPI** { #normal-fastapi }

Спочатку напишіть ваш застосунок **FastAPI** як зазвичай:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[1,4,7:9] *}

### Згенерувати схему OpenAPI { #generate-the-openapi-schema }

Далі використайте ту ж утилітарну функцію для генерації схеми OpenAPI всередині функції `custom_openapi()`:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[2,15:21] *}

### Змінити схему OpenAPI { #modify-the-openapi-schema }

Тепер можна додати розширення ReDoc, додавши власний `x-logo` до «об'єкта» `info` у схемі OpenAPI:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[22:24] *}

### Кешувати схему OpenAPI { #cache-the-openapi-schema }

Ви можете використовувати властивість `.openapi_schema` як «кеш» для збереження згенерованої схеми.

Так вашому застосунку не доведеться щоразу генерувати схему, коли користувач відкриває документацію вашого API.

Вона буде згенерована лише один раз, а потім та сама закешована схема використовуватиметься для наступних запитів.

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[13:14,25:26] *}

### Переписати метод { #override-the-method }

Тепер ви можете замінити метод `.openapi()` вашою новою функцією.

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[29] *}

### Перевірте { #check-it }

Коли ви перейдете за адресою <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>, побачите, що використовується ваш власний логотип (у цьому прикладі логотип **FastAPI**):

<img src="/img/tutorial/extending-openapi/image01.png">
