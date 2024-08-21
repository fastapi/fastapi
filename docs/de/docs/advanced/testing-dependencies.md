# Testen mit Ersatz für Abhängigkeiten

## Abhängigkeiten beim Testen überschreiben

Es gibt einige Szenarien, in denen Sie beim Testen möglicherweise eine Abhängigkeit überschreiben möchten.

Sie möchten nicht, dass die ursprüngliche Abhängigkeit ausgeführt wird (und auch keine der möglicherweise vorhandenen Unterabhängigkeiten).

Stattdessen möchten Sie eine andere Abhängigkeit bereitstellen, die nur während Tests (möglicherweise nur bei einigen bestimmten Tests) verwendet wird und einen Wert bereitstellt, der dort verwendet werden kann, wo der Wert der ursprünglichen Abhängigkeit verwendet wurde.

### Anwendungsfälle: Externer Service

Ein Beispiel könnte sein, dass Sie einen externen Authentifizierungsanbieter haben, mit dem Sie sich verbinden müssen.

Sie senden ihm ein Token und er gibt einen authentifizierten Benutzer zurück.

Dieser Anbieter berechnet Ihnen möglicherweise Gebühren pro Anfrage, und der Aufruf könnte etwas länger dauern, als wenn Sie einen vordefinierten Scheinbenutzer für Tests hätten.

Sie möchten den externen Anbieter wahrscheinlich einmal testen, ihn aber nicht unbedingt bei jedem weiteren ausgeführten Test aufrufen.

In diesem Fall können Sie die Abhängigkeit, die diesen Anbieter aufruft, überschreiben und eine benutzerdefinierte Abhängigkeit verwenden, die einen Scheinbenutzer zurückgibt, nur für Ihre Tests.

### Verwenden Sie das Attribut `app.dependency_overrides`.

Für diese Fälle verfügt Ihre **FastAPI**-Anwendung über das Attribut `app.dependency_overrides`, bei diesem handelt sich um ein einfaches `dict`.

Um eine Abhängigkeit für das Testen zu überschreiben, geben Sie als Schlüssel die ursprüngliche Abhängigkeit (eine Funktion) und als Wert Ihre Überschreibung der Abhängigkeit (eine andere Funktion) ein.

Und dann ruft **FastAPI** diese Überschreibung anstelle der ursprünglichen Abhängigkeit auf.

//// tab | Python 3.10+

```Python hl_lines="26-27  30"
{!> ../../../docs_src/dependency_testing/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="28-29  32"
{!> ../../../docs_src/dependency_testing/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="29-30  33"
{!> ../../../docs_src/dependency_testing/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="24-25  28"
{!> ../../../docs_src/dependency_testing/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="28-29  32"
{!> ../../../docs_src/dependency_testing/tutorial001.py!}
```

////

/// tip | "Tipp"

Sie können eine Überschreibung für eine Abhängigkeit festlegen, die an einer beliebigen Stelle in Ihrer **FastAPI**-Anwendung verwendet wird.

Die ursprüngliche Abhängigkeit könnte in einer *Pfadoperation-Funktion*, einem *Pfadoperation-Dekorator* (wenn Sie den Rückgabewert nicht verwenden), einem `.include_router()`-Aufruf, usw. verwendet werden.

FastAPI kann sie in jedem Fall überschreiben.

///

Anschließend können Sie Ihre Überschreibungen zurücksetzen (entfernen), indem Sie `app.dependency_overrides` auf ein leeres `dict` setzen:

```Python
app.dependency_overrides = {}
```

/// tip | "Tipp"

Wenn Sie eine Abhängigkeit nur während einiger Tests überschreiben möchten, können Sie die Überschreibung zu Beginn des Tests (innerhalb der Testfunktion) festlegen und am Ende (am Ende der Testfunktion) zurücksetzen.

///
