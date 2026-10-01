# OpenTelemetry { #opentelemetry }

Wenn Ihre API läuft, möchten Sie vielleicht wissen, wie viel Traffic sie erhält, welche Requests langsam sind und wann Fehler auftreten.

**Telemetrie** sind Daten über das Verhalten Ihrer Anwendung, die Ihnen helfen, diese Fragen zu beantworten. Häufige Arten sind:

- **Metriken**: Messwerte, die Sie über die Zeit zusammenfassen können, etwa Responsezeiten und die Anzahl der Requests, die verarbeitet werden.
- **Traces**: Aufzeichnungen einzelner Requests und der Operationen, die zu deren Verarbeitung ausgeführt werden. Jede zeitlich gemessene Operation wird **Span** genannt.
- **Logs**: mit Zeitstempel versehene Aufzeichnungen von Events, etwa dass eine Anwendung startet oder eine Operation fehlschlägt.

[**OpenTelemetry**](https://opentelemetry.io/) ist eine Sammlung von Standards und Tools zum Sammeln von Telemetrie und zum Senden dieser Daten an einen Monitoring-Dienst, wo Sie sie in Dashboards untersuchen können.

**FastAPI bietet standardmäßig OpenTelemetry-Unterstützung** für HTTP-Request-Traces, Metriken und Logs. WebSocket-Verbindungen liefern ebenfalls Traces und Logs. Um diese Daten zu sehen, konfigurieren Sie einen Monitoring-Dienst, der sie empfängt.

## FastAPI installieren { #install-fastapi }

Installieren Sie FastAPI mit den `standard`-Extras, welche die Pakete zum Senden von Telemetrie enthalten:

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## Die Anwendung erstellen { #create-the-app }

Erstellen Sie eine Datei `main.py`:

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

Beachten Sie, dass all das standardmäßig funktioniert; Sie müssen keinen eigenen Code schreiben, damit Telemetrie funktioniert.

## FastAPI Cloud { #fastapi-cloud }

Wenn Sie mit `fastapi[standard]` auf [FastAPI Cloud](https://fastapicloud.com) deployen, funktionieren Metriken automatisch. Sie müssen sonst nichts konfigurieren.

Bei Pro-Tarifen können Sie Request-Anzahlen, Fehlerraten und Responsezeiten im [Metrik-Dashboard](https://fastapicloud.com/docs/monitoring-and-performance/metrics/) ansehen.

<img src="/img/tutorial/opentelemetry/image01.png" alt="FastAPI-Cloud-Pro-Metrik-Dashboard mit Beispieldaten">

## Andere Monitoring-Dienste { #other-monitoring-services }

Um Telemetrie an einen anderen Monitoring-Dienst zu senden, konfigurieren Sie einen Endpoint, der **OTLP** akzeptiert, das OpenTelemetry-Protokoll zum Senden von Telemetrie. Verwenden Sie den HTTP/protobuf-Basis-Endpoint des Dienstes.

Setzen Sie diese Umgebungsvariablen und ersetzen Sie die Beispiel-URL durch Ihren Endpoint:

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME` identifiziert Ihre Anwendung im Monitoring-Dienst. Der Endpoint ist die Basis-URL zum Empfangen von Daten. Traces werden unter dieser URL an `/v1/traces` gesendet, Metriken an `/v1/metrics` und Logs an `/v1/logs`.

Wenn Ihr Dienst Authentifizierung erfordert, setzen Sie `OTEL_EXPORTER_OTLP_HEADERS` auf die von ihm angegebenen Header, zum Beispiel `api-key=YOUR_API_KEY`.

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

Öffnen Sie Ihren Monitoring-Dienst und suchen Sie `my-api`. Nach dem nächsten Export können Sie einen Trace mit einem `GET /items/{item_id}`-Span sehen, zusammen mit Metriken für Request-Anzahlen, Responsedauer und aktive Requests.

## Telemetrie anpassen { #customize-telemetry }

### Provider und Exporter konfigurieren { #configure-providers-and-exporters }

Ein **Provider** stellt die Objekte bereit, die Traces, Metriken oder Logs aufzeichnen. Seine Konfiguration steuert, wie diese Daten verarbeitet und exportiert werden.

Telemetriebibliotheken können die globalen Provider von OpenTelemetry konfigurieren. Konfigurieren Sie die Bibliothek, bevor die Anwendung startet, und FastAPI verwendet diese Provider automatisch.

Wenn ein OTLP-Endpoint in der Umgebung gesetzt ist, fügt FastAPI jedem aktivierten Provider einen Exporter für dieses Ziel hinzu. Bestehende Exporter senden weiterhin Daten an ihre Ziele.

Konfigurieren Sie jedes Ziel einmal. Wenn eine andere Bibliothek das in der Umgebung angegebene Ziel bereits verarbeitet, deaktivieren Sie ihren Umgebungsexport oder schalten Sie FastAPIs automatische Einrichtung aus:

```python
app = FastAPI(telemetry={"auto_configure": False})
```

Sie können auch direkt einen Provider im `telemetry`-Dictionary übergeben. Zum Beispiel verwendet dieser Provider OpenTelemetrys Konsolen-Exporter, um Request-Spans in Ihrem Terminal auszugeben:

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

Der **Exporter** sendet die Spans an ihr Ziel. `BatchSpanProcessor` gruppiert Spans und sendet sie im Hintergrund. Ersetzen Sie den Konsolen-Exporter durch einen Exporter, der von Ihrer Monitoring-Bibliothek bereitgestellt wird, um deren Ziel zu verwenden. Weitere Konfigurationsoptionen finden Sie in der [Python-Instrumentierungsanleitung von OpenTelemetry](https://opentelemetry.io/docs/languages/python/instrumentation/).

Verwenden Sie `meter_provider` oder `logger_provider` im selben Dictionary, um einen Metrik- oder Logs-Provider bereitzustellen. Die Anwendung oder Bibliothek, die einen Provider erstellt, verwaltet dessen Herunterfahren. FastAPI verwaltet die Exportkomponenten, die es hinzufügt.

/// warning | Achtung

OpenTelemetry verwendet standardmäßig globale Provider. Eine unabhängige Telemetriekonfiguration für [gemountete Sub-Anwendungen](sub-applications.md) ist nicht garantiert.

///

### Request-Operationen tracen { #trace-request-operations }

Standardmäßig enthalten Request-Traces Spans für das Auflösen von Abhängigkeiten, das Ausführen Ihrer Pfadoperation-Funktion, das Serialisieren der Response und das Ausführen jedes Tasks in FastAPIs `BackgroundTasks`. Diese Spans verwenden denselben Provider und dieselben Exporter.

Hintergrundtask-Spans bleiben Teil des Traces des Requests. Sie werden ausgeführt, nachdem der HTTP-Response-Span endet, und erhöhen daher nicht die gemessene Responsezeit.

Um nur den HTTP-Request-Span aufzuzeichnen, setzen Sie `operation_spans` auf `False`:

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### WebSocket-Verbindungen tracen { #trace-websocket-connections }

Jede WebSocket-Verbindung hat einen Span wie `WS /ws/{room}`, der den Handler und die Bereinigung der Abhängigkeiten umfasst. Er verwendet dieselben Provider und Einstellungen, einschließlich `operation_spans` für die Auflösung von Abhängigkeiten und die Ausführung des Endpoints.

HTTP-Request-Metriken decken nur HTTP-Requests ab. Normale WebSocket-Trennungen mit den Codes `1000` oder `1001` erzeugen keine Error-Logs.

### Fehler untersuchen { #inspect-errors }

FastAPI zeichnet unbehandelte Exceptions als OpenTelemetry-Logs auf, die mit dem Trace des Requests oder der Verbindung verknüpft sind. Error-Logs werden auch dann aufgezeichnet, wenn der Trace nicht gesampelt wird.

Exception-Logs enthalten den Typ, die Nachricht und den Stacktrace der Exception. Nachrichten und Stacktraces können vertrauliche Informationen enthalten. Verwenden Sie die Log-Prozessoren Ihres Providers, um sie zu filtern oder zu schwärzen, oder setzen Sie `logs` auf `False`, um diese Logs zu deaktivieren.

FastAPI zeichnet außerdem Request-Validierungsfehler als Warning-Logs mit der Route und der Fehleranzahl auf. Diese Logs enthalten nicht die ungültige Eingabe.

## Auswählen, was aufgezeichnet werden soll { #choose-what-to-record }

Das `telemetry`-Dictionary akzeptiert außerdem diese Einstellungen:

| Einstellung | Zweck | Defaultwert |
| --- | --- | --- |
| `tracing` | HTTP-Request- und WebSocket-Verbindungsspans aufzeichnen | `True` |
| `metrics` | HTTP-Request-Metriken aufzeichnen | `True` |
| `logs` | Validierungsfehler und unbehandelte Exceptions aufzeichnen | `True` |
| `operation_spans` | Spans für Request-Operationen hinzufügen | `True` |
| `exclude` | Requests überspringen, wenn eine Funktion, die den ASGI-Scope erhält, `True` zurückgibt | `None` |
| `auto_configure` | Exporter für Endpoints hinzufügen, die in Umgebungsvariablen gesetzt sind | `True` |

Zum Beispiel, um Metriken zu sammeln und dabei Healthchecks auszuschließen:

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

Setzen Sie `auto_configure` auf `False`, wenn Ihre Anwendung die Provider-Einrichtung selbst übernimmt, etwa innerhalb ihrer Lifespan-Funktion.
