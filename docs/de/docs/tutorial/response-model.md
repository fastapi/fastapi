# Responsemodell – Rückgabetyp

Sie können den Typ der <abbr title="Response – Antwort: Daten, die zum anfragenden Client zurückgeschickt werden">Response</abbr> deklarieren, indem Sie den **Rückgabetyp** der *Pfadoperation* annotieren.

Hierbei können Sie **Typannotationen** genauso verwenden, wie Sie es bei Werten von Funktions-**Parametern** machen; verwenden Sie Pydantic-Modelle, Listen, Dicts und skalare Werte wie Nummern, Booleans, usw.

=== "Python 3.10+"

    ```Python hl_lines="16  21"
    {!> ../../../docs_src/response_model/tutorial001_01_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="18  23"
    {!> ../../../docs_src/response_model/tutorial001_01_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="18  23"
    {!> ../../../docs_src/response_model/tutorial001_01.py!}
    ```

FastAPI wird diesen Rückgabetyp verwenden, um:

* Die zurückzugebenden Daten zu **validieren**.
    * Wenn die Daten ungültig sind (Sie haben z. B. ein Feld vergessen), bedeutet das, *Ihr* Anwendungscode ist fehlerhaft, er gibt nicht zurück, was er sollte, und daher wird ein <abbr title="Server-Fehler">Server-Error</abbr> ausgegeben, statt falscher Daten. So können Sie und ihre Clients sicher sein, dass diese die erwarteten Daten, in der richtigen Form erhalten.
* In der OpenAPI *Pfadoperation* ein **JSON-Schema** für die Response hinzuzufügen.
    * Dieses wird von der **automatischen Dokumentation** verwendet.
    * Es wird auch von automatisch Client-Code-generierenden Tools verwendet.

Aber am wichtigsten:

* Es wird die Ausgabedaten auf das **limitieren und filtern**, was im Rückgabetyp definiert ist.
    * Das ist insbesondere für die **Sicherheit** wichtig, mehr dazu unten.

## `response_model`-Parameter

Es gibt Fälle, da möchten oder müssen Sie Daten zurückgeben, die nicht genau dem entsprechen, was der Typ deklariert.

Zum Beispiel könnten Sie **ein Dict zurückgeben** wollen, oder ein Datenbank-Objekt, aber **es als Pydantic-Modell deklarieren**. Auf diese Weise übernimmt das Pydantic-Modell alle Datendokumentation, -validierung, usw. für das Objekt, welches Sie zurückgeben (z. B. ein Dict oder ein Datenbank-Objekt).

Würden Sie eine hierfür eine Rückgabetyp-Annotation verwenden, dann würden Tools und Editoren (korrekterweise) Fehler ausgeben, die Ihnen sagen, dass Ihre Funktion einen Typ zurückgibt (z. B. ein Dict), der sich unterscheidet von dem, was Sie deklariert haben (z. B. ein Pydantic-Modell).

In solchen Fällen können Sie statt des Rückgabetyps den **Pfadoperation-Dekorator**-Parameter `response_model` verwenden.

Sie können `response_model` in jeder möglichen *Pfadoperation* verwenden:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* usw.

=== "Python 3.10+"

    ```Python hl_lines="17  22  24-27"
    {!> ../../../docs_src/response_model/tutorial001_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="17  22  24-27"
    {!> ../../../docs_src/response_model/tutorial001_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="17  22  24-27"
    {!> ../../../docs_src/response_model/tutorial001.py!}
    ```

!!! note "Hinweis"
    Beachten Sie, dass `response_model` ein Parameter der „Dekorator“-Methode ist (`get`, `post`, usw.). Nicht der *Pfadoperation-Funktion*, so wie die anderen Parameter.

`response_model` nimmt denselben Typ entgegen, den Sie auch für ein Pydantic-Modellfeld deklarieren würden, also etwa ein Pydantic-Modell, aber es kann auch z. B. eine `list`e von Pydantic-Modellen sein, wie etwa `List[Item]`.

FastAPI wird dieses `response_model` nehmen, um die Daten zu dokumentieren, validieren, usw. und auch, um **die Ausgabedaten** entsprechend der Typdeklaration **zu konvertieren und filtern**.

