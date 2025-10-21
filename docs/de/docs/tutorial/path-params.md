# Pfad-Parameter { #path-parameters }

Sie können Pfad-„Parameter“ oder -„Variablen“ mit der gleichen Syntax deklarieren, welche in Python-<abbr title="Formatstring – Formatierter String: Der String enthält Ausdrücke, die mit geschweiften Klammern umschlossen sind. Solche Stellen werden durch den Wert des Ausdrucks ersetzt">Formatstrings</abbr> verwendet wird:

{* ../../docs_src/path_params/tutorial001.py hl[6:7] *}

Der Wert des Pfad-Parameters `item_id` wird Ihrer Funktion als das Argument `item_id` übergeben.

Wenn Sie dieses Beispiel ausführen und auf <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> gehen, sehen Sie als <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>:

```JSON
{"item_id":"foo"}
```

## Pfad-Parameter mit Typen { #path-parameters-with-types }

Sie können den Typ eines Pfad-Parameters in der Argumentliste der Funktion deklarieren, mit Standard-Python-Typannotationen:

{* ../../docs_src/path_params/tutorial002.py hl[7] *}

In diesem Fall wird `item_id` als `int` deklariert, also als Ganzzahl.

/// check | Testen

Dadurch erhalten Sie Editor-Unterstützung innerhalb Ihrer Funktion, mit Fehlerprüfungen, Codevervollständigung, usw.

///

## Daten-<abbr title="Auch bekannt als: Serialisierung, Parsen, Marshalling">Konversion</abbr> { #data-conversion }

Wenn Sie dieses Beispiel ausführen und Ihren Browser unter <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a> öffnen, sehen Sie als Response:

```JSON
{"item_id":3}
```

/// check | Testen

Beachten Sie, dass der Wert, den Ihre Funktion erhält und zurückgibt, die Zahl `3` ist, also ein `int`. Nicht der String `"3"`, also ein `str`.

Sprich, mit dieser Typdeklaration wird **FastAPI** den <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> automatisch <abbr title="Den String, der von einem HTTP-Request kommt, in Python-Objekte konvertieren">„parsen“</abbr>.

///

