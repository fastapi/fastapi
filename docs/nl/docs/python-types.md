# Introductie tot Python Types

Python biedt ondersteuning voor optionele "type hints" (ook wel "type annotaties" genoemd).

Deze **"type hints"** of annotaties zijn een speciale syntax waarmee het <abbr title="bijvoorbeeld: str, int, float, bool">type</abbr> van een variabele kan worden gedeclareerd.

Door types voor je variabelen te declareren, kunnen editors en hulpmiddelen je beter ondersteunen.

Dit is slechts een **korte tutorial/opfrisser** over Python type hints. Het behandelt enkel het minimum dat nodig is om ze te gebruiken met **FastAPI**... en dat is relatief weinig.

**FastAPI** is helemaal gebaseerd op deze type hints, ze geven veel voordelen.

Maar zelfs als je **FastAPI** nooit gebruikt, heb je er baat bij om er iets over te leren.

/// note

Als je een Python expert bent en alles al weet over type hints, sla dan dit hoofdstuk over.

///

## Motivatie

Laten we beginnen met een eenvoudig voorbeeld:

```Python
{!../../../docs_src/python_types/tutorial001.py!}
```

Het aanroepen van dit programma leidt tot het volgende resultaat:

```
John Doe
```

De functie voert het volgende uit:

* Neem een `first_name` en een `last_name`
* Converteer de eerste letter van elk naar een hoofdletter met `title()`.
``
* <abbr title="Voegt ze samen, als één. Met de inhoud van de een na de ander.">Voeg samen</abbr> met een spatie in het midden.

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial001.py!}
```

### Bewerk het

Dit is een heel eenvoudig programma.

Maar stel je nu voor dat je het vanaf nul zou moeten maken.

Op een gegeven moment zou je aan de definitie van de functie zijn begonnen, je had de parameters klaar...

Maar dan moet je “die methode die de eerste letter naar hoofdletters converteert” aanroepen.

Was het `upper`? Was het `uppercase`? `first_uppercase`? `capitalize`?

Dan roep je de hulp in van je oude programmeursvriend, (automatische) code aanvulling in je editor.

Je typt de eerste parameter van de functie, `first_name`, dan een punt (`.`) en drukt dan op `Ctrl+Spatie` om de aanvulling te activeren.

Maar helaas krijg je niets bruikbaars:

<img src="/img/python-types/image01.png">

### Types toevoegen

Laten we een enkele regel uit de vorige versie aanpassen.

We zullen precies dit fragment, de parameters van de functie, wijzigen van:

```Python
    first_name, last_name
```

naar:

```Python
    first_name: str, last_name: str
```

Dat is alles.

Dat zijn de "type hints":

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial002.py!}
```

Dit is niet hetzelfde als het declareren van standaardwaarden zoals bij:

```Python
    first_name="john", last_name="doe"
```

Het is iets anders.

We gebruiken dubbele punten (`:`), geen gelijkheidstekens (`=`).

Het toevoegen van type hints verandert normaal gesproken niet wat er gebeurt in je programma t.o.v. wat er zonder type hints zou gebeuren.

Maar stel je voor dat je weer bezig bent met het maken van een functie, maar deze keer met type hints.

Op hetzelfde moment probeer je de automatische aanvulling te activeren met `Ctrl+Spatie` en je ziet:

<img src="/img/python-types/image02.png">

Nu kun je de opties bekijken en er doorheen scrollen totdat je de optie vindt die “een belletje doet rinkelen”:

<img src="/img/python-types/image03.png">

### Meer motivatie

Bekijk deze functie, deze heeft al type hints:

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial003.py!}
```

Omdat de editor de types van de variabelen kent, krijgt u niet alleen aanvulling, maar ook controles op fouten:

<img src="/img/python-types/image04.png">

Nu weet je hoe je het moet oplossen, converteer `age` naar een string met `str(age)`:

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial004.py!}
```

## Types declareren

