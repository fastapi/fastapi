# Clients generieren

Da **FastAPI** auf der OpenAPI-Spezifikation basiert, erhalten Sie automatische Kompatibilität mit vielen Tools, einschließlich der automatischen API-Dokumentation (bereitgestellt von Swagger UI).

Ein besonderer Vorteil, der nicht unbedingt offensichtlich ist, besteht darin, dass Sie für Ihre API **Clients generieren** können (manchmal auch <abbr title="Software Development Kits">**SDKs**</abbr> genannt), für viele verschiedene **Programmiersprachen**.

## OpenAPI-Client-Generatoren

Es gibt viele Tools zum Generieren von Clients aus **OpenAPI**.

Ein gängiges Tool ist <a href="https://openapi-generator.tech/" class="external-link" target="_blank">OpenAPI Generator</a>.

Wenn Sie ein **Frontend** erstellen, ist <a href="https://github.com/hey-api/openapi-ts" class="external-link" target="_blank">openapi-ts</a> eine sehr interessante Alternative.

## Client- und SDK-Generatoren – Sponsor

Es gibt auch einige **vom Unternehmen entwickelte** Client- und SDK-Generatoren, die auf OpenAPI (FastAPI) basieren. In einigen Fällen können diese Ihnen **weitere Funktionalität** zusätzlich zu qualitativ hochwertigen generierten SDKs/Clients bieten.

