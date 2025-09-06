# FastAPI in Containern – Docker { #fastapi-in-containers-docker }

Beim Deployment von FastAPI-Anwendungen besteht ein gängiger Ansatz darin, ein **Linux-Containerimage** zu erstellen. Normalerweise erfolgt dies mit <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a>. Sie können dieses Containerimage dann auf eine von mehreren möglichen Arten bereitstellen.

Die Verwendung von Linux-Containern bietet mehrere Vorteile, darunter **Sicherheit**, **Replizierbarkeit**, **Einfachheit** und andere.

/// tip | Tipp

Sie haben es eilig und kennen sich bereits aus? Springen Sie zum [`Dockerfile` unten 👇](#build-a-docker-image-for-fastapi).

///

<details>
<summary>Dockerfile-Vorschau 👀</summary>

```Dockerfile
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# Wenn Sie hinter einem Proxy wie Nginx oder Traefik sind, fügen Sie --proxy-headers hinzu
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

</details>

## Was ist ein Container { #what-is-a-container }

Container (hauptsächlich Linux-Container) sind eine sehr **leichtgewichtige** Möglichkeit, Anwendungen einschließlich aller ihrer Abhängigkeiten und erforderlichen Dateien zu verpacken und sie gleichzeitig von anderen Containern (anderen Anwendungen oder Komponenten) im selben System isoliert zu halten.

Linux-Container werden mit demselben Linux-Kernel des Hosts (Maschine, virtuellen Maschine, Cloud-Servers, usw.) ausgeführt. Das bedeutet einfach, dass sie sehr leichtgewichtig sind (im Vergleich zu vollständigen virtuellen Maschinen, die ein gesamtes Betriebssystem emulieren).

Auf diese Weise verbrauchen Container **wenig Ressourcen**, eine Menge vergleichbar mit der direkten Ausführung der Prozesse (eine virtuelle Maschine würde viel mehr verbrauchen).

Container verfügen außerdem über ihre eigenen **isoliert** laufenden Prozesse (üblicherweise nur einen Prozess), über ihr eigenes Dateisystem und ihr eigenes Netzwerk, was die Bereitstellung, Sicherheit, Entwicklung usw. vereinfacht.

## Was ist ein Containerimage { #what-is-a-container-image }

Ein **Container** wird von einem **Containerimage** ausgeführt.

Ein Containerimage ist eine **statische** Version aller Dateien, Umgebungsvariablen und des Standardbefehls/-programms, welche in einem Container vorhanden sein sollten. **Statisch** bedeutet hier, dass das Container-**Image** nicht läuft, nicht ausgeführt wird, sondern nur die gepackten Dateien und Metadaten enthält.

Im Gegensatz zu einem „**Containerimage**“, bei dem es sich um den gespeicherten statischen Inhalt handelt, bezieht sich ein „**Container**“ normalerweise auf die laufende Instanz, das Ding, das **ausgeführt** wird.

Wenn der **Container** gestartet und ausgeführt wird (gestartet von einem **Containerimage**), kann er Dateien, Umgebungsvariablen usw. erstellen oder ändern. Diese Änderungen sind nur in diesem Container vorhanden, nicht im zugrunde liegenden Containerimage (werden nicht auf der Festplatte gespeichert).

Ein Containerimage ist vergleichbar mit der **Programmdatei** und ihrem Inhalt, z. B. `python` und eine Datei `main.py`.

Und der **Container** selbst (im Gegensatz zum **Containerimage**) ist die tatsächlich laufende Instanz des Images, vergleichbar mit einem **Prozess**. Tatsächlich läuft ein Container nur, wenn er einen **laufenden Prozess** hat (und normalerweise ist es nur ein einzelner Prozess). Der Container stoppt, wenn kein Prozess darin ausgeführt wird.

## Containerimages { #container-images }

Docker ist eines der wichtigsten Tools zum Erstellen und Verwalten von **Containerimages** und **Containern**.

Und es gibt einen öffentlichen <a href="https://hub.docker.com/" class="external-link" target="_blank">Docker <abbr title="Umschlagplatz">Hub</abbr></a> mit vorgefertigten **offiziellen Containerimages** für viele Tools, Umgebungen, Datenbanken und Anwendungen.

Beispielsweise gibt es ein offizielles <a href="https://hub.docker.com/_/python" class="external-link" target="_blank">Python-Image</a>.

Und es gibt viele andere Images für verschiedene Dinge wie Datenbanken, zum Beispiel für:

* <a href="https://hub.docker.com/_/postgres" class="external-link" target="_blank">PostgreSQL</a>
* <a href="https://hub.docker.com/_/mysql" class="external-link" target="_blank">MySQL</a>
* <a href="https://hub.docker.com/_/mongo" class="external-link" target="_blank">MongoDB</a>
* <a href="https://hub.docker.com/_/redis" class="external-link" target="_blank">Redis</a>, usw.

Durch die Verwendung eines vorgefertigten Containerimages ist es sehr einfach, verschiedene Tools zu **kombinieren** und zu verwenden. Zum Beispiel, um eine neue Datenbank auszuprobieren. In den meisten Fällen können Sie die **offiziellen Images** verwenden und diese einfach mit Umgebungsvariablen konfigurieren.

Auf diese Weise können Sie in vielen Fällen etwas über Container und Docker lernen und dieses Wissen mit vielen verschiedenen Tools und Komponenten wiederverwenden.

Sie würden also **mehrere Container** mit unterschiedlichen Dingen ausführen, wie einer Datenbank, einer Python-Anwendung, einem Webserver mit einer React-Frontend-Anwendung, und diese über ihr internes Netzwerk miteinander verbinden.

In alle Containerverwaltungssysteme (wie Docker oder Kubernetes) sind diese Netzwerkfunktionen integriert.

## Container und Prozesse { #containers-and-processes }

Ein **Containerimage** enthält normalerweise in seinen Metadaten das Standardprogramm oder den Standardbefehl, der ausgeführt werden soll, wenn der **Container** gestartet wird, sowie die Parameter, die an dieses Programm übergeben werden sollen. Sehr ähnlich zu dem, was wäre, wenn es über die Befehlszeile gestartet werden würde.

Wenn ein **Container** gestartet wird, führt er diesen Befehl/dieses Programm aus (Sie können ihn jedoch überschreiben und einen anderen Befehl/ein anderes Programm ausführen lassen).

Ein Container läuft, solange der **Hauptprozess** (Befehl oder Programm) läuft.

Ein Container hat normalerweise einen **einzelnen Prozess**, aber es ist auch möglich, Unterprozesse vom Hauptprozess aus zu starten, und auf diese Weise haben Sie **mehrere Prozesse** im selben Container.

Es ist jedoch nicht möglich, einen laufenden Container, ohne **mindestens einen laufenden Prozess** zu haben. Wenn der Hauptprozess stoppt, stoppt der Container.

## Ein Docker-Image für FastAPI erstellen { #build-a-docker-image-for-fastapi }

Okay, wollen wir jetzt etwas bauen! 🚀

Ich zeige Ihnen, wie Sie ein **Docker-Image** für FastAPI **von Grund auf** erstellen, basierend auf dem **offiziellen Python**-Image.

Das ist, was Sie in **den meisten Fällen** tun möchten, zum Beispiel:

* Bei Verwendung von **Kubernetes** oder ähnlichen Tools
* Beim Betrieb auf einem **Raspberry Pi**
* Bei Verwendung eines Cloud-Dienstes, der ein Containerimage für Sie ausführt, usw.

### Paketanforderungen { #package-requirements }

Normalerweise befinden sich die **Paketanforderungen** für Ihre Anwendung in einer Datei.

Dies hängt hauptsächlich von dem Tool ab, mit dem Sie diese Anforderungen **installieren**.

Die gebräuchlichste Methode besteht darin, eine Datei `requirements.txt` mit den Namen der Packages und deren Versionen zu erstellen, eine pro Zeile.

Sie würden natürlich die gleichen Ideen verwenden, die Sie in [Über FastAPI-Versionen](versions.md){.internal-link target=_blank} gelesen haben, um die Versionsbereiche festzulegen.

Ihre `requirements.txt` könnte beispielsweise so aussehen:

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

Und normalerweise würden Sie diese Paketabhängigkeiten mit `pip` installieren, zum Beispiel:

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

</div>

/// info | Info

Es gibt andere Formate und Tools zum Definieren und Installieren von Paketabhängigkeiten.

///

### Den **FastAPI**-Code erstellen { #create-the-fastapi-code }

* Erstellen Sie ein `app`-Verzeichnis und betreten Sie es.
* Erstellen Sie eine leere Datei `__init__.py`.
* Erstellen Sie eine `main.py`-Datei mit:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile { #dockerfile }

Erstellen Sie nun im selben Projektverzeichnis eine Datei `Dockerfile` mit:

```{ .dockerfile .annotate }
# (1)!
FROM python:3.9

# (2)!
WORKDIR /code

# (3)!
COPY ./requirements.txt /code/requirements.txt

# (4)!
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)!
COPY ./app /code/app

