# Einführung in Python-Typen { #python-types-intro }

Python hat Unterstützung für optionale <abbr title="englisch: Type hints">„Typhinweise“</abbr> (auch <abbr title="englisch: Type annotations">„Typannotationen“</abbr> genannt).

Diese **„Typhinweise“** oder -Annotationen sind eine spezielle Syntax, die es erlaubt, den <abbr title="zum Beispiel: str, int, float, bool">Typ</abbr> einer Variablen zu deklarieren.

Durch das Deklarieren von Typen für Ihre Variablen können Editoren und Tools bessere Unterstützung bieten.

Dies ist lediglich eine **schnelle Anleitung / Auffrischung** über Pythons Typhinweise. Sie deckt nur das Minimum ab, das nötig ist, um diese mit **FastAPI** zu verwenden ... was tatsächlich sehr wenig ist.

**FastAPI** basiert vollständig auf diesen Typhinweisen, sie geben der Anwendung viele Vorteile und Möglichkeiten.

Aber selbst wenn Sie **FastAPI** nie verwenden, wird es für Sie nützlich sein, ein wenig darüber zu lernen.

/// note | Hinweis

Wenn Sie ein Python-Experte sind und bereits alles über Typhinweise wissen, überspringen Sie dieses Kapitel und fahren Sie mit dem nächsten fort.

///

## Motivation { #motivation }

Fangen wir mit einem einfachen Beispiel an:

{* ../../docs_src/python_types/tutorial001.py *}

Dieses Programm gibt aus:

```
John Doe
```

Die Funktion macht Folgendes:

* Nimmt einen `first_name` und `last_name`.
* Schreibt den ersten Buchstaben eines jeden Wortes groß, mithilfe von `title()`.
* <abbr title="Füge zu einer Einheit zusammen, eins nach dem anderen.">Verkettet</abbr> sie mit einem Leerzeichen in der Mitte.

{* ../../docs_src/python_types/tutorial001.py hl[2] *}

### Es bearbeiten { #edit-it }

Es ist ein sehr einfaches Programm.

Aber nun stellen Sie sich vor, Sie würden es selbst schreiben.

Irgendwann sind die Funktions-Parameter fertig, Sie starten mit der Definition des Körpers ...

Aber dann müssen Sie „diese Methode aufrufen, die den ersten Buchstaben in Großbuchstaben umwandelt“.

War es `upper`? War es `uppercase`? `first_uppercase`? `capitalize`?

Dann versuchen Sie es mit dem langjährigen Freund des Programmierers, der Editor-Autovervollständigung.

Sie geben den ersten Parameter der Funktion ein, `first_name`, dann einen Punkt (`.`) und drücken `Strg+Leertaste`, um die Vervollständigung auszulösen.

Aber leider erhalten Sie nichts Nützliches:

<img src="/img/python-types/image01.png">

### Typen hinzufügen { #add-types }

Lassen Sie uns eine einzelne Zeile aus der vorherigen Version ändern.

Wir ändern den folgenden Teil, die Parameter der Funktion, von:

```Python
    first_name, last_name
```

zu:

```Python
    first_name: str, last_name: str
```

Das war's.

Das sind die „Typhinweise“:

{* ../../docs_src/python_types/tutorial002.py hl[1] *}

Das ist nicht das gleiche wie das Deklarieren von Defaultwerten, wie es hier der Fall ist:

```Python
    first_name="john", last_name="doe"
```

Das ist eine andere Sache.

Wir verwenden Doppelpunkte (`:`), nicht Gleichheitszeichen (`=`).

Und das Hinzufügen von Typhinweisen ändert normalerweise nichts an dem, was ohne sie passieren würde.

Aber jetzt stellen Sie sich vor, Sie sind wieder mitten in der Erstellung dieser Funktion, aber mit Typhinweisen.

An derselben Stelle versuchen Sie, die Autovervollständigung mit „Strg+Leertaste“ auszulösen, und Sie sehen:

<img src="/img/python-types/image02.png">

Hier können Sie durch die Optionen blättern, bis Sie diejenige finden, bei der es „Klick“ macht:

<img src="/img/python-types/image03.png">

## Mehr Motivation { #more-motivation }

Sehen Sie sich diese Funktion an, sie hat bereits Typhinweise:

{* ../../docs_src/python_types/tutorial003.py hl[1] *}

