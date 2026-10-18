# Responsemodell – Rückgabetyp { #response-model-return-type }

Sie können den Typ der <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> deklarieren, indem Sie den **Rückgabetyp** der *Pfadoperation-Funktion* annotieren.

Hierbei können Sie **Typannotationen** genauso verwenden, wie Sie es bei Eingabedaten in Funktions-**Parametern** machen; verwenden Sie Pydantic-Modelle, Listen, Dictionaries und skalare Werte wie Integer, Booleans, usw.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

FastAPI wird diesen Rückgabetyp verwenden, um:

* Die zurückzugebenden Daten zu **validieren**.
    * Wenn die Daten ungültig sind (Sie haben z. B. ein Feld vergessen), bedeutet das, *Ihr* Anwendungscode ist fehlerhaft, er gibt nicht zurück, was er sollte, und daher wird ein <abbr title="Server-Fehler">Server-Error</abbr> ausgegeben, statt falscher Daten. So können Sie und Ihre Clients sicher sein, dass diese die erwarteten Daten, in der richtigen Form erhalten.
* In der OpenAPI *Pfadoperation* ein **JSON-Schema** für die Response hinzuzufügen.
    * Dieses wird von der **automatischen Dokumentation** verwendet.
    * Es wird auch von automatisch Client-Code-generierenden Tools verwendet.
* Die zurückgegebenen Daten mit Pydantic zu **serialisieren** (zu JSON). Pydantic ist in **Rust** geschrieben und daher **viel schneller**.

Aber am wichtigsten:

* Es wird die Ausgabedaten auf das **limitieren und filtern**, was im Rückgabetyp definiert ist.
    * Das ist insbesondere für die **Sicherheit** wichtig, mehr dazu unten.

## `response_model`-Parameter { #response-model-parameter }

Es gibt Fälle, da möchten oder müssen Sie Daten zurückgeben, die nicht genau dem entsprechen, was der Typ deklariert.

Zum Beispiel könnten Sie **ein Dictionary zurückgeben** wollen, oder ein Datenbankobjekt, aber **es als Pydantic-Modell deklarieren**. Auf diese Weise übernimmt das Pydantic-Modell alle Datendokumentation, -validierung, usw. für das Objekt, welches Sie zurückgeben (z. B. ein Dictionary oder ein Datenbankobjekt).

Würden Sie eine Rückgabetyp-Annotation hinzufügen, dann würden Tools und Editoren (korrekterweise) Fehler ausgeben, die Ihnen sagen, dass Ihre Funktion einen Typ zurückgibt (z. B. ein Dict), der sich unterscheidet von dem, was Sie deklariert haben (z. B. ein Pydantic-Modell).

In solchen Fällen können Sie statt des Rückgabetyps den **Pfadoperation-Dekorator**-Parameter `response_model` verwenden.

Sie können `response_model` in jeder möglichen *Pfadoperation* verwenden:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* usw.

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | Hinweis

Beachten Sie, dass `response_model` ein Parameter der „Dekorator“-Methode ist (`get`, `post`, usw.). Nicht Ihrer *Pfadoperation-Funktion*, so wie alle Parameter und der Body.

///

`response_model` nimmt denselben Typ entgegen, den Sie auch für ein Pydantic-Modellfeld deklarieren würden, also etwa ein Pydantic-Modell, aber es kann auch z. B. eine `list` von Pydantic-Modellen sein, wie etwa `List[Item]`.

FastAPI wird dieses `response_model` nehmen, um die Daten zu dokumentieren, validieren, usw. und auch, um **die Ausgabedaten** entsprechend der Typdeklaration **zu konvertieren und filtern**.

/// tip | Tipp

Wenn Sie in Ihrem Editor strikte Typchecks haben, mypy, usw., können Sie den Funktions-Rückgabetyp als `Any` deklarieren.

So sagen Sie dem Editor, dass Sie absichtlich *irgendetwas* zurückgeben. Aber FastAPI wird trotzdem die Dokumentation, Validierung, Filterung, usw. der Daten übernehmen, via `response_model`.

///

### `response_model`-Priorität { #response-model-priority }

Wenn sowohl Rückgabetyp als auch `response_model` deklariert sind, hat `response_model` die Priorität und wird von FastAPI verwendet.

So können Sie korrekte Typannotationen zu Ihren Funktionen hinzufügen, selbst wenn Sie einen anderen Typ als das Responsemodell zurückgeben, die von Ihrem Editor und Tools wie mypy verwendet werden. Und dennoch übernimmt FastAPI die Validierung und Dokumentation, usw., der Daten anhand von `response_model`.

