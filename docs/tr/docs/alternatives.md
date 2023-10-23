# Alternatifler, İlham Kaynakları ve Karşılaştırmalar

**FastAPI**'ye neler ilham verdi? Diğer alternatiflerle karşılaştırıldığında farkları neler? **FastAPI** diğer alternatiflerinden neler öğrendi?

## Giriş

Eğer geçmişte diğerlerinin yaptığı çalışmalar olmasaydı **FastAPI**'da var olamazdı.

Geçmişte oluşturulan pek çok araç **FastAPI**'a ilham kaynağı olmuştur.

Yıllardır yeni bir framework oluşturmaktan kaçınıyordum. Başlangıçta **FastAPI**'ın çözdüğü sorunları çözebilmek için pek çok farklı framework, <abbr title="Eklenti: Plug-In">eklenti</abbr> ve araç kullanmayı denedim.

Ancak bir noktada, geçmişteki diğer araçlardan en iyi fikirleri alarak bütün bu çözümleri kapsayan, ayrıca bütün bunları Python'ın daha önce mevcut olmayan özelliklerini (Python 3.6+ ile gelen <abbr title="Tip belirteçleri: Type Hints">tip belirteçleri</abbr>) kullanarak yapan bir şey üretmekten başka seçenek kalmamıştı.

## Daha Önce Geliştirilen Araçlar

### <a href="https://www.djangoproject.com/" class="external-link" target="_blank">Django</a>

Django geniş çapta güvenilen, Python ekosistemindeki en popüler web framework'üdür. Instagram gibi sistemleri geliştirmede kullanılmıştır.

MySQL ve PostgreSQL gibi ilişkisel veritabanlarıyla nispeten sıkı bir şekilde bağlantılıdır. Bu nedenle Couchbase, MongoDB ve Cassandra gibi NoSQL veritabanlarını ana veritabanı motoru olarak kullanmak pek de kolay değil.

Modern ön uçlarda (React, Vue.js ve Angular gibi) veya diğer sistemler (örneğin <abbr title="Nesnelerin interneti: IoT (Internet of Things)">nesnelerin interneti</abbr> cihazları) tarafından kullanılan API'ler yerine arka uçta HTML üretmek için oluşturuldu.

### <a href="https://www.django-rest-framework.org/" class="external-link" target="_blank">Django REST Framework</a>

Django REST framework'ü, Django'nun API kabiliyetlerini arttırmak için arka planda Django kullanan esnek bir araç grubu olarak oluşturuldu. Üstelik Mozilla, Red Hat ve Eventbrite gibi pek çok şirket tarafından kullanılıyor.

**Otomatik API dökümantasyonu**nun ilk örneklerinden biri olduğu için, **FastAPI** arayışına ilham veren ilk fikirlerden biri oldu.

!!! note "Not"
    Django REST Framework'ü, aynı zamanda **FastAPI**'ın dayandığı Starlette ve Uvicorn'un da yaratıcısı olan Tom Christie tarafından geliştirildi.

!!! check "**FastAPI**'a nasıl ilham verdi?"
    Kullanıcılar için otomatik API dökümantasyonu sunan bir web arayüzüne sahip olmalı.

### <a href="https://flask.palletsprojects.com" class="external-link" target="_blank">Flask</a>

Flask bir <abbr title="Mikro Framework: Micro Framework">mikro framework</abbr> olduğundan Django gibi framework'lerin aksine veritabanı integrasyonu gibi Django ile gelen pek çok özelliği direkt sağlamaz.

Bu basitlik ve esneklik NoSQL veritabanlarını ana veritabanı sistemi olarak kullanmak gibi şeyler yapmaya olanak sağlar.

Yapısı oldukça basit olduğundan öğrenmesi de nispeten basittir, tabii dökümantasyon bazı noktalarda biraz teknik hale geliyor.

Ayrıca Django ile birlikte gelen veritabanı, kullanıcı yönetimi ve diğer pek çok özelliğe ihtiyaç duymayan uygulamalarda da yaygın olarak kullanılıyor. Ancak bu tür özelliklerin pek çoğu <abbr title="Eklentiler: Plug-Ins">eklentiler</abbr> ile eklenebiliyor.

