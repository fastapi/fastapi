# Egyidejűség és async / await

Részletek az *elérési út műveleti függvényei* `async def` szintaxisáról, valamint némi háttérinformáció az aszinkron kódról, egyidejűségről és a párhuzamosságról.

## Sietne?

<abbr title="túl hosszú; nem olvastam"><strong>TL;DR:</strong></abbr>

Ha olyan harmadik féltől származó könyvtárakat használ, amelyek azt mondják, hogy `await`-tel hívja meg őket, például:

``` Python
results = await some_library()
```

Akkor deklarálja az *elérési út műveleti függvényeit* az `async def` paraméterrel, úgy mint:

``` Python hl_lines="2"
@app.get('/')
async def read_results():
     results = await some_library()
     return results
```

!!! jegyzet
     Csak az `async def` paraméterrel létrehozott függvényeken belül használhatja az `await` kifejezést.
---

Ha olyan harmadik féltől származó könyvtárat használ, amely kommunikál valamivel (adatbázissal, API-val, fájlrendszerrel stb.), és nem támogatja a `await` használatát (jelenleg ez a helyet a legtöbb adatbázis-könyvtár esetében), akkor deklarálja az *elérési út műveleti függvényeit* a szokásos módon, csak `def`-el, például:

``` Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

Ha az alkalmazásnak (valahogy) nem kell mással kommunikálnia, és várnia kell a válaszra, használja az `async def` parancsot.

---

Ha nem tudja, használja a normál `def`-et.

---

**Megjegyzés**: A `def` és az `async def` függvényeket annyiszor keverheti az *elérési út műveleti függvényeiben*, amennyire szüksége van, és mindegyiket az Ön számára legmegfelelőbb beállítással határozhatja meg. A FastAPI a megfelelő dolgot fogja tenni velük.

Mindenesetre a fenti esetek bármelyikében a FastAPI továbbra is aszinkron módon működik, és rendkívül gyors.

A fenti lépések követésével azonban képes lesz néhány teljesítményoptimalizálásra.

## Műszaki információk

A Python modern verziói támogatják az **"aszinkron kódot"** a **"korutin"** néven, **`async` és `await`** szintaxissal.

Lássuk ezt a kifejezést részenként az alábbi szakaszokban:

* **Aszinkron kód**
* **`async` és `await`**
* **Korutinok**

## Aszinkron kód

Az aszinkron kód csak azt jelenti, hogy a nyelvnek 💬 megvan a módja annak, hogy elmondja a számítógépnek/programnak 🤖, hogy a kód egy pontján 🤖 várnia kell, amíg *valami más* befejeződik valahol máshol. Tegyük fel, hogy *valami mást* „lassú fájlnak” hívnak 📝.

Tehát ezalatt a számítógép mehet és végezhet más munkát, miközben a "lassú fájl" 📝 befejeződik.

Ekkor a számítógép/program 🤖 minden alkalommal visszatér, amikor van rá lehetősége, ugyanis még mindig vár, vagy amikor 🤖 befejezte az addig végzett munkáját. És 🤖 meglátja, hogy a várt feladatok közül valamelyik befejeződött-e már, megtéve azt, amit tennie kellett.

Ezután 🤖 befejezi az első feladatot (mondjuk a "lassú fájlunkat" 📝), és folytatja, amit tenni akart  vele.

A "várni valami mást" általában olyan <abbr title="Input és Output">I/O</abbr> műveletekre utal, amelyek viszonylag "lassúak" (a processzor és a RAM-memória sebességéhez képest), mint például a várakozás:

* a klienstől a hálózaton keresztül küldendő adatokra
* a program által küldött adatokra, amelyeket a kliens a hálózaton keresztül fogad
* a lemezen lévő fájl tartalmának rendszer általi beolvasnásaés és átadása a programnak
* a program által a rendszernek adott tartalom lemezre írására
* távoli API műveletre
* egy adatbázis-művelet befejezésére
* adatbázis lekérdezés eredményének visszaadásáre
* stb.

Mivel a végrehajtási időt leginkább az <abbr title="Input és Output">I/O</abbr> műveletekre való várakozás emészti fel, ezeket "I/O bound" műveleteknek nevezik.

"Aszinkron"-nak hívják, mert a számítógépnek/programnak nem kell "szinkronizálnia" a lassú feladattal, megvárva a pontos pillanatot, amikor a feladat befejeződik, miközben nem csinál semmit, hogy át tudja venni a feladat eredményét és folytatni tudja a munkát.

Ehelyett, mivel egy "aszinkron" rendszer, miután befejeződött, a feladat várhat egy kicsit (néhány mikroszekundumot) a sorban, amíg a számítógép/program befejezi, amit csinált, majd visszatér, hogy megkapja az eredményeket és folytassa velük a munkát.

A "szinkron" kifejezésre (ellentétben az "aszinkronnal") általában a "szekvenciális" kifejezést is használják, mivel a számítógép/program sorban követi az összes lépést, mielőtt másik feladatra váltana, még akkor is, ha ezek a lépések várakozással járnak.

### Egyidejűség és hamburgerek

Az **aszinkron** kód fentebb leírt ötletét néha **"egyidejűségnek"** is nevezik. Ez különbözik a **"párhuzamosságtól"**.

Az **egyidejűség** és a **párhuzamosság** egyaránt arra vonatkozik, hogy „különböző dolgok történnek többé-kevésbé egyszerre”.

De az *egyidejűség* és a *párhuzamosság* közötti részletek egészen eltérőek.

A különbség megtekintéséhez képzelje el a következő történetet a hamburgerekről:

### Egyidejű hamburgerek

A szerelmével elmegy egy gyorsétterembe, ahol sorban áll, miközben a pénztáros veszi a rendeléseket az Ön előtt lévőktől. 😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illusztráció">

Amikor Önön a sor, 2 darab nagyon elegáns hamburgert rendel a szerelmének és magának. 🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illusztráció">

A pénztáros mond valamit a szakácsnak a konyhában, hogy tudják, hogy el kell készíteniük a hamburgereket (bár éppen a korábbi ügyfeleknek készítik).

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illusztráció">

Ön fizet. 💸

A pénztáros kiadja a sorszámukat.

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illusztráció">

Amíg vár, elmegy a szerelmével és asztalt választ, hosszan ülnek és beszélgetnek egymással (mivel a hamburgerek nagyon finomak, és időbe telik az elkészítésük).

Miközben a szerelmével az asztalnál ülnek és a hamburgerekre várnak, azt az időt töltheti azzal, hogy csodálja, milyen fantasztikus, aranyos és okos a szerelme ✨😍✨.

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illusztráció">

Várakozás közben és a szerelmével beszélgetve időről időre megnézi a pulton megjelenő számot, hátha Önön van a sor.

Aztán egy ponton végre magán a sor. Odamegy a pulthoz, felveszi a hamburgereit és visszamegy az asztalhoz.

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illusztráció">

Ön és a szerelme megeszik a hamburgert, és jól érzik magukat. ✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illusztráció">

!!! info
     Gyönyörű illusztrációk <a href="https://www.instagram.com/ketrinadrawsalot" class="external-link" target="_blank">Ketrina Thompson-tól</a>. 🎨

---

Képzelje el, hogy Ön a számítógép/program 🤖 abban a történetben.

Amíg a sorban áll, csak tétlenkedik😴, várja a sorát, nem csinál semmi nagyon "produktívat". De gyors a sor, mert a pénztáros csak a rendeléseket veszi fel (nem készíti elő), így rendben van minden.

Aztán amikor önre kerül a sor, tényleges "produktív" munkát végez, feldolgozza az étlapot, eldönti, hogy mit szeretne, szerelme is eldönti, fizet, ellenőrzi, hogy a megfelelő számlát vagy kártyát adta-e be, ellenőrzi, hogy helyesen van-e felszámítva, ellenőrzi hogy a rendelésben a megfelelő tételek szerepelnek, stb.

De akkor, bár még mindig nincsenek meg a hamburgerei, a pénztárossal végzett munkája "szünetel" ⏸, mert várnia kell🕙, hogy elkészüljenek a hamburgerei.

De ahogy elmegy a pulttól és leül az asztalhoz egy számmal, amint sorra kerül, átkapcsolhatja 🔀 figyelmét a szerelmére, és azon "dolgozhat" ⏯ 🤓. Akkor megint valami nagyon "produktív" dolgot csinál, például flörtöl a szerelmével 😍.

Ekkor a pénztáros 💁 azt mondja: "Befejeztem a hamburger elkészítését" úgy, hogy felteszi a számát a pult kijelzőjére, de nem ugrik azonnal őrülten, amikor a kijelzett szám az Önére vált. Tudja, hogy senki nem fogja ellopni a hamburgereit, mert Önnek megvan a saját száma, másoknak pedig a sajátjuk.

Tehát megvárja, hogy szerelme befejezze a történetét (befejezze az aktuális munkát ⏯ / feldolgozás alatt lévő feladatot 🤓), mosolyog, és azt mondja, hogy megy a hamburgerért⏸.

Ezután odamegy a pulthoz 🔀, a most befejezett kezdő feladathoz ⏯, kiválasztja a hamburgereket, megköszöni és odaviszi az asztalhoz. Ezzel befejeződik a pulttal való interakció lépése/feladata ⏹. Ez viszont egy új feladatot teremt, a "hamburgerevést" 🔀 ⏯, de az előző, a "hamburger vásárlás" véget ért ⏹.

### Párhuzamos hamburgerek

Most képzeljük el, hogy ezek nem „egyidejű hamburgerek”, hanem „párhuzamos hamburgerek”.

A szerelmével párhuzamos gyorsétteremet keres.

Sorban áll, miközben több (mondjuk 8) pénztáros, egyben szakács is felveszi a rendeléseket az Ön előtt állóktól.

Mindenki Ön előtt várja, hogy elkészüljön a hamburgere, mielőtt elhagyja a pultot, mert a 8 pénztáros mindegyike elmegy, és azonnal elkészíti a hamburgert, mielőtt megkapja a következő rendelést.

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illusztráció">

Aztán végre Önön a sor, megrendel 2 nagyon finom hamburgert a szerelmének és magának.

Ön fizet 💸.

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illusztráció">

A pénztáros kimegy a konyhába.

A pult előtt állva vár 🕙, hogy senki más ne vegye el Ön elől a hamburgereiket, mivel nincs sorszám.

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illusztráció">

Mivel Ön és a szerelme azzal vannak elfoglalva, hogy senki ne álljon Önök elé, és ne vigye el a hamburgereiket, amikor megérkeznek, nem tud a szerelmére figyelni. 😞

Ez "szinkron" munka, "szinkronban" van a pénztárossal/szakácsnővel 👨‍🍳. Várnia kell 🕙 és pontosan abban a pillanatban ott lenni, amikor a pénztáros/szakács 👨‍🍳 elkészíti a hamburgert és odaadja, különben valaki más elviheti.

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illusztráció">

Aztán a pénztárosa/szakácsa 👨‍🍳 végre visszatér a hamburgereivel, hosszú várakozás után🕙 ott a pult előtt.

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illusztráció">

Fogja a hamburgereit, és odamegy az asztalhoz a szerelmével.

Csak megeszi őket, és kész. ⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

Nem sok beszéd, flört volt, mivel az idő nagy része várakozással telt 🕙 a pult előtt. 😞

!!! info
     Gyönyörű illusztrációk <a href="https://www.instagram.com/ketrinadrawsalot" class="external-link" target="_blank">Ketrina Thompson-tól</a>. 🎨

---

A párhuzamos hamburgerek ebben a forgatókönyvében Ön egy számítógép/program 🤖 két processzorral (ön és a szerelme), mindketten arra várnak 🕙 és arra szentelik a figyelmüket ⏯, hogy sokáig "várjanak a pultnál" 🕙.

A gyorsétteremben 8 db feldolgozó (pénztáros/szakács) működik. Míg a párhuzamos hamburgerboltban csak 2 lehetett (egy pénztáros és egy szakács).

De a végső élmény mégsem a legjobb. 😞

---

Ez lenne a párhuzamos ekvivalens történet a hamburgereknél. 🍔

Ennek „valódibb” példájához képzeljünk el egy bankot.

Egészen a közelmúltig a legtöbb bankban több pénztáros volt 👨‍💼👨‍💼👨‍💼👨‍💼 és egy nagy sor 🕙🕙🕙🕙🕙🕙🕙🕙.

A pénztárosok mindegyike egy-egy ügyféllel végzi a munkát 👨‍💼⏯.

És sokáig kell várni 🕙 a sorban, különben elveszik a sor.

Valószínűleg nem szeretné magával vinni a szerelmét 😍 a banki ügyek intézésére 🏦.

### Burger tapasztalatok

Ebben a „gyorséttermi hamburger a szerelmeddel” forgatókönyvben, mivel sok a várakozás 🕙, sokkal értelmesebb egy párhuzamos rendszer ⏸🔀⏯.

Ez a helyzet a legtöbb webalkalmazás esetében.

Sok-sok felhasználó a szervere vár 🕙 a nem túl jó kapcsolatára, hogy elküldje a kérését.

Aztán megint vár 🕙 a válaszokra.

Ez a "várakozás" 🕙 mikroszekundumban mérhető, de így is, mindent összegezve, sok várakozás a végén.

Éppen ezért nagyon ésszerű az aszinkron ⏸🔀⏯ kód használata webes API-khoz.

Ez a fajta aszinkronitás tette népszerűvé a NodeJS-t (bár a NodeJS nem párhuzamos), és ez a Go programozási nyelv erőssége.

És ez ugyanaz a teljesítményszint, mint a **FastAPI** használata.

És mivel párhuzamosságot és aszinkronitást is hasznélhat egyszerre, nagyobb teljesítményt érhet el, mint a legtöbb tesztelt NodeJS-keretrendszer, és egyenrangú a Go-val, amely egy olyan lefordított nyelv, amely közelebb áll a C-hez <a href="https://www.techempower .com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1" class="external-link" target="_blank">(mind a Starlette-nek köszönhetően)</a>.

### Jobb az egyidejűség, mint a párhuzamosság?

Dehogy! Nem ez a történet lényege.

Az egyidejűség más, mint a párhuzamosság. Ez jobb **specifikus** forgatókönyvek esetén, amelyek sok várakozással járnak. Emiatt általában sokkal jobb, mint a párhuzamosság a webalkalmazások fejlesztésében. De nem mindenre.

Tehát ennek kiegyensúlyozására képzeljük el a következő rövid történetet:

> Egy nagy, koszos házat kell kitakarítania.

*Igen, ez az egész történet*.

---

Nincs várakozás 🕙 sehol, csak sok a munka, a ház több pontján.

Lehetne egy sorozatban takarítani, mint a hamburgeres példában, először a nappali, aztán a konyha, de mivel nem vár 🕙 semmire, csak takarításra és takarításra, a sorrend semmit nem befolyásolna.

Ugyanannyi időbe telt volna a befejezés akármilyen sorrendben (egyidejűség), és ugyanannyi munkát végzett volna.

De ebben az esetben, ha elhozná a 8 volt-pénztárost/szakácsot/most-takarítót, és mindegyikük (plusz Ön is) a háznak csak egy részét takarítaná ki, akkor az összes munkát elvégezhetné **párhuzamosan**, egy kis extra segítséggel, és a munka sokkal hamarabb befejeződne.

Ebben a forgatókönyvben a takarítók mindegyike (beleértve Önt is) egy processzor lenne, aki elvégzi a feladatát.

És mivel a végrehajtási idő nagy részét a tényleges munka veszi el (várakozás helyett), és a számítógépben a munkát egy <abbr title="Central Processing Unit">CPU</abbr> végzi, ezeket a problémákat "CPU-kötött"-nek nevezik.

---

A CPU-kötött műveletek gyakori példái olyan dolgok, amelyek bonyolult matematikai feldolgozást igényelnek.

Például:

* **Hang** vagy **képfeldolgozás**.
* **Számítógépes látás**: egy kép több millió pixelből áll, minden képpontnak 3 értéke/színe van, a feldolgozás általában megköveteli, hogy ezeken a pixeleken egy időben számítsanak ki valamit.
* **Gépi tanulás**: általában sok "mátrix" és "vektor" szorzást igényel. Képzeljen el egy hatalmas táblázatot számokkal, és mindegyiket egyszerre szorozza össze.
* **Mély tanulás**: ez a gépi tanulás egyik alterülete, tehát ugyanez érvényes. Csak arról van szó, hogy nem egyetlen számtáblázatot kell szorozni, hanem egy hatalmas halmazt, és sok esetben speciális processzort kell használni a modellek felépítéséhez és/vagy használatához.

### Egyidejűség + párhuzamosság: web + gépi tanulás

A **FastAPI** segítségével kihasználhatja a párhuzamosság előnyeit, amely nagyon gyakori a webfejlesztésben (a NodeJS fő vonzereje).

De Ön is ki tudja használni a párhuzamosság és a több feldolgozás előnyeit (amikor több folyamat fut párhuzamosan) a **CPU-kötött** munkaterhelésekhez, mint amilenek a gépi tanulásban előfordulnak.

Ez, valamint az az egyszerű tény, hogy a Python a **Data Science**, a gépi tanulás és különösen a mély tanulás fő nyelve, a FastAPI nagyon jól illeszkedik a Data Science / gépi tanulás webes API-khoz és alkalmazásokhoz (sok egyéb mellett).

Ha meg szeretné tudni, hogyan érheti el ezt a párhuzamosságot az éles környezetben, tekintse meg a [Deployment](deployment/index.md){.internal-link target=_blank} című részt.

## `async` és `await`

A Python modern verziói nagyon intuitív módon határozzák meg az aszinkron kódot. Emiatt úgy néz ki, mint a normál „szekvenciális” kód, és a megfelelő pillanatokban elvégzi a „várakozást”.

Ha van egy művelet, amelynél várni kell az eredmények megadása előtt, és amely támogatja ezeket az új Python-szolgáltatásokat, a következőképpen kódolhatja:

``` Python
burgers = await get_burgers(2)
```

A kulcs itt az `await`. Azt mondja a Pythonnak, hogy várnia kell ⏸, amíg a `get_burgers(2)` befejezi a dolgát 🕙, mielőtt eltárolja az eredményeket a `burgers` változóban. Ezzel a Python tudni fogja, hogy elmehet és közben mást is csinálhat 🔀 ⏯ (például újabb kérést kaphat).

Ahhoz, hogy az `await` működjön, egy olyan függvényen belül kell lennie, amely támogatja ezt az aszinkronitást. Ehhez egyszerűen deklarálja az `async def` paranccsal:

``` Python hl_lines="1"
async def get_burgers(number: int):
     # Csináljon néhány aszinkron dolgot a hamburgerek elkészítéséhez
     return burgers