Je hebt net de belangrijkste plek om type hints te declareren gezien. Namelijk als functieparameters.

Dit is ook de belangrijkste plek waar je ze gebruikt met **FastAPI**.

### Eenvoudige types

Je kunt alle standaard Python types declareren, niet alleen `str`.

Je kunt bijvoorbeeld het volgende gebruiken:

* `int`
* `float`
* `bool`
* `bytes`

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial005.py!}
```

### Generieke types met typeparameters

Er zijn enkele datastructuren die andere waarden kunnen bevatten, zoals `dict`, `list`, `set` en `tuple` en waar ook de interne waarden hun eigen type kunnen hebben.

Deze types die interne types hebben worden “**generieke**” types genoemd. Het is mogelijk om ze te declareren, zelfs met hun interne types.

Om deze types en de interne types te declareren, kun je de standaard Python module `typing` gebruiken. Deze module is speciaal gemaakt om deze type hints te ondersteunen.

#### Nieuwere versies van Python

De syntax met `typing` is **verenigbaar** met alle versies, van Python 3.6 tot aan de nieuwste, inclusief Python 3.9, Python 3.10, enz.

Naarmate Python zich ontwikkelt, worden **nieuwere versies**, met verbeterde ondersteuning voor deze type annotaties, beschikbaar. In veel gevallen hoef je niet eens de `typing` module te importeren en te gebruiken om de type annotaties te declareren.

Als je een recentere versie van Python kunt kiezen voor je project, kun je profiteren van die extra eenvoud.

In alle documentatie staan voorbeelden die compatibel zijn met elke versie van Python (als er een verschil is).

Bijvoorbeeld “**Python 3.6+**” betekent dat het compatibel is met Python 3.6 of hoger (inclusief 3.7, 3.8, 3.9, 3.10, etc). En “**Python 3.9+**” betekent dat het compatibel is met Python 3.9 of hoger (inclusief 3.10, etc).

Als je de **laatste versies van Python** kunt gebruiken, gebruik dan de voorbeelden voor de laatste versie, die hebben de **beste en eenvoudigste syntax**, bijvoorbeeld “**Python 3.10+**”.

#### List

Laten we bijvoorbeeld een variabele definiëren als een `list` van `str`.

//// tab | Python 3.9+

Declareer de variabele met dezelfde dubbele punt (`:`) syntax.

Als type, vul `list` in.

Doordat de list een type is dat enkele interne types bevat, zet je ze tussen vierkante haakjes:

```Python hl_lines="1"
{!> ../../../docs_src/python_types/tutorial006_py39.py!}
```

////

//// tab | Python 3.8+

Van `typing`, importeer `List` (met een hoofdletter `L`):

```Python hl_lines="1"
{!> ../../../docs_src/python_types/tutorial006.py!}
```

Declareer de variabele met dezelfde dubbele punt (`:`) syntax.

Zet als type de `List` die je hebt geïmporteerd uit `typing`.

Doordat de list een type is dat enkele interne types bevat, zet je ze tussen vierkante haakjes:

```Python hl_lines="4"
{!> ../../../docs_src/python_types/tutorial006.py!}
```

////

/// info

De interne types tussen vierkante haakjes worden “typeparameters” genoemd.

In dit geval is `str` de typeparameter die wordt doorgegeven aan `List` (of `list` in Python 3.9 en hoger).

///

Dat betekent: “de variabele `items` is een `list`, en elk van de items in deze list is een `str`”.

/// tip

Als je Python 3.9 of hoger gebruikt, hoef je `List` niet te importeren uit `typing`, je kunt in plaats daarvan hetzelfde reguliere `list` type gebruiken.

///

Door dat te doen, kan je editor ondersteuning bieden, zelfs tijdens het verwerken van items uit de list:

<img src="/img/python-types/image05.png">

Zonder types is dat bijna onmogelijk om te bereiken.

Merk op dat de variabele `item` een van de elementen is in de lijst `items`.

Toch weet de editor dat het een `str` is, en biedt daar vervolgens ondersteuning voor aan.

#### Tuple en Set

Je kunt hetzelfde doen om `tuple`s en `set`s te declareren:

//// tab | Python 3.9+

```Python hl_lines="1"
{!> ../../../docs_src/python_types/tutorial007_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../../docs_src/python_types/tutorial007.py!}
```

////

Dit betekent:

* De variabele `items_t` is een `tuple` met 3 items, een `int`, nog een `int`, en een `str`.
* De variabele `items_s` is een `set`, en elk van de items is van het type `bytes`.

#### Dict

Om een `dict` te definiëren, geef je 2 typeparameters door, gescheiden door komma's.

De eerste typeparameter is voor de sleutels (keys) van de `dict`.

De tweede typeparameter is voor de waarden  (values) van het `dict`:

//// tab | Python 3.9+

```Python hl_lines="1"
{!> ../../../docs_src/python_types/tutorial008_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../../docs_src/python_types/tutorial008.py!}
```

////

Dit betekent:

* De variabele `prices` is een `dict`:
    * De sleutels van dit `dict` zijn van het type `str` (bijvoorbeeld de naam van elk item).
    * De waarden van dit `dict` zijn van het type `float` (bijvoorbeeld de prijs van elk item).

#### Union

Je kunt een variable declareren die van **verschillende types** kan zijn, bijvoorbeeld een `int` of een `str`.

In Python 3.6 en hoger (inclusief Python 3.10) kun je het `Union`-type van `typing` gebruiken en de mogelijke types die je wilt accepteren, tussen de vierkante haakjes zetten.

In Python 3.10 is er ook een **nieuwe syntax** waarin je de mogelijke types kunt scheiden door een <abbr title='ook wel "bitwise of operator" genoemd, maar die betekenis is hier niet relevant'>verticale balk (`|`)</abbr>.

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../../docs_src/python_types/tutorial008b_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../../docs_src/python_types/tutorial008b.py!}
```

