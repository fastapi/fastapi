# Özelikler

## FastAPI özellikleri

**FastAPI** sana bunları sağlıyor

### Açık standartları temel alır

* API oluşturma işlemlerinde <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> buna <abbr title="also known as: endpoints, routes">path</abbr> <abbr title=" HTTP metodları olarak bilinen, POST, GET, PUT, DELETE">operasyonları </abbr>parametreleri, body talebi, güvenlik  gibi şeyler dahil olmak üzere deklare bunların deklare edilmesi.
* Otomatik olarak data modelinin <a href="http://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> ile beraber dokümante edilmesi (OpenAPI'n kendisi zaten JSON Schema'ya dayanıyor).
* Titiz bir çalışmanın sonucunda yukarıdaki standartlara uygun bir framework oluşturduk. Standartları pastanın üzerine sonradan eklenmiş bir çilek olarak görmedik.
* Ayrıca bu bir çok dilde kullanılabilecek **client code generator** kullanımına da izin veriyor.

### Otomatik dokümantasyon


OpenAPI standartlarına dayalı olan bir framework olarak, geliştiricilerin birden çok seçeneği var, varsayılan olarak gelen 2 farklı interaktif API dokümantasyonu ve web kullanıcı arayüzü var.


* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a> interaktif olarak API'ınızı tarayıcı üzerinden çağırıp test edebilmenize olanak sağlıyor.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a> ile beraber alternatif API dokümantasyonu.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Sadece modern Python

Tamamiyle standartlar **Python 3.6**'nın type hintlerine dayanıyor (Pydantic'in sayesinde). Yeni bir syntax öğrenmene gerek yok. Sadece modern Python.


Eğer Python type hintlerini bilmiyorsan veya bir hatırlatmaya ihtiyacın var ise(FastAPI kullanmasan bile) şu iki dakikalık küçük bilgilendirici içeriğe bir göz at: [Python Types](python-types.md){.internal-link target=_blank}.

Standart Python'u typelarını belirterek yazıyorsun:

