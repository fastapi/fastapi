<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, yüksək məshuldarlı, öyrənməsi asan, çevik kodlama, istifadəyə hazırdır</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Əhatə">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Paket versiyası">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Dəstəklənən Python versiyaları">
</a>
</p>

---

**Sənədlər**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Qaynaq Kodu**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI Python ilə API yaratmaq üçün standart Python <abbr title="Tip Məsləhətləri: Type Hints">tip məsləhətlərinə</abbr> əsaslanan, müasir, sürətli (yüksək performanslı) framework-dür.

Əsas xüsusiyyətləri bunlardır:

* **Sürətli**: Çox yüksək performans, **NodeJS** və **Go** səviyyəsində (Starlette və Pydantic-ə təşəkkürlər). [Ən sürətli Python frameworklərindən biridir](#performans).
* **Çevik kodlama**: Funksiyanallıqları inkişaf etdirmək sürətini təxminən 200%-dən 300%-ə qədər artırın. *
* **Daha az xəta**: İnsan (developer) tərəfindən törədilən səhvlərin təxminən 40% -ni azaldın. *
* **İntuitiv**: Əla redaktor dəstəyi. Hər yerdə <abbr title="auto-complete, autocompletion, IntelliSense olaraq da bilinir">otomatik tamamlama</abbr>. Xətaları müəyyənləşdirməyə daha az vaxt sərf edəcəksiniz.
* **Asan**: İstifadəsi və öyrənilməsi asan olması üçün nəzərdə tutulmuşdur. Sənədləri oxumaq üçün daha az vaxt ayıracaqsınız.
* **Qısa**: Kod təkrarlanmasını minimuma endirin. Hər bir parametr tərifində birdən çox xüsusiyyət ilə və daha az səhvlə qarşılaşacaqsınız.
* **Güclü**: Avtomatik və interaktiv sənədlərlə birlikdə istifadəyə hazır kod əldə edə bilərsiniz.
* **Standartlara əsaslanan**: API-lar üçün açıq standartlara əsaslanır (və tam uyğun gəlir): <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (əvvəlki adı ilə Swagger) və <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* Bu fikirlər daxili development komandasının hazırladıqları məhsulların sınaqlarına əsaslanır.</small>

## Sponsorlar

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}`
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/az/fastapi-people/#sponsors" class="external-link" target="_blank">Digər sponsorlar</a>

## Rəylər

"_[...] Son günlərdə **FastAPI**-ı çox istifadə edirəm. [...]  Əslində onu komandamın bütün **Microsoftda ML sevislərində** istifadə etməyi planlayıram. Onların bəziləri **windows**-un əsas məhsuluna və bəzi **Office** məhsullarına inteqrasiya olunurlar._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_**FastAPI** kitabxanasını **Proqnozlar** əldə etmək üçün sorğulana bilən **REST** serverini yaratmaqda istifadə etdik._"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** **böhran idarəçiliyi** orkestrləşmə framework-nün açıq qaynaqlı buraxılışını elan etməkdən məmnundur: **Dispatch**! [**FastAPI** ilə quruldu]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_**FastAPI** üçün həyəcanlıyam. Çox əyləncəlidir!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Düzünü desəm, sizin qurduğunuz şey həqiqətən möhkəm və peşəkar görünür. Bir çox cəhətdən **Hug**-un olmasını istədiyim kimdir - kiminsə belə bir şey qurduğunu görmək həqiqətən ruhlandırıcıdır._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Əgər REST API-lər yaratmaq üçün **müasir framework** öyrənmək istəyirsinizsə, **FastAPI**-a baxın [...] Sürətli, istifadəsi və öyrənməsi asandır. [...]_"

"_**API** xidmətlərimizi **FastAPI**-a köçürdük [...] Sizin də bəyənəcəyinizi düşünürük._"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_Python ilə istifadəyə hazır API qurmaq istəyən hər kəsə **FastAPI**-ı tövsiyə edirəm. **Möhtəşəm şəkildə dizayn edilmiş**, **istifadəsi asan** və **yüksək dərəcədə genişlənə bilən**-dir, API əsaslı inkişaf strategiyamızın **əsas komponentinə** çevrilib və Virtual TAC Engineer kimi bir çox avtomatlaşdırma və servisləri idarə edir._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, CLI-ların FastAPI-ı

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Əgər siz veb API əvəzinə terminalda istifadə ediləcək <abbr title="Command Line Interface">CLI</abbr> proqramı qurursunuzsa, <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>-a baxa bilərsiniz.

**Typer** FastAPI-ın kiçik qardaşıdır. Və o, CLI-lərin **FastAPI**-ı olmaq üçün nəzərdə tutulub. ⌨️ 🚀

## Tələblər

FastAPI nəhənglərin çiyinlərində dayanır:

* Web tərəfi üçün <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a>.
* Data tərəfi üçün <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>.

## Quraşdırma

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Tətbiqimizi əlçatan etmək üçün bizə <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> və ya <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a> kimi ASGI server lazımdır.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## Nümunə

### Kodu yaradaq

* `main.py` adlı fayl yaradaq və ona aşağıdakı kodu yerləşdirək:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Və ya <code>async def</code>...</summary>

Əgər kodunuzda `async` və ya `await` vardırsa `async def` istifadə edə bilərik:

```Python hl_lines="9  14"
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

