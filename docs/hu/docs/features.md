# Funkciók

## FastAPI funkciók

A **FastAPI** a következőket nyújtja:

### Nyílt szabványokon alapul

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> API létrehozásához, beleértve <abbr title="más néven: endpoints, routes">útvonal</abbr> <abbr title="más néven HTTP metódusok, mint POST, GET, PUT, DELETE">műveletek</abbr>, paraméterek, test kérések, biztonság stb.
* Automatikus adatmodell-dokumentáció a <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON-sémával</strong></a> (mint Maga az OpenAPI a JSON-sémán alapul).
* Ezen szabványok köré tervezve, alapos tanulmányozás után. Utólagos réteg helyett a tetején.
* Ez számos nyelven lehetővé teszi az automatikus **klienskód-generálás** használatát is.

### Automatikus dokumentumok

Interaktív API dokumentációs és felfedező webes felhasználói felületek. Mivel a keretrendszer OpenAPI-n alapul, több lehetőség is létezik, amelyek közül 2 alapértelmezés szerint benne van.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, interaktív felfedezés, hívja és tesztelje API-ját közvetlenül a böngészőből.

![Swagger UI interakció](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Alternatív API dokumentáció a <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a> segítségével.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Csak Modern Python

Mindez szabványos **Python 3.6 típusú** deklarációkon alapul (hála a Pydantic-nek). Nincs új megtanulandó szintaxis. Csak szabványos modern Python.

Ha 2 perces felfrissítésre van szüksége a Python-típusok használatáról (még ha nem is használja a FastAPI-t), tekintse meg a rövid oktatóanyagot: [Python Types](python-types.md){.internal-link target=_blank}.

A szabványos Python típusokat írod:

``` Python
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

Ezt így lehet használni:

``` Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! info
     A "**második_felhasználói adatok" jelentése:

     Közvetlenül adja át a `second_user_data` szótár kulcsait és értékeit kulcs-érték argumentumként, ami egyenértékű a következővel: `User(id=4, name="Mary", joined="2018-11-30")`

### Szerkesztő támogatás

Az összes keretrendszert úgy tervezték meg, hogy könnyen és intuitívan használható legyen, minden döntést több szerkesztőn is teszteltek még a fejlesztés megkezdése előtt, hogy a legjobb fejlesztési élményt biztosítsák.

A legutóbbi Python fejlesztői felmérésben egyértelmű volt, <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target= "_blank">hogy a leggyakrabban használt funkció az "automatikus kiegészítés"</a>.

A teljes **FastAPI** keretrendszer ennek kielégítésére épül. Az automatikus kiegészítés mindenhol működik.

Ritkán kell visszamennie a dokihoz.

A szerkesztője a következőképpen segíthet Önnek:

* <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code-ban</a>:

![szerkesztő támogatása](https://fastapi.tiangolo.com/img/vscode-completion.png)

* <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharmban</a>:

![szerkesztő támogatása](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Olyan kódot kapsz, amelyet korábban lehetetlennek tartottál. Például a „price” kulcs egy JSON-törzsben (amely lehet beágyazott), amely egy kérelemből származik.

Nem kell többé rossz kulcsneveket begépelnie, oda-vissza lépkedni a dokumentumok között, vagy fel-le görgetni, hogy megtudja, hogy végre használta-e a "felhasználónév" vagy a "felhasználónév" értéket.

### Rövid

Mindenhez ésszerű **alapbeállításai** vannak, mindenhol választható konfigurációkkal. Az összes paraméter finomhangolható, hogy azt tegye, amire szüksége van, és amire az API-nak szüksége van.

De alapértelmezés szerint mindez **"csak működik"**.

### Érvényesítés

* Érvényesítés a legtöbb (vagy az összes?) Python **adattípushoz**, beleértve:
     * JSON objektumok (`dict`).
     * JSON-tömb (`lista`), amely elemtípusokat határoz meg.
     * String (`str`) mezők, amelyek meghatározzák a minimális és maximális hosszúságot.
     * Számok ('int', 'float') min és max értékekkel stb.

* Érvényesítés az egzotikusabb típusokhoz, mint például:
     * URL.
     * E-mail.
     * UUID.
     * ...és mások.

Az összes érvényesítést a jól bevált és robusztus **Pydantic** kezeli.

### Biztonság és hitelesítés

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