Da der Editor die Typen der Variablen kennt, erhalten Sie nicht nur Code-Vervollständigung, sondern auch eine Fehlerprüfung:

<img src="/img/python-types/image04.png">

Jetzt, da Sie wissen, dass Sie das reparieren müssen, konvertieren Sie `age` mittels `str(age)` in einen String:

{* ../../docs_src/python_types/tutorial004.py hl[2] *}

## Deklarieren von Typen { #declaring-types }

Sie haben gerade den Haupt-Einsatzort für die Deklaration von Typhinweisen gesehen. Als Funktionsparameter.

Das ist auch meistens, wie sie in **FastAPI** verwendet werden.

### Einfache Typen { #simple-types }

Sie können alle Standard-Python-Typen deklarieren, nicht nur `str`.

Zum Beispiel diese:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005.py hl[1] *}

### Generische Typen mit Typ-Parametern { #generic-types-with-type-parameters }

Es gibt Datenstrukturen, die andere Werte enthalten können, wie etwa `dict`, `list`, `set` und `tuple`. Die inneren Werte können auch ihren eigenen Typ haben.

Diese Typen mit inneren Typen werden „**generische**“ Typen genannt. Es ist möglich, sie mit ihren inneren Typen zu deklarieren.

Um diese Typen und die inneren Typen zu deklarieren, können Sie Pythons Standardmodul `typing` verwenden. Es existiert speziell für die Unterstützung dieser Typhinweise.

#### Neuere Python-Versionen { #newer-versions-of-python }

Die Syntax, welche `typing` verwendet, ist **kompatibel** mit allen Versionen, von Python 3.6 aufwärts zu den neuesten, inklusive Python 3.9, Python 3.10, usw.

Mit der Weiterentwicklung von Python kommen **neuere Versionen** heraus, mit verbesserter Unterstützung für Typannotationen, und in vielen Fällen müssen Sie gar nicht mehr das `typing`-Modul importieren, um Typannotationen zu schreiben.

Wenn Sie eine neuere Python-Version für Ihr Projekt wählen können, werden Sie aus dieser zusätzlichen Vereinfachung Nutzen ziehen können.

In der gesamten Dokumentation gibt es Beispiele, welche kompatibel mit unterschiedlichen Python-Versionen sind (wenn es Unterschiede gibt).

Zum Beispiel bedeutet „**Python 3.6+**“, dass das Beispiel kompatibel mit Python 3.6 oder höher ist (inklusive 3.7, 3.8, 3.9, 3.10, usw.). Und „**Python 3.9+**“ bedeutet, es ist kompatibel mit Python 3.9 oder höher (inklusive 3.10, usw.).

Wenn Sie über die **neueste Version von Python** verfügen, verwenden Sie die Beispiele für die neueste Version, diese werden die **beste und einfachste Syntax** haben, zum Beispiel, „**Python 3.10+**“.

#### Liste { #list }

Definieren wir zum Beispiel eine Variable, die eine `list` von `str` – eine Liste von Strings – sein soll.

//// tab | Python 3.9+

Deklarieren Sie die Variable mit der gleichen Doppelpunkt-Syntax (`:`).

Als Typ nehmen Sie `list`.

Da die Liste ein Typ ist, welcher innere Typen enthält, werden diese von eckigen Klammern umfasst:

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial006_py39.py!}
```

////

//// tab | Python 3.8+

Von `typing` importieren Sie `List` (mit Großbuchstaben `L`):

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial006.py!}
```

Deklarieren Sie die Variable mit der gleichen Doppelpunkt-Syntax (`:`).

Als Typ nehmen Sie das `List`, das Sie von `typing` importiert haben.

Da die Liste ein Typ ist, welcher innere Typen enthält, werden diese von eckigen Klammern umfasst:

```Python hl_lines="4"
{!> ../../docs_src/python_types/tutorial006.py!}
```

////

/// info | Info

Die inneren Typen in den eckigen Klammern werden als „Typ-Parameter“ bezeichnet.

In diesem Fall ist `str` der Typ-Parameter, der an `List` übergeben wird (oder `list` in Python 3.9 und darüber).

///

Das bedeutet: Die Variable `items` ist eine Liste – `list` – und jedes der Elemente in dieser Liste ist ein String – `str`.

/// tip | Tipp

Wenn Sie Python 3.9 oder höher verwenden, müssen Sie `List` nicht von `typing` importieren, Sie können stattdessen den regulären `list`-Typ verwenden.

