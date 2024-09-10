# Query-Parameter und Stringvalidierung

**FastAPI** erlaubt es Ihnen, Ihre Parameter zusätzlich zu validieren, und zusätzliche Informationen hinzuzufügen.

Nehmen wir als Beispiel die folgende Anwendung:

//// tab | Python 3.10+

```Python hl_lines="7"
{!> ../../../docs_src/query_params_str_validations/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial001.py!}
```

////

Der Query-Parameter `q` hat den Typ `Union[str, None]` (oder `str | None` in Python 3.10), was bedeutet, er ist entweder ein `str` oder `None`. Der Defaultwert ist `None`, also weiß FastAPI, der Parameter ist nicht erforderlich.

/// note | "Hinweis"

FastAPI weiß nur dank des definierten Defaultwertes `=None`, dass der Wert von `q` nicht erforderlich ist

`Union[str, None]` hingegen erlaubt ihren Editor, Sie besser zu unterstützen und Fehler zu erkennen.

///

## Zusätzliche Validierung

Wir werden bewirken, dass, obwohl `q` optional ist, wenn es gegeben ist, **seine Länge 50 Zeichen nicht überschreitet**.

### `Query` und `Annotated` importieren

Importieren Sie zuerst:

* `Query` von `fastapi`
* `Annotated` von `typing` (oder von `typing_extensions` in Python unter 3.9)

//// tab | Python 3.10+

In Python 3.9 oder darüber, ist `Annotated` Teil der Standardbibliothek, also können Sie es von `typing` importieren.

```Python hl_lines="1  3"
{!> ../../../docs_src/query_params_str_validations/tutorial002_an_py310.py!}
```

////

//// tab | Python 3.8+

In Versionen unter Python 3.9 importieren Sie `Annotated` von `typing_extensions`.

Es wird bereits mit FastAPI installiert sein.

```Python hl_lines="3-4"
{!> ../../../docs_src/query_params_str_validations/tutorial002_an.py!}
```

////

/// info

FastAPI unterstützt (und empfiehlt die Verwendung von) `Annotated` seit Version 0.95.0.

Wenn Sie eine ältere Version haben, werden Sie Fehler angezeigt bekommen, wenn Sie versuchen, `Annotated` zu verwenden.

