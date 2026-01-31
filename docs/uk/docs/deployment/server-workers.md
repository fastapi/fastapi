# Воркери сервера — Uvicorn із воркерами { #server-workers-uvicorn-with-workers }

Повернімося до розглянутих раніше концепцій розгортання:

* Безпека — HTTPS
* Запуск під час старту системи
* Перезапуски
* **Реплікація (кількість запущених процесів)**
* Пам’ять
* Попередні кроки перед запуском

До цього моменту, з усіма навчальними матеріалами в документації, ви, ймовірно, запускали **серверну програму**, наприклад за допомогою команди `fastapi`, яка запускає Uvicorn, і працювали в **одному процесі**.

Під час розгортання застосунків вам, імовірно, захочеться мати певну **реплікацію процесів**, щоб використати переваги **кількох ядер** і мати змогу обробляти більше запитів.

Як ви бачили в попередньому розділі про [Концепції розгортання](concepts.md){.internal-link target=_blank}, існує кілька стратегій, які можна застосувати.

Тут я покажу, як використовувати **Uvicorn** із **воркер-процесами**, використовуючи команду `fastapi` або безпосередньо команду `uvicorn`.

/// info | Інформація

Якщо ви використовуєте контейнери, наприклад Docker або Kubernetes, я розповім про це докладніше в наступному розділі: [FastAPI у контейнерах — Docker](docker.md){.internal-link target=_blank}.

Зокрема, під час запуску в **Kubernetes** вам, імовірно, **не** варто використовувати воркери, а натомість запускати **один процес Uvicorn на контейнер**, але про це я розповім пізніше в тому розділі.

///

## Кілька воркерів { #multiple-workers }

Ви можете запустити кілька воркерів за допомогою опції командного рядка `--workers`:

//// tab | `fastapi`

Якщо ви використовуєте команду `fastapi`:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started parent process <b>[</b><font color="#34E2E2"><b>27365</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27368</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27369</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27370</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27367</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

////

//// tab | `uvicorn`

Якщо ви надаєте перевагу використанню команди `uvicorn` безпосередньо:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

</div>

////

Єдина нова опція тут — `--workers`, яка наказує Uvicorn запустити 4 воркер-процеси.

Також ви можете бачити, що він показує **PID** кожного процесу: `27365` для батьківського процесу (це **менеджер процесів**) і по одному для кожного воркер-процесу: `27368`, `27369`, `27370` та `27367`.

## Концепції розгортання { #deployment-concepts }

Тут ви побачили, як використовувати кілька **воркерів**, щоб **паралелізувати** виконання застосунку, використати переваги **кількох ядер** CPU та мати змогу обслуговувати **більше запитів**.

Із наведеного вище списку концепцій розгортання використання воркерів здебільшого допоможе з частиною **реплікації**, і трохи — з **перезапусками**, але про решту все одно потрібно подбати:

* **Безпека — HTTPS**
* **Запуск під час старту системи**
* ***Перезапуски***
* Реплікація (кількість запущених процесів)
* **Пам’ять**
* **Попередні кроки перед запуском**

## Контейнери та Docker { #containers-and-docker }

У наступному розділі про [FastAPI у контейнерах — Docker](docker.md){.internal-link target=_blank} я поясню деякі стратегії, які ви можете використати, щоб опрацювати інші **концепції розгортання**.

Я покажу вам, як **зібрати власний image з нуля**, щоб запускати один процес Uvicorn. Це простий процес і, ймовірно, саме те, що вам потрібно при використанні розподіленої системи керування контейнерами на кшталт **Kubernetes**.

## Підсумок { #recap }

Ви можете використовувати кілька воркер-процесів за допомогою CLI-опції `--workers` з командами `fastapi` або `uvicorn`, щоб скористатися перевагами **багатоядерних CPU** та запускати **кілька процесів паралельно**.

Ви можете застосувати ці інструменти та ідеї, якщо налаштовуєте **власну систему розгортання**, водночас самостійно дбаючи про інші концепції розгортання.

Перегляньте наступний розділ, щоб дізнатися про **FastAPI** з контейнерами (наприклад, Docker і Kubernetes). Ви побачите, що ці інструменти також мають прості способи розв’язати інші **концепції розгортання**. ✨