////

In beide gevallen betekent dit dat `item` een `int` of een `str` kan zijn.

#### Mogelijk `None`

Je kunt declareren dat een waarde een type kan hebben, zoals `str`, maar dat het ook `None` kan zijn.

In Python 3.6 en hoger (inclusief Python 3.10) kun je het declareren door `Optional` te importeren en te gebruiken vanuit de `typing`-module.

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009.py!}
```

Door `Optional[str]` te gebruiken in plaats van alleen `str`, kan de editor je helpen fouten te detecteren waarbij je ervan uit zou kunnen gaan dat een waarde altijd een `str` is, terwijl het in werkelijkheid ook `None` zou kunnen zijn.

`Optional[EenType]` is eigenlijk een snelkoppeling voor `Union[EenType, None]`, ze zijn equivalent.

Dit betekent ook dat je in Python 3.10 `EenType | None` kunt gebruiken:

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../../docs_src/python_types/tutorial009_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../../docs_src/python_types/tutorial009.py!}
```

////

//// tab | Python 3.8+ alternative

```Python hl_lines="1  4"
{!> ../../../docs_src/python_types/tutorial009b.py!}
```

////

#### Gebruik van `Union` of `Optional`

Als je een Python versie lager dan 3.10 gebruikt, is dit een tip vanuit mijn **subjectieve** standpunt:

* 🚨 Vermijd het gebruik van `Optional[EenType]`.
* Gebruik in plaats daarvan **`Union[EenType, None]`** ✨.

Beide zijn gelijkwaardig en onderliggend zijn ze hetzelfde, maar ik zou `Union` aanraden in plaats van `Optional` omdat het woord “**optional**” lijkt te impliceren dat de waarde optioneel is, en het eigenlijk betekent “het kan `None` zijn”, zelfs als het niet optioneel is en nog steeds vereist is.

Ik denk dat `Union[SomeType, None]` explicieter is over wat het betekent.

