# Учебник - Руководство пользователя

В этом руководстве шаг за шагом показано, как использовать **FastAPI** с большинством его функций.

Каждый раздел постепенно основывается на предыдущих, но он структурирован по отдельным темам, так что вы можете перейти непосредственно к конкретной теме для решения ваших конкретных потребностей в API.

Он также создан для использования в качестве будущего справочника.

Так что вы можете вернуться и посмотреть именно то, что вам нужно.

## Запустите код

Все блоки кода можно копировать и использовать напрямую (на самом деле это проверенные файлы Python).

Чтобы запустить любой из примеров, скопируйте код в файл `main.py`, и запустите `fastapi dev` с:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

**НАСТОЯТЕЛЬНО рекомендуется**, чтобы вы написали или скопировали код, отредактировали его и запустили локально.

Использование кода в вашем редакторе — это то, что действительно показывает вам преимущества FastAPI, видя, как мало кода вам нужно написать, все проверки типов, автодополнение и т.д.

---

## Установка FastAPI

Первый шаг — установить FastAPI.

Убедитесь, что вы создаете [виртуальное окружение](../virtual-environments.md){.internal-link target=_blank}, активируете его и затем **устанавливаете FastAPI**:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note | Технические детали

Когда вы устанавливаете с помощью `pip install "fastapi[standard]"`, это включает некоторые стандартные необязательные зависимости, включая `fastapi-cloud-cli`, который позволяет развернуть приложение на <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>.

Если вы не хотите иметь эти необязательные зависимости, вы можете вместо этого выполнить установку с помощью `pip install fastapi`.

Если вы хотите установить стандартные зависимости, но без `fastapi-cloud-cli`, вы можете установить их с `pip install "fastapi[standard-no-fastapi-cloud-cli]"`.

///

## Продвинутое руководство пользователя

Существует также **Продвинутое руководство пользователя**, которое вы сможете прочитать после руководства **Учебник - Руководство пользователя**.

**Продвинутое руководство пользователя** основано на этом, использует те же концепции и учит вас некоторым дополнительным функциям.

Но вы должны сначала прочитать **Учебник - Руководство пользователя** (то, что вы читаете прямо сейчас).

Он разработан таким образом, что вы можете создать полноценное приложение, используя только **Учебник - Руководство пользователя**, а затем расширить его различными способами, в зависимости от ваших потребностей, используя некоторые дополнительные идеи из **Продвинутого руководства пользователя**.
