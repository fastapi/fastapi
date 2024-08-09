# Middleware

Sie können Middleware zu **FastAPI**-Anwendungen hinzufügen.

Eine „Middleware“ ist eine Funktion, die mit jedem **Request** arbeitet, bevor er von einer bestimmten *Pfadoperation* verarbeitet wird. Und auch mit jeder **Response**, bevor sie zurückgegeben wird.

* Sie nimmt jeden **Request** entgegen, der an Ihre Anwendung gesendet wird.
* Sie kann dann etwas mit diesem **Request** tun oder beliebigen Code ausführen.
* Dann gibt sie den **Request** zur Verarbeitung durch den Rest der Anwendung weiter (durch eine bestimmte *Pfadoperation*).
* Sie nimmt dann die **Response** entgegen, die von der Anwendung generiert wurde (durch eine bestimmte *Pfadoperation*).
* Sie kann etwas mit dieser **Response** tun oder beliebigen Code ausführen.
* Dann gibt sie die **Response** zurück.

/// note | "Technische Details"

Wenn Sie Abhängigkeiten mit `yield` haben, wird der Exit-Code *nach* der Middleware ausgeführt.

Wenn es Hintergrundaufgaben gab (später dokumentiert), werden sie *nach* allen Middlewares ausgeführt.

///

## Erstellung einer Middleware

Um eine Middleware zu erstellen, verwenden Sie den Dekorator `@app.middleware("http")` über einer Funktion.

Die Middleware-Funktion erhält:

* Den `request`.
* Eine Funktion `call_next`, die den `request` als Parameter erhält.
    * Diese Funktion gibt den `request` an die entsprechende *Pfadoperation* weiter.
    * Dann gibt es die von der entsprechenden *Pfadoperation* generierte `response` zurück.
* Sie können die `response` dann weiter modifizieren, bevor Sie sie zurückgeben.

```Python hl_lines="8-9  11  14"
{!../../../docs_src/middleware/tutorial001.py!}
```

/// tip | "Tipp"

Beachten Sie, dass benutzerdefinierte proprietäre Header hinzugefügt werden können. <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">Verwenden Sie dafür das Präfix 'X-'</a>.

Wenn Sie jedoch benutzerdefinierte Header haben, die ein Client in einem Browser sehen soll, müssen Sie sie zu Ihrer CORS-Konfigurationen ([CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank}) hinzufügen, indem Sie den Parameter `expose_headers` verwenden, der in der <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette-CORS-Dokumentation</a> dokumentiert ist.

///

/// note | "Technische Details"

Sie könnten auch `from starlette.requests import Request` verwenden.

**FastAPI** bietet es als Komfort für Sie, den Entwickler, an. Aber es stammt direkt von Starlette.

///

### Vor und nach der `response`

Sie können Code hinzufügen, der mit dem `request` ausgeführt wird, bevor dieser von einer beliebigen *Pfadoperation* empfangen wird.

Und auch nachdem die `response` generiert wurde, bevor sie zurückgegeben wird.

Sie könnten beispielsweise einen benutzerdefinierten Header `X-Process-Time` hinzufügen, der die Zeit in Sekunden enthält, die benötigt wurde, um den Request zu verarbeiten und eine Response zu generieren:

```Python hl_lines="10  12-13"
{!../../../docs_src/middleware/tutorial001.py!}
```

## Andere Middlewares

Sie können später mehr über andere Middlewares in [Handbuch für fortgeschrittene Benutzer: Fortgeschrittene Middleware](../advanced/middleware.md){.internal-link target=_blank} lesen.

In der nächsten Sektion erfahren Sie, wie Sie <abbr title="Cross-Origin Resource Sharing">CORS</abbr> mit einer Middleware behandeln können.
