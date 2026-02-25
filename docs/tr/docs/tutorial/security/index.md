# Güvenlik { #security }

Güvenlik, authentication ve authorization’ı ele almanın birçok yolu vardır.

Ve bu konu genellikle karmaşık ve "zor"dur.

Birçok framework ve sistemde yalnızca security ve authentication’ı yönetmek bile ciddi miktarda emek ve kod gerektirir (çoğu durumda yazılan toplam kodun %50’si veya daha fazlası olabilir).

**FastAPI**, tüm security spesifikasyonlarını baştan sona inceleyip öğrenmek zorunda kalmadan **Security** konusunu kolay, hızlı ve standart bir şekilde ele almanıza yardımcı olacak çeşitli araçlar sunar.

Ama önce, küçük birkaç kavrama bakalım.

## Acelem var? { #in-a-hurry }

Bu terimlerin hiçbirini umursamıyorsanız ve sadece kullanıcı adı ve parola tabanlı authentication ile security’yi *hemen şimdi* eklemeniz gerekiyorsa, bir sonraki bölümlere geçin.

## OAuth2 { #oauth2 }

OAuth2, authentication ve authorization’ı yönetmek için çeşitli yöntemleri tanımlayan bir spesifikasyondur.

Oldukça kapsamlı bir spesifikasyondur ve birkaç karmaşık use case’i kapsar.

"Üçüncü taraf" kullanarak authentication yapmanın yollarını da içerir.

"Facebook, Google, X (Twitter), GitHub ile giriş yap" bulunan sistemlerin arka planda kullandığı şey de budur.

### OAuth 1 { #oauth-1 }

OAuth 1 de vardı; OAuth2’den çok farklıdır ve daha karmaşıktır, çünkü iletişimi nasıl şifreleyeceğinize dair doğrudan spesifikasyonlar içeriyordu.

Günümüzde pek popüler değildir veya pek kullanılmaz.

OAuth2 ise iletişimin nasıl şifreleneceğini belirtmez; uygulamanızın HTTPS ile sunulmasını bekler.

/// tip | İpucu

**deployment** bölümünde Traefik ve Let's Encrypt kullanarak ücretsiz şekilde HTTPS’i nasıl kuracağınızı göreceksiniz.

///

## OpenID Connect { #openid-connect }

OpenID Connect, **OAuth2** tabanlı başka bir spesifikasyondur.

OAuth2’de nispeten belirsiz kalan bazı noktaları tanımlayarak onu daha birlikte çalışabilir (interoperable) hâle getirmeye çalışır.

Örneğin, Google ile giriş OpenID Connect kullanır (arka planda OAuth2 kullanır).

Ancak Facebook ile giriş OpenID Connect’i desteklemez. Kendine özgü bir OAuth2 çeşidi vardır.

### OpenID ("OpenID Connect" değil) { #openid-not-openid-connect }

Bir de "OpenID" spesifikasyonu vardı. Bu da **OpenID Connect** ile aynı problemi çözmeye çalışıyordu ama OAuth2 tabanlı değildi.

Dolayısıyla tamamen ayrı, ek bir sistemdi.

Günümüzde pek popüler değildir veya pek kullanılmaz.

## OpenAPI { #openapi }

OpenAPI (önceden Swagger olarak biliniyordu), API’ler inşa etmek için açık spesifikasyondur (artık Linux Foundation’ın bir parçası).

**FastAPI**, **OpenAPI** tabanlıdır.

Bu sayede birden fazla otomatik etkileşimli dokümantasyon arayüzü, code generation vb. mümkün olur.

OpenAPI, birden fazla security "scheme" tanımlamanın bir yolunu sunar.

Bunları kullanarak, etkileşimli dokümantasyon sistemleri de dahil olmak üzere tüm bu standart tabanlı araçlardan faydalanabilirsiniz.

OpenAPI şu security scheme’lerini tanımlar:

* `apiKey`: uygulamaya özel bir anahtar; şuradan gelebilir:
    * Bir query parameter.
    * Bir header.
    * Bir cookie.
* `http`: standart HTTP authentication sistemleri, örneğin:
    * `bearer`: `Authorization` header’ı; değeri `Bearer ` + bir token olacak şekilde. Bu, OAuth2’den gelir.
    * HTTP Basic authentication.
    * HTTP Digest, vb.
* `oauth2`: OAuth2 ile security’yi yönetmenin tüm yolları ("flow" olarak adlandırılır).
    * Bu flow’ların birçoğu, bir OAuth 2.0 authentication provider (Google, Facebook, X (Twitter), GitHub vb.) oluşturmak için uygundur:
        * `implicit`
        * `clientCredentials`
        * `authorizationCode`
    * Ancak, aynı uygulamanın içinde doğrudan authentication yönetmek için mükemmel şekilde kullanılabilecek özel bir "flow" vardır:
        * `password`: sonraki bazı bölümlerde bunun örnekleri ele alınacak.
* `openIdConnect`: OAuth2 authentication verisinin otomatik olarak nasıl keşfedileceğini tanımlamanın bir yolunu sunar.
    * Bu otomatik keşif, OpenID Connect spesifikasyonunda tanımlanan şeydir.


/// tip | İpucu

Google, Facebook, X (Twitter), GitHub vb. gibi diğer authentication/authorization provider’larını entegre etmek de mümkündür ve nispeten kolaydır.

En karmaşık kısım, bu tür bir authentication/authorization provider’ı inşa etmektir; ancak **FastAPI** ağır işleri sizin yerinize yaparken bunu kolayca yapabilmeniz için araçlar sunar.

///

## **FastAPI** yardımcı araçları { #fastapi-utilities }

FastAPI, `fastapi.security` modülünde bu security scheme’lerinin her biri için, bu mekanizmaları kullanmayı kolaylaştıran çeşitli araçlar sağlar.

Sonraki bölümlerde, **FastAPI**’nin sunduğu bu araçları kullanarak API’nize nasıl security ekleyeceğinizi göreceksiniz.

Ayrıca bunun etkileşimli dokümantasyon sistemine nasıl otomatik olarak entegre edildiğini de göreceksiniz.