```Python
from typing import List, Dict
from datetime import date

from pydantic import BaseModel

# Değişkeni str olarak belirt
# ve o fonksiyon için harika bir editör desteği al
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

!!! info
    `**second_user_data` şu anlama geliyor:

    Key-Value çiftini direkt olarak  `second_user_data` dictionarysine kaydet , yaptığın şey buna eşit olacak: `User(id=4, name="Mary", joined="2018-11-30")`

### Editor desteği

Bütün framework kullanılması kolay ve sezgileri güçlü olması için tasarlandı, verilen bütün kararlar geliştiricilere en iyi geliştirme deneyimini yaşatmak üzere, bir çok editör üzerinde test edildi.

Son yapılan Python geliştiricileri anketinde, açık ara <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">en çok kullanılan özellik "oto-tamamlama" idi.</a>.

Bütün **FastAPI** frameworkü oto-tamamlama açısından geliştiriciyi tatmin etmek üzerine tasarlandı. Otomatik tamamlama her yerde çalışıyor.

Dokümantasyona tekrardan çok nadir olarak geleceksin.

Editörün sana nasıl yardım ettiğine bir bak:

* <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a> ile:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> ile:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)


Daha önceden düşünüp en imkansız diyebileceğin durumlarda bile otomatik tamamlama alacaksın, örnek olarak `price` JSON body içerisinde (nested bir JSON body de olabilirdi.) direkt olarak istekten geliyor, bu durumda bile oto-tammalama sağlıyor.

Artık key isimlerini yanlış yazma, dokümantasyona dönüp deliler gibi yukarı aşağı sayfada gezmek ve en sonunda `username` mi yoksa `user_name` mi kullandım gibi sorular yok.

### Kısa

Her şey için mantıklı bir **varsayılanı** var. Parametrelerini opsiyonel olarak tanımlayıp API'nı istediğin gibi modifiye edebilirsin.

Hepsi varsayılan olarak **çalışıyor**.


### Doğrulama

* Neredeyse bütün (ya da hepsi?) Python **data typeları** için doğrulama, kapsadıkları:
    * JSON objeleri (`dict`).
    * JSON array (`list`) item type'ı belirtirken.
    * String (`str`) parametresi, minimum ve maksimum uzunluk gibi sınırlandırmalar yaparken.
    * Numaralar (`int`, `float`) maksimum ve minimum gibi sınırlandırmalar yaparken.

* Bunlar gibi en egzotik typelarla bile doğrulama yapabiliyorsunuz.:
    * URL.
    * Email.
    * UUID.
    * ...ve diğerleri.

Bütün doğrulama olayları çok güçlü bir kütüphane sayesinde yapılıyor, **Pydantic**.

### Güvenlik ve kimlik doğrulama

Güvenlik ve doğrulama database ve data modellerinden taviz vermeden entegre edilebilir durumda.

Bütün güvenlik şemaları OpenAPI'da tanımlanmış durumda, kapsadıkları:

* HTTP Basic.
* **OAuth2** (ve **JWT tokenleriyle** beraber). Bu öğretici içeriğe göz atabilirsin [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* API anahtarları:
    * Headerlar.
    * Query parametreleri.
    * Cookies, vs.

Bütün güvenlik özellikleri Starlette'den geliyor (**session cookies'de** dahil olmak üzere).

Bütün hepsi tekrardan kullanılabilir aletler ve bileşenler olarak, kolayca sistemlerinize, data depolarınıza, ilişkisel ve NoSQL databaselerinize entegre edebileceğiniz şekilde yapıldı.

### Dependency injection

FastAPI'ın inanılmaz derecede kullanımı kolay, fakat inanılmaz derecede güçlü <abbr title='"components", "resources", "services", "providers" olarak da bilinen'><strong>Dependency Injection </strong></abbr> sistemi var.

* Dependencylerin bile dependencies'i olabiliyor, FastAPI bunun  için **graph of "dependency"** yaratıyor.
* Hepsi **otomatik olarak** FastAPI tarafından hallediliyor.
* Bütün zorunlulukların gelen datalara bağlı olarak farklı gereksinimleri olabiliyor, ilave path operasyonlarının kısıtlamaları ve otomatik dokümantasyonu da ayrıca yapılıyor .
* Path operasyonu parametreleri içerisinde belirtilen gereksinimler için bile **Otomatik doğrulama** yapılabiliyor.
* Kompleks kimlik doğrulama sistemleri için destek, **database bağlantıları**, vs.
* **Taviz yok** hiçbir şeyden taviz vermeden, database frontend vs. Bütün hepsinin kolayca entegre edilebiliyor.

### Sınırsız "plug-inler"

Başka bir deyişle, plug-inlere ihtiyacımız yok, import edip direkt olarak kullanmaya başlayabiliriz.

Bütün entegrasyonlar kullanımı kolay olmak üzere (zorunluluklar ile beraber) tasarlandı, sen bir "plug-in" yaratıp 2 satır kod ile, *path operasyonlarında* kullandığımız syntax ve aynı yapı ile koduna entregre edebilirsin.


### Test edildi

* 100% <abbr title="Kodun ne kadarının test edildiği">test coverage</abbr>.
* 100% <abbr title="Python type annotations, with this your editor and external tools can give you better support">typeları belirtilmiş</abbr> codebase.
* FastAPI ile yapılan bir çok proje insanlar tarafından kullanılıyor.

## Starlette özellikleri

**FastAPI**, <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong></a> ile tamamiyle uyumlu ve üzerine kurulu. Yani FastAPI üzerine ekleme yapacağınız herhangi bir Starlette kodu da çalışacaktır.

`FastAPI` aslında `Starlette`'nin bir sub-class'ı. Eğer Starlette'nin nasıl kullanılacağını biliyor isen, çoğu işlevini aynı şekilde yapıyor.

**FastAPI** ile beraber **Starlette**'nin bütün özelliklerine de sahip olacaksınız (FastAPI aslında Starlette'nin steroid basmış hali):

* Gerçekten etkileyici bir performansa sahip.Python'un ise en hızlı frameworklerinden bir tanesi, <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">**NodeJS** ve **Go** ile ise eşdeğer performansa sahip.</a>.
* **WebSocket** desteği.
* **GraphQL** desteği.
* Kullanım halinde arka plan işlevleri.
* Başlatma ve kapatma eventleri(startup and shutdown).
* Test sunucusu HTTPX üzerine kurulu.
* **CORS**, GZip, Static dosyalar, Streaming responseları.
* **Session and Cookie** desteği.
* 100% test kapsayıcılığı.
* 100% typeları belirtilmiş codebase.

## Pydantic özellikleri

**FastAPI** ile <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a> tamamiyle uyumlu ve üzerine kurulu. Yani FastAPI üzerine ekleme yapacağınız herhangi bir Pydantic kodu da çalışacaktır.

Bunlara Pydantic üzerine kurulu <abbr title="Object-Relational Mapper">ORM</abbr> databaseler ve , <abbr title="Object-Document Mapper">ODM</abbr> kütüphaneler de dahil olmak üzere.

Bu ayrıca şu anlama da geliyor, bir çok durumda requestten gelen objeyi **direkt olarak database**'e her şeyi otomatik olarak doğrulanmış bir biçimde aktarabilirisin.

Aynı şekilde, databaseden gelen objeyi de **direkt olarak isteğe** de tamamiyle doğrulanmış bir biçimde gönderebilirsiniz.

**FastAPI** ile beraber **Pydantic**'in bütün özelliklerine sahip olacaksınız (FastAPI data kontrolünü Pydantic'in üzerine kurduğu için):

* **Kafa karıştırmaz**:
    * Farklı bir syntax öğrenmenize gerek kalmaz,
    * Eğer Python typelarını nasıl kullanacağını biliyorsan Pydantic kullanmayı da biliyorsundur.
* Kullandığın geliştirme araçları ile iyi çalışır **<abbr title="Integrated Development Environment, kod editörüne benzer">IDE</abbr>/<abbr title="Code errorlarınızı inceleyen program">linter</abbr>/brain**:
    * Pydantic'in veri yapıları aslında sadece senin tanımladığın classlar; Bu yüzden doğrulanmış dataların ile otomatik tamamlama, linting ve mypy'ı kullanarak sorunsuz bir şekilde çalışabilirsin
* **Hızlı**:
    * <a href="https://pydantic-docs.helpmanual.io/benchmarks/" class="external-link" target="_blank">Benchmarklarda</a>, Pydantic'in diğer bütün test edilmiş bütün kütüphanelerden daha hızlı.
* **En kompleks** yapıları bile doğrula:
    * Hiyerarşik Pydantic modellerinin kullanımı ile beraber, Python `typing`’s `List` and `Dict`, vs gibi şeyleri doğrula.
    * Doğrulayıcılar en kompleks data şemalarının bile temiz ve kolay bir şekilde tanımlanmasına izin veriyor, ve hepsi JSON şeması olarak dokümante ediliyor
    * Pydantic, JSON objen ne kadar derin (nested) olursa olsun doğrulamasını ve gösterimini yapıyor
* **Genişletilebilir**:
    * Pydantic özelleştirilmiş data tiplerinin tanımlanmasının yapılmasına izin veriyor ayrıca validator decoratorü ile senin doğrulamaları genişletip, kendi doğrulayıcılarını yazmana izin veriyor.
* 100% test kapsayıcılığı.
