# Alternatifler, İlham ve Karşılaştırmalar

**FastAPI**'yi neyin ilham verdiği, diğer alternatiflerle karşılaştırması ve onlardan öğrendikleri önemlidir.

## Giriş

**FastAPI**, öncekilerin çalışmaları olmasaydı var olmazdı.

Bu oluşturulmuş birçok araç vardı ve bunlar **FastAPI**'nin oluşturulmasında ilham kaynağı oldu.

Yıllarca yeni bir çerçeve oluşturmaktan kaçındım. İlk olarak, **FastAPI** tarafından kapsanan tüm özellikleri çözmek için birçok farklı çerçeve, eklenti ve araç kullandım.

Ancak bir noktada, tüm bu özellikleri sağlayan, önceki araçlardan en iyi fikirleri alıp bunları mümkün olan en iyi şekilde birleştiren, hatta önceki mevcut olmayan dil özelliklerini (Python 3.6+ tip ipuçları) kullanarak bir şey oluşturmanın başka bir seçenek olmadı.

## Önceki Araçlar

### [Django](https://www.djangoproject.com/)

Bu, en popüler Python çerçevesidir ve geniş bir güvene sahiptir. Instagram gibi sistemleri oluşturmak için kullanılır.

Nispeten sıkı bir şekilde ilişkisel veritabanlarıyla (MySQL veya PostgreSQL gibi) bağlantılıdır, bu nedenle bir NoSQL veritabanını (Couchbase, MongoDB, Cassandra, vb.) ana depolama motoru olarak kullanmak pek kolay değildir.

HTML'yi backend'te oluşturmak için oluşturuldu, modern bir frontend (React, Vue.js ve Angular gibi) veya diğer sistemlerle iletişim kuran (IoT cihazları gibi) bir API oluşturmak için değil.

### [Django REST Framework](https://www.django-rest-framework.org/)

Django REST Framework, Django'nun altında kullanılmak üzere Web API'leri oluşturmak için esnek bir araç takımı oluşturmak amacıyla oluşturuldu.

Mozilla, Red Hat ve Eventbrite gibi birçok şirket tarafından kullanılmaktadır.

Bu, **otomatik API belgelendirmesi** örneklerinden biriydi ve bu özellikle "arama için" **FastAPI**'yi ilham veren ilk fikirlerden biriydi.

!!! not
    Django REST Framework, Tom Christie tarafından oluşturuldu. **FastAPI**'nin temelini oluşturan Starlette ve Uvicorn'un aynı yaratıcısıdır.

!!! kontrol "FastAPI'yi İlham Alan"
    Otomatik API belgelendirmesi web kullanıcı arayüzüne sahip olma.

### [Flask](https://flask.palletsprojects.com)

Flask bir "mikroçerçeve" olarak adlandırılır; veritabanı entegrasyonlarını veya Django'da varsayılan olarak gelen birçok özelliği içermez.

Bu basitlik ve esneklik, NoSQL veritabanlarını ana veri depolama sistemi olarak kullanma gibi şeyleri mümkün kılar.

Çok basit olduğu için öğrenmesi nispeten sezgiseldir, ancak belgeler bazı noktalarda biraz teknikleşir.

Ayrıca, Django'da önceden oluşturulmuş birçok özelliğe ihtiyaç duymayan, kullanıcı yönetimi veya veritabanı gibi şeylere gerek duymayan diğer uygulamalar için de yaygın olarak kullanılır. Bununla birlikte, birçok bu tür özellik, eklentilerle eklenabilir.

Bu parçaların ayrılabilir olması ve tam olarak ihtiyaç duyulanı kapsayacak şekilde genişletilebilen bir "mikroçerçeve" olması, korumak istediğim temel bir özellikti.

Flask'ın basitliği nedeniyle, API'lar oluşturmak için iyi bir seçenek gibi görünüyordu. Sonraki şey, Flask için bir "Django REST Framework" bulmaktı.

!!! kontrol "FastAPI'yi İlham Alan"
    Bir mikroçerçeve olmak. Gereken araçları ve parçaları kolayca karıştırıp eşleştirmeyi mümkün kılmak.

    Basit ve kullanımı kolay bir yönlendirme sistemi olmaya devam etmek.

### [Requests](https://requests.readthedocs.io)

