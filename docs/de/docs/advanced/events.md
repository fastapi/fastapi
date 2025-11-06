# Lifespan-Events { #lifespan-events }

Sie können Logik (Code) definieren, die ausgeführt werden soll, bevor die Anwendung **hochfährt**. Dies bedeutet, dass dieser Code **einmal** ausgeführt wird, **bevor** die Anwendung **beginnt, <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Requests</abbr> entgegenzunehmen**.

Auf die gleiche Weise können Sie Logik (Code) definieren, die ausgeführt werden soll, wenn die Anwendung **heruntergefahren** wird. In diesem Fall wird dieser Code **einmal** ausgeführt, **nachdem** möglicherweise **viele Requests** bearbeitet wurden.

Da dieser Code ausgeführt wird, bevor die Anwendung **beginnt**, Requests entgegenzunehmen, und unmittelbar, nachdem sie die Bearbeitung von Requests **abgeschlossen hat**, deckt er den gesamten Anwendungs-<abbr title="Lebensdauer">**Lifespan**</abbr> ab (das Wort „Lifespan“ wird gleich wichtig sein 😉).

Dies kann sehr nützlich sein, um **Ressourcen** einzurichten, die Sie in der gesamten App verwenden wollen und die von Requests **gemeinsam genutzt** werden und/oder die Sie anschließend **aufräumen** müssen. Zum Beispiel ein Pool von Datenbankverbindungen oder das Laden eines gemeinsam genutzten Modells für maschinelles Lernen.

## Anwendungsfall { #use-case }

Beginnen wir mit einem Beispiel-**Anwendungsfall** und schauen uns dann an, wie wir ihn mit dieser Methode implementieren können.

Stellen wir uns vor, Sie verfügen über einige **Modelle für maschinelles Lernen**, die Sie zur Bearbeitung von Requests verwenden möchten. 🤖

Die gleichen Modelle werden von den Requests gemeinsam genutzt, es handelt sich also nicht um ein Modell pro Request, pro Benutzer, oder ähnliches.

Stellen wir uns vor, dass das Laden des Modells **eine ganze Weile dauern** kann, da viele **Daten von der Festplatte** gelesen werden müssen. Sie möchten das also nicht für jeden Request tun.

Sie könnten das auf der obersten Ebene des Moduls/der Datei machen, aber das würde auch bedeuten, dass **das Modell geladen wird**, selbst wenn Sie nur einen einfachen automatisierten Test ausführen, dann wäre dieser Test **langsam**, weil er warten müsste, bis das Modell geladen ist, bevor er einen davon unabhängigen Teil des Codes ausführen könnte.

Das wollen wir besser machen: Laden wir das Modell, bevor die Requests bearbeitet werden, aber unmittelbar bevor die Anwendung beginnt, Requests zu empfangen, und nicht, während der Code geladen wird.

## Lifespan { #lifespan }

Sie können diese Logik beim <abbr title="Hochfahren">*Startup*</abbr> und <abbr title="Herunterfahren">*Shutdown*</abbr> mithilfe des `lifespan`-Parameters der `FastAPI`-App und eines „Kontextmanagers“ definieren (ich zeige Ihnen gleich, was das ist).

Beginnen wir mit einem Beispiel und sehen es uns dann im Detail an.

Wir erstellen eine asynchrone Funktion `lifespan()` mit `yield` wie folgt:

{* ../../docs_src/events/tutorial003.py hl[16,19] *}

Hier simulieren wir den langsamen *Startup*, das Laden des Modells, indem wir die (Fake-)Modellfunktion vor dem `yield` in das <abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">Dictionary</abbr> mit Modellen für maschinelles Lernen einfügen. Dieser Code wird ausgeführt, **bevor** die Anwendung **beginnt, Requests entgegenzunehmen**, während des *Startups*.

Und dann, direkt nach dem `yield`, entladen wir das Modell. Dieser Code wird ausgeführt, **nachdem** die Anwendung **die Bearbeitung von Requests abgeschlossen hat**, direkt vor dem *Shutdown*. Dadurch könnten beispielsweise Ressourcen wie Arbeitsspeicher oder eine GPU freigegeben werden.

/// tip | Tipp

Das `shutdown` würde erfolgen, wenn Sie die Anwendung **stoppen**.

Möglicherweise müssen Sie eine neue Version starten, oder Sie haben es einfach satt, sie auszuführen. 🤷

///

### Lifespan-Funktion { #lifespan-function }

Das Erste, was auffällt, ist, dass wir eine asynchrone Funktion mit `yield` definieren. Das ist sehr ähnlich zu Abhängigkeiten mit `yield`.

{* ../../docs_src/events/tutorial003.py hl[14:19] *}

Der erste Teil der Funktion, vor dem `yield`, wird ausgeführt **bevor** die Anwendung startet.

Und der Teil nach `yield` wird ausgeführt, **nachdem** die Anwendung beendet ist.

### Asynchroner Kontextmanager { #async-context-manager }

Wie Sie sehen, ist die Funktion mit einem `@asynccontextmanager` versehen.

Dadurch wird die Funktion in einen sogenannten „**asynchronen Kontextmanager**“ umgewandelt.

{* ../../docs_src/events/tutorial003.py hl[1,13] *}

Ein **Kontextmanager** in Python ist etwas, das Sie in einer `with`-Anweisung verwenden können, zum Beispiel kann `open()` als Kontextmanager verwendet werden:

```Python
with open("file.txt") as file:
    file.read()
```

