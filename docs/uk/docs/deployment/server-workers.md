# Працівники сервера - Uvicorn з працівниками { #server-workers-uvicorn-with-workers }

Повернімося до попередніх концепцій розгортання:

- Безпека - HTTPS
- Запуск під час старту
- Перезапуски
- Реплікація (кількість процесів, що виконуються)
- Пам'ять
- Попередні кроки перед запуском

До цього моменту, проходячи всі навчальні посібники в документації, ви, ймовірно, запускали серверну програму, наприклад, використовуючи команду `fastapi`, яка запускає Uvicorn у вигляді одного процесу.

Під час розгортання застосунків ви, найімовірніше, захочете мати реплікацію процесів, щоб використовувати кілька ядер і обробляти більше запитів.

Як ви бачили в попередньому розділі про [Концепції розгортання](concepts.md){.internal-link target=_blank}, існує кілька стратегій, які можна використовувати.

Тут я покажу, як використовувати Uvicorn із процесами-працівниками за допомогою команди `fastapi` або безпосередньо команди `uvicorn`.

/// info | Інформація

Якщо ви використовуєте контейнери, наприклад з Docker або Kubernetes, я розповім про це більше в наступному розділі: [FastAPI у контейнерах - Docker](docker.md){.internal-link target=_blank}.

Зокрема, під час запуску в Kubernetes вам, найімовірніше, не варто використовувати працівників, натомість запускати один процес Uvicorn на контейнер. Але про це я розповім пізніше в тому розділі.

///

## Кілька працівників { #multiple-workers }

Ви можете запустити кілька працівників за допомогою параметра командного рядка `--workers`:

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

Якщо ви віддаєте перевагу використовувати команду `uvicorn` безпосередньо:

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

Єдина нова опція тут — `--workers`, яка вказує Uvicorn запустити 4 процеси-працівники.

Також ви можете побачити, що виводиться PID кожного процесу: `27365` для батьківського процесу (це менеджер процесів) і по одному для кожного процесу-працівника: `27368`, `27369`, `27370` і `27367`.

## Концепції розгортання { #deployment-concepts }

Тут ви побачили, як використовувати кілька працівників, щоб паралелізувати виконання застосунку, використати кілька ядер процесора та обслуговувати більше запитів.

Із наведеного вище списку концепцій розгортання, використання працівників головним чином допоможе з частиною про реплікацію і трохи з перезапусками, але про інше все ще треба подбати:

- Безпека - HTTPS
- Запуск під час старту
- ***Перезапуски***
- Реплікація (кількість процесів, що виконуються)
- Пам'ять
- Попередні кроки перед запуском

## Контейнери і Docker { #containers-and-docker }

У наступному розділі про [FastAPI у контейнерах - Docker](docker.md){.internal-link target=_blank} я поясню кілька стратегій, які ви можете використати для інших концепцій розгортання.

Я покажу, як побудувати власний образ з нуля для запуску одного процесу Uvicorn. Це простий процес і, ймовірно, саме те, що потрібно при використанні розподіленої системи керування контейнерами, такої як Kubernetes.

## Підсумок { #recap }

Ви можете використовувати кілька процесів-працівників за допомогою параметра CLI `--workers` у командах `fastapi` або `uvicorn`, щоб скористатися перевагами багатоядерних процесорів і запускати кілька процесів паралельно.

Ви можете застосувати ці інструменти та ідеї, якщо налаштовуєте власну систему розгортання і самостійно дбаєте про інші концепції розгортання.

Перегляньте наступний розділ, щоб дізнатися про FastAPI з контейнерами (наприклад Docker і Kubernetes). Ви побачите, що ці інструменти також мають прості способи вирішити інші концепції розгортання. ✨
