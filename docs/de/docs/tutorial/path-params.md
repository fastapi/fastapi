# Pfad-Parameter { #path-parameters }

Sie können Pfad-„Parameter“ oder -„Variablen“ mit der gleichen Syntax deklarieren, welche in Python-<abbr title="Formatstring – Formatierter String: Der String enthält Ausdrücke, die mit geschweiften Klammern umschlossen sind. Solche Stellen werden durch den Wert des Ausdrucks ersetzt">Formatstrings</abbr> verwendet wird:

{* ../../docs_src/path_params/tutorial001_py310.py hl[6:7] *}

Der Wert des Pfad-Parameters `item_id` wird Ihrer Funktion als das Argument `item_id` übergeben.

Wenn Sie also dieses Beispiel ausführen und auf [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo) gehen, sehen Sie als <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>:

```JSON
{"item_id":"foo"}
```

## Pfad-Parameter mit Typen { #path-parameters-with-types }

Sie können den Typ eines Pfad-Parameters in der Funktion deklarieren, mit Standard-Python-Typannotationen:

{* ../../docs_src/path_params/tutorial002_py310.py hl[7] *}

In diesem Fall wird `item_id` als `int` deklariert.

/// tip | Tipp

Dadurch erhalten Sie Editor-Unterstützung innerhalb Ihrer Funktion, mit Fehlerprüfungen, Codevervollständigung, usw.

///

## Daten-<dfn title="auch bekannt als: Serialisierung, Parsen, Marshalling">Konversion</dfn> { #data-conversion }

