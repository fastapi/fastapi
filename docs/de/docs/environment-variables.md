# Umgebungsvariablen

/// tip | Tipp

Wenn Sie bereits wissen, was „Umgebungsvariablen“ sind und wie Sie sie verwenden, können Sie diesen Abschnitt überspringen.

///

Eine Umgebungsvariable (auch bekannt als "**Env Var**") ist eine Variable, die **außerhalb** des Python-Codes, im **Betriebssystem** lebt und von Ihrem Python-Code (oder auch von anderen Programmen) gelesen werden kann.

Umgebungsvariablen können nützlich sein, um Anwendungs-**Einstellungen** zu handhaben, als Teil der **Installation** von Python, usw.

## Env Vars erstellen und verwenden

Sie können Umgebungsvariablen in der **Shell (Terminal)** erstellen und verwenden, ohne Python zu benötigen:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Sie könnten eine Env Var MY_NAME erstellen mit
$ export MY_NAME="Wade Wilson"

// Dann könnten Sie es mit anderen Programmen verwenden, wie
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Erstellen Sie eine Env Var MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Verwenden Sie es mit anderen Programmen, wie
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Env Vars in Python lesen

Sie können Umgebungsvariablen auch **außerhalb** von Python, im Terminal (oder mit jeder anderen Methode) erstellen und dann **in Python lesen**.

Zum Beispiel könnten Sie eine Datei `main.py` haben mit:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | Tipp

Das zweite Argument von <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> ist der Defaultwert, der zurückgegeben wird.

Wenn keiner angegeben wird, ist es `None` standardmäßig; hier geben wir `"World"` als den zu verwendenden Defaultwert an.

///

Dann könnten Sie dieses Python-Programm aufrufen:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Hier setzen wir die Env Var noch nicht
$ python main.py

// Da wir die Env Var nicht gesetzt haben, erhalten wir den Defaultwert

Hello World from Python

// Aber wenn wir zuerst eine Umgebungsvariable erstellen
$ export MY_NAME="Wade Wilson"

// Und das Programm dann erneut aufrufen
$ python main.py

// Jetzt kann es die Umgebungsvariable lesen

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Hier setzen wir die Env Var noch nicht
$ python main.py

// Da wir die Env Var nicht gesetzt haben, erhalten wir den Defaultwert

Hello World from Python

// Aber wenn wir zunächst eine Umgebungsvariable erstellen
$ $Env:MY_NAME = "Wade Wilson"

// Und das Programm dann erneut aufrufen
$ python main.py

// Jetzt kann es die Umgebungsvariable lesen

Hello Wade Wilson from Python
```

</div>

////

Da Umgebungsvariablen außerhalb des Codes gesetzt werden können, aber vom Code gelesen werden können und nicht mit den restlichen Dateien gespeichert werden müssen (über `git`), ist es üblich, sie für Konfigurationen oder **Einstellungen** zu verwenden.

Sie können auch eine Umgebungsvariable nur für eine **spezifische Programmausführung** erstellen, die nur für dieses Programm und nur für dessen Dauer verfügbar ist.

Um dies zu tun, erstellen Sie sie direkt vor dem Programm selbst, in derselben Zeile:

<div class="termy">

```console
// Erstellen Sie eine Env Var MY_NAME in derselben Zeile für diesen Programmaufruf
$ MY_NAME="Wade Wilson" python main.py

// Jetzt kann es die Umgebungsvariable lesen

Hello Wade Wilson from Python

// Die Env Var existiert danach nicht mehr
$ python main.py

