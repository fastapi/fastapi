# Alternatifler, İlham Kaynakları ve Karşılaştırmalar { #alternatives-inspiration-and-comparisons }

**FastAPI**'a nelerin ilham verdiği, alternatiflerle nasıl karşılaştırıldığı ve onlardan neler öğrendiği.

## Giriş { #intro }

Başkalarının daha önceki çalışmaları olmasaydı, **FastAPI** var olmazdı.

Önceden oluşturulan birçok araç, ortaya çıkışına ilham verdi.

Yıllarca yeni bir framework oluşturmaktan kaçındım. Önce **FastAPI**’ın bugün kapsadığı özelliklerin tamamını, birçok farklı framework, eklenti ve araçla çözmeyi denedim.

Ancak bir noktada, geçmişteki araçlardan en iyi fikirleri alıp, mümkün olan en iyi şekilde birleştiren ve daha önce mevcut olmayan dil özelliklerini (Python 3.6+ tip belirteçleri) kullanarak tüm bu özellikleri sağlayan bir şey geliştirmekten başka seçenek kalmadı.

## Daha Önce Geliştirilen Araçlar { #previous-tools }

### <a href="https://www.djangoproject.com/" class="external-link" target="_blank">Django</a> { #django }

Python ekosistemindeki en popüler ve yaygın olarak güvenilen web framework’üdür. Instagram gibi sistemleri geliştirmede kullanılmıştır.

MySQL veya PostgreSQL gibi ilişkisel veritabanlarıyla nispeten sıkı bağlıdır, bu nedenle Couchbase, MongoDB, Cassandra vb. gibi bir NoSQL veritabanını ana depolama motoru olarak kullanmak pek kolay değildir.

Modern bir ön uç (React, Vue.js, Angular gibi) veya onunla haberleşen diğer sistemler (ör. <abbr title="Internet of Things - Nesnelerin İnterneti">IoT</abbr> cihazları) tarafından tüketilen API’lar üretmekten ziyade, arka uçta HTML üretmek için oluşturulmuştur.

### <a href="https://www.django-rest-framework.org/" class="external-link" target="_blank">Django REST Framework</a> { #django-rest-framework }

Django REST Framework, Django üzerine kurulu esnek bir araç takımı olarak, Web API’lar geliştirmeyi ve Django’nun API kabiliyetlerini artırmayı hedefler.

Mozilla, Red Hat ve Eventbrite gibi birçok şirket tarafından kullanılmaktadır.

**Otomatik API dökümantasyonu**nun ilk örneklerinden biriydi ve bu, “**FastAPI** arayışına” ilham veren ilk fikirlerden biriydi.

/// note | Not

Django REST Framework, **FastAPI**'ın üzerine inşa edildiği Starlette ve Uvicorn'un da yaratıcısı olan Tom Christie tarafından geliştirildi.

///

/// check | **FastAPI**'a ilham olan

Otomatik API dökümantasyonu sağlayan bir web arayüzü sunmak.

///

### <a href="https://flask.palletsprojects.com" class="external-link" target="_blank">Flask</a> { #flask }

Flask bir “mikroframework”tür, Django’da varsayılan gelen pek çok özelliği (veritabanı entegrasyonları vb.) içermez.

Bu basitlik ve esneklik, NoSQL veritabanlarını ana veri depolama sistemi olarak kullanmak gibi şeyleri mümkün kılar.

Çok basit olduğu için öğrenmesi nispeten sezgiseldir, ancak dökümantasyon bazı noktalarda biraz teknikleşebilir.

Ayrıca veritabanı, kullanıcı yönetimi veya Django’da önceden gelen pek çok özelliğe ihtiyaç duymayan uygulamalar için de yaygın olarak kullanılır. Yine de bu özelliklerin çoğu eklentilerle eklenebilir.

Bileşenlerin ayrık olması ve gerekeni tam olarak kapsayacak şekilde genişletilebilen bir “mikroframework” olması, özellikle korumak istediğim bir özelliktir.

Flask’ın sadeliği göz önüne alındığında, API geliştirmek için iyi bir aday gibi görünüyordu. Sırada, Flask için bir “Django REST Framework” bulmak vardı.

