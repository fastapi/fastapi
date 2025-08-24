1) Translate to German (Deutsch).

Language code: de.


2) Use the formal grammar (use `Sie` instead of `Du`).


3) Translate quotation marks ("") in the English source with typographic quotation marks („“).

Example:

Source (English):

"hello world"

Result (German):

„Hallo Welt“

However, when the quotation marks are inside code snippets or code blocks then do not change them. See the earlier defined rules about code snippets and code blocks.

Do not randomly add normal or typographic quotation marks into the German translation.


4) Translate HTML abbr elements as follows:

4.1) If the title attribute gives the full phrase for an abbrevation, then keep the phrase, append a long dash (`–`), followed by the translation of the phrase.

Examples:

Source (English):

<abbr title="Internet of Things">IoT</abbr>
<abbr title="Central Processing Unit">CPU</abbr>
<abbr title="too long; didn't read"><strong>TL;DR:</strong></abbr>

Result (German):

<abbr title="Internet of Things – Internet der Dinge">IoT</abbr>
<abbr title="Central Processing Unit – Zentrale Verarbeitungseinheit">CPU</abbr>
<abbr title="too long; didn't read – zu lang; hab's nicht gelesen"><strong>TL;DR:</strong></abbr>

Conversion scheme title attribute:

Source (English):

{full phrase}

Result (German):

{full phrase} – {translation of full phrase}

If the phrase can not be translated or it is the same in the translation, then keep the title attribute as is.

Examples:

Source (English):

<abbr title="JSON Web Tokens">JWT</abbr>
<abbr title="Enumeration">`Enum`</abbr>

Result (German):

<abbr title="JSON Web Tokens">JWT</abbr>
<abbr title="Enumeration">`Enum`</abbr>

Conversion scheme title attribute:

Source (English):

{full phrase}

Result (German):

{full phrase}

4.2) If the title attribute explains something in its own words, then translate it, if possible.

Examples:

Source (English):

<abbr title="also known as: endpoints, routes">path</abbr>
<abbr title="A program that checks for code errors">linter</abbr>
<abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>
<abbr title="before 2023-03">0.95.0</abbr>
<abbr title="2023-08-26">at the time of writing this</abbr>

Result (German):

<abbr title="auch bekannt als: Endpunkte, Routen">Pfad</abbr>
<abbr title="Programm das auf Fehler im Code prüft">Linter</abbr>
<abbr title="Konvertieren des Strings eines HTTP-Requests in Python-Daten">„Parsen“</abbr>
<abbr title="vor 2023-03">0.95.0</abbr>
<abbr title="2023-08-26">zum Zeitpunkt als das hier geschrieben wurde</abbr>

Conversion scheme title attribute:

Source (English):

{explanation}

Result (German):

{translation of explanation}

If the term, which the HTML abbr element wraps, stays English in the translation, but it also has a translation, whose knowledge improves the explanation, then let the title attribute be that translation, followed by a colon (`:`), followed by the translation of the title attribute.

Examples:

Source (English):

<abbr title="also known as components, resources, providers, services, injectables">Dependency Injection</abbr>

Result (German):

<abbr title="Einbringen von Abhängigkeiten: auch bekannt als Komponenten, Ressourcen, Provider, Services, Injectables">Dependency Injection</abbr>

Conversion scheme title attribute:

Source (English):

{explanation}

Result (German):

{translation of term which abbr wraps}: {translation of explanation}


4.3) If the title attribute gives the full phrase for an abbrevation, followed by a colon (`:`) or a comma (`,`), followed by an explanation, then keep the phrase, append a long dash (`–`), followed by the translation of the phrase, followed by a colon (`:`), followed by the translation of the explanation.

Examples:

Source (English):

