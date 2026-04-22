# FastAPI CLI { #fastapi-cli }

**FastAPI <abbr title="command line interface - інтерфейс командного рядка">CLI</abbr>** — це програма командного рядка, яку ви можете використовувати, щоб обслуговувати ваш застосунок FastAPI, керувати вашим проєктом FastAPI тощо.

Коли ви встановлюєте FastAPI (наприклад, за допомогою `pip install "fastapi[standard]"`), він постачається з програмою командного рядка, яку можна запускати в терміналі.

Щоб запустити ваш застосунок FastAPI для розробки, ви можете використати команду `fastapi dev`:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

/// tip | Порада

Для продакшну ви б використовували `fastapi run` замість `fastapi dev`. 🚀

///

Внутрішньо **FastAPI CLI** використовує [Uvicorn](https://www.uvicorn.dev), високопродуктивний, готовий до продакшну ASGI сервер. 😎

CLI `fastapi` спробує автоматично визначити застосунок FastAPI для запуску, припускаючи, що це об'єкт з назвою `app` у файлі `main.py` (або кілька інших варіантів).

Але ви можете явно налаштувати застосунок, який слід використовувати.

## Налаштуйте `entrypoint` застосунку в `pyproject.toml` { #configure-the-app-entrypoint-in-pyproject-toml }

Ви можете налаштувати розташування вашого застосунку у файлі `pyproject.toml`, наприклад:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Цей `entrypoint` підкаже команді `fastapi`, що слід імпортувати застосунок так:

```python
from main import app
```

Якщо ваш код має таку структуру:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

Тоді ви встановили б `entrypoint` як:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

що еквівалентно:

```python
from backend.main import app
```

### `fastapi dev` зі шляхом { #fastapi-dev-with-path }

Ви також можете передати шлях до файлу команді `fastapi dev`, і вона здогадається, який об'єкт застосунку FastAPI використовувати:

```console
$ fastapi dev main.py
```

Але вам доведеться щоразу пам'ятати, щоб передавати правильний шлях під час виклику команди `fastapi`.

Крім того, інші інструменти можуть не знайти його, наприклад [Розширення VS Code](editor-support.md) або [FastAPI Cloud](https://fastapicloud.com), тому рекомендується використовувати `entrypoint` у `pyproject.toml`.

## `fastapi dev` { #fastapi-dev }

Запуск `fastapi dev` ініціює режим розробки.

За замовчуванням **auto-reload** увімкнено, і сервер автоматично перезавантажується, коли ви вносите зміни у ваш код. Це ресурсоємно та може бути менш стабільним, ніж коли його вимкнено. Вам слід використовувати це лише для розробки. Також він слухає IP-адресу `127.0.0.1`, яка є IP-адресою для того, щоб ваша машина могла взаємодіяти лише сама з собою (`localhost`).

## `fastapi run` { #fastapi-run }

Виконання `fastapi run` за замовчуванням запускає FastAPI у продакшн-режимі.

За замовчуванням **auto-reload** вимкнено. Також він слухає IP-адресу `0.0.0.0`, що означає всі доступні IP-адреси, таким чином він буде публічно доступним для будь-кого, хто може взаємодіяти з машиною. Зазвичай саме так ви запускатимете його в продакшн, наприклад у контейнері.

У більшості випадків ви (і вам слід) матимете «termination proxy», який обробляє HTTPS для вас зверху; це залежатиме від того, як ви розгортаєте ваш застосунок: ваш провайдер може зробити це за вас, або вам може знадобитися налаштувати це самостійно.

/// tip | Порада

Ви можете дізнатися більше про це в [документації з розгортання](deployment/index.md).

///
