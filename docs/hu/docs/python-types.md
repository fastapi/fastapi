# Python Típusok Bevezető

A Python támogatja az opcionális "típustippeket" (más néven "típusjegyzeteket").

Ezek a **"típustippek"** vagy annotációk egy speciális szintaxis, amely lehetővé teszi egy változó <abbr title="például: str, int, float, bool">típusának</abbr> deklarálását.

A változók típusainak deklarálásával a szerkesztők és eszközök jobb támogatást nyújthatnak.

Ez csak egy **gyors útmutató/frissítő** a Python típustippekről. Csak a **FastAPI** használatához szükséges minimumot fedi le... ami valójában nagyon kevés.

A **FastAPI** mind ezeken a típustippeken alapul, amelyek számos előnnyel járnak.

De még ha soha nem is használja a **FastAPI-t**, akkor is előnyös lenne, ha tanulna róluk egy kicsit.

!!! jegyzet
     Ha Ön már mindent tud a típustippekről, ugorjon a következő fejezetre.

## Motiváció

Kezdjük egy egyszerű példával:

``` Python
{!../../../docs_src/python_types/tutorial001.py!}
```

A program meghívásának kimenete:

```
John Doe
```

A függvény a következőket teszi:

* Veszi a `first_name`-et és a `last_name`-et.
* Mindegyik első betűjét nagybetűvé alakítja a `title()`-lel.
* <abbr title="Egybe rakja őket. Egymás után a tartalommal.">Összefűzi</abbr> őket egy szóközzel a közepén.

``` Python hl_lines="2"
{!../../../docs_src/python_types/tutorial001.py!}
```

### Szerkesse

Ez egy nagyon egyszerű program.

De most képzelje el, hogy a semmiből írja.

Egy ponton elkezdte volna a függvény definícióját, készen voltak a paraméterek...

De akkor meg kell hívnia "azt a módszert, amely az első betűt nagybetűvé alakítja".

`upper` volt? Vagy `uppercase`? `first_uppercase`? `capitalize`?

Ezután próbálkozik egy idős programozó barátjával, a szerkesztő automatikus kiegészítésével.

Be kell írnia a függvény első paraméterét, a `first_name`-et, majd egy pontot (`.`), majd megnyomja a `Ctrl+Szóköz` billentyűt a befejezés elindításához.

De sajnos semmi hasznosat nem kap:

<img src="/img/python-types/image01.png">

### Típusok hozzáadása

Módosítsunk egyetlen sort az előző verzióhoz képest.

Pontosan ezt a töredéket, a függvény paramétereit változtatjuk meg ebből:

``` Python
     first_name, last_name
```

arra, hogy:

``` Python
     first_name: str, first_name: str
```

Ez az.

Ezek a "típustippek":

``` Python hl_lines="1"
{!../../../docs_src/python_types/tutorial002.py!}
```

Ez nem ugyanaz, mint az alapértelmezett értékek deklarálása, mint például:

``` Python
     first_name="john", last_name="doe"
```

Ez két különböző dolog.

Kettőspontokat (`:`) használunk, nem egyenlőségjelet (`=`).

A típustippek hozzáadása általában nem változtatja meg azt, ami történik, mint ami nélkülük történne.

De most képzelje el, hogy ismét a függvény létrehozásának kellős közepén van, de típusjelekkel.

Ugyanazon a ponton megpróbálja elindítani az automatikus kiegészítést a `Ctrl+Szóköz` billentyűkombinációval, és ezt látja:

<img src="/img/python-types/image02.png">

Ezzel a lehetőségeket látva görgethet, amíg meg nem találja azt, amelyik már ismerős:

<img src="/img/python-types/image03.png">

## Több motiváció

Nézze meg ezt a függvény, ennek már vannak típus tippjei:

``` Python hl_lines="1"
{!../../../docs_src/python_types/tutorial003.py!}
```

Mivel a szerkesztő ismeri a változók típusát, nem csak kódkiegészítést kap, hanem hibaellenőrzést is:

<img src="/img/python-types/image04.png">

Most már tudja, hogy ki kell javítana, alakítsa át az `age` változót `str(age)` karakterláncra:

``` Python hl_lines="2"
{!../../../docs_src/python_types/tutorial004.py!}
```

## Típusok deklarálása

Épp most látta a fő helyet a típustippek deklarálásához. Függvényparaméterként.

