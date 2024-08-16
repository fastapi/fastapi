# Entwicklung – Mitwirken

Vielleicht möchten Sie sich zuerst die grundlegenden Möglichkeiten anschauen, [FastAPI zu helfen und Hilfe zu erhalten](help-fastapi.md){.internal-link target=_blank}.

## Entwicklung

Wenn Sie das <a href="https://github.com/fastapi/fastapi" class="external-link" target="_blank">fastapi Repository</a> bereits geklont haben und tief in den Code eintauchen möchten, hier einen Leitfaden zum Einrichten Ihrer Umgebung.

### Virtuelle Umgebung mit `venv`

Sie können mit dem Python-Modul `venv` in einem Verzeichnis eine isolierte virtuelle lokale Umgebung erstellen. Machen wir das im geklonten Repository (da wo sich die `requirements.txt` befindet):

<div class="termy">

```console
$ python -m venv env
```

</div>

Das erstellt ein Verzeichnis `./env/` mit den Python-Binärdateien und Sie können dann Packages in dieser lokalen Umgebung installieren.

### Umgebung aktivieren

Aktivieren Sie die neue Umgebung mit:

//// tab | Linux, macOS

<div class="termy">

```console
$ source ./env/bin/activate
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ .\env\Scripts\Activate.ps1
```

</div>

////

//// tab | Windows Bash

Oder, wenn Sie Bash für Windows verwenden (z. B. <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>):

<div class="termy">

```console
$ source ./env/Scripts/activate
```

</div>

////

Um zu überprüfen, ob es funktioniert hat, geben Sie ein:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
$ which pip

some/directory/fastapi/env/bin/pip
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ Get-Command pip

some/directory/fastapi/env/bin/pip
```

</div>

////

Wenn die `pip` Binärdatei unter `env/bin/pip` angezeigt wird, hat es funktioniert. 🎉

Stellen Sie sicher, dass Sie über die neueste Version von pip in Ihrer lokalen Umgebung verfügen, um Fehler bei den nächsten Schritten zu vermeiden:

<div class="termy">

```console
$ python -m pip install --upgrade pip

---> 100%
```

</div>

/// tip | "Tipp"

Aktivieren Sie jedes Mal, wenn Sie ein neues Package mit `pip` in dieser Umgebung installieren, die Umgebung erneut.

Dadurch wird sichergestellt, dass Sie, wenn Sie ein von diesem Package installiertes Terminalprogramm verwenden, das Programm aus Ihrer lokalen Umgebung verwenden und kein anderes, das global installiert sein könnte.

///

### Benötigtes mit pip installieren

Nachdem Sie die Umgebung wie oben beschrieben aktiviert haben:

<div class="termy">

```console
$ pip install -r requirements.txt

---> 100%
```

</div>

Das installiert alle Abhängigkeiten und Ihr lokales FastAPI in Ihrer lokalen Umgebung.

#### Das lokale FastAPI verwenden

Wenn Sie eine Python-Datei erstellen, die FastAPI importiert und verwendet, und diese mit dem Python aus Ihrer lokalen Umgebung ausführen, wird Ihr geklonter lokaler FastAPI-Quellcode verwendet.

Und wenn Sie diesen lokalen FastAPI-Quellcode aktualisieren und dann die Python-Datei erneut ausführen, wird die neue Version von FastAPI verwendet, die Sie gerade bearbeitet haben.

Auf diese Weise müssen Sie Ihre lokale Version nicht „installieren“, um jede Änderung testen zu können.

/// note | "Technische Details"

Das geschieht nur, wenn Sie die Installation mit der enthaltenen `requirements.txt` durchführen, anstatt `pip install fastapi` direkt auszuführen.

Das liegt daran, dass in der Datei `requirements.txt` die lokale Version von FastAPI mit der Option `-e` für die Installation im „editierbaren“ Modus markiert ist.

///

### Den Code formatieren

Es gibt ein Skript, das, wenn Sie es ausführen, Ihren gesamten Code formatiert und bereinigt:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

Es sortiert auch alle Ihre Importe automatisch.

Damit es sie richtig sortiert, muss FastAPI lokal in Ihrer Umgebung installiert sein, mit dem Befehl vom obigen Abschnitt, welcher `-e` verwendet.

## Dokumentation

Stellen Sie zunächst sicher, dass Sie Ihre Umgebung wie oben beschrieben einrichten, was alles Benötigte installiert.

### Dokumentation live

Während der lokalen Entwicklung gibt es ein Skript, das die Site erstellt, auf Änderungen prüft und direkt neu lädt (Live Reload):

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

Das stellt die Dokumentation unter `http://127.0.0.1:8008` bereit.