Het gaat alleen om de woorden en naamgeving. Maar die naamgeving kan invloed hebben op hoe jij en je teamgenoten over de code denken.

Laten we als voorbeeld deze functie nemen:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009c.py!}
```

De parameter `name` is gedefinieerd als `Optional[str]`, maar is **niet optioneel**, je kunt de functie niet aanroepen zonder de parameter:

```Python
say_hi()  # Oh, nee, dit geeft een foutmelding! 😱
```

De `name` parameter is **nog steeds vereist** (niet *optioneel*) omdat het geen standaardwaarde heeft. Toch accepteert `name` `None` als waarde:

```Python
say_hi(name=None)  # Dit werkt, None is geldig 🎉
```

Het goede nieuws is dat als je eenmaal Python 3.10 gebruikt, je je daar geen zorgen meer over hoeft te maken, omdat je dan gewoon `|` kunt gebruiken om unions van types te definiëren:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009c_py310.py!}
```

Dan hoef je je geen zorgen te maken over namen als `Optional` en `Union`. 😎

#### Generieke typen

De types die typeparameters in vierkante haakjes gebruiken, worden **Generieke types** of **Generics** genoemd, bijvoorbeeld:

//// tab | Python 3.10+

Je kunt dezelfde ingebouwde types gebruiken als generics (met vierkante haakjes en types erin):

* `list`
* `tuple`
* `set`
* `dict`

Hetzelfde als bij Python 3.8, uit de `typing`-module:

* `Union`
* `Optional` (hetzelfde als bij Python 3.8)
* ...en anderen.

In Python 3.10 kun je , als alternatief voor de generieke `Union` en `Optional`, de <abbr title='ook wel "bitwise or operator" genoemd, maar die betekenis is hier niet relevant'>verticale lijn (`|`)</abbr> gebruiken om unions van typen te voorzien, dat is veel beter en eenvoudiger.

////

//// tab | Python 3.9+

Je kunt dezelfde ingebouwde types gebruiken als generieke types (met vierkante haakjes en types erin):

* `list`
* `tuple`
* `set`
* `dict`

En hetzelfde als met Python 3.8, vanuit de `typing`-module:

* `Union`
* `Optional`
* ...en anderen.

////

