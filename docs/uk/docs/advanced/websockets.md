# WebSockets { #websockets }

Ви можете використовувати <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSockets</a> з **FastAPI**.

## Встановіть `websockets` { #install-websockets }

Переконайтеся, що ви створили [віртуальне оточення](../virtual-environments.md){.internal-link target=_blank}, активували його та встановили `websockets` (бібліотеку Python, що полегшує використання протоколу «WebSocket»):

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## Клієнт WebSockets { #websockets-client }

### У продакшені { #in-production }

У вашій продакшен-системі у вас, напевно, є фронтенд, створений за допомогою сучасного фреймворку на кшталт React, Vue.js або Angular.

Для спілкування через WebSockets з бекендом ви, ймовірно, використовуватимете утиліти вашого фронтенду.

Або у вас може бути нативний мобільний застосунок, що напряму спілкується з вашим WebSocket-бекендом нативним кодом.

Або будь-який інший спосіб спілкування з кінцевою точкою WebSocket.

---

Але для цього прикладу ми використаємо дуже простий HTML-документ з невеликим JavaScript, усе всередині довгого рядка.

Звісно, це не оптимально і ви б не використовували це у продакшені.

У продакшені ви б використали один з варіантів вище.

Але це найпростіший спосіб зосередитися на серверній частині WebSockets і мати робочий приклад:

{* ../../docs_src/websockets/tutorial001_py310.py hl[2,6:38,41:43] *}

## Створіть `websocket` { #create-a-websocket }

У вашому застосунку **FastAPI** створіть `websocket`:

{* ../../docs_src/websockets/tutorial001_py310.py hl[1,46:47] *}

/// note | Технічні деталі

Ви також можете використати `from starlette.websockets import WebSocket`.

**FastAPI** надає той самий `WebSocket` напряму як зручність для вас, розробника. Але він походить безпосередньо зі Starlette.

///

## Очікуйте повідомлення та надсилайте повідомлення { #await-for-messages-and-send-messages }

У вашому маршруті WebSocket ви можете `await` повідомлення і надсилати повідомлення.

{* ../../docs_src/websockets/tutorial001_py310.py hl[48:52] *}

Ви можете отримувати та надсилати бінарні, текстові та JSON-дані.

## Спробуйте { #try-it }

Якщо ваш файл називається `main.py`, запустіть ваш застосунок командою:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Відкрийте у браузері <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Ви побачите просту сторінку на кшталт:

<img src="/img/tutorial/websockets/image01.png">

Ви можете вводити повідомлення у поле вводу та надсилати їх:

<img src="/img/tutorial/websockets/image02.png">

І ваш застосунок **FastAPI** з WebSockets відповість:

<img src="/img/tutorial/websockets/image03.png">

Ви можете надсилати (і отримувати) багато повідомлень:

<img src="/img/tutorial/websockets/image04.png">

І всі вони використовуватимуть те саме з'єднання WebSocket.

## Використання `Depends` та іншого { #using-depends-and-others }

У кінцевих точках WebSocket ви можете імпортувати з `fastapi` і використовувати:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

Вони працюють так само, як для інших ендпойнтів FastAPI/*операцій шляху*:

{* ../../docs_src/websockets/tutorial002_an_py310.py hl[68:69,82] *}

/// info

Оскільки це WebSocket, не має сенсу піднімати `HTTPException`, натомість ми піднімаємо `WebSocketException`.

Ви можете використати код закриття з <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">чинних кодів, визначених у специфікації</a>.

///

### Спробуйте WebSockets із залежностями { #try-the-websockets-with-dependencies }

Якщо ваш файл називається `main.py`, запустіть ваш застосунок командою:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Відкрийте у браузері <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Там ви можете встановити:

* «Item ID», який використовується у шляху.
* «Token», який використовується як параметр запиту.

/// tip

Зверніть увагу, що параметр запиту `token` буде оброблено залежністю.

///

Після цього ви зможете під'єднати WebSocket, а далі надсилати й отримувати повідомлення:

<img src="/img/tutorial/websockets/image05.png">

## Обробка відключень і кількох клієнтів { #handling-disconnections-and-multiple-clients }

Коли з'єднання WebSocket закривається, `await websocket.receive_text()` підніме виняток `WebSocketDisconnect`, який ви можете перехопити й обробити, як у цьому прикладі.

{* ../../docs_src/websockets/tutorial003_py310.py hl[79:81] *}

Щоб спробувати:

* Відкрийте застосунок у кількох вкладках браузера.
* Надсилайте з них повідомлення.
* Потім закрийте одну з вкладок.

Це підніме виняток `WebSocketDisconnect`, і всі інші клієнти отримають повідомлення на кшталт:

```
Client #1596980209979 left the chat
```

/// tip

Застосунок вище - це мінімальний і простий приклад, що демонструє, як обробляти та розсилати повідомлення кільком з'єднанням WebSocket.

Але майте на увазі, що оскільки все обробляється в пам'яті, в одному списку, це працюватиме лише поки процес запущений, і лише з одним процесом.

Якщо вам потрібне щось просте для інтеграції з FastAPI, але більш надійне, з підтримкою Redis, PostgreSQL чи інших, перегляньте <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a>.

///

## Детальніше { #more-info }

Щоб дізнатися більше про можливості, перегляньте документацію Starlette:

* <a href="https://www.starlette.dev/websockets/" class="external-link" target="_blank">Клас `WebSocket`</a>.
* <a href="https://www.starlette.dev/endpoints/#websocketendpoint" class="external-link" target="_blank">Обробка WebSocket на основі класів</a>.
