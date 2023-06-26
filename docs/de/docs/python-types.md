# Einführung in Python-Typen

Python unterstützt die optionalen "type hints".

Diese **"type hints"** sind eine spezielle Syntax, die es erlaubt, den <abbr title="zum Beispiel: str, int, float, bool">Typ</abbr> einer Variablen zu deklarieren.

Durch das Deklarieren von Typen für Ihre Variablen können Editoren und Tools bessere Unterstützung bieten.

Dies ist nur eine **schnelle Anleitung / Auffrischung** über Pythons Typ-Hinweise. Es deckt nur das Minimum ab, das nötig ist, um sie mit **FastAPI** zu verwenden... was eigentlich sehr wenig ist.

**FastAPI** basiert komplett auf diesen Typ-Hinweisen, sie geben der Anwendung viele Vorteile und Möglichkeiten.

Aber selbst wenn Sie **FastAPI** nie verwenden, würden Sie davon profitieren, ein wenig über sie zu lernen.

!!! note
    Wenn Sie ein Python-Experte sind und bereits alles über Typ-Hinweise wissen, überspringen Sie das nächste Kapitel.

## Motivation

Fangen wir mit einem einfachen Beispiel an:

```Python
{!../../../docs_src/python_types/tutorial001.py!}
```

Der Aufruf dieses Programms liefert die Ausgaben:

```
John Doe
```

Die Funktion bewirkt das Folgende:

* Nimmt einen `first_name` und `last_name`.
* Konvertiert den ersten Buchstaben von jedem in Großbuchstaben mit `title()`.
* <abbr title="Fügt sie zusammen, als eins. Mit dem Inhalt des einen nach dem anderen.">Verkettet sie mit einem Leerzeichen in der Mitte</abbr>.

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial001.py!}
```

### Bearbeite es

Es ist ein sehr einfaches Programm.

Aber nun stellen Sie sich vor, Sie würden es von Grund auf neu schreiben.

Irgendwann hätten Sie mit der Definition der Funktion begonnen, Sie hätten die Parameter parat...

Aber dann müssen Sie "die Methode aufrufen, die den ersten Buchstaben in Großbuchstaben umwandelt".

Was es `upper`? Was es `uppercase`? `first_uppercase`? `capitalize`?

Dann versuchen Sie es mit dem langjährigen Freund des Programmierers, der Editor-Autovervollständigung.

Sie geben den ersten Parameter der Funktion ein, `first_name`, dann einen Punkt (`.`) und drücken dann `Strg+Leertaste`, um die Vervollständigung auszulösen.

Aber leider erhalten Sie nichts Nützliches:

<img src="/img/python-types/image01.png">

### Typen hinzufügen

Lassen Sie uns eine einzelne Zeile aus der vorherigen Version ändern.

Wir werden genau diesen Teil, die Parameter der Funktion, ändern von:

```Python
    first_name, last_name
```

zu:

```Python
    first_name: str, last_name: str
```

Das war's.

Das sind die "Typ-Hinweise":

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial002.py!}
```

Das ist nicht dasselbe wie das Deklarieren von Standardwerten, wie es bei hier der Fall wäre:

```Python
    first_name="john", last_name="doe"
```

Das ist eine andere Sache.

Wir verwenden Doppelpunkte (`:`), nicht Gleichheitszeichen (`=`).

Und das Hinzufügen von Typ-Hinweisen ändert normalerweise nichts an dem, was ohne sie passieren würde.

Aber jetzt stellen Sie sich vor, Sie sind wieder mitten in der Erstellung dieser Funktion, aber mit Typ-Hinweisen.

An der gleichen Stelle versuchen Sie, die Autovervollständigung mit "Strg+Leertaste" auszulösen, und Sie sehen:

<img src="/img/python-types/image02.png">

Damit können Sie durch die Optionen blättern, bis Sie diejenige finden, bei der es "Klick" macht:

<img src="/img/python-types/image03.png">

## Mehr Motivation

Prüfen Sie diese Funktion, sie hat bereits Typ-Hinweise:

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial003.py!}
```

Da der Editor die Typen der Variablen kennt, erhalten Sie nicht nur eine Vervollständigung, sondern auch eine Fehlerprüfung:

<img src="/img/python-types/image04.png">

Da Sie nun wissen, dass Sie das Problem beheben müssen, konvertieren Sie `age` mit `str(age)` in eine Zeichenkette:

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial004.py!}
```

## Deklarieren von Typen

Sie haben gerade den wichtigsten Einsatzort für die Deklaration von Typ-Hinweisen gesehen. Als Funktionsparameter.

Dies ist auch der häufigste Bereich, in dem sie mit **FastAPI** verwendet werden.

### Einfache Typen

Sie können alle Standard Python-Typen deklarieren, nicht nur `str`.

Sie können z.B. folgende verwenden:

* `int`
* `float`
* `bool`
* `bytes`

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial005.py!}
```

### Generische Typen mit Typ-Parametern

Es gibt einige Datenstrukturen, die andere Werte enthalten können, wie `dict`, `list`, `set` und `tuple`. Und die internen Werte können auch ihren eigenen Typ haben.

Um diese Typen und die internen Typen zu deklarieren, können Sie das Standard Python-Modul `typing` verwenden.

Es existiert speziell für die Unterstützung dieser Typ-Hinweise.

#### `List`

Definieren wir zum Beispiel eine Variable, die eine `list` von `str` sein soll.

Von `typing`, importieren wir `List` (mit dem Großbuchstaben `L`):

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial006.py!}
```

Deklarieren Sie die Variable, mit der gleichen Doppelpunkt (`:`) Syntax.

Als Typ geben Sie `List` an.

Da die Liste ein Typ ist, der einige interne Typen enthält, setzen Sie diese in eckige Klammern:

```Python hl_lines="4"
{!../../../docs_src/python_types/tutorial006.py!}
```

!!! tip
    Die internen Typen in den eckigen Klammern werden als "Typparameter" bezeichnet.

    In diesem Fall ist `str` der Typparameter, der an `List` übergeben wird.

Das bedeutet: "die Variable `items` ist eine `list`, und jedes der Elemente in dieser Liste ist ein `str`".

Auf diese Weise kann Ihr Editor auch bei der Bearbeitung von Einträgen aus der Liste unterstützen:

<img src="/img/python-types/image05.png">

Ohne Typen ist das fast unmöglich zu erreichen.

Beachten Sie, dass die Variable `item` eines der Elemente in der Liste `items` ist.

Und trotzdem weiß der Editor, dass es sich um eine `str` handelt, und bietet entsprechende Unterstützung.

#### `Tuple` und `Set`

Das Gleiche gilt für die Deklaration von `Tuple` und `Set`:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial007.py!}
```

Das bedeutet:

* Die Variable `items_t` ist ein `Tupel` mit 3 Elementen, einem `int`, einem weiteren `int` und einem `str`.
* Die Variable `items_s` ist ein `set`, und jedes ihrer Elemente ist vom Typ `bytes`.

#### `Dict`

Um ein `dict` zu definieren, übergeben Sie 2 Typ-Parameter, getrennt durch Kommas.

Der erste Typ-Parameter ist für die Schlüssel des `dict`.

Der zweite Typ-Parameter ist für die Werte des `dict`:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial008.py!}
```

Dies bedeutet:

* Die Variable `prices` ist ein `dict`:
    * Die Schlüssel dieses `dict` sind vom Typ `str` (z.B. die Namen der einzelnen Artikel).
    * Die Werte dieses `dict` sind vom Typ `float` (z.B. der Preis jedes Artikels).

#### `Optional`

