# Password ve Bearer ile Basit OAuth2 { #simple-oauth2-with-password-and-bearer }

Şimdi önceki bölümün üzerine inşa edip, eksik parçaları ekleyerek tam bir güvenlik akışı oluşturalım.

## `username` ve `password`’ü Alma { #get-the-username-and-password }

`username` ve `password`’ü almak için **FastAPI** security yardımcı araçlarını kullanacağız.

OAuth2, (bizim kullandığımız) "password flow" kullanılırken client/kullanıcının form verisi olarak `username` ve `password` alanlarını göndermesi gerektiğini belirtir.

Ayrıca spesifikasyon, bu alanların adlarının tam olarak böyle olması gerektiğini söyler. Yani `user-name` veya `email` işe yaramaz.

Ancak merak etmeyin, frontend’de son kullanıcılarınıza dilediğiniz gibi gösterebilirsiniz.

Veritabanı model(ler)inizde de istediğiniz başka isimleri kullanabilirsiniz.

Fakat login *path operation*’ı için, spesifikasyonla uyumlu olmak (ve örneğin entegre API dokümantasyon sistemini kullanabilmek) adına bu isimleri kullanmamız gerekiyor.

Spesifikasyon ayrıca `username` ve `password`’ün form verisi olarak gönderilmesi gerektiğini de söyler (yani burada JSON yok).

### `scope` { #scope }

Spesifikasyon, client’ın "`scope`" adlı başka bir form alanı da gönderebileceğini söyler.

Form alanının adı `scope`’tur (tekil), ama aslında boşluklarla ayrılmış "scope"’lardan oluşan uzun bir string’dir.

Her bir "scope" sadece bir string’dir (boşluk içermez).

Genelde belirli güvenlik izinlerini (permission) belirtmek için kullanılırlar, örneğin:

* `users:read` veya `users:write` yaygın örneklerdir.
* `instagram_basic` Facebook / Instagram tarafından kullanılır.
* `https://www.googleapis.com/auth/drive` Google tarafından kullanılır.

/// info | Bilgi

OAuth2’de bir "scope", gerekli olan belirli bir izni ifade eden basit bir string’dir.

`:` gibi başka karakterler içermesi veya URL olması önemli değildir.

Bu detaylar implementasyon’a özeldir.

OAuth2 açısından bunlar sadece string’lerdir.

///

## `username` ve `password`’ü Almak İçin Kod { #code-to-get-the-username-and-password }

Şimdi bunu yönetmek için **FastAPI**’nin sağladığı araçları kullanalım.

### `OAuth2PasswordRequestForm` { #oauth2passwordrequestform }

Önce `OAuth2PasswordRequestForm`’u import edin ve `/token` için *path operation* içinde `Depends` ile dependency olarak kullanın:

{* ../../docs_src/security/tutorial003_an_py310.py hl[4,78] *}

`OAuth2PasswordRequestForm`, şu alanları içeren bir form body tanımlayan bir class dependency’sidir:

* `username`.
* `password`.
* Boşlukla ayrılmış string’lerden oluşan büyük bir string olarak opsiyonel `scope` alanı.
* Opsiyonel `grant_type`.

/// tip | İpucu

OAuth2 spesifikasyonu aslında `grant_type` alanını sabit bir `password` değeriyle *zorunlu kılar*, ancak `OAuth2PasswordRequestForm` bunu zorlamaz.

Bunu zorlamak istiyorsanız, `OAuth2PasswordRequestForm` yerine `OAuth2PasswordRequestFormStrict` kullanın.

///

* Opsiyonel `client_id` (bu örnekte ihtiyacımız yok).
* Opsiyonel `client_secret` (bu örnekte ihtiyacımız yok).

/// info | Bilgi

`OAuth2PasswordRequestForm`, `OAuth2PasswordBearer` gibi **FastAPI**’ye özel “özel bir sınıf” değildir.

`OAuth2PasswordBearer`, bunun bir security scheme olduğunu **FastAPI**’ye bildirir. Bu yüzden OpenAPI’ye o şekilde eklenir.

