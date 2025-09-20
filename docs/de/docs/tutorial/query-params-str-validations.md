# Query-Parameter und String-Validierungen { #query-parameters-and-string-validations }

**FastAPI** ermöglicht es Ihnen, zusätzliche Informationen und Validierungen für Ihre Parameter zu deklarieren.

Nehmen wir diese Anwendung als Beispiel:

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

Der Query-Parameter `q` hat den Typ `str | None`, das bedeutet, dass er vom Typ `str` sein kann, aber auch `None`, und tatsächlich ist der Defaultwert `None`, sodass FastAPI weiß, dass er nicht erforderlich ist.

/// note | Hinweis

FastAPI erkennt, dass der Wert von `q` nicht erforderlich ist, aufgrund des Defaultwertes `= None`.

Die Verwendung von `str | None` ermöglicht es Ihrem Editor, Ihnen bessere Unterstützung zu bieten und Fehler zu erkennen.

///

## Zusätzliche Validierung { #additional-validation }

Wir werden sicherstellen, dass, obwohl `q` optional ist, wann immer es bereitgestellt wird, **seine Länge 50 Zeichen nicht überschreitet**.

### `Query` und `Annotated` importieren { #import-query-and-annotated }

Um dies zu erreichen, importieren Sie zuerst:

* `Query` von `fastapi`
* `Annotated` von `typing`

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[1,3] *}

/// info | Info

FastAPI hat Unterstützung für `Annotated` hinzugefügt (und begonnen, es zu empfehlen) in der Version 0.95.0.

Wenn Sie eine ältere Version haben, würden Sie Fehler erhalten, beim Versuch, `Annotated` zu verwenden.

Stellen Sie sicher, dass Sie [die FastAPI-Version aktualisieren](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}, auf mindestens Version 0.95.1, bevor Sie `Annotated` verwenden.

///

## Verwenden von `Annotated` im Typ für den `q`-Parameter { #use-annotated-in-the-type-for-the-q-parameter }