/// check | **FastAPI**'a ilham olan

Gereken araç ve parçaları kolayca eşleştirip birleştirmeyi sağlayan bir mikroframework olmak.

Basit ve kullanımı kolay bir yönlendirme (routing) sistemine sahip olmak.

///

### <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Requests</a> { #requests }

**FastAPI** aslında **Requests**’in bir alternatifi değildir. Kapsamları çok farklıdır.

Hatta bir FastAPI uygulamasının içinde Requests kullanmak yaygındır.

Yine de FastAPI, Requests’ten epey ilham almıştır.

**Requests** bir kütüphane olarak API’larla (istemci olarak) etkileşime geçmeye yararken, **FastAPI** API’lar (sunucu olarak) geliştirmeye yarar.

Yani daha çok zıt uçlardadırlar ama birbirlerini tamamlarlar.

Requests çok basit ve sezgisel bir tasarıma sahiptir, mantıklı varsayılanlarla kullanımı çok kolaydır. Aynı zamanda çok güçlü ve özelleştirilebilirdir.

Bu yüzden resmi web sitesinde de söylendiği gibi:

> Requests, tüm zamanların en çok indirilen Python paketlerinden biridir

Kullanımı çok basittir. Örneğin bir `GET` isteği yapmak için:

```Python
response = requests.get("http://example.com/some/url")
```

Buna karşılık bir FastAPI API *path operation*’ı şöyle olabilir:

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

`requests.get(...)` ile `@app.get(...)` arasındaki benzerliklere bakın.

/// check | **FastAPI**'a ilham olan

* Basit ve sezgisel bir API’ya sahip olmak.
* HTTP metot isimlerini (işlemlerini) doğrudan, anlaşılır ve sezgisel bir şekilde kullanmak.
* Mantıklı varsayılanlara sahip olmak ama güçlü özelleştirmeler de sunmak.

///

### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a> { #swagger-openapi }

Django REST Framework’ünden istediğim ana özellik otomatik API dökümantasyonuydu.

Sonra API’ları JSON (veya JSON’un bir uzantısı olan YAML) kullanarak dökümante etmek için Swagger adlı bir standart olduğunu gördüm.

Ve Swagger API’ları için zaten oluşturulmuş bir web arayüzü vardı. Yani bir API için Swagger dökümantasyonu üretebilmek, bu web arayüzünü otomatik kullanabilmek demekti.

Bir noktada Swagger, Linux Foundation’a devredildi ve OpenAPI olarak yeniden adlandırıldı.

Bu yüzden, 2.0 sürümü söz konusu olduğunda “Swagger”, 3+ sürümler için ise “OpenAPI” denmesi yaygındır.

/// check | **FastAPI**'a ilham olan

API spesifikasyonları için özel bir şema yerine açık bir standart benimsemek ve kullanmak.

Ve standartlara dayalı kullanıcı arayüzü araçlarını entegre etmek:

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>
* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>

Bu ikisi oldukça popüler ve istikrarlı oldukları için seçildi; hızlı bir aramayla OpenAPI için onlarca alternatif kullanıcı arayüzü bulabilirsiniz (**FastAPI** ile de kullanabilirsiniz).

///

### Flask REST framework’leri { #flask-rest-frameworks }

Birçok Flask REST framework’ü var; ancak zaman ayırıp inceledikten sonra çoğunun artık sürdürülmediğini veya bazı kritik sorunlar nedeniyle uygun olmadıklarını gördüm.

### <a href="https://marshmallow.readthedocs.io/en/stable/" class="external-link" target="_blank">Marshmallow</a> { #marshmallow }

API sistemlerinin ihtiyaç duyduğu temel özelliklerden biri, koddan (Python) veriyi alıp ağ üzerinden gönderilebilecek bir şeye dönüştürmek, yani veri “<dfn title="marshalling, conversion olarak da adlandırılır">dönüşüm</dfn>”üdür. Örneğin, bir veritabanından gelen verileri içeren bir objeyi JSON objesine dönüştürmek, `datetime` objelerini string’e çevirmek vb.