Ez egyben a fő hely, ahol ezeket a **FastAPI**-val használja.

### Egyszerű típusok

Az összes szabványos Python típust deklarálhatja, nem csak az str.

Használhat például:

* `int`
* `float`
* `bool`
* `byte`

``` Python hl_lines="1"
{!../../../docs_src/python_types/tutorial005.py!}
```

### Általános típusok típusparaméterekkel

Vannak olyan adatstruktúrák, amelyek más értékeket is tartalmazhatnak, mint például a `dict`, `list`, `set` és `tuple`. És a belső értékeknek is lehet saját típusuk.

Ezeket a belső típusokkal rendelkező típusokat "**általános**" típusoknak nevezzük. És lehet deklarálni őket, akár belső típusaikkal együtt is.

A típusok és a belső típusok deklarálásához használhatja a szabványos Python `typing` modult. Kifejezetten az ilyen típustippek támogatására létezik.

#### A Python újabb verziói

A `typing`-et használó szintaxis **kompatibilis** az összes verzióval, a Python 3.6-tól a legújabb verziókig, beleértve a Python 3.9-et, Python 3.10-et stb.

Ahogy a Python fejlődik, az **újabb verziók** továbbfejlesztett támogatást nyújtanak ezekhez a típusjegyzetekhez, és sok esetben nem is kell importálnia és használnia a `typing` modult a típusjegyzetek deklarálásához.

Ha használhat a Python egy újabb verzióját a projekthez, akkor ezt az extra egyszerűséget kihasználhatja.

Az összes dokumentumban találhatók a Python egyes verzióival kompatibilis példák (ha van különbség).

Például a „**Python 3.6+**” azt jelenti, hogy kompatibilis a Python 3.6 vagy újabb verzióival (beleértve a 3.7, 3.8, 3.9, 3.10, stb.) A „**Python 3.9+**” pedig azt jelenti, hogy kompatibilis a Python 3.9 vagy újabb verziójával (beleértve a 3.10-et stb.).

Ha használhatja a **a Python legújabb verzióit**, használja a példákat a legújabb verzióhoz, ezeknek lesz a **legjobb és legegyszerűbb szintaxisa**, például „**Python 3.10+**”.

#### Lista

Például definiáljunk egy változót úgy, hogy az az `str` "listája" legyen.

=== "Python 3.9+"

     Deklarálja a változót ugyanazzal a kettőspont (`:`) szintaxissal.

     Típusként írja be a `list` szót.

     Mivel a lista néhány belső típust tartalmaz, ezeket szögletes zárójelbe kell tenni:

     ``` Python hl_lines="1"
     {!> ../../../docs_src/python_types/tutorial006_py39.py!}
     ```

=== "Python 3.6+"

     From `typing` import `List` (nagy `L` betűvel):

     ``` Python hl_lines="1"
     {!> ../../../docs_src/python_types/tutorial006.py!}
     ```

     Deklarálja a változót ugyanazzal a kettőspont (`:`) szintaxissal.

     Típusként adja meg azt a `List`-át, amelyet a `typing`-ból importált.

     Mivel a lista néhány belső típust tartalmaz, ezeket szögletes zárójelbe kell tenni:

     ``` Python hl_lines="4"
     {!> ../../../docs_src/python_types/tutorial006.py!}
     ```

!!! info
     A szögletes zárójelben lévő belső típusokat "típusparamétereknek" nevezzük.

     Ebben az esetben az `str` a `List`-nek (vagy a Python 3.9-es és újabb verzióiban a `list`-nek) átadott típusparaméter.

Ez azt jelenti, hogy az `items` változó egy `list`, és ebben a listában minden elem egy `str`.

!!! tipp
     Ha Python 3.9-et vagy újabb verziót használ, akkor nem kell importálnia a `List`-et a `typing`-ból, helyette használhatja ugyanazt a szokásos `list` típust.

Ezzel a szerkesztője még a lista elemeinek feldolgozása közben is támogatást nyújthat:

<img src="/img/python-types/image05.png">

Típusok nélkül ezt szinte lehetetlen elérni.

Figyelje meg, hogy az `item` változó az `items` lista egyik eleme.

És mégis, a szerkesztő tudja, hogy ez egy `str`, és ehhez támogatást nyújt.

#### Tuple és halmaz

Ugyanezt tennéd, ha `tuple`-t és halmazt (`set`-et) deklarálnál:

=== "Python 3.9+"

     ``` Python hl_lines="1"
     {!> ../../../docs_src/python_types/tutorial007_py39.py!}
     ```

=== "Python 3.6+"

     ``` Python hl_lines="1 4"
     {!> ../../../docs_src/python_types/tutorial007.py!}
     ```

Ez azt jelenti, hogy:

* Az `items_t` változó egy `tuple`, amely 3 elemből áll, egy `int`, egy másik `int` és egy `str`.
* Az `items_s` változó egy `set`, és minden eleme `bytes` típusú.

#### Szótár

A `dict` (szótár) meghatározásához 2 típusú paramétert kell átadni, vesszővel elválasztva.

Az első típusú paraméter a `dict` kulcsaira vonatkozik.

A második típusú paraméter a `dict` értékeire vonatkozik:

=== "Python 3.9+"

     ``` Python hl_lines="1"
     {!> ../../../docs_src/python_types/tutorial008_py39.py!}
     ```

=== "Python 3.6+"

     ``` Python hl_lines="1 4"
     {!> ../../../docs_src/python_types/tutorial008.py!}
     ```

Ez azt jelenti, hogy:

* A `prices` változó egy `dict`:
     * A `dict` kulcsai `str` típusúak (mondjuk az egyes elemek neve).
     * A `dict` értékei `float` típusúak (tegyük fel, hogy az egyes cikkek ára).

#### Unió

Deklarálhatja, hogy egy változó **többféle** lehet, például egy `int` vagy egy `str`.

A Python 3.6 és újabb verzióiban (beleértve a Python 3.10-et is) használhatja az `Union` típust a `typing` modulból, és szögletes zárójelbe teheti az elfogadandó típusokat.

A Python 3.10-ben van egy **új szintaxis** is, ahol a lehetséges típusokat elválaszthatja egy <abbr title='más néven "bitenkénti vagy operátor"-ral, de ez a jelentés nem releváns'>függőleges sáv (`|` )</abbr>.

=== "Python 3.10+"

     ``` Python hl_lines="1"
     {!> ../../../docs_src/python_types/tutorial008b_py310.py!}
     ```

=== "Python 3.6+"

     ``` Python hl_lines="1 4"
     {!> ../../../docs_src/python_types/tutorial008b.py!}
     ```

Ez mindkét esetben azt jelenti, hogy az `item` lehet `int` vagy `str`.

#### Esetleg `None`.

Deklarálhatja, hogy egy értéknek lehet egy típusa, például az `str`, de lehet `None` is.

A Python 3.6-os és újabb verzióiban (beleértve a Python 3.10-et is) deklarálhatja és használhatja az `Optional` importálásával a `typing` modulból.

``` Python hl_lines="1 4"
{!../../../docs_src/python_types/tutorial009.py!}
```

Az `Optional[str]` használata az `str` helyett lehetővé teszi, hogy a szerkesztő segít felismerni azokat a hibákat, ahol feltételezhető, hogy egy érték mindig `str`, holott valójában az is lehet, hogy `None`.

Az `Optional[Something]` valójában az `Union[Something, None]` lerövidítése, ezek egyenértékűek.

Ez azt is jelenti, hogy a Python 3.10-ben használhatja a `Something | None` kifejezést:

=== "Python 3.10+"

     ``` Python hl_lines="1"
     {!> ../../../docs_src/python_types/tutorial009_py310.py!}
     ```

=== "Python 3.6+"

     ``` Python hl_lines="1 4"
     {!> ../../../docs_src/python_types/tutorial009.py!}
     ```

=== "Python 3.6+ alternatíva"

     ``` Python hl_lines="1 4"
     {!> ../../../docs_src/python_types/tutorial009b.py!}
     ```

#### Az `Union` vagy az `Optional` használata

Ha 3.10-nél régebbi Python-verziót használ, itt van a tipp az én nagyon **szubjektív** nézőpontomból:

* 🚨 Kerülje az `Optional[SomeType]` használatát
* Ehelyett ✨ **használja az `Union[SomeType, None]`** ✨ lehetőséget.

Mindkettő ekvivalens, és ugyanazt éri el, de én az `Union` szót javaslom az `Optional` helyett, mert a "**opcionális**" szó azt sugallja, hogy az érték nem kötelező, viszont valójában azt jelenti, hogy "lehet `None` is", akkor is ha a típus megadása kötelező.

