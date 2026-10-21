# Веб-сокеты { #websockets }

Вы можете использовать [веб-сокеты](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) в **FastAPI**.

## Установка `websockets` { #install-websockets }

Добавьте `websockets` (библиотека Python, упрощающая работу с протоколом "WebSocket") в ваш проект:

<div class="termy">

```console
$ uv add websockets

---> 100%
```

</div>

## Клиент WebSockets { #websockets-client }

### В продакшн { #in-production }

В продакшн у вас, вероятно, есть фронтенд, созданный с помощью современного фреймворка вроде React, Vue.js или Angular.

И для взаимодействия с бекендом по WebSocket вы, скорее всего, будете использовать инструменты вашего фронтенда.

Также у вас может быть нативное мобильное приложение, которое напрямую, нативным кодом, взаимодействует с вашим WebSocket-бекендом.

Либо у вас может быть любой другой способ взаимодействия с WebSocket-эндпоинтом.

---

Но для этого примера мы воспользуемся очень простым HTML‑документом с небольшим JavaScript, всё внутри одной длинной строки.

Конечно же, это неоптимально, и вы бы не использовали это в продакшн.

В продакшн у вас был бы один из вариантов выше.

Но это самый простой способ сосредоточиться на серверной части веб‑сокетов и получить рабочий пример:

{* ../../docs_src/websockets_/tutorial001_py310.py hl[2,6:38,41:43] *}

## Создание `websocket` { #create-a-websocket }

В вашем **FastAPI** приложении создайте `websocket`:

{* ../../docs_src/websockets_/tutorial001_py310.py hl[1,46:47] *}

/// note | Технические детали

Вы также можете использовать `from starlette.websockets import WebSocket`.

**FastAPI** напрямую предоставляет тот же самый `WebSocket` просто для удобства вас, разработчика. Но на самом деле это `WebSocket` из Starlette.

///

## Ожидание и отправка сообщений { #await-for-messages-and-send-messages }

В вашем WebSocket-маршруте вы можете `await` сообщения и отправлять сообщения.

{* ../../docs_src/websockets_/tutorial001_py310.py hl[48:52] *}

Вы можете получать и отправлять двоичные, текстовые и JSON данные.

## Проверка в действии { #try-it }

Поместите ваш код в файл `main.py`, затем запустите приложение:

<div class="termy">

```console
$ uv run fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Откройте браузер по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

Вы увидите следующую простенькую страницу:

<img src="/img/tutorial/websockets/image01.png">

Вы можете набирать сообщения в поле ввода и отправлять их:

<img src="/img/tutorial/websockets/image02.png">

И ваше **FastAPI** приложение с веб-сокетами ответит:

<img src="/img/tutorial/websockets/image03.png">

Вы можете отправлять (и получать) множество сообщений:

<img src="/img/tutorial/websockets/image04.png">

И все они будут использовать одно и то же WebSocket-соединение.

## Использование `Depends` и не только { #using-depends-and-others }

В WebSocket-эндпоинтах вы можете импортировать из `fastapi` и использовать:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

Они работают так же, как и в других FastAPI эндпоинтах/*операциях пути*:

{* ../../docs_src/websockets_/tutorial002_an_py310.py hl[68:69,82] *}

/// note | Примечание

Поскольку это WebSocket, вызывать `HTTPException` на самом деле не имеет смысла, вместо этого мы вызываем `WebSocketException`.

Вы можете использовать код закрытия из [допустимых кодов, определённых в спецификации](https://tools.ietf.org/html/rfc6455#section-7.4.1).

///

### Веб-сокеты с зависимостями: проверка в действии { #try-the-websockets-with-dependencies }

Запустите приложение:

<div class="termy">

```console
$ uv run fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Откройте браузер по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

Там вы можете задать:

* "Item ID", используемый в пути.
* "Token", используемый как query-параметр.

/// tip | Подсказка

Обратите внимание, что query `token` будет обработан в зависимости.

///

После этого вы можете подключиться к веб-сокету, а затем отправлять и получать сообщения:

<img src="/img/tutorial/websockets/image05.png">

## Обработка отключений и работа с несколькими клиентами { #handling-disconnections-and-multiple-clients }

Когда WebSocket-соединение закрыто, `await websocket.receive_text()` вызовет исключение `WebSocketDisconnect`, которое можно поймать и обработать как в этом примере.

{* ../../docs_src/websockets_/tutorial003_py310.py hl[79:81] *}

Чтобы воспроизвести пример:

* Откройте приложение в нескольких вкладках браузера.
* Отправьте из них сообщения.
* Затем закройте одну из вкладок.

Это вызовет исключение `WebSocketDisconnect`, и все остальные клиенты получат следующее сообщение:

```
Client #1596980209979 left the chat
```

/// tip | Подсказка

Приложение выше - это минимальный и простой пример, демонстрирующий обработку и рассылку сообщений нескольким WebSocket-соединениям.

Но имейте в виду, что, так как всё обрабатывается в памяти, в простом списке, это будет работать только пока процесс запущен и только с одним процессом.

Если нужно что-то легко интегрируемое с FastAPI, но более надежное и с поддержкой Redis, PostgreSQL или другого, то можно воспользоваться [encode/broadcaster](https://github.com/encode/broadcaster).

///

## Дополнительная информация { #more-info }

Для более глубокого изучения возможностей воспользуйтесь документацией Starlette:

* [Класс `WebSocket`](https://starlette.dev/websockets/).
* [Обработка WebSocket на основе классов](https://starlette.dev/endpoints/#websocketendpoint).
