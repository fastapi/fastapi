# LLM Testbestand { #llm-test-file }

Dit document test of de <abbr title="Large Language Model - Groot taalmodel">LLM</abbr>, die de documentatie vertaalt, de `general_prompt` in `scripts/translate.py` en de taalspecifieke prompt in `docs/{language code}/llm-prompt.md` begrijpt. De taalspecifieke prompt wordt toegevoegd aan het einde van `general_prompt`.

De tests die hier worden toegevoegd zullen worden gezien door alle mensen die taalspecifieke prompts ontwerpen.

Gebruik het als volgt:

* Heb een taalspecifieke prompt - `docs/{language code}/llm-prompt.md`.
* Maak een nieuwe vertaling van dit document naar je doeltaal (zie bijvoorbeeld het `translate-page` commando van `translate.py`). Dit zal de vertaling aanmaken in `docs/{language code}/docs/_llm-test.md`.
* Controleer of de dingen goed zijn in de vertaling.
* Indien nodig, verbeter je taalspecifieke prompt, de algemene prompt, of het Engelse document.
* Corrigeer vervolgens handmatig de resterende problemen in de vertaling zodat het een goede vertaling is.
* Vertaal opnieuw, met de goede vertaling op zijn plaats. Het ideale resultaat zou zijn dat de LLM geen wijzigingen meer aanbrengt in de vertaling. Dat betekent dat de algemene prompt en je taalspecifieke prompt zo goed zijn als ze kunnen zijn (Soms zal het enkele schijnbaar willekeurige wijzigingen maken; de reden is dat <a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">LLM's geen deterministische algoritmes zijn</a>).

De tests:

## Code snippets { #code-snippets }

//// tab | Test

Dit is een code snippet: `foo`. En dit is een ander code snippet: `bar`. En nog een: `baz quux`.

////

//// tab | Info

De inhoud van code snippets moet onveranderd worden gelaten.

Zie de sectie `### Content of code snippets` in de algemene prompt in `scripts/translate.py`.

////

## Aanhalingstekens { #quotes }

//// tab | Test

Gisteren schreef mijn vriend: "Als je 'incorrectly' correct schrijft, heb je het incorrect geschreven". Waarop ik antwoordde: "Correct, maar 'incorrectly' is incorrect, niet '"incorrectly"'".

/// note | Opmerking

De LLM zal dit waarschijnlijk verkeerd vertalen. Wat interessant is, is of het de gecorrigeerde vertaling behoudt bij het opnieuw vertalen.

///

////

//// tab | Info

De persoon die de prompt ontwerpt kan kiezen of hij neutrale aanhalingstekens wil omzetten naar typografische aanhalingstekens. Het is ook prima om ze te laten zoals ze zijn.

Zie bijvoorbeeld de sectie `### Quotes` in `docs/de/llm-prompt.md`.

////

## Aanhalingstekens in code snippets { #quotes-in-code-snippets }

//// tab | Test

`pip install "foo[bar]"`

Voorbeelden van string literals in code snippets: `"this"`, `'that'`.

Een moeilijk voorbeeld van string literals in code snippets: `f"I like {'oranges' if orange else "apples"}"`

Hardcore: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | Info

... Echter, aanhalingstekens binnen code snippets moeten onveranderd blijven.

////

## Codeblokken { #code-blocks }

//// tab | Test

Een voorbeeld van Bash code...

```bash
# Print een groet naar het universum
echo "Hello universe"
```

...en een voorbeeld van console code...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

...en nog een voorbeeld van console code...

```console
// Maak een "Code" directory
$ mkdir code
// Ga naar die directory
$ cd code
```

...en een voorbeeld van Python code...

```Python
wont_work()  # Dit gaat niet werken 😱
works(foo="bar")  # Dit werkt 🎉
```

...en dat is alles.

////

//// tab | Info

De code in codeblokken mag niet worden gewijzigd, met uitzondering van commentaar.

Zie de sectie `### Content of code blocks` in de algemene prompt in `scripts/translate.py`.

////

## Tabs en gekleurde vakken { #tabs-and-colored-boxes }

//// tab | Test

/// info | Informatie
Wat tekst
///

/// note | Opmerking
Wat tekst
///

/// note | Technische details
Wat tekst
///

/// check | Controleer
Wat tekst
///

/// tip | Tip
Wat tekst
///

/// warning | Waarschuwing
Wat tekst
///

/// danger | Gevaar
Wat tekst
///

////

//// tab | Info

Tabs en `Info`/`Note`/`Warning`/etc. blokken moeten de vertaling van hun titel toegevoegd krijgen na een verticale streep (`|`).

Zie de secties `### Special blocks` en `### Tab blocks` in de algemene prompt in `scripts/translate.py`.

////

## Web en interne links { #web-and-internal-links }

//// tab | Test

De linktekst moet worden vertaald, het linkadres moet onveranderd blijven:

* [Link naar de kop hierboven](#code-snippets)
* [Interne link](index.md#installation){.internal-link target=_blank}
* <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">Externe link</a>
* <a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">Link naar een stylesheet</a>
* <a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">Link naar een script</a>
* <a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">Link naar een afbeelding</a>

De linktekst moet worden vertaald, het linkadres moet naar de vertaling wijzen:

* <a href="https://fastapi.tiangolo.com/nl/" class="external-link" target="_blank">Link naar FastAPI</a>

////

//// tab | Info

Links moeten worden vertaald, maar hun adres moet onveranderd blijven. Een uitzondering zijn absolute links naar FastAPI documentatiepagina's. In dat geval moeten ze linken naar de vertaling.

Zie de sectie `### Links` in de algemene prompt in `scripts/translate.py`.

////

## HTML "abbr" elementen { #html-abbr-elements }

//// tab | Test

Hier zijn enkele dingen verpakt in HTML "abbr" elementen (sommige zijn verzonnen):

### De abbr geeft een volledige frase { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done - Dingen voor elkaar krijgen">GTD</abbr>
* <abbr title="less than - kleiner dan"><code>lt</code></abbr>
* <abbr title="XML Web Token - XML web token">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface - Parallelle server gateway interface">PSGI</abbr>

### De abbr geeft een uitleg { #the-abbr-gives-an-explanation }

* <abbr title="Een groep machines geconfigureerd om verbonden te zijn en op een of andere manier samen te werken.">cluster</abbr>
* <abbr title="Een machine learning methode die gebruik maakt van kunstmatige neurale netwerken met talrijke verborgen lagen tussen de invoer- en uitvoerlagen, en zo een complexe interne structuur ontwikkelt">Deep Learning</abbr>

### De abbr geeft een volledige frase en een uitleg { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network - Mozilla Ontwikkelaar Netwerk: documentatie voor ontwikkelaars, geschreven door de mensen van Firefox">MDN</abbr>
* <abbr title="Input/Output - Invoer/Uitvoer: lezen of schrijven naar schijf, netwerkcommunicatie.">I/O</abbr>.

////

//// tab | Info

De "title" attributen van "abbr" elementen worden vertaald volgens specifieke instructies.

Vertalingen kunnen hun eigen "abbr" elementen toevoegen die de LLM niet moet verwijderen. Bijv. om Engelse woorden uit te leggen.

Zie de sectie `### HTML abbr elements` in de algemene prompt in `scripts/translate.py`.

////

## Koppen { #headings }

//// tab | Test

### Ontwikkel een webapp - een tutorial { #develop-a-webapp-a-tutorial }

Hallo.

### Type hints en -annotaties { #type-hints-and-annotations }

Hallo weer.

### Superclasses en subclasses { #super-and-subclasses }

Hallo weer.

////

//// tab | Info

De enige strikte regel voor koppen is dat de LLM het hash-gedeelte binnen accolades onveranderd laat, wat ervoor zorgt dat links niet breken.

Zie de sectie `### Headings` in de algemene prompt in `scripts/translate.py`.

Voor taalspecifieke instructies, zie bijv. de sectie `### Headings` in `docs/de/llm-prompt.md`.

////

## Termen gebruikt in de documentatie { #terms-used-in-the-docs }

//// tab | Test

* jij
* jouw

* bijv.
* enz.

* `foo` als een `int`
* `bar` als een `str`
* `baz` als een `list`

* de Tutorial - Gebruikershandleiding
* de Geavanceerde Gebruikershandleiding
* de SQLModel documentatie
* de API documentatie
* de automatische documentatie

* Data Science
* Deep Learning
* Machine Learning
* Dependency Injection
* HTTP Basic authenticatie
* HTTP Digest
* ISO formaat
* de JSON Schema standaard
* het JSON Schema
* de schema definitie
* Password Flow
* Mobiel

* verouderd
* ontworpen
* ongeldig
* on the fly
* standaard
* standaard waarde
* hoofdlettergevoelig
* niet hoofdlettergevoelig

* de applicatie serveren
* de pagina serveren

* de app
* de applicatie

* de request
* de response
* de error response

* de path operation
* de path operation decorator
* de path operation functie

* de body
* de request body
* de response body
* de JSON body
* de form body
* de file body
* het functie body

* de parameter
* de body parameter
* de path parameter
* de query parameter
* de cookie parameter
* de header parameter
* de form parameter
* de functie parameter

* de event
* de startup event
* de server startup
* de shutdown event
* de lifespan event

* de handler
* de event handler
* de exception handler
* handelen

* het model
* het Pydantic model
* het data model
* het database model
* het form model
* het model object

* de class
* de base class
* de parent class
* de subclass
* de child class
* de sibling class
* de class method

* de header
* de headers
* de authorization header
* de `Authorization` header
* de forwarded header

* het dependency injection systeem
* de dependency
* de dependable
* de dependent

* I/O gebonden
* CPU gebonden
* concurrency
* parallelisme
* multiprocessing

* de env var
* de environment variable
* de `PATH`
* de `PATH` variable

* de authenticatie
* de authenticatie provider
* de autorisatie
* het autorisatie formulier
* de autorisatie provider
* de gebruiker authenticeert
* het systeem authenticeert de gebruiker

* de CLI
* de command-line interface

* de server
* de client

* de cloud provider
* de cloud service

* de ontwikkeling
* de ontwikkelfases

* de dict
* het dictionary
* de enumeratie
* de enum
* het enum member

* de encoder
* de decoder
* encoderen
* decoderen

* de exception
* gooien

* de expressie
* het statement

* de frontend
* de backend

* de GitHub discussie
* de GitHub issue

* de performance
* de performance optimalisatie

* het return type
* de return waarde

* de beveiliging
* het beveiligingsschema

* de taak
* de achtergrondtaak
* de taak functie

* de template
* de template engine

* de type annotatie
* de type annotaties

* de server worker
* de Uvicorn worker
* de Gunicorn Worker
* het worker process
* de worker class
* de workload

* de deployment
* deployen

* de SDK
* de software development kit

* de `APIRouter`
* de `requirements.txt`
* de Bearer Token
* de breaking change
* de bug
* de button
* de callable
* de code
* de commit
* de context manager
* de coroutine
* de database sessie
* de disk
* het domein
* de engine
* de nepX
* de HTTP GET methode
* het item
* het package
* de lifespan
* de lock
* de middleware
* de mobiele app
* de module
* de mount
* het netwerk
* de origin
* de override
* de payload
* de processor
* de property
* de proxy
* de pull request
* de query
* de RAM
* de remote machine
* de status code
* de string
* de tag
* het web framework
* de wildcard
* retourneren
* valideren

////

//// tab | Info

Dit is een niet-complete en niet-normatieve lijst van (meestal) technische termen die in de documentatie voorkomen. Het kan de persoon die de prompt ontwerpt helpen om te identificeren voor welke termen de LLM een handje nodig heeft. Bijvoorbeeld wanneer het steeds een goede vertaling blijft terugdraaien naar een suboptimale vertaling. Of wanneer het problemen heeft met het vervoegen/verbuigen van een term in jouw taal.

Zie bijv. de sectie `### List of English terms and their preferred German translations` in `docs/de/llm-prompt.md`.

////
