# Concurrency na async / await { #concurrency-and-async-await }

Maelezo kuhusu sintaksia ya `async def` kwa *path operation functions* na maelezo ya msingi kuhusu msimbo wa asynchronous, concurrency, na parallelism.

## Una haraka? { #in-a-hurry }

<abbr title="too long; didn't read - ni ndefu sana; sikusoma"><strong>TL;DR:</strong></abbr>

Ikiwa unatumia library za wahusika wengine zinazokuambia uziite kwa `await`, kama:

```Python
results = await some_library()
```

Basi, tangaza *path operation functions* zako kwa `async def` kama:

```Python hl_lines="2"
@app.get("/")
async def read_results():
    results = await some_library()
    return results
```

/// note | Kumbuka

Unaweza kutumia `await` ndani tu ya function zilizoundwa kwa `async def`.

///

---

Ikiwa unatumia library ya mhusika mwingine inayowasiliana na kitu fulani (database, API, file system, n.k.) na haiwezeshi matumizi ya `await`, (kwa sasa hivi ndivyo ilivyo kwa library nyingi za database), basi tangaza *path operation functions* zako kama kawaida, kwa `def` tu, kama:

```Python hl_lines="2"
@app.get("/")
def results():
    results = some_library()
    return results
```

---

Ikiwa programu yako (kwa namna fulani) haihitaji kuwasiliana na kitu kingine chochote na kukisubiri kijibu, tumia `async def`, hata kama huhitaji kutumia `await` ndani yake.

---

Ikiwa hujui tu cha kutumia, tumia `def` ya kawaida.

---

**Kumbuka**: Unaweza kuchanganya `def` na `async def` katika *path operation functions* zako kadiri unavyohitaji na kufafanua kila moja kwa kutumia chaguo linalokufaa zaidi. FastAPI itazishughulikia ipasavyo.

Kwa vyovyote vile, katika hali zote zilizo hapo juu, FastAPI bado itafanya kazi kwa namna ya asynchronous na itakuwa na kasi sana.

Lakini kwa kufuata hatua zilizo hapo juu, itaweza kuboresha utendaji kwa namna fulani.

## Maelezo ya Kiufundi { #technical-details }

Matoleo ya kisasa ya Python yanawezesha matumizi ya **"msimbo wa asynchronous"** kwa kutumia kitu kinachoitwa **"coroutines"**, kwa sintaksia ya **`async` na `await`**.

Hebu tuangalie kauli hiyo sehemu kwa sehemu katika vipengele vilivyo hapa chini:

* **Msimbo wa Asynchronous**
* **`async` na `await`**
* **Coroutines**

## Msimbo wa Asynchronous { #asynchronous-code }

Msimbo wa asynchronous unamaanisha tu kwamba lugha 💬 ina njia ya kuiambia kompyuta / programu 🤖 kwamba katika sehemu fulani ya msimbo, itabidi 🤖 isubiri *kitu kingine* kikamilike mahali pengine. Tuseme kwamba *kitu hicho kingine* kinaitwa "slow-file" 📝.

Kwa hiyo, katika muda huo, kompyuta inaweza kwenda kufanya kazi nyingine, huku "slow-file" 📝 ikikamilika.

Kisha kompyuta / programu 🤖 itarudi kila inapopata nafasi kwa sababu inasubiri tena, au kila inapomaliza 🤖 kazi zote ilizokuwa nazo wakati huo. Nayo 🤖 itaangalia kama kazi yoyote iliyokuwa ikisubiri tayari imemaliza kufanya ilichopaswa kufanya.

Halafu, 🤖 inachukua kazi ya kwanza kukamilika (tuseme, "slow-file" 📝 yetu) na kuendelea na chochote ilichopaswa kufanya nayo.

Huko "kusubiri kitu kingine" kwa kawaida kunahusu operesheni za <abbr title="Input and Output - Ingizo na Tokeo">I/O</abbr> ambazo ni za "polepole" kwa kulinganisha (na kasi ya processor na memory ya RAM), kama kusubiri:

* data kutoka kwa client itumwe kupitia network
* data iliyotumwa na programu yako ipokelewe na client kupitia network
* yaliyomo kwenye file katika disk yasomwe na mfumo na yapewe programu yako
* maudhui ambayo programu yako iliupa mfumo yaandikwe kwenye disk
* operesheni ya API ya mbali
* operesheni ya database ikamilike
* query ya database irudishe matokeo
* n.k.

