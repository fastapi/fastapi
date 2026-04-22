# Middleware { #middleware }

Sie können Middleware zu **FastAPI**-Anwendungen hinzufügen.

Eine „Middleware“ ist eine Funktion, die mit jedem **<abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr>** arbeitet, bevor er von einer bestimmten *Pfadoperation* verarbeitet wird. Und auch mit jeder **<abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>**, bevor sie zurückgegeben wird.

* Sie nimmt jeden **Request** entgegen, der an Ihre Anwendung gesendet wird.
* Sie kann dann etwas mit diesem **Request** tun oder beliebigen Code ausführen.
* Dann gibt sie den **Request** zur Verarbeitung durch den Rest der Anwendung weiter (durch eine bestimmte *Pfadoperation*).
* Sie nimmt dann die **Response** entgegen, die von der Anwendung generiert wurde (durch eine bestimmte *Pfadoperation*).
* Sie kann etwas mit dieser **Response** tun oder beliebigen Code ausführen.
* Dann gibt sie die **Response** zurück.

/// note | Technische Details

Wenn Sie Abhängigkeiten mit `yield` haben, wird der Exit-Code *nach* der Middleware ausgeführt.

Wenn es Hintergrundtasks gab (dies wird später im [Hintergrundtasks](background-tasks.md)-Abschnitt behandelt), werden sie *nach* allen Middlewares ausgeführt.

///

## Eine Middleware erstellen { #create-a-middleware }

Um eine Middleware zu erstellen, verwenden Sie den Dekorator `@app.middleware("http")` über einer Funktion.

Die Middleware-Funktion erhält:

* Den `request`.
* Eine Funktion `call_next`, die den `request` als Parameter erhält.
    * Diese Funktion gibt den `request` an die entsprechende *Pfadoperation* weiter.
    * Dann gibt es die von der entsprechenden *Pfadoperation* generierte `response` zurück.
* Sie können die `response` dann weiter modifizieren, bevor Sie sie zurückgeben.

{* ../../docs_src/middleware/tutorial001_py310.py hl[8:9,11,14] *}

/// tip | Tipp

Beachten Sie, dass benutzerdefinierte proprietäre Header hinzugefügt werden können [unter Verwendung des `X-`-Präfixes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers).

Wenn Sie jedoch benutzerdefinierte Header haben, die ein Client in einem Browser sehen soll, müssen Sie sie zu Ihrer CORS-Konfiguration ([CORS (Cross-Origin Resource Sharing)](cors.md)) hinzufügen, indem Sie den Parameter `expose_headers` verwenden, der in [Starlettes CORS-Dokumentation](https://www.starlette.dev/middleware/#corsmiddleware) dokumentiert ist.

///

/// note | Technische Details

Sie könnten auch `from starlette.requests import Request` verwenden.

**FastAPI** bietet es als Komfort für Sie, den Entwickler, an. Aber es stammt direkt von Starlette.

///

### Vor und nach der `response` { #before-and-after-the-response }

Sie können Code hinzufügen, der mit dem `request` ausgeführt wird, bevor dieser von einer beliebigen *Pfadoperation* empfangen wird.

Und auch nachdem die `response` generiert wurde, bevor sie zurückgegeben wird.

Sie könnten beispielsweise einen benutzerdefinierten Header `X-Process-Time` hinzufügen, der die Zeit in Sekunden enthält, die benötigt wurde, um den Request zu verarbeiten und eine Response zu generieren:

{* ../../docs_src/middleware/tutorial001_py310.py hl[10,12:13] *}

/// tip | Tipp

Hier verwenden wir [`time.perf_counter()`](https://docs.python.org/3/library/time.html#time.perf_counter) anstelle von `time.time()`, da es für diese Anwendungsfälle präziser sein kann. 🤓

///

## Ausführungsreihenfolge bei mehreren Middlewares { #multiple-middleware-execution-order }

Wenn Sie mehrere Middlewares hinzufügen, entweder mit dem `@app.middleware()` Dekorator oder der Methode `app.add_middleware()`, umschließt jede neue Middleware die Anwendung und bildet einen Stapel. Die zuletzt hinzugefügte Middleware ist die *äußerste*, und die erste ist die *innerste*.

Auf dem Requestpfad läuft die *äußerste* Middleware zuerst.

Auf dem Responsepfad läuft sie zuletzt.

Zum Beispiel:

```Python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

Dies führt zu folgender Ausführungsreihenfolge:

* **Request**: MiddlewareB → MiddlewareA → Route

* **Response**: Route → MiddlewareA → MiddlewareB

Dieses Stapelverhalten stellt sicher, dass Middlewares in einer vorhersehbaren und kontrollierbaren Reihenfolge ausgeführt werden.

## Andere Middlewares { #other-middlewares }

Sie können später mehr über andere Middlewares im [Handbuch für fortgeschrittene Benutzer: Fortgeschrittene Middleware](../advanced/middleware.md) lesen.

In der nächsten Sektion erfahren Sie, wie Sie <abbr title="Cross-Origin Resource Sharing – Ressourcenfreigabe zwischen Ursprüngen">CORS</abbr> mit einer Middleware behandeln können.
