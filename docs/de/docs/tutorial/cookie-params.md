# Cookie-Parameter

So wie `Query`- und `Path`-Parameter können Sie auch <abbr title='Cookie – „Keks“: Mechanismus, der kurze Daten in Textform im Browser des Benutzers speichert und abfragt'>Cookie</abbr>-Parameter definieren.

## `Cookie` importieren

Importieren Sie zuerst `Cookie`:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## `Cookie`-Parameter deklarieren

Dann deklarieren Sie Ihre Cookie-Parameter, auf die gleiche Weise, wie Sie auch `Path`- und `Query`-Parameter deklarieren.

Der erste Wert ist der Typ. Sie können `Cookie` die gehabten Extra Validierungs- und Beschreibungsparameter hinzufügen. Danach können Sie einen Defaultwert vergeben:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | Technische Details

`Cookie` ist eine Schwesterklasse von `Path` und `Query`. Sie erbt von derselben gemeinsamen `Param`-Elternklasse.

Aber erinnern Sie sich, dass, wenn Sie `Query`, `Path`, `Cookie` und andere von `fastapi` importieren, diese tatsächlich Funktionen sind, welche spezielle Klassen zurückgeben.

///

/// info

Um Cookies zu deklarieren, müssen Sie `Cookie` verwenden, da diese Parameter sonst als Query-Parameter interpretiert werden würden.

///

## Zusammenfassung

Deklarieren Sie Cookies mittels `Cookie`, auf die gleiche Weise wie bei `Query` und `Path`.
