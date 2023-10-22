---
hide:
  - navigation
---

# Özellikler

## FastAPI Özellikleri

**FastAPI** bize şu özellikleri sunuyor:

### Açık Kaynak Standartlar Üzerine Kurulu

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> oluşturduğumuz <abbr title="path, endpoints yada routes olarak da isimlendirilebilir">adres</abbr> <abbr title="HTTP metodları olarak bilinen, POST, GET, PUT, DELETE">operasyonlarını </abbr>parametreleri, gövde talebi, güvenlik gibi şeyler dahil olmak üzere bunların tanımlamalarının yapılması.
* Otomatik olarak veri modelinin <a href="http://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> ile beraber dökümante edilmesi (OpenAPI'n kendisi zaten JSON Schema'ya dayanıyor).
* Titiz bir çalışmanın sonucunda yukarıdaki standartlara uygun bir framework oluşturduk. Standartları pastanın üzerine sonradan eklenmiş bir çilek olarak görmedik.* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> oluşturduğumuz <abbr title="path, endpoints yada routes olarak da isimlendirilebilir">adres</abbr> <abbr title="HTTP metodları olarak bilinen, POST, GET, PUT, DELETE">operasyonlarını </abbr>parametreleri, gövde talebi, güvenlik gibi şeyler dahil olmak üzere bunların tanımlamalarının yapılması.
* Ayrıca bu bir çok dilde kullanılabilecek <abbr title="client code generation">**istemci taraflı kod oluşturucu**</abbr> kullanımına da izin veriyor.

### Otomatik Dokümantasyon

Etkileşimli API Dokümantasyonu ve Web Kullanıcı Arayüzü: Bu framework OpenAPI standartlarına dayalı olduğu için, birden fazla opsiyonumuz var ve bunlardan iki tanesi kullanımınıza hazır.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a> interaktif olarak API'ınızı tarayıcı üzerinden çağırıp test edebilmenize olanak sağlıyor.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a> ile beraber alternatif API dokümantasyonu.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Sadece Modern Python

Tamamen **Python 3.6**'nın tip belirteçlerine dayanıyor (Pydantic'in sayesinde). Yeni bir syntax öğrenmene gerek yok. Sadece modern Python.

Eğer Python tip belirteçlerini bilmiyorsan veya bir hatırlatmaya ihtiyacın var ise (FastAPI kullanmasan bile) şu iki dakikalık küçük bilgilendirici içeriğe bir göz atabilirsin: [Python Types](python-types.md){.internal-link target=_blank}.

Standart Python'u tiplerini belirterek yazıyorsun:

