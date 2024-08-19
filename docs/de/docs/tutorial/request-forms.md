# Formulardaten

Wenn Sie Felder aus Formularen statt JSON empfangen müssen, können Sie `Form` verwenden.

/// info

Um Formulare zu verwenden, installieren Sie zuerst <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>.

Z. B. `pip install python-multipart`.

///

## `Form` importieren

Importieren Sie `Form` von `fastapi`:

//// tab | Python 3.9+

```Python hl_lines="3"
{!> ../../../docs_src/request_forms/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1"
{!> ../../../docs_src/request_forms/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="1"
{!> ../../../docs_src/request_forms/tutorial001.py!}
```

////

## `Form`-Parameter definieren

Erstellen Sie Formular-Parameter, so wie Sie es auch mit `Body` und `Query` machen würden:

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/request_forms/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8"
{!> ../../../docs_src/request_forms/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/request_forms/tutorial001.py!}
```

////

Zum Beispiel stellt eine der Möglichkeiten, die OAuth2 Spezifikation zu verwenden (genannt <abbr title='„Passwort-Fluss“'>„password flow“</abbr>), die Bedingung, einen `username` und ein `password` als Formularfelder zu senden.

Die <abbr title="Specification – Spezifikation">Spec</abbr> erfordert, dass die Felder exakt `username` und `password` genannt werden und als Formularfelder, nicht JSON, gesendet werden.

Mit `Form` haben Sie die gleichen Konfigurationsmöglichkeiten wie mit `Body` (und `Query`, `Path`, `Cookie`), inklusive Validierung, Beispielen, einem Alias (z. B. `user-name` statt `username`), usw.

/// info

`Form` ist eine Klasse, die direkt von `Body` erbt.

///

/// tip | "Tipp"

Um Formularbodys zu deklarieren, verwenden Sie explizit `Form`, da diese Parameter sonst als Query-Parameter oder Body(-JSON)-Parameter interpretiert werden würden.

///

## Über „Formularfelder“

HTML-Formulare (`<form></form>`) senden die Daten in einer „speziellen“ Kodierung zum Server, welche sich von JSON unterscheidet.

**FastAPI** stellt sicher, dass diese Daten korrekt ausgelesen werden, statt JSON zu erwarten.

/// note | "Technische Details"

Daten aus Formularen werden normalerweise mit dem <abbr title='Media type – Medientyp, Typ des Mediums'>„media type“</abbr> `application/x-www-form-urlencoded` kodiert.

Wenn das Formular stattdessen Dateien enthält, werden diese mit `multipart/form-data` kodiert. Im nächsten Kapitel erfahren Sie mehr über die Handhabung von Dateien.

Wenn Sie mehr über Formularfelder und ihre Kodierungen lesen möchten, besuchen Sie die <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network – Mozilla-Entwickler-Netzwerk">MDN</abbr>-Webdokumentation für <code>POST</code></a>.

///

/// warning | "Achtung"

Sie können mehrere `Form`-Parameter in einer *Pfadoperation* deklarieren, aber Sie können nicht gleichzeitig auch `Body`-Felder deklarieren, welche Sie als JSON erwarten, da der Request den Body mittels `application/x-www-form-urlencoded` statt `application/json` kodiert.

Das ist keine Limitation von **FastAPI**, sondern Teil des HTTP-Protokolls.

///

## Zusammenfassung

Verwenden Sie `Form`, um Eingabe-Parameter für Formulardaten zu deklarieren.