Auf diese Weise können Sie die Dokumentation/Quelldateien bearbeiten und die Änderungen live sehen.

/// tip | "Tipp"

Alternativ können Sie die Schritte des Skripts auch manuell ausführen.

Gehen Sie in das Verzeichnis für die entsprechende Sprache. Das für die englischsprachige Hauptdokumentation befindet sich unter `docs/en/`:

```console
$ cd docs/en/
```

Führen Sie dann `mkdocs` in diesem Verzeichnis aus:

```console
$ mkdocs serve --dev-addr 8008
```

///

#### Typer-CLI (optional)

Die Anleitung hier zeigt Ihnen, wie Sie das Skript unter `./scripts/docs.py` direkt mit dem `python` Programm verwenden.

Sie können aber auch <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a> verwenden und erhalten dann Autovervollständigung für Kommandos in Ihrem Terminal, nach dem Sie dessen Vervollständigung installiert haben.

Wenn Sie Typer CLI installieren, können Sie die Vervollständigung installieren mit:

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### Dokumentationsstruktur

Die Dokumentation verwendet <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

Und es gibt zusätzliche Tools/Skripte für Übersetzungen, in `./scripts/docs.py`.

/// tip | "Tipp"

Sie müssen sich den Code in `./scripts/docs.py` nicht anschauen, verwenden Sie ihn einfach in der Kommandozeile.

///

Die gesamte Dokumentation befindet sich im Markdown-Format im Verzeichnis `./docs/en/`.

Viele der Tutorials enthalten Codeblöcke.

In den meisten Fällen handelt es sich bei diesen Codeblöcken um vollständige Anwendungen, die unverändert ausgeführt werden können.

Tatsächlich sind diese Codeblöcke nicht Teil des Markdowns, sondern Python-Dateien im Verzeichnis `./docs_src/`.

Und diese Python-Dateien werden beim Generieren der Site in die Dokumentation eingefügt.

### Dokumentation für Tests

Tatsächlich arbeiten die meisten Tests mit den Beispielquelldateien in der Dokumentation.

Dadurch wird sichergestellt, dass:

* Die Dokumentation aktuell ist.
* Die Dokumentationsbeispiele ohne Änderung ausgeführt werden können.
* Die meisten Funktionalitäten durch die Dokumentation abgedeckt werden, sichergestellt durch die Testabdeckung.

#### Gleichzeitig Apps und Dokumentation

Wenn Sie die Beispiele ausführen, mit z. B.:

<div class="termy">

