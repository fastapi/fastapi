# Веб-сокеты

Вы можете использовать <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">веб-сокеты</a> в **FastAPI**.

## Установка `WebSockets`

Убедитесь, что [виртуальная среда](../virtual-environments.md){.internal-link target=_blank} создана, активируйте её и установите `websockets`:

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## Клиент WebSockets

### Рабочее приложение

Скорее всего, в вашей реальной продуктовой системе есть фронтенд, реализованный при помощи современных фреймворков React, Vue.js или Angular.

И наверняка для взаимодействия с бекендом через веб-сокеты вы будете использовать средства фронтенда.

Также у вас может быть нативное мобильное приложение, коммуницирующее непосредственно с веб-сокетами на бекенд-сервере.

Либо вы можете сделать какой-либо другой способ взаимодействия с веб-сокетами.

---

Но для этого примера мы воспользуемся очень простым HTML документом с небольшими вставками JavaScript кода.

Конечно же это неоптимально, и на практике так делать не стоит.

В реальных приложениях стоит воспользоваться одним из вышеупомянутых способов.

Для примера нам нужен наиболее простой способ, который позволит сосредоточиться на серверной части веб-сокетов и получить рабочий код:

{* ../../docs_src/websockets/tutorial001.py hl[2,6:38,41:43] *}

## Создание `websocket`

Создайте `websocket` в своем **FastAPI** приложении:

{* ../../docs_src/websockets/tutorial001.py hl[1,46:47] *}

/// note | Технические детали

Вы также можете использовать `from starlette.websockets import WebSocket`.

**FastAPI** напрямую предоставляет тот же самый `WebSocket` просто для удобства. На самом деле это `WebSocket` из Starlette.

///

## Ожидание и отправка сообщений

Через эндпоинт веб-сокета вы можете получать и отправлять сообщения.

{* ../../docs_src/websockets/tutorial001.py hl[48:52] *}

Вы можете получать и отправлять двоичные, текстовые и JSON данные.

## Проверка в действии

Если ваш файл называется `main.py`, то запустите приложение командой:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Откройте браузер по адресу <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Вы увидите следующую простенькую страницу:

<img src="/img/tutorial/websockets/image01.png">

Вы можете набирать сообщения в поле ввода и отправлять их:

<img src="/img/tutorial/websockets/image02.png">

И ваше **FastAPI** приложение с веб-сокетами ответит:

<img src="/img/tutorial/websockets/image03.png">

Вы можете отправлять и получать множество сообщений:

<img src="/img/tutorial/websockets/image04.png">

И все они будут использовать одно и то же веб-сокет соединение.

## Использование `Depends` и не только

Вы можете импортировать из `fastapi` и использовать в эндпоинте вебсокета:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

Они работают так же, как и в других FastAPI эндпоинтах/*операциях пути*:

{* ../../docs_src/websockets/tutorial002_an_py310.py hl[68:69,82] *}

/// info | Примечание

В веб-сокете вызывать `HTTPException` не имеет смысла. Вместо этого нужно использовать `WebSocketException`.

Закрывающий статус код можно использовать из <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">valid codes defined in the specification</a>.

///

### Веб-сокеты с зависимостями: проверка в действии

Если ваш файл называется `main.py`, то запустите приложение командой:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Откройте браузер по адресу <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Там вы можете задать:

* "Item ID", используемый в пути.
* "Token", используемый как query-параметр.

/// tip | Подсказка

Обратите внимание, что query-параметр `token` будет обработан в зависимости.

///

Теперь вы можете подключиться к веб-сокету и начинать отправку и получение сообщений:

<img src="/img/tutorial/websockets/image05.png">

## Обработка отключений и работа с несколькими клиентами

Если веб-сокет соединение закрыто, то `await websocket.receive_text()` вызовет исключение `WebSocketDisconnect`, которое можно поймать и обработать как в этом примере:

{* ../../docs_src/websockets/tutorial003_py39.py hl[79:81] *}

Чтобы воспроизвести пример:

* Откройте приложение в нескольких вкладках браузера.
* Отправьте из них сообщения.
* Затем закройте одну из вкладок.

Это вызовет исключение `WebSocketDisconnect`, и все остальные клиенты получат следующее сообщение:

```
Client #1596980209979 left the chat
```

/// tip | Примечание

Приложение выше - это всего лишь простой минимальный пример, демонстрирующий обработку и передачу сообщений нескольким веб-сокет соединениям.

Но имейте в виду, что это будет работать только в одном процессе и только пока он активен, так как всё обрабатывается в простом списке в оперативной памяти.

Если нужно что-то легко интегрируемое с FastAPI, но более надежное и с поддержкой Redis, PostgreSQL или другого, то можно воспользоваться <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a>.

///

## Дополнительная информация

Для более глубокого изучения темы воспользуйтесь документацией Starlette:

* <a href="https://www.starlette.io/websockets/" class="external-link" target="_blank">The `WebSocket` class</a>.
* <a href="https://www.starlette.io/endpoints/#websocketendpoint" class="external-link" target="_blank">Class-based WebSocket handling</a>.
