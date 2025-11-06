# Benutzerdefinierte Request- und APIRoute-Klasse { #custom-request-and-apiroute-class }

In einigen Fällen möchten Sie möglicherweise die von den Klassen `Request` und `APIRoute` verwendete Logik überschreiben.

Das kann insbesondere eine gute Alternative zur Logik in einer Middleware sein.

Wenn Sie beispielsweise den <abbr title="Anfragekörper">Requestbody</abbr> lesen oder manipulieren möchten, bevor er von Ihrer Anwendung verarbeitet wird.

/// danger | Gefahr

Dies ist eine „fortgeschrittene“ Funktion.

Wenn Sie gerade erst mit **FastAPI** beginnen, möchten Sie diesen Abschnitt vielleicht überspringen.

///

## Anwendungsfälle { #use-cases }

Einige Anwendungsfälle sind:

* Konvertieren von Nicht-JSON-Requestbodys nach JSON (z. B. <a href="https://msgpack.org/index.html" class="external-link" target="_blank">`msgpack`</a>).
* Dekomprimierung gzip-komprimierter Requestbodys.
* Automatisches Loggen aller Requestbodys.

## Handhaben von benutzerdefinierten Requestbody-Kodierungen { #handling-custom-request-body-encodings }

Sehen wir uns an, wie Sie eine benutzerdefinierte `Request`-Unterklasse verwenden, um gzip-Requests zu dekomprimieren.

Und eine `APIRoute`-Unterklasse zur Verwendung dieser benutzerdefinierten Requestklasse.

### Eine benutzerdefinierte `GzipRequest`-Klasse erstellen { #create-a-custom-gziprequest-class }

/// tip | Tipp

Dies ist nur ein einfaches Beispiel, um zu demonstrieren, wie es funktioniert. Wenn Sie Gzip-Unterstützung benötigen, können Sie die bereitgestellte [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware){.internal-link target=_blank} verwenden.

///

Zuerst erstellen wir eine `GzipRequest`-Klasse, welche die Methode `Request.body()` überschreibt, um den Body bei Vorhandensein eines entsprechenden Headers zu dekomprimieren.

Wenn der Header kein `gzip` enthält, wird nicht versucht, den Body zu dekomprimieren.

Auf diese Weise kann dieselbe Routenklasse gzip-komprimierte oder unkomprimierte Requests verarbeiten.

{* ../../docs_src/custom_request_and_route/tutorial001.py hl[8:15] *}

### Eine benutzerdefinierte `GzipRoute`-Klasse erstellen { #create-a-custom-gziproute-class }

Als Nächstes erstellen wir eine benutzerdefinierte Unterklasse von `fastapi.routing.APIRoute`, welche `GzipRequest` nutzt.

Dieses Mal wird die Methode `APIRoute.get_route_handler()` überschrieben.

Diese Methode gibt eine Funktion zurück. Und diese Funktion empfängt einen <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> und gibt eine <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> zurück.

Hier verwenden wir sie, um aus dem ursprünglichen Request einen `GzipRequest` zu erstellen.

{* ../../docs_src/custom_request_and_route/tutorial001.py hl[18:26] *}

/// note | Technische Details

Ein `Request` hat ein `request.scope`-Attribut, welches einfach ein Python-<abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">`dict`</abbr> ist, welches die mit dem Request verbundenen Metadaten enthält.

Ein `Request` hat auch ein `request.receive`, welches eine Funktion ist, die den Body des Requests <abbr title="Englisch „receive“">empfängt</abbr>.

Das `scope`-`dict` und die `receive`-Funktion sind beide Teil der ASGI-Spezifikation.

Und diese beiden Dinge, `scope` und `receive`, werden benötigt, um eine neue `Request`-Instanz zu erstellen.

Um mehr über den `Request` zu erfahren, schauen Sie sich <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">Starlettes Dokumentation zu Requests</a> an.

///

Das Einzige, was die von `GzipRequest.get_route_handler` zurückgegebene Funktion anders macht, ist die Konvertierung von `Request` in ein `GzipRequest`.

Dabei kümmert sich unser `GzipRequest` um die Dekomprimierung der Daten (falls erforderlich), bevor diese an unsere *Pfadoperationen* weitergegeben werden.

Danach ist die gesamte Verarbeitungslogik dieselbe.

Aufgrund unserer Änderungen in `GzipRequest.body` wird der Requestbody jedoch bei Bedarf automatisch dekomprimiert, wenn er von **FastAPI** geladen wird.

## Zugriff auf den Requestbody in einem Exceptionhandler { #accessing-the-request-body-in-an-exception-handler }

/// tip | Tipp

Um dasselbe Problem zu lösen, ist es wahrscheinlich viel einfacher, den `body` in einem benutzerdefinierten Handler für `RequestValidationError` zu verwenden ([Fehlerbehandlung](../tutorial/handling-errors.md#use-the-requestvalidationerror-body){.internal-link target=_blank}).

Dieses Beispiel ist jedoch immer noch gültig und zeigt, wie mit den internen Komponenten interagiert wird.

///

Wir können denselben Ansatz auch verwenden, um in einem Exceptionhandler auf den Requestbody zuzugreifen.

Alles, was wir tun müssen, ist, den Request innerhalb eines `try`/`except`-Blocks zu handhaben:

{* ../../docs_src/custom_request_and_route/tutorial002.py hl[13,15] *}

Wenn eine Exception auftritt, befindet sich die `Request`-Instanz weiterhin im Gültigkeitsbereich, sodass wir den Requestbody lesen und bei der Fehlerbehandlung verwenden können:

{* ../../docs_src/custom_request_and_route/tutorial002.py hl[16:18] *}

## Benutzerdefinierte `APIRoute`-Klasse in einem Router { #custom-apiroute-class-in-a-router }

Sie können auch den Parameter `route_class` eines `APIRouter` festlegen:

{* ../../docs_src/custom_request_and_route/tutorial003.py hl[26] *}

In diesem Beispiel verwenden die *Pfadoperationen* unter dem `router` die benutzerdefinierte `TimedRoute`-Klasse und haben in der Response einen zusätzlichen `X-Response-Time`-Header mit der Zeit, die zum Generieren der Response benötigt wurde:

{* ../../docs_src/custom_request_and_route/tutorial003.py hl[13:20] *}
