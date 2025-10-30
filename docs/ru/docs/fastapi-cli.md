# FastAPI CLI { #fastapi-cli }

**FastAPI CLI** это программа командной строки, которую вы можете использовать для запуска вашего FastAPI приложения, для управления FastAPI-проектом, а также для многих других вещей.

`fastapi-cli` устанавливается вместе со стандартным пакетом FastAPI (при запуске команды `pip install "fastapi[standard]"`). Данный пакет предоставляет доступ к программе `fastapi` через терминал.

Чтобы запустить приложение FastAPI в режиме разработки, вы можете использовать команду `fastapi dev`:

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

Приложение командной строки `fastapi` это и есть **FastAPI CLI**.

FastAPI CLI берет путь к вашей Python-программе (напр. `main.py`) и автоматически находит объект `FastAPI` (обычно это `app`), затем определяет правильный процесс импорта и запускает сервер приложения.

Для работы в режиме продакшн вместо `fastapi dev` нужно использовать `fastapi run`. 🚀

Внутри **FastAPI CLI** используется <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>, высокопроизводительный, готовый к работе в продакшне ASGI-сервер. 😎

## `fastapi dev` { #fastapi-dev }

Вызов `fastapi dev` запускает режим разработки.

По умолчанию включена авто-перезагрузка (**auto-reload**), благодаря этому при изменении кода происходит перезагрузка сервера приложения. Эта установка требует значительных ресурсов и делает систему менее стабильной. Используйте её только при разработке. Приложение слушает входящие подключения на IP `127.0.0.1`. Это IP адрес вашей машины, предназначенный для внутренних коммуникаций (`localhost`).

## `fastapi run` { #fastapi-run }

Вызов `fastapi run` по умолчанию запускает FastAPI в режиме продакшн.

По умолчанию авто-перезагрузка (**auto-reload**) отключена. Приложение слушает входящие подключения на IP `0.0.0.0`, т.е. на всех доступных адресах компьютера. Таким образом, приложение будет находиться в публичном доступе для любого, кто может подсоединиться к вашей машине. Продуктовые приложения запускаются именно так, например, с помощью контейнеров.

В большинстве случаев вы будете (и должны) использовать прокси-сервер ("termination proxy"), который будет поддерживать HTTPS поверх вашего приложения. Всё будет зависеть от того, как вы развертываете приложение: за вас это либо сделает ваш провайдер, либо вам придется сделать настройки самостоятельно.

/// tip | Подсказка

Вы можете больше узнать об этом в [документации по развертыванию](deployment/index.md){.internal-link target=_blank}.

///
