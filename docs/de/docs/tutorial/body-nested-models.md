# Body – Verschachtelte Modelle { #body-nested-models }

Mit **FastAPI** können Sie (dank Pydantic) beliebig tief verschachtelte Modelle definieren, validieren, dokumentieren und verwenden.

## Listen als Felder { #list-fields }

Sie können ein Attribut als Kindtyp definieren. Zum Beispiel eine Python-`list`:

{* ../../docs_src/body_nested_models/tutorial001_py310.py hl[12] *}

Das bewirkt, dass `tags` eine Liste ist, wenngleich es nichts über den Typ der Elemente der Liste aussagt.

## Listen mit Typ-Parametern als Felder { #list-fields-with-type-parameter }

Aber Python hat eine spezifische Möglichkeit, Listen mit inneren Typen, auch „Typ-Parameter“ genannt, zu deklarieren:

### Eine `list` mit einem Typ-Parameter deklarieren { #declare-a-list-with-a-type-parameter }

Um Typen zu deklarieren, die Typ-Parameter (innere Typen) haben, wie `list`, `dict`, `tuple`,
übergeben Sie den/die inneren Typ(en) als „Typ-Parameter“ in eckigen Klammern: `[` und `]`

```Python
my_list: list[str]
```

Das ist alles Standard-Python-Syntax für Typdeklarationen.

Verwenden Sie dieselbe Standardsyntax für Modellattribute mit inneren Typen.

In unserem Beispiel können wir also bewirken, dass `tags` spezifisch eine „Liste von Strings“ ist:

{* ../../docs_src/body_nested_models/tutorial002_py310.py hl[12] *}

## Set-Typen { #set-types }

Aber dann denken wir darüber nach und stellen fest, dass sich die Tags nicht wiederholen sollten, sie wären wahrscheinlich eindeutige Strings.

Und Python hat einen speziellen Datentyp für Mengen eindeutiger Elemente, das <abbr title="Menge">`set`</abbr>.

Dann können wir `tags` als Set von Strings deklarieren:

{* ../../docs_src/body_nested_models/tutorial003_py310.py hl[12] *}

Damit wird, selbst wenn Sie einen <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> mit duplizierten Daten erhalten, dieser zu einem Set eindeutiger Elemente konvertiert.

Und wann immer Sie diese Daten ausgeben, selbst wenn die Quelle Duplikate hatte, wird es als Set von eindeutigen Elementen ausgegeben.

Und es wird entsprechend annotiert / dokumentiert.

## Verschachtelte Modelle { #nested-models }

Jedes Attribut eines Pydantic-Modells hat einen Typ.

Aber dieser Typ kann selbst ein anderes Pydantic-Modell sein.

Sie können also tief verschachtelte JSON-„Objekte“ deklarieren, mit spezifischen Attributnamen, Typen und Validierungen.

Alles das beliebig tief verschachtelt.

### Ein Kindmodell definieren { #define-a-submodel }

Zum Beispiel können wir ein `Image`-Modell definieren:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[7:9] *}

### Das Kindmodell als Typ verwenden { #use-the-submodel-as-a-type }

Und dann können wir es als Typ eines Attributes verwenden:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[18] *}

Das würde bedeuten, dass **FastAPI** einen Body ähnlich dem folgenden erwartet:

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

Wiederum, nur mit dieser Deklaration erhalten Sie mit **FastAPI**:

* Editor-Unterstützung (Codevervollständigung, usw.), selbst für verschachtelte Modelle
* Datenkonvertierung
* Datenvalidierung
* Automatische Dokumentation

## Spezielle Typen und Validierungen { #special-types-and-validation }

Abgesehen von normalen einfachen Typen wie `str`, `int`, `float`, usw. können Sie komplexere einfache Typen verwenden, die von `str` erben.

