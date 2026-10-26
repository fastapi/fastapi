---
include_yaml:
  sponsors: data/sponsors.yml
---

# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/sw"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>Framework ya FastAPI, yenye utendaji wa juu, rahisi kujifunza, ya haraka kuandika msimbo, tayari kwa matumizi halisi</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Majaribio">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Kiwango cha msimbo unaopimwa">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Toleo la kifurushi">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Matoleo ya Python yanayoungwa mkono">
</a>
</p>

---

**Nyaraka**: [https://fastapi.tiangolo.com/sw](https://fastapi.tiangolo.com/sw)

**Msimbo Chanzo**: [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI ni framework ya wavuti ya kisasa, ya haraka (yenye utendaji wa juu), ya kujenga API kwa Python kwa kutumia vidokezo vya aina vya kawaida vya Python.

Vipengele vyake muhimu ni:

* **Haraka**: Utendaji wa juu sana, sawa na **NodeJS** na **Go** (shukrani kwa Starlette na Pydantic). [Mojawapo ya framework za Python zenye kasi kubwa zaidi zinazopatikana](#performance).
* **Haraka kuandika msimbo**: Ongeza kasi ya kuunda vipengele kwa takribani 200% hadi 300%. *
* **Hitilafu chache**: Punguza takribani 40% ya makosa yanayosababishwa na binadamu (waundaji wa programu). *
* **Rahisi kuelewa**: Usaidizi mzuri katika kihariri. <dfn title="pia hujulikana kama ukamilishaji otomatiki, autocompletion, IntelliSense">Ukamilishaji</dfn> kila mahali. Muda mchache wa kutafuta na kurekebisha hitilafu.
* **Rahisi**: Imebuniwa kuwa rahisi kutumia na kujifunza. Muda mchache wa kusoma nyaraka.
* **Fupi**: Punguza urudiaji wa msimbo. Vipengele vingi kutokana na kila tamko la kigezo. Hitilafu chache.
* **Imara**: Pata msimbo ulio tayari kwa matumizi halisi. Pamoja na nyaraka shirikishi zinazozalishwa kiotomatiki.
* **Inafuata viwango**: Inategemea (na inaendana kikamilifu na) viwango huria vya API: [OpenAPI](https://github.com/OAI/OpenAPI-Specification) (iliyokuwa ikijulikana kama Swagger) na [JSON Schema](https://json-schema.org/).

<small>* makadirio yanayotokana na majaribio yaliyofanywa na timu ya ndani ya uundaji wa programu, ikijenga programu kwa matumizi halisi.</small>

## Wadhamini { #sponsors }

<!-- sponsors -->

### Mdhamini Mkuu { #keystone-sponsor }

<div class="fastapi-sponsors fastapi-sponsors--keystone">
{% for sponsor in sponsors.keystone -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--keystone" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}"></a>
{% endfor -%}
</div>

### Wadhamini wa Dhahabu { #gold-sponsors }

<div class="fastapi-sponsors fastapi-sponsors--gold">
{% for sponsor in sponsors.gold -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--gold" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}" loading="lazy"></a>
{% endfor -%}
</div>

### Wadhamini wa Fedha { #silver-sponsors }

<div class="fastapi-sponsors fastapi-sponsors--silver">
{% for sponsor in sponsors.silver -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--silver" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}" loading="lazy"></a>
{% endfor %}
</div>

<!-- /sponsors -->

[Wadhamini wengine](https://fastapi.tiangolo.com/sw/fastapi-people/#sponsors)

## Maoni { #opinions }

<!-- only-mkdocs -->
<div class="fastapi-opinions" data-fastapi-opinions>
  <div class="fastapi-opinions__tabs" role="tablist" aria-label="Kampuni zinazotumia FastAPI">
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-microsoft" aria-controls="fo-panel-microsoft" aria-selected="true" tabindex="0">
      <span class="fastapi-opinions__mark"><img src="/img/logos/microsoft.svg" alt="Microsoft" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-uber" aria-controls="fo-panel-uber" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/uber.svg" alt="Uber" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-netflix" aria-controls="fo-panel-netflix" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/netflix.svg" alt="Netflix" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-cisco" aria-controls="fo-panel-cisco" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/cisco.svg" alt="Cisco" loading="lazy"></span>
    </button>
  </div>

  <div class="fastapi-opinions__panel" id="fo-panel-microsoft" role="tabpanel" aria-labelledby="fo-tab-microsoft" tabindex="0">
    <blockquote class="fastapi-opinions__quote">"Ninatumia <strong>FastAPI</strong> sana siku hizi. Kwa kweli ninapanga kuitumia kwa <strong>huduma zote za ML za timu yangu katika Microsoft</strong>. Baadhi yake zinaunganishwa kwenye bidhaa kuu ya <strong>Windows</strong> na baadhi ya bidhaa za <strong>Office</strong>."</blockquote>
    <div class="fastapi-opinions__attr">— Kabir Khan, <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26">(rejea)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-uber" role="tabpanel" aria-labelledby="fo-tab-uber" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">"Tulichagua maktaba ya <strong>FastAPI</strong> kuanzisha seva ya <strong>REST</strong> inayoweza kuulizwa ili kupata <strong>utabiri</strong>." <em>[kwa Ludwig]</em></blockquote>
    <div class="fastapi-opinions__attr">— Piero Molino, Yaroslav Dudin, Sai Sumanth Miryala, <strong>Uber</strong> <a href="https://www.uber.com/us/en/blog/ludwig-v0-2/">(rejea)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-netflix" role="tabpanel" aria-labelledby="fo-tab-netflix" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">"<strong>Netflix</strong> inafuraha kutangaza kutolewa kwa framework yetu ya uratibu wa <strong>usimamizi wa migogoro</strong> kama programu ya msimbo huria: <strong>Dispatch</strong>!" <em>[imejengwa kwa FastAPI]</em></blockquote>
    <div class="fastapi-opinions__attr">— Kevin Glisson, Marc Vilanova, Forest Monsen, <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072">(rejea)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-cisco" role="tabpanel" aria-labelledby="fo-tab-cisco" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">"Ikiwa mtu yeyote anataka kujenga API ya Python kwa matumizi halisi, ningependekeza sana <strong>FastAPI</strong>. <strong>Imebuniwa kwa ustadi</strong>, ni <strong>rahisi kutumia</strong> na <strong>ina uwezo mkubwa wa kukua kulingana na mahitaji</strong> — imekuwa <strong>sehemu muhimu</strong> ya mkakati wetu wa uundaji wa programu unaotanguliza API."</blockquote>
    <div class="fastapi-opinions__attr">— Deon Pillsbury, <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/">(rejea)</a></div>
  </div>
</div>
<!-- /only-mkdocs -->

<div class="only-github" markdown="1">

"_[...] Ninatumia **FastAPI** sana siku hizi. [...] Kwa kweli ninapanga kuitumia kwa **huduma zote za ML za timu yangu katika Microsoft**. Baadhi yake zinaunganishwa kwenye bidhaa kuu ya **Windows** na baadhi ya bidhaa za **Office**._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(rejea)</small></a></div>

---

"_Tulichagua maktaba ya **FastAPI** kuanzisha seva ya **REST** inayoweza kuulizwa ili kupata **utabiri**. [kwa Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, na Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://www.uber.com/us/en/blog/ludwig-v0-2/"><small>(rejea)</small></a></div>

---

"_**Netflix** inafuraha kutangaza kutolewa kwa framework yetu ya uratibu wa **usimamizi wa migogoro** kama programu ya msimbo huria: **Dispatch**! [imejengwa kwa **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(rejea)</small></a></div>

---

"_Ikiwa mtu yeyote anataka kujenga API ya Python kwa matumizi halisi, ningependekeza sana **FastAPI**. **Imebuniwa kwa ustadi**, ni **rahisi kutumia** na **ina uwezo mkubwa wa kukua kulingana na mahitaji**, imekuwa **sehemu muhimu** ya mkakati wetu wa uundaji wa programu unaotanguliza API na inaendesha kazi nyingi za kiotomatiki na huduma kama vile Virtual TAC Engineer yetu._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(rejea)</small></a></div>

---

</div>

## Filamu fupi ya makala kuhusu FastAPI { #fastapi-mini-documentary }

Kuna [filamu fupi ya makala kuhusu FastAPI](https://www.youtube.com/watch?v=mpR8ngthqiE) iliyotolewa mwishoni mwa 2025, unaweza kuitazama mtandaoni:

<a class="fastapi-feature-banner" href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="Filamu Fupi ya Makala kuhusu FastAPI"></a>

## **Typer**, FastAPI ya CLI { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Ikiwa unajenga programu ya <abbr title="Command Line Interface - Kiolesura cha Mstari wa Amri">CLI</abbr> itakayotumika kwenye terminal badala ya API ya wavuti, angalia [**Typer**](https://typer.tiangolo.com/).

**Typer** ni mdogo wake FastAPI. Na imekusudiwa kuwa **FastAPI ya CLI**. ⌨️ 🚀

## Mahitaji { #requirements }

FastAPI imejengwa juu ya kazi kubwa za wengine:

* [Starlette](https://starlette.dev/) kwa sehemu za wavuti.
* [Pydantic](https://pydantic.dev/docs/) kwa sehemu za data.

## Usakinishaji { #installation }

Kwanza, [sakinisha `uv`](https://docs.astral.sh/uv/getting-started/installation/), kisha ongeza FastAPI kwenye mradi wako:

<div class="termy">

```console
$ uv add "fastapi[standard]"

---> 100%
```

</div>

**Kumbuka**: Hakikisha unaweka `"fastapi[standard]"` ndani ya alama za kunukuu ili ifanye kazi katika terminal zote.

Ikiwa unapendelea kutumia `pip`, sakinisha `fastapi[standard]` ndani ya mazingira pepe. Angalia [mwongozo wa usakinishaji](tutorial/#install-fastapi) kwa hatua mbadala.

## Mfano { #example }

### Iunde { #create-it }

Unda faili `main.py` yenye:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Au tumia <code>async def</code>...</summary>

Ikiwa msimbo wako unatumia `async` / `await`, tumia `async def`:

```Python hl_lines="7  12"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

**Kumbuka**:

Ikiwa huna uhakika, angalia sehemu ya _"Una haraka?"_ kuhusu [`async` na `await` kwenye nyaraka](https://fastapi.tiangolo.com/sw/async/#in-a-hurry).

</details>

### Iendeshe { #run-it }

Endesha seva kwa:

<div class="termy">

```console
$ uv run fastapi dev

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>Kuhusu amri <code>fastapi dev</code>...</summary>

Amri `fastapi dev` husoma faili lako la `main.py` kiotomatiki, hutambua programu ya **FastAPI** iliyomo, na huanzisha seva kwa kutumia [Uvicorn](https://uvicorn.dev).

Kwa chaguo-msingi, `fastapi dev` huanza ikiwa na upakiaji upya wa kiotomatiki uliowezeshwa kwa uundaji wa programu kwenye kompyuta yako.

Unaweza kusoma zaidi kuihusu kwenye [nyaraka za FastAPI CLI](https://fastapi.tiangolo.com/sw/fastapi-cli/).

</details>

### Iangalie { #check-it }

Fungua kivinjari chako kwenye [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery).

Utaona jibu la JSON kama:

```JSON
{"item_id": 5, "q": "somequery"}
```

Tayari umeunda API ambayo:

* Inapokea maombi ya HTTP kwenye _njia_ `/` na `/items/{item_id}`.
* _Njia_ zote mbili zinakubali <em>operesheni</em> za `GET` (pia hujulikana kama _mbinu_ za HTTP).
* _Njia_ `/items/{item_id}` ina _kigezo cha njia_ `item_id` ambacho kinapaswa kuwa `int`.
* _Njia_ `/items/{item_id}` ina _kigezo cha hoja_ `q` cha hiari cha aina ya `str`.

### Nyaraka shirikishi za API { #interactive-api-docs }

Sasa nenda kwenye [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Utaona nyaraka shirikishi za API zinazozalishwa kiotomatiki (zinazotolewa na [Swagger UI](https://github.com/swagger-api/swagger-ui)):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Nyaraka mbadala za API { #alternative-api-docs }

Na sasa, nenda kwenye [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

Utaona nyaraka mbadala zinazozalishwa kiotomatiki (zinazotolewa na [ReDoc](https://github.com/Redocly/redoc)):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Kuboresha mfano { #example-upgrade }

Sasa rekebisha faili `main.py` ili lipokee mwili wa ombi la `PUT`.

Tamka mwili huo kwa kutumia aina za kawaida za Python, shukrani kwa Pydantic.

```Python hl_lines="2  7-10 23-25"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Seva ya `fastapi dev` inapaswa kupakia upya kiotomatiki.

### Kuboresha nyaraka shirikishi za API { #interactive-api-docs-upgrade }

Sasa nenda kwenye [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

* Nyaraka shirikishi za API zitasasishwa kiotomatiki, zikijumuisha mwili mpya wa ombi:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Bofya kitufe cha "Try it out", kinakuruhusu kujaza vigezo na kuingiliana moja kwa moja na API:

![Mwingiliano wa Swagger UI](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Kisha bofya kitufe cha "Execute", kiolesura cha mtumiaji kitawasiliana na API yako, kutuma vigezo, kupata matokeo na kuyaonyesha kwenye skrini:

![Mwingiliano wa Swagger UI](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Kuboresha nyaraka mbadala za API { #alternative-api-docs-upgrade }

Na sasa, nenda kwenye [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

* Nyaraka mbadala pia zitaonyesha kigezo kipya cha hoja na mwili wa ombi:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Muhtasari { #recap }

Kwa ufupi, unatamka **mara moja** aina za vigezo, mwili wa ombi, n.k. kama vigezo vya function.

Unafanya hivyo kwa kutumia aina za kawaida za kisasa za Python.

Huhitaji kujifunza sintaksia mpya, mbinu au madarasa ya maktaba fulani, n.k.

Ni **Python** ya kawaida tu.

Kwa mfano, kwa `int`:

```Python
item_id: int
```

au kwa modeli changamano zaidi ya `Item`:

```Python
item: Item
```

...na kwa tamko hilo moja unapata:

* Usaidizi wa kihariri, ukiwemo:
    * Ukamilishaji.
    * Ukaguzi wa aina.
* Uhakiki wa uhalali wa data:
    * Ujumbe wa makosa ulio wazi unaotolewa kiotomatiki data inapokuwa si halali.
    * Uhakiki hata kwa objekti za JSON zilizopachikwa ndani ya nyingine kwa kina.
* <dfn title="pia hujulikana kama: serialization, uchanganuzi, marshalling">Ubadilishaji</dfn> wa data ya ingizo: inayotoka kwenye mtandao kuwa data na aina za Python. Kusoma kutoka:
    * JSON.
    * Vigezo vya njia.
    * Vigezo vya hoja.
    * Vidakuzi.
    * Vichwa.
    * Fomu.
    * Faili.
* <dfn title="pia hujulikana kama: serialization, uchanganuzi, marshalling">Ubadilishaji</dfn> wa data ya matokeo: kubadilisha data na aina za Python kuwa data ya mtandao (kama JSON):
    * Kubadilisha aina za Python (`str`, `int`, `float`, `bool`, `list`, n.k.).
    * Objekti za `datetime`.
    * Objekti za `UUID`.
    * Modeli za hifadhidata.
    * ...na nyingine nyingi.
* Nyaraka shirikishi za API zinazozalishwa kiotomatiki, zikiwemo chaguo 2 za violesura vya mtumiaji:
    * Swagger UI.
    * ReDoc.

---

Tukirudi kwenye mfano wa msimbo uliotangulia, **FastAPI** itafanya yafuatayo:

* Kuhakiki kuwa kuna `item_id` kwenye njia kwa maombi ya `GET` na `PUT`.
* Kuhakiki kuwa `item_id` ni ya aina ya `int` kwa maombi ya `GET` na `PUT`.
    * Ikiwa sivyo, mteja ataona ujumbe wa kosa ulio wazi na wenye manufaa.
* Kukagua ikiwa kuna kigezo cha hoja cha hiari kinachoitwa `q` (kama kwenye `http://127.0.0.1:8000/items/foo?q=somequery`) kwa maombi ya `GET`.
    * Kwa kuwa kigezo cha `q` kimetamkwa na `= None`, ni cha hiari.
    * Bila `None` kingehitajika (kama mwili wa ombi unavyohitajika kwa `PUT`).
* Kwa maombi ya `PUT` kwenda `/items/{item_id}`, kusoma mwili wa ombi kama JSON:
    * Kukagua kuwa una sifa inayohitajika ya `name` ambayo inapaswa kuwa `str`.
    * Kukagua kuwa una sifa inayohitajika ya `price` ambayo lazima iwe `float`.
    * Kukagua kuwa una sifa ya hiari ya `is_offer`, ambayo inapaswa kuwa `bool`, ikiwa ipo.
    * Yote haya yangefanya kazi pia kwa objekti za JSON zilizopachikwa ndani ya nyingine kwa kina.
* Kubadilisha kutoka na kwenda JSON kiotomatiki.
* Kuandika nyaraka za kila kitu kwa OpenAPI, zinazoweza kutumiwa na:
    * Mifumo ya nyaraka shirikishi.
    * Mifumo ya kuzalisha msimbo wa mteja kiotomatiki, kwa lugha nyingi.
* Kutoa moja kwa moja violesura 2 vya wavuti vya nyaraka shirikishi.

---

Tumegusia kwa juu juu tu, lakini tayari unaelewa jinsi yote yanavyofanya kazi.

Jaribu kubadilisha mstari wenye:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...kutoka:

```Python
        ... "item_name": item.name ...
```

...kuwa:

```Python
        ... "item_price": item.price ...
```

...na uone jinsi kihariri chako kitakavyokamilisha sifa kiotomatiki na kujua aina zake:

![usaidizi wa kihariri](https://fastapi.tiangolo.com/img/vscode-completion.png)

Kwa mfano kamili zaidi unaojumuisha vipengele zaidi, angalia <a href="https://fastapi.tiangolo.com/sw/tutorial/">Mafunzo - Mwongozo wa Mtumiaji</a>.

**Dokezo la yaliyomo**: mafunzo - mwongozo wa mtumiaji unajumuisha:

* Utamkaji wa **vigezo** kutoka sehemu nyingine tofauti kama vile: **vichwa**, **vidakuzi**, **nyuga za fomu** na **faili**.
* Jinsi ya kuweka **vikwazo vya uhakiki wa uhalali** kama vile `maximum_length` au `regex`.
* Mfumo wenye uwezo mkubwa na rahisi kutumia wa **<dfn title="pia hujulikana kama vipengele, rasilimali, watoa huduma, huduma, vipengele vinavyoweza kudungwa">Udungaji wa Vitegemezi</dfn>**.
* Usalama na uthibitishaji wa utambulisho, ikiwemo usaidizi wa **OAuth2** yenye **tokeni za JWT** na uthibitishaji wa utambulisho wa **HTTP Basic**.
* Mbinu za kiwango cha juu zaidi (lakini rahisi vilevile) za kutamka **modeli za JSON zilizopachikwa ndani ya nyingine kwa kina** (shukrani kwa Pydantic).
* Uunganishaji wa **GraphQL** na [Strawberry](https://strawberry.rocks) na maktaba nyingine.
* Vipengele vingi vya ziada (shukrani kwa Starlette) kama vile:
    * **WebSockets**
    * majaribio rahisi sana yanayotumia HTTPX na `pytest`
    * **CORS**
    * **Vikao vya Vidakuzi**
    * ...na zaidi.

### Weka programu yako iweze kuendeshwa (hiari) { #deploy-your-app-optional }

Ukipenda, unaweza kuweka programu yako ya FastAPI iweze kuendeshwa kwenye [FastAPI Cloud](https://fastapicloud.com) kwa amri moja. 🚀

<div class="termy">

```console
$ uv run fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

CLI itatambua programu yako ya FastAPI kiotomatiki na kuiweka iweze kuendeshwa kwenye wingu. Ikiwa hujaingia katika akaunti yako, kivinjari chako kitafunguka ili kukamilisha mchakato wa uthibitishaji wa utambulisho.

Ni hivyo tu! Sasa unaweza kufikia programu yako kwenye URL hiyo. ✨

#### Kuhusu FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** imejengwa na mtunzi yuleyule na timu iliyounda **FastAPI**.

Inarahisisha mchakato wa **kujenga**, **kuweka iweze kuendeshwa**, na **kufikia** API kwa juhudi ndogo sana.

Inaleta **urahisi uleule kwa waundaji wa programu** wanaojenga programu kwa FastAPI kwenye mchakato wa **kuziweka ziweze kuendeshwa** kwenye wingu. 🎉

FastAPI Cloud ndiyo mdhamini mkuu na mtoa ufadhili wa miradi ya msimbo huria ya *FastAPI na marafiki*. ✨

#### Weka programu iweze kuendeshwa kwa watoa huduma wengine wa wingu { #deploy-to-other-cloud-providers }

FastAPI ni ya msimbo huria na inafuata viwango. Unaweza kuweka programu za FastAPI ziweze kuendeshwa kwa mtoa huduma yeyote wa wingu unayemchagua.

Fuata miongozo ya mtoa huduma wako wa wingu ili kuweka programu za FastAPI ziweze kuendeshwa kwake. 🤓

## Utendaji { #performance }

Vipimo huru vya utendaji vya TechEmpower vinaonyesha programu za **FastAPI** zinazoendeshwa kwa Uvicorn zikiifanya iwe [mojawapo ya framework za Python zenye kasi kubwa zaidi zinazopatikana](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7), ikizidiwa tu na Starlette na Uvicorn zenyewe (zinazotumiwa ndani ya FastAPI). (*)

Ili kuelewa zaidi kuhusu hili, angalia sehemu ya [Vipimo vya Utendaji](https://fastapi.tiangolo.com/sw/benchmarks/).

## Vitegemezi { #dependencies }

FastAPI inategemea Pydantic na Starlette.

### Vitegemezi vya `standard` { #standard-dependencies }

Unaposakinisha FastAPI kwa `uv add "fastapi[standard]"` inakuja na kundi la `standard` la vitegemezi vya hiari:

Vinavyotumiwa na Pydantic:

* [`email-validator`](https://github.com/JoshData/python-email-validator) - kwa uhakiki wa uhalali wa anwani za barua pepe.

Vinavyotumiwa na Starlette:

* [`httpx2`](https://pydantic.dev/docs/httpx2/) (au `httpx`) - Hutumiwa na `TestClient`.
* [`jinja2`](https://jinja.palletsprojects.com) - Inahitajika ikiwa unataka kutumia usanidi wa chaguo-msingi wa violezo.
* [`python-multipart`](https://github.com/Kludex/python-multipart) - Inahitajika ikiwa unataka kuwezesha <dfn title="kubadilisha mfuatano wa herufi unaotoka kwenye ombi la HTTP kuwa data ya Python">"uchanganuzi"</dfn> wa fomu, kwa `request.form()`.

Vinavyotumiwa na FastAPI:

* [`uvicorn`](https://uvicorn.dev) - kwa seva inayopakia na kuendesha programu yako ili kuhudumia maombi. Hii inajumuisha `uvicorn[standard]`, ambayo inajumuisha baadhi ya vitegemezi (k.m. `uvloop`) vinavyohitajika kwa kuhudumia maombi kwa utendaji wa juu.
* `fastapi-cli[standard]` - kutoa amri ya `fastapi`.
    * Hii inajumuisha `fastapi-cloud-cli`, ambayo inakuwezesha kuweka programu yako ya FastAPI iweze kuendeshwa kwenye [FastAPI Cloud](https://fastapicloud.com).

### Bila Vitegemezi vya `standard` { #without-standard-dependencies }

Ikiwa hutaki kujumuisha vitegemezi vya hiari vya `standard`, unaweza kusakinisha kwa `uv add fastapi` badala ya `uv add "fastapi[standard]"`.

### Bila `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

Ikiwa unataka kusakinisha FastAPI pamoja na vitegemezi vya kawaida lakini bila `fastapi-cloud-cli`, unaweza kusakinisha kwa `uv add "fastapi[standard-no-fastapi-cloud-cli]"`.

### Vitegemezi vya Ziada vya Hiari { #additional-optional-dependencies }

Kuna baadhi ya vitegemezi vya ziada ambavyo huenda ukataka kusakinisha.

Vitegemezi vya ziada vya hiari vya Pydantic:

* [`pydantic-settings`](https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/) - kwa usimamizi wa mipangilio.
* [`pydantic-extra-types`](https://github.com/pydantic/pydantic-extra-types) - kwa aina za ziada za kutumia na Pydantic.

Vitegemezi vya ziada vya hiari vya FastAPI:

* [`orjson`](https://github.com/ijl/orjson) - Inahitajika ikiwa unataka kutumia `ORJSONResponse`.
* [`ujson`](https://github.com/ultrajson/ultrajson) - Inahitajika ikiwa unataka kutumia `UJSONResponse`.

## Leseni { #license }

Mradi huu umepewa leseni chini ya masharti ya leseni ya MIT.
