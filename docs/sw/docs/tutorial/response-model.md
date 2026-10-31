# Modeli ya Jibu - Aina ya Thamani Inayorejeshwa { #response-model-return-type }

Unaweza kutangaza aina inayotumiwa kwa jibu kwa kuwekea *kitendakazi cha operesheni ya njia* **kidokezo cha aina ya thamani inayorejeshwa**.

Unaweza kutumia **vidokezo vya aina** kama unavyofanya kwa data ya ingizo katika **vigezo** vya kitendakazi; unaweza kutumia modeli za Pydantic, orodha, kamusi, thamani za skala kama vile namba kamili, thamani za boolean, n.k.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

FastAPI itatumia aina hii ya thamani inayorejeshwa kufanya yafuatayo:

* **Kuhakiki uhalali** wa data inayorejeshwa.
    * Ikiwa data si halali (k.m. kuna uga unaokosekana), inamaanisha kuwa msimbo wa programu *yako* una hitilafu, haurejeshi kinachotarajiwa, na itarejesha hitilafu ya seva badala ya kurejesha data isiyo sahihi. Kwa njia hii, wewe na wateja wa API yako mnaweza kuwa na uhakika kwamba watapokea data na muundo wa data unaotarajiwa.
* Kuongeza **JSON Schema** ya jibu katika *operesheni ya njia* ya OpenAPI.
    * Hii itatumiwa na **nyaraka zinazozalishwa kiotomatiki**.
    * Pia itatumiwa na zana zinazozalisha msimbo wa mteja kiotomatiki.
* **Kusirialisha** data inayorejeshwa kuwa JSON kwa kutumia Pydantic, ambayo imeandikwa kwa **Rust**, hivyo itakuwa **haraka zaidi**.

Lakini muhimu zaidi:

* **Itawekea mipaka na kuchuja** data ya matokeo ili ibaki ile tu iliyofafanuliwa katika aina ya thamani inayorejeshwa.
    * Hili ni muhimu hasa kwa **usalama**, tutaona zaidi kuhusu hilo hapa chini.

## Kigezo cha `response_model` { #response-model-parameter }

Kuna hali ambapo unahitaji au unataka kurejesha data ambayo hailingani kabisa na aina iliyotangazwa.

Kwa mfano, huenda ukataka **kurejesha kamusi** au objekti ya hifadhidata, lakini **uitangaze kama modeli ya Pydantic**. Kwa njia hii modeli ya Pydantic ingeshughulikia uundaji wa nyaraka zote za data, uhakiki wa uhalali, n.k. kwa objekti uliyorejesha (k.m. kamusi au objekti ya hifadhidata).

Ukiweka kidokezo cha aina ya thamani inayorejeshwa, zana na vihariri vitaonyesha hitilafu (kwa usahihi) vikikuambia kwamba kitendakazi chako kinarejesha aina (k.m. dict) ambayo ni tofauti na uliyotangaza (k.m. modeli ya Pydantic).

Katika hali hizo, unaweza kutumia kigezo cha *decorator ya operesheni ya njia* cha `response_model` badala ya aina ya thamani inayorejeshwa.

Unaweza kutumia kigezo cha `response_model` katika *operesheni yoyote ya njia*:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* n.k.

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | Kumbuka

Zingatia kwamba `response_model` ni kigezo cha method ya "decorator" (`get`, `post`, n.k.). Si cha *kitendakazi chako cha operesheni ya njia*, kama vilivyo vigezo vyote na mwili wa ombi.

///

`response_model` hupokea aina ileile ambayo ungetangaza kwa uga wa modeli ya Pydantic, hivyo inaweza kuwa modeli ya Pydantic, lakini pia inaweza kuwa, kwa mfano, `list` ya modeli za Pydantic, kama `List[Item]`.

FastAPI itatumia `response_model` hii kufanya uundaji wa nyaraka zote za data, uhakiki wa uhalali, n.k. na pia **kubadilisha na kuchuja data ya matokeo** ili ilingane na aina iliyotangazwa.