```console
$ uvicorn tutorial001:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

wird das, da Uvicorn standardmäßig den Port `8000` verwendet, mit der Dokumentation auf dem Port `8008` nicht in Konflikt geraten.

### Übersetzungen

Hilfe bei Übersetzungen wird SEHR geschätzt! Und es kann nicht getan werden, ohne die Hilfe der Gemeinschaft. 🌎 🚀

Hier sind die Schritte, die Ihnen bei Übersetzungen helfen.

#### Tipps und Richtlinien

* Schauen Sie nach <a href="https://github.com/fastapi/fastapi/pulls" class="external-link" target="_blank">aktuellen Pull Requests</a> für Ihre Sprache. Sie können die Pull Requests nach dem Label für Ihre Sprache filtern. Für Spanisch lautet das Label beispielsweise <a href="https://github.com/fastapi/fastapi/pulls?q=is%3Aopen+sort%3Aupdated-desc+label%3Alang-es+label%3Aawaiting-review" class="external-link" target="_blank">`lang-es`</a>.

* Sehen Sie diese Pull Requests durch (Review), schlagen Sie Änderungen vor, oder segnen Sie sie ab (Approval). Bei den Sprachen, die ich nicht spreche, warte ich, bis mehrere andere die Übersetzung durchgesehen haben, bevor ich den Pull Request merge.

/// tip | "Tipp"

Sie können <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request" class="external-link" target="_blank">Kommentare mit Änderungsvorschlägen</a> zu vorhandenen Pull Requests hinzufügen.

Schauen Sie sich die Dokumentation an, <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank">wie man ein Review zu einem Pull Request hinzufügt</a>, welches den PR absegnet oder Änderungen vorschlägt.

///

* Überprüfen Sie, ob es eine <a href="https://github.com/fastapi/fastapi/discussions/categories/translations" class="external-link" target="_blank">GitHub-Diskussion</a> gibt, die Übersetzungen für Ihre Sprache koordiniert. Sie können sie abonnieren, und wenn ein neuer Pull Request zum Review vorliegt, wird der Diskussion automatisch ein Kommentar hinzugefügt.

* Wenn Sie Seiten übersetzen, fügen Sie einen einzelnen Pull Request pro übersetzter Seite hinzu. Dadurch wird es für andere viel einfacher, ihn zu durchzusehen.

* Um den Zwei-Buchstaben-Code für die Sprache zu finden, die Sie übersetzen möchten, schauen Sie sich die Tabelle <a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" class="external-link" target= verwenden "_blank">List of ISO 639-1 codes</a> an.

#### Vorhandene Sprache

Angenommen, Sie möchten eine Seite für eine Sprache übersetzen, die bereits Übersetzungen für einige Seiten hat, beispielsweise für Spanisch.

Im Spanischen lautet der Zwei-Buchstaben-Code `es`. Das Verzeichnis für spanische Übersetzungen befindet sich also unter `docs/es/`.

/// tip | "Tipp"

Die Haupt („offizielle“) Sprache ist Englisch und befindet sich unter `docs/en/`.

///

Führen Sie nun den Live-Server für die Dokumentation auf Spanisch aus:

<div class="termy">

```console
// Verwenden Sie das Kommando „live“ und fügen Sie den Sprach-Code als Argument hinten an
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

/// tip | "Tipp"

Alternativ können Sie die Schritte des Skripts auch manuell ausführen.

Gehen Sie in das Sprachverzeichnis, für die spanischen Übersetzungen ist das `docs/es/`:

```console
$ cd docs/es/
```

Dann führen Sie in dem Verzeichnis `mkdocs` aus:

```console
$ mkdocs serve --dev-addr 8008
```

///

Jetzt können Sie auf <a href="http://127.0.0.1:8008" class="external-link" target="_blank">http://127.0.0.1:8008</a> gehen und Ihre Änderungen live sehen.

Sie werden sehen, dass jede Sprache alle Seiten hat. Einige Seiten sind jedoch nicht übersetzt und haben oben eine Info-Box, dass die Übersetzung noch fehlt.

Nehmen wir nun an, Sie möchten eine Übersetzung für den Abschnitt [Features](features.md){.internal-link target=_blank} hinzufügen.

* Kopieren Sie die Datei:

```
docs/en/docs/features.md
```

* Fügen Sie sie an genau derselben Stelle ein, jedoch für die Sprache, die Sie übersetzen möchten, z. B.:

```
docs/es/docs/features.md
```

/// tip | "Tipp"

Beachten Sie, dass die einzige Änderung in Pfad und Dateiname der Sprachcode ist, von `en` zu `es`.

///

Wenn Sie in Ihrem Browser nachsehen, werden Sie feststellen, dass die Dokumentation jetzt Ihren neuen Abschnitt anzeigt (die Info-Box oben ist verschwunden). 🎉

Jetzt können Sie alles übersetzen und beim Speichern sehen, wie es aussieht.

#### Neue Sprache

Nehmen wir an, Sie möchten Übersetzungen für eine Sprache hinzufügen, die noch nicht übersetzt ist, nicht einmal einige Seiten.

Angenommen, Sie möchten Übersetzungen für Kreolisch hinzufügen, diese sind jedoch noch nicht in den Dokumenten enthalten.

Wenn Sie den Link von oben überprüfen, lautet der Sprachcode für Kreolisch `ht`.

Der nächste Schritt besteht darin, das Skript auszuführen, um ein neues Übersetzungsverzeichnis zu erstellen:

<div class="termy">

```console
// Verwenden Sie das Kommando new-lang und fügen Sie den Sprach-Code als Argument hinten an
$ python ./scripts/docs.py new-lang ht

Successfully initialized: docs/ht
```

</div>

Jetzt können Sie in Ihrem Code-Editor das neu erstellte Verzeichnis `docs/ht/` sehen.

