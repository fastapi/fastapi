# Body – Mehrere Parameter

Jetzt, da wir gesehen haben, wie `Path` und `Query` verwendet werden, schauen wir uns fortgeschrittenere Verwendungsmöglichkeiten von Requestbody-Deklarationen an.

## `Path`-, `Query`- und Body-Parameter vermischen

Zuerst einmal, Sie können `Path`-, `Query`- und Requestbody-Parameter-Deklarationen frei mischen und **FastAPI** wird wissen, was zu tun ist.

Und Sie können auch Body-Parameter als optional kennzeichnen, indem Sie den Defaultwert auf `None` setzen:

//// tab | Python 3.10+

```Python hl_lines="18-20"
{!> ../../../docs_src/body_multiple_params/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="18-20"
{!> ../../../docs_src/body_multiple_params/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="19-21"
{!> ../../../docs_src/body_multiple_params/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="17-19"
{!> ../../../docs_src/body_multiple_params/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="19-21"
{!> ../../../docs_src/body_multiple_params/tutorial001.py!}
```

////

/// note | "Hinweis"

Beachten Sie, dass in diesem Fall das `item`, welches vom Body genommen wird, optional ist. Da es `None` als Defaultwert hat.

///

## Mehrere Body-Parameter

Im vorherigen Beispiel erwartete die *Pfadoperation* einen JSON-Body mit den Attributen eines `Item`s, etwa:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

Aber Sie können auch mehrere Body-Parameter deklarieren, z. B. `item` und `user`:

//// tab | Python 3.10+

```Python hl_lines="20"
{!> ../../../docs_src/body_multiple_params/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="22"
{!> ../../../docs_src/body_multiple_params/tutorial002.py!}
```

////

In diesem Fall wird **FastAPI** bemerken, dass es mehr als einen Body-Parameter in der Funktion gibt (zwei Parameter, die Pydantic-Modelle sind).

Es wird deshalb die Parameternamen als Schlüssel (Feldnamen) im Body verwenden, und erwartet einen Body wie folgt:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

/// note | "Hinweis"

Beachten Sie, dass, obwohl `item` wie zuvor deklariert wurde, es nun unter einem Schlüssel `item` im Body erwartet wird.

///

**FastAPI** wird die automatische Konvertierung des Requests übernehmen, sodass der Parameter `item` seinen spezifischen Inhalt bekommt, genau so wie der Parameter `user`.

Es wird die Validierung dieser zusammengesetzten Daten übernehmen, und sie im OpenAPI-Schema und der automatischen Dokumentation dokumentieren.

## Einzelne Werte im Body

So wie `Query` und `Path` für Query- und Pfad-Parameter, hat **FastAPI** auch das Äquivalent `Body`, um Extra-Daten für Body-Parameter zu definieren.

Zum Beispiel, das vorherige Modell erweiternd, könnten Sie entscheiden, dass Sie einen weiteren Schlüssel <abbr title="Wichtigkeit">`importance`</abbr> haben möchten, im selben Body, Seite an Seite mit `item` und `user`.

Wenn Sie diesen Parameter einfach so hinzufügen, wird **FastAPI** annehmen, dass es ein Query-Parameter ist.

Aber Sie können **FastAPI** instruieren, ihn als weiteren Body-Schlüssel zu erkennen, indem Sie `Body` verwenden:

//// tab | Python 3.10+

```Python hl_lines="23"
{!> ../../../docs_src/body_multiple_params/tutorial003_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="23"
{!> ../../../docs_src/body_multiple_params/tutorial003_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="24"
{!> ../../../docs_src/body_multiple_params/tutorial003_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="20"
{!> ../../../docs_src/body_multiple_params/tutorial003_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="22"
{!> ../../../docs_src/body_multiple_params/tutorial003.py!}
```

////

In diesem Fall erwartet **FastAPI** einen Body wie:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

Wiederum wird es die Daten konvertieren, validieren, dokumentieren, usw.

## Mehrere Body-Parameter und Query-Parameter

Natürlich können Sie auch, wann immer Sie das brauchen, weitere Query-Parameter hinzufügen, zusätzlich zu den Body-Parametern.

Da einfache Werte standardmäßig als Query-Parameter interpretiert werden, müssen Sie `Query` nicht explizit hinzufügen, Sie können einfach schreiben:

```Python
q: Union[str, None] = None
```

Oder in Python 3.10 und darüber:

```Python
q: str | None = None
```

Zum Beispiel:

//// tab | Python 3.10+

```Python hl_lines="27"
{!> ../../../docs_src/body_multiple_params/tutorial004_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="27"
{!> ../../../docs_src/body_multiple_params/tutorial004_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="28"
{!> ../../../docs_src/body_multiple_params/tutorial004_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="25"
{!> ../../../docs_src/body_multiple_params/tutorial004_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="27"
{!> ../../../docs_src/body_multiple_params/tutorial004.py!}
```

////

/// info

`Body` hat die gleichen zusätzlichen Validierungs- und Metadaten-Parameter wie `Query` und `Path` und andere, die Sie später kennenlernen.

///

## Einen einzelnen Body-Parameter einbetten

Nehmen wir an, Sie haben nur einen einzelnen `item`-Body-Parameter, ein Pydantic-Modell `Item`.

Normalerweise wird **FastAPI** dann seinen JSON-Body direkt erwarten.

Aber wenn Sie möchten, dass es einen JSON-Body erwartet, mit einem Schlüssel `item` und darin den Inhalt des Modells, so wie es das tut, wenn Sie mehrere Body-Parameter deklarieren, dann können Sie den speziellen `Body`-Parameter `embed` setzen:

```Python
item: Item = Body(embed=True)
```

so wie in:

//// tab | Python 3.10+

```Python hl_lines="17"
{!> ../../../docs_src/body_multiple_params/tutorial005_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="17"
{!> ../../../docs_src/body_multiple_params/tutorial005_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="18"
{!> ../../../docs_src/body_multiple_params/tutorial005_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="15"
{!> ../../../docs_src/body_multiple_params/tutorial005_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="17"
{!> ../../../docs_src/body_multiple_params/tutorial005.py!}
```

////

In diesem Fall erwartet **FastAPI** einen Body wie:

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

statt:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## Zusammenfassung

Sie können mehrere Body-Parameter zu ihrer *Pfadoperation-Funktion* hinzufügen, obwohl ein Request nur einen einzigen Body enthalten kann.

**FastAPI** wird sich darum kümmern, Ihnen korrekte Daten in Ihrer Funktion zu überreichen, und das korrekte Schema in der *Pfadoperation* zu validieren und zu dokumentieren.

Sie können auch einzelne Werte deklarieren, die als Teil des Bodys empfangen werden.

Und Sie können **FastAPI** instruieren, den Body in einem Schlüssel unterzubringen, selbst wenn nur ein einzelner Body-Parameter deklariert ist.
