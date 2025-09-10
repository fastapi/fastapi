# Testen mit Überschreibungen für Abhängigkeiten { #testing-dependencies-with-overrides }

## Abhängigkeiten beim Testen überschreiben { #overriding-dependencies-during-testing }

Es gibt einige Szenarien, in denen Sie beim Testen möglicherweise eine Abhängigkeit überschreiben möchten.

Sie möchten nicht, dass die ursprüngliche Abhängigkeit ausgeführt wird (und auch keine der möglicherweise vorhandenen Unterabhängigkeiten).

Stattdessen möchten Sie eine andere Abhängigkeit bereitstellen, die nur während Tests (möglicherweise nur bei einigen bestimmten Tests) verwendet wird und einen Wert bereitstellt, der dort verwendet werden kann, wo der Wert der ursprünglichen Abhängigkeit verwendet wurde.

### Anwendungsfälle: Externer Service { #use-cases-external-service }

Ein Beispiel könnte sein, dass Sie einen externen Authentifizierungsanbieter haben, mit dem Sie sich verbinden müssen.

Sie senden ihm ein Token und er gibt einen authentifizierten Benutzer zurück.

Dieser Anbieter berechnet Ihnen möglicherweise Gebühren pro <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr>, und der Aufruf könnte etwas länger dauern, als wenn Sie einen vordefinierten <abbr title="Platzhalter, vorgetäuscht, zum Schein">Mock</abbr>-Benutzer für Tests hätten.

Sie möchten den externen Anbieter wahrscheinlich einmal testen, ihn aber nicht unbedingt bei jedem weiteren ausgeführten Test aufrufen.

In diesem Fall können Sie die Abhängigkeit, die diesen Anbieter aufruft, überschreiben und eine benutzerdefinierte Abhängigkeit verwenden, die einen Mock-Benutzer zurückgibt, nur für Ihre Tests.

### Das Attribut `app.dependency_overrides` verwenden { #use-the-app-dependency-overrides-attribute }

Für diese Fälle verfügt Ihre **FastAPI**-Anwendung über das Attribut `app.dependency_overrides`, bei diesem handelt sich um ein einfaches <abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">`dict`</abbr>.

Um eine Abhängigkeit für das Testen zu überschreiben, geben Sie als Schlüssel die ursprüngliche Abhängigkeit (eine Funktion) und als Wert Ihre Überschreibung der Abhängigkeit (eine andere Funktion) ein.

Und dann ruft **FastAPI** diese Überschreibung anstelle der ursprünglichen Abhängigkeit auf.

{* ../../docs_src/dependency_testing/tutorial001_an_py310.py hl[26:27,30] *}

/// tip | Tipp

Sie können eine Überschreibung für eine Abhängigkeit festlegen, die an einer beliebigen Stelle in Ihrer **FastAPI**-Anwendung verwendet wird.

Die ursprüngliche Abhängigkeit könnte in einer *Pfadoperation-Funktion*, einem *Pfadoperation-Dekorator* (wenn Sie den Rückgabewert nicht verwenden), einem `.include_router()`-Aufruf, usw. verwendet werden.

FastAPI kann sie in jedem Fall überschreiben.

///

Anschließend können Sie Ihre Überschreibungen zurücksetzen (entfernen), indem Sie `app.dependency_overrides` auf ein leeres `dict` setzen:

```Python
app.dependency_overrides = {}
```


/// tip | Tipp

Wenn Sie eine Abhängigkeit nur während einiger Tests überschreiben möchten, können Sie die Überschreibung zu Beginn des Tests (innerhalb der Testfunktion) festlegen und am Ende (am Ende der Testfunktion) zurücksetzen.

///
