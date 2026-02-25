# OAuth2 scope'ları { #oauth2-scopes }

OAuth2 scope'larını **FastAPI** ile doğrudan kullanabilirsiniz; sorunsuz çalışacak şekilde entegre edilmiştir.

Bu sayede OAuth2 standardını takip eden, daha ince taneli bir izin sistemini OpenAPI uygulamanıza (ve API dokümanlarınıza) entegre edebilirsiniz.

Scope'lu OAuth2; Facebook, Google, GitHub, Microsoft, X (Twitter) vb. birçok büyük kimlik doğrulama sağlayıcısının kullandığı mekanizmadır. Kullanıcı ve uygulamalara belirli izinler vermek için bunu kullanırlar.

Facebook, Google, GitHub, Microsoft, X (Twitter) ile "giriş yaptığınızda", o uygulama scope'lu OAuth2 kullanıyor demektir.

Bu bölümde, **FastAPI** uygulamanızda aynı scope'lu OAuth2 ile authentication ve authorization'ı nasıl yöneteceğinizi göreceksiniz.

/// warning | Uyarı

Bu bölüm az çok ileri seviye sayılır. Yeni başlıyorsanız atlayabilirsiniz.

OAuth2 scope'larına mutlaka ihtiyacınız yok; authentication ve authorization'ı istediğiniz şekilde ele alabilirsiniz.

Namun scope'lu OAuth2, API'nize (OpenAPI ile) ve API dokümanlarınıza güzel biçimde entegre edilebilir.

Buna rağmen, bu scope'ları (veya başka herhangi bir security/authorization gereksinimini) kodunuzda ihtiyaç duyduğunuz şekilde yine siz zorunlu kılarsınız.

Birçok durumda scope'lu OAuth2 gereğinden fazla (overkill) olabilir.

Ama ihtiyacınız olduğunu biliyorsanız ya da merak ediyorsanız okumaya devam edin.

///

## OAuth2 scope'ları ve OpenAPI { #oauth2-scopes-and-openapi }

OAuth2 spesifikasyonu, "scope"ları boşluklarla ayrılmış string'lerden oluşan bir liste olarak tanımlar.

Bu string'lerin her birinin içeriği herhangi bir formatta olabilir, ancak boşluk içermemelidir.

Bu scope'lar "izinleri" temsil eder.

OpenAPI'de (ör. API dokümanlarında) "security scheme" tanımlayabilirsiniz.

Bu security scheme'lerden biri OAuth2 kullanıyorsa, scope'ları da tanımlayıp kullanabilirsiniz.

Her bir "scope" sadece bir string'dir (boşluksuz).

Genellikle belirli güvenlik izinlerini tanımlamak için kullanılır, örneğin:

* `users:read` veya `users:write` sık görülen örneklerdir.
* `instagram_basic` Facebook / Instagram tarafından kullanılır.
* `https://www.googleapis.com/auth/drive` Google tarafından kullanılır.

/// info | Bilgi

OAuth2'de "scope", gereken belirli bir izni bildiren bir string'den ibarettir.

`:` gibi başka karakterler içermesi ya da bir URL olması önemli değildir.

Bu detaylar implementasyon'a bağlıdır.

OAuth2 için bunlar sadece string'dir.

///

## Genel görünüm { #global-view }

Önce, ana **Tutorial - User Guide** içindeki [Password (ve hashing) ile OAuth2, JWT token'lı Bearer](../../tutorial/security/oauth2-jwt.md){.internal-link target=_blank} örneklerinden, OAuth2 scope'larına geçince hangi kısımların değiştiğine hızlıca bakalım:

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,9,13,47,65,106,108:116,122:126,130:136,141,157] *}

Şimdi bu değişiklikleri adım adım inceleyelim.

## OAuth2 Security scheme { #oauth2-security-scheme }

İlk değişiklik, artık OAuth2 security scheme'ini iki adet kullanılabilir scope ile tanımlamamız: `me` ve `items`.

`scopes` parametresi; her scope'un key, açıklamasının ise value olduğu bir `dict` alır:

{* ../../docs_src/security/tutorial005_an_py310.py hl[63:66] *}

Bu scope'ları tanımladığımız için, login/authorize yaptığınızda API dokümanlarında görünecekler.

Ve hangi scope'lara erişim vermek istediğinizi seçebileceksiniz: `me` ve `items`.

