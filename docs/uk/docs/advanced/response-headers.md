# Заголовки відповіді { #response-headers }

## Використовуйте параметр `Response` { #use-a-response-parameter }

Ви можете оголосити параметр типу `Response` у вашій *функції операції шляху* (так само, як і для cookies).

Після цього ви можете встановлювати заголовки в цьому *тимчасовому* об’єкті відповіді.

{* ../../docs_src/response_headers/tutorial002_py39.py hl[1, 7:8] *}

Далі ви можете повертати будь-який потрібний об’єкт, як зазвичай (наприклад, `dict`, модель бази даних тощо).

Якщо ви оголосили `response_model`, він усе одно буде використаний, щоб відфільтрувати та перетворити повернений об’єкт.

**FastAPI** використає цю *тимчасову* відповідь, щоб витягти заголовки (а також cookies і код стану), і додасть їх до фінальної відповіді, що містить значення, яке ви повернули, відфільтроване через `response_model`.

Також ви можете оголосити параметр `Response` у залежностях і встановлювати в них заголовки (та cookies).

## Повертайте `Response` напряму { #return-a-response-directly }

Ви також можете додавати заголовки, коли повертаєте `Response` безпосередньо.

Створіть відповідь, як описано в [Повернути Response напряму](response-directly.md){.internal-link target=_blank}, і передайте заголовки як додатковий параметр:

{* ../../docs_src/response_headers/tutorial001_py39.py hl[10:12] *}

/// note | Технічні деталі

Ви також можете використовувати `from starlette.responses import Response` або `from starlette.responses import JSONResponse`.

**FastAPI** надає ті самі `starlette.responses` як `fastapi.responses` просто для зручності для вас, розробника. Але більшість доступних відповідей надходять безпосередньо зі Starlette.

А оскільки `Response` часто використовується для встановлення заголовків і cookies, **FastAPI** також надає його як `fastapi.Response`.

///

## Користувацькі заголовки { #custom-headers }

Пам’ятайте, що власні пропрієтарні заголовки можна додавати <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">використовуючи префікс `X-`</a>.

Але якщо у вас є користувацькі заголовки, які ви хочете зробити видимими для клієнта в браузері, вам потрібно додати їх у налаштування CORS (докладніше в [CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md){.internal-link target=_blank}), використовуючи параметр `expose_headers`, описаний у <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">документації Starlette про CORS</a>.