```

...a `def` helyett:

``` Python hl_lines="2"
# Ez nem aszinkron
def get_sequential_burgers(number: int):
     # Végezzen néhány szekvenciális dolgot a hamburgerek elkészítéséhez
     return burgers
```

Az `async def` használatával a Python tudja, hogy ezen a függvényen belül tisztában kell lennie a `await` kifejezésekkel, és hogy "szünetelheti" ⏸ a függvény végrehajtását, és valami mást csinálhat 🔀, mielőtt visszatérne.

Ha egy `async def` függvényt szeretne meghívni, akkor `await`-elnie is kell. Szóval ez nem fog működni:

``` Python
# Ez nem fog működni, mert a get_burgers a következővel lett meghatározva: async def
burgers = get_burgers(2)
```

---

Tehát, ha olyan könyvtárat használ, amely azt mondja, hogy meghívhatja a `await`-tel, akkor létre kell hoznia a *elérési út műveleti függvényeit*, amelyek az `async def` paraméterrel használják, például:

``` Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
     burgers = await get_burgers(2)
     return burgers
```

### További technikai részletek

Lehet, hogy észrevette, hogy az `await` csak az `async def` paraméterrel definiált függvényeken belül használható.

Ugyanakkor az `async def`-vel definiált függvényeket csak az `await` kulcsszóval lehet meghívni. Tehát az `async def` függvények csak az `async def` paraméterrel definiált függvényeken belül hívhatók meg.

Szóval, a tojással és a csirkével kapcsolatban hogyan hívják az első `async` függvényt?

Ha a **FastAPI-val** dolgozik, emiatt nem kell aggódnia, mert ez az „első” függvény a *elérési út műveleti függvénye* lesz, és a FastAPI tudni fogja, hogyan kell helyesen cselekedni.

De ha a FastAPI nélkül szeretné használni az `async` / `await` parancsot, akkor azt is megteheti.

### Írja meg saját aszinkron kódját

A Starlette (és a **FastAPI**) az <a href="https://anio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO-n</a> alapul, ami kompatibilissé teszi mindkét Python szabványos <a href="https://docs.python.org/3/library/asyncio-task.html" class="external-link" target="_blank">asyncio-könyvtárával </a> és <a href="https://trio.readthedocs.io/en/stable/" class="external-link" target="_blank">Trio-val</a> is.

Közvetlenül használhatja az <a href="https://anio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO-t</a> a haladó párhuzamos használathoz olyan esetekben, amelyek fejlettebb mintákat igényelnek az Ön saját kódjában.

És még ha nem is FastAPI-t használna, saját aszinkron alkalmazásait is írhatja <a href="https://anio.readthedocs.io/en/stable/" class="external-link" target="_blank" segítségével >AnyIO-val</a>, hogy nagymértékben kompatibilis legyen, és kihasználja annak előnyeit (pl. *strukturált egyidejűség*).

### Az aszinkron kód egyéb formái

Az `async` és a `await` használatának ez a stílusa viszonylag új a nyelvben.

De sokkal könnyebbé teszi az aszinkron kóddal való munkát.

Ugyanez a szintaxis (vagy majdnem azonos) nemrégiben a JavaScript modern verzióiba is bekerült (a böngészőben és a NodeJS-ben).

De előtte az aszinkron kód kezelése sokkal összetettebb és nehezebb volt.

A Python korábbi verzióiban végrehajtási szálakat vagy <a href="https://www.gevent.org/" class="external-link" target="_blank">Geventet</a> használhatott volna. De a kód megértése, debug-olása és átgondolása sokkal bonyolultabb volt.

A NodeJS / Browser JavaScript korábbi verzióiban "callback"-eket használta volna. Ez a <a href="http://callbackhell.com/" class="external-link" target="_blank">callback pokolhoz</a> vezetett.

## Korutinok

A **korutin** csak a nagyon divatos kifejezés az `async def` függvény által visszaadott dologra. A Python tudja, hogy ez valami olyan funkció, amelyre valamikor kezdődik, és valamikor véget ér, de előfordulhat, hogy belsőleg is szüneteltethető ⏸, amikor `await` van benne.

Az aszinkron kód használatát az `async` és a `await` kifejezésekkel sokszor "korutin"-ként foglalják össze. Hasonló szinten van a Go fő jellemzőjével, a "Goroutin"-nal.

## Következtetés

Nézzük a fenti mondatot még egyszer:

> A Python modern verziói támogatják az **"aszinkron kódot"** a **"korutin"** néven, **`async` és `await`** szintaxissal.

Ennek most már több értelme kellene, hogy legyen. ✨

Ez az ami a FastAPI-t támogatja (a Starlette-en keresztül), és ezért olyan lenyűgöző a teljesítménye.

## Nagyon technikai részletek

!!! Figyelem
     Ezt a részt valószínűleg kihagyhatod.

     Ezek nagyon technikai részletek a **FastAPI** működéséről.

     Ha van némi technikai tudása (társrutinok, végrehajtási szálak, blokkolások stb.), és kíváncsi arra, hogy a FastAPI hogyan kezeli az `async def` és a normál `def` értékeket, akkor folytassa az olvasást.

### Útvonal műveleti funkciók

Ha az `async def` helyett normál `def`-vel deklarálunk egy *elérési út műveleti függvényei*, akkor az egy külső szálkészletben fut, amelyet ezután "await"-eltet, ahelyett, hogy közvetlenül meghívnák (mivel blokkolná a szervert).

Ha Ön egy másik aszinkron keretrendszerből érkezik, amely nem a fent leírt módon működik, és hozzászokott ahhoz, hogy triviális, csak számítási *elérési út műveleti függvényeket* definiál sima `def`-fel, kis teljesítménynövekedés érdekében (körülbelül 100 nanoszekundum), kérjük, vegye figyelembe, hogy a **FastAPI**-ban a hatás teljesen ellentétes lenne. Ezekben az esetekben jobb az `async def` használata, kivéve, ha az *elérési út műveleti függvényei* olyan kódot használnak, amely blokkolja a <abbr title="Input/Output: lemez olvasása vagy írása, hálózati kommunikáció.">I/O-t</abbr>.

Ennek ellenére mindkét helyzetben valószínű, hogy a **FastAPI** [továbbra is gyorsabb](/#performance){.internal-link target=_blank} lesz, mint (vagy legalábbis összehasonlítható) az előző keretrendszer.

### Függőségek

Ugyanez vonatkozik a [függőségekre](/tutorial/dependencies/index.md){.internal-link target=_blank}. Ha egy függőség egy szabványos `def` függvény az `async def` helyett, akkor a külső szálkészletben fut.

### Részfüggőségek

Több függősége és [részfüggősége](/tutorial/dependencies/sub-dependencies.md){.internal-link target=_blank} lehet (a függvénydefiníciók paramétereiként), ezek közül néhányat létrehozhat `async def`-fel és néhány normál `def`-fel. Továbbra is működne, és a normál `def`-el létrehozottakat külső szálon hívnák meg (a szálkészletből), ahelyett, hogy "await"-elnék.

### Egyéb segédfunkciók

Bármely más, közvetlenül meghívott segédfunkció létrehozható normál `def` vagy `async def` paraméterrel, és a FastAPI nem befolyásolja a hívás módját.

Ez ellentétben áll azokkal a függvényekkel, amelyeket a FastAPI hív meg: *elérési út műveleti függvények* és függőségek.

Ha a segédprogram egy normál függvény `def`-el, akkor közvetlenül (ahogyan beírod a kódodba) hívódik meg, nem pedig egy szálkészletben, ha a függvény az `async def`-el van létrehozva, akkor `await`-elni kell a függvényt, amikor meghívja a kódjában.

---

Megint csak, ezek nagyon technikai részletek, amelyek valószínűleg hasznosak lennének, ha ezek után kutatna.

Ellenkező esetben a fenti szakasz irányelvei bőben elegek: <a href="#Sietne">Sietne?</a>.