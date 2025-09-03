# LLM-Test { #llm-test }

Dieses Dokument testet, ob das <abbr title="Large Language Model – Großes Sprachmodell">LLM</abbr> die Anweisungen im allgemeinen Prompt in `scripts/translate.py` und diejenigen im sprachspezifischen Prompt `docs/{language code}/llm-prompt.md` versteht (die an die Anweisungen im allgemeinen Prompt angehängt werden).

Wie folgt verwenden:

* Eine frische Übersetzung dieses Dokuments in die gewünschte Zielsprache erstellen.
* Prüfen, ob alles größtenteils in Ordnung ist.
* Wenn manches nicht in Ordnung ist, sich aber durch Verbesserungen am englischen Dokument oder am allgemeinen Prompt oder am sprachspezifischen Prompt beheben lässt, das tun.
* Dann die verbleibenden Probleme in der Übersetzung manuell beheben, sodass es eine gute Übersetzung ist.
* Erneut übersetzen, wobei die existierende, gute Übersetzung verwendet wird. Das ideale Ergebnis wäre, dass das LLM gar keine Änderungen vornimmt. Das würde bedeuten, dass der allgemeine Prompt und der Sprach-Prompt so gut wie möglich sind. (Plot Twist: Es wird normalerweise ein paar scheinbar zufällige Änderungen machen, der Grund ist vermutlich, dass <a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">LLMs keine deterministischen Algorithmen sind</a>).

Die Idee ist, dass Sie, wenn Sie an einer Übersetzung für eine Sprache arbeiten (unter der Annahme, dass Sie `scripts/translate.py` ausführen können), hier Beispiele gefundener Sonderfälle aufnehmen (keine detaillierte Liste, nur Beispiele für solche Sonderfälle) und mit diesem Dokument testen, statt jedes andere einzelne Dokument mehrfach zu testen und zu übersetzen, was pro Übersetzung ein paar Cent kostet. Außerdem werden durch das Hinzufügen solcher Sonderfälle hier auch andere Übersetzungsprojekte auf solche Sonderfälle aufmerksam.

## Codeschnipsel { #code-snippets}

Dies ist ein Codeschnipsel: `foo`. Und dies ist ein weiteres Codeschnipsel: `bar`. Und noch eins: `baz quux`.

## Anführungszeichen { #quotes }

Gestern schrieb mein Freund: „Wenn man falsch richtig buchstabiert, hat man es falsch buchstabiert“. Worauf ich antwortete: „Richtig, aber ‚falsch‘ ist fälschlich nicht ‚„falsch“‘“.

## Anführungszeichen in Codeschnipseln { #quotes-in-code-snippets}

`pip install "foo[bar]"`

Beispiele für Stringliterale in Codeschnipseln: `"this"`, `'that'`.

Ein schwieriges Beispiel für Stringliterale in Codeschnipseln: `f"I like {'oranges' if orange else "apples"}"`

Hardcore: `Yesterday my friend wrote: "If you spell incorrectly correctly you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'!"`

## Codeblöcke { #code-blocks }

Ein Bash-Codebeispiel ...

```bash
# Gruß an das Universum ausgeben
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
// Erstellen Sie ein Verzeichnis "Code"
$ mkdir code
// Wechseln Sie in dieses Verzeichnis
$ cd code
```

... und ein Python-Codebeispiel ...

```Python
wont_work()  # Das wird nicht funktionieren 😱
works(foo="bar")  # Das funktioniert 🎉
```

... und das war’s.

## Tabs und farbige Kästen { #tabs-and-colored-boxes }

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

## Web- und interne Links { #web-and-internal-links }

[Link zur Überschrift oben](#code-snippets)

<a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">Externer Link</a>

<a href="https://fastapi.tiangolo.com/de/the/link/#target" class="external-link" target="_blank">FastAPI-Link</a>

<a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">Link zu einem Stil</a>
<a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">Link zu einem Skript</a>
<a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">Link zu einem Bild</a>

[Interner Link](foo.md#bar){.internal-link target=_blank}

## HTML-„abbr“-Elemente { #html-abbr-elements }

Hier einige Dinge, die in HTML-„abbr“-Elemente gewrappt sind (einige sind erfunden):

### Ganze Phrase { #full-phrase }

* <abbr title="Getting Things Done – Dinge erledigt bekommen">GTD</abbr>
* <abbr title="less than – kleiner als"><code>lt</code></abbr>
* <abbr title="XML-Web-Token">XWT</abbr>
* <abbr title="Paralleles Server-Gateway-Interface">PSGI</abbr>

### Erklärung { #explanation }

* <abbr title="Eine Gruppe von Maschinen, die so konfiguriert sind, dass sie verbunden sind und in irgendeiner Weise zusammenarbeiten.">Cluster</abbr>
* <abbr title="Eine Methode des maschinellen Lernens, die künstliche neuronale Netze mit zahlreichen verdeckten Schichten zwischen Eingabe- und Ausgabeschichten verwendet und dabei eine umfassende interne Struktur entwickelt">Deep Learning</abbr>

### Ganze Phrase: Erklärung { #full-phrase-explanation }

* <abbr title="Mozilla Developer Network – Mozilla-Entwicklernetzwerk: Dokumentation für Entwickler, geschrieben von den Firefox-Leuten">MDN</abbr>
* <abbr title="Input/Output – Eingabe/Ausgabe: Lesen oder Schreiben auf der Festplatte, Netzwerkkommunikation.">I/O</abbr>.

## Überschriften { #headings }

### Eine Webapp entwickeln – ein Tutorial { #develop-a-webapp-a-tutorial }

Hallo.

### Typhinweise und -annotationen { #type-hints-and-annotations }

Hallo nochmal.

### Super- und Subklassen { #super-and-subclasses }

Hallo nochmal.

## Sätze mit bevorzugten Übersetzungen, (vielleicht) im Sprach-Prompt definiert { #sentences-with-preferred-translations-maybe-defined-in-the-language-prompt }

Ich heiße Sie willkommen.
Ich bewundere Ihren Pullover.
Sie mag Obst, z. B. Äpfel
Er mag Orangen, Bananen, usw.
Lesen Sie die Dokumentation.
Lesen Sie das Tutorial – Benutzerhandbuch.
Lesen Sie dann das Handbuch für fortgeschrittene Benutzer.
Wenn die Umgebungsvariable existiert, tun Sie etwas.
Lesen Sie die `PATH`-Umgebungsvariable.
Was dasselbe ist wie der `PATH`.
Installieren Sie aus der `requirements.txt`.
Verwenden Sie den API-Router.
Starten Sie die App.
Erstellen Sie die Anwendung.
Dies ist der Autorisierungsheader.
Dies ist der `Authorization`-Header.
Warten auf den Hintergrundtask.
Den Button drücken.
Probieren Sie diesen Cloudanbieter.
Verwenden Sie das CLI.
Was das Kommandozeileninterface ist.
Der Defaultwert ist „foo“.
Die Default-Deklaration ist „bar“.
Dictionaries, oder Dicts, sind nützliche Datenstrukturen.
Enumerationen, oder Enums, haben ebenfalls ihre Verwendung.
Die Engine wird das tun.
Eine Error-Response zurückgeben.
Auf das Event warten.
Die Exception auslösen.
Der Exceptionhandler behandelt sie.
Das Formularmodell definieren.
Den Formularbody senden.
Auf den Header zugreifen.
Die Header ändern.
Schreibweise in Headern.
Die Forwarded-Header werden häufig in Verbindung mit Proxys verwendet.
Auf das Lifespan-Event lauschen.
Locking bedeutet, dass wir ein Lock setzen, um etwas sicher zu ändern.
Eine Mobile-Anwendung entwickeln.
Das Modellobjekt definieren.
Etwas wartet auf das Mounten.
Es ist jetzt gemountet.
Ein weiteres Origin.
Dafür haben wir eine Überschreibung.
Die Funktion hat einen Parameter.
Der Funktionsparameter ist ein int.
Die Funktion hat viele Parameter.
Der Defaultparameter ist ein bool.
Der Body-Parameter enthält den Body des Requests.
Auch der Requestbody-Parameter genannt.
Der Pfad-Parameter enthält eine Variable im Requestpfad.
Der Query-Parameter enthält die Query-Parameter im Requestpfad.
Der Cookie-Parameter enthält die Request-Cookies.
Der Header-Parameter enthält die Request-Header.
Der Formular-Parameter enthält die Formularfelder des Requests.
Die Payload ist der Request/die Response ohne Metadaten.
Diese Query fragt nach Items, die älter als eine Woche sind.
Zusammenfassung: Es ist smooth.
Der Request wurde empfangen.
Den Requestbody empfangen.
Die Requestbodys empfangen.
Die Response zurückgeben.
Was eine Funktion zurückgibt, hat einen Rückgabewert.
Und einen Rückgabetyp.
Wir lauschen auf die Startup- und Shutdown-Events.
Wir warten auf das Hochfahren des Servers.
Details sind in der SQLModel-Dokumentation beschrieben.
Verwenden Sie das SDK.
Der Tag `Horst` bedeutet, Horst muss es tun.
Dieser Parameter hat eine Typannotation.
Was ein Typhinweis ist.
Die Wildcard ist `*`.
Die Workerklasse macht dies und das.
Der Workerprozess macht auch Dinge.
Ich werde das morgen committen.
Gestern habe ich den Code geändert.
Lassen Sie uns unsere App bereitstellen.
Lassen Sie uns diese Seite ausliefern.
Aktualisieren Sie FastAPI, bevor Sie das tun.
Dies ist in ein HTML-Tag gewrappt.
`foo` vom Typ `int`.
`bar` vom Typ `str`.
`baz` vom Typ `list`.
FastAPIs Dokumentation.
Starlettes Performanz.
Groß-/Klein­schrei­bung ist relevant in `foo`.
Groß-/Klein­schrei­bung ist nicht relevant in „Bar“.
Standard-Python-Klassen.
Dies ist deprecatet.
