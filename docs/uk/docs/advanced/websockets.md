# WebSockets { #websockets }

Ви можете використовувати <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSockets</a> з **FastAPI**.

## Встановлення `websockets` { #install-websockets }

Переконайтеся, що ви створили [віртуальне середовище](../virtual-environments.md){.internal-link target=_blank}, активували його та встановили `websockets` (бібліотеку Python, яка спрощує використання протоколу «WebSocket»):

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## Клієнт WebSockets { #websockets-client }

### У продакшені { #in-production }

У вашій продакшен-системі, ймовірно, є фронтенд, створений за допомогою сучасного фреймворку на кшталт React, Vue.js або Angular.

А для обміну даними через WebSockets з вашим бекендом ви, ймовірно, використовуватимете утиліти вашого фронтенда.

Або у вас може бути нативний мобільний застосунок, який напряму взаємодіє з вашим WebSocket-бекендом у нативному коді.

Або у вас може бути будь-який інший спосіб зв’язку з WebSocket endpoint.

---

Але для цього прикладу ми використаємо дуже простий HTML-документ з невеликою кількістю JavaScript — усе всередині довгого рядка.

Звісно, це не оптимально, і ви не використовували б це в продакшені.

У продакшені ви б скористалися одним із варіантів вище.

Але це найпростіший спосіб зосередитися на серверній частині WebSockets і мати робочий приклад:

{* ../../docs_src/websockets/tutorial001_py39.py hl[2,6:38,41:43] *}

## Створення `websocket` { #create-a-websocket }

У вашому застосунку **FastAPI** створіть `websocket`:

{* ../../docs_src/websockets/tutorial001_py39.py hl[1,46:47] *}

/// note | Технічні деталі

Ви також можете використати `from starlette.websockets import WebSocket`.

**FastAPI** надає той самий `WebSocket` напряму просто для зручності розробника. Але він походить безпосередньо зі Starlette.

///

## Очікування повідомлень і надсилання повідомлень { #await-for-messages-and-send-messages }

У вашому WebSocket маршруті ви можете робити `await` для отримання повідомлень і надсилати повідомлення.

{* ../../docs_src/websockets/tutorial001_py39.py hl[48:52] *}

Ви можете отримувати та надсилати двійкові дані, текст і JSON.

## Спробуйте { #try-it }

Якщо ваш файл має назву `main.py`, запустіть застосунок командою:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Відкрийте браузер за адресою <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Ви побачите просту сторінку на кшталт:

<img src="/img/tutorial/websockets/image01.png">

Ви можете вводити повідомлення в полі вводу та надсилати їх:

<img src="/img/tutorial/websockets/image02.png">

І ваш застосунок **FastAPI** з WebSockets надішле відповідь у відповідь:

<img src="/img/tutorial/websockets/image03.png">

Ви можете надсилати (і отримувати) багато повідомлень:

<img src="/img/tutorial/websockets/image04.png">

І всі вони використовуватимуть одне й те саме WebSocket-з’єднання.

## Використання `Depends` та інших { #using-depends-and-others }

У WebSocket endpoints ви можете імпортувати з `fastapi` та використовувати:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

Вони працюють так само, як і для інших endpoints FastAPI/*операцій шляху*:

{* ../../docs_src/websockets/tutorial002_an_py310.py hl[68:69,82] *}

/// info | Інформація

Оскільки це WebSocket, піднімати `HTTPException` насправді не має сенсу — натомість ми піднімаємо `WebSocketException`.

Ви можете використати код закриття зі <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">списку валідних кодів, визначених у специфікації</a>.

///

### Спробуйте WebSockets із залежностями { #try-the-websockets-with-dependencies }

Якщо ваш файл має назву `main.py`, запустіть застосунок командою:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Відкрийте браузер за адресою <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Там ви можете задати:

* «Item ID», який використовується в path.
* «Token», який використовується як query parameter.

/// tip | Порада

Зверніть увагу, що query `token` буде оброблено залежністю.

///

Після цього ви зможете під’єднати WebSocket, а потім надсилати й отримувати повідомлення:

<img src="/img/tutorial/websockets/image05.png">

## Обробка роз’єднань і кількох клієнтів { #handling-disconnections-and-multiple-clients }

Коли WebSocket-з’єднання закрито, `await websocket.receive_text()` підніме виняток `WebSocketDisconnect`, який ви можете перехопити та обробити, як у цьому прикладі.

{* ../../docs_src/websockets/tutorial003_py39.py hl[79:81] *}

Щоб спробувати:

* Відкрийте застосунок у кількох вкладках браузера.
* Надсилайте повідомлення з них.
* Потім закрийте одну з вкладок.

Це підніме виняток `WebSocketDisconnect`, і всі інші клієнти отримають повідомлення на кшталт:

```
Client #1596980209979 left the chat
```

/// tip | Порада

Застосунок вище — мінімальний і простий приклад, що демонструє, як обробляти та транслювати повідомлення на кілька WebSocket-з’єднань.

Але майте на увазі, що оскільки все обробляється в пам’яті, в одному списку, це працюватиме лише доки працює процес, і лише з одним процесом.

Якщо вам потрібно щось, що легко інтегрується з FastAPI, але є більш надійним і підтримується Redis, PostgreSQL чи іншими, перегляньте <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a>.

///

## Додаткова інформація { #more-info }

Щоб дізнатися більше про можливості, перегляньте документацію Starlette щодо:

* <a href="https://www.starlette.dev/websockets/" class="external-link" target="_blank">класу `WebSocket`</a>.
* <a href="https://www.starlette.dev/endpoints/#websocketendpoint" class="external-link" target="_blank">обробки WebSocket на основі класів</a>.