Bu, Facebook/Google/GitHub vb. ile giriş yaparken izin verdiğinizde kullanılan mekanizmanın aynısıdır:

<img src="/img/tutorial/security/image11.png">

## Scope'lu JWT token { #jwt-token-with-scopes }

Şimdi token *path operation*'ını, istenen scope'ları döndürecek şekilde değiştirin.

Hâlâ aynı `OAuth2PasswordRequestForm` kullanılıyor. Bu form, request'te aldığı her scope için `str`'lerden oluşan bir `list` içeren `scopes` özelliğine sahiptir.

Ve scope'ları JWT token'ın bir parçası olarak döndürüyoruz.

/// danger | Uyarı

Basitlik için burada, gelen scope'ları doğrudan token'a ekliyoruz.

Ama uygulamanızda güvenlik açısından, yalnızca kullanıcının gerçekten sahip olabileceği scope'ları (veya sizin önceden tanımladıklarınızı) eklediğinizden emin olmalısınız.

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[157] *}

## *Path operation*'larda ve dependency'lerde scope tanımlama { #declare-scopes-in-path-operations-and-dependencies }

Artık `/users/me/items/` için olan *path operation*'ın `items` scope'unu gerektirdiğini tanımlıyoruz.

Bunun için `fastapi` içinden `Security` import edip kullanıyoruz.

Dependency'leri (`Depends` gibi) tanımlamak için `Security` kullanabilirsiniz; fakat `Security`, ayrıca string'lerden oluşan bir scope listesi alan `scopes` parametresini de alır.

Bu durumda `Security`'ye dependency fonksiyonu olarak `get_current_active_user` veriyoruz (`Depends` ile yaptığımız gibi).

Ama ayrıca bir `list` olarak scope'ları da veriyoruz; burada tek bir scope var: `items` (daha fazla da olabilir).

Ve `get_current_active_user` dependency fonksiyonu, sadece `Depends` ile değil `Security` ile de alt-dependency'ler tanımlayabilir. Kendi alt-dependency fonksiyonunu (`get_current_user`) ve daha fazla scope gereksinimini tanımlar.

Bu örnekte `me` scope'unu gerektiriyor (birden fazla scope da isteyebilirdi).

/// note | Not

Farklı yerlerde farklı scope'lar eklemek zorunda değilsiniz.

Burada, **FastAPI**'nin farklı seviyelerde tanımlanan scope'ları nasıl ele aldığını göstermek için böyle yapıyoruz.

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,141,172] *}

/// info | Teknik Detaylar

`Security` aslında `Depends`'in bir alt sınıfıdır ve sadece birazdan göreceğimiz bir ek parametreye sahiptir.

Ancak `Depends` yerine `Security` kullanınca **FastAPI**, security scope'larının tanımlanabileceğini bilir, bunları içeride kullanır ve API'yi OpenAPI ile dokümante eder.

Fakat `fastapi` içinden `Query`, `Path`, `Depends`, `Security` vb. import ettiğiniz şeyler, aslında özel sınıflar döndüren fonksiyonlardır.

///

## `SecurityScopes` kullanımı { #use-securityscopes }

Şimdi `get_current_user` dependency'sini güncelleyelim.

Bu fonksiyon, yukarıdaki dependency'ler tarafından kullanılıyor.

Burada, daha önce oluşturduğumuz aynı OAuth2 scheme'i dependency olarak tanımlıyoruz: `oauth2_scheme`.

Bu dependency fonksiyonunun kendi içinde bir scope gereksinimi olmadığı için, `oauth2_scheme` ile `Depends` kullanabiliriz; security scope'larını belirtmemiz gerekmiyorsa `Security` kullanmak zorunda değiliz.

Ayrıca `fastapi.security` içinden import edilen, `SecurityScopes` tipinde özel bir parametre tanımlıyoruz.

Bu `SecurityScopes` sınıfı, `Request`'e benzer (`Request`, request nesnesini doğrudan almak için kullanılmıştı).

{* ../../docs_src/security/tutorial005_an_py310.py hl[9,106] *}

## `scopes`'ları kullanma { #use-the-scopes }

`security_scopes` parametresi `SecurityScopes` tipinde olacaktır.