Kwa kuwa muda wa utekelezaji hutumika zaidi kusubiri operesheni za <abbr title="Input and Output - Ingizo na Tokeo">I/O</abbr>, zinaitwa operesheni za "I/O bound".

Inaitwa "asynchronous" kwa sababu kompyuta / programu haihitaji kuwa "synchronized" na kazi ya polepole, ikisubiri wakati hasa ambapo kazi hiyo inakamilika, bila kufanya chochote, ili iweze kuchukua matokeo ya kazi hiyo na kuendelea na kazi.

Badala yake, kwa kuwa mfumo ni wa "asynchronous", kazi ikishakamilika inaweza kusubiri kwenye foleni kwa muda mfupi (microseconds chache) ili kompyuta / programu imalize chochote ilichoenda kufanya, kisha irudi kuchukua matokeo na kuendelea kuyafanyia kazi.

Kwa "synchronous" (kinyume cha "asynchronous") kwa kawaida pia hutumia neno "sequential", kwa sababu kompyuta / programu hufuata hatua zote kwa mfuatano kabla ya kuhamia kazi tofauti, hata kama hatua hizo zinahusisha kusubiri.

### Concurrency na Baga { #concurrency-and-burgers }

Dhana hii ya msimbo wa **asynchronous** iliyoelezwa hapo juu pia wakati mwingine huitwa **"concurrency"**. Ni tofauti na **"parallelism"**.

**Concurrency** na **parallelism** zote zinahusiana na "mambo tofauti yanayotokea takribani wakati mmoja".

Lakini maelezo ya *concurrency* na *parallelism* ni tofauti sana.

Ili kuona tofauti hiyo, fikiria hadithi ifuatayo kuhusu baga:

### Baga za Concurrent { #concurrent-burgers }

Unaenda na mtu unayempenda kupata chakula cha haraka, unasimama kwenye foleni huku mhudumu wa malipo akipokea oda kutoka kwa watu walio mbele yako. 😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

Kisha zamu yako inafika, unaagiza baga 2 za kipekee sana kwa ajili yako na mtu unayempenda. 🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

Mhudumu wa malipo anamwambia mpishi aliye jikoni jambo fulani ili ajue kwamba anapaswa kuandaa baga zenu (ingawa kwa sasa anaandaa zile za wateja waliotangulia).

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

Unalipa. 💸

Mhudumu wa malipo anakupa namba ya zamu yako.

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

Mnaposubiri, unaenda na mtu unayempenda na kuchagua meza, mnaketi na kuzungumza kwa muda mrefu (kwa kuwa baga zenu ni za kipekee sana na zinachukua muda kuandaliwa).

Unapokuwa umeketi mezani na mtu unayempenda, huku mkisubiri baga, unaweza kutumia muda huo kuvutiwa na jinsi alivyo mzuri, mwenye haiba na mwerevu ✨😍✨.

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

Unaposubiri na kuzungumza na mtu unayempenda, mara kwa mara unaangalia namba inayoonyeshwa kaunta ili kuona kama zamu yako imefika.

Kisha wakati fulani, hatimaye zamu yako inafika. Unaenda kaunta, unachukua baga zenu na kurudi mezani.

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

Wewe na mtu unayempenda mnakula baga na kufurahia muda wenu pamoja. ✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

/// note | Kumbuka

Vielelezo maridadi vimechorwa na [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot). 🎨

///

---

Fikiria kwamba wewe ndiye kompyuta / programu 🤖 katika hadithi hiyo.

Ukiwa kwenye foleni, hufanyi chochote 😴, unasubiri zamu yako, hufanyi kitu chochote chenye "tija" sana. Lakini foleni inasonga haraka kwa sababu mhudumu wa malipo anapokea oda tu (haziandai), kwa hiyo hilo si tatizo.

Kisha, zamu yako inapofika, unafanya kazi yenye "tija" kweli, unapitia menyu, unaamua unachotaka, unapata chaguo la mtu unayempenda, unalipa, unahakikisha kwamba unatoa noti au kadi sahihi, unahakikisha kwamba unatozwa kiasi sahihi, unahakikisha kwamba oda ina vitu sahihi, n.k.

Lakini baadaye, ingawa bado hujapata baga zenu, kazi yako na mhudumu wa malipo "imesitishwa kwa muda" ⏸, kwa sababu unapaswa kusubiri 🕙 baga zenu ziwe tayari.

