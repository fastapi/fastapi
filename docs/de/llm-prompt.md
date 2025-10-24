### Target language

Translate to German (Deutsch).

Language code: de.


### Definitions

"hyphen"
    The character «-»
    Unicode U+002D (HYPHEN-MINUS)
    Alternative names: hyphen, dash, minus sign

"dash"
    The character «–»
    Unicode U+2013 (EN DASH)
    German name: Halbgeviertstrich


### Grammar to use when talking to the reader

Use the formal grammar (use «Sie» instead of «Du»).


### Quotes

1) Convert neutral double quotes («"») and English double typographic quotes («“» and «”») to German double typographic quotes («„» and «“»). Convert neutral single quotes («'») and English single typographic quotes («‘» and «’») to German single typographic quotes («‚» and «‘»). Do NOT convert «`"» to «„», do NOT convert «"`» to «“».

Examples:

    Source (English):

        «««
        "Hello world"
        “Hello Universe”
        "He said: 'Hello'"
        “my name is ‘Nils’”
        `"__main__"`
        `"items"`
        »»»

    Result (German):

        «««
        „Hallo Welt“
        „Hallo Universum“
        „Er sagte: ‚Hallo‘“
        „Mein Name ist ‚Nils‘“
        `"__main__"`
        `"items"`
        »»»


### Ellipsis

1) Make sure there is a space between an ellipsis and a word following or preceding the ellipsis.

Examples:

    Source (English):

        «««
        ...as we intended.
        ...this would work:
        ...etc.
        others...
        More to come...
        »»»

    Result (German):

        «««
        ... wie wir es beabsichtigt hatten.
        ... das würde funktionieren:
        ... usw.
        Andere ...
        Später mehr ...
        »»»

2) This does not apply in URLs, code blocks, and code snippets. Do not remove or add spaces there.


### Headings

1) Translate headings using the infinite form.

Examples:

    Source (English):

        «««
        ## Create a Project { #create-a-project }
        »»»

    Translate with (German):

        «««
        ## Ein Projekt erstellen { #create-a-project }
        »»»

    Do NOT translate with (German):

        «««
        ## Erstellen Sie ein Projekt { #create-a-project }
        »»»

    Source (English):

        «««
        # Install Packages { #install-packages }
        »»»

    Translate with (German):

        «««
        # Pakete installieren { #install-packages }
        »»»

    Do NOT translate with (German):

        «««
        # Installieren Sie Pakete { #install-packages }
        »»»

    Source (English):

        «««
        ### Run Your Program { #run-your-program }
        »»»

    Translate with (German):

        «««
        ### Ihr Programm ausführen { #run-your-program }
        »»»

    Do NOT translate with (German):

        «««
        ### Führen Sie Ihr Programm aus { #run-your-program }
        »»»

2) Make sure that the translated part of the heading does not end with a period.

Example:

    Source (English):

        «««
        ## Another module with `APIRouter` { #another-module-with-apirouter }
        »»»

    Translate with (German):

        «««
        ## Ein weiteres Modul mit `APIRouter` { #another-module-with-apirouter }
        »»»

    Do NOT translate with (German) – notice the added period:

        «««
        ## Ein weiteres Modul mit `APIRouter`. { #another-module-with-apirouter }
        »»»

3) Replace occurrences of literal « - » (a space followed by a hyphen followed by a space) with « – » (a space followed by a dash followed by a space) in the translated part of the heading.

Example:

    Source (English):

        «««
        # FastAPI in Containers - Docker { #fastapi-in-containers-docker }
        »»»

    Translate with (German) – notice the dash:

        «««
        # FastAPI in Containern – Docker { #fastapi-in-containers-docker }
        »»»

    Do NOT translate with (German) – notice the hyphen:

        «««
        # FastAPI in Containern - Docker { #fastapi-in-containers-docker }
        »»»

3.1) Do not apply rule 3 when there is no space before or no space after the hyphen.

