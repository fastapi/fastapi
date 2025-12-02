# FastAPI

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, yüksek performanslı, öğrenmesi oldukça kolay, kodlaması hızlı, kullanıma hazır</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Dokümantasyon**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Kaynak Kod**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI, Python 'nin standart <abbr title="Tip Belirteçleri: Type Hints">tip belirteçleri</abbr>ne dayalı, modern ve hızlı (yüksek performanslı) API'lar oluşturmak için kullanılabilecek web framework'tür.

Temel özellikleri şunlardır:

* **Hızlı**: Çok yüksek performanslı, **NodeJS** ve **Go** ile eşit düzeyde (Starlette ve Pydantic sayesinde). [En hızlı Python framework'lerinden bir tanesidir](#performans).
* **Kodlaması Hızlı**: Geliştirme hızını yaklaşık %200 ile %300 aralığında arttırır. *
* **Daha az hata**: İnsan (geliştirici) kaynaklı hataları yaklaşık %40 azaltır. *
* **Sezgisel**: Muhteşem bir editör desteği. Her yerde <abbr title="Otomatik Tamamlama: auto-complete, autocompletion, IntelliSense">otomatik tamamlama</abbr>. Hata ayıklama ile daha az zaman harcayacaksınız.
* **Kolay**: Öğrenmesi ve kullanması kolay olacak şekilde tasarlandı. Doküman okuma ile daha az zaman harcayacaksınız.
* **Kısa**: Kod tekrarı minimize edildi. Her parametre tanımlamasında birden fazla özellik ve daha az hatayla karşılaşacaksınız.
* **Güçlü**: Otomatik ve etkileşimli dokümantasyon ile birlikte, kullanıma hazır kod elde edebilirsiniz.
* **Standard öncelikli**: API'lar için açık standartlara dayalı (ve tamamen uyumlu); <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (eski adıyla Swagger) ve <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* ilgili kanılar, dahili geliştirme ekibinin geliştirdikleri ürünlere yaptıkları testlere dayanmaktadır.</small>

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

<a href="https://fastapi.tiangolo.com/tr/fastapi-people/#sponsors" class="external-link" target="_blank">Diğer Sponsorlar</a>

## Görüşler

"_[...] Bugünlerde **FastAPI**'ı çok fazla kullanıyorum. [...] Aslında bunu ekibimin **Microsoft'taki Machine Learning servislerinin** tamamında kullanmayı planlıyorum. Bunlardan bazıları **Windows**'un ana ürünlerine ve **Office** ürünlerine entegre ediliyor._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_**FastAPI**'ı **tahminlerimiz**'i sorgulanabilir hale getirecek bir **REST** sunucu oluşturmak için benimsedik/kullanmaya başladık._"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix**, **kriz yönetiminde** orkestrasyon yapabilmek için geliştirdiği yeni framework'ü **Dispatch**'in, açık kaynak sürümünü paylaşmaktan gurur duyuyor. [**FastAPI** ile yapıldı.]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_**FastAPI** için ayın üzerindeymişcesine heyecanlıyım. Çok eğlenceli!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Dürüst olmak gerekirse, inşa ettiğiniz şey gerçekten sağlam ve profesyonel görünüyor. Birçok açıdan **Hug**'ın olmasını istediğim şey tam da bu - böyle bir şeyi inşa eden birini görmek gerçekten ilham verici._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="http://www.hug.rest/" target="_blank">Hug</a>'ın Yaratıcısı</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Eğer REST API geliştirmek için **modern bir framework** öğrenme arayışında isen, **FastAPI**'a bir göz at [...] Hızlı, kullanımı ve öğrenmesi kolay. [...]_"

"_**API** servislerimizi **FastAPI**'a taşıdık [...] Sizin de beğeneceğinizi düşünüyoruz. [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> kurucuları - <a href="https://spacy.io" target="_blank">spaCy</a> yaratıcıları</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_Python ile kullanıma hazır bir API oluşturmak isteyen herhangi biri için, **FastAPI**'ı şiddetle tavsiye ederim. **Harika tasarlanmış**, **kullanımı kolay** ve **yüksek ölçeklenebilir**, API odaklı geliştirme stratejimizin **ana bileşeni** haline geldi ve Virtual TAC Engineer gibi birçok otomasyon ve servisi yönetiyor._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## Komut Satırı Uygulamalarının FastAPI'ı: **Typer**

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Eğer API yerine, terminalde kullanılmak üzere bir <abbr title="Komut Satırı: Command Line Interface">komut satırı uygulaması</abbr> geliştiriyorsanız <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>'a göz atabilirsiniz.

**Typer** kısaca FastAPI'ın küçük kardeşi. Ve hedefi komut satırı uygulamalarının **FastAPI'ı** olmak. ⌨️ 🚀

## Gereksinimler

FastAPI iki devin omuzları üstünde duruyor:

* Web tarafı için <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a>.
* Data tarafı için <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>.

## Kurulum

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Uygulamamızı kullanılabilir hale getirmek için <a href="http://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a> ya da <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a> gibi bir ASGI sunucusuna ihtiyacımız olacak.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## Örnek

### Kodu Oluşturalım

* `main.py` adında bir dosya oluşturup içine şu kodu yapıştıralım:

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

Eğer kodunuzda `async` / `await` varsa, `async def` kullanalım:

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

**Not**:

Eğer bu konu hakkında bilginiz yoksa <a href="https://fastapi.tiangolo.com/tr/async/#in-a-hurry" target="_blank">`async` ve `await`</a> dokümantasyonundaki _"Aceleniz mi var?"_ kısmını kontrol edebilirsiniz.

</details>

### Kodu Çalıştıralım

Sunucuyu aşağıdaki komutla çalıştıralım:

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
<summary><code>uvicorn main:app --reload</code> komutuyla ilgili...</summary>

`uvicorn main:app` komutunu şu şekilde açıklayabiliriz:

* `main`: dosya olan `main.py` (yani Python "modülü").
* `app`: ise `main.py` dosyasının içerisinde `app = FastAPI()` satırında oluşturduğumuz `FastAPI` nesnesi.
* `--reload`: kod değişikliklerinin ardından sunucuyu otomatik olarak yeniden başlatır. Bu parameteyi sadece geliştirme aşamasında kullanmalıyız.

</details>

### Şimdi de Kontrol Edelim

Tarayıcımızda şu bağlantıyı açalım <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Aşağıdaki gibi bir JSON yanıtıyla karşılaşacağız:

```JSON
{"item_id": 5, "q": "somequery"}
```

Az önce oluşturduğumuz API:

* `/` ve `/items/{item_id}` <abbr title="Adres / Yol: Path ">_yollarına_</abbr> HTTP isteği alabilir.
* İki _yolda_ `GET` <em>operasyonlarını</em> (HTTP _metodları_ olarak da bilinen) kabul ediyor.
* `/items/{item_id}` _yolu_ `item_id` adında bir _yol parametresine_ sahip ve bu parametre `int` değer almak zorundadır.
* `/items/{item_id}` _yolu_ `q` adında bir _yol parametresine_ sahip ve bu parametre opsiyonel olmakla birlikte, `str` değer almak zorundadır.

### Etkileşimli API Dokümantasyonu

Şimdi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> bağlantısını açalım.

<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> tarafından sağlanan otomatik etkileşimli bir API dokümantasyonu göreceğiz:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternatif API Dokümantasyonu

Şimdi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> bağlantısını açalım.

<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> tarafından sağlanan otomatik dokümantasyonu göreceğiz:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Örneği Güncelleyelim

Şimdi `main.py` dosyasını, `PUT` isteğiyle birlikte bir gövde alacak şekilde değiştirelim.

<abbr title="Gövde: Body">Gövde</abbr>yi Pydantic sayesinde standart python tiplerini kullanarak tanımlayalım.

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

Sunucu otomatik olarak yeniden başlamış olmalı (çünkü yukarıda `uvicorn` komutuyla birlikte `--reload` parametresini kullandık).

### Etkileşimli API Dokümantasyonundaki Değişimi Görelim

Şimdi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> bağlantısına tekrar gidelim.

* Etkileşimli API dokümantasyonu, yeni gövdede dahil olmak üzere otomatik olarak güncellenmiş olacak:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* "Try it out" butonuna tıklayalım, bu işlem API parametleri üzerinde değişiklik yapmamıza ve doğrudan API ile etkileşime geçmemize imkan sağlayacak:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Şimdi "Execute" butonuna tıklayalım, kullanıcı arayüzü API'ımız ile bağlantı kurup parametreleri gönderecek ve sonucu ekranımıza getirecek:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternatif API Dokümantasyonundaki Değişimi Görelim

Şimdi ise <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> bağlantısına tekrar gidelim.

* Alternatif dokümantasyonda yaptığımız değişiklikler ile birlikte yeni sorgu parametresi ve gövde bilgisi ile güncelemiş olacak:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Özet

Özetlemek gerekirse, parametrelerin, gövdenin, vb. veri tiplerini fonksiyon parametreleri olarak **bir kere** tanımlıyoruz.

Bu işlemi standart modern Python tipleriyle yapıyoruz.

Yeni bir sözdizimi yapısını, bir kütüphane özel metod veya sınıfları öğrenmeye gerek yoktur.

Hepsi sadece **Python** standartlarına dayalıdır.

Örnek olarak, `int` tanımlamak için:

```Python
item_id: int
```

ya da daha kompleks herhangi bir python modelini tanımlayabiliriz, örneğin `Item` modeli için:

```Python
item: Item
```

...ve sadece kısa bir parametre tipi belirterek elde ettiklerimiz:

* Editör desteğiyle birlikte:
    * Otomatik tamamlama.
    * Tip kontrolü.
* Veri Doğrulama:
    * Veri geçerli değilse, otomatik olarak açıklayıcı hatalar gösterir.
    * Çok <abbr title="Derin / İç içe: Nested">derin</abbr> JSON nesnelerinde bile doğrulama yapar.
* Gelen verinin <abbr title="Dönüşüm: serialization, parsing, marshalling olarak da biliniyor">dönüşümünü</abbr> aşağıdaki veri tiplerini kullanarak gerçekleştirir:
    * JSON.
    * Yol parametreleri.
    * Sorgu parametreleri.
    * Çerezler.
    * Headers.
    * Formlar.
    * Dosyalar.
* Giden verinin <abbr title="Dönüşüm: serialization, parsing, marshalling olarak da biliniyor">dönüşümünü</abbr> aşağıdaki veri tiplerini kullanarak gerçekleştirir (JSON olarak):
    * Python tiplerinin (`str`, `int`, `float`, `bool`, `list`, vb) dönüşümü.
    * `datetime` nesnesi.
    * `UUID` nesnesi.
    * Veritabanı modelleri.
    * ve çok daha fazlası...
* 2 alternatif kullanıcı arayüzü dahil olmak üzere, otomatik etkileşimli API dokümantasyonu sağlar:
    * Swagger UI.
    * ReDoc.

---

Az önceki örneğe geri dönelim, **FastAPI**'ın yapacaklarına bir bakış atalım:

* `item_id`'nin `GET` ve `PUT` istekleri için, yolda olup olmadığının kontol edecek.
* `item_id`'nin `GET` ve `PUT` istekleri için, tipinin `int` olduğunu doğrulayacak.
    * Eğer değilse, sebebini belirten bir hata mesajı gösterecek.
* Opsiyonel bir `q` parametresinin `GET` isteği içinde (`http://127.0.0.1:8000/items/foo?q=somequery` gibi) olup olmadığını kontrol edecek
    * `q` parametresini `= None` ile oluşturduğumuz için, opsiyonel bir parametre olacak.
    * Eğer `None` olmasa zorunlu bir parametre olacaktı (`PUT` metodunun gövdesinde olduğu gibi).
* `PUT` isteği için `/items/{item_id}`'nin gövdesini, JSON olarak doğrulayıp okuyacak:
    * `name` adında zorunlu bir parametre olup olmadığını ve varsa tipinin `str` olup olmadığını kontol edecek.
    * `price` adında zorunlu bir parametre olup olmadığını ve varsa tipinin `float` olup olmadığını kontol edecek.
    * `is_offer` adında opsiyonel bir parametre olup olmadığını ve varsa tipinin `float` olup olmadığını kontol edecek.
    * Bunların hepsi en derin JSON nesnelerinde bile çalışacak.
* Verilerin JSON'a ve JSON'ın python nesnesine dönüşümü otomatik olarak yapılacak.
* Her şeyi OpenAPI ile uyumlu bir şekilde otomatik olarak dokümanlayacak ve bunlarda aşağıdaki gibi kullanılabilecek:
    * Etkileşimli dokümantasyon sistemleri.
    * Bir çok programlama dili için otomatik istemci kodu üretim sistemleri.
* İki ayrı etkileşimli dokümantasyon arayüzünü doğrudan sağlayacak.

---

Daha yeni başladık ama çalışma mantığını çoktan anlamış oldunuz.

Şimdi aşağıdaki satırı değiştirmeyi deneyin:

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

...ve editörünün veri tiplerini bildiğini ve otomatik tamamladığını göreceksiniz:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Daha fazal özellik içeren, daha eksiksiz bir örnek için <a href="https://fastapi.tiangolo.com/tr/tutorial/">Öğretici - Kullanıcı Rehberi</a> sayfasını ziyaret edebilirsin.

**Spoiler**: Öğretici - Kullanıcı rehberi şunları içerir:

* **Parameterlerin**, **headers**, **çerezler**, **form alanları** ve **dosyalar** olarak tanımlanması.
* `maximum_length` ya da `regex` gibi **doğrulama kısıtlamalarının** nasıl yapılabileceği.
* Çok güçlü ve kullanımı kolay **<abbr title="Bağımlılık Enjeksiyonu: components, resources, providers, services, injectables olarak da biliniyor.">Bağımlılık Enjeksiyonu</abbr>** sistemi oluşturmayı.
* Güvenlik ve kimlik doğrulama, **JWT tokenleri** ile **OAuth2** desteği, ve **HTTP Basic** doğrulaması.
* İleri seviye fakat bir o kadarda basit olan **çok derin JSON modelleri** (Pydantic sayesinde).
* **GraphQL** entegrasyonu: <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> ve diğer kütüphaneleri kullanarak.
* Diğer ekstra özellikler (Starlette sayesinde):
    * **WebSocketler**
    * HTTPX ve `pytest` sayesinde aşırı kolay testler.
    * **CORS**
    * **Cookie Sessions**
    * ...ve daha fazlası.

## Performans

Bağımsız TechEmpower kıyaslamaları gösteriyor ki, Uvicorn ile çalıştırılan **FastAPI** uygulamaları <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">en hızlı Python framework'lerinden birisi</a>, sadece Starlette ve Uvicorn'dan yavaş, ki FastAPI bunların üzerine kurulu bir kütüphanedir.

Daha fazla bilgi için, bu bölüme bir göz at <a href="https://fastapi.tiangolo.com/tr/benchmarks/" class="internal-link" target="_blank">Kıyaslamalar</a>.

## Opsiyonel Gereksinimler

Pydantic tarafında kullanılan:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - email doğrulaması için.
* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - ayar yönetimi için.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - Pydantic ile birlikte kullanılabilecek ek tipler için.

Starlette tarafında kullanılan:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Eğer `TestClient` yapısını kullanacaksanız gereklidir.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Eğer varsayılan template konfigürasyonunu kullanacaksanız gereklidir.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - Eğer `request.form()` ile form <abbr title="HTTP isteği ile gelen string veriyi Python nesnesine çevirme.">dönüşümü</abbr> desteğini kullanacaksanız gereklidir.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - `SessionMiddleware` desteği için gerekli.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - `SchemaGenerator` desteği için gerekli (Muhtemelen FastAPI kullanırken ihtiyacınız olmaz).

Hem FastAPI hem de Starlette tarafından kullanılan:

* <a href="https://www.uvicorn.dev" target="_blank"><code>uvicorn</code></a> - oluşturduğumuz uygulamayı servis edecek web sunucusu görevini üstlenir.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - `ORJSONResponse` kullanacaksanız gereklidir.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - `UJSONResponse` kullanacaksanız gerekli.

Bunların hepsini `pip install fastapi[all]` ile yükleyebilirsin.

## Lisans

Bu proje, MIT lisansı şartları altında lisanslanmıştır.
