# Daten streamen { #stream-data }

Wenn Sie Daten streamen möchten, die als JSON strukturiert werden können, sollten Sie [JSON Lines streamen](../tutorial/stream-json-lines.md).

Wenn Sie jedoch **reine Binärdaten** oder Strings streamen möchten, so können Sie es machen.

/// info | Info

Hinzugefügt in FastAPI 0.134.0.

///

## Anwendungsfälle { #use-cases }

Sie könnten dies verwenden, wenn Sie reine Strings streamen möchten, z. B. direkt aus der Ausgabe eines **AI-LLM**-Dienstes.

Sie könnten es auch nutzen, um **große Binärdateien** zu streamen, wobei Sie jeden Datenchunk beim Lesen streamen, ohne alles auf einmal in den Speicher laden zu müssen.

Sie könnten auf diese Weise auch **Video** oder **Audio** streamen, es könnte sogar beim Verarbeiten erzeugt und gesendet werden.

## Eine `StreamingResponse` mit `yield` { #a-streamingresponse-with-yield }

Wenn Sie in Ihrer Pfadoperation-Funktion ein `response_class=StreamingResponse` deklarieren, können Sie `yield` verwenden, um nacheinander jeden Datenchunk zu senden.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[1:23] hl[20,23] *}

FastAPI übergibt jeden Datenchunk unverändert an die `StreamingResponse`, es wird nicht versucht, ihn in JSON oder etwas Ähnliches zu konvertieren.

### Nicht-async-Pfadoperation-Funktionen { #non-async-path-operation-functions }

Sie können auch reguläre `def`-Funktionen (ohne `async`) verwenden und `yield` auf die gleiche Weise einsetzen.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[26:29] hl[27] *}

### Keine Annotation { #no-annotation }

Sie müssen den Rückgabetyp für das Streamen von Binärdaten nicht wirklich annotieren.

Da FastAPI die Daten nicht mit Pydantic in JSON umzuwandeln oder sie anderweitig zu serialisieren versucht, ist die Typannotation hier nur für Ihren Editor und Tools relevant, sie wird von FastAPI nicht verwendet.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[32:35] hl[33] *}

Das bedeutet auch, dass Sie mit `StreamingResponse` die **Freiheit** und **Verantwortung** haben, die Datenbytes genau so zu erzeugen und zu encodieren, wie sie gesendet werden sollen, unabhängig von den Typannotationen. 🤓

### Bytes streamen { #stream-bytes }

Einer der Hauptanwendungsfälle wäre, `bytes` statt Strings zu streamen, das können Sie selbstverständlich tun.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[44:47] hl[47] *}

## Eine benutzerdefinierte `PNGStreamingResponse` { #a-custom-pngstreamingresponse }

In den obigen Beispielen wurden die Datenbytes gestreamt, aber die Response hatte keinen `Content-Type`-Header, sodass der Client nicht wusste, welchen Datentyp er erhielt.

Sie können eine benutzerdefinierte Unterklasse von `StreamingResponse` erstellen, die den `Content-Type`-Header auf den Typ der gestreamten Daten setzt.

Zum Beispiel können Sie eine `PNGStreamingResponse` erstellen, die den `Content-Type`-Header mit dem Attribut `media_type` auf `image/png` setzt:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[6,19:20] hl[20] *}

Dann können Sie diese neue Klasse mit `response_class=PNGStreamingResponse` in Ihrer Pfadoperation-Funktion verwenden:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[23:27] hl[23] *}

### Eine Datei simulieren { #simulate-a-file }

In diesem Beispiel simulieren wir eine Datei mit `io.BytesIO`, einem dateiähnlichen Objekt, das nur im Speicher lebt, uns aber dieselbe Schnittstelle nutzen lässt.

Wir können z. B. darüber iterieren, um seinen Inhalt zu konsumieren, so wie bei einer Datei.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[1:27] hl[3,12:13,25] *}

/// note | Technische Details

Die anderen beiden Variablen, `image_base64` und `binary_image`, sind ein in Base64 encodiertes Bild, dann in Bytes konvertiert, um es anschließend an `io.BytesIO` zu übergeben.

Nur damit es in derselben Datei leben kann, für dieses Beispiel, und Sie es unverändert kopieren und ausführen können. 🥚

///

Mit einem `with`-Block stellen wir sicher, dass das dateiähnliche Objekt geschlossen wird, nachdem die Generatorfunktion (die Funktion mit `yield`) fertig ist. Also nachdem die Response gesendet wurde.

In diesem speziellen Beispiel wäre das nicht so wichtig, weil es sich um eine unechte In-Memory-Datei (mit `io.BytesIO`) handelt, aber bei einer echten Datei wäre es wichtig sicherzustellen, dass die Datei nach der Arbeit damit geschlossen wird.

### Dateien und Async { #files-and-async }

In den meisten Fällen sind dateiähnliche Objekte standardmäßig nicht mit async und await kompatibel.

Beispielsweise haben sie kein `await file.read()` oder `async for chunk in file`.

Und in vielen Fällen wäre das Lesen eine blockierende Operation (die die Event-Loop blockieren könnte), weil von der Festplatte oder aus dem Netzwerk gelesen wird.

/// info | Info

Das obige Beispiel ist tatsächlich eine Ausnahme, weil sich das `io.BytesIO`-Objekt bereits im Speicher befindet, daher blockiert sein Lesen nichts.

Aber in vielen Fällen würde das Lesen einer Datei oder eines dateiähnlichen Objekts blockieren.

///

Um die Event-Loop nicht zu blockieren, können Sie die Pfadoperation-Funktion einfach mit normalem `def` statt `async def` deklarieren, dadurch führt FastAPI sie in einem Threadpool-Worker aus, um die Haupt-Event-Loop nicht zu blockieren.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[30:34] hl[31] *}

/// tip | Tipp

Wenn Sie blockierenden Code aus einer async-Funktion heraus aufrufen müssen, oder eine async-Funktion aus einer blockierenden Funktion, könnten Sie [Asyncer](https://asyncer.tiangolo.com), eine Schwesterbibliothek zu FastAPI, verwenden.

///

### `yield from` { #yield-from }

Wenn Sie über etwas iterieren, z. B. ein dateiähnliches Objekt, und dann für jedes Element `yield` verwenden, könnten Sie auch `yield from` verwenden, um jedes Element direkt weiterzugeben und die `for`-Schleife zu sparen.

Das ist nichts Spezifisches an FastAPI, das ist einfach Python, aber ein netter Trick. 😎

{* ../../docs_src/stream_data/tutorial002_py310.py ln[37:40] hl[40] *}
