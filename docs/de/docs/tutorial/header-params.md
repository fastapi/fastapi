# Header-Parameter

So wie `Query`-, `Path`-, und `Cookie`-Parameter können Sie auch <abbr title='Header – Kopfzeilen, Header, Header-Felder: Schlüssel-Wert-Metadaten, die vom Client beim Request, und vom Server bei der Response gesendet werden'>Header</abbr>-Parameter definieren.

## `Header` importieren

Importieren Sie zuerst `Header`:

//// tab | Python 3.10+

```Python hl_lines="3"
{!> ../../../docs_src/header_params/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="3"
{!> ../../../docs_src/header_params/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="3"
{!> ../../../docs_src/header_params/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="1"
{!> ../../../docs_src/header_params/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="3"
{!> ../../../docs_src/header_params/tutorial001.py!}
```

////

## `Header`-Parameter deklarieren

Dann deklarieren Sie Ihre Header-Parameter, auf die gleiche Weise, wie Sie auch `Path`-, `Query`-, und `Cookie`-Parameter deklarieren.

Der erste Wert ist der Typ. Sie können `Header` die gehabten Extra Validierungs- und Beschreibungsparameter hinzufügen. Danach können Sie einen Defaultwert vergeben:

//// tab | Python 3.10+

```Python hl_lines="9"
{!> ../../../docs_src/header_params/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/header_params/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10"
{!> ../../../docs_src/header_params/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/header_params/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="9"
{!> ../../../docs_src/header_params/tutorial001.py!}
```

////

/// note | "Technische Details"

`Header` ist eine Schwesterklasse von `Path`, `Query` und `Cookie`. Sie erbt von derselben gemeinsamen `Param`-Elternklasse.

Aber erinnern Sie sich, dass, wenn Sie `Query`, `Path`,  `Header` und andere von `fastapi` importieren, diese tatsächlich Funktionen sind, welche spezielle Klassen zurückgeben.

///

/// info

Um Header zu deklarieren, müssen Sie `Header` verwenden, da diese Parameter sonst als Query-Parameter interpretiert werden würden.

///

## Automatische Konvertierung

`Header` hat weitere Funktionalität, zusätzlich zu der, die `Path`, `Query` und `Cookie` bereitstellen.

Die meisten Standard-Header benutzen als Trennzeichen einen Bindestrich, auch bekannt als das „Minus-Symbol“ (`-`).

Aber eine Variable wie `user-agent` ist in Python nicht gültig.

Darum wird `Header` standardmäßig in Parameternamen den Unterstrich (`_`) zu einem Bindestrich (`-`) konvertieren.

HTTP-Header sind außerdem unabhängig von Groß-/Kleinschreibung, darum können Sie sie mittels der Standard-Python-Schreibweise deklarieren (auch bekannt als "snake_case").

Sie können also `user_agent` schreiben, wie Sie es normalerweise in Python-Code machen würden, statt etwa die ersten Buchstaben groß zu schreiben, wie in `User_Agent`.

Wenn Sie aus irgendeinem Grund das automatische Konvertieren von Unterstrichen zu Bindestrichen abschalten möchten, setzen Sie den Parameter `convert_underscores` auf `False`.

//// tab | Python 3.10+

```Python hl_lines="10"
{!> ../../../docs_src/header_params/tutorial002_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="11"
{!> ../../../docs_src/header_params/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="12"
{!> ../../../docs_src/header_params/tutorial002_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="8"
{!> ../../../docs_src/header_params/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="10"
{!> ../../../docs_src/header_params/tutorial002.py!}
```

////

/// warning | "Achtung"

Bevor Sie `convert_underscores` auf `False` setzen, bedenken Sie, dass manche HTTP-Proxys und Server die Verwendung von Headern mit Unterstrichen nicht erlauben.

///

## Doppelte Header

Es ist möglich, doppelte Header zu empfangen. Also den gleichen Header mit unterschiedlichen Werten.

Sie können solche Fälle deklarieren, indem Sie in der Typdeklaration eine Liste verwenden.

Sie erhalten dann alle Werte von diesem doppelten Header als Python-`list`e.

Um zum Beispiel einen Header `X-Token` zu deklarieren, der mehrmals vorkommen kann, schreiben Sie:

//// tab | Python 3.10+

```Python hl_lines="9"
{!> ../../../docs_src/header_params/tutorial003_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/header_params/tutorial003_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10"
{!> ../../../docs_src/header_params/tutorial003_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="7"
{!> ../../../docs_src/header_params/tutorial003_py310.py!}
```

////

//// tab | Python 3.9+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="9"
{!> ../../../docs_src/header_params/tutorial003_py39.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="9"
{!> ../../../docs_src/header_params/tutorial003.py!}
```

////

Wenn Sie mit einer *Pfadoperation* kommunizieren, die zwei HTTP-Header sendet, wie:

```
X-Token: foo
X-Token: bar
```

Dann wäre die Response:

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## Zusammenfassung

Deklarieren Sie Header mittels `Header`, auf die gleiche Weise wie bei `Query`, `Path` und `Cookie`.

Machen Sie sich keine Sorgen um Unterstriche in ihren Variablen, **FastAPI** wird sich darum kümmern, diese zu konvertieren.
