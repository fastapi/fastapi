# Pfad-Parameter

Sie können Pfad-„Parameter“ oder -„Variablen“ mit der gleichen Syntax deklarieren, welche in Python-<abbr title="Format-String – Formatierter String: Der String enthält Variablen, die mit geschweiften Klammern umschlossen sind. Solche Stellen werden durch den Wert der Variable ersetzt">Format-Strings</abbr> verwendet wird:

```Python hl_lines="6-7"
{!../../../docs_src/path_params/tutorial001.py!}
```

Der Wert des Pfad-Parameters `item_id` wird Ihrer Funktion als das Argument `item_id` übergeben.

Wenn Sie dieses Beispiel ausführen und auf <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> gehen, sehen Sie als Response:

```JSON
{"item_id":"foo"}
```

## Pfad-Parameter mit Typen

Sie können den Typ eines Pfad-Parameters in der Argumentliste der Funktion deklarieren, mit Standard-Python-Typannotationen:

```Python hl_lines="7"
{!../../../docs_src/path_params/tutorial002.py!}
```

In diesem Fall wird `item_id` als `int` deklariert, also als Ganzzahl.

/// check

Dadurch erhalten Sie Editor-Unterstützung innerhalb Ihrer Funktion, mit Fehlerprüfungen, Codevervollständigung, usw.

///

## Daten-<abbr title="Auch bekannt als: Serialisierung, Parsen, Marshalling">Konversion</abbr>

Wenn Sie dieses Beispiel ausführen und Ihren Browser unter <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a> öffnen, sehen Sie als Response:

```JSON
{"item_id":3}
```

/// check

Beachten Sie, dass der Wert, den Ihre Funktion erhält und zurückgibt, die Zahl `3` ist, also ein `int`. Nicht der String `"3"`, also ein `str`.

Sprich, mit dieser Typdeklaration wird **FastAPI** die Anfrage automatisch <abbr title="Den String, der von einer HTTP Anfrage kommt, in Python-Objekte konvertieren">„parsen“</abbr>.

///

## Datenvalidierung

Wenn Sie aber im Browser <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> besuchen, erhalten Sie eine hübsche HTTP-Fehlermeldung:

```JSON
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo",
      "url": "https://errors.pydantic.dev/2.1/v/int_parsing"
    }
  ]
}
```

Der Pfad-Parameter `item_id` hatte den Wert `"foo"`, was kein `int` ist.

Die gleiche Fehlermeldung würde angezeigt werden, wenn Sie ein `float` (also eine Kommazahl) statt eines `int`s übergeben würden, wie etwa in: <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

/// check

Sprich, mit der gleichen Python-Typdeklaration gibt Ihnen **FastAPI** Datenvalidierung.

Beachten Sie, dass die Fehlermeldung auch direkt die Stelle anzeigt, wo die Validierung nicht erfolgreich war.

Das ist unglaublich hilfreich, wenn Sie Code entwickeln und debuggen, welcher mit ihrer API interagiert.

///

## Dokumentation

Wenn Sie die Seite <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> in Ihrem Browser öffnen, sehen Sie eine automatische, interaktive API-Dokumentation:

<img src="/img/tutorial/path-params/image01.png">

/// check

Wiederum, mit dieser gleichen Python-Typdeklaration gibt Ihnen **FastAPI** eine automatische, interaktive Dokumentation (verwendet die Swagger-Benutzeroberfläche).

Beachten Sie, dass der Pfad-Parameter dort als Ganzzahl deklariert ist.

///

## Nützliche Standards. Alternative Dokumentation

Und weil das generierte Schema vom <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a>-Standard kommt, gibt es viele kompatible Tools.

Zum Beispiel bietet **FastAPI** selbst eine alternative API-Dokumentation (verwendet ReDoc), welche Sie unter <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> einsehen können:

<img src="/img/tutorial/path-params/image02.png">

Und viele weitere kompatible Tools. Inklusive Codegenerierung für viele Sprachen.

## Pydantic

Die ganze Datenvalidierung wird hinter den Kulissen von <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> durchgeführt, Sie profitieren also von dessen Vorteilen. Und Sie wissen, dass Sie in guten Händen sind.

Sie können für Typ Deklarationen auch `str`, `float`, `bool` und viele andere komplexe Datentypen verwenden.

Mehrere davon werden wir in den nächsten Kapiteln erkunden.

## Die Reihenfolge ist wichtig

Wenn Sie *Pfadoperationen* erstellen, haben Sie manchmal einen fixen Pfad.

Etwa `/users/me`, um Daten über den aktuellen Benutzer zu erhalten.

Und Sie haben auch einen Pfad `/users/{user_id}`, um Daten über einen spezifischen Benutzer zu erhalten, mittels einer Benutzer-ID.

Weil *Pfadoperationen* in ihrer Reihenfolge ausgewertet werden, müssen Sie sicherstellen, dass der Pfad `/users/me` vor `/users/{user_id}` deklariert wurde:

```Python hl_lines="6  11"
{!../../../docs_src/path_params/tutorial003.py!}
```

Ansonsten würde der Pfad für `/users/{user_id}` auch `/users/me` auswerten, und annehmen, dass ein Parameter `user_id` mit dem Wert `"me"` übergeben wurde.

Sie können eine Pfadoperation auch nicht erneut definieren:

```Python hl_lines="6  11"
{!../../../docs_src/path_params/tutorial003b.py!}
```

Die erste Definition wird immer verwendet werden, da ihr Pfad zuerst übereinstimmt.

## Vordefinierte Parameterwerte

