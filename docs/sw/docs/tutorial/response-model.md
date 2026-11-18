# Response Model - Return Type { #response-model-return-type }

Unaweza kutangaza type inayotumiwa kwa response kwa kuongeza annotation ya **return type** kwenye *path operation function*.

Unaweza kutumia **type annotations** kama unavyofanya kwa data ya ingizo katika **vigezo** vya function; unaweza kutumia model za Pydantic, list, dictionary, thamani za scalar kama integer, boolean, n.k.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

FastAPI itatumia return type hii kufanya yafuatayo:

* **Kuhakiki uhalali** wa data inayorejeshwa.
    * Ikiwa data si halali (k.m. field inakosekana), inamaanisha kuwa msimbo wa programu *yako* una hitilafu na haurejeshi unachopaswa kurejesha. Itarejesha hitilafu ya server badala ya kurejesha data isiyo sahihi. Kwa njia hii, wewe na client zako mnaweza kuwa na uhakika kwamba zitapokea data inayotarajiwa katika muundo unaotarajiwa.
* Kuongeza **JSON Schema** ya response katika *path operation* ya OpenAPI.
    * Itatumiwa na **nyaraka zinazozalishwa kiotomatiki**.
    * Pia itatumiwa na zana za kuzalisha msimbo wa client kiotomatiki.
* Kufanya **serialization** ya data inayorejeshwa kwenda JSON kwa kutumia Pydantic, iliyoandikwa kwa **Rust**, hivyo itakuwa **ya kasi zaidi**.

Lakini muhimu zaidi:

* Itaweka **mipaka na kufanya filtering** ya data ya matokeo ili ibaki tu ile iliyofafanuliwa katika return type.
    * Hili ni muhimu hasa kwa **usalama**; tutaona zaidi kuhusu hilo hapa chini.

## Kigezo cha `response_model` { #response-model-parameter }

Kuna hali ambapo unahitaji au unataka kurejesha data ambayo hailingani kabisa na kile ambacho type inatangaza.

Kwa mfano, unaweza kutaka **kurejesha dictionary** au object ya database, lakini **uitangaze kama model ya Pydantic**. Kwa njia hii, model ya Pydantic itashughulikia uandishi wote wa nyaraka za data, uhakiki wa uhalali, n.k. kwa object uliyorejesha (k.m. dictionary au object ya database).

Ukiweka annotation ya return type, zana na editor zitaonyesha hitilafu (iliyo sahihi) inayokuambia kuwa function yako inarejesha type (k.m. dict) ambayo ni tofauti na uliyotangaza (k.m. model ya Pydantic).

Katika hali hizo, unaweza kutumia kigezo cha `response_model` cha *path operation decorator* badala ya return type.

Unaweza kutumia kigezo cha `response_model` katika *path operation* yoyote:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* n.k.

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | Kumbuka

Tambua kwamba `response_model` ni kigezo cha method ya "decorator" (`get`, `post`, n.k.). Si cha *path operation function* yako, kama vilivyo vigezo vingine vyote na body.

///

`response_model` hupokea type ileile ambayo ungetangaza kwa field ya model ya Pydantic. Kwa hiyo, inaweza kuwa model ya Pydantic, lakini pia inaweza kuwa, kwa mfano, `list` ya model za Pydantic, kama `List[Item]`.

FastAPI itatumia `response_model` hii kushughulikia uandishi wote wa nyaraka za data, uhakiki wa uhalali, n.k. na pia **kubadilisha na kufanya filtering ya data ya matokeo** ili ilingane na type iliyotangazwa.

/// tip | Kidokezo

Ikiwa una ukaguzi mkali wa type katika editor yako, mypy, n.k., unaweza kutangaza return type ya function kuwa `Any`.

Kwa njia hiyo, unaiambia editor kwamba unarejesha chochote kwa makusudi. Lakini FastAPI bado itashughulikia uandishi wa nyaraka za data, uhakiki wa uhalali, filtering, n.k. kwa kutumia `response_model`.

///

### Kipaumbele cha `response_model` { #response-model-priority }

Ukitangaza return type na pia `response_model`, `response_model` itapewa kipaumbele na kutumiwa na FastAPI.

Kwa njia hii, unaweza kuongeza type annotations sahihi kwenye function zako hata unaporejesha type iliyo tofauti na response model, ili zitumiwe na editor na zana kama mypy. Na bado unaweza kuifanya FastAPI ihakiki uhalali wa data, iandike nyaraka, n.k. kwa kutumia `response_model`.

