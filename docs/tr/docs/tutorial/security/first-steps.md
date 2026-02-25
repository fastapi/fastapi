# Güvenlik - İlk Adımlar { #security-first-steps }

**backend** API’nizin bir domain’de olduğunu düşünelim.

Ve başka bir domain’de ya da aynı domain’in farklı bir path’inde (veya bir mobil uygulamada) bir **frontend**’iniz var.

Ve frontend’in, **username** ve **password** kullanarak backend ile kimlik doğrulaması yapabilmesini istiyorsunuz.

Bunu **FastAPI** ile **OAuth2** kullanarak oluşturabiliriz.

Ama ihtiyacınız olan küçük bilgi parçalarını bulmak için uzun spesifikasyonun tamamını okuma zahmetine girmeyelim.

Güvenliği yönetmek için **FastAPI**’nin sunduğu araçları kullanalım.

## Nasıl Görünüyor { #how-it-looks }

Önce kodu kullanıp nasıl çalıştığına bakalım, sonra neler olup bittiğini anlamak için geri döneriz.

## `main.py` Oluşturun { #create-main-py }

Örneği `main.py` adlı bir dosyaya kopyalayın:

{* ../../docs_src/security/tutorial001_an_py310.py *}

## Çalıştırın { #run-it }

/// info | Bilgi

<a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> paketi, `pip install "fastapi[standard]"` komutunu çalıştırdığınızda **FastAPI** ile birlikte otomatik olarak kurulur.

Ancak `pip install fastapi` komutunu kullanırsanız, `python-multipart` paketi varsayılan olarak dahil edilmez.