Bu nesnenin `scopes` adlı bir özelliği vardır; bu liste, kendisinin ve bunu alt-dependency olarak kullanan tüm dependency'lerin gerektirdiği tüm scope'ları içerir. Yani tüm "dependant"lar... kafa karıştırıcı gelebilir; aşağıda tekrar açıklanıyor.

`security_scopes` nesnesi (`SecurityScopes` sınıfından) ayrıca, bu scope'ları boşluklarla ayrılmış tek bir string olarak veren `scope_str` attribute'una sahiptir (bunu kullanacağız).

Sonrasında birkaç farklı noktada tekrar kullanabileceğimiz (`raise` edebileceğimiz) bir `HTTPException` oluşturuyoruz.

Bu exception içinde, gerekiyorsa, gerekli scope'ları boşlukla ayrılmış bir string olarak (`scope_str` ile) ekliyoruz. Bu scope'ları içeren string'i `WWW-Authenticate` header'ına koyuyoruz (spesifikasyonun bir parçası).

{* ../../docs_src/security/tutorial005_an_py310.py hl[106,108:116] *}

## `username` ve veri şeklinin doğrulanması { #verify-the-username-and-data-shape }

Bir `username` aldığımızı doğruluyoruz ve scope'ları çıkarıyoruz.

Ardından bu veriyi Pydantic model'i ile doğruluyoruz (`ValidationError` exception'ını yakalayarak). JWT token'ı okurken veya Pydantic ile veriyi doğrularken bir hata olursa, daha önce oluşturduğumuz `HTTPException`'ı fırlatıyoruz.

Bunun için Pydantic model'i `TokenData`'yı, `scopes` adlı yeni bir özellik ekleyerek güncelliyoruz.

Veriyi Pydantic ile doğrulayarak örneğin scope'ların tam olarak `str`'lerden oluşan bir `list` olduğunu ve `username`'in bir `str` olduğunu garanti edebiliriz.

Aksi halde, örneğin bir `dict` veya başka bir şey gelebilir; bu da daha sonra uygulamanın bir yerinde kırılmaya yol açıp güvenlik riski oluşturabilir.

Ayrıca bu `username` ile bir kullanıcı olduğunu doğruluyoruz; yoksa yine aynı exception'ı fırlatıyoruz.

{* ../../docs_src/security/tutorial005_an_py310.py hl[47,117:129] *}

## `scopes`'ların doğrulanması { #verify-the-scopes }

