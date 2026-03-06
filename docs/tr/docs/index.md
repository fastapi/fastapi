# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/tr"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, yüksek performanslı, öğrenmesi kolay, kodlaması hızlı, production'a hazır</em>
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

**Dokümantasyon**: <a href="https://fastapi.tiangolo.com/tr" target="_blank">https://fastapi.tiangolo.com</a>

**Kaynak Kod**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI, Python'un standart type hints'lerine dayalı olarak Python ile API'lar oluşturmak için kullanılan modern ve hızlı (yüksek performanslı) bir web framework'üdür.

Temel özellikleri şunlardır:

* **Hızlı**: Çok yüksek performanslı, **NodeJS** ve **Go** ile eşit düzeyde (Starlette ve Pydantic sayesinde). [Mevcut en hızlı Python framework'lerinden biri](#performance).
* **Kodlaması Hızlı**: Özellik geliştirme hızını yaklaşık %200 ile %300 aralığında artırır. *
* **Daha az hata**: İnsan (geliştirici) kaynaklı hataları yaklaşık %40 azaltır. *
* **Sezgisel**: Harika bir editör desteği. Her yerde <dfn title="oto-tamamlama, autocompletion, IntelliSense olarak da bilinir">Tamamlama</dfn>. Hata ayıklamaya daha az zaman.
* **Kolay**: Kullanımı ve öğrenmesi kolay olacak şekilde tasarlandı. Doküman okumaya daha az zaman.
* **Kısa**: Kod tekrarını minimize eder. Her parametre tanımından birden fazla özellik. Daha az hata.
* **Sağlam**: Production'a hazır kod elde edersiniz. Otomatik etkileşimli dokümantasyon ile birlikte.
* **Standardlara dayalı**: API'lar için açık standartlara dayalıdır (ve tamamen uyumludur); <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (önceden Swagger olarak biliniyordu) ve <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* tahmin, production uygulamalar geliştiren dahili bir geliştirme ekibinin yaptığı testlere dayanmaktadır.</small>

## Sponsorlar { #sponsors }

<!-- sponsors -->

### Keystone Sponsor { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### Gold and Silver Sponsors { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/tr/fastapi-people/#sponsors" class="external-link" target="_blank">Diğer sponsorlar</a>

## Görüşler { #opinions }

"_[...] Bugünlerde **FastAPI**'ı çok fazla kullanıyorum. [...] Aslında bunu ekibimin **Microsoft'taki ML servislerinin** tamamında kullanmayı planlıyorum. Bunlardan bazıları ana **Windows** ürününe ve bazı **Office** ürünlerine entegre ediliyor._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_**predictions** almak için sorgulanabilecek bir **REST** server oluşturmak amacıyla **FastAPI** kütüphanesini benimsedik. [Ludwig için]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix**, **kriz yönetimi** orkestrasyon framework'ümüz: **Dispatch**'in open-source sürümünü duyurmaktan memnuniyet duyar! [**FastAPI** ile geliştirildi]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_**FastAPI** için ayın üzerindeymişcesine heyecanlıyım. Çok eğlenceli!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Dürüst olmak gerekirse, inşa ettiğiniz şey gerçekten sağlam ve profesyonel görünüyor. Birçok açıdan, **Hug**'ın olmasını istediğim şey tam da bu - böyle bir şeyi inşa eden birini görmek gerçekten ilham verici._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> yaratıcısı</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_REST API'lar geliştirmek için **modern bir framework** öğrenmek istiyorsanız, **FastAPI**'a bir göz atın [...] Hızlı, kullanımı ve öğrenmesi kolay [...]_"

"_**API**'larımız için **FastAPI**'a geçtik [...] Bence hoşunuza gidecek [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> kurucuları - <a href="https://spacy.io" target="_blank">spaCy</a> yaratıcıları</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_Production'da Python API geliştirmek isteyen herkese **FastAPI**'ı şiddetle tavsiye ederim. **Harika tasarlanmış**, **kullanımı kolay** ve **yüksek ölçeklenebilir**; API-first geliştirme stratejimizin **kilit bir bileşeni** haline geldi ve Virtual TAC Engineer gibi birçok otomasyon ve servise güç veriyor._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## FastAPI mini belgeseli { #fastapi-mini-documentary }

2025'in sonunda yayınlanan bir <a href="https://www.youtube.com/watch?v=mpR8ngthqiE" class="external-link" target="_blank">FastAPI mini belgeseli</a> var, online olarak izleyebilirsiniz:

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE" target="_blank"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## CLI'ların FastAPI'ı: **Typer** { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Web API yerine terminalde kullanılacak bir <abbr title="Command Line Interface - Komut Satırı Arayüzü">CLI</abbr> uygulaması geliştiriyorsanız <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>'a göz atın.

**Typer**, FastAPI'ın küçük kardeşi. Ve hedefi CLI'ların **FastAPI'ı** olmak. ⌨️ 🚀

## Gereksinimler { #requirements }

FastAPI iki devin omuzları üstünde duruyor:

* Web kısımları için <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a>.
* Data kısımları için <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>.

## Kurulum { #installation }

Bir <a href="https://fastapi.tiangolo.com/tr/virtual-environments/" class="external-link" target="_blank">virtual environment</a> oluşturup etkinleştirelim ve ardından FastAPI'ı yükleyelim:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Not**: Tüm terminallerde çalıştığından emin olmak için `"fastapi[standard]"` ifadesini tırnak içinde yazdığınızdan emin olun.

## Örnek { #example }

### Oluşturalım { #create-it }

Şu içerikle `main.py` adında bir dosya oluşturalım:

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
<summary>Ya da <code>async def</code> kullanalım...</summary>

Eğer kodunuz `async` / `await` kullanıyorsa, `async def` kullanın:

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

**Not**:

Eğer bilmiyorsanız, dokümanlardaki <a href="https://fastapi.tiangolo.com/tr/async/#in-a-hurry" target="_blank">`async` ve `await`</a> hakkında _"Aceleniz mi var?"_ bölümüne bakın.

</details>

### Çalıştıralım { #run-it }

Sunucuyu şu komutla çalıştıralım:

<div class="termy">

```console
$ fastapi dev main.py

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
<summary><code>fastapi dev main.py</code> komutu hakkında...</summary>

`fastapi dev` komutu, `main.py` dosyanızı okur, içindeki **FastAPI** uygulamasını algılar ve <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a> kullanarak bir server başlatır.

Varsayılan olarak `fastapi dev`, local geliştirme için auto-reload etkin şekilde başlar.

Daha fazla bilgi için <a href="https://fastapi.tiangolo.com/tr/fastapi-cli/" target="_blank">FastAPI CLI dokümantasyonu</a>'nu okuyabilirsiniz.

</details>

### Kontrol Edelim { #check-it }

Tarayıcınızda şu bağlantıyı açın: <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Şu JSON response'unu göreceksiniz:

```JSON
{"item_id": 5, "q": "somequery"}
```

Artık şunları yapan bir API oluşturdunuz:

* `/` ve `/items/{item_id}` _path_'lerinde HTTP request'leri alır.
* Her iki _path_ de `GET` <em>operasyonlarını</em> (HTTP _method_'ları olarak da bilinir) kabul eder.
* `/items/{item_id}` _path_'i, `int` olması gereken `item_id` adlı bir _path parameter_'a sahiptir.
* `/items/{item_id}` _path_'i, opsiyonel `str` bir _query parameter_ olan `q`'ya sahiptir.

### Etkileşimli API dokümantasyonu { #interactive-api-docs }

Şimdi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> adresine gidin.

Otomatik etkileşimli API dokümantasyonunu göreceksiniz (<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> tarafından sağlanır):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternatif API dokümantasyonu { #alternative-api-docs }

Ve şimdi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> adresine gidin.

Alternatif otomatik dokümantasyonu göreceksiniz (<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> tarafından sağlanır):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Örneği Güncelleyelim { #example-upgrade }

Şimdi `main.py` dosyasını, `PUT` request'iyle gelen bir body alacak şekilde değiştirelim.

Body'yi Pydantic sayesinde standart Python tiplerini kullanarak tanımlayalım.

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

`fastapi dev` server'ı otomatik olarak yeniden yüklemelidir.

### Etkileşimli API dokümantasyonu güncellemesi { #interactive-api-docs-upgrade }

Şimdi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> adresine gidin.

* Etkileşimli API dokümantasyonu, yeni body dahil olacak şekilde otomatik olarak güncellenecek:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* "Try it out" butonuna tıklayın; parametreleri doldurmanıza ve API ile doğrudan etkileşime girmenize olanak sağlar:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Sonra "Execute" butonuna tıklayın; kullanıcı arayüzü API'nız ile iletişim kuracak, parametreleri gönderecek, sonuçları alacak ve ekranda gösterecek:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternatif API dokümantasyonu güncellemesi { #alternative-api-docs-upgrade }

Ve şimdi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> adresine gidin.

* Alternatif dokümantasyon da yeni query parameter ve body'yi yansıtacak:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Özet { #recap }

Özetle, parametrelerin, body'nin vb. type'larını fonksiyon parametreleri olarak **bir kere** tanımlarsınız.

Bunu standart modern Python tipleriyle yaparsınız.

Yeni bir syntax, belirli bir kütüphanenin method'larını ya da class'larını vb. öğrenmeniz gerekmez.

Sadece standart **Python**.

Örneğin bir `int` için:

```Python
item_id: int
```

ya da daha karmaşık bir `Item` modeli için:

```Python
item: Item
```

...ve bu tek tanımla şunları elde edersiniz:

* Şunlar dahil editör desteği:
    * Completion.
    * Type kontrolleri.
* Verinin doğrulanması:
    * Veri geçersiz olduğunda otomatik ve anlaşılır hatalar.
    * Çok derin iç içe JSON nesneleri için bile doğrulama.
* Girdi verisinin <dfn title="şöyle de bilinir: serileştirme, ayrıştırma, marshalling">Dönüşümü</dfn>: network'ten gelen veriyi Python verisine ve type'larına çevirir. Şunlardan okur:
    * JSON.
    * Path parameter'lar.
    * Query parameter'lar.
    * Cookie'ler.
    * Header'lar.
    * Form'lar.
    * File'lar.
* Çıktı verisinin <dfn title="şöyle de bilinir: serileştirme, ayrıştırma, marshalling">Dönüşümü</dfn>: Python verisini ve type'larını network verisine çevirir (JSON olarak):
    * Python type'larını dönüştürür (`str`, `int`, `float`, `bool`, `list`, vb.).
    * `datetime` nesneleri.
    * `UUID` nesneleri.
    * Veritabanı modelleri.
    * ...ve daha fazlası.
* 2 alternatif kullanıcı arayüzü dahil otomatik etkileşimli API dokümantasyonu:
    * Swagger UI.
    * ReDoc.

---

Önceki kod örneğine dönersek, **FastAPI** şunları yapacaktır:

* `GET` ve `PUT` request'leri için path'te `item_id` olduğunu doğrular.
* `GET` ve `PUT` request'leri için `item_id`'nin type'ının `int` olduğunu doğrular.
    * Değilse, client faydalı ve anlaşılır bir hata görür.
* `GET` request'leri için `q` adlı opsiyonel bir query parameter olup olmadığını kontrol eder (`http://127.0.0.1:8000/items/foo?q=somequery` örneğindeki gibi).
    * `q` parametresi `= None` ile tanımlandığı için opsiyoneldir.
    * `None` olmasaydı zorunlu olurdu (tıpkı `PUT` örneğindeki body gibi).
* `/items/{item_id}`'ye yapılan `PUT` request'leri için body'yi JSON olarak okur:
    * `str` olması gereken, zorunlu `name` alanı olduğunu kontrol eder.
    * `float` olması gereken, zorunlu `price` alanı olduğunu kontrol eder.
    * Varsa, `bool` olması gereken opsiyonel `is_offer` alanını kontrol eder.
    * Bunların hepsi çok derin iç içe JSON nesneleri için de çalışır.
* JSON'a ve JSON'dan dönüşümü otomatik yapar.
* Her şeyi OpenAPI ile dokümante eder; bu dokümantasyon şunlar tarafından kullanılabilir:
    * Etkileşimli dokümantasyon sistemleri.
    * Birçok dil için otomatik client kodu üretim sistemleri.
* 2 etkileşimli dokümantasyon web arayüzünü doğrudan sunar.

---

Daha yolun başındayız, ama bunun nasıl çalıştığı hakkında fikri kaptınız.

Şu satırı değiştirmeyi deneyin:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...şundan:

```Python
        ... "item_name": item.name ...
```

...şuna:

```Python
        ... "item_price": item.price ...
```

...ve editörünüzün alanları otomatik tamamladığını ve type'larını bildiğini görün:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Daha fazla özellik içeren daha kapsamlı bir örnek için <a href="https://fastapi.tiangolo.com/tr/tutorial/">Öğretici - Kullanıcı Rehberi</a>'ne bakın.

**Spoiler alert**: öğretici - kullanıcı rehberi şunları içerir:

* **parameter**'ların farklı yerlerden: **header**'lar, **cookie**'ler, **form alanları** ve **file**'lar olarak tanımlanması.
* `maximum_length` ya da `regex` gibi **doğrulama kısıtlamalarının** nasıl ayarlanacağı.
* Çok güçlü ve kullanımı kolay bir **<dfn title="şöyle de bilinir: bileşenler, kaynaklar, sağlayıcılar, servisler, enjekte edilebilirler">Bağımlılık Enjeksiyonu</dfn>** sistemi.
* **JWT tokens** ve **HTTP Basic** auth ile **OAuth2** desteği dahil güvenlik ve kimlik doğrulama.
* **Çok derin iç içe JSON modelleri** tanımlamak için daha ileri (ama aynı derecede kolay) teknikler (Pydantic sayesinde).
* <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> ve diğer kütüphaneler ile **GraphQL** entegrasyonu.
* Starlette sayesinde gelen birçok ek özellik:
    * **WebSockets**
    * HTTPX ve `pytest` tabanlı aşırı kolay testler
    * **CORS**
    * **Cookie Sessions**
    * ...ve daha fazlası.

### Uygulamanızı deploy edin (opsiyonel) { #deploy-your-app-optional }

İsterseniz FastAPI uygulamanızı <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>'a deploy edebilirsiniz; eğer henüz yapmadıysanız gidip bekleme listesine katılın. 🚀

Zaten bir **FastAPI Cloud** hesabınız varsa (bekleme listesinden sizi davet ettiysek 😉), uygulamanızı tek bir komutla deploy edebilirsiniz.

Deploy etmeden önce, giriş yaptığınızdan emin olun:

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

Sonra uygulamanızı deploy edin:

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

Hepsi bu! Artık uygulamanıza bu URL'den erişebilirsiniz. ✨

#### FastAPI Cloud hakkında { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>**, **FastAPI**'ın arkasındaki aynı yazar ve ekip tarafından geliştirilmiştir.

**Bir API'ı build etmek**, **deploy etmek** ve **erişmek** süreçlerini minimum eforla kolaylaştırır.

FastAPI ile uygulama geliştirmenin sağladığı aynı **developer experience**'ı, onları cloud'a **deploy etmeye** de taşır. 🎉

FastAPI Cloud, *FastAPI and friends* open source projelerinin ana sponsoru ve finansman sağlayıcısıdır. ✨

#### Diğer cloud sağlayıcılarına deploy { #deploy-to-other-cloud-providers }

FastAPI open source'tur ve standartlara dayanır. FastAPI uygulamalarını seçtiğiniz herhangi bir cloud sağlayıcısına deploy edebilirsiniz.

FastAPI uygulamalarını onlarla deploy etmek için cloud sağlayıcınızın rehberlerini takip edin. 🤓

## Performans { #performance }

Bağımsız TechEmpower kıyaslamaları, Uvicorn altında çalışan **FastAPI** uygulamalarının <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">mevcut en hızlı Python framework'lerinden biri</a> olduğunu gösteriyor; sadece Starlette ve Uvicorn'un kendisinin gerisinde (FastAPI tarafından dahili olarak kullanılır). (*)

Daha iyi anlamak için <a href="https://fastapi.tiangolo.com/tr/benchmarks/" class="internal-link" target="_blank">Kıyaslamalar</a> bölümüne bakın.

## Bağımlılıklar { #dependencies }

FastAPI, Pydantic ve Starlette'a bağımlıdır.

### `standard` Bağımlılıkları { #standard-dependencies }

FastAPI'ı `pip install "fastapi[standard]"` ile yüklediğinizde, opsiyonel bağımlılıkların `standard` grubuyla birlikte gelir:

Pydantic tarafından kullanılanlar:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - email doğrulaması için.

Starlette tarafından kullanılanlar:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - `TestClient` kullanmak istiyorsanız gereklidir.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - varsayılan template yapılandırmasını kullanmak istiyorsanız gereklidir.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - `request.form()` ile, form <dfn title="HTTP request'ten gelen string'i Python verisine dönüştürme">"ayrıştırma"</dfn> desteği istiyorsanız gereklidir.

FastAPI tarafından kullanılanlar:

* <a href="https://www.uvicorn.dev" target="_blank"><code>uvicorn</code></a> - uygulamanızı yükleyen ve servis eden server için. Buna, yüksek performanslı servis için gereken bazı bağımlılıkları (örn. `uvloop`) içeren `uvicorn[standard]` dahildir.
* `fastapi-cli[standard]` - `fastapi` komutunu sağlamak için.
    * Buna, FastAPI uygulamanızı <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>'a deploy etmenizi sağlayan `fastapi-cloud-cli` dahildir.

### `standard` Bağımlılıkları Olmadan { #without-standard-dependencies }

`standard` opsiyonel bağımlılıklarını dahil etmek istemiyorsanız, `pip install fastapi` ile kurabilirsiniz.

### `fastapi-cloud-cli` Olmadan { #without-fastapi-cloud-cli }

FastAPI'ı standard bağımlılıklarla ama `fastapi-cloud-cli` olmadan kurmak istiyorsanız, `pip install "fastapi[standard-no-fastapi-cloud-cli]"` ile yükleyebilirsiniz.

### Ek Opsiyonel Bağımlılıklar { #additional-optional-dependencies }

Yüklemek isteyebileceğiniz bazı ek bağımlılıklar da vardır.

Ek opsiyonel Pydantic bağımlılıkları:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - ayar yönetimi için.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - Pydantic ile kullanılacak ek type'lar için.

Ek opsiyonel FastAPI bağımlılıkları:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - `ORJSONResponse` kullanmak istiyorsanız gereklidir.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - `UJSONResponse` kullanmak istiyorsanız gereklidir.

## Lisans { #license }

Bu proje MIT lisansı şartları altında lisanslanmıştır.
