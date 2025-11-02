# LLM-Testdatei { #llm-test-file }

Dieses Dokument testet, ob das <abbr title="Large Language Model – Großes Sprachmodell">LLM</abbr>, das die Dokumentation übersetzt, den <abbr title="General Prompt – Allgemeiner Prompt">`general_prompt`</abbr> in `scripts/translate.py` und den sprachspezifischen Prompt in `docs/{language code}/llm-prompt.md` versteht. Der sprachspezifische Prompt wird an `general_prompt` angehängt.

Hier hinzugefügte Tests werden von allen Erstellern sprachspezifischer Prompts gesehen.

So verwenden:

* Einen sprachspezifischen Prompt haben – `docs/{language code}/llm-prompt.md`.
* Eine frische Übersetzung dieses Dokuments in die gewünschte Zielsprache durchführen (siehe z. B. das Kommando `translate-page` der `translate.py`). Dadurch wird die Übersetzung unter `docs/{language code}/docs/_llm-test.md` erstellt.
* Prüfen Sie, ob in der Übersetzung alles in Ordnung ist.
* Verbessern Sie bei Bedarf Ihren sprachsspezifischen Prompt, den allgemeinen Prompt oder das englische Dokument.
* Beheben Sie anschließend manuell die verbleibenden Probleme in der Übersetzung, sodass es eine gute Übersetzung ist.
* Übersetzen Sie erneut, nachdem die gute Übersetzung vorliegt. Das ideale Ergebnis wäre, dass das LLM an der Übersetzung keine Änderungen mehr vornimmt. Das bedeutet, dass der allgemeine Prompt und Ihr sprachsspezifischer Prompt so gut sind, wie sie sein können (Es wird manchmal ein paar scheinbar zufällige Änderungen machen, der Grund ist, dass <a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">LLMs keine deterministischen Algorithmen sind</a>).

Die Tests:

## Codeschnipsel { #code-snippets}

//// tab | Test

Dies ist ein Codeschnipsel: `foo`. Und dies ist ein weiteres Codeschnipsel: `bar`. Und noch eins: `baz quux`.

////

//// tab | Info

Der Inhalt von Codeschnipseln sollte unverändert bleiben.

Siehe Abschnitt `### Content of code snippets` im allgemeinen Prompt in `scripts/translate.py`.

////

## Anführungszeichen { #quotes }

//// tab | Test

Gestern schrieb mein Freund: „Wenn man unkorrekt korrekt schreibt, hat man es unkorrekt geschrieben“. Worauf ich antwortete: „Korrekt, aber ‚unkorrekt‘ ist unkorrekterweise nicht ‚„unkorrekt“‘“.

/// note | Hinweis

Das LLM wird dies wahrscheinlich falsch übersetzen. Interessant ist nur, ob es die korrigierte Übersetzung bei einer erneuten Übersetzung beibehält.

///

////

//// tab | Info

Der Promptdesigner kann entscheiden, ob neutrale Anführungszeichen in typografische Anführungszeichen umgewandelt werden sollen. Es ist in Ordnung, sie unverändert zu lassen.

Siehe zum Beispiel den Abschnitt `### Quotes` in `docs/de/llm-prompt.md`.

////

## Anführungszeichen in Codeschnipseln { #quotes-in-code-snippets}

//// tab | Test

`pip install "foo[bar]"`

Beispiele für Stringliterale in Codeschnipseln: `"this"`, `'that'`.

Ein schwieriges Beispiel für Stringliterale in Codeschnipseln: `f"I like {'oranges' if orange else "apples"}"`

Hardcore: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | Info

... Allerdings müssen Anführungszeichen in Codeschnipseln unverändert bleiben.

////

## Codeblöcke { #code-blocks }

//// tab | Test

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

////

//// tab | Info

Code in Codeblöcken sollte nicht verändert werden, mit Ausnahme von Kommentaren.

Siehe Abschnitt `### Content of code blocks` im allgemeinen Prompt in `scripts/translate.py`.

////

## Tabs und farbige Boxen { #tabs-and-colored-boxes }

//// tab | Test

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

//// tab | Info

Tabs und `Info`/`Note`/`Warning`/usw. Blöcke sollten die Übersetzung ihres Titels nach einem vertikalen Strich (`|`) erhalten.

Siehe die Abschnitte `### Special blocks` und `### Tab blocks` im allgemeinen Prompt in `scripts/translate.py`.

////

## Web- und interne Links { #web-and-internal-links }

//// tab | Test

Der Linktext sollte übersetzt werden, die Linkadresse sollte unverändert bleiben:

* [Link zur Überschrift oben](#code-snippets)
* [Interner Link](index.md#installation){.internal-link target=_blank}
* <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">Externer Link</a>
* <a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">Link zu einem Stil</a>
* <a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">Link zu einem Skript</a>
* <a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">Link zu einem Bild</a>

Der Linktext sollte übersetzt werden, die Linkadresse sollte auf die Übersetzung zeigen:

* <a href="https://fastapi.tiangolo.com/de/" class="external-link" target="_blank">FastAPI-Link</a>

////

//// tab | Info

Links sollten übersetzt werden, aber ihre Adresse soll unverändert bleiben. Eine Ausnahme sind absolute Links zu Seiten der FastAPI-Dokumentation. In diesem Fall sollte auf die Übersetzung verlinkt werden.

Siehe Abschnitt `### Links` im allgemeinen Prompt in `scripts/translate.py`.

////

## HTML „abbr“-Elemente { #html-abbr-elements }

//// tab | Test

Hier einige Dinge, die in HTML-„abbr“-Elemente gepackt sind (einige sind erfunden):

### Das abbr gibt eine vollständige Phrase { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done – Dinge erledigt bekommen">GTD</abbr>
* <abbr title="less than – kleiner als"><code>lt</code></abbr>
* <abbr title="XML Web Token">XWT</abbr>
* <abbr title="Paralleles Server-Gateway-Interface">PSGI</abbr>

### Das abbr gibt eine Erklärung { #the-abbr-gives-an-explanation }

* <abbr title="Eine Gruppe von Maschinen, die so konfiguriert sind, dass sie verbunden sind und in irgendeiner Weise zusammenarbeiten.">Cluster</abbr>
* <abbr title="Eine Methode des Machine Learning, die künstliche neuronale Netze mit zahlreichen versteckten Schichten zwischen Eingabe- und Ausgabeschicht verwendet und so eine umfassende interne Struktur entwickelt">Deep Learning</abbr>

### Das abbr gibt eine vollständige Phrase und eine Erklärung { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network – Mozilla-Entwicklernetzwerk: Dokumentation für Entwickler, geschrieben von den Firefox-Leuten">MDN</abbr>
* <abbr title="Input/Output – Eingabe/Ausgabe: Lesen oder Schreiben auf der Festplatte, Netzwerkkommunikation.">I/O</abbr>.

////

//// tab | Info

„title“-Attribute von „abbr“-Elementen werden nach bestimmten Anweisungen übersetzt.

Übersetzungen können eigene „abbr“-Elemente hinzufügen, die das LLM nicht entfernen soll. Z. B. um englische Wörter zu erklären.

Siehe Abschnitt `### HTML abbr elements` im allgemeinen Prompt in `scripts/translate.py`.

////

## Überschriften { #headings }

//// tab | Test

### Eine Webapp entwickeln – ein Tutorial { #develop-a-webapp-a-tutorial }

Hallo.

### Typhinweise und -annotationen { #type-hints-and-annotations }

Hallo wieder.

### Super- und Subklassen { #super-and-subclasses }

Hallo wieder.

////

//// tab | Info

Die einzige strenge Regel für Überschriften ist, dass das LLM den Hash-Teil in geschweiften Klammern unverändert lässt, damit Links nicht kaputtgehen.

Siehe Abschnitt `### Headings` im allgemeinen Prompt in `scripts/translate.py`.

Für einige sprachspezifische Anweisungen, siehe z. B. den Abschnitt `### Headings` in `docs/de/llm-prompt.md`.

////

## In der Dokumentation verwendete Begriffe { #terms-used-in-the-docs }

//// tab | Test

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
* Groß-/Klein­schrei­bung ist relevant
* Groß-/Klein­schrei­bung ist nicht relevant

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
* die Datenbanksession
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

////

//// tab | Info

Dies ist eine nicht vollständige und nicht normative Liste von (meist) technischen Begriffen, die in der Dokumentation vorkommen. Sie kann dem Promptdesigner helfen herauszufinden, bei welchen Begriffen das LLM Unterstützung braucht. Zum Beispiel, wenn es eine gute Übersetzung immer wieder auf eine suboptimale Übersetzung zurücksetzt. Oder wenn es Probleme hat, einen Begriff in Ihrer Sprache zu konjugieren/deklinieren.

Siehe z. B. den Abschnitt `### List of English terms and their preferred German translations` in `docs/de/llm-prompt.md`.

////