# (6)!
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

1. Beginne mit dem offiziellen Python-Basisimage.

2. Setze das aktuelle Arbeitsverzeichnis auf `/code`.

    Hier platzieren wir die Datei `requirements.txt` und das Verzeichnis `app`.

3. Kopiere die Datei mit den Paketanforderungen in das Verzeichnis `/code`.

    Kopieren Sie zuerst **nur** die Datei mit den Anforderungen, nicht den Rest des Codes.

    Da sich diese Datei **nicht oft ändert**, erkennt Docker das und verwendet den **Cache** für diesen Schritt, wodurch der Cache auch für den nächsten Schritt aktiviert wird.

4. Installiere die Paketabhängigkeiten aus der Anforderungsdatei.

    Die Option `--no-cache-dir` weist `pip` an, die heruntergeladenen Pakete nicht lokal zu speichern, da dies nur benötigt wird, sollte `pip` erneut ausgeführt werden, um dieselben Pakete zu installieren, aber das ist beim Arbeiten mit Containern nicht der Fall.

    /// note | Hinweis

    Das `--no-cache-dir` bezieht sich nur auf `pip`, es hat nichts mit Docker oder Containern zu tun.

    ///

    Die Option `--upgrade` weist `pip` an, die Packages zu aktualisieren, wenn sie bereits installiert sind.

    Da der vorherige Schritt des Kopierens der Datei vom **Docker-Cache** erkannt werden konnte, wird dieser Schritt auch **den Docker-Cache verwenden**, sofern verfügbar.

    Durch die Verwendung des Caches in diesem Schritt **sparen** Sie viel **Zeit**, wenn Sie das Image während der Entwicklung immer wieder erstellen, anstatt **jedes Mal** alle Abhängigkeiten **herunterzuladen und zu installieren**.

