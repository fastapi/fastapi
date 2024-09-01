# Benutzerdefinierte Request- und APIRoute-Klasse

In einigen Fällen möchten Sie möglicherweise die von den Klassen `Request` und `APIRoute` verwendete Logik überschreiben.

Das kann insbesondere eine gute Alternative zur Logik in einer Middleware sein.

Wenn Sie beispielsweise den Requestbody lesen oder manipulieren möchten, bevor er von Ihrer Anwendung verarbeitet wird.

/// danger | "Gefahr"

Dies ist eine „fortgeschrittene“ Funktion.

Wenn Sie gerade erst mit **FastAPI** beginnen, möchten Sie diesen Abschnitt vielleicht überspringen.

///

## Anwendungsfälle

Einige Anwendungsfälle sind:

* Konvertieren von Nicht-JSON-Requestbodys nach JSON (z. B. <a href="https://msgpack.org/index.html" class="external-link" target="_blank">`msgpack`</a>).
* Dekomprimierung gzip-komprimierter Requestbodys.
* Automatisches Loggen aller Requestbodys.

## Handhaben von benutzerdefinierten Requestbody-Kodierungen

Sehen wir uns an, wie Sie eine benutzerdefinierte `Request`-Unterklasse verwenden, um gzip-Requests zu dekomprimieren.

Und eine `APIRoute`-Unterklasse zur Verwendung dieser benutzerdefinierten Requestklasse.

### Eine benutzerdefinierte `GzipRequest`-Klasse erstellen

/// tip | "Tipp"

Dies ist nur ein einfaches Beispiel, um zu demonstrieren, wie es funktioniert. Wenn Sie Gzip-Unterstützung benötigen, können Sie die bereitgestellte [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware){.internal-link target=_blank} verwenden.

///

Zuerst erstellen wir eine `GzipRequest`-Klasse, welche die Methode `Request.body()` überschreibt, um den Body bei Vorhandensein eines entsprechenden Headers zu dekomprimieren.

Wenn der Header kein `gzip` enthält, wird nicht versucht, den Body zu dekomprimieren.

Auf diese Weise kann dieselbe Routenklasse gzip-komprimierte oder unkomprimierte Requests verarbeiten.

```Python hl_lines="8-15"
{!../../../docs_src/custom_request_and_route/tutorial001.py!}
```

### Eine benutzerdefinierte `GzipRoute`-Klasse erstellen

Als Nächstes erstellen wir eine benutzerdefinierte Unterklasse von `fastapi.routing.APIRoute`, welche `GzipRequest` nutzt.

Dieses Mal wird die Methode `APIRoute.get_route_handler()` überschrieben.

Diese Methode gibt eine Funktion zurück. Und diese Funktion empfängt einen Request und gibt eine Response zurück.

Hier verwenden wir sie, um aus dem ursprünglichen Request einen `GzipRequest` zu erstellen.

```Python hl_lines="18-26"
{!../../../docs_src/custom_request_and_route/tutorial001.py!}
```

/// note | "Technische Details"

Ein `Request` hat ein `request.scope`-Attribut, welches einfach ein Python-`dict` ist, welches die mit dem Request verbundenen Metadaten enthält.

Ein `Request` hat auch ein `request.receive`, welches eine Funktion ist, die den Hauptteil des Requests empfängt.

Das `scope`-`dict` und die `receive`-Funktion sind beide Teil der ASGI-Spezifikation.

Und diese beiden Dinge, `scope` und `receive`, werden benötigt, um eine neue `Request`-Instanz zu erstellen.

Um mehr über den `Request` zu erfahren, schauen Sie sich <a href="https://www.starlette.io/requests/" class="external-link" target="_blank">Starlettes Dokumentation zu Requests</a> an.

///

Das Einzige, was die von `GzipRequest.get_route_handler` zurückgegebene Funktion anders macht, ist die Konvertierung von `Request` in ein `GzipRequest`.

Dabei kümmert sich unser `GzipRequest` um die Dekomprimierung der Daten (falls erforderlich), bevor diese an unsere *Pfadoperationen* weitergegeben werden.

Danach ist die gesamte Verarbeitungslogik dieselbe.

Aufgrund unserer Änderungen in `GzipRequest.body` wird der Requestbody jedoch bei Bedarf automatisch dekomprimiert, wenn er von **FastAPI** geladen wird.

## Zugriff auf den Requestbody in einem Exceptionhandler

/// tip | "Tipp"

Um dasselbe Problem zu lösen, ist es wahrscheinlich viel einfacher, den `body` in einem benutzerdefinierten Handler für `RequestValidationError` zu verwenden ([Fehlerbehandlung](../tutorial/handling-errors.md#den-requestvalidationerror-body-verwenden){.internal-link target=_blank}).

Dieses Beispiel ist jedoch immer noch gültig und zeigt, wie mit den internen Komponenten interagiert wird.

///

Wir können denselben Ansatz auch verwenden, um in einem Exceptionhandler auf den Requestbody zuzugreifen.

Alles, was wir tun müssen, ist, den Request innerhalb eines `try`/`except`-Blocks zu handhaben:

```Python hl_lines="13  15"
{!../../../docs_src/custom_request_and_route/tutorial002.py!}
```

Wenn eine Exception auftritt, befindet sich die `Request`-Instanz weiterhin im Gültigkeitsbereich, sodass wir den Requestbody lesen und bei der Fehlerbehandlung verwenden können:

```Python hl_lines="16-18"
{!../../../docs_src/custom_request_and_route/tutorial002.py!}
```

## Benutzerdefinierte `APIRoute`-Klasse in einem Router

Sie können auch den Parameter `route_class` eines `APIRouter` festlegen:

```Python hl_lines="26"
{!../../../docs_src/custom_request_and_route/tutorial003.py!}
```

In diesem Beispiel verwenden die *Pfadoperationen* unter dem `router` die benutzerdefinierte `TimedRoute`-Klasse und haben in der Response einen zusätzlichen `X-Response-Time`-Header mit der Zeit, die zum Generieren der Response benötigt wurde:

```Python hl_lines="13-20"
{!../../../docs_src/custom_request_and_route/tutorial003.py!}
```