API’ların ihtiyaç duyduğu bir diğer önemli özellik, veri doğrulamadır; belirli parametreler göz önüne alındığında verinin geçerli olduğundan emin olmak. Örneğin, bir alanın `int` olması ve rastgele bir metin olmaması. Bu özellikle dışarıdan gelen veriler için kullanışlıdır.

Bir veri doğrulama sistemi olmadan, tüm bu kontrolleri kod içinde el ile yapmanız gerekir.

Marshmallow, bu özellikleri sağlamak için inşa edildi. Harika bir kütüphanedir ve geçmişte çok kullandım.

Ancak Python tip belirteçlerinden önce yazılmıştır. Dolayısıyla her <dfn title="verinin nasıl oluşturulması gerektiğinin tanımı">şemayı</dfn> tanımlamak için Marshmallow’un sağladığı belirli yardımcılar ve sınıflar kullanılır.

/// check | **FastAPI**'a ilham olan

Kodla, veri tiplerini ve doğrulamayı otomatik sağlayan “şemalar” tanımlamak.

///

### <a href="https://webargs.readthedocs.io/en/latest/" class="external-link" target="_blank">Webargs</a> { #webargs }

API’ların ihtiyaç duyduğu bir diğer büyük özellik, gelen isteklerden veriyi <dfn title="okuyup Python verisine dönüştürme">ayrıştırma</dfn>dır.

Webargs, Flask dahil birkaç framework’ün üzerinde bunu sağlamak için geliştirilmiş bir araçtır.

Veri doğrulama için arka planda Marshmallow’u kullanır. Aynı geliştiriciler tarafından yazılmıştır.

**FastAPI**’dan önce benim de çok kullandığım harika bir araçtır.

/// info | Bilgi

Webargs, Marshmallow geliştiricileri tarafından oluşturuldu.

///

/// check | **FastAPI**'a ilham olan

Gelen istek verisini otomatik doğrulamak.

///

### <a href="https://apispec.readthedocs.io/en/stable/" class="external-link" target="_blank">APISpec</a> { #apispec }

Marshmallow ve Webargs; doğrulama, ayrıştırma ve dönüşümü eklenti olarak sağlar.

Ama dökümantasyon eksikti. Sonra APISpec geliştirildi.

Birçok framework için bir eklentidir (Starlette için de bir eklenti vardır).

Çalışma şekli: Her bir route’u işleyen fonksiyonun docstring’i içine YAML formatında şema tanımı yazarsınız.

Ve OpenAPI şemaları üretir.

Flask, Starlette, Responder vb. için çalışma şekli böyledir.

Ancak yine, Python metni içinde (kocaman bir YAML) mikro bir söz dizimi sorunu ortaya çıkar.

Editör bu konuda pek yardımcı olamaz. Parametreleri veya Marshmallow şemalarını değiştirip docstring’teki YAML’ı güncellemeyi unutursak, üretilen şema geçerliliğini yitirir.

/// info | Bilgi

APISpec, Marshmallow geliştiricileri tarafından oluşturuldu.

///

/// check | **FastAPI**'a ilham olan

API’lar için açık standart olan OpenAPI’ı desteklemek.

///

### <a href="https://flask-apispec.readthedocs.io/en/latest/" class="external-link" target="_blank">Flask-apispec</a> { #flask-apispec }

Webargs, Marshmallow ve APISpec’i bir araya getiren bir Flask eklentisidir.

Webargs ve Marshmallow’dan aldığı bilgiyi kullanarak, APISpec ile otomatik OpenAPI şemaları üretir.

Harika ama yeterince değer görmeyen bir araçtır. Mevcut birçok Flask eklentisinden çok daha popüler olmalıydı. Muhtemelen dökümantasyonunun fazla kısa ve soyut olmasından kaynaklanıyor olabilir.

Python docstring’leri içine YAML (farklı bir söz dizimi) yazma ihtiyacını ortadan kaldırdı.

**FastAPI**’yı inşa edene kadar, Flask + Flask-apispec + Marshmallow + Webargs kombinasyonu benim favori arka uç stack’imdi.

Bunu kullanmak, birkaç Flask full‑stack üreticisinin ortaya çıkmasına yol açtı. Şu ana kadar benim (ve birkaç harici ekibin) kullandığı ana stack’ler:

* <a href="https://github.com/tiangolo/full-stack" class="external-link" target="_blank">https://github.com/tiangolo/full-stack</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchbase</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchdb" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchdb</a>

Aynı full‑stack üreticiler, [**FastAPI** Proje Üreticileri](project-generation.md){.internal-link target=_blank}’nin de temelini oluşturdu.

/// info | Bilgi

Flask-apispec, Marshmallow geliştiricileri tarafından oluşturuldu.

///

/// check | **FastAPI**'a ilham olan

Veri dönüşümü ve doğrulamayı tanımlayan aynı koddan, OpenAPI şemasını otomatik üretmek.

///

### <a href="https://nestjs.com/" class="external-link" target="_blank">NestJS</a> (ve <a href="https://angular.io/" class="external-link" target="_blank">Angular</a>) { #nestjs-and-angular }

Bu Python bile değil; NestJS, Angular’dan ilham alan bir JavaScript (TypeScript) NodeJS framework’üdür.

Flask-apispec ile yapılabilene kısmen benzer bir şey başarır.

Angular 2’den esinlenen, entegre bir bağımlılık enjeksiyonu sistemi vardır. “Injectable”ları önceden kaydetmeyi gerektirir (bildiğim diğer bağımlılık enjeksiyonu sistemlerinde olduğu gibi), bu da ayrıntıyı ve kod tekrarını artırır.

Parametreler TypeScript tipleriyle (Python tip belirteçlerine benzer) açıklandığından, editör desteği oldukça iyidir.

Ancak TypeScript tip bilgisi JavaScript’e derlemeden sonra korunmadığından, aynı anda tiplere dayanarak doğrulama, dönüşüm ve dökümantasyon tanımlanamaz. Bu ve bazı tasarım kararları nedeniyle doğrulama, dönüşüm ve otomatik şema üretimi için birçok yere dekoratör eklemek gerekir; proje oldukça ayrıntılı hâle gelir.

İçiçe modelleri çok iyi işleyemez. Yani istek gövdesindeki JSON, içinde başka alanları ve onlar da içiçe JSON objelerini içeriyorsa, doğru şekilde dökümante edilip doğrulanamaz.

/// check | **FastAPI**'a ilham olan

Harika editör desteği için Python tiplerini kullanmak.

Güçlü bir bağımlılık enjeksiyonu sistemine sahip olmak. Kod tekrarını en aza indirmenin bir yolunu bulmak.

///

### <a href="https://sanic.readthedocs.io/en/latest/" class="external-link" target="_blank">Sanic</a> { #sanic }

`asyncio` tabanlı, son derece hızlı ilk Python framework’lerinden biriydi. Flask’a oldukça benzer olacak şekilde geliştirilmişti.

/// note | Teknik Detaylar

Varsayılan Python `asyncio` döngüsü yerine <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a> kullanır; hızını esasen bu sağlar.

Açık kıyaslamalarda, bugün Uvicorn ve Starlette’in Sanic’ten daha hızlı olduğu görülür; Sanic bu ikisine ilham vermiştir.

///

/// check | **FastAPI**'a ilham olan

Çok yüksek performans elde etmenin bir yolunu bulmak.

Bu yüzden **FastAPI**, en hızlı framework olduğu için (üçüncü parti kıyaslamalara göre) Starlette üzerine kuruludur.

///

### <a href="https://falconframework.org/" class="external-link" target="_blank">Falcon</a> { #falcon }

Falcon, başka bir yüksek performanslı Python framework’üdür; minimal olacak şekilde tasarlanmış ve Hug gibi diğer framework’lere temel olmuştur.

İki parametre alan fonksiyonlar etrafında tasarlanmıştır: “request” ve “response”. İstekten parçalar “okur”, cevaba parçalar “yazarsınız”. Bu tasarım nedeniyle, fonksiyon parametreleriyle standart Python tip belirteçlerini kullanarak istek parametrelerini ve gövdelerini ilan etmek mümkün değildir.

Dolayısıyla veri doğrulama, dönüşüm ve dökümantasyon kodda yapılmalı; otomatik olmaz. Ya da Hug’da olduğu gibi Falcon’un üzerine bir framework olarak uygulanmalıdır. Falcon’un tasarımından etkilenen ve tek bir request objesi ile response objesini parametre olarak alan diğer framework’lerde de aynı ayrım vardır.