5. Kopiere das Verzeichnis `./app` in das Verzeichnis `/code`.

    Da hier der gesamte Code enthalten ist, der sich **am häufigsten ändert**, wird der Docker-**Cache** nicht ohne weiteres für diesen oder andere **folgende Schritte** verwendet.

    Daher ist es wichtig, dies **nahe dem Ende** des `Dockerfile`s zu platzieren, um die Erstellungszeiten des Containerimages zu optimieren.

6. Lege den **Befehl** fest, um `fastapi run` zu nutzen, welches Uvicorn darunter verwendet.

    `CMD` nimmt eine Liste von Zeichenfolgen entgegen. Jede dieser Zeichenfolgen entspricht dem, was Sie durch Leerzeichen getrennt in die Befehlszeile eingeben würden.

    Dieser Befehl wird aus dem **aktuellen Arbeitsverzeichnis** ausgeführt, dem gleichen `/code`-Verzeichnis, das Sie oben mit `WORKDIR /code` festgelegt haben.

/// tip | Tipp

Lernen Sie, was jede Zeile bewirkt, indem Sie auf die Zahlenblasen im Code klicken. 👆

///

/// warning | Achtung

Stellen Sie sicher, dass Sie **immer** die **exec form** der Anweisung `CMD` verwenden, wie unten erläutert.

///

#### `CMD` – Exec Form verwenden { #use-cmd-exec-form }

Die <a href="https://docs.docker.com/reference/dockerfile/#cmd" class="external-link" target="_blank">`CMD`</a> Docker-Anweisung kann in zwei Formen geschrieben werden:

✅ **Exec** form:

