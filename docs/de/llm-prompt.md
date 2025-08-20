Translate to German (Deutsch).

Language code: de.

Use the formal grammar (use "Sie" instead of "Du").

Translate quotation marks ("") in the English text with typographic quotation marks („“) in the German translation. For example, translate "word" with „Wort“. But don't do that when the quotation marks are inside backticks (`). For example, keep `"word"` as is, because it is surrounded by backticks, do not translate it to `„Wort“`. Do not wrap words or sentences, which don't have any quotation marks in the English text, with normal quotation marks or with typographic quotation marks in the German translation.

If a word in an existing translation has an explanation in brackets after it, of the form "(deutsch: foo)" or "(englisch: bar)", then keep that explanation, even if it is not in the english text. It was manually added by the reviewer of the translation, to explain the meaning of a word to the reader of the translation. For example, if the English text is: "This is an origin" and the translation is "Das ist ein Origin (deutsch: Ursprung)" then the " (deutsch: Ursprung)" explains the meaning of the word "Origin" to the reader and you should therefore keep this part. This rule only applies when the part in brackets starts with "deutsch:" or with "englisch:" For example if the English text is "Hello World!" and the translation is "Hallo Welt (schon wieder)", then remove the " (schon wieder)" and translate with "Hallo Welt" instead of "Hallo Welt (schon wieder)", because the part in brackets does not start with "deutsch:" and not with "englisch:".

If a word or text snippet in the English text is wrapped in an `abbr` HTML-element, translate the text inside its `title` attribute. For example, translate `Hello <abbr title="World">Universe</abbr>` with `Hallo <abbr title="Welt">Universum</abbr>`, translate `The files are served from a <abbr title="Content Delivery Network: A service that provides static files">CDN</abbr>` with `Die Dateien werden von einem <abbr title="Content Delivery Network: Ein Dienst, der statische Dateien bereitstellt">CDN</abbr> bereitgestellt`.

If possible, translate headings using the infinite form. For example, translate `## Create a Project { #create-a-project }` with `## Ein Projekt erstellen { #create-a-project }`, not with `## Erstellen Sie ein Projekt { #create-a-project }`. Translate `# Install Packages { #install-packages }` with `# Pakete installieren { #install-packages }`, not with `# Installieren Sie Pakete { #install-packages }`. Translate `### Run Your Program { #run-your-program }` with `### Ihr Programm ausführen { #run-your-program }`, not with `### Führen Sie Ihr Programm aus { #run-your-program }`.

Preserve indentation. Do not translate link targets. Keep emoticons. Encode in utf-8. Use Linux linebreaks (LF)

---

Follow these instructions (they are in German):

In der Regel versuche ich so weit wie möglich Worte zusammenzuschreiben, also ohne Bindestrich, es sei denn, es ist Konkretesding-Klassevondingen, etwa `Pydantic-Modell` (aber: `Datenbankmodell`), `Python-Modul` (aber: `Standardmodul`). Ich setze auch einen Bindestrich, wenn er die gleichen Buchstaben verbindet, etwa `Enum-Member`, `Cloud-Dienst`, `Template-Engine`. Oder wenn das Wort sonst einfach zu lang wird, etwa, `Performance-Optimierung`. Oder um etwas visuell besser zu dokumentieren, etwa `Pfadoperation-Dekorator`,  `Pfadoperation-Funktion`.

Ich versuche nicht, alles einzudeutschen. Das bezieht sich besonders auf Begriffe aus dem Bereich der Programmierung. Ich wandele zwar korrekt in Großschreibung um und setze Bindestriche, wo notwendig, aber ansonsten lasse ich solch ein Wort unverändert. Beispielsweise wird aus dem englischen Wort `string` in der deutschen Übersetzung `String`, aber nicht `Zeichenkette`. Oder aus dem englischen Wort `request body` wird in der deutschen Übersetzung `Requestbody`, aber nicht `Anfragekörper`. Oder aus dem englischen `response` wird im Deutschen `Response`, aber nicht `Antwort`.

---

Below is a list of English terms and their German translations (separated by `: `). Use these translations, do not use your own. words inside brackets are explanations and not part of the term or the translation. If a list item starts with "NOT", that means: do NOT use this translation.

* /// check: /// check | Testen
* /// danger: /// danger | Gefahr
* /// info: /// info | Info
* /// note | Technical Details: /// note | Technische Details
* /// note: /// note | Hinweis
* /// tip: /// tip | Tipp
* /// warning: /// warning | Achtung
* `foo` as a `type`: `foo` vom Typ `type`
* `foo` as a `type`: `foo`, ein `type`
* e.g: z.B.
* etc.: usw.
* the `PATH` environment variable: die `PATH`-Umgebungsvariable
* the `PATH`: der `PATH`
* the `requirements.txt`: die `requirements.txt`
* the app: die App
* the application: die Anwendung
* the Advanced User Guide: das Handbuch für fortgeschrittene Benutzer
* the Authorization-Header: der Autorisierungsheader
* the background task: der Hintergrundtask
* the cloud provider: der Cloudanbieter
* the CLI: Das CLI
* the command line interface: Das Kommandozeileninterface
* the docs: die Dokumentation (use singular case)
* the default value: der Defaultwert
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
* the origin: das Origin
* the override: Die Überschreibung
* the payload: die Payload
* the recap: die Zusammenfassung
* the request: der Request
* the response: die Response
* the return type: der Rückgabetyp
* the return value: der Rückgabewert
* the SQLModel docs: die SQLModel-Dokumentation
* the SDK: das SDK
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
* you: Sie
* your: Ihr
