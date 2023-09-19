# Pfad-Parameter

Man kann die Pfad-"Parameter" oder -"Variablen" mit der gleichen Syntax deklarieren, die man auch für Formatierungsstrings in Python verwendet:

```Python hl_lines="6-7"
{!../../../docs_src/path_params/tutorial001.py!}
```

Der Wert des Pfad-Parameters `item_id` wird der Funktion als Argument `item_id` übergeben.

Wenn man also dieses Beispiel ausführt und auf <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> geht, bekommt man folgende Antwort zurück:

```JSON
{"item_id":"foo"}
```

## Pfad-Parameter mit Typen

Man kann den Typ eines Pfad-Parameters in der Funkiton deklarieren, in dem man Standard Python-Typannotationen verwendet:

```Python hl_lines="7"
{!../../../docs_src/path_params/tutorial002.py!}
```

In diesem Fall wird `item_id` als `int` deklariert.

!!! check
    Dies wird Ihnen Editor-Unterstützung innerhalb Ihrer Funktion geben, mit Fehlerüberprüfungen, Vervollständigung usw.

## <abbr title="Auch bekannt als: Serialisierung, Parsing, Marshalling">Datenkonversion</abbr>

Wenn Sie dieses Beispiel ausführen und im Browser <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a> öffnen, erhalten Sie folgende Antwort:

```JSON
{"item_id":3}
```

!!! check
    Beachten Sie, dass der Wert, den Ihre Funktion erhält (und zurückgibt) `3` ist, also ein Python `int` und nicht der String `"3"`.

    Mit dieser Typdeklarierung, gibt Ihnen **FastAPI** also eine automatische Request-<abbr title="Den String, der von der HTTP-Anfrage kommt in Python-Daten umwandeln">"Serialisierung"</abbr>.

## Datenvalidierung

Gehen Sie jedoch im Browser auf <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, erhalten Sie diesen HTTP-Fehler:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

Das liegt daran, dass der Pfad-Parameter `item_id` einen Wert von `"foo"` hat, was kein `int` ist.

Der gleiche Fehler würde erscheinen, wenn man ein `float` statt einem `int` verwendet, also: <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

!!! check
    Über die Typdeklaration aus Python, gibt einem **FastAPI** also Datenvalidierung.

    Beachten Sie, dass der Fehler genau darstellt, wo die Validierung gescheitert ist.

    Das ist unglaublich nützlich während man entwickelt und Code debugged, der mit der API interagiert.

## Dokumentation

Und wenn Sie im Browser auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> gehen, erhalten Sie eine automatische, interaktive API-Dokumentation:

<img src="/img/tutorial/path-params/image01.png">

!!! check
    Nochmal, alleine durch die selben Python Typdeklarationen, gibt einem **FastAPI** eine automatische, interaktive Dokumentation (über die Swagger UI).

    Man beachte, dass der Pfad-Parameter als ein Integer deklariert ist.

## Vorteile durch Standardisierung, alternative Dokumentation

Und weil das generierte Schema nach dem <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a>-Standard ist, gibt es viele kompatible Tools.

Aufgrund dessen stellt **FastAPI** selbst eine alternative API-Dokumentation (ReDoc) zur Verfügung, auf welche man über <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> zugreifen kann:

<img src="/img/tutorial/path-params/image02.png">

Auf die gleiche Art, gibt es viele kompatible Tools. Darunter auch Code-Generierungs-Tools für viele verschiedene Sprachen.

## Pydantic

Jegliche Datenvalidierung, die hier unter der Haube stattfindet, passiert durch <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>, wodurch jene in guten Händen liegt, weil man alle Vorteile von Pydantic bekommt.

Man kann die gleichen Typdeklarationen wie `str`, `float`, `bool`und viele andere komplexe Datentypen verwenden.

Einige davon werden in den nächsten Kapiteln behandelt.

## Reihenfolge ist wichtig

Wenn wir *Pfad-Operationen* erstellen, fiden wir uns in Situationen wieder, wo wir einen festgelegten Pfad haben.

Sagen wir bspw. `/users/me` ist dazu da, um Daten über den Benutzer zu erhalten.

Und dann ist da noch ein Pfad `/users/{user_id}` um Daten über einen spezifischen Nutzer unter Verwendung einer Benutzer-ID zu erhalten.

Weil *Pfad-Operationen* über die Anordnung nach ihrer Reihenfolge, wie sie im Code geschrieben sind, ausgewertet werden, müssen wir sicherstellen, dass der Pfad für `/users/me` vor dem Pfad für `/users/{user_id}` deklariert wird:

```Python hl_lines="6  11"
{!../../../docs_src/path_params/tutorial003.py!}
```

Ansonsten würde der Pfad für `/users/{user_id}` so ausgewertet werden, dass er mit `/users/me` übereinstimmen und **FastAPI** "denken" würde, dass es den Parameter `user_id` mit einem Wert von `"me"` erhält.

Gleichzeitig kann man keine Pfad-Operation nochmal definieren:

```Python hl_lines="6  11"
{!../../../docs_src/path_params/tutorial003b.py!}
```

Der zuerst definierte Pfad wird also immer verwendet werden, weil er zuerst übereinstimmt.

## Vordefinierte Werte

Wenn Sie eine *Pfad-Operation* haben, die einen *Pfad-Parameter* erhält, aber Sie wollen die möglichen, validen *Pfad-Parameter* als vordefinierte Werte, können Sie ein standardmäßiges Python <abbr title="Enumeration">`Enum`</abbr> verwenden.

