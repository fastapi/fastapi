# Benutzerdefinierte Response – HTML, Stream, Datei, andere { #custom-response-html-stream-file-others }

Standardmäßig gibt **FastAPI** JSON-Responses zurück.

Sie können dies überschreiben, indem Sie direkt eine `Response` zurückgeben, wie in [Eine Response direkt zurückgeben](response-directly.md) gezeigt.

Wenn Sie jedoch direkt eine `Response` (oder eine Unterklasse wie `JSONResponse`) zurückgeben, werden die Daten nicht automatisch konvertiert (selbst wenn Sie ein `response_model` deklarieren), und die Dokumentation wird nicht automatisch generiert (zum Beispiel einschließlich des spezifischen „Medientyps“ im HTTP-Header `Content-Type` als Teil der generierten OpenAPI).

Sie können jedoch auch die `Response`, die Sie verwenden möchten (z. B. jede `Response`-Unterklasse), im *Pfadoperation-Dekorator* mit dem `response_class`-Parameter deklarieren.

Der Inhalt, den Sie von Ihrer *Pfadoperation-Funktion* zurückgeben, wird in diese `Response` eingefügt.

/// note | Hinweis

Wenn Sie eine Response-Klasse ohne Medientyp verwenden, erwartet FastAPI, dass Ihre Response keinen Inhalt hat, und dokumentiert daher das Format der Response nicht in deren generierter OpenAPI-Dokumentation.

///

## JSON-Responses { #json-responses }

Standardmäßig gibt FastAPI JSON-Responses zurück.

Wenn Sie ein [Responsemodell](../tutorial/response-model.md) deklarieren, verwendet FastAPI Pydantic, um die Daten zu JSON zu serialisieren.

Wenn Sie kein Responsemodell deklarieren, verwendet FastAPI den `jsonable_encoder`, wie in [JSON-kompatibler Encoder](../tutorial/encoder.md) erklärt, und packt das Ergebnis in eine `JSONResponse`.

Wenn Sie eine `response_class` mit einem JSON-Medientyp (`application/json`) deklarieren, wie es bei `JSONResponse` der Fall ist, werden die von Ihnen zurückgegebenen Daten automatisch mit jedem Pydantic-`response_model` (das Sie im *Pfadoperation-Dekorator* deklariert haben) konvertiert (und gefiltert). Aber die Daten werden nicht mit Pydantic zu JSON-Bytes serialisiert, stattdessen werden sie mit dem `jsonable_encoder` konvertiert und anschließend an die `JSONResponse`-Klasse übergeben, die sie dann mit der Standard-JSON-Bibliothek in Python in Bytes serialisiert.

### JSON-Leistung { #json-performance }

Kurz gesagt: Wenn Sie die maximale Leistung möchten, verwenden Sie ein [Responsemodell](../tutorial/response-model.md) und deklarieren Sie keine `response_class` im *Pfadoperation-Dekorator*.

{* ../../docs_src/response_model/tutorial001_01_py310.py ln[15:17] hl[16] *}

## HTML-Response { #html-response }

Um eine Response mit HTML direkt von **FastAPI** zurückzugeben, verwenden Sie `HTMLResponse`.

* Importieren Sie `HTMLResponse`.
* Übergeben Sie `HTMLResponse` als den Parameter `response_class` Ihres *Pfadoperation-Dekorators*.

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// info | Info

Der Parameter `response_class` wird auch verwendet, um den „Medientyp“ der Response zu definieren.

In diesem Fall wird der HTTP-Header `Content-Type` auf `text/html` gesetzt.

Und er wird als solcher in OpenAPI dokumentiert.

///

### Eine `Response` zurückgeben { #return-a-response }

Wie in [Eine Response direkt zurückgeben](response-directly.md) gezeigt, können Sie die Response auch direkt in Ihrer *Pfadoperation* überschreiben, indem Sie diese zurückgeben.

Das gleiche Beispiel von oben, das eine `HTMLResponse` zurückgibt, könnte so aussehen:

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning | Achtung

Eine `Response`, die direkt von Ihrer *Pfadoperation-Funktion* zurückgegeben wird, wird in OpenAPI nicht dokumentiert (zum Beispiel wird der `Content-Type` nicht dokumentiert) und ist in der automatischen interaktiven Dokumentation nicht sichtbar.

///

/// info | Info

Natürlich stammen der eigentliche `Content-Type`-Header, der Statuscode, usw., aus dem `Response`-Objekt, das Sie zurückgegeben haben.

///

### In OpenAPI dokumentieren und `Response` überschreiben { #document-in-openapi-and-override-response }