Hello World from Python
```

</div>

/// tip | Tipp

Sie können mehr darüber in <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a> lesen.

///

## Typen und Validierung

Diese Umgebungsvariablen können nur **Textstrings** handhaben, da sie extern zu Python sind und mit anderen Programmen und dem Rest des Systems (und sogar mit verschiedenen Betriebssystemen wie Linux, Windows, macOS) kompatibel sein müssen.

Das bedeutet, dass **jeder Wert**, der in Python aus einer Umgebungsvariablen gelesen wird, **ein `str`** sein wird. Jede Umwandlung in einen anderen Typ oder jede Validierung muss im Code erfolgen.

Sie werden mehr darüber lernen, wie Umgebungsvariablen zur Handhabung von **Anwendungseinstellungen** verwendet werden, im [Handbuch für fortgeschrittene Benutzer - Einstellungen und Umgebungsvariablen](./advanced/settings.md){.internal-link target=_blank}.

## `PATH`-Umgebungsvariable

Es gibt eine **spezielle** Umgebungsvariable namens **`PATH`**, die von den Betriebssystemen (Linux, macOS, Windows) verwendet wird, um Programme zu finden, die ausgeführt werden sollen.

Der Wert der Variablen `PATH` ist ein langer String, der aus durch Doppelpunkte `:` getrennten Verzeichnissen unter Linux und macOS besteht und unter Windows durch Semikolons `;` getrennt wird.

Zum Beispiel könnte die `PATH`-Umgebungsvariable so aussehen:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Das bedeutet, dass das System in den Verzeichnissen nach Programmen suchen sollte:

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

Das bedeutet, dass das System in den Verzeichnissen nach Programmen suchen sollte:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

Wenn Sie einen **Befehl** im Terminal eingeben, sucht das Betriebssystem das Programm in **jedem dieser Verzeichnisse**, die in der `PATH`-Umgebungsvariable aufgeführt sind.

Zum Beispiel, wenn Sie `python` im Terminal eingeben, sucht das Betriebssystem nach einem Programm namens `python` im **ersten Verzeichnis** in dieser Liste.

Findet es das Programm, wird es **verwendet**. Andernfalls sucht es weiter in den **anderen Verzeichnissen**.

### Python installieren und die `PATH` aktualisieren

Wenn Sie Python installieren, könnten Sie gefragt werden, ob Sie die `PATH`-Umgebungsvariable aktualisieren möchten.

//// tab | Linux, macOS

Angenommen, Sie installieren Python und es landet in einem Verzeichnis `/opt/custompython/bin`.

Wenn Sie ja sagen, um die `PATH`-Umgebungsvariable zu aktualisieren, wird der Installer `/opt/custompython/bin` zur `PATH`-Umgebungsvariable hinzufügen.

Es könnte dann so aussehen:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

Auf diese Weise wird das System, wenn Sie `python` im Terminal eingeben, das Python-Programm in `/opt/custompython/bin` (dem letzten Verzeichnis) finden und dieses verwenden.

////

//// tab | Windows

Angenommen, Sie installieren Python und es endet in einem Verzeichnis `C:\opt\custompython\bin`.

Wenn Sie ja sagen, um die `PATH`-Umgebungsvariable zu aktualisieren, wird der Installer `C:\opt\custompython\bin` zur `PATH` hinzugefügt.

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

Auf diese Weise wird das System, wenn Sie `python` im Terminal eingeben, das Python-Programm in `C:\opt\custompython\bin` (dem letzten Verzeichnis) finden und dieses verwenden.

////

Wenn Sie also eingeben:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

Das System wird das `python`-Programm in `/opt/custompython/bin` finden und es ausführen.

Es wäre ungefähr so, als würden Sie eingeben:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

Das System wird das `python`-Programm in `C:\opt\custompython\bin\python` finden und es ausführen.

Es wäre ungefähr so, als würden Sie eingeben:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

Diese Informationen werden nützlich sein, wenn Sie mehr über [Virtuelle Umgebungen](virtual-environments.md){.internal-link target=_blank} lernen.

## Fazit

Mit diesem Wissen sollten Sie nun ein grundlegendes Verständnis darüber haben, was **Umgebungsvariablen** sind und wie Sie sie in Python verwenden können.

Sie können auch mehr darüber im <a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia-Artikel zu Umgebungsvariablen</a> lesen.

In vielen Fällen ist es nicht sehr offensichtlich, wie Umgebungsvariablen sofort nützlich und anwendbar sein können. Aber sie tauchen in vielen verschiedenen Szenarien beim Entwickeln auf, daher ist es gut, sie zu kennen.

Zum Beispiel werden Sie diese Informationen im nächsten Abschnitt über [Virtuelle Umgebungen](virtual-environments.md) benötigen.
