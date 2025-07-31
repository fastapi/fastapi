# Включение WSGI - Flask, Django и другие

Вы можете монтировать WSGI-приложения, как вы видели в разделе [Дополнительные приложения - Монтирования](sub-applications.md){.internal-link target=_blank}, [За прокси](behind-a-proxy.md){.internal-link target=_blank}.

Для этого вы можете использовать `WSGIMiddleware`, чтобы обернуть ваше WSGI-приложение, например, Flask, Django и т.д.

## Использование `WSGIMiddleware`

Вам нужно импортировать `WSGIMiddleware`.

Затем обернуть WSGI (например, Flask) приложение с помощью middleware (промежуточного слоя).

И затем смонтировать это под path.

{* ../../docs_src/wsgi/tutorial001.py hl[2:3,3] *}

## Проверьте это

Теперь каждый HTTP-запрос по path `/v1/` будет обработан приложением Flask.

А остальные запросы будут обработаны **FastAPI**.

Если вы запустите его и перейдете по ссылке <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a>, вы увидите ответ от Flask:

```txt
Hello, World from Flask!
```

И если вы перейдете по ссылке <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a>, вы увидите ответ от FastAPI:

```JSON
{
    "message": "Hello World"
}
```