///

Auf diese Weise kann Ihr Editor Sie auch bei der Bearbeitung von Einträgen aus der Liste unterstützen:

<img src="/img/python-types/image05.png">

Ohne Typen ist das fast unmöglich zu erreichen.

Beachten Sie, dass die Variable `item` eines der Elemente in der Liste `items` ist.

Und trotzdem weiß der Editor, dass es sich um ein `str` handelt, und bietet entsprechende Unterstützung.

#### Tupel und Menge { #tuple-and-set }

Das Gleiche gilt für die Deklaration eines Tupels – `tuple` – und einer Menge – `set`:

//// tab | Python 3.9+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial007_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial007.py!}
```

////

Das bedeutet:

* Die Variable `items_t` ist ein `tuple` mit 3 Elementen, einem `int`, einem weiteren `int` und einem `str`.
* Die Variable `items_s` ist ein `set`, und jedes seiner Elemente ist vom Typ `bytes`.

#### Dict { #dict }

Um ein `dict` zu definieren, übergeben Sie zwei Typ-Parameter, getrennt durch Kommas.

Der erste Typ-Parameter ist für die Schlüssel des `dict`.

Der zweite Typ-Parameter ist für die Werte des `dict`:

//// tab | Python 3.9+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial008.py!}
```

////

Das bedeutet:

* Die Variable `prices` ist ein `dict`:
    * Die Schlüssel dieses `dict` sind vom Typ `str` (z. B. die Namen der einzelnen Artikel).
    * Die Werte dieses `dict` sind vom Typ `float` (z. B. der Preis jedes Artikels).

#### <abbr title="Union – Verbund, Einheit‚ Vereinigung: Eines von Mehreren">Union</abbr> { #union }

Sie können deklarieren, dass eine Variable einer von **verschiedenen Typen** sein kann, zum Beispiel ein `int` oder ein `str`.

In Python 3.6 und höher (inklusive Python 3.10) können Sie den `Union`-Typ von `typing` verwenden und die möglichen Typen innerhalb der eckigen Klammern auflisten.

In Python 3.10 gibt es zusätzlich eine **neue Syntax**, die es erlaubt, die möglichen Typen getrennt von einem <abbr title='Allgemein: „oder“. In anderem Zusammenhang auch „Bitweises ODER“, aber letztere Bedeutung ist hier nicht relevant'>vertikalen Balken (`|`)</abbr> aufzulisten.

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial008b.py!}
```

////

In beiden Fällen bedeutet das, dass `item` ein `int` oder ein `str` sein kann.

#### Vielleicht `None` { #possibly-none }

Sie können deklarieren, dass ein Wert ein `str`, aber vielleicht auch `None` sein kann.

In Python 3.6 und darüber (inklusive Python 3.10) können Sie das deklarieren, indem Sie `Optional` vom `typing` Modul importieren und verwenden.

```Python hl_lines="1  4"
{!../../docs_src/python_types/tutorial009.py!}
```

Wenn Sie `Optional[str]` anstelle von nur `str` verwenden, wird Ihr Editor Ihnen dabei helfen, Fehler zu erkennen, bei denen Sie annehmen könnten, dass ein Wert immer eine String (`str`) ist, obwohl er auch `None` sein könnte.

`Optional[Something]` ist tatsächlich eine Abkürzung für `Union[Something, None]`, diese beiden sind äquivalent.

Das bedeutet auch, dass Sie in Python 3.10 `Something | None` verwenden können:

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009.py!}
```

////