Erinnern Sie sich, dass ich Ihnen zuvor in [Python-Typen-Intro](../python-types.md#type-hints-with-metadata-annotations){.internal-link target=_blank} gesagt habe, dass `Annotated` verwendet werden kann, um Metadaten zu Ihren Parametern hinzuzufügen?

Jetzt ist es soweit, dies mit FastAPI zu verwenden. 🚀

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

Was wir tun werden, ist, dies mit `Annotated` zu wrappen, sodass es zu:

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

Beide dieser Versionen bedeuten dasselbe: `q` ist ein Parameter, der ein `str` oder `None` sein kann, und standardmäßig ist er `None`.

Jetzt springen wir zu den spannenden Dingen. 🎉

## `Query` zu `Annotated` im `q`-Parameter hinzufügen { #add-query-to-annotated-in-the-q-parameter }

Da wir nun `Annotated` haben, in das wir mehr Informationen (in diesem Fall einige zusätzliche Validierungen) einfügen können, fügen Sie `Query` innerhalb von `Annotated` hinzu und setzen Sie den Parameter `max_length` auf `50`:

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

Beachten Sie, dass der Defaultwert weiterhin `None` ist, so dass der Parameter weiterhin optional ist.

Aber jetzt, mit `Query(max_length=50)` innerhalb von `Annotated`, sagen wir FastAPI, dass wir eine **zusätzliche Validierung** für diesen Wert wünschen, wir wollen, dass er maximal 50 Zeichen hat. 😎

/// tip | Tipp

Hier verwenden wir `Query()`, weil dies ein **Query-Parameter** ist. Später werden wir andere wie `Path()`, `Body()`, `Header()`, und `Cookie()` sehen, die auch dieselben Argumente wie `Query()` akzeptieren.

///

FastAPI wird nun:

* Die Daten **validieren**, um sicherzustellen, dass die Länge maximal 50 Zeichen beträgt
* Einen **klaren Fehler** für den Client anzeigen, wenn die Daten ungültig sind
* Den Parameter in der OpenAPI-Schema-*Pfadoperation* **dokumentieren** (sodass er in der **automatischen Dokumentation** angezeigt wird)

## Alternative (alt): `Query` als Defaultwert { #alternative-old-query-as-the-default-value }

Frühere Versionen von FastAPI (vor <abbr title="vor 2023-03">0.95.0</abbr>) erforderten, dass Sie `Query` als den Defaultwert Ihres Parameters verwendeten, anstatt es innerhalb von `Annotated` zu platzieren. Es besteht eine hohe Wahrscheinlichkeit, dass Sie Code sehen, der es so verwendet, also werde ich es Ihnen erklären.

/// tip | Tipp

Für neuen Code und wann immer es möglich ist, verwenden Sie `Annotated` wie oben erklärt. Es gibt mehrere Vorteile (unten erläutert) und keine Nachteile. 🍰

///

So würden Sie `Query()` als den Defaultwert Ihres Funktionsparameters verwenden und den Parameter `max_length` auf 50 setzen:

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

Da wir in diesem Fall (ohne die Verwendung von `Annotated`) den Defaultwert `None` in der Funktion durch `Query()` ersetzen müssen, müssen wir nun den Defaultwert mit dem Parameter `Query(default=None)` setzen, er erfüllt den gleichen Zweck, diesen Defaultwert zu definieren (zumindest für FastAPI).

Also:

```Python
q: str | None = Query(default=None)
```

... macht den Parameter optional mit einem Defaultwert von `None`, genauso wie:

```Python
q: str | None = None
```

Aber die `Query`-Version deklariert ihn explizit als Query-Parameter.

Dann können wir mehr Parameter an `Query` übergeben. In diesem Fall den `max_length`-Parameter, der auf Strings angewendet wird:

```Python
q: str | None = Query(default=None, max_length=50)
```

Dies wird die Daten validieren, einen klaren Fehler anzeigen, wenn die Daten nicht gültig sind, und den Parameter in der OpenAPI-Schema-*Pfadoperation* dokumentieren.

### `Query` als Defaultwert oder in `Annotated` { #query-as-the-default-value-or-in-annotated }

Beachten Sie, dass wenn Sie `Query` innerhalb von `Annotated` verwenden, Sie den `default`-Parameter für `Query` nicht verwenden dürfen.

Setzen Sie stattdessen den tatsächlichen Defaultwert des Funktionsparameters. Andernfalls wäre es inkonsistent.

Zum Beispiel ist das nicht erlaubt:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

... denn es ist nicht klar, ob der Defaultwert `"rick"` oder `"morty"` sein soll.

Sie würden also (bevorzugt) schreiben:

```Python
q: Annotated[str, Query()] = "rick"
```

... oder in älteren Codebasen finden Sie:

```Python
q: str = Query(default="rick")
```

### Vorzüge von `Annotated` { #advantages-of-annotated }

**Es wird empfohlen, `Annotated` zu verwenden**, anstelle des Defaultwertes in Funktionsparametern, es ist aus mehreren Gründen **besser**. 🤓

Der **Default**wert des **Funktionsparameters** ist der **tatsächliche Default**wert, das ist in der Regel intuitiver mit Python. 😌

Sie könnten **diese gleiche Funktion** in **anderen Stellen** ohne FastAPI **aufrufen**, und es würde **wie erwartet funktionieren**. Wenn es einen **erforderlichen** Parameter gibt (ohne Defaultwert), wird Ihr **Editor** Ihnen dies mit einem Fehler mitteilen, außerdem wird **Python** sich beschweren, wenn Sie es ausführen, ohne den erforderlichen Parameter zu übergeben.

Wenn Sie `Annotated` nicht verwenden und stattdessen die **(alte) Defaultwert-Stilform** verwenden, müssen Sie sich daran **erinnern**, die Argumente der Funktion zu übergeben, wenn Sie diese Funktion ohne FastAPI in **anderen Stellen** aufrufen. Ansonsten sind die Werte anders als erwartet (z. B. `QueryInfo` oder etwas Ähnliches statt `str`). Ihr Editor kann Ihnen nicht helfen, und Python wird die Funktion ohne Klagen ausführen und sich nur beschweren wenn die Operationen innerhalb auf einen Fehler stoßen.

Da `Annotated` mehr als eine Metadaten-Annotation haben kann, könnten Sie dieselbe Funktion sogar mit anderen Tools verwenden, wie z. B. <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a>. 🚀

## Mehr Validierungen hinzufügen { #add-more-validations }

Sie können auch einen `min_length`-Parameter hinzufügen:

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## Reguläre Ausdrücke hinzufügen { #add-regular-expressions }

Sie können einen <abbr title="Ein regulärer Ausdruck, regex oder regexp genannt, ist eine Sequenz von Zeichen, die ein Suchmuster für Zeichenfolgen definiert.">regulären Ausdruck</abbr> `pattern` definieren, mit dem der Parameter übereinstimmen muss:

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

Dieses spezielle Suchmuster im regulären Ausdruck überprüft, dass der erhaltene Parameterwert:

* `^`: mit den nachfolgenden Zeichen beginnt, keine Zeichen davor hat.
* `fixedquery`: den exakten Text `fixedquery` hat.
* `$`: dort endet, keine weiteren Zeichen nach `fixedquery` hat.

Wenn Sie sich mit all diesen **„regulärer Ausdruck“**-Ideen verloren fühlen, keine Sorge. Sie sind ein schwieriges Thema für viele Menschen. Sie können noch viele Dinge tun, ohne reguläre Ausdrücke direkt zu benötigen.

Aber nun wissen Sie, dass Sie sie in **FastAPI** immer dann verwenden können, wenn Sie sie brauchen.

### Pydantic v1 `regex` statt `pattern` { #pydantic-v1-regex-instead-of-pattern }

Vor Pydantic Version 2 und FastAPI 0.100.0, hieß der Parameter `regex` statt `pattern`, aber das ist jetzt obsolet.

Sie könnten immer noch Code sehen, der den alten Namen verwendet:

//// tab | Pydantic v1

{* ../../docs_src/query_params_str_validations/tutorial004_regex_an_py310.py hl[11] *}

////

Beachten Sie aber, dass das obsolet ist und auf den neuen Parameter `pattern` aktualisiert werden sollte. 🤓

## Defaultwerte { #default-values }

Natürlich können Sie Defaultwerte verwenden, die nicht `None` sind.

Nehmen wir an, Sie möchten, dass der `q` Query-Parameter eine `min_length` von `3` hat und einen Defaultwert von `"fixedquery"`:

{* ../../docs_src/query_params_str_validations/tutorial005_an_py39.py hl[9] *}

/// note | Hinweis

Ein Defaultwert irgendeines Typs, einschließlich `None`, macht den Parameter optional (nicht erforderlich).

///

## Erforderliche Parameter { #required-parameters }

Wenn wir keine weiteren Validierungen oder Metadaten deklarieren müssen, können wir den `q` Query-Parameter erforderlich machen, indem wir einfach keinen Defaultwert deklarieren, wie:

```Python
q: str
```

statt:

```Python
q: str | None = None
```

Aber jetzt deklarieren wir es mit `Query`, zum Beispiel so:

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

Wenn Sie einen Wert als erforderlich deklarieren müssen, während Sie `Query` verwenden, deklarieren Sie einfach keinen Defaultwert:

{* ../../docs_src/query_params_str_validations/tutorial006_an_py39.py hl[9] *}

### Erforderlich, kann `None` sein { #required-can-be-none }

Sie können deklarieren, dass ein Parameter `None` akzeptieren kann, aber trotzdem erforderlich ist. Dadurch müssten Clients den Wert senden, selbst wenn der Wert `None` ist.

Um das zu tun, können Sie deklarieren, dass `None` ein gültiger Typ ist, einfach indem Sie keinen Defaultwert deklarieren:

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

## Query-Parameter-Liste / Mehrere Werte { #query-parameter-list-multiple-values }

Wenn Sie einen Query-Parameter explizit mit `Query` definieren, können Sie ihn auch so deklarieren, dass er eine Liste von Werten empfängt, oder anders gesagt, dass er mehrere Werte empfangen kann.

Um zum Beispiel einen Query-Parameter `q` zu deklarieren, der mehrmals in der URL vorkommen kann, schreiben Sie:

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

Dann, mit einer URL wie:

```
http://localhost:8000/items/?q=foo&q=bar
```

würden Sie die mehreren `q`-*Query-Parameter*-Werte (`foo` und `bar`) in einer Python-`list` in Ihrer *Pfadoperation-Funktion* im *Funktionsparameter* `q` erhalten.

So wäre die <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> zu dieser URL:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | Tipp

Um einen Query-Parameter mit einem Typ `list` zu deklarieren, wie im obigen Beispiel, müssen Sie explizit `Query` verwenden, da er andernfalls als <abbr title="Anfragekörper">Requestbody</abbr> interpretiert würde.

///

Die interaktive API-Dokumentation wird entsprechend aktualisiert, um mehrere Werte zu erlauben:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### Query-Parameter-Liste / Mehrere Werte mit Defaults { #query-parameter-list-multiple-values-with-defaults }

Sie können auch eine Default-`list` von Werten definieren, wenn keine bereitgestellt werden:

{* ../../docs_src/query_params_str_validations/tutorial012_an_py39.py hl[9] *}

Wenn Sie zu:

```
http://localhost:8000/items/
```

gehen, wird der Default für `q` sein: `["foo", "bar"]`, und Ihre Response wird sein:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### Nur `list` verwenden { #using-just-list }

Sie können auch `list` direkt verwenden, anstelle von `list[str]`:

{* ../../docs_src/query_params_str_validations/tutorial013_an_py39.py hl[9] *}

/// note | Hinweis

Beachten Sie, dass FastAPI in diesem Fall den Inhalt der Liste nicht überprüft.

Zum Beispiel würde `list[int]` überprüfen (und dokumentieren), dass der Inhalt der Liste Ganzzahlen sind. Aber `list` alleine würde das nicht.

///

## Mehr Metadaten deklarieren { #declare-more-metadata }

Sie können mehr Informationen über den Parameter hinzufügen.

Diese Informationen werden in das generierte OpenAPI aufgenommen und von den Dokumentationsoberflächen und externen Tools verwendet.

/// note | Hinweis

Beachten Sie, dass verschiedene Tools möglicherweise unterschiedliche Unterstützungslevels für OpenAPI haben.

Einige davon könnten noch nicht alle zusätzlichen Informationen anzuzeigen, die Sie erklärten, obwohl in den meisten Fällen die fehlende Funktionalität bereits in der Entwicklung geplant ist.

///

Sie können einen `title` hinzufügen:

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

Und eine `description`:

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## Alias-Parameter { #alias-parameters }

Stellen Sie sich vor, Sie möchten, dass der Parameter `item-query` ist.

Wie in:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

Aber `item-query` ist kein gültiger Name für eine Variable in Python.

Der am ähnlichsten wäre `item_query`.

Aber Sie benötigen dennoch, dass er genau `item-query` ist ...

Dann können Sie ein `alias` deklarieren, und dieser Alias wird verwendet, um den Parameterwert zu finden:

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## Parameter als deprecatet ausweisen { #deprecating-parameters }

Nehmen wir an, Ihnen gefällt dieser Parameter nicht mehr.

Sie müssen ihn eine Weile dort belassen, da es Clients gibt, die ihn verwenden, aber Sie möchten, dass die Dokumentation ihn klar als <abbr title="veraltet, obsolet: Es soll nicht mehr verwendet werden">deprecatet</abbr> anzeigt.

Dann übergeben Sie den Parameter `deprecated=True` an `Query`:

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

Die Dokumentation wird es so anzeigen:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## Parameter von OpenAPI ausschließen { #exclude-parameters-from-openapi }

Um einen Query-Parameter aus dem generierten OpenAPI-Schema auszuschließen (und somit aus den automatischen Dokumentationssystemen), setzen Sie den Parameter `include_in_schema` von `Query` auf `False`:

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## Benutzerdefinierte Validierung { #custom-validation }

Es kann Fälle geben, in denen Sie eine **benutzerdefinierte Validierung** durchführen müssen, die nicht mit den oben gezeigten Parametern durchgeführt werden kann.

In diesen Fällen können Sie eine **benutzerdefinierte Validierungsfunktion** verwenden, die nach der normalen Validierung angewendet wird (z. B. nach der Validierung, dass der Wert ein `str` ist).

Sie können dies mit <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator" class="external-link" target="_blank">Pydantic's `AfterValidator`</a> innerhalb von `Annotated` erreichen.

/// tip | Tipp

Pydantic unterstützt auch <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-before-validator" class="external-link" target="_blank">`BeforeValidator`</a> und andere. 🤓

///

Zum Beispiel überprüft dieser benutzerdefinierte Validator, ob die Artikel-ID mit `isbn-` für eine <abbr title="ISBN bedeutet Internationale Standardbuchnummer">ISBN</abbr>-Buchnummer oder mit `imdb-` für eine <abbr title="IMDB (Internet Movie Database) ist eine Website mit Informationen über Filme">IMDB</abbr>-Film-URL-ID beginnt:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py hl[5,16:19,24] *}

