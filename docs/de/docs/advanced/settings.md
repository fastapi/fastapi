# Einstellungen und Umgebungsvariablen

In vielen Fällen benötigt Ihre Anwendung möglicherweise einige externe Einstellungen oder Konfigurationen, zum Beispiel geheime Schlüssel, Datenbank-Anmeldeinformationen, Anmeldeinformationen für E-Mail-Dienste, usw.

Die meisten dieser Einstellungen sind variabel (können sich ändern), wie z. B. Datenbank-URLs. Und vieles könnten schützenswerte, geheime Daten sein.

Aus diesem Grund werden diese üblicherweise in Umgebungsvariablen bereitgestellt, die von der Anwendung gelesen werden.

## Umgebungsvariablen

/// tip | "Tipp"

Wenn Sie bereits wissen, was „Umgebungsvariablen“ sind und wie man sie verwendet, können Sie gerne mit dem nächsten Abschnitt weiter unten fortfahren.

///

Eine <a href="https://de.wikipedia.org/wiki/Umgebungsvariable" class="external-link" target="_blank">Umgebungsvariable</a> (auch bekannt als „env var“) ist eine Variable, die sich außerhalb des Python-Codes im Betriebssystem befindet und von Ihrem Python-Code (oder auch von anderen Programmen) gelesen werden kann.

Sie können Umgebungsvariablen in der Shell erstellen und verwenden, ohne Python zu benötigen:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Sie könnten eine Umgebungsvariable MY_NAME erstellen mittels
$ export MY_NAME="Wade Wilson"

// Dann könnten Sie diese mit anderen Programmen verwenden, etwa
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Erstelle eine Umgebungsvariable MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Verwende sie mit anderen Programmen, etwa
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

### Umgebungsvariablen mit Python auslesen

Sie können Umgebungsvariablen auch außerhalb von Python im Terminal (oder mit einer anderen Methode) erstellen und diese dann mit Python auslesen.

Sie könnten zum Beispiel eine Datei `main.py` haben mit:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | "Tipp"

Das zweite Argument für <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> ist der zurückzugebende Defaultwert.

Wenn nicht angegeben, ist er standardmäßig `None`. Hier übergeben wir `"World"` als Defaultwert.

///

Dann könnten Sie dieses Python-Programm aufrufen:

<div class="termy">

```console
// Hier legen wir die Umgebungsvariable noch nicht fest
$ python main.py

// Da wir die Umgebungsvariable nicht festgelegt haben, erhalten wir den Standardwert

Hello World from Python

// Aber wenn wir zuerst eine Umgebungsvariable erstellen
$ export MY_NAME="Wade Wilson"

// Und dann das Programm erneut aufrufen
$ python main.py

// Kann es jetzt die Umgebungsvariable lesen

Hello Wade Wilson from Python
```

</div>

Da Umgebungsvariablen außerhalb des Codes festgelegt, aber vom Code gelesen werden können und nicht zusammen mit den übrigen Dateien gespeichert (an `git` committet) werden müssen, werden sie häufig für Konfigurationen oder Einstellungen verwendet.

Sie können eine Umgebungsvariable auch nur für einen bestimmten Programmaufruf erstellen, die nur für dieses Programm und nur für dessen Dauer verfügbar ist.

Erstellen Sie diese dazu direkt vor dem Programm selbst, in derselben Zeile:

<div class="termy">

```console
// Erstelle eine Umgebungsvariable MY_NAME inline für diesen Programmaufruf
$ MY_NAME="Wade Wilson" python main.py

// main.py kann jetzt diese Umgebungsvariable lesen

Hello Wade Wilson from Python

// Die Umgebungsvariable existiert danach nicht mehr
$ python main.py

Hello World from Python
```

</div>

/// tip | "Tipp"

Weitere Informationen dazu finden Sie unter <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a>.

///

### Typen und Validierung

