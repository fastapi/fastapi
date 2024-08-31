# Requestbody

Wenn Sie Daten von einem <abbr title="Client: Eine Software, die sich mit einem Server verbindet.">Client</abbr> (sagen wir, einem Browser) zu Ihrer API senden, dann senden Sie diese als einen **Requestbody** (Deutsch: Anfragekörper).

Ein **Request**body sind Daten, die vom Client zu Ihrer API gesendet werden. Ein **Response**body (Deutsch: Antwortkörper) sind Daten, die Ihre API zum Client sendet.

Ihre API sendet fast immer einen **Response**body. Aber Clients senden nicht unbedingt immer **Request**bodys (sondern nur Metadaten).

Um einen **Request**body zu deklarieren, verwenden Sie <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>-Modelle mit allen deren Fähigkeiten und Vorzügen.

/// info

Um Daten zu versenden, sollten Sie eines von: `POST` (meistverwendet), `PUT`, `DELETE` oder `PATCH` verwenden.

Senden Sie einen Body mit einem `GET`-Request, dann führt das laut Spezifikation zu undefiniertem Verhalten. Trotzdem wird es von FastAPI unterstützt, für sehr komplexe/extreme Anwendungsfälle.

Da aber davon abgeraten wird, zeigt die interaktive Dokumentation mit Swagger-Benutzeroberfläche die Dokumentation für den Body auch nicht an, wenn `GET` verwendet wird. Dazwischengeschaltete Proxys unterstützen es möglicherweise auch nicht.

///

## Importieren Sie Pydantics `BaseModel`

Zuerst müssen Sie `BaseModel` von `pydantic` importieren:

//// tab | Python 3.10+

```Python hl_lines="2"
{!> ../../../docs_src/body/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="4"
{!> ../../../docs_src/body/tutorial001.py!}
```

////

## Erstellen Sie Ihr Datenmodell

Dann deklarieren Sie Ihr Datenmodell als eine Klasse, die von `BaseModel` erbt.

Verwenden Sie Standard-Python-Typen für die Klassenattribute:

//// tab | Python 3.10+

```Python hl_lines="5-9"
{!> ../../../docs_src/body/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="7-11"
{!> ../../../docs_src/body/tutorial001.py!}
```

////

Wie auch bei Query-Parametern gilt, wenn ein Modellattribut einen Defaultwert hat, ist das Attribut nicht erforderlich. Ansonsten ist es erforderlich. Verwenden Sie `None`, um es als optional zu kennzeichnen.

Zum Beispiel deklariert das obige Modell ein JSON "`object`" (oder Python-`dict`) wie dieses:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

Da `description` und `tax` optional sind (mit `None` als Defaultwert), wäre folgendes JSON "`object`" auch gültig:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## Deklarieren Sie es als Parameter

Um es zu Ihrer *Pfadoperation* hinzuzufügen, deklarieren Sie es auf die gleiche Weise, wie Sie Pfad- und Query-Parameter deklariert haben:

//// tab | Python 3.10+

```Python hl_lines="16"
{!> ../../../docs_src/body/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="18"
{!> ../../../docs_src/body/tutorial001.py!}
```

////

... und deklarieren Sie seinen Typ als das Modell, welches Sie erstellt haben, `Item`.

## Resultate

Mit nur dieser Python-Typdeklaration, wird **FastAPI**:

* Den Requestbody als JSON lesen.
* Die entsprechenden Typen konvertieren (falls nötig).
* Diese Daten validieren.
    * Wenn die Daten ungültig sind, einen klar lesbaren Fehler zurückgeben, der anzeigt, wo und was die inkorrekten Daten waren.
* Ihnen die erhaltenen Daten im Parameter `item` übergeben.
    * Da Sie diesen in der Funktion als vom Typ `Item` deklariert haben, erhalten Sie die ganze Editor-Unterstützung (Autovervollständigung, usw.) für alle Attribute und deren Typen.
* Eine <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> Definition für Ihr Modell generieren, welche Sie überall sonst verwenden können, wenn es für Ihr Projekt Sinn macht.
* Diese Schemas werden Teil des generierten OpenAPI-Schemas und werden von den <abbr title="User Interface – Benutzeroberfläche">UIs</abbr> der automatischen Dokumentation verwendet.

