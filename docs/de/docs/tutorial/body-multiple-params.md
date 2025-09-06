# Body – Mehrere Parameter { #body-multiple-parameters }

Nun, da wir gesehen haben, wie `Path` und `Query` verwendet werden, schauen wir uns fortgeschrittenere Verwendungsmöglichkeiten von <abbr title="Anfragekörper">Requestbody</abbr>-Deklarationen an.

## `Path`-, `Query`- und Body-Parameter vermischen { #mix-path-query-and-body-parameters }

Zuerst einmal, Sie können `Path`-, `Query`- und Requestbody-Parameter-Deklarationen frei mischen und **FastAPI** wird wissen, was zu tun ist.

Und Sie können auch Body-Parameter als optional kennzeichnen, indem Sie den Defaultwert auf `None` setzen:

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note | Hinweis

Beachten Sie, dass in diesem Fall das `item`, welches vom Body genommen wird, optional ist. Da es `None` als Defaultwert hat.

///

## Mehrere Body-Parameter { #multiple-body-parameters }

Im vorherigen Beispiel erwarteten die *Pfadoperationen* einen JSON-Body mit den Attributen eines `Item`s, etwa:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

Aber Sie können auch mehrere Body-Parameter deklarieren, z. B. `item` und `user`:

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}

In diesem Fall wird **FastAPI** bemerken, dass es mehr als einen Body-Parameter in der Funktion gibt (zwei Parameter, die Pydantic-Modelle sind).

Es wird deshalb die Parameternamen als Schlüssel (Feldnamen) im Body verwenden und erwartet einen Body wie folgt:

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

/// note | Hinweis

Beachten Sie, dass, obwohl `item` wie zuvor deklariert wurde, es nun unter einem Schlüssel `item` im Body erwartet wird.

///

**FastAPI** wird die automatische Konvertierung des Requests übernehmen, sodass der Parameter `item` seinen spezifischen Inhalt bekommt, und das Gleiche gilt für den Parameter `user`.

Es wird die Validierung dieser zusammengesetzten Daten übernehmen, und diese im OpenAPI-Schema und der automatischen Dokumentation dokumentieren.

## Einzelne Werte im Body { #singular-values-in-body }

So wie `Query` und `Path` für Query- und Pfad-Parameter, stellt **FastAPI** das Äquivalent `Body` zur Verfügung, um Extra-Daten für Body-Parameter zu definieren.

Zum Beispiel, das vorherige Modell erweiternd, könnten Sie entscheiden, dass Sie einen weiteren Schlüssel `importance` im selben Body haben möchten, neben `item` und `user`.

Wenn Sie diesen Parameter einfach so hinzufügen, wird **FastAPI** annehmen, dass es ein Query-Parameter ist, da er ein einzelner Wert ist.

Aber Sie können **FastAPI** instruieren, ihn als weiteren Body-Schlüssel zu erkennen, indem Sie `Body` verwenden:

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}

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

Wiederum wird es die Datentypen konvertieren, validieren, dokumentieren, usw.

## Mehrere Body-Parameter und Query-Parameter { #multiple-body-params-and-query }

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

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}

/// info | Info

`Body` hat die gleichen zusätzlichen Validierungs- und Metadaten-Parameter wie `Query`, `Path` und andere, die Sie später kennenlernen werden.

///

## Einen einzelnen Body-Parameter einbetten { #embed-a-single-body-parameter }

Nehmen wir an, Sie haben nur einen einzelnen `item`-Body-Parameter von einem Pydantic-Modell `Item`.

Standardmäßig wird **FastAPI** dann seinen Body direkt erwarten.

Aber wenn Sie möchten, dass es einen JSON-Body mit einem Schlüssel `item` erwartet, und darin den Inhalt des Modells, so wie es das tut, wenn Sie mehrere Body-Parameter deklarieren, dann können Sie den speziellen `Body`-Parameter `embed` setzen:

```Python
item: Item = Body(embed=True)
```

so wie in:

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}

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

## Zusammenfassung { #recap }

Sie können mehrere Body-Parameter zu Ihrer *Pfadoperation-Funktion* hinzufügen, obwohl ein Request nur einen einzigen Body enthalten kann.

Aber **FastAPI** wird sich darum kümmern, Ihnen korrekte Daten in Ihrer Funktion zu überreichen, und das korrekte Schema in der *Pfadoperation* zu validieren und zu dokumentieren.

Sie können auch einzelne Werte deklarieren, die als Teil des Bodys empfangen werden.

Und Sie können **FastAPI** instruieren, den Body in einem Schlüssel unterzubringen, selbst wenn nur ein einzelner Body-Parameter deklariert ist.
