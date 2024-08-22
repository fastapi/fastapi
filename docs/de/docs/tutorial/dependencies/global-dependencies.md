# Globale Abhängigkeiten

Bei einigen Anwendungstypen möchten Sie möglicherweise Abhängigkeiten zur gesamten Anwendung hinzufügen.

Ähnlich wie Sie [`dependencies` zu den *Pfadoperation-Dekoratoren* hinzufügen](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} können, können Sie sie auch zur `FastAPI`-Anwendung hinzufügen.

In diesem Fall werden sie auf alle *Pfadoperationen* in der Anwendung angewendet:

//// tab | Python 3.9+

```Python hl_lines="16"
{!> ../../../docs_src/dependencies/tutorial012_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="16"
{!> ../../../docs_src/dependencies/tutorial012_an.py!}
```

////

//// tab | Python 3.8 nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="15"
{!> ../../../docs_src/dependencies/tutorial012.py!}
```

////

Und alle Ideen aus dem Abschnitt über das [Hinzufügen von `dependencies` zu den *Pfadoperation-Dekoratoren*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} gelten weiterhin, aber in diesem Fall für alle *Pfadoperationen* in der Anwendung.

## Abhängigkeiten für Gruppen von *Pfadoperationen*

Wenn Sie später lesen, wie Sie größere Anwendungen strukturieren ([Bigger Applications - Multiple Files](../../tutorial/bigger-applications.md){.internal-link target=_blank}), möglicherweise mit mehreren Dateien, lernen Sie, wie Sie einen einzelnen `dependencies`-Parameter für eine Gruppe von *Pfadoperationen* deklarieren.
