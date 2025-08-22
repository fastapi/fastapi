Translate to German (Deutsch).

Language code: de.

Use the formal grammar (use "Sie" instead of "Du").


Translate quotation marks ("") in the English text with typographic quotation marks („“) in the German translation.

Example:

Source (English):

"word"

Result (German):

„Wort“

But don't do that when the quotation marks are themselves surrounded by backticks (`).

Example:

Source (English):

`"word"`

Result (German) – You don't translate the word, and you don't change the quotation marks:

`"word"`

Do not wrap words or sentences, which don't have any quotation marks in the English text, with normal quotation marks or with typographic quotation marks in the German translation.


In sentences, keep translations in brackets. DO NOT REMOVE THEM. Translations in brackets start with the exact text `(deutsch: `, speak, an opening bracket (`(`), followed by the text `deutsch`, followed by a colon (`:`), followed by a space (` `). And they end with a closing bracket (`)`) For example, keep `(deutsch: Anfragekörper)`, keep `(deutsch: Arbeiter)`, keep `(deutsch: Bereitstellen der Anwendung)`. Keep them even if they are not in the English text. Keep them, even if you think they are bad translations. The only exception to this rule is when you remove the whole sentence from the translation, because the whole sentence was removed in the English text. In that case also remove that translation in brackets. The reasoning for this rule is that these are one-time translations for English words which the human editor has added to the translation, in order to explain that word to the human readers of the translation. So these additions should be kept, even though they are not part of the English text.


In `abbr` HTML-elements, translate the content of the `title` attribute.

Example:

Source (English):

<abbr title="obsolete, recommended not to use it">deprecated</abbr>

Result (German):

<abbr title="veraltet, von der Verwendung wird abgeraten">deprecated</abbr>


Translate headings using the infinite form.

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


Follow these German instructions:

In der Regel versuche ich so weit wie möglich Worte zusammenzuschreiben, also ohne Bindestrich, es sei denn, es ist Konkretesding-Klassevondingen, etwa `Pydantic-Modell` (aber: `Datenbankmodell`), `Python-Modul` (aber: `Standardmodul`). Ich setze auch einen Bindestrich, wenn er die gleichen Buchstaben verbindet, etwa `Enum-Member`, `Cloud-Dienst`, `Template-Engine`. Oder wenn das Wort sonst einfach zu lang wird, etwa, `Performance-Optimierung`. Oder um etwas visuell besser zu dokumentieren, etwa `Pfadoperation-Dekorator`,  `Pfadoperation-Funktion`.

Ich versuche nicht, alles einzudeutschen. Das bezieht sich besonders auf Begriffe aus dem Bereich der Programmierung. Ich wandele zwar korrekt in Großschreibung um und setze Bindestriche, wo notwendig, aber ansonsten lasse ich solch ein Wort unverändert. Beispielsweise wird aus dem englischen Wort `string` in der deutschen Übersetzung `String`, aber nicht `Zeichenkette`. Oder aus dem englischen Wort `request body` wird in der deutschen Übersetzung `Requestbody`, aber nicht `Anfragekörper`. Oder aus dem englischen `response` wird im Deutschen `Response`, aber nicht `Antwort`.


Below is a list of English terms and their German translations, separated by a colon (`:`). Use these translations, do not use your own. Words inside brackets are explanations for you, they are not part of the term or the translation. If a list item starts with `NOT`, then that means: do NOT use this translation. Nouns, starting with the word `the`, have their German genus – `der`, `die`, `das` – included, to help you to grammatically decline them in the translation, and they are given in singular case unless they have `(plural case)` attached, which means they are given in plural case. Verbs are given in the full infinitive – starting with the word `to`.

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
* X is case-sensitive: Groß-/Klein­schrei­bung ist relevant in X
* X is case-insensitive: Groß-/Klein­schrei­bung ist nicht relevant in X
* you: Sie
* your: Ihr


Preserve indentation. Keep emoticons. Encode in utf-8. Use Linux line breaks (LF)