//// tab | Python 3.8+ Alternative

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009b.py!}
```

////

#### `Union` oder `Optional` verwenden? { #using-union-or-optional }

Wenn Sie eine Python-Version unterhalb 3.10 verwenden, hier ist mein sehr **subjektiver** Standpunkt dazu:

* 🚨 Vermeiden Sie `Optional[SomeType]`
* Stattdessen ✨ **verwenden Sie `Union[SomeType, None]`** ✨.

Beide sind äquivalent und im Hintergrund dasselbe, aber ich empfehle `Union` statt `Optional`, weil das Wort „**optional**“ impliziert, dass dieser Wert, zum Beispiel als Funktionsparameter, optional ist. Tatsächlich bedeutet es aber nur „Der Wert kann `None` sein“, selbst wenn der Wert nicht optional ist und benötigt wird.

Ich denke, `Union[SomeType, None]` ist expliziter bezüglich seiner Bedeutung.

Es geht nur um Wörter und Namen. Aber diese Worte können beeinflussen, wie Sie und Ihre Teamkollegen über den Code denken.

Nehmen wir zum Beispiel diese Funktion:

{* ../../docs_src/python_types/tutorial009c.py hl[1,4] *}

Der Parameter `name` ist definiert als `Optional[str]`, aber er ist **nicht optional**, Sie können die Funktion nicht ohne diesen Parameter aufrufen:

```Python
say_hi()  # Oh, nein, das löst einen Fehler aus! 😱
```

Der `name` Parameter wird **immer noch benötigt** (nicht *optional*), weil er keinen Default-Wert hat. `name` akzeptiert aber dennoch `None` als Wert:

```Python
say_hi(name=None)  # Das funktioniert, None ist gültig 🎉
```

Die gute Nachricht ist, dass Sie sich darüber keine Sorgen mehr machen müssen, wenn Sie Python 3.10 verwenden, da Sie einfach `|` verwenden können, um Vereinigungen von Typen zu definieren:

{* ../../docs_src/python_types/tutorial009c_py310.py hl[1,4] *}

Und dann müssen Sie sich nicht mehr um Namen wie `Optional` und `Union` kümmern. 😎

#### Generische Typen { #generic-types }

Diese Typen, die Typ-Parameter in eckigen Klammern akzeptieren, werden **generische Typen** oder **Generics** genannt.

//// tab | Python 3.10+

Sie können die eingebauten Typen als Generics verwenden (mit eckigen Klammern und Typen darin):

* `list`
* `tuple`
* `set`
* `dict`

Verwenden Sie für den Rest, wie unter Python 3.8, das `typing`-Modul:

* `Union`
* `Optional` (so wie unter Python 3.8)
* ... und andere.

In Python 3.10 können Sie als Alternative zu den Generics `Union` und `Optional` den <abbr title='Allgemein: „oder“. In anderem Zusammenhang auch „Bitweises ODER“, aber letztere Bedeutung ist hier nicht relevant'>vertikalen Balken (`|`)</abbr> verwenden, um Vereinigungen von Typen zu deklarieren, das ist besser und einfacher.

////

//// tab | Python 3.9+

Sie können die eingebauten Typen als Generics verwenden (mit eckigen Klammern und Typen darin):

* `list`
* `tuple`
* `set`
* `dict`

Verwenden Sie für den Rest, wie unter Python 3.8, das `typing`-Modul:

* `Union`
* `Optional`
* ... und andere.

////

//// tab | Python 3.8+

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Union`
* `Optional`
* ... und andere.

////

### Klassen als Typen { #classes-as-types }

Sie können auch eine Klasse als Typ einer Variablen deklarieren.

Nehmen wir an, Sie haben eine Klasse `Person`, mit einem Namen:

{* ../../docs_src/python_types/tutorial010.py hl[1:3] *}

Dann können Sie eine Variable vom Typ `Person` deklarieren:

{* ../../docs_src/python_types/tutorial010.py hl[6] *}

Und wiederum bekommen Sie die volle Editor-Unterstützung:

<img src="/img/python-types/image06.png">

Beachten Sie, das bedeutet: „`one_person` ist eine **Instanz** der Klasse `Person`“.

Es bedeutet nicht: „`one_person` ist die **Klasse** genannt `Person`“.

## Pydantic-Modelle { #pydantic-models }

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> ist eine Python-Bibliothek für die Validierung von Daten.

Sie deklarieren die „Form“ der Daten als Klassen mit Attributen.

Und jedes Attribut hat einen Typ.

Dann erzeugen Sie eine Instanz dieser Klasse mit einigen Werten, und Pydantic validiert die Werte, konvertiert sie in den passenden Typ (falls notwendig) und gibt Ihnen ein Objekt mit allen Daten.

Und Sie erhalten volle Editor-Unterstützung für dieses Objekt.

Ein Beispiel aus der offiziellen Pydantic Dokumentation:

//// tab | Python 3.10+

```Python
{!> ../../docs_src/python_types/tutorial011_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!> ../../docs_src/python_types/tutorial011_py39.py!}
```

////

//// tab | Python 3.8+

```Python
{!> ../../docs_src/python_types/tutorial011.py!}
```

////