**FastAPI**, aslında **Requests**'in bir alternatifi değildir. Kapsamı çok farklıdır.

Aslında, FastAPI uygulaması *içinde* Requests'ı kullanmak oldukça yaygındır.

Ancak yine de, FastAPI, Requests'tan oldukça fazla ilham almıştır.

**Requests**, API'larla etkileşimde bulunmak (bir istemci olarak) için bir kütüphanedir, **FastAPI** ise API'lar oluşturmak (bir sunucu olarak) için bir kütüphanedir.

Daha çok, birbirini tamamlayan, karşıt uçlarda bulunurlar.

Requests'ın çok basit ve sezgisel bir tasarımı vardır, kullanımı çok kolaydır ve mantıklı varsayılanlara sahiptir. Ancak aynı zamanda çok güçlü ve özelleştirilebilirdir.

Bu nedenle, resmi web sitesinde belirtildiği gibi:

> Requests, tüm zamanların en çok indirilen Python paketlerinden biridir.

Kullanımı çok basittir. Örneğin, bir `GET` isteği yapmak için şu şekilde yazarsınız:

```Python
response = requests.get("http://example.com/some/url")
```

FastAPI karşıt API *yol işlemi* örneği şu şekilde olabilir:

```python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"mesaj": "Merhaba Dünya"}
```

Görüldüğü gibi, `requests.get(...)` ve `@app.get(...)` arasında benzerlikler bulunmaktadır.

!!! "İlham **FastAPI** tarafından alınmıştır"
    * Basit ve sezgisel bir API'ye sahip olun.
    * HTTP yöntem adlarını (işlemleri) doğrudan, basit ve sezgisel bir şekilde kullanın.
    * Mantıklı varsayılanlara sahip olun, ancak güçlü özelleştirmelere de izin verin.


### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a>

Django REST Framework'ten istediğim temel özellik otomatik API belgeleriydi.

Sonra API'leri belgelemek için bir standart olduğunu fark ettim; JSON (veya JSON'un bir uzantısı olan YAML) kullanılıyordu ve buna Swagger deniyordu.

Ve zaten Swagger API'leri için bir web kullanıcı arayüzü oluşturulmuştu. Bu nedenle, bir API için Swagger belgesi oluşturabilmek, bu web kullanıcı arayüzünü otomatik olarak kullanmaya olanak tanırdı.

Bir noktada, Swagger, Linux Foundation'a devredildi ve adı OpenAPI olarak değiştirildi.

Bu nedenle, sürüm 2.0'den bahsedilirken genellikle "Swagger" denirken, sürüm 3+ için "OpenAPI" denilmektedir.

!!! "İlham **FastAPI** tarafından alınmıştır"
    API spesifikasyonları için özel bir şemadan ziyade açık bir standartı benimseyin ve kullanın.

    Ve standartlara dayalı kullanıcı arayüzü araçlarını entegre edin:

    * <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>
    * <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>

    Bu ikisi, oldukça popüler ve stabil olmaları nedeniyle seçilmiştir, ancak hızlı bir arama yaparak OpenAPI için onlarca alternatif kullanıcı arayüzü bulabilirsiniz (ki bunları **FastAPI** ile kullanabilirsiniz).

### Flask REST Frameworks

Birçok Flask REST framework'u bulunmaktadır, ancak bunları araştırmak için zaman ve çaba harcadıktan sonra, birçoğunun durdurulduğu veya terkedildiği, kullanılamaz hale getiren birkaç sorunla karşılaştığımı fark ettim.

### <a href="https://marshmallow.readthedocs.io/en/stable/" class="external-link" target="_blank">Marshmallow</a>

API sistemleri tarafından ihtiyaç duyulan temel özelliklerden biri veri "<abbr title="ayrıca marshalling, dönüştürme olarak da adlandırılır">serileştirme</abbr>"dir, yani kod (Python) içindeki veriyi alıp ağ üzerinden gönderilebilecek bir şeye dönüştürme işlemidir. Örneğin, bir veritabanındaki veriyi içeren bir nesneyi JSON nesnesine dönüştürme. `datetime` nesnelerini dizelere dönüştürme, vb.