Úgy gondolom, hogy az `Union[SomeType, None]` egyértelműbb a jelentéséről.

Ez csak a szavakról és a nevekről szól. De ezek a szavak befolyásolhatják, hogy Ön és csapattársai hogyan gondolkodnak a kódról.

Példaként vegyük ezt a függvényt:

``` Python hl_lines="1 4"
{!../../../docs_src/python_types/tutorial009c.py!}
```

A `name` paraméter `Optional[str]`-ként van definiálva, de **nem opcionális**, a függvény nem hívható meg a paraméter nélkül:

``` Python
say_hi() # Ó, nem, ez hibát okoz! 😱
```

A `name` paraméter **továbbra is kötelező** (nem *opcionális*), mert nincs alapértelmezett értéke. Ennek ellenére a `name` elfogadja a `None` értéket:

``` Python
say_hi(name=None) # Ez működik, None egy érvényes típus🎉
```

A jó hír az, hogy ha már a Python 3.10-et használja, nem kell aggódnia emiatt, mivel egyszerűen használhatja a `|`-t a típusok unióinak meghatározásához:

``` Python hl_lines="1 4"
{!../../../docs_src/python_types/tutorial009c_py310.py!}
```

És akkor nem kell aggódnia az olyan nevek miatt, mint az `Optional` és az `Union`. 😎

#### Általános típusok

Az ilyen típusú paramétereket szögletes zárójelben **Általános típusoknak** vagy **Általánosoknak** nevezzük, például:

=== "Python 3.10+"

     Ugyanazokat a beépített típusokat használhatja általános típusként (szögletes zárójelekkel és típusokkal):

     * `list`
     * `tuple`.
     * `set`
     * `dict`

     És ugyanaz, mint a Python 3.6-nál, a `typing` modulból:

     * `Union`.
     * `Optional` (ugyanaz, mint a Python 3.6-nál)
     * ...és mások.

     A Python 3.10-ben az `Union` és az `Optional` általános kifejezések alternatívájaként használhatja a <abbr title='más néven "bitenkénti vagy operátor"-t, de ez a jelentés itt nem releváns'>függőleges sáv (`|`)</abbr> típusok uniójának deklarálásához, az sokkal jobb és egyszerűbb.

=== "Python 3.9+"

     Ugyanazokat a beépített típusokat használhatja általános típusként (szögletes zárójelekkel és típusokkal):

     * `lista`
     * `tuple`.
     * `set`
     * `dict`

     És ugyanaz, mint a Python 3.6-nál, a `typing` modulból:

     * `Union`.
     * `Optional`.
     * ...és mások.

=== "Python 3.6+"

     * `List`.
     * `Tuple`.
     * `Set`.
     * `Dict`.
     * `Union`.
     * `Optional`.
     * ...és mások.

### Osztályok mint típus

Egy osztályt is deklarálhat a változó típusaként.

Tegyük fel, hogy van egy `Person` osztálya, akinek egy neve van:

``` Python hl_lines="1-3"
{!../../../docs_src/python_types/tutorial010.py!}
```

Ezután deklarálhat egy változót `Person` típusúnak:

``` Python hl_lines="6"
{!../../../docs_src/python_types/tutorial010.py!}
```

És akkor ismét megkapja az összes szerkesztő támogatást:

<img src="/img/python-types/image06.png">

Figyeld meg, hogy ez azt jelenti, hogy "a `one_person` a `Person` osztály **példánya**".

Ez nem azt jelenti, hogy "a `one_person` a `Person` nevű **osztály**".

## Pydantikus modellek

A <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> egy Python-könyvtár adatok ellenőrzésére.

Az adatok "alakját" attribútumokkal rendelkező osztályokként deklarálod.

És minden attribútumnak van típusa.

Ezután létrehoz egy példányt az adott osztályból néhány értékkel, és az érvényesíti az értékeket, átalakítja őket a megfelelő típusra (ha ez a helyzet), és ad egy objektumot az összes adattal.

És megkapja az összes szerkesztő támogatást az eredményül kapott objektummal.

Példa a hivatalos Pydantic dokumentációból:

=== "Python 3.10+"

     ``` Python
     {!> ../../../docs_src/python_types/tutorial011_py310.py!}
     ```

=== "Python 3.9+"

     ``` Python
     {!> ../../../docs_src/python_types/tutorial011_py39.py!}
     ```