## Datenvalidierung { #data-validation }

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
      "input": "foo"
    }
  ]
}
```

Der Pfad-Parameter `item_id` hatte den Wert `"foo"`, was kein `int` ist.

Die gleiche Fehlermeldung würde angezeigt werden, wenn Sie ein `float` (also eine Kommazahl) statt eines `int`s übergeben würden, wie etwa in: <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

/// check | Testen

Sprich, mit der gleichen Python-Typdeklaration gibt Ihnen **FastAPI** Datenvalidierung.

Beachten Sie, dass die Fehlermeldung auch direkt die Stelle anzeigt, wo die Validierung nicht erfolgreich war.

Das ist unglaublich hilfreich, wenn Sie Code entwickeln und debuggen, welcher mit Ihrer API interagiert.

///

## Dokumentation { #documentation }

Wenn Sie die Seite <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> in Ihrem Browser öffnen, sehen Sie eine automatische, interaktive API-Dokumentation:

<img src="/img/tutorial/path-params/image01.png">

/// check | Testen

Wiederum, mit dieser gleichen Python-Typdeklaration gibt Ihnen **FastAPI** eine automatische, interaktive Dokumentation (verwendet die Swagger-Benutzeroberfläche).

Beachten Sie, dass der Pfad-Parameter dort als Ganzzahl deklariert ist.

///

## Nützliche Standards, alternative Dokumentation { #standards-based-benefits-alternative-documentation }

Und weil das generierte Schema vom <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a>-Standard kommt, gibt es viele kompatible Tools.

Zum Beispiel bietet **FastAPI** selbst eine alternative API-Dokumentation (verwendet ReDoc), welche Sie unter <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> einsehen können:

<img src="/img/tutorial/path-params/image02.png">

Und viele weitere kompatible Tools. Inklusive Codegenerierung für viele Sprachen.

## Pydantic { #pydantic }

Die ganze Datenvalidierung wird hinter den Kulissen von <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> durchgeführt, Sie profitieren also von dessen Vorteilen. Und Sie wissen, dass Sie in guten Händen sind.

Sie können für Typdeklarationen auch `str`, `float`, `bool` und viele andere komplexe Datentypen verwenden.

Mehrere davon werden wir in den nächsten Kapiteln erkunden.

## Die Reihenfolge ist wichtig { #order-matters }

Wenn Sie *Pfadoperationen* erstellen, haben Sie manchmal einen fixen Pfad.

Etwa `/users/me`, um Daten über den aktuellen Benutzer zu erhalten.

Und Sie haben auch einen Pfad `/users/{user_id}`, um Daten über einen spezifischen Benutzer zu erhalten, mittels einer Benutzer-ID.

Weil *Pfadoperationen* in ihrer Reihenfolge ausgewertet werden, müssen Sie sicherstellen, dass der Pfad `/users/me` vor `/users/{user_id}` deklariert wurde:

{* ../../docs_src/path_params/tutorial003.py hl[6,11] *}

Ansonsten würde der Pfad für `/users/{user_id}` auch `/users/me` auswerten, und annehmen, dass ein Parameter `user_id` mit dem Wert `"me"` übergeben wurde.

Sie können eine Pfadoperation auch nicht erneut definieren:

{* ../../docs_src/path_params/tutorial003b.py hl[6,11] *}

Die erste Definition wird immer verwendet werden, da ihr Pfad zuerst übereinstimmt.

## Vordefinierte Parameterwerte { #predefined-values }

Wenn Sie eine *Pfadoperation* haben, welche einen *Pfad-Parameter* hat, aber Sie wollen, dass dessen gültige Werte vordefiniert sind, können Sie ein Standard-Python <abbr title="Enumeration">`Enum`</abbr> verwenden.

### Eine `Enum`-Klasse erstellen { #create-an-enum-class }

Importieren Sie `Enum` und erstellen Sie eine Unterklasse, die von `str` und `Enum` erbt.

Indem Sie von `str` erben, weiß die API-Dokumentation, dass die Werte vom Typ `str` sein müssen, und wird in der Lage sein, korrekt zu rendern.

Erstellen Sie dann Klassen-Attribute mit festgelegten Werten, welches die erlaubten Werte sein werden:

{* ../../docs_src/path_params/tutorial005.py hl[1,6:9] *}

/// info | Info

<a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">Enumerationen (oder Enums)</a> gibt es in Python seit Version 3.4.

///

/// tip | Tipp

Falls Sie sich fragen, was „AlexNet“, „ResNet“ und „LeNet“ ist, das sind Namen von <abbr title="Genau genommen, Deep-Learning-Modellarchitekturen">Modellen</abbr> für maschinelles Lernen.

///

### Einen *Pfad-Parameter* deklarieren { #declare-a-path-parameter }

Dann erstellen Sie einen *Pfad-Parameter*, der als Typ die gerade erstellte Enum-Klasse hat (`ModelName`):

{* ../../docs_src/path_params/tutorial005.py hl[16] *}

### Die API-Dokumentation testen { #check-the-docs }

Weil die erlaubten Werte für den *Pfad-Parameter* nun vordefiniert sind, kann die interaktive Dokumentation sie als Auswahl-Drop-Down anzeigen:

<img src="/img/tutorial/path-params/image03.png">

### Mit Python-*Enumerationen* arbeiten { #working-with-python-enumerations }

Der *Pfad-Parameter* wird ein *<abbr title="Member – Mitglied: Einer der möglichen Werte einer Enumeration">Member</abbr> einer Enumeration* sein.

#### *Enumeration-Member* vergleichen { #compare-enumeration-members }

Sie können ihn mit einem Member Ihrer Enumeration `ModelName` vergleichen:

{* ../../docs_src/path_params/tutorial005.py hl[17] *}

#### *Enumerations-Wert* erhalten { #get-the-enumeration-value }

Den tatsächlichen Wert (in diesem Fall ein `str`) erhalten Sie via `model_name.value`, oder generell, `your_enum_member.value`:

{* ../../docs_src/path_params/tutorial005.py hl[20] *}

/// tip | Tipp

Sie können den Wert `"lenet"` außerdem mittels `ModelName.lenet.value` abrufen.

///

#### *Enumeration-Member* zurückgeben { #return-enumeration-members }

Sie können *Enum-Member* in ihrer *Pfadoperation* zurückgeben, sogar verschachtelt in einem JSON-Body (z. B. als `dict`).

Diese werden zu ihren entsprechenden Werten konvertiert (in diesem Fall Strings), bevor sie zum Client übertragen werden:

{* ../../docs_src/path_params/tutorial005.py hl[18,21,23] *}

In Ihrem Client erhalten Sie eine JSON-Response, wie etwa:

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

OpenAPI bietet nicht die Möglichkeit, dass ein *Pfad-Parameter* seinerseits einen *Pfad* enthalten kann, das würde zu Szenarios führen, die schwierig zu testen und zu definieren sind.

Trotzdem können Sie das in **FastAPI** tun, indem Sie eines der internen Tools von Starlette verwenden.

Die Dokumentation würde weiterhin funktionieren, allerdings wird nicht dokumentiert werden, dass der Parameter ein Pfad sein sollte.

### Pfad-Konverter { #path-convertor }

Mittels einer Option direkt von Starlette können Sie einen *Pfad-Parameter* deklarieren, der einen Pfad enthalten soll, indem Sie eine URL wie folgt definieren:

```
/files/{file_path:path}
```

In diesem Fall ist der Name des Parameters `file_path`. Der letzte Teil, `:path`, sagt aus, dass der Parameter ein *Pfad* sein soll.

Sie verwenden das also wie folgt:

{* ../../docs_src/path_params/tutorial004.py hl[6] *}

/// tip | Tipp

Der Parameter könnte einen führenden Schrägstrich (`/`) haben, wie etwa in `/home/johndoe/myfile.txt`.

In dem Fall wäre die URL: `/files//home/johndoe/myfile.txt`, mit einem doppelten Schrägstrich (`//`) zwischen `files` und `home`.

///

## Zusammenfassung { #recap }

In **FastAPI** erhalten Sie mittels kurzer, intuitiver Typdeklarationen:

* Editor-Unterstützung: Fehlerprüfungen, Codevervollständigung, usw.
* Daten "<abbr title="Den String, der von einem HTTP-Request kommt, nach Python-Daten konvertieren">parsen</abbr>"
* Datenvalidierung
* API-Annotationen und automatische Dokumentation

Und Sie müssen sie nur einmal deklarieren.

Das ist wahrscheinlich der sichtbarste Unterschied zwischen **FastAPI** und alternativen Frameworks (abgesehen von der reinen Performanz).