Example:

    Source (English):

        «««
        ## Type hints and annotations { #type-hints-and-annotations }
        »»»

    Translate with (German) – notice the hyphen:

        «««
        ## Typhinweise und -annotationen { #type-hints-and-annotations }
        »»»

    Do NOT translate with (German) – notice the dash:

        «««
        ## Typhinweise und –annotationen { #type-hints-and-annotations }
        »»»

3.2) Do not apply rule 3 to the untranslated part of the heading inside curly brackets, which you shall not translate.


### German instructions, when to use and when not to use hyphens in words (written in first person, which is you)

In der Regel versuche ich so weit wie möglich Worte zusammenzuschreiben, also ohne Bindestrich, es sei denn, es ist Konkretesding-Klassevondingen, etwa «Pydantic-Modell» (aber: «Datenbankmodell»), «Python-Modul» (aber: «Standardmodul»). Ich setze auch einen Bindestrich, wenn er die gleichen Buchstaben verbindet, etwa «Enum-Member», «Cloud-Dienst», «Template-Engine». Oder wenn das Wort sonst einfach zu lang wird, etwa, «Performance-Optimierung». Oder um etwas visuell besser zu dokumentieren, etwa «Pfadoperation-Dekorator»,  «Pfadoperation-Funktion».


### German instructions about difficult to translate technical terms (written in first person, which is you)

Ich versuche nicht, alles einzudeutschen. Das bezieht sich besonders auf Begriffe aus dem Bereich der Programmierung. Ich wandele zwar korrekt in Großschreibung um und setze Bindestriche, wo notwendig, aber ansonsten lasse ich solch ein Wort unverändert. Beispielsweise wird aus dem englischen Wort «string» in der deutschen Übersetzung «String», aber nicht «Zeichenkette». Oder aus dem englischen Wort «request body» wird in der deutschen Übersetzung «Requestbody», aber nicht «Anfragekörper». Oder aus dem englischen «response» wird im Deutschen «Response», aber nicht «Antwort».


### List of English terms and their preferred German translations

Below is a list of English terms and their preferred German translations, separated by a colon («:»). Use these translations, do not use your own. If an existing translation does not use these terms, update it to use them. In the below list, a term or a translation may be followed by an explanation in brackets, which explains when to translate the term this way. If a translation is preceded by «NOT», then that means: do NOT use this translation for this term. English nouns, starting with the word «the», have the German genus – «der», «die», «das» – prepended to their German translation, to help you to grammatically decline them in the translation. They are given in singular case, unless they have «(plural)» attached, which means they are given in plural case. Verbs are given in the full infinitive – starting with the word «to».