Bitte [aktualisieren Sie FastAPI](../deployment/versions.md#upgrade-der-fastapi-versionen){.internal-link target=_blank} daher mindestens zu Version 0.95.1, bevor Sie `Annotated` verwenden.

///

## `Annotated` im Typ des `q`-Parameters verwenden

Erinnern Sie sich, wie ich in [Einführung in Python-Typen](../python-types.md#typhinweise-mit-metadaten-annotationen){.internal-link target=_blank} sagte, dass Sie mittels `Annotated` Metadaten zu Ihren Parametern hinzufügen können?

Jetzt ist es an der Zeit, das mit FastAPI auszuprobieren. 🚀

Wir hatten diese Typannotation:

//// tab | Python 3.10+

```Python
q: str | None = None
```

////

//// tab | Python 3.8+

```Python
q: Union[str, None] = None
```

////

Wir wrappen das nun in `Annotated`, sodass daraus wird:

//// tab | Python 3.10+

```Python
q: Annotated[str | None] = None
```

////

//// tab | Python 3.8+

```Python
q: Annotated[Union[str, None]] = None
```

////

Beide Versionen bedeuten dasselbe: `q` ist ein Parameter, der `str` oder `None` sein kann. Standardmäßig ist er `None`.

Wenden wir uns jetzt den spannenden Dingen zu. 🎉

## `Query` zu `Annotated` im `q`-Parameter hinzufügen

Jetzt, da wir `Annotated` für unsere Metadaten deklariert haben, fügen Sie `Query` hinzu, und setzen Sie den Parameter `max_length` auf `50`:

//// tab | Python 3.10+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial002_an_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial002_an.py!}
```

////

Beachten Sie, dass der Defaultwert immer noch `None` ist, sodass der Parameter immer noch optional ist.

Aber jetzt, mit `Query(max_length=50)` innerhalb von `Annotated`, sagen wir FastAPI, dass es diesen Wert aus den Query-Parametern extrahieren soll (das hätte es sowieso gemacht 🤷) und dass wir eine **zusätzliche Validierung** für diesen Wert haben wollen (darum machen wir das, um die zusätzliche Validierung zu bekommen). 😎

FastAPI wird nun:

* Die Daten **validieren** und sicherstellen, dass sie nicht länger als 50 Zeichen sind
* Dem Client einen **verständlichen Fehler** anzeigen, wenn die Daten ungültig sind
* Den Parameter in der OpenAPI-Schema-*Pfadoperation* **dokumentieren** (sodass er in der **automatischen Dokumentation** angezeigt wird)

## Alternativ (alt): `Query` als Defaultwert

Frühere Versionen von FastAPI (vor <abbr title="vor 2023-03">0.95.0</abbr>) benötigten `Query` als Defaultwert des Parameters, statt es innerhalb von `Annotated` unterzubringen. Die Chance ist groß, dass Sie Quellcode sehen, der das immer noch so macht, darum erkläre ich es Ihnen.

/// tip | "Tipp"

Verwenden Sie für neuen Code, und wann immer möglich, `Annotated`, wie oben erklärt. Es gibt mehrere Vorteile (unten erläutert) und keine Nachteile. 🍰

///

So würden Sie `Query()` als Defaultwert Ihres Funktionsparameters verwenden, den Parameter `max_length` auf 50 gesetzt:

//// tab | Python 3.10+

```Python hl_lines="7"
{!> ../../../docs_src/query_params_str_validations/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial002.py!}
```

////

Da wir in diesem Fall (ohne die Verwendung von `Annotated`) den Parameter-Defaultwert `None` mit `Query()` ersetzen, müssen wir nun dessen Defaultwert mit dem Parameter `Query(default=None)` deklarieren. Das dient demselben Zweck, `None` als Defaultwert für den Funktionsparameter zu setzen (zumindest für FastAPI).

Sprich:

```Python
q: Union[str, None] = Query(default=None)
```

... macht den Parameter optional, mit dem Defaultwert `None`, genauso wie:

```Python
q: Union[str, None] = None
```

Und in Python 3.10 und darüber macht:

```Python
q: str | None = Query(default=None)
```

... den Parameter optional, mit dem Defaultwert `None`, genauso wie:

```Python
q: str | None = None
```

Nur, dass die `Query`-Versionen den Parameter explizit als Query-Parameter deklarieren.

/// info

Bedenken Sie, dass:

```Python
= None
```

oder:

```Python
= Query(default=None)
```

der wichtigste Teil ist, um einen Parameter optional zu machen, da dieses `None` der Defaultwert ist, und das ist es, was diesen Parameter **nicht erforderlich** macht.

Der Teil mit `Union[str, None]` erlaubt es Ihrem Editor, Sie besser zu unterstützen, aber er sagt FastAPI nicht, dass dieser Parameter optional ist.

///

Jetzt können wir `Query` weitere Parameter übergeben. Fangen wir mit dem `max_length` Parameter an, der auf Strings angewendet wird:

```Python
q: Union[str, None] = Query(default=None, max_length=50)
```

Das wird die Daten validieren, einen verständlichen Fehler ausgeben, wenn die Daten nicht gültig sind, und den Parameter in der OpenAPI-Schema-*Pfadoperation* dokumentieren.

### `Query` als Defaultwert oder in `Annotated`

Bedenken Sie, dass wenn Sie `Query` innerhalb von `Annotated` benutzen, Sie den `default`-Parameter für `Query` nicht verwenden dürfen.

Setzen Sie stattdessen den Defaultwert des Funktionsparameters, sonst wäre es inkonsistent.

Zum Beispiel ist das nicht erlaubt:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

... denn es wird nicht klar, ob der Defaultwert `"rick"` oder `"morty"` sein soll.

Sie würden also (bevorzugt) schreiben:

```Python
q: Annotated[str, Query()] = "rick"
```

In älterem Code werden Sie auch finden:

```Python
q: str = Query(default="rick")
```

### Vorzüge von `Annotated`

**Es wird empfohlen, `Annotated` zu verwenden**, statt des Defaultwertes im Funktionsparameter, das ist aus mehreren Gründen **besser**: 🤓

Der **Default**wert des **Funktionsparameters** ist der **tatsächliche Default**wert, das spielt generell intuitiver mit Python zusammen. 😌

Sie können die Funktion ohne FastAPI an **anderen Stellen aufrufen**, und es wird **wie erwartet funktionieren**. Wenn es einen **erforderlichen** Parameter gibt (ohne Defaultwert), und Sie führen die Funktion ohne den benötigten Parameter aus, dann wird Ihr **Editor** Sie das mit einem Fehler wissen lassen, und **Python** wird sich auch beschweren.

Wenn Sie aber nicht `Annotated` benutzen und stattdessen die **(alte) Variante mit einem Defaultwert**, dann müssen Sie, wenn Sie die Funktion ohne FastAPI an **anderen Stellen** aufrufen, sich daran **erinnern**, die Argumente der Funktion zu übergeben, damit es richtig funktioniert. Ansonsten erhalten Sie unerwartete Werte (z. B. `QueryInfo` oder etwas Ähnliches, statt `str`). Ihr Editor kann ihnen nicht helfen, und Python wird die Funktion ohne Beschwerden ausführen, es sei denn, die Operationen innerhalb lösen einen Fehler aus.

Da `Annotated` mehrere Metadaten haben kann, können Sie dieselbe Funktion auch mit anderen Tools verwenden, wie etwa <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a>. 🚀

## Mehr Validierungen hinzufügen

Sie können auch einen Parameter `min_length` hinzufügen:

//// tab | Python 3.10+

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial003_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial003_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11"
{!> ../../../docs_src/query_params_str_validations/tutorial003_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/query_params_str_validations/tutorial003_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial003.py!}
```

////

## Reguläre Ausdrücke hinzufügen

Sie können einen <abbr title="Ein regulärer Ausdruck, auch regex oder regexp genannt, ist eine Zeichensequenz, die ein Suchmuster für Strings definiert.">Regulären Ausdruck</abbr> `pattern` definieren, mit dem der Parameter übereinstimmen muss:

//// tab | Python 3.10+

```Python hl_lines="11"
{!> ../../../docs_src/query_params_str_validations/tutorial004_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="11"
{!> ../../../docs_src/query_params_str_validations/tutorial004_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="12"
{!> ../../../docs_src/query_params_str_validations/tutorial004_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial004_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="11"
{!> ../../../docs_src/query_params_str_validations/tutorial004.py!}
```

////

Dieses bestimmte reguläre Suchmuster prüft, ob der erhaltene Parameter-Wert:

* `^`: mit den nachfolgenden Zeichen startet, keine Zeichen davor hat.
* `fixedquery`: den exakten Text `fixedquery` hat.
* `$`: danach endet, keine weiteren Zeichen hat als `fixedquery`.

Wenn Sie sich verloren fühlen bei all diesen **„Regulärer Ausdruck“**-Konzepten, keine Sorge. Reguläre Ausdrücke sind für viele Menschen ein schwieriges Thema. Sie können auch ohne reguläre Ausdrücke eine ganze Menge machen.

Aber wenn Sie sie brauchen und sie lernen, wissen Sie, dass Sie sie bereits direkt in **FastAPI** verwenden können.

### Pydantic v1 `regex` statt `pattern`

Vor Pydantic Version 2 und vor FastAPI Version 0.100.0, war der Name des Parameters `regex` statt `pattern`, aber das ist jetzt <abbr title="deprecated – obsolet, veraltet: Es soll nicht mehr verwendet werden">deprecated</abbr>.

Sie könnten immer noch Code sehen, der den alten Namen verwendet:

//// tab | Python 3.10+ Pydantic v1

```Python hl_lines="11"
{!> ../../../docs_src/query_params_str_validations/tutorial004_an_py310_regex.py!}
```

////

Beachten Sie aber, dass das deprecated ist, und zum neuen Namen `pattern` geändert werden sollte. 🤓

## Defaultwerte

Sie können natürlich andere Defaultwerte als `None` verwenden.

Beispielsweise könnten Sie den `q` Query-Parameter so deklarieren, dass er eine `min_length` von `3` hat, und den Defaultwert `"fixedquery"`:

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial005_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8"
{!> ../../../docs_src/query_params_str_validations/tutorial005_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/query_params_str_validations/tutorial005.py!}
```

////

/// note | "Hinweis"

Ein Parameter ist optional (nicht erforderlich), wenn er irgendeinen Defaultwert, auch `None`, hat.

///

## Erforderliche Parameter

Wenn wir keine Validierungen oder Metadaten haben, können wir den `q` Query-Parameter erforderlich machen, indem wir einfach keinen Defaultwert deklarieren, wie in:

```Python
q: str
```

statt:

```Python
q: Union[str, None] = None
```

Aber jetzt deklarieren wir den Parameter mit `Query`, wie in:

//// tab | Annotiert

```Python
q: Annotated[Union[str, None], Query(min_length=3)] = None
```

////

//// tab | Nicht annotiert

```Python
q: Union[str, None] = Query(default=None, min_length=3)
```

////

Wenn Sie einen Parameter erforderlich machen wollen, während Sie `Query` verwenden, deklarieren Sie ebenfalls einfach keinen Defaultwert:

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial006_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8"
{!> ../../../docs_src/query_params_str_validations/tutorial006_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/query_params_str_validations/tutorial006.py!}
```

/// tip | "Tipp"

Beachten Sie, dass, obwohl in diesem Fall `Query()` der Funktionsparameter-Defaultwert ist, wir nicht `default=None` zu `Query()` hinzufügen.

Verwenden Sie bitte trotzdem die `Annotated`-Version. 😉

///

////

### Erforderlich mit Ellipse (`...`)

Es gibt eine Alternative, die explizit deklariert, dass ein Wert erforderlich ist. Sie können als Default das <abbr title='Zeichenfolge, die einen Wert direkt darstellt, etwa 1, "hallowelt", True, None'>Literal</abbr> `...` setzen:

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial006b_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8"
{!> ../../../docs_src/query_params_str_validations/tutorial006b_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/query_params_str_validations/tutorial006b.py!}
```

////

/// info

Falls Sie das `...` bisher noch nicht gesehen haben: Es ist ein spezieller einzelner Wert, <a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">Teil von Python und wird „Ellipsis“ genannt</a> (Deutsch: Ellipse).

Es wird von Pydantic und FastAPI verwendet, um explizit zu deklarieren, dass ein Wert erforderlich ist.

///

Dies wird **FastAPI** wissen lassen, dass dieser Parameter erforderlich ist.

### Erforderlich, kann `None` sein

Sie können deklarieren, dass ein Parameter `None` akzeptiert, aber dennoch erforderlich ist. Das zwingt Clients, den Wert zu senden, selbst wenn er `None` ist.

Um das zu machen, deklarieren Sie, dass `None` ein gültiger Typ ist, aber verwenden Sie dennoch `...` als Default:

//// tab | Python 3.10+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial006c_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial006c_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial006c_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/query_params_str_validations/tutorial006c_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial006c.py!}
```

////

/// tip | "Tipp"

Pydantic, welches die gesamte Datenvalidierung und Serialisierung in FastAPI antreibt, hat ein spezielles Verhalten, wenn Sie `Optional` oder `Union[Something, None]` ohne Defaultwert verwenden, Sie können mehr darüber in der Pydantic-Dokumentation unter <a href="https://docs.pydantic.dev/2.3/usage/models/#required-fields" class="external-link" target="_blank">Required fields</a> erfahren.

///

/// tip | "Tipp"

Denken Sie daran, dass Sie in den meisten Fällen, wenn etwas erforderlich ist, einfach den Defaultwert weglassen können. Sie müssen also normalerweise `...` nicht verwenden.

///

## Query-Parameter-Liste / Mehrere Werte

Wenn Sie einen Query-Parameter explizit mit `Query` auszeichnen, können Sie ihn auch eine Liste von Werten empfangen lassen, oder anders gesagt, mehrere Werte.

Um zum Beispiel einen Query-Parameter `q` zu deklarieren, der mehrere Male in der URL vorkommen kann, schreiben Sie:

//// tab | Python 3.10+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial011_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial011_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial011_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/query_params_str_validations/tutorial011_py310.py!}
```

////

//// tab | Python 3.9+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial011_py39.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial011.py!}
```

////

Dann, mit einer URL wie:

```
http://localhost:8000/items/?q=foo&q=bar
```

bekommen Sie alle `q`-*Query-Parameter*-Werte (`foo` und `bar`) in einer Python-Liste – `list` – in ihrer *Pfadoperation-Funktion*, im Funktionsparameter `q`, überreicht.

Die Response für diese URL wäre also:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | "Tipp"

Um einen Query-Parameter vom Typ `list` zu deklarieren, wie im Beispiel oben, müssen Sie explizit `Query` verwenden, sonst würde der Parameter als Requestbody interpretiert werden.

///

Die interaktive API-Dokumentation wird entsprechend aktualisiert und erlaubt jetzt mehrere Werte.

<img src="/img/tutorial/query-params-str-validations/image02.png">

### Query-Parameter-Liste / Mehrere Werte mit Defaults

Und Sie können auch eine Default-`list`e von Werten definieren, wenn keine übergeben werden:

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial012_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial012_an.py!}
```

////

//// tab | Python 3.9+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/query_params_str_validations/tutorial012_py39.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial012.py!}
```

////

Wenn Sie auf:

```
http://localhost:8000/items/
```

gehen, wird der Default für `q` verwendet: `["foo", "bar"]`, und als Response erhalten Sie:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### `list` alleine verwenden

Sie können auch `list` direkt verwenden, anstelle von `List[str]` (oder `list[str]` in Python 3.9+):

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial013_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8"
{!> ../../../docs_src/query_params_str_validations/tutorial013_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/query_params_str_validations/tutorial013.py!}
```

////

/// note | "Hinweis"

Beachten Sie, dass FastAPI in diesem Fall den Inhalt der Liste nicht überprüft.

Zum Beispiel würde `List[int]` überprüfen (und dokumentieren) dass die Liste Ganzzahlen enthält. `list` alleine macht das nicht.

///

## Deklarieren von mehr Metadaten

Sie können mehr Informationen zum Parameter hinzufügen.

Diese Informationen werden zur generierten OpenAPI hinzugefügt, und von den Dokumentations-Oberflächen und von externen Tools verwendet.

/// note | "Hinweis"

Beachten Sie, dass verschiedene Tools OpenAPI möglicherweise unterschiedlich gut unterstützen.

Einige könnten noch nicht alle zusätzlichen Informationen anzeigen, die Sie deklariert haben, obwohl in den meisten Fällen geplant ist, das fehlende Feature zu implementieren.

///

Sie können einen Titel hinzufügen – `title`:

//// tab | Python 3.10+

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial007_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial007_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11"
{!> ../../../docs_src/query_params_str_validations/tutorial007_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="8"
{!> ../../../docs_src/query_params_str_validations/tutorial007_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial007.py!}
```

////

Und eine Beschreibung – `description`:

//// tab | Python 3.10+

```Python hl_lines="14"
{!> ../../../docs_src/query_params_str_validations/tutorial008_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="14"
{!> ../../../docs_src/query_params_str_validations/tutorial008_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="15"
{!> ../../../docs_src/query_params_str_validations/tutorial008_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="11"
{!> ../../../docs_src/query_params_str_validations/tutorial008_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="13"
{!> ../../../docs_src/query_params_str_validations/tutorial008.py!}
```

////

## Alias-Parameter

Stellen Sie sich vor, der Parameter soll `item-query` sein.

Wie in:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

Aber `item-query` ist kein gültiger Name für eine Variable in Python.

Am ähnlichsten wäre `item_query`.

Aber Sie möchten dennoch exakt `item-query` verwenden.

Dann können Sie einen `alias` deklarieren, und dieser Alias wird verwendet, um den Parameter-Wert zu finden:

//// tab | Python 3.10+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial009_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial009_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial009_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/query_params_str_validations/tutorial009_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="9"
{!> ../../../docs_src/query_params_str_validations/tutorial009.py!}
```

////

## Parameter als deprecated ausweisen

Nehmen wir an, Sie mögen diesen Parameter nicht mehr.

Sie müssen ihn eine Weile dort belassen, weil Clients ihn benutzen, aber Sie möchten, dass die Dokumentation klar anzeigt, dass er <abbr title="deprecated – obsolet, veraltet: Es soll nicht mehr verwendet werden">deprecated</abbr> ist.

In diesem Fall fügen Sie den Parameter `deprecated=True` zu `Query` hinzu.

//// tab | Python 3.10+

```Python hl_lines="19"
{!> ../../../docs_src/query_params_str_validations/tutorial010_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="19"
{!> ../../../docs_src/query_params_str_validations/tutorial010_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="20"
{!> ../../../docs_src/query_params_str_validations/tutorial010_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="16"
{!> ../../../docs_src/query_params_str_validations/tutorial010_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="18"
{!> ../../../docs_src/query_params_str_validations/tutorial010.py!}
```

////

Die Dokumentation wird das so anzeigen:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## Parameter von OpenAPI ausschließen

Um einen Query-Parameter vom generierten OpenAPI-Schema auszuschließen (und daher von automatischen Dokumentations-Systemen), setzen Sie den Parameter `include_in_schema` in `Query` auf `False`.

//// tab | Python 3.10+

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial014_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial014_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11"
{!> ../../../docs_src/query_params_str_validations/tutorial014_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="8"
{!> ../../../docs_src/query_params_str_validations/tutorial014_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="10"
{!> ../../../docs_src/query_params_str_validations/tutorial014.py!}
```

////

## Zusammenfassung

Sie können zusätzliche Validierungen und Metadaten zu ihren Parametern hinzufügen.

Allgemeine Validierungen und Metadaten:

* `alias`
* `title`
* `description`
* `deprecated`

Validierungen spezifisch für Strings:

* `min_length`
* `max_length`
* `pattern`

In diesen Beispielen haben Sie gesehen, wie Sie Validierungen für Strings hinzufügen.

In den nächsten Kapiteln sehen wir, wie man Validierungen für andere Typen hinzufügt, etwa für Zahlen.
