# Fortgeschrittene Abhängigkeiten { #advanced-dependencies }

## Parametrisierte Abhängigkeiten { #parameterized-dependencies }

Alle Abhängigkeiten, die wir bisher gesehen haben, waren festgelegte Funktionen oder Klassen.

Es kann jedoch Fälle geben, in denen Sie Parameter für eine Abhängigkeit festlegen möchten, ohne viele verschiedene Funktionen oder Klassen zu deklarieren.

Stellen wir uns vor, wir möchten eine Abhängigkeit haben, die prüft, ob ein Query-Parameter `q` einen vordefinierten Inhalt hat.

Aber wir wollen diesen vordefinierten Inhalt per Parameter festlegen können.

## Eine „aufrufbare“ Instanz { #a-callable-instance }

In Python gibt es eine Möglichkeit, eine Instanz einer Klasse <abbr title="Englisch „callable“">„aufrufbar“</abbr> zu machen.

Nicht die Klasse selbst (die bereits aufrufbar ist), sondern eine Instanz dieser Klasse.

Dazu deklarieren wir eine Methode `__call__`:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[12] *}

In diesem Fall ist dieses `__call__` das, was **FastAPI** verwendet, um nach zusätzlichen Parametern und Unterabhängigkeiten zu suchen, und das ist es auch, was später aufgerufen wird, um einen Wert an den Parameter in Ihrer *Pfadoperation-Funktion* zu übergeben.

## Die Instanz parametrisieren { #parameterize-the-instance }

Und jetzt können wir `__init__` verwenden, um die Parameter der Instanz zu deklarieren, die wir zum „Parametrisieren“ der Abhängigkeit verwenden können:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[9] *}

In diesem Fall wird **FastAPI** `__init__` nie berühren oder sich darum kümmern, wir werden es direkt in unserem Code verwenden.

## Eine Instanz erstellen { #create-an-instance }

Wir könnten eine Instanz dieser Klasse erstellen mit:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[18] *}

Und auf diese Weise können wir unsere Abhängigkeit „parametrisieren“, die jetzt `"bar"` enthält, als das Attribut `checker.fixed_content`.

## Die Instanz als Abhängigkeit verwenden { #use-the-instance-as-a-dependency }

Dann könnten wir diesen `checker` in einem `Depends(checker)` anstelle von `Depends(FixedContentQueryChecker)` verwenden, da die Abhängigkeit die Instanz `checker` und nicht die Klasse selbst ist.

Und beim Auflösen der Abhängigkeit ruft **FastAPI** diesen `checker` wie folgt auf:

```Python
checker(q="somequery")
```

... und übergibt, was immer das als Wert dieser Abhängigkeit in unserer *Pfadoperation-Funktion* zurückgibt, als den Parameter `fixed_content_included`:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[22] *}

/// tip | Tipp

Das alles mag gekünstelt wirken. Und es ist möglicherweise noch nicht ganz klar, welchen Nutzen das hat.

Diese Beispiele sind bewusst einfach gehalten, zeigen aber, wie alles funktioniert.

In den Kapiteln zum Thema Sicherheit gibt es Hilfsfunktionen, die auf die gleiche Weise implementiert werden.

Wenn Sie das hier alles verstanden haben, wissen Sie bereits, wie diese Sicherheits-Hilfswerkzeuge unter der Haube funktionieren.

///

## Abhängigkeiten mit `yield`, `HTTPException`, `except` und Hintergrundtasks { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | Achtung

Sie benötigen diese technischen Details höchstwahrscheinlich nicht.

Diese Details sind hauptsächlich nützlich, wenn Sie eine FastAPI-Anwendung haben, die älter als 0.121.0 ist, und Sie auf Probleme mit Abhängigkeiten mit `yield` stoßen.

///

Abhängigkeiten mit `yield` haben sich im Laufe der Zeit weiterentwickelt, um verschiedene Anwendungsfälle abzudecken und einige Probleme zu beheben, hier ist eine Zusammenfassung der Änderungen.

