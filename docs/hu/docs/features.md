# Funkciók

## FastAPI funkciók

**FastAPI** a következőket nyújtja:

### Nyílt szabványok alapján

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> az API fejlesztéshez, ebbe beletartozik az <abbr title="más néven végpontok, utak">útvonal</abbr> <abbr title="más néven HTTP parancsok, úgymint POST, GET, PUT, DELETE">műveletek</abbr>, paraméterek, "test" lekérések, biztonság, stb. deklarálása
* Automatikus adat modell dokumentáció <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a>-val (mivel az OpenAPI maga is JSON Schema-n alapul).
* A fejlesztés ezen szabványokat fejben tartva történt, aprólékos tanulmányt követve, nem csak egy utógondolatként rápakolva egy rétegként.
* Ez automatikus **kliens kód generálást** is engedélyez számos programozási nyelvben.

### Automatikus documentáció

Interaktív API dokumentáció és webes felhasználói felület. Mivelhogy a keretrendszer az OpenAPI-on alapul, több lehetőség is van, ezek közül 2 alapból elérhető.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, interaktív felfedezéssel, hívd meg és teszteld az API-odat közvetlenül a böngésződből.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Alternatív API dokumentáció <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>-kal.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Csupán Modern Python

Minden a standard **Python 3.6 típus** deklarációkon alapul (Pydantic-nak köszönhetően). Nem kell új szintaxist megtanulni. Csakis standard modern Python.

Ha szükséged van egy 2 perces frissítőre a Python típusokról (még akkor is, ha em használod a FastAPI-t), nézd meg a rövid oktató videót: [Python Típusok](python-types.md){.internal-link target=_blank}.

Standard Python kód típusokkal:

