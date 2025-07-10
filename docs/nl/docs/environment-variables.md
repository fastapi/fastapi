# Omgevingsvariabelen

/// tip

Als je al weet wat "omgevingsvariabelen" zijn en hoe je ze kunt gebruiken, kun je deze stap gerust overslaan.

///

Een omgevingsvariabele (ook bekend als "**env var**") is een variabele die **buiten** de Python-code leeft, in het **besturingssysteem** en die door je Python-code (of door andere programma's) kan worden gelezen.

Omgevingsvariabelen kunnen nuttig zijn voor het bijhouden van applicatie **instellingen**, als onderdeel van de **installatie** van Python, enz.

## Omgevingsvariabelen maken en gebruiken

Je kunt omgevingsvariabelen **maken** en gebruiken in de **shell (terminal)**, zonder dat je Python nodig hebt:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Je zou een omgevingsvariabele MY_NAME kunnen maken met
$ export MY_NAME="Wade Wilson"

// Dan zou je deze met andere programma's kunnen gebruiken, zoals
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Maak een omgevingsvariabel MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Gebruik het met andere programma's, zoals
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Omgevingsvariabelen uitlezen in Python

Je kunt omgevingsvariabelen **buiten** Python aanmaken, in de terminal (of met een andere methode) en ze vervolgens **in Python uitlezen**.

Je kunt bijvoorbeeld een bestand `main.py` hebben met:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip

Het tweede argument van <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> is de standaardwaarde die wordt geretourneerd.

Als je dit niet meegeeft, is de standaardwaarde `None`. In dit geval gebruiken we standaard `"World"`.

///

Dan zou je dat Python-programma kunnen aanroepen:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Hier stellen we de omgevingsvariabelen nog niet in
$ python main.py

// Omdat we de omgevingsvariabelen niet hebben ingesteld, krijgen we de standaardwaarde

Hello World from Python

// Maar als we eerst een omgevingsvariabele aanmaken
$ export MY_NAME="Wade Wilson"

// en het programma dan opnieuw aanroepen
$ python main.py

// kan het de omgevingsvariabele nu wel uitlezen

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Hier stellen we de omgevingsvariabelen nog niet in
$ python main.py

// Omdat we de omgevingsvariabelen niet hebben ingesteld, krijgen we de standaardwaarde

Hello World from Python

// Maar als we eerst een omgevingsvariabele aanmaken
$ $Env:MY_NAME = "Wade Wilson"

// en het programma dan opnieuw aanroepen
$ python main.py

// kan het de omgevingsvariabele nu wel uitlezen

Hello Wade Wilson from Python
```

</div>

////

Omdat omgevingsvariabelen buiten de code kunnen worden ingesteld, maar wel door de code kunnen worden gelezen en niet hoeven te worden opgeslagen (gecommit naar `git`) met de rest van de bestanden, worden ze vaak gebruikt voor configuraties of **instellingen**.

Je kunt ook een omgevingsvariabele maken die alleen voor een **specifieke programma-aanroep** beschikbaar is, die alleen voor dat programma beschikbaar is en alleen voor de duur van dat programma.

Om dat te doen, maak je het vlak voor het programma zelf aan, op dezelfde regel:

<div class="termy">

```console
// Maak een omgevingsvariabele MY_NAME in de regel voor deze programma-aanroep
$ MY_NAME="Wade Wilson" python main.py

// Nu kan het de omgevingsvariabele lezen

Hello Wade Wilson from Python

// De omgevingsvariabelen bestaan daarna niet meer
$ python main.py

Hello World from Python
```

</div>

/// tip

Je kunt er meer over lezen op <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a>.

///

## Types en Validatie

Deze omgevingsvariabelen kunnen alleen **tekstuele gegevens** verwerken, omdat ze extern zijn aan Python, compatibel moeten zijn met andere programma's en de rest van het systeem (zelfs met verschillende besturingssystemen, zoals Linux, Windows en macOS).

Dat betekent dat **elke waarde** die in Python uit een omgevingsvariabele wordt gelezen **een `str` zal zijn** en dat elke conversie naar een ander type of elke validatie in de code moet worden uitgevoerd.

Meer informatie over het gebruik van omgevingsvariabelen voor het verwerken van **applicatie instellingen** vind je in de [Geavanceerde gebruikershandleiding - Instellingen en Omgevingsvariabelen](./advanced/settings.md){.internal-link target=_blank}.

## `PATH` Omgevingsvariabele

Er is een **speciale** omgevingsvariabele met de naam **`PATH`**, die door de besturingssystemen (Linux, macOS, Windows) wordt gebruikt om programma's te vinden die uitgevoerd kunnen worden.

De waarde van de variabele `PATH` is een lange string die bestaat uit mappen die gescheiden worden door een dubbele punt `:` op Linux en macOS en door een puntkomma `;` op Windows.

De omgevingsvariabele `PATH` zou er bijvoorbeeld zo uit kunnen zien:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Dit betekent dat het systeem naar programma's zoekt in de mappen:

* `/usr/local/bin`
* `/usr/bin`
* `/bin`
* `/usr/sbin`
* `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

Dit betekent dat het systeem naar programma's zoekt in de mappen:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

Wanneer je een **opdracht** in de terminal typt, **zoekt** het besturingssysteem naar het programma in **elk van de mappen** die vermeld staan in de omgevingsvariabele `PATH`.

Wanneer je bijvoorbeeld `python` in de terminal typt, zoekt het besturingssysteem naar een programma met de naam `python` in de **eerste map** in die lijst.

Zodra het gevonden wordt, zal het dat programma **gebruiken**. Anders blijft het in de **andere mappen** zoeken.

### Python installeren en `PATH` bijwerken

Wanneer je Python installeert, word je mogelijk gevraagd of je de omgevingsvariabele `PATH` wilt bijwerken.

//// tab | Linux, macOS

Stel dat je Python installeert en het komt terecht in de map `/opt/custompython/bin`.

Als je kiest om de `PATH` omgevingsvariabele bij te werken, zal het installatieprogramma `/opt/custompython/bin` toevoegen aan de `PATH` omgevingsvariabele.

Dit zou er zo uit kunnen zien:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

Op deze manier zal het systeem, wanneer je `python` in de terminal typt, het Python-programma in `/opt/custompython/bin` (de laatste map) vinden en dat gebruiken.

////

//// tab | Windows

Stel dat je Python installeert en het komt terecht in de map `C:\opt\custompython\bin`.

Als je kiest om de `PATH` omgevingsvariabele bij te werken, zal het installatieprogramma `C:\opt\custompython\bin` toevoegen aan de `PATH` omgevingsvariabele.

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

Op deze manier zal het systeem, wanneer je `python` in de terminal typt, het Python-programma in `C:\opt\custompython\bin` (de laatste map) vinden en dat gebruiken.

////

Dus als je typt:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

Zal het systeem het `python`-programma in `/opt/custompython/bin` **vinden** en uitvoeren.

Het zou ongeveer hetzelfde zijn als het typen van:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

Zal het systeem het `python`-programma in `C:\opt\custompython\bin\python` **vinden** en uitvoeren.

Het zou ongeveer hetzelfde zijn als het typen van:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

Deze informatie is handig wanneer je meer wilt weten over [virtuele omgevingen](virtual-environments.md){.internal-link target=_blank}.

## Conclusion

Hiermee heb je basiskennis van wat **omgevingsvariabelen** zijn en hoe je ze in Python kunt gebruiken.

Je kunt er ook meer over lezen op de <a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia over omgevingsvariabelen</a>.

In veel gevallen is het niet direct duidelijk hoe omgevingsvariabelen nuttig zijn en hoe je ze moet toepassen. Maar ze blijven in veel verschillende scenario's opduiken als je aan het ontwikkelen bent, dus het is goed om er meer over te weten.

Je hebt deze informatie bijvoorbeeld nodig in de volgende sectie, over [Virtuele Omgevingen](virtual-environments.md).
