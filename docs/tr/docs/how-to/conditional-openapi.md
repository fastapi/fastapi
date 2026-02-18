# Koşullu OpenAPI { #conditional-openapi }

Gerekirse, ayarlar ve environment variable'ları kullanarak OpenAPI'yi ortama göre koşullu şekilde yapılandırabilir, hatta tamamen devre dışı bırakabilirsiniz.

## Güvenlik, API'ler ve dokümantasyon hakkında { #about-security-apis-and-docs }

Production ortamında dokümantasyon arayüzlerini gizlemek, API'nizi korumanın yolu olmamalıdır.

Bu, API'nize ekstra bir güvenlik katmanı eklemez; path operation'lar bulundukları yerde yine erişilebilir olacaktır.

Kodunuzda bir güvenlik açığı varsa, o açık yine var olmaya devam eder.

Dokümantasyonu gizlemek, API'nizle nasıl etkileşime geçileceğini anlamayı zorlaştırır ve production'da debug etmeyi de daha zor hale getirebilir. Bu yaklaşım, basitçe <a href="https://en.wikipedia.org/wiki/Security_through_obscurity" class="external-link" target="_blank">Security through obscurity</a> olarak değerlendirilebilir.

API'nizi güvence altına almak istiyorsanız, yapabileceğiniz daha iyi birçok şey var; örneğin:

* request body'leriniz ve response'larınız için iyi tanımlanmış Pydantic model'larına sahip olduğunuzdan emin olun.
* dependencies kullanarak gerekli izinleri ve rolleri yapılandırın.
* Asla düz metin (plaintext) şifre saklamayın, yalnızca password hash'leri saklayın.
* pwdlib ve JWT token'ları gibi, iyi bilinen kriptografik araçları uygulayın ve kullanın.
* Gerektiğinde OAuth2 scope'ları ile daha ayrıntılı izin kontrolleri ekleyin.
* ...vb.

Yine de, bazı ortamlarda (örn. production) veya environment variable'lardan gelen konfigürasyonlara bağlı olarak API docs'u gerçekten devre dışı bırakmanız gereken çok spesifik bir use case'iniz olabilir.

## Ayarlar ve env var'lar ile koşullu OpenAPI { #conditional-openapi-from-settings-and-env-vars }

Üretilen OpenAPI'yi ve docs UI'larını yapılandırmak için aynı Pydantic settings'i kolayca kullanabilirsiniz.

Örneğin:

{* ../../docs_src/conditional_openapi/tutorial001_py310.py hl[6,11] *}

Burada `openapi_url` ayarını, varsayılanı `"/openapi.json"` olacak şekilde tanımlıyoruz.

Ardından `FastAPI` app'ini oluştururken bunu kullanıyoruz.

Sonrasında, environment variable `OPENAPI_URL`'i boş string olarak ayarlayarak OpenAPI'yi (UI docs dahil) devre dışı bırakabilirsiniz; örneğin:

<div class="termy">

```console
$ OPENAPI_URL= uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Böylece `/openapi.json`, `/docs` veya `/redoc` URL'lerine giderseniz, aşağıdaki gibi bir `404 Not Found` hatası alırsınız:

```JSON
{
    "detail": "Not Found"
}
```