Elle kurmak için bir [virtual environment](../../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan, onu aktive ettiğinizden emin olun ve ardından şununla kurun:

```console
$ pip install python-multipart
```

Bunun nedeni, **OAuth2**’nin `username` ve `password` göndermek için "form data" kullanmasıdır.

///

Örneği şu şekilde çalıştırın:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## Kontrol Edin { #check-it }

Etkileşimli dokümantasyona gidin: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Şuna benzer bir şey göreceksiniz:

<img src="/img/tutorial/security/image01.png">

/// check | Authorize butonu!

Artık parıl parıl yeni bir "Authorize" butonunuz var.

Ayrıca *path operation*’ınızın sağ üst köşesinde tıklayabileceğiniz küçük bir kilit simgesi de bulunuyor.

///

Ve ona tıklarsanız, `username` ve `password` (ve diğer opsiyonel alanları) girebileceğiniz küçük bir yetkilendirme formu görürsünüz:

<img src="/img/tutorial/security/image02.png">

/// note | Not

Formda ne yazdığınızın önemi yok; şimdilik çalışmayacak. Ama birazdan oraya da geleceğiz.

///

Bu, elbette son kullanıcılar için bir frontend değil; ancak tüm API’nizi etkileşimli şekilde belgelemek için harika bir otomatik araçtır.

Frontend ekibi tarafından kullanılabilir (bu ekip siz de olabilirsiniz).

Üçüncü taraf uygulamalar ve sistemler tarafından kullanılabilir.

Ve aynı uygulamayı debug etmek, kontrol etmek ve test etmek için sizin tarafınızdan da kullanılabilir.

## `password` Flow { #the-password-flow }

Şimdi biraz geri dönüp bunların ne olduğuna bakalım.

`password` "flow"u, OAuth2’de güvenlik ve authentication’ı yönetmek için tanımlanmış yöntemlerden ("flow"lardan) biridir.

OAuth2, backend’in veya API’nin, kullanıcıyı authenticate eden server’dan bağımsız olabilmesi için tasarlanmıştır.

Ancak bu örnekte, aynı **FastAPI** uygulaması hem API’yi hem de authentication’ı yönetecek.

O yüzden basitleştirilmiş bu bakış açısından üzerinden geçelim:

* Kullanıcı frontend’de `username` ve `password` yazar ve `Enter`’a basar.
* Frontend (kullanıcının browser’ında çalışır), bu `username` ve `password` değerlerini API’mizdeki belirli bir URL’ye gönderir (`tokenUrl="token"` ile tanımlanan).
* API, `username` ve `password` değerlerini kontrol eder ve bir "token" ile response döner (henüz bunların hiçbirini implement etmedik).
    * "Token", daha sonra bu kullanıcıyı doğrulamak için kullanabileceğimiz içerik taşıyan bir string’dir.
    * Normalde token’ın bir süre sonra süresi dolacak şekilde ayarlanması beklenir.
        * Böylece kullanıcının bir noktada tekrar giriş yapması gerekir.
        * Ayrıca token çalınırsa risk daha düşük olur. Çoğu durumda, sonsuza kadar çalışacak kalıcı bir anahtar gibi değildir.
* Frontend bu token’ı geçici olarak bir yerde saklar.
* Kullanıcı frontend’de tıklayarak web uygulamasının başka bir bölümüne gider.
* Frontend’in API’den daha fazla veri alması gerekir.
    * Ancak o endpoint için authentication gereklidir.
    * Bu yüzden API’mizle authenticate olmak için `Authorization` header’ını, `Bearer ` + token değeriyle gönderir.
    * Token `foobar` içeriyorsa `Authorization` header’ının içeriği `Bearer foobar` olur.

## **FastAPI**’nin `OAuth2PasswordBearer`’ı { #fastapis-oauth2passwordbearer }

**FastAPI**, bu güvenlik özelliklerini implement etmek için farklı soyutlama seviyelerinde çeşitli araçlar sağlar.

Bu örnekte **OAuth2**’yi, **Password** flow ile, **Bearer** token kullanarak uygulayacağız. Bunu `OAuth2PasswordBearer` sınıfı ile yaparız.

/// info | Bilgi

"Bearer" token tek seçenek değildir.

Ama bizim kullanım senaryomuz için en iyi seçenek odur.

Ayrıca bir OAuth2 uzmanı değilseniz ve ihtiyaçlarınıza daha uygun başka bir seçeneğin neden gerekli olduğunu net olarak bilmiyorsanız, çoğu kullanım senaryosu için de en uygun seçenek olacaktır.

Bu durumda bile **FastAPI**, onu oluşturabilmeniz için gereken araçları sunar.

///

`OAuth2PasswordBearer` sınıfının bir instance’ını oluştururken `tokenUrl` parametresini veririz. Bu parametre, client’ın (kullanıcının browser’ında çalışan frontend’in) token almak için `username` ve `password` göndereceği URL’yi içerir.

{* ../../docs_src/security/tutorial001_an_py310.py hl[8] *}

/// tip | İpucu

Burada `tokenUrl="token"`, henüz oluşturmadığımız göreli bir URL olan `token`’ı ifade eder. Göreli URL olduğu için `./token` ile eşdeğerdir.

Göreli URL kullandığımız için, API’niz `https://example.com/` adresinde olsaydı `https://example.com/token` anlamına gelirdi. Ama API’niz `https://example.com/api/v1/` adresinde olsaydı, bu kez `https://example.com/api/v1/token` anlamına gelirdi.

Göreli URL kullanmak, [Behind a Proxy](../../advanced/behind-a-proxy.md){.internal-link target=_blank} gibi daha ileri kullanım senaryolarında bile uygulamanızın çalışmaya devam etmesini garanti etmek açısından önemlidir.

///

Bu parametre o endpoint’i / *path operation*’ı oluşturmaz; fakat `/token` URL’sinin client’ın token almak için kullanması gereken URL olduğunu bildirir. Bu bilgi OpenAPI’de, dolayısıyla etkileşimli API dokümantasyon sistemlerinde kullanılır.

Birazdan gerçek path operation’ı da oluşturacağız.

/// info | Teknik Detaylar

Eğer çok katı bir "Pythonista" iseniz, `token_url` yerine `tokenUrl` şeklindeki parametre adlandırma stilini sevmeyebilirsiniz.

Bunun nedeni, OpenAPI spesifikasyonundaki isimle aynı adın kullanılmasıdır. Böylece bu güvenlik şemalarından herhangi biri hakkında daha fazla araştırma yapmanız gerekirse, adı kopyalayıp yapıştırarak kolayca daha fazla bilgi bulabilirsiniz.

///

`oauth2_scheme` değişkeni, `OAuth2PasswordBearer`’ın bir instance’ıdır; ama aynı zamanda "callable"dır.

Şu şekilde çağrılabilir:

```Python
oauth2_scheme(some, parameters)
```

Dolayısıyla `Depends` ile kullanılabilir.

### Kullanın { #use-it }

Artık `Depends` ile bir dependency olarak `oauth2_scheme`’i geçebilirsiniz.

{* ../../docs_src/security/tutorial001_an_py310.py hl[12] *}

Bu dependency, *path operation function* içindeki `token` parametresine atanacak bir `str` sağlar.

**FastAPI**, bu dependency’yi OpenAPI şemasında (ve otomatik API dokümanlarında) bir "security scheme" tanımlamak için kullanabileceğini bilir.

/// info | Teknik Detaylar

**FastAPI**, bir dependency içinde tanımlanan `OAuth2PasswordBearer` sınıfını OpenAPI’de security scheme tanımlamak için kullanabileceğini bilir; çünkü bu sınıf `fastapi.security.oauth2.OAuth2`’den kalıtım alır, o da `fastapi.security.base.SecurityBase`’den kalıtım alır.

OpenAPI (ve otomatik API dokümanları) ile entegre olan tüm security araçları `SecurityBase`’den kalıtım alır; **FastAPI** bu sayede onları OpenAPI’ye nasıl entegre edeceğini anlayabilir.

///

## Ne Yapar { #what-it-does }

Request içinde `Authorization` header’ını arar, değerin `Bearer ` + bir token olup olmadığını kontrol eder ve token’ı `str` olarak döndürür.

Eğer `Authorization` header’ını görmezse ya da değer `Bearer ` token’ı içermiyorsa, doğrudan 401 status code hatasıyla (`UNAUTHORIZED`) response döner.

Token’ın var olup olmadığını kontrol edip ayrıca hata döndürmenize bile gerek yoktur. Fonksiyonunuz çalışıyorsa, token içinde bir `str` olacağından emin olabilirsiniz.

Bunu şimdiden etkileşimli dokümanlarda deneyebilirsiniz:

<img src="/img/tutorial/security/image03.png">

Henüz token’ın geçerliliğini doğrulamıyoruz, ama başlangıç için bu bile yeterli.

## Özet { #recap }

Yani sadece 3 veya 4 ekstra satırla, şimdiden ilkel de olsa bir güvenlik katmanı elde etmiş oldunuz.
