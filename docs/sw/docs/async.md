# Concurrency na async / await { #concurrency-and-async-await }

Maelezo kuhusu sintaksia ya `async def` kwa *vitendakazi vya operesheni za njia* na maelezo ya msingi kuhusu msimbo wa asynchronous, concurrency, na parallelism.

## Una haraka? { #in-a-hurry }

<abbr title="too long; didn't read - ni ndefu sana; sikusoma"><strong>TL;DR:</strong></abbr>

Ikiwa unatumia maktaba za wahusika wengine zinazokuambia uziite kwa `await`, kama:

```Python
results = await some_library()
```

Basi, tangaza *vitendakazi vyako vya operesheni za njia* kwa `async def` kama:

```Python hl_lines="2"
@app.get("/")
async def read_results():
    results = await some_library()
    return results
```

/// note | Kumbuka

Unaweza kutumia `await` ndani ya vitendakazi vilivyoundwa kwa `async def` pekee.

///

---

Ikiwa unatumia maktaba ya mhusika mwingine inayowasiliana na kitu fulani (hifadhidata, API, mfumo wa faili, n.k.) na haina uwezo wa kutumia `await`, (kwa sasa hali hii inahusu maktaba nyingi za hifadhidata), basi tangaza *vitendakazi vyako vya operesheni za njia* kama kawaida, kwa `def` tu, kama:

```Python hl_lines="2"
@app.get("/")
def results():
    results = some_library()
    return results
```

---

Ikiwa programu yako (kwa namna fulani) haihitaji kuwasiliana na kitu kingine chochote na kusubiri kijibu, tumia `async def`, hata kama huhitaji kutumia `await` ndani yake.

---

Ikiwa hujui cha kuchagua, tumia `def` ya kawaida.

---

**Kumbuka**: Unaweza kuchanganya `def` na `async def` katika *vitendakazi vyako vya operesheni za njia* kadiri unavyohitaji na kufafanua kila kimoja kwa chaguo linalokufaa zaidi. FastAPI itavishughulikia ipasavyo.

Kwa vyovyote vile, katika hali zote zilizo hapo juu, FastAPI bado itafanya kazi kwa namna ya asynchronous na itakuwa na kasi kubwa sana.

Lakini kwa kufuata hatua zilizo hapo juu, itaweza kuboresha utendaji kwa namna fulani.

## Maelezo ya Kiufundi { #technical-details }

Matoleo ya kisasa ya Python yana uwezo wa kutumia **"msimbo wa asynchronous"** kwa kutumia kitu kinachoitwa **"coroutines"**, kwa sintaksia ya **`async` na `await`**.

Hebu tuangalie kauli hiyo sehemu kwa sehemu katika sehemu zilizo hapa chini:

* **Msimbo wa Asynchronous**
* **`async` na `await`**
* **Coroutines**

## Msimbo wa Asynchronous { #asynchronous-code }

Msimbo wa asynchronous unamaanisha tu kwamba lugha 💬 ina njia ya kuiambia kompyuta / programu 🤖 kwamba katika sehemu fulani ya msimbo, itabidi 🤖 isubiri *kitu kingine* kikamilike mahali pengine. Tuseme *kitu hicho kingine* kinaitwa "faili-linalochelewa" 📝.

Kwa hiyo, wakati huo, kompyuta inaweza kwenda kufanya kazi nyingine, huku "faili-linalochelewa" 📝 likikamilika.

Kisha kompyuta / programu 🤖 itarudi kila inapopata nafasi kwa sababu inasubiri tena, au kila inapomaliza 🤖 kazi zote ilizokuwa nazo wakati huo. Nayo 🤖 itaangalia kama kuna kazi zozote ilizokuwa ikizisubiri ambazo tayari zimemaliza kufanya zilichopaswa kufanya.

Halafu, 🤖 itachukua kazi ya kwanza kukamilika (tuseme, "faili-linalochelewa" 📝 letu) na kuendelea na chochote ilichopaswa kufanya nayo.