/// info | Info

Um mehr über <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic zu erfahren, schauen Sie sich dessen Dokumentation an</a>.

///

**FastAPI** basiert vollständig auf Pydantic.

Viel mehr von all dem werden Sie in praktischer Anwendung im [Tutorial – Benutzerhandbuch](tutorial/index.md){.internal-link target=_blank} sehen.

/// tip | Tipp

Pydantic verhält sich speziell, wenn Sie `Optional` oder `Union[Something, None]` ohne einen Defaultwert verwenden. Sie können darüber in der Pydantic Dokumentation unter <a href="https://docs.pydantic.dev/2.3/usage/models/#required-fields" class="external-link" target="_blank">Erforderliche optionale Felder</a> mehr erfahren.

///

## Typhinweise mit Metadaten-Annotationen { #type-hints-with-metadata-annotations }

Python bietet auch die Möglichkeit, **zusätzliche <abbr title="Daten über die Daten, in diesem Fall Informationen über den Typ, z. B. eine Beschreibung.">Metadaten</abbr>** in Typhinweisen unterzubringen, mittels `Annotated`.

//// tab | Python 3.9+

In Python 3.9 ist `Annotated` ein Teil der Standardbibliothek, Sie können es von `typing` importieren.

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial013_py39.py!}
```

////

//// tab | Python 3.8+

In Versionen niedriger als Python 3.9 importieren Sie `Annotated` von `typing_extensions`.

Es wird bereits mit **FastAPI** installiert sein.

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial013.py!}
```

////

Python selbst macht nichts mit `Annotated`. Für Editoren und andere Tools ist der Typ immer noch `str`.

Aber Sie können `Annotated` nutzen, um **FastAPI** mit Metadaten zu versorgen, die ihm sagen, wie sich Ihre Anwendung verhalten soll.

Wichtig ist, dass **der erste *Typ-Parameter***, den Sie `Annotated` übergeben, der **tatsächliche Typ** ist. Der Rest sind Metadaten für andere Tools.

Im Moment müssen Sie nur wissen, dass `Annotated` existiert, und dass es Standard-Python ist. 😎

Später werden Sie sehen, wie **mächtig** es sein kann.

/// tip | Tipp

Der Umstand, dass es **Standard-Python** ist, bedeutet, dass Sie immer noch die **bestmögliche Entwickler-Erfahrung** in Ihrem Editor haben, sowie mit den Tools, die Sie nutzen, um Ihren Code zu analysieren, zu refaktorisieren, usw. ✨

Und ebenfalls, dass Ihr Code sehr kompatibel mit vielen anderen Python-Tools und -Bibliotheken sein wird. 🚀

///

## Typhinweise in **FastAPI** { #type-hints-in-fastapi }

**FastAPI** macht sich diese Typhinweise zunutze, um mehrere Dinge zu tun.

Mit **FastAPI** deklarieren Sie Parameter mit Typhinweisen, und Sie erhalten:

* **Editorunterstützung**.
* **Typ-Prüfungen**.

... und **FastAPI** verwendet dieselben Deklarationen, um:

* **Anforderungen** zu definieren: aus <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr>-Pfadparametern, Query-Parametern, Header-Feldern, Bodys, Abhängigkeiten, usw.
* **Daten umzuwandeln**: aus dem Request in den erforderlichen Typ.
* **Daten zu validieren**: aus jedem Request:
    * **Automatische Fehler** generieren, die an den Client zurückgegeben werden, wenn die Daten ungültig sind.
* Die API mit OpenAPI zu **dokumentieren**:
    * Die dann von den Benutzeroberflächen der automatisch generierten interaktiven Dokumentation verwendet wird.

Das mag alles abstrakt klingen. Machen Sie sich keine Sorgen. Sie werden all das in Aktion sehen im [Tutorial – Benutzerhandbuch](tutorial/index.md){.internal-link target=_blank}.

Das Wichtigste ist, dass **FastAPI** durch die Verwendung von Standard-Python-Typen an einer einzigen Stelle (anstatt weitere Klassen, Dekoratoren usw. hinzuzufügen) einen Großteil der Arbeit für Sie erledigt.

/// info | Info

Wenn Sie bereits das ganze Tutorial durchgearbeitet haben und mehr über Typen erfahren wollen, dann ist eine gute Ressource <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">der „Cheat Sheet“ von `mypy`</a>.

///
