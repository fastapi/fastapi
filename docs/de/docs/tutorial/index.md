# Tutorial – Benutzerhandbuch { #tutorial-user-guide }

Dieses Tutorial zeigt Ihnen Schritt für Schritt, wie Sie **FastAPI** mit den meisten seiner Funktionen verwenden können.

Jeder Abschnitt baut schrittweise auf den vorhergehenden auf, ist jedoch in einzelne Themen gegliedert, sodass Sie direkt zu einem bestimmten Thema übergehen können, um Ihre spezifischen API-Anforderungen zu lösen.

Es ist auch so gestaltet, dass es als zukünftige Referenz dient, sodass Sie jederzeit zurückkommen und genau das sehen, was Sie benötigen.

## Den Code ausführen { #run-the-code }

Alle Codeblöcke können kopiert und direkt verwendet werden (es sind tatsächlich getestete Python-Dateien).

Um eines der Beispiele auszuführen, kopieren Sie den Code in eine Datei `main.py` und starten Sie `fastapi dev` mit:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

Es wird **dringend empfohlen**, den Code zu schreiben oder zu kopieren, ihn zu bearbeiten und lokal auszuführen.

Die Verwendung in Ihrem eigenen Editor zeigt Ihnen die Vorteile von FastAPI am besten, wenn Sie sehen, wie wenig Code Sie schreiben müssen, all die Typprüfungen, die automatische Vervollständigung usw.

---

## FastAPI installieren { #install-fastapi }

Der erste Schritt besteht darin, FastAPI zu installieren.

Stellen Sie sicher, dass Sie eine [virtuelle Umgebung](../virtual-environments.md){.internal-link target=_blank} erstellen, sie aktivieren und dann **FastAPI installieren**:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note | Hinweis

Wenn Sie mit `pip install "fastapi[standard]"` installieren, werden einige optionale Standard-Abhängigkeiten mit installiert, einschließlich `fastapi-cloud-cli`, welches Ihnen das Deployment in der <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a> ermöglicht.

Wenn Sie diese optionalen Abhängigkeiten nicht haben möchten, können Sie stattdessen `pip install fastapi` installieren.

Wenn Sie die Standard-Abhängigkeiten, aber ohne das `fastapi-cloud-cli` installieren möchten, können Sie mit `pip install "fastapi[standard-no-fastapi-cloud-cli]"` installieren.

///

## Handbuch für fortgeschrittene Benutzer { #advanced-user-guide }

Es gibt auch ein **Handbuch für fortgeschrittene Benutzer**, das Sie nach diesem **Tutorial – Benutzerhandbuch** lesen können.

Das **Handbuch für fortgeschrittene Benutzer** baut hierauf auf, verwendet dieselben Konzepte und bringt Ihnen einige zusätzliche Funktionen bei.

Sie sollten jedoch zuerst das **Tutorial – Benutzerhandbuch** lesen (was Sie gerade tun).

Es ist so konzipiert, dass Sie mit dem **Tutorial – Benutzerhandbuch** eine vollständige Anwendung erstellen können und diese dann je nach Bedarf mit einigen der zusätzlichen Ideen aus dem **Handbuch für fortgeschrittene Benutzer** erweitern können.
