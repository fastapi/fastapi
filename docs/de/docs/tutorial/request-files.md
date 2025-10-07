# Dateien im Request { #request-files }

Sie können Dateien, die vom Client hochgeladen werden, mithilfe von `File` definieren.

/// info | Info

Um hochgeladene Dateien zu empfangen, installieren Sie zuerst <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Stellen Sie sicher, dass Sie eine [virtuelle Umgebung](../virtual-environments.md){.internal-link target=_blank} erstellen, sie aktivieren und dann das Paket installieren, zum Beispiel:

```console
$ pip install python-multipart
```

Das liegt daran, dass hochgeladene Dateien als „Formulardaten“ gesendet werden.

///

## `File` importieren { #import-file }

Importieren Sie `File` und `UploadFile` von `fastapi`:

{* ../../docs_src/request_files/tutorial001_an_py39.py hl[3] *}

## `File`-Parameter definieren { #define-file-parameters }

Erstellen Sie Datei-Parameter, so wie Sie es auch mit `Body` und `Form` machen würden:

{* ../../docs_src/request_files/tutorial001_an_py39.py hl[9] *}

/// info | Info

`File` ist eine Klasse, die direkt von `Form` erbt.

Aber erinnern Sie sich, dass, wenn Sie `Query`, `Path`, `File` und andere von `fastapi` importieren, diese tatsächlich Funktionen sind, welche spezielle Klassen zurückgeben.

///

/// tip | Tipp

Um Dateibodys zu deklarieren, müssen Sie `File` verwenden, da diese Parameter sonst als Query-Parameter oder Body (JSON)-Parameter interpretiert werden würden.

///

Die Dateien werden als „Formulardaten“ hochgeladen.

Wenn Sie den Typ Ihrer *Pfadoperation-Funktion* als `bytes` deklarieren, wird **FastAPI** die Datei für Sie auslesen, und Sie erhalten den Inhalt als `bytes`.

Bedenken Sie, dass das bedeutet, dass sich der gesamte Inhalt der Datei im Arbeitsspeicher befindet. Das wird für kleinere Dateien gut funktionieren.

Aber es gibt viele Fälle, in denen Sie davon profitieren, `UploadFile` zu verwenden.

## Datei-Parameter mit `UploadFile` { #file-parameters-with-uploadfile }

Definieren Sie einen Datei-Parameter mit dem Typ `UploadFile`:

{* ../../docs_src/request_files/tutorial001_an_py39.py hl[14] *}

`UploadFile` zu verwenden, hat mehrere Vorzüge gegenüber `bytes`:

* Sie müssen `File()` nicht als Parameter-Defaultwert verwenden.
* Es wird eine <abbr title="warteschlangenartig">„gespoolte“</abbr> Datei verwendet:
    * Eine Datei, die bis zu einem bestimmten Größen-Limit im Arbeitsspeicher behalten wird, und wenn das Limit überschritten wird, auf der Festplatte gespeichert wird.
* Das bedeutet, es wird für große Dateien wie Bilder, Videos, große Binärdateien, usw. gut funktionieren, ohne den ganzen Arbeitsspeicher aufzubrauchen.
* Sie können Metadaten aus der hochgeladenen Datei auslesen.
* Es hat eine <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">dateiartige</a> `async`hrone Schnittstelle.
* Es stellt ein tatsächliches Python-<a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a>-Objekt bereit, welches Sie direkt anderen Bibliotheken übergeben können, die ein dateiartiges Objekt erwarten.

### `UploadFile` { #uploadfile }

`UploadFile` hat die folgenden Attribute:

* `filename`: Ein `str` mit dem ursprünglichen Namen der hochgeladenen Datei (z. B. `meinbild.jpg`).
* `content_type`: Ein `str` mit dem Inhaltstyp (MIME-Typ / Medientyp) (z. B. `image/jpeg`).
* `file`: Ein <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> (ein <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">dateiartiges</a> Objekt). Das ist das tatsächliche Python-Objekt, das Sie direkt anderen Funktionen oder Bibliotheken übergeben können, welche ein „file-like“-Objekt erwarten.

`UploadFile` hat die folgenden `async`hronen Methoden. Sie alle rufen die entsprechenden Methoden des darunterliegenden Datei-Objekts auf (wobei intern `SpooledTemporaryFile` verwendet wird).

* `write(daten)`: Schreibt `daten` (`str` oder `bytes`) in die Datei.
* `read(anzahl)`: Liest `anzahl` (`int`) bytes/Zeichen aus der Datei.
* `seek(versatz)`: Geht zur Position `versatz` (`int`) in der Datei.
    * Z. B. würde `await myfile.seek(0)` zum Anfang der Datei gehen.
    * Das ist besonders dann nützlich, wenn Sie `await myfile.read()` einmal ausführen und dann diese Inhalte erneut auslesen müssen.
* `close()`: Schließt die Datei.

Da alle diese Methoden `async`hron sind, müssen Sie sie „await“en („erwarten“).

Zum Beispiel können Sie innerhalb einer `async` *Pfadoperation-Funktion* den Inhalt wie folgt auslesen:

```Python
contents = await myfile.read()
```

Wenn Sie sich innerhalb einer normalen `def`-*Pfadoperation-Funktion* befinden, können Sie direkt auf `UploadFile.file` zugreifen, zum Beispiel:

```Python
contents = myfile.file.read()
```

/// note | Technische Details zu `async`

Wenn Sie die `async`-Methoden verwenden, führt **FastAPI** die Datei-Methoden in einem <abbr title="Mehrere unabhängige Kindprozesse">Threadpool</abbr> aus und erwartet sie.

///

/// note | Technische Details zu Starlette

**FastAPI**s `UploadFile` erbt direkt von **Starlette**s `UploadFile`, fügt aber ein paar notwendige Teile hinzu, um es kompatibel mit **Pydantic** und anderen Teilen von FastAPI zu machen.

///

## Was sind „Formulardaten“ { #what-is-form-data }

Der Weg, wie HTML-Formulare (`<form></form>`) die Daten zum Server senden, verwendet normalerweise eine „spezielle“ Kodierung für diese Daten. Diese unterscheidet sich von JSON.

**FastAPI** stellt sicher, dass diese Daten korrekt ausgelesen werden, statt JSON zu erwarten.

/// note | Technische Details

Daten aus Formularen werden, wenn es keine Dateien sind, normalerweise mit dem <abbr title='Media type – Medientyp, Typ des Mediums'>„media type“</abbr> `application/x-www-form-urlencoded` kodiert.

Sollte das Formular aber Dateien enthalten, dann werden diese mit `multipart/form-data` kodiert. Wenn Sie `File` verwenden, wird **FastAPI** wissen, dass es die Dateien vom korrekten Teil des Bodys holen muss.

Wenn Sie mehr über diese Kodierungen und Formularfelder lesen möchten, besuchen Sie die <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network – Mozilla-Entwicklernetzwerk">MDN</abbr>-Webdokumentation für <code>POST</code></a>.

///

/// warning | Achtung

Sie können mehrere `File`- und `Form`-Parameter in einer *Pfadoperation* deklarieren, aber Sie können nicht gleichzeitig auch `Body`-Felder deklarieren, welche Sie als JSON erwarten, da der <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> den Body mittels `multipart/form-data` statt `application/json` kodiert.

Das ist keine Limitation von **FastAPI**, sondern Teil des HTTP-Protokolls.

///

## Optionaler Datei-Upload { #optional-file-upload }

Sie können eine Datei optional machen, indem Sie Standard-Typannotationen verwenden und den Defaultwert auf `None` setzen:

{* ../../docs_src/request_files/tutorial001_02_an_py310.py hl[9,17] *}

## `UploadFile` mit zusätzlichen Metadaten { #uploadfile-with-additional-metadata }

Sie können auch `File()` mit `UploadFile` verwenden, um zum Beispiel zusätzliche Metadaten zu setzen:

{* ../../docs_src/request_files/tutorial001_03_an_py39.py hl[9,15] *}

## Mehrere Datei-Uploads { #multiple-file-uploads }

Es ist auch möglich, mehrere Dateien gleichzeitig hochzuladen.

Diese werden demselben Formularfeld zugeordnet, welches mit den Formulardaten gesendet wird.

Um das zu machen, deklarieren Sie eine Liste von `bytes` oder `UploadFile`s:

{* ../../docs_src/request_files/tutorial002_an_py39.py hl[10,15] *}

Sie erhalten, wie deklariert, eine `list` von `bytes` oder `UploadFile`s.

/// note | Technische Details

Sie können auch `from starlette.responses import HTMLResponse` verwenden.

**FastAPI** bietet dieselben `starlette.responses` auch via `fastapi.responses` an, als Annehmlichkeit für Sie, den Entwickler. Die meisten verfügbaren <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Responses</abbr> kommen aber direkt von Starlette.

///

### Mehrere Datei-Uploads mit zusätzlichen Metadaten { #multiple-file-uploads-with-additional-metadata }

Und so wie zuvor können Sie `File()` verwenden, um zusätzliche Parameter zu setzen, sogar für `UploadFile`:

{* ../../docs_src/request_files/tutorial003_an_py39.py hl[11,18:20] *}

## Zusammenfassung { #recap }

Verwenden Sie `File`, `bytes` und `UploadFile`, um hochladbare Dateien im Request zu deklarieren, die als Formulardaten gesendet werden.
