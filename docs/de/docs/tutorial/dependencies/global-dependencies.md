# Globale Abhängigkeiten { #global-dependencies }

Bei einigen Anwendungstypen möchten Sie möglicherweise Abhängigkeiten zur gesamten Anwendung hinzufügen.

Ähnlich wie Sie [`dependencies` zu den *Pfadoperation-Dekoratoren* hinzufügen](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} können, können Sie sie auch zur `FastAPI`-Anwendung hinzufügen.

In diesem Fall werden sie auf alle *Pfadoperationen* in der Anwendung angewendet:

{* ../../docs_src/dependencies/tutorial012_an_py39.py hl[16] *}

Und alle Ideen aus dem Abschnitt über das [Hinzufügen von `dependencies` zu den *Pfadoperation-Dekoratoren*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} gelten weiterhin, aber in diesem Fall für alle *Pfadoperationen* in der App.

## Abhängigkeiten für Gruppen von *Pfadoperationen* { #dependencies-for-groups-of-path-operations }

Wenn Sie später lesen, wie Sie größere Anwendungen strukturieren ([Größere Anwendungen – mehrere Dateien](../../tutorial/bigger-applications.md){.internal-link target=_blank}), möglicherweise mit mehreren Dateien, lernen Sie, wie Sie einen einzelnen `dependencies`-Parameter für eine Gruppe von *Pfadoperationen* deklarieren.
