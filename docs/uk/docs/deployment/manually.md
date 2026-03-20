# Запустіть сервер вручну { #run-a-server-manually }

## Використовуйте команду `fastapi run` { #use-the-fastapi-run-command }

Коротко: використовуйте `fastapi run`, щоб запустити ваш застосунок FastAPI:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>2306215</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
```

</div>

Це спрацює в більшості випадків. 😎

Цю команду можна використати, наприклад, щоб запустити ваш застосунок FastAPI у контейнері, на сервері тощо.

## Сервери ASGI { #asgi-servers }

Розгляньмо деталі.

FastAPI використовує стандарт для побудови Python вебфреймворків і серверів під назвою <abbr title="Asynchronous Server Gateway Interface - Асинхронний шлюзовий інтерфейс сервера">ASGI</abbr>. FastAPI - це ASGI вебфреймворк.

Головне, що потрібно, щоб запустити застосунок **FastAPI** (або будь-який інший ASGI-застосунок) на віддаленій серверній машині, - це програма ASGI-сервера на кшталт **Uvicorn**; саме вона постачається за замовчуванням у команді `fastapi`.

Є кілька альтернатив, зокрема:

* [Uvicorn](https://www.uvicorn.dev/): високопродуктивний ASGI-сервер.
* [Hypercorn](https://hypercorn.readthedocs.io/): ASGI-сервер, сумісний з HTTP/2 і Trio, серед інших можливостей.
* [Daphne](https://github.com/django/daphne): ASGI-сервер, створений для Django Channels.
* [Granian](https://github.com/emmett-framework/granian): Rust HTTP-сервер для Python-застосунків.
* [NGINX Unit](https://unit.nginx.org/howto/fastapi/): NGINX Unit - легке й універсальне середовище виконання вебзастосунків.

## Серверна машина і серверна програма { #server-machine-and-server-program }

Є невелика деталь щодо назв, яку варто пам'ятати. 💡

Слово «**сервер**» зазвичай означає і віддалений/хмарний комп'ютер (фізична або віртуальна машина), і програму, що працює на цій машині (наприклад, Uvicorn).

Майте на увазі, що коли ви бачите слово «сервер» загалом, воно може стосуватися будь-якого з цих двох значень.

Коли йдеться про віддалену машину, її часто називають «сервер», а також «машина», «VM» (віртуальна машина), «вузол». Усе це означає різновиди віддаленої машини, зазвичай з Linux, на якій ви запускаєте програми.

## Встановіть серверну програму { #install-the-server-program }

Після встановлення FastAPI ви отримуєте продакшн-сервер Uvicorn і можете запускати його командою `fastapi run`.

Але ви також можете встановити ASGI-сервер вручну.

Переконайтеся, що ви створили [віртуальне оточення](../virtual-environments.md), активували його, після чого можете встановити серверну програму.

Наприклад, щоб установити Uvicorn:

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

Подібний процес застосовується до будь-якої іншої ASGI-серверної програми.

/// tip | Порада

Додавши `standard`, Uvicorn встановить і використовуватиме деякі рекомендовані додаткові залежності.

Зокрема `uvloop` - високопродуктивну заміну «без змін у коді» для `asyncio`, що суттєво підвищує рівночасність і продуктивність.

Якщо ви встановлюєте FastAPI через `pip install "fastapi[standard]"`, ви вже отримаєте і `uvicorn[standard]`.

///

## Запустіть серверну програму { #run-the-server-program }

Якщо ви встановили ASGI-сервер вручну, зазвичай потрібно передати рядок імпорту в спеціальному форматі, щоб він імпортував ваш застосунок FastAPI:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note | Примітка

Команда `uvicorn main:app` означає:

* `main`: файл `main.py` (Python «модуль»).
* `app`: об'єкт, створений у `main.py` рядком `app = FastAPI()`.

Це еквівалентно:

```Python
from main import app
```

///

Кожна альтернативна ASGI-серверна програма матиме подібну команду; читайте більше в їхній документації.

/// warning | Попередження

Uvicorn та інші сервери підтримують опцію `--reload`, корисну під час розробки.

Опція `--reload` споживає значно більше ресурсів, є менш стабільною тощо.

Вона дуже допомагає під час **розробки**, але її **не слід** використовувати в **продакшні**.

///

## Концепції розгортання { #deployment-concepts }

Ці приклади запускають серверну програму (наприклад, Uvicorn), піднімаючи один процес, що слухає всі IP (`0.0.0.0`) на визначеному порту (наприклад, `80`).

Це базова ідея. Але, ймовірно, вам знадобиться подбати ще про таке:

* Безпека - HTTPS
* Автозапуск
* Перезапуски
* Реплікація (кількість запущених процесів)
* Пам'ять
* Попередні кроки перед стартом

У наступних розділах я розповім більше про кожну з цих концепцій, як про них думати, і наведу конкретні приклади та стратегії для їх опрацювання. 🚀