Sie können auch `response_model=None` verwenden, um das Erstellen eines Responsemodells für diese *Pfadoperation* zu unterbinden. Sie könnten das tun müssen, wenn Sie Typannotationen für Dinge hinzufügen, die keine gültigen Pydantic-Felder sind. Ein Beispiel dazu werden Sie in einem der Abschnitte unten sehen.

## Dieselben Eingabedaten zurückgeben { #return-the-same-input-data }

Im Folgenden deklarieren wir ein `UserIn`-Modell; es enthält ein Klartext-Passwort:

{* ../../docs_src/response_model/tutorial002_py310.py hl[7,9] *}

/// note | Hinweis

Um `EmailStr` zu verwenden, installieren Sie zuerst [`email-validator`](https://github.com/JoshData/python-email-validator).

Fügen Sie es Ihrem Projekt hinzu:

```console
$ uv add email-validator
```

oder mit:

```console
$ uv add "pydantic[email]"
```

///

Wir verwenden dieses Modell, um sowohl unsere Eingabe- als auch Ausgabedaten zu deklarieren:

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

Immer wenn jetzt ein Browser einen Benutzer mit Passwort erzeugt, gibt die API dasselbe Passwort in der Response zurück.

Hier ist das möglicherweise kein Problem, da es derselbe Benutzer ist, der das Passwort sendet.

Aber wenn wir dasselbe Modell für eine andere *Pfadoperation* verwenden, könnten wir die Passwörter unserer Benutzer an jeden Client senden.

/// danger | Gefahr

Speichern Sie niemals das Klartext-Passwort eines Benutzers, oder versenden Sie es in einer Response wie dieser, es sei denn, Sie kennen alle Einschränkungen und wissen, was Sie tun.

///

## Ausgabemodell hinzufügen { #add-an-output-model }

Wir können stattdessen ein Eingabemodell mit dem Klartext-Passwort, und ein Ausgabemodell ohne das Passwort erstellen:

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

Obwohl unsere *Pfadoperation-Funktion* hier denselben `user` von der Eingabe zurückgibt, der das Passwort enthält:

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

... haben wir deklariert, dass `response_model` unser Modell `UserOut` ist, welches das Passwort nicht enthält:

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

Darum wird **FastAPI** sich darum kümmern, dass alle Daten, die nicht im Ausgabemodell deklariert sind, herausgefiltert werden (mittels Pydantic).

### `response_model` oder Rückgabetyp { #response-model-or-return-type }

Da unsere zwei Modelle in diesem Fall unterschiedlich sind, würde, wenn wir den Funktions-Rückgabetyp als `UserOut` deklarieren, der Editor sich beschweren, dass wir einen ungültigen Typ zurückgeben, weil das unterschiedliche Klassen sind.

Darum müssen wir es in diesem Beispiel im `response_model`-Parameter deklarieren.

... aber lesen Sie weiter, um zu sehen, wie man das anders lösen kann.

## Rückgabetyp und Datenfilterung { #return-type-and-data-filtering }

Führen wir unser vorheriges Beispiel fort. Wir wollten **die Funktion mit einem Typ annotieren**, aber wir wollten in der Funktion tatsächlich etwas zurückgeben, das **mehr Daten** enthält.

Wir möchten, dass FastAPI die Daten weiterhin mithilfe des Responsemodells **filtert**. Selbst wenn die Funktion mehr Daten zurückgibt, soll die Response nur die Felder enthalten, die im Responsemodell deklariert sind.

Im vorherigen Beispiel mussten wir den `response_model`-Parameter verwenden, weil die Klassen unterschiedlich waren. Das bedeutet aber auch, wir bekommen keine Unterstützung vom Editor und anderen Tools, die den Funktions-Rückgabetyp überprüfen.

Aber in den meisten Fällen, wenn wir so etwas machen, wollen wir nur, dass das Modell einige der Daten **filtert/entfernt**, so wie in diesem Beispiel.

Und in solchen Fällen können wir Klassen und Vererbung verwenden, um Vorteil aus den **Typannotationen** in der Funktion zu ziehen, was vom Editor und von Tools besser unterstützt wird, während wir gleichzeitig FastAPIs **Datenfilterung** behalten.

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

Damit erhalten wir Tool-Unterstützung, vom Editor und mypy, da dieser Code hinsichtlich der Typen korrekt ist, aber wir erhalten auch die Datenfilterung von FastAPI.

Wie funktioniert das? Schauen wir uns das mal an. 🤓

### Typannotationen und Tooling { #type-annotations-and-tooling }

Sehen wir uns zunächst an, wie Editor, mypy und andere Tools dies sehen würden.

`BaseUser` verfügt über die Basis-Felder. Dann erbt `UserIn` von `BaseUser` und fügt das Feld `password` hinzu, sodass es nun alle Felder beider Modelle hat.

Wir annotieren den Funktionsrückgabetyp als `BaseUser`, geben aber tatsächlich eine `UserIn`-Instanz zurück.

Der Editor, mypy und andere Tools werden sich darüber nicht beschweren, weil `UserIn` im Sinne des Typings eine Unterklasse von `BaseUser` ist. Das bedeutet, es ist ein *gültiger* Typ, wenn etwas erwartet wird, das ein `BaseUser` ist.

### FastAPI Datenfilterung { #fastapi-data-filtering }

FastAPI seinerseits wird den Rückgabetyp sehen und sicherstellen, dass das, was zurückgegeben wird, **nur** diejenigen Felder enthält, welche im Typ deklariert sind.

FastAPI macht intern mehrere Dinge mit Pydantic, um sicherzustellen, dass obige Ähnlichkeitsregeln der Klassenvererbung nicht auf die Filterung der zurückgegebenen Daten angewendet werden, sonst könnten Sie am Ende mehr Daten zurückgeben als gewollt.

Auf diese Weise erhalten Sie das beste beider Welten: Sowohl Typannotationen mit **Tool-Unterstützung** als auch **Datenfilterung**.

## Anzeige in der Dokumentation { #see-it-in-the-docs }

Wenn Sie sich die automatische Dokumentation betrachten, können Sie sehen, dass Eingabe- und Ausgabemodell beide ihr eigenes JSON-Schema haben:

<img src="/img/tutorial/response-model/image01.png">

Und beide Modelle werden auch in der interaktiven API-Dokumentation verwendet:

<img src="/img/tutorial/response-model/image02.png">

## Andere Rückgabetyp-Annotationen { #other-return-type-annotations }

Es kann Fälle geben, bei denen Sie etwas zurückgeben, das kein gültiges Pydantic-Feld ist, und Sie annotieren es in der Funktion nur, um Unterstützung von Tools zu erhalten (Editor, mypy, usw.).

### Eine Response direkt zurückgeben { #return-a-response-directly }

Der häufigste Anwendungsfall ist, wenn Sie [eine Response direkt zurückgeben, wie es später in der Dokumentation für fortgeschrittene Benutzer erläutert wird](../advanced/response-directly.md).

{* ../../docs_src/response_model/tutorial003_02_py310.py hl[8,10:11] *}

Dieser einfache Anwendungsfall wird automatisch von FastAPI gehandhabt, weil die Annotation des Rückgabetyps die Klasse (oder eine Unterklasse von) `Response` ist.

Und Tools werden auch glücklich sein, weil sowohl `RedirectResponse` als auch `JSONResponse` Unterklassen von `Response` sind, die Typannotation ist daher korrekt.

### Eine Unterklasse von Response annotieren { #annotate-a-response-subclass }

Sie können auch eine Unterklasse von `Response` in der Typannotation verwenden:

{* ../../docs_src/response_model/tutorial003_03_py310.py hl[8:9] *}

Das wird ebenfalls funktionieren, weil `RedirectResponse` eine Unterklasse von `Response` ist, und FastAPI sich um diesen einfachen Anwendungsfall automatisch kümmert.

### Ungültige Rückgabetyp-Annotationen { #invalid-return-type-annotations }

Aber wenn Sie ein beliebiges anderes Objekt zurückgeben, das kein gültiger Pydantic-Typ ist (z. B. ein Datenbankobjekt), und Sie annotieren es so in der Funktion, wird FastAPI versuchen, ein Pydantic-Responsemodell von dieser Typannotation zu erstellen, und scheitern.

Das gleiche wird passieren, wenn Sie eine <dfn title="Eine Union zwischen mehreren Typen bedeutet: „irgendeiner dieser Typen“.">Union</dfn> mehrerer Typen haben, und einer oder mehrere sind nicht gültige Pydantic-Typen. Zum Beispiel funktioniert folgendes nicht 💥:

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

... das scheitert, da die Typannotation kein Pydantic-Typ ist, und auch keine einzelne `Response`-Klasse, oder -Unterklasse, es ist eine Union (eines von beiden) von `Response` und `dict`.

### Responsemodell deaktivieren { #disable-response-model }

Beim Beispiel oben fortsetzend, mögen Sie vielleicht die standardmäßige Datenvalidierung, -Dokumentation, -Filterung, usw., die von FastAPI durchgeführt wird, nicht haben.

Aber Sie möchten dennoch den Rückgabetyp in der Funktion annotieren, um Unterstützung von Editoren und Typcheckern (z. B. mypy) zu erhalten.

In diesem Fall können Sie die Generierung des Responsemodells abschalten, indem Sie `response_model=None` setzen:

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

Das bewirkt, dass FastAPI die Generierung des Responsemodells unterlässt, und damit können Sie jede gewünschte Rückgabetyp-Annotation haben, ohne dass es Ihre FastAPI-Anwendung beeinflusst. 🤓

## Parameter für die Enkodierung des Responsemodells { #response-model-encoding-parameters }

Ihr Responsemodell könnte Defaultwerte haben, wie:

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None` (oder `str | None = None` in Python 3.10) hat einen Defaultwert `None`.
* `tax: float = 10.5` hat einen Defaultwert `10.5`.
* `tags: List[str] = []` hat eine leere Liste als Defaultwert: `[]`.

Aber Sie möchten diese vielleicht vom Resultat ausschließen, wenn sie tatsächlich nicht gespeichert wurden.

Wenn Sie zum Beispiel Modelle mit vielen optionalen Attributen in einer NoSQL-Datenbank haben, und Sie möchten nicht ellenlange JSON-Responses voller Defaultwerte senden.

### Den `response_model_exclude_unset`-Parameter verwenden { #use-the-response-model-exclude-unset-parameter }

Sie können den *Pfadoperation-Dekorator*-Parameter `response_model_exclude_unset=True` setzen:

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

Die Defaultwerte werden dann nicht in der Response enthalten sein, sondern nur die tatsächlich gesetzten Werte.

Wenn Sie also einen Request an diese *Pfadoperation* für den Artikel mit der ID `foo` senden, wird (ohne die Defaultwerte) die Response sein:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// note | Hinweis

Sie können auch:

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

verwenden, wie in der [Pydantic-Dokumentation](https://pydantic.dev/docs/validation/latest/concepts/serialization/#excluding-and-including-fields-based-on-their-value) für `exclude_defaults` und `exclude_none` beschrieben.

///

#### Daten mit Werten für Felder mit Defaultwerten { #data-with-values-for-fields-with-defaults }

Aber wenn Ihre Daten Werte für die Felder des Modells mit Defaultwerten haben, wie etwa der Artikel mit der ID `bar`:

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

dann werden diese Werte in der Response enthalten sein.

#### Daten mit den gleichen Werten wie die Defaultwerte { #data-with-the-same-values-as-the-defaults }

Wenn Daten die gleichen Werte haben wie ihre Defaultwerte, wie etwa der Artikel mit der ID `baz`:

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

dann ist FastAPI klug genug (tatsächlich ist Pydantic klug genug) zu erkennen, dass, obwohl `description`, `tax`, und `tags` die gleichen Werte haben wie ihre Defaultwerte, sie explizit gesetzt wurden (statt dass sie von den Defaultwerten genommen wurden).

Diese Felder werden also in der JSON-Response enthalten sein.

/// tip | Tipp

Beachten Sie, dass Defaultwerte alles Mögliche sein können, nicht nur `None`.

Sie können eine Liste (`[]`), ein `float` `10.5`, usw. sein.

///

### `response_model_include` und `response_model_exclude` { #response-model-include-and-response-model-exclude }

Sie können auch die Parameter `response_model_include` und `response_model_exclude` im **Pfadoperation-Dekorator** verwenden.

Diese nehmen ein `set` von `str`s entgegen, welches Namen von Attributen sind, die eingeschlossen (ohne die Anderen) oder ausgeschlossen (nur die Anderen) werden sollen.

Das kann als schnelle Abkürzung verwendet werden, wenn Sie nur ein Pydantic-Modell haben und ein paar Daten von der Ausgabe ausschließen wollen.

/// tip | Tipp

Es wird dennoch empfohlen, dass Sie die Ideen von oben verwenden, also mehrere Klassen statt dieser Parameter.

Der Grund ist, dass das das generierte JSON-Schema in der OpenAPI Ihrer Anwendung (und deren Dokumentation) dennoch das komplette Modell abbildet, selbst wenn Sie `response_model_include` oder `response_model_exclude` verwenden, um einige Attribute auszuschließen.

Das trifft auch auf `response_model_by_alias` zu, welches ähnlich funktioniert.

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | Tipp

Die Syntax `{"name", "description"}` erzeugt ein `set` mit diesen zwei Werten.

Äquivalent zu `set(["name", "description"])`.

///

#### `list`s statt `set`s verwenden { #using-lists-instead-of-sets }

Wenn Sie vergessen, ein `set` zu verwenden, und stattdessen eine `list` oder ein `tuple` übergeben, wird FastAPI die dennoch in ein `set` konvertieren, und es wird korrekt funktionieren:

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## Zusammenfassung { #recap }

Verwenden Sie den Parameter `response_model` im *Pfadoperation-Dekorator*, um Responsemodelle zu definieren, und besonders, um sicherzustellen, dass private Daten herausgefiltert werden.

Verwenden Sie `response_model_exclude_unset`, um nur explizit gesetzte Werte zurückzugeben.