/// tip | Kidokezo

Ikiwa una ukaguzi mkali wa aina katika kihariri chako, mypy, n.k., unaweza kutangaza aina ya thamani inayorejeshwa na kitendakazi kuwa `Any`.

Kwa njia hiyo unakiambia kihariri kwamba unarejesha chochote kwa makusudi. Lakini FastAPI bado itafanya uundaji wa nyaraka za data, uhakiki wa uhalali, uchujaji, n.k. kwa kutumia `response_model`.

///

### Kipaumbele cha `response_model` { #response-model-priority }

Ukitangaza aina ya thamani inayorejeshwa pamoja na `response_model`, `response_model` itapewa kipaumbele na kutumiwa na FastAPI.

Kwa njia hii unaweza kuongeza vidokezo sahihi vya aina kwenye vitendakazi vyako hata unaporejesha aina tofauti na modeli ya jibu, ili vitumiwe na kihariri na zana kama mypy. Na bado unaweza kuifanya FastAPI ihakiki uhalali wa data, itengeneze nyaraka, n.k. kwa kutumia `response_model`.

Unaweza pia kutumia `response_model=None` kuzima uundaji wa modeli ya jibu kwa *operesheni hiyo ya njia*. Huenda ukahitaji kufanya hivyo ikiwa unaongeza vidokezo vya aina kwa vitu ambavyo si nyuga halali za Pydantic; utaona mfano wa hilo katika mojawapo ya sehemu zilizo hapa chini.

## Rejesha data ileile ya ingizo { #return-the-same-input-data }

Hapa tunatangaza modeli ya `UserIn`, ambayo itakuwa na nenosiri katika maandishi wazi:

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

Na tunatumia modeli hii kutangaza ingizo letu na modeli hiyohiyo kutangaza matokeo yetu:

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

Sasa, kila wakati kivinjari kinapounda mtumiaji mwenye nenosiri, API itarejesha nenosiri hilohilo katika jibu.

Katika hali hii, huenda lisiwe tatizo, kwa sababu ni mtumiaji yuleyule anayetuma nenosiri.

Lakini tukitumia modeli hiyohiyo kwa *operesheni nyingine ya njia*, tunaweza kuwa tunatuma manenosiri ya watumiaji wetu kwa kila mteja.

/// danger | Hatari

Kamwe usihifadhi nenosiri la mtumiaji katika maandishi wazi wala kulituma katika jibu kama hili, isipokuwa kama unajua tahadhari zote na unajua unachofanya.

///

## Ongeza modeli ya matokeo { #add-an-output-model }

Badala yake tunaweza kuunda modeli ya ingizo yenye nenosiri katika maandishi wazi na modeli ya matokeo isiyo nalo:

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

Hapa, ingawa *kitendakazi chetu cha operesheni ya njia* kinarejesha data ileile ya mtumiaji iliyoingizwa yenye nenosiri:

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

...tulitangaza `response_model` kuwa modeli yetu ya `UserOut`, ambayo haijumuishi nenosiri:

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

Kwa hiyo, **FastAPI** itashughulikia uchujaji wa kuondoa data yote ambayo haijatangazwa katika modeli ya matokeo (kwa kutumia Pydantic).

### `response_model` au Aina ya Thamani Inayorejeshwa { #response-model-or-return-type }

Katika hali hii, kwa sababu modeli hizi mbili ni tofauti, tukiwekea kitendakazi kidokezo cha aina ya thamani inayorejeshwa kuwa `UserOut`, kihariri na zana zitaonyesha hitilafu kwamba tunarejesha aina isiyo halali, kwa kuwa hizo ni class tofauti.

Ndiyo sababu katika mfano huu tunapaswa kuitangaza katika kigezo cha `response_model`.

...lakini endelea kusoma hapa chini uone jinsi ya kushinda kikwazo hicho.

## Aina ya Thamani Inayorejeshwa na Uchujaji wa Data { #return-type-and-data-filtering }

