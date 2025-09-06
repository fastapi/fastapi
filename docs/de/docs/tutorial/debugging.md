# Debugging { #debugging }

Sie können den Debugger in Ihrem Editor verbinden, zum Beispiel mit Visual Studio Code oder PyCharm.

## `uvicorn` aufrufen { #call-uvicorn }

Importieren und führen Sie `uvicorn` direkt in Ihrer FastAPI-Anwendung aus:

{* ../../docs_src/debugging/tutorial001.py hl[1,15] *}

### Über `__name__ == "__main__"` { #about-name-main }

Der Hauptzweck von `__name__ == "__main__"` ist, dass Code ausgeführt wird, wenn Ihre Datei mit folgendem Befehl aufgerufen wird:

<div class="termy">

```console
$ python myapp.py
```

</div>

aber nicht aufgerufen wird, wenn eine andere Datei sie importiert, wie in:

```Python
from myapp import app
```

#### Weitere Details { #more-details }

Angenommen, Ihre Datei heißt `myapp.py`.

Wenn Sie sie mit folgendem Befehl ausführen:

<div class="termy">

```console
$ python myapp.py
```

</div>

dann hat in Ihrer Datei die interne Variable `__name__`, die von Python automatisch erstellt wird, als Wert den String `"__main__"`.

Daher wird der Abschnitt:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

ausgeführt.

---

Dies wird nicht passieren, wenn Sie das Modul (die Datei) importieren.

Wenn Sie also eine weitere Datei `importer.py` mit folgendem Inhalt haben:

```Python
from myapp import app

# Hier mehr Code
```

wird in diesem Fall in `myapp.py` die automatisch erstellte Variable `__name__` nicht den Wert `"__main__"` haben.

Daher wird die Zeile:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

nicht ausgeführt.

/// info | Info

Für weitere Informationen besuchen Sie bitte <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">die offizielle Python-Dokumentation</a>.

///

## Ihren Code mit Ihrem Debugger ausführen { #run-your-code-with-your-debugger }

Da Sie den Uvicorn-Server direkt aus Ihrem Code ausführen, können Sie Ihr Python-Programm (Ihre FastAPI-Anwendung) direkt aus dem Debugger aufrufen.

---

Zum Beispiel können Sie in Visual Studio Code:

* Zum „Debug“-Panel gehen.
* „Konfiguration hinzufügen ...“ auswählen.
* „Python“ auswählen.
* Den Debugger mit der Option „`Python: Current File (Integrated Terminal)`“ ausführen.

Der Server wird dann mit Ihrem **FastAPI**-Code gestartet, an Ihren Haltepunkten angehalten, usw.

So könnte es aussehen:

<img src="/img/tutorial/debugging/image01.png">

---

Wenn Sie Pycharm verwenden, können Sie:

* Das Menü „Run“ öffnen.
* Die Option „Debug ...“ auswählen.
* Ein Kontextmenü wird angezeigt.
* Die zu debuggende Datei auswählen (in diesem Fall `main.py`).

Der Server wird dann mit Ihrem **FastAPI**-Code gestartet, an Ihren Haltepunkten angehalten, usw.

So könnte es aussehen:

<img src="/img/tutorial/debugging/image02.png">
