# SDKs generieren { #generating-sdks }

Da **FastAPI** auf der **OpenAPI**-Spezifikation basiert, können dessen APIs in einem standardisierten Format beschrieben werden, das viele Tools verstehen.

Dies vereinfacht es, aktuelle **Dokumentation** und Client-Bibliotheken (<abbr title="Software Development Kits - Software-Entwicklungspakete">**SDKs**</abbr>) in verschiedenen Sprachen zu generieren sowie **Test-** oder **Automatisierungs-Workflows**, die mit Ihrem Code synchron bleiben.

In diesem Leitfaden erfahren Sie, wie Sie ein **TypeScript-SDK** für Ihr FastAPI-Backend generieren.

## Open Source SDK-Generatoren { #open-source-sdk-generators }

Eine vielseitige Möglichkeit ist der [OpenAPI Generator](https://openapi-generator.tech/), der **viele Programmiersprachen** unterstützt und SDKs aus Ihrer OpenAPI-Spezifikation generieren kann.

Für **TypeScript-Clients** ist [Hey API](https://heyapi.dev/) eine speziell entwickelte Lösung, die ein optimiertes Erlebnis für das TypeScript-Ökosystem bietet.

Weitere SDK-Generatoren finden Sie auf [OpenAPI.Tools](https://openapi.tools/#sdk).

/// tip | Tipp

FastAPI generiert automatisch **OpenAPI 3.1**-Spezifikationen, daher muss jedes von Ihnen verwendete Tool diese Version unterstützen.

///

## SDK-Generatoren von FastAPI-Sponsoren { #sdk-generators-from-fastapi-sponsors }

Dieser Abschnitt hebt **venture-unterstützte** und **firmengestützte** Lösungen hervor, die von Unternehmen entwickelt werden, welche FastAPI sponsern. Diese Produkte bieten **zusätzliche Funktionen** und **Integrationen** zusätzlich zu hochwertig generierten SDKs.

Durch das ✨ [**Sponsoring von FastAPI**](../help-fastapi.md#sponsor-the-author) ✨ helfen diese Unternehmen sicherzustellen, dass das Framework und sein **Ökosystem** gesund und **nachhaltig** bleiben.

Ihr Sponsoring zeigt auch ein starkes Engagement für die FastAPI-**Community** (Sie), was bedeutet, dass sie nicht nur einen **großartigen Service** bieten möchten, sondern auch ein **robustes und florierendes Framework**, FastAPI, unterstützen möchten. 🙇

Zum Beispiel könnten Sie ausprobieren:

* [Speakeasy](https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship)
* [Stainless](https://www.stainless.com/?utm_source=fastapi&utm_medium=referral)
* [liblab](https://developers.liblab.com/tutorials/sdk-for-fastapi?utm_source=fastapi)

Einige dieser Lösungen sind möglicherweise auch Open Source oder bieten kostenlose Tarife an, sodass Sie diese ohne finanzielle Verpflichtung ausprobieren können. Andere kommerzielle SDK-Generatoren sind online verfügbar und können dort gefunden werden. 🤓

## Ein TypeScript-SDK erstellen { #create-a-typescript-sdk }

Beginnen wir mit einer einfachen FastAPI-Anwendung:

{* ../../docs_src/generate_clients/tutorial001_py310.py hl[7:9,12:13,16:17,21] *}

Beachten Sie, dass die *Pfadoperationen* die Modelle definieren, die sie für die <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr>- und <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>-<abbr title="Die eigentlichen Nutzdaten, abzüglich der Metadaten">Payload</abbr> verwenden, indem sie die Modelle `Item` und `ResponseMessage` verwenden.

### API-Dokumentation { #api-docs }

Wenn Sie zu `/docs` gehen, sehen Sie, dass es die **Schemas** für die Daten enthält, die in Requests gesendet und in Responses empfangen werden:

<img src="/img/tutorial/generate-clients/image01.png">

Sie können diese Schemas sehen, da sie mit den Modellen in der App deklariert wurden.

Diese Informationen sind im **OpenAPI-Schema** der Anwendung verfügbar und werden in der API-Dokumentation angezeigt.

Diese Informationen aus den Modellen, die in OpenAPI enthalten sind, können verwendet werden, um **den Client-Code zu generieren**.

### Hey API { #hey-api }

Sobald wir eine FastAPI-App mit den Modellen haben, können wir Hey API verwenden, um einen TypeScript-Client zu generieren. Der schnellste Weg das zu tun, ist über npx.

```sh
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

Dies generiert ein TypeScript-SDK in `./src/client`.

Sie können lernen, wie man [`@hey-api/openapi-ts` installiert](https://heyapi.dev/openapi-ts/get-started) und über die [erzeugte Ausgabe](https://heyapi.dev/openapi-ts/output) auf deren Website lesen.

### Das SDK verwenden { #using-the-sdk }

Jetzt können Sie den Client-Code importieren und verwenden. Er könnte wie folgt aussehen, beachten Sie, dass Sie eine automatische Vervollständigung für die Methoden erhalten:

<img src="/img/tutorial/generate-clients/image02.png">

Sie werden auch eine automatische Vervollständigung für die zu sendende Payload erhalten:

<img src="/img/tutorial/generate-clients/image03.png">

/// tip | Tipp

Beachten Sie die automatische Vervollständigung für `name` und `price`, die in der FastAPI-Anwendung im `Item`-Modell definiert wurden.

///

Sie erhalten Inline-Fehlerberichte für die von Ihnen gesendeten Daten:

<img src="/img/tutorial/generate-clients/image04.png">

Das Response-Objekt hat auch automatische Vervollständigung:

<img src="/img/tutorial/generate-clients/image05.png">

## FastAPI-Anwendung mit Tags { #fastapi-app-with-tags }

In vielen Fällen wird Ihre FastAPI-App größer sein und Sie werden wahrscheinlich Tags verwenden, um verschiedene Gruppen von *Pfadoperationen* zu separieren.

Zum Beispiel könnten Sie einen Abschnitt für **Items** und einen weiteren Abschnitt für **Users** haben, und diese könnten durch Tags getrennt sein:

{* ../../docs_src/generate_clients/tutorial002_py310.py hl[21,26,34] *}

### Einen TypeScript-Client mit Tags generieren { #generate-a-typescript-client-with-tags }

Wenn Sie einen Client für eine FastAPI-App generieren, die Tags verwendet, wird normalerweise der Client-Code auch anhand der Tags getrennt.

Auf diese Weise können Sie die Dinge für den Client-Code richtig ordnen und gruppieren:

<img src="/img/tutorial/generate-clients/image06.png">

In diesem Fall haben Sie:

* `ItemsService`
* `UsersService`

### Client-Methodennamen { #client-method-names }

Im Moment sehen die generierten Methodennamen wie `createItemItemsPost` nicht sehr sauber aus:

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

... das liegt daran, dass der Client-Generator für jede *Pfadoperation* die OpenAPI-interne **Operation-ID** verwendet.

OpenAPI erfordert, dass jede Operation-ID innerhalb aller *Pfadoperationen* einzigartig ist. Daher verwendet FastAPI den **Funktionsnamen**, den **Pfad** und die **HTTP-Methode/-Operation**, um diese Operation-ID zu generieren. Denn so kann sichergestellt werden, dass die Operation-IDs einzigartig sind.

Aber ich zeige Ihnen als Nächstes, wie Sie das verbessern können. 🤓

## Benutzerdefinierte Operation-IDs und bessere Methodennamen { #custom-operation-ids-and-better-method-names }

Sie können die Art und Weise, wie diese Operation-IDs **generiert** werden, **ändern**, um sie einfacher zu machen und **einfachere Methodennamen** in den Clients zu haben.

In diesem Fall müssen Sie auf andere Weise sicherstellen, dass jede Operation-ID **einzigartig** ist.

Zum Beispiel könnten Sie sicherstellen, dass jede *Pfadoperation* einen Tag hat, und dann die Operation-ID basierend auf dem **Tag** und dem *Pfadoperation*-**Namen** (dem Funktionsnamen) generieren.

### Eine benutzerdefinierte Funktion zur Erzeugung einer eindeutigen ID erstellen { #custom-generate-unique-id-function }

FastAPI verwendet eine **eindeutige ID** für jede *Pfadoperation*, die für die **Operation-ID** und auch für die Namen aller benötigten benutzerdefinierten Modelle für Requests oder Responses verwendet wird.

Sie können diese Funktion anpassen. Sie nimmt ein `APIRoute` und gibt einen String zurück.

Hier verwendet sie beispielsweise den ersten Tag (Sie werden wahrscheinlich nur einen Tag haben) und den *Pfadoperation*-Namen (den Funktionsnamen).

Anschließend können Sie diese benutzerdefinierte Funktion als `generate_unique_id_function`-Parameter an **FastAPI** übergeben:

{* ../../docs_src/generate_clients/tutorial003_py310.py hl[6:7,10] *}

### Einen TypeScript-Client mit benutzerdefinierten Operation-IDs generieren { #generate-a-typescript-client-with-custom-operation-ids }

Wenn Sie nun den Client erneut generieren, werden Sie feststellen, dass er über die verbesserten Methodennamen verfügt:

<img src="/img/tutorial/generate-clients/image07.png">

Wie Sie sehen, haben die Methodennamen jetzt den Tag und dann den Funktionsnamen, aber keine Informationen aus dem URL-Pfad und der HTTP-Operation.

### Die OpenAPI-Spezifikation für den Client-Generator vorab modifizieren { #preprocess-the-openapi-specification-for-the-client-generator }

Der generierte Code enthält immer noch einige **verdoppelte Informationen**.

Wir wissen bereits, dass diese Methode mit den **Items** zusammenhängt, weil dieses Wort in `ItemsService` enthalten ist (vom Tag übernommen), aber wir haben den Tag-Namen dennoch im Methodennamen vorangestellt. 😕

Wir werden das wahrscheinlich weiterhin für OpenAPI allgemein beibehalten wollen, da dadurch sichergestellt wird, dass die Operation-IDs **einzigartig** sind.

Aber für den generierten Client könnten wir die OpenAPI-Operation-IDs direkt vor der Generierung der Clients **modifizieren**, um diese Methodennamen schöner und **sauberer** zu machen.

Wir könnten das OpenAPI-JSON in eine Datei `openapi.json` herunterladen und dann mit einem Skript wie dem folgenden **den präfixierten Tag entfernen**:

{* ../../docs_src/generate_clients/tutorial004_py310.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

Damit würden die Operation-IDs von Dingen wie `items-get_items` in `get_items` umbenannt, sodass der Client-Generator einfachere Methodennamen generieren kann.

### Einen TypeScript-Client mit der vorverarbeiteten OpenAPI generieren { #generate-a-typescript-client-with-the-preprocessed-openapi }

Da das Endergebnis nun in einer `openapi.json`-Datei vorliegt, müssen Sie Ihren Eingabeort aktualisieren:

```sh
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

Nach der Generierung des neuen Clients haben Sie jetzt **saubere Methodennamen**, mit allen **Autovervollständigungen**, **Inline-Fehlerberichten**, usw.:

<img src="/img/tutorial/generate-clients/image08.png">

## Vorteile { #benefits }

Wenn Sie die automatisch generierten Clients verwenden, erhalten Sie **Autovervollständigung** für:

* Methoden.
* Request-Payloads im Body, Query-Parameter, usw.
* Response-Payloads.

Sie erhalten auch **Inline-Fehlerberichte** für alles.

Und wann immer Sie den Backend-Code aktualisieren und **das Frontend neu generieren**, stehen alle neuen *Pfadoperationen* als Methoden zur Verfügung, die alten werden entfernt und alle anderen Änderungen werden im generierten Code reflektiert. 🤓

Das bedeutet auch, dass, wenn sich etwas ändert, dies automatisch im Client-Code **reflektiert** wird. Und wenn Sie den Client **erstellen**, wird eine Fehlermeldung ausgegeben, wenn die verwendeten Daten **nicht übereinstimmen**.

Sie würden also **viele Fehler sehr früh** im Entwicklungszyklus erkennen, anstatt darauf warten zu müssen, dass die Fehler Ihren Endbenutzern in der Produktion angezeigt werden, und dann zu versuchen, zu debuggen, wo das Problem liegt. ✨