Um alle Optionen kennenzulernen, die Sie haben, schauen Sie sich [Pydantics Typübersicht](https://docs.pydantic.dev/latest/concepts/types/) an. Sie werden einige Beispiele im nächsten Kapitel kennenlernen.

Zum Beispiel, da wir im `Image`-Modell ein Feld `url` haben, können wir deklarieren, dass das eine Instanz von Pydantics `HttpUrl` sein soll, anstelle eines `str`:

{* ../../docs_src/body_nested_models/tutorial005_py310.py hl[2,8] *}

Es wird getestet, ob der String eine gültige URL ist, und als solche wird er in JSON Schema / OpenAPI dokumentiert.

## Attribute mit Listen von Kindmodellen { #attributes-with-lists-of-submodels }

Sie können Pydantic-Modelle auch als Kindtypen von `list`, `set`, usw. verwenden:

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

/// note | Hinweis

Beachten Sie, dass der `images`-Schlüssel jetzt eine Liste von Bild-Objekten hat.

///

## Tief verschachtelte Modelle { #deeply-nested-models }

Sie können beliebig tief verschachtelte Modelle definieren:

{* ../../docs_src/body_nested_models/tutorial007_py310.py hl[7,12,18,21,25] *}

/// note | Hinweis

Beachten Sie, wie `Offer` eine Liste von `Item`s hat, die ihrerseits eine optionale Liste von `Image`s haben

///

## Bodys aus reinen Listen { #bodies-of-pure-lists }

Wenn der Wert auf oberster Ebene des JSON-Bodys, den Sie erwarten, ein JSON-`array` (eine Python-`list`) ist, können Sie den Typ im Parameter der Funktion deklarieren, genau wie in Pydantic-Modellen:

```Python
images: list[Image]
```

so wie in:

{* ../../docs_src/body_nested_models/tutorial008_py310.py hl[13] *}

## Editor-Unterstützung überall { #editor-support-everywhere }

Und Sie erhalten Editor-Unterstützung überall.

Selbst für Elemente innerhalb von Listen:

<img src="/img/tutorial/body-nested-models/image01.png">

Sie würden diese Art von Editor-Unterstützung nicht erhalten, wenn Sie direkt mit `dict`, statt mit Pydantic-Modellen arbeiten würden.

Aber Sie müssen sich auch nicht um diese kümmern, hereinkommende Dicts werden automatisch konvertiert und Ihre Ausgabe wird ebenfalls automatisch nach JSON konvertiert.

## Bodys mit beliebigen `dict`s { #bodies-of-arbitrary-dicts }

Sie können einen Body auch als `dict` deklarieren, mit Schlüsseln eines Typs und Werten eines anderen Typs.

So brauchen Sie vorher nicht zu wissen, wie die gültigen Feld-/Attributnamen lauten (wie es bei Pydantic-Modellen der Fall wäre).

Das ist nützlich, wenn Sie Schlüssel empfangen wollen, die Sie nicht bereits kennen.

---

Ein anderer nützlicher Anwendungsfall ist, wenn Sie Schlüssel eines anderen Typs haben wollen, z. B. `int`.

Das schauen wir uns hier an.

In diesem Fall akzeptieren Sie irgendein `dict`, solange es `int`-Schlüssel mit `float`-Werten hat:

{* ../../docs_src/body_nested_models/tutorial009_py310.py hl[7] *}

/// tip | Tipp

Bedenken Sie, dass JSON nur `str` als Schlüssel unterstützt.

Aber Pydantic hat automatische Datenkonvertierung.

Das bedeutet, dass Ihre API-Clients zwar nur Strings als Schlüssel senden können, Pydantic diese aber konvertieren und validieren wird, solange diese Strings nur Ganzzahlen enthalten.

Und das `dict`, welches Sie als `weights` erhalten, wird tatsächlich `int`-Schlüssel und `float`-Werte haben.

///

## Zusammenfassung { #recap }

Mit **FastAPI** haben Sie die maximale Flexibilität von Pydantic-Modellen, während Ihr Code einfach, kurz und elegant bleibt.

Aber mit all den Vorzügen:

* Editor-Unterstützung (Codevervollständigung überall!)
* Datenkonvertierung (auch bekannt als Parsen / Serialisierung)
* Datenvalidierung
* Schema-Dokumentation
* Automatische Dokumentation