Tuendelee na mfano uliopita. Tulitaka **kuwekea kitendakazi kidokezo cha aina moja**, lakini tulitaka kuweza kurejesha kutoka kwenye kitendakazi kitu ambacho kwa kweli kinajumuisha **data zaidi**.

Tunataka FastAPI iendelee **kuchuja** data kwa kutumia modeli ya jibu. Ili hata kama kitendakazi kinarejesha data zaidi, jibu lijumuishe tu nyuga zilizotangazwa katika modeli ya jibu.

Katika mfano uliopita, kwa sababu class zilikuwa tofauti, tulilazimika kutumia kigezo cha `response_model`. Lakini hilo pia linamaanisha kwamba hatupati usaidizi wa kihariri na zana zinazokagua aina ya thamani inayorejeshwa na kitendakazi.

Lakini katika hali nyingi ambapo tunahitaji kufanya kitu kama hiki, tunataka modeli **ichuje/iondoe** tu baadhi ya data kama katika mfano huu.

Na katika hali hizo, tunaweza kutumia class na urithi ili kunufaika na **vidokezo vya aina** vya kitendakazi kupata usaidizi bora katika kihariri na zana, na bado kupata **uchujaji wa data** wa FastAPI.

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

Kwa hili, tunapata usaidizi wa zana, kutoka kwa vihariri na mypy kwa kuwa msimbo huu ni sahihi kwa upande wa aina, lakini pia tunapata uchujaji wa data kutoka FastAPI.

Hili linafanyaje kazi? Hebu tuangalie. 🤓

### Vidokezo vya Aina na Zana { #type-annotations-and-tooling }

Kwanza tuone jinsi vihariri, mypy na zana nyingine zingechukulia hili.

`BaseUser` ina nyuga za msingi. Kisha `UserIn` hurithi kutoka `BaseUser` na kuongeza uga wa `password`, hivyo itajumuisha nyuga zote kutoka modeli zote mbili.

Tunaweka kidokezo cha aina ya thamani inayorejeshwa na kitendakazi kuwa `BaseUser`, lakini kwa kweli tunarejesha instance ya `UserIn`.

Kihariri, mypy, na zana nyingine hazitaonyesha hitilafu kuhusu hili kwa sababu, kwa upande wa aina, `UserIn` ni class inayotokana na `BaseUser`, ambayo inamaanisha ni aina *halali* wakati kinachotarajiwa ni kitu chochote kilicho `BaseUser`.

### Uchujaji wa Data wa FastAPI { #fastapi-data-filtering }

Sasa, kwa upande wa FastAPI, itaangalia aina ya thamani inayorejeshwa na kuhakikisha kwamba unachorejesha kinajumuisha **tu** nyuga zilizotangazwa katika aina hiyo.

FastAPI hufanya mambo kadhaa ndani kwa ndani kwa kutumia Pydantic ili kuhakikisha kwamba kanuni hizo za urithi wa class hazitumiki katika uchujaji wa data inayorejeshwa, la sivyo unaweza kuishia kurejesha data nyingi zaidi kuliko ulivyotarajia.

Kwa njia hii, unaweza kupata faida za pande zote mbili: vidokezo vya aina vyenye **usaidizi wa zana** na **uchujaji wa data**.

## Ione katika nyaraka { #see-it-in-the-docs }

Unapoangalia nyaraka zinazozalishwa kiotomatiki, unaweza kuona kwamba modeli ya ingizo na modeli ya matokeo zitakuwa na JSON Schema zao wenyewe:

<img src="/img/tutorial/response-model/image01.png">

Na modeli zote mbili zitatumiwa katika nyaraka shirikishi za API:

<img src="/img/tutorial/response-model/image02.png">

## Vidokezo Vingine vya Aina ya Thamani Inayorejeshwa { #other-return-type-annotations }

Huenda kukawa na hali ambapo unarejesha kitu ambacho si uga halali wa Pydantic na unakiwekea kidokezo cha aina katika kitendakazi, ili tu kupata usaidizi unaotolewa na zana (kihariri, mypy, n.k.).