Wenn Sie dieses Beispiel ausführen und Ihren Browser unter [http://127.0.0.1:8000/items/3](http://127.0.0.1:8000/items/3) öffnen, sehen Sie als Response:

```JSON
{"item_id":3}
```

/// tip | Tipp

Beachten Sie, dass der Wert, den Ihre Funktion erhalten (und zurückgegeben) hat, `3` ist, als Python-`int`, nicht als String `"3"`.

Sprich, mit dieser Typdeklaration bietet **FastAPI** Ihnen automatisches Request-<dfn title="Den String, der von einem HTTP-Request kommt, in Python-Daten konvertieren">„Parsing“</dfn>.

///

## Datenvalidierung { #data-validation }

Wenn Sie aber im Browser [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo) besuchen, erhalten Sie eine hübsche HTTP-Fehlermeldung:

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
      "input": "foo"
    }
  ]
}
```

denn der Pfad-Parameter `item_id` hatte den Wert `"foo"`, was kein `int` ist.

Die gleiche Fehlermeldung würde angezeigt werden, wenn Sie ein `float` statt eines `int`s übergeben würden, wie etwa in: [http://127.0.0.1:8000/items/4.2](http://127.0.0.1:8000/items/4.2)

/// tip | Tipp

Sprich, mit der gleichen Python-Typdeklaration gibt Ihnen **FastAPI** Datenvalidierung.

Beachten Sie, dass die Fehlermeldung auch direkt die Stelle anzeigt, wo die Validierung nicht erfolgreich war.

Das ist unglaublich hilfreich, wenn Sie Code entwickeln und debuggen, welcher mit Ihrer API interagiert.

///

## Dokumentation { #documentation }

Und wenn Sie die Seite [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in Ihrem Browser öffnen, sehen Sie eine automatische, interaktive API-Dokumentation wie:

<img src="/img/tutorial/path-params/image01.png">

/// tip | Tipp

Wiederum, nur mit dieser gleichen Python-Typdeklaration gibt Ihnen **FastAPI** eine automatische, interaktive Dokumentation (integriert Swagger UI).

Beachten Sie, dass der Pfad-Parameter dort als Ganzzahl deklariert ist.

///

## Standardbasierte Vorteile, alternative Dokumentation { #standards-based-benefits-alternative-documentation }

Und weil das generierte Schema vom [OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md)-Standard kommt, gibt es viele kompatible Tools.

Aus diesem Grund bietet **FastAPI** selbst eine alternative API-Dokumentation (verwendet ReDoc), welche Sie unter [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) einsehen können:

<img src="/img/tutorial/path-params/image02.png">

Auf die gleiche Weise gibt es viele kompatible Tools. Inklusive Codegenerierungstools für viele Sprachen.

## Pydantic { #pydantic }

Die ganze Datenvalidierung wird hinter den Kulissen von [Pydantic](https://pydantic.dev/docs/) durchgeführt, Sie profitieren also von dessen Vorteilen. Und Sie wissen, dass Sie in guten Händen sind.

Sie können die gleichen Typdeklarationen auch mit `str`, `float`, `bool` und vielen anderen komplexen Datentypen verwenden.

Mehrere davon werden in den nächsten Kapiteln des Tutorials erkundet.

## Die Reihenfolge ist wichtig { #order-matters }

Wenn Sie *Pfadoperationen* erstellen, haben Sie manchmal Situationen, in denen Sie einen fixen Pfad haben.

Etwa `/users/me`, sagen wir, um Daten über den aktuellen Benutzer zu erhalten.

Und Sie können auch einen Pfad `/users/{user_id}` haben, um Daten über einen spezifischen Benutzer mittels irgendeiner Benutzer-ID zu erhalten.

Weil *Pfadoperationen* in ihrer Reihenfolge ausgewertet werden, müssen Sie sicherstellen, dass der Pfad für `/users/me` vor dem für `/users/{user_id}` deklariert wurde:

{* ../../docs_src/path_params/tutorial003_py310.py hl[6,11] *}

Ansonsten würde der Pfad für `/users/{user_id}` auch auf `/users/me` passen und „denken“, dass er einen Parameter `user_id` mit dem Wert `"me"` erhält.

Ebenso können Sie eine Pfadoperation nicht erneut definieren:

{* ../../docs_src/path_params/tutorial003b_py310.py hl[6,11] *}

Die erste Definition wird immer verwendet werden, da ihr Pfad zuerst übereinstimmt.

## Vordefinierte Werte { #predefined-values }

Wenn Sie eine *Pfadoperation* haben, welche einen *Pfad-Parameter* erhält, aber Sie wollen, dass die möglichen gültigen *Pfad-Parameter*-Werte vordefiniert sind, können Sie ein Standard-Python-<abbr title="Enumeration">`Enum`</abbr> verwenden.

### Eine `Enum`-Klasse erstellen { #create-an-enum-class }

Importieren Sie `Enum` und erstellen Sie eine Unterklasse, die von `str` und `Enum` erbt.

Indem Sie von `str` erben, weiß die API-Dokumentation, dass die Werte vom Typ `string` sein müssen, und wird in der Lage sein, korrekt zu rendern.

Erstellen Sie dann Klassen-Attribute mit festgelegten Werten, welche die verfügbaren gültigen Werte sein werden:

{* ../../docs_src/path_params/tutorial005_py310.py hl[1,6:9] *}

/// tip | Tipp

Falls Sie sich fragen: „AlexNet“, „ResNet“ und „LeNet“ sind nur Namen von <dfn title="Genauer gesagt: Deep-Learning-Modellarchitekturen">Modellen</dfn> für maschinelles Lernen.

///

### Einen *Pfad-Parameter* deklarieren { #declare-a-path-parameter }

Dann erstellen Sie einen *Pfad-Parameter* mit einer Typannotation, welche die von Ihnen erstellte Enum-Klasse (`ModelName`) verwendet:

{* ../../docs_src/path_params/tutorial005_py310.py hl[16] *}

### Die Dokumentation testen { #check-the-docs }

Weil die verfügbaren Werte für den *Pfad-Parameter* nun vordefiniert sind, kann die interaktive Dokumentation diese hübsch anzeigen:

<img src="/img/tutorial/path-params/image03.png">

### Mit Python-*Enumerationen* arbeiten { #working-with-python-enumerations }

Der Wert des *Pfad-Parameters* wird ein *<abbr title="Member – Mitglied: Einer der möglichen Werte einer Enumeration">Member</abbr> einer Enumeration* sein.

#### *Enumeration-Member* vergleichen { #compare-enumeration-members }

Sie können ihn mit dem *Enumeration-Member* in Ihrem erstellten Enum `ModelName` vergleichen:

{* ../../docs_src/path_params/tutorial005_py310.py hl[17] *}

#### *Enumerations-Wert* erhalten { #get-the-enumeration-value }

Den tatsächlichen Wert (in diesem Fall ein `str`) erhalten Sie mittels `model_name.value`, oder generell, `your_enum_member.value`:

{* ../../docs_src/path_params/tutorial005_py310.py hl[20] *}

/// tip | Tipp

Sie können den Wert `"lenet"` außerdem mittels `ModelName.lenet.value` abrufen.

///

#### *Enumeration-Member* zurückgeben { #return-enumeration-members }

Sie können *Enum-Member* von Ihrer *Pfadoperation* zurückgeben, sogar verschachtelt in einem JSON-Body (z. B. als `dict`).

Diese werden zu ihren entsprechenden Werten konvertiert (in diesem Fall Strings), bevor sie an den Client zurückgegeben werden:

{* ../../docs_src/path_params/tutorial005_py310.py hl[18,21,23] *}

In Ihrem Client erhalten Sie eine JSON-Response wie:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Pfad-Parameter, die Pfade enthalten { #path-parameters-containing-paths }

Angenommen, Sie haben eine *Pfadoperation* mit einem Pfad `/files/{file_path}`.

Aber `file_path` soll selbst einen *Pfad* enthalten, etwa `home/johndoe/myfile.txt`.

Sprich, die URL für diese Datei wäre etwas wie: `/files/home/johndoe/myfile.txt`.

### OpenAPI-Unterstützung { #openapi-support }

OpenAPI bietet nicht die Möglichkeit, zu deklarieren, dass ein *Pfad-Parameter* in sich einen *Pfad* enthalten kann, da das zu Szenarios führen könnte, die schwierig zu testen und zu definieren sind.

Trotzdem können Sie das in **FastAPI** tun, indem Sie eines der internen Tools von Starlette verwenden.

Die Dokumentation würde weiterhin funktionieren, allerdings ohne irgendeine Dokumentation hinzuzufügen, die besagt, dass der Parameter einen Pfad enthalten sollte.

### Pfad-Konverter { #path-convertor }

Mittels einer Option direkt von Starlette können Sie einen *Pfad-Parameter* deklarieren, der einen *Pfad* enthält, indem Sie eine URL wie folgt definieren:

```
/files/{file_path:path}
```

In diesem Fall ist der Name des Parameters `file_path`, und der letzte Teil, `:path`, sagt ihm, dass der Parameter mit jedem *Pfad* übereinstimmen sollte.

Sie verwenden das also wie folgt:

{* ../../docs_src/path_params/tutorial004_py310.py hl[6] *}

/// tip | Tipp

Der Parameter könnte `/home/johndoe/myfile.txt` enthalten müssen, mit einem führenden Schrägstrich (`/`).

In dem Fall wäre die URL: `/files//home/johndoe/myfile.txt`, mit einem doppelten Schrägstrich (`//`) zwischen `files` und `home`.

///

## Zusammenfassung { #recap }

Mit **FastAPI** erhalten Sie mittels kurzer, intuitiver und Standard-Python-Typdeklarationen:

* Editor-Unterstützung: Fehlerprüfungen, Codevervollständigung, usw.
* Daten „<dfn title="Den String, der von einem HTTP-Request kommt, in Python-Daten konvertieren">parsen</dfn>“
* Datenvalidierung
* API-Annotation und automatische Dokumentation

Und Sie müssen sie nur einmal deklarieren.

Das ist wahrscheinlich der wichtigste sichtbare Vorteil von **FastAPI** im Vergleich zu alternativen Frameworks (abgesehen von der rohen Performanz).
