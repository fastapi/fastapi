# FastAPI CLI

**FastAPI CLI** ist ein Befehlszeilenprogramm, mit dem Sie Ihre FastAPI-Anwendung bedienen, Ihr FastAPI-Projekt verwalten und mehr tun können.

Wenn Sie FastAPI installieren (z. B. mit `pip install "fastapi[standard]"`), wird ein Package namens `fastapi-cli` eingeschlossen, dieses Package stellt den `fastapi`-Befehl im Terminal bereit.

Um Ihre FastAPI-Anwendung zur Entwicklung auszuführen, können Sie den Befehl `fastapi dev` verwenden:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Entwicklungsserver wird gestartet 🚀

             Suche nach Package-Dateistruktur in Verzeichnissen mit
             <font color="#3465A4">__init__.py</font> Dateien
             Import aus <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Das FastAPI-Anwendungsobjekt wird aus dem Modul mit dem
             folgenden Code importiert:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Verwenden des Import Strings: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server gestartet unter <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Dokumentation unter <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Läuft im Entwicklungsmodus, für die Produktion verwenden Sie:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Es wird auf Änderungen in diesen Verzeichnissen geachtet:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn läuft auf <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Drücken Sie STRG+C zum
             Beenden<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Reloader-Prozess wurde gestartet <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> unter Verwendung von WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Server-Prozess gestartet <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Warten auf den Start der Anwendung.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Anwendungsstart vollständig.
```

</div>

Das Befehlszeilenprogramm namens `fastapi` ist **FastAPI CLI**.

FastAPI CLI nimmt den Pfad zu Ihrem Python-Programm (z. B. `main.py`) entgegen und erkennt automatisch die `FastAPI`-Instanz (gewöhnlich `app` genannt), bestimmt den korrekten Importprozess und bedient sie dann.

Für die Produktion würden Sie stattdessen `fastapi run` verwenden. 🚀

Intern verwendet **FastAPI CLI** <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>, einen leistungsfähigen, produktionsbereiten, ASGI-Server. 😎

## `fastapi dev`

Das Ausführen von `fastapi dev` startet den Entwicklungsmodus.

Standardmäßig ist **auto-reload** aktiviert, was den Server automatisch neu lädt, wenn Sie Änderungen an Ihrem Code vornehmen. Dies ist ressourcenintensiv und könnte weniger stabil sein als wenn es deaktiviert ist. Sie sollten es nur zur Entwicklung verwenden. Es hört auch auf die IP-Adresse `127.0.0.1`, welche die IP für Ihren Rechner ist, um nur mit sich selbst zu kommunizieren (`localhost`).

## `fastapi run`

Das Ausführen von `fastapi run` startet FastAPI standardmäßig im Produktionsmodus.

Standardmäßig ist **auto-reload** deaktiviert. Es hört auch auf die IP-Adresse `0.0.0.0`, was alle verfügbaren IP-Adressen bedeutet, so dass es für jeden zugänglich ist, der mit dem Rechner kommunizieren kann. So würden Sie es normalerweise in der Herstellung betreiben, zum Beispiel in einem Container.

In den meisten Fällen hätten (und sollten) Sie einen „Termination Proxy“, der HTTPS für Sie oben handhabt; dies hängt davon ab, wie Sie Ihre Anwendung bereitstellen, Ihr Anbieter könnte dies für Sie tun, oder Sie müssen es selbst einrichten.

/// tip | Tipp

Sie können mehr darüber in der [Deployment-Dokumentation](deployment/index.md){.internal-link target=_blank} erfahren.

///