/// check | **FastAPI**'a ilham olan

Harika performans elde etmenin yollarını bulmak.

Hug ile birlikte (Hug, Falcon’a dayanır) **FastAPI**’da fonksiyonlarda opsiyonel bir `response` parametresi ilan edilmesi fikrine ilham vermek. FastAPI’da bu parametre çoğunlukla header, cookie ve alternatif durum kodlarını ayarlamak için kullanılır.

///

### <a href="https://moltenframework.com/" class="external-link" target="_blank">Molten</a> { #molten }

**FastAPI**’ı geliştirmenin ilk aşamalarında Molten’ı keşfettim. Oldukça benzer fikirleri vardı:

* Python tip belirteçlerine dayanır.
* Bu tiplere bağlı doğrulama ve dökümantasyon sağlar.
* Bağımlılık enjeksiyonu sistemi vardır.

Pydantic gibi doğrulama, dönüşüm ve dökümantasyon için üçüncü parti bir kütüphane kullanmaz; kendi içinde sağlar. Bu yüzden bu veri tipi tanımlarını tekrar kullanmak o kadar kolay olmaz.

Biraz daha ayrıntılı yapılandırma ister. Ve ASGI yerine WSGI tabanlı olduğundan, Uvicorn, Starlette ve Sanic gibi araçların yüksek performansından faydalanmaya yönelik tasarlanmamıştır.

Bağımlılık enjeksiyonu sistemi, bağımlılıkların önceden kaydedilmesini ve tiplerine göre çözülmesini gerektirir. Yani belirli bir tipi sağlayan birden fazla “bileşen” tanımlanamaz.

Route’lar, endpoint’i işleyen fonksiyonun üstüne konan dekoratörlerle değil, tek bir yerde, farklı yerlerde tanımlanmış fonksiyonlar kullanılarak ilan edilir. Bu yaklaşım, Flask (ve Starlette) yerine Django’ya daha yakındır; kodda aslında birbirine sıkı bağlı olan şeyleri ayırır.

/// check | **FastAPI**'a ilham olan

Model özelliklerinin “varsayılan” değerlerini kullanarak veri tiplerine ekstra doğrulamalar tanımlamak. Bu, editör desteğini iyileştirir ve Pydantic’te daha önce yoktu.

Bu yaklaşım, Pydantic’te de aynı doğrulama beyan stilinin desteklenmesine ilham verdi (bu işlevselliklerin tamamı artık Pydantic’te mevcut).

///

### <a href="https://github.com/hugapi/hug" class="external-link" target="_blank">Hug</a> { #hug }

Hug, Python tip belirteçlerini kullanarak API parametre tiplerini ilan etmeyi uygulayan ilk framework’lerden biriydi. Diğer araçlara da ilham veren harika bir fikirdi.

Standart Python tipleri yerine kendi özel tiplerini kullansa da büyük bir adımdı.

JSON ile tüm API’ı beyan eden özel bir şema üreten ilk framework’lerden biriydi.

OpenAPI veya JSON Schema gibi bir standarda dayanmadığı için Swagger UI gibi diğer araçlarla doğrudan entegre edilemezdi. Yine de oldukça yenilikçiydi.

Nadir bir özelliği daha vardı: aynı framework ile hem API’lar hem de CLI’lar oluşturmak mümkündü.

Senkron Python web framework’leri için önceki standart olan WSGI’ye dayandığından, WebSocket vb. şeyleri işleyemez, ancak yine de yüksek performansa sahiptir.

/// info | Bilgi

Hug, Python dosyalarındaki import’ları otomatik sıralayan harika bir araç olan <a href="https://github.com/timothycrosley/isort" class="external-link" target="_blank">`isort`</a>’un geliştiricisi Timothy Crosley tarafından geliştirildi.

///

/// check | **FastAPI**'a ilham olan fikirler

Hug, APIStar’ın bazı kısımlarına ilham verdi ve APIStar ile birlikte en umut verici bulduğum araçlardandı.

