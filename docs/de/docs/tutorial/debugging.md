# Debuggen

Sie können FastAPI in Ihrem Editor debuggen, was wir am Beispiel Visual Studio Code und PyCharm hier zeigen wollen.

## Visual Studio Code

Visual Studio Code (oder kurz, VS Code) verfügt bereits über eine Debugger-Konfiguration speziell für FastAPI.

Nehmen wir an, Sie haben ihre FastAPI Anwendung in einer Datei `myapp.py` untergebracht:

```Python
{!../../../docs_src/debugging/tutorial001.py!}
```

In VS Code können Sie diese Anwendung nun wie folgt debuggen:

* Öffnen Sie ihre `myapp.py`. Achten Sie auch darauf, dass deren Editor-Tab aktiv ist.

* Öffnen Sie nun links das Debug-Panel – Das Panel „Ausführen und debuggen“.

* Klicken Sie dort auf den Link „erstellen Sie eine launch.json-Datei“.

* Im Dropdown-Menü wählen Sie „Python Debugger“.

* Wählen Sie als nächstes „FastAPI“ von den Optionen.

* In dem anschließenden Dropdown geben Sie den Namen ihrer Anwendungsdatei ein, hier `myapp.py` (Das ist nur notwendig, weil VS Code keine Datei `main.py` gefunden hat).

* Jetzt wird in ihrem Projekt, im Unterordner `.vscode/`, eine Datei `launch.json` erstellt und im Editor geöffnet. Sie wird ungefähr so aussehen:

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "myapp:app",
                "--reload"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

* Alle wichtigen Einstellungen sind bereits vorgenommen, Sie müssen diese Datei nicht weiter bearbeiten, und können sie schließen.

* Die von ihnen soeben erzeugte Debug-Konfiguration wird jetzt auch im Debug-Panel oben als „Python: FastAPI“ angezeigt.

* Klicken Sie auf das grüne Dreieck neben Ihrer „Python Debugger: FastAPI“- Konfiguration, oder drücken Sie die Taste `F5`.

*  Das Debuggen beginnt. Oben erscheint ein Kästchen mit Buttons, etwa um das Debuggen nach einem Haltepunkt fortzusetzen, oder um das Debuggen zu beenden.

* Der FastAPI Entwicklungsserver wird gestartet, wie Sie im sich unten öffnenden Terminal sehen können.

* Fügen Sie jetzt in `myapp.py`, beispielsweise in der letzten Zeile der Funktion, einen Haltepunkt hinzu, indem Sie auf den roten Punkt klicken, der erscheint, wenn Sie die Maus über die Zeilennummer bewegen.

* Besuchen Sie in Ihrem Webbrowser die Startseite Ihrer Anwendung unter <a href="http://127.0.0.1:8000/" class="external-link" target="_blank">http://127.0.0.1:8000/</a>.

* In VS Code können Sie jetzt sehen, dass der Debugger bei ihrem Haltepunkt stoppt. Die aufgerufene Webseite hört nicht auf, zu laden, da Sie dem Debugger gesagt haben, vor der Rückgabe der Response zu stoppen. Links in Debug-Panel sehen Sie die aktuell verfügbaren lokalen und globalen Variablen. So sieht es etwa aus:

<img src="/img/tutorial/debugging/image01.png">

* Um die Ausführung fortzusetzen, klicken Sie im Debug-Kästchen auf den Button „Continue“. Jetzt wird die Response zurückgeliefert und die Webseite im Browser lädt zu Ende.

* Um das Debuggen zu beenden, klicken Sie (eventuell mehrmals) auf den Stop-Button im selben Kästchen. Der Entwicklungsserver wird beendet.

Damit wissen Sie die Grundlagen, um Ihre Anwendung in VS Code zu debuggen! 🚀

## PyCharm

PyCharm verfügt derzeit noch über keine Debug-Konfiguration speziell für FastAPI-Anwendungen, daher werden wir den `uvicorn`-Server direkt aus unserer `myapp.py` heraus ausführen.

### `uvicorn` aufrufen

Importieren Sie  `uvicorn` und führen Sie es direkt aus:

```Python hl_lines="1  15"
{!../../../docs_src/debugging/tutorial002.py!}
```

### Über `__name__ == "__main__"`

Der Hauptzweck von `__name__ == "__main__"` besteht darin, einen Codeblock zu haben, der ausgeführt wird, wenn Ihre Datei aufgerufen wird mit:

<div class="termy">

```console
$ python myapp.py
```

</div>

der aber nicht ausgeführt wird, wenn eine andere Datei sie importiert, wie in:

```Python
from myapp import app
```

#### Weitere Details

Wenn Sie Ihre Datei ausführen mit:

<div class="termy">

```console
$ python myapp.py
```

</div>

dann wird die interne Variable `__name__` in Ihrer Datei, welche automatisch von Python erstellt wird, als Wert den String `"__main__"` haben.

Also wird der Abschnitt:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

ausgeführt.

---

Dies wird nicht passieren, wenn Sie dieses Modul (diese Datei) importieren.

Wenn Sie also eine andere Datei `importer.py` haben mit:

```Python
from myapp import app

# Hier mehr Code
```

wird in dem Fall die automatisch erstellte Variable `__name__` in `myapp.py` nicht den Wert `"__main__"` haben.

Also wird die Zeile:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

nicht ausgeführt.

!!! info
    Weitere Informationen finden Sie in der <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">offiziellen Python-Dokumentation</a>.

### Den Code mit dem Debugger ausführen

Da Sie den Uvicorn-Server nun direkt aus Ihrem Code heraus ausführen, können Sie Ihr Python-Programm (Ihre FastAPI-Anwendung) direkt über den PyCharm Debugger (oder Debuggern von anderen Editoren) aufrufen.

* Klicken Sie einfach auf das grüne Dreieck, das links neben der Zeile `if __name__ == "__main__":` erscheint, und wählen Sie „Debug 'myapp'“.

* Der Debugger startet. Unten öffnen sich ein Konsolenfenster, das anzeigt, dass der Uvicorn Entwicklungsserver hochfährt.

* Fahren Sie anschließend fort wie unter [Visual Studio Code](#visual-studio-code): Setzen Sie Haltepunkte, laden Sie die Seite im Browser, begutachten Sie den aktuellen Zustand Ihrer Anwendung. Und auch hier haben Sie, diesmal unten, Buttons, um mit dem Debuggen fortzufahren, es zu beenden, usw. So sieht es etwa aus:

<img src="/img/tutorial/debugging/image02.png">

Und damit kennen Sie auch die Grundlagen, um Ihre Anwendung in PyCharm zu debuggen! 🚀