**Qeyd**:

Əgər bu mövzu haqqında məlumatınız yoxdursa <a href="https://fastapi.tiangolo.com/az/async/#in-a-hurry" target="_blank">`async` və `await` sənədindəki</a> _"Tələsirsən?"_ bölməsinə baxa bilərsiniz.

</details>

### Kodu işə salaq

Serveri aşağıdakı əmr ilə işə salaq:

<div class="termy">

```console
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary><code>uvicorn main:app --reload</code> əmri haqqında...</summary>

`uvicorn main:app` əmri aşağıdakılara instinad edir:

* `main`: `main.py` faylı (yəni Python "modulu").
* `app`: `main.py` faylında `app = FastAPI()` sətrində yaratdığımız `FastAPI` obyektidir.
* `--reload`: kod dəyişikliyindən sonra avtomatik olaraq serveri yenidən işə salır. Bu parametrdən yalnız development mərhələsində istifadə etməliyik.

</details>

### İndi yoxlayaq

Bu linki brauzerimizdə açaq <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Aşağıdakı kimi bir JSON cavabı görəcəksiniz:

```JSON
{"item_id": 5, "q": "somequery"}
```

Siz artıq bir API yaratmısınız, hansı ki:

* `/` və `/items/{item_id}` <abbr title="Yol: Path ">_yollarında_</abbr> HTTP sorğularını qəbul edir.
* Hər iki _yolda_ `GET` <em>əməliyyatlarını</em> (həmçinin HTTP _metodları_ kimi bilinir) aparır.
* `/items/{item_id}` _yolu_ `item_id` adlı `int` qiyməti almalı olan _yol parametrinə_ sahibdir.
* `/items/{item_id}` _yolunun_ `q` adlı yol parametri var və bu parametr istəyə bağlı olsa da, `str` qiymətini almalıdır.

### İnteraktiv API Sənədləri

İndi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> ünvanına daxil olun.

Avtomatik interaktiv API sənədlərini görəcəksiniz (<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> tərəfindən təmin edilir):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternativ API sənədləri

İndi isə <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> ünvanına daxil olun.

<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> tərəfindən təqdim edilən avtomatik sənədləri görəcəksiniz:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Nümunəni Yeniləyək

İndi gəlin `main.py` faylını `PUT` sorğusu ilə birlikdə <abbr title="Gövdə: Body ">gövdə</abbr> qəbul edəcək şəkildə dəyişdirək.

Pydantic sayəsində standart Python tiplərindən istifadə edərək <abbr title="Gövdə: Body ">gövdə</abbr>ni müəyyən edək.

```Python hl_lines="4  9-12  25-27"
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```
Server avtomatik olaraq yenidən işə salınmalı idi (çünki biz yuxarıda `uvicorn` əmri ilə `--reload` parametrindən istifadə etmişik).

### İnteraktiv API sənədlərindəki dəyişikliyə baxaq

Yenidən <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> ünvanına daxil olun.

* İnteraktiv API sənədləri yeni gövdə də daxil olmaq ilə avtomatik olaraq yenilənəcək:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* "Try it out" düyməsini klikləyin, bu, parametrləri doldurmağa və API ilə birbaşa əlaqə saxlamağa imkan verir:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Sonra "Execute" düyməsini klikləyin, istifadəçi interfeysi API ilə əlaqə quracaq, parametrləri göndərəcək, nəticələri əldə edəcək və onları ekranda göstərəcək:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternativ API Sənədlərindəki Dəyişikliyə Baxaq

İndi isə yenidən <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> ünvanına daxil olun.

* Alternativ sənədlər həm də yeni sorğu parametri və gövdəsini əks etdirəcək:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Xülasə

Ümumiləşdirsək, parametrlər, gövdə və s. Biz məlumat növlərini **bir dəfə** funksiya parametrləri kimi təyin edirik.

Bunu standart müasir Python tipləri ilə edirsiniz.

Yeni sintaksis, müəyyən bir kitabxananın metodlarını və ya siniflərini və s. öyrənmək məcburiyyətində deyilsiniz.

Sadəcə standart **Python**.

Məsələn, `int` üçün:

```Python
item_id: int
```

və ya daha mürəkkəb `Item` modeli üçün:

```Python
item: Item
```

...və yalnız parametr tipini təyin etməklə bunları əldə edirsiniz:

* Redaktor dəstəyi ilə:
    * Avtomatik tamamlama.
    * Tip yoxlanması.
* Məlumatların Təsdiqlənməsi:
    * Məlumat etibarsız olduqda avtomatik olaraq aydın xətalar göstərir.
    * Hətta çox dərin JSON obyektlərində belə doğrulama aparır.
* Daxil olan məlumatları <abbr title="Çevrilmə: serialization, parsing, marshalling olaraq da bilinir">çevirmək</abbr> üçün aşağıdakı məlumat növlərindən istifadə edilir:
    * JSON.
    * <abbr title="Yol: Path">Yol</abbr> parametrləri.
    * <abbr title="Sorğu: Query">Sorğu</abbr> parametrləri.
    * <abbr title="Çərəz: Cookie">Çərəzlər</abbr>.
    * <abbr title="Başlıq: Header">Başlıqlaq</abbr>.
    * <abbr title="Forma: Form">Formalar</abbr>.
    * Fayllar.
* Daxil olan məlumatları <abbr title="Çevrilmə: serialization, parsing, marshalling olaraq da bilinir">çevirmək</abbr> üçün aşağıdakı məlumat növlərindən istifadə edilir (JSON olaraq):
    * Python tiplərinin (`str`, `int`, `float`, `bool`, `list`, və s) çevrilməsi.
    * `datetime` obyektləri.
    * `UUID` obyektləri.
    * Verilənlər bazası modelləri.
    * və daha çoxu...
* 2 alternativ istifadəçi interfeysi daxil olmaqla avtomatik interaktiv API sənədlərini təmin edir:
    * Swagger UI.
    * ReDoc.

---

Gəlin əvvəlki nümunəyə qayıdaq və **FastAPI**-nin nələr edəcəyinə nəzər salaq:

* `GET` və `PUT` sorğuları üçün `item_id`-nin <abbr title="Yol: Path">yolda</abbr> olub-olmadığını yoxlayacaq.
* `item_id`-nin `GET` və `PUT` sorğuları üçün növünün `int` olduğunu yoxlayacaq.
    * Əgər `int` deyilsə, səbəbini göstərən bir xəta mesajı göstərəcəkdir.
* <abbr title="Məcburi olmayan: Optional">məcburi olmayan</abbr> `q` parametrinin `GET` (`http://127.0.0.1:8000/items/foo?q=somequery` burdakı kimi) sorğusu içərisində olub olmadığını yoxlayacaq.
    * `q` parametrini `= None` ilə yaratdığımız üçün, <abbr title="Məcburi olmayan: Optional">məcburi olmayan</abbr> parametr olacaq.
    * Əgər `None` olmasaydı, bu məcburi parametr olardı (`PUT` metodunun gövdəsində olduğu kimi).