Uygulama parçalarının böyle ayrılıyor oluşu ve istenilen özelliklerle genişletilebilecek bir <abbr title="Mikro Framework: Micro Framework">mikro framework</abbr> olmak tam da benim istediğim bir özellikti.

Flask'ın basitliği göz önünde bulundurulduğu zaman, API geliştirmek için iyi bir eşleşme gibi görünüyordu. Bulunacak bir sonraki şey ise Flask için bir "Django REST Framework"!

!!! check "**FastAPI**'a nasıl ilham verdi?"
    Gereken araçları ve parçaları birleştirip eşleştirmeyi kolaylaştıracak bir mikro framework olmalı.

    Basit ve kullanması kolay bir <abbr title="Yönlendirme: Routing">routing sistemine</abbr> sahip olmalı.

### <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Requests</a>

**FastAPI** aslında **Requests**'in bir alternatifi değil. İkisininde kapsamı oldukça farklı.

Aslında Requests'i bir FastAPI uygulamasının *içinde* kullanmak daha olağan olurdu.

Ama yine de, FastAPI, Requests'ten oldukça ilham aldı.

**Requests**, <abbr title="API (Application Programming Interface): Uygulama Programlama Arayüzü">API'lar</abbr> ile bir istemci olarak *etkileşime geçmeyi* sağlayan bir kütüphaneyken **FastAPI** bir sunucu olarak <abbr title="API (Application Programming Interface): Uygulama Programlama Arayüzü">API'lar</abbr> oluşturmaya yarar.

Birbirlerini, zıt uçlarda olmalarına rağmen az çok tamamlıyorlar.

Requests oldukça basit ve sezgisel bir tasarıma sahip, kullanması da mantıklı varsayılan değerlerle oldukça kolay. Ama aynı zamanda çok güçlü ve gayet özelleştirilebilir.

Bu yüzden resmi web sitede de söylendiği gibi:

> Requests, tüm zamanların en çok indirilen Python  <abbr title="Paket: Package">paketlerinden</abbr> biridir.

Kullanım şekli bayağı basit. Örneğin bir `GET` isteği yapmak için aşağıdaki yeterli:

```Python
response = requests.get("http://example.com/some/url")
```