//// tab | Python 3.8+

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Union`
* `Optional`
* ...en anderen.

////

### Klassen als types

Je kunt een klasse ook declareren als het type van een variabele.

Stel dat je een klasse `Person` hebt, met een naam:

```Python hl_lines="1-3"
{!../../../docs_src/python_types/tutorial010.py!}
```

Vervolgens kun je een variabele van het type `Persoon` declareren:

```Python hl_lines="6"
{!../../../docs_src/python_types/tutorial010.py!}
```

Dan krijg je ook nog eens volledige editorondersteuning:

<img src="/img/python-types/image06.png">

Merk op dat dit betekent dat "`one_person` een **instantie** is van de klasse `Person`".

Dit betekent niet dat `one_person` de **klasse** is met de naam `Person`.

## Pydantic modellen

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> is een Python-pakket voor het uitvoeren van datavalidatie.

Je declareert de "vorm" van de data als klassen met attributen.

Elk attribuut heeft een type.

Vervolgens maak je een instantie van die klasse met een aantal waarden en het valideert de waarden, converteert ze naar het juiste type (als dat het geval is) en geeft je een object met alle data terug.

Daarnaast krijg je volledige editorondersteuning met dat resulterende object.

Een voorbeeld uit de officiële Pydantic-documentatie:

//// tab | Python 3.10+

```Python
{!> ../../../docs_src/python_types/tutorial011_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!> ../../../docs_src/python_types/tutorial011_py39.py!}
```

////

//// tab | Python 3.8+

```Python
{!> ../../../docs_src/python_types/tutorial011.py!}
```

////

/// info

Om meer te leren over <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic, bekijk de documentatie</a>.

///

**FastAPI** is volledig gebaseerd op Pydantic.

Je zult veel meer van dit alles in de praktijk zien in de [Tutorial - Gebruikershandleiding](tutorial/index.md){.internal-link target=_blank}.

/// tip

Pydantic heeft een speciaal gedrag wanneer je `Optional` of `Union[EenType, None]` gebruikt zonder een standaardwaarde, je kunt er meer over lezen in de Pydantic-documentatie over <a href="https://docs.pydantic.dev/2.3/usage/models/#required-fields" class="external-link" target="_blank">Verplichte optionele velden</a>.

///

## Type Hints met Metadata Annotaties

Python heeft ook een functie waarmee je **extra <abbr title="Data over de data, in dit geval informatie over het type, bijvoorbeeld een beschrijving.">metadata</abbr>** in deze type hints kunt toevoegen met behulp van `Annotated`.

//// tab | Python 3.9+

In Python 3.9 is `Annotated` onderdeel van de standaardpakket, dus je kunt het importeren vanuit `typing`.

```Python hl_lines="1  4"
{!> ../../../docs_src/python_types/tutorial013_py39.py!}
```

////

//// tab | Python 3.8+

In versies lager dan Python 3.9 importeer je `Annotated` vanuit `typing_extensions`.

Het wordt al geïnstalleerd met **FastAPI**.

```Python hl_lines="1  4"
{!> ../../../docs_src/python_types/tutorial013.py!}
```

////

Python zelf doet niets met deze `Annotated` en voor editors en andere hulpmiddelen is het type nog steeds een `str`.

Maar je kunt deze ruimte in `Annotated` gebruiken om **FastAPI** te voorzien van extra metadata over hoe je wilt dat je applicatie zich gedraagt.

Het belangrijkste om te onthouden is dat **de eerste *typeparameter*** die je doorgeeft aan `Annotated` het **werkelijke type** is. De rest is gewoon metadata voor andere hulpmiddelen.

Voor nu hoef je alleen te weten dat `Annotated` bestaat en dat het standaard Python is. 😎

Later zul je zien hoe **krachtig** het kan zijn.

/// tip

Het feit dat dit **standaard Python** is, betekent dat je nog steeds de **best mogelijke ontwikkelaarservaring** krijgt in je editor, met de hulpmiddelen die je gebruikt om je code te analyseren en te refactoren, enz. ✨

Daarnaast betekent het ook dat je code zeer verenigbaar zal zijn met veel andere Python-hulpmiddelen en -pakketten. 🚀

///

## Type hints in **FastAPI**

**FastAPI** maakt gebruik van type hints om verschillende dingen te doen.

Met **FastAPI** declareer je parameters met type hints en krijg je:

* **Editor ondersteuning**.
* **Type checks**.

...en **FastAPI** gebruikt dezelfde declaraties om:

* **Vereisten te definïeren **: van request pad parameters, query parameters, headers, bodies, dependencies, enz.
* **Data te converteren**: van de request naar het vereiste type.
* **Data te valideren**: afkomstig van elke request:
    * **Automatische foutmeldingen** te genereren die naar de client worden geretourneerd wanneer de data ongeldig is.
* De API met OpenAPI te **documenteren**:
    * die vervolgens wordt gebruikt door de automatische interactieve documentatie gebruikersinterfaces.

Dit klinkt misschien allemaal abstract. Maak je geen zorgen. Je ziet dit allemaal in actie in de [Tutorial - Gebruikershandleiding](tutorial/index.md){.internal-link target=_blank}.

Het belangrijkste is dat door standaard Python types te gebruiken, op één plek (in plaats van meer klassen, decorators, enz. toe te voegen), **FastAPI** een groot deel van het werk voor je doet.

/// info

Als je de hele tutorial al hebt doorgenomen en terug bent gekomen om meer te weten te komen over types, is een goede bron <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">het "cheat sheet" van `mypy`</a>.

///
