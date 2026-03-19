# Запуск сервера вручную { #run-a-server-manually }

## Используйте команду `fastapi run` { #use-the-fastapi-run-command }

Коротко: используйте `fastapi run`, чтобы запустить ваше приложение FastAPI:

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

В большинстве случаев этого достаточно. 😎

Этой командой, например, можно запускать приложение **FastAPI** в контейнере, на сервере и т.д.

## ASGI‑серверы { #asgi-servers }

Давайте немного углубимся в детали.

FastAPI использует стандарт для построения Python‑веб‑фреймворков и серверов под названием <abbr title="Asynchronous Server Gateway Interface – Асинхронный шлюзовый интерфейс сервера">ASGI</abbr>. FastAPI — ASGI-веб‑фреймворк.

Главное, что вам нужно, чтобы запустить приложение **FastAPI** (или любое другое ASGI‑приложение) на удалённой серверной машине, — это программа ASGI‑сервера, такая как **Uvicorn**; именно он используется по умолчанию в команде `fastapi`.

Есть несколько альтернатив, например:

* [Uvicorn](https://www.uvicorn.dev/): высокопроизводительный ASGI‑сервер.
* [Hypercorn](https://hypercorn.readthedocs.io/): ASGI‑сервер, среди прочего совместимый с HTTP/2 и Trio.
* [Daphne](https://github.com/django/daphne): ASGI‑сервер, созданный для Django Channels.
* [Granian](https://github.com/emmett-framework/granian): HTTP‑сервер на Rust для Python‑приложений.
* [NGINX Unit](https://unit.nginx.org/howto/fastapi/): NGINX Unit — лёгкая и многофункциональная среда выполнения веб‑приложений.

## Сервер как машина и сервер как программа { #server-machine-and-server-program }

Есть небольшой нюанс в терминологии, о котором стоит помнить. 💡

Слово «сервер» обычно используют и для обозначения удалённого/облачного компьютера (физической или виртуальной машины), и для программы, работающей на этой машине (например, Uvicorn).

Имейте в виду, что слово «сервер» в целом может означать любое из этих двух.

Когда речь идёт об удалённой машине, её зачастую называют **сервер**, а также **машина**, **VM** (виртуальная машина), **нода**. Всё это — варианты названия удалённой машины, обычно под управлением Linux, на которой вы запускаете программы.

## Установка серверной программы { #install-the-server-program }

При установке FastAPI он поставляется с продакшн‑сервером Uvicorn, и вы можете запустить его командой `fastapi run`.

Но вы также можете установить ASGI‑сервер вручную.

Создайте [виртуальное окружение](../virtual-environments.md), активируйте его и затем установите серверное приложение.

Например, чтобы установить Uvicorn:

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

Аналогично устанавливаются и другие ASGI‑серверы.

/// tip | Совет

С добавлением `standard` Uvicorn установит и будет использовать ряд рекомендованных дополнительных зависимостей.

В их числе `uvloop` — высокопроизводительная замена `asyncio`, дающая серьёзный прирост производительности при параллельной работе.

Если вы устанавливаете FastAPI, например так: `pip install "fastapi[standard]"`, вы уже получаете и `uvicorn[standard]`.

///

## Запуск серверной программы { #run-the-server-program }

Если вы установили ASGI‑сервер вручную, обычно нужно передать строку импорта в специальном формате, чтобы он смог импортировать ваше приложение FastAPI:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note | Примечание

Команда `uvicorn main:app` означает:

* `main`: файл `main.py` (Python‑«модуль»).
* `app`: объект, созданный в `main.py` строкой `app = FastAPI()`.

Эквивалентно:

```Python
from main import app
```

///

У каждого альтернативного ASGI‑сервера будет похожая команда; подробнее см. в их документации.

/// warning | Предупреждение

Uvicorn и другие серверы поддерживают опцию `--reload`, полезную в период разработки.

Опция `--reload` потребляет значительно больше ресурсов, менее стабильна и т.п.

Она сильно помогает во время **разработки**, но в **продакшн** её использовать **не следует**.

///

## Концепции развёртывания { #deployment-concepts }

В этих примерах серверная программа (например, Uvicorn) запускает **один процесс**, слушающий все IP‑адреса (`0.0.0.0`) на заранее заданном порту (например, `80`).

Это базовая идея. Но, вероятно, вам понадобится позаботиться и о некоторых дополнительных вещах, например:

* Безопасность — HTTPS
* Запуск при старте системы
* Перезапуски
* Репликация (количество запущенных процессов)
* Память
* Предварительные шаги перед запуском

В следующих главах я расскажу подробнее про каждую из этих концепций, о том, как о них думать, и приведу конкретные примеры со стратегиями, как с ними работать. 🚀