### Erstellen einer `Enum` Klasse

Importieren Sie `Enum` und erstellen Sie eine Unterklasse die von `str` und `Enum` erbt.

Indem man von `str` erbt, werden die API docs in die Lage versetzt, zu wissen, dass die Werte vom Datentyp `string` sein müssen und dementsprechend korrekt rendern.

Danach erstellen Sie Klassenattribute mit festen Werten, welche dann die zur Verfügung stehenden validen Werte sein werden:

```Python hl_lines="1  6-9"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! info
    <a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">Enumerations (oder Enums) sind in Python</a> seit Version 3.4 verfügbar.

!!! tip
    Falls Sie sich wundern: "AlexNet", "ResNet", und "LeNet" sind bloß Namen von Machine Learning <abbr title="Genauer, Deep Learning Model Architekturen">Modellen</abbr>.

### Deklarieren Sie einen *Pfad-Parameter*

Danach erstellen Sie einen *Pfad-Parameter* mit einer Typannotation, die die Enum-Klasse verwendet, die Sie erstellt haben (`ModelName`):

```Python hl_lines="16"
{!../../../docs_src/path_params/tutorial005.py!}
```

### Überprüfen Sie die Docs

Weil die zur Verfügung stehenden Werte für die *Pfad-Parameter* vordefiniert wurden, können die interaktiven Dokumentationen sie anschaulich darstellen:

<img src="/img/tutorial/path-params/image03.png">

### Mit Python's *Enumerationen* arbeiten

Der Wert der *Pfad-Parameter* wird ein *Enumerationsattribut* sein.

#### *Enumerationsattribute* vergleichen

Sie können es mit dem *Enumerationsattribut* in Ihrem erstelltem Enum `ModelName` vergleichen:

```Python hl_lines="17"
{!../../../docs_src/path_params/tutorial005.py!}
```

#### Den *Enumerationswert* erhalten

Sie können den eigentlichen Wert (ein `str` in diesem Fall) erhalten, wenn Sie `model_name.value` verwenden, oder im Allgemeinen `ihr_enum_attribut.wert`:

```Python hl_lines="20"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! tip
    Sie können ebenfalls auf den Wert `"lenet"` über `ModelName.lenet.value` zugreifen.

#### *Enumerationsattribute* zurückgeben

Sie können *Enumattribute* von ihren *Pfad-Parametern* zurückgeben, sogar in einer JSON-Struktur verschachtelt (z.B. über einen `dict`).

Diese werden zu ihren entsprechenden Werten konvertiert (strings in diesem Fall) bevor sie an den Client zurückgegeben werden:

```Python hl_lines="18  21  23"
{!../../../docs_src/path_params/tutorial005.py!}
```

In Ihrem Client erhalten Sie eine JSON-Response:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Pfad-Parameter, die Pfade enthalten

Sagen wir, Sie haben eine *Pfad-Operation* mit einem Pfad `/files/{file_path}`.

Jedoch benötigen Sie, dass `file_path` selbst einen *Pfad* wie `home/johndoe/myfile.txt`enthält.

Die URL dafür wäre etwas in dieser Art: `/files/home/johndoe/myfile.txt`.

### OpenAPI-Unterstützung

OpenAPI unterstützt keine Möglichkeit, einen *Pfad-Parameter* so zu deklarieren, dass er einen *Pfad* enthält, da dies zu Szenarien führen könnte, die schwer zu testen und zu definieren sind.

Man kann dies dennoch in **FastAPI** tun, in dem man eines der internen Tools von Starlette verwendet.

Und auch die Docs würden immer noch funktionieren, auch wenn keine zusätzliche Dokumentaiton für den beinhalteten Pfad innerhalb des Pfad-Parameters generiert wird.

### Pfadkonvertierer

Mithilfe einer Option direkt von Starlette können Sie einen *Pfad-Parameter*, der einen *Pfad* enthält, in einer URL deklarieren, wie zum Beispiel:

```
/files/{file_path:path}
```

In diesem Fall lautet der Name des *Parameters* `file_path`, und der letzte Teil `:path` gibt an, dass der Parameter mit einem beliebigen *Pfad* übereinstimmen sollte.

Damit können Sie es folgend verwenden:

```Python hl_lines="6"
{!../../../docs_src/path_params/tutorial004.py!}
```

!!! tip
    Möglicherweise sollte der Parameter `/home/johndoe/myfile.txt` und einen führenden Schrägstrich (`/`) enthalten.

    In solch einem Fall wäre die URL: `/files//home/johndoe/myfile.txt` mit einem doppelten Schrägstrich (`//`) zwischen `files` und `home`.

## Zusammenfassung

Indem Sie mit **FastAPI** kurze, intuitive und standardmäßige Python-Typdeklarationen verwenden, erhalten Sie:

* Editor-Unterstützung: Fehlerprüfungen, Autovervollständigung usw.
* Daten "<abbr title="Die Umwandlung der Zeichenfolge, die aus einer HTTP-Anfrage stammt, in Python-Daten">Parsing</abbr>"
* Datenvalidierung
* API-Annotationen und automatische Dokumentation

Und Sie müssen Sie nur einmal deklarieren.

Das ist vermutlich das Hauptaugenmerk von **FastAPI** im Vergleich zu alternativen Frameworks (mal abgesehen von der reinen Performance).