Diese Umgebungsvariablen können nur Text-Zeichenketten verarbeiten, da sie außerhalb von Python liegen und mit anderen Programmen und dem Rest des Systems (und sogar mit verschiedenen Betriebssystemen wie Linux, Windows, macOS) kompatibel sein müssen.

Das bedeutet, dass jeder in Python aus einer Umgebungsvariablen gelesene Wert ein `str` ist und jede Konvertierung in einen anderen Typ oder jede Validierung im Code erfolgen muss.

## Pydantic `Settings`

Glücklicherweise bietet Pydantic ein großartiges Werkzeug zur Verarbeitung dieser Einstellungen, die von Umgebungsvariablen stammen, mit <a href="https://docs.pydantic.dev/latest/concepts/pydantic_settings/" class="external-link" target="_blank">Pydantic: Settings Management</a>.

### `pydantic-settings` installieren

Installieren Sie zunächst das Package `pydantic-settings`:

<div class="termy">

```console
$ pip install pydantic-settings
---> 100%
```

</div>

Es ist bereits enthalten, wenn Sie die `all`-Extras installiert haben, mit:

<div class="termy">

```console
$ pip install "fastapi[all]"
---> 100%
```

</div>

/// info

In Pydantic v1 war das im Hauptpackage enthalten. Jetzt wird es als unabhängiges Package verteilt, sodass Sie wählen können, ob Sie es installieren möchten oder nicht, falls Sie die Funktionalität nicht benötigen.

///

### Das `Settings`-Objekt erstellen

Importieren Sie `BaseSettings` aus Pydantic und erstellen Sie eine Unterklasse, ganz ähnlich wie bei einem Pydantic-Modell.

Auf die gleiche Weise wie bei Pydantic-Modellen deklarieren Sie Klassenattribute mit Typannotationen und möglicherweise Defaultwerten.

Sie können dieselben Validierungs-Funktionen und -Tools verwenden, die Sie für Pydantic-Modelle verwenden, z. B. verschiedene Datentypen und zusätzliche Validierungen mit `Field()`.

//// tab | Pydantic v2

```Python hl_lines="2  5-8  11"
{!> ../../../docs_src/settings/tutorial001.py!}
```

////

//// tab | Pydantic v1

/// info

In Pydantic v1 würden Sie `BaseSettings` direkt von `pydantic` statt von `pydantic_settings` importieren.

///

```Python hl_lines="2  5-8  11"
{!> ../../../docs_src/settings/tutorial001_pv1.py!}
```

////

/// tip | "Tipp"

Für ein schnelles Copy-and-paste verwenden Sie nicht dieses Beispiel, sondern das letzte unten.

///

Wenn Sie dann eine Instanz dieser `Settings`-Klasse erstellen (in diesem Fall als `settings`-Objekt), liest Pydantic die Umgebungsvariablen ohne Berücksichtigung der Groß- und Kleinschreibung. Eine Variable `APP_NAME` in Großbuchstaben wird also als Attribut `app_name` gelesen.

Als Nächstes werden die Daten konvertiert und validiert. Wenn Sie also dieses `settings`-Objekt verwenden, verfügen Sie über Daten mit den von Ihnen deklarierten Typen (z. B. ist `items_per_user` ein `int`).

### `settings` verwenden

Dann können Sie das neue `settings`-Objekt in Ihrer Anwendung verwenden:

```Python hl_lines="18-20"
{!../../../docs_src/settings/tutorial001.py!}
```

### Den Server ausführen

Als Nächstes würden Sie den Server ausführen und die Konfigurationen als Umgebungsvariablen übergeben. Sie könnten beispielsweise `ADMIN_EMAIL` und `APP_NAME` festlegen mit:

<div class="termy">