/// info | Info

Dies ist verfügbar seit Pydantic Version 2 oder höher. 😎

///

/// tip | Tipp

Wenn Sie irgendeine Art von Validierung durchführen müssen, die eine Kommunikation mit einer **externen Komponente** erfordert, wie z. B. einer Datenbank oder einer anderen API, sollten Sie stattdessen **FastAPI-Abhängigkeiten** verwenden. Sie werden diese später kennenlernen.

Diese benutzerdefinierten Validatoren sind für Dinge gedacht, die einfach mit denselben **Daten** überprüft werden können, die im Request bereitgestellt werden.

///

### Dieses Codebeispiel verstehen { #understand-that-code }

Der wichtige Punkt ist einfach die Verwendung von **`AfterValidator` mit einer Funktion innerhalb von `Annotated`**. Fühlen Sie sich frei, diesen Teil zu überspringen. 🤸

---

Aber wenn Sie neugierig auf dieses spezielle Codebeispiel sind und immer noch Spaß haben, hier sind einige zusätzliche Details.

#### Zeichenkette mit `value.startswith()` { #string-with-value-startswith }

Haben Sie bemerkt? Eine Zeichenkette mit `value.startswith()` kann ein Tuple übernehmen, und es wird jeden Wert im Tuple überprüfen:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[16:19] hl[17] *}

