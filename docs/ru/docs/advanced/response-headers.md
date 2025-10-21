# HTTP-заголовки ответа { #response-headers }

## Использовать параметр `Response` { #use-a-response-parameter }

Вы можете объявить параметр типа `Response` в вашей функции-обработчике пути (как можно сделать и для cookie).

А затем вы можете устанавливать HTTP-заголовки в этом *временном* объекте ответа.

{* ../../docs_src/response_headers/tutorial002.py hl[1, 7:8] *}

После этого вы можете вернуть любой нужный объект, как обычно (например, `dict`, модель из базы данных и т.д.).

И, если вы объявили `response_model`, он всё равно будет использован для фильтрации и преобразования возвращённого объекта.

**FastAPI** использует этот *временный* ответ, чтобы извлечь HTTP-заголовки (а также cookie и статус-код) и поместит их в финальный HTTP-ответ, который содержит возвращённое вами значение, отфильтрованное согласно `response_model`.

Вы также можете объявлять параметр `Response` в зависимостях и устанавливать в них заголовки (и cookie).

## Вернуть `Response` напрямую { #return-a-response-directly }

Вы также можете добавить HTTP-заголовки, когда возвращаете `Response` напрямую.

Создайте ответ, как описано в [Вернуть Response напрямую](response-directly.md){.internal-link target=_blank}, и передайте заголовки как дополнительный параметр:

{* ../../docs_src/response_headers/tutorial001.py hl[10:12] *}

/// note | Технические детали

Вы также можете использовать `from starlette.responses import Response` или `from starlette.responses import JSONResponse`.

**FastAPI** предоставляет те же самые `starlette.responses` как `fastapi.responses` — для вашего удобства как разработчика. Но большинство доступных классов ответов поступают напрямую из Starlette.

И поскольку `Response` часто используется для установки заголовков и cookie, **FastAPI** также предоставляет его как `fastapi.Response`.

///

## Пользовательские HTTP-заголовки { #custom-headers }

Помните, что собственные проприетарные заголовки можно добавлять, <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">используя префикс `X-`</a>.

Но если у вас есть пользовательские заголовки, которые вы хотите показывать клиенту в браузере, вам нужно добавить их в настройки CORS (подробнее см. в [CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md){.internal-link target=_blank}), используя параметр `expose_headers`, описанный в <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">документации Starlette по CORS</a>.
