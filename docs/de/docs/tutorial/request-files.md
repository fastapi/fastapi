# Dateien im Request

Mit `File` können sie vom Client hochzuladende Dateien definieren.

/// info

Um hochgeladene Dateien zu empfangen, installieren Sie zuerst <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>.

Z. B. `pip install python-multipart`.

Das, weil hochgeladene Dateien als „Formulardaten“ gesendet werden.

///

## `File` importieren

Importieren Sie `File` und `UploadFile` von `fastapi`:

//// tab | Python 3.9+

```Python hl_lines="3"
{!> ../../../docs_src/request_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1"
{!> ../../../docs_src/request_files/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="1"
{!> ../../../docs_src/request_files/tutorial001.py!}
```

////

## `File`-Parameter definieren

Erstellen Sie Datei-Parameter, so wie Sie es auch mit `Body` und `Form` machen würden:

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/request_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8"
{!> ../../../docs_src/request_files/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/request_files/tutorial001.py!}
```

////

/// info

`File` ist eine Klasse, die direkt von `Form` erbt.

Aber erinnern Sie sich, dass, wenn Sie `Query`, `Path`,  `File` und andere von `fastapi` importieren, diese tatsächlich Funktionen sind, welche spezielle Klassen zurückgeben

///

/// tip | "Tipp"

Um Dateibodys zu deklarieren, müssen Sie `File` verwenden, da diese Parameter sonst als Query-Parameter oder Body(-JSON)-Parameter interpretiert werden würden.

///

Die Dateien werden als „Formulardaten“ hochgeladen.

Wenn Sie den Typ Ihrer *Pfadoperation-Funktion* als `bytes` deklarieren, wird **FastAPI** die Datei für Sie auslesen, und Sie erhalten den Inhalt als `bytes`.

Bedenken Sie, dass das bedeutet, dass sich der gesamte Inhalt der Datei im Arbeitsspeicher befindet. Das wird für kleinere Dateien gut funktionieren.

Aber es gibt viele Fälle, in denen Sie davon profitieren, `UploadFile` zu verwenden.

## Datei-Parameter mit `UploadFile`

Definieren Sie einen Datei-Parameter mit dem Typ `UploadFile`:

//// tab | Python 3.9+

```Python hl_lines="14"
{!> ../../../docs_src/request_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="13"
{!> ../../../docs_src/request_files/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="12"
{!> ../../../docs_src/request_files/tutorial001.py!}
```

////

`UploadFile` zu verwenden, hat mehrere Vorzüge gegenüber `bytes`:

* Sie müssen `File()` nicht als Parameter-Defaultwert verwenden.
* Es wird eine <abbr title='Aufgespult, Warteschlangenartig'>„Spool“</abbr>-Datei verwendet:
    * Eine Datei, die bis zu einem bestimmten Größen-Limit im Arbeitsspeicher behalten wird, und wenn das Limit überschritten wird, auf der Festplatte gespeichert wird.
* Das bedeutet, es wird für große Dateien wie Bilder, Videos, große Binärdateien, usw. gut funktionieren, ohne den ganzen Arbeitsspeicher aufzubrauchen.
* Sie können Metadaten aus der hochgeladenen Datei auslesen.
* Es hat eine <abbr title="dateiartig"><a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a></abbr> `async`hrone Schnittstelle.
* Es stellt ein tatsächliches Python-<abbr title="Warteschlangenartige, temporäre Datei"><a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a></abbr>-Objekt bereit, welches Sie direkt anderen Bibliotheken übergeben können, die ein dateiartiges Objekt erwarten.

### `UploadFile`

`UploadFile` hat die folgenden Attribute:

* `filename`: Ein `str` mit dem ursprünglichen Namen der hochgeladenen Datei (z. B. `meinbild.jpg`).
* `content_type`: Ein `str` mit dem Inhaltstyp (MIME-Typ / Medientyp) (z. B. `image/jpeg`).
* `file`: Ein <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> (ein <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> Objekt). Das ist das tatsächliche Python-Objekt, das Sie direkt anderen Funktionen oder Bibliotheken übergeben können, welche ein „file-like“-Objekt erwarten.

`UploadFile` hat die folgenden `async`hronen Methoden. Sie alle rufen die entsprechenden Methoden des darunterliegenden Datei-Objekts auf (wobei intern `SpooledTemporaryFile` verwendet wird).

* `write(daten)`: Schreibt `daten` (`str` oder `bytes`) in die Datei.
* `read(anzahl)`: Liest `anzahl` (`int`) bytes/Zeichen aus der Datei.
* `seek(versatz)`: Geht zur Position `versatz` (`int`) in der Datei.
    * Z. B. würde `await myfile.seek(0)` zum Anfang der Datei gehen.
    * Das ist besonders dann nützlich, wenn Sie `await myfile.read()` einmal ausführen und dann diese Inhalte erneut auslesen müssen.
* `close()`: Schließt die Datei.

Da alle diese Methoden `async`hron sind, müssen Sie sie `await`en („erwarten“).

Zum Beispiel können Sie innerhalb einer `async` *Pfadoperation-Funktion* den Inhalt wie folgt auslesen:

```Python
contents = await myfile.read()
```

Wenn Sie sich innerhalb einer normalen `def`-*Pfadoperation-Funktion* befinden, können Sie direkt auf `UploadFile.file` zugreifen, zum Beispiel:

```Python
contents = myfile.file.read()
```

/// note | "Technische Details zu `async`"

Wenn Sie die `async`-Methoden verwenden, führt **FastAPI** die Datei-Methoden in einem <abbr title="Mehrere unabhängige Kindprozesse">Threadpool</abbr> aus und erwartet sie.

///

/// note | "Technische Details zu Starlette"

**FastAPI**s `UploadFile` erbt direkt von **Starlette**s `UploadFile`, fügt aber ein paar notwendige Teile hinzu, um es kompatibel mit **Pydantic** und anderen Teilen von FastAPI zu machen.

///

## Was sind „Formulardaten“

HTML-Formulare (`<form></form>`) senden die Daten in einer „speziellen“ Kodierung zum Server, welche sich von JSON unterscheidet.

**FastAPI** stellt sicher, dass diese Daten korrekt ausgelesen werden, statt JSON zu erwarten.

/// note | "Technische Details"

Daten aus Formularen werden, wenn es keine Dateien sind, normalerweise mit dem <abbr title='Media type – Medientyp, Typ des Mediums'>„media type“</abbr> `application/x-www-form-urlencoded` kodiert.

Sollte das Formular aber Dateien enthalten, dann werden diese mit `multipart/form-data` kodiert. Wenn Sie `File` verwenden, wird **FastAPI** wissen, dass es die Dateien vom korrekten Teil des Bodys holen muss.

Wenn Sie mehr über Formularfelder und ihre Kodierungen lesen möchten, besuchen Sie die <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network – Mozilla-Entwickler-Netzwerk">MDN</abbr>-Webdokumentation für <code>POST</code></a>.

///

/// warning | "Achtung"

Sie können mehrere `File`- und `Form`-Parameter in einer *Pfadoperation* deklarieren, aber Sie können nicht gleichzeitig auch `Body`-Felder deklarieren, welche Sie als JSON erwarten, da der Request den Body mittels `multipart/form-data` statt `application/json` kodiert.

Das ist keine Limitation von **FastAPI**, sondern Teil des HTTP-Protokolls.

///

## Optionaler Datei-Upload

Sie können eine Datei optional machen, indem Sie Standard-Typannotationen verwenden und den Defaultwert auf `None` setzen:

//// tab | Python 3.10+

```Python hl_lines="9  17"
{!> ../../../docs_src/request_files/tutorial001_02_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9  17"
{!> ../../../docs_src/request_files/tutorial001_02_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10  18"
{!> ../../../docs_src/request_files/tutorial001_02_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7  15"
{!> ../../../docs_src/request_files/tutorial001_02_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="9  17"
{!> ../../../docs_src/request_files/tutorial001_02.py!}
```

////

## `UploadFile` mit zusätzlichen Metadaten

Sie können auch `File()` zusammen mit `UploadFile` verwenden, um zum Beispiel zusätzliche Metadaten zu setzen:

//// tab | Python 3.9+

```Python hl_lines="9  15"
{!> ../../../docs_src/request_files/tutorial001_03_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8  14"
{!> ../../../docs_src/request_files/tutorial001_03_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7  13"
{!> ../../../docs_src/request_files/tutorial001_03.py!}
```

////

## Mehrere Datei-Uploads

Es ist auch möglich, mehrere Dateien gleichzeitig hochzuladen.

Diese werden demselben Formularfeld zugeordnet, welches mit den Formulardaten gesendet wird.

Um das zu machen, deklarieren Sie eine Liste von `bytes` oder `UploadFile`s:

//// tab | Python 3.9+

```Python hl_lines="10  15"
{!> ../../../docs_src/request_files/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11  16"
{!> ../../../docs_src/request_files/tutorial002_an.py!}
```

////

//// tab | Python 3.9+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="8  13"
{!> ../../../docs_src/request_files/tutorial002_py39.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="10  15"
{!> ../../../docs_src/request_files/tutorial002.py!}
```

////

Sie erhalten, wie deklariert, eine `list`e von `bytes` oder `UploadFile`s.

/// note | "Technische Details"

Sie können auch `from starlette.responses import HTMLResponse` verwenden.

**FastAPI** bietet dieselben `starlette.responses` auch via `fastapi.responses` an, als Annehmlichkeit für Sie, den Entwickler. Die meisten verfügbaren Responses kommen aber direkt von Starlette.

///

### Mehrere Datei-Uploads mit zusätzlichen Metadaten

Und so wie zuvor können Sie `File()` verwenden, um zusätzliche Parameter zu setzen, sogar für `UploadFile`:

//// tab | Python 3.9+

```Python hl_lines="11  18-20"
{!> ../../../docs_src/request_files/tutorial003_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="12  19-21"
{!> ../../../docs_src/request_files/tutorial003_an.py!}
```

////

//// tab | Python 3.9+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="9  16"
{!> ../../../docs_src/request_files/tutorial003_py39.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="11  18"
{!> ../../../docs_src/request_files/tutorial003.py!}
```

////

## Zusammenfassung

Verwenden Sie `File`, `bytes` und `UploadFile`, um hochladbare Dateien im Request zu deklarieren, die als Formulardaten gesendet werden.
