# Server-Sent Events (SSE) { #server-sent-events-sse }

Sie können Daten mithilfe von **Server-Sent Events** (SSE) an den Client streamen.

Das ist ähnlich wie [JSON Lines streamen](stream-json-lines.md), verwendet aber das Format `text/event-stream`, das von Browsern nativ mit der [die `EventSource`-API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) unterstützt wird.

/// info | Info

Hinzugefügt in FastAPI 0.135.0.

///

## Was sind Server-Sent Events? { #what-are-server-sent-events }

SSE ist ein Standard zum Streamen von Daten vom Server zum Client über HTTP.

Jedes Event ist ein kleiner Textblock mit „Feldern“ wie `data`, `event`, `id` und `retry`, getrennt durch Leerzeilen.

Das sieht so aus:

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE wird häufig für KI-Chat-Streaming, Live-Benachrichtigungen, Logs und Observability sowie andere Fälle verwendet, in denen der Server Updates an den Client pusht.

/// tip | Tipp

Wenn Sie Binärdaten streamen wollen, z. B. Video oder Audio, sehen Sie im fortgeschrittenen Handbuch nach: [Daten streamen](../advanced/stream-data.md).

///

## SSE mit FastAPI streamen { #stream-sse-with-fastapi }

Um SSE mit FastAPI zu streamen, verwenden Sie `yield` in Ihrer *Pfadoperation-Funktion* und setzen Sie `response_class=EventSourceResponse`.

Importieren Sie `EventSourceResponse` aus `fastapi.sse`:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

Jedes mit `yield` zurückgegebene Element wird als JSON kodiert und im Feld `data:` eines SSE-Events gesendet.

Wenn Sie den Rückgabetyp als `AsyncIterable[Item]` deklarieren, verwendet FastAPI ihn, um die Daten mit Pydantic zu **validieren**, zu **dokumentieren** und zu **serialisieren**.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip | Tipp

Da Pydantic es auf der **Rust**-Seite serialisiert, erhalten Sie eine deutlich höhere **Leistung**, als wenn Sie keinen Rückgabetyp deklarieren.

///

### Nicht-async-*Pfadoperation-Funktionen* { #non-async-path-operation-functions }

Sie können auch normale `def`-Funktionen (ohne `async`) verwenden und `yield` genauso einsetzen.

FastAPI stellt sicher, dass sie korrekt ausgeführt wird, sodass sie die Event Loop nicht blockiert.

Da die Funktion in diesem Fall nicht async ist, wäre der passende Rückgabetyp `Iterable[Item]`:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### Kein Rückgabetyp { #no-return-type }

Sie können den Rückgabetyp auch weglassen. FastAPI verwendet dann den [`jsonable_encoder`](./encoder.md), um die Daten zu konvertieren und zu senden.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

Wenn Sie SSE-Felder wie `event`, `id`, `retry` oder `comment` setzen müssen, können Sie statt reiner Daten `ServerSentEvent`-Objekte yielden.

Importieren Sie `ServerSentEvent` aus `fastapi.sse`:

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

Das Feld `data` wird immer als JSON kodiert. Sie können jeden Wert übergeben, der als JSON serialisierbar ist, einschließlich Pydantic-Modellen.

## Rohdaten { #raw-data }

Wenn Sie Daten **ohne** JSON-Kodierung senden müssen, verwenden Sie `raw_data` statt `data`.

Das ist nützlich zum Senden vorformatierter Texte, Logzeilen oder spezieller <dfn title="Ein Wert, der verwendet wird, um eine besondere Bedingung oder einen besonderen Zustand anzuzeigen">„Sentinel“</dfn>-Werte wie `[DONE]`.

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note | Hinweis

`data` und `raw_data` schließen sich gegenseitig aus. Sie können pro `ServerSentEvent` nur eines von beiden setzen.

///

## Mit `Last-Event-ID` fortsetzen { #resuming-with-last-event-id }

Wenn ein Browser nach einem Verbindungsabbruch erneut verbindet, sendet er die zuletzt empfangene `id` im Header `Last-Event-ID`.

Sie können ihn als Header-Parameter einlesen und verwenden, um den Stream dort fortzusetzen, wo der Client aufgehört hat:

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## SSE mit POST { #sse-with-post }

SSE funktioniert mit **jedem HTTP-Method**, nicht nur mit `GET`.

Das ist nützlich für Protokolle wie [MCP](https://modelcontextprotocol.io), die SSE über `POST` streamen:

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## Technische Details { #technical-details }

FastAPI implementiert einige bewährte SSE-Praktiken direkt out of the box.

- Alle 15 Sekunden, wenn keine Nachricht gesendet wurde, einen **„keep alive“-`ping`-Kommentar** senden, um zu verhindern, dass einige Proxys die Verbindung schließen, wie in der [HTML-Spezifikation: Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes) vorgeschlagen.
- Den Header `Cache-Control: no-cache` setzen, um **Caching** des Streams zu verhindern.
- Einen speziellen Header `X-Accel-Buffering: no` setzen, um **Buffering** in einigen Proxys wie Nginx zu verhindern.

Sie müssen dafür nichts tun, das funktioniert out of the box. 🤓
