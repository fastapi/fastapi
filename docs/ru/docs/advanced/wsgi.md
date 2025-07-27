# Включение WSGI - Flask, Django, другие

Вы можете монтировать WSGI-приложения, как вы видели в [Sub Applications - Mounts](sub-applications.md){.internal-link target=_blank}, [Behind a Proxy](behind-a-proxy.md){.internal-link target=_blank}.

Для этого вы можете использовать `WSGIMiddleware` и использовать его для обёртки вашего WSGI-приложения, например, Flask, Django и т. д.

## Использование `WSGIMiddleware`

Вам нужно импортировать `WSGIMiddleware`.

Затем оберните WSGI (например, Flask) приложение с помощью middleware.

И затем смонтируйте его под определённым путём.

{* ../../docs_src/wsgi/tutorial001.py hl[2:3,3] *}

## Проверка

Теперь каждый запрос по пути `/v1/` будет обрабатываться приложением Flask.

А остальные будут обрабатываться **FastAPI**.

Если вы запустите его и перейдёте на <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a>, вы увидите ответ от Flask:

```txt
Hello, World from Flask!
```

А если вы перейдёте на <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a>, вы увидите ответ от FastAPI:

```JSON
{
    "message": "Hello World"
}
```