```console
$ ADMIN_EMAIL="deadpool@example.com" APP_NAME="ChimichangApp" uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

/// tip | "Tipp"

Um mehrere Umgebungsvariablen für einen einzelnen Befehl festzulegen, trennen Sie diese einfach durch ein Leerzeichen und fügen Sie alle vor dem Befehl ein.

///

Und dann würde die Einstellung `admin_email` auf `"deadpool@example.com"` gesetzt.

Der `app_name` wäre `"ChimichangApp"`.

Und `items_per_user` würde seinen Standardwert von `50` behalten.

## Einstellungen in einem anderen Modul

Sie könnten diese Einstellungen in eine andere Moduldatei einfügen, wie Sie in [Größere Anwendungen – mehrere Dateien](../tutorial/bigger-applications.md){.internal-link target=_blank} gesehen haben.

Sie könnten beispielsweise eine Datei `config.py` haben mit:

```Python
{!../../../docs_src/settings/app01/config.py!}
```

Und dann verwenden Sie diese in einer Datei `main.py`:

```Python hl_lines="3  11-13"
{!../../../docs_src/settings/app01/main.py!}
```

/// tip | "Tipp"

Sie benötigen außerdem eine Datei `__init__.py`, wie in [Größere Anwendungen – mehrere Dateien](../tutorial/bigger-applications.md){.internal-link target=_blank} gesehen.

///

## Einstellungen in einer Abhängigkeit

In manchen Fällen kann es nützlich sein, die Einstellungen mit einer Abhängigkeit bereitzustellen, anstatt ein globales Objekt `settings` zu haben, das überall verwendet wird.

Dies könnte besonders beim Testen nützlich sein, da es sehr einfach ist, eine Abhängigkeit mit Ihren eigenen benutzerdefinierten Einstellungen zu überschreiben.

### Die Konfigurationsdatei

Ausgehend vom vorherigen Beispiel könnte Ihre Datei `config.py` so aussehen:

```Python hl_lines="10"
{!../../../docs_src/settings/app02/config.py!}
```

Beachten Sie, dass wir jetzt keine Standardinstanz `settings = Settings()` erstellen.

### Die Haupt-Anwendungsdatei

Jetzt erstellen wir eine Abhängigkeit, die ein neues `config.Settings()` zurückgibt.

//// tab | Python 3.9+

```Python hl_lines="6  12-13"
{!> ../../../docs_src/settings/app02_an_py39/main.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="6  12-13"
{!> ../../../docs_src/settings/app02_an/main.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="5  11-12"
{!> ../../../docs_src/settings/app02/main.py!}
```

////

/// tip | "Tipp"

Wir werden das `@lru_cache` in Kürze besprechen.

Im Moment nehmen Sie an, dass `get_settings()` eine normale Funktion ist.

///

Und dann können wir das von der *Pfadoperation-Funktion* als Abhängigkeit einfordern und es überall dort verwenden, wo wir es brauchen.

//// tab | Python 3.9+

```Python hl_lines="17  19-21"
{!> ../../../docs_src/settings/app02_an_py39/main.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="17  19-21"
{!> ../../../docs_src/settings/app02_an/main.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="16  18-20"
{!> ../../../docs_src/settings/app02/main.py!}
```

////

### Einstellungen und Tests

Dann wäre es sehr einfach, beim Testen ein anderes Einstellungsobjekt bereitzustellen, indem man eine Abhängigkeitsüberschreibung für `get_settings` erstellt:

```Python hl_lines="9-10  13  21"
{!../../../docs_src/settings/app02/test_main.py!}
```

Bei der Abhängigkeitsüberschreibung legen wir einen neuen Wert für `admin_email` fest, wenn wir das neue `Settings`-Objekt erstellen, und geben dann dieses neue Objekt zurück.

Dann können wir testen, ob das verwendet wird.

## Lesen einer `.env`-Datei

Wenn Sie viele Einstellungen haben, die sich möglicherweise oft ändern, vielleicht in verschiedenen Umgebungen, kann es nützlich sein, diese in eine Datei zu schreiben und sie dann daraus zu lesen, als wären sie Umgebungsvariablen.

Diese Praxis ist so weit verbreitet, dass sie einen Namen hat. Diese Umgebungsvariablen werden üblicherweise in einer Datei `.env` abgelegt und die Datei wird „dotenv“ genannt.

/// tip | "Tipp"

Eine Datei, die mit einem Punkt (`.`) beginnt, ist eine versteckte Datei in Unix-ähnlichen Systemen wie Linux und macOS.

Aber eine dotenv-Datei muss nicht unbedingt genau diesen Dateinamen haben.

///

Pydantic unterstützt das Lesen dieser Dateitypen mithilfe einer externen Bibliothek. Weitere Informationen finden Sie unter <a href="https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support" class="external-link" target="_blank">Pydantic Settings: Dotenv (.env) support</a>.

/// tip | "Tipp"

Damit das funktioniert, müssen Sie `pip install python-dotenv` ausführen.

///

### Die `.env`-Datei

Sie könnten eine `.env`-Datei haben, mit:

```bash
ADMIN_EMAIL="deadpool@example.com"
APP_NAME="ChimichangApp"
```

### Einstellungen aus `.env` lesen

Und dann aktualisieren Sie Ihre `config.py` mit:

//// tab | Pydantic v2

```Python hl_lines="9"
{!> ../../../docs_src/settings/app03_an/config.py!}
```

/// tip | "Tipp"

Das Attribut `model_config` wird nur für die Pydantic-Konfiguration verwendet. Weitere Informationen finden Sie unter <a href="https://docs.pydantic.dev/latest/concepts/config/" class="external-link" target="_blank">Pydantic: Configuration</a>.

///

////

//// tab | Pydantic v1

```Python hl_lines="9-10"
{!> ../../../docs_src/settings/app03_an/config_pv1.py!}
```

/// tip | "Tipp"

Die Klasse `Config` wird nur für die Pydantic-Konfiguration verwendet. Weitere Informationen finden Sie unter <a href="https://docs.pydantic.dev/1.10/usage/model_config/" class="external-link" target="_blank">Pydantic Model Config</a>.

///

////

/// info

In Pydantic Version 1 erfolgte die Konfiguration in einer internen Klasse `Config`, in Pydantic Version 2 erfolgt sie in einem Attribut `model_config`. Dieses Attribut akzeptiert ein `dict`. Um automatische Codevervollständigung und Inline-Fehlerberichte zu erhalten, können Sie `SettingsConfigDict` importieren und verwenden, um dieses `dict` zu definieren.

///

Hier definieren wir die Konfiguration `env_file` innerhalb Ihrer Pydantic-`Settings`-Klasse und setzen den Wert auf den Dateinamen mit der dotenv-Datei, die wir verwenden möchten.

### Die `Settings` nur einmal laden mittels `lru_cache`

Das Lesen einer Datei von der Festplatte ist normalerweise ein kostspieliger (langsamer) Vorgang, daher möchten Sie ihn wahrscheinlich nur einmal ausführen und dann dasselbe Einstellungsobjekt erneut verwenden, anstatt es für jeden Request zu lesen.

Aber jedes Mal, wenn wir ausführen:

```Python
Settings()
```

würde ein neues `Settings`-Objekt erstellt und bei der Erstellung würde die `.env`-Datei erneut ausgelesen.

Wenn die Abhängigkeitsfunktion wie folgt wäre:

```Python
def get_settings():
    return Settings()
```

würden wir dieses Objekt für jeden Request erstellen und die `.env`-Datei für jeden Request lesen. ⚠️

Da wir jedoch den `@lru_cache`-Dekorator oben verwenden, wird das `Settings`-Objekt nur einmal erstellt, nämlich beim ersten Aufruf. ✔️

//// tab | Python 3.9+

```Python hl_lines="1  11"
{!> ../../../docs_src/settings/app03_an_py39/main.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  11"
{!> ../../../docs_src/settings/app03_an/main.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="1  10"
{!> ../../../docs_src/settings/app03/main.py!}
```

////

Dann wird bei allen nachfolgenden Aufrufen von `get_settings()`, in den Abhängigkeiten für darauffolgende Requests, dasselbe Objekt zurückgegeben, das beim ersten Aufruf zurückgegeben wurde, anstatt den Code von `get_settings()` erneut auszuführen und ein neues `Settings`-Objekt zu erstellen.

#### Technische Details zu `lru_cache`

`@lru_cache` ändert die Funktion, die es dekoriert, dahingehend, denselben Wert zurückzugeben, der beim ersten Mal zurückgegeben wurde, anstatt ihn erneut zu berechnen und den Code der Funktion jedes Mal auszuführen.

Die darunter liegende Funktion wird also für jede Argumentkombination einmal ausgeführt. Und dann werden die von jeder dieser Argumentkombinationen zurückgegebenen Werte immer wieder verwendet, wenn die Funktion mit genau derselben Argumentkombination aufgerufen wird.

Wenn Sie beispielsweise eine Funktion haben:

```Python
@lru_cache
def say_hi(name: str, salutation: str = "Ms."):
    return f"Hello {salutation} {name}"
```

könnte Ihr Programm so ausgeführt werden:

```mermaid
sequenceDiagram

participant code as Code
participant function as say_hi()
participant execute as Funktion ausgeführt

    rect rgba(0, 255, 0, .1)
        code ->> function: say_hi(name="Camila")
        function ->> execute: führe Code der Funktion aus
        execute ->> code: gib das Resultat zurück
    end

    rect rgba(0, 255, 255, .1)
        code ->> function: say_hi(name="Camila")
        function ->> code: gib das gespeicherte Resultat zurück
    end

    rect rgba(0, 255, 0, .1)
        code ->> function: say_hi(name="Rick")
        function ->> execute: führe Code der Funktion aus
        execute ->> code: gib das Resultat zurück
    end

    rect rgba(0, 255, 0, .1)
        code ->> function: say_hi(name="Rick", salutation="Mr.")
        function ->> execute: führe Code der Funktion aus
        execute ->> code: gib das Resultat zurück
    end

    rect rgba(0, 255, 255, .1)
        code ->> function: say_hi(name="Rick")
        function ->> code: gib das gespeicherte Resultat zurück
    end

    rect rgba(0, 255, 255, .1)
        code ->> function: say_hi(name="Camila")
        function ->> code: gib das gespeicherte Resultat zurück
    end
```

Im Fall unserer Abhängigkeit `get_settings()` akzeptiert die Funktion nicht einmal Argumente, sodass sie immer den gleichen Wert zurückgibt.

Auf diese Weise verhält es sich fast so, als wäre es nur eine globale Variable. Da es jedoch eine Abhängigkeitsfunktion verwendet, können wir diese zu Testzwecken problemlos überschreiben.

`@lru_cache` ist Teil von `functools`, welches Teil von Pythons Standardbibliothek ist. Weitere Informationen dazu finden Sie in der <a href="https://docs.python.org/3/library/functools.html#functools.lru_cache" class="external-link" target="_blank">Python Dokumentation für `@lru_cache`</a>.

## Zusammenfassung

Mit Pydantic Settings können Sie die Einstellungen oder Konfigurationen für Ihre Anwendung verwalten und dabei die gesamte Leistungsfähigkeit der Pydantic-Modelle nutzen.

* Durch die Verwendung einer Abhängigkeit können Sie das Testen vereinfachen.
* Sie können `.env`-Dateien damit verwenden.
* Durch die Verwendung von `@lru_cache` können Sie vermeiden, die dotenv-Datei bei jedem Request erneut zu lesen, während Sie sie während des Testens überschreiben können.