```Dockerfile
# ✅ Tun Sie das
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ **Shell** form:

```Dockerfile
# ⛔️ Tun Sie das nicht
CMD fastapi run app/main.py --port 80
```

Achten Sie darauf, stets die **exec** form zu verwenden, um sicherzustellen, dass FastAPI ordnungsgemäß heruntergefahren wird und [Lifespan-Events](../advanced/events.md){.internal-link target=_blank} ausgelöst werden.

Sie können mehr darüber in der <a href="https://docs.docker.com/reference/dockerfile/#shell-and-exec-form" class="external-link" target="_blank">Docker-Dokumentation für Shell und Exec Form lesen</a>.

Dies kann insbesondere bei der Verwendung von `docker compose` deutlich spürbar sein. Sehen Sie sich diesen Abschnitt in der Docker Compose-FAQ für technische Details an: <a href="https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop" class="external-link" target="_blank">Warum benötigen meine Dienste 10 Sekunden, um neu erstellt oder gestoppt zu werden?</a>.

#### Verzeichnisstruktur { #directory-structure }

Sie sollten jetzt eine Verzeichnisstruktur wie diese haben:

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### Hinter einem TLS-Terminierungsproxy { #behind-a-tls-termination-proxy }

Wenn Sie Ihren Container hinter einem TLS-Terminierungsproxy (Load Balancer) wie Nginx oder Traefik ausführen, fügen Sie die Option `--proxy-headers` hinzu. Das sagt Uvicorn (durch das FastAPI CLI), den von diesem Proxy gesendeten Headern zu vertrauen und dass die Anwendung hinter HTTPS ausgeführt wird, usw.

```Dockerfile
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### Docker-Cache { #docker-cache }

In diesem `Dockerfile` gibt es einen wichtigen Trick: Wir kopieren zuerst die **Datei nur mit den Abhängigkeiten**, nicht den Rest des Codes. Lassen Sie mich Ihnen erklären, warum.

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Docker und andere Tools **erstellen** diese Containerimages **inkrementell**, fügen **eine Ebene über der anderen** hinzu, beginnend am Anfang des `Dockerfile`s und fügen alle durch die einzelnen Anweisungen des `Dockerfile`s erstellten Dateien hinzu.

Docker und ähnliche Tools verwenden beim Erstellen des Images auch einen **internen Cache**. Wenn sich eine Datei seit der letzten Erstellung des Containerimages nicht geändert hat, wird **dieselbe Ebene wiederverwendet**, die beim letzten Mal erstellt wurde, anstatt die Datei erneut zu kopieren und eine neue Ebene von Grund auf zu erstellen.

Das bloße Vermeiden des Kopierens von Dateien führt nicht unbedingt zu einer großen Verbesserung, aber da der Cache für diesen Schritt verwendet wurde, kann **der Cache für den nächsten Schritt verwendet werden**. Beispielsweise könnte der Cache verwendet werden für die Anweisung, welche die Abhängigkeiten installiert mit:

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

Die Datei mit den Paketanforderungen wird sich **nicht häufig ändern**. Wenn Docker also nur diese Datei kopiert, kann es für diesen Schritt **den Cache verwenden**.

Und dann kann Docker **den Cache für den nächsten Schritt verwenden**, der diese Abhängigkeiten herunterlädt und installiert. Und hier **sparen wir viel Zeit**. ✨ ... und vermeiden die Langeweile beim Warten. 😪😆

Das Herunterladen und Installieren der Paketabhängigkeiten **könnte Minuten dauern**, aber die Verwendung des **Cache** würde höchstens **Sekunden** dauern.

Und da Sie das Containerimage während der Entwicklung immer wieder erstellen würden, um zu überprüfen, ob Ihre Codeänderungen funktionieren, würde dies viel Zeit sparen.

Dann, gegen Ende des `Dockerfile`s, kopieren wir den gesamten Code. Da sich der **am häufigsten ändert**, platzieren wir das am Ende, da fast immer alles nach diesem Schritt nicht mehr in der Lage sein wird, den Cache zu verwenden.

```Dockerfile
COPY ./app /code/app
```

### Das Docker-Image erstellen { #build-the-docker-image }

Nachdem nun alle Dateien vorhanden sind, erstellen wir das Containerimage.

* Gehen Sie zum Projektverzeichnis (dort, wo sich Ihr `Dockerfile` und Ihr `app`-Verzeichnis befindet).
* Erstellen Sie Ihr FastAPI-Image:

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

/// tip | Tipp

Beachten Sie das `.` am Ende, es entspricht `./` und teilt Docker mit, welches Verzeichnis zum Erstellen des Containerimages verwendet werden soll.

In diesem Fall handelt es sich um dasselbe aktuelle Verzeichnis (`.`).

///

### Den Docker-Container starten { #start-the-docker-container }

* Führen Sie einen Container basierend auf Ihrem Image aus:

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## Es testen { #check-it }

Sie sollten es in der URL Ihres Docker-Containers überprüfen können, zum Beispiel: <a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> oder <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a> (oder gleichwertig, unter Verwendung Ihres Docker-Hosts).

Sie werden etwas sehen wie:

```JSON
{"item_id": 5, "q": "somequery"}
```

## Interaktive API-Dokumentation { #interactive-api-docs }

