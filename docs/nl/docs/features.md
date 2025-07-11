# Functionaliteit

## FastAPI functionaliteit

**FastAPI** biedt je het volgende:

### Gebaseerd op open standaarden

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> voor het maken van API's, inclusief declaraties van <abbr title="ook bekend als: endpoints, routess">pad</abbr><abbr title="ook bekend als HTTP-methoden, zoals POST, GET, PUT, DELETE">bewerkingen</abbr>, parameters, request bodies, beveiliging, enz.
* Automatische datamodel documentatie met <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (aangezien OpenAPI zelf is gebaseerd op JSON Schema).
* Ontworpen op basis van deze standaarden, na zorgvuldig onderzoek. In plaats van achteraf deze laag er bovenop te bouwen.
* Dit maakt het ook mogelijk om automatisch **clientcode te genereren** in verschillende programmeertalen.

### Automatische documentatie

Interactieve API-documentatie en verkenning van webgebruikersinterfaces. Aangezien dit framework is gebaseerd op OpenAPI, zijn er meerdere documentatie opties mogelijk, waarvan er standaard 2 zijn inbegrepen.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, met interactieve interface, maakt het mogelijk je API rechtstreeks vanuit de browser aan te roepen en te testen.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Alternatieve API-documentatie met <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Gewoon Moderne Python

Het is allemaal gebaseerd op standaard **Python type** declaraties (dankzij Pydantic). Je hoeft dus geen nieuwe syntax te leren. Het is gewoon standaard moderne Python.

Als je een opfriscursus van 2 minuten nodig hebt over het gebruik van Python types (zelfs als je FastAPI niet gebruikt), bekijk dan deze korte tutorial: [Python Types](python-types.md){.internal-link target=_blank}.

Je schrijft gewoon standaard Python met types:

```Python
from datetime import date

from pydantic import BaseModel

# Declareer een variabele als een str
# en krijg editorondersteuning in de functie
def main(user_id: str):
    return user_id


# Een Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Vervolgens kan je het op deze manier gebruiken:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

/// info

`**second_user_data` betekent:

Geef de sleutels (keys) en waarden (values) van de `second_user_data` dict direct door als sleutel-waarden argumenten, gelijk aan: `User(id=4, name=“Mary”, joined=“2018-11-30”)`

///

### Editor-ondersteuning

Het gehele framework is ontworpen om eenvoudig en intuïtief te zijn in gebruik. Alle beslissingen zijn getest op meerdere code-editors nog voordat het daadwerkelijke ontwikkelen begon, om zo de beste ontwikkelervaring te garanderen.

Uit enquêtes onder Python ontwikkelaars blijkt maar al te duidelijk dat "(automatische) code aanvulling" <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">een van de meest gebruikte functionaliteiten is</a>.

Het hele **FastAPI** framework is daarop gebaseerd. Automatische code aanvulling werkt overal.

Je hoeft zelden terug te vallen op de documentatie.

Zo kan je editor je helpen:

* in <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

![editor ondersteuning](https://fastapi.tiangolo.com/img/vscode-completion.png)

* in <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![editor ondersteuning](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Je krijgt autocomletion die je voorheen misschien zelfs voor onmogelijk had gehouden. Zoals bijvoorbeeld de `price` key in een JSON body (die genest had kunnen zijn) die afkomstig is van een request.

Je hoeft niet langer de verkeerde keys in te typen, op en neer te gaan tussen de documentatie, of heen en weer te scrollen om te checken of je `username` of toch `user_name` had gebruikt.

### Kort

Dit framework heeft voor alles verstandige **standaardinstellingen**, met overal optionele configuraties. Alle parameters kunnen worden verfijnd zodat het past bij wat je nodig hebt, om zo de API te kunnen definiëren die jij nodig hebt.

Maar standaard werkt alles **“gewoon”**.

### Validatie

* Validatie voor de meeste (of misschien wel alle?) Python **datatypes**, inclusief:
    * JSON objecten (`dict`).
    * JSON array (`list`) die itemtypes definiëren.
    * String (`str`) velden, die min en max lengtes hebben.
    * Getallen (`int`, `float`) met min en max waarden, enz.

* Validatie voor meer exotische typen, zoals:
    * URL.
    * E-mail.
    * UUID.
    * ...en anderen.

Alle validatie wordt uitgevoerd door het beproefde en robuuste **Pydantic**.

### Beveiliging en authenticatie

Beveiliging en authenticatie is geïntegreerd. Zonder compromissen te doen naar databases of datamodellen.

Alle beveiligingsschema's gedefinieerd in OpenAPI, inclusief:

* HTTP Basic.
* **OAuth2** (ook met **JWT tokens**). Bekijk de tutorial over [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* API keys in:
    * Headers.
    * Query parameters.
    * Cookies, enz.

Plus alle beveiligingsfuncties van Starlette (inclusief **sessiecookies**).

Gebouwd als een herbruikbare tool met componenten die makkelijk te integreren zijn in en met je systemen, datastores, relationele en NoSQL databases, enz.

### Dependency Injection

FastAPI bevat een uiterst eenvoudig, maar uiterst krachtig <abbr title='ook bekend als "componenten", "bronnen", "diensten", "aanbieders"'><strong>Dependency Injection</strong></abbr> systeem.

* Zelfs dependencies kunnen dependencies hebben, waardoor een hiërarchie of **“graph” van dependencies** ontstaat.
* Allemaal **automatisch afgehandeld** door het framework.
* Alle dependencies kunnen data nodig hebben van request, de vereiste **padoperaties veranderen** en automatische documentatie verstrekken.
* **Automatische validatie** zelfs voor *padoperatie* parameters gedefinieerd in dependencies.
* Ondersteuning voor complexe gebruikersauthenticatiesystemen, **databaseverbindingen**, enz.
* **Geen compromisen** met databases, gebruikersinterfaces, enz. Maar eenvoudige integratie met ze allemaal.

### Ongelimiteerde "plug-ins"

Of anders gezegd, je hebt ze niet nodig, importeer en gebruik de code die je nodig hebt.

Elke integratie is ontworpen om eenvoudig te gebruiken (met afhankelijkheden), zodat je een “plug-in" kunt maken in 2 regels code, met dezelfde structuur en syntax die wordt gebruikt voor je *padbewerkingen*.

### Getest

* 100% <abbr title="De hoeveelheid code die automatisch wordt getest">van de code is getest</abbr>.
* 100% <abbr title="Python type annotaties, hiermee kunnen je editor en externe tools je beter ondersteunen">type geannoteerde</abbr> codebase.
* Wordt gebruikt in productietoepassingen.

## Starlette functies

**FastAPI** is volledig verenigbaar met (en gebaseerd op) <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong></a>.

`FastAPI` is eigenlijk een subklasse van `Starlette`. Dus als je Starlette al kent of gebruikt, zal de meeste functionaliteit op dezelfde manier werken.

Met **FastAPI** krijg je alle functies van **Starlette** (FastAPI is gewoon Starlette op steroïden):

* Zeer indrukwekkende prestaties. Het is <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">een van de snelste Python frameworks, vergelijkbaar met **NodeJS** en **Go**</a>.
* **WebSocket** ondersteuning.
* Taken in de achtergrond tijdens het proces.
* Opstart- en afsluit events.
* Test client gebouwd op HTTPX.
* **CORS**, GZip, Statische bestanden, Streaming reacties.
* **Sessie en Cookie** ondersteuning.
* 100% van de code is getest.
* 100% type geannoteerde codebase.

## Pydantic functionaliteit

**FastAPI** is volledig verenigbaar met (en gebaseerd op) Pydantic. Dus alle extra <a href="https://docs.pydantic.dev/" class="external-link" target="_blank"><strong>Pydantic</strong></a> code die je nog hebt werkt ook.

Inclusief externe pakketten die ook gebaseerd zijn op Pydantic, zoals <abbr title="Object-Relational Mapper">ORM</abbr>s, <abbr title="Object-Document Mapper">ODM</abbr>s voor databases.

Dit betekent ook dat je in veel gevallen het object dat je van een request krijgt **direct naar je database** kunt sturen, omdat alles automatisch wordt gevalideerd.

Hetzelfde geldt ook andersom, in veel gevallen kun je dus het object dat je krijgt van de database **direct doorgeven aan de client**.

Met **FastAPI** krijg je alle functionaliteit van **Pydantic** (omdat FastAPI is gebaseerd op Pydantic voor alle dataverwerking):

* **Geen brainfucks**:
    * Je hoeft geen nieuwe microtaal voor schemadefinities te leren.
    * Als je bekend bent Python types, weet je hoe je Pydantic moet gebruiken.
* Werkt goed samen met je **<abbr title=“Integrated Development Environment, vergelijkbaar met een code editor”>IDE</abbr>/<abbr title=“Een programma dat controleert op fouten in de code”>linter</abbr>/hersenen**:
    * Doordat pydantic's datastructuren enkel instanties zijn van klassen, die je definieert, werkt automatische aanvulling, linting, mypy en je intuïtie allemaal goed met je gevalideerde data.
* Valideer **complexe structuren**:
    * Gebruik van hiërarchische Pydantic modellen, Python `typing`'s `List` en `Dict`, enz.
    * Met validators kunnen complexe dataschema's duidelijk en eenvoudig worden gedefinieerd, gecontroleerd en gedocumenteerd als JSON Schema.
    * Je kunt diep **geneste JSON** objecten laten valideren en annoteren.
* **Uitbreidbaar**:
    * Met Pydantic kunnen op maat gemaakte datatypen worden gedefinieerd of je kunt validatie uitbreiden met methoden op een model dat is ingericht met de decorator validator.
* 100% van de code is getest.
