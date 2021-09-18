
{!../../../docs/missing-translation.md!}


<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, yüksək performans, sadə öyrənmək, çevik kodlamaq, istehsal üçün hazır</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---

**Sənədlər**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Mənbə kodu**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI müasir, sürətli (yüksək performanslı), standart Python tipli göstərişlərə əsaslanaraq Python 3.6+ ilə API qurmaq üçün veb framework-ü.

Aşağıdakılar əsas xüsusiyyətlərdir:

* **Sürətli**: Çox yüksək performans, **NodeJS** və **Go** ilə bərabər (Starlette və Pydantic-ə təşəkkürlər). [Ən sürətli Python frameworklərindən biri](#performans).

* **Çevik kodlama**: Xüsusiyyətləri inkişaf etdirmə sürətini təxminən 200-300% artırın. *
* **Daha az boşluq**: İnsan (developer) tərəfindən törədilən səhvlərin təxminən 40% -ni azaldın. *
* **İntuitiv**: Böyük redaktor dəstəyi. <abbr title="auto-complete, autocompletion, IntelliSense olaraq da bilinir">Tamamlama</abbr> həryerdə. Xəta müəyyənləşdirmək üçün daha az vaxt.
* **Asan**: İstifadəsi və öyrənməsi asan olması üçün hazırlanmışdır. Sənədləri oxumaq üçün daha az vaxt.
* **Qısa**: Kodun təkrarlanmasını minimuma endirin. Hər bir parametr bəyannaməsindən birdən çox xüsusiyyət. Daha az səhv.
* **Sağlam**: İstehsal üçün hazır kodu əldə edin. Avtomatik interaktiv sənədlərlə.
* **Standartlara əsaslanan**: API üçün açıq standartlara əsaslanır (və tam uyğun gəlir): <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (əvvəllər Swagger olaraq bilinirdi) və <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Sxeması</a>.

<small>* təxmin daxili developer komandasının istehsal tətbiqləri hazırlayarkən aparılan testlərə görə müəyyənləşdirilmişdir.</small>

## Sponsorlar

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Digər sponsorlar</a>

## Rəylər

"_[...] Mən son günlərdə həddindən çox **FastAPI** istifadə edirəm. [...] Mən əslində onu komandamın bütün **Microsoftda ML sevislərində** istifadə etməyi planlayıram. Onların bəziləri **windowsun** əsas məhsuluna və bəzi **Office** məhsullarına inteqrasiya olunurlar._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_**FastAPI** kitabxanasını **proqnozlar** əldə etmək üçün sorğular edilə bilən **REST** serveri yaratmaq üçün istifadə etdik. [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, və Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** **böhran idarəçiliyi** orkestrləşmə framework-nün açıq mənbəli buraxılışını elan etməkdən məmnundur: **Dispatch**! [**FastAPI** ilə quruldu]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Mən **FastAPI** üçün çox həyəcanlıyam. O çox əyləncəlidir!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podkast sahibi</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Düzünü desəm, qurduğunuz şey çox dayanıqlı və səliqəli görünür. Bir çox cəhətdən, bu **Hug-ın** olmasını istədiyim kimidir - birinin bunu qurduğunu görmək həqiqətən də ruhlandırıcıdır._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> yaradıcısı</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Əgər siz REST API-lar qurmaq üçün **müasir framework** axtarışındasınızsa, **FastAPI-ya** nəzər salın [...] O sürətli, istifadəsi və öyrənməsi asandır [...]_"

"_Biz API-larımız üçün **FastAPI**-ya keçdik [...] Sizin onu bəyənəcəyinizi düşünürəm [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> təsisçiləri - <a href="https://spacy.io" target="_blank">spaCy</a> yaradıcıları</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, CLI-ların FastAPI-ı

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Əgər siz veb API yerinə terminalda istifadə ediləcək <abbr title="Command Line Interface">CLI</abbr> tətbiqi qurursunuzsa, <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**-a</a>. nəzər salın

**Typer** FastAPI-ın balaca qardaşıdır. Və onun **CLI-ların FastAPI-ı** olması nəzərdə tutulur. ⌨️ 🚀

## Tələblər

Python 3.6+

FastAPI nəhənglərin çiyinlərində dayanır:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> veb hissələri üçün.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> data hissələri üçün.

## Quraşdırma

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Sizin həm də istehsal üçün <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> və ya <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a> kimi bir ASGI serverinə ehtiyacınız olacaq.

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## Nümunə

### Yarat

* `main.py` faylını aşağıdakı yaradın:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Və ya<code>async def</code> istifadə edin...</summary>

Əgər sizin kodunuz `async` / `await` istifadə edirsə, `async def` istifadə edin:

```Python hl_lines="9  14"
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

**Qeyd**:

Bilmirsinizsə, <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` və `await`</a>. haqqında olan _"Tələsirsən?"_ bölməsindəki sənədlərə nəzər salın.

</details>

### Çalışdır

Serveri işə salın:

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

`uvicorn main:app` əmri aşağıdakı hissələrdən ibarətdir:

* `main`: `main.py` faylı (Python "modulu").
* `app`: `main.py` faylı daxilində `app = FastAPI()` sətri ilə yaradılmış obyekt.
* `--reload`: kodu dəyişdirdikdən sonra serveri yenidən başladın. Bunu yalnız "development" üçün edin.

</details>

### Yoxlayın

Brauzerinizdə bu adresə yönlənin <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Aşağıdakı kimi JSON cavabı görəcəksiniz:

```JSON
{"item_id": 5, "q": "somequery"}
```

Siz artıq bir API yaratmısınız, hansı ki:

* `/` və `/items/{item_id}` _yollarında_ HTTP sorğularını qəbul edir.
* Hər iki _yol_ `GET` <em>əməliyyatlarını</em> aparır (HTTP üsulları olaraq da bilinir).
* `/items/{item_id}` _yolu_ `item_id` adlı `int` olmalı olan _yol parametrinə_ sahibdir.
* `/items/{item_id}` _yolu_ istəyə bağlı `q` adlı `str` sorğu parametrinə sahibdir.

### İnteraktiv API sənədləri

İndi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>-a daxil olun.

Siz burada avtomatik interaktiv API sənədləşməni görəcəksiniz (<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> tərəfindən təmin edilmiş):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternativ API sənədləri

İndi isə <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>-a keçid edin.

Siz burada alternativ avtomatik sənədləşməni görəcəksiniz (<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> tərəfindən təmin edilmiş):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Nümunə yüksəltmə

İndi `PUT` sorğunusu qəbul etmək üçün `main.py` faylını dəyişdirin.

Pydantic sayəsində standart Python növlərindən istifadə edərək bədəni bildirin.

```Python hl_lines="4  9-12  25-27"
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Server avtomatik yenilənməlidir (çünki yuxarıdakı `uvicorn` əmrinə `--reload` əlavə etdiniz)

### İnteraktiv API sənədləri yüksəltməsi

İndi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> keçidinə daxil olun.

* İnteraktiv API sənədləri yeni gövdə daxil olmaqla avtomatik olaraq yenilənəcəkdir:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Parametrləri doldurmağa və API ilə birbaşa əlaqə qurmağa imkan verən "Try it out" düyməsini basın:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Sonra "Execute" düyməsini basın, istifadəçi interfeysi API ilə əlaqə quracaq, parametrləri göndərəcək, nəticələr əldə edəcək və onları ekranda göstərəcək.:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternati  API sənədləri yüksəltməsi

İndi isə <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> keçidinə daxil olun.

* Alternativ sənədlər də yeni sorğu parametrini və gövdəsini əks etdirəcək:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Xülasə

In summary, you declare **once** the types of parameters, body, etc. as function parameters. 
Xülasə olaraq, siz parametr növlərini, bədəni və s. **bir dəfə** funksiya parametsləri olaraq bəyan edirsiniz.

Bunu standart müasir Python növləri ilə edirsiniz.

Siz yeni bir sintaksis, müəyyən bir kitabxananın metodlarını və ya siniflərini öyrənmək məcburiyyətində deyilsiniz.

Yalnız standart **Python 3.6+**.

Məsələn, `int` üçün:

```Python
item_id: int
```

və ya daha mürəkkəb bir `Item` modeli üçün:

```Python
item: Item
```

... və bu tək bəyannamə ilə əldə edirsiniz:

* Redaktor dəstəyi, aşağıdakılar daxil olmaqla:
    * Tamamlanma.
    * Tip yoxlamaları.
* Məlumatların təsdiqlənməsi:
    * Məlumatlar etibarsız olduqda avtomatik və dəqiq səhvlər.
    * Dərin iç içə yerləşən JSON obyektləri üçün də doğrulama.
* Giriş məlumatlarının <abbr title="serializasiya, təhlil, marshalling kimi də tanınır">çevrilməsi</abbr>: şəbəkədən Python məlumatlarına və növlərinə çevrilir. Buradan oxuyur:
    * JSON.
    * Yol parametrləri.
    * Sorğu parametrləri.
    * Çərəzlər.
    * Hederlər.
    * Anketlər.
    * Fayllar.
* Çıxış məlumatlarının <abbr title="serializasiya, təhlil, marshalling kimi də tanınır">çevrilməsi</abbr>: Python məlumatları və növlərindən şəbəkə datasına çevirir. Buradan oxuyur:
    * Python tiplərini çevir (`str`, `int`, `float`, `bool`, `list`, etc).
    * `datetime` obyektləri.
    * `UUID` obyektləri.
    * Verilənlər bazası modelləri.
    * ...və daha çoxu.
* 2 alternativ istifadəçi interfeysi daxil olmaqla avtomatik interaktiv API sənədləri:
    * Swagger UI.
    * ReDoc.

---

Əvvəlki kod nümunəsinə geri döndükdə, **FastAPI** bunları edəcək:

* `GET` və `PUT` sorğuları üçün yolda `item_id` olduğunu təsdiq edəcək.
* `GET` və `PUT` sorğuları üçün `item_id` parametrinin hansısa bir `int` tipi olduğunu təsdiq edəcək.
    * Əgər deyilsə, müştəri yararlı, təmiz xəta görəcək.
* `GET` sorğusu üçün `q` adlandırılmış istəyə bağlı sorğu parametrinin olmasını yoxlayacaq (`http://127.0.0.1:8000/items/foo?q=somequery` kimi).
    * As the `q` parameter is declared with `= None`, it is optional.
    * `q` parametri `= None` ilə bəyan edildiyi üçün o istəyə bağlıdır.
    * `None` olmadan o tələb olunan parametr olacaq (`PUT` ilə olan vəziyyətdəki gövdə kimi).
* `/items/{item_id}` yoluna olan `PUT` sorğuları üçün gövdəni JSON kimi oxuyacaq:
    * Onun `str` olan tələb olunan `name` atributunun olmasını  yoxlayacaq. 
    * Onun `float` olan tələb olunan `price` atributunun olmasını  yoxlayacaq. 
    * Onun istəyə bağlı `is_offer` atributunun olmasını və varsa `bool` tipində olmasını yoxlayacaq. 
    * Bunların hamısı həm də dərin yuvalanmış JSON obyektləri üçün işləməlidir.
* JSON-a və JSON-dan avtomatik çevirmə.
* OpenAPI vasitəsilə hər şeyi sənədləşdirmə, hansı ki, aşağıdakılar tərəfindən istifadə oluna bilər:
    * İnteraktiv sənədləşdirmə sistemləri.
    * Automatic client code generation systems, for many languages.
    * Bir çox dil üçün, avtomatik müştəri kodu generasiya edən sistemlər.
* Birbaşa 2 interaktiv sənəd veb interfeysi təqdim etmək.

---

Üzərindən keçməyimizə baxmayaraq artıq hamısının necə işlədiyini başa düşürsən.

Sətri dəyişdirmək üçün cəhd edin:

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

...və redaktorunuzun atributları avtomatik olaraq necə tamamlayacağını və növlərini biləcəyini görün:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Daha çox xüsusiyyət daxil olmaqla daha tam bir nümunə üçün <a href="https://fastapi.tiangolo.com/tutorial/">Öyrədici - İstifadəçi Bələdçisinə</a> baxın.

**Spoyler xəbərdarlığı:**: öyrədici - istifadəçi bələdçisi ehtiva edir:

* **Hederlər**, **çərəzlər**, **forma sahələri** və **fayllar** kimi digər fərqli yerlərdən **parametrlərin** bəyannaməsi.
* `maximum_length` və ya `regex` kimi **Doğrulama məhdidiyyətlərinin** necə təyin edilməsi.
* Çox güclü və istifadə asan **<abbr title="komponentlər, qaynaqlar, provayderlər, xidmətlər, enjektabl olaraq da bilinir">Asılılıq injeksiyası</abbr>** sistemi.
* **JWT tokenləri** və **HTTP Basic** auth ilə ** OAuth2 ** dəstəyi daxil olmaqla, təhlükəsizlik və identifikasiya.
* **Dərin yuvalı JSON modelləri** (Pydantic sayəsində) bildirmək üçün daha inkişaf etmiş (lakin eyni dərəcədə asan) üsullar.
* Bir çox əlavə xüsusiyyət (Starlette sayəsində):
    * **WebSocketlər**
    * **GraphQL**
    * `requests` və `pytest`-ə əsaslanan son dərəcə asan testlər.
    * **CORS**
    * **Çərəz sessiyaları**
    * ...və daha çoxu.

## Performans

Müstəqil TechEmpower meyarları Uvicorn altın çalışan **FastAPI** tətbiqlərini <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">mövcud olan ən sürətli Python frameworklərindən biri</a> kimi göstərir, hansı ki, sadəcə Starlette və Uvicorn-un özündədən aşağıdadır. (Amma bunlar da FastAPI tərəfindən daxildə istifadə olunur). (*)
Bu barədə daha çox məlumat əldə etmək üçün bölməyə baxın <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Göstəricilər</a>.

## İstəyə bağlı asılılıqlar

Pydantic tərəfindən istifadə olunur:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - daha sürətli JSON <abbr title="bir HTTP sorğusundan gələn sətiri Python məlumatlarına çevirmək">"parçalaması"</abbr> üçün.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - e-poçt doğrulaması üçün.

Starlette tərəfindən istifadə olunur:

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - `TestClient` istifadə etmək istəyirsinizsə, tələb olunur.
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - `FileResponse` və ya `StaticFiles` istifadə etmək istəyirsinizsə, tələb olunur.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Varsayılan şablon konfiqurasiyasından istifadə etmək istəyirsinizsə, tələb olunur.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - <abbr title="converting the string that comes from an HTTP request into Python data">"parçalamadan"</abbr> `request.form()` ilə dəstək istəyirsinizsə, tələb olunur .
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - `SessionMiddleware` dəstəyi üçün tələb olunur.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Starlette-in `SchemaGenerator` dəstəyi üçün tələb olunur (ehtimal ki, FastAPI ilə ehtiyacınız yoxdur).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - `GraphQLApp` dəstəyi üçün tələb olunur.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - `UJSONResponse` istifadə etmək istəyirsiznizsə, tələb olunur.

FastAPI / Starlette tərəfindən istifadə olunur:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - tətbiqinizi yükləyən və xidmət edən server üçün.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - `ORJSONResponse` istifadə etmək istəyirsinizsə tələb olunur.

Bunların hamısını `pip install fastapi[all]` ilə quraşdıra bilərsiniz.

## Lisenziya

Bu layihə MIT lisenziyası şərtləri ilə lisenziyalaşdırılmışdır.