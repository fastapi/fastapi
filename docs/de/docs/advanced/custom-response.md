# Benutzerdefinierte Response – HTML, Stream, Datei, andere { #custom-response-html-stream-file-others }

Standardmäßig gibt **FastAPI** die <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Responses</abbr> mittels `JSONResponse` zurück.

Sie können dies überschreiben, indem Sie direkt eine `Response` zurückgeben, wie in [Eine Response direkt zurückgeben](response-directly.md){.internal-link target=_blank} gezeigt.

Wenn Sie jedoch direkt eine `Response` (oder eine Unterklasse wie `JSONResponse`) zurückgeben, werden die Daten nicht automatisch konvertiert (selbst wenn Sie ein `response_model` deklariert haben), und die Dokumentation wird nicht automatisch generiert (zum Beispiel wird der spezifische „Medientyp“, der im HTTP-Header `Content-Type` angegeben ist, nicht Teil der generierten OpenAPI).

Sie können jedoch auch die `Response`, die Sie verwenden möchten (z. B. jede `Response`-Unterklasse), im *Pfadoperation-Dekorator* mit dem `response_class`-Parameter deklarieren.

Der Inhalt, den Sie von Ihrer *Pfadoperation-Funktion* zurückgeben, wird in diese `Response` eingefügt.

Und wenn diese `Response` einen JSON-Medientyp (`application/json`) hat, wie es bei `JSONResponse` und `UJSONResponse` der Fall ist, werden die von Ihnen zurückgegebenen Daten automatisch mit jedem Pydantic `response_model` konvertiert (und gefiltert), das Sie im *Pfadoperation-Dekorator* deklariert haben.

/// note | Hinweis

Wenn Sie eine Response-Klasse ohne Medientyp verwenden, erwartet FastAPI, dass Ihre Response keinen Inhalt hat, und dokumentiert daher das Format der Response nicht in deren generierter OpenAPI-Dokumentation.

///

## `ORJSONResponse` verwenden { #use-orjsonresponse }

Um beispielsweise noch etwas Leistung herauszuholen, können Sie <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> installieren und die Response als `ORJSONResponse` setzen.

Importieren Sie die `Response`-Klasse (Unterklasse), die Sie verwenden möchten, und deklarieren Sie sie im *Pfadoperation-Dekorator*.

Bei umfangreichen Responses ist die direkte Rückgabe einer `Response` wesentlich schneller als ein <abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">Dictionary</abbr> zurückzugeben.

Das liegt daran, dass FastAPI standardmäßig jedes enthaltene Element überprüft und sicherstellt, dass es als JSON serialisierbar ist, und zwar unter Verwendung desselben [JSON-kompatiblen Encoders](../tutorial/encoder.md){.internal-link target=_blank}, der im Tutorial erläutert wurde. Dadurch können Sie **beliebige Objekte** zurückgeben, zum Beispiel Datenbankmodelle.

Wenn Sie jedoch sicher sind, dass der von Ihnen zurückgegebene Inhalt **mit JSON serialisierbar** ist, können Sie ihn direkt an die Response-Klasse übergeben und die zusätzliche Arbeit vermeiden, die FastAPI hätte, indem es Ihren zurückgegebenen Inhalt durch den `jsonable_encoder` leitet, bevor es ihn an die Response-Klasse übergibt.

{* ../../docs_src/custom_response/tutorial001b.py hl[2,7] *}

/// info | Info

Der Parameter `response_class` wird auch verwendet, um den „Medientyp“ der Response zu definieren.

In diesem Fall wird der HTTP-Header `Content-Type` auf `application/json` gesetzt.

Und er wird als solcher in OpenAPI dokumentiert.

///

/// tip | Tipp

Die `ORJSONResponse` ist nur in FastAPI verfügbar, nicht in Starlette.

///

## HTML-Response { #html-response }

Um eine Response mit HTML direkt von **FastAPI** zurückzugeben, verwenden Sie `HTMLResponse`.

* Importieren Sie `HTMLResponse`.
* Übergeben Sie `HTMLResponse` als den Parameter `response_class` Ihres *Pfadoperation-Dekorators*.

{* ../../docs_src/custom_response/tutorial002.py hl[2,7] *}

/// info | Info

Der Parameter `response_class` wird auch verwendet, um den „Medientyp“ der Response zu definieren.