=== "Python 3.6+"

     ``` Python
     {!> ../../../docs_src/python_types/tutorial011.py!}
     ```

!!! info
     Ha többet szeretne megtudni a Pydanticról, tekintse meg a <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">dokumentumációját</a>.

Az egész **FastAPI** Pydantic-on alapul.

Mindezekből a gyakorlatban sokkal többet fog látni a [Oktatói anyag - Felhasználói Útmutató](tutorial/index.md){.internal-link target=_blank} részben.

!!! tipp
     A Pydantic különleges viselkedést mutat, ha az `Optional` vagy a `Union[Something, None]`-t alapértelmezett érték nélkül használja. Erről bővebben a Pydantic dokumentumentációban a <a href="https://pydantic-docs.helpmanual .io/usage/models/#required-optional-fields" class="external-link" target="_blank">Kötelező opcionális mezők</a> fejezetben olvashat.

## Típustippek metaadat-jegyzetekkel

A Python rendelkezik egy olyan funkcióval is, amely lehetővé teszi **további metaadatok** elhelyezését az ilyen típusú tippekben az `Annotated` használatával.

=== "Python 3.9+"

     A Python 3.9-ben az `Annotated` a standard könyvtár része, így importálhatja a `typing` modulból.

     ``` Python hl_lines="1 4"
     {!> ../../../docs_src/python_types/tutorial013_py39.py!}
     ```

=== "Python 3.6+"

     A Python 3.9 alatti verziókban az "Annotation" importálható a "typing_extensions" modulból.

     Alapból telepítve lesz a **FastAPI**-val.

     ``` Python hl_lines="1 4"
     {!> ../../../docs_src/python_types/tutorial013.py!}
     ```

Maga a Python nem csinál semmit ezzel az `Annotated`-del. A szerkesztők és egyéb eszközök esetében a típus továbbra is `str`.

De használhatja ezt a helyet a `Annotated` mezőben, hogy a **FastAPI-t** további metaadatokkal lássa el arról, hogyan szeretné, hogy az alkalmazás működjön.

Fontos megjegyezni, hogy **az első *típusparaméter***, amelyet az `Annotated`-nek továbbít, a **tényleges típus**. A maradék csak metaadat más eszközöknek.

Egyelőre csak azt kell tudnia, hogy az `Annotated` létezik, és hogy ez standard Python. 😎

Később meglátja, milyen **hasznos** lehet.

!!! tipp
     Az a tény, hogy ez egy **standard Python**, azt jelenti, hogy továbbra is a **lehető legjobb fejlesztői élményt** kapja meg a szerkesztőjében, a kód elemzéséhez és újrafeldolgozásához használt eszközökkel, stb. ✨

     És azt is, hogy a kódja kompatibilis lesz sok más Python-eszközzel és -könyvtárral. 🚀

## Típustippek a **FastAPI-ba**

A **FastAPI** kihasználja az ilyen típusú tippeket számos dolog elvégzésére.

A **FastAPI**-val a paramétereket típustippekkel deklarálja, és a következőket kapja:

* **A szerkesztő támogatása**.
* **Típusellenőrzés**.

...és a **FastAPI** ugyanazokat a deklarációkat használja:

* **Követelmények meghatározása**: kérési útvonal paramétereiből, lekérdezési paramétereiből, fejlécekből, törzsekből, függőségekből stb.
* **Adatok konvertálása**: a kérésből a kívánt típusba.
* **Adatok érvényesítése**: minden kérésből származik:
     * **Automatikus hibák** generálása visszaküldésre kerül az ügyfélnek, ha az adatok érvénytelenek.
* **Dokumentálja** az API-t OpenAPI használatával:
     * amelyet azután az automatikus interaktív dokumentációs felhasználói felületek használnak.

Lehet, hogy mindez elvontnak hangzik. Ne aggódjon. Mindezt működés közben a [Oktatói anyag - Felhasználói Útmutató](tutorial/index.md){.internal-link target=_blank} részben láthatja.

A fontos dolog az, hogy a standard Python típusok használatával egyetlen helyen (ahelyett, hogy több osztályt, dekorátort stb. adna hozzá), a **FastAPI** elvégzi Ön helyett a sok munkát.

!!! info
     Ha már végignézte az összes oktatóanyagot, és visszatért, hogy többet megtudjon a típusokról, jó forrás ez  <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link " target="_blank">a "puska" a `mypy`-től</a>.