Jetzt können Sie auf <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> oder <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a> gehen (oder ähnlich, unter Verwendung Ihres Docker-Hosts).

Sie sehen die automatische interaktive API-Dokumentation (bereitgestellt von <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger-Oberfläche](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## Alternative API-Dokumentation { #alternative-api-docs }

Sie können auch auf <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> oder <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a> gehen (oder ähnlich, unter Verwendung Ihres Docker-Hosts).

Sie sehen die alternative automatische Dokumentation (bereitgestellt von <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Ein Docker-Image mit einem Single-File-FastAPI erstellen { #build-a-docker-image-with-a-single-file-fastapi }

Wenn Ihr FastAPI eine einzelne Datei ist, zum Beispiel `main.py` ohne ein `./app`-Verzeichnis, könnte Ihre Dateistruktur wie folgt aussehen:

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

Dann müssten Sie nur noch die entsprechenden Pfade ändern, um die Datei im `Dockerfile` zu kopieren:

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)!
COPY ./main.py /code/

# (2)!
CMD ["fastapi", "run", "main.py", "--port", "80"]
```

1. Kopiere die Datei `main.py` direkt in das Verzeichnis `/code` (ohne ein Verzeichnis `./app`).

2. Verwenden Sie `fastapi run`, um Ihre Anwendung in der einzelnen Datei `main.py` bereitzustellen.

Indem Sie die Datei an `fastapi run` übergeben, wird automatisch erkannt, dass es sich um eine einzelne Datei handelt und nicht um den Teil eines Packages, und es wird wissen, wie es zu importieren ist und Ihre FastAPI-App bereitzustellen. 😎

## Deployment-Konzepte { #deployment-concepts }

Lassen Sie uns noch einmal über einige der gleichen [Deployment-Konzepte](concepts.md){.internal-link target=_blank} in Bezug auf Container sprechen.

Container sind hauptsächlich ein Werkzeug, um den Prozess des **Erstellens und Deployments** einer Anwendung zu vereinfachen, sie erzwingen jedoch keinen bestimmten Ansatz für die Handhabung dieser **Deployment-Konzepte**, und es gibt mehrere mögliche Strategien.

Die **gute Nachricht** ist, dass es mit jeder unterschiedlichen Strategie eine Möglichkeit gibt, alle Deployment-Konzepte abzudecken. 🎉

Sehen wir uns diese **Deployment-Konzepte** im Hinblick auf Container noch einmal an:

* HTTPS
* Beim Hochfahren ausführen
* Neustarts
* Replikation (die Anzahl der laufenden Prozesse)
* Arbeitsspeicher
* Schritte vor dem Start

## HTTPS { #https }

Wenn wir uns nur auf das **Containerimage** für eine FastAPI-Anwendung (und später auf den laufenden **Container**) konzentrieren, würde HTTPS normalerweise **extern** von einem anderen Tool verarbeitet.

Es könnte sich um einen anderen Container handeln, zum Beispiel mit <a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a>, welcher **HTTPS** und **automatischen** Erwerb von **Zertifikaten** handhabt.

/// tip | Tipp

Traefik verfügt über Integrationen mit Docker, Kubernetes und anderen, sodass Sie damit ganz einfach HTTPS für Ihre Container einrichten und konfigurieren können.

///

Alternativ könnte HTTPS von einem Cloud-Anbieter als einer seiner Dienste gehandhabt werden (während die Anwendung weiterhin in einem Container ausgeführt wird).

## Beim Hochfahren ausführen und Neustarts { #running-on-startup-and-restarts }

Normalerweise gibt es ein anderes Tool, das für das **Starten und Ausführen** Ihres Containers zuständig ist.

Es könnte sich um **Docker** direkt, **Docker Compose**, **Kubernetes**, einen **Cloud-Dienst**, usw. handeln.

In den meisten (oder allen) Fällen gibt es eine einfache Option, um die Ausführung des Containers beim Hochfahren und Neustarts bei Fehlern zu ermöglichen. In Docker ist es beispielsweise die Befehlszeilenoption `--restart`.

Ohne die Verwendung von Containern kann es umständlich und schwierig sein, Anwendungen beim Hochfahren auszuführen und neu zu starten. Bei der **Arbeit mit Containern** ist diese Funktionalität jedoch in den meisten Fällen standardmäßig enthalten. ✨

## Replikation – Anzahl der Prozesse { #replication-number-of-processes }

Wenn Sie einen <abbr title="Eine Gruppe von Maschinen, die so konfiguriert sind, dass sie verbunden sind und auf irgendeine Weise zusammenarbeiten.">Cluster</abbr> von Maschinen mit **Kubernetes**, Docker Swarm Mode, Nomad verwenden, oder einem anderen, ähnlich komplexen System zur Verwaltung verteilter Container auf mehreren Maschinen, möchten Sie wahrscheinlich die **Replikation auf Cluster-Ebene abwickeln**, anstatt in jedem Container einen **Prozessmanager** (wie Uvicorn mit Workern) zu verwenden.

Diese verteilten Containerverwaltungssysteme wie Kubernetes verfügen normalerweise über eine integrierte Möglichkeit, die **Replikation von Containern** zu handhaben und gleichzeitig **Load Balancing** für die eingehenden <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Requests</abbr> zu unterstützen. Alles auf **Cluster-Ebene**.

In diesen Fällen möchten Sie wahrscheinlich ein **Docker-Image von Grund auf** erstellen, wie [oben erklärt](#dockerfile), Ihre Abhängigkeiten installieren und **einen einzelnen Uvicorn-Prozess** ausführen, anstatt mehrere Uvicorn-Worker zu verwenden.

### Load Balancer { #load-balancer }

Bei der Verwendung von Containern ist normalerweise eine Komponente vorhanden, **die am Hauptport lauscht**. Es könnte sich um einen anderen Container handeln, der auch ein **TLS-Terminierungsproxy** ist, um **HTTPS** zu verarbeiten, oder ein ähnliches Tool.

Da diese Komponente die **Last** an Requests aufnehmen und diese (hoffentlich) **ausgewogen** auf die Worker verteilen würde, wird sie üblicherweise auch <abbr title="Lastverteiler">**Load Balancer**</abbr> genannt.

/// tip | Tipp

Die gleiche **TLS-Terminierungsproxy**-Komponente, die für HTTPS verwendet wird, wäre wahrscheinlich auch ein **Load Balancer**.

///

Und wenn Sie mit Containern arbeiten, verfügt das gleiche System, mit dem Sie diese starten und verwalten, bereits über interne Tools, um die **Netzwerkkommunikation** (z. B. HTTP-Requests) von diesem **Load Balancer** (das könnte auch ein **TLS-Terminierungsproxy** sein) zu den Containern mit Ihrer Anwendung weiterzuleiten.

### Ein Load Balancer – mehrere Workercontainer { #one-load-balancer-multiple-worker-containers }

Bei der Arbeit mit **Kubernetes** oder ähnlichen verteilten Containerverwaltungssystemen würde die Verwendung ihrer internen Netzwerkmechanismen es dem einzelnen **Load Balancer**, der den Haupt-**Port** überwacht, ermöglichen, Kommunikation (Requests) an möglicherweise **mehrere Container** weiterzuleiten, in denen Ihre Anwendung ausgeführt wird.

Jeder dieser Container, in denen Ihre Anwendung ausgeführt wird, verfügt normalerweise über **nur einen Prozess** (z. B. einen Uvicorn-Prozess, der Ihre FastAPI-Anwendung ausführt). Es wären alles **identische Container**, die das Gleiche ausführen, welche aber jeweils über einen eigenen Prozess, Speicher, usw. verfügen. Auf diese Weise würden Sie die **Parallelisierung** in **verschiedenen Kernen** der CPU nutzen. Oder sogar in **verschiedenen Maschinen**.

Und das verteilte Containersystem mit dem **Load Balancer** würde **die Requests abwechselnd** an jeden einzelnen Container mit Ihrer Anwendung verteilen. Jeder Request könnte also von einem der mehreren **replizierten Container** verarbeitet werden, in denen Ihre Anwendung ausgeführt wird.

Und normalerweise wäre dieser **Load Balancer** in der Lage, Requests zu verarbeiten, die an *andere* Anwendungen in Ihrem Cluster gerichtet sind (z. B. eine andere Domain oder unter einem anderen URL-Pfad-Präfix), und würde diese Kommunikation an die richtigen Container weiterleiten für *diese andere* Anwendung, die in Ihrem Cluster ausgeführt wird.

### Ein Prozess pro Container { #one-process-per-container }

In einem solchen Szenario möchten Sie wahrscheinlich **einen einzelnen (Uvicorn-)Prozess pro Container** haben, da Sie die Replikation bereits auf Cluster-Ebene durchführen würden.

In diesem Fall möchten Sie also **nicht** mehrere Worker im Container haben, z. B. mit der `--workers` Befehlszeilenoption. Sie möchten nur einen **einzelnen Uvicorn-Prozess** pro Container haben (wahrscheinlich aber mehrere Container).

Ein weiterer Prozessmanager im Container (wie es bei mehreren Workern der Fall wäre) würde nur **unnötige Komplexität** hinzufügen, um welche Sie sich höchstwahrscheinlich bereits mit Ihrem Clustersystem kümmern.

### Container mit mehreren Prozessen und Sonderfälle { #containers-with-multiple-processes-and-special-cases }

Natürlich gibt es **Sonderfälle**, in denen Sie **einen Container** mit mehreren **Uvicorn-Workerprozessen** haben möchten.

In diesen Fällen können Sie die `--workers` Befehlszeilenoption verwenden, um die Anzahl der zu startenden Worker festzulegen:

```{ .dockerfile .annotate }
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1. Hier verwenden wir die `--workers` Befehlszeilenoption, um die Anzahl der Worker auf 4 festzulegen.

Hier sind einige Beispiele, wann das sinnvoll sein könnte:

#### Eine einfache Anwendung { #a-simple-app }

Sie könnten einen Prozessmanager im Container haben wollen, wenn Ihre Anwendung **einfach genug** ist, sodass Sie es auf einem **einzelnen Server** ausführen können, nicht auf einem Cluster.

#### Docker Compose { #docker-compose }

Sie könnten das Deployment auf einem **einzelnen Server** (kein Cluster) mit **Docker Compose** durchführen, sodass Sie keine einfache Möglichkeit hätten, die Replikation von Containern (mit Docker Compose) zu verwalten und gleichzeitig das gemeinsame Netzwerk mit **Load Balancing** zu haben.

Dann möchten Sie vielleicht **einen einzelnen Container** mit einem **Prozessmanager** haben, der darin **mehrere Workerprozesse** startet.

---

Der Hauptpunkt ist, dass **keine** dieser Regeln **in Stein gemeißelt** ist, der man blind folgen muss. Sie können diese Ideen verwenden, um **Ihren eigenen Anwendungsfall zu evaluieren**, zu entscheiden, welcher Ansatz für Ihr System am besten geeignet ist und herauszufinden, wie Sie folgende Konzepte verwalten:

* Sicherheit – HTTPS
* Beim Hochfahren ausführen
* Neustarts
* Replikation (die Anzahl der laufenden Prozesse)
* Arbeitsspeicher
* Schritte vor dem Start

## Arbeitsspeicher { #memory }

Wenn Sie **einen einzelnen Prozess pro Container** ausführen, wird von jedem dieser Container (mehr als einer, wenn sie repliziert werden) eine mehr oder weniger klar definierte, stabile und begrenzte Menge an Arbeitsspeicher verbraucht.

Und dann können Sie dieselben Speichergrenzen und -anforderungen in Ihren Konfigurationen für Ihr Container-Management-System festlegen (z. B. in **Kubernetes**). Auf diese Weise ist es in der Lage, die Container auf den **verfügbaren Maschinen** zu replizieren, wobei die von diesen benötigte Speichermenge und die auf den Maschinen im Cluster verfügbare Menge berücksichtigt werden.

Wenn Ihre Anwendung **einfach** ist, wird dies wahrscheinlich **kein Problem darstellen** und Sie müssen möglicherweise keine festen Speichergrenzen angeben. Wenn Sie jedoch **viel Speicher verbrauchen** (z. B. bei **Modellen für maschinelles Lernen**), sollten Sie überprüfen, wie viel Speicher Sie verbrauchen, und die **Anzahl der Container** anpassen, die in **jeder Maschine** ausgeführt werden (und möglicherweise weitere Maschinen zu Ihrem Cluster hinzufügen).

Wenn Sie **mehrere Prozesse pro Container** ausführen, müssen Sie sicherstellen, dass die Anzahl der gestarteten Prozesse nicht **mehr Speicher verbraucht** als verfügbar ist.

## Schritte vor dem Start und Container { #previous-steps-before-starting-and-containers }

Wenn Sie Container (z. B. Docker, Kubernetes) verwenden, können Sie hauptsächlich zwei Ansätze verwenden.

### Mehrere Container { #multiple-containers }

Wenn Sie **mehrere Container** haben, von denen wahrscheinlich jeder einen **einzelnen Prozess** ausführt (z. B. in einem **Kubernetes**-Cluster), dann möchten Sie wahrscheinlich einen **separaten Container** haben, welcher die Arbeit der **Vorab-Schritte** in einem einzelnen Container, mit einem einzelnen Prozess ausführt, **bevor** die replizierten Workercontainer ausgeführt werden.

/// info | Info

Wenn Sie Kubernetes verwenden, wäre dies wahrscheinlich ein <a href="https://kubernetes.io/docs/concepts/workloads/pods/init-containers/" class="external-link" target="_blank">Init-Container</a>.

///

Wenn es in Ihrem Anwendungsfall kein Problem darstellt, diese vorherigen Schritte **mehrmals parallel** auszuführen (z. B. wenn Sie keine Datenbankmigrationen ausführen, sondern nur prüfen, ob die Datenbank bereits bereit ist), können Sie sie auch einfach in jedem Container direkt vor dem Start des Hauptprozesses einfügen.

### Einzelner Container { #single-container }

Wenn Sie ein einfaches Setup mit einem **einzelnen Container** haben, welcher dann mehrere **Workerprozesse** (oder auch nur einen Prozess) startet, können Sie die Vorab-Schritte im selben Container direkt vor dem Starten des Prozesses mit der Anwendung ausführen.

### Docker-Basisimage { #base-docker-image }

Es gab ein offizielles FastAPI-Docker-Image: <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>. Dieses ist jedoch jetzt veraltet. ⛔️

Sie sollten wahrscheinlich **nicht** dieses Basis-Docker-Image (oder ein anderes ähnliches) verwenden.

Wenn Sie **Kubernetes** (oder andere) verwenden und bereits **Replikation** auf Cluster-Ebene mit mehreren **Containern** eingerichtet haben. In diesen Fällen ist es besser, **ein Image von Grund auf neu zu erstellen**, wie oben beschrieben: [Ein Docker-Image für FastAPI erstellen](#build-a-docker-image-for-fastapi).

Und wenn Sie mehrere Worker benötigen, können Sie einfach die `--workers` Befehlszeilenoption verwenden.

/// note | Technische Details

Das Docker-Image wurde erstellt, als Uvicorn das Verwalten und Neustarten von ausgefallenen Workern noch nicht unterstützte, weshalb es notwendig war, Gunicorn mit Uvicorn zu verwenden, was zu einer erheblichen Komplexität führte, nur damit Gunicorn die Uvicorn-Workerprozesse verwaltet und neu startet.

Aber jetzt, da Uvicorn (und der `fastapi`-Befehl) die Verwendung von `--workers` unterstützen, gibt es keinen Grund, ein Basis-Docker-Image an Stelle eines eigenen (das praktisch denselben Code enthält 😅) zu verwenden.

///

## Deployment des Containerimages { #deploy-the-container-image }

Nachdem Sie ein Containerimage (Docker) haben, gibt es mehrere Möglichkeiten, es bereitzustellen.

Zum Beispiel:

* Mit **Docker Compose** auf einem einzelnen Server
* Mit einem **Kubernetes**-Cluster
* Mit einem Docker Swarm Mode-Cluster
* Mit einem anderen Tool wie Nomad
* Mit einem Cloud-Dienst, der Ihr Containerimage nimmt und es bereitstellt

## Docker-Image mit `uv` { #docker-image-with-uv }

Wenn Sie <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">uv</a> verwenden, um Ihr Projekt zu installieren und zu verwalten, können Sie deren <a href="https://docs.astral.sh/uv/guides/integration/docker/" class="external-link" target="_blank">uv-Docker-Leitfaden</a> befolgen.

## Zusammenfassung { #recap }

Mithilfe von Containersystemen (z. B. mit **Docker** und **Kubernetes**) ist es ziemlich einfach, alle **Deployment-Konzepte** zu handhaben:

* HTTPS
* Beim Hochfahren ausführen
* Neustarts
* Replikation (die Anzahl der laufenden Prozesse)
* Arbeitsspeicher
* Schritte vor dem Start

In den meisten Fällen möchten Sie wahrscheinlich kein Basisimage verwenden und stattdessen **ein Containerimage von Grund auf erstellen**, eines basierend auf dem offiziellen Python-Docker-Image.

Indem Sie auf die **Reihenfolge** der Anweisungen im `Dockerfile` und den **Docker-Cache** achten, können Sie **die Build-Zeiten minimieren**, um Ihre Produktivität zu erhöhen (und Langeweile zu vermeiden). 😎