```Python
from datetime import date

from pydantic import BaseModel

# Değişkeni str olarak belirtelim
# Bu bize o fonksiyon için harika bir editör desteği vericek
def main(user_id: str):
    return user_id


# Pydantic modeli
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Sonrasında bu şekilde kullanabilirsin

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! info "Bilgi"
    `**second_user_data` şu anlama geliyor:

    Anahtar-Değer çiftini doğrudan `second_user_data` sözlüğüne kaydet, bu işlemin sonucunda alacağınız çıktı: `User(id=4, name="Mary", joined="2018-11-30")`

### Editor Desteği

Bütün framework kolay ve sezgisel olması için tasarlandı, verilen bütün kararlar geliştiricilere en iyi geliştirme deneyimini yaşatmak üzere tasarlandı ve bir çok editör üzerinde test edildi.

Son yapılan Python geliştiricileri anketinde, açık ara <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">en çok kullanılan özellik "otomatik tamamlama" idi.</a>.

**FastAPI** frameworkü baştan sona otomatik tamamlama açısından geliştiriciyi tatmin etmek üzerine tasarlandı. Otomatik tamamlama her yerde çalışıyor.

Dokümantasyona tekrardan çok nadir olarak geleceksin.

Editörün sana nasıl yardım ettiğine bir bak:

* <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a> ile:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> ile:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Daha önceden düşünüp en imkansız diyebileceğin durumlarda bile otomatik tamamlama alacaksın, örnek olarak `price` JSON içerisinde (iç içer bir JSON'da olabilirdi.) direkt olarak istekten geliyor, bu durumda bile otomatik tamamlama sağlıyor.

Artık key isimlerini yanlış yazma, dokümantasyona dönüp deliler gibi yukarı aşağı sayfada gezmek ve en sonunda `username` mi yoksa `user_name` mi kullandım gibi sorular yok.

### Kısa

Her şey için mantıklı bir **varsayılanı** var. Parametrelerini opsiyonel olarak tanımlayıp API'nı istediğin gibi modifiye edebilirsin.

Hepsi varsayılan olarak **çalışıyor**.

### Doğrulama

* Neredeyse bütün (ya da hepsi?) Python **veri tipleri** için doğrulama, kapsadıkları:
    * JSON nesneleri (`dict`).
    * JSON array (`list`) item tipini belirtirken.
    * String (`str`) parametresi, minimum ve maksimum uzunluk gibi sınırlandırmalar yaparken.
    * Numaralar (`int`, `float`) maksimum ve minimum gibi sınırlandırmalar yaparken.

* Bunlar gibi sık kullanılmayan tiplerle bile doğrulama yapabiliyorsunuz:
    * URL.
    * Email.
    * UUID.
    * ...ve diğerleri.

Bütün doğrulama olayları çok güçlü bir kütüphane sayesinde yapılıyor, **Pydantic**.

### Güvenlik ve Kimlik Doğrulama

Güvenlik ve doğrulama veritabanı ve veri modellerinden taviz vermeden entegre edilebilir durumda.

Bütün güvenlik şemaları OpenAPI'da tanımlanmış durumda, kapsadıkları:

* HTTP Basic.
* **OAuth2** (ve **JWT tokenleriyle** beraber). Bu öğretici içeriğe göz atabilirsin [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* API anahtarları:
    * Headerlar.
    * Sorgu parametreleri.
    * Çerezler vb

Bütün güvenlik özellikleri Starlette'den geliyor (**session cookies'de** dahil olmak üzere).

Bunların tamamı tekrardan kullanılabilir araçlar ve bileşenler olarak, sistemlerinize, veri depolarınıza, ilişkisel ve NoSQL veritabanlarınıza kolayca entegre edebileceğiniz şekilde yapıldı

### Bağımlılık Enjeksiyonu

FastAPI'ın inanılmaz derecede kullanımı kolay, fakat inanılmaz derecede güçlü <abbr title='"bileşen", "kaynak", "servis", "sağlayıcı" olarak da bilinen'><strong>Bağımlılık Enjeksiyonu </strong></abbr> sistemi var.

* Bağımlılıkların bile bağımlılıkları olabiliyor, FastAPI bunun  için **"bağımlılık" grafiği** oluşturuyor.
* Hepsi **otomatik olarak** FastAPI tarafından hallediliyor.
* Bütün zorunlulukların gelen datalara bağlı olarak farklı gereksinimleri olabiliyor, ilave yol operasyonlarının kısıtlamaları ve otomatik dokümantasyonu da ayrıca yapılıyor .
* Yol operasyonu parametreleri içerisinde belirtilen gereksinimler için bile **Otomatik doğrulama** yapılabiliyor.
* Kompleks kimlik doğrulama sistemleri için destek, **veritabanı bağlantıları**, vb.
* **Taviz yok** hiçbir şeyden taviz vermeden, database frontend vb. Bütün hepsinin kolayca entegre edilebiliyor.

### Sınırsız "Eklenti"

Başka bir deyişle, eklentilere ihtiyacımız yok, import edip direkt olarak kullanmaya başlayabiliriz.

Bütün entegrasyonlar kullanımı kolay olmak üzere (zorunluluklar ile beraber) tasarlandı, sen bir "eklenti" oluşturup 2 satır kod ile, *yol operasyonlarında* kullandığımız syntax ve aynı yapı ile koduna entregre edebilirsin.

### Tamamen Test Edilmiş ve Güvenilir

* %100 <abbr title="Kodun ne kadarının test edildiği">testle kapsanmış</abbr>.
* %100 <abbr title="Python tip belirteçleri bazı kod editörleri ve araçlarda daha iyi destek sunar">tipleri belirtilmiş</abbr> kod tabanı.
* Son kullanıcılar tarafından kullanılan FastAPI ile geliştirilmiş bir çok proje bulunuyor.

## Starlette Özellikleri

**FastAPI**, <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong></a> ile tamamiyle uyumlu ve üzerine kurulu. Yani FastAPI üzerine ekleme yapacağınız herhangi bir Starlette kodu da çalışacaktır.

`FastAPI` aslında `Starlette`'nin alt katmanında kullanan bir üst framework. Eğer Starlette'nin nasıl kullanılacağını biliyorsanız, çoğu işlevini aynı şekilde yapıyor.

**FastAPI** ile beraber **Starlette**'nin bütün özelliklerine de sahip olacaksınız (FastAPI aslında Starlette'nin steroid basmış hali):

* Gerçekten etkileyici bir performansa sahip. Python'un ise en hızlı frameworklerinden bir tanesi, <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">**NodeJS** ve **Go** ile ise eşdeğer performansa sahip.</a>.
* **WebSocket** desteği.
* Çalışma anında arka planda iş  parçacıkları çalıştırabilme imkanı.
* Başlatma ve kapatma anında kod çalıştırabilme (startup and shutdown).
* HTTPX kütüphanesi üzerine kurulu test sistemi sunar.
* **CORS**, GZip, Static dosyalar, Streaming yanıtları.
* **Oturum and Çerez** desteği.
* Kod tabanının tamamen (100%) test ile kapsanmıştır.
* Kod tabanının tamamen (100%) tip belirteçleriyle desteklenmiştir.

## Pydantic Özellikleri

**FastAPI**  <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a> ile tamamen uyumlu ve üzerine kurulu. Sonuç olarak sahip olduğunuz herhangi bir Pydantic kodu FastAPI ile birlikte çalışacaktır.

Bunlara Pydantic üzerine kurulu <abbr title="Object-Relational Mapper">ORM</abbr> veritabanları ve , <abbr title="Object-Document Mapper">ODM</abbr> kütüphaneler de dahil olmak üzere.

Bu ayrıca şu anlama da geliyor, bir çok durumda requestten gelen nesneyi **direkt olarak database**'e her şeyi otomatik olarak doğrulanmış bir biçimde aktarabilirisin.

Aynı şekilde, veritabanından gelen nesneyi de **direkt olarak isteğe** de tamamiyle doğrulanmış bir biçimde gönderebilirsiniz.

**FastAPI** ile beraber **Pydantic**'in bütün özelliklerine sahip olacaksınız (FastAPI data kontrolünü Pydantic'in üzerine kurduğu için):

* **Kafa karıştırmaz**:
    * Farklı bir sözyazımı öğrenmenize gerek kalmaz,
    * Eğer Python tiplerini nasıl kullanacağını biliyorsan Pydantic kullanmayı da biliyorsundur.
* Kullandığın geliştirme araçları ile iyi çalışır **<abbr title="Integrated Development Environment, kod editörüne benzer">IDE</abbr>/<abbr title="Code errorlarınızı inceleyen program">linter</abbr>/brain**:
    * Pydantic'in veri yapıları aslında sadece senin tanımladığın classlar; Bu yüzden doğrulanmış dataların ile otomatik tamamlama, linting ve mypy'ı kullanarak sorunsuz bir şekilde çalışabilirsin.
* **En kompleks** yapıları bile doğrula:
    * Hiyerarşik Pydantic modellerinin kullanımı ile beraber, Python `typing`’s `List` and `Dict`, vs gibi şeyleri doğrula.
    * Doğrulayıcılar en kompleks data şemalarının bile temiz ve kolay bir şekilde tanımlanmasına izin veriyor, ve hepsi JSON şeması olarak dokümante ediliyor.
    * Pydantic, JSON nesnen ne kadar derin (nested) olursa olsun doğrulamasını ve gösterimini yapıyor.
* **Genişletilebilir**:
    * Pydantic özelleştirilmiş data tiplerinin tanımlanmasının yapılmasına izin veriyor ayrıca validator decoratorü ile senin doğrulamaları genişletip, kendi doğrulayıcılarını yazmana izin veriyor.
* 100% test kapsayıcılığı.
