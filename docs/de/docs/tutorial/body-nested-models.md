# Body – Verschachtelte Modelle

Mit **FastAPI** können Sie (dank Pydantic) beliebig tief verschachtelte Modelle definieren, validieren und dokumentieren.

## Listen als Felder

Sie können ein Attribut als Kindtyp definieren, zum Beispiel eine Python-`list`e.

//// tab | Python 3.10+

```Python hl_lines="12"
{!> ../../../docs_src/body_nested_models/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="14"
{!> ../../../docs_src/body_nested_models/tutorial001.py!}
```

////

Das bewirkt, dass `tags` eine Liste ist, wenngleich es nichts über den Typ der Elemente der Liste aussagt.

## Listen mit Typ-Parametern als Felder

Aber Python erlaubt es, Listen mit inneren Typen, auch „Typ-Parameter“ genannt, zu deklarieren.

### `List` von `typing` importieren

In Python 3.9 oder darüber können Sie einfach `list` verwenden, um diese Typannotationen zu deklarieren, wie wir unten sehen werden. 💡

In Python-Versionen vor 3.9 (3.6 und darüber), müssen Sie zuerst `List` von Pythons Standardmodul `typing` importieren.

```Python hl_lines="1"
{!> ../../../docs_src/body_nested_models/tutorial002.py!}
```

### Eine `list`e mit einem Typ-Parameter deklarieren

Um Typen wie `list`, `dict`, `tuple` mit inneren Typ-Parametern (inneren Typen) zu deklarieren:

* Wenn Sie eine Python-Version kleiner als 3.9 verwenden, importieren Sie das Äquivalent zum entsprechenden Typ vom `typing`-Modul
* Überreichen Sie den/die inneren Typ(en) von eckigen Klammern umschlossen, `[` und `]`, als „Typ-Parameter“

In Python 3.9 wäre das:

```Python
my_list: list[str]
```

Und in Python-Versionen vor 3.9:

```Python
from typing import List

my_list: List[str]
```

Das ist alles Standard-Python-Syntax für Typdeklarationen.

Verwenden Sie dieselbe Standardsyntax für Modellattribute mit inneren Typen.

In unserem Beispiel können wir also bewirken, dass `tags` spezifisch eine „Liste von Strings“ ist:

//// tab | Python 3.10+

```Python hl_lines="12"
{!> ../../../docs_src/body_nested_models/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="14"
{!> ../../../docs_src/body_nested_models/tutorial002_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="14"
{!> ../../../docs_src/body_nested_models/tutorial002.py!}
```

////

## Set-Typen

Aber dann denken wir darüber nach und stellen fest, dass sich die Tags nicht wiederholen sollen, es sollen eindeutige Strings sein.

Python hat einen Datentyp speziell für Mengen eindeutiger Dinge: das <abbr title="Menge">`set`</abbr>.

Deklarieren wir also `tags` als Set von Strings.

//// tab | Python 3.10+

```Python hl_lines="12"
{!> ../../../docs_src/body_nested_models/tutorial003_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="14"
{!> ../../../docs_src/body_nested_models/tutorial003_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  14"
{!> ../../../docs_src/body_nested_models/tutorial003.py!}
```

////

Jetzt, selbst wenn Sie einen Request mit duplizierten Daten erhalten, werden diese zu einem Set eindeutiger Dinge konvertiert.

Und wann immer Sie diese Daten ausgeben, selbst wenn die Quelle Duplikate hatte, wird es als Set von eindeutigen Dingen ausgegeben.

Und es wird entsprechend annotiert/dokumentiert.

## Verschachtelte Modelle

Jedes Attribut eines Pydantic-Modells hat einen Typ.

Aber dieser Typ kann selbst ein anderes Pydantic-Modell sein.

Sie können also tief verschachtelte JSON-„Objekte“ deklarieren, mit spezifischen Attributnamen, -typen, und -validierungen.

Alles das beliebig tief verschachtelt.

### Ein Kindmodell definieren

Wir können zum Beispiel ein `Image`-Modell definieren.

//// tab | Python 3.10+

```Python hl_lines="7-9"
{!> ../../../docs_src/body_nested_models/tutorial004_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9-11"
{!> ../../../docs_src/body_nested_models/tutorial004_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9-11"
{!> ../../../docs_src/body_nested_models/tutorial004.py!}
```

////

### Das Kindmodell als Typ verwenden

Und dann können wir es als Typ eines Attributes verwenden.

//// tab | Python 3.10+

```Python hl_lines="18"
{!> ../../../docs_src/body_nested_models/tutorial004_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="20"
{!> ../../../docs_src/body_nested_models/tutorial004_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="20"
{!> ../../../docs_src/body_nested_models/tutorial004.py!}
```

////

Das würde bedeuten, dass **FastAPI** einen Body erwartet wie:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

Wiederum, nur mit dieser Deklaration erhalten Sie von **FastAPI**:

* Editor-Unterstützung (Codevervollständigung, usw.), selbst für verschachtelte Modelle
* Datenkonvertierung
* Datenvalidierung
* Automatische Dokumentation

## Spezielle Typen und Validierungen

Abgesehen von normalen einfachen Typen, wie `str`, `int`, `float`, usw. können Sie komplexere einfache Typen verwenden, die von `str` erben.