Huko "kusubiri kitu kingine" kwa kawaida kunarejelea operesheni za <abbr title="Input and Output - Ingizo na Tokeo">I/O</abbr> ambazo ni za "polepole" kwa kulinganisha (na kasi ya kichakataji na kumbukumbu ya RAM), kama kusubiri:

* data kutoka kwa mteja itumwe kupitia mtandao
* data iliyotumwa na programu yako ipokelewe na mteja kupitia mtandao
* yaliyomo kwenye faili lililo kwenye diski yasomwe na mfumo na kupewa programu yako
* yaliyomo ambayo programu yako iliupa mfumo yaandikwe kwenye diski
* operesheni ya API ya mbali
* operesheni ya hifadhidata ikamilike
* hoja ya hifadhidata irudishe matokeo
* n.k.

Kwa kuwa muda mwingi wa utekelezaji hutumika kusubiri operesheni za <abbr title="Input and Output - Ingizo na Tokeo">I/O</abbr>, operesheni hizo huitwa "I/O bound".

Inaitwa "asynchronous" kwa sababu kompyuta / programu haihitaji "kusawazishwa" na kazi ya polepole, ikisubiri wakati uleule ambapo kazi inakamilika, bila kufanya chochote, ili iweze kuchukua matokeo ya kazi na kuendelea kufanya kazi.

Badala yake, kwa kuwa ni mfumo wa "asynchronous", baada ya kukamilika, kazi inaweza kusubiri kwenye foleni kwa muda mfupi (mikrosekunde chache) ili kompyuta / programu imalize chochote ilichoenda kufanya, kisha irudi kuchukua matokeo na kuendelea kuyafanyia kazi.

Kwa "synchronous" (kinyume cha "asynchronous"), kwa kawaida pia hutumia neno "sequential", yaani kwa mfuatano, kwa sababu kompyuta / programu hufuata hatua zote kwa mfuatano kabla ya kuhamia kazi tofauti, hata kama hatua hizo zinahusisha kusubiri.

### Concurrency na Baga { #concurrency-and-burgers }

Wazo hili la msimbo wa **asynchronous** lililoelezwa hapo juu pia wakati mwingine huitwa **"concurrency"**. Ni tofauti na **"parallelism"**.

**Concurrency** na **parallelism** zote zinahusiana na "mambo tofauti yanayotokea takribani wakati mmoja".

Lakini maelezo ya *concurrency* na *parallelism* yanatofautiana sana.

Ili kuona tofauti, fikiria hadithi ifuatayo kuhusu baga:

### Baga kwa Concurrency { #concurrent-burgers }

Unaenda na mtu unayempenda kupata chakula cha haraka, unasimama kwenye foleni huku mhudumu wa malipo akipokea oda kutoka kwa watu walio mbele yako. 😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

Kisha zamu yako inafika, unaagiza baga 2 za kifahari sana kwa ajili yako na mtu unayempenda. 🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

Mhudumu wa malipo anamwambia mpishi aliye jikoni kitu fulani ili ajue kwamba anapaswa kuandaa baga zenu (hata ingawa kwa sasa anaandaa za wateja waliotangulia).

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

Unalipa. 💸

Mhudumu wa malipo anakupa namba ya zamu yako.

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

Wakati unasubiri, unaenda na mtu unayempenda kuchagua meza, mnaketi na kuzungumza kwa muda mrefu (kwa kuwa baga zenu ni za kifahari sana na zinachukua muda kuandaliwa).

Mkiwa mmeketi mezani pamoja, huku mkisubiri baga, unaweza kutumia muda huo kuvutiwa na jinsi mtu unayempenda alivyo wa ajabu, wa kupendeza na mwenye akili ✨😍✨.

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

Unaposubiri na kuzungumza na mtu unayempenda, mara kwa mara unaangalia namba inayoonyeshwa kwenye kaunta ili kuona kama zamu yako imefika tayari.

