# Навчальний посібник - Посібник користувача { #tutorial-user-guide }

У цьому посібнику показано, як користуватися **FastAPI** з більшістю його функцій, крок за кроком.

Кожен розділ поступово надбудовується на попередні, але він структурований на окремі теми, щоб ви могли перейти безпосередньо до будь-якої конкретної, щоб вирішити ваші конкретні потреби API.

Також він створений як довідник для роботи у майбутньому, тож ви можете повернутися і побачити саме те, що вам потрібно.

## Запустіть код { #run-the-code }

Усі блоки коду можна скопіювати та використовувати безпосередньо (це фактично перевірені файли Python).

Щоб запустити будь-який із прикладів, скопіюйте код у файл `main.py`, і запустіть `fastapi dev`:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

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

**ДУЖЕ радимо** написати або скопіювати код, відредагувати його та запустити локально.

Використання його у своєму редакторі – це те, що дійсно показує вам переваги FastAPI, бачите, як мало коду вам потрібно написати, всі перевірки типів, автозаповнення тощо.

---

## Встановлення FastAPI { #install-fastapi }

Першим кроком є встановлення FastAPI.

Переконайтеся, що ви створили [віртуальне середовище](../virtual-environments.md), активували його, а потім **встановіть FastAPI**:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note | Примітка

Коли ви встановлюєте через `pip install "fastapi[standard]"`, він постачається з деякими типовими необов’язковими стандартними залежностями, включно з `fastapi-cloud-cli`, який дозволяє розгортати в [FastAPI Cloud](https://fastapicloud.com).

Якщо ви не хочете мати ці необов’язкові залежності, натомість можете встановити `pip install fastapi`.

Якщо ви хочете встановити стандартні залежності, але без `fastapi-cloud-cli`, ви можете встановити через `pip install "fastapi[standard-no-fastapi-cloud-cli]"`.

///

/// tip | Порада

FastAPI має [офіційне розширення для VS Code](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode) (та Cursor), яке надає багато можливостей, включно з переглядачем операцій шляху, пошуком операцій шляху, навігацією CodeLens у тестах (перехід до визначення з тестів), а також розгортанням і журналами FastAPI Cloud — усе безпосередньо з вашого редактора.

///

## Просунутий посібник користувача { #advanced-user-guide }

Існує також **Просунутий посібник користувача**, який ви зможете прочитати пізніше після цього **Навчальний посібник - Посібник користувача**.

**Просунутий посібник користувача** засновано на цьому, використовує ті самі концепції та навчає вас деяким додатковим функціям.

Але вам слід спочатку прочитати **Навчальний посібник - Посібник користувача** (те, що ви зараз читаєте).

Він розроблений таким чином, що ви можете створити повну програму лише за допомогою **Навчальний посібник - Посібник користувача**, а потім розширити її різними способами, залежно від ваших потреб, використовуючи деякі з додаткових ідей з **Просунутого посібника користувача**.
