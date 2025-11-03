# FastAPI CLI { #fastapi-cli }

**FastAPI CLI** ist ein Kommandozeilenprogramm, mit dem Sie Ihre FastAPI-App bereitstellen, Ihr FastAPI-Projekt verwalten und mehr.

Wenn Sie FastAPI installieren (z. B. mit `pip install "fastapi[standard]"`), wird ein Package namens `fastapi-cli` mitgeliefert, das den Befehl `fastapi` im Terminal bereitstellt.

Um Ihre FastAPI-App für die Entwicklung auszuführen, können Sie den Befehl `fastapi dev` verwenden:

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

Das Kommandozeilenprogramm namens `fastapi` ist das **FastAPI CLI**.

FastAPI CLI nimmt den Pfad zu Ihrem Python-Programm (z. B. `main.py`), erkennt automatisch die `FastAPI`-Instanz (häufig `app` genannt), bestimmt den korrekten Importprozess und stellt sie dann bereit.

Für die Produktion würden Sie stattdessen `fastapi run` verwenden. 🚀

Intern verwendet das **FastAPI CLI** <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>, einen leistungsstarken, produktionsreifen, ASGI-Server. 😎

## `fastapi dev` { #fastapi-dev }

Das Ausführen von `fastapi dev` startet den Entwicklermodus.

Standardmäßig ist **Autoreload** aktiviert, das den Server automatisch neu lädt, wenn Sie Änderungen an Ihrem Code vornehmen. Dies ist ressourcenintensiv und könnte weniger stabil sein als wenn es deaktiviert ist. Sie sollten es nur für die Entwicklung verwenden. Es horcht auch auf der IP-Adresse `127.0.0.1`, die die IP für Ihre Maschine ist, um nur mit sich selbst zu kommunizieren (`localhost`).

## `fastapi run` { #fastapi-run }

Das Ausführen von `fastapi run` startet FastAPI standardmäßig im Produktionsmodus.

Standardmäßig ist **Autoreload** deaktiviert. Es horcht auch auf der IP-Adresse `0.0.0.0`, was alle verfügbaren IP-Adressen bedeutet, so wird es öffentlich zugänglich für jeden, der mit der Maschine kommunizieren kann. So würden Sie es normalerweise in der Produktion ausführen, beispielsweise in einem Container.

In den meisten Fällen würden (und sollten) Sie einen „Terminierungsproxy“ haben, der HTTPS für Sie verwaltet. Dies hängt davon ab, wie Sie Ihre Anwendung bereitstellen. Ihr Anbieter könnte dies für Sie erledigen, oder Sie müssen es selbst einrichten.

/// tip | Tipp

Sie können mehr darüber in der [Deployment-Dokumentation](deployment/index.md){.internal-link target=_blank} erfahren.

///
