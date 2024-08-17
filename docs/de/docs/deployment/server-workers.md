# Serverworker – Gunicorn mit Uvicorn

Schauen wir uns die Deployment-Konzepte von früher noch einmal an:

* Sicherheit – HTTPS
* Beim Hochfahren ausführen
* Neustarts
* **Replikation (die Anzahl der laufenden Prozesse)**
* Arbeitsspeicher
* Schritte vor dem Start

Bis zu diesem Punkt, in allen Tutorials in der Dokumentation, haben Sie wahrscheinlich ein **Serverprogramm** wie Uvicorn ausgeführt, in einem **einzelnen Prozess**.

Wenn Sie Anwendungen bereitstellen, möchten Sie wahrscheinlich eine gewisse **Replikation von Prozessen**, um **mehrere CPU-Kerne** zu nutzen und mehr Requests bearbeiten zu können.

Wie Sie im vorherigen Kapitel über [Deployment-Konzepte](concepts.md){.internal-link target=_blank} gesehen haben, gibt es mehrere Strategien, die Sie anwenden können.

Hier zeige ich Ihnen, wie Sie <a href="https://gunicorn.org/" class="external-link" target="_blank">**Gunicorn**</a> mit **Uvicorn Workerprozessen** verwenden.

/// info

Wenn Sie Container verwenden, beispielsweise mit Docker oder Kubernetes, erzähle ich Ihnen mehr darüber im nächsten Kapitel: [FastAPI in Containern – Docker](docker.md){.internal-link target=_blank}.

Insbesondere wenn die Anwendung auf **Kubernetes** läuft, werden Sie Gunicorn wahrscheinlich **nicht** verwenden wollen und stattdessen **einen einzelnen Uvicorn-Prozess pro Container** ausführen wollen, aber ich werde Ihnen später in diesem Kapitel mehr darüber erzählen.

///

## Gunicorn mit Uvicorn-Workern

**Gunicorn** ist hauptsächlich ein Anwendungsserver, der den **WSGI-Standard** verwendet. Das bedeutet, dass Gunicorn Anwendungen wie Flask und Django ausliefern kann. Gunicorn selbst ist nicht mit **FastAPI** kompatibel, da FastAPI den neuesten **<a href="https://asgi.readthedocs.io/en/latest/" class="external-link" target="_blank">ASGI-Standard</a>** verwendet.

Aber Gunicorn kann als **Prozessmanager** arbeiten und Benutzer können ihm mitteilen, welche bestimmte **Workerprozessklasse** verwendet werden soll. Dann würde Gunicorn einen oder mehrere **Workerprozesse** starten, diese Klasse verwendend.

Und **Uvicorn** hat eine **Gunicorn-kompatible Workerklasse**.

Mit dieser Kombination würde Gunicorn als **Prozessmanager** fungieren und den **Port** und die **IP** abhören. Und er würde die Kommunikation an die Workerprozesse **weiterleiten**, welche die **Uvicorn-Klasse** ausführen.

Und dann wäre die Gunicorn-kompatible **Uvicorn-Worker**-Klasse dafür verantwortlich, die von Gunicorn gesendeten Daten in den ASGI-Standard zu konvertieren, damit FastAPI diese verwenden kann.

## Gunicorn und Uvicorn installieren

<div class="termy">

```console
$ pip install "uvicorn[standard]" gunicorn

---> 100%
```

</div>

Dadurch wird sowohl Uvicorn mit zusätzlichen `standard`-Packages (um eine hohe Leistung zu erzielen) als auch Gunicorn installiert.

## Gunicorn mit Uvicorn-Workern ausführen

Dann können Sie Gunicorn ausführen mit:

<div class="termy">

```console
$ gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80

[19499] [INFO] Starting gunicorn 20.1.0
[19499] [INFO] Listening at: http://0.0.0.0:80 (19499)
[19499] [INFO] Using worker: uvicorn.workers.UvicornWorker
[19511] [INFO] Booting worker with pid: 19511
[19513] [INFO] Booting worker with pid: 19513
[19514] [INFO] Booting worker with pid: 19514
[19515] [INFO] Booting worker with pid: 19515
[19511] [INFO] Started server process [19511]
[19511] [INFO] Waiting for application startup.
[19511] [INFO] Application startup complete.
[19513] [INFO] Started server process [19513]
[19513] [INFO] Waiting for application startup.
[19513] [INFO] Application startup complete.
[19514] [INFO] Started server process [19514]
[19514] [INFO] Waiting for application startup.
[19514] [INFO] Application startup complete.
[19515] [INFO] Started server process [19515]
[19515] [INFO] Waiting for application startup.
[19515] [INFO] Application startup complete.
```

</div>

Sehen wir uns an, was jede dieser Optionen bedeutet:

* `main:app`: Das ist die gleiche Syntax, die auch von Uvicorn verwendet wird. `main` bedeutet das Python-Modul mit dem Namen `main`, also eine Datei `main.py`. Und `app` ist der Name der Variable, welche die **FastAPI**-Anwendung ist.
    * Stellen Sie sich einfach vor, dass `main:app` einer Python-`import`-Anweisung wie der folgenden entspricht:

        ```Python
        from main import app
        ```

    * Der Doppelpunkt in `main:app` entspricht also dem Python-`import`-Teil in `from main import app`.