In diesem Fall wird der HTTP-Header `Content-Type` auf `text/html` gesetzt.

Und er wird als solcher in OpenAPI dokumentiert.

///

### Eine `Response` zurückgeben { #return-a-response }

Wie in [Eine Response direkt zurückgeben](response-directly.md){.internal-link target=_blank} gezeigt, können Sie die Response auch direkt in Ihrer *Pfadoperation* überschreiben, indem Sie diese zurückgeben.

Das gleiche Beispiel von oben, das eine `HTMLResponse` zurückgibt, könnte so aussehen:

{* ../../docs_src/custom_response/tutorial003.py hl[2,7,19] *}

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

{* ../../docs_src/custom_response/tutorial004.py hl[7,21,23] *}

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

FastAPI (eigentlich Starlette) fügt automatisch einen Content-Length-Header ein. Außerdem wird es einen Content-Type-Header einfügen, der auf dem media_type basiert, und für Texttypen einen Zeichensatz (charset) anfügen.

{* ../../docs_src/response_directly/tutorial002.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

Nimmt Text oder Bytes entgegen und gibt eine HTML-Response zurück, wie Sie oben gelesen haben.

### `PlainTextResponse` { #plaintextresponse }

Nimmt Text oder Bytes entgegen und gibt eine Plain-Text-Response zurück.

{* ../../docs_src/custom_response/tutorial005.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

Nimmt einige Daten entgegen und gibt eine `application/json`-codierte Response zurück.

Dies ist die Standard-Response, die in **FastAPI** verwendet wird, wie Sie oben gelesen haben.

### `ORJSONResponse` { #orjsonresponse }

Eine schnelle alternative JSON-Response mit <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, wie Sie oben gelesen haben.

/// info | Info

Dazu muss `orjson` installiert werden, z. B. mit `pip install orjson`.

///

### `UJSONResponse` { #ujsonresponse }

Eine alternative JSON-Response mit <a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a>.

/// info | Info

Dazu muss `ujson` installiert werden, z. B. mit `pip install ujson`.

///

/// warning | Achtung

`ujson` ist bei der Behandlung einiger Sonderfälle weniger sorgfältig als Pythons eingebaute Implementierung.

///

{* ../../docs_src/custom_response/tutorial001.py hl[2,7] *}

/// tip | Tipp

Möglicherweise ist `ORJSONResponse` eine schnellere Alternative.

///

### `RedirectResponse` { #redirectresponse }

Gibt eine HTTP-Weiterleitung (HTTP-Redirect) zurück. Verwendet standardmäßig den Statuscode 307 – Temporäre Weiterleitung (Temporary Redirect).

Sie können eine `RedirectResponse` direkt zurückgeben:

{* ../../docs_src/custom_response/tutorial006.py hl[2,9] *}

---

Oder Sie können sie im Parameter `response_class` verwenden:

{* ../../docs_src/custom_response/tutorial006b.py hl[2,7,9] *}

Wenn Sie das tun, können Sie die URL direkt von Ihrer *Pfadoperation*-Funktion zurückgeben.

In diesem Fall ist der verwendete `status_code` der Standardcode für die `RedirectResponse`, also `307`.

---

Sie können den Parameter `status_code` auch in Kombination mit dem Parameter `response_class` verwenden:

{* ../../docs_src/custom_response/tutorial006c.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

Nimmt einen asynchronen Generator oder einen normalen Generator/Iterator und streamt den Responsebody.

{* ../../docs_src/custom_response/tutorial007.py hl[2,14] *}

#### Verwendung von `StreamingResponse` mit dateiartigen Objekten { #using-streamingresponse-with-file-like-objects }

Wenn Sie ein dateiartiges (<a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a>) Objekt haben (z. B. das von `open()` zurückgegebene Objekt), können Sie eine Generatorfunktion erstellen, um über dieses dateiartige Objekt zu iterieren.

Auf diese Weise müssen Sie nicht alles zuerst in den Arbeitsspeicher lesen und können diese Generatorfunktion an `StreamingResponse` übergeben und zurückgeben.

Das umfasst viele Bibliotheken zur Interaktion mit Cloud-Speicher, Videoverarbeitung und anderen.

{* ../../docs_src/custom_response/tutorial008.py hl[2,10:12,14] *}

1. Das ist die Generatorfunktion. Es handelt sich um eine „Generatorfunktion“, da sie `yield`-Anweisungen enthält.
2. Durch die Verwendung eines `with`-Blocks stellen wir sicher, dass das dateiartige Objekt geschlossen wird, nachdem die Generatorfunktion fertig ist. Also, nachdem sie mit dem Senden der Response fertig ist.
3. Dieses `yield from` weist die Funktion an, über das Ding namens `file_like` zu iterieren. Und dann für jeden iterierten Teil, diesen Teil so zurückzugeben, als wenn er aus dieser Generatorfunktion (`iterfile`) stammen würde.

    Es handelt sich also hier um eine Generatorfunktion, die die „generierende“ Arbeit intern auf etwas anderes überträgt.

    Auf diese Weise können wir das Ganze in einen `with`-Block einfügen und so sicherstellen, dass das dateiartige Objekt nach Abschluss geschlossen wird.

/// tip | Tipp

Beachten Sie, dass wir, da wir Standard-`open()` verwenden, welches `async` und `await` nicht unterstützt, hier die Pfadoperation mit normalen `def` deklarieren.

///

### `FileResponse` { #fileresponse }

Streamt eine Datei asynchron als Response.

Nimmt zur Instanziierung einen anderen Satz von Argumenten entgegen als die anderen Response-Typen:

* `path` – Der Dateipfad zur Datei, die gestreamt werden soll.
* `headers` – Alle benutzerdefinierten Header, die inkludiert werden sollen, als Dictionary.
* `media_type` – Ein String, der den Medientyp angibt. Wenn nicht gesetzt, wird der Dateiname oder Pfad verwendet, um auf einen Medientyp zu schließen.
* `filename` – Wenn gesetzt, wird das in der `Content-Disposition` der Response eingefügt.

Datei-Responses enthalten die entsprechenden `Content-Length`-, `Last-Modified`- und `ETag`-Header.

{* ../../docs_src/custom_response/tutorial009.py hl[2,10] *}

Sie können auch den Parameter `response_class` verwenden:

{* ../../docs_src/custom_response/tutorial009b.py hl[2,8,10] *}

In diesem Fall können Sie den Dateipfad direkt von Ihrer *Pfadoperation*-Funktion zurückgeben.

## Benutzerdefinierte Response-Klasse { #custom-response-class }

Sie können Ihre eigene benutzerdefinierte Response-Klasse erstellen, die von `Response` erbt und diese verwendet.

Nehmen wir zum Beispiel an, dass Sie <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> verwenden möchten, aber mit einigen benutzerdefinierten Einstellungen, die in der enthaltenen `ORJSONResponse`-Klasse nicht verwendet werden.

Sie möchten etwa, dass Ihre Response eingerücktes und formatiertes JSON zurückgibt. Dafür möchten Sie die orjson-Option `orjson.OPT_INDENT_2` verwenden.

Sie könnten eine `CustomORJSONResponse` erstellen. Das Wichtigste, was Sie tun müssen, ist, eine `Response.render(content)`-Methode zu erstellen, die den Inhalt als `bytes` zurückgibt:

{* ../../docs_src/custom_response/tutorial009c.py hl[9:14,17] *}

Statt:

```json
{"message": "Hello World"}
```

... wird die Response jetzt Folgendes zurückgeben:

```json
{
  "message": "Hello World"
}
```

Natürlich werden Sie wahrscheinlich viel bessere Möglichkeiten finden, Vorteil daraus zu ziehen, als JSON zu formatieren. 😉

## Standard-Response-Klasse { #default-response-class }

Beim Erstellen einer **FastAPI**-Klasseninstanz oder eines `APIRouter`s können Sie angeben, welche Response-Klasse standardmäßig verwendet werden soll.

Der Parameter, der das definiert, ist `default_response_class`.

Im folgenden Beispiel verwendet **FastAPI** standardmäßig `ORJSONResponse` in allen *Pfadoperationen*, anstelle von `JSONResponse`.

{* ../../docs_src/custom_response/tutorial010.py hl[2,4] *}

/// tip | Tipp

Sie können dennoch weiterhin `response_class` in *Pfadoperationen* überschreiben, wie bisher.

///

## Zusätzliche Dokumentation { #additional-documentation }

Sie können auch den Medientyp und viele andere Details in OpenAPI mit `responses` deklarieren: [Zusätzliche Responses in OpenAPI](additional-responses.md){.internal-link target=_blank}.
