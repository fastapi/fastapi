# Özellikler { #features }

## FastAPI Özellikleri { #fastapi-features }

**FastAPI** size şunları sağlar:

### Açık Standartlara Dayalı { #based-on-open-standards }

* API oluşturmada <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a>, buna <dfn title="şöyle de bilinir: endpoints, routes">path</dfn> <dfn title="HTTP metodları olarak da bilinir; POST, GET, PUT, DELETE gibi">operasyonları</dfn>, parametreler, request body'leri, güvenlik vb. deklarasyonları dahildir.
* <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> ile otomatik veri modeli dokümantasyonu (OpenAPI zaten JSON Schema'ya dayanır).
* Bu standartlar etrafında, titiz bir çalışmanın ardından tasarlandı; sonradan eklenmiş bir katman değil.
* Bu sayede birçok dilde otomatik **client code generation** da kullanılabilir.

### Otomatik Dokümantasyon { #automatic-docs }

Etkileşimli API dokümantasyonu ve keşif için web arayüzleri. Framework OpenAPI’ye dayandığından, birden fazla seçenek vardır; varsayılan olarak 2’si dahildir.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a> ile etkileşimli keşif; API’nizi tarayıcıdan doğrudan çağırıp test edin.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a> ile alternatif API dokümantasyonu.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Sadece Modern Python { #just-modern-python }

Her şey standart **Python type** deklarasyonlarına dayanır (Pydantic sayesinde). Öğrenilecek yeni bir söz dizimi yok. Sadece standart, modern Python.

Python type’larını nasıl kullanacağınıza dair 2 dakikalık bir hatırlatmaya ihtiyacınız varsa (FastAPI kullanmasanız bile) kısa eğitime göz atın: [Python Types](python-types.md){.internal-link target=_blank}.

Türleriyle standart Python yazarsınız:

```Python
from datetime import date

from pydantic import BaseModel

# Bir değişkeni str olarak belirt
# ve fonksiyon içinde editör desteği al
def main(user_id: str):
    return user_id


# Bir Pydantic modeli
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Sonra şöyle kullanabilirsiniz:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```


/// info

`**second_user_data` şu anlama gelir:

`second_user_data` dict’indeki anahtar ve değerleri doğrudan anahtar-değer argümanları olarak geç; şu ifadeye eşdeğerdir: `User(id=4, name="Mary", joined="2018-11-30")`

///

### Editör Desteği { #editor-support }

Tüm framework, kullanımı kolay ve sezgisel olacak şekilde tasarlandı; en iyi geliştirme deneyimini sağlamak için geliştirmeye başlamadan önce bile alınan kararlar birden çok editörde test edildi.

Python geliştirici anketlerinde açıkça görülüyor ki <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">en çok kullanılan özelliklerden biri "otomatik tamamlama"</a>.

Tüm **FastAPI** bunun tatmin edilmesi üzerine kuruldu. Otomatik tamamlama her yerde çalışır.

Dokümana geri dönmeniz nadiren gerekecek.

Editörünüz şöyle yardımcı olabilir:

* <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a> ile:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> ile:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Daha önce imkânsız olduğunu düşünebileceğiniz yerlerde bile tamamlama alırsınız. Örneğin, bir request’ten gelen (iç içe de olabilir) JSON body içindeki `price` anahtarı için.

Artık anahtar adlarını yanlış yazmak, dokümana gidip gelmek ya da sonunda `username` mi `user_name` mi kullandığınızı bulmak için sayfayı yukarı aşağı kaydırmak yok.

### Kısa { #short }

Her şey için mantıklı **varsayılanlar** ve her yerde isteğe bağlı yapılandırmalar vardır. Tüm parametreler, ihtiyacınızı karşılayacak şekilde ince ayar yapılarak tanımlamak istediğiniz API’yi oluşturabilir.

Ancak varsayılan hâliyle hepsi **“hemen çalışır”**.

### Doğrulama { #validation }

* Çoğu (veya hepsi?) Python **veri tipi** için doğrulama, şunlar dâhil:
    * JSON nesneleri (`dict`).
    * Eleman tipleri tanımlanan JSON dizileri (`list`).
    * Minimum ve maksimum uzunlukları tanımlanan String (`str`) alanları.
    * Min ve max değerleri olan sayılar (`int`, `float`) vb.

* Daha “egzotik” tipler için doğrulama:
    * URL.
    * Email.
    * UUID.
    * ...ve diğerleri.

Tüm doğrulama köklü ve sağlam **Pydantic** tarafından yapılır.

### Güvenlik ve Kimlik Doğrulama { #security-and-authentication }

Güvenlik ve kimlik doğrulama entegredir. Veritabanları veya veri modelleriyle ilgili hiçbir taviz yoktur.

OpenAPI’da tanımlanan tüm güvenlik şemaları, şunlar dâhil:

* HTTP Basic.
* **OAuth2** (ayrıca **JWT token**’larla). Şu eğitime göz atın: [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* API anahtarları:
    * Header’larda.
    * Query parametrelerinde.
    * Cookie’lerde vb.

Buna ek olarak Starlette’in tüm güvenlik özellikleri (**session cookies** dâhil).

Tümü, sistemleriniz, veri depolarınız, ilişkisel ve NoSQL veritabanlarınız vb. ile kolayca entegre edilebilen, yeniden kullanılabilir araçlar ve bileşenler olarak inşa edilmiştir.

### Dependency Injection { #dependency-injection }

FastAPI, son derece kolay kullanımlı ama son derece güçlü bir <dfn title='şöyle de bilinir: "components", "resources", "services", "providers"'><strong>Dependency Injection</strong></dfn> sistemine sahiptir.

* Bağımlılıkların da kendi bağımlılıkları olabilir; böylece bir hiyerarşi veya **bağımlılıklar "grafı"** oluşur.
* Tüm süreç framework tarafından **otomatik olarak yönetilir**.
* Tüm bağımlılıklar, request’lerden veri talep edebilir ve *path operation* kısıtlarını ve otomatik dokümantasyonu **zenginleştirebilir**.
* Bağımlılıklarda tanımlanan *path operation* parametreleri için bile **otomatik doğrulama**.
* Karmaşık kullanıcı kimlik doğrulama sistemleri, **veritabanı bağlantıları** vb. için destek.
* Veritabanları, frontend’ler vb. ile **taviz yok**; ancak hepsiyle kolay entegrasyon.

### Sınırsız "Plug-in" { #unlimited-plug-ins }

Başka bir deyişle, onlara gerek yok; ihtiyaç duyduğunuz kodu import edin ve kullanın.

Her entegrasyon (bağımlılıklar ile) o kadar basit olacak şekilde tasarlanmıştır ki, uygulamanız için, *path operations* ile kullandığınız aynı yapı ve söz dizimiyle sadece 2 satırda bir “plug-in” yazabilirsiniz.

### Test Edildi { #tested }

* %100 <dfn title="Otomatik olarak test edilen kod miktarı">test kapsayıcılığı</dfn>.
* %100 <dfn title="Python type annotations; bununla editörünüz ve harici araçlar size daha iyi destek verebilir">type annotated</dfn> kod tabanı.
* Üretimde kullanılan uygulamalarda kullanılıyor.

## Starlette Özellikleri { #starlette-features }

**FastAPI**, <a href="https://www.starlette.dev/" class="external-link" target="_blank"><strong>Starlette</strong></a> ile tamamen uyumludur (ve onun üzerine kuruludur). Dolayısıyla elinizdeki ek Starlette kodları da çalışır.

`FastAPI` aslında `Starlette`’in bir alt sınıfıdır. Starlette’i zaten biliyor veya kullanıyorsanız, işlevlerin çoğu aynı şekilde çalışır.

**FastAPI** ile **Starlette**’in tüm özelliklerini elde edersiniz (FastAPI, steroid basılmış Starlette gibidir):

* Cidden etkileyici performans. <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">Mevcut en hızlı Python frameworklerinden biridir; **NodeJS** ve **Go** ile aynı seviyededir</a>.
* **WebSocket** desteği.
* Süreç içi arka plan görevleri.
* Başlatma ve kapatma olayları.
* HTTPX üzerine kurulu test istemcisi.
* **CORS**, GZip, Static Files, Streaming response’lar.
* **Session** ve **Cookie** desteği.
* %100 test kapsayıcılığı.
* %100 type annotated kod tabanı.

## Pydantic Özellikleri { #pydantic-features }

**FastAPI**, <a href="https://docs.pydantic.dev/" class="external-link" target="_blank"><strong>Pydantic</strong></a> ile tamamen uyumludur (ve onun üzerine kuruludur). Dolayısıyla elinizdeki ek Pydantic kodları da çalışır.

Pydantic’e dayanan harici kütüphaneler de dâhildir; veritabanları için <abbr title="Object-Relational Mapper - Nesne-İlişkisel Eşleyici">ORM</abbr>’ler, <abbr title="Object-Document Mapper - Nesne-Belge Eşleyici">ODM</abbr>’ler gibi.

Bu aynı zamanda, birçok durumda request’ten aldığınız nesneyi **doğrudan veritabanına** iletebileceğiniz anlamına gelir; zira her şey otomatik olarak doğrulanır.

Tersi yönde de geçerlidir; birçok durumda veritabanından aldığınız nesneyi **doğrudan client**’a gönderebilirsiniz.

**FastAPI** ile **Pydantic**’in tüm özelliklerini elde edersiniz (FastAPI, tüm veri işlemede Pydantic’e dayanır):

* **Kafa karıştırmaz**:
    * Öğrenmeniz gereken yeni bir şema tanımlama mikro-dili yok.
    * Python type’larını biliyorsanız Pydantic’i nasıl kullanacağınızı da biliyorsunuz.
* **<abbr title="Integrated Development Environment - Tümleşik Geliştirme Ortamı: bir kod editörüne benzer">IDE</abbr>/<dfn title="koddaki hataları denetleyen bir program">linter</dfn>/beyin**’inizle iyi anlaşır:
    * Pydantic veri yapıları, sizin tanımladığınız sınıfların örnekleridir; bu nedenle doğrulanmış verilerinizle otomatik tamamlama, linting ve mypy sorunsuz çalışır, sezgileriniz de yol gösterir.
* **Karmaşık yapıları** doğrulayın:
    * Hiyerarşik Pydantic modelleri, Python `typing`’in `List` ve `Dict`’i vb. kullanımı.
    * Doğrulayıcılar (validators), karmaşık veri şemalarının net ve kolay şekilde tanımlanmasını, kontrol edilmesini ve JSON Schema olarak dokümante edilmesini sağlar.
    * Derinlemesine iç içe **JSON** nesnelerine sahip olabilir, hepsinin doğrulanmasını ve anotasyonlanmasını sağlayabilirsiniz.
* **Genişletilebilir**:
    * Pydantic, özel veri tiplerinin tanımlanmasına izin verir; ayrıca validator decorator’üyle bir modeldeki metodlarla doğrulamayı genişletebilirsiniz.
* %100 test kapsayıcılığı.
