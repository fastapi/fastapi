# Налаштування операції шляху { #path-operation-configuration }

Є кілька параметрів, які ви можете передати вашому *декоратору операції шляху*, щоб налаштувати його.

/// warning | Попередження

Зверніть увагу, що ці параметри передаються безпосередньо *декоратору операції шляху*, а не вашій *функції операції шляху*.

///

## Код статусу відповіді { #response-status-code }

Ви можете визначити (HTTP) `status_code`, який буде використано у відповіді вашої *операції шляху*.

Ви можете передати безпосередньо код `int`, наприклад `404`.

Але якщо ви не пам’ятаєте, для чого призначений кожен числовий код, можете використати скорочені константи в `status`:

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

Цей код статусу буде використано у відповіді та додано до схеми OpenAPI.

/// note | Технічні деталі

Ви також можете використати `from starlette import status`.

**FastAPI** надає той самий `starlette.status` як `fastapi.status` просто для зручності для вас, розробника. Але він надходить безпосередньо зі Starlette.

///

## Теги { #tags }

Ви можете додати теги до вашої *операції шляху*: передайте параметр `tags` зі значенням `list` із `str` (зазвичай лише один `str`):

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

Їх буде додано до схеми OpenAPI та використано інтерфейсами автоматичної документації:

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Теги з Enum { #tags-with-enums }

Якщо у вас великий застосунок, у вас може накопичитися **кілька тегів**, і ви захочете переконатися, що завжди використовуєте **той самий тег** для пов’язаних *операцій шляху*.

У таких випадках може мати сенс зберігати теги в `Enum`.

**FastAPI** підтримує це так само, як і зі звичайними рядками:

{* ../../docs_src/path_operation_configuration/tutorial002b_py39.py hl[1,8:10,13,18] *}

## Підсумок і опис { #summary-and-description }

Ви можете додати `summary` і `description`:

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[18:19] *}

## Опис із docstring { #description-from-docstring }

Оскільки описи зазвичай довгі та займають кілька рядків, ви можете оголосити опис *операції шляху* у <abbr title="a multi-line string as the first expression inside a function (not assigned to any variable) used for documentation - багаторядковий рядок як перший вираз усередині функції (не присвоєний жодній змінній), який використовується для документації">docstring</abbr> функції, і **FastAPI** прочитає його звідти.

Ви можете писати <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a> у docstring — його буде інтерпретовано та правильно показано (з урахуванням відступів docstring).

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

Це буде використано в інтерактивній документації:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## Опис відповіді { #response-description }

Ви можете вказати опис відповіді за допомогою параметра `response_description`:

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[19] *}

/// info | Інформація

Зверніть увагу, що `response_description` стосується конкретно відповіді, а `description` — *операції шляху* загалом.

///

/// check

OpenAPI визначає, що кожна *операція шляху* потребує опису відповіді.

Тож якщо ви його не надасте, **FastAPI** автоматично згенерує «Successful response».

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## Позначення *операції шляху* як застарілої { #deprecate-a-path-operation }

Якщо вам потрібно позначити *операцію шляху* як <abbr title="obsolete, recommended not to use it - застаріле, рекомендовано не використовувати">deprecated</abbr>, але без її видалення, передайте параметр `deprecated`:

{* ../../docs_src/path_operation_configuration/tutorial006_py39.py hl[16] *}

В інтерактивній документації її буде чітко позначено як застарілу:

<img src="/img/tutorial/path-operation-configuration/image04.png">

Перевірте, як виглядають застарілі й не застарілі *операції шляху*:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## Підсумок { #recap }

Ви можете легко налаштовувати та додавати метадані для ваших *операцій шляху*, передаючи параметри *декораторам операцій шляху*.
