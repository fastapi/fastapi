# Faili ya majaribio ya LLM { #llm-test-file }

Hati hii inajaribu kama <abbr title="Large Language Model - Modeli Kubwa ya Lugha">LLM</abbr>, inayotafsiri nyaraka, inaelewa `general_prompt` katika `scripts/translate.py` na prompt maalumu ya lugha katika `docs/{language code}/llm-prompt.md`. Prompt maalumu ya lugha huongezwa mwishoni mwa `general_prompt`.

Majaribio yanayoongezwa hapa yataonekana kwa wabunifu wote wa prompt maalumu za lugha.

Tumia kama ifuatavyo:

* Kuwa na prompt maalumu ya lugha - `docs/{language code}/llm-prompt.md`.
* Tafsiri hati hii upya kwenda lugha unayolenga (tazama, kwa mfano, amri ya `translate-page` ya `translate.py`). Hii itaunda tafsiri katika `docs/{language code}/docs/_llm-test.md`.
* Kagua kama kila kitu kiko sawa katika tafsiri.
* Ikihitajika, boresha prompt yako maalumu ya lugha, prompt ya jumla, au hati ya Kiingereza.
* Kisha rekebisha mwenyewe matatizo yaliyobaki katika tafsiri, ili iwe tafsiri nzuri.
* Tafsiri tena, huku tafsiri hiyo nzuri ikiwa tayari ipo. Matokeo bora yangekuwa kwamba LLM haifanyi tena mabadiliko yoyote kwenye tafsiri. Hiyo inamaanisha kwamba prompt ya jumla na prompt yako maalumu ya lugha ni bora kadiri iwezekanavyo (Wakati mwingine itafanya mabadiliko machache yanayoonekana kuwa ya nasibu; sababu ni kwamba [LLM si algoriti zinazotoa matokeo yaleyale kila mara kwa ingizo lilelile](https://doublespeak.chat/#/handbook#deterministic-output)).

Majaribio:

## Vipande vya msimbo { #code-snippets }

//// tab | Jaribio

Hiki ni kipande cha msimbo: `foo`. Na hiki ni kipande kingine cha msimbo: `bar`. Na kingine: `baz quux`.

////

//// tab | Maelezo

Maudhui ya vipande vya msimbo yanapaswa kuachwa kama yalivyo.

Tazama sehemu ya `### Content of code snippets` katika prompt ya jumla katika `scripts/translate.py`.

////

## Alama za kunukuu { #quotes }

//// tab | Jaribio

Jana, rafiki yangu aliandika: "Ukiandika neno kimakosa kwa usahihi, umeliandika kimakosa". Nikamjibu: "Sahihi, lakini 'kimakosa' ni kimakosa, si '"kimakosa"'".

/// note | Tanbihi

Huenda LLM ikatafsiri hili vibaya. Kinachovutia tu ni kama itahifadhi tafsiri iliyorekebishwa wakati wa kutafsiri tena.

///

////

//// tab | Maelezo

Mbunifu wa prompt anaweza kuchagua kama anataka kubadilisha alama za kunukuu zilizonyooka kuwa alama za kunukuu za uchapaji. Ni sawa kuziacha kama zilivyo.

Tazama, kwa mfano, sehemu ya `### Quotes` katika `docs/de/llm-prompt.md`.

////

## Alama za kunukuu katika vipande vya msimbo { #quotes-in-code-snippets }

//// tab | Jaribio

`pip install "foo[bar]"`

Mifano ya string literals katika vipande vya msimbo: `"this"`, `'that'`.

Mfano mgumu wa string literals katika vipande vya msimbo: `f"I like {'oranges' if orange else "apples"}"`

Mgumu sana: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | Maelezo

... Hata hivyo, alama za kunukuu ndani ya vipande vya msimbo lazima zibaki kama zilivyo.

////

## Vitalu vya msimbo { #code-blocks }

//// tab | Jaribio

Mfano wa msimbo wa Bash...

```bash
# Chapisha salamu kwa ulimwengu
echo "Hello universe"
```

...na mfano wa msimbo wa console...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

...na mfano mwingine wa msimbo wa console...

```console
// Unda saraka "Code"
$ mkdir code
// Hamia kwenye saraka hiyo
$ cd code
```

...na mfano wa msimbo wa Python...

```Python
wont_work()  # Hii haitafanya kazi 😱
works(foo="bar")  # Hii inafanya kazi 🎉
```

...na ni hayo tu.

////

//// tab | Maelezo

Msimbo katika vitalu vya msimbo haupaswi kubadilishwa, isipokuwa maoni.

Tazama sehemu ya `### Content of code blocks` katika prompt ya jumla katika `scripts/translate.py`.

////

## Vichupo na visanduku vya rangi { #tabs-and-colored-boxes }

//// tab | Jaribio

/// note | Tanbihi
Maandishi fulani
///

/// note | Maelezo ya kiufundi
Maandishi fulani
///

/// tip | Kidokezo
Maandishi fulani
///

/// warning | Onyo
Maandishi fulani
///

/// danger | Hatari
Maandishi fulani
///

////

//// tab | Maelezo

Vichupo na vitalu vya `Info`/`Note`/`Warning`/n.k. vinapaswa kuongezewa tafsiri ya kichwa chake baada ya mstari wima (`|`).

Tazama sehemu za `### Special blocks` na `### Tab blocks` katika prompt ya jumla katika `scripts/translate.py`.

////

## Viungo vya wavuti na vya ndani { #web-and-internal-links }

//// tab | Jaribio

Maandishi ya kiungo yanapaswa kutafsiriwa, anwani ya kiungo ibaki bila kubadilishwa:

* [Kiungo cha kichwa kilicho juu](#code-snippets)
* [Kiungo cha ndani](index.md#installation)
* [Kiungo cha nje](https://sqlmodel.tiangolo.com/)
* [Kiungo cha mtindo](https://fastapi.tiangolo.com/css/styles.css)
* [Kiungo cha script](https://fastapi.tiangolo.com/js/logic.js)
* [Kiungo cha picha](https://fastapi.tiangolo.com/img/foo.jpg)

Maandishi ya kiungo yanapaswa kutafsiriwa, anwani ya kiungo ielekeze kwenye tafsiri:

* [Kiungo cha FastAPI](https://fastapi.tiangolo.com/sw/)

////

//// tab | Maelezo

Viungo vinapaswa kutafsiriwa, lakini anwani zake zibaki bila kubadilishwa. Isipokuwa ni viungo vyenye anwani kamili vya kurasa za nyaraka za FastAPI. Katika hali hiyo, kiungo kinapaswa kuelekeza kwenye tafsiri.

Tazama sehemu ya `### Links` katika prompt ya jumla katika `scripts/translate.py`.

////

## Vipengele vya HTML vya "abbr" { #html-abbr-elements }

//// tab | Jaribio

Hapa kuna baadhi ya vitu vilivyowekwa ndani ya vipengele vya HTML vya "abbr" (Baadhi vimebuniwa):

### abbr inatoa kifungu kamili cha maneno { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done - Kukamilisha Mambo">GTD</abbr>
* <abbr title="less than - ndogo kuliko"><code>lt</code></abbr>
* <abbr title="XML Web Token - Tokeni ya Wavuti ya XML">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface - Kiolesura cha Lango la Seva za Parallel">PSGI</abbr>

### abbr inatoa kifungu kamili cha maneno na ufafanuzi { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network - Mtandao wa Watengenezaji wa Mozilla: nyaraka kwa watengenezaji, zilizoandikwa na watu wa Firefox">MDN</abbr>
* <abbr title="Input/Output - Ingizo/Tokeo: kusoma au kuandika kwenye diski, mawasiliano ya mtandao.">I/O</abbr>.

////

//// tab | Maelezo

Sifa za "title" za vipengele vya "abbr" hutafsiriwa kwa kufuata maagizo maalumu.

Tafsiri zinaweza kuongeza vipengele vyake vya "abbr" ambavyo LLM haipaswi kuondoa. Kwa mfano, ili kufafanua maneno ya Kiingereza.

Tazama sehemu ya `### HTML abbr elements` katika prompt ya jumla katika `scripts/translate.py`.

////

## Vipengele vya HTML vya "dfn" { #html-dfn-elements }

* <dfn title="Kundi la mashine zilizosanidiwa ili ziunganishwe na kufanya kazi pamoja kwa namna fulani.">cluster</dfn>
* <dfn title="Mbinu ya ujifunzaji wa mashine inayotumia mitandao bandia ya neva yenye tabaka nyingi zilizofichwa kati ya tabaka za ingizo na tokeo, na hivyo kujenga muundo wa ndani wenye kina">Ujifunzaji wa Kina</dfn>

## Vichwa { #headings }

//// tab | Jaribio

### Unda programu ya wavuti - mafunzo { #develop-a-webapp-a-tutorial }

Habari.

### Vidokezo na viashirio vya aina { #type-hints-and-annotations }

Habari tena.

### Madarasa ya msingi na madarasa yanayotokana nayo { #super-and-subclasses }

Habari tena.

////

//// tab | Maelezo

Kanuni pekee ya lazima kwa vichwa ni kwamba LLM iache sehemu ya hash iliyo ndani ya mabano ya mawimbi bila kubadilishwa, jambo linalohakikisha kwamba viungo haviathiriki.

Tazama sehemu ya `### Headings` katika prompt ya jumla katika `scripts/translate.py`.

Kwa baadhi ya maagizo maalumu ya lugha, tazama, kwa mfano, sehemu ya `### Headings` katika `docs/de/llm-prompt.md`.

////

## Istilahi zinazotumiwa katika nyaraka { #terms-used-in-the-docs }

//// tab | Jaribio

* wewe
* yako

* k.m.
* n.k.

* `foo` kama `int`
* `bar` kama `str`
* `baz` kama `list`

* Mafunzo - Mwongozo wa Mtumiaji
* Mwongozo wa Mtumiaji wa Kiwango cha Juu
* nyaraka za SQLModel
* nyaraka za API
* nyaraka zinazozalishwa kiotomatiki

* Sayansi ya Data
* Ujifunzaji wa Kina
* Ujifunzaji wa Mashine
* Uingizaji wa Vitegemezi
* uthibitishaji wa utambulisho wa HTTP Basic
* HTTP Digest
* umbizo la ISO
* kiwango cha JSON Schema
* schema ya JSON
* ufafanuzi wa schema
* Mtiririko wa Nenosiri
* Simu za mkononi

* iliyopitwa na wakati na isiyopendekezwa tena
* iliyoundwa
* isiyo halali
* wakati wa utekelezaji
* ya kawaida
* ya chaguo-msingi
* inayotofautisha herufi kubwa na ndogo
* isiyotofautisha herufi kubwa na ndogo

* kuendesha programu ili ipatikane kwa watumiaji
* kutoa ukurasa kwa mteja

* app
* programu

* ombi
* jibu
* jibu la hitilafu

* operesheni ya njia
* decorator ya operesheni ya njia
* function ya operesheni ya njia

* mwili
* mwili wa ombi
* mwili wa jibu
* mwili wa JSON
* mwili wa fomu
* mwili wa faili
* mwili wa function

* kigezo
* kigezo cha mwili
* kigezo cha njia
* kigezo cha query
* kigezo cha cookie
* kigezo cha kichwa
* kigezo cha fomu
* kigezo cha function

* tukio
* tukio la kuanza
* kuanza kwa seva
* tukio la kuzimwa
* tukio la muda wa uhai

* kishughulikiaji
* kishughulikiaji cha tukio
* kishughulikiaji cha exception
* kushughulikia

* modeli
* modeli ya Pydantic
* modeli ya data
* modeli ya hifadhidata
* modeli ya fomu
* objekti ya modeli

* darasa
* darasa la msingi
* darasa mzazi
* darasa linalotokana na darasa jingine
* darasa mtoto
* darasa lenye mzazi yuleyule
* method ya darasa

* kichwa
* vichwa
* kichwa cha uidhinishaji
* kichwa cha `Authorization`
* kichwa kilichopitishwa

* mfumo wa uingizaji wa vitegemezi
* kitegemezi
* kinachoweza kutegemewa
* kinachotegemea kingine

* I/O bound
* CPU bound
* concurrency
* parallelism
* multiprocessing

* env var
* kigeu cha mazingira
* `PATH`
* kigeu cha `PATH`

* uthibitishaji wa utambulisho
* mtoa huduma ya uthibitishaji wa utambulisho
* uidhinishaji
* fomu ya uidhinishaji
* mtoa huduma ya uidhinishaji
* mtumiaji anathibitisha utambulisho wake
* mfumo unathibitisha utambulisho wa mtumiaji

* CLI
* kiolesura cha mstari wa amri

* seva
* mteja

* mtoa huduma za wingu
* huduma ya wingu

* uundaji wa programu
* hatua za uundaji wa programu

* dict
* kamusi
* enumeration
* enum
* mwanachama wa enum

* kisimbaji
* kisimbuaji
* kusimba
* kusimbua

* exception
* kuibua exception

* expression
* statement

* frontend
* backend

* mjadala wa GitHub
* suala la GitHub

* utendaji
* uboreshaji wa utendaji

* aina ya thamani inayorudishwa
* thamani inayorudishwa

* usalama
* mpango wa usalama

* kazi
* kazi ya chinichini
* function ya kazi

* kiolezo
* injini ya violezo

* kiashirio cha aina
* kidokezo cha aina

* worker wa seva
* worker wa Uvicorn
* Worker wa Gunicorn
* mchakato wa worker
* darasa la worker
* mzigo wa kazi

* uwekaji wa programu ili iweze kuendeshwa
* kuweka programu ili iweze kuendeshwa

* SDK
* zana za uundaji wa programu

* `APIRouter`
* `requirements.txt`
* Tokeni ya Bearer
* mabadiliko yanayovunja utangamano
* hitilafu ya programu
* kitufe
* callable
* msimbo
* commit
* kidhibiti cha muktadha
* coroutine
* kipindi cha hifadhidata
* diski
* kikoa
* injini
* X bandia
* mbinu ya HTTP GET
* kipengee
* maktaba
* muda wa uhai
* kufuli
* middleware
* programu ya simu
* moduli
* mounting
* mtandao
* asili
* ubatilishaji
* payload
* kichakataji
* sifa
* seva wakilishi
* pull request
* query
* RAM
* mashine ya mbali
* msimbo wa hali
* mfuatano wa herufi
* lebo
* framework ya wavuti
* wildcard
* kurudisha
* kuhakiki uhalali

////

//// tab | Maelezo

Hii si orodha kamili wala orodha inayoweka kanuni za istilahi (nyingi zikiwa za kiufundi) zinazopatikana katika nyaraka. Inaweza kumsaidia mbunifu wa prompt kubaini istilahi ambazo LLM inahitaji msaada nazo. Kwa mfano, inapozidi kubadilisha tafsiri nzuri na kuirudisha kwenye tafsiri isiyo nzuri sana. Au inapokuwa na matatizo ya kunyambua au kupatanisha kisarufi istilahi katika lugha yako.

Tazama, kwa mfano, sehemu ya `### List of English terms and their preferred German translations` katika `docs/de/llm-prompt.md`.

////
