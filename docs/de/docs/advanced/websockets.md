# WebSockets { #websockets }

Sie können <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSockets</a> mit **FastAPI** verwenden.

## `websockets` installieren { #install-websockets }

Stellen Sie sicher, dass Sie eine [virtuelle Umgebung](../virtual-environments.md){.internal-link target=_blank} erstellen, sie aktivieren und `websockets` installieren (eine Python-Bibliothek, die die Verwendung des „WebSocket“-Protokolls erleichtert):

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## WebSockets-Client { #websockets-client }

### In Produktion { #in-production }

In Ihrem Produktionssystem haben Sie wahrscheinlich ein Frontend, das mit einem modernen Framework wie React, Vue.js oder Angular erstellt wurde.

Und um über WebSockets mit Ihrem Backend zu kommunizieren, würden Sie wahrscheinlich die Werkzeuge Ihres Frontends verwenden.

Oder Sie verfügen möglicherweise über eine native Mobile-Anwendung, die direkt in nativem Code mit Ihrem WebSocket-Backend kommuniziert.

Oder Sie haben andere Möglichkeiten, mit dem WebSocket-Endpunkt zu kommunizieren.

---

Für dieses Beispiel verwenden wir jedoch ein sehr einfaches HTML-Dokument mit etwas JavaScript, alles in einem langen String.

Das ist natürlich nicht optimal und man würde das nicht in der Produktion machen.

In der Produktion hätten Sie eine der oben genannten Optionen.

Aber es ist der einfachste Weg, sich auf die Serverseite von WebSockets zu konzentrieren und ein funktionierendes Beispiel zu haben:

{* ../../docs_src/websockets/tutorial001.py hl[2,6:38,41:43] *}

## Einen `websocket` erstellen { #create-a-websocket }

Erstellen Sie in Ihrer **FastAPI**-Anwendung einen `websocket`:

{* ../../docs_src/websockets/tutorial001.py hl[1,46:47] *}

/// note | Technische Details

Sie könnten auch `from starlette.websockets import WebSocket` verwenden.

**FastAPI** stellt den gleichen `WebSocket` direkt zur Verfügung, als Annehmlichkeit für Sie, den Entwickler. Er kommt aber direkt von Starlette.

///

## Nachrichten erwarten und Nachrichten senden { #await-for-messages-and-send-messages }

In Ihrer WebSocket-Route können Sie Nachrichten `await`en und Nachrichten senden.

{* ../../docs_src/websockets/tutorial001.py hl[48:52] *}

Sie können Binär-, Text- und JSON-Daten empfangen und senden.

## Es ausprobieren { #try-it }

Wenn Ihre Datei `main.py` heißt, führen Sie Ihre Anwendung so aus:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Öffnen Sie Ihren Browser unter <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Sie sehen eine einfache Seite wie:

<img src="/img/tutorial/websockets/image01.png">

Sie können Nachrichten in das Eingabefeld tippen und absenden:

<img src="/img/tutorial/websockets/image02.png">

Und Ihre **FastAPI**-Anwendung mit WebSockets antwortet:

<img src="/img/tutorial/websockets/image03.png">

Sie können viele Nachrichten senden (und empfangen):

<img src="/img/tutorial/websockets/image04.png">

Und alle verwenden dieselbe WebSocket-Verbindung.

## Verwendung von `Depends` und anderen { #using-depends-and-others }

In WebSocket-Endpunkten können Sie Folgendes aus `fastapi` importieren und verwenden:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

Diese funktionieren auf die gleiche Weise wie für andere FastAPI-Endpunkte/*Pfadoperationen*:

{* ../../docs_src/websockets/tutorial002_an_py310.py hl[68:69,82] *}

/// info | Info

Da es sich um einen WebSocket handelt, macht es keinen Sinn, eine `HTTPException` auszulösen, stattdessen lösen wir eine `WebSocketException` aus.

Sie können einen „Closing“-Code verwenden, aus den <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">gültigen Codes, die in der Spezifikation definiert sind</a>.

///

### WebSockets mit Abhängigkeiten ausprobieren { #try-the-websockets-with-dependencies }

Wenn Ihre Datei `main.py` heißt, führen Sie Ihre Anwendung mit Folgendem aus:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Öffnen Sie Ihren Browser unter <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Dort können Sie einstellen:

* Die „Item ID“, die im Pfad verwendet wird.
* Das „Token“, das als Query-Parameter verwendet wird.

/// tip | Tipp

Beachten Sie, dass die Query `token` von einer Abhängigkeit verarbeitet wird.

///

Damit können Sie den WebSocket verbinden und dann Nachrichten senden und empfangen:

<img src="/img/tutorial/websockets/image05.png">

## Verbindungsabbrüche und mehrere Clients handhaben { #handling-disconnections-and-multiple-clients }

Wenn eine WebSocket-Verbindung geschlossen wird, löst `await websocket.receive_text()` eine `WebSocketDisconnect`-Exception aus, die Sie dann wie in folgendem Beispiel abfangen und behandeln können.

{* ../../docs_src/websockets/tutorial003_py39.py hl[79:81] *}

Zum Ausprobieren:

* Öffnen Sie die Anwendung mit mehreren Browser-Tabs.
* Schreiben Sie Nachrichten in den Tabs.
* Schließen Sie dann einen der Tabs.

Das wird die Ausnahme `WebSocketDisconnect` auslösen und alle anderen Clients erhalten eine Nachricht wie:

```
Client #1596980209979 left the chat
```

/// tip | Tipp

Die obige Anwendung ist ein minimales und einfaches Beispiel, das zeigt, wie Nachrichten verarbeitet und an mehrere WebSocket-Verbindungen gesendet werden.

Beachten Sie jedoch, dass, da alles nur im Speicher in einer einzigen Liste verwaltet wird, es nur funktioniert, während der Prozess ausgeführt wird, und nur mit einem einzelnen Prozess.

Wenn Sie etwas benötigen, das sich leicht in FastAPI integrieren lässt, aber robuster ist und von Redis, PostgreSQL und anderen unterstützt wird, sehen Sie sich <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a> an.

///

## Mehr Informationen { #more-info }

Weitere Informationen zu Optionen finden Sie in der Dokumentation von Starlette:

* <a href="https://www.starlette.dev/websockets/" class="external-link" target="_blank">Die `WebSocket`-Klasse</a>.
* <a href="https://www.starlette.dev/endpoints/#websocketendpoint" class="external-link" target="_blank">Klassen-basierte Handhabung von WebSockets</a>.