#### Ein zufälliges Item { #a-random-item }

Mit `data.items()` erhalten wir ein <abbr title="Etwas, das man mit einer for-Schleife durchlaufen kann, wie eine Liste, Set, usw.">iterierbares Objekt</abbr> mit Tupeln, die Schlüssel und Wert für jedes <abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">Dictionary</abbr>-Element enthalten.

Wir konvertieren dieses iterierbare Objekt mit `list(data.items())` in eine richtige `list`.

Dann können wir mit `random.choice()` einen **zufälligen Wert** aus der Liste erhalten, also bekommen wir ein Tuple mit `(id, name)`. Es wird etwas wie `("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy")` sein.

Dann **weisen wir diese beiden Werte** des Tupels den Variablen `id` und `name` zu.

Wenn der Benutzer also keine Artikel-ID bereitgestellt hat, erhält er trotzdem einen zufälligen Vorschlag.

... wir tun all dies in einer **einzelnen einfachen Zeile**. 🤯 Lieben Sie nicht auch Python? 🐍

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[22:30] hl[29] *}

## Zusammenfassung { #recap }

Sie können zusätzliche Validierungen und Metadaten für Ihre Parameter deklarieren.

Allgemeine Validierungen und Metadaten:

* `alias`
* `title`
* `description`
* `deprecated`

Validierungen, die spezifisch für Strings sind:

* `min_length`
* `max_length`
* `pattern`

Benutzerdefinierte Validierungen mit `AfterValidator`.

In diesen Beispielen haben Sie gesehen, wie Sie Validierungen für `str`-Werte deklarieren.

Sehen Sie sich die nächsten Kapitel an, um zu erfahren, wie Sie Validierungen für andere Typen, wie z. B. Zahlen, deklarieren.
