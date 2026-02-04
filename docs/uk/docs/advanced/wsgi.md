# Підключення WSGI — Flask, Django та інші { #including-wsgi-flask-django-others }

Ви можете монтувати WSGI-застосунки так само, як ви бачили в [Підзастосунки — монтування](sub-applications.md){.internal-link target=_blank}, [За проксі](behind-a-proxy.md){.internal-link target=_blank}.

Для цього ви можете використати `WSGIMiddleware` і обгорнути ним ваш WSGI-застосунок, наприклад Flask, Django тощо.

## Використання `WSGIMiddleware` { #using-wsgimiddleware }

Потрібно імпортувати `WSGIMiddleware`.

Потім обгорнути WSGI-застосунок (наприклад, Flask) цим middleware.

І після цього змонтувати його за певним шляхом.

{* ../../docs_src/wsgi/tutorial001_py39.py hl[1,3,23] *}

## Перевірка { #check-it }

Тепер кожен запит за шляхом `/v1/` буде оброблятися застосунком Flask.

А решта — **FastAPI**.

Якщо ви запустите це й перейдете на <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a>, ви побачите відповідь від Flask:

```txt
Hello, World from Flask!
```

А якщо ви перейдете на <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a>, ви побачите відповідь від FastAPI:

```JSON
{
    "message": "Hello World"
}
```
