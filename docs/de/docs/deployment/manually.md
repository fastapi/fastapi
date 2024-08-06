# Einen Server manuell ausführen – Uvicorn

Das Wichtigste, was Sie zum Ausführen einer **FastAPI**-Anwendung auf einer entfernten Servermaschine benötigen, ist ein ASGI-Serverprogramm, wie **Uvicorn**.

Es gibt 3 Hauptalternativen:

* <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>: ein hochperformanter ASGI-Server.
* <a href="https://hypercorn.readthedocs.io/" class="external-link" target="_blank">Hypercorn</a>: ein ASGI-Server, der unter anderem mit HTTP/2 und Trio kompatibel ist.
* <a href="https://github.com/django/daphne" class="external-link" target="_blank">Daphne</a>: Der für Django Channels entwickelte ASGI-Server.

## Servermaschine und Serverprogramm

Bei den Benennungen gibt es ein kleines Detail, das Sie beachten sollten. 💡

Das Wort „**Server**“ bezieht sich häufig sowohl auf den entfernten-/Cloud-Computer (die physische oder virtuelle Maschine) als auch auf das Programm, das auf dieser Maschine ausgeführt wird (z. B. Uvicorn).

Denken Sie einfach daran, wenn Sie „Server“ im Allgemeinen lesen, dass es sich auf eines dieser beiden Dinge beziehen kann.

Wenn man sich auf die entfernte Maschine bezieht, wird sie üblicherweise als **Server**, aber auch als **Maschine**, **VM** (virtuelle Maschine) oder **Knoten** bezeichnet. Diese Begriffe beziehen sich auf irgendeine Art von entfernten Rechner, normalerweise unter Linux, auf dem Sie Programme ausführen.

## Das Serverprogramm installieren

Sie können einen ASGI-kompatiblen Server installieren mit:

//// tab | Uvicorn

* <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>, ein blitzschneller ASGI-Server, basierend auf uvloop und httptools.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

/// tip | "Tipp"

Durch das Hinzufügen von `standard` installiert und verwendet Uvicorn einige empfohlene zusätzliche Abhängigkeiten.

Inklusive `uvloop`, einen hochperformanten Drop-in-Ersatz für `asyncio`, welcher für einen großen Leistungsschub bei der Nebenläufigkeit sorgt.

///

////

//// tab | Hypercorn

* <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>, ein ASGI-Server, der auch mit HTTP/2 kompatibel ist.

<div class="termy">

```console
$ pip install hypercorn

---> 100%
```

</div>

... oder jeden anderen ASGI-Server.

////

## Das Serverprogramm ausführen

Anschließend können Sie Ihre Anwendung auf die gleiche Weise ausführen, wie Sie es in den Tutorials getan haben, jedoch ohne die Option `--reload`, z. B.:

//// tab | Uvicorn

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

////

//// tab | Hypercorn

<div class="termy">

```console
$ hypercorn main:app --bind 0.0.0.0:80

Running on 0.0.0.0:8080 over http (CTRL + C to quit)
```

</div>

////

/// warning | "Achtung"

Denken Sie daran, die Option `--reload` zu entfernen, wenn Sie diese verwendet haben.

Die Option `--reload` verbraucht viel mehr Ressourcen, ist instabiler, usw.

Sie hilft sehr während der **Entwicklung**, aber Sie sollten sie **nicht** in der **Produktion** verwenden.

///

## Hypercorn mit Trio

Starlette und **FastAPI** basieren auf <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a>, welches diese sowohl mit der Python-Standardbibliothek <a href="https://docs.python.org/3/library/asyncio-task.html" class="external-link" target="_blank">asyncio</a>, als auch mit <a href="https://trio.readthedocs.io/en/stable/" class="external-link" target="_blank">Trio</a> kompatibel macht.

Dennoch ist Uvicorn derzeit nur mit asyncio kompatibel und verwendet normalerweise <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a>, den leistungsstarken Drop-in-Ersatz für `asyncio`.

Wenn Sie jedoch **Trio** direkt verwenden möchten, können Sie **Hypercorn** verwenden, da dieses es unterstützt. ✨

### Hypercorn mit Trio installieren

Zuerst müssen Sie Hypercorn mit Trio-Unterstützung installieren:

<div class="termy">

```console
$ pip install "hypercorn[trio]"
---> 100%
```

</div>

### Mit Trio ausführen

Dann können Sie die Befehlszeilenoption `--worker-class` mit dem Wert `trio` übergeben:

<div class="termy">

```console
$ hypercorn main:app --worker-class trio
```

</div>

Und das startet Hypercorn mit Ihrer Anwendung und verwendet Trio als Backend.

Jetzt können Sie Trio intern in Ihrer Anwendung verwenden. Oder noch besser: Sie können AnyIO verwenden, sodass Ihr Code sowohl mit Trio als auch asyncio kompatibel ist. 🎉

## Konzepte des Deployments

Obige Beispiele führen das Serverprogramm (z. B. Uvicorn) aus, starten **einen einzelnen Prozess** und überwachen alle IPs (`0.0.0.0`) an einem vordefinierten Port (z. B. `80`).

Das ist die Grundidee. Aber Sie möchten sich wahrscheinlich um einige zusätzliche Dinge kümmern, wie zum Beispiel:

* Sicherheit – HTTPS
* Beim Hochfahren ausführen
* Neustarts
* Replikation (die Anzahl der laufenden Prozesse)
* Arbeitsspeicher
* Schritte vor dem Start

In den nächsten Kapiteln erzähle ich Ihnen mehr über jedes dieser Konzepte, wie Sie über diese nachdenken, und gebe Ihnen einige konkrete Beispiele mit Strategien für den Umgang damit. 🚀