Einige von diesen ✨ [**sponsern FastAPI**](../help-fastapi.md#den-autor-sponsern){.internal-link target=_blank} ✨, das gewährleistet die kontinuierliche und gesunde **Entwicklung** von FastAPI und seinem **Ökosystem**.

Und es zeigt deren wahres Engagement für FastAPI und seine **Community** (Sie), da diese Ihnen nicht nur einen **guten Service** bieten möchten, sondern auch sicherstellen möchten, dass Sie über ein **gutes und gesundes Framework** verfügen, FastAPI. 🙇

Beispielsweise könnten Sie <a href="https://speakeasy.com/?utm_source=fastapi+repo&utm_medium=github+sponsorship" class="external-link" target="_blank">Speakeasy</a> ausprobieren.

Es gibt auch mehrere andere Unternehmen, welche ähnliche Dienste anbieten und die Sie online suchen und finden können. 🤓

## Einen TypeScript-Frontend-Client generieren

Beginnen wir mit einer einfachen FastAPI-Anwendung:

//// tab | Python 3.9+

```Python hl_lines="7-9  12-13  16-17  21"
{!> ../../../docs_src/generate_clients/tutorial001_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9-11  14-15  18  19  23"
{!> ../../../docs_src/generate_clients/tutorial001.py!}
```

////

Beachten Sie, dass die *Pfadoperationen* die Modelle definieren, welche diese für die Request- und Response-<abbr title="Die eigentlichen Nutzdaten, abzüglich der Metadaten">Payload</abbr> verwenden, indem sie die Modelle `Item` und `ResponseMessage` verwenden.

### API-Dokumentation

Wenn Sie zur API-Dokumentation gehen, werden Sie sehen, dass diese die **Schemas** für die Daten enthält, welche in Requests gesendet und in Responses empfangen werden:

<img src="/img/tutorial/generate-clients/image01.png">

Sie können diese Schemas sehen, da sie mit den Modellen in der Anwendung deklariert wurden.

Diese Informationen sind im **OpenAPI-Schema** der Anwendung verfügbar und werden dann in der API-Dokumentation angezeigt (von Swagger UI).

Und dieselben Informationen aus den Modellen, die in OpenAPI enthalten sind, können zum **Generieren des Client-Codes** verwendet werden.

### Einen TypeScript-Client generieren

Nachdem wir nun die Anwendung mit den Modellen haben, können wir den Client-Code für das Frontend generieren.

#### `openapi-ts` installieren

Sie können `openapi-ts` in Ihrem Frontend-Code installieren mit:

<div class="termy">

```console
$ npm install @hey-api/openapi-ts --save-dev

---> 100%
```

</div>

#### Client-Code generieren

Um den Client-Code zu generieren, können Sie das Kommandozeilentool `openapi-ts` verwenden, das soeben installiert wurde.

Da es im lokalen Projekt installiert ist, könnten Sie diesen Befehl wahrscheinlich nicht direkt aufrufen, sondern würden ihn in Ihre Datei `package.json` einfügen.

Diese könnte so aussehen:

```JSON  hl_lines="7"
{
  "name": "frontend-app",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "generate-client": "openapi-ts --input http://localhost:8000/openapi.json --output ./src/client --client axios"
  },
  "author": "",
  "license": "",
  "devDependencies": {
    "@hey-api/openapi-ts": "^0.27.38",
    "typescript": "^4.6.2"
  }
}
```

Nachdem Sie das NPM-Skript `generate-client` dort stehen haben, können Sie es ausführen mit:

<div class="termy">

```console
$ npm run generate-client

frontend-app@1.0.0 generate-client /home/user/code/frontend-app
> openapi-ts --input http://localhost:8000/openapi.json --output ./src/client --client axios
```

</div>

Dieser Befehl generiert Code in `./src/client` und verwendet intern `axios` (die Frontend-HTTP-Bibliothek).

### Den Client-Code ausprobieren

Jetzt können Sie den Client-Code importieren und verwenden. Er könnte wie folgt aussehen, beachten Sie, dass Sie automatische Codevervollständigung für die Methoden erhalten:

<img src="/img/tutorial/generate-clients/image02.png">

Sie erhalten außerdem automatische Vervollständigung für die zu sendende Payload:

<img src="/img/tutorial/generate-clients/image03.png">

/// tip | "Tipp"

Beachten Sie die automatische Vervollständigung für `name` und `price`, welche in der FastAPI-Anwendung im `Item`-Modell definiert wurden.

///

Sie erhalten Inline-Fehlerberichte für die von Ihnen gesendeten Daten:

<img src="/img/tutorial/generate-clients/image04.png">

Das Response-Objekt hat auch automatische Vervollständigung:

<img src="/img/tutorial/generate-clients/image05.png">

## FastAPI-Anwendung mit Tags

In vielen Fällen wird Ihre FastAPI-Anwendung größer sein und Sie werden wahrscheinlich Tags verwenden, um verschiedene Gruppen von *Pfadoperationen* zu separieren.

Beispielsweise könnten Sie einen Abschnitt für **Items (Artikel)** und einen weiteren Abschnitt für **Users (Benutzer)** haben, und diese könnten durch Tags getrennt sein:

//// tab | Python 3.9+

```Python hl_lines="21  26  34"
{!> ../../../docs_src/generate_clients/tutorial002_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="23  28  36"
{!> ../../../docs_src/generate_clients/tutorial002.py!}
```

////

### Einen TypeScript-Client mit Tags generieren

Wenn Sie unter Verwendung von Tags einen Client für eine FastAPI-Anwendung generieren, wird normalerweise auch der Client-Code anhand der Tags getrennt.

Auf diese Weise können Sie die Dinge für den Client-Code richtig ordnen und gruppieren:

<img src="/img/tutorial/generate-clients/image06.png">

In diesem Fall haben Sie:

* `ItemsService`
* `UsersService`

### Client-Methodennamen

Im Moment sehen die generierten Methodennamen wie `createItemItemsPost` nicht sehr sauber aus:

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

... das liegt daran, dass der Client-Generator für jede *Pfadoperation* die OpenAPI-interne **Operation-ID** verwendet.

OpenAPI erfordert, dass jede Operation-ID innerhalb aller *Pfadoperationen* eindeutig ist. Daher verwendet FastAPI den **Funktionsnamen**, den **Pfad** und die **HTTP-Methode/-Operation**, um diese Operation-ID zu generieren. Denn so kann sichergestellt werden, dass die Operation-IDs eindeutig sind.

Aber ich zeige Ihnen als nächstes, wie Sie das verbessern können. 🤓

## Benutzerdefinierte Operation-IDs und bessere Methodennamen

Sie können die Art und Weise, wie diese Operation-IDs **generiert** werden, **ändern**, um sie einfacher zu machen und **einfachere Methodennamen** in den Clients zu haben.

In diesem Fall müssen Sie auf andere Weise sicherstellen, dass jede Operation-ID **eindeutig** ist.

Sie könnten beispielsweise sicherstellen, dass jede *Pfadoperation* einen Tag hat, und dann die Operation-ID basierend auf dem **Tag** und dem **Namen** der *Pfadoperation* (dem Funktionsnamen) generieren.

### Funktion zum Generieren einer eindeutigen ID erstellen

FastAPI verwendet eine **eindeutige ID** für jede *Pfadoperation*, diese wird für die **Operation-ID** und auch für die Namen aller benötigten benutzerdefinierten Modelle für Requests oder Responses verwendet.

Sie können diese Funktion anpassen. Sie nimmt eine `APIRoute` und gibt einen String zurück.

Hier verwendet sie beispielsweise den ersten Tag (Sie werden wahrscheinlich nur einen Tag haben) und den Namen der *Pfadoperation* (den Funktionsnamen).

Anschließend können Sie diese benutzerdefinierte Funktion als Parameter `generate_unique_id_function` an **FastAPI** übergeben:

//// tab | Python 3.9+

```Python hl_lines="6-7  10"
{!> ../../../docs_src/generate_clients/tutorial003_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8-9  12"
{!> ../../../docs_src/generate_clients/tutorial003.py!}
```

////

### Einen TypeScript-Client mit benutzerdefinierten Operation-IDs generieren

Wenn Sie nun den Client erneut generieren, werden Sie feststellen, dass er über die verbesserten Methodennamen verfügt:

<img src="/img/tutorial/generate-clients/image07.png">

Wie Sie sehen, haben die Methodennamen jetzt den Tag und dann den Funktionsnamen, aber keine Informationen aus dem URL-Pfad und der HTTP-Operation.

### Vorab-Modifikation der OpenAPI-Spezifikation für den Client-Generator

Der generierte Code enthält immer noch etwas **verdoppelte Information**.

Wir wissen bereits, dass diese Methode mit den **Items** zusammenhängt, da sich dieses Wort in `ItemsService` befindet (vom Tag übernommen), aber wir haben auch immer noch den Tagnamen im Methodennamen vorangestellt. 😕

Wir werden das wahrscheinlich weiterhin für OpenAPI im Allgemeinen beibehalten wollen, da dadurch sichergestellt wird, dass die Operation-IDs **eindeutig** sind.

Aber für den generierten Client könnten wir die OpenAPI-Operation-IDs direkt vor der Generierung der Clients **modifizieren**, um diese Methodennamen schöner und **sauberer** zu machen.

Wir könnten das OpenAPI-JSON in eine Datei `openapi.json` herunterladen und dann mit einem Skript wie dem folgenden **den vorangestellten Tag entfernen**:

//// tab | Python

```Python
{!> ../../../docs_src/generate_clients/tutorial004.py!}
```

////

//// tab | Node.js

```Javascript
{!> ../../../docs_src/generate_clients/tutorial004.js!}
```

////

Damit würden die Operation-IDs von Dingen wie `items-get_items` in `get_items` umbenannt, sodass der Client-Generator einfachere Methodennamen generieren kann.

### Einen TypeScript-Client mit der modifizierten OpenAPI generieren

Da das Endergebnis nun in einer Datei `openapi.json` vorliegt, würden Sie die `package.json` ändern, um diese lokale Datei zu verwenden, zum Beispiel:

```JSON  hl_lines="7"
{
  "name": "frontend-app",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "generate-client": "openapi-ts --input ./openapi.json --output ./src/client --client axios"
  },
  "author": "",
  "license": "",
  "devDependencies": {
    "@hey-api/openapi-ts": "^0.27.38",
    "typescript": "^4.6.2"
  }
}
```

Nach der Generierung des neuen Clients hätten Sie nun **saubere Methodennamen** mit allen **Autovervollständigungen**, **Inline-Fehlerberichten**, usw.:

<img src="/img/tutorial/generate-clients/image08.png">

## Vorteile

Wenn Sie die automatisch generierten Clients verwenden, erhalten Sie **automatische Codevervollständigung** für:

* Methoden.
* Request-Payloads im Body, Query-Parameter, usw.
* Response-Payloads.

Außerdem erhalten Sie für alles **Inline-Fehlerberichte**.

Und wann immer Sie den Backend-Code aktualisieren und das Frontend **neu generieren**, stehen alle neuen *Pfadoperationen* als Methoden zur Verfügung, die alten werden entfernt und alle anderen Änderungen werden im generierten Code reflektiert. 🤓

Das bedeutet auch, dass, wenn sich etwas ändert, dies automatisch im Client-Code **reflektiert** wird. Und wenn Sie den Client **erstellen**, kommt es zu einer Fehlermeldung, wenn die verwendeten Daten **nicht übereinstimmen**.

Sie würden also sehr früh im Entwicklungszyklus **viele Fehler erkennen**, anstatt darauf warten zu müssen, dass die Fehler Ihren Endbenutzern in der Produktion angezeigt werden, und dann zu versuchen, zu debuggen, wo das Problem liegt. ✨