In neueren Versionen von Python gibt es auch einen **asynchronen Kontextmanager**. Sie würden ihn mit `async with` verwenden:

```Python
async with lifespan(app):
    await do_stuff()
```

Wenn Sie wie oben einen Kontextmanager oder einen asynchronen Kontextmanager erstellen, führt dieser vor dem Betreten des `with`-Blocks den Code vor dem `yield` aus, und nach dem Verlassen des `with`-Blocks wird er den Code nach dem `yield` ausführen.

In unserem obigen Codebeispiel verwenden wir ihn nicht direkt, sondern übergeben ihn an FastAPI, damit es ihn verwenden kann.

Der Parameter `lifespan` der `FastAPI`-App benötigt einen **asynchronen Kontextmanager**, wir können ihm also unseren neuen asynchronen Kontextmanager `lifespan` übergeben.

{* ../../docs_src/events/tutorial003.py hl[22] *}

## Alternative Events (<abbr title="veraltet, obsolet: Es soll nicht mehr verwendet werden">deprecatet</abbr>) { #alternative-events-deprecated }

/// warning | Achtung

Der empfohlene Weg, den *Startup* und *Shutdown* zu handhaben, ist die Verwendung des `lifespan`-Parameters der `FastAPI`-App, wie oben beschrieben. Wenn Sie einen `lifespan`-Parameter übergeben, werden die `startup`- und `shutdown`-Eventhandler nicht mehr aufgerufen. Es ist entweder alles `lifespan` oder alles Events, nicht beides.

Sie können diesen Teil wahrscheinlich überspringen.

///

Es gibt eine alternative Möglichkeit, diese Logik zu definieren, sodass sie beim *Startup* und beim *Shutdown* ausgeführt wird.

Sie können <abbr title="Eventhandler – Ereignisbehandler: Funktion, die beim Eintreten eines bestimmten Ereignisses ausgeführt wird">Eventhandler</abbr> (Funktionen) definieren, die ausgeführt werden sollen, bevor die Anwendung hochgefahren wird oder wenn die Anwendung heruntergefahren wird.

Diese Funktionen können mit `async def` oder normalem `def` deklariert werden.

### `startup`-Event { #startup-event }

Um eine Funktion hinzuzufügen, die vor dem Start der Anwendung ausgeführt werden soll, deklarieren Sie diese mit dem Event `startup`:

{* ../../docs_src/events/tutorial001.py hl[8] *}

In diesem Fall initialisiert die Eventhandler-Funktion `startup` die „Datenbank“ der Items (nur ein `dict`) mit einigen Werten.

Sie können mehr als eine Eventhandler-Funktion hinzufügen.

Und Ihre Anwendung empfängt erst dann Requests, wenn alle `startup`-Eventhandler abgeschlossen sind.

### `shutdown`-Event { #shutdown-event }

Um eine Funktion hinzuzufügen, die beim Shutdown der Anwendung ausgeführt werden soll, deklarieren Sie sie mit dem Event `shutdown`:

{* ../../docs_src/events/tutorial002.py hl[6] *}

Hier schreibt die `shutdown`-Eventhandler-Funktion eine Textzeile `"Application shutdown"` in eine Datei `log.txt`.

/// info | Info

In der Funktion `open()` bedeutet `mode="a"` „append“ („anhängen“), sodass die Zeile nach dem, was sich in dieser Datei befindet, hinzugefügt wird, ohne den vorherigen Inhalt zu überschreiben.

///

/// tip | Tipp

Beachten Sie, dass wir in diesem Fall eine Standard-Python-Funktion `open()` verwenden, die mit einer Datei interagiert.

Es handelt sich also um I/O (Input/Output), welches „Warten“ erfordert, bis Dinge auf die Festplatte geschrieben werden.

Aber `open()` verwendet nicht `async` und `await`.

Daher deklarieren wir die Eventhandler-Funktion mit Standard-`def` statt mit `async def`.

///

### `startup` und `shutdown` zusammen { #startup-and-shutdown-together }

Es besteht eine hohe Wahrscheinlichkeit, dass die Logik für Ihr *Startup* und *Shutdown* miteinander verknüpft ist. Vielleicht möchten Sie etwas beginnen und es dann beenden, eine Ressource laden und sie dann freigeben usw.

Bei getrennten Funktionen, die keine gemeinsame Logik oder Variablen haben, ist dies schwieriger, da Sie Werte in globalen Variablen speichern oder ähnliche Tricks verwenden müssen.

Aus diesem Grund wird jetzt empfohlen, stattdessen `lifespan` wie oben erläutert zu verwenden.

## Technische Details { #technical-details }

Nur ein technisches Detail für die neugierigen Nerds. 🤓

In der technischen ASGI-Spezifikation ist dies Teil des <a href="https://asgi.readthedocs.io/en/latest/specs/lifespan.html" class="external-link" target="_blank">Lifespan Protokolls</a> und definiert Events namens `startup` und `shutdown`.

/// info | Info

Weitere Informationen zu Starlettes `lifespan`-Handlern finden Sie in <a href="https://www.starlette.dev/lifespan/" class="external-link" target="_blank">Starlettes Lifespan-Dokumentation</a>.

Einschließlich, wie man Lifespan-Zustand handhabt, der in anderen Bereichen Ihres Codes verwendet werden kann.

///

## Unteranwendungen { #sub-applications }

🚨 Beachten Sie, dass diese Lifespan-Events (Startup und Shutdown) nur für die Hauptanwendung ausgeführt werden, nicht für [Unteranwendungen – Mounts](sub-applications.md){.internal-link target=_blank}.