```Python
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Amit aztán így lehet használni:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! info
    `**second_user_data` jelentése:

    Átadod a `second_user_data` szótár kulcsait és a hozzájuk tartozó értékeket közvetlenül mint kulcs-érték paramétereket , a fenti kóddal ekvivalens: `User(id=4, name="Mary", joined="2018-11-30")`

### Kódszerkesztés segítség

A keretsrendszer úgy lett felépítve, hogy könnyű és egyértelmű legyen használni, minden egyes döntés számos fejlesztői környezetben le lett tesztelve még a fejlesztés előtt, hogy a legjobb fejlesztői élményt nyújtsa.

A legutóbbi Python fejlesztői kutatásban látszott, <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">hogy a legtöbbet használt funkció az "automatikus kitöltés" volt</a>.

Az egész **FastAPI** keretrendszer azon alapul, hogy ezt az igényt kielégítse. Az automatikus kitöltés működik mindenhol.

Nagyon ritkán kell majd csak visszajönnöd a dokumentációhoz.

A fejlesztői környezeted így tud neked segíteni:

*<a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>-ban:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

*<a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>-ban:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Olyan kódot is ki tud egészíteni, amire nem is gondoltál volna. Pl. a `price` kulcsot a JSON "test"-ben (ami akár beágyazva is lehetne) ami a kérésből jön.

Nincs többé elírt kulcsnév, ugrálás dokumentációk között, vagy görgetés fel és le, hogy vajon `username`-et vagy `user_name`-et kell használni.

### Rövid

Magától érthetődő **alapbeállítások** mindenhol, de opcionális változtatások elérhetők akárhol. Az összes paramétert finomhangolatod aszerint, hogy mire van szükséged, és hogy az API-nak mire van szüksége.

De alapból minden **"csak működik, és kész"**.

### Érvényesítés

* Érvényesítés majdnem mindegyik (vagy az összes?) Python **adattípusra**, többek között:
    * JSON objektumok (`dict`).
    * JSON tömb (`list`) definiáló tárgytípusok.
    * Szöveg (`str`) mezők, minimális és maximális hosszak megadása.
    * Számok (`int`, `float`) minimális és maximális hosszak megadásával, stb.

* Érvényesítés egzotikusabb típusra, például:
    * Link(URL).
    * Email.
    * Globálisan egyedi azonosító (UUID).
    * ...és még sok más.

Az összes érvényesítés a **Pydantic** segítségével történik.

### Biztonság és azonosítás

Biztonság és azonosítás integrálva. Kompromisszumok nélkül az adatbázisokkal vagy adatmodellekkel.

Az OpenAPI-ban meghatározott összes biztonsági séma, beleértve:

* HTTP Basic.
* **OAuth2** (**JWT tokenekkel** is). Tekintse meg az [OAuth2 with JWT] (tutorial/security/oauth2-jwt.md){.internal-link target=_blank} oktatóanyagát.
* API kulcsok:
     * Fejlécek.
     * Paraméterek lekérdezése.
     * Cookie-k stb.

Plusz a Starlette összes biztonsági funkciója (beleértve a **session cookie-kat**).

Mindegyik újrafelhasználható eszközként és komponensként készült, amelyek könnyen integrálhatók a rendszerekkel, adattárolókkal, relációs és NoSQL adatbázisokkal stb.

### Függőség Injekció

A FastAPI egy rendkívül könnyen használható, de rendkívül hatékony <abbr title='más néven "összetevők", "erőforrások", "szolgáltatások", "szolgáltatók"'><strong>függőség-injekció</strong></abbr> rendszert tartalmaz.

* Még a függőségeknek is lehetnek függőségei, létrehozva a függőségek hierarchiáját vagy **"grafikonját"**.
* Mindent **automatikusan kezel** a keretrendszer.
* Minden függőség igényelhet adatokat a kérésekből, és **kibővítheti az útvonalművelet** megszorítását és az automatikus dokumentációt.
* **Automatikus érvényesítés** még a függőségekben meghatározott *elérési út* paramétereknél is.
* Komplex felhasználói hitelesítési rendszerek támogatása, **adatbázis-kapcsolatok** stb.
* **Nincs kompromisszum** adatbázisokkal, frontendekkel stb. De mindegyikkel könnyen integrálható.

### Korlátlan "bővítmények"

Vagy más módon, nincs szükség rájuk, importálja és használja a szükséges kódot.

Minden integrációt úgy terveztek meg, hogy olyan egyszerűen használható legyen (függőségekkel), hogy létrehozhat egy „beépülő modult” az alkalmazásához 2 kódsorból, ugyanazzal a struktúrával és szintaxissal, mint az *elérési út műveleteinél*.

### Tesztelve

* 100% <abbr title="Az automatikusan tesztelt kód mennyisége">tesztlefedettség</abbr>.
* 100%-ban <abbr title="Python típusú megjegyzések, ezzel a szerkesztője és a külső eszközei jobb támogatást nyújtanak a">jegyzett</abbr> kódbázishoz.
* Gyártási alkalmazásokban használják.

## A Starlette jellemzői

A **FastAPI** teljes mértékben kompatibilis a <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong>-tel (és azon alapul) </a>. Tehát minden további Starlette kód is működni fog.

A „FastAPI” valójában a „Starlette” alosztálya. Tehát, ha már ismeri vagy használja a Starlette-et, a legtöbb funkció ugyanúgy fog működni.

A **FastAPI** segítségével megkapja a **Starlette** összes funkcióját (mivel a FastAPI csak Starlette szteroidokon):

* Komolyan lenyűgöző teljesítmény. Ez <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">az egyik leggyorsabb Python-keretrendszer, amely egyenrangú a **NodeJS-szel** és **Go-val**</a>.
* **WebSocket** támogatás.
* Folyamat közbeni háttérfeladatok.
* Indítási és leállítási események.
* HTTPX-re épülő tesztkliens.
* **CORS**, GZip, statikus fájlok, streaming válaszok.
* **Session és Cookie** támogatás.
* 100%-os tesztlefedettség.
* 100%-os típusú megjegyzésekkel ellátott kódbázis.

## Pydantic funkciók

A **FastAPI** teljes mértékben kompatibilis <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic-kal</strong></a>, sőt, azon alapul. Tehát minden további Pydantic kód is működni fog.

Beleértve a Pydantic alapú külső könyvtárakat is, mint <abbr title="Object-Relational Mapper">ORM</abbr>, <abbr title="Object-Document Mapper">ODM</abbr> adatbázisokhoz.

Ez azt is jelenti, hogy sok esetben ugyanazt az objektumot, amit egy kérésből kapunk, **közvetlenül az adatbázisnak** továbbíthatjuk, mivel minden automatikusan érvényesítésre kerül.

Ugyanez fordítva is érvényes, sok esetben az adatbázisból kapott objektumot **közvetlenül a kliensnek** adhatod át.

A **FastAPI** segítségével megkapja a **Pydantic** összes funkcióját (mivel a FastAPI a Pydanticon alapul az összes adatkezeléshez):

**Nincs agyafúrás**:
     * Nincs új megtanulni való sémadefiníciós mikronyelv.
     * Ha ismeri a Python típusokat, tudja, hogyan kell használni a Pydantic-ot.
* Szépen kapcsolódik az **<abbr title="Integrated Development Environment, hasonló a kódszerkesztőhöz">IDE</abbr>/<abbr title="A program, amely ellenőrzi a kódhibákat">linter</abbr>/brain **-hez:
     * Mivel a pydantikus adatstruktúrák csak az Ön által meghatározott osztályok példányai; Az automatikus kiegészítésnek, a lintingnek, a mypy-nek és az intuíciónak mind megfelelően működnie kell az ellenőrzött adatokkal.
* Érvényesítsen **összetett struktúrákat**:
     * Hierarchikus Pydantic modellek, Python "gépelés" listák és szótárak stb. használata.
     * Az érvényesítők pedig lehetővé teszik az összetett adatsémák egyértelműen és egyszerűen definiálását, ellenőrzését és JSON-sémaként dokumentálását.
     * Mélyen **beágyazott JSON** objektumokkal rendelkezhet, és mindegyiket ellenőrizheti és megjegyzésekkel látja el.
**Bővíthető**:
     * A Pydantic lehetővé teszi egyéni adattípusok meghatározását, vagy kiterjesztheti az érvényesítést módszerekkel a validátor dekorátorral díszített modelleken.
* 100%-os tesztlefedettség.
