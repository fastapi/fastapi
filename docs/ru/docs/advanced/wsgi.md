# Подключение WSGI — Flask, Django и другие { #including-wsgi-flask-django-others }

Вы можете монтировать WSGI‑приложения, как вы видели в [Подприложения — Mounts](sub-applications.md){.internal-link target=_blank}, [За прокси‑сервером](behind-a-proxy.md){.internal-link target=_blank}.

Для этого вы можете использовать `WSGIMiddleware` и обернуть им ваше WSGI‑приложение, например Flask, Django и т.д.

## Использование `WSGIMiddleware` { #using-wsgimiddleware }

Нужно импортировать `WSGIMiddleware`.

Затем оберните WSGI‑приложение (например, Flask) в middleware (Промежуточный слой).

После этого смонтируйте его на путь.

{* ../../docs_src/wsgi/tutorial001.py hl[2:3,3] *}

## Проверьте { #check-it }

Теперь каждый HTTP‑запрос по пути `/v1/` будет обрабатываться приложением Flask.

А всё остальное будет обрабатываться **FastAPI**.

Если вы запустите это и перейдёте по <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a>, вы увидите HTTP‑ответ от Flask:

```txt
Hello, World from Flask!
```

А если вы перейдёте по <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a>, вы увидите HTTP‑ответ от FastAPI:

```JSON
{
    "message": "Hello World"
}
```