Bunun FastAPI'deki API <abbr title="Yol İşlemi: Path Operation">*yol işlemi*</abbr> şöyle görünür:

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World!"}
```

`requests.get(...)` ile `@app.get(...)` arasındaki benzerliklere bakın.

!!! check "**FastAPI**'a nasıl ilham verdi?"
    * Basit ve sezgisel bir API'ya sahip olmalı.
    * HTTP metot isimlerini (işlemlerini) anlaşılır olacak bir şekilde, direkt kullanmalı.
    * Mantıklı varsayılan değerlere ve buna rağmen güçlü bir özelleştirme desteğine sahip olmalı.

### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a>

Benim Django REST Framework'ünden istediğim ana özellik otomatik API dökümantasyonuydu.

Daha sonra API'ları dökümanlamak için Swagger adında JSON (veya JSON'un bir uzantısı olan YAML'ı) kullanan bir standart olduğunu buldum.

Üstelik Swagger API'ları için zaten halihazırda oluşturulmuş bir web arayüzü vardı. Yani, bir API için Swagger dökümantasyonu oluşturmak bu arayüzü otomatik olarak kullanabilmek demekti.

Swagger bir noktada Linux Foundation'a verildi ve adı OpenAPI olarak değiştirildi.

İşte bu yüzden versiyon 2.0 hakkında konuşurken "Swagger", versiyon 3 ve üzeri için ise "OpenAPI" adını kullanmak daha yaygın.

!!! check "**FastAPI**'a nasıl ilham verdi?"
    API spesifikasyonları için özel bir şema yerine bir <abbr title="Open Standard: Açık Standart, Açık kaynak olarak yayınlanan standart">açık standart</abbr> benimseyip kullanmalı.

    Ayrıca standarda bağlı kullanıcı arayüzü araçlarını entegre etmeli:

    * <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>
    * <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>

    Yukarıdaki ikisi oldukça popüler ve istikrarlı olduğu için seçildi, ancak hızlı bir araştırma yaparak **FastAPI** ile kullanabileceğiniz pek çok OpenAPI alternatifi arayüz bulabilirsiniz.

    Örneğin <a href="https://www.buildwithfern.com/?utm_source=tiangolo&utm_medium=website&utm_campaign=docs-alternatives" class="external-link" target="_blank">Fern</a>'i deneyebilirisiniz, kendisi aynı zamanda bir FastAPI sponsoru. 😎🎉

### Flask REST framework'leri

Pek çok Flask REST framework'ü var, fakat bunları biraz araştırdıktan sonra pek çoğunun artık geliştirilmediğini ve göze batan bazı sorunlarının olduğunu gördüm.

### <a href="https://marshmallow.readthedocs.io/en/stable/" class="external-link" target="_blank">Marshmallow</a>

API sistemlerine gereken ana özelliklerden biri de koddan veriyi alıp ağ üzerinde gönderilebilecek bir şeye çevirmek, yani veri <abbr title="Dönüşüm: serialization, parsing, marshalling olarak da biliniyor">dönüşümü</abbr>. Bu işleme veritabanındaki veriyi içeren bir objeyi JSON objesine çevirmek, `datetime` objelerini metinlere çevirmek gibi örnekler verilebilir.

API'lara gereken bir diğer büyük özellik ise veri doğrulamadır, yani verinin çeşitli parametrelere bağlı olarak doğru ve tutarlı olduğundan emin olmaktır. Örneğin bir alanın `int` olmasına karar verdiniz, daha sonra değerini rastgele bir metin olarak bulmak istemezsiniz. Bu özellikle sisteme dışarıdan gelen veri için kullanışlı bir özellik oluyor.

Bir veri doğrulama sistemi yokken bütün bu kontrolleri koda dökerek kendiniz yapmak zorunda kalırdınız.

Marshmallow bu özellikleri sağlamak için geliştirilmişti. Benim de geçmişte oldukça sık kullandığım harika bir kütüphanedir.

Ama... Python'un tip belirteçleri gelmeden önce oluşturulmuştu. Yani her <abbr title="Verilerin nasıl oluşturulması gerektiğinin tanımı">şemayı</abbr> tanımlamak için Marshmallow'un sunduğu spesifik araçları ve sınıfları kullanmanız gerekiyordu.

!!! check "**FastAPI**'a nasıl ilham verdi?"
    Kod kullanarak otomatik olarak veri tipini ve veri doğrulamayı belirten "şemalar" tanımlamalı.

### <a href="https://webargs.readthedocs.io/en/latest/" class="external-link" target="_blank">Webargs</a>

API'ların ihtiyacı olan bir diğer önemli özellik ise gelen isteklerdeki verileri Python objelerine ayrıştırabilmektir (<abbr title="Parsing: dönüştürmek, ayrıştırmak, çözümlemek">parsing</abbr>, <abbr title="Data parsing: Dışarıdan gelen veriyi programlama dilindeki bir objeye çevirmek">data parsing</abbr>)

Webargs, Flask gibi bir kaç framework'ün üzerinde bunu sağlamak için geliştirilen bir araçtır.

Veri doğrulamak için arka planda Marshmallow kullanıyor, hatta aynı geliştiriciler tarafından oluşturuldu.

Webargs da harika bir araç ve onu da geçmişte henüz **FastAPI** yokken çok kullandım.

!!! info "Bilgi"
    Webargs aynı Marshmallow geliştirileri tarafından oluşturuldu.

!!! check "**FastAPI**'a nasıl ilham verdi?"
    Gelen istek verisi için otomatik veri doğrulamaya sahip olmalı.

### <a href="https://apispec.readthedocs.io/en/stable/" class="external-link" target="_blank">APISpec</a>

Marshmallow ve Webargs <abbr title="Eklenti: Plug-In">eklentiler</abbr> olarak; veri doğrulama, ayrıştırma ve dönüştürmeyi sağlıyor. Ancak dökümantasyondan hala ses seda yok. Daha sonrasında APISpec oluşturuldu.

APISpec pek çok framework için bir <abbr title="Eklenti: Plug-In">eklenti</abbr> olarak kullanılıyor (Starlette için de bir <abbr title="Eklenti: Plug-In">eklentisi</abbr> var).

Şemanın tanımını <abbr title="Route: HTTP isteğinin gittiği yol">route</abbr>'u işleyen her bir fonksiyonun <abbr title="Döküman dizesi: docstring">döküman dizesinin</abbr> içine YAML formatında olacak şekilde yazıyorsunuz, o da OpenAPI şemaları üretiyor.

Flask, Starlette, Responder ve benzerlerinde bu şekilde çalışıyor.

Fakat sonrasında yine mikro syntax problemiyle karşılaşıyoruz. Python metinlerinin içinde koskoca bir YAML oluyor.

Editör bu konuda pek yardımcı olamaz. Üstelik eğer parametreleri ya da Marshmallow şemalarını değiştirip YAML güncellemeyi unutursak artık döküman geçerliliğini yitiriyor.

!!! info "Bilgi"
    APISpec de aynı Marshmallow geliştiricileri tarafından oluşturuldu

!!! check "**FastAPI**'a nasıl ilham verdi?"
    API'lar için açık standart desteği olmalı (OpenAPI gibi).

### <a href="https://flask-apispec.readthedocs.io/en/latest/" class="external-link" target="_blank">Flask-apispec</a>

Flask-apispec ise Webargs, Marshmallow ve APISpec'i birbirine bağlayan bir Flask <abbr title="Eklenti: Plug-In">eklentisi</abbr>.

Webargs ve Marshmallow'daki bilgiyi APISpec ile otomatik OpenAPI şemaları üretmek için kullanıyor.

Hak ettiği değeri görmeyen, harika bir araç. Piyasadaki çoğu Flask <abbr title="Eklenti: Plug-In">eklentisinden</abbr> çok daha popüler olmalı. Hak ettiği değeri görmüyor oluşunun sebebi ise dökümantasyonun çok kısa ve soyut olması olabilir.

Böylece Flask-apispec, Python döküman dizilerine YAML gibi farklı bir syntax yazma sorununu çözmüş oldu.

**FastAPI**'ı geliştirene dek benim favori arka uç kombinasyonum Flask'in yanında Marshmallow ve Webargs ile birlikte Flask-apispec idi.

Bunu kullanmak, bir kaç <abbr title="full-stack: Hem ön uç hem de arka uç geliştirme">full-stack</abbr> Flask projesi oluşturucusunun yaratılmasına yol açtı. Bunlar benim (ve bir kaç harici ekibin de) şimdiye kadar kullandığı asıl <abbr title="stack: Projeyi geliştirirken kullanılan araçlar dizisi">stack</abbr>:

* <a href="https://github.com/tiangolo/full-stack" class="external-link" target="_blank">https://github.com/tiangolo/full-stack</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchbase</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchdb" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchdb</a>

Aynı full-stack üreticiler [**FastAPI** Proje Üreticileri](project-generation.md){.internal-link target=_blank}'nin de temelini oluşturdu.

!!! info "Bilgi"
    Flask-apispec de aynı Marshmallow geliştiricileri tarafından üretildi

!!! check "**FastAPI**'a nasıl ilham oldu?"
    Veri dönüşümü ve veri doğrulamayı tanımlayan kodu kullanarak otomatik olarak OpenAPI şeması oluşturmalı.

### <a href="https://nestjs.com/" class="external-link" target="_blank">NestJS</a> (and <a href="https://angular.io/" class="external-link" target="_blank">Angular</a>)

Bu Python bile değil. NestJS, Angulardan ilham almış olan bir JavaScript (TypeScript) NodeJS framework'ü.

Flask-apispec ile yapılabileceklere nispeten benzeyen bir şey elde ediyor.

Angular 2'den ilham alan, içine gömülü bir <abbr title="Bağımlılık enjeksiyonu: Dependency Injection">bağımlılık enjeksiyonu</abbr> sistemi var. "<abbr title="Injectable: dependency injection sistemi tarafından enjekte edilecek dependency (bağımlılık)">injectable</abbr>"ları önceden kaydetmenizi gerektiriyor, aynı benim bildiğim diğer her bağımlılık enjeksiyonu sisteminde olduğu gibi. Böylece projeyi daha detaylı hale getiriyor ve kod tekrarını da arttırıyor.

Parametreler TypeScript tipleri (Python tip belirteçlerine benzer) ile açıklandığından editör desteği oldukça iyi.

Ama TypeScript verileri kod JavaScript'e derlendikten sonra korunmadığından, bunlara dayanarak aynı anda veri doğrulaması, veri dönüşümü ve dökümantasyon tanımlanamıyor. Bundan ve bazı tasarım tercihlerinden dolayı veri doğrulaması, dönüşümü ve otomatik şema üretimi için pek çok yere dekorator eklemek gerekiyor. Bu da projeyi oldukça detaylandırıyor.

İç içe geçen derin modelleri pek iyi işleyemiyor. Yani eğer istekteki JSON gövdesi derin bir JSON objesiyse düzgün bir şekilde dökümante edilip doğrulanamıyor.

!!! check "**FastAPI**'a nasıl ilham oldu?"
    Güzel bir editör desteği için Python tiplerini kullanmalı.

    Güçlü bir bağımlılık enjeksiyon sistemine sahip olmalı. Kod tekrarını minimuma indirecek bir yol bulmalı.

### <a href="https://sanic.readthedocs.io/en/latest/" class="external-link" target="_blank">Sanic</a>

Sanic, `asyncio`'ya dayanan son derece hızlı Python kütüphanelerinden biriydi. Flask'a epey benzeyecek şekilde geliştirilmişti.


!!! note "Teknik detaylar"
    <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a> içerisinde standart Python `asyncio` döngüsü yerine kullanıldı. `uvloop`'u çok hızlı yapan şey buydu.

    Uvicorn ve Starlette'ye ilham kaynağı olduğu oldukça açık, şu anda ikisi de açık karşılaştırmalarda Sanicten daha hızlı gözüküyor.

!!! check "**FastAPI**'a nasıl ilham oldu?"

    Uçuk performans sağlayacak bir yol bulmalı.

    Tam da bu yüzden **FastAPI** Starlette'e dayanıyor, çünkü Starlette şu anda kullanılabir en hızlı framework. (üçüncü parti karşılaştırmalı değerlendirmelerce test edildi)

### <a href="https://falconframework.org/" class="external-link" target="_blank">Falcon</a>

Falcon ise bir diğer yüksek performanslı Python framework'ü. Minimal olacak şekilde Hug gibi diğer framework'lerin temeli olabilmek için dizayn edildi.

İki parametre kabul eden fonksiyonler şeklide tasarlandı, biri "istek" ve diğeri ise "cevap". Sonra isteğin çeşitli kısımlarını **okuyup** cevaba **yazıyorsunuz**. Bu dizayndan dolayı istek parametrelerini ve gövdelerini standart Python tip belirteçlerini kullanarak fonksiyon parametreleriyle belirtmek mümkün değil.

Yani veri doğrulama, veri dönüştürme ve dökümantasyonun hepsi kodda yer almalı, otomatik halledemiyoruz. Ya da Falcon üzerine bir framework olarak uygulanmaları gerekiyor, aynı Hug'da olduğu gibi. Bu ayrım Falcon'un dizaynından esinlenen, istek ve cevap objelerini parametre olarak işleyen diğer kütüphanelerde de yer alıyor.

!!! check "**FastAPI**'a nasıl ilham oldu?"

    Harika bir performans'a sahip olmanın yollarını bulmalı.
    Hug ile birlikte (Hug zaten Falcon'a dayandığından) **FastAPI**'ın fonksiyonlarda `cevap` parametresi belirtmesinde ilham kaynağı oldu.

    FastAPI'da opsiyonel olmasına rağmen, daha çok header'lar, çerezler ve alternatif durum kodları belirlemede kullanılıyor.

### <a href="https://moltenframework.com/" class="external-link" target="_blank">Molten</a>

**FastAPI**'ı geliştirmenin ilk aşamalarında Molten'ı keşfettim. Pek çok ortak fikrimiz vardı:

* Python'daki tip belirteçlerini baz alıyordu.
* Bunlara bağlı olarak veri doğrulaması ve dökümantasyon sağlıyordu.
* Bir <abbr title="Bağımlılık enjeksiyonu: Dependency Injection">bağımlılık enjeksiyonu</abbr> sistemi vardı.

Veri doğrulama, veri dönüştürme ve dökümantasyon için Pydantic gibi bir üçüncü parti kütüphane kullanmıyor, kendi içerisinde bunlara sahip. Yani bu veri tipi tanımlarını tekrar kullanmak pek de kolay değil.

Biraz daha detaylı ayarlamalara gerek duyuyor. Ayrıca <abbr title="ASGI (Asynchronous Server Gateway Interface): Asenkron Sunucu Ağ Geçidi Arabirimi, asenkron Python web uygulamaları geliştirmek için yeni standart.">ASGI</abbr>  yerine <abbr title="WSGI (Web Server Gateway Interface): Web Sunucusu Ağ Geçidi Arabirimi, Pythonda senkron web uygulamaları geliştirmek için eski standart.">WSGI</abbr>'a dayanıyor. Yani Uvicorn, Starlette ve Sanic gibi araçların yüksek performansından faydalanacak şekilde dizayn edilmemiş.

<abbr title="Bağımlılık enjeksiyonu: Dependency Injection">Bağımlılık enjeksiyonu</abbr> sistemi bağımlılıkların önceden kaydedilmesini ve sonrasında belirlenen veri tiplerine göre çözülmesini gerektiriyor. Yani spesifik bir tip, birden fazla bileşen ile belirlenemiyor.

<abbr title="Route: HTTP isteğinin gittiği yol">Route</abbr>'lar fonksiyonun üstünde endpoint'i işleyen dekoratörler yerine farklı yerlerde tanımlanan fonksiyonlarla belirlenir. Bu Flask (ve Starlette) yerine daha çok Django'nun yaklaşımına daha yakın bir metot. Bu, kodda nispeten birbiriyle sıkı ilişkili olan şeyleri ayırmaya olanak sağlıyor.

!!! check "**FastAPI**'a nasıl ilham oldu?"
    Model özelliklerinin "standart" değerlerini kullanarak veri tipleri için ekstra veri doğrulama koşulları tanımlamalı. Bu editör desteğini geliştiriyor ve daha önceden Pydantic'te yoktu.

### <a href="https://www.hug.rest/" class="external-link" target="_blank">Hug</a>

Hug, Python tip belirteçlerini kullanarak API parametrelerinin tipini belirlemeyi uygulayan ilk framework'lerdendi. Bu, diğer araçlara da ilham kaynağı olan harika bir fikirdi.

Tip belirlerken standart Python veri tipleri yerine kendi özel tiplerini kullandı, yine de bu ileriye dönük devasa bir adımdı.

Hug ayrıca tüm API'ı JSON ile ifade eden özel bir şema oluşturan ilk framework'lerdendir.

OpenAPI veya JSON Şeması gibi bir standarda bağlı değildi. Yani Swagger UI gibi diğer araçlarla entegre etmek kolay olmazdı. Ama yine de, bu oldukça yenilikçi bir fikirdi.

Ayrıca ilginç ve çok rastlanmayan bir özelliği vardı: aynı framework'ü kullanarak hem API'lar hem de <abbr title="Command Line Tool (CLI): Komut satırı aracı">CLI</abbr>'lar oluşturmak mümkündü.

Senkron çalışan Python web framework'lerinin standardına (WSGI) dayandığından dolayı Websocket'leri ve diğer şeyleri işleyemiyor, ancak yine de yüksek performansa sahip.

!!! info "Bilgi"
    Hug, Python dosyalarını otomatik olarak sıralayan harika bir araç olan  <a href="https://github.com/timothycrosley/isort" class="external-link" target="_blank">`isort`</a>'un geliştiricisi Timothy Crosley tarafından üretildi.

!!! check "**FastAPI**'a nasıl ilham oldu?"
    Hug, APIStar'ın çeşitli kısımlarında esin kaynağı oldu ve APIStar'la birlikte en umut verici bulduğum araçlardan biriydi.

    **FastAPI**, Python tip belirteçlerini kullanarak parametre belirlemede ve API'ı otomatık tanımlayan bir şema üretmede de Hug'a esinlendi.

    **FastAPI**'ın header ve çerez tanımlamak için fonksiyonlarda `response` parametresini belirtmesinde de Hug'dan ilham alındı.

### <a href="https://github.com/encode/apistar" class="external-link" target="_blank">APIStar</a> (<= 0.5)

**FastAPI**'ı geliştirmeye başlamadan önce **APIStar** sunucusunu buldum. Benim aradığım şeylerin neredeyse hepsine sahipti ve harika bir tasarımı vardı.

Benim şimdiye kadar gördüğüm Python tip belirteçlerini kullanarak parametre ve istekler belirlemeyi uygulayan ilk framework'lerdendi (Molten ve NestJS'den önce). APIStar'ı da aşağı yukarı Hug ile aynı zamanlarda buldum. Fakat APIStar OpenAPI standardını kullanıyordu.

Otomatik veri doğrulama, veri dönüştürme ve farklı yerlerdeki tip belirteçlerine bağlı olarak OpenAPI şeması oluşturma desteği sunuyordu.

Gövde şema tanımları Pydantic ile aynı Python tip belirteçlerini kullanmıyordu, biraz daha Marsmallow'a benziyordu. Dolayısıyla editör desteği de o kadar iyi olmazdı ama APIStar eldeki en iyi seçenekti.

O dönemlerde karşılaştırmalarda en iyi performansa sahipti (yalnızca Starlette'ye kaybediyordu).

Başlangıçta otomatik API dökümantasyonu sunan bir web arayüzü yoktu, ama ben ona Swagger UI ekleyebileceğimi biliyordum.

Bağımlılık enjeksiyon sistemi vardı. Yukarıda bahsettiğim diğer araçlar gibi bundaki sistem de bileşenlerin önceden kaydedilmesini gerektiriyordu. Yine de harika bir özellikti.

Güvenlik entegrasyonu olmadığından dolayı APIStar'ı hiç bir zaman tam bir projede kullanamadım. Bu yüzden Flask-apispec'e bağlı full-stack proje üreticilerde sahip olduğum özellikleri tamamen değiştiremedim. Bu güvenlik entegrasyonunu ekleyen bir <abbr title="Pull request (PR): Git sistemlerinde projenin bir branch'ine yapılan değişikliğin sistemde diğer kullanıcılara ifade edilmesi">PR</abbr> oluşturmak da projelerim arasında yer alıyordu.

Sonrasında ise projenin odağı değişti.

Geliştiricinin Starlette'e odaklanması gerekince proje de artık bir API web framework'ü olmayı bıraktı.

Artık APIStar, OpenAPI özelliklerini doğrulamak için bir dizi araç sunan bir proje haline geldi.

!!! info "Bilgi"

    APIStar, aşağıdaki projeleri de üreten Tom Christie tarafından geliştirildi:

    * Django REST Framework
    * **FastAPI**'ın da dayandığı Starlette
    * Starlette ve **FastAPI** tarafından da kullanılan Uvicorn

!!! check "**FastAPI**'a nasıl ilham oldu?"
    Var oldu.

    Aynı Python veri tipleriyle birden fazla şeyi belirleme ve aynı zamanda harika bir editör desteği sunma, benim muhteşem bulduğum bir fikirdi.

    Uzunca bir süre boyunca benzer bir framework arayıp pek çok farklı alternatifi denedikten sonra, APIStar en iyi seçenekti.

    Sonra APIStar bir sunucu olmayı bıraktı ve Starlette oluşturuldu. Starlette, böyle bir sunucu sistemi için daha iyi bir temel sunuyordu. Bu da **FastAPI**'ın son esin kaynağıydı.

    Ben bu önceki araçlardan öğrendiklerime dayanarak **FastAPI**'ın özelliklerini arttırıp geliştiriyor, typing sistemini ve diğer kısımları iyileştiriyorum ancak yine de **FastAPI**'ı APIStar'ın "ruhani varisi" olarak görüyorum.

## **FastAPI** Tarafından Kullanılanlar

### <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>

Pydantic Python tip belirteçlerine dayanan; veri doğrulama, veri dönüştürme ve dökümantasyon tanımlamak (JSON Şema kullanarak) için bir kütüphanedir.

Tip belirteçleri kullanıyor olması onu aşırı sezgisel yapıyor. Marshmallow ile karşılaştırılabilir bile. Ancak karşılaştırmalarda Marshmallowdan daha hızlı görünüyor. Aynı Python tip belirteçlerine dayanıyor ve editör desteği de harika.

!!! check "**FastAPI** nerede kullanıyor?"

    Bütün veri doğrulama, veri dönüştürme ve JSON Şemasına bağlı otomatik model dökümantasyonunu halletmek için!

    **FastAPI** yaptığı her şeyin yanı sıra bu JSON Şema verisini alıp daha sonra OpenAPI'ya yerleştiriyor.

### <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a>

Starlette hafif bir <abbr title="ASGI (Asynchronous Server Gateway Interface): Asenkron Sunucu Ağ Geçidi Arabirimi, asenkron Python web uygulamaları geliştirmek için yeni standart.">ASGI</abbr> framework'ü ve yüksek performanslı asyncio servisleri oluşturmak için ideal.

Kullanımı çok kolay ve sezgisel, kolaylıkla genişletilebilecek ve modüler bileşenlere sahip olacak şekilde dizayn edildi.

Sahip olduğu bir kaç özellik:

* Cidden etkileyici bir performans.
* WebSocket desteği.
* İşlem-içi arka plan görevleri.
* Başlatma ve kapanış olayları.
* HTTPX ile geliştirilmiş bir test istemcisi.
* CORS, GZip, Static Files ve Streaming cevapları desteği.
* Session ve Cookie desteği.
* Kodun %100'ü test kapsamında.
* Kodun %100'ünde kullanılan veri tipleri açıklanıyor.
* Yalnızca bir kaç zorunlu bağımlılığa sahip.

Starlette şu anda test edilen en hızlı Python framework'ü. Yalnızca bir sunucu olan Uvicorn'a yeniliyor, o da zaten bir framework değil.

Starlette bütün basit web mikro framework işlevselliğini sağlıyor.

Ancak otomatik veri doğrulama, veri dönüştürme ve dökümantasyon sağlamyor.

Bu, **FastAPI**'ın onun üzerine tamamen Python tip belirteçlerine bağlı olarak eklediği (Pydantic ile) ana şeylerden biri. **FastAPI** bunun yanında artı olarak bağımlılık enjeksiyonu sistemi, güvenlik araçları, OpenAPI şema üretimi ve benzeri özellikler de ekliyor.

!!! note "Teknik Detaylar"
    ASGI, Django'nun ana ekibi tarafından geliştirilen yeni bir "standart". Bir "Python standardı" (PEP) olma sürecinde fakat henüz bir standart değil.

    Bununla birlikte, halihazırda birçok araç tarafından bir "standart" olarak kullanılmakta. Bu, Uvicorn'u farklı ASGI sunucularıyla (Daphne veya Hypercorn gibi) değiştirebileceğiniz veya `python-socketio` gibi ASGI ile uyumlu araçları ekleyebileciğiniz için birlikte çalışılabilirliği büyük ölçüde arttırıyor.

!!! check "**FastAPI** nerede kullanıyor?"

    Tüm temel web kısımlarında üzerine özellikler eklenerek kullanılmakta.

    `FastAPI` sınıfının kendisi direkt olarak `Starlette` sınıfından miras alıyor!

    Yani, Starlette ile yapabileceğiniz her şeyi, Starlette'in bir nevi güçlendirilmiş hali olan **FastAPI** ile doğrudan yapabilirsiniz.

### <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>

Uvicorn, uvlook ile httptools üzerine kurulu ışık hzında bir ASGI sunucusudur.

Bir web framework'ünden ziyade bir sunucudur, yani yollara bağlı routing yapmanızı sağlayan araçları yoktur. Bu daha çok Starlette (ya da **FastAPI**) gibi bir framework'ün sunucuya ek olarak sağladığı bir şeydir.

Starlette ve **FastAPI** için tavsiye edilen sunucu Uvicorndur.

!!! check "**FastAPI** neden tavsiye ediyor?"
    **FastAPI** uygulamalarını çalıştırmak için ana web sunucusu Uvicorn!

    Gunicorn ile birleştirdiğinizde asenkron ve çoklu işlem destekleyen bir sunucu elde ediyorsunuz!

    Daha fazla detay için [Deployment](deployment/index.md){.internal-link target=_blank} bölümünü inceleyebilirsiniz.

## Karşılaştırma ve Hız

Uvicorn, Starlette ve FastAPI arasındakı farkı daha iyi anlamak ve karşılaştırma yapmak için [Benchmarks](benchmarks.md){.internal-link target=_blank} bölümüne bakın!
