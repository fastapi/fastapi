# HTTP Basic Auth { #http-basic-auth }

En basit senaryolarda HTTP Basic Auth kullanabilirsiniz.

HTTP Basic Auth’ta uygulama, içinde kullanıcı adı ve şifre bulunan bir header bekler.

Eğer bunu almazsa HTTP 401 "Unauthorized" hatası döndürür.

Ayrıca değeri `Basic` olan ve isteğe bağlı `realm` parametresi içerebilen `WWW-Authenticate` header’ını da döndürür.

Bu da tarayıcıya, kullanıcı adı ve şifre için entegre giriş penceresini göstermesini söyler.

Ardından kullanıcı adı ve şifreyi yazdığınızda tarayıcı bunları otomatik olarak header içinde gönderir.

## Basit HTTP Basic Auth { #simple-http-basic-auth }

* `HTTPBasic` ve `HTTPBasicCredentials` import edin.
* `HTTPBasic` kullanarak bir "`security` scheme" oluşturun.
* *path operation*’ınızda bir dependency ile bu `security`’yi kullanın.
* Bu, `HTTPBasicCredentials` tipinde bir nesne döndürür:
    * İçinde gönderilen `username` ve `password` bulunur.

{* ../../docs_src/security/tutorial006_an_py310.py hl[4,8,12] *}

URL’yi ilk kez açmaya çalıştığınızda (veya dokümanlardaki "Execute" butonuna tıkladığınızda) tarayıcı sizden kullanıcı adınızı ve şifrenizi ister:

<img src="/img/tutorial/security/image12.png">

## Kullanıcı adını kontrol edin { #check-the-username }

Daha kapsamlı bir örneğe bakalım.

Kullanıcı adı ve şifrenin doğru olup olmadığını kontrol etmek için bir dependency kullanın.

Bunun için kullanıcı adı ve şifreyi kontrol ederken Python standart modülü olan <a href="https://docs.python.org/3/library/secrets.html" class="external-link" target="_blank">`secrets`</a>’i kullanın.

`secrets.compare_digest()`; `bytes` ya da yalnızca ASCII karakterleri (İngilizce’deki karakterler) içeren bir `str` almalıdır. Bu da `Sebastián` içindeki `á` gibi karakterlerle çalışmayacağı anlamına gelir.

Bunu yönetmek için önce `username` ve `password` değerlerini UTF-8 ile encode ederek `bytes`’a dönüştürürüz.

Sonra `secrets.compare_digest()` kullanarak `credentials.username`’in `"stanleyjobson"` ve `credentials.password`’ün `"swordfish"` olduğundan emin olabiliriz.

{* ../../docs_src/security/tutorial007_an_py310.py hl[1,12:24] *}

Bu, kabaca şuna benzer olurdu:

```Python
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # Bir hata döndür
    ...
```

Ancak `secrets.compare_digest()` kullanarak, "timing attacks" denilen bir saldırı türüne karşı güvenli olursunuz.

### Timing Attacks { #timing-attacks }

Peki "timing attack" nedir?

Bazı saldırganların kullanıcı adı ve şifreyi tahmin etmeye çalıştığını düşünelim.

Ve `johndoe` kullanıcı adı ve `love123` şifresi ile bir request gönderiyorlar.

Uygulamanızdaki Python kodu o zaman kabaca şuna denk olur:

```Python
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Ancak Python, `johndoe` içindeki ilk `j` ile `stanleyjobson` içindeki ilk `s`’i karşılaştırdığı anda `False` döndürür; çünkü iki string’in aynı olmadığını zaten anlar ve "kalan harfleri karşılaştırmak için daha fazla hesaplama yapmaya gerek yok" diye düşünür. Uygulamanız da "Incorrect username or password" der.

Sonra saldırganlar bu sefer `stanleyjobsox` kullanıcı adı ve `love123` şifresi ile dener.

Uygulama kodunuz da şuna benzer bir şey yapar:

```Python
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Bu kez Python, iki string’in aynı olmadığını fark etmeden önce hem `stanleyjobsox` hem de `stanleyjobson` içinde `stanleyjobso` kısmının tamamını karşılaştırmak zorunda kalır. Bu nedenle "Incorrect username or password" yanıtını vermesi birkaç mikro saniye daha uzun sürer.

#### Yanıt süresi saldırganlara yardımcı olur { #the-time-to-answer-helps-the-attackers }

Bu noktada saldırganlar, server’ın "Incorrect username or password" response’unu göndermesinin birkaç mikro saniye daha uzun sürdüğünü fark ederek _bir şeyleri_ doğru yaptıklarını anlar; yani başlangıçtaki bazı harfler doğrudur.

Sonra tekrar denerken, bunun `johndoe`’dan ziyade `stanleyjobsox`’a daha yakın bir şey olması gerektiğini bilerek devam edebilirler.

#### "Profesyonel" bir saldırı { #a-professional-attack }

Elbette saldırganlar bunu elle tek tek denemez; bunu yapan bir program yazarlar. Muhtemelen saniyede binlerce ya da milyonlarca test yaparlar ve her seferinde yalnızca bir doğru harf daha elde ederler.

Böylece birkaç dakika ya da birkaç saat içinde doğru kullanıcı adı ve şifreyi, yanıt süresini kullanarak ve uygulamamızın "yardımıyla" tahmin etmiş olurlar.

#### `secrets.compare_digest()` ile düzeltin { #fix-it-with-secrets-compare-digest }

Ancak bizim kodumuzda `secrets.compare_digest()` kullanıyoruz.

Kısacası, `stanleyjobsox` ile `stanleyjobson`’u karşılaştırmak için geçen süre, `johndoe` ile `stanleyjobson`’u karşılaştırmak için geçen süreyle aynı olur. Şifre için de aynı şekilde.

Bu sayede uygulama kodunuzda `secrets.compare_digest()` kullanarak bu güvenlik saldırıları ailesine karşı güvenli olursunuz.

### Hatayı döndürün { #return-the-error }

Credential’ların hatalı olduğunu tespit ettikten sonra, 401 status code ile (credential verilmediğinde dönenle aynı) bir `HTTPException` döndürün ve tarayıcının giriş penceresini yeniden göstermesi için `WWW-Authenticate` header’ını ekleyin:

{* ../../docs_src/security/tutorial007_an_py310.py hl[26:30] *}
