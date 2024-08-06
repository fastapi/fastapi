# Pfadoperation-Konfiguration

Es gibt mehrere Konfigurations-Parameter, die Sie Ihrem *Pfadoperation-Dekorator* übergeben können.

/// warning | "Achtung"

Beachten Sie, dass diese Parameter direkt dem *Pfadoperation-Dekorator* übergeben werden, nicht der *Pfadoperation-Funktion*.

///

## Response-Statuscode

Sie können den (HTTP-)`status_code` definieren, den die Response Ihrer *Pfadoperation* verwenden soll.

Sie können direkt den `int`-Code übergeben, etwa `404`.

Aber falls Sie sich nicht mehr erinnern, wofür jede Nummer steht, können Sie die Abkürzungs-Konstanten in `status` verwenden:

//// tab | Python 3.10+

```Python hl_lines="1  15"
{!> ../../../docs_src/path_operation_configuration/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="3  17"
{!> ../../../docs_src/path_operation_configuration/tutorial001_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="3  17"
{!> ../../../docs_src/path_operation_configuration/tutorial001.py!}
```

////

Dieser Statuscode wird in der Response verwendet und zum OpenAPI-Schema hinzugefügt.

/// note | "Technische Details"

Sie können auch `from starlette import status` verwenden.

**FastAPI** bietet dieselben `starlette.status`-Codes auch via `fastapi.status` an, als Annehmlichkeit für Sie, den Entwickler. Sie kommen aber direkt von Starlette.

///

## Tags

Sie können Ihrer *Pfadoperation* Tags hinzufügen, mittels des Parameters `tags`, dem eine `list`e von `str`s übergeben wird (in der Regel nur ein `str`):

//// tab | Python 3.10+

```Python hl_lines="15  20  25"
{!> ../../../docs_src/path_operation_configuration/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="17  22  27"
{!> ../../../docs_src/path_operation_configuration/tutorial002_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="17  22  27"
{!> ../../../docs_src/path_operation_configuration/tutorial002.py!}
```

////

Diese werden zum OpenAPI-Schema hinzugefügt und von den automatischen Dokumentations-Benutzeroberflächen verwendet:

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Tags mittels Enumeration

Wenn Sie eine große Anwendung haben, können sich am Ende **viele Tags** anhäufen, und Sie möchten sicherstellen, dass Sie für verwandte *Pfadoperationen* immer den **gleichen Tag** nehmen.

In diesem Fall macht es Sinn, die Tags in einem `Enum` zu speichern.

**FastAPI** unterstützt diese genauso wie einfache Strings:

```Python hl_lines="1  8-10  13  18"
{!../../../docs_src/path_operation_configuration/tutorial002b.py!}
```

## Zusammenfassung und Beschreibung

Sie können eine Zusammenfassung (`summary`) und eine Beschreibung (`description`) hinzufügen:

//// tab | Python 3.10+

```Python hl_lines="18-19"
{!> ../../../docs_src/path_operation_configuration/tutorial003_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="20-21"
{!> ../../../docs_src/path_operation_configuration/tutorial003_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="20-21"
{!> ../../../docs_src/path_operation_configuration/tutorial003.py!}
```

////

## Beschreibung mittels Docstring

Da Beschreibungen oft mehrere Zeilen lang sind, können Sie die Beschreibung der *Pfadoperation* im <abbr title="Ein mehrzeiliger String (keiner Variable zugewiesen) als erster Ausdruck in einer Funktion, wird für die Dokumentation derselben verwendet">Docstring</abbr> der Funktion deklarieren, und **FastAPI** wird sie daraus auslesen.

Sie können im Docstring <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a> schreiben, es wird korrekt interpretiert und angezeigt (die Einrückung des Docstring beachtend).

//// tab | Python 3.10+

```Python hl_lines="17-25"
{!> ../../../docs_src/path_operation_configuration/tutorial004_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="19-27"
{!> ../../../docs_src/path_operation_configuration/tutorial004_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="19-27"
{!> ../../../docs_src/path_operation_configuration/tutorial004.py!}
```

////

In der interaktiven Dokumentation sieht das dann so aus:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## Beschreibung der Response

Die Response können Sie mit dem Parameter `response_description` beschreiben:

//// tab | Python 3.10+

```Python hl_lines="19"
{!> ../../../docs_src/path_operation_configuration/tutorial005_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="21"
{!> ../../../docs_src/path_operation_configuration/tutorial005_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="21"
{!> ../../../docs_src/path_operation_configuration/tutorial005.py!}
```

////

/// info

beachten Sie, dass sich `response_description` speziell auf die Response bezieht, während `description` sich generell auf die *Pfadoperation* bezieht.

///

/// check

OpenAPI verlangt, dass jede *Pfadoperation* über eine Beschreibung der Response verfügt.

Daher, wenn Sie keine vergeben, wird **FastAPI** automatisch eine für „Erfolgreiche Response“ erstellen.

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## Eine *Pfadoperation* deprecaten

Wenn Sie eine *Pfadoperation* als <abbr title="deprecated – obsolet, veraltet: Es soll nicht mehr verwendet werden">deprecated</abbr> kennzeichnen möchten, ohne sie zu entfernen, fügen Sie den Parameter `deprecated` hinzu:

```Python hl_lines="16"
{!../../../docs_src/path_operation_configuration/tutorial006.py!}
```

Sie wird in der interaktiven Dokumentation gut sichtbar als deprecated markiert werden:

<img src="/img/tutorial/path-operation-configuration/image04.png">

Vergleichen Sie, wie deprecatete und nicht-deprecatete *Pfadoperationen* aussehen:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## Zusammenfassung

Sie können auf einfache Weise Metadaten für Ihre *Pfadoperationen* definieren, indem Sie den *Pfadoperation-Dekoratoren* Parameter hinzufügen.
