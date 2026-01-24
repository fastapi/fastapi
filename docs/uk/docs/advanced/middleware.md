# Розширені middleware { #advanced-middleware }

У головному посібнику ви прочитали, як додати [власний Middleware](../tutorial/middleware.md){.internal-link target=_blank} до вашого застосунку.

Також ви прочитали, як обробляти [CORS за допомогою `CORSMiddleware`](../tutorial/cors.md){.internal-link target=_blank}.

У цьому розділі ми розглянемо, як використовувати інші middleware.

## Додавання ASGI middleware { #adding-asgi-middlewares }

Оскільки **FastAPI** базується на Starlette і реалізує специфікацію <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr>, ви можете використовувати будь-який ASGI middleware.

Middleware не обов’язково має бути зроблений спеціально для FastAPI або Starlette, головне — щоб він відповідав специфікації ASGI.

Загалом, ASGI middleware — це класи, які очікують отримати ASGI застосунок як перший аргумент.

Тож у документації сторонніх ASGI middleware вам, імовірно, скажуть зробити щось на кшталт:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

Але FastAPI (фактично Starlette) надає простіший спосіб, який гарантує, що внутрішні middleware коректно обробляють помилки сервера, а користувацькі обробники винятків працюють правильно.

Для цього використовуйте `app.add_middleware()` (як у прикладі для CORS).

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` отримує клас middleware як перший аргумент і будь-які додаткові аргументи, які буде передано middleware.

## Інтегровані middleware { #integrated-middlewares }

**FastAPI** містить кілька middleware для поширених випадків використання; далі розглянемо, як ними користуватися.

/// note | Технічні деталі

Для наступних прикладів ви також можете використати `from starlette.middleware.something import SomethingMiddleware`.

**FastAPI** надає кілька middleware у `fastapi.middleware` лише для зручності для вас, розробника. Але більшість доступних middleware походять безпосередньо зі Starlette.

///

## `HTTPSRedirectMiddleware` { #httpsredirectmiddleware }

Гарантує, що всі вхідні запити мають бути або `https`, або `wss`.

Будь-який вхідний запит до `http` або `ws` буде перенаправлено на безпечну схему.

{* ../../docs_src/advanced_middleware/tutorial001_py39.py hl[2,6] *}

## `TrustedHostMiddleware` { #trustedhostmiddleware }

Гарантує, що всі вхідні запити мають коректно встановлений заголовок `Host`, щоб захиститися від атак на HTTP Host Header.

{* ../../docs_src/advanced_middleware/tutorial002_py39.py hl[2,6:8] *}

Підтримуються такі аргументи:

* `allowed_hosts` — список доменних імен, які слід дозволити як імена хостів. Підтримуються домени з wildcard, як-от `*.example.com`, для зіставлення піддоменів. Щоб дозволити будь-яке ім’я хоста, використайте `allowed_hosts=["*"]` або не додавайте цей middleware.
* `www_redirect` — якщо встановлено в True, запити до версій дозволених хостів без `www` буде перенаправлено на відповідні версії з `www`. За замовчуванням `True`.

Якщо вхідний запит не проходить перевірку, буде надіслано відповідь `400`.

## `GZipMiddleware` { #gzipmiddleware }

Обробляє GZip-відповіді для будь-якого запиту, що містить `"gzip"` у заголовку `Accept-Encoding`.

Middleware оброблятиме як стандартні, так і потокові відповіді.

{* ../../docs_src/advanced_middleware/tutorial003_py39.py hl[2,6] *}

Підтримуються такі аргументи:

* `minimum_size` — не застосовувати GZip до відповідей, менших за цей мінімальний розмір у байтах. За замовчуванням `500`.
* `compresslevel` — використовується під час стиснення GZip. Це ціле число в діапазоні від 1 до 9. За замовчуванням `9`. Менше значення дає швидше стиснення, але більший розмір файлів, тоді як більше значення — повільніше стиснення, але менший розмір файлів.

## Інші middleware { #other-middlewares }

Існує багато інших ASGI middleware.

Наприклад:

* <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">`ProxyHeadersMiddleware` в Uvicorn</a>
* <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

Щоб переглянути інші доступні middleware, ознайомтеся з <a href="https://www.starlette.dev/middleware/" class="external-link" target="_blank">документацією Starlette щодо Middleware</a> та <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">ASGI Awesome List</a>.
