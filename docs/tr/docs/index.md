<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, yüksek performanslı, öğrenmesi kolay, geliştirmesi hızlı, kullanıma sunulmaya hazır.</em>
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

**dokümantasyon**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Kaynak kodu**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI, Python 3.6+'nın standart type hintlerine dayanan modern ve hızlı (yüksek performanslı) API'lar oluşturmak için kullanılabilecek web framework'ü.

Ana özellikleri:

* **Hızlı**: çok yüksek performanslı, **NodeJS** ve **Go** ile eşdeğer seviyede performans sağlıyor, (Starlette ve Pydantic sayesinde.) [Python'un en hızlı frameworklerinden bir tanesi.](#performans).
* **Kodlaması hızlı**: Yeni özellikler geliştirmek neredeyse %200 - %300 daha hızlı. *
* **Daha az bug**: Geliştirici (insan) kaynaklı hatalar neredeyse %40 azaltıldı. *
* **Sezgileri güçlü**: Editor (otomatik-tamamlama) desteği harika. <abbr title="Otomatik tamamlama-IntelliSense">Otomatik tamamlama</abbr> her yerde. Debuglamak ile daha az zaman harcayacaksınız.
* **Kolay**: Öğrenmesi ve kullanması kolay olacak şekilde. Doküman okumak için harcayacağınız süre azaltıldı.
* **Kısa**: Kod tekrarını minimuma indirdik. Fonksiyon parametrelerinin tiplerini belirtmede farklı yollar sunarak karşılaşacağınız bug'ları azalttık.
* **Güçlü**: Otomatik dokümantasyon ile beraber, kullanıma hazır kod yaz.

* **Standartlar belirli**: Tamamiyle API'ların açık standartlara bağlı ve (tam uyumlululuk içerisinde); <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (eski adıyla Swagger) ve <a href="http://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* Bahsi geçen rakamsal ifadeler tamamiyle, geliştirme takımının kendi sundukları ürünü geliştirirken yaptıkları testlere dayanmakta.</small>

## Sponsors

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Other sponsors</a>

## Görüşler


"_[...] Bugünlerde **FastAPI**'ı çok fazla kullanıyorum [...] Aslına bakarsanız **Microsoft'taki Machine Learning servislerimizin** hepsinde kullanmayı düşünüyorum. FastAPI ile geliştirdiğimiz servislerin bazıları çoktan **Windows**'un ana ürünlerine ve **Office** ürünlerine entegre edilmeye başlandı bile._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---


"_**FastAPI**'ı **tahminlerimiz**'i sorgulanabilir hale getirmek için **REST** mimarisı ile beraber server üzerinde kullanmaya başladık._"


<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---


"_**Netflix** **kriz yönetiminde** orkestrasyon yapabilmek için geliştirdiği yeni framework'ü **Dispatch**'in, açık kaynak versiyonunu paylaşmaktan gurur duyuyor. [**FastAPI** ile yapıldı.]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---


"_**FastAPI** için ayın üzerindeymişcesine heyecanlıyım. Çok eğlenceli!_"


<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Dürüst olmak gerekirse, geliştirdiğin şey bir çok açıdan çok sağlam ve parlak gözüküyor. Açıkcası benim **Hug**'ı tasarlarken yapmaya çalıştığım şey buydu - bunu birisinin başardığını görmek gerçekten çok ilham verici._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="http://www.hug.rest/" target="_blank">Hug</a>'ın  Yaratıcısı</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Eğer REST API geliştirmek için **modern bir framework** öğrenme arayışında isen, **FastAPI**'a bir göz at [...] Hızlı, kullanımı ve öğrenmesi kolay.  [...]_"

"_Biz **API** servislerimizi **FastAPI**'a geçirdik [...] Sizin de beğeneceğinizi düşünüyoruz. [...]_"



<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> kurucuları - <a href="https://spacy.io" target="_blank">spaCy</a> yaratıcıları</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, komut satırı uygulamalarının FastAPI'ı

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Eğer API yerine <abbr title="Command Line Interface">komut satırı uygulaması</abbr> geliştiriyor isen <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>'a bir göz at.

**Typer** kısaca FastAPI'ın küçük kız kardeşi. Komut satırı uygulamalarının **FastAPI'ı** olması hedeflendi. ⌨️ 🚀

## Gereksinimler

Python 3.7+

FastAPI iki devin omuzları üstünde duruyor:

* Web tarafı için <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a>.
* Data tarafı için <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>.

## Yükleme

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Uygulamanı kullanılabilir hale getirmek için <a href="http://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> ya da <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a> gibi bir ASGI serverına ihtiyacın olacak.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## Örnek

### Şimdi dene

* `main.py` adında bir dosya oluştur :

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
<summary>Ya da <code>async def</code>...</summary>

Eğer kodunda `async` / `await` var ise, `async def` kullan:

```Python hl_lines="9 14"
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

**Not**:

Eğer ne olduğunu bilmiyor isen _"Acelen mi var?"_ kısmını oku <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` ve `await`</a>.

</details>

### Çalıştır

Serverı aşağıdaki komut ile çalıştır:

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
<summary>Çalıştırdığımız <code>uvicorn main:app --reload</code> hakkında...</summary>

`uvicorn main:app` şunları ifade ediyor:

* `main`: dosya olan `main.py` (yani Python "modülü").
* `app`: ise `main.py` dosyasının içerisinde oluşturduğumuz `app = FastAPI()` 'a denk geliyor.
* `--reload`: ise kodda herhangi bir değişiklik yaptığımızda serverın yapılan değişiklerileri algılayıp, değişiklikleri siz herhangi bir şey yapmadan uygulamasını sağlıyor.

</details>

### Dokümantasyonu kontrol et

Browserını aç ve şu linke git <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Bir JSON yanıtı göreceksin:

```JSON
{"item_id": 5, "q": "somequery"}
```

Az önce oluşturduğun API:

* `/` ve `/items/{item_id}` adreslerine HTTP talebi alabilir hale geldi.
* İki _adresde_ `GET` <em>operasyonlarını</em> (HTTP  _metodları_ olarakta bilinen) yapabilir hale geldi.
* `/items/{item_id}` _adresi_ ayrıca bir `item_id` _adres parametresine_  sahip ve bu bir `int` olmak zorunda.
* `/items/{item_id}` _adresi_ opsiyonel bir `str` _sorgu paramtersine_ sahip bu da `q`.

### İnteraktif API dokümantasyonu

Şimdi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> adresine git.

Senin için otomatik oluşturulmuş(<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> tarafından sağlanan) interaktif bir API dokümanı göreceksin:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternatif API dokümantasyonu

Şimdi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> adresine git.

Senin için alternatif olarak (<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> tarafından sağlanan) bir API dokümantasyonu daha göreceksin:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Örnek bir değişiklik

Şimdi `main.py` dosyasını değiştirelim ve body ile `PUT` talebi alabilir hale getirelim.

Şimdi Pydantic sayesinde, Python'un standart tiplerini kullanarak bir body tanımlayacağız.

```Python hl_lines="4  9 10 11 12  25 26 27"
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

Server otomatik olarak yeniden başlamalı (çünkü yukarıda `uvicorn`'u çalıştırırken `--reload` parametresini kullandık.).

### İnteraktif API dokümantasyonu'nda değiştirme yapmak

Şimdi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> bağlantısına tekrar git.

* İnteraktif API dokümantasyonu, yeni body ile beraber çoktan yenilenmiş olması lazım:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* "Try it out"a tıkla, bu senin API parametleri üzerinde deneme yapabilmene izin veriyor:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Şimdi "Execute" butonuna tıkla, kullanıcı arayüzü otomatik olarak API'ın ile bağlantı kurarak ona bu parametreleri gönderecek ve sonucu karşına getirecek.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternatif API dokümantasyonunda değiştirmek

Şimdi ise <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> adresine git.

* Alternatif dokümantasyonda koddaki değişimler ile beraber kendini yeni query ve body ile güncelledi.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Özet

Özetleyecek olursak, URL, sorgu veya request body'deki parametrelerini fonksiyon parametresi olarak kullanıyorsun. Bu parametrelerin veri tiplerini bir kere belirtmen yeterli.

Type-hinting işlemini Python dilindeki standart veri tipleri ile yapabilirsin

Yeni bir syntax'e alışmana gerek yok, metodlar ve classlar zaten spesifik kütüphanelere ait.

Sadece standart **Python 3.6+**.

Örnek olarak, `int` tanımlamak için:

```Python
item_id: int
```

ya da daha kompleks `Item` tipi:

```Python
item: Item
```

...sadece kısa bir parametre tipi belirtmekle beraber, sahip olacakların:

* Editör desteği dahil olmak üzere:
    * Otomatik tamamlama.
    * Tip sorguları.
* Datanın tipe uyumunun sorgulanması:
    * Eğer data geçersiz ise, otomatik olarak hataları ayıklar.
    * Çok derin JSON objelerinde bile veri tipi sorgusu yapar.
* Gelen verinin  <abbr title="parsing, serializing, marshalling olarakta biliniyor">dönüşümünü</abbr> aşağıdaki veri tiplerini kullanarak gerçekleştirebiliyor.
    * JSON.
    * Path parametreleri.
    * Query parametreleri.
    * Cookies.
    * Headers.
    * Forms.
    * Files.
* Giden verinin <abbr title="also known as: serialization, parsing, marshalling">dönüşümünü</abbr> aşağıdaki veri tiplerini kullanarak gerçekleştirebiliyor (JSON olarak):
    * Python tiplerinin (`str`, `int`, `float`, `bool`, `list`, vs) çevirisi.
    * `datetime` objesi.
    * `UUID` objesi.
    * Veritabanı modelleri.
    * ve daha fazlası...
* 2 alternatif kullanıcı arayüzü dahil olmak üzere, otomatik interaktif API dokümanu:
    * Swagger UI.
    * ReDoc.

---

Az önceki kod örneğine geri dönelim, **FastAPI**'ın yapacaklarına bir bakış atalım:

* `item_id`'nin `GET` ve `PUT` talepleri içinde olup olmadığının doğruluğunu kontol edecek.
* `item_id`'nin tipinin `int` olduğunu `GET` ve `PUT` talepleri içinde olup olmadığının doğruluğunu kontol edecek.
    * Eğer `GET` ve `PUT` içinde yok ise ve `int` değil ise, sebebini belirten bir hata mesajı gösterecek
* Opsiyonel bir `q` parametresinin `GET` talebi için (`http://127.0.0.1:8000/items/foo?q=somequery` içinde) olup olmadığını kontrol edecek
    * `q` parametresini `= None` ile oluşturduğumuz için, opsiyonel bir parametre olacak.
    * Eğer `None` olmasa zorunlu bir parametre olacak idi (bu yüzden body'de `PUT` parametresi var).
* `PUT` talebi için `/items/{item_id}`'nin body'sini, JSON olarak okuyor:
    * `name` adında bir parametetre olup olmadığını ve var ise onun `str` olup olmadığını kontol ediyor.
    * `price` adında bir parametetre olup olmadığını ve var ise onun `float` olup olmadığını kontol ediyor.
    * `is_offer` adında bir parametetre olup olmadığını ve var ise onun `bool` olup olmadığını kontol ediyor.
    * Bunların hepsini en derin JSON modellerinde bile yapacaktır.
* Bütün veri tiplerini otomatik olarak JSON'a çeviriyor veya tam tersi.
* Her şeyi dokümanlayıp, çeşitli yerlerde:
    * İnteraktif dokümantasyon sistemleri.
    * Otomatik alıcı kodu üretim sistemlerinde ve çeşitli dillerde.
* İki ayrı web arayüzüyle direkt olarak interaktif bir dokümantasyon sunuyor.

---

Henüz yüzeysel bir bakış attık, fakat sen çoktan çalışma mantığını anladın.

Şimdi aşağıdaki satırı değiştirmeyi dene:

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

...şimdi editör desteğinin nasıl veri tiplerini bildiğini ve otomatik tamamladığını gör:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Daha fazla örnek ve özellik için <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - User Guide</a> sayfasını git.

**Spoiler**: Öğretici - Kullanıcı rehberi şunları içeriyor:

* **Parameterlerini** nasıl **headers**, **cookies**, **form fields** ve **files** olarak deklare edebileceğini.
* `maximum_length` ya da `regex` gibi şeylerle nasıl **doğrulama** yapabileceğini.
* Çok güçlü ve kullanımı kolay **<abbr title="also known as components, resources, providers, services, injectables">Zorunluluk Entegrasyonu</abbr>** oluşturmayı.
* Güvenlik ve kimlik doğrulama, **JWT tokenleri**'yle beraber **OAuth2** desteği, ve **HTTP Basic** doğrulaması.
* İleri seviye fakat ona göre oldukça basit olan **derince oluşturulmuş JSON modelleri** (Pydantic sayesinde).
* Diğer ekstra özellikler (Starlette sayesinde):
    * **WebSockets**
    * **GraphQL**
    * HTTPX ve `pytest` sayesinde aşırı kolay testler.
    * **CORS**
    * **Cookie Sessions**
    * ...ve daha fazlası.

## Performans

Bağımsız TechEmpower kıyaslamaları gösteriyor ki, Uvicorn'la beraber çalışan **FastAPI** uygulamaları <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">Python'un en hızlı frameworklerinden birisi </a>, sadece Starlette ve Uvicorn'dan daha yavaş ki FastAPI bunların üzerine kurulu.

Daha fazla bilgi için, bu bölüme bir göz at <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Opsiyonel gereksinimler

Pydantic tarafında kullanılan:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - email doğrulaması için.

Starlette tarafında kullanılan:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Eğer `TestClient` kullanmak istiyorsan gerekli.
* <a href="http://jinja.pocoo.org" target="_blank"><code>jinja2</code></a> - Eğer kendine ait template konfigürasyonu oluşturmak istiyorsan gerekli
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Form kullanmak istiyorsan gerekli <abbr title="HTTP bağlantısından gelen stringi Python objesine çevirmek için">("dönüşümü")</abbr>.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - `SessionMiddleware` desteği için gerekli.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - `SchemaGenerator` desteği için gerekli (Muhtemelen FastAPI kullanırken ihtiyacınız olmaz).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - `GraphQLApp` desteği için gerekli.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - `UJSONResponse` kullanmak istiyorsan gerekli.

Hem FastAPI hem de Starlette tarafından kullanılan:

* <a href="http://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - oluşturduğumuz uygulamayı bir web sunucusuna servis etmek için gerekli
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - `ORJSONResponse` kullanmak istiyor isen gerekli.

Bunların hepsini `pip install fastapi[all]` ile yükleyebilirsin.

## Lisans

Bu proje, MIT lisansı şartlarına göre lisanslanmıştır.
