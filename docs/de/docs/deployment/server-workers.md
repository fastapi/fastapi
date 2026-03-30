# Serverworker – Uvicorn mit Workern { #server-workers-uvicorn-with-workers }

Schauen wir uns die Deployment-Konzepte von früher noch einmal an:

* Sicherheit – HTTPS
* Beim Hochfahren ausführen
* Neustarts
* **Replikation (die Anzahl der laufenden Prozesse)**
* Arbeitsspeicher
* Schritte vor dem Start

Bis zu diesem Punkt, in allen Tutorials in der Dokumentation, haben Sie wahrscheinlich ein **Serverprogramm** ausgeführt, zum Beispiel mit dem `fastapi`-Befehl, der Uvicorn startet, und einen **einzelnen Prozess** ausführt.

Wenn Sie Anwendungen deployen, möchten Sie wahrscheinlich eine gewisse **Replikation von Prozessen**, um **mehrere Kerne** zu nutzen und mehr <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Requests</abbr> bearbeiten zu können.

Wie Sie im vorherigen Kapitel über [Deployment-Konzepte](concepts.md) gesehen haben, gibt es mehrere Strategien, die Sie anwenden können.

Hier zeige ich Ihnen, wie Sie **Uvicorn** mit **Workerprozessen** verwenden, indem Sie den `fastapi`-Befehl oder den `uvicorn`-Befehl direkt verwenden.

/// info | Info

Wenn Sie Container verwenden, beispielsweise mit Docker oder Kubernetes, erzähle ich Ihnen mehr darüber im nächsten Kapitel: [FastAPI in Containern – Docker](docker.md).

Insbesondere wenn die Anwendung auf **Kubernetes** läuft, werden Sie wahrscheinlich **keine** Worker verwenden wollen, und stattdessen **einen einzelnen Uvicorn-Prozess pro Container** ausführen wollen, aber ich werde Ihnen später in diesem Kapitel mehr darüber erzählen.

///

## Mehrere Worker { #multiple-workers }

Sie können mehrere Worker mit der `--workers`-Befehlszeilenoption starten:

//// tab | `fastapi`

Wenn Sie den `fastapi`-Befehl verwenden:

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

Wenn Sie den `uvicorn`-Befehl direkt verwenden möchten:

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

Die einzige neue Option hier ist `--workers`, die Uvicorn anweist, 4 Workerprozesse zu starten.

Sie können auch sehen, dass die **PID** jedes Prozesses angezeigt wird, `27365` für den übergeordneten Prozess (dies ist der **Prozessmanager**) und eine für jeden Workerprozess: `27368`, `27369`, `27370` und `27367`.

## Deployment-Konzepte { #deployment-concepts }

Hier haben Sie gesehen, wie Sie mehrere **Worker** verwenden, um die Ausführung der Anwendung zu **parallelisieren**, **mehrere Kerne** der CPU zu nutzen und in der Lage zu sein, **mehr Requests** zu bearbeiten.

In der Liste der Deployment-Konzepte von oben würde die Verwendung von Workern hauptsächlich bei der **Replikation** und ein wenig bei **Neustarts** helfen, aber Sie müssen sich trotzdem um die anderen kümmern:

* **Sicherheit – HTTPS**
* **Beim Hochfahren ausführen**
* ***Neustarts***
* Replikation (die Anzahl der laufenden Prozesse)
* **Arbeitsspeicher**
* **Schritte vor dem Start**

## Container und Docker { #containers-and-docker }

Im nächsten Kapitel über [FastAPI in Containern – Docker](docker.md) werde ich einige Strategien erläutern, die Sie für den Umgang mit den anderen **Deployment-Konzepten** verwenden können.

Ich zeige Ihnen, wie Sie **Ihr eigenes Image von Grund auf erstellen**, um einen einzelnen Uvicorn-Prozess auszuführen. Es ist ein einfacher Vorgang und wahrscheinlich das, was Sie tun möchten, wenn Sie ein verteiltes Containerverwaltungssystem wie **Kubernetes** verwenden.

## Zusammenfassung { #recap }

Sie können mehrere Workerprozesse mit der `--workers`-CLI-Option über die `fastapi`- oder `uvicorn`-Befehle nutzen, um **Multikern-CPUs** auszunutzen und **mehrere Prozesse parallel** auszuführen.

Sie könnten diese Tools und Ideen nutzen, wenn Sie **Ihr eigenes Deployment-System** einrichten und sich dabei selbst um die anderen Deployment-Konzepte kümmern.

Schauen Sie sich das nächste Kapitel an, um mehr über **FastAPI** mit Containern (z. B. Docker und Kubernetes) zu erfahren. Sie werden sehen, dass diese Tools auch einfache Möglichkeiten bieten, die anderen **Deployment-Konzepte** zu lösen. ✨
