# FastAPI CLI { #fastapi-cli }

**FastAPI CLI** — це програма командного рядка, яку ви можете використовувати, щоб обслуговувати ваш застосунок FastAPI, керувати вашим проєктом FastAPI тощо.

Коли ви встановлюєте FastAPI (наприклад, за допомогою `pip install "fastapi[standard]"`), він включає пакет під назвою `fastapi-cli`, цей пакет надає команду `fastapi` у терміналі.

Щоб запустити ваш застосунок FastAPI для розробки, ви можете використати команду `fastapi dev`:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

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

Програма командного рядка під назвою `fastapi` — це **FastAPI CLI**.

FastAPI CLI бере шлях до вашої Python-програми (наприклад, `main.py`) і автоматично виявляє екземпляр `FastAPI` (зазвичай з назвою `app`), визначає правильний процес імпорту, а потім обслуговує його.

Натомість, для продакшн ви використали б `fastapi run`. 🚀

Внутрішньо **FastAPI CLI** використовує <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>, високопродуктивний, production-ready, ASGI сервер. 😎

## `fastapi dev` { #fastapi-dev }

Запуск `fastapi dev` ініціює режим розробки.

За замовчуванням **auto-reload** увімкнено, і сервер автоматично перезавантажується, коли ви вносите зміни у ваш код. Це ресурсоємно та може бути менш стабільним, ніж коли його вимкнено. Вам слід використовувати це лише для розробки. Також він слухає IP-адресу `127.0.0.1`, яка є IP-адресою для того, щоб ваша машина могла взаємодіяти лише сама з собою (`localhost`).

## `fastapi run` { #fastapi-run }

Виконання `fastapi run` за замовчуванням запускає FastAPI у продакшн-режимі.

За замовчуванням **auto-reload** вимкнено. Також він слухає IP-адресу `0.0.0.0`, що означає всі доступні IP-адреси, таким чином він буде публічно доступним для будь-кого, хто може взаємодіяти з машиною. Зазвичай саме так ви запускатимете його в продакшн, наприклад у контейнері.

У більшості випадків ви (і вам слід) матимете «termination proxy», який обробляє HTTPS для вас зверху; це залежатиме від того, як ви розгортаєте ваш застосунок: ваш провайдер може зробити це за вас, або вам може знадобитися налаштувати це самостійно.

/// tip | Порада

Ви можете дізнатися більше про це в [документації з розгортання](deployment/index.md){.internal-link target=_blank}.

///