* `--workers`: Die Anzahl der zu verwendenden Workerprozesse, jeder führt einen Uvicorn-Worker aus, in diesem Fall 4 Worker.

* `--worker-class`: Die Gunicorn-kompatible Workerklasse zur Verwendung in den Workerprozessen.
    * Hier übergeben wir die Klasse, die Gunicorn etwa so importiert und verwendet:

        ```Python
        import uvicorn.workers.UvicornWorker
        ```

* `--bind`: Das teilt Gunicorn die IP und den Port mit, welche abgehört werden sollen, wobei ein Doppelpunkt (`:`) verwendet wird, um die IP und den Port zu trennen.
    * Wenn Sie Uvicorn direkt ausführen würden, würden Sie anstelle von `--bind 0.0.0.0:80` (die Gunicorn-Option) stattdessen `--host 0.0.0.0` und `--port 80` verwenden.

In der Ausgabe können Sie sehen, dass die **PID** (Prozess-ID) jedes Prozesses angezeigt wird (es ist nur eine Zahl).

Sie können sehen, dass:

* Der Gunicorn **Prozessmanager** beginnt, mit der PID `19499` (in Ihrem Fall ist es eine andere Nummer).
* Dann beginnt er zu lauschen: `Listening at: http://0.0.0.0:80`.
* Dann erkennt er, dass er die Workerklasse `uvicorn.workers.UvicornWorker` verwenden muss.
* Und dann werden **4 Worker** gestartet, jeder mit seiner eigenen PID: `19511`, `19513`, `19514` und `19515`.

Gunicorn würde sich bei Bedarf auch um die Verwaltung **beendeter Prozesse** und den **Neustart** von Prozessen kümmern, um die Anzahl der Worker aufrechtzuerhalten. Das hilft also teilweise beim **Neustarts**-Konzept aus der obigen Liste.

Dennoch möchten Sie wahrscheinlich auch etwas außerhalb haben, um sicherzustellen, dass Gunicorn bei Bedarf **neu gestartet wird**, und er auch **beim Hochfahren ausgeführt wird**, usw.

## Uvicorn mit Workern

Uvicorn bietet ebenfalls die Möglichkeit, mehrere **Workerprozesse** zu starten und auszuführen.

Dennoch sind die Fähigkeiten von Uvicorn zur Abwicklung von Workerprozessen derzeit eingeschränkter als die von Gunicorn. Wenn Sie also einen Prozessmanager auf dieser Ebene (auf der Python-Ebene) haben möchten, ist es vermutlich besser, es mit Gunicorn als Prozessmanager zu versuchen.

Wie auch immer, Sie würden es so ausführen:

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

Die einzige neue Option hier ist `--workers`, die Uvicorn anweist, 4 Workerprozesse zu starten.

Sie können auch sehen, dass die **PID** jedes Prozesses angezeigt wird, `27365` für den übergeordneten Prozess (dies ist der **Prozessmanager**) und eine für jeden Workerprozess: `27368`, `27369`, `27370` und `27367`.

## Deployment-Konzepte

Hier haben Sie gesehen, wie Sie mit **Gunicorn** (oder Uvicorn) **Uvicorn-Workerprozesse** verwalten, um die Ausführung der Anwendung zu **parallelisieren**, **mehrere Kerne** der CPU zu nutzen und in der Lage zu sein, **mehr Requests** zu bedienen.

In der Liste der Deployment-Konzepte von oben würde die Verwendung von Workern hauptsächlich beim **Replikation**-Teil und ein wenig bei **Neustarts** helfen, aber Sie müssen sich trotzdem um die anderen kümmern:

* **Sicherheit – HTTPS**
* **Beim Hochfahren ausführen**
* **Neustarts**
* Replikation (die Anzahl der laufenden Prozesse)
* **Arbeitsspeicher**
* **Schritte vor dem Start**

## Container und Docker

Im nächsten Kapitel über [FastAPI in Containern – Docker](docker.md){.internal-link target=_blank} werde ich einige Strategien erläutern, die Sie für den Umgang mit den anderen **Deployment-Konzepten** verwenden können.

Ich zeige Ihnen auch das **offizielle Docker-Image**, welches **Gunicorn mit Uvicorn-Workern** und einige Standardkonfigurationen enthält, die für einfache Fälle nützlich sein können.

Dort zeige ich Ihnen auch, wie Sie **Ihr eigenes Image von Grund auf erstellen**, um einen einzelnen Uvicorn-Prozess (ohne Gunicorn) auszuführen. Es ist ein einfacher Vorgang und wahrscheinlich das, was Sie tun möchten, wenn Sie ein verteiltes Containerverwaltungssystem wie **Kubernetes** verwenden.

## Zusammenfassung

Sie können **Gunicorn** (oder auch Uvicorn) als Prozessmanager mit Uvicorn-Workern verwenden, um **Multikern-CPUs** zu nutzen und **mehrere Prozesse parallel** auszuführen.

Sie können diese Tools und Ideen nutzen, wenn Sie **Ihr eigenes Deployment-System** einrichten und sich dabei selbst um die anderen Deployment-Konzepte kümmern.

Schauen Sie sich das nächste Kapitel an, um mehr über **FastAPI** mit Containern (z. B. Docker und Kubernetes) zu erfahren. Sie werden sehen, dass diese Tools auch einfache Möglichkeiten bieten, die anderen **Deployment-Konzepte** zu lösen. ✨
