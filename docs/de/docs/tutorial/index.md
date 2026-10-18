# Tutorial – Benutzerhandbuch { #tutorial-user-guide }

This tutorial shows you how to use **FastAPI** with most of its features, step by step.

Each section gradually builds on the previous ones, but it's structured to separate topics, so that you can go directly to any specific one to solve your specific API needs.

It is also built to work as a future reference so you can come back and see exactly what you need.

## Den Code ausführen { #run-the-code }

Alle Codeblöcke können kopiert und direkt verwendet werden (es sind tatsächlich getestete Python-Dateien).

Um eines der Beispiele auszuführen, kopieren Sie den Code in eine Datei `main.py`, und starten Sie `fastapi dev` mit `uv run`:

<div class="termy">

```console
$ <font color="#4E9A06">uv run fastapi</font> dev

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

Der erste Schritt besteht darin, Ihr Projekt einzurichten und FastAPI hinzuzufügen.

Installieren Sie [`uv`](https://docs.astral.sh/uv/getting-started/installation/), erstellen Sie dann ein Projekt und fügen Sie FastAPI hinzu:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"

---> 100%
```

</div>

`uv add` erstellt die virtuelle Umgebung des Projekts in `.venv`, fügt FastAPI zu `pyproject.toml` hinzu und erstellt `uv.lock`, sodass dieselben Packageversionen später installiert werden können.

/// details | Was diese Befehle tun

* `uv init`: Erstellt ein neues Python-Projekt.
* `awesome-project`: Erstellt das Projekt in einem neuen Verzeichnis mit diesem Namen.
* `--bare`: Erstellt nur die minimale Datei `pyproject.toml`, ohne eine Beispiel-`main.py`, `README.md` oder andere Dateien zu generieren. Sie erstellen die Anwendungsdateien in den nächsten Schritten dieses Tutorials selbst.

Dann betritt `cd awesome-project` das neue Projektverzeichnis, bevor FastAPI hinzugefügt wird.

`uv` verwendet eine kompatible Python-Version, die bereits auf Ihrem System installiert ist, oder lädt bei Bedarf eine herunter.

Wenn Sie `uv add` ausführen, wählt es kompatible Versionen von FastAPI und aller Packages aus, von denen FastAPI abhängt. Es zeichnet die exakten Versionen in `uv.lock` auf, wodurch es möglich wird, dieselben Packageversionen später auf einem anderen Computer oder beim Deployen der Anwendung zu installieren.

Das Erstellen oder Aktualisieren dieser Datei wird [**Locking** der Projektabhängigkeiten](https://docs.astral.sh/uv/concepts/projects/sync/) genannt. `uv` erledigt dies automatisch, wenn Sie ein Package hinzufügen.

///

/// details | FastAPI-Installationsoptionen

Wenn Sie mit `uv add "fastapi[standard]"` installieren, werden einige optionale Standard-Abhängigkeiten mit installiert, einschließlich `fastapi-cloud-cli`, welches Ihnen das Deployment in der [FastAPI Cloud](https://fastapicloud.com) ermöglicht.

Wenn Sie diese optionalen Abhängigkeiten nicht haben möchten, können Sie stattdessen `uv add fastapi` installieren.

Wenn Sie die Standard-Abhängigkeiten, aber ohne das `fastapi-cloud-cli` installieren möchten, können Sie mit `uv add "fastapi[standard-no-fastapi-cloud-cli]"` installieren.

///

/// details | Stattdessen `pip` verwenden

Wenn Sie es bevorzugen, eine virtuelle Umgebung und Packages manuell zu verwalten, erstellen und aktivieren Sie eine virtuelle Umgebung und installieren Sie dann FastAPI mit `pip install "fastapi[standard]"`.

Lesen Sie den [Leitfaden zu virtuellen Umgebungen](https://tiangolo.com/guides/virtual-environments/) für die detaillierten Schritte.

///

## Skills für AI-Agenten { #ai-agent-skills }

FastAPI enthält einen offiziellen Skill für AI-Coding-Agenten. Er ist mit dem Package gebündelt, sodass seine Anleitung mit der in Ihrem Projekt installierten FastAPI-Version übereinstimmt und aktualisiert wird, wenn Sie FastAPI aktualisieren.

Nachdem Sie FastAPI in Ihrem Projekt installiert haben, können Sie den Skill mit <a href="https://library-skills.io">Library Skills</a> installieren:

```bash
uvx library-skills
```

/// note | Hinweis

`uvx` ist ein Alias für `uv tool run`. Es führt Library Skills in einer temporären, isolierten Umgebung aus, während Library Skills die in Ihrem Projekt installierten Packages scannt.

///

Der Skill ist kompatibel mit Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, Pi, OpenCode und den meisten anderen Coding-Agenten. Wählen Sie bei Claude Code `.claude/skills`, wenn Sie gefragt werden, wo der Skill installiert werden soll.

## Handbuch für fortgeschrittene Benutzer { #advanced-user-guide }

Es gibt auch ein **Handbuch für fortgeschrittene Benutzer**, das Sie nach diesem **Tutorial – Benutzerhandbuch** lesen können.

Das **Handbuch für fortgeschrittene Benutzer** baut hierauf auf, verwendet dieselben Konzepte und bringt Ihnen einige zusätzliche Funktionen bei.

Sie sollten jedoch zuerst das **Tutorial – Benutzerhandbuch** lesen (was Sie gerade tun).

Es ist so konzipiert, dass Sie mit dem **Tutorial – Benutzerhandbuch** eine vollständige Anwendung erstellen können und diese dann je nach Bedarf mit einigen der zusätzlichen Ideen aus dem **Handbuch für fortgeschrittene Benutzer** erweitern können.