### Abhängigkeiten mit `yield` und `scope` { #dependencies-with-yield-and-scope }

In Version 0.121.0 hat FastAPI Unterstützung für `Depends(scope="function")` für Abhängigkeiten mit `yield` hinzugefügt.

Mit `Depends(scope="function")` wird der Exit-Code nach `yield` direkt nach dem Ende der *Pfadoperation-Funktion* ausgeführt, bevor die Response an den Client gesendet wird.

Und bei Verwendung von `Depends(scope="request")` (dem Default) wird der Exit-Code nach `yield` ausgeführt, nachdem die Response gesendet wurde.

Mehr dazu finden Sie in der Dokumentation zu [Abhängigkeiten mit `yield` – Frühes Beenden und `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope).

### Abhängigkeiten mit `yield` und `StreamingResponse`, Technische Details { #dependencies-with-yield-and-streamingresponse-technical-details }

Vor FastAPI 0.118.0 wurde bei Verwendung einer Abhängigkeit mit `yield` der Exit-Code nach der *Pfadoperation-Funktion* ausgeführt, aber unmittelbar bevor die Response gesendet wurde.

Die Absicht war, Ressourcen nicht länger als nötig zu halten, während darauf gewartet wird, dass die Response durchs Netzwerk reist.

Diese Änderung bedeutete auch, dass bei Rückgabe einer `StreamingResponse` der Exit-Code der Abhängigkeit mit `yield` bereits ausgeführt worden wäre.

Wenn Sie beispielsweise eine Datenbanksession in einer Abhängigkeit mit `yield` hatten, konnte die `StreamingResponse` diese Session während des Streamens von Daten nicht verwenden, weil die Session im Exit-Code nach `yield` bereits geschlossen worden wäre.

Dieses Verhalten wurde in 0.118.0 zurückgenommen, sodass der Exit-Code nach `yield` ausgeführt wird, nachdem die Response gesendet wurde.

/// info | Info

Wie Sie unten sehen werden, ähnelt dies sehr dem Verhalten vor Version 0.106.0, jedoch mit mehreren Verbesserungen und Bugfixes für Sonderfälle.

///

#### Anwendungsfälle mit frühem Exit-Code { #use-cases-with-early-exit-code }

Es gibt einige Anwendungsfälle mit spezifischen Bedingungen, die vom alten Verhalten profitieren könnten, den Exit-Code von Abhängigkeiten mit `yield` vor dem Senden der Response auszuführen.

Stellen Sie sich zum Beispiel vor, Sie haben Code, der in einer Abhängigkeit mit `yield` eine Datenbanksession verwendet, nur um einen Benutzer zu verifizieren, die Datenbanksession wird aber in der *Pfadoperation-Funktion* nie wieder verwendet, sondern nur in der Abhängigkeit, und die Response benötigt lange, um gesendet zu werden, wie eine `StreamingResponse`, die Daten langsam sendet, aus irgendeinem Grund aber die Datenbank nicht verwendet.

In diesem Fall würde die Datenbanksession gehalten, bis das Senden der Response abgeschlossen ist, aber wenn Sie sie nicht verwenden, wäre es nicht notwendig, sie zu halten.

So könnte es aussehen:

{* ../../docs_src/dependencies/tutorial013_an_py310.py *}

Der Exit-Code, das automatische Schließen der `Session` in:

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[19:21] *}

... würde ausgeführt, nachdem die Response das langsame Senden der Daten beendet:

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] hl[31:33] *}

Da `generate_stream()` die Datenbanksession jedoch nicht verwendet, ist es nicht wirklich notwendig, die Session während des Sendens der Response offen zu halten.

Wenn Sie diesen spezifischen Anwendungsfall mit SQLModel (oder SQLAlchemy) haben, könnten Sie die Session explizit schließen, nachdem Sie sie nicht mehr benötigen:

{* ../../docs_src/dependencies/tutorial014_an_py310.py ln[24:28] hl[28] *}

Auf diese Weise würde die Session die Datenbankverbindung freigeben, sodass andere Requests sie verwenden könnten.

Wenn Sie einen anderen Anwendungsfall haben, der ein frühes Beenden aus einer Abhängigkeit mit `yield` benötigt, erstellen Sie bitte eine <a href="https://github.com/fastapi/fastapi/discussions/new?category=questions" class="external-link" target="_blank">GitHub-Diskussion-Frage</a> mit Ihrem spezifischen Anwendungsfall und warum Sie von einem frühen Schließen für Abhängigkeiten mit `yield` profitieren würden.

Wenn es überzeugende Anwendungsfälle für ein frühes Schließen bei Abhängigkeiten mit `yield` gibt, würde ich erwägen, eine neue Möglichkeit hinzuzufügen, um ein frühes Schließen optional zu aktivieren.

### Abhängigkeiten mit `yield` und `except`, Technische Details { #dependencies-with-yield-and-except-technical-details }

Vor FastAPI 0.110.0 war es so, dass wenn Sie eine Abhängigkeit mit `yield` verwendet und dann in dieser Abhängigkeit mit `except` eine Exception abgefangen haben und die Exception nicht erneut geworfen haben, die Exception automatisch an beliebige Exceptionhandler oder den Handler für interne Serverfehler weitergereicht/weitergeworfen wurde.

Dies wurde in Version 0.110.0 geändert, um unbehandelten Speicherverbrauch durch weitergeleitete Exceptions ohne Handler (interne Serverfehler) zu beheben und um es mit dem Verhalten von normalem Python-Code konsistent zu machen.

### Hintergrundtasks und Abhängigkeiten mit `yield`, Technische Details { #background-tasks-and-dependencies-with-yield-technical-details }

Vor FastAPI 0.106.0 war das Werfen von Exceptions nach `yield` nicht möglich, der Exit-Code in Abhängigkeiten mit `yield` wurde ausgeführt, nachdem die Response gesendet wurde, sodass [Exceptionhandler](../handling-errors.md#install-custom-exception-handlers){.internal-link target=_blank} bereits ausgeführt worden wären.

Dies war so designt, hauptsächlich um die Verwendung derselben von Abhängigkeiten „geyieldeten“ Objekte in Hintergrundtasks zu ermöglichen, da der Exit-Code erst ausgeführt wurde, nachdem die Hintergrundtasks abgeschlossen waren.

Dies wurde in FastAPI 0.106.0 geändert mit der Absicht, keine Ressourcen zu halten, während darauf gewartet wird, dass die Response durchs Netzwerk reist.

/// tip | Tipp

Zusätzlich ist ein Hintergrundtask normalerweise ein unabhängiger Logikblock, der separat gehandhabt werden sollte, mit eigenen Ressourcen (z. B. eigener Datenbankverbindung).

So haben Sie wahrscheinlich saubereren Code.

///

Wenn Sie sich bisher auf dieses Verhalten verlassen haben, sollten Sie jetzt die Ressourcen für Hintergrundtasks innerhalb des Hintergrundtasks selbst erstellen und intern nur Daten verwenden, die nicht von den Ressourcen von Abhängigkeiten mit `yield` abhängen.

Anstatt beispielsweise dieselbe Datenbanksession zu verwenden, würden Sie innerhalb des Hintergrundtasks eine neue Datenbanksession erstellen und die Objekte aus der Datenbank mithilfe dieser neuen Session beziehen. Und anstatt das Objekt aus der Datenbank als Parameter an die Hintergrundtask-Funktion zu übergeben, würden Sie die ID dieses Objekts übergeben und das Objekt dann innerhalb der Hintergrundtask-Funktion erneut beziehen.