Lakini unapoondoka kaunta na kuketi mezani ukiwa na namba ya zamu yako, unaweza kuelekeza 🔀 umakini wako kwa mtu unayempenda, na "kufanyia kazi" ⏯ 🤓 hilo. Hapo unakuwa tena unafanya jambo lenye "tija" sana, yaani kumtongoza mtu unayempenda 😍.

Kisha mhudumu wa malipo 💁 anasema "Nimemaliza kuandaa baga" kwa kuweka namba yako kwenye skrini ya kaunta, lakini huruki kama kichaa mara tu namba inayoonyeshwa inapobadilika na kuwa namba ya zamu yako. Unajua hakuna atakayeiba baga zenu kwa sababu una namba ya zamu yako, na wengine wana zao.

Kwa hiyo unasubiri mtu unayempenda amalize hadithi yake (amalize kazi ya sasa ⏯ / kazi inayoshughulikiwa 🤓), unatabasamu kwa upole na kusema kwamba unaenda kuchukua baga ⏸.

Kisha unaenda kaunta 🔀, kwenye kazi ya awali ambayo sasa imekamilika ⏯, unachukua baga, unashukuru na kuzipeleka mezani. Hilo linakamilisha hatua / kazi hiyo ya kuwasiliana na kaunta ⏹. Hilo nalo linaunda kazi mpya, ya "kula baga" 🔀 ⏯, lakini ile ya awali ya "kupata baga" imekamilika ⏹.

### Baga za Parallel { #parallel-burgers }

Sasa hebu tufikirie kwamba hizi si "Baga za Concurrent", bali ni "Baga za Parallel".

Unaenda na mtu unayempenda kupata chakula cha haraka cha parallel.

Unasimama kwenye foleni huku wahudumu kadhaa wa malipo (tuseme 8), ambao pia ni wapishi, wakipokea oda kutoka kwa watu walio mbele yako.

Kila mtu aliye mbele yako anasubiri baga zake ziwe tayari kabla ya kuondoka kaunta kwa sababu kila mmoja wa wahudumu 8 wa malipo anaenda kuandaa baga mara moja kabla ya kupokea oda inayofuata.

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

Kisha hatimaye zamu yako inafika, unaagiza baga 2 za kipekee sana kwa ajili yako na mtu unayempenda.

Unalipa 💸.

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

Mhudumu wa malipo anaenda jikoni.

Unasubiri, ukiwa umesimama mbele ya kaunta 🕙, ili mtu mwingine asichukue baga zenu kabla yako, kwa kuwa hakuna namba za zamu.

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

Kwa kuwa wewe na mtu unayempenda mnajishughulisha na kuhakikisha hakuna anayepita mbele yenu na kuchukua baga zenu zinapofika, huwezi kumpa umakini mtu unayempenda. 😞

Hii ni kazi ya "synchronous", wewe uko "synchronized" na mhudumu wa malipo/mpishi 👨‍🍳. Unapaswa kusubiri 🕙 na kuwepo wakati hasa ambapo mhudumu wa malipo/mpishi 👨‍🍳 anamaliza kuandaa baga na kukupa, la sivyo mtu mwingine anaweza kuzichukua.

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

Kisha mhudumu wako wa malipo/mpishi 👨‍🍳 hatimaye anarudi na baga zenu, baada ya muda mrefu wa kusubiri 🕙 pale mbele ya kaunta.

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

Unachukua baga zenu na kwenda mezani na mtu unayempenda.

Mnazila tu, kisha mmemaliza. ⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

Hakukuwa na mazungumzo mengi wala kutongozana kwa kuwa muda mwingi ulitumika kusubiri 🕙 mbele ya kaunta. 😞

/// note | Kumbuka

Vielelezo maridadi vimechorwa na [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot). 🎨

///

---

Katika hali hii ya baga za parallel, wewe ni kompyuta / programu 🤖 yenye processor mbili (wewe na mtu unayempenda), zote zikisubiri 🕙 na kuelekeza umakini wao ⏯ kwenye "kusubiri kaunta" 🕙 kwa muda mrefu.

Mgahawa wa chakula cha haraka una processor 8 (wahudumu wa malipo/wapishi). Ilhali mgahawa wa baga za concurrent huenda ulikuwa na 2 tu (mhudumu mmoja wa malipo na mpishi mmoja).

