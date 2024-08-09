# Tutorial – Benutzerhandbuch

Dieses Tutorial zeigt Ihnen Schritt für Schritt, wie Sie **FastAPI** und die meisten seiner Funktionen verwenden können.

Jeder Abschnitt baut schrittweise auf den vorhergehenden auf. Diese Abschnitte sind aber nach einzelnen Themen gegliedert, sodass Sie direkt zu einem bestimmten Thema übergehen können, um Ihre speziellen API-Anforderungen zu lösen.

Außerdem dienen diese als zukünftige Referenz.

Dadurch können Sie jederzeit  zurückkommen und sehen genau das, was Sie benötigen.

## Den Code ausführen

Alle Codeblöcke können kopiert und direkt verwendet werden (da es sich um getestete Python-Dateien handelt).

Um eines der Beispiele auszuführen, kopieren Sie den Code in eine Datei `main.py`, und starten Sie `uvicorn` mit:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

Es wird **ausdrücklich empfohlen**, dass Sie den Code schreiben oder kopieren, ihn bearbeiten und lokal ausführen.

Die Verwendung in Ihrem eigenen Editor zeigt Ihnen die Vorteile von FastAPI am besten, wenn Sie sehen, wie wenig Code Sie schreiben müssen, all die Typprüfungen, die automatische Vervollständigung usw.

---

## FastAPI installieren

Der erste Schritt besteht aus der Installation von FastAPI.

Für dieses Tutorial empfiehlt es sich, FastAPI mit allen optionalen Abhängigkeiten und Funktionen zu installieren:

<div class="termy">

```console
$ pip install "fastapi[all]"

---> 100%
```

</div>

... das beinhaltet auch `uvicorn`, welchen Sie als Server verwenden können, der ihren Code ausführt.

/// note | "Hinweis"

Sie können die einzelnen Teile auch separat installieren.

Das folgende würden Sie wahrscheinlich tun, wenn Sie Ihre Anwendung in der Produktion einsetzen:

```
pip install fastapi
```

Installieren Sie auch `uvicorn` als Server:

```
pip install "uvicorn[standard]"
```

Das gleiche gilt für jede der optionalen Abhängigkeiten, die Sie verwenden möchten.

///

## Handbuch für fortgeschrittene Benutzer

Es gibt auch ein **Handbuch für fortgeschrittene Benutzer**, welches Sie später nach diesem **Tutorial – Benutzerhandbuch** lesen können.

Das **Handbuch für fortgeschrittene Benutzer** baut auf diesem Tutorial auf, verwendet dieselben Konzepte und bringt Ihnen einige zusätzliche Funktionen bei.

Allerdings sollten Sie zuerst das **Tutorial – Benutzerhandbuch** lesen (was Sie hier gerade tun).

Die Dokumentation ist so konzipiert, dass Sie mit dem **Tutorial – Benutzerhandbuch** eine vollständige Anwendung erstellen können und diese dann je nach Bedarf mit einigen der zusätzlichen Ideen aus dem **Handbuch für fortgeschrittene Benutzer** vervollständigen können.
