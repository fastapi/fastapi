# LLM-Testdatei { #llm-test-file }

Dieses Dokument testet, ob das <abbr title="Large Language Model – Großes Sprachmodell">LLM</abbr> die Anweisungen aus dem allgemeinen Prompt in `scripts/translate.py` und diejenigen im sprachspezifischen Prompt `docs/{language code}/llm-prompt.md` versteht (die an die Anweisungen im allgemeinen Prompt angehängt werden). Durch das Hinzufügen von Spezialfällen hier werden Übersetzungsprojekte leichter darauf aufmerksam.

So verwenden:

* Führen Sie eine frische Übersetzung dieses Dokuments in die gewünschte Zielsprache durch.
* Prüfen Sie, ob die Dinge größtenteils in Ordnung sind.
* Wenn einige Dinge nicht in Ordnung sind, sich aber durch Verbesserungen am englischen Dokument oder am allgemeinen bzw. sprachsspezifischen Prompt beheben lassen, tun Sie das.
* Beheben Sie anschließend manuell die verbleibenden Probleme in der Übersetzung, sodass es eine gute Übersetzung ist.
* Übersetzen Sie erneut unter Verwendung der bestehenden, guten Übersetzung. Das ideale Ergebnis wäre, dass das LLM überhaupt keine Änderungen vornimmt. Das würde bedeuten, dass der allgemeine Prompt und der Sprach-Prompt so gut sind, wie sie sein können (es wird manchmal ein paar scheinbar zufällige Änderungen machen, der Grund ist, dass <a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">LLMs keine deterministischen Algorithmen sind</a>).


## Codeschnipsel { #code-snippets}

Dies ist ein Codeschnipsel: `foo`. Und dies ist ein weiteres Codeschnipsel: `bar`. Und noch eins: `baz quux`.


## Anführungszeichen { #quotes }

Gestern schrieb mein Freund: „Wenn man unkorrekt korrekt schreibt, hat man es unkorrekt geschrieben“. Worauf ich antwortete: „Korrekt, aber ‚unkorrekt‘ ist unkorrekterweise nicht ‚„unkorrekt“‘“.


## Anführungszeichen in Codeschnipseln { #quotes-in-code-snippets}

`pip install "foo[bar]"`

Beispiele für Stringliterale in Codeschnipseln: `"this"`, `'that'`.

Ein schwieriges Beispiel für Stringliterale in Code-Snippets: `f"I like {'oranges' if orange else "apples"}"`

Hardcore: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`


## Codeblöcke { #code-blocks }

Ein Bash-Codebeispiel ...

```bash
# Eine Begrüßung an das Universum ausgeben
echo "Hello universe"
```

... und ein Konsolen-Codebeispiel ...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

... und noch ein Konsolen-Codebeispiel ...

```console
// Ein Verzeichnis „Code“ erstellen
$ mkdir code
// In dieses Verzeichnis wechseln
$ cd code
```

... und ein Python-Codebeispiel ...

```Python
wont_work()  # Das wird nicht funktionieren 😱
works(foo="bar")  # Das funktioniert 🎉
```

... und das war's.


## Tabs und farbige Boxen { #tabs-and-colored-boxes }

//// tab | Dies ist ein Tab

/// info | Info
Etwas Text
///

/// note | Hinweis
Etwas Text
///

/// note | Technische Details
Etwas Text
///

/// check | Testen
Etwas Text
///

/// tip | Tipp
Etwas Text
///

/// warning | Achtung
Etwas Text
///

/// danger | Gefahr
Etwas Text
///

////

//// tab | Hier ein weiterer Tab

Hallo

////


## Web- und interne Links { #web-and-internal-links }

Der Linktext sollte übersetzt werden, das Linkziel sollte unverändert bleiben:

* [Link zur Überschrift oben](#code-snippets)
* [Interner Link](foo.md#bar){.internal-link target=_blank}
* <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">Externer Link</a>
* <a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">Link zu einem Stil</a>
* <a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">Link zu einem Skript</a>
* <a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">Link zu einem Bild</a>

Der Linktext sollte übersetzt werden, das Linkziel sollte die Übersetzung sein, nicht der englische Text:

* <a href="https://fastapi.tiangolo.com/de/" class="external-link" target="_blank">FastAPI-Link</a>


## HTML „abbr“-Elemente { #html-abbr-elements }

Hier einige Dinge, die in HTML-„abbr“-Elemente gepackt sind (einige sind erfunden):

### Vollständige Phrase { #full-phrase }

* <abbr title="Getting Things Done – Dinge erledigt bekommen">GTD</abbr>
* <abbr title="less than – kleiner als"><code>lt</code></abbr>
* <abbr title="XML Web Token">XWT</abbr>
* <abbr title="Paralleles Server-Gateway-Interface">PSGI</abbr>

### Erklärung { #explanation }

* <abbr title="Eine Gruppe von Maschinen, die so konfiguriert sind, dass sie verbunden sind und in irgendeiner Weise zusammenarbeiten.">Cluster</abbr>
* <abbr title="Eine Methode des Machine Learning, die künstliche neuronale Netze mit zahlreichen versteckten Schichten zwischen Eingabe- und Ausgabeschicht verwendet und so eine umfassende interne Struktur entwickelt">Deep Learning</abbr>

### Vollständige Phrase: Erklärung { #full-phrase-explanation }

* <abbr title="Mozilla Developer Network – Mozilla-Entwicklernetzwerk: Dokumentation für Entwickler, geschrieben von den Firefox-Leuten">MDN</abbr>
* <abbr title="Input/Output – Eingabe/Ausgabe: Lesen oder Schreiben auf der Festplatte, Netzwerkkommunikation.">I/O</abbr>.


## Überschriften { #headings }

### Eine Webapp entwickeln – ein Tutorial { #develop-a-webapp-a-tutorial }

Hallo.

### Typhinweise und -annotationen { #type-hints-and-annotations }

Hallo wieder.

### Super- und Subklassen { #super-and-subclasses }

Hallo wieder.


## In der Dokumentation verwendete Begriffe { #terms-used-in-the-docs }

* Sie
* Ihr

* z. B.
* usw.

* `foo` vom Typ `int`
* `bar` vom Typ `str`
* `baz` vom Typ `list`

* das Tutorial – Benutzerhandbuch
* das Handbuch für fortgeschrittene Benutzer
* die SQLModel-Dokumentation
* die API-Dokumentation
* die automatische Dokumentation

* Data Science
* Deep Learning
* Machine Learning
* Dependency Injection
* HTTP Basic-Authentifizierung
* HTTP Digest
* ISO-Format
* der JSON-Schema-Standard
* das JSON-Schema
* die Schema-Definition
* Password Flow
* Mobile

* deprecatet
* designt
* ungültig
* on the fly
* Standard
* Default
* case-sensitive
* case-insensitive

* die Anwendung bereitstellen
* die Seite ausliefern

* die App
* die Anwendung

* der Request
* die Response
* die Error-Response

* die Pfadoperation
* der Pfadoperation-Dekorator
* die Pfadoperation-Funktion

* der Body
* der Requestbody
* der Responsebody
* der JSON-Body
* der Formularbody
* der Dateibody
* der Funktionskörper

* der Parameter
* der Body-Parameter
* der Pfad-Parameter
* der Query-Parameter
* der Cookie-Parameter
* der Header-Parameter
* der Formular-Parameter
* der Funktionsparameter

* das Event
* das Startup-Event
* das Hochfahren des Servers
* das Shutdown-Event
* das Lifespan-Event

* der Handler
* der Eventhandler
* der Exceptionhandler
* handhaben

* das Modell
* das Pydantic-Modell
* das Datenmodell
* das Datenbankmodell
* das Formularmodell
* das Modellobjekt

* die Klasse
* die Basisklasse
* die Elternklasse
* die Subklasse
* die Kindklasse
* die Geschwisterklasse
* die Klassenmethode

* der Header
* die Header
* der Autorisierungsheader
* der `Authorization`-Header
* der Forwarded-Header

* das Dependency-Injection-System
* die Dependency
* das Dependable
* der Dependant

* I/O-lastig
* CPU-lastig
* Nebenläufigkeit
* Parallelität
* Multiprocessing

* die Umgebungsvariable
* die Umgebungsvariable
* der `PATH`
* die `PATH`-Umgebungsvariable

* die Authentifizierung
* der Authentifizierungsanbieter
* die Autorisierung
* das Anmeldeformular
* der Autorisierungsanbieter
* der Benutzer authentisiert sich
* das System authentifiziert den Benutzer

* Das CLI
* Das Kommandozeileninterface

* der Server
* der Client

* der Cloudanbieter
* der Clouddienst

* die Entwicklung
* die Entwicklungsphasen

* das Dict
* das Dictionary
* die Enumeration
* das Enum
* das Enum-Member

* der Encoder
* der Decoder
* kodieren
* dekodieren

* die Exception
* werfen

* der Ausdruck
* die Anweisung

* das Frontend
* das Backend

* die GitHub-Diskussion
* das GitHub-Issue

* die Leistung
* die Leistungsoptimierung

* der Rückgabetyp
* der Rückgabewert

* die Sicherheit
* das Sicherheitsschema

* der Task
* der Hintergrundtask
* die Taskfunktion

* das Template
* die Template-Engine

* die Typannotation
* der Typhinweis

* der Serverworker
* der Uvicorn-Worker
* der Gunicorn-Worker
* der Workerprozess
* die Workerklasse
* die Workload

* das Deployment
* bereitstellen

* das SDK
* das Software Development Kit

* der `APIRouter`
* die `requirements.txt`
* das Bearer-Token
* der Breaking Change
* der Bug
* der Button
* das Callable
* der Code
* der Commit
* der Contextmanager
* die Coroutine
* die Datenbank-Session
* die Festplatte
* die Domain
* die Engine
* das Fake-X
* die HTTP-GET-Methode
* das Item
* die Bibliothek
* der Lifespan
* der Lock
* die Middleware
* die Mobile-Anwendung
* das Modul
* das Mounten
* das Netzwerk
* das Origin
* Die Überschreibung
* die Payload
* der Prozessor
* die Property
* der Proxy
* der Pull Request
* die Query
* der RAM
* der entfernte Rechner
* der Statuscode
* der String
* der Tag
* das Webframework
* die Wildcard
* zurückgeben
* validieren