Unaweza pia kutumia `response_model=None` kuzima uundaji wa response model kwa *path operation* hiyo. Huenda ukahitaji kufanya hivyo ikiwa unaongeza type annotations kwa vitu ambavyo si field halali za Pydantic; utaona mfano wa hilo katika mojawapo ya sehemu zilizo hapa chini.

## Rejesha data ileile ya ingizo { #return-the-same-input-data }

Hapa tunatangaza model ya `UserIn`, ambayo itakuwa na password katika plaintext:

{* ../../docs_src/response_model/tutorial002_py310.py hl[7,9] *}

/// note | Kumbuka

Ili kutumia `EmailStr`, kwanza sakinisha [`email-validator`](https://github.com/JoshData/python-email-validator).

Iongeze kwenye mradi wako:

```console
$ uv add email-validator
```

au kwa kutumia:

```console
$ uv add "pydantic[email]"
```

///

Na tunatumia model hii kutangaza ingizo letu na model hiyo hiyo kutangaza matokeo yetu:

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

Sasa, kila browser inapounda mtumiaji mwenye password, API itarejesha password hiyo hiyo kwenye response.

Katika hali hii, huenda isiwe tatizo, kwa sababu ni mtumiaji yuleyule anayetuma password.

Lakini tukitumia model hiyo hiyo kwa *path operation* nyingine, tunaweza kuwa tunatuma password za watumiaji wetu kwa kila client.

/// danger | Hatari

Kamwe usihifadhi password ya mtumiaji katika plaintext wala kuituma kwenye response namna hii, isipokuwa kama unajua tahadhari zote na unaelewa unachofanya.

///

## Ongeza model ya matokeo { #add-an-output-model }

Badala yake, tunaweza kuunda model ya ingizo yenye password katika plaintext na model ya matokeo isiyo nayo:

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

Hapa, ingawa *path operation function* yetu inarejesha data ileile ya mtumiaji iliyotolewa kama ingizo na iliyo na password:

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

...tumetangaza `response_model` kuwa model yetu ya `UserOut`, ambayo haina password:

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

Kwa hiyo, **FastAPI** itashughulikia kuondoa data yote ambayo haijatangazwa katika model ya matokeo (kwa kutumia Pydantic).

### `response_model` au Return Type { #response-model-or-return-type }

Katika hali hii, kwa sababu model hizi mbili ni tofauti, tukiweka annotation ya return type ya function kuwa `UserOut`, editor na zana zitaonyesha kuwa tunarejesha type isiyo halali, kwa kuwa hizo ni class tofauti.

Ndiyo sababu katika mfano huu tunapaswa kuitangaza katika kigezo cha `response_model`.

...lakini endelea kusoma hapa chini uone jinsi ya kutatua hilo.

## Return Type na Filtering ya Data { #return-type-and-data-filtering }

Tuendelee kutoka kwenye mfano uliotangulia. Tulitaka **kuweka annotation ya type moja kwenye function**, lakini tulitaka kuweza kurejesha kutoka kwenye function kitu ambacho kwa kweli kina **data zaidi**.

Tunataka FastAPI iendelee **kufanya filtering** ya data kwa kutumia response model. Hivyo, ingawa function inarejesha data zaidi, response itajumuisha tu field zilizotangazwa katika response model.

Katika mfano uliotangulia, kwa sababu class zilikuwa tofauti, tulilazimika kutumia kigezo cha `response_model`. Lakini hilo pia linamaanisha kuwa hatupati usaidizi wa editor na zana zinazokagua return type ya function.

Hata hivyo, katika hali nyingi ambapo tunahitaji kufanya jambo kama hili, tunataka model **ifanye filtering/iondoe** tu baadhi ya data kama katika mfano huu.

Na katika hali hizo, tunaweza kutumia class na inheritance ili kunufaika na **type annotations** za function kwa kupata usaidizi bora zaidi katika editor na zana, na bado kupata **filtering ya data** ya FastAPI.

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

Kwa hili, tunapata usaidizi wa zana, kutoka kwa editor na mypy, kwa kuwa msimbo huu ni sahihi kwa upande wa type, lakini pia tunapata filtering ya data kutoka FastAPI.

Hili linafanyaje kazi? Hebu tulichunguze. 🤓

### Type Annotations na Zana { #type-annotations-and-tooling }

Kwanza tuone jinsi editor, mypy na zana nyingine zitakavyoliona hili.

`BaseUser` ina field za msingi. Kisha `UserIn` inatumia inheritance kutoka `BaseUser` na kuongeza field ya `password`, kwa hiyo itajumuisha field zote kutoka kwenye model zote mbili.

Tunaweka annotation ya return type ya function kuwa `BaseUser`, lakini kwa kweli tunarejesha instance ya `UserIn`.

Editor, mypy na zana nyingine hazitaonyesha hitilafu kuhusu hili kwa sababu, kwa upande wa typing, `UserIn` ni subclass ya `BaseUser`, ambayo inamaanisha kuwa ni type *halali* wakati kinachotarajiwa ni chochote ambacho ni `BaseUser`.

### Filtering ya Data ya FastAPI { #fastapi-data-filtering }

Sasa, kwa upande wa FastAPI, itaangalia return type na kuhakikisha kuwa unachorejesha kinajumuisha **tu** field zilizotangazwa katika type hiyo.

FastAPI hufanya mambo kadhaa ndani yake kwa kutumia Pydantic kuhakikisha kwamba sheria hizo hizo za class inheritance hazitumiwi kwa filtering ya data inayorejeshwa; vinginevyo, unaweza kuishia kurejesha data nyingi zaidi kuliko ulivyotarajia.

Kwa njia hii, unaweza kupata manufaa ya pande zote mbili: type annotations zenye **usaidizi wa zana** na **filtering ya data**.

## Ione katika nyaraka { #see-it-in-the-docs }

Unapoangalia nyaraka zinazozalishwa kiotomatiki, unaweza kuthibitisha kuwa model ya ingizo na model ya matokeo kila moja itakuwa na JSON Schema yake:

<img src="/img/tutorial/response-model/image01.png">

Na model zote mbili zitatumiwa kwa nyaraka shirikishi za API:

<img src="/img/tutorial/response-model/image02.png">

## Annotations Nyingine za Return Type { #other-return-type-annotations }

Huenda kukawa na hali ambapo unarejesha kitu ambacho si field halali ya Pydantic na kukiwekea annotation katika function, ili tu kupata usaidizi unaotolewa na zana (editor, mypy, n.k.).

### Rejesha Response Moja kwa Moja { #return-a-response-directly }

Hali inayotokea mara nyingi zaidi ni [kurejesha Response moja kwa moja kama inavyoelezwa baadaye katika nyaraka za kiwango cha juu](../advanced/response-directly.md).

{* ../../docs_src/response_model/tutorial003_02_py310.py hl[8,10:11] *}

Hali hii rahisi inashughulikiwa kiotomatiki na FastAPI kwa sababu annotation ya return type ni class ya `Response` (au subclass yake).

Na zana pia hazitaonyesha hitilafu kwa sababu `RedirectResponse` na `JSONResponse` zote mbili ni subclass za `Response`, kwa hiyo type annotation ni sahihi.

### Weka Annotation ya Subclass ya Response { #annotate-a-response-subclass }

Unaweza pia kutumia subclass ya `Response` katika type annotation:

{* ../../docs_src/response_model/tutorial003_03_py310.py hl[8:9] *}

Hili pia litafanya kazi kwa sababu `RedirectResponse` ni subclass ya `Response`, na FastAPI itashughulikia hali hii rahisi kiotomatiki.

### Annotations za Return Type Zisizo Halali { #invalid-return-type-annotations }

Lakini unaporejesha object nyingine yoyote ambayo si type halali ya Pydantic (k.m. object ya database) na kuiwekea annotation hivyo katika function, FastAPI itajaribu kuunda response model ya Pydantic kutoka kwenye type annotation hiyo, na itashindwa.

Hilo hilo litatokea ukiwa na kitu kama <dfn title='Union ya type nyingi inamaanisha "type yoyote kati ya hizi".'>union</dfn> ya type tofauti ambapo moja au zaidi kati yazo si type halali za Pydantic. Kwa mfano, hili litashindwa 💥:

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

...hili linashindwa kwa sababu type annotation si type ya Pydantic na wala si class moja tu ya `Response` au subclass yake; ni union (yoyote kati ya hizo mbili) ya `Response` na `dict`.

### Zima Response Model { #disable-response-model }

Tukiendelea kutoka kwenye mfano hapo juu, huenda usitake uhakiki wa uhalali wa data, uandishi wa nyaraka, filtering, n.k. unaofanywa na FastAPI kwa chaguo-msingi.

Lakini huenda bado ukataka kuweka annotation ya return type katika function ili kupata usaidizi kutoka kwa zana kama editor na type checker (k.m. mypy).

Katika hali hii, unaweza kuzima uzalishaji wa response model kwa kuweka `response_model=None`:

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

Hili litaifanya FastAPI iruke uzalishaji wa response model, na kwa njia hiyo unaweza kuwa na annotations zozote za return type unazohitaji bila kuathiri programu yako ya FastAPI. 🤓

## Vigezo vya encoding vya Response Model { #response-model-encoding-parameters }

Response model yako inaweza kuwa na thamani za chaguo-msingi, kama:

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None` (au `str | None = None` katika Python 3.10) ina thamani ya chaguo-msingi ya `None`.
* `tax: float = 10.5` ina thamani ya chaguo-msingi ya `10.5`.
* `tags: List[str] = []` ina thamani ya chaguo-msingi ya list tupu: `[]`.

lakini huenda ukataka kutozijumuisha katika matokeo ikiwa hazikuhifadhiwa kwa kweli.

Kwa mfano, ikiwa una model zenye attribute nyingi zisizo za lazima katika database ya NoSQL, lakini hutaki kutuma response ndefu sana za JSON zilizojaa thamani za chaguo-msingi.

### Tumia kigezo cha `response_model_exclude_unset` { #use-the-response-model-exclude-unset-parameter }

Unaweza kuweka kigezo cha *path operation decorator* kuwa `response_model_exclude_unset=True`:

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

na thamani hizo za chaguo-msingi hazitajumuishwa katika response; zitajumuishwa tu thamani zilizowekwa kwa kweli.

Kwa hiyo, ukituma request kwa *path operation* hiyo kwa item yenye ID `foo`, response (bila kujumuisha thamani za chaguo-msingi) itakuwa:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// note | Kumbuka

Unaweza pia kutumia:

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

kama ilivyoelezwa katika [nyaraka za Pydantic](https://pydantic.dev/docs/validation/latest/concepts/serialization/#excluding-and-including-fields-based-on-their-value) kwa `exclude_defaults` na `exclude_none`.

///

#### Data yenye thamani za field zilizo na chaguo-msingi { #data-with-values-for-fields-with-defaults }

Lakini ikiwa data yako ina thamani za field za model zilizo na thamani za chaguo-msingi, kama item yenye ID `bar`:

<!-- fmt:off -->
```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```
<!-- fmt:on -->

zitajumuishwa katika response.

#### Data yenye thamani sawa na za chaguo-msingi { #data-with-the-same-values-as-the-defaults }

Ikiwa data ina thamani sawa na zile za chaguo-msingi, kama item yenye ID `baz`:

<!-- fmt:off -->
```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```
<!-- fmt:on -->

FastAPI ina uwezo wa kutambua (kwa kweli, Pydantic ndiyo yenye uwezo huo) kwamba, ingawa `description`, `tax`, na `tags` zina thamani sawa na za chaguo-msingi, ziliwekwa waziwazi (badala ya kuchukuliwa kutoka kwenye chaguo-msingi).

Kwa hiyo, zitajumuishwa katika response ya JSON.

/// tip | Kidokezo

Tambua kwamba thamani za chaguo-msingi zinaweza kuwa chochote, si `None` tu.

Zinaweza kuwa list (`[]`), `float` ya `10.5`, n.k.

///

### `response_model_include` na `response_model_exclude` { #response-model-include-and-response-model-exclude }

Unaweza pia kutumia vigezo vya *path operation decorator* vya `response_model_include` na `response_model_exclude`.

Vinapokea `set` ya `str` yenye majina ya attribute za kujumuisha (bila kujumuisha zilizobaki) au za kutojumuisha (huku zikijumuisha zilizobaki).

Hii inaweza kutumiwa kama njia ya mkato ya haraka ikiwa una model moja tu ya Pydantic na unataka kuondoa baadhi ya data kwenye matokeo.

/// tip | Kidokezo

Lakini bado inapendekezwa kutumia mbinu zilizo hapo juu, kwa kutumia class nyingi, badala ya vigezo hivi.

Hii ni kwa sababu JSON Schema inayozalishwa katika OpenAPI ya programu yako (na nyaraka) bado itakuwa ya model kamili, hata ukitumia `response_model_include` au `response_model_exclude` kutojumuisha baadhi ya attribute.

Hili pia linatumika kwa `response_model_by_alias`, ambayo hufanya kazi kwa namna inayofanana.

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | Kidokezo

Syntax ya `{"name", "description"}` huunda `set` yenye thamani hizo mbili.

Ni sawa na `set(["name", "description"])`.

///

#### Kutumia `list` badala ya `set` { #using-lists-instead-of-sets }

Ukisahau kutumia `set` na badala yake ukatumia `list` au `tuple`, FastAPI bado itaibadilisha kuwa `set` na itafanya kazi kwa usahihi:

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## Muhtasari { #recap }

Tumia kigezo cha `response_model` cha *path operation decorator* kufafanua response model, na hasa kuhakikisha kwamba data ya faragha inaondolewa.

Tumia `response_model_exclude_unset` kurejesha tu thamani zilizowekwa waziwazi.
