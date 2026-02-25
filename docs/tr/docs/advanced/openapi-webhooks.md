# OpenAPI Webhook'lar { #openapi-webhooks }

Bazı durumlarda, API'nizi kullanan **kullanıcılara** uygulamanızın *onların* uygulamasını (request göndererek) bazı verilerle çağırabileceğini; genellikle bir tür **event** hakkında **bildirim** yapmak için kullanacağını söylemek istersiniz.

Bu da şunu ifade eder: Kullanıcılarınızın API'nize request göndermesi şeklindeki normal akış yerine, request'i **sizin API'niz** (veya uygulamanız) **onların sistemine** (onların API'sine, onların uygulamasına) **gönderebilir**.

Buna genellikle **webhook** denir.

## Webhook adımları { #webhooks-steps }

Süreç genellikle şöyledir: Kodunuzda göndereceğiniz mesajın ne olduğunu, yani request'in **body**'sini **siz tanımlarsınız**.

Ayrıca uygulamanızın bu request'leri veya event'leri hangi **anlarda** göndereceğini de bir şekilde tanımlarsınız.

Ve **kullanıcılarınız** da bir şekilde (örneğin bir web dashboard üzerinden) uygulamanızın bu request'leri göndermesi gereken **URL**'yi tanımlar.

Webhook'lar için URL'lerin nasıl kaydedileceğine dair tüm **mantık** ve bu request'leri gerçekten gönderen kod tamamen size bağlıdır. Bunu **kendi kodunuzda** istediğiniz gibi yazarsınız.

## **FastAPI** ve OpenAPI ile webhook'ları dokümante etmek { #documenting-webhooks-with-fastapi-and-openapi }

**FastAPI** ile OpenAPI kullanarak bu webhook'ların adlarını, uygulamanızın gönderebileceği HTTP operation türlerini (örn. `POST`, `PUT`, vb.) ve uygulamanızın göndereceği request **body**'lerini tanımlayabilirsiniz.

Bu, kullanıcılarınızın **webhook** request'lerinizi alacak şekilde **API'lerini implement etmesini** çok daha kolaylaştırabilir; hatta kendi API kodlarının bir kısmını otomatik üretebilirler.

/// info | Bilgi

Webhook'lar OpenAPI 3.1.0 ve üzeri sürümlerde mevcuttur; FastAPI `0.99.0` ve üzeri tarafından desteklenir.

///

## Webhook'ları olan bir uygulama { #an-app-with-webhooks }

Bir **FastAPI** uygulaması oluşturduğunuzda, *webhook*'ları tanımlamak için kullanabileceğiniz bir `webhooks` attribute'u vardır; *path operation* tanımlar gibi, örneğin `@app.webhooks.post()` ile.

{* ../../docs_src/openapi_webhooks/tutorial001_py310.py hl[9:12,15:20] *}

Tanımladığınız webhook'lar **OpenAPI** şemasında ve otomatik **docs UI**'da yer alır.

/// info | Bilgi

`app.webhooks` nesnesi aslında sadece bir `APIRouter`'dır; uygulamanızı birden fazla dosya ile yapılandırırken kullanacağınız türün aynısıdır.

///

Dikkat edin: Webhook'larda aslında bir *path* (ör. `/items/`) deklare etmiyorsunuz; oraya verdiğiniz metin sadece webhook'un bir **identifier**'ıdır (event'in adı). Örneğin `@app.webhooks.post("new-subscription")` içinde webhook adı `new-subscription`'dır.

Bunun nedeni, webhook request'ini almak istedikleri gerçek **URL path**'i **kullanıcılarınızın** başka bir şekilde (örn. bir web dashboard üzerinden) tanımlamasının beklenmesidir.

### Dokümanları kontrol edin { #check-the-docs }

Şimdi uygulamanızı başlatıp <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> adresine gidin.

Dokümanlarınızda normal *path operation*'ları ve artık bazı **webhook**'ları da göreceksiniz:

<img src="/img/tutorial/openapi-webhooks/image01.png">