* `PUT` sorğusu üçün, `/items/{item_id}` gövdəsini JSON olaraq oxuyacaq:
    * `name` adında məcburi bir parametr olub olmadığını və əgər varsa, tipinin `str` olub olmadığını yoxlayacaq.
    * `price` adında məcburi bir parametr olub olmadığını və əgər varsa, tipinin `float` olub olmadığını yoxlayacaq.
    * `is_offer` adında <abbr title="Məcburi olmayan: Optional">məcburi olmayan</abbr> bir parametr olub olmadığını və əgər varsa, tipinin `float` olub olmadığını yoxlayacaq.
    * Bütün bunlar ən dərin JSON obyektlərində belə işləyəcək.
* Məlumatların JSON-a və JSON-un Python obyektinə çevrilməsi avtomatik həyata keçiriləcək.
* Hər şeyi OpenAPI ilə uyğun olacaq şəkildə avtomatik olaraq sənədləşdirəcək və onları aşağıdakı kimi istifadə edə biləcək:
    * İnteraktiv sənədləşmə sistemləri.
    * Bir çox proqramlaşdırma dilləri üçün avtomatlaşdırılmış <abbr title="Müştəri: Client">müştəri</abbr> kodu yaratma sistemləri.
* 2 interaktiv sənədləşmə veb interfeysini birbaşa təmin edəcək.

