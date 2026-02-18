# Fortgeschrittene Python-Typen { #advanced-python-types }

Hier sind einige zusätzliche Ideen, die beim Arbeiten mit Python-Typen nützlich sein könnten.

## `Union` oder `Optional` verwenden { #using-union-or-optional }

Wenn Ihr Code aus irgendeinem Grund nicht `|` verwenden kann, z. B. wenn es nicht in einer Typannotation ist, sondern in etwas wie `response_model=`, können Sie anstelle des senkrechten Strichs (`|`) `Union` aus `typing` verwenden.

Zum Beispiel könnten Sie deklarieren, dass etwas ein `str` oder `None` sein könnte:

```python
from typing import Union


def say_hi(name: Union[str, None]):
        print(f"Hi {name}!")
```

`typing` hat außerdem eine Abkürzung, um zu deklarieren, dass etwas `None` sein könnte, mit `Optional`.

Hier ist ein Tipp aus meiner sehr **subjektiven** Perspektive:

* 🚨 Vermeiden Sie die Verwendung von `Optional[SomeType]`
* Verwenden Sie stattdessen ✨ **`Union[SomeType, None]`** ✨.

Beides ist äquivalent und unter der Haube identisch, aber ich würde `Union` statt `Optional` empfehlen, weil das Wort „**optional**“ implizieren könnte, dass der Wert optional ist; tatsächlich bedeutet es jedoch „es kann `None` sein“, selbst wenn es nicht optional ist und weiterhin erforderlich bleibt.

Ich finde, `Union[SomeType, None]` ist expliziter in dem, was es bedeutet.

Es geht nur um Wörter und Namen. Aber diese Wörter können beeinflussen, wie Sie und Ihr Team über den Code denken.

Als Beispiel nehmen wir diese Funktion:

```python
from typing import Optional


def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

Der Parameter `name` ist als `Optional[str]` definiert, aber er ist **nicht optional**, Sie können die Funktion nicht ohne den Parameter aufrufen:

```Python
say_hi()  # Oh nein, das löst einen Fehler aus! 😱
```

Der Parameter `name` ist **weiterhin erforderlich** (nicht *optional*), weil er keinen Defaultwert hat. Dennoch akzeptiert `name` den Wert `None`:

```Python
say_hi(name=None)  # Das funktioniert, None ist gültig 🎉
```

Die gute Nachricht ist: In den meisten Fällen können Sie einfach `|` verwenden, um Unions von Typen zu definieren:

```python
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

Sie müssen sich also normalerweise keine Gedanken über Namen wie `Optional` und `Union` machen. 😎