Ama `OAuth2PasswordRequestForm` sadece bir class dependency’dir; bunu kendiniz de yazabilirdiniz ya da doğrudan `Form` parametreleri tanımlayabilirdiniz.

Fakat çok yaygın bir kullanım olduğu için **FastAPI** bunu işleri kolaylaştırmak adına doğrudan sağlar.

///

### Form Verisini Kullanma { #use-the-form-data }

/// tip | İpucu

`OAuth2PasswordRequestForm` dependency class’ının instance’ında boşluklarla ayrılmış uzun string olarak bir `scope` attribute’u olmaz; bunun yerine gönderilen her scope için gerçek string listesini içeren `scopes` attribute’u olur.

Bu örnekte `scopes` kullanmıyoruz, ama ihtiyacınız olursa bu özellik hazır.

///

Şimdi form alanındaki `username`’i kullanarak (sahte) veritabanından kullanıcı verisini alın.

Böyle bir kullanıcı yoksa, "Incorrect username or password" diyerek bir hata döndürelim.

Hata için `HTTPException` exception’ını kullanıyoruz:

{* ../../docs_src/security/tutorial003_an_py310.py hl[3,79:81] *}

### Password’ü Kontrol Etme { #check-the-password }

Bu noktada veritabanından kullanıcı verisine sahibiz, ancak password’ü henüz kontrol etmedik.

Önce bu veriyi Pydantic `UserInDB` modeline koyalım.

Asla düz metin (plaintext) password kaydetmemelisiniz; bu yüzden (sahte) password hashing sistemini kullanacağız.

Password’ler eşleşmezse, aynı hatayı döndürürüz.

#### Password hashing { #password-hashing }

"Hashing" şudur: bir içeriği (bu örnekte password) anlaşılmaz görünen bayt dizisine (yani bir string’e) dönüştürmek.

Aynı içeriği (aynı password’ü) her verdiğinizde, birebir aynı anlamsız görünen çıktıyı elde edersiniz.

Ama bu anlamsız çıktıyı tekrar password’e geri çeviremezsiniz.

##### Neden password hashing kullanılır { #why-use-password-hashing }

Veritabanınız çalınırsa, hırsız kullanıcılarınızın düz metin password’lerine değil, sadece hash’lere sahip olur.

Dolayısıyla hırsız, aynı password’leri başka bir sistemde denemeye çalışamaz (birçok kullanıcı her yerde aynı password’ü kullandığı için bu tehlikeli olurdu).

{* ../../docs_src/security/tutorial003_an_py310.py hl[82:85] *}

#### `**user_dict` Hakkında { #about-user-dict }

`UserInDB(**user_dict)` şu anlama gelir:

*`user_dict` içindeki key ve value’ları doğrudan key-value argümanları olarak geçir; şu ifadeyle eşdeğerdir:*

```Python
UserInDB(
    username = user_dict["username"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    disabled = user_dict["disabled"],
    hashed_password = user_dict["hashed_password"],
)
```

/// info | Bilgi