Lakini bado, hali ya mwisho si ya kufurahisha zaidi. 😞

---

Hiyo ndiyo ingekuwa hadithi sawia ya parallel kwa baga. 🍔

Kwa mfano wa hili unaokaribiana zaidi na "maisha halisi", fikiria benki.

Hadi hivi karibuni, benki nyingi zilikuwa na wahudumu wengi wa kaunta 👨‍💼👨‍💼👨‍💼👨‍💼 na foleni ndefu 🕙🕙🕙🕙🕙🕙🕙🕙.

Wahudumu wote wa kaunta wakifanya kazi yote na mteja mmoja baada ya mwingine 👨‍💼⏯.

Na unapaswa kusubiri 🕙 kwenye foleni kwa muda mrefu, la sivyo unapoteza zamu yako.

Pengine usingependa kwenda na mtu unayempenda 😍 kufanya shughuli zako benki 🏦.

### Hitimisho la Baga { #burger-conclusion }

Katika hali hii ya "baga za chakula cha haraka pamoja na mtu unayempenda", kwa kuwa kuna kusubiri sana 🕙, ina maana zaidi kuwa na mfumo wa concurrent ⏸🔀⏯.

Hivi ndivyo ilivyo kwa programu nyingi za wavuti.

Watumiaji wengi sana, lakini server yako inasubiri 🕙 muunganisho wao usio mzuri sana utume request zao.

Na kisha inasubiri 🕙 tena response zirudi.

Huku "kusubiri" 🕙 hupimwa kwa microseconds, lakini bado, ukijumlisha muda huo wote, mwishowe ni kusubiri sana.

Ndiyo maana ina maana sana kutumia msimbo wa asynchronous ⏸🔀⏯ kwa API za wavuti.

Aina hii ya asynchronicity ndiyo iliyofanya NodeJS iwe maarufu (ingawa NodeJS si parallel) na huo ndio uwezo wa kipekee wa Go kama lugha ya programu.

Na hicho ndicho kiwango cha utendaji unachopata kwa **FastAPI**.

Na kwa kuwa unaweza kuwa na parallelism na asynchronicity kwa wakati mmoja, unapata utendaji wa juu zaidi kuliko framework nyingi za NodeJS zilizojaribiwa na unaolingana na Go, ambayo ni lugha inayotumia compiler iliyo karibu zaidi na C [(yote kutokana na Starlette)](https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1).

### Je, concurrency ni bora kuliko parallelism? { #is-concurrency-better-than-parallelism }

Hapana! Hilo si fundisho la hadithi hii.

Concurrency ni tofauti na parallelism. Nayo ni bora katika hali **maalumu** zinazohusisha kusubiri sana. Kwa sababu hiyo, kwa ujumla ni bora sana kuliko parallelism kwa uundaji wa programu za wavuti. Lakini si kwa kila kitu.

Kwa hiyo, ili kusawazisha hilo, fikiria hadithi fupi ifuatayo:

> Unapaswa kusafisha nyumba kubwa, chafu.

*Ndio, hiyo ndiyo hadithi nzima*.

---

Hakuna kusubiri 🕙 popote, kuna kazi nyingi tu za kufanya, katika sehemu mbalimbali za nyumba.

Ungeweza kufanya kazi kwa zamu kama katika mfano wa baga, kwanza sebule, kisha jiko, lakini kwa kuwa husubiri 🕙 chochote, unasafisha tu bila kuacha, zamu hizo hazingeleta tofauti yoyote.

Ingechukua muda uleule kumaliza, iwe kwa zamu (concurrency) au bila zamu, na ungekuwa umefanya kiasi kilekile cha kazi.

Lakini katika hali hii, kama ungeweza kuwaleta wale wahudumu wa malipo/wapishi 8 wa zamani ambao sasa ni wasafishaji, na kila mmoja wao (pamoja nawe) achukue sehemu ya nyumba ya kusafisha, mngeweza kufanya kazi yote kwa **parallel**, kwa msaada huo wa ziada, na kumaliza mapema zaidi.

Katika hali hii, kila mmoja wa wasafishaji (pamoja nawe) angekuwa processor, akifanya sehemu yake ya kazi.