* «/// check»: «/// check | Testen»
* «/// danger»: «/// danger | Gefahr»
* «/// info»: «/// info | Info»
* «/// note | Technical Details»: «/// note | Technische Details»
* «/// note»: «/// note | Hinweis»
* «/// tip»: «/// tip | Tipp»
* «/// warning»: «/// warning | Achtung»
* «you»: «Sie»
* «your»: «Ihr»
* «e.g»: «z. B.»
* «etc.»: «usw.»
* «ref»: «Ref.»
* «the Tutorial - User guide»: «das Tutorial – Benutzerhandbuch»
* «the Advanced User Guide»: «das Handbuch für fortgeschrittene Benutzer»
* «the SQLModel docs»: «die SQLModel-Dokumentation»
* «the docs»: «die Dokumentation» (use singular case)
* «the env var»: «die Umgebungsvariable»
* «the `PATH` environment variable»: «die `PATH`-Umgebungsvariable»
* «the `PATH`»: «der `PATH`»
* «the `requirements.txt`»: «die `requirements.txt`»
* «the API Router»: «der API-Router»
* «the Authorization-Header»: «der Autorisierungsheader»
* «the `Authorization`-Header»: «der `Authorization`-Header»
* «the background task»: «der Hintergrundtask»
* «the button»: «der Button»
* «the cloud provider»: «der Cloudanbieter»
* «the CLI»: «Das CLI»
* «the command line interface»: «Das Kommandozeileninterface»
* «the default value»: «der Defaultwert»
* «the default value»: NOT «der Standardwert»
* «the default declaration»: «die Default-Deklaration»
* «the dict»: «das Dict»
* «the dictionary»: «das Dictionary»
* «the enumeration»: «die Enumeration»
* «the enum»: «das Enum»
* «the engine»: «die Engine»
* «the error response»: «die Error-Response»
* «the event»: «das Event»
* «the exception»: «die Exception»
* «the exception handler»: «der Exceptionhandler»
* «the form model»: «das Formularmodell»
* «the form body»: «der Formularbody»
* «the header»: «der Header»
* «the headers» (plural): «die Header»
* «in headers» (plural): «in Headern»
* «the forwarded header»: «der Forwarded-Header»
* «the lifespan event»: «das Lifespan-Event»
* «the lock»: «der Lock»
* «the locking»: «das Locking»
* «the mobile application»: «die Mobile-Anwendung»
* «the model object»: «das Modellobjekt»
* «the mounting»: «das Mounten»
* «mounted»: «gemountet»
* «the origin»: «das Origin»
* «the override»: «Die Überschreibung»
* «the parameter»: «der Parameter»
* «the parameters» (plural): «die Parameter»
* «the function parameter»: «der Funktionsparameter»
* «the default parameter»: «der Defaultparameter»
* «the body parameter»: «der Body-Parameter»
* «the request body parameter»: «der Requestbody-Parameter»
* «the path parameter»: «der Pfad-Parameter»
* «the query parameter»: «der Query-Parameter»
* «the cookie parameter»: «der Cookie-Parameter»
* «the header parameter»: «der Header-Parameter»
* «the form parameter»: «der Formular-Parameter»
* «the payload»: «die Payload»
* «the performance»: NOT «die Performance»
* «the query»: «die Query»
* «the recap»: «die Zusammenfassung»
* «the request» (what the client sends to the server): «der Request»
* «the request body»: «der Requestbody»
* «the request bodies» (plural): «die Requestbodys»
* «the response» (what the server sends back to the client): «die Response»
* «the return type»: «der Rückgabetyp»
* «the return value»: «der Rückgabewert»
* «the startup» (the event of the app): «der Startup»
* «the shutdown» (the event of the app): «der Shutdown»
* «the startup event»: «das Startup-Event»
* «the shutdown event»: «das Shutdown-Event»
* «the startup» (of the server): «das Hochfahren»
* «the startup» (the company): «das Startup»
* «the SDK»: «das SDK»
* «the tag»: «der Tag»
* «the type annotation»: «die Typannotation»
* «the type hint»: «der Typhinweis»
* «the wildcard»: «die Wildcard»
* «the worker class»: «die Workerklasse»
* «the worker class»: NOT «die Arbeiterklasse»
* «the worker process»: «der Workerprozess»
* «the worker process»: NOT «der Arbeiterprozess»
* «to commit»: «committen»
* «to modify»: «ändern»
* «to serve» (an application): «bereitstellen»
* «to serve» (a response): «ausliefern»
* «to serve»: NOT «bedienen»
* «to upgrade»: «aktualisieren»
* «to wrap»: «wrappen»
* «to wrap»: NOT «hüllen»
* «`foo` as a `type`»: «`foo` vom Typ `type`»
* «`foo` as a `type`»: «`foo`, ein `type`»
* «FastAPI's X»: «FastAPIs X»
* «Starlette's Y»: «Starlettes Y»
* «X is case-sensitive»: «Groß-/Klein­schrei­bung ist relevant in X»
* «X is case-insensitive»: «Groß-/Klein­schrei­bung ist nicht relevant in X»
* «standard Python»: «Standard-Python»
* «deprecated»: «deprecatet»


### Other rules

Preserve indentation. Keep emoticons. Encode in utf-8. Use Linux line breaks (LF).