**FastAPI**, parametreleri ilan etmek ve API’ı otomatik tanımlayan bir şema üretmek için Python tip belirteçlerini kullanma fikrini Hug’dan ilhamla benimsedi.

Ayrıca header ve cookie ayarlamak için fonksiyonlarda `response` parametresi ilan etme fikrine de Hug ilham verdi.

///

### <a href="https://github.com/encode/apistar" class="external-link" target="_blank">APIStar</a> (<= 0.5) { #apistar-0-5 }

**FastAPI**’yi inşa etmeye karar vermeden hemen önce **APIStar** sunucusunu buldum. Aradığım şeylerin neredeyse hepsine sahipti ve harika bir tasarımı vardı.

Python tip belirteçleriyle parametreleri ve istekleri ilan eden bir framework’ün gördüğüm ilk örneklerindendi (NestJS ve Molten’dan önce). Aşağı yukarı Hug ile aynı zamanlarda buldum; ancak APIStar, OpenAPI standardını kullanıyordu.

Farklı yerlerdeki aynı tip belirteçlerine dayanarak otomatik veri doğrulama, veri dönüşümü ve OpenAPI şeması üretimi vardı.

Gövde şema tanımları Pydantic’tekiyle aynı Python tip belirteçlerini kullanmıyordu; biraz daha Marshmallow’a benziyordu. Bu yüzden editör desteği o kadar iyi olmazdı; yine de APIStar mevcut en iyi seçenekti.

O dönem kıyaslamalarda en iyi performansa sahipti (sadece Starlette tarafından geçiliyordu).

Başta otomatik API dökümantasyonu sunan bir web arayüzü yoktu ama Swagger UI ekleyebileceğimi biliyordum.

Bağımlılık enjeksiyonu sistemi vardı. Diğer araçlarda olduğu gibi bileşenlerin önceden kaydedilmesini gerektiriyordu. Yine de harika bir özellikti.

Güvenlik entegrasyonu olmadığından tam bir projede kullanamadım; bu yüzden Flask-apispec tabanlı full‑stack üreticilerle sahip olduğum özelliklerin tamamını ikame edemedim. Bu işlevi ekleyen bir pull request’i yapılacaklar listeme almıştım.

Sonra projenin odağı değişti.

Artık bir API web framework’ü değildi; geliştirici Starlette’e odaklanmak zorundaydı.

Şimdi APIStar, bir web framework’ü değil, OpenAPI spesifikasyonlarını doğrulamak için araçlar takımından ibaret.

/// info | Bilgi

APIStar, aşağıdakilerin de yaratıcısı olan Tom Christie tarafından geliştirildi:

* Django REST Framework
* **FastAPI**’ın üzerine kurulu Starlette
* Starlette ve **FastAPI** tarafından kullanılan Uvicorn

///

/// check | **FastAPI**'a ilham olan

Var olmak.

Aynı Python tipleriyle (hem veri doğrulama, dönüşüm ve dökümantasyon) birden çok şeyi ilan etmek ve aynı anda harika editör desteği sağlamak, bence dahiyane bir fikirdi.

Uzun süre benzer bir framework arayıp birçok alternatifi denedikten sonra, APIStar mevcut en iyi seçenekti.

Sonra APIStar bir sunucu olarak var olmaktan çıktı ve Starlette oluşturuldu; böyle bir sistem için daha iyi bir temel oldu. Bu, **FastAPI**’yi inşa etmek için son ilhamdı.

Önceki bu araçlardan edinilen deneyimler üzerine özellikleri, tip sistemi ve diğer kısımları geliştirip artırırken, **FastAPI**’yi APIStar’ın “ruhani varisi” olarak görüyorum.

///

## **FastAPI** Tarafından Kullanılanlar { #used-by-fastapi }

### <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> { #pydantic }

Pydantic, Python tip belirteçlerine dayalı olarak veri doğrulama, dönüşüm ve dökümantasyon (JSON Schema kullanarak) tanımlamak için bir kütüphanedir.

Bu onu aşırı sezgisel kılar.

Marshmallow ile karşılaştırılabilir. Kıyaslamalarda Marshmallow’dan daha hızlıdır. Aynı Python tip belirteçlerine dayandığı için editör desteği harikadır.