---

Yeni başlamışıq, amma siz artıq işin məntiqini başa düşmüsünüz.

İndi aşağıdakı sətri dəyişdirməyə çalışın:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...bundan:

```Python
        ... "item_name": item.name ...
```

...buna:

```Python
        ... "item_price": item.price ...
```

...və redaktorun məlumat tiplərini bildiyini və avtomatik tamaladığını görəcəksiniz:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Daha çox funksiyaya malik daha dolğun nümunə üçün <a href="https://fastapi.tiangolo.com/az/tutorial/">Öyrədici - İstifadəçi Təlimatı</a> səhifəsinə baxa bilərsiniz.

**Spoiler xəbərdarlığı**: Öyrədici - istifadəçi təlimatına bunlar daxildir:

* **Parametrlərin**, <abbr title="Başlıq: Header">**başlıqlar**</abbr>, <abbr title="Çərəz: Cookie">çərəzlər</abbr>, **forma sahələri** və **fayllar** olaraq müəyyən edilməsi.
* `maximum_length` və ya `regex` kimi **doğrulama məhdudiyyətlərinin** necə təyin ediləcəyi.
* Çox güclü və istifadəsi asan **<abbr title="components, resources, providers, services, injectables olaraq da bilinir">Dependency Injection</abbr>** sistemi.
* Təhlükəsizlik və autentifikasiya, **JWT tokenləri** ilə **OAuth2** dəstəyi və **HTTP Basic** autentifikasiyası.
* **çox dərin JSON modellərini** müəyyən etmək üçün daha irəli səviyyə (lakin eyni dərəcədə asan) üsullar (Pydantic sayəsində).
* <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> və digər kitabxanalar ilə **GraphQL** inteqrasiyası.
* Digər əlavə xüsusiyyətlər (Starlette sayəsində):
    * **WebSockets**
    * HTTPX və `pytest` sayəsində çox asan testlər
    * **CORS**
    * **Cookie Sessions**
    * ...və daha çoxu.

## Performans

Müstəqil TechEmpower meyarları göstərir ki, Uvicorn üzərində işləyən **FastAPI** proqramları <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">ən sürətli Python kitabxanalarından biridir</a>, yalnız Starlette və Uvicorn-un özündən yavaşdır, ki FastAPI bunların üzərinə qurulmuş bir framework-dür. (*)

Ətraflı məlumat üçün bu bölməyə nəzər salın <a href="https://fastapi.tiangolo.com/az/benchmarks/" class="internal-link" target="_blank"><abbr title="Müqayisələr: Benchmarks">Müqayisələr</abbr></a>.

## Məcburi Olmayan Tələblər

Pydantic tərəfindən istifadə olunanlar:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - e-poçtun yoxlanılması üçün.
* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - parametrlərin idarə edilməsi üçün.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - Pydantic ilə istifadə edilə bilən əlavə tiplər üçün.

Starlette tərəfindən istifadə olunanlar:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Əgər `TestClient` strukturundan istifadə edəcəksinizsə, tələb olunur.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Standart <abbr title="Şablon: Template">şablon</abbr> konfiqurasiyasından istifadə etmək istəyirsinizsə, tələb olunur.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - `request.form()` ilə forma <abbr title="HTTP sorğusu ilə alınan string məlumatın Python obyektinə çevrilməsi">"çevirmə"</abbr> dəstəyindən istifadə etmək istəyirsinizsə, tələb olunur.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - `SessionMiddleware` dəstəyi üçün tələb olunur.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - `SchemaGenerator` dəstəyi üçün tələb olunur (Çox güman ki, FastAPI istifadə edərkən buna ehtiyacınız olmayacaq).
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - `UJSONResponse` istifadə etmək istəyirsinizsə, tələb olunur.

Həm FastAPI, həm də Starlette tərəfindən istifadə olunur:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - Yaratdığımız proqramı servis edəcək veb server kimi fəaliyyət göstərir.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - `ORJSONResponse` istifadə edəcəksinizsə tələb olunur.

Bütün bunları `pip install fastapi[all]` ilə quraşdıra bilərsiniz.

## Lisenziya

Bu layihə MIT lisenziyasının şərtlərinə əsasən lisenziyalaşdırılıb.
