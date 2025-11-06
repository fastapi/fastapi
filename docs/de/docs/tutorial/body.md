# Requestbody { #request-body }

Wenn Sie Daten von einem <abbr title="Client: Eine Software, die sich mit einem Server verbindet.">Client</abbr> (sagen wir, einem Browser) zu Ihrer API senden müssen, senden Sie sie als **Requestbody**.

Ein <abbr title="Anfragekörper">**Request**body</abbr> sind Daten, die vom Client zu Ihrer API gesendet werden. Ein <abbr title="Antwortkörper">**Response**body</abbr> sind Daten, die Ihre API zum Client sendet.

Ihre API muss fast immer einen **Response**body senden. Aber Clients müssen nicht unbedingt immer **Requestbodys** senden, manchmal fordern sie nur einen Pfad an, vielleicht mit einigen Query-Parametern, aber senden keinen Body.

Um einen **Request**body zu deklarieren, verwenden Sie <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>-Modelle mit all deren Fähigkeiten und Vorzügen.

/// info | Info

Um Daten zu senden, sollten Sie eines von: `POST` (meistverwendet), `PUT`, `DELETE` oder `PATCH` verwenden.

Das Senden eines Bodys mit einem `GET`-Request hat ein undefiniertes Verhalten in den Spezifikationen, wird aber dennoch von FastAPI unterstützt, nur für sehr komplexe/extreme Anwendungsfälle.

Da davon abgeraten wird, zeigt die interaktive Dokumentation mit Swagger-Benutzeroberfläche die Dokumentation für den Body nicht an, wenn `GET` verwendet wird, und zwischengeschaltete Proxys unterstützen es möglicherweise nicht.

///

## Pydantics `BaseModel` importieren { #import-pydantics-basemodel }

Zuerst müssen Sie `BaseModel` von `pydantic` importieren:

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## Ihr Datenmodell erstellen { #create-your-data-model }

Dann deklarieren Sie Ihr Datenmodell als eine Klasse, die von `BaseModel` erbt.

Verwenden Sie Standard-Python-Typen für alle Attribute:

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}

Wie auch bei der Deklaration von Query-Parametern gilt: Wenn ein Modellattribut einen Defaultwert hat, ist das Attribut nicht erforderlich. Andernfalls ist es erforderlich. Verwenden Sie `None`, um es einfach optional zu machen.

