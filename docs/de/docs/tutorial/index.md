# Tutorial - Anleitung - Einstieg

Dieses Tutorial zeigt Ihnen Schritt für Schritt, wie Sie **FastAPI** mit den meisten seiner Funktionen nutzen können.

Jeder Abschnitt baut schrittweise auf den vorhergehenden auf, ist aber nach einzelnen Themen gegliedert, so dass Sie direkt zu einem bestimmten Thema gehen können, um Ihre speziellen API-Anforderungen zu lösen.

Es ist auch als Nachschlagewerk für die Zukunft gedacht.

Sie können also zurückkommen und genau sehen, was Sie brauchen.

## Code ausführen

Alle Codeblöcke können kopiert und direkt verwendet werden (es handelt sich dabei um getestete Python-Dateien).

Um eines der Beispiele auszuführen, kopieren Sie den Code in die Datei `main.py`, und starten Sie `uvicorn` mit:

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

Es ist **ÄUSSERST empfehlenswert**, den Code zu schreiben oder zu kopieren, zu bearbeiten und lokal auszuführen.

Wenn Sie den Code in Ihrem Editor verwenden, können Sie die Vorteile von FastAPI am besten erkennen, da Sie sehen, wie wenig Code Sie schreiben müssen, wie gut die Typüberprüfungen und die automatische Vervollständigung funktionieren, usw.

---

## FastAPI installieren

Der erste Schritt ist die Installation von FastAPI.

Für das Lernprogramm sollten Sie es mit allen optionalen Abhängigkeiten und Funktionen installieren:

<div class="termy">

```console
$ pip install "fastapi[all]"

---> 100%
```

</div>

...das betrifft auch `uvicorn`, das Sie als Server verwenden können, auf dem Ihr Code läuft.

!!! Hinweis
    Sie können FastApi auch in Teilen installieren.

    Das folgende würden Sie wahrscheinlich tun, wenn Sie Ihre Anwendung in der Produktion einsetzen wollen:

    ```
    pip install fastapi
    ```

    Installieren Sie auch `uvicorn`, um es als Server einzusetzen:

    ```
    pip install "uvicorn[standard]"
    ```

    Dasselbe gilt für jede der optionalen Abhängigkeiten, die Sie verwenden möchten.

## Anleitung für Fortgeschrittene

Es gibt auch ein **Anleitung für Fortgeschrittene**, das Sie später nach diesem **Tutorial - Anleitung** lesen können.

Die **Anleitung für Fortgeschrittene** baut auf diesem auf, verwendet die gleichen Konzepte und bringt Ihnen einige zusätzliche Funktionen bei.

Sie sollten jedoch zuerst das **Tutorial - Anleitung** (das, was Sie gerade lesen) lesen.

Es ist so konzipiert, dass Sie mit dem **Tutorial - Anleitung** eine komplette Anwendung erstellen und diese dann je nach Ihren Bedürfnissen mit einigen der zusätzlichen Ideen aus der **Anleitung für Fortgeschrittene** erweitern können.
