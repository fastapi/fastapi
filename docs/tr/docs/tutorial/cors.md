# CORS (Cross-Origin Resource Sharing) { #cors-cross-origin-resource-sharing }

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">CORS veya "Cross-Origin Resource Sharing"</a>, tarayıcıda çalışan bir frontend’in JavaScript kodunun bir backend ile iletişim kurduğu ve backend’in frontend’den farklı bir "origin"de olduğu durumları ifade eder.

## Origin { #origin }

Origin; protocol (`http`, `https`), domain (`myapp.com`, `localhost`, `localhost.tiangolo.com`) ve port’un (`80`, `443`, `8080`) birleşimidir.

Dolayısıyla şunların hepsi farklı origin’lerdir:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

Hepsi `localhost` üzerinde olsa bile, farklı protocol veya port kullandıkları için farklı "origin" sayılırlar.

## Adımlar { #steps }

Diyelim ki tarayıcınızda `http://localhost:8080` adresinde çalışan bir frontend’iniz var ve JavaScript’i, `http://localhost` adresinde çalışan bir backend ile iletişim kurmaya çalışıyor (port belirtmediğimiz için tarayıcı varsayılan port olan `80`’i kullanacaktır).

Bu durumda tarayıcı, `:80`-backend’e bir HTTP `OPTIONS` request’i gönderir. Eğer backend, bu farklı origin’den (`http://localhost:8080`) gelen iletişimi yetkilendiren uygun header’ları gönderirse, `:8080`-tarayıcı frontend’deki JavaScript’in `:80`-backend’e request göndermesine izin verir.

Bunu sağlayabilmek için `:80`-backend’in bir "allowed origins" listesi olmalıdır.

Bu örnekte `:8080`-frontend’in doğru çalışması için listede `http://localhost:8080` bulunmalıdır.

## Wildcard'lar { #wildcards }

Listeyi `"*"` (bir "wildcard") olarak tanımlayıp, hepsine izin verildiğini söylemek de mümkündür.

Ancak bu, credentials içeren her şeyi hariç tutarak yalnızca belirli iletişim türlerine izin verir: Cookie’ler, Bearer Token’larla kullanılanlar gibi Authorization header’ları, vb.

Bu yüzden her şeyin düzgün çalışması için, izin verilen origin’leri açıkça belirtmek daha iyidir.

## `CORSMiddleware` Kullanımı { #use-corsmiddleware }

Bunu **FastAPI** uygulamanızda `CORSMiddleware` ile yapılandırabilirsiniz.

* `CORSMiddleware`’i import edin.
* İzin verilen origin’lerden (string) oluşan bir liste oluşturun.
* Bunu **FastAPI** uygulamanıza bir "middleware" olarak ekleyin.

Ayrıca backend’in şunlara izin verip vermediğini de belirtebilirsiniz:

* Credentials (Authorization header’ları, Cookie’ler, vb).
* Belirli HTTP method’ları (`POST`, `PUT`) veya wildcard `"*"` ile hepsini.
* Belirli HTTP header’ları veya wildcard `"*"` ile hepsini.

{* ../../docs_src/cors/tutorial001_py310.py hl[2,6:11,13:19] *}


`CORSMiddleware` implementasyonu tarafından kullanılan varsayılan parametreler kısıtlayıcıdır; bu nedenle tarayıcıların Cross-Domain bağlamında kullanmasına izin vermek için belirli origin’leri, method’ları veya header’ları açıkça etkinleştirmeniz gerekir.

Aşağıdaki argümanlar desteklenir:

* `allow_origins` - Cross-origin request yapmasına izin verilmesi gereken origin’lerin listesi. Örn. `['https://example.org', 'https://www.example.org']`. Herhangi bir origin’e izin vermek için `['*']` kullanabilirsiniz.
* `allow_origin_regex` - Cross-origin request yapmasına izin verilmesi gereken origin’lerle eşleşecek bir regex string’i. Örn. `'https://.*\.example\.org'`.
* `allow_methods` - Cross-origin request’lerde izin verilmesi gereken HTTP method’larının listesi. Varsayılanı `['GET']`. Tüm standart method’lara izin vermek için `['*']` kullanabilirsiniz.
* `allow_headers` - Cross-origin request’lerde desteklenmesi gereken HTTP request header’larının listesi. Varsayılanı `[]`. Tüm header’lara izin vermek için `['*']` kullanabilirsiniz. `Accept`, `Accept-Language`, `Content-Language` ve `Content-Type` header’larına <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests" class="external-link" rel="noopener" target="_blank">basit CORS request'leri</a> için her zaman izin verilir.
* `allow_credentials` - Cross-origin request’ler için cookie desteği olup olmayacağını belirtir. Varsayılanı `False`.

    `allow_credentials` `True` olarak ayarlanmışsa, `allow_origins`, `allow_methods` ve `allow_headers` değerlerinin hiçbiri `['*']` olamaz. Hepsinin <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#credentialed_requests_and_wildcards" class="external-link" rel="noopener" target="_blank">açıkça belirtilmesi</a> gerekir.

* `expose_headers` - Tarayıcının erişebilmesi gereken response header’larını belirtir. Varsayılanı `[]`.
* `max_age` - Tarayıcıların CORS response’larını cache’lemesi için saniye cinsinden azami süreyi ayarlar. Varsayılanı `600`.

Middleware iki özel HTTP request türüne yanıt verir...

### CORS preflight request'leri { #cors-preflight-requests }

Bunlar, `Origin` ve `Access-Control-Request-Method` header’larına sahip herhangi bir `OPTIONS` request’idir.

Bu durumda middleware gelen request’i intercept eder ve uygun CORS header’larıyla yanıt verir; bilgilendirme amaçlı olarak da `200` veya `400` response döndürür.

### Basit request'ler { #simple-requests }

`Origin` header’ı olan herhangi bir request. Bu durumda middleware request’i normal şekilde geçirir, ancak response’a uygun CORS header’larını ekler.

## Daha Fazla Bilgi { #more-info }

<abbr title="Cross-Origin Resource Sharing - Kökenler Arası Kaynak Paylaşımı">CORS</abbr> hakkında daha fazla bilgi için <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">Mozilla CORS dokümantasyonu</a>na bakın.

/// note | Teknik Detaylar

`from starlette.middleware.cors import CORSMiddleware` şeklinde de kullanabilirsiniz.

**FastAPI**, geliştirici olarak size kolaylık olması için `fastapi.middleware` içinde bazı middleware’ler sağlar. Ancak mevcut middleware’lerin çoğu doğrudan Starlette’ten gelir.

///
