# Merkmale { #features }

## FastAPI-Merkmale { #fastapi-features }

**FastAPI** ermöglicht Ihnen Folgendes:

### Auf offenen Standards basieren { #based-on-open-standards }

* [**OpenAPI**](https://github.com/OAI/OpenAPI-Specification) für die Erstellung von APIs, inklusive Deklarationen von <dfn title="auch bekannt als: Endpunkte, Routen">Pfad</dfn>-<dfn title="auch bekannt als HTTP-Methoden, wie POST, GET, PUT, DELETE">Operationen</dfn>, Parametern, <abbr title="Requestbody">Requestbodys</abbr>, Sicherheit, usw.
* Automatische Dokumentation der Datenmodelle mit [**JSON Schema**](https://json-schema.org/) (da OpenAPI selbst auf JSON Schema basiert).
* Um diese Standards herum entworfen, nach sorgfältigem Studium. Statt einer nachträglichen Schicht darüber.
* Dies ermöglicht auch automatische **Client-Code-Generierung** in vielen Sprachen.

### Automatische Dokumentation { #automatic-docs }

Interaktive API-Dokumentation und erkundbare Web-Benutzeroberflächen. Da das Framework auf OpenAPI basiert, gibt es mehrere Optionen, zwei sind standardmäßig vorhanden.

* [**Swagger UI**](https://github.com/swagger-api/swagger-ui), mit interaktiver Erkundung, rufen Sie Ihre API direkt vom Browser aus auf und testen Sie sie.

![Swagger UI Interaktion](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Alternative API-Dokumentation mit [**ReDoc**](https://github.com/Rebilly/ReDoc).

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Nur modernes Python { #just-modern-python }

Alles basiert auf Standard-**Python-Typ**deklarationen (dank Pydantic). Es muss keine neue Syntax gelernt werden, nur standardisiertes modernes Python.

Wenn Sie eine zweiminütige Auffrischung benötigen, wie man Python-Typen verwendet (auch wenn Sie FastAPI nicht benutzen), schauen Sie sich das kurze Tutorial an: [Einführung in Python-Typen](python-types.md).

Sie schreiben Standard-Python mit Typen:

```Python
from datetime import date

from pydantic import BaseModel

# Deklarieren Sie eine Variable vom Typ str
# und bekommen Sie Editor-Unterstützung innerhalb der Funktion
def main(user_id: str):
    return user_id


# Ein Pydantic-Modell
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Das kann nun wie folgt verwendet werden:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

/// note | Hinweis

`**second_user_data` bedeutet:

Übergeben Sie die Schlüssel und Werte des `second_user_data` <abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">Dicts</abbr> direkt als Schlüssel-Wert-Argumente, äquivalent zu: `User(id=4, name="Mary", joined="2018-11-30")`

///

### Editorunterstützung { #editor-support }

Das ganze Framework wurde so entworfen, dass es einfach und intuitiv zu benutzen ist; alle Entscheidungen wurden auf mehreren Editoren getestet, sogar vor der Implementierung, um die bestmögliche Entwicklererfahrung zu gewährleisten.

In den Python-Entwickler-Umfragen wird klar, [dass die meist genutzte Funktion die „Autovervollständigung“ ist](https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features).

Das gesamte **FastAPI**-Framework ist darauf ausgelegt, das zu erfüllen. Autovervollständigung funktioniert überall.

Sie werden selten noch mal in der Dokumentation nachschauen müssen.

So kann Ihr Editor Sie unterstützen:

* in [Visual Studio Code](https://code.visualstudio.com/):

![Editorunterstützung](https://fastapi.tiangolo.com/img/vscode-completion.png)

* in [PyCharm](https://www.jetbrains.com/pycharm/):

![Editorunterstützung](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Sie bekommen sogar Autovervollständigung an Stellen, an denen Sie dies vorher nicht für möglich gehalten hätten. Zum Beispiel der `price`-Schlüssel innerhalb eines JSON-Bodys (dieser könnte auch verschachtelt sein), der aus einem Request kommt.

Nie wieder falsche Schlüsselnamen tippen, Hin und Herhüpfen zwischen der Dokumentation, Hoch- und Runterscrollen, um herauszufinden, ob es `username` oder `user_name` war.

### Kompakt { #short }

Es gibt für alles sinnvolle **Defaultwerte**, mit optionaler Konfiguration überall. Alle Parameter können feinjustiert werden, damit sie tun, was Sie benötigen, und die API definieren, die Sie brauchen.

Aber standardmäßig **„funktioniert einfach alles“**.

### Validierung { #validation }

* Validierung für die meisten (oder alle?) Python-**Datentypen**, hierzu gehören:
    * JSON-Objekte (`dict`).
    * JSON-Array (`list`), das Elementtypen definiert.
    * String-Felder (`str`) mit definierter minimaler und maximaler Länge.
    * Zahlen (`int`, `float`) mit Mindest- und Maximalwerten, usw.

* Validierung für exotischere Typen, wie:
    * URL.
    * E-Mail.
    * UUID.
    * ... und andere.

Die gesamte Validierung übernimmt das gut etablierte und robuste **Pydantic**.

### Sicherheit und Authentifizierung { #security-and-authentication }

Sicherheit und Authentifizierung sind integriert. Ohne Kompromisse bei Datenbanken oder Datenmodellen.

Alle in OpenAPI definierten Sicherheitsschemas, inklusive:

* HTTP Basic.
* **OAuth2** (auch mit **JWT-Tokens**). Siehe dazu das Tutorial zu [OAuth2 mit JWT](tutorial/security/oauth2-jwt.md).
* API-Schlüssel in:
    * Headern.
    * Query-Parametern.
    * Cookies, usw.

Zusätzlich alle Sicherheitsfunktionen von Starlette (inklusive **Session-Cookies**).

Alles als wiederverwendbare Tools und Komponenten gebaut, die einfach in Ihre Systeme, Datenspeicher, relationale und NoSQL-Datenbanken, usw., integriert werden können.

### Dependency Injection { #dependency-injection }

FastAPI enthält ein extrem einfach zu verwendendes, aber extrem mächtiges <dfn title='auch bekannt als „Komponenten“, „Ressourcen“, „Dienste“, „Anbieter“'><strong>Dependency Injection</strong></dfn>-System.

* Selbst Abhängigkeiten können Abhängigkeiten haben, woraus eine Hierarchie oder ein **„Graph“ von Abhängigkeiten** entsteht.
* Alles **automatisch gehandhabt** durch das Framework.
* Alle Abhängigkeiten können Daten von Requests anfordern und die Einschränkungen der **Pfadoperationen** sowie die automatische Dokumentation **erweitern**.
* **Automatische Validierung** selbst für solche Parameter von *Pfadoperationen*, welche in Abhängigkeiten definiert sind.
* Unterstützung für komplexe Benutzerauthentifizierungssysteme, **Datenbankverbindungen**, usw.
* **Keine Kompromisse** bei Datenbanken, Frontends, usw., sondern einfache Integration mit allen.

### Unbegrenzte „Plug-ins“ { #unlimited-plug-ins }

Oder mit anderen Worten, sie werden nicht benötigt. Importieren und nutzen Sie den Code, den Sie brauchen.

Jede Integration wurde so entworfen, dass sie so einfach zu nutzen ist (mit Abhängigkeiten), dass Sie ein „Plug-in“ für Ihre Anwendung mit nur 2 Zeilen Code erstellen können. Hierbei nutzen Sie die gleiche Struktur und Syntax, wie bei *Pfadoperationen*.

### Getestet { #tested }

* 100 % <dfn title="Der Prozentsatz an Code, der automatisch getestet wird">Testabdeckung</dfn>.
* Zu 100 % <dfn title="Python-Typannotationen, mit denen Ihr Editor und andere externe Werkzeuge Sie besser unterstützen können">typannotierte</dfn> Codebasis.
* Verwendet in Produktionsanwendungen.

## Starlette-Merkmale { #starlette-features }

**FastAPI** ist vollkommen kompatibel (und basiert auf) [**Starlette**](https://www.starlette.dev/). Das bedeutet, wenn Sie eigenen Starlette-Quellcode haben, funktioniert dieser auch.

`FastAPI` ist tatsächlich eine Unterklasse von `Starlette`. Wenn Sie also bereits Starlette kennen oder benutzen, das meiste funktioniert genau so.

Mit **FastAPI** bekommen Sie alles von **Starlette** (da FastAPI nur Starlette auf Steroiden ist):

* Schwer beeindruckende Performanz. Es ist [eines der schnellsten Python-Frameworks, auf Augenhöhe mit **NodeJS** und **Go**](https://github.com/encode/starlette#performance).
* **WebSocket**-Unterstützung.
* Hintergrundtasks im selben Prozess.
* Startup- und Shutdown-Events.
* Testclient basierend auf HTTPX.
* **CORS**, GZip, statische Dateien, Responses streamen.
* **Sitzungs- und Cookie**-Unterstützung.
* 100 % Testabdeckung.
* Zu 100 % typannotierte Codebasis.

## Pydantic-Merkmale { #pydantic-features }

**FastAPI** ist vollkommen kompatibel (und basiert auf) [**Pydantic**](https://docs.pydantic.dev/). Das bedeutet, wenn Sie eigenen Pydantic-Quellcode haben, funktioniert dieser auch.

Inklusive externer Bibliotheken, die auf Pydantic basieren, wie <abbr title="Object-Relational Mapper - Objektrelationaler Mapper">ORM</abbr>s, <abbr title="Object-Document Mapper - Objekt-Dokument-Mapper">ODM</abbr>s für Datenbanken.

Daher können Sie in vielen Fällen das Objekt eines Requests **direkt zur Datenbank** schicken, weil alles automatisch validiert wird.

Das gleiche gilt auch für die andere Richtung: Sie können in vielen Fällen das Objekt aus der Datenbank **direkt zum Client** senden.

Mit **FastAPI** bekommen Sie alle Funktionen von **Pydantic** (da FastAPI für die gesamte Datenverarbeitung Pydantic nutzt):

* **Kein Kopfzerbrechen**:
    * Keine neue Schemadefinitions-Mikrosprache zu lernen.
    * Wenn Sie Pythons Typen kennen, wissen Sie, wie man Pydantic verwendet.
* Gutes Zusammenspiel mit Ihrer/Ihrem **<abbr title="Integrated Development Environment - Integrierte Entwicklungsumgebung: Ähnlich einem Code-Editor">IDE</abbr>/<dfn title="Ein Programm, das Fehler im Quellcode sucht">Linter</dfn>/Gehirn**:
    * Weil Pydantics Datenstrukturen einfach nur Instanzen ihrer definierten Klassen sind; Autovervollständigung, Linting, mypy und Ihre Intuition sollten alle einwandfrei mit Ihren validierten Daten funktionieren.
* Validierung von **komplexen Strukturen**:
    * Benutzung von hierarchischen Pydantic-Modellen, Python-`typing`s `List` und `Dict`, usw.
    * Die Validierer erlauben es, komplexe Datenschemas klar und einfach zu definieren, überprüft und dokumentiert als JSON Schema.
    * Sie können tief **verschachtelte JSON**-Objekte haben, die alle validiert und annotiert sind.
* **Erweiterbar**:
    * Pydantic erlaubt die Definition von eigenen Datentypen oder Sie können die Validierung mit Methoden in einem Modell erweitern, die mit dem Validator-Dekorator dekoriert sind.
* 100 % Testabdeckung.
