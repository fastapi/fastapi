# Заголовки відповіді { #response-headers }

## Використовуйте параметр `Response` { #use-a-response-parameter }

Ви можете оголосити параметр типу `Response` у вашій функції операції шляху (так само, як і для кукі).

Потім ви можете встановлювати заголовки в цьому *тимчасовому* обʼєкті відповіді.

{* ../../docs_src/response_headers/tutorial002_py310.py hl[1, 7:8] *}

Далі ви можете повернути будь-який потрібний обʼєкт, як зазвичай (наприклад, `dict`, модель бази даних тощо).

Якщо ви оголосили `response_model`, його все одно буде використано для фільтрації та перетворення поверненого обʼєкта.

FastAPI використає цей *тимчасовий* обʼєкт відповіді, щоб витягти заголовки (а також кукі та код статусу) і помістить їх у кінцеву відповідь, яка міститиме повернуте вами значення, відфільтроване будь-яким `response_model`.

Також ви можете оголосити параметр `Response` у залежностях і встановлювати в них заголовки (та кукі).

## Поверніть `Response` безпосередньо { #return-a-response-directly }

Ви також можете додавати заголовки, коли повертаєте `Response` безпосередньо.

Створіть відповідь, як описано в [Повернення Response безпосередньо](response-directly.md){.internal-link target=_blank}, і передайте заголовки як додатковий параметр:

{* ../../docs_src/response_headers/tutorial001_py310.py hl[10:12] *}

/// note | Технічні деталі

Ви також можете використати `from starlette.responses import Response` або `from starlette.responses import JSONResponse`.

FastAPI надає ті самі `starlette.responses` як `fastapi.responses` просто для зручності для вас, розробника. Але більшість доступних типів відповідей походять безпосередньо зі Starlette.

Оскільки `Response` часто використовують для встановлення заголовків і кукі, FastAPI також надає його як `fastapi.Response`.

///

## Власні заголовки { #custom-headers }

Майте на увазі, що власні закриті заголовки можна додавати <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">за допомогою префікса `X-`</a>.

Але якщо у вас є власні заголовки, які клієнт у браузері має бачити, вам потрібно додати їх у вашу конфігурацію CORS (докладніше в [CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md){.internal-link target=_blank}), використовуючи параметр `expose_headers`, задокументований у <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">документації Starlette щодо CORS</a>.