### Rejesha Response Moja kwa Moja { #return-a-response-directly }

Hali ya kawaida zaidi ingekuwa [kurejesha Response moja kwa moja kama ilivyoelezwa baadaye katika nyaraka za kina](../advanced/response-directly.md).

{* ../../docs_src/response_model/tutorial003_02_py310.py hl[8,10:11] *}

Hali hii rahisi hushughulikiwa kiotomatiki na FastAPI kwa sababu kidokezo cha aina ya thamani inayorejeshwa ni class ya `Response` (au class inayotokana nayo).

Na zana pia hazitaonyesha hitilafu kwa sababu `RedirectResponse` na `JSONResponse` zote mbili ni class zinazotokana na `Response`, hivyo kidokezo cha aina ni sahihi.

### Tumia Kidokezo cha Aina ya Class Inayotokana na Response { #annotate-a-response-subclass }

Unaweza pia kutumia class inayotokana na `Response` katika kidokezo cha aina:

{* ../../docs_src/response_model/tutorial003_03_py310.py hl[8:9] *}

Hili pia litafanya kazi kwa sababu `RedirectResponse` ni class inayotokana na `Response`, na FastAPI itashughulikia hali hii rahisi kiotomatiki.

### Vidokezo Visivyo Halali vya Aina ya Thamani Inayorejeshwa { #invalid-return-type-annotations }

Lakini unaporejesha objekti nyingine yoyote ambayo si aina halali ya Pydantic (k.m. objekti ya hifadhidata) na kuiwekea kidokezo hicho katika kitendakazi, FastAPI itajaribu kuunda modeli ya jibu ya Pydantic kutokana na kidokezo hicho cha aina, na itashindwa.

Hilo pia lingetokea ikiwa ungekuwa na kitu kama <dfn title='Muungano wa aina nyingi unamaanisha "yoyote kati ya aina hizi".'>muungano</dfn> wa aina tofauti ambapo moja au zaidi si aina halali za Pydantic, kwa mfano hili lingeshindwa 💥:

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

...hili linashindwa kwa sababu kidokezo cha aina si aina ya Pydantic wala si class moja tu ya `Response` au class inayotokana nayo; ni muungano (yoyote kati ya hizo mbili) wa `Response` na `dict`.

### Zima Modeli ya Jibu { #disable-response-model }

Tukiendelea na mfano hapo juu, huenda usitake uhakiki wa uhalali wa data, uundaji wa nyaraka, uchujaji, n.k. unaofanywa na FastAPI kwa chaguo-msingi.

Lakini huenda bado ukataka kuweka kidokezo cha aina ya thamani inayorejeshwa katika kitendakazi ili kupata usaidizi kutoka kwa zana kama vihariri na vikaguzi vya aina (k.m. mypy).

Katika hali hii, unaweza kuzima uzalishaji wa modeli ya jibu kwa kuweka `response_model=None`:

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

Hili litaifanya FastAPI iruke uzalishaji wa modeli ya jibu na kwa njia hiyo unaweza kuwa na vidokezo vyovyote vya aina ya thamani inayorejeshwa unavyohitaji bila kuathiri programu yako ya FastAPI. 🤓

## Vigezo vya usimbaji wa Modeli ya Jibu { #response-model-encoding-parameters }

