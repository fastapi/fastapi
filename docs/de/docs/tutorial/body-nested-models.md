# Body – Verschachtelte Modelle { #body-nested-models }

Mit **FastAPI** können Sie (dank Pydantic) beliebig tief verschachtelte Modelle definieren, validieren, dokumentieren und verwenden.

## Listen als Felder { #list-fields }

Sie können ein Attribut als Kindtyp definieren, zum Beispiel eine Python-`list`.

{* ../../docs_src/body_nested_models/tutorial001_py310.py hl[12] *}

Das bewirkt, dass `tags` eine Liste ist, wenngleich es nichts über den Typ der Elemente der Liste aussagt.

## Listen mit Typ-Parametern als Felder { #list-fields-with-type-parameter }

Aber Python erlaubt es, Listen mit inneren Typen, auch „Typ-Parameter“ genannt, zu deklarieren.

### `List` von `typing` importieren { #import-typings-list }

In Python 3.9 oder darüber können Sie einfach `list` verwenden, um diese Typannotationen zu deklarieren, wie wir unten sehen werden. 💡

In Python-Versionen vor 3.9 (3.6 und darüber), müssen Sie zuerst `List` von Pythons Standardmodul `typing` importieren.

{* ../../docs_src/body_nested_models/tutorial002.py hl[1] *}

### Eine `list` mit einem Typ-Parameter deklarieren { #declare-a-list-with-a-type-parameter }

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

{* ../../docs_src/body_nested_models/tutorial002_py310.py hl[12] *}

## Set-Typen { #set-types }

Aber dann denken wir darüber nach und stellen fest, dass sich die Tags nicht wiederholen sollen, es sollen eindeutige Strings sein.

Python hat einen Datentyp speziell für Mengen eindeutiger Dinge: das <abbr title="Menge">`set`</abbr>.

Deklarieren wir also `tags` als Set von Strings.

{* ../../docs_src/body_nested_models/tutorial003_py310.py hl[12] *}

Jetzt, selbst wenn Sie einen <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> mit duplizierten Daten erhalten, werden diese zu einem Set eindeutiger Dinge konvertiert.

Und wann immer Sie diese Daten ausgeben, selbst wenn die Quelle Duplikate hatte, wird es als Set von eindeutigen Dingen ausgegeben.

Und es wird entsprechend annotiert/dokumentiert.

## Verschachtelte Modelle { #nested-models }

Jedes Attribut eines Pydantic-Modells hat einen Typ.

Aber dieser Typ kann selbst ein anderes Pydantic-Modell sein.

Sie können also tief verschachtelte JSON-„Objekte“ deklarieren, mit spezifischen Attributnamen, -typen, und -validierungen.

Alles das beliebig tief verschachtelt.

### Ein Kindmodell definieren { #define-a-submodel }

Für ein Beispiel können wir ein `Image`-Modell definieren.

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[7:9] *}

### Das Kindmodell als Typ verwenden { #use-the-submodel-as-a-type }

Und dann können wir es als Typ eines Attributes verwenden:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[18] *}

Das würde bedeuten, dass **FastAPI** einen Body wie folgt erwartet:

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

## Spezielle Typen und Validierungen { #special-types-and-validation }

Abgesehen von normalen einfachen Typen wie `str`, `int`, `float`, usw. können Sie komplexere einfache Typen verwenden, die von `str` erben.

Um alle Optionen kennenzulernen, die Sie haben, schauen Sie sich <a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">Pydantics Typübersicht</a> an. Sie werden einige Beispiele im nächsten Kapitel kennenlernen.

Zum Beispiel, da wir im `Image`-Modell ein Feld `url` haben, können wir deklarieren, dass das eine Instanz von Pydantics `HttpUrl` sein soll, anstelle eines `str`:

{* ../../docs_src/body_nested_models/tutorial005_py310.py hl[2,8] *}

Es wird getestet, ob der String eine gültige URL ist, und als solche wird er in JSON Schema / OpenAPI dokumentiert.

