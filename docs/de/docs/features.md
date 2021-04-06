# Funktionen

## FastAPI Funktionen:

Mit **FastAPI** erhalten Sie Folgendes:

### Basierend auf offenen Standards

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> für die API-Erstellung, einschließlich Deklarationen von <abbr title="auch bekannt als: Endpunkte, Routen">Pfad</abbr>, <abbr title="auch bekannt als HTTP-Methoden, wie POST, GET, PUT, DELETE">Operationen</abbr>, Parameter, Body-Requests, Sicherheit, etc.
* Automatische Datenmodell-Dokumentation mit <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (da OpenAPI selbst auf JSON Schema basiert).
* Entworfen um diese Standards herum, nach einer akribischen Studie. Statt einer nachträglich aufgesetzten Schicht.
* Dies ermöglicht auch die Verwendung einer automatischen **Client-Code-Generierung** in vielen Sprachen.

### Automatische Dokumentation

Interaktive API-Dokumentation und Web-Benutzeroberflächen zur Analyse. Da das Framework auf OpenAPI basiert, gibt es mehrere Optionen, 2 sind standardmäßig enthalten.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, mit interaktiver Auswertung, Aufruf und Test Ihrer API direkt aus dem Browser.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Alternative API-Dokumentation mit <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Einfach modernes Python

Es basiert alles auf Standard **Python 3.6 Typ**-Deklarationen (dank Pydantic). Sie müssen keine neue Syntax lernen. Nur modernes Standard-Python.

Wenn Sie eine 2-minütige Auffrischung benötigen, wie man Python-Typen verwendet (auch wenn Sie FastAPI nicht verwenden), sehen Sie sich das kurze Tutorial an: [Python Types](python-types.md){.internal-link target=_blank}.

Sie schreiben Standard-Python mit Typen:


```Python
from typing import List, Dict
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Das kann dann wie folgt verwendet werden:
```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! info
    `**second_user_data` bedeutet:

    Übergeben Sie die Schlüssel und Werte des Dictionarys `second_user_data` direkt als Schlüssel-Wert-Argumente, entsprechend: `User(id=4, name="Mary", joined="2018-11-30")`

### Editor-Unterstützung

Das gesamte Framework wurde so konzipiert, dass es einfach und intuitiv zu bedienen ist. Alle Entscheidungen wurden bereits vor Beginn der Entwicklung auf mehreren Editoren getestet, um die beste Entwicklungserfahrung zu gewährleisten.

In der letzten Python-Entwicklerumfrage wurde deutlich, <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">dass die am meisten genutzte Funktion "Autovervollständigung"</a> ist.

Das gesamte **FastAPI**-Framework ist darauf ausgerichtet, dies zu erfüllen. Die Autovervollständigung funktioniert überall.

Sie werden nur selten auf die Dokumentation zurückkommen müssen.

Hier ein Beispiel, wie Ihr Editor Ihnen helfen kann:

* in <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* in <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Sie erhalten Vervollständigung in Code, den Sie vorher vielleicht sogar für unmöglich hielten. Wie zum Beispiel der Schlüssel "price" in einem JSON-Body (der verschachtelt sein könnte), der von einer Anfrage kommt.

Sie müssen nicht mehr die falschen Schlüsselnamen eintippen, zwischen den Dokumenten hin- und herspringen oder nach oben und unten scrollen, um herauszufinden, ob Sie letztendlich `username` oder `user_name` verwendet haben.

### Kurz

Es hat sinnvolle **Standardwerte** für alles, mit optionalen Konfigurationen überall. Alle Parameter können fein abgestimmt werden, um das zu tun, was Sie brauchen, und um die API zu definieren, die Sie brauchen.

Aber standardmäßig funktioniert das alles **"einfach so "**.

### Validierung

* Validierung für die meisten (oder alle?) Python **Datentypen**, einschließlich:
    * JSON-Objekte (`dict`).
    * JSON-Arrays (`list`), die Elementtypen definieren.
    * String-Felder (`str`), die minimale und maximale Längen definieren.
    * Zahlen (`int`, `float`) mit Min- und Max-Werten, etc.

* Validierung für exotischere Typen, wie:
    * URL.
    * E-Mail.
    * UUID.
    * ...und andere.

Die gesamte Validierung wird von dem bewährten und robusten **Pydantic** übernommen.

### Sicherheit und Authentifizierung

Sicherheit und Authentifizierung integriert. Ohne Kompromisse bei Datenbanken oder Datenmodellen.

Alle in OpenAPI definierten Sicherheitsschemata, einschließlich:

* HTTP Basic.
* **OAuth2** (auch mit **JWT-Tokens**). Lesen Sie das Tutorial zu [OAuth2 mit JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* API-Schlüssel in:
    * Header.
    * Abfrageparameter.
    * Cookies, etc.

Plus alle Sicherheitsfunktionen von Starlette (einschließlich **Session Cookies**).

Alles aufgebaut als wiederverwendbare Tools und Komponenten, die sich leicht in Ihre Systeme, Datenspeicher, Relationalen-Datenbanken und NoSQL-Datenbanken usw. integrieren lassen.

### Dependency Injection

FastAPI beinhaltet ein extrem einfach zu bedienendes, aber äußerst leistungsfähiges <abbr title='auch bekannt als "Komponenten", "Ressourcen", "Services", "Provider"'><strong>Dependency Injection</strong></abbr> System.

* Auch Abhängigkeiten können Abhängigkeiten haben, wodurch eine Hierarchie oder ein **"Graph" von Abhängigkeiten** entsteht.
* Alle **automatisch behandelt** durch das Framework.
* Alle Abhängigkeiten können Daten von Anfragen anfordern und die **Pfadoperationen** einschränken und automatisch dokumentieren.
* **Automatische Validierung** auch für die in den Abhängigkeiten definierten Parameter der *Pfadoperationen**.
* Unterstützung für komplexe Benutzerauthentifizierungssysteme, **Datenbankverbindungen**, etc.
* **Keine Kompromisse** mit Datenbanken, Frontends, etc. Sondern einfache Integration mit allen von ihnen.

### Unbegrenzte "plug-ins"

Oder anders ausgedrückt: Sie brauchen sie nicht, importieren und verwenden Sie den Code, den Sie benötigen.

Jede Integration soll so einfach zu bedienen sein (mit Abhängigkeiten), dass Sie in 2 Zeilen Code ein "Plug-in" für Ihre Anwendung erstellen können, das die gleiche Struktur und Syntax verwendet wie Ihre *Pfad-Operationen*.

### Getestet

* 100% <abbr title="Der Anteil des Codes, der automatisch getestet wird">Testabdeckung</abbr>.
* 100% <abbr title="Python-Typ-Annotationen, damit Ihr Editor und externe Tools Sie besser unterstützen können">Typ-annotierte</abbr> Codebasis.
* Wird in Produktionsanwendungen eingesetzt.

## Eigenschaften von Starlette

**FastAPI** ist vollständig kompatibel mit (und basiert auf) <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong></a>. Das heißt, jeder zusätzliche Starlette-Code, den Sie haben, wird auch funktionieren.

`FastAPI` ist eigentlich eine Unterklasse von `Starlette`. Wenn Sie also Starlette bereits kennen oder verwenden, wird der größte Teil der Funktionalität auf die gleiche Weise funktionieren.

Mit **FastAPI** erhalten Sie alle Funktionen von **Starlette** (da FastAPI nur Starlette auf Steroiden ist):

* Ernsthaft beeindruckende Leistung. Es ist <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">eines der schnellsten verfügbaren Python-Frameworks, auf Augenhöhe mit **NodeJS** und **Go**</a>.
* **WebSocket**-Unterstützung.
* **GraphQL**-Unterstützung.
* Prozessinterne Hintergrundaufgaben.
* Startup- und Shutdown-Ereignisse.
* Test-Client, der auf **Requests** aufbaut.
* **CORS**, GZip, Statische Dateien, Streaming-Antworten.
* **Session- und Cookie**-Unterstützung.
* 100% Testabdeckung.
* 100% typ-kommentierte Codebasis.

## Eigenschaften von Pydantic

**FastAPI** ist vollständig kompatibel mit (und basiert auf) <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a>. Das heißt, jeder zusätzliche Pydantic-Code, den Sie haben, wird auch funktionieren.

Einschließlich externer Bibliotheken, die ebenfalls auf Pydantic basieren, wie <abbr title="Object-Relational Mapper">ORM</abbr>s, <abbr title="Object-Document Mapper">ODM</abbr>s für Datenbanken.

Das bedeutet auch, dass Sie in vielen Fällen das gleiche Objekt, das Sie von einer Anfrage erhalten, **direkt an die Datenbank** übergeben können, da alles automatisch validiert wird.

Das Gleiche gilt umgekehrt, in vielen Fällen können Sie das Objekt, das Sie von der Datenbank erhalten, **direkt an den Client** weitergeben.

Mit **FastAPI** erhalten Sie alle Funktionen von **Pydantic** (da FastAPI für die gesamte Datenverarbeitung auf Pydantic basiert):

**Kein Brainfuck**:
    * Keine neue Schema-definitions Mikrosprache zu lernen.
    * Wenn Sie Python-Typen kennen, wissen Sie, wie Sie Pydantic verwenden können.
* Spielt gut mit Ihrem **<abbr title="Integrated Development Environment, ähnlich einem Code-Editor">IDE</abbr>/<abbr title="Ein Programm, das auf Code-Fehler prüft">Liner</abbr>/Gehirn**:
    * Weil Pydantic Datenstrukturen nur Instanzen von Klassen sind, die Sie definieren; Autovervollständigung, Linting, mypy und Ihre Intuition sollten alle korrekt mit Ihren validierten Daten arbeiten.
* **Schnell**:
    * In <a href="https://pydantic-docs.helpmanual.io/#benchmarks-tag" class="external-link" target="_blank">Benchmarks</a> ist Pydantic schneller als alle anderen getesteten Bibliotheken.
* Validierung **komplexer Strukturen**:
    * Verwendung von hierarchischen Pydantic-Modellen, Python `typing`'s `List` und `Dict`, etc.
    * Und mit Validatoren lassen sich komplexe Datenschemata klar und einfach definieren, prüfen und als JSON-Schema dokumentieren.
    * Sie können tief **verschachtelte JSON**-Objekte haben und sie alle validieren und annotieren lassen.
* **Erweiterbar**:
    * Pydantic erlaubt die Definition von benutzerdefinierten Datentypen oder Sie können die Validierung mit Methoden auf einem mit dem Validator-Dekorator dekorierten Modell erweitern.
* 100 % Testabdeckung.
