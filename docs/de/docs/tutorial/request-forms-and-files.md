# Formulardaten und Dateien im Request

Sie können gleichzeitig Dateien und Formulardaten mit `File` und `Form` definieren.

/// info

Um hochgeladene Dateien und/oder Formulardaten zu empfangen, installieren Sie zuerst <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>.

Z. B. `pip install python-multipart`.

///

## `File` und `Form` importieren

//// tab | Python 3.9+

```Python hl_lines="3"
{!> ../../../docs_src/request_forms_and_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1"
{!> ../../../docs_src/request_forms_and_files/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="1"
{!> ../../../docs_src/request_forms_and_files/tutorial001.py!}
```

////

## `File` und `Form`-Parameter definieren

Erstellen Sie Datei- und Formularparameter, so wie Sie es auch mit `Body` und `Query` machen würden:

//// tab | Python 3.9+

```Python hl_lines="10-12"
{!> ../../../docs_src/request_forms_and_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9-11"
{!> ../../../docs_src/request_forms_and_files/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="8"
{!> ../../../docs_src/request_forms_and_files/tutorial001.py!}
```

////

Die Datei- und Formularfelder werden als Formulardaten hochgeladen, und Sie erhalten diese Dateien und Formularfelder.

Und Sie können einige der Dateien als `bytes` und einige als `UploadFile` deklarieren.

/// warning | "Achtung"

Sie können mehrere `File`- und `Form`-Parameter in einer *Pfadoperation* deklarieren, aber Sie können nicht gleichzeitig auch `Body`-Felder deklarieren, welche Sie als JSON erwarten, da der Request den Body mittels `multipart/form-data` statt `application/json` kodiert.

Das ist keine Limitation von **FastAPI**, sondern Teil des HTTP-Protokolls.

///

## Zusammenfassung

Verwenden Sie `File` und `Form` zusammen, wenn Sie Daten und Dateien zusammen im selben Request empfangen müssen.