!!! tip "Tipp"
    Wenn Sie in Ihrem Editor strikte Typchecks haben, mypy, usw., können Sie den Funktions-Rückgabetyp als <abbr title='„Irgend etwas“'>`Any`</abbr> deklarieren.

    So sagen Sie dem Editor, dass Sie absichtlich *irgendetwas* zurückgeben. Aber FastAPI wird trotzdem die Dokumentation, Validierung, Filterung, usw. der Daten übernehmen, via `response_model`.

### `response_model`-Priorität

Wenn sowohl Rückgabetyp als auch `response_model` deklariert sind, hat `response_model` die Priorität und wird von FastAPI bevorzugt verwendet.

So können Sie korrekte Typannotationen zu ihrer Funktion hinzufügen, die von ihrem Editor und Tools wie mypy verwendet werden. Und dennoch übernimmt FastAPI die Validierung und Dokumentation, usw., der Daten anhand von `response_model`.

Sie können auch `response_model=None` verwenden, um das Erstellen eines Responsemodells für diese *Pfadoperation* zu unterbinden. Sie könnten das tun wollen, wenn sie Dinge annotieren, die nicht gültige Pydantic-Felder sind. Ein Beispiel dazu werden Sie in einer der Abschnitte unten sehen.

## Dieselben Eingabedaten zurückgeben

Im Folgenden deklarieren wir ein `UserIn`-Modell; es enthält ein Klartext-Passwort:

=== "Python 3.10+"

    ```Python hl_lines="7  9"
    {!> ../../../docs_src/response_model/tutorial002_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9  11"
    {!> ../../../docs_src/response_model/tutorial002.py!}
    ```

!!! info
    Um `EmailStr` zu verwenden, installieren Sie zuerst <a href="https://github.com/JoshData/python-email-validator" class="external-link" target="_blank">`email_validator`</a>.

    Z. B. `pip install email-validator`
    oder `pip install pydantic[email]`.

Wir verwenden dieses Modell, um sowohl unsere Eingabe- als auch Ausgabedaten zu deklarieren:

=== "Python 3.10+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/response_model/tutorial002_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="18"
    {!> ../../../docs_src/response_model/tutorial002.py!}
    ```

Immer wenn jetzt ein Browser einen Benutzer mit Passwort erzeugt, gibt die API dasselbe Passwort in der Response zurück.

Hier ist das möglicherweise kein Problem, da es derselbe Benutzer ist, der das Passwort sendet.

Aber wenn wir dasselbe Modell für eine andere *Pfadoperation* verwenden, könnten wir das Passwort dieses Benutzers zu jedem Client schicken.

!!! danger "Gefahr"
    Speichern Sie niemals das Klartext-Passwort eines Benutzers, oder versenden Sie es in einer Response wie dieser, wenn Sie sich nicht der resultierenden Gefahren bewusst sind und nicht wissen, was Sie tun.

## Ausgabemodell hinzufügen

Wir können stattdessen ein Eingabemodell mit dem Klartext-Passwort, und ein Ausgabemodell ohne das Passwort erstellen:

=== "Python 3.10+"

    ```Python hl_lines="9  11  16"
    {!> ../../../docs_src/response_model/tutorial003_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9  11  16"
    {!> ../../../docs_src/response_model/tutorial003.py!}
    ```

Obwohl unsere *Pfadoperation-Funktion* hier denselben `user` von der Eingabe zurückgibt, der das Passwort enthält:

=== "Python 3.10+"

    ```Python hl_lines="24"
    {!> ../../../docs_src/response_model/tutorial003_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="24"
    {!> ../../../docs_src/response_model/tutorial003.py!}
    ```

... haben wir deklariert, dass `response_model` das Modell `UserOut` ist, welches das Passwort nicht enthält:

=== "Python 3.10+"

    ```Python hl_lines="22"
    {!> ../../../docs_src/response_model/tutorial003_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="22"
    {!> ../../../docs_src/response_model/tutorial003.py!}
    ```

Darum wird **FastAPI** sich darum kümmern, dass alle Daten, die nicht im Ausgabemodell deklariert sind, herausgefiltert werden (mittels Pydantic).

### `response_model` oder Rückgabewert

Da unsere zwei Modelle in diesem Fall unterschiedlich sind, würde, wenn wir den Rückgabewert der Funktion als `UserOut` deklarieren, der Editor sich beschweren, dass wir einen ungültigen Typ zurückgeben, weil das unterschiedliche Klassen sind.

Darum müssen wir es in diesem Fall im `response_model`-Parameter deklarieren.

... aber lesen Sie weiter, um zu sehen, wie man das anders lösen kann.

## Rückgabewert und Datenfilterung

Führen wir unser vorheriges Beispiel fort. Wir wollten **die Funktion mit einem Typ annotieren**, aber etwas zurückgeben, das **weniger Daten** enthält.

Wir möchten auch, dass FastAPI die Daten weiterhin, dem Responsemodell entsprechend, **filtert**.

Im vorherigen Beispiel mussten wir den `response_model`-Parameter verwenden, weil die Klassen unterschiedlich waren. Das bedeutet aber auch, wir bekommen keine Unterstützung vom Editor und anderen Tools, die den Funktions-Rückgabewert überprüfen.

Aber in den meisten Fällen, wenn wir so etwas machen, wollen wir nur, dass das Modell einige der Daten **filtert/entfernt**, so wie in diesem Beispiel.

Und in solchen Fällen können wir Klassen und Vererbung verwenden, um Vorteil aus den Typannotationen in der Funktion zu ziehen, was vom Editor und von Tools besser unterstützt wird, während wir gleichzeitig FastAPIs **Datenfilterung** behalten.

=== "Python 3.10+"

    ```Python hl_lines="7-10  13-14  18"
    {!> ../../../docs_src/response_model/tutorial003_01_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9-13  15-16  20"
    {!> ../../../docs_src/response_model/tutorial003_01.py!}
    ```

Damit erhalten wir Tool-Unterstützung, vom Editor und mypy, da dieser Code hinsichtlich der Typen korrekt ist, aber wir erhalten auch die Datenfilterung von FastAPI.

Wie funktioniert das? Schauen wir uns das mal an. 🤓

### Typannotationen und Tooling

Sehen wir uns zunächst an, wie Editor, mypy und andere Tools dies sehen würden.

`BaseUser` verfügt über die Basis-Felder. Dann erbt `UserIn` von `BaseUser` und fügt das Feld `Passwort` hinzu, sodass dass es nun alle Felder beider Modelle hat.

Wir annotieren den Funktionsrückgabetyp als `BaseUser`, geben aber tatsächlich eine `UserIn`-Instanz zurück.

Für den Editor, mypy und andere Tools ist das kein Problem, da `UserIn` eine Unterklasse von `BaseUser` ist (Salopp: `UserIn` ist ein `BaseUser`). Es handelt sich um einen *gültigen* Typ, solange irgendetwas überreicht wird, das ein `BaseUser` ist.

### FastAPI Datenfilterung

FastAPI seinerseits wird den Rückgabetyp sehen und sicherstellen, dass das, was zurückgegeben wird, **nur** diejenigen Felder enthält, welche im Typ deklariert sind.

FastAPI macht intern mehrere Dinge mit Pydantic, um sicherzustellen, dass obige Ähnlichkeitsregeln der Klassenvererbung nicht auf die Filterung der zurückgegebenen Daten angewendet werden, sonst könnten Sie am Ende mehr Daten zurückgeben als gewollt.

Auf diese Weise erhalten Sie das beste beider Welten: Sowohl Typannotationen mit **Tool-Unterstützung** als auch **Datenfilterung**.

## Anzeige in der Dokumentation

Wenn Sie sich die automatische Dokumentation betrachten, können Sie sehen, dass Eingabe- und Ausgabemodell beide ihr eigenes JSON-Schema haben:

<img src="/img/tutorial/response-model/image01.png">

Und beide Modelle werden auch in der interaktiven API-Dokumentation verwendet:

<img src="/img/tutorial/response-model/image02.png">

## Andere Rückgabetyp-Annotationen

Es kann Fälle geben, bei denen Sie etwas zurückgeben, das kein gültiges Pydantic-Feld ist, und Sie annotieren es in der Funktion nur, um Unterstützung von Tools zu erhalten (Editor, mypy, usw.).

### Eine Response direkt zurückgeben

Der häufigste Anwendungsfall ist, wenn Sie [eine Response direkt zurückgeben, wie es später im Handbuch für fortgeschrittene Benutzer erläutert wird](../advanced/response-directly.md){.internal-link target=_blank}.

```Python hl_lines="8  10-11"
{!> ../../../docs_src/response_model/tutorial003_02.py!}
```

Dieser einfache Anwendungsfall wird automatisch von FastAPI gehandhabt, weil die Annotation des Rückgabetyps die Klasse (oder eine Unterklasse von) `Response` ist.

Und Tools werden auch glücklich sein, weil sowohl `RedirectResponse` als auch `JSONResponse` Unterklassen von `Response` sind, die Typannotation ist daher korrekt.

### Eine Unterklasse von Response annotieren

Sie können auch eine Unterklasse von `Response` in der Typannotation verwenden.

```Python hl_lines="8-9"
{!> ../../../docs_src/response_model/tutorial003_03.py!}
```

Das wird ebenfalls funktionieren, weil `RedirectResponse` eine Unterklasse von `Response` ist, und FastAPI sich um diesen einfachen Anwendungsfall automatisch kümmert.

### Ungültige Rückgabetyp-Annotationen

Aber wenn Sie ein beliebiges anderes Objekt zurückgeben, das kein gültiger Pydantic-Typ ist (z. B. ein Datenbank-Objekt), und Sie annotieren es so in der Funktion, wird FastAPI versuchen, ein Pydantic-Responsemodell von dieser Typannotation zu erstellen, und scheitern.

Das gleiche wird passieren, wenn Sie eine <abbr title='Eine Union mehrerer Typen bedeutet: „Irgendeiner dieser Typen“'>Union</abbr> mehrerer Typen haben, und einer oder mehrere sind nicht gültige Pydantic-Typen. Zum Beispiel funktioniert folgendes nicht 💥:

=== "Python 3.10+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/response_model/tutorial003_04_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/response_model/tutorial003_04.py!}
    ```

... das scheitert, da die Typannotation kein Pydantic-Typ ist, und auch keine einzelne `Response`-Klasse, oder -Unterklasse, es ist eine Union (eines von beiden) von `Response` und `dict`.

### Responsemodell deaktivieren

Beim Beispiel oben fortsetzend, mögen Sie vielleicht die standardmäßige Datenvalidierung, -Dokumentation, -Filterung, usw., die von FastAPI durchgeführt wird, nicht haben.

Aber Sie möchten dennoch den Rückgabetyp in der Funktion annotieren, um Unterstützung von Editoren und Typcheckern (z. B. mypy) zu erhalten.

In diesem Fall können Sie die Generierung des Responsemodells abschalten, indem Sie `response_model=None` setzen:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/response_model/tutorial003_05_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/response_model/tutorial003_05.py!}
    ```

Das bewirkt, dass FastAPI die Generierung des Responsemodells unterlässt, und damit können Sie jede gewünschte Rückgabetyp-Annotation haben, ohne dass es Ihre FastAPI-Anwendung beeinflusst. 🤓

## Parameter für die Enkodierung des Responsemodells

Ihr Responsemodell könnte Defaultwerte haben, wie:

=== "Python 3.10+"

    ```Python hl_lines="9  11-12"
    {!> ../../../docs_src/response_model/tutorial004_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="11  13-14"
    {!> ../../../docs_src/response_model/tutorial004_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="11  13-14"
    {!> ../../../docs_src/response_model/tutorial004.py!}
    ```

* `description: Union[str, None] = None` (oder `str | None = None` in Python 3.10) hat einen Defaultwert `None`.
* `tax: float = 10.5` hat einen Defaultwert `10.5`.
* `tags: List[str] = []` hat eine leere Liste als Defaultwert: `[]`.

Aber Sie möchten diese vielleicht vom Resultat ausschließen, wenn Sie gar nicht gesetzt wurden.

Wenn Sie zum Beispiel Modelle mit vielen optionalen Attributen in einer NoSQL-Datenbank haben, und Sie möchten nicht ellenlange JSON-Responses voller Defaultwerte senden.

### Den `response_model_exclude_unset`-Parameter verwenden

Sie können den *Pfadoperation-Dekorator*-Parameter `response_model_exclude_unset=True` setzen:

=== "Python 3.10+"

    ```Python hl_lines="22"
    {!> ../../../docs_src/response_model/tutorial004_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="24"
    {!> ../../../docs_src/response_model/tutorial004_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="24"
    {!> ../../../docs_src/response_model/tutorial004.py!}
    ```

Die Defaultwerte werden dann nicht in der Response enthalten sein, sondern nur die tatsächlich gesetzten Werte.

Wenn Sie also den Artikel mit der ID `foo` bei der *Pfadoperation* anfragen, wird (ohne die Defaultwerte) die Response sein:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

!!! info
    In Pydantic v1 hieß diese Methode `.dict()`, in Pydantic v2 wurde sie deprecated (aber immer noch unterstützt) und in `.model_dump()` umbenannt.

    Die Beispiele hier verwenden `.dict()` für die Kompatibilität mit Pydantic v1, Sie sollten jedoch stattdessen `.model_dump()` verwenden, wenn Sie Pydantic v2 verwenden können.

!!! info
    FastAPI verwendet `.dict()` von Pydantic Modellen, <a href="https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict" class="external-link" target="_blank">mit dessen `exclude_unset`-Parameter</a>, um das zu erreichen.

!!! info
    Sie können auch:

    * `response_model_exclude_defaults=True`
    * `response_model_exclude_none=True`

    verwenden, wie in der <a href="https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict" class="external-link" target="_blank">Pydantic Dokumentation</a> für `exclude_defaults` und `exclude_none` beschrieben.

#### Daten mit Werten für Felder mit Defaultwerten

Aber wenn ihre Daten Werte für Modellfelder mit Defaultwerten haben, wie etwa der Artikel mit der ID `bar`:

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

dann werden diese Werte in der Response enthalten sein.

#### Daten mit den gleichen Werten wie die Defaultwerte

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

!!! tip "Tipp"
    Beachten Sie, dass Defaultwerte alles Mögliche sein können, nicht nur `None`.

    Sie können eine Liste (`[]`), ein `float` `10.5`, usw. sein.

### `response_model_include` und `response_model_exclude`

Sie können auch die Parameter `response_model_include` und `response_model_exclude` im **Pfadoperation-Dekorator** verwenden.

Diese nehmen ein `set` von `str`s entgegen, welches Namen von Attributen sind, die eingeschlossen (ohne die Anderen) oder ausgeschlossen (nur die Anderen) werden sollen.

Das kann als schnelle Abkürzung verwendet werden, wenn Sie nur ein Pydantic-Modell haben und ein paar Daten von der Ausgabe ausschließen wollen.

!!! tip "Tipp"
    Es wird dennoch empfohlen, dass Sie die Ideen von oben verwenden, also mehrere Klassen statt dieser Parameter.

    Der Grund ist, dass das das generierte JSON-Schema in der OpenAPI ihrer Anwendung (und deren Dokumentation) dennoch das komplette Modell abbildet, selbst wenn Sie `response_model_include` oder `response_model_exclude` verwenden, um einige Attribute auszuschließen.

    Das trifft auch auf `response_model_by_alias` zu, welches ähnlich funktioniert.

=== "Python 3.10+"

    ```Python hl_lines="29  35"
    {!> ../../../docs_src/response_model/tutorial005_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="31  37"
    {!> ../../../docs_src/response_model/tutorial005.py!}
    ```

!!! tip "Tipp"
    Die Syntax `{"name", "description"}` erzeugt ein `set` mit diesen zwei Werten.

    Äquivalent zu `set(["name", "description"])`.

#### `list`en statt `set`s verwenden

Wenn Sie vergessen, ein `set` zu verwenden, und stattdessen eine `list`e oder ein `tuple` übergeben, wird FastAPI die dennoch in ein `set` konvertieren, und es wird korrekt funktionieren:

=== "Python 3.10+"

    ```Python hl_lines="29  35"
    {!> ../../../docs_src/response_model/tutorial006_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="31  37"
    {!> ../../../docs_src/response_model/tutorial006.py!}
    ```

## Zusammenfassung

Verwenden Sie den Parameter `response_model` im *Pfadoperation-Dekorator*, um Responsemodelle zu definieren, und besonders, um private Daten herauszufiltern.

Verwenden Sie `response_model_exclude_unset`, um nur explizit gesetzte Werte zurückzugeben.
