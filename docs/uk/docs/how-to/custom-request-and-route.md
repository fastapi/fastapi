# Власні класи Request і APIRoute { #custom-request-and-apiroute-class }

У деяких випадках ви можете захотіти перевизначити логіку, яку використовують класи `Request` і `APIRoute`.

Зокрема, це може бути хорошою альтернативою логіці в middleware.

Наприклад, якщо ви хочете прочитати або змінити тіло запиту до того, як його обробить ваш застосунок.

/// danger | Обережно

Це «просунута» можливість.

Якщо ви лише починаєте працювати з **FastAPI**, вам, імовірно, варто пропустити цей розділ.

///

## Випадки використання { #use-cases }

Деякі випадки використання:

* Перетворення не-JSON тіл запитів на JSON (наприклад, <a href="https://msgpack.org/index.html" class="external-link" target="_blank">`msgpack`</a>).
* Розпаковування gzip-стиснених тіл запитів.
* Автоматичне логування всіх тіл запитів.

## Обробка власних кодувань тіла запиту { #handling-custom-request-body-encodings }

Розгляньмо, як використати власний підклас `Request`, щоб розпаковувати gzip-запити.

А також підклас `APIRoute`, щоб використовувати цей власний клас запиту.

### Створіть власний клас `GzipRequest` { #create-a-custom-gziprequest-class }

/// tip | Порада

Це навчальний приклад, щоб продемонструвати, як це працює. Якщо вам потрібна підтримка Gzip, ви можете використати наданий [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware){.internal-link target=_blank}.

///

Спочатку створюємо клас `GzipRequest`, який перевизначить метод `Request.body()`, щоб розпаковувати тіло за наявності відповідного заголовка.

Якщо в заголовку немає `gzip`, він не намагатиметься розпаковувати тіло.

Так один і той самий клас маршруту може обробляти як gzip-стиснені, так і нестиснені запити.

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[9:16] *}

### Створіть власний клас `GzipRoute` { #create-a-custom-gziproute-class }

Далі створюємо власний підклас `fastapi.routing.APIRoute`, який використовуватиме `GzipRequest`.

Цього разу він перевизначить метод `APIRoute.get_route_handler()`.

Цей метод повертає функцію. І саме ця функція отримуватиме запит і повертатиме відповідь.

Тут ми використовуємо її, щоб створити `GzipRequest` з початкового запиту.

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[19:27] *}

/// note | Технічні деталі

`Request` має атрибут `request.scope` — це просто Python-`dict`, що містить метадані, пов’язані із запитом.

`Request` також має `request.receive` — це функція для «отримання» тіла запиту.

`dict` `scope` і функція `receive` обидва є частиною специфікації ASGI.

І саме ці дві речі — `scope` та `receive` — потрібні, щоб створити новий екземпляр `Request`.

Щоб дізнатися більше про `Request`, перегляньте <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">документацію Starlette про Requests</a>.

///

Єдина відмінність у роботі функції, яку повертає `GzipRequest.get_route_handler`, — це перетворення `Request` на `GzipRequest`.

Завдяки цьому наш `GzipRequest` подбає про розпаковування даних (за потреби) перед тим, як передати їх у наші *операції шляху*.

Після цього вся логіка обробки залишається тією самою.

Але через наші зміни в `GzipRequest.body` тіло запиту буде автоматично розпаковане, коли **FastAPI** завантажуватиме його за потреби.

## Доступ до тіла запиту в обробнику винятків { #accessing-the-request-body-in-an-exception-handler }

/// tip | Порада

Щоб розв’язати цю саму задачу, ймовірно, значно простіше використати `body` у власному обробнику для `RequestValidationError` ([Обробка помилок](../tutorial/handling-errors.md#use-the-requestvalidationerror-body){.internal-link target=_blank}).

Але цей приклад усе одно коректний і показує, як взаємодіяти з внутрішніми компонентами.

///

Ми також можемо використати цей самий підхід, щоб отримати доступ до тіла запиту в обробнику винятків.

Усе, що потрібно зробити, — обробляти запит усередині блоку `try`/`except`:

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[14,16] *}

Якщо станеться виняток, екземпляр `Request` усе ще буде в області видимості, тож ми зможемо прочитати та використати тіло запиту під час обробки помилки:

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[17:19] *}

## Власний клас `APIRoute` у router { #custom-apiroute-class-in-a-router }

Ви також можете встановити параметр `route_class` для `APIRouter`:

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[26] *}

У цьому прикладі *операції шляху* під `router` використовуватимуть власний клас `TimedRoute` і матимуть додатковий заголовок `X-Response-Time` у відповіді з часом, який знадобився для генерування відповіді:

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[13:20] *}
