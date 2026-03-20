# Серверные воркеры — Uvicorn с воркерами { #server-workers-uvicorn-with-workers }

Давайте снова вспомним те концепции деплоя, о которых говорили ранее:

* Безопасность — HTTPS
* Запуск при старте
* Перезапуски
* **Репликация (количество запущенных процессов)**
* Память
* Предварительные шаги перед запуском

До этого момента, следуя руководствам в документации, вы, вероятно, запускали **серверную программу**, например с помощью команды `fastapi`, которая запускает Uvicorn в **одном процессе**.

При деплое приложения вам, скорее всего, захочется использовать **репликацию процессов**, чтобы задействовать **несколько ядер** и иметь возможность обрабатывать больше запросов.

Как вы видели в предыдущей главе о [Концепциях деплоя](concepts.md), существует несколько стратегий.

Здесь я покажу, как использовать **Uvicorn** с **воркер-процессами** через команду `fastapi` или напрямую через команду `uvicorn`.

/// info | Информация

Если вы используете контейнеры, например Docker или Kubernetes, я расскажу об этом подробнее в следующей главе: [FastAPI в контейнерах — Docker](docker.md).

В частности, при запуске в **Kubernetes** вам, скорее всего, **не** понадобится использовать воркеры — вместо этого запускайте **один процесс Uvicorn на контейнер**, но об этом подробнее далее в той главе.

///

## Несколько воркеров { #multiple-workers }

Можно запустить несколько воркеров с помощью опции командной строки `--workers`:

//// tab | `fastapi`

Если вы используете команду `fastapi`:

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

Если вы предпочитаете использовать команду `uvicorn` напрямую:

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

Единственная новая опция здесь — `--workers`, она говорит Uvicorn запустить 4 воркер-процесса.

Также видно, что выводится **PID** каждого процесса: `27365` — для родительского процесса (это **менеджер процессов**) и по одному для каждого воркер-процесса: `27368`, `27369`, `27370` и `27367`.

## Концепции деплоя { #deployment-concepts }

Здесь вы увидели, как использовать несколько **воркеров**, чтобы **распараллелить** выполнение приложения, задействовать **несколько ядер** CPU и обслуживать **больше запросов**.

Из списка концепций деплоя выше использование воркеров в основном помогает с **репликацией**, и немного — с **перезапусками**, но об остальных по-прежнему нужно позаботиться:

* **Безопасность — HTTPS**
* **Запуск при старте**
* ***Перезапуски***
* Репликация (количество запущенных процессов)
* **Память**
* **Предварительные шаги перед запуском**

## Контейнеры и Docker { #containers-and-docker }

В следующей главе о [FastAPI в контейнерах — Docker](docker.md) я объясню стратегии, которые можно использовать для решения остальных **концепций деплоя**.

Я покажу, как **собрать свой образ с нуля**, чтобы запускать один процесс Uvicorn. Это простой подход и, вероятно, именно то, что вам нужно при использовании распределённой системы управления контейнерами, такой как **Kubernetes**.

## Резюме { #recap }

Вы можете использовать несколько воркер-процессов с опцией командной строки `--workers` в командах `fastapi` или `uvicorn`, чтобы задействовать **многоядерные CPU**, запуская **несколько процессов параллельно**.

Вы можете использовать эти инструменты и идеи, если настраиваете **собственную систему деплоя** и самостоятельно закрываете остальные концепции деплоя.

Перейдите к следующей главе, чтобы узнать о **FastAPI** в контейнерах (например, Docker и Kubernetes). Вы увидите, что эти инструменты тоже предлагают простые способы решить другие **концепции деплоя**. ✨