`**user_dict` için daha kapsamlı bir açıklama için [**Extra Models** dokümantasyonundaki ilgili bölüme](../extra-models.md#about-user-in-dict){.internal-link target=_blank} geri dönüp bakın.

///

## Token’ı Döndürme { #return-the-token }

`token` endpoint’inin response’u bir JSON object olmalıdır.

Bir `token_type` içermelidir. Biz "Bearer" token’ları kullandığımız için token type "`bearer`" olmalıdır.

Ayrıca `access_token` içermelidir; bunun değeri access token’ımızı içeren bir string olmalıdır.

Bu basit örnekte tamamen güvensiz davranıp token olarak aynı `username`’i döndüreceğiz.

/// tip | İpucu

Bir sonraki bölümde, password hashing ve <abbr title="JSON Web Tokens">JWT</abbr> token’ları ile gerçekten güvenli bir implementasyon göreceksiniz.

Ama şimdilik ihtiyacımız olan spesifik detaylara odaklanalım.

///

{* ../../docs_src/security/tutorial003_an_py310.py hl[87] *}

/// tip | İpucu

Spesifikasyona göre, bu örnekteki gibi `access_token` ve `token_type` içeren bir JSON döndürmelisiniz.

Bunu kendi kodunuzda kendiniz yapmalı ve bu JSON key’lerini kullandığınızdan emin olmalısınız.

Spesifikasyonlara uyum için, doğru yapmanız gereken neredeyse tek şey budur.

Geri kalanını **FastAPI** sizin yerinize yönetir.

///

## Dependency’leri Güncelleme { #update-the-dependencies }

Şimdi dependency’lerimizi güncelleyeceğiz.

`current_user`’ı *sadece* kullanıcı aktifse almak istiyoruz.

Bu yüzden, `get_current_user`’ı dependency olarak kullanan ek bir dependency olan `get_current_active_user`’ı oluşturuyoruz.

Bu iki dependency de kullanıcı yoksa veya pasifse sadece HTTP hatası döndürecek.

Dolayısıyla endpoint’imizde kullanıcıyı ancak kullanıcı varsa, doğru şekilde authenticate edildiyse ve aktifse alacağız:

{* ../../docs_src/security/tutorial003_an_py310.py hl[58:66,69:74,94] *}

/// info | Bilgi

Burada `Bearer` değerine sahip ek `WWW-Authenticate` header’ını döndürmemiz de spesifikasyonun bir parçasıdır.

Herhangi bir HTTP (hata) durum kodu 401 "UNAUTHORIZED", ayrıca `WWW-Authenticate` header’ı da döndürmelidir.

Bearer token’lar (bizim durumumuz) için bu header’ın değeri `Bearer` olmalıdır.

Aslında bu ekstra header’ı atlayabilirsiniz, yine de çalışır.

Ama spesifikasyonlara uyumlu olması için burada eklenmiştir.

Ayrıca, bunu bekleyen ve kullanan araçlar olabilir (şimdi veya ileride) ve bu da sizin ya da kullanıcılarınız için faydalı olabilir.

Standartların faydası da bu...

///

## Çalışır Halini Görün { #see-it-in-action }

Etkileşimli dokümanları açın: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

### Authenticate Olma { #authenticate }

"Authorize" butonuna tıklayın.

Şu bilgileri kullanın:

User: `johndoe`

Password: `secret`

<img src="/img/tutorial/security/image04.png">

Sistemde authenticate olduktan sonra şöyle görürsünüz:

<img src="/img/tutorial/security/image05.png">

### Kendi Kullanıcı Verinizi Alma { #get-your-own-user-data }

Şimdi `/users/me` path’inde `GET` operasyonunu kullanın.

Kullanıcınızın verisini şöyle alırsınız:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
```

<img src="/img/tutorial/security/image06.png">

Kilit ikonuna tıklayıp logout olursanız ve sonra aynı operasyonu tekrar denerseniz, şu şekilde bir HTTP 401 hatası alırsınız:

```JSON
{
  "detail": "Not authenticated"
}
```

### Pasif Kullanıcı { #inactive-user }

Şimdi pasif bir kullanıcıyla deneyin; şu bilgilerle authenticate olun:

User: `alice`

Password: `secret2`

Ve `/users/me` path’inde `GET` operasyonunu kullanmayı deneyin.

Şöyle bir "Inactive user" hatası alırsınız:

```JSON
{
  "detail": "Inactive user"
}
```

## Özet { #recap }

Artık API’niz için `username` ve `password` tabanlı, eksiksiz bir güvenlik sistemi implement etmek için gerekli araçlara sahipsiniz.

Bu araçlarla güvenlik sistemini herhangi bir veritabanıyla ve herhangi bir user veya veri modeliyle uyumlu hale getirebilirsiniz.

Eksik kalan tek detay, bunun henüz gerçekten "güvenli" olmamasıdır.

Bir sonraki bölümde güvenli bir password hashing kütüphanesini ve <abbr title="JSON Web Tokens">JWT</abbr> token’larını nasıl kullanacağınızı göreceksiniz.
