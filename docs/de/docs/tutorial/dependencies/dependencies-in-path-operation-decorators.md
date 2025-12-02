# Abhängigkeiten in Pfadoperation-Dekoratoren { #dependencies-in-path-operation-decorators }

Manchmal benötigen Sie den Rückgabewert einer Abhängigkeit innerhalb Ihrer *Pfadoperation-Funktion* nicht wirklich.

Oder die Abhängigkeit gibt keinen Wert zurück.

Aber Sie müssen sie trotzdem ausführen/auflösen.

In diesen Fällen können Sie, anstatt einen Parameter der *Pfadoperation-Funktion* mit `Depends` zu deklarieren, eine `list`e von `dependencies` zum *Pfadoperation-Dekorator* hinzufügen.

## `dependencies` zum *Pfadoperation-Dekorator* hinzufügen { #add-dependencies-to-the-path-operation-decorator }

Der *Pfadoperation-Dekorator* erhält ein optionales Argument `dependencies`.

Es sollte eine `list`e von `Depends()` sein:

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[19] *}

Diese Abhängigkeiten werden auf die gleiche Weise wie normale Abhängigkeiten ausgeführt/aufgelöst. Aber ihr Wert (falls sie einen zurückgeben) wird nicht an Ihre *Pfadoperation-Funktion* übergeben.

/// tip | Tipp

Einige Editoren prüfen, ob Funktionsparameter nicht verwendet werden, und zeigen das als Fehler an.

Wenn Sie `dependencies` im *Pfadoperation-Dekorator* verwenden, stellen Sie sicher, dass sie ausgeführt werden, während gleichzeitig Ihr Editor/Ihre Tools keine Fehlermeldungen ausgeben.

Damit wird auch vermieden, neue Entwickler möglicherweise zu verwirren, die einen nicht verwendeten Parameter in Ihrem Code sehen und ihn für unnötig halten könnten.

///

/// info | Info

In diesem Beispiel verwenden wir zwei erfundene benutzerdefinierte Header `X-Key` und `X-Token`.

Aber in realen Fällen würden Sie bei der Implementierung von Sicherheit mehr Vorteile durch die Verwendung der integrierten [Sicherheits-Werkzeuge (siehe nächstes Kapitel)](../security/index.md){.internal-link target=_blank} erzielen.

///

## Abhängigkeitsfehler und -Rückgabewerte { #dependencies-errors-and-return-values }

Sie können dieselben Abhängigkeits-*Funktionen* verwenden, die Sie normalerweise verwenden.

### Abhängigkeitsanforderungen { #dependency-requirements }

Sie können Anforderungen für einen <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> (wie Header) oder andere Unterabhängigkeiten deklarieren:

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[8,13] *}

### Exceptions auslösen { #raise-exceptions }

Die Abhängigkeiten können Exceptions `raise`n, genau wie normale Abhängigkeiten:

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[10,15] *}

### Rückgabewerte { #return-values }

Und sie können Werte zurückgeben oder nicht, die Werte werden nicht verwendet.

Sie können also eine normale Abhängigkeit (die einen Wert zurückgibt), die Sie bereits an anderer Stelle verwenden, wiederverwenden, und auch wenn der Wert nicht verwendet wird, wird die Abhängigkeit ausgeführt:

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[11,16] *}

## Abhängigkeiten für eine Gruppe von *Pfadoperationen* { #dependencies-for-a-group-of-path-operations }

Wenn Sie später lesen, wie Sie größere Anwendungen strukturieren ([Größere Anwendungen – Mehrere Dateien](../../tutorial/bigger-applications.md){.internal-link target=_blank}), möglicherweise mit mehreren Dateien, lernen Sie, wie Sie einen einzelnen `dependencies`-Parameter für eine Gruppe von *Pfadoperationen* deklarieren.

## Globale Abhängigkeiten { #global-dependencies }

Als Nächstes werden wir sehen, wie man Abhängigkeiten zur gesamten `FastAPI`-Anwendung hinzufügt, sodass sie für jede *Pfadoperation* gelten.