Na kwa kuwa muda mwingi wa utekelezaji unatumiwa kufanya kazi yenyewe (badala ya kusubiri), na kazi kwenye kompyuta hufanywa na <abbr title="Central Processing Unit - Kitengo Kikuu cha Uchakataji">CPU</abbr>, matatizo haya huitwa "CPU bound".

---

Mifano ya kawaida ya operesheni za CPU bound ni mambo yanayohitaji uchakataji changamano wa kihisabati.

Kwa mfano:

* **Uchakataji wa sauti** au **picha**.
* **Computer vision**: picha ina mamilioni ya pixels, kila pixel ina thamani / rangi 3, na uchakataji huo kwa kawaida unahitaji kufanya hesabu fulani kwenye pixels hizo, zote kwa wakati mmoja.
* **Machine Learning**: kwa kawaida inahitaji kuzidisha "matrix" na "vector" mara nyingi. Fikiria spreadsheet kubwa yenye namba na kuzizidisha zote pamoja kwa wakati mmoja.
* **Deep Learning**: hii ni sehemu ya Machine Learning, kwa hiyo maelezo hayo hayo yanatumika. Tofauti ni kwamba hakuna spreadsheet moja tu ya namba za kuzidisha, bali ni mkusanyiko mkubwa wa spreadsheet, na katika hali nyingi, unatumia processor maalumu kujenga na / au kutumia model hizo.

### Concurrency + Parallelism: Wavuti + Machine Learning { #concurrency-parallelism-web-machine-learning }

Kwa **FastAPI** unaweza kufaidika na concurrency ambayo ni ya kawaida sana katika uundaji wa programu za wavuti (hilo ndilo pia jambo kuu linalovutia watu kwenye NodeJS).

Lakini unaweza pia kutumia faida za parallelism na multiprocessing (kuwa na process nyingi zinazoendeshwa kwa parallel) kwa kazi za **CPU bound** kama zile zilizo kwenye mifumo ya Machine Learning.

Hilo, pamoja na ukweli kwamba Python ndiyo lugha kuu ya **Data Science**, Machine Learning na hasa Deep Learning, hufanya FastAPI ifae sana kwa API na programu za wavuti za Data Science / Machine Learning (miongoni mwa nyingine nyingi).

Ili kuona jinsi ya kufanikisha parallelism hii katika mazingira ya matumizi halisi, angalia sehemu kuhusu [Deployment](deployment/index.md).

## `async` na `await` { #async-and-await }

Matoleo ya kisasa ya Python yana njia rahisi sana kuelewa ya kufafanua msimbo wa asynchronous. Hii hufanya uonekane kama msimbo wa kawaida wa "sequential" na kukufanyia "kusubiri" katika nyakati zinazofaa.

Kunapokuwa na operesheni ambayo itahitaji kusubiri kabla ya kutoa matokeo na inayowezesha matumizi ya vipengele hivi vipya vya Python, unaweza kuiandika hivi:

```Python
burgers = await get_burgers(2)
```

Jambo muhimu hapa ni `await`. Inaiambia Python kwamba inapaswa kusubiri ⏸ `get_burgers(2)` imalize kufanya kazi yake 🕙 kabla ya kuhifadhi matokeo katika `burgers`. Kwa hilo, Python itajua kwamba inaweza kwenda kufanya kitu kingine 🔀 ⏯ wakati huo (kama kupokea request nyingine).

Ili `await` ifanye kazi, inapaswa kuwa ndani ya function inayowezesha asynchronicity hii. Ili kufanya hivyo, unaitangaza tu kwa `async def`:

```Python hl_lines="1"
async def get_burgers(number: int):
    # Fanya mambo fulani ya asynchronous ili kuandaa baga
    return burgers
```

...badala ya `def`:

```Python hl_lines="2"
# Hii si asynchronous
def get_sequential_burgers(number: int):
    # Fanya mambo fulani kwa mfuatano ili kuandaa baga
    return burgers
```

Kwa `async def`, Python inajua kwamba, ndani ya function hiyo, inapaswa kuzingatia expression za `await`, na kwamba inaweza "kusitisha kwa muda" ⏸ utekelezaji wa function hiyo na kwenda kufanya kitu kingine 🔀 kabla ya kurudi.

Unapotaka kuita function ya `async def`, unapaswa kuitumia na "await". Kwa hiyo, hii haitafanya kazi:

```Python
# Hii haitafanya kazi, kwa sababu get_burgers ilifafanuliwa kwa: async def
burgers = get_burgers(2)
```

