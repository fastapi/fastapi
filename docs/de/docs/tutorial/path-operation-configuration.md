# Pfadoperation-Konfiguration { #path-operation-configuration }

Es gibt mehrere Parameter, die Sie Ihrem *Pfadoperation-Dekorator* übergeben können, um ihn zu konfigurieren.

/// warning | Achtung

Beachten Sie, dass diese Parameter direkt dem *Pfadoperation-Dekorator* übergeben werden, nicht der *Pfadoperation-Funktion*.

///

## Response-Statuscode { #response-status-code }

Sie können den (HTTP-)`status_code` definieren, der in der <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> Ihrer *Pfadoperation* verwendet werden soll.

Sie können direkt den `int`-Code übergeben, etwa `404`.

Aber falls Sie sich nicht mehr erinnern, wofür jeder Nummerncode steht, können Sie die Abkürzungs-Konstanten in `status` verwenden:

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

Dieser Statuscode wird in der Response verwendet und zum OpenAPI-Schema hinzugefügt.

/// note | Technische Details

Sie können auch `from starlette import status` verwenden.

**FastAPI** bietet dieselben `starlette.status`-Codes auch via `fastapi.status` an, als Annehmlichkeit für Sie, den Entwickler. Sie kommen aber direkt von Starlette.

///

## Tags { #tags }

Sie können Ihrer *Pfadoperation* Tags hinzufügen, indem Sie dem Parameter `tags` eine `list`e von `str`s übergeben (in der Regel nur ein `str`):

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

Diese werden zum OpenAPI-Schema hinzugefügt und von den automatischen Dokumentations-Benutzeroberflächen verwendet:

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Tags mittels Enumeration { #tags-with-enums }

Wenn Sie eine große Anwendung haben, können sich am Ende **viele Tags** anhäufen, und Sie möchten sicherstellen, dass Sie für verwandte *Pfadoperationen* immer den **gleichen Tag** verwenden.

In diesem Fall macht es Sinn, die Tags in einem `Enum` zu speichern.

**FastAPI** unterstützt das auf die gleiche Weise wie einfache Strings:

{* ../../docs_src/path_operation_configuration/tutorial002b.py hl[1,8:10,13,18] *}

## Zusammenfassung und Beschreibung { #summary-and-description }

Sie können eine <abbr title="Zusammenfassung">`summary`</abbr> und eine <abbr title="Beschreibung">`description`</abbr> hinzufügen:

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[18:19] *}

## Beschreibung mittels Docstring { #description-from-docstring }

Da Beschreibungen oft mehrere Zeilen lang sind, können Sie die Beschreibung der *Pfadoperation* im <abbr title="Ein mehrzeiliger String (keiner Variable zugewiesen) als erster Ausdruck in einer Funktion, wird für die Dokumentation derselben verwendet">Docstring</abbr> der Funktion deklarieren, und **FastAPI** wird sie daraus auslesen.

Sie können <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a> im Docstring schreiben, es wird korrekt interpretiert und angezeigt (unter Berücksichtigung der Einrückung des Docstring).

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

Es wird in der interaktiven Dokumentation verwendet:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## Beschreibung der Response { #response-description }

Sie können die Response mit dem Parameter `response_description` beschreiben:

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[19] *}

/// info | Info

Beachten Sie, dass sich `response_description` speziell auf die Response bezieht, während `description` sich generell auf die *Pfadoperation* bezieht.

///

/// check | Testen

OpenAPI verlangt, dass jede *Pfadoperation* über eine Beschreibung der Response verfügt.

Daher, wenn Sie keine vergeben, wird **FastAPI** automatisch eine für „Erfolgreiche Response“ erstellen.

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## Eine *Pfadoperation* deprecaten { #deprecate-a-path-operation }

Wenn Sie eine *Pfadoperation* als <abbr title="veraltet, obsolet: Es soll nicht mehr verwendet werden">deprecatet</abbr> kennzeichnen möchten, ohne sie zu entfernen, fügen Sie den Parameter `deprecated` hinzu:

{* ../../docs_src/path_operation_configuration/tutorial006.py hl[16] *}

Sie wird in der interaktiven Dokumentation gut sichtbar als deprecatet markiert werden:

<img src="/img/tutorial/path-operation-configuration/image04.png">

Vergleichen Sie, wie deprecatete und nicht-deprecatete *Pfadoperationen* aussehen:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## Zusammenfassung { #recap }

Sie können auf einfache Weise Metadaten für Ihre *Pfadoperationen* definieren, indem Sie den *Pfadoperation-Dekoratoren* Parameter hinzufügen.