Kisha wakati fulani, hatimaye zamu yako inafika. Unaenda kwenye kaunta, unachukua baga zenu na kurudi mezani.

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

Wewe na mtu unayempenda mnakula baga na kufurahia muda wenu pamoja. ✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

/// note | Kumbuka

Michoro mizuri imetengenezwa na [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot). 🎨

///

---

Fikiria wewe ndiye kompyuta / programu 🤖 katika hadithi hiyo.

Ukiwa kwenye foleni, hufanyi kitu 😴, unasubiri zamu yako, bila kufanya chochote chenye "tija" sana. Lakini foleni inasonga haraka kwa sababu mhudumu wa malipo anapokea oda tu (haziandai), kwa hiyo hilo si tatizo.

Kisha, zamu yako inapofika, unafanya kazi halisi yenye "tija": unasoma menyu, unaamua unachotaka, unapata chaguo la mtu unayempenda, unalipa, unahakikisha unatoa noti au kadi sahihi, unahakikisha umetozwa kiasi sahihi, unahakikisha oda ina vitu sahihi, n.k.

Lakini baadaye, hata ingawa bado hamjapata baga zenu, kazi yako na mhudumu wa malipo "imesitishwa kwa muda" ⏸, kwa sababu unapaswa kusubiri 🕙 baga zenu ziwe tayari.

Lakini unapoondoka kauntani na kuketi mezani ukiwa na namba ya zamu yako, unaweza kuhamisha 🔀 umakini wako kwa mtu unayempenda, na "kufanyia kazi" ⏯ 🤓 hilo. Hapo unakuwa tena unafanya kitu chenye "tija" sana, kama vile kumtongoza mtu unayempenda 😍.

Kisha mhudumu wa malipo 💁 anasema "Nimemaliza kuandaa baga" kwa kuweka namba yako kwenye skrini ya kaunta, lakini huruki kama kichaa mara tu namba inayoonyeshwa inapobadilika kuwa namba ya zamu yako. Unajua hakuna atakayeiba baga zenu kwa sababu una namba ya zamu yako, na wengine wana zao.

Kwa hiyo unasubiri mtu unayempenda amalize hadithi yake (kumaliza kazi ya sasa ⏯ / kazi inayoshughulikiwa 🤓), unatabasamu kwa upole na kusema kwamba unaenda kuchukua baga ⏸.

Kisha unaenda kauntani 🔀, kwenye kazi ya awali ambayo sasa imekamilika ⏯, unachukua baga, unashukuru na kuzipeleka mezani. Hilo linakamilisha hatua / kazi hiyo ya kushughulika na kaunta ⏹. Hiyo nayo inaunda kazi mpya, ya "kula baga" 🔀 ⏯, lakini ile ya awali ya "kupata baga" imekamilika ⏹.

### Baga kwa Parallelism { #parallel-burgers }

Sasa hebu tufikirie hizi si "Baga kwa Concurrency", bali "Baga kwa Parallelism".

Unaenda na mtu unayempenda kupata chakula cha haraka kwa parallelism.

Unasimama kwenye foleni huku wahudumu kadhaa wa malipo (tuseme 8), ambao pia ni wapishi, wakipokea oda kutoka kwa watu walio mbele yako.

Kila mtu aliye mbele yako anasubiri baga zake ziwe tayari kabla ya kuondoka kauntani, kwa sababu kila mmoja wa wahudumu 8 wa malipo anaenda kuandaa baga mara moja kabla ya kupokea oda inayofuata.

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

Kisha hatimaye zamu yako inafika, unaagiza baga 2 za kifahari sana kwa ajili yako na mtu unayempenda.

Unalipa 💸.

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

Mhudumu wa malipo anaenda jikoni.

Unasubiri, ukiwa umesimama mbele ya kaunta 🕙, ili mtu mwingine asichukue baga zenu kabla yako, kwa kuwa hakuna namba za zamu.

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