<abbr title="Input/Output: disk reading or writing, network communication.">I/O</abbr>
<abbr title="Content Delivery Network: Service, that provides static files.">CDN</abbr>
<abbr title="Integrated Development Environment, similar to a code editor">IDE</abbr>
<abbr title="Object Relational Mapper, a fancy term for a library where some classes represent SQL tables and instances represent rows in those tables">"ORMs"</abbr>

Result (German):

<abbr title="Input/Output – Eingabe/Ausgabe: Lesen oder Schreiben auf der Festplatte, Netzwerkkommunikation.">I/O</abbr>
<abbr title="Content Delivery Network – Inhalte auslieferndes Netzwerk: Dienst, der statische Dateien bereitstellt.">CDN</abbr>
<abbr title="Integrated Development Environment – Integrierte Entwicklungsumgebung: Ähnlich einem Code-Editor">IDE</abbr>
<abbr title="Object Relational Mapper – Objektrelationaler Mapper: Ein Fachbegriff für eine Bibliothek, in der einige Klassen SQL-Tabellen und Instanzen Zeilen in diesen Tabellen darstellen">„ORMs“</abbr>

Conversion scheme title attribute:

Source (English):

{full phrase}: {explanation}

OR

Source (English):

{full phrase}, {explanation}

Result (German):

{full phrase} – {translation of full phrase}: {translation of explanation}

4.4) If there is an HTML abbr element in a sentence in an existing translation, but that element does not exist in the related sentence in the English text, then keep that HTML abbr element in the translation, do not change or remove it. Except when you remove the whole sentence from the translation, because the whole sentence was removed from the English text. The reasoning for this rule is, that such abbr elements are manually added by the human editor of the translation, in order to translate or explain an English word to the human readers of the translation. They would not make sense in the English text but they do make sense in the translation. So keep them in the translation, even though they are not part of the English text. This rule only applies to HTML abbr elements.


5) Translate headings using the infinite form.

Examples:

Source (English):

## Create a Project { #create-a-project }

Translate with (German):

## Ein Projekt erstellen { #create-a-project }

Do NOT translate with (German):

## Erstellen Sie ein Projekt { #create-a-project }

Source (English):

# Install Packages { #install-packages }

Translate with (German):

# Pakete installieren { #install-packages }

Do NOT translate with (German):

# Installieren Sie Pakete { #install-packages }

Source (English):

### Run Your Program { #run-your-program }

Translate with (German):

### Ihr Programm ausführen { #run-your-program }

Do NOT translate with (German):

### Führen Sie Ihr Programm aus { #run-your-program }


6) Follow these German instructions:

In der Regel versuche ich so weit wie möglich Worte zusammenzuschreiben, also ohne Bindestrich, es sei denn, es ist Konkretesding-Klassevondingen, etwa `Pydantic-Modell` (aber: `Datenbankmodell`), `Python-Modul` (aber: `Standardmodul`). Ich setze auch einen Bindestrich, wenn er die gleichen Buchstaben verbindet, etwa `Enum-Member`, `Cloud-Dienst`, `Template-Engine`. Oder wenn das Wort sonst einfach zu lang wird, etwa, `Performance-Optimierung`. Oder um etwas visuell besser zu dokumentieren, etwa `Pfadoperation-Dekorator`,  `Pfadoperation-Funktion`.

Ich versuche nicht, alles einzudeutschen. Das bezieht sich besonders auf Begriffe aus dem Bereich der Programmierung. Ich wandele zwar korrekt in Großschreibung um und setze Bindestriche, wo notwendig, aber ansonsten lasse ich solch ein Wort unverändert. Beispielsweise wird aus dem englischen Wort `string` in der deutschen Übersetzung `String`, aber nicht `Zeichenkette`. Oder aus dem englischen Wort `request body` wird in der deutschen Übersetzung `Requestbody`, aber nicht `Anfragekörper`. Oder aus dem englischen `response` wird im Deutschen `Response`, aber nicht `Antwort`.


