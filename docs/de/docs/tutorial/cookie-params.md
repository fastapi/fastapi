# Cookie-Parameter { #cookie-parameters }

Sie können Cookie-Parameter auf die gleiche Weise definieren wie `Query`- und `Path`-Parameter.

## `Cookie` importieren { #import-cookie }

Importieren Sie zuerst `Cookie`:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## `Cookie`-Parameter deklarieren { #declare-cookie-parameters }

Deklarieren Sie dann die Cookie-Parameter mit derselben Struktur wie bei `Path` und `Query`.

Sie können den Defaultwert sowie alle zusätzlichen Validierungen oder Annotierungsparameter definieren:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | Technische Details

`Cookie` ist eine „Schwester“-Klasse von `Path` und `Query`. Sie erbt auch von derselben gemeinsamen `Param`-Klasse.

Aber denken Sie daran, dass, wenn Sie `Query`, `Path`, `Cookie` und andere von `fastapi` importieren, diese tatsächlich Funktionen sind, die spezielle Klassen zurückgeben.

///

/// info | Info

Um Cookies zu deklarieren, müssen Sie `Cookie` verwenden, da die Parameter sonst als Query-Parameter interpretiert würden.

///

## Zusammenfassung { #recap }

Deklarieren Sie Cookies mit `Cookie` und verwenden Sie dabei das gleiche allgemeine Muster wie bei `Query` und `Path`.