## Attribute mit Listen von Kindmodellen { #attributes-with-lists-of-submodels }

Sie können Pydantic-Modelle auch als Typen innerhalb von `list`, `set`, usw. verwenden:

{* ../../docs_src/body_nested_models/tutorial006_py310.py hl[18] *}

Das wird einen JSON-Body erwarten (konvertieren, validieren, dokumentieren, usw.) wie:

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

/// info | Info

Beachten Sie, dass der `images`-Schlüssel jetzt eine Liste von Bild-Objekten hat.

///

## Tief verschachtelte Modelle { #deeply-nested-models }

Sie können beliebig tief verschachtelte Modelle definieren:

{* ../../docs_src/body_nested_models/tutorial007_py310.py hl[7,12,18,21,25] *}

/// info | Info

Beachten Sie, wie `Offer` eine Liste von `Item`s hat, die ihrerseits eine optionale Liste von `Image`s haben.

///

## Bodys aus reinen Listen { #bodies-of-pure-lists }

Wenn das äußerste Element des JSON-Bodys, das Sie erwarten, ein JSON-`array` (eine Python-`list`) ist, können Sie den Typ im Funktionsparameter deklarieren, mit der gleichen Syntax wie in Pydantic-Modellen:

```Python
images: List[Image]
```

oder in Python 3.9 und darüber:

```Python
images: list[Image]
```

so wie in:

{* ../../docs_src/body_nested_models/tutorial008_py39.py hl[13] *}

## Editor-Unterstützung überall { #editor-support-everywhere }

Und Sie erhalten Editor-Unterstützung überall.

Selbst für Dinge in Listen:

<img src="/img/tutorial/body-nested-models/image01.png">

Sie würden diese Editor-Unterstützung nicht erhalten, wenn Sie direkt mit `dict`, statt mit Pydantic-Modellen arbeiten würden.

Aber Sie müssen sich auch nicht weiter um die Modelle kümmern, hereinkommende Dicts werden automatisch in sie konvertiert. Und was Sie zurückgeben, wird automatisch nach JSON konvertiert.

## Bodys mit beliebigen `dict`s { #bodies-of-arbitrary-dicts }

Sie können einen Body auch als `dict` deklarieren, mit Schlüsseln eines Typs und Werten eines anderen Typs.

So brauchen Sie vorher nicht zu wissen, wie die Feld-/Attributnamen lauten (wie es bei Pydantic-Modellen der Fall wäre).

Das ist nützlich, wenn Sie Schlüssel empfangen, deren Namen Sie nicht bereits kennen.

---

Ein anderer nützlicher Anwendungsfall ist, wenn Sie Schlüssel eines anderen Typs haben wollen, z. B. `int`.

Das schauen wir uns mal an.

Im folgenden Beispiel akzeptieren Sie irgendein `dict`, solange es `int`-Schlüssel und `float`-Werte hat:

{* ../../docs_src/body_nested_models/tutorial009_py39.py hl[7] *}

/// tip | Tipp

Bedenken Sie, dass JSON nur `str` als Schlüssel unterstützt.

Aber Pydantic hat automatische Datenkonvertierung.

Das bedeutet, dass Ihre API-Clients nur Strings senden können, aber solange diese Strings nur Zahlen enthalten, wird Pydantic sie konvertieren und validieren.

Und das `dict`, welches Sie als `weights` erhalten, wird `int`-Schlüssel und `float`-Werte haben.

///

## Zusammenfassung { #recap }

Mit **FastAPI** haben Sie die maximale Flexibilität von Pydantic-Modellen, während Ihr Code einfach, kurz und elegant bleibt.

Aber mit all den Vorzügen:

* Editor-Unterstützung (Codevervollständigung überall)
* Datenkonvertierung (auch bekannt als Parsen, Serialisierung)
* Datenvalidierung
* Schema-Dokumentation
* Automatische Dokumentation