Şimdi bu dependency'nin ve tüm dependant'ların ( *path operation*'lar dahil) gerektirdiği tüm scope'ların, alınan token'da sağlanan scope'lar içinde olup olmadığını doğruluyoruz; değilse `HTTPException` fırlatıyoruz.

Bunun için, tüm bu scope'ları `str` olarak içeren bir `list` olan `security_scopes.scopes` kullanılır.

{* ../../docs_src/security/tutorial005_an_py310.py hl[130:136] *}

## Dependency ağacı ve scope'lar { #dependency-tree-and-scopes }

Bu dependency ağacını ve scope'ları tekrar gözden geçirelim.

`get_current_active_user` dependency'si, alt-dependency olarak `get_current_user`'ı kullandığı için, `get_current_active_user` üzerinde tanımlanan `"me"` scope'u, `get_current_user`'a geçirilen `security_scopes.scopes` içindeki gerekli scope listesine dahil edilir.

*Path operation*'ın kendisi de `"items"` scope'unu tanımlar; bu da `get_current_user`'a geçirilen `security_scopes.scopes` listesinde yer alır.

Dependency'lerin ve scope'ların hiyerarşisi şöyle görünür:

* *Path operation* `read_own_items` şunlara sahiptir:
    * Dependency ile gerekli scope'lar `["items"]`:
    * `get_current_active_user`:
        * `get_current_active_user` dependency fonksiyonu şunlara sahiptir:
            * Dependency ile gerekli scope'lar `["me"]`:
            * `get_current_user`:
                * `get_current_user` dependency fonksiyonu şunlara sahiptir:
                    * Kendisinin gerektirdiği scope yok.
                    * `oauth2_scheme` kullanan bir dependency.
                    * `SecurityScopes` tipinde bir `security_scopes` parametresi:
                        * Bu `security_scopes` parametresinin `scopes` adlı bir özelliği vardır ve yukarıda tanımlanan tüm scope'ları içeren bir `list` taşır, yani:
                            * *Path operation* `read_own_items` için `security_scopes.scopes` `["me", "items"]` içerir.
                            * *Path operation* `read_users_me` için `security_scopes.scopes` `["me"]` içerir; çünkü bu scope `get_current_active_user` dependency'sinde tanımlanmıştır.
                            * *Path operation* `read_system_status` için `security_scopes.scopes` `[]` (boş) olur; çünkü herhangi bir `Security` ile `scopes` tanımlamamıştır ve dependency'si olan `get_current_user` da `scopes` tanımlamaz.

/// tip | İpucu

Buradaki önemli ve "sihirli" nokta şu: `get_current_user`, her *path operation* için kontrol etmesi gereken farklı bir `scopes` listesi alır.

Bu, belirli bir *path operation* için dependency ağacındaki her *path operation* ve her dependency üzerinde tanımlanan `scopes`'lara bağlıdır.

///

## `SecurityScopes` hakkında daha fazla detay { #more-details-about-securityscopes }

`SecurityScopes`'u herhangi bir noktada ve birden fazla yerde kullanabilirsiniz; mutlaka "kök" dependency'de olmak zorunda değildir.

Her zaman, **o spesifik** *path operation* ve **o spesifik** dependency ağacı için, mevcut `Security` dependency'lerinde ve tüm dependant'larda tanımlanan security scope'larını içerir.

`SecurityScopes`, dependant'ların tanımladığı tüm scope'ları barındırdığı için, gereken scope'ların token'da olup olmadığını merkezi bir dependency fonksiyonunda doğrulayıp, farklı *path operation*'larda farklı scope gereksinimleri tanımlayabilirsiniz.

Bu kontroller her *path operation* için bağımsız yapılır.

## Deneyin { #check-it }

API dokümanlarını açarsanız, authenticate olup hangi scope'ları authorize etmek istediğinizi seçebilirsiniz.

<img src="/img/tutorial/security/image11.png">

Hiç scope seçmezseniz "authenticated" olursunuz; ancak `/users/me/` veya `/users/me/items/`'e erişmeye çalıştığınızda, yeterli izniniz olmadığını söyleyen bir hata alırsınız. Yine de `/status/`'a erişebilirsiniz.

`me` scope'unu seçip `items` scope'unu seçmezseniz `/users/me/`'a erişebilirsiniz ama `/users/me/items/`'e erişemezsiniz.

Bu, bir üçüncü taraf uygulamanın, bir kullanıcı tarafından sağlanan token ile bu *path operation*'lardan birine erişmeye çalıştığında; kullanıcının uygulamaya kaç izin verdiğine bağlı olarak yaşayacağı durumdur.

## Üçüncü taraf entegrasyonları hakkında { #about-third-party-integrations }

Bu örnekte OAuth2 "password" flow'unu kullanıyoruz.

Bu, kendi uygulamamıza giriş yaptığımız durumlar için uygundur; muhtemelen kendi frontend'imiz vardır.

Çünkü `username` ve `password` alacağını bildiğimiz frontend'i biz kontrol ediyoruz, dolayısıyla güvenebiliriz.

Ancak başkalarının bağlanacağı bir OAuth2 uygulaması geliştiriyorsanız (yani Facebook, Google, GitHub vb. gibi bir authentication provider muadili geliştiriyorsanız) diğer flow'lardan birini kullanmalısınız.

En yaygını implicit flow'dur.

En güvenlisi code flow'dur; ancak daha fazla adım gerektirdiği için implementasyonu daha karmaşıktır. Daha karmaşıktır olduğundan, birçok sağlayıcı implicit flow'yu önermeye yönelir.

/// note | Not

Her authentication provider'ın flow'ları markasının bir parçası yapmak için farklı şekilde adlandırması yaygındır.

Ama sonuçta aynı OAuth2 standardını implement ediyorlar.

///

**FastAPI**, bu OAuth2 authentication flow'larının tamamı için `fastapi.security.oauth2` içinde yardımcı araçlar sunar.

## Decorator `dependencies` içinde `Security` { #security-in-decorator-dependencies }

Decorator'ın `dependencies` parametresinde bir `list` `Depends` tanımlayabildiğiniz gibi ( [Path operation decorator'larında Dependencies](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank} bölümünde açıklandığı üzere), burada `scopes` ile birlikte `Security` de kullanabilirsiniz.
