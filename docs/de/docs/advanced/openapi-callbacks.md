# OpenAPI-Callbacks { #openapi-callbacks }

Sie könnten eine API mit einer *Pfadoperation* erstellen, die einen <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> an eine *externe API* auslösen könnte, welche von jemand anderem erstellt wurde (wahrscheinlich derselbe Entwickler, der Ihre API *verwenden* würde).

Der Vorgang, der stattfindet, wenn Ihre API-Anwendung die *externe API* aufruft, wird als <abbr title="„Rückruf“">„Callback“</abbr> bezeichnet. Denn die Software, die der externe Entwickler geschrieben hat, sendet einen Request an Ihre API und dann *ruft Ihre API zurück* (*calls back*) und sendet einen Request an eine *externe API* (die wahrscheinlich vom selben Entwickler erstellt wurde).

In diesem Fall möchten Sie möglicherweise dokumentieren, wie diese externe API aussehen *sollte*. Welche *Pfadoperation* sie haben sollte, welchen Body sie erwarten sollte, welche <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> sie zurückgeben sollte, usw.

## Eine Anwendung mit Callbacks { #an-app-with-callbacks }

Sehen wir uns das alles anhand eines Beispiels an.

Stellen Sie sich vor, Sie entwickeln eine Anwendung, mit der Sie Rechnungen erstellen können.

Diese Rechnungen haben eine `id`, einen optionalen `title`, einen `customer` (Kunde) und ein `total` (Gesamtsumme).

Der Benutzer Ihrer API (ein externer Entwickler) erstellt mit einem POST-Request eine Rechnung in Ihrer API.

Dann wird Ihre API (stellen wir uns vor):

* die Rechnung an einen Kunden des externen Entwicklers senden.
* das Geld einsammeln.
* eine Benachrichtigung an den API-Benutzer (den externen Entwickler) zurücksenden.
    * Dies erfolgt durch Senden eines POST-Requests (von *Ihrer API*) an eine *externe API*, die von diesem externen Entwickler bereitgestellt wird (das ist der „Callback“).

## Die normale **FastAPI**-Anwendung { #the-normal-fastapi-app }

Sehen wir uns zunächst an, wie die normale API-Anwendung aussehen würde, bevor wir den Callback hinzufügen.

Sie verfügt über eine *Pfadoperation*, die einen `Invoice`-Body empfängt, und einen Query-Parameter `callback_url`, der die URL für den Callback enthält.

Dieser Teil ist ziemlich normal, der größte Teil des Codes ist Ihnen wahrscheinlich bereits bekannt:

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[9:13,36:53] *}

/// tip | Tipp

Der Query-Parameter `callback_url` verwendet einen Pydantic-<a href="https://docs.pydantic.dev/latest/api/networks/" class="external-link" target="_blank">Url</a>-Typ.

///

Das einzig Neue ist `callbacks=invoices_callback_router.routes` als Argument für den *Pfadoperation-Dekorator*. Wir werden als Nächstes sehen, was das ist.

## Dokumentation des Callbacks { #documenting-the-callback }

Der tatsächliche Callback-Code hängt stark von Ihrer eigenen API-Anwendung ab.

Und er wird wahrscheinlich von Anwendung zu Anwendung sehr unterschiedlich sein.

Es könnten nur eine oder zwei Codezeilen sein, wie zum Beispiel:

```Python
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

Der möglicherweise wichtigste Teil des Callbacks besteht jedoch darin, sicherzustellen, dass Ihr API-Benutzer (der externe Entwickler) die *externe API* gemäß den Daten, die *Ihre API* im Requestbody des Callbacks senden wird, korrekt implementiert, usw.

Als Nächstes fügen wir den Code hinzu, um zu dokumentieren, wie diese *externe API* aussehen sollte, um den Callback von *Ihrer API* zu empfangen.

Diese Dokumentation wird in der Swagger-Oberfläche unter `/docs` in Ihrer API angezeigt und zeigt externen Entwicklern, wie diese die *externe API* erstellen sollten.

In diesem Beispiel wird nicht der Callback selbst implementiert (das könnte nur eine Codezeile sein), sondern nur der Dokumentationsteil.

/// tip | Tipp

Der eigentliche Callback ist nur ein HTTP-Request.

Wenn Sie den Callback selbst implementieren, können Sie beispielsweise <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> oder <a href="https://requests.readthedocs.io/" class="external-link" target="_blank">Requests</a> verwenden.

///

## Schreiben des Codes, der den Callback dokumentiert { #write-the-callback-documentation-code }

Dieser Code wird nicht in Ihrer Anwendung ausgeführt, wir benötigen ihn nur, um zu *dokumentieren*, wie diese *externe API* aussehen soll.

Sie wissen jedoch bereits, wie Sie mit **FastAPI** ganz einfach eine automatische Dokumentation für eine API erstellen.

Daher werden wir dasselbe Wissen nutzen, um zu dokumentieren, wie die *externe API* aussehen sollte ... indem wir die *Pfadoperation(en)* erstellen, welche die externe API implementieren soll (die, welche Ihre API aufruft).

/// tip | Tipp

Wenn Sie den Code zum Dokumentieren eines Callbacks schreiben, kann es hilfreich sein, sich vorzustellen, dass Sie dieser *externe Entwickler* sind. Und dass Sie derzeit die *externe API* implementieren, nicht *Ihre API*.

Wenn Sie diese Sichtweise (des *externen Entwicklers*) vorübergehend übernehmen, wird es offensichtlicher, wo die Parameter, das Pydantic-Modell für den Body, die Response, usw. für diese *externe API* hingehören.

///

### Einen Callback-`APIRouter` erstellen { #create-a-callback-apirouter }

Erstellen Sie zunächst einen neuen `APIRouter`, der einen oder mehrere Callbacks enthält.

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[3,25] *}

### Die Callback-*Pfadoperation* erstellen { #create-the-callback-path-operation }

Um die Callback-*Pfadoperation* zu erstellen, verwenden Sie denselben `APIRouter`, den Sie oben erstellt haben.

Sie sollte wie eine normale FastAPI-*Pfadoperation* aussehen:

* Sie sollte wahrscheinlich eine Deklaration des Bodys enthalten, die sie erhalten soll, z. B. `body: InvoiceEvent`.
* Und sie könnte auch eine Deklaration der Response enthalten, die zurückgegeben werden soll, z. B. `response_model=InvoiceEventReceived`.

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[16:18,21:22,28:32] *}

Es gibt zwei Hauptunterschiede zu einer normalen *Pfadoperation*:

* Es muss kein tatsächlicher Code vorhanden sein, da Ihre Anwendung diesen Code niemals aufruft. Sie wird nur zur Dokumentation der *externen API* verwendet. Die Funktion könnte also einfach `pass` enthalten.
* Der *Pfad* kann einen <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression" class="external-link" target="_blank">OpenAPI-3-Ausdruck</a> enthalten (mehr dazu weiter unten), wo er Variablen mit Parametern und Teilen des ursprünglichen Requests verwenden kann, der an *Ihre API* gesendet wurde.

### Der Callback-Pfadausdruck { #the-callback-path-expression }

Der Callback-*Pfad* kann einen <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression" class="external-link" target="_blank">OpenAPI-3-Ausdruck</a> enthalten, welcher Teile des ursprünglichen Requests enthalten kann, der an *Ihre API* gesendet wurde.

In diesem Fall ist es der `str`:

```Python
"{$callback_url}/invoices/{$request.body.id}"
```

Wenn Ihr API-Benutzer (der externe Entwickler) also einen Request an *Ihre API* sendet, via:

```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

mit einem JSON-Körper:

```JSON
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

dann verarbeitet *Ihre API* die Rechnung und sendet irgendwann später einen Callback-Request an die `callback_url` (die *externe API*):

```
https://www.external.org/events/invoices/2expen51ve
```

mit einem JSON-Body, der etwa Folgendes enthält:

```JSON
{
    "description": "Payment celebration",
    "paid": true
}
```

und sie würde eine Response von dieser *externen API* mit einem JSON-Body wie dem folgenden erwarten:

```JSON
{
    "ok": true
}
```

/// tip | Tipp

Beachten Sie, dass die verwendete Callback-URL die URL enthält, die als Query-Parameter in `callback_url` (`https://www.external.org/events`) empfangen wurde, und auch die Rechnungs-`id` aus dem JSON-Body (`2expen51ve`).

///

### Den Callback-Router hinzufügen { #add-the-callback-router }

An diesem Punkt haben Sie die benötigte(n) *Callback-Pfadoperation(en)* (diejenige(n), die der *externe Entwickler* in der *externen API* implementieren sollte) im Callback-Router, den Sie oben erstellt haben.

Verwenden Sie nun den Parameter `callbacks` im *Pfadoperation-Dekorator Ihrer API*, um das Attribut `.routes` (das ist eigentlich nur eine `list`e von Routen/*Pfadoperationen*) dieses Callback-Routers zu übergeben:

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[35] *}

/// tip | Tipp

Beachten Sie, dass Sie nicht den Router selbst (`invoices_callback_router`) an `callback=` übergeben, sondern das Attribut `.routes`, wie in `invoices_callback_router.routes`.

///

### Es in der Dokumentation testen { #check-the-docs }

Jetzt können Sie Ihre Anwendung starten und auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> gehen.

Sie sehen Ihre Dokumentation, einschließlich eines Abschnitts „Callbacks“ für Ihre *Pfadoperation*, der zeigt, wie die *externe API* aussehen sollte:

<img src="/img/tutorial/openapi-callbacks/image01.png">
