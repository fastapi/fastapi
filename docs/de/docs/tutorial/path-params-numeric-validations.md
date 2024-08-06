# Pfad-Parameter und Validierung von Zahlen

So wie Sie mit `Query` für Query-Parameter zusätzliche Validierungen und Metadaten hinzufügen können, können Sie das mittels `Path` auch für Pfad-Parameter tun.

## `Path` importieren

Importieren Sie zuerst `Path` von `fastapi`, und importieren Sie `Annotated`.

//// tab | Python 3.10+

```Python hl_lines="1  3"
{!> ../../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="1  3"
{!> ../../../docs_src/path_params_numeric_validations/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="3-4"
{!> ../../../docs_src/path_params_numeric_validations/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="1"
{!> ../../../docs_src/path_params_numeric_validations/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="3"
{!> ../../../docs_src/path_params_numeric_validations/tutorial001.py!}
```

////

/// info

FastAPI unterstützt (und empfiehlt die Verwendung von) `Annotated` seit Version 0.95.0.

Wenn Sie eine ältere Version haben, werden Sie Fehler angezeigt bekommen, wenn Sie versuchen, `Annotated` zu verwenden.

Bitte [aktualisieren Sie FastAPI](../deployment/versions.md#upgrade-der-fastapi-versionen){.internal-link target=_blank} daher mindestens zu Version 0.95.1, bevor Sie `Annotated` verwenden.

///

## Metadaten deklarieren

Sie können die gleichen Parameter deklarieren wie für `Query`.

Um zum Beispiel einen `title`-Metadaten-Wert für den Pfad-Parameter `item_id` zu deklarieren, schreiben Sie:

//// tab | Python 3.10+

```Python hl_lines="10"
{!> ../../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="10"
{!> ../../../docs_src/path_params_numeric_validations/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11"
{!> ../../../docs_src/path_params_numeric_validations/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="8"
{!> ../../../docs_src/path_params_numeric_validations/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="10"
{!> ../../../docs_src/path_params_numeric_validations/tutorial001.py!}
```

////

/// note | "Hinweis"

Ein Pfad-Parameter ist immer erforderlich, weil er Teil des Pfads sein muss.

Sie sollten ihn daher mit `...` deklarieren, um ihn als erforderlich auszuzeichnen.

Doch selbst wenn Sie ihn mit `None` deklarieren, oder einen Defaultwert setzen, bewirkt das nichts, er bleibt immer erforderlich.

///

## Sortieren Sie die Parameter, wie Sie möchten

/// tip | "Tipp"

Wenn Sie `Annotated` verwenden, ist das folgende nicht so wichtig / nicht notwendig.

///

Nehmen wir an, Sie möchten den Query-Parameter `q` als erforderlichen `str` deklarieren.

Und Sie müssen sonst nichts anderes für den Parameter deklarieren, Sie brauchen also nicht wirklich `Query`.

Aber Sie brauchen `Path` für den `item_id`-Pfad-Parameter. Und Sie möchten aus irgendeinem Grund nicht `Annotated` verwenden.

Python wird sich beschweren, wenn Sie einen Parameter mit Defaultwert vor einen Parameter ohne Defaultwert setzen.

Aber Sie können die Reihenfolge der Parameter ändern, den Query-Parameter ohne Defaultwert zuerst.

Für **FastAPI** ist es nicht wichtig. Es erkennt die Parameter anhand ihres Namens, ihrer Typen, und ihrer Defaultwerte (`Query`, `Path`, usw.). Es kümmert sich nicht um die Reihenfolge.

Sie können Ihre Funktion also so deklarieren:

//// tab | Python 3.8 nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/path_params_numeric_validations/tutorial002.py!}
```

////

Aber bedenken Sie, dass Sie dieses Problem nicht haben, wenn Sie `Annotated` verwenden, da Sie nicht die Funktions-Parameter-Defaultwerte für `Query()` oder `Path()` verwenden.

//// tab | Python 3.9+

```Python hl_lines="10"
{!> ../../../docs_src/path_params_numeric_validations/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9"
{!> ../../../docs_src/path_params_numeric_validations/tutorial002_an.py!}
```

////

## Sortieren Sie die Parameter wie Sie möchten: Tricks

/// tip | "Tipp"

Wenn Sie `Annotated` verwenden, ist das folgende nicht so wichtig / nicht notwendig.

///

Hier ein **kleiner Trick**, der nützlich sein kann, aber Sie werden ihn nicht oft brauchen.

Wenn Sie eines der folgenden Dinge tun möchten:

* den `q`-Parameter ohne `Query` oder irgendeinem Defaultwert deklarieren
* den Pfad-Parameter `item_id` mittels `Path` deklarieren
* die Parameter in einer unterschiedlichen Reihenfolge haben
* `Annotated` nicht verwenden

... dann hat Python eine kleine Spezial-Syntax für Sie.

Übergeben Sie der Funktion `*` als ersten Parameter.

Python macht nichts mit diesem `*`, aber es wird wissen, dass alle folgenden Parameter als <abbr title="Keyword-Argument – Schlüsselwort-Argument: Das Argument wird anhand seines Namens erkannt, nicht anhand seiner Reihenfolge in der Argumentliste">Keyword-Argumente</abbr> (Schlüssel-Wert-Paare), auch bekannt als <abbr title="Von: K-ey W-ord Arg-uments"><code>kwargs</code></abbr>, verwendet werden. Selbst wenn diese keinen Defaultwert haben.

```Python hl_lines="7"
{!../../../docs_src/path_params_numeric_validations/tutorial003.py!}
```

### Besser mit `Annotated`

Bedenken Sie, dass Sie, wenn Sie `Annotated` verwenden, dieses Problem nicht haben, weil Sie keine Defaultwerte für Ihre Funktionsparameter haben. Sie müssen daher wahrscheinlich auch nicht `*` verwenden.

//// tab | Python 3.9+

```Python hl_lines="10"
{!> ../../../docs_src/path_params_numeric_validations/tutorial003_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9"
{!> ../../../docs_src/path_params_numeric_validations/tutorial003_an.py!}
```

////

## Validierung von Zahlen: Größer oder gleich

Mit `Query` und `Path` (und anderen, die Sie später kennenlernen), können Sie Zahlenbeschränkungen deklarieren.

Hier, mit `ge=1`, wird festgelegt, dass `item_id` eine Ganzzahl benötigt, die größer oder gleich `1` ist (`g`reater than or `e`qual).
//// tab | Python 3.9+

```Python hl_lines="10"
{!> ../../../docs_src/path_params_numeric_validations/tutorial004_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9"
{!> ../../../docs_src/path_params_numeric_validations/tutorial004_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="8"
{!> ../../../docs_src/path_params_numeric_validations/tutorial004.py!}
```

////

## Validierung von Zahlen: Größer und kleiner oder gleich

Das Gleiche trifft zu auf:

* `gt`: `g`reater `t`han – größer als
* `le`: `l`ess than or `e`qual – kleiner oder gleich

//// tab | Python 3.9+

```Python hl_lines="10"
{!> ../../../docs_src/path_params_numeric_validations/tutorial005_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9"
{!> ../../../docs_src/path_params_numeric_validations/tutorial005_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="9"
{!> ../../../docs_src/path_params_numeric_validations/tutorial005.py!}
```

////

## Validierung von Zahlen: Floats, größer und kleiner

Zahlenvalidierung funktioniert auch für <abbr title="Kommazahl">`float`</abbr>-Werte.

Hier wird es wichtig, in der Lage zu sein, <abbr title="greater than – größer als"><code>gt</code></abbr> zu deklarieren, und nicht nur <abbr title="greater than or equal – größer oder gleich"><code>ge</code></abbr>, da Sie hiermit bestimmen können, dass ein Wert, zum Beispiel, größer als `0` sein muss, obwohl er kleiner als `1` ist.

`0.5` wäre also ein gültiger Wert, aber nicht `0.0` oder `0`.

Das gleiche gilt für <abbr title="less than – kleiner als"><code>lt</code></abbr>.

//// tab | Python 3.9+

```Python hl_lines="13"
{!> ../../../docs_src/path_params_numeric_validations/tutorial006_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="12"
{!> ../../../docs_src/path_params_numeric_validations/tutorial006_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="11"
{!> ../../../docs_src/path_params_numeric_validations/tutorial006.py!}
```

////

## Zusammenfassung

Mit `Query` und `Path` (und anderen, die Sie noch nicht gesehen haben) können Sie Metadaten und Stringvalidierungen deklarieren, so wie in [Query-Parameter und Stringvalidierungen](query-params-str-validations.md){.internal-link target=_blank} beschrieben.

Und Sie können auch Validierungen für Zahlen deklarieren:

* `gt`: `g`reater `t`han – größer als
* `ge`: `g`reater than or `e`qual – größer oder gleich
* `lt`: `l`ess `t`han – kleiner als
* `le`: `l`ess than or `e`qual – kleiner oder gleich

/// info

`Query`, `Path`, und andere Klassen, die Sie später kennenlernen, sind Unterklassen einer allgemeinen `Param`-Klasse.

Sie alle teilen die gleichen Parameter für zusätzliche Validierung und Metadaten, die Sie gesehen haben.

///

/// note | "Technische Details"

`Query`, `Path` und andere, die Sie von `fastapi` importieren, sind tatsächlich Funktionen.

Die, wenn sie aufgerufen werden, Instanzen der Klassen mit demselben Namen zurückgeben.

Sie importieren also `Query`, welches eine Funktion ist. Aber wenn Sie es aufrufen, gibt es eine Instanz der Klasse zurück, die auch `Query` genannt wird.

Diese Funktionen existieren (statt die Klassen direkt zu verwenden), damit Ihr Editor keine Fehlermeldungen über ihre Typen ausgibt.

Auf diese Weise können Sie Ihren Editor und Ihre Programmier-Tools verwenden, ohne besondere Einstellungen vornehmen zu müssen, um diese Fehlermeldungen stummzuschalten.

///
