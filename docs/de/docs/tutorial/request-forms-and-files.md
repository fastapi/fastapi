# Formulardaten und Dateien im Request { #request-forms-and-files }

Sie können gleichzeitig Dateien und Formulardaten mit `File` und `Form` definieren.

/// info | Info

Um hochgeladene Dateien und/oder Formulardaten zu empfangen, installieren Sie zuerst <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Stellen Sie sicher, dass Sie eine [virtuelle Umgebung](../virtual-environments.md){.internal-link target=_blank} erstellen, diese aktivieren und es dann installieren, z. B.:

```console
$ pip install python-multipart
```

///

## `File` und `Form` importieren { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[3] *}

## `File` und `Form`-Parameter definieren { #define-file-and-form-parameters }

Erstellen Sie Datei- und Formularparameter, so wie Sie es auch mit `Body` oder `Query` machen würden:

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[10:12] *}

Die Datei- und Formularfelder werden als Formulardaten hochgeladen, und Sie erhalten diese Dateien und Formularfelder.

Und Sie können einige der Dateien als `bytes` und einige als `UploadFile` deklarieren.

/// warning | Achtung

Sie können mehrere `File`- und `Form`-Parameter in einer *Pfadoperation* deklarieren, aber Sie können nicht auch `Body`-Felder deklarieren, die Sie als JSON erwarten, da der Body des <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> mittels `multipart/form-data` statt `application/json` kodiert sein wird.

Das ist keine Limitation von **FastAPI**, sondern Teil des HTTP-Protokolls.

///

## Zusammenfassung { #recap }

Verwenden Sie `File` und `Form` zusammen, wenn Sie Daten und Dateien zusammen im selben Request empfangen müssen.
