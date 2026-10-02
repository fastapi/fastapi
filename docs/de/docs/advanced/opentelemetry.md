# OpenTelemetry { #opentelemetry }

Wenn Ihre API läuft, möchten Sie vielleicht wissen, wie viel Traffic sie erhält, welche Requests langsam sind und wann Fehler auftreten.

**Telemetrie** umfasst Daten über das Verhalten Ihrer Anwendung, die Ihnen helfen, diese Fragen zu beantworten. Zu den gängigen Typen gehören:

- **Metriken**: Messwerte, die Sie über einen Zeitraum zusammenfassen können, etwa Responsezeiten und die Anzahl der verarbeiteten Requests.
- **Traces**: Aufzeichnungen einzelner Requests und der Operationen, die zu ihrer Verarbeitung ausgeführt werden. Jede zeitlich erfasste Operation wird als **Span** bezeichnet.
- **Logs**: Aufzeichnungen von Events mit Zeitstempel, etwa das Starten einer Anwendung oder das Fehlschlagen einer Operation.

[**OpenTelemetry**](https://opentelemetry.io/) ist eine Sammlung von Standards und Werkzeugen zum Erfassen von Telemetriedaten und zum Senden dieser Daten an einen Monitoring-Dienst, wo Sie sie in Dashboards untersuchen können.

**FastAPI bietet standardmäßig OpenTelemetry-Unterstützung** für HTTP-Request-Traces, Metriken und Logs. WebSocket-Verbindungen liefern ebenfalls Traces und Logs. Um diese Daten anzuzeigen, konfigurieren Sie einen Monitoring-Dienst, der sie empfängt.

## FastAPI installieren { #install-fastapi }

Installieren Sie FastAPI mit den `standard`-Extras, die die Pakete zum Senden von Telemetriedaten enthalten:

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## Die Anwendung erstellen { #create-the-app }

Erstellen Sie eine Datei `main.py`:

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

Beachten Sie, dass alles standardmäßig funktioniert. Sie müssen keinen eigenen Code schreiben, damit die Telemetrie funktioniert.

## FastAPI Cloud { #fastapi-cloud }

Wenn Sie mit `fastapi[standard]` auf [FastAPI Cloud](https://fastapicloud.com) deployen, funktionieren Metriken automatisch. Sie müssen nichts weiter konfigurieren.

Mit einem Pro-Tarif können Sie die Anzahl der Requests, Fehlerraten und Responsezeiten im [Metriken-Dashboard](https://fastapicloud.com/docs/monitoring-and-performance/metrics/) anzeigen.

<img src="/img/tutorial/opentelemetry/image01.png" alt="FastAPI Cloud Pro-Metriken-Dashboard mit Beispieldaten">

## Andere Monitoring-Dienste { #other-monitoring-services }

Um Telemetriedaten an einen anderen Monitoring-Dienst zu senden, konfigurieren Sie einen Endpunkt, der **OTLP** akzeptiert, das OpenTelemetry-Protokoll zum Senden von Telemetriedaten. Verwenden Sie den HTTP/protobuf-Basisendpunkt des Dienstes.

Setzen Sie diese Umgebungsvariablen und ersetzen Sie die Beispiel-URL durch Ihren Endpunkt:

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME` identifiziert Ihre Anwendung im Monitoring-Dienst. Der Endpunkt ist die Basis-URL für den Empfang von Daten. Unter dieser URL werden Traces an `/v1/traces`, Metriken an `/v1/metrics` und Logs an `/v1/logs` gesendet.

Wenn Ihr Dienst Authentifizierung erfordert, setzen Sie `OTEL_EXPORTER_OTLP_HEADERS` auf die von ihm vorgegebenen Header, zum Beispiel `api-key=YOUR_API_KEY`.

## Die Anwendung ausführen { #run-the-app }

Starten Sie die Anwendung im selben Terminal:

<div class="termy">

```console
$ uv run fastapi run
```

</div>

Senden Sie in einem anderen Terminal einen Request:

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

Öffnen Sie Ihren Monitoring-Dienst und suchen Sie nach `my-api`. Nach dem nächsten Export sehen Sie einen Trace mit einem `GET /items/{item_id}`-Span sowie Metriken zur Anzahl der Requests, zur Responsedauer und zu aktiven Requests.

## Telemetrie anpassen { #customize-telemetry }

### Provider und Exporter konfigurieren { #configure-providers-and-exporters }

Ein **Provider** stellt die Objekte bereit, die Traces, Metriken oder Logs aufzeichnen. Seine Konfiguration steuert, wie diese Daten verarbeitet und exportiert werden.

Telemetriebibliotheken können die globalen Provider von OpenTelemetry konfigurieren. Konfigurieren Sie die Bibliothek, bevor die Anwendung startet, und FastAPI verwendet diese Provider automatisch.

Wenn ein OTLP-Endpunkt in der Umgebung gesetzt ist, fügt FastAPI jedem aktivierten Provider einen Exporter für dieses Ziel hinzu. Vorhandene Exporter senden weiterhin Daten an ihre Ziele.

Konfigurieren Sie jedes Ziel einmal. Wenn eine andere Bibliothek bereits das in der Umgebung angegebene Ziel verwaltet, deaktivieren Sie deren Export über die Umgebung oder schalten Sie FastAPIs automatische Einrichtung aus:

```python
app = FastAPI(telemetry={"auto_configure": False})
```

Sie können auch einen Provider direkt im Dictionary `telemetry` übergeben. Dieser Provider verwendet beispielsweise den Konsolenexporter von OpenTelemetry, um Request-Spans in Ihrem Terminal auszugeben:

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

Der **Exporter** sendet die Spans an ihr Ziel. `BatchSpanProcessor` gruppiert Spans und sendet sie im Hintergrund. Ersetzen Sie den Konsolenexporter durch einen Exporter Ihrer Monitoring-Bibliothek, um deren Ziel zu verwenden. Weitere Konfigurationsoptionen finden Sie im [Leitfaden zur Python-Instrumentierung von OpenTelemetry](https://opentelemetry.io/docs/languages/python/instrumentation/).

Verwenden Sie `meter_provider` oder `logger_provider` im selben Dictionary, um einen Provider für Metriken oder Logs bereitzustellen. Die Anwendung oder Bibliothek, die einen Provider erstellt, verwaltet dessen Shutdown. FastAPI verwaltet die Exportkomponenten, die es hinzufügt.

/// warning | Achtung

OpenTelemetry verwendet standardmäßig globale Provider. Eine unabhängige Telemetriekonfiguration für [gemountete Unteranwendungen](sub-applications.md) ist nicht garantiert.

///

### Request-Operationen nachverfolgen { #trace-request-operations }

Standardmäßig enthalten Request-Traces Spans für das Auflösen von Abhängigkeiten, das Ausführen Ihrer Pfadoperation-Funktion, das Serialisieren der Response und das Ausführen jedes Tasks in FastAPIs `BackgroundTasks`. Diese Spans verwenden denselben Provider und dieselben Exporter.

Die Spans der Hintergrundtasks bleiben Teil des Request-Traces. Sie werden ausgeführt, nachdem der HTTP-Response-Span beendet ist, und erhöhen daher nicht die gemessene Responsezeit.

Um nur den HTTP-Request-Span aufzuzeichnen, setzen Sie `operation_spans` auf `False`:

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### WebSocket-Verbindungen nachverfolgen { #trace-websocket-connections }

Jede WebSocket-Verbindung hat einen Span wie `WS /ws/{room}`, der den Handler und das Aufräumen der Abhängigkeiten umfasst. Er verwendet dieselben Provider und Einstellungen, einschließlich `operation_spans` für das Auflösen von Abhängigkeiten und das Ausführen des Endpunkts.

HTTP-Request-Metriken erfassen nur HTTP-Requests. Normale WebSocket-Verbindungsabbrüche mit den Codes `1000` oder `1001` erzeugen keine Fehlerlogs.

### Fehler untersuchen { #inspect-errors }

FastAPI zeichnet unbehandelte Exceptions als OpenTelemetry-Logs auf, die mit dem Trace des Requests oder der Verbindung verknüpft sind. Fehlerlogs werden auch dann aufgezeichnet, wenn der Trace nicht durch Sampling erfasst wird.

Exception-Logs enthalten den Typ, die Nachricht und den Stacktrace der Exception. Nachrichten und Stacktraces können sensible Informationen enthalten. Verwenden Sie die Logprozessoren Ihres Providers, um diese zu filtern oder zu schwärzen, oder setzen Sie `logs` auf `False`, um diese Logs zu deaktivieren.

FastAPI zeichnet außerdem fehlgeschlagene Request-Validierungen als Warnungslogs mit der Route und der Fehleranzahl auf. Diese Logs enthalten nicht die ungültigen Eingabedaten.

## Die aufzuzeichnenden Daten auswählen { #choose-what-to-record }

Das Dictionary `telemetry` akzeptiert außerdem diese Einstellungen:

| Einstellung | Zweck | Defaultwert |
| --- | --- | --- |
| `tracing` | Spans für HTTP-Requests und WebSocket-Verbindungen aufzeichnen | `True` |
| `metrics` | HTTP-Request-Metriken aufzeichnen | `True` |
| `logs` | Fehlgeschlagene Validierungen und unbehandelte Exceptions aufzeichnen | `True` |
| `operation_spans` | Spans für Request-Operationen hinzufügen | `True` |
| `exclude` | Requests überspringen, wenn eine Funktion, die den ASGI-Scope empfängt, `True` zurückgibt | `None` |
| `auto_configure` | Exporter für Endpunkte hinzufügen, die in Umgebungsvariablen gesetzt sind | `True` |

Um beispielsweise Metriken zu erfassen und dabei Healthchecks auszuschließen:

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

Setzen Sie `auto_configure` auf `False`, wenn Ihre Anwendung die Einrichtung der Provider selbst übernimmt, etwa innerhalb ihrer Lifespan-Funktion.