7) Below is a list of English terms and their German translations, separated by a colon (`:`). Use these translations, do not use your own. Words inside brackets are explanations for you, they are not part of the term or the translation. If a list item starts with `NOT`, then that means: do NOT use this translation. Nouns, starting with the word `the`, have their German genus – `der`, `die`, `das` – included, to help you to grammatically decline them in the translation, and they are given in singular case unless they have `(plural case)` attached, which means they are given in plural case. Verbs are given in the full infinitive – starting with the word `to`.

* /// check: /// check | Testen
* /// danger: /// danger | Gefahr
* /// info: /// info | Info
* /// note | Technical Details: /// note | Technische Details
* /// note: /// note | Hinweis
* /// tip: /// tip | Tipp
* /// warning: /// warning | Achtung
* you: Sie
* your: Ihr
* e.g: z.B.
* etc.: usw.
* the `PATH` environment variable: die `PATH`-Umgebungsvariable
* the `PATH`: der `PATH`
* the `requirements.txt`: die `requirements.txt`
* the API Router: der API-Router
* the app: die App
* the application: die Anwendung
* the Advanced User Guide: das Handbuch für fortgeschrittene Benutzer
* the Authorization-Header: der Autorisierungsheader
* the background task: der Hintergrundtask
* the cloud provider: der Cloudanbieter
* the CLI: Das CLI
* the configurations (plural case): die Einstellungen
* the command line interface: Das Kommandozeileninterface
* the docs: die Dokumentation (use singular case)
* the default value: der Defaultwert
* NOT the default value: der Standardwert
* the default declaration: die Default-Deklaration
* the engine: die Engine
* the env var: die Umgebungsvariable
* the error response: die Error-Response
* the event: das Event
* the exception: die Exception
* the form model: das Formularmodell
* the form body: der Formularbody
* the header: der Header
* the headers (plural case): die Header
* the lifespan event: das Lifespan-Event
* the locking: das Locking
* the mobile application: die Mobile-Anwendung
* the model object: das Modellobjekt
* the mounting: das Mounten
* mounted: gemountet
* the origin: das Origin
* the override: Die Überschreibung
* the parameter: der Parameter
* the parameters (plural case): die Parameter
* the function parameter: der Funktionsparameter
* the default parameter: der Defaultparameter
* the body parameter: der Body-Parameter
* the request body parameter: der Requestbody-Parameter
* the path parameter: der Pfad-Parameter
* the query parameter: der Query-Parameter
* the cookie parameter: der Cookie-Parameter
* the header parameter: der Header-Parameter
* the form parameter: der Formular-Parameter
* the payload: die Payload
* the query: die Query
* the recap: die Zusammenfassung
* the request: der Request
* the response: die Response
* the return type: der Rückgabetyp
* the return value: der Rückgabewert
* the SQLModel docs: die SQLModel-Dokumentation
* the SDK: das SDK
* the tag: der Tag
* the Tutorial - User guide: das Tutorial – Benutzerhandbuch
* the type annotation: die Typannotation
* the type hint: der Typhinweis
* the wildcard: die Wildcard
* the worker class: die Workerklasse
* NOT the worker class: die Arbeiterklasse
* the worker process: der Workerprozess
* NOT the worker process: der Arbeiterprozess
* to commit: committen
* to modify: ändern
* to serve (an application): bereitstellen
* to serve (a response): ausliefern
* NOT to serve: bedienen
* to upgrade: aktualisieren
* to wrap: wrappen
* `foo` as a `type`: `foo` vom Typ `type`
* `foo` as a `type`: `foo`, ein `type`
* FastAPI's X: FastAPIs X
* Starlette's Y: Starlettes Y
* X is case-sensitive: Groß-/Klein­schrei­bung ist relevant in X
* X is case-insensitive: Groß-/Klein­schrei­bung ist nicht relevant in X


8) Preserve indentation. Keep emoticons. Encode in utf-8. Use Linux line breaks (LF)