Obiges Kommando hat eine Datei `docs/ht/mkdocs.yml` mit einer Minimal-Konfiguration erstellt, die alles von der `en`-Version erbt:

```yaml
INHERIT: ../en/mkdocs.yml
```

/// tip | "Tipp"

Sie können diese Datei mit diesem Inhalt auch einfach manuell erstellen.

///

Das Kommando hat auch eine Dummy-Datei `docs/ht/index.md` für die Hauptseite erstellt. Sie können mit der Übersetzung dieser Datei beginnen.

Sie können nun mit den obigen Instruktionen für eine „vorhandene Sprache“ fortfahren.

Fügen Sie dem ersten Pull Request beide Dateien `docs/ht/mkdocs.yml` und `docs/ht/index.md` bei. 🎉

#### Vorschau des Ergebnisses

Wie bereits oben erwähnt, können Sie `./scripts/docs.py` mit dem Befehl `live` verwenden, um eine Vorschau der Ergebnisse anzuzeigen (oder `mkdocs serve`).

Sobald Sie fertig sind, können Sie auch alles so testen, wie es online aussehen würde, einschließlich aller anderen Sprachen.

Bauen Sie dazu zunächst die gesamte Dokumentation:

<div class="termy">

```console
// Verwenden Sie das Kommando „build-all“, das wird ein wenig dauern
$ python ./scripts/docs.py build-all

Building docs for: en
Building docs for: es
Successfully built docs for: es
```

</div>

Dadurch werden alle diese unabhängigen MkDocs-Sites für jede Sprache erstellt, kombiniert und das endgültige Resultat unter `./site/` gespeichert.

Dieses können Sie dann mit dem Befehl `serve` bereitstellen:

<div class="termy">

```console
// Verwenden Sie das Kommando „serve“ nachdem Sie „build-all“ ausgeführt haben.
$ python ./scripts/docs.py serve

Warning: this is a very simple server. For development, use mkdocs serve instead.
This is here only to preview a site with translations already built.
Make sure you run the build-all command first.
Serving at: http://127.0.0.1:8008
```

</div>

#### Übersetzungsspezifische Tipps und Richtlinien

* Übersetzen Sie nur die Markdown-Dokumente (`.md`). Übersetzen Sie nicht die Codebeispiele unter `./docs_src`.

* In Codeblöcken innerhalb des Markdown-Dokuments, übersetzen Sie Kommentare (`# ein Kommentar`), aber lassen Sie den Rest unverändert.

* Ändern Sie nichts, was in "``" (Inline-Code) eingeschlossen ist.

* In Zeilen, die mit `===` oder `!!!` beginnen, übersetzen Sie nur den ` "... Text ..."`-Teil. Lassen Sie den Rest unverändert.

* Sie können Info-Boxen wie `!!! warning` mit beispielsweise `!!! warning "Achtung"` übersetzen. Aber ändern Sie nicht das Wort direkt nach dem `!!!`, es bestimmt die Farbe der Info-Box.

* Ändern Sie nicht die Pfade in Links zu Bildern, Codedateien, Markdown Dokumenten.

* Wenn ein Markdown-Dokument übersetzt ist, ändern sich allerdings unter Umständen die `#hash-teile` in Links zu dessen Überschriften. Aktualisieren Sie diese Links, wenn möglich.
    * Suchen Sie im übersetzten Dokument nach solchen Links mit dem Regex `#[^# ]`.
    * Suchen Sie in allen bereits in ihre Sprache übersetzen Dokumenten nach `ihr-ubersetztes-dokument.md`. VS Code hat beispielsweise eine Option „Bearbeiten“ -> „In Dateien suchen“.
    * Übersetzen Sie bei der Übersetzung eines Dokuments nicht „im Voraus“ `#hash-teile`, die zu Überschriften in noch nicht übersetzten Dokumenten verlinken.

## Tests

Es gibt ein Skript, das Sie lokal ausführen können, um den gesamten Code zu testen und Code Coverage Reporte in HTML zu generieren:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

Dieses Kommando generiert ein Verzeichnis `./htmlcov/`. Wenn Sie die Datei `./htmlcov/index.html` in Ihrem Browser öffnen, können Sie interaktiv die Codebereiche erkunden, die von den Tests abgedeckt werden, und feststellen, ob Bereiche fehlen.
