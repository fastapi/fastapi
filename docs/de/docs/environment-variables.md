# Umgebungsvariablen { #environment-variables }

/// tip | Tipp

Wenn Sie bereits wissen, was „Umgebungsvariablen“ sind und wie man sie verwendet, können Sie dies überspringen.

///

Eine Umgebungsvariable (auch bekannt als „**env var**“) ist eine Variable, die **außerhalb** des Python-Codes im **Betriebssystem** lebt und von Ihrem Python-Code (oder auch von anderen Programmen) gelesen werden kann.

Umgebungsvariablen können nützlich sein, um **Einstellungen** der Anwendung zu handhaben, als Teil der **Installation** von Python usw.

## Umgebungsvariablen erstellen und verwenden { #create-and-use-env-vars }

Sie können Umgebungsvariablen in der **Shell (Terminal)** erstellen und verwenden, ohne Python zu benötigen:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Sie können eine Umgebungsvariable MY_NAME erstellen mit
$ export MY_NAME="Wade Wilson"

// Dann können Sie sie mit anderen Programmen verwenden, etwa
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Erstellen Sie eine Umgebungsvariable MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Verwenden Sie sie mit anderen Programmen, etwa
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Umgebungsvariablen in Python lesen { #read-env-vars-in-python }

Sie können auch Umgebungsvariablen **außerhalb** von Python erstellen, im Terminal (oder mit jeder anderen Methode) und sie dann **in Python** lesen.

Zum Beispiel könnten Sie eine Datei `main.py` haben mit:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | Tipp

Das zweite Argument von <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> ist der Defaultwert, der zurückgegeben wird.

Wenn er nicht angegeben wird, ist er standardmäßig `None`. Hier geben wir `"World"` als den zu verwendenden Defaultwert an.

///

Dann könnten Sie das Python-Programm aufrufen:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Hier setzen wir die Umgebungsvariable noch nicht
$ python main.py

// Da wir die Umgebungsvariable nicht gesetzt haben, erhalten wir den Defaultwert

Hello World from Python

// Aber wenn wir zuerst eine Umgebungsvariable erstellen
$ export MY_NAME="Wade Wilson"

// Und dann das Programm erneut aufrufen
$ python main.py

// Jetzt kann es die Umgebungsvariable lesen

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Hier setzen wir die Umgebungsvariable noch nicht
$ python main.py

// Da wir die Umgebungsvariable nicht gesetzt haben, erhalten wir den Defaultwert

Hello World from Python

// Aber wenn wir zuerst eine Umgebungsvariable erstellen
$ $Env:MY_NAME = "Wade Wilson"

// Und dann das Programm erneut aufrufen
$ python main.py

// Jetzt kann es die Umgebungsvariable lesen

Hello Wade Wilson from Python
```

</div>

////

Da Umgebungsvariablen außerhalb des Codes gesetzt werden können, aber vom Code gelesen werden können und nicht mit den restlichen Dateien gespeichert (in `git` committet) werden müssen, werden sie häufig für Konfigurationen oder **Einstellungen** verwendet.

Sie können auch eine Umgebungsvariable nur für einen **spezifischen Programmaufruf** erstellen, die nur für dieses Programm und nur für dessen Dauer verfügbar ist.

Um dies zu tun, erstellen Sie sie direkt vor dem Programmaufruf, in derselben Zeile:

<div class="termy">

```console
// Erstellen Sie eine Umgebungsvariable MY_NAME in der Zeile für diesen Programmaufruf
$ MY_NAME="Wade Wilson" python main.py

// Jetzt kann es die Umgebungsvariable lesen

Hello Wade Wilson from Python

// Die Umgebungsvariable existiert danach nicht mehr
$ python main.py

Hello World from Python
```

</div>

/// tip | Tipp

Sie können mehr darüber lesen auf <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a>.

///

## Typen und Validierung { #types-and-validation }

Diese Umgebungsvariablen können nur **Textstrings** handhaben, da sie extern zu Python sind und kompatibel mit anderen Programmen und dem Rest des Systems (und sogar mit verschiedenen Betriebssystemen, wie Linux, Windows, macOS) sein müssen.

Das bedeutet, dass **jeder Wert**, der in Python von einer Umgebungsvariable gelesen wird, **ein `str` sein wird**, und jede Konvertierung in einen anderen Typ oder jede Validierung muss im Code vorgenommen werden.

Sie werden mehr darüber lernen, wie man Umgebungsvariablen zur Handhabung von **Anwendungseinstellungen** verwendet, im [Handbuch für fortgeschrittene Benutzer – Einstellungen und Umgebungsvariablen](./advanced/settings.md){.internal-link target=_blank}.

## `PATH`-Umgebungsvariable { #path-environment-variable }

Es gibt eine **spezielle** Umgebungsvariable namens **`PATH`**, die von den Betriebssystemen (Linux, macOS, Windows) verwendet wird, um Programme zu finden, die ausgeführt werden sollen.

Der Wert der Variable `PATH` ist ein langer String, der aus Verzeichnissen besteht, die auf Linux und macOS durch einen Doppelpunkt `:` und auf Windows durch ein Semikolon `;` getrennt sind.

Zum Beispiel könnte die `PATH`-Umgebungsvariable so aussehen:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Das bedeutet, dass das System nach Programmen in den Verzeichnissen suchen sollte:

* `/usr/local/bin`
* `/usr/bin`
* `/bin`
* `/usr/sbin`
* `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

Das bedeutet, dass das System nach Programmen in den Verzeichnissen suchen sollte:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

Wenn Sie einen **Befehl** im Terminal eingeben, **sucht** das Betriebssystem nach dem Programm in **jedem dieser Verzeichnisse**, die in der `PATH`-Umgebungsvariablen aufgeführt sind.

Zum Beispiel, wenn Sie `python` im Terminal eingeben, sucht das Betriebssystem nach einem Programm namens `python` im **ersten Verzeichnis** in dieser Liste.

Wenn es es findet, wird es **benutzt**. Andernfalls sucht es weiter in den **anderen Verzeichnissen**.

### Python installieren und den `PATH` aktualisieren { #installing-python-and-updating-the-path }

Wenn Sie Python installieren, könnten Sie gefragt werden, ob Sie die `PATH`-Umgebungsvariable aktualisieren möchten.

//// tab | Linux, macOS

Angenommen, Sie installieren Python und es landet in einem Verzeichnis `/opt/custompython/bin`.

Wenn Sie erlauben, die `PATH`-Umgebungsvariable zu aktualisieren, fügt der Installer `/opt/custompython/bin` zur `PATH`-Umgebungsvariable hinzu.

Das könnte so aussehen:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

Auf diese Weise, wenn Sie `python` im Terminal eingeben, findet das System das Python-Programm in `/opt/custompython/bin` (das letzte Verzeichnis) und verwendet dieses.

////

//// tab | Windows

Angenommen, Sie installieren Python und es landet in einem Verzeichnis `C:\opt\custompython\bin`.

Wenn Sie erlauben, die `PATH`-Umgebungsvariable zu aktualisieren, fügt der Installer `C:\opt\custompython\bin` zur `PATH`-Umgebungsvariable hinzu.

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

Auf diese Weise, wenn Sie `python` im Terminal eingeben, findet das System das Python-Programm in `C:\opt\custompython\bin` (das letzte Verzeichnis) und verwendet dieses.

////

Also, wenn Sie tippen:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

Das System wird das `python` Programm in `/opt/custompython/bin` **finden** und es ausführen.

Es wäre ungefähr gleichbedeutend mit der Eingabe von:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

Das System wird das `python` Programm in `C:\opt\custompython\bin\python` **finden** und es ausführen.

Es wäre ungefähr gleichbedeutend mit der Eingabe von:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

Diese Informationen werden nützlich sein, wenn Sie über [Virtuelle Umgebungen](virtual-environments.md){.internal-link target=_blank} lernen.

## Fazit { #conclusion }

Mit diesem Wissen sollten Sie ein grundlegendes Verständnis davon haben, was **Umgebungsvariablen** sind und wie man sie in Python verwendet.

Sie können auch mehr darüber in der <a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia zu Umgebungsvariablen</a> lesen.

In vielen Fällen ist es nicht sehr offensichtlich, wie Umgebungsvariablen nützlich und sofort anwendbar sein könnten. Aber sie tauchen immer wieder in vielen verschiedenen Szenarien auf, wenn Sie entwickeln, deshalb ist es gut, darüber Bescheid zu wissen.

Zum Beispiel werden Sie diese Informationen im nächsten Abschnitt über [Virtuelle Umgebungen](virtual-environments.md) benötigen.