/// check | **FastAPI** bunu şurada kullanır

Tüm veri doğrulama, veri dönüşümü ve JSON Schema tabanlı otomatik model dökümantasyonunu halletmekte.

**FastAPI** daha sonra bu JSON Schema verisini alır ve (yaptığı diğer şeylerin yanı sıra) OpenAPI içine yerleştirir.

///

### <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> { #starlette }

Starlette, yüksek performanslı asyncio servisleri oluşturmak için ideal, hafif bir <dfn title="Asenkron Python web uygulamaları geliştirmek için yeni standart">ASGI</dfn> framework’ü/araç takımıdır.

Çok basit ve sezgiseldir. Kolayca genişletilebilir ve modüler bileşenlere sahip olacak şekilde tasarlanmıştır.

Şunlara sahiptir:

* Cidden etkileyici performans.
* WebSocket desteği.
* Süreç içi arka plan görevleri.
* Başlatma ve kapatma olayları.
* HTTPX üzerinde geliştirilmiş test istemcisi.
* CORS, GZip, Statik Dosyalar, Streaming cevaplar.
* Oturum (Session) ve Cookie desteği.
* %100 test kapsamı.
* %100 tip anotasyonlu kod tabanı.
* Az sayıda zorunlu bağımlılık.

Starlette, şu anda test edilen en hızlı Python framework’üdür. Yalnızca bir framework değil, bir sunucu olan Uvicorn tarafından geçilir.

Starlette, temel web mikroframework işlevselliğinin tamamını sağlar.

Ancak otomatik veri doğrulama, dönüşüm veya dökümantasyon sağlamaz.

**FastAPI**’nin bunun üzerine eklediği ana şeylerden biri, Pydantic kullanarak, bütünüyle Python tip belirteçlerine dayalı bu özelliklerdir. Buna ek olarak bağımlılık enjeksiyonu sistemi, güvenlik yardımcıları, OpenAPI şema üretimi vb. gelir.

/// note | Teknik Detaylar

ASGI, Django çekirdek ekip üyeleri tarafından geliştirilen yeni bir “standart”tır. Hâlâ resmi bir “Python standardı” (PEP) değildir, ancak bu süreç üzerindedirler.

Buna rağmen, şimdiden birçok araç tarafından bir “standart” olarak kullanılmaktadır. Bu, birlikte çalışabilirliği büyük ölçüde artırır; örneğin Uvicorn’u başka bir ASGI sunucusuyla (Daphne veya Hypercorn gibi) değiştirebilir ya da `python-socketio` gibi ASGI uyumlu araçlar ekleyebilirsiniz.

///

/// check | **FastAPI** bunu şurada kullanır

Tüm temel web kısımlarını ele almak; üzerine özellikler eklemek.

`FastAPI` sınıfı, doğrudan `Starlette` sınıfından miras alır.

Dolayısıyla Starlette ile yapabildiğiniz her şeyi, adeta “turbo şarjlı Starlette” olan **FastAPI** ile de doğrudan yapabilirsiniz.

///

### <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a> { #uvicorn }

Uvicorn, uvloop ve httptools üzerinde inşa edilmiş, ışık hızında bir ASGI sunucusudur.

Bir web framework’ü değil, bir sunucudur. Örneğin path’lere göre yönlendirme araçları sağlamaz; bunu Starlette (veya **FastAPI**) gibi bir framework üstte sağlar.

Starlette ve **FastAPI** için önerilen sunucudur.

/// check | **FastAPI** bunu şöyle önerir

**FastAPI** uygulamalarını çalıştırmak için ana web sunucusu.

Komut satırında `--workers` seçeneğini kullanarak asenkron çok süreçli (multi‑process) bir sunucu da elde edebilirsiniz.

Daha fazla detay için [Dağıtım](deployment/index.md){.internal-link target=_blank} bölümüne bakın.

///

## Kıyaslamalar ve Hız { #benchmarks-and-speed }

Uvicorn, Starlette ve FastAPI arasındaki farkı anlamak ve karşılaştırmak için [Kıyaslamalar](benchmarks.md){.internal-link target=_blank} bölümüne göz atın.
