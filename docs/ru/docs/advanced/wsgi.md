# Подключение WSGI — Flask, Django и другие { #including-wsgi-flask-django-others }

Вы можете монтировать WSGI‑приложения, как вы видели в [Подприложения — Mounts](sub-applications.md), [За прокси‑сервером](behind-a-proxy.md).

Для этого вы можете использовать `WSGIMiddleware` и обернуть им ваше WSGI‑приложение, например Flask, Django и т.д.

## Использование `WSGIMiddleware` { #using-wsgimiddleware }

/// info | Информация

Для этого требуется установить `a2wsgi`, например с помощью `pip install a2wsgi`.

///

Нужно импортировать `WSGIMiddleware` из `a2wsgi`.

Затем оберните WSGI‑приложение (например, Flask) в middleware (Промежуточный слой).

После этого смонтируйте его на путь.

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note | Примечание

Ранее рекомендовалось использовать `WSGIMiddleware` из `fastapi.middleware.wsgi`, но теперь он помечен как устаревший.

Вместо него рекомендуется использовать пакет `a2wsgi`. Использование остаётся таким же.

Просто убедитесь, что пакет `a2wsgi` установлен, и импортируйте `WSGIMiddleware` из `a2wsgi`.

///

## Проверьте { #check-it }

Теперь каждый HTTP‑запрос по пути `/v1/` будет обрабатываться приложением Flask.

А всё остальное будет обрабатываться **FastAPI**.

Если вы запустите это и перейдёте по [http://localhost:8000/v1/](http://localhost:8000/v1/), вы увидите HTTP‑ответ от Flask:

```txt
Hello, World from Flask!
```

А если вы перейдёте по [http://localhost:8000/v2](http://localhost:8000/v2), вы увидите HTTP‑ответ от FastAPI:

```JSON
{
    "message": "Hello World"
}
```
