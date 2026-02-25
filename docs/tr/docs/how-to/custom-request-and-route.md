# Özel Request ve APIRoute sınıfı { #custom-request-and-apiroute-class }

Bazı durumlarda, `Request` ve `APIRoute` sınıflarının kullandığı mantığı override etmek isteyebilirsiniz.

Özellikle bu yaklaşım, bir middleware içindeki mantığa iyi bir alternatif olabilir.

Örneğin, request body uygulamanız tarafından işlenmeden önce okumak veya üzerinde değişiklik yapmak istiyorsanız.

/// danger | Uyarı

Bu "ileri seviye" bir özelliktir.

**FastAPI**'ye yeni başlıyorsanız bu bölümü atlamak isteyebilirsiniz.

///

## Kullanım senaryoları { #use-cases }

Bazı kullanım senaryoları:

* JSON olmayan request body'leri JSON'a dönüştürmek (örn. <a href="https://msgpack.org/index.html" class="external-link" target="_blank">`msgpack`</a>).
* gzip ile sıkıştırılmış request body'leri açmak (decompress).
* Tüm request body'lerini otomatik olarak loglamak.

## Özel request body encoding'lerini ele alma { #handling-custom-request-body-encodings }

Gzip request'lerini açmak için özel bir `Request` alt sınıfını nasıl kullanabileceğimize bakalım.

Ayrıca, o özel request sınıfını kullanmak için bir `APIRoute` alt sınıfı da oluşturacağız.

### Özel bir `GzipRequest` sınıfı oluşturun { #create-a-custom-gziprequest-class }

/// tip | İpucu

Bu, nasıl çalıştığını göstermek için hazırlanmış basit bir örnektir; Gzip desteğine ihtiyacınız varsa sağlanan [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware){.internal-link target=_blank} bileşenini kullanabilirsiniz.

///

Önce, uygun bir header mevcut olduğunda body'yi açmak için `Request.body()` metodunu overwrite edecek bir `GzipRequest` sınıfı oluşturuyoruz.

Header'da `gzip` yoksa body'yi açmayı denemez.

Böylece aynı route sınıfı, gzip ile sıkıştırılmış veya sıkıştırılmamış request'leri handle edebilir.

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[9:16] *}

### Özel bir `GzipRoute` sınıfı oluşturun { #create-a-custom-gziproute-class }

Sonra, `GzipRequest`'i kullanacak `fastapi.routing.APIRoute` için özel bir alt sınıf oluşturuyoruz.

Bu kez `APIRoute.get_route_handler()` metodunu overwrite edeceğiz.

Bu metot bir fonksiyon döndürür. Bu fonksiyon da request'i alır ve response döndürür.

Burada bu fonksiyonu, orijinal request'ten bir `GzipRequest` oluşturmak için kullanıyoruz.

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[19:27] *}

/// note | Teknik Detaylar

Bir `Request`'in, request ile ilgili metadata'yı içeren bir Python `dict` olan `request.scope` attribute'u vardır.

Bir `Request` ayrıca `request.receive` içerir; bu, request'in body'sini "almak" (receive etmek) için kullanılan bir fonksiyondur.

`scope` `dict`'i ve `receive` fonksiyonu, ASGI spesifikasyonunun parçalarıdır.

Ve bu iki şey, `scope` ve `receive`, yeni bir `Request` instance'ı oluşturmak için gerekenlerdir.

`Request` hakkında daha fazla bilgi için <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">Starlette'ın Request dokümantasyonuna</a> bakın.

///

`GzipRequest.get_route_handler` tarafından döndürülen fonksiyonun farklı yaptığı tek şey, `Request`'i bir `GzipRequest`'e dönüştürmektir.

Bunu yaptığımızda `GzipRequest`, veriyi (gerekliyse) *path operations*'larımıza geçirmeden önce açma (decompress) işini üstlenir.

Bundan sonra tüm işleme mantığı aynıdır.

Ancak `GzipRequest.body` içindeki değişikliklerimiz sayesinde, request body gerektiğinde **FastAPI** tarafından yüklendiğinde otomatik olarak decompress edilir.

## Bir exception handler içinde request body'ye erişme { #accessing-the-request-body-in-an-exception-handler }

/// tip | İpucu

Aynı problemi çözmek için, muhtemelen `RequestValidationError` için özel bir handler içinde `body` kullanmak çok daha kolaydır ([Hataları Ele Alma](../tutorial/handling-errors.md#use-the-requestvalidationerror-body){.internal-link target=_blank}).

Yine de bu örnek geçerlidir ve dahili bileşenlerle nasıl etkileşime geçileceğini gösterir.

///

Aynı yaklaşımı bir exception handler içinde request body'ye erişmek için de kullanabiliriz.

Tek yapmamız gereken, request'i bir `try`/`except` bloğu içinde handle etmek:

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[14,16] *}

Bir exception oluşursa, `Request` instance'ı hâlâ scope içinde olacağı için, hatayı handle ederken request body'yi okuyup kullanabiliriz:

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[17:19] *}

## Bir router içinde özel `APIRoute` sınıfı { #custom-apiroute-class-in-a-router }

Bir `APIRouter` için `route_class` parametresini de ayarlayabilirsiniz:

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[26] *}

Bu örnekte, `router` altındaki *path operations*'lar özel `TimedRoute` sınıfını kullanır ve response'u üretmek için geçen süreyi içeren ekstra bir `X-Response-Time` header'ı response'ta bulunur:

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[13:20] *}
