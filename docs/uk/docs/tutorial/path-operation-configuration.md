# Налаштування операції шляху { #path-operation-configuration }

Є кілька параметрів, які ви можете передати вашому «декоратору операції шляху» для налаштування.

/// warning | Попередження

Зверніть увагу, що ці параметри передаються безпосередньо «декоратору операції шляху», а не вашій «функції операції шляху».

///

## Код статусу відповіді { #response-status-code }

Ви можете визначити (HTTP) `status_code`, який буде використано у відповіді вашої «операції шляху».

Можна передати безпосередньо цілий код, наприклад `404`.

Якщо ви не пам'ятаєте призначення числових кодів, скористайтеся скороченими константами в `status`:

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

Цей код статусу буде використано у відповіді та додано до схеми OpenAPI.

/// note | Технічні деталі

Ви також можете використати `from starlette import status`.

FastAPI надає той самий `starlette.status` як `fastapi.status` для вашої зручності як розробника. Але він походить безпосередньо зі Starlette.

///

## Мітки { #tags }

Ви можете додати мітки до вашої «операції шляху», передайте параметр `tags` зі `list` із `str` (зазвичай лише один `str`):

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

Вони будуть додані до схеми OpenAPI та використані інтерфейсами автоматичної документації:

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Мітки з переліками { #tags-with-enums }

У великому застосунку ви можете накопичити багато міток і захочете переконатися, що завжди використовуєте ту саму мітку для пов'язаних «операцій шляху».

У таких випадках має сенс зберігати мітки в `Enum`.

FastAPI підтримує це так само, як і зі звичайними строками:

{* ../../docs_src/path_operation_configuration/tutorial002b_py310.py hl[1,8:10,13,18] *}

## Короткий опис і опис { #summary-and-description }

Ви можете додати `summary` і `description`:

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[17:18] *}

## Опис зі строки документації { #description-from-docstring }

Оскільки описи зазвичай довгі та займають кілька рядків, ви можете оголосити опис «операції шляху» у <dfn title="багаторядкова строка як перший вираз усередині функції (не прив'язаний до жодної змінної), використовується для документації">строці документації</dfn> функції, і FastAPI прочитає його звідти.

Ви можете писати <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a> у строці документації, його буде інтерпретовано та показано коректно (з урахуванням відступів у строці документації).

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

Його буде використано в інтерактивній документації:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## Опис відповіді { #response-description }

Ви можете вказати опис відповіді параметром `response_description`:

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[18] *}

/// info | Інформація

Зверніть увагу, що `response_description` стосується саме відповіді, а `description` стосується «операції шляху» загалом.

///

/// check | Перевірте

OpenAPI визначає, що кожна «операція шляху» потребує опису відповіді.

Тому, якщо ви його не надасте, FastAPI автоматично згенерує «Successful response».

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## Позначити операцію шляху як застарілу { #deprecate-a-path-operation }

Якщо потрібно позначити «операцію шляху» як <dfn title="застарілий, не рекомендується використовувати">застарілу</dfn>, але не видаляючи її, передайте параметр `deprecated`:

{* ../../docs_src/path_operation_configuration/tutorial006_py310.py hl[16] *}

У інтерактивній документації вона буде чітко позначена як застаріла:

<img src="/img/tutorial/path-operation-configuration/image04.png">

Подивіться, як виглядають застарілі та незастарілі «операції шляху»:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## Підсумок { #recap }

Ви можете легко налаштовувати та додавати метадані до ваших «операцій шляху», передаючи параметри «декораторам операцій шляху».
