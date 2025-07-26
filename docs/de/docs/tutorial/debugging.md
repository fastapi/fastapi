# Debugging

Sie können den Debugger in Ihrem Editor verbinden, zum Beispiel mit Visual Studio Code oder PyCharm.

## Aufruf von `uvicorn`

Importieren und führen Sie `uvicorn` direkt in Ihrer FastAPI-Anwendung aus:

{* ../../docs_src/debugging/tutorial001.py hl[1,15] *}

### Über `__name__ == "__main__"`

Der Hauptzweck von `__name__ == "__main__"` ist, dass bestimmter Code ausgeführt wird, wenn Ihre Datei mit:

<div class="termy">

```console
$ python myapp.py
```

</div>

aufgerufen wird, aber nicht ausgeführt wird, wenn eine andere Datei sie importiert, wie in:

```Python
from myapp import app
```

#### Mehr Details

Angenommen, Ihre Datei heißt `myapp.py`.

Wenn Sie sie mit:

<div class="termy">

```console
$ python myapp.py
```

</div>

ausführen, hat die interne Variable `__name__` in Ihrer Datei, die automatisch von Python erstellt wird, den Wert der Zeichenkette `"__main__"`.

Also wird der Abschnitt:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

ausgeführt.

---

Das wird nicht passieren, wenn Sie dieses Modul (Datei) importieren.

Wenn Sie also eine andere Datei `importer.py` mit folgendem Inhalt haben:

```Python
from myapp import app

# Weiterer Code
```

wird in diesem Fall die automatisch erstellte Variable innerhalb von `myapp.py` nicht den Wert `"__main__"` für die Variable `__name__` haben.

Daher wird die Zeile:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

nicht ausgeführt.

/// info | Hinweis

Für weitere Informationen schauen Sie in die <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">offiziellen Python-Dokumentationen</a>.

///

## Führen Sie Ihren Code mit Ihrem Debugger aus

Da Sie den Uvicorn-Server direkt aus Ihrem Code heraus ausführen, können Sie Ihr Python-Programm (Ihre FastAPI-Anwendung) direkt aus dem Debugger aufrufen.

---

Zum Beispiel können Sie in Visual Studio Code:

* Zum "Debug"-Panel gehen.
* "Konfiguration hinzufügen..." wählen.
* "Python" auswählen.
* Den Debugger mit der Option "`Python: Current File (Integrated Terminal)`" ausführen.

Damit wird dann der Server mit Ihrem **FastAPI**-Code gestartet, an Ihren Breakpoints angehalten usw.

So könnte es aussehen:

<img src="/img/tutorial/debugging/image01.png">

---

Wenn Sie Pycharm verwenden, können Sie:

* Das "Run"-Menü öffnen.
* Die Option "Debug..." auswählen.
* Es erscheint ein Kontextmenü.
* Die Datei zum Debuggen auswählen (in diesem Fall `main.py`).

Damit wird dann der Server mit Ihrem **FastAPI**-Code gestartet, an Ihren Breakpoints angehalten usw.

So könnte es aussehen:

<img src="/img/tutorial/debugging/image02.png">