Wenn Sie die Response innerhalb der Funktion überschreiben und gleichzeitig den „Medientyp“ in OpenAPI dokumentieren möchten, können Sie den `response_class`-Parameter verwenden UND ein `Response`-Objekt zurückgeben.

Die `response_class` wird dann nur zur Dokumentation der OpenAPI-*Pfadoperation* verwendet, Ihre `Response` wird jedoch unverändert verwendet.

#### Eine `HTMLResponse` direkt zurückgeben { #return-an-htmlresponse-directly }

Es könnte zum Beispiel so etwas sein:

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

In diesem Beispiel generiert die Funktion `generate_html_response()` bereits eine `Response` und gibt sie zurück, anstatt das HTML in einem `str` zurückzugeben.

Indem Sie das Ergebnis des Aufrufs von `generate_html_response()` zurückgeben, geben Sie bereits eine `Response` zurück, die das Standardverhalten von **FastAPI** überschreibt.

Aber da Sie die `HTMLResponse` auch in der `response_class` übergeben haben, weiß **FastAPI**, dass sie in OpenAPI und der interaktiven Dokumentation als HTML mit `text/html` zu dokumentieren ist:

<img src="/img/tutorial/custom-response/image01.png">

## Verfügbare Responses { #available-responses }

Hier sind einige der verfügbaren Responses.

Bedenken Sie, dass Sie `Response` verwenden können, um alles andere zurückzugeben, oder sogar eine benutzerdefinierte Unterklasse zu erstellen.

/// note | Technische Details

Sie können auch `from starlette.responses import HTMLResponse` verwenden.

**FastAPI** bietet dieselben `starlette.responses` auch via `fastapi.responses` an, als Annehmlichkeit für Sie, den Entwickler. Die meisten verfügbaren Responses kommen aber direkt von Starlette.

///

### `Response` { #response }

Die Hauptklasse `Response`, alle anderen Responses erben von ihr.

Sie können sie direkt zurückgeben.

Sie akzeptiert die folgenden Parameter:

* `content` – Ein `str` oder `bytes`.
* `status_code` – Ein `int`-HTTP-Statuscode.
* `headers` – Ein `dict` von Strings.
* `media_type` – Ein `str`, der den Medientyp angibt. Z. B. `"text/html"`.

FastAPI (eigentlich Starlette) fügt automatisch einen Content-Length-Header ein. Außerdem wird es einen Content-Type-Header einfügen, der auf dem `media_type` basiert, und für Texttypen einen Zeichensatz (charset) anfügen.

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

Nimmt Text oder Bytes entgegen und gibt eine HTML-Response zurück, wie Sie oben gelesen haben.

### `PlainTextResponse` { #plaintextresponse }

Nimmt Text oder Bytes entgegen und gibt eine Plain-Text-Response zurück.

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

Nimmt einige Daten entgegen und gibt eine `application/json`-codierte Response zurück.

Dies ist die Standard-Response, die in **FastAPI** verwendet wird, wie Sie oben gelesen haben.

/// note | Technische Details

Wenn Sie jedoch ein Responsemodell oder einen Rückgabetyp deklarieren, wird dieser direkt verwendet, um die Daten zu JSON zu serialisieren, und eine Response mit dem richtigen Medientyp für JSON wird direkt zurückgegeben, ohne die `JSONResponse`-Klasse zu verwenden.

Dies ist der ideale Weg, um die beste Leistung zu erzielen.

///

### `RedirectResponse` { #redirectresponse }

Gibt eine HTTP-Weiterleitung (HTTP-Redirect) zurück. Verwendet standardmäßig den Statuscode 307 – Temporäre Weiterleitung (Temporary Redirect).

Sie können eine `RedirectResponse` direkt zurückgeben:

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

Oder Sie können sie im Parameter `response_class` verwenden:

{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

Wenn Sie das tun, können Sie die URL direkt von Ihrer *Pfadoperation*-Funktion zurückgeben.

In diesem Fall ist der verwendete `status_code` der Standardcode für die `RedirectResponse`, also `307`.

---

Sie können den Parameter `status_code` auch in Kombination mit dem Parameter `response_class` verwenden:

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

Nimmt einen asynchronen Generator oder einen normalen Generator/Iterator (eine Funktion mit `yield`) und streamt den Responsebody.

{* ../../docs_src/custom_response/tutorial007_py310.py hl[3,16] *}

/// note | Technische Details

Ein `async`-Task kann nur abgebrochen werden, wenn er ein `await` erreicht. Wenn es kein `await` gibt, kann der Generator (Funktion mit `yield`) nicht ordnungsgemäß abgebrochen werden und könnte weiterlaufen, selbst nachdem der Abbruch angefordert wurde.

Da dieses kleine Beispiel keine `await`-Anweisungen benötigt, fügen wir ein `await anyio.sleep(0)` hinzu, um dem Event Loop die Chance zu geben, den Abbruch zu verarbeiten.

Dies wäre bei großen oder unendlichen Streams noch wichtiger.

///

/// tip | Tipp

Anstatt eine `StreamingResponse` direkt zurückzugeben, sollten Sie wahrscheinlich dem Stil in [Daten streamen](./stream-data.md) folgen. Das ist wesentlich bequemer und behandelt den Abbruch im Hintergrund für Sie.

Wenn Sie JSON Lines streamen, folgen Sie dem Tutorial [JSON Lines streamen](../tutorial/stream-json-lines.md).

///

### `FileResponse` { #fileresponse }

Streamt eine Datei asynchron als Response.

Nimmt zur Instanziierung einen anderen Satz von Argumenten entgegen als die anderen Response-Typen:

* `path` – Der Dateipfad zur Datei, die gestreamt werden soll.
* `headers` – Alle benutzerdefinierten Header, die inkludiert werden sollen, als Dictionary.
* `media_type` – Ein String, der den Medientyp angibt. Wenn nicht gesetzt, wird der Dateiname oder Pfad verwendet, um auf einen Medientyp zu schließen.
* `filename` – Wenn gesetzt, wird das in der `Content-Disposition` der Response eingefügt.

Datei-Responses enthalten die entsprechenden `Content-Length`-, `Last-Modified`- und `ETag`-Header.

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

Sie können auch den Parameter `response_class` verwenden:

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

In diesem Fall können Sie den Dateipfad direkt von Ihrer *Pfadoperation*-Funktion zurückgeben.

## Benutzerdefinierte Response-Klasse { #custom-response-class }

Sie können Ihre eigene benutzerdefinierte Response-Klasse erstellen, die von `Response` erbt und diese verwendet.

Nehmen wir zum Beispiel an, dass Sie [`orjson`](https://github.com/ijl/orjson) mit einigen Einstellungen verwenden möchten.

Sie möchten etwa, dass Ihre Response eingerücktes und formatiertes JSON zurückgibt. Dafür möchten Sie die orjson-Option `orjson.OPT_INDENT_2` verwenden.

Sie könnten eine `CustomORJSONResponse` erstellen. Das Wichtigste, was Sie tun müssen, ist, eine `Response.render(content)`-Methode zu erstellen, die den Inhalt als `bytes` zurückgibt:

{* ../../docs_src/custom_response/tutorial009c_py310.py hl[9:14,17] *}

Anstatt Folgendes zurückzugeben:

```json
{"message": "Hello World"}
```

... wird diese Response Folgendes zurückgeben:

```json
{
  "message": "Hello World"
}
```

Natürlich werden Sie wahrscheinlich viel bessere Möglichkeiten finden, Vorteil daraus zu ziehen, als JSON zu formatieren. 😉

### `orjson` oder Responsemodell { #orjson-or-response-model }

Wenn es Ihnen um Leistung geht, sind Sie wahrscheinlich mit einem [Responsemodell](../tutorial/response-model.md) besser beraten als mit einer `orjson`-Response.

Mit einem Responsemodell verwendet FastAPI Pydantic, um die Daten ohne Zwischenschritte zu JSON zu serialisieren, also ohne sie z. B. erst mit `jsonable_encoder` zu konvertieren, was sonst der Fall wäre.

Und unter der Haube verwendet Pydantic dieselben Rust-Mechanismen wie `orjson`, um nach JSON zu serialisieren. Sie erhalten mit einem Responsemodell also ohnehin die beste Leistung.

## Standard-Response-Klasse { #default-response-class }

Beim Erstellen einer **FastAPI**-Klasseninstanz oder eines `APIRouter`s können Sie angeben, welche Response-Klasse standardmäßig verwendet werden soll.

Der Parameter, der das definiert, ist `default_response_class`.

Im folgenden Beispiel verwendet **FastAPI** standardmäßig `HTMLResponse` in allen *Pfadoperationen*, anstelle von JSON.

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | Tipp

Sie können dennoch weiterhin `response_class` in *Pfadoperationen* überschreiben, wie bisher.

///

## Zusätzliche Dokumentation { #additional-documentation }

Sie können auch den Medientyp und viele andere Details in OpenAPI mit `responses` deklarieren: [Zusätzliche Responses in OpenAPI](additional-responses.md).