Zum Beispiel deklariert das obige Modell ein JSON „`object`“ (oder Python-<abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">`dict`</abbr>) wie dieses:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

Da `description` und `tax` optional sind (mit `None` als Defaultwert), wäre folgendes JSON „`object`“ auch gültig:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## Als Parameter deklarieren { #declare-it-as-a-parameter }

Um es zu Ihrer *Pfadoperation* hinzuzufügen, deklarieren Sie es auf die gleiche Weise, wie Sie Pfad- und Query-Parameter deklariert haben:

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

... und deklarieren Sie dessen Typ als das Modell, welches Sie erstellt haben, `Item`.

## Resultate { #results }

Mit nur dieser Python-Typdeklaration wird **FastAPI**:

* Den Requestbody als JSON lesen.
* Die entsprechenden Typen konvertieren (falls nötig).
* Diese Daten validieren.
    * Wenn die Daten ungültig sind, wird ein klar lesbarer Fehler zurückgegeben, der genau anzeigt, wo und was die inkorrekten Daten sind.
* Ihnen die erhaltenen Daten im Parameter `item` übergeben.
    * Da Sie ihn in der Funktion als vom Typ `Item` deklariert haben, erhalten Sie auch die volle Unterstützung des Editors (Autovervollständigung, usw.) für alle Attribute und deren Typen.
* <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a>-Definitionen für Ihr Modell generieren, die Sie auch überall sonst verwenden können, wenn es für Ihr Projekt Sinn macht.
* Diese Schemas werden Teil des generierten OpenAPI-Schemas und werden von den <abbr title="User Interfaces – Benutzeroberflächen">UIs</abbr> der automatischen Dokumentation genutzt.

## Automatische Dokumentation { #automatic-docs }

Die JSON-Schemas Ihrer Modelle werden Teil Ihres OpenAPI-generierten Schemas und in der interaktiven API-Dokumentation angezeigt:

<img src="/img/tutorial/body/image01.png">

Und werden auch in der API-Dokumentation innerhalb jeder *Pfadoperation*, die sie benötigt, verwendet:

<img src="/img/tutorial/body/image02.png">

## Editor-Unterstützung { #editor-support }

In Ihrem Editor erhalten Sie innerhalb Ihrer Funktion Typhinweise und Code-Vervollständigung überall (was nicht der Fall wäre, wenn Sie ein `dict` anstelle eines Pydantic-Modells erhalten hätten):

<img src="/img/tutorial/body/image03.png">

Sie bekommen auch Fehlermeldungen für inkorrekte Typoperationen:

<img src="/img/tutorial/body/image04.png">

Das ist nicht zufällig so, das ganze Framework wurde um dieses Design herum aufgebaut.

Und es wurde in der Designphase gründlich getestet, bevor irgendeine Implementierung stattfand, um sicherzustellen, dass es mit allen Editoren funktioniert.

Es gab sogar einige Änderungen an Pydantic selbst, um dies zu unterstützen.

Die vorherigen Screenshots wurden mit <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a> aufgenommen.

Aber Sie würden die gleiche Editor-Unterstützung in <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> und den meisten anderen Python-Editoren erhalten:

<img src="/img/tutorial/body/image05.png">

/// tip | Tipp

Wenn Sie <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> als Ihren Editor verwenden, können Sie das <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a> ausprobieren.

Es verbessert die Editor-Unterstützung für Pydantic-Modelle, mit:

* Code-Vervollständigung
* Typüberprüfungen
* Refaktorisierung
* Suche
* Inspektionen

///

## Das Modell verwenden { #use-the-model }

Innerhalb der Funktion können Sie alle Attribute des Modellobjekts direkt verwenden:

{* ../../docs_src/body/tutorial002_py310.py *}

/// info | Info

In Pydantic v1 hieß die Methode `.dict()`, sie wurde in Pydantic v2 deprecatet (aber weiterhin unterstützt) und in `.model_dump()` umbenannt.

Die Beispiele hier verwenden `.dict()` zur Kompatibilität mit Pydantic v1, aber Sie sollten stattdessen `.model_dump()` verwenden, wenn Sie Pydantic v2 nutzen können.

///

## Requestbody- + Pfad-Parameter { #request-body-path-parameters }

Sie können Pfad-Parameter und den Requestbody gleichzeitig deklarieren.

**FastAPI** erkennt, dass Funktionsparameter, die mit Pfad-Parametern übereinstimmen, **vom Pfad genommen** werden sollen, und dass Funktionsparameter, welche Pydantic-Modelle sind, **vom Requestbody genommen** werden sollen.

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}


## Requestbody- + Pfad- + Query-Parameter { #request-body-path-query-parameters }

Sie können auch zur gleichen Zeit **Body-**, **Pfad-** und **Query-Parameter** deklarieren.

**FastAPI** wird jeden von ihnen korrekt erkennen und die Daten vom richtigen Ort holen.

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

Die Funktionsparameter werden wie folgt erkannt:

* Wenn der Parameter auch im **Pfad** deklariert wurde, wird er als Pfad-Parameter verwendet.
* Wenn der Parameter ein **einfacher Typ** ist (wie `int`, `float`, `str`, `bool`, usw.), wird er als **Query**-Parameter interpretiert.
* Wenn der Parameter vom Typ eines **Pydantic-Modells** ist, wird er als Request**body** interpretiert.

/// note | Hinweis

FastAPI weiß, dass der Wert von `q` nicht erforderlich ist, aufgrund des definierten Defaultwertes `= None`.

Das `str | None` (Python 3.10+) oder `Union` in `Union[str, None]` (Python 3.8+) wird von FastAPI nicht verwendet, um zu bestimmen, dass der Wert nicht erforderlich ist. FastAPI weiß, dass er nicht erforderlich ist, weil er einen Defaultwert von `= None` hat.

Das Hinzufügen der Typannotationen ermöglicht jedoch Ihrem Editor, Ihnen eine bessere Unterstützung zu bieten und Fehler zu erkennen.

///

## Ohne Pydantic { #without-pydantic }

Wenn Sie keine Pydantic-Modelle verwenden möchten, können Sie auch **Body**-Parameter verwenden. Siehe die Dokumentation unter [Body – Mehrere Parameter: Einfache Werte im Body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}.
