# Query-Parameter

Wenn Sie in ihrer Funktion Parameter deklarieren, die nicht Teil der Pfad-Parameter sind, dann werden diese automatisch als „Query“-Parameter interpretiert.

```Python hl_lines="9"
{!../../../docs_src/query_params/tutorial001.py!}
```

Query-Parameter (Deutsch: Abfrage-Parameter) sind die Schlüssel-Wert-Paare, die nach dem `?` in einer URL aufgelistet sind, getrennt durch `&`-Zeichen.

Zum Beispiel sind in der URL:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

... die Query-Parameter:

* `skip`: mit dem Wert `0`
* `limit`: mit dem Wert `10`

Da sie Teil der URL sind, sind sie „naturgemäß“ Strings.

Aber wenn Sie sie mit Python-Typen deklarieren (im obigen Beispiel als `int`), werden sie zu diesem Typ konvertiert, und gegen diesen validiert.

Die gleichen Prozesse, die für Pfad-Parameter stattfinden, werden auch auf Query-Parameter angewendet:

* Editor Unterstützung (natürlich)
* <abbr title="Konvertieren des Strings, der von einer HTTP-Anfrage kommt, in Python-Daten">„Parsen“</abbr> der Daten
* Datenvalidierung
* Automatische Dokumentation

## Defaultwerte

Da Query-Parameter nicht ein festgelegter Teil des Pfades sind, können sie optional sein und Defaultwerte haben.

Im obigen Beispiel haben sie die Defaultwerte `skip=0` und `limit=10`.

Wenn Sie also zur URL:

```
http://127.0.0.1:8000/items/
```

gehen, so ist das das gleiche wie die URL:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

Aber wenn Sie zum Beispiel zu:

```
http://127.0.0.1:8000/items/?skip=20
```

gehen, werden die Parameter-Werte Ihrer Funktion sein:

* `skip=20`: da Sie das in der URL gesetzt haben
* `limit=10`: weil das der Defaultwert ist

## Optionale Parameter

Auf die gleiche Weise können Sie optionale Query-Parameter deklarieren, indem Sie deren Defaultwert auf `None` setzen:

//// tab | Python 3.10+

```Python hl_lines="7"
{!> ../../../docs_src/query_params/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9"
{!> ../../../docs_src/query_params/tutorial002.py!}
```

////

In diesem Fall wird der Funktionsparameter `q` optional, und standardmäßig `None` sein.

/// check

Beachten Sie auch, dass **FastAPI** intelligent genug ist, um zu erkennen, dass `item_id` ein Pfad-Parameter ist und `q` keiner, daher muss letzteres ein Query-Parameter sein.

///

## Query-Parameter Typkonvertierung

Sie können auch `bool`-Typen deklarieren und sie werden konvertiert:

//// tab | Python 3.10+

```Python hl_lines="7"
{!> ../../../docs_src/query_params/tutorial003_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9"
{!> ../../../docs_src/query_params/tutorial003.py!}
```

////

Wenn Sie nun zu:

```
http://127.0.0.1:8000/items/foo?short=1
```

oder

```
http://127.0.0.1:8000/items/foo?short=True
```

oder

```
http://127.0.0.1:8000/items/foo?short=true
```

oder

```
http://127.0.0.1:8000/items/foo?short=on
```

oder

```
http://127.0.0.1:8000/items/foo?short=yes
```

gehen, oder zu irgendeiner anderen Variante der Groß-/Kleinschreibung (Alles groß, Anfangsbuchstabe groß, usw.), dann wird Ihre Funktion den Parameter `short` mit dem `bool`-Wert `True` sehen, ansonsten mit dem Wert `False`.

## Mehrere Pfad- und Query-Parameter

Sie können mehrere Pfad-Parameter und Query-Parameter gleichzeitig deklarieren, **FastAPI** weiß, was welches ist.

Und Sie müssen sie auch nicht in einer spezifischen Reihenfolge deklarieren.

Parameter werden anhand ihres Namens erkannt:

//// tab | Python 3.10+

```Python hl_lines="6  8"
{!> ../../../docs_src/query_params/tutorial004_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8  10"
{!> ../../../docs_src/query_params/tutorial004.py!}
```

////

## Erforderliche Query-Parameter

Wenn Sie einen Defaultwert für Nicht-Pfad-Parameter deklarieren (Bis jetzt haben wir nur Query-Parameter gesehen), dann ist der Parameter nicht erforderlich.

Wenn Sie keinen spezifischen Wert haben wollen, sondern der Parameter einfach optional sein soll, dann setzen Sie den Defaultwert auf `None`.

Aber wenn Sie wollen, dass ein Query-Parameter erforderlich ist, vergeben Sie einfach keinen Defaultwert:

```Python hl_lines="6-7"
{!../../../docs_src/query_params/tutorial005.py!}
```

Hier ist `needy` ein erforderlicher Query-Parameter vom Typ `str`.

Wenn Sie in Ihrem Browser eine URL wie:

```
http://127.0.0.1:8000/items/foo-item
```

... öffnen, ohne den benötigten Parameter `needy`, dann erhalten Sie einen Fehler wie den folgenden:

```JSON
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "needy"
      ],
      "msg": "Field required",
      "input": null,
      "url": "https://errors.pydantic.dev/2.1/v/missing"
    }
  ]
}
```

Da `needy` ein erforderlicher Parameter ist, müssen Sie ihn in der URL setzen:

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

... Das funktioniert:

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

Und natürlich können Sie einige Parameter als erforderlich, einige mit Defaultwert, und einige als vollständig optional definieren:

//// tab | Python 3.10+

```Python hl_lines="8"
{!> ../../../docs_src/query_params/tutorial006_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10"
{!> ../../../docs_src/query_params/tutorial006.py!}
```

////

In diesem Fall gibt es drei Query-Parameter:

* `needy`, ein erforderlicher `str`.
* `skip`, ein `int` mit einem Defaultwert `0`.
* `limit`, ein optionales `int`.

/// tip | "Tipp"

Sie können auch `Enum`s verwenden, auf die gleiche Weise wie mit [Pfad-Parametern](path-params.md#vordefinierte-parameterwerte){.internal-link target=_blank}.

///