Kwa kuwa wewe na mtu unayempenda mko bize kuzuia mtu yeyote asiingie mbele yenu na kuchukua baga zenu zinapofika, huwezi kumwelekezea umakini mtu unayempenda. 😞

Hii ni kazi ya "synchronous", "umesawazishwa" na mhudumu wa malipo/mpishi 👨‍🍳. Unapaswa kusubiri 🕙 na kuwepo wakati uleule mhudumu wa malipo/mpishi 👨‍🍳 anapomaliza baga na kukupa, la sivyo, mtu mwingine anaweza kuzichukua.

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

Kisha mhudumu wako wa malipo/mpishi 👨‍🍳 hatimaye anarudi na baga zenu, baada ya kusubiri 🕙 kwa muda mrefu hapo mbele ya kaunta.

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

Unachukua baga zenu na kwenda mezani na mtu unayempenda.

Mnazila tu, na mmemaliza. ⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

Hakukuwa na mazungumzo mengi wala kutongozana kwani muda mwingi ulitumika kusubiri 🕙 mbele ya kaunta. 😞

/// note | Kumbuka

Michoro mizuri imetengenezwa na [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot). 🎨

///

---

Katika hali hii ya baga kwa parallelism, wewe ni kompyuta / programu 🤖 yenye vichakataji viwili (wewe na mtu unayempenda), vyote vikisubiri 🕙 na kuelekeza umakini wao ⏯ kwenye "kusubiri kauntani" 🕙 kwa muda mrefu.

Duka la chakula cha haraka lina vichakataji 8 (wahudumu wa malipo/wapishi). Ilhali duka la baga kwa concurrency huenda lilikuwa na 2 tu (mhudumu mmoja wa malipo na mpishi mmoja).

Lakini bado, uzoefu wa mwisho si mzuri zaidi. 😞

---

Hii ndiyo ingekuwa hadithi inayolingana ya baga kwa parallelism. 🍔

Kwa mfano wa hili ulio karibu zaidi na "maisha halisi", fikiria benki.

Hadi hivi karibuni, benki nyingi zilikuwa na wahudumu wengi wa malipo 👨‍💼👨‍💼👨‍💼👨‍💼 na foleni kubwa 🕙🕙🕙🕙🕙🕙🕙🕙.

Wahudumu wote wakifanya kazi yote na mteja mmoja baada ya mwingine 👨‍💼⏯.

Na unapaswa kusubiri 🕙 kwenye foleni kwa muda mrefu, la sivyo unapoteza zamu yako.

Huenda usingependa kwenda na mtu unayempenda 😍 kufanya shughuli zako benki 🏦.

### Hitimisho la Baga { #burger-conclusion }

Katika hali hii ya "baga za chakula cha haraka na mtu unayempenda", kwa kuwa kuna kusubiri kwingi 🕙, inaleta maana zaidi kuwa na mfumo wa concurrency ⏸🔀⏯.

Hii ndiyo hali ya programu nyingi za wavuti.

Watumiaji ni wengi sana, lakini seva yako inasubiri 🕙 miunganisho yao isiyo mizuri sana itume maombi yao.

Na kisha inasubiri 🕙 tena majibu yarudi.

Huku "kusubiri" 🕙 hupimwa kwa mikrosekunde, lakini bado, ukijumlisha yote, mwishowe ni muda mwingi wa kusubiri.

Ndiyo maana inaleta maana sana kutumia msimbo wa asynchronous ⏸🔀⏯ kwa API za wavuti.

Namna hii ya kufanya kazi kwa asynchronous ndiyo iliyofanya NodeJS iwe maarufu (hata ingawa NodeJS haitumii parallelism) na huo ndio uwezo mkuu wa Go kama lugha ya programu.

Na hicho ndicho kiwango cha utendaji unachopata kwa **FastAPI**.

Na kwa kuwa unaweza kuwa na parallelism na asynchronous kwa wakati mmoja, unapata utendaji wa juu kuliko framework nyingi za NodeJS zilizojaribiwa, na unaolingana na Go, ambayo ni lugha inayotumia compiler iliyo karibu zaidi na C [(yote haya kutokana na Starlette)](https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1).