Um alle Optionen kennenzulernen, die Sie haben, schauen Sie sich <a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">Pydantics Typübersicht</a> an. Sie werden im nächsten Kapitel ein paar Beispiele kennenlernen.

Da wir zum Beispiel im `Image`-Modell ein Feld `url` haben, können wir deklarieren, dass das eine Instanz von Pydantics `HttpUrl` sein soll, anstelle eines `str`:

//// tab | Python 3.10+

```Python hl_lines="2  8"
{!> ../../../docs_src/body_nested_models/tutorial005_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="4  10"
{!> ../../../docs_src/body_nested_models/tutorial005_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="4  10"
{!> ../../../docs_src/body_nested_models/tutorial005.py!}
```

////

Es wird getestet, ob der String eine gültige URL ist, und als solche wird er in JSON Schema / OpenAPI dokumentiert.

## Attribute mit Listen von Kindmodellen

Sie können Pydantic-Modelle auch als Typen innerhalb von `list`, `set`, usw. verwenden:

//// tab | Python 3.10+

```Python hl_lines="18"
{!> ../../../docs_src/body_nested_models/tutorial006_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="20"
{!> ../../../docs_src/body_nested_models/tutorial006_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="20"
{!> ../../../docs_src/body_nested_models/tutorial006.py!}
```

////

Das wird einen JSON-Body erwarten (konvertieren, validieren, dokumentieren), wie:

```JSON hl_lines="11"
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
```

/// info

Beachten Sie, dass der `images`-Schlüssel jetzt eine Liste von Bild-Objekten hat.

///

## Tief verschachtelte Modelle

Sie können beliebig tief verschachtelte Modelle definieren:

//// tab | Python 3.10+

```Python hl_lines="7  12  18  21  25"
{!> ../../../docs_src/body_nested_models/tutorial007_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9  14  20  23  27"
{!> ../../../docs_src/body_nested_models/tutorial007_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9  14  20  23  27"
{!> ../../../docs_src/body_nested_models/tutorial007.py!}
```

////

/// info

Beachten Sie, wie `Offer` eine Liste von `Item`s hat, von denen jedes seinerseits eine optionale Liste von `Image`s hat.

///

## Bodys aus reinen Listen

Wenn Sie möchten, dass das äußerste Element des JSON-Bodys ein JSON-`array` (eine Python-`list`e) ist, können Sie den Typ im Funktionsparameter deklarieren, mit der gleichen Syntax wie in Pydantic-Modellen:

```Python
images: List[Image]
```

oder in Python 3.9 und darüber:

```Python
images: list[Image]
```

so wie in:

//// tab | Python 3.9+

```Python hl_lines="13"
{!> ../../../docs_src/body_nested_models/tutorial008_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="15"
{!> ../../../docs_src/body_nested_models/tutorial008.py!}
```

////

## Editor-Unterstützung überall

Und Sie erhalten Editor-Unterstützung überall.

Selbst für Dinge in Listen:

<img src="/img/tutorial/body-nested-models/image01.png">

Sie würden diese Editor-Unterstützung nicht erhalten, wenn Sie direkt mit `dict`, statt mit Pydantic-Modellen arbeiten würden.

Aber Sie müssen sich auch nicht weiter um die Modelle kümmern, hereinkommende Dicts werden automatisch in sie konvertiert. Und was Sie zurückgeben, wird automatisch nach JSON konvertiert.

## Bodys mit beliebigen `dict`s

Sie können einen Body auch als `dict` deklarieren, mit Schlüsseln eines Typs und Werten eines anderen Typs.

So brauchen Sie vorher nicht zu wissen, wie die Feld-/Attribut-Namen lauten (wie es bei Pydantic-Modellen der Fall wäre).

Das ist nützlich, wenn Sie Schlüssel empfangen, deren Namen Sie nicht bereits kennen.

---

Ein anderer nützlicher Anwendungsfall ist, wenn Sie Schlüssel eines anderen Typs haben wollen, z. B. `int`.

Das schauen wir uns mal an.

Im folgenden Beispiel akzeptieren Sie irgendein `dict`, solange es `int`-Schlüssel und `float`-Werte hat.

//// tab | Python 3.9+

```Python hl_lines="7"
{!> ../../../docs_src/body_nested_models/tutorial009_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9"
{!> ../../../docs_src/body_nested_models/tutorial009.py!}
```

////

/// tip | "Tipp"

Bedenken Sie, dass JSON nur `str` als Schlüssel unterstützt.

Aber Pydantic hat automatische Datenkonvertierung.

Das bedeutet, dass Ihre API-Clients nur Strings senden können, aber solange diese Strings nur Zahlen enthalten, wird Pydantic sie konvertieren und validieren.

Und das `dict` welches Sie als `weights` erhalten, wird `int`-Schlüssel und `float`-Werte haben.

///

## Zusammenfassung

Mit **FastAPI** haben Sie die maximale Flexibilität von Pydantic-Modellen, während Ihr Code einfach, kurz und elegant bleibt.

Aber mit all den Vorzügen:

* Editor-Unterstützung (Codevervollständigung überall)
* Datenkonvertierung (auch bekannt als Parsen, Serialisierung)
* Datenvalidierung
* Schema-Dokumentation
* Automatische Dokumentation
