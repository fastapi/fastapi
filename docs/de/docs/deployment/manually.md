# Einen Server manuell ausführen { #run-a-server-manually }

## Den `fastapi run`-Befehl verwenden { #use-the-fastapi-run-command }

Kurz gesagt, nutzen Sie `fastapi run`, um Ihre FastAPI-Anwendung bereitzustellen:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>2306215</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
```

</div>

Das würde in den meisten Fällen funktionieren. 😎

Sie könnten diesen Befehl beispielsweise verwenden, um Ihre **FastAPI**-App in einem Container, auf einem Server usw. zu starten.

## ASGI-Server { #asgi-servers }

Lassen Sie uns ein wenig tiefer in die Details eintauchen.

FastAPI verwendet einen Standard zum Erstellen von Python-Webframeworks und -Servern, der als <abbr title="Asynchrones Server-Gateway-Interface">ASGI</abbr> bekannt ist. FastAPI ist ein ASGI-Webframework.

Das Wichtigste, was Sie benötigen, um eine **FastAPI**-Anwendung (oder eine andere ASGI-Anwendung) auf einer entfernten Servermaschine auszuführen, ist ein ASGI-Serverprogramm wie **Uvicorn**, der standardmäßig im `fastapi`-Kommando enthalten ist.

Es gibt mehrere Alternativen, einschließlich:

* [Uvicorn](https://www.uvicorn.dev/): ein hochperformanter ASGI-Server.
* [Hypercorn](https://hypercorn.readthedocs.io/): ein ASGI-Server, der unter anderem kompatibel mit HTTP/2 und Trio ist.
* [Daphne](https://github.com/django/daphne): der für Django Channels entwickelte ASGI-Server.
* [Granian](https://github.com/emmett-framework/granian): Ein Rust HTTP-Server für Python-Anwendungen.
* [NGINX Unit](https://unit.nginx.org/howto/fastapi/): NGINX Unit ist eine leichte und vielseitige Laufzeitumgebung für Webanwendungen.

## Servermaschine und Serverprogramm { #server-machine-and-server-program }

Es gibt ein kleines Detail bei den Namen, das Sie beachten sollten. 💡

Das Wort „**Server**“ wird häufig verwendet, um sowohl den entfernten/Cloud-Computer (die physische oder virtuelle Maschine) als auch das Programm zu bezeichnen, das auf dieser Maschine läuft (z. B. Uvicorn).

Denken Sie einfach daran, dass sich „Server“ im Allgemeinen auf eines dieser beiden Dinge beziehen kann.

Wenn man sich auf die entfernte Maschine bezieht, wird sie üblicherweise als **Server**, aber auch als **Maschine**, **VM** (virtuelle Maschine) oder **Knoten** bezeichnet. Diese Begriffe beziehen sich auf irgendeine Art von entfernten Rechner, normalerweise unter Linux, auf dem Sie Programme ausführen.

## Das Serverprogramm installieren { #install-the-server-program }

Wenn Sie FastAPI installieren, wird es mit einem Produktionsserver, Uvicorn, geliefert, und Sie können ihn mit dem `fastapi run` Befehl starten.

Aber Sie können auch ein ASGI-Serverprogramm manuell installieren.

Stellen Sie sicher, dass Sie eine [virtuelle Umgebung](../virtual-environments.md) erstellen, sie aktivieren und dann die Serveranwendung installieren.

Zum Beispiel, um Uvicorn zu installieren:

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

Ein ähnlicher Prozess würde für jedes andere ASGI-Serverprogramm gelten.

/// tip | Tipp

Durch das Hinzufügen von `standard` installiert und verwendet Uvicorn einige empfohlene zusätzliche Abhängigkeiten.

Dazu gehört `uvloop`, der hochperformante Drop-in-Ersatz für `asyncio`, der den großen Nebenläufigkeits-Leistungsschub bietet.

Wenn Sie FastAPI mit etwas wie `pip install "fastapi[standard]"` installieren, erhalten Sie auch `uvicorn[standard]`.

///

## Das Serverprogramm ausführen { #run-the-server-program }

Wenn Sie einen ASGI-Server manuell installiert haben, müssen Sie normalerweise einen Importstring in einem speziellen Format übergeben, damit er Ihre FastAPI-Anwendung importiert:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note | Hinweis

Der Befehl `uvicorn main:app` bezieht sich auf:

* `main`: die Datei `main.py` (das Python-„Modul“).
* `app`: das Objekt, das innerhalb von `main.py` mit der Zeile `app = FastAPI()` erstellt wurde.

Es ist äquivalent zu:

```Python
from main import app
```

///

Jedes alternative ASGI-Serverprogramm hätte einen ähnlichen Befehl, Sie können in deren jeweiligen Dokumentationen mehr lesen.

/// warning | Achtung

Uvicorn und andere Server unterstützen eine `--reload`-Option, die während der Entwicklung nützlich ist.

Die `--reload`-Option verbraucht viel mehr Ressourcen, ist instabiler, usw.

Sie hilft während der **Entwicklung**, Sie sollten sie jedoch **nicht** in der **Produktion** verwenden.

///

## Deployment-Konzepte { #deployment-concepts }

Diese Beispiele führen das Serverprogramm (z. B. Uvicorn) aus, starten **einen einzelnen Prozess** und überwachen alle IPs (`0.0.0.0`) an einem vordefinierten Port (z. B. `80`).

Das ist die Grundidee. Aber Sie möchten sich wahrscheinlich um einige zusätzliche Dinge kümmern, wie zum Beispiel:

* Sicherheit – HTTPS
* Beim Hochfahren ausführen
* Neustarts
* Replikation (die Anzahl der laufenden Prozesse)
* Speicher
* Schritte vor dem Start

In den nächsten Kapiteln erzähle ich Ihnen mehr über jedes dieser Konzepte, wie Sie über diese nachdenken, und gebe Ihnen einige konkrete Beispiele mit Strategien für den Umgang damit. 🚀