Modeli yako ya jibu inaweza kuwa na thamani za chaguo-msingi, kama vile:

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None` (au `str | None = None` katika Python 3.10) ina thamani ya chaguo-msingi ya `None`.
* `tax: float = 10.5` ina thamani ya chaguo-msingi ya `10.5`.
* `tags: List[str] = []` ina thamani ya chaguo-msingi ya orodha tupu: `[]`.

lakini huenda ukataka kuziondoa kwenye matokeo ikiwa hazikuhifadhiwa kwa kweli.

Kwa mfano, ikiwa una modeli zenye sifa nyingi za hiari katika hifadhidata ya NoSQL, lakini hutaki kutuma majibu marefu sana ya JSON yaliyojaa thamani za chaguo-msingi.

### Tumia kigezo cha `response_model_exclude_unset` { #use-the-response-model-exclude-unset-parameter }

Unaweza kuweka kigezo cha *decorator ya operesheni ya njia* kuwa `response_model_exclude_unset=True`:

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

na thamani hizo za chaguo-msingi hazitajumuishwa katika jibu, ila thamani zilizowekwa kweli pekee.

Kwa hiyo, ukituma ombi kwa *operesheni hiyo ya njia* kwa kipengee chenye ID `foo`, jibu (bila kujumuisha thamani za chaguo-msingi) litakuwa:

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

kama ilivyoelezwa katika [nyaraka za Pydantic](https://pydantic.dev/docs/validation/latest/concepts/serialization/#excluding-and-including-fields-based-on-their-value) kuhusu `exclude_defaults` na `exclude_none`.

///

#### Data yenye thamani za nyuga zenye chaguo-msingi { #data-with-values-for-fields-with-defaults }

Lakini ikiwa data yako ina thamani za nyuga za modeli zilizo na thamani za chaguo-msingi, kama kipengee chenye ID `bar`:

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

thamani hizo zitajumuishwa katika jibu.

#### Data yenye thamani zinazolingana na za chaguo-msingi { #data-with-the-same-values-as-the-defaults }

Ikiwa data ina thamani zinazolingana na zile za chaguo-msingi, kama kipengee chenye ID `baz`:

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

FastAPI ina uwezo wa kutambua (kwa kweli, Pydantic ndiyo yenye uwezo huo) kwamba, ingawa `description`, `tax`, na `tags` zina thamani zinazolingana na zile za chaguo-msingi, ziliwekwa waziwazi (badala ya kuchukuliwa kutoka kwenye chaguo-msingi).

Kwa hiyo, zitajumuishwa katika jibu la JSON.

/// tip | Kidokezo

Zingatia kwamba thamani za chaguo-msingi zinaweza kuwa chochote, si `None` pekee.

Zinaweza kuwa orodha (`[]`), `float` ya `10.5`, n.k.

///

### `response_model_include` na `response_model_exclude` { #response-model-include-and-response-model-exclude }

Unaweza pia kutumia vigezo vya *decorator ya operesheni ya njia* vya `response_model_include` na `response_model_exclude`.

Vinapokea `set` ya `str` yenye majina ya sifa za kujumuisha (ukiacha nyingine zote) au za kuondoa (ukijumuisha nyingine zote).

Hii inaweza kutumiwa kama njia ya mkato ya haraka ikiwa una modeli moja tu ya Pydantic na unataka kuondoa baadhi ya data kutoka kwenye matokeo.

/// tip | Kidokezo

Lakini bado inapendekezwa kutumia mawazo yaliyo hapo juu, ya kutumia class nyingi, badala ya vigezo hivi.

Hii ni kwa sababu JSON Schema inayozalishwa katika OpenAPI ya programu yako (na nyaraka) bado itakuwa ya modeli nzima, hata ukitumia `response_model_include` au `response_model_exclude` kuondoa baadhi ya sifa.

Hili pia linahusu `response_model_by_alias` inayofanya kazi kwa namna inayofanana.

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | Kidokezo

Sintaksia ya `{"name", "description"}` huunda `set` yenye thamani hizo mbili.

Ni sawa na `set(["name", "description"])`.

///

#### Kutumia `list` badala ya `set` { #using-lists-instead-of-sets }

Ukisahau kutumia `set` na badala yake ukatumia `list` au `tuple`, FastAPI bado itaibadilisha kuwa `set` na itafanya kazi kwa usahihi:

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## Muhtasari { #recap }

Tumia kigezo cha `response_model` cha *decorator ya operesheni ya njia* kufafanua modeli za jibu na hasa kuhakikisha kwamba data ya faragha inachujwa na kuondolewa.

Tumia `response_model_exclude_unset` kurejesha tu thamani zilizowekwa waziwazi.