## Automatische Dokumentation

Die JSON-Schemas Ihrer Modelle werden Teil ihrer OpenAPI-generierten Schemas und werden in der interaktiven API Dokumentation angezeigt:

<img src="/img/tutorial/body/image01.png">

Und werden auch verwendet in der API-Dokumentation innerhalb jeder *Pfadoperation*, welche sie braucht:

<img src="/img/tutorial/body/image02.png">

## Editor Unterstützung

In Ihrem Editor, innerhalb Ihrer Funktion, erhalten Sie Typhinweise und Code-Vervollständigung überall (was nicht der Fall wäre, wenn Sie ein `dict` anstelle eines Pydantic Modells erhalten hätten):

<img src="/img/tutorial/body/image03.png">

Sie bekommen auch Fehler-Meldungen für inkorrekte Typoperationen:

<img src="/img/tutorial/body/image04.png">

Das ist nicht zufällig so, das ganze Framework wurde um dieses Design herum aufgebaut.

Und es wurde in der Designphase gründlich getestet, vor der Implementierung, um sicherzustellen, dass es mit jedem Editor funktioniert.

Es gab sogar ein paar Änderungen an Pydantic selbst, um das zu unterstützen.

Die vorherigen Screenshots zeigten <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>.

Aber Sie bekommen die gleiche Editor-Unterstützung in <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> und in den meisten anderen Python-Editoren:

<img src="/img/tutorial/body/image05.png">

/// tip | "Tipp"

Wenn Sie <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> als Ihren Editor verwenden, probieren Sie das <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a> aus.

Es verbessert die Editor-Unterstützung für Pydantic-Modelle, mit:

* Code-Vervollständigung
* Typüberprüfungen
* Refaktorisierung
* Suchen
* Inspektionen

///

## Das Modell verwenden

Innerhalb der Funktion können Sie alle Attribute des Modells direkt verwenden:

//// tab | Python 3.10+

```Python hl_lines="19"
{!> ../../../docs_src/body/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="21"
{!> ../../../docs_src/body/tutorial002.py!}
```

////

## Requestbody- + Pfad-Parameter

Sie können Pfad- und Requestbody-Parameter gleichzeitig deklarieren.

**FastAPI** erkennt, dass Funktionsparameter, die mit Pfad-Parametern übereinstimmen, **vom Pfad genommen** werden sollen, und dass Funktionsparameter, welche Pydantic-Modelle sind, **vom Requestbody genommen** werden sollen.

//// tab | Python 3.10+

```Python hl_lines="15-16"
{!> ../../../docs_src/body/tutorial003_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="17-18"
{!> ../../../docs_src/body/tutorial003.py!}
```

////

## Requestbody- + Pfad- + Query-Parameter

Sie können auch zur gleichen Zeit **Body-**, **Pfad-** und **Query-Parameter** deklarieren.

**FastAPI** wird jeden Parameter korrekt erkennen und die Daten vom richtigen Ort holen.

//// tab | Python 3.10+

```Python hl_lines="16"
{!> ../../../docs_src/body/tutorial004_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="18"
{!> ../../../docs_src/body/tutorial004.py!}
```

////

Die Funktionsparameter werden wie folgt erkannt:

* Wenn der Parameter auch im **Pfad** deklariert wurde, wird er als Pfad-Parameter interpretiert.
* Wenn der Parameter ein **einfacher Typ** ist (wie `int`, `float`, `str`, `bool`, usw.), wird er als **Query**-Parameter interpretiert.
* Wenn der Parameter vom Typ eines **Pydantic-Modells** ist, wird er als Request**body** interpretiert.

/// note | "Hinweis"

FastAPI weiß, dass der Wert von `q` nicht erforderlich ist, wegen des definierten Defaultwertes `= None`

Das `Union` in `Union[str, None]` wird von FastAPI nicht verwendet, aber es erlaubt Ihrem Editor, Sie besser zu unterstützen und Fehler zu erkennen.

///

## Ohne Pydantic

Wenn Sie keine Pydantic-Modelle verwenden wollen, können Sie auch **Body**-Parameter nehmen. Siehe die Dokumentation unter [Body – Mehrere Parameter: Einfache Werte im Body](body-multiple-params.md#einzelne-werte-im-body){.internal-link target=\_blank}.