Wenn Sie eine *Pfadoperation* haben, welche einen *Pfad-Parameter* hat, aber Sie wollen, dass dessen gültige Werte vordefiniert sind, können Sie ein Standard-Python <abbr title="Enumeration, oder kurz Enum – Aufzählung">`Enum`</abbr> verwenden.

### Erstellen Sie eine `Enum`-Klasse

Importieren Sie `Enum` und erstellen Sie eine Unterklasse, die von `str` und `Enum` erbt.

Indem Sie von `str` erben, weiß die API Dokumentation, dass die Werte des Enums vom Typ `str` sein müssen, und wird in der Lage sein, korrekt zu rendern.

Erstellen Sie dann Klassen-Attribute mit festgelegten Werten, welches die erlaubten Werte sein werden:

```Python hl_lines="1  6-9"
{!../../../docs_src/path_params/tutorial005.py!}
```

/// info

<a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">Enumerationen (oder kurz Enums)</a> gibt es in Python seit Version 3.4.

///

/// tip | "Tipp"

Falls Sie sich fragen, was „AlexNet“, „ResNet“ und „LeNet“ ist, das sind Namen von <abbr title="Genau genommen, Deep-Learning-Modellarchitekturen">Modellen</abbr> für maschinelles Lernen.

///

### Deklarieren Sie einen *Pfad-Parameter*

Dann erstellen Sie einen *Pfad-Parameter*, der als Typ die gerade erstellte Enum-Klasse hat (`ModelName`):

```Python hl_lines="16"
{!../../../docs_src/path_params/tutorial005.py!}
```

### Testen Sie es in der API-Dokumentation

Weil die erlaubten Werte für den *Pfad-Parameter* nun vordefiniert sind, kann die interaktive Dokumentation sie als Auswahl-Drop-Down anzeigen:

<img src="/img/tutorial/path-params/image03.png">

### Mit Python-*<abbr title="Enumeration – Aufzählung">Enums</abbr>* arbeiten

Der *Pfad-Parameter* wird ein *<abbr title="Member – Mitglied: Einer der möglichen Werte einer Enumeration">Member</abbr> eines Enums* sein.

#### *Enum-Member* vergleichen

Sie können ihn mit einem Member Ihres Enums `ModelName` vergleichen:

```Python hl_lines="17"
{!../../../docs_src/path_params/tutorial005.py!}
```

#### *Enum-Wert* erhalten

Den tatsächlichen Wert (in diesem Fall ein `str`) erhalten Sie via `model_name.value`, oder generell, `ihr_enum_member.value`:

```Python hl_lines="20"
{!../../../docs_src/path_params/tutorial005.py!}
```

/// tip | "Tipp"

Sie können den Wert `"lenet"` außerdem mittels `ModelName.lenet.value` abrufen.

///

#### *Enum-Member* zurückgeben

Sie können *Enum-Member* in ihrer *Pfadoperation* zurückgeben, sogar verschachtelt in einem JSON-Body (z. B. als `dict`).

Diese werden zu ihren entsprechenden Werten konvertiert (in diesem Fall Strings), bevor sie zum Client übertragen werden:

```Python hl_lines="18  21  23"
{!../../../docs_src/path_params/tutorial005.py!}
```

In Ihrem Client erhalten Sie eine JSON-Response, wie etwa:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Pfad Parameter die Pfade enthalten

Angenommen, Sie haben eine *Pfadoperation* mit einem Pfad `/files/{file_path}`.

Aber `file_path` soll selbst einen *Pfad* enthalten, etwa `home/johndoe/myfile.txt`.

Sprich, die URL für diese Datei wäre etwas wie: `/files/home/johndoe/myfile.txt`.

### OpenAPI Unterstützung

OpenAPI bietet nicht die Möglichkeit, dass ein *Pfad-Parameter* seinerseits einen *Pfad* enthalten kann, das würde zu Szenarios führen, die schwierig zu testen und zu definieren sind.

Trotzdem können Sie das in **FastAPI** tun, indem Sie eines der internen Tools von Starlette verwenden.

Die Dokumentation würde weiterhin funktionieren, allerdings wird nicht dokumentiert werden, dass der Parameter ein Pfad sein sollte.

### Pfad Konverter

Mittels einer Option direkt von Starlette können Sie einen *Pfad-Parameter* deklarieren, der einen Pfad enthalten soll, indem Sie eine URL wie folgt definieren:

```
/files/{file_path:path}
```

In diesem Fall ist der Name des Parameters `file_path`. Der letzte Teil, `:path`, sagt aus, dass der Parameter ein *Pfad* sein soll.

Sie verwenden das also wie folgt:

```Python hl_lines="6"
{!../../../docs_src/path_params/tutorial004.py!}
```

/// tip | "Tipp"

Der Parameter könnte einen führenden Schrägstrich (`/`) haben, wie etwa in `/home/johndoe/myfile.txt`.

In dem Fall wäre die URL: `/files//home/johndoe/myfile.txt`, mit einem doppelten Schrägstrich (`//`) zwischen `files` und `home`.

///

## Zusammenfassung

In **FastAPI** erhalten Sie mittels kurzer, intuitiver Typdeklarationen:

* Editor-Unterstützung: Fehlerprüfungen, Codevervollständigung, usw.
* Daten "<abbr title="Den String, der von einer HTTP Anfrage kommt, nach Python-Daten konvertieren">parsen</abbr>"
* Datenvalidierung
* API-Annotationen und automatische Dokumentation

Und Sie müssen sie nur einmal deklarieren.

Das ist wahrscheinlich der sichtbarste Unterschied zwischen **FastAPI** und alternativen Frameworks (abgesehen von der reinen Performanz).