### Je, concurrency ni bora kuliko parallelism? { #is-concurrency-better-than-parallelism }

La hasha! Hilo si fundisho la hadithi hii.

Concurrency ni tofauti na parallelism. Na ni bora katika hali **maalumu** zinazohusisha kusubiri kwingi. Kwa sababu hiyo, kwa ujumla ni bora sana kuliko parallelism kwa uundaji wa programu za wavuti. Lakini si kwa kila kitu.

Kwa hiyo, ili kusawazisha hilo, fikiria hadithi fupi ifuatayo:

> Unapaswa kusafisha nyumba kubwa iliyo chafu.

*Ndiyo, hiyo ndiyo hadithi yote*.

---

Hakuna kusubiri 🕙 popote, ni kazi nyingi tu zinazopaswa kufanywa, katika sehemu nyingi za nyumba.

Unaweza kufanya kwa zamu kama katika mfano wa baga, kwanza sebule, kisha jikoni, lakini kwa kuwa husubiri 🕙 kitu chochote, unasafisha tu mfululizo, zamu hazitabadilisha kitu chochote.

Ingechukua muda uleule kumaliza ukiwa na zamu (concurrency) au bila zamu, na ungekuwa umefanya kiasi kilekile cha kazi.

Lakini katika hali hii, kama ungeweza kuwaleta wale 8 waliokuwa wahudumu wa malipo/wapishi na ambao sasa ni wasafishaji, na kila mmoja wao (pamoja na wewe) achukue sehemu ya nyumba aisafishe, mngeweza kufanya kazi yote kwa **parallelism**, kwa msaada huo wa ziada, na kumaliza mapema zaidi.

Katika hali hii, kila mmoja wa wasafishaji (pamoja na wewe) angekuwa kichakataji, akifanya sehemu yake ya kazi.

Na kwa kuwa muda mwingi wa utekelezaji unatumika kufanya kazi halisi (badala ya kusubiri), na kazi katika kompyuta hufanywa na <abbr title="Central Processing Unit - Kitengo Kikuu cha Uchakataji">CPU</abbr>, matatizo haya huitwa "CPU bound".

---

Mifano ya kawaida ya operesheni za CPU bound ni vitu vinavyohitaji uchakataji wa hesabu changamano.

Kwa mfano:

* **Uchakataji wa sauti** au **picha**.
* **Computer vision**: picha inaundwa na mamilioni ya pikseli, kila pikseli ina thamani / rangi 3, na kuichakata kwa kawaida kunahitaji kufanya hesabu fulani kwenye pikseli hizo, zote kwa wakati mmoja.
* **Machine Learning**: kwa kawaida inahitaji uzidishaji mwingi wa "matrix" na "vector". Fikiria lahajedwali kubwa lenye namba na kuzizidisha zote pamoja kwa wakati mmoja.
* **Deep Learning**: hii ni tawi la Machine Learning, kwa hiyo, hali hiyo hiyo inatumika. Tofauti ni kwamba hakuna lahajedwali moja tu la namba za kuzidisha, bali kuna kundi kubwa la lahajedwali hizo, na katika hali nyingi, unatumia kichakataji maalumu kujenga na / au kutumia modeli hizo.

### Concurrency + Parallelism: Wavuti + Machine Learning { #concurrency-parallelism-web-machine-learning }

Kwa **FastAPI** unaweza kunufaika na concurrency ambayo ni ya kawaida sana katika uundaji wa programu za wavuti (kivutio kikuu hichohicho cha NodeJS).

Lakini pia unaweza kutumia manufaa ya parallelism na multiprocessing (kuwa na michakato mingi inayotekelezwa kwa parallelism) kwa kazi za **CPU bound** kama zile za mifumo ya Machine Learning.

Hilo, pamoja na ukweli rahisi kwamba Python ndiyo lugha kuu ya **Sayansi ya Data**, Machine Learning na hasa Deep Learning, hufanya FastAPI ifae sana kwa API na programu za wavuti za Sayansi ya Data / Machine Learning (miongoni mwa nyingine nyingi).

Ili kuona jinsi ya kufanikisha parallelism hii katika mazingira ya matumizi halisi, angalia sehemu kuhusu [Deployment](deployment/index.md).

## `async` na `await` { #async-and-await }

Matoleo ya kisasa ya Python yana njia rahisi sana kueleweka ya kufafanua msimbo wa asynchronous. Hii hufanya uonekane kama msimbo wa kawaida wa "mfuatano" na kufanya "kusubiri" kwa niaba yako katika nyakati zinazofaa.

Kunapokuwa na operesheni itakayohitaji kusubiri kabla ya kutoa matokeo na ambayo ina uwezo wa kutumia vipengele hivi vipya vya Python, unaweza kuiandika hivi:

```Python
burgers = await get_burgers(2)
```

Jambo muhimu hapa ni `await`. Inaiambia Python kwamba inapaswa kusubiri ⏸ `get_burgers(2)` imalize kufanya kazi yake 🕙 kabla ya kuhifadhi matokeo kwenye `burgers`. Kwa hilo, Python itajua kwamba inaweza kwenda kufanya kitu kingine 🔀 ⏯ wakati huo (kama kupokea ombi jingine).

Ili `await` ifanye kazi, lazima iwe ndani ya kitendakazi kinachowezesha namna hii ya kufanya kazi kwa asynchronous. Ili kufanya hivyo, unakitangaza tu kwa `async def`:

```Python hl_lines="1"
async def get_burgers(number: int):
    # Fanya mambo fulani kwa asynchronous ili kuandaa baga
    return burgers
```

...badala ya `def`:

```Python hl_lines="2"
# Hii si asynchronous
def get_sequential_burgers(number: int):
    # Fanya mambo fulani kwa mfuatano ili kuandaa baga
    return burgers
```

Kwa `async def`, Python inajua kwamba, ndani ya kitendakazi hicho, inapaswa kuzingatia semi za `await`, na kwamba inaweza "kusitisha kwa muda" ⏸ utekelezaji wa kitendakazi hicho na kwenda kufanya kitu kingine 🔀 kabla ya kurudi.

Unapotaka kuita kitendakazi cha `async def`, unapaswa kukisubiri kwa `await`. Kwa hiyo, hii haitafanya kazi:

```Python
# Hii haitafanya kazi, kwa sababu get_burgers ilifafanuliwa kwa: async def
burgers = get_burgers(2)
```

---

Kwa hiyo, ikiwa unatumia maktaba inayokuambia kwamba unaweza kuiita kwa `await`, unahitaji kuunda *vitendakazi vya operesheni za njia* vinavyoitumia kwa `async def`, kama katika:

```Python hl_lines="2-3"
@app.get("/burgers")
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### Maelezo zaidi ya kiufundi { #more-technical-details }

Huenda umeona kwamba `await` inaweza kutumika tu ndani ya vitendakazi vilivyofafanuliwa kwa `async def`.

Lakini wakati huo huo, vitendakazi vilivyofafanuliwa kwa `async def` vinapaswa "kusubiriwa" kwa `await`. Kwa hiyo, vitendakazi vyenye `async def` vinaweza kuitwa tu ndani ya vitendakazi ambavyo pia vimefafanuliwa kwa `async def`.

Kwa hiyo, kuhusu yai na kuku, unaitaje kitendakazi cha kwanza cha `async`?

Ikiwa unatumia **FastAPI**, huhitaji kuwa na wasiwasi kuhusu hilo, kwa sababu kitendakazi hicho cha "kwanza" kitakuwa *kitendakazi chako cha operesheni ya njia*, na FastAPI itajua jinsi ya kufanya jambo linalofaa.

Lakini ikiwa unataka kutumia `async` / `await` bila FastAPI, unaweza kufanya hivyo pia.

### Andika msimbo wako mwenyewe wa async { #write-your-own-async-code }

Starlette (na **FastAPI**) zimejengwa juu ya [AnyIO](https://anyio.readthedocs.io/en/stable/), ambayo inazifanya ziendane na [asyncio](https://docs.python.org/3/library/asyncio-task.html) ya maktaba ya kawaida ya Python pamoja na [Trio](https://trio.readthedocs.io/en/stable/).

Hasa, unaweza kutumia [AnyIO](https://anyio.readthedocs.io/en/stable/) moja kwa moja kwa matumizi yako ya hali ya juu ya concurrency yanayohitaji mifumo ya hali ya juu zaidi katika msimbo wako.

Na hata kama hutumii FastAPI, unaweza pia kuandika programu zako mwenyewe za async kwa [AnyIO](https://anyio.readthedocs.io/en/stable/) ili ziwe na uoanifu mkubwa na kupata manufaa yake (k.m. *structured concurrency*).

Niliunda maktaba nyingine juu ya AnyIO, kama tabaka jepesi juu yake, ili kuboresha kidogo maelezo ya aina na kupata **ukamilishaji wa kiotomatiki** bora zaidi, **makosa yanayoonyeshwa ndani ya msimbo**, n.k. Pia ina utangulizi na mafunzo rahisi kufuata ili kukusaidia **kuelewa** na kuandika **msimbo wako mwenyewe wa async**: [Asyncer](https://asyncer.tiangolo.com/). Ingefaa hasa ikiwa unahitaji **kuchanganya msimbo wa async na msimbo wa kawaida** (blocking/synchronous).

### Aina nyingine za msimbo wa asynchronous { #other-forms-of-asynchronous-code }

Mtindo huu wa kutumia `async` na `await` ni mpya kiasi katika lugha hii.

Lakini unafanya kazi na msimbo wa asynchronous iwe rahisi zaidi.

Sintaksia hii hii (au inayokaribia kufanana kabisa) pia iliongezwa hivi karibuni katika matoleo ya kisasa ya JavaScript (kwenye Kivinjari na NodeJS).

Lakini kabla ya hapo, kushughulikia msimbo wa asynchronous kulikuwa na uchangamano na ugumu zaidi.

Katika matoleo ya awali ya Python, ungeweza kutumia threads au [Gevent](https://www.gevent.org/). Lakini msimbo huo ni changamano zaidi kuuelewa, kutafuta na kurekebisha makosa yake, na kuufikiria.

Katika matoleo ya awali ya NodeJS / JavaScript ya Kivinjari, ungetumia "callbacks". Jambo linalosababisha "callback hell".

## Coroutines { #coroutines }

**Coroutine** ni neno la kitaalamu tu kwa kitu kinachorudishwa na kitendakazi cha `async def`. Python inajua kwamba ni kitu kinachofanana na kitendakazi, ambacho inaweza kukianzisha na ambacho kitakamilika wakati fulani, lakini ambacho pia kinaweza kusitishwa kwa muda ⏸ ndani yake, kila kunapokuwa na `await` ndani yake.

Lakini utendaji huu wote wa kutumia msimbo wa asynchronous kwa `async` na `await` mara nyingi hufupishwa kama kutumia "coroutines". Unalinganishwa na kipengele kikuu muhimu cha Go, "Goroutines".

## Hitimisho { #conclusion }

Hebu tuangalie kauli ileile ya hapo juu:

> Matoleo ya kisasa ya Python yana uwezo wa kutumia **"msimbo wa asynchronous"** kwa kutumia kitu kinachoitwa **"coroutines"**, kwa sintaksia ya **`async` na `await`**.

Hiyo sasa inapaswa kueleweka zaidi. ✨

Hayo yote ndiyo yanayowezesha FastAPI kufanya kazi (kupitia Starlette) na kuifanya iwe na utendaji wa kuvutia kiasi hicho.

## Maelezo ya Kina Sana ya Kiufundi { #very-technical-details }

/// warning | Onyo

Huenda unaweza kuruka sehemu hii.

Haya ni maelezo ya kina sana ya kiufundi kuhusu jinsi **FastAPI** inavyofanya kazi ndani yake.

Ikiwa una ujuzi wa kutosha wa kiufundi (coroutines, threads, blocking, n.k.) na una shauku ya kujua jinsi FastAPI inavyoshughulikia `async def` ikilinganishwa na `def` ya kawaida, endelea.

///

### Vitendakazi vya operesheni za njia { #path-operation-functions }

Unapotangaza *kitendakazi cha operesheni ya njia* kwa `def` ya kawaida badala ya `async def`, kinaendeshwa katika threadpool ya nje ambayo kisha husubiriwa kwa `await`, badala ya kuitwa moja kwa moja (kwani kingezuia seva kuendelea na kazi nyingine).

Ikiwa unatoka kwenye framework nyingine ya async ambayo haifanyi kazi kwa namna iliyoelezwa hapo juu na umezoea kufafanua *vitendakazi vya operesheni za njia* rahisi vya kufanya hesabu tu kwa `def` ya kawaida ili kupata ongezeko dogo la utendaji (takribani nanosekunde 100), tafadhali kumbuka kwamba katika **FastAPI** matokeo yatakuwa kinyume kabisa. Katika hali hizi, ni bora kutumia `async def` isipokuwa *vitendakazi vyako vya operesheni za njia* vinatumia msimbo unaofanya operesheni za <abbr title="Input/Output - Ingizo/Tokeo: kusoma au kuandika kwenye diski, mawasiliano ya mtandao.">I/O</abbr> zinazozuia utekelezaji kuendelea.

Hata hivyo, katika hali zote mbili, kuna uwezekano kwamba **FastAPI** [bado itakuwa na kasi zaidi](index.md#performance) kuliko (au angalau kulingana na) framework yako ya awali.

### Vitegemezi { #dependencies }

Hali hiyo hiyo inatumika kwa [vitegemezi](tutorial/dependencies/index.md). Ikiwa kitegemezi ni kitendakazi cha kawaida cha `def` badala ya `async def`, kinaendeshwa katika threadpool ya nje.

### Vitegemezi vya vitegemezi vingine { #sub-dependencies }

Unaweza kuwa na vitegemezi vingi na [vitegemezi vya vitegemezi vingine](tutorial/dependencies/sub-dependencies.md) vinavyohitajiana (kama vigezo katika ufafanuzi wa vitendakazi), baadhi yake vinaweza kuundwa kwa `async def` na vingine kwa `def` ya kawaida. Bado vitafanya kazi, na vile vilivyoundwa kwa `def` ya kawaida vitaitwa kwenye thread ya nje (kutoka kwenye threadpool) badala ya "kusubiriwa" kwa `await`.

### Vitendakazi vingine vya usaidizi { #other-utility-functions }

Kitendakazi kingine chochote cha usaidizi unachokiita moja kwa moja kinaweza kuundwa kwa `def` ya kawaida au `async def`, na FastAPI haitaathiri namna unavyokiita.

Hii ni tofauti na vitendakazi ambavyo FastAPI inaita kwa niaba yako: *vitendakazi vya operesheni za njia* na vitegemezi.

Ikiwa kitendakazi chako cha usaidizi ni kitendakazi cha kawaida chenye `def`, kitaitwa moja kwa moja (kama unavyokiandika katika msimbo wako), si katika threadpool; ikiwa kitendakazi kimeundwa kwa `async def`, basi unapaswa kutumia `await` kwa kitendakazi hicho unapokiita katika msimbo wako.

---

Kwa mara nyingine, haya ni maelezo ya kina sana ya kiufundi ambayo huenda yakawa na manufaa ikiwa ulikuja kuyatafuta.

Vinginevyo, miongozo ya sehemu iliyo hapo juu inapaswa kukutosha: <a href="#in-a-hurry">Una haraka?</a>.
