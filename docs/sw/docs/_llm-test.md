# Faili ya majaribio ya LLM { #llm-test-file }

Hati hii inajaribu kama <abbr title="Large Language Model - Modeli Kubwa ya Lugha">LLM</abbr>, inayotafsiri nyaraka, inaelewa `general_prompt` katika `scripts/translate.py` na prompt mahususi ya lugha katika `docs/{language code}/llm-prompt.md`. Prompt mahususi ya lugha huongezwa mwishoni mwa `general_prompt`.

Majaribio yanayoongezwa hapa yataonekana kwa wabunifu wote wa prompt mahususi za lugha.

Tumia kama ifuatavyo:

* Kuwa na prompt mahususi ya lugha - `docs/{language code}/llm-prompt.md`.
* Tafsiri hati hii upya katika lugha unayotaka (tazama, kwa mfano, amri ya `translate-page` ya `translate.py`). Hii itaunda tafsiri katika `docs/{language code}/docs/_llm-test.md`.
* Kagua kama mambo yako sawa katika tafsiri.
* Ikihitajika, boresha prompt yako mahususi ya lugha, prompt ya jumla, au hati ya Kiingereza.
* Kisha rekebisha mwenyewe matatizo yaliyosalia katika tafsiri, ili iwe tafsiri nzuri.
* Tafsiri tena, huku tafsiri nzuri ikiwa tayari ipo. Matokeo bora yangekuwa kwamba LLM haibadilishi tena chochote katika tafsiri. Hiyo inamaanisha kwamba prompt ya jumla na prompt yako mahususi ya lugha ni bora kadiri inavyowezekana (Wakati mwingine itafanya mabadiliko machache yanayoonekana kuwa ya nasibu, sababu ikiwa kwamba [LLM si algoriti zinazotoa matokeo yale yale kila wakati kwa ingizo lile lile](https://doublespeak.chat/#/handbook#deterministic-output)).

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

Huenda LLM ikatafsiri hili vibaya. Kinachovutia ni kama itahifadhi tafsiri iliyorekebishwa wakati wa kutafsiri tena.

///

////

//// tab | Maelezo

Mbunifu wa prompt anaweza kuchagua kama anataka kubadilisha alama za kunukuu zilizonyooka kuwa alama za kunukuu za kitipografia. Ni sawa kuziacha kama zilivyo.

Kwa mfano, tazama sehemu ya `### Quotes` katika `docs/de/llm-prompt.md`.

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
// Unda directory "Code"
$ mkdir code
// Ingia katika directory hiyo
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

Msimbo ndani ya vitalu vya msimbo haupaswi kubadilishwa, isipokuwa maoni.

Tazama sehemu ya `### Content of code blocks` katika prompt ya jumla katika `scripts/translate.py`.

////

## Tab na visanduku vyenye rangi { #tabs-and-colored-boxes }

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

Tab na vitalu vya `Info`/`Note`/`Warning`/n.k. vinapaswa kuongezewa tafsiri ya kichwa chake baada ya mstari wima (`|`).

Tazama sehemu za `### Special blocks` na `### Tab blocks` katika prompt ya jumla katika `scripts/translate.py`.

////

## Viungo vya wavuti na vya ndani { #web-and-internal-links }

//// tab | Jaribio

Maandishi ya kiungo yanapaswa kutafsiriwa, anwani ya kiungo inapaswa kubaki bila kubadilishwa:

* [Kiungo cha kichwa kilicho hapo juu](#code-snippets)
* [Kiungo cha ndani](index.md#installation)
* [Kiungo cha nje](https://sqlmodel.tiangolo.com/)
* [Kiungo cha style](https://fastapi.tiangolo.com/css/styles.css)
* [Kiungo cha script](https://fastapi.tiangolo.com/js/logic.js)
* [Kiungo cha picha](https://fastapi.tiangolo.com/img/foo.jpg)

Maandishi ya kiungo yanapaswa kutafsiriwa, anwani ya kiungo inapaswa kuelekeza kwenye tafsiri:

* [Kiungo cha FastAPI](https://fastapi.tiangolo.com/sw/)

////

//// tab | Maelezo

Viungo vinapaswa kutafsiriwa, lakini anwani zake zinapaswa kubaki bila kubadilishwa. Isipokuwa ni viungo kamili vya kurasa za nyaraka za FastAPI. Katika hali hiyo, kiungo kinapaswa kuelekeza kwenye tafsiri.

Tazama sehemu ya `### Links` katika prompt ya jumla katika `scripts/translate.py`.

////

## Elementi za HTML za "abbr" { #html-abbr-elements }

//// tab | Jaribio

Hapa kuna baadhi ya vitu vilivyowekwa ndani ya elementi za HTML za "abbr" (Baadhi vimebuniwa):

### Abbr inatoa kishazi kamili { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done - Kukamilisha Mambo">GTD</abbr>
* <abbr title="less than - ndogo kuliko"><code>lt</code></abbr>
* <abbr title="XML Web Token - Tokeni ya Wavuti ya XML">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface - Interface ya Gateway ya Server za Parallel">PSGI</abbr>

### Abbr inatoa kishazi kamili na ufafanuzi { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network - Mtandao wa Wasanidi Programu wa Mozilla: nyaraka za wasanidi programu, zilizoandikwa na watu wa Firefox">MDN</abbr>
* <abbr title="Input/Output - Ingizo/Tokeo: kusoma au kuandika kwenye disk, mawasiliano ya mtandao.">I/O</abbr>.

////

//// tab | Maelezo

Sifa za "title" za elementi za "abbr" hutafsiriwa kwa kufuata maagizo fulani mahususi.

Tafsiri zinaweza kuongeza elementi zao za "abbr" ambazo LLM haipaswi kuondoa. Kwa mfano, ili kufafanua maneno ya Kiingereza.

Tazama sehemu ya `### HTML abbr elements` katika prompt ya jumla katika `scripts/translate.py`.

////

## Elementi za HTML za "dfn" { #html-dfn-elements }

* <dfn title="Kundi la mashine zilizosanidiwa ili ziunganishwe na kufanya kazi pamoja kwa namna fulani.">cluster</dfn>
* <dfn title="Mbinu ya machine learning inayotumia mitandao bandia ya neva yenye tabaka nyingi zilizofichwa kati ya tabaka za ingizo na tokeo, na hivyo kujenga muundo wa ndani wa kina">Deep Learning</dfn>

## Vichwa { #headings }

//// tab | Jaribio

### Unda programu ya wavuti - mafunzo { #develop-a-webapp-a-tutorial }

Habari.

### Type hints na type annotations { #type-hints-and-annotations }

Habari tena.

### Superclass na subclass { #super-and-subclasses }

Habari tena.

////

//// tab | Maelezo

Kanuni pekee ya lazima kwa vichwa ni kwamba LLM iachie sehemu ya hash iliyo ndani ya mabano yaliyopinda bila kuibadilisha, ili kuhakikisha kwamba viungo vinaendelea kufanya kazi.

Tazama sehemu ya `### Headings` katika prompt ya jumla katika `scripts/translate.py`.

Kwa baadhi ya maagizo mahususi ya lugha, tazama, kwa mfano, sehemu ya `### Headings` katika `docs/de/llm-prompt.md`.

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
* Mwongozo wa Kina wa Mtumiaji
* nyaraka za SQLModel
* nyaraka za API
* nyaraka zinazozalishwa kiotomatiki

* Sayansi ya Data
* Deep Learning
* Machine Learning
* Dependency Injection
* uthibitishaji wa utambulisho wa HTTP Basic
* HTTP Digest
* umbizo la ISO
* kiwango cha JSON Schema
* schema ya JSON
* ufafanuzi wa schema
* Password Flow
* Mobile

* imepitwa na wakati na matumizi yake hayapendekezwi tena
* imebuniwa
* si halali
* papo hapo wakati wa utekelezaji
* kiwango
* default
* inatofautisha herufi kubwa na ndogo
* haitofautishi herufi kubwa na ndogo

* kuhudumia programu
* kuhudumia ukurasa

* app
* programu

* request
* response
* response ya hitilafu

* path operation
* decorator ya path operation
* function ya path operation

* body
* body ya request
* body ya response
* body ya JSON
* body ya form
* body ya faili
* body ya function

* kigezo
* kigezo cha body
* kigezo cha path
* kigezo cha query
* kigezo cha cookie
* kigezo cha header
* kigezo cha form
* kigezo cha function

* event
* event ya kuanza
* kuanza kwa server
* event ya kuzima
* event ya lifespan

* handler
* handler ya event
* handler ya exception
* kushughulikia

* model
* model ya Pydantic
* model ya data
* model ya database
* model ya form
* object ya model

* class
* base class
* parent class
* subclass
* child class
* sibling class
* method ya class

* header
* headers
* header ya uidhinishaji
* header ya `Authorization`
* header iliyopitishwa

* mfumo wa dependency injection
* kitegemezi
* dependable
* kinachotegemea kitegemezi

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
* form ya uidhinishaji
* mtoa huduma ya uidhinishaji
* mtumiaji anathibitisha utambulisho wake
* mfumo unathibitisha utambulisho wa mtumiaji

* CLI
* interface ya mstari wa amri

* server
* client

* mtoa huduma za cloud
* huduma ya cloud

* uundaji wa programu
* hatua za uundaji wa programu

* dict
* dictionary
* enumeration
* enum
* member wa enum

* encoder
* decoder
* kusimba
* kusimbua

* exception
* kuibua exception

* expression
* statement

* frontend
* backend

* mjadala wa GitHub
* issue ya GitHub

* utendaji
* uboreshaji wa utendaji

* type ya thamani inayorejeshwa
* thamani inayorejeshwa

* usalama
* scheme ya usalama

* task
* task ya background
* function ya task

* template
* engine ya template

* type annotation
* type hint

* worker wa server
* worker wa Uvicorn
* Worker wa Gunicorn
* process ya worker
* class ya worker
* workload

* uwekaji wa programu ili iweze kuendeshwa
* kuweka programu ili iweze kuendeshwa

* SDK
* zana za uundaji wa programu

* `APIRouter`
* `requirements.txt`
* Bearer Token
* mabadiliko yanayovunja utangamano
* bug
* button
* callable
* msimbo
* commit
* context manager
* coroutine
* session ya database
* disk
* domain
* engine
* X bandia
* method ya HTTP GET
* item
* library
* lifespan
* lock
* middleware
* programu ya kifaa cha mkononi
* module
* mounting
* mtandao
* origin
* override
* payload
* processor
* property
* proxy
* pull request
* query
* RAM
* mashine ya mbali
* status code
* string
* tag
* framework ya wavuti
* wildcard
* kurejesha
* kuhakiki uhalali

////

//// tab | Maelezo

Hii si orodha kamili wala orodha inayoweka kanuni za istilahi (nyingi zikiwa za kiufundi) zinazopatikana katika nyaraka. Inaweza kumsaidia mbunifu wa prompt kutambua istilahi ambazo LLM inahitaji kusaidiwa nazo. Kwa mfano, inapoendelea kubadilisha tafsiri nzuri na kuirudisha kwenye tafsiri isiyo nzuri sana. Au inapopata matatizo ya kunyambua neno au kubadilisha umbo lake kisarufi katika lugha yako.

Kwa mfano, tazama sehemu ya `### List of English terms and their preferred German translations` katika `docs/de/llm-prompt.md`.

////