---

Kwa hiyo, ikiwa unatumia library inayokuambia kwamba unaweza kuiita kwa `await`, unahitaji kuunda *path operation functions* zinazoitumia kwa `async def`, kama katika:

```Python hl_lines="2-3"
@app.get("/burgers")
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### Maelezo zaidi ya kiufundi { #more-technical-details }

Huenda umeona kwamba `await` inaweza kutumika ndani tu ya function zilizofafanuliwa kwa `async def`.

Lakini wakati huohuo, function zilizofafanuliwa kwa `async def` zinapaswa kuitwa kwa "await". Kwa hiyo, function zenye `async def` zinaweza kuitwa ndani tu ya function ambazo pia zimefafanuliwa kwa `async def`.

Basi, kuhusu swali la yai na kuku, unaitaje function ya kwanza ya `async`?

Ikiwa unafanya kazi na **FastAPI** huhitaji kuwa na wasiwasi kuhusu hilo, kwa sababu function hiyo ya "kwanza" itakuwa *path operation function* yako, na FastAPI itajua jinsi ya kuishughulikia ipasavyo.

Lakini ikiwa unataka kutumia `async` / `await` bila FastAPI, unaweza kufanya hivyo pia.

### Andika msimbo wako mwenyewe wa async { #write-your-own-async-code }

Starlette (na **FastAPI**) zimejengwa juu ya [AnyIO](https://anyio.readthedocs.io/en/stable/), ambayo huziwezesha kutumika pamoja na library ya kawaida ya Python ya [asyncio](https://docs.python.org/3/library/asyncio-task.html) na pia [Trio](https://trio.readthedocs.io/en/stable/).

Hasa, unaweza kutumia [AnyIO](https://anyio.readthedocs.io/en/stable/) moja kwa moja kwa matumizi yako ya juu ya concurrency yanayohitaji mbinu za juu zaidi katika msimbo wako mwenyewe.

Na hata kama usingekuwa unatumia FastAPI, ungeweza pia kuandika programu zako mwenyewe za async kwa [AnyIO](https://anyio.readthedocs.io/en/stable/) ili ziweze kutumika kwa urahisi na mifumo mingine na kupata faida zake (k.m. *structured concurrency*).

Niliunda library nyingine juu ya AnyIO, kama safu nyembamba juu yake, ili kuboresha kidogo type annotations na kupata **autocompletion**, **inline errors**, n.k. zilizo bora zaidi. Pia ina utangulizi na mafunzo rahisi kufuata ili kukusaidia **kuelewa** na kuandika **msimbo wako mwenyewe wa async**: [Asyncer](https://asyncer.tiangolo.com/). Ingekuwa muhimu hasa ikiwa unahitaji **kuchanganya msimbo wa async na msimbo wa kawaida** (blocking/synchronous).

### Aina nyingine za msimbo wa asynchronous { #other-forms-of-asynchronous-code }

Mtindo huu wa kutumia `async` na `await` ni mpya kiasi katika lugha hii.

Lakini hurahisisha sana kufanya kazi na msimbo wa asynchronous.

Sintaksia hii hii (au inayokaribia kufanana kabisa) pia ilijumuishwa hivi karibuni katika matoleo ya kisasa ya JavaScript (katika Browser na NodeJS).

Lakini kabla ya hapo, kushughulikia msimbo wa asynchronous kulikuwa changamano na kugumu zaidi.

Katika matoleo ya awali ya Python, ungeweza kutumia threads au [Gevent](https://www.gevent.org/). Lakini msimbo wake ni changamano zaidi kuelewa, kutafuta na kurekebisha hitilafu, na kuufikiria.

Katika matoleo ya awali ya NodeJS / Browser JavaScript, ungetumia "callbacks". Hili husababisha "callback hell".

## Coroutines { #coroutines }

**Coroutine** ni istilahi ya kitaalamu tu ya kitu kinachorudishwa na function ya `async def`. Python inajua kwamba ni kitu kinachofanana na function, ambacho inaweza kukianzisha na kwamba kitakamilika wakati fulani, lakini pia kinaweza kusitishwa kwa muda ⏸ ndani yake, kila kunapokuwa na `await` ndani yake.

Lakini utendaji huu wote wa kutumia msimbo wa asynchronous kwa `async` na `await` mara nyingi hufupishwa kama kutumia "coroutines". Unalinganishwa na kipengele kikuu muhimu cha Go, "Goroutines".

## Hitimisho { #conclusion }

Hebu tuangalie kauli ileile kutoka hapo juu:

> Matoleo ya kisasa ya Python yanawezesha matumizi ya **"msimbo wa asynchronous"** kwa kutumia kitu kinachoitwa **"coroutines"**, kwa sintaksia ya **`async` na `await`**.

Sasa hiyo inapaswa kueleweka zaidi. ✨

Yote hayo ndiyo yanayowezesha FastAPI (kupitia Starlette) na kuifanya iwe na utendaji unaovutia sana.

## Maelezo ya Kina Sana ya Kiufundi { #very-technical-details }

/// warning | Onyo

Pengine unaweza kuruka sehemu hii.

Haya ni maelezo ya kina sana ya kiufundi kuhusu jinsi **FastAPI** inavyofanya kazi ndani kwa ndani.

Ikiwa una maarifa ya kiufundi ya kutosha (coroutines, threads, blocking, n.k.) na una hamu ya kujua jinsi FastAPI inavyoshughulikia `async def` ikilinganishwa na `def` ya kawaida, endelea.

///

### Path operation functions { #path-operation-functions }

Unapotangaza *path operation function* kwa `def` ya kawaida badala ya `async def`, inaendeshwa katika threadpool ya nje ambayo kisha inasubiriwa kwa await, badala ya kuitwa moja kwa moja (kwa kuwa kufanya hivyo kungezuia server kuendelea na kazi nyingine).

Ikiwa unatoka kwenye framework nyingine ya async ambayo haifanyi kazi kwa njia iliyoelezwa hapo juu na umezoea kufafanua *path operation functions* rahisi zinazofanya hesabu tu kwa `def` ya kawaida ili kupata ongezeko dogo la utendaji (takribani nanoseconds 100), tafadhali kumbuka kwamba katika **FastAPI** athari yake ingekuwa kinyume kabisa. Katika hali hizi, ni bora kutumia `async def` isipokuwa kama *path operation functions* zako zinatumia msimbo unaofanya <abbr title="Input/Output - Ingizo/Tokeo: kusoma au kuandika kwenye disk, mawasiliano ya network.">I/O</abbr> ya blocking.

Hata hivyo, katika hali zote mbili, kuna uwezekano kwamba **FastAPI** [bado itakuwa na kasi zaidi](index.md#performance) kuliko (au angalau kulingana na) framework yako ya awali.

### Vitegemezi { #dependencies }

Hali hiyohiyo inatumika kwa [vitegemezi](tutorial/dependencies/index.md). Ikiwa kitegemezi ni function ya kawaida ya `def` badala ya `async def`, kinaendeshwa katika threadpool ya nje.

### Vitegemezi vya vitegemezi vingine { #sub-dependencies }

Unaweza kuwa na vitegemezi vingi na [vitegemezi vya vitegemezi vingine](tutorial/dependencies/sub-dependencies.md) vinavyohitajiana (kama vigezo vya ufafanuzi wa function), baadhi yake vinaweza kuwa vimeundwa kwa `async def` na vingine kwa `def` ya kawaida. Bado ingefanya kazi, na vile vilivyoundwa kwa `def` ya kawaida vingeitwa kwenye thread ya nje (kutoka kwenye threadpool) badala ya kuitwa kwa "await".

### Function nyingine za kusaidia { #other-utility-functions }

Function nyingine yoyote ya kusaidia unayoiita moja kwa moja inaweza kuundwa kwa `def` ya kawaida au `async def` na FastAPI haitaathiri namna unavyoiita.

Hii ni tofauti na function ambazo FastAPI inaziita kwa niaba yako: *path operation functions* na vitegemezi.

Ikiwa function yako ya kusaidia ni function ya kawaida yenye `def`, itaitwa moja kwa moja (kama unavyoiandika katika msimbo wako), si katika threadpool; ikiwa function imeundwa kwa `async def` basi unapaswa kutumia `await` kwa function hiyo unapoiita katika msimbo wako.

---

Kwa mara nyingine, haya ni maelezo ya kina sana ya kiufundi ambayo pengine yangekuwa muhimu kama ulikuja kuyatafuta.

Vinginevyo, miongozo ya sehemu iliyo hapo juu inapaswa kukutosha: <a href="#in-a-hurry">Una haraka?</a>.