Sie können auch `Optional` verwenden, um zu deklarieren, dass eine Variable einen Typ hat, wie z. B. `str`, aber dass sie "optional" ist, was bedeutet, dass sie auch `None` sein könnte:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009.py!}
```

Wenn Sie `Optional[str]` statt nur `str` verwenden, kann der Editor Ihnen helfen, Fehler zu erkennen, bei denen Sie davon ausgehen, dass ein Wert immer ein `str` ist, obwohl er eigentlich auch `None` sein könnte.

#### Generische Typen

Diese Typen, die Typparameter in eckigen Klammern akzeptieren, wie:

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Optional`
* ...und andere.

werden **Generische Typen** oder **Generics** genannt.

### Klassen als Typen

Sie können auch eine Klasse als Typ einer Variablen deklarieren.

Nehmen wir an, Sie haben eine Klasse `Person`, mit einem Namen:

```Python hl_lines="1-3"
{!../../../docs_src/python_types/tutorial010.py!}
```

Dann können Sie eine Variable vom Typ `Person` deklarieren:

```Python hl_lines="6"
{!../../../docs_src/python_types/tutorial010.py!}
```

Und dann bekommen Sie wieder die volle Editorunterstützung:

<img src="/img/python-types/image06.png">

## Pydantic models

<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> ist eine Python-Bibliothek zur Durchführung von Datenvalidierung.

Sie deklarieren die "Form" der Daten als Klassen mit Attributen.

Und jedes Attribut hat einen Typ.

Dann erzeugen Sie eine Instanz dieser Klasse mit einigen Werten, und sie validiert die Werte, konvertiert sie in den passenden Typ (wenn das der Fall ist) und gibt Ihnen ein Objekt mit allen Daten.

Und Sie erhalten die gesamte Editor-Unterstützung mit diesem resultierenden Objekt.

Entnommen aus den offiziellen Pydantic-Dokumenten:

```Python
{!../../../docs_src/python_types/tutorial011.py!}
```

!!! info
    Um mehr über <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic zu erfahren, schauen Sie in die Dokumentation</a>.

Die **FastAPI** basiert komplett auf Pydantic.

Viel mehr von all dem in der Praxis werden Sie im [Tutorial - Benutzerhandbuch](tutorial/index.md){.internal-link target=_blank} sehen.

## Typ-Hinweise in **FastAPI**

**FastAPI** macht sich diese Typ-Hinweise zunutze, um mehrere Dinge zu tun.

Mit **FastAPI** deklarieren Sie Parameter mit Typ-Hinweisen und Sie erhalten:

* **Editor-Unterstützung**.
* **Typ-Prüfungen**.

...und **FastAPI** setzt die gleichen Deklarationen ein, um:

* **Anforderungen** definieren: aus Anfragepfad-Parametern, Abfrageparametern, Headern, Bodies, Abhängigkeiten, etc.
* **Daten umwandeln**: aus der Anfrage in den erforderlichen Typ.
* **Daten validieren**: aus jeder Anfrage:
    * **Automatische Fehler** generieren, die an den Client zurückgegeben werden, wenn die Daten ungültig sind.
* **Dokumentieren** der API mit OpenAPI:
    * die dann von den Benutzeroberflächen der automatischen interaktiven Dokumentation verwendet wird.

Das mag alles abstrakt klingen. Machen Sie sich keine Sorgen. Sie werden all dies in Aktion sehen im [Tutorial - Benutzerhandbuch](tutorial/index.md){.internal-link target=_blank}.

Das Wichtigste ist, dass **FastAPI** durch die Verwendung von Standard-Python-Typen an einer einzigen Stelle (anstatt weitere Klassen, Dekoratoren usw. hinzuzufügen) einen Großteil der Arbeit für Sie erledigen wird.

!!! info
    Wenn Sie bereits das ganze Tutorial durchgearbeitet haben und mehr über Typen erfahren wollen, dann ist eine gute Ressource <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">der "cheat sheet" von `mypy`</a>.