API'ler tarafından ihtiyaç duyulan diğer önemli bir özellik ise veri doğrulamasıdır, yani belirli parametreler verildiğinde verinin geçerli olduğunu sağlama işlemidir. Örneğin, bir alanın bir `int` olduğundan ve rastgele bir dize olmadığından emin olma. Bu özellik özellikle gelen veri için kullanışlıdır.

Veri doğrulama sistemi olmadan, tüm kontrolleri kod içinde manuel olarak yapmanız gerekirdi.

Bu özellikleri sağlamak için Marshmallow oluşturulmuştur. Harika bir kütüphanedir ve önceden birçok kez kullandım.

Ancak, Python tip ipuçları mevcut olmadan önce oluşturuldu. Bu nedenle, her <abbr title="verinin nasıl oluşturulması gerektiğinin tanımı">şemayı</abbr> tanımlamak için Marshmallow tarafından sağlanan belirli araçlar ve sınıfları kullanmanız gerekmektedir.

!!! "İlham **FastAPI** tarafından alınmıştır"
    "Şemaları" tanımlamak için kodu kullanın ve otomatik olarak veri türleri ve doğrulama sağlayın.

### <a href="https://webargs.readthedocs.io/en/latest/" class="external-link" target="_blank">Webargs</a>

API'ler tarafından gereken diğer büyük bir özellik gelen isteklerden veri <abbr title="okuma ve Python verisine dönüştürme">çıkarma</abbr>dır.

Webargs, birkaç çerçeve üzerine (Flask dahil) bunu sağlamak için yapılmış bir araçtır.

Veri doğrulamasını yapmak için altta Marshmallow'yu kullanır ve aynı geliştiriciler tarafından oluşturulmuştur.

Harika bir araçtır ve **FastAPI**'ye sahip olmadan önce birçok kez kullandım.

!!! info
    Webargs, aynı Marshmallow geliştiricileri tarafından oluşturulmuştur.

!!! "İlham **FastAPI** tarafından alınmıştır"
    Gelen istek verilerinin otomatik doğrulamasını yapın.

### <a href="https://apispec.readthedocs.io/en/stable/" class="external-link" target="_blank">APISpec</a>

Marshmallow ve Webargs, eklentiler olarak doğrulama, çıkarma ve serileştirme sağlar.

Ancak belgeleme hala eksiktir. Bu nedenle APISpec oluşturuldu.

Bu, birçok çerçeve için bir eklentidir (ve Starlette için bir eklenti de vardır).

Çalışma şekli, her bir rotayı işleyen işlevin docstring'i içinde YAML formatında şema tanımını yazmanızdır.

Ve OpenAPI şemalarını oluşturur.

Bu, Flask, Starlette, Responder, vb. için nasıl çalışır.

Ancak burada tekrar bir mikro sözdizimi sorunuyla karşılaşıyoruz, bir Python dizesi içinde (büyük bir YAML içinde) bir mikro sözdizimi var.

Düzenleyici bu konuda çok yardımcı olamaz. Ve parametreleri veya Marshmallow şemalarını değiştirirken ve bu YAML docstring'i değiştirmeyi unutursak, oluşturulan şema güncellenmemiş olur.

!!! info
    APISpec, aynı Marshmallow geliştiricileri tarafından oluşturulmuştur.

!!! "İlham **FastAPI** tarafından alınmıştır"
    API'ler için açık bir standart olan OpenAPI'yi destekleyin.

### [Flask-apispec](https://flask-apispec.readthedocs.io/en/latest/)

Flask-apispec, Webargs, Marshmallow ve APISpec'i bir araya getiren bir Flask eklentisidir.

Webargs ve Marshmallow'dan gelen bilgileri kullanarak APISpec'i kullanarak otomatik olarak OpenAPI şemaları oluşturur.

Bu, Python docstring'lerine YAML (başka bir sözdizimi) yazma zorunluluğunu ortadan kaldırdı.

Flask, Flask-apispec, Marshmallow ve Webargs kombinasyonu, **FastAPI** inşa edilene kadar favori backend yığınımdı.

Bu kullanım, birkaç Flask tam yığını oluşturucusunun ortaya çıkmasına yol açtı. Şu ana kadar benim (ve birçok harici takımın) kullandığı ana yığınlar şunlar:

- [https://github.com/tiangolo/full-stack](https://github.com/tiangolo/full-stack)
- [https://github.com/tiangolo/full-stack-flask-couchbase](https://github.com/tiangolo/full-stack-flask-couchbase)
- [https://github.com/tiangolo/full-stack-flask-couchdb](https://github.com/tiangolo/full-stack-flask-couchdb)

Ve bu aynı tam yığın oluşturucuları, [**FastAPI** Proje Oluşturucularının](project-generation.md){.internal-link target=_blank} temelini oluşturdu.

!!! info
    Flask-apispec, aynı Marshmallow geliştiricileri tarafından oluşturuldu.

!!! check "Inspired **FastAPI** to"
    Aynı kodu kullanarak otomatik olarak OpenAPI şemasını oluşturun, serileştirme ve doğrulamayı tanımlayan.

### [NestJS](https://nestjs.com/) (ve [Angular](https://angular.io/))

Bu Python bile değil, NestJS, Angular'dan esinlenmiş JavaScript (TypeScript) NodeJS bir çerçevedir.

Flask-apispec ile benzer bir şey başarmayı amaçlar.

Angular iki tarafından ilham alan entegre bir bağımlılık enjeksiyon sistemine sahiptir. "Injectables" (bildiğim diğer tüm bağımlılık enjeksiyon sistemleri gibi) önceden kaydedilmelidir, bu da kelime tekrarına neden olur.

Parametreler TypeScript türleri ile açıklanır (Python tip ipuçlarına benzer şekilde), bu nedenle düzenleyici desteği oldukça iyidir.

Ancak TypeScript verileri JavaScript'e derlendikten sonra korunmadığı için, aynı anda doğrulama, serileştirme ve belge oluşturmak için tiplere güvenmek mümkün değildir. Bu nedenle, doğrulama, serileştirme ve otomatik şema oluşturmak için birçok yere dekoratör eklemek gereklidir, bu da oldukça açıklayıcı hale gelir.

İç içe geçmiş modellerle iyi başa çıkamaz. Bu nedenle, isteğin JSON gövdesi içinde iç içe geçmiş JSON nesnelerini içeren iç alanlara uygun şekilde belgelendirilemez ve doğrulanamaz.

!!! check "Inspired **FastAPI** to"
    Mükemmel düzenleyici desteği için Python tiplerini kullanın.

    Güçlü bir bağımlılık enjeksiyon sistemine sahip olun. Kod tekrarını en aza indirmek için bir yol bulun.

### [Sanic](https://sanic.readthedocs.io/en/latest/)

Bu, `asyncio` temelliyken Python'un ilk son derece hızlı frameworklerinden biriydi. Flask'a çok benzer bir şekilde yapılmıştır.

!!! note "Teknik Detaylar"
    Bu, varsayılan Python `asyncio` döngüsü yerine <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a> kullanıyordu. Bu, onu bu kadar hızlı yapan şeydi.

    Açık benchmarklarda Uvicorn ve Starlette'yi açıkça etkiledi ve şu anda Sanic'ten daha hızlıdır.

!!! check "Inspired **FastAPI** to"
    Çılgın performansa sahip bir yol bulun.

    Bu nedenle **FastAPI**, en hızlı çerçeve olduğu için Starlette'e dayanmaktadır (üçüncü taraf benchmarklar tarafından test edilmiştir).

### [Falcon](https://falconframework.org/)

Falcon, yüksek performanslı başka bir Python framework'üdür; minimal olarak tasarlanmıştır ve Hug gibi diğer framework'lerin temeli olarak çalışması amaçlanmıştır.

İki parametre alan işlevlere sahip olacak şekilde tasarlanmıştır: biri "request" (istek) ve diğeri "response" (yanıt). Ardından isteğin bölümlerini "okur" ve yanıta bölümler "yazar". Bu tasarım nedeniyle, standart Python tip ipuçları kullanılarak istek parametreleri ve gövdeleri bildirmek mümkün değildir.

Bu nedenle, veri doğrulama, serileştirme ve belgeleme, otomatik olarak değil, kod içinde yapılmalıdır. Veya bunlar, Falcon'un üstünde bir çerçeve olarak, Hug gibi uygulanmalıdır. Bu tasarımın etkilendiği diğer framework'lerde de aynı ayrım meydana gelir: bir istek nesnesi ve bir yanıt nesnesi olarak parametreleri olan.

!!! Kontrol et "FastAPI'yi **esinlenen**"
    Harika performans elde etmek için yollar bulun.

    Hug ile birlikte (Hug, Falcon'a dayandığından) **FastAPI**'yi fonksiyonlarda bir `response` parametresi bildirmeye özendirdi.

    FastAPI'de bu isteğe bağlıdır ve genellikle başlıkları, çerezleri ve alternatif durum kodlarını ayarlamak için kullanılır.

### [Molten](https://moltenframework.com/)

Molten'u **FastAPI** oluşturma sürecinin ilk aşamalarında keşfettim ve oldukça benzer fikirlere sahip:

* Python tip ipuçlarına dayanıyor.
* Bu tiplerden doğrulama ve belgeleme.
* Bağımlılık enjeksiyon sistemi.

Pydantic gibi bir veri doğrulama, serileştirme ve belgeleme üçüncü taraf kütüphanesi kullanmaz, kendi kütüphanesine sahiptir. Bu nedenle, bu veri tipleri tanımlamaları aynı kolaylıkla yeniden kullanılamaz.

Biraz daha açıklayıcı yapılandırmalar gerektirir. Ve WSGI'ye dayanmaktadır (ASGI yerine geçer), bu nedenle Uvicorn, Starlette ve Sanic gibi araçların sağladığı yüksek performanstan faydalanmak için tasarlanmamıştır.

Bağımlılık enjeksiyon sistemi, bağımlılıkların önceden kaydedilmesini gerektirir ve bağımlılıklar, bildirilen tiplere dayalı olarak çözülür. Bu nedenle, belirli bir türü sağlayan birden fazla "bileşen" bildirmek mümkün değildir.

Yollar, tek bir yerde bildirilir ve uç noktayı işleyen işlevler başka yerlerde bildirilir (işlevi işleyen uç nokta üzerine doğrudan yerleştirilebilecek dekoratörler yerine). Bu, kod içinde nispeten sıkı bir şekilde bağlı olan şeyleri ayırır, bu da Flask (ve Starlette) tarafından nasıl yapıldığından daha çok Django'nun nasıl yapıldığına benzer.

!!! Kontrol et "FastAPI'yi **esinlenen**"
    "Varsayılan" model özniteliklerinin değeri üzerinden veri türleri için ek doğrulamalar tanımlamak. Bu, editör desteğini artırır ve Pydantic'te önce mevcut olmayan bir özellikti.

    Bu aslında Pydantic'in bazı bölümlerini güncelleme konusunda esin kaynağı oldu, aynı doğrulama bildirimi stiline destek şu anda Pydantic'te mevcuttur.

### [Hug](https://www.hug.rest/)

Hug, Python tip ipuçları kullanarak API parametre tiplerini bildirmeyi uygulayan ilk framework'lerden biriydi. Bu harika bir fikirdi ve diğer araçları aynısını yapmaya teşvik etti.

Standart Python tipleri yerine özel tipleri bildirimlerinde kullanıyordu, ancak bu yine de büyük bir adımdı.

Ayrıca, API'nin tamamını JSON içinde bildiren özel bir şema oluşturan ilk framework'lerden biriydi.

OpenAPI ve JSON Schema gibi bir standarta dayanmıyordu. Bu nedenle, Swagger UI gibi diğer araçlarla entegre etmek doğrudan mümkün olmayabilirdi. Ancak yine de çok yenilikçi bir fikirdi.

İlginç ve sıradışı bir özelliği vardı: aynı framework kullanılarak API'lar ve CLI'lar oluşturmak mümkündü.

Daha önceki senkron Python web framework'leri için bir standarta dayandığı için (WSGI), Websockets ve diğer şeylerle başa çıkamaz, ancak yine de yüksek performansa sahiptir.

!!! Bilgi
    Hug, <a href="https://github.com/timothycrosley/isort" class="external-link" target="_blank">`isort`</a> adlı, Python dosyalarındaki içe aktarılmışları otomatik olarak sıralamak için harika bir araç olan Timothy Crosley tarafından oluşturuldu.

!!! Kontrol et "FastAPI'yi **esinlenen**"
    Hug, APIStar'ın birçok bölümünü ilham verdi ve APIStar ile birlikte en umut verici araçlardan biriydi.

    Hug, **FastAPI**'yi parametreleri bildirmek ve API'yi otomatik olarak tanımlayan bir şema oluşturmak için Python tip ipuçları kullanmaya teşvik etti.

    Hug, **FastAPI**'yi fonksiyonlarda başlık ve çerezleri ayarlamak için bir `response` parametresi bildirmeye özendirdi.

### [APIStar](https://github.com/encode/apistar) (<= 0.5)

**FastAPI**'yi oluşturmaya karar vermeden hemen önce **APIStar** sunucusunu buldum. Neredeyse aradığım her şeye sahipti ve harika bir tasarıma sahipti.

Python tip ipuçlarını kullanarak parametreleri ve istekleri bildiren bir framework'ün ilk uygulamalarından biriydi (NestJS ve Molten'den önce). Hug'u aynı zamanda keşfettiğim bir dönemdi. Ancak APIStar, OpenAPI standardını kullanıyordu.

Aynı tip ipuçlarına dayalı olarak birkaç yerde otomatik veri doğrulama, veri serileştirme ve OpenAPI şema oluşturması vardı.

Pydantic gibi Python tip ipuçlarını kullanmayan bir vücut şema tanımı vardı; biraz daha çok Marshmallow'ya benziyordu, bu nedenle editör desteği o kadar iyi olmazdı, ancak yine de APIStar mevcut en iyi seçenekti.

O dönemde en iyi performans test sonuçlarına sahipti (yalnızca Starlette tarafından aşıldı).

İlk başta otomatik bir API belgelendirme web arayüzü yoktu, ancak buna Swagger UI ekleyebileceğimi biliyordum.

Bağımlılık enjeksiyon sistemine sahipti. Yukarıda tartışılan diğer araçlar gibi, bileşenlerin önceden kaydedilmesini gerektiriyordu. Ancak yine de harika bir özellikti.

Asla tam bir projede kullanamadım, çünkü güvenlik entegrasyonu yoktu, bu nedenle Flask-apispec'e dayalı tam yığın üreteçleriyle sahip olduğum tüm özellikleri değiştiremiyordum. Bu işlevselliği ekleyen bir pull isteği oluşturmak için projelerimin gündemimde vardı.

Ancak sonra, projenin odak noktası değişti.

Artık bir API web framework değil, yaratıcının Starlette'ye odaklanması gerekiyordu.

Şimdi APIStar, OpenAPI belirtimlerini doğrulamak için bir dizi araçtır, bir web framework değildir.

!!! Bilgi
    APIStar, Tom Christie tarafından oluşturuldu. Aynı kişi şunları da oluşturdu:

    * Django REST Framework
    * Starlette (ki **FastAPI** ona dayanmaktadır)
    * Uvicorn (Starlette ve **FastAPI** tarafından kullanılır)

!!! Kontrol et "FastAPI'yi **esinlenen**"
    Var.

    Aynı Python tiplerini kullanarak birden çok şeyi (veri doğrulama, serileştirme ve belgeleme) bildirme fikri, aynı zamanda harika bir editör desteği sağlıyordu ve benim için parlak bir fikir olarak kabul ettim.

    Ve benzer bir framework arayışında uzun bir süre geçirdikten ve birçok farklı alternatifi test ettikten sonra, APIStar en iyi seçenekti.

    Sonra APIStar'ın bir sunucu olarak varlığını sürdürmeyi bıraktı ve Starlette oluşturuldu, bu da böyle bir sistem için yeni ve daha iyi bir temel oldu. Bu, **FastAPI**'yi oluşturmak için son ilham kaynağıydı.

    **FastAPI**'yi APIStar'ın "ruhsal halefi" olarak kabul ediyorum, aynı zamanda tüm bu önceki araçlardan alınan öğrenimlere dayanarak özellikleri, tip sistemi ve diğer parçaları geliştirip arttırıyor.

## **FastAPI** tarafından Kullanılanlar

### [Pydantic](https://pydantic-docs.helpmanual.io/)

Pydantic, Python tip ipuçlarına dayalı olarak veri doğrulama, serileştirme ve belgeleme (JSON Schema kullanarak) tanımlamak için bir kütüphanedir.

Bu onu son derece sezgisel hale getirir.

Marshmallow ile karşılaştırılabilir. Benchmarklarda Marshmallow'dan daha hızlıdır. Ve aynı Python tip ipuçlarına dayandığı için editör desteği harikadır.

!!! Kontrol et "**FastAPI** bunu kullanır çünkü"
    Tüm veri doğrulama, veri serileştirme ve otomatik model belgesi işlemlerini (JSON Schema'ya dayalı olarak) yönetir.

    **FastAPI**, ardından bu JSON Schema verilerini OpenAPI'ye koyar, diğer yaptığı birçok şeyden ayrı olarak.

### [Starlette](https://www.starlette.io/)

Starlette, yüksek performanslı asyncio hizmetleri oluşturmak için ideal olan hafif bir <abbr title="Asenkron Python web uygulamaları oluşturmak için yeni standart">ASGI</abbr> çerçeve/toolkit'tir.

Çok basit ve sezgiseldir. Kolayca genişletilebilir olacak şekilde tasarlanmıştır ve modüler bileşenlere sahiptir.

Bunlar şunlardır:

* Ciddi derecede etkileyici performans.
* WebSocket desteği.
* İşlem içi arka plan görevleri.
* Başlatma ve kapatma etkinlikleri.
* HTTPX üzerine inşa edilmiş test istemcisi.
* CORS, GZip, Statik Dosyalar, Akışlı yanıtlar.
* Oturum ve Çerez desteği.
* %100 test kapsamı.
* %100 tip belirtilmiş kod tabanı.
* Az sayıda sıkı bağımlılık.

Starlette şu anda test edilen en hızlı Python çerçevesidir. Yalnızca bir sunucu değil, ancak bir sunucu olan Uvicorn tarafından aşılmıştır.

Starlette, temel web mikroçerçeve işlevselliğini sağlar.

Ancak otomatik veri doğrulama, serileştirme veya belgeleme sağlamaz.

Bu, **FastAPI**'nin üzerine eklediği temel şeylerden biridir, hepsi Python tip ipuçlarına dayanır (Pydantic kullanarak). Buna ek olarak, bağımlılık enjeksiyon sistemi, güvenlik yardımcı programları, OpenAPI şema oluşturma, vb.

!!! not "Teknik Detaylar"
    ASGI, Django çekirdek ekibi üyeleri tarafından geliştirilmekte olan yeni bir "standart"tır. Henüz bir "Python standardı" (PEP) değildir, ancak bunu yapma sürecindedirler.

    Yine de, birkaç araç tarafından zaten bir "standart" olarak kullanılmaktadır. Bu, değiştirilebilen Uvicorn'u başka herhangi bir ASGI sunucusuyla (örneğin Daphne veya Hypercorn gibi) değiştirebileceğiniz veya `python-socketio` gibi ASGI uyumlu araçları ekleyebileceğiniz anlamına gelir.

!!! kontrol "**FastAPI** bunu kullanır çünkü"
    Tüm temel web parçalarını yönetir. Üzerine özellikler ekler.

    `FastAPI` sınıfı kendisini doğrudan `Starlette` sınıfından miras alır.

    Bu nedenle, Starlette ile yapabileceğiniz her şeyi, **FastAPI** ile doğrudan yapabilirsiniz, çünkü temelde **FastAPI**, Starlette'in steroidlerle güçlendirilmiş hali olarak düşünülebilir.

### [Uvicorn](https://www.uvicorn.org/)

Uvicorn, uvloop ve httptools üzerine inşa edilmiş hızlı bir ASGI sunucusudur.

Bu bir web çerçevesi değil, ancak bir sunucudur. Örneğin, yolları belirleme araçları sağlamaz. Bu, Starlette (veya **FastAPI**) gibi bir çerçeve tarafından üzerine eklenir.

Starlette ve **FastAPI** için önerilen sunucudur.

!!! kontrol "**FastAPI** bunu önerir çünkü"
    **FastAPI** uygulamalarını çalıştırmak için ana web sunucusudur.

    Gunicorn ile birleştirerek, asenkron çok işlemli bir sunucuya sahip olabilirsiniz.

    Daha fazla ayrıntıyı [Dağıtım](deployment/index.md){.internal-link target=_blank} bölümünde kontrol edebilirsiniz.

## Performans ve Hız Karşılaştırmaları

Uvicorn, Starlette ve FastAPI arasındaki farkları anlamak, karşılaştırmak ve görmek için [Benchmarks](benchmarks.md){.internal-link target=_blank} bölümüne göz atın.

