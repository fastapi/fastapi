# Middleware { #middleware }

**FastAPI** uygulamalarına middleware ekleyebilirsiniz.

"Middleware", herhangi bir özel *path operation* tarafından işlenmeden önce her **request** ile çalışan bir fonksiyondur. Ayrıca geri döndürmeden önce her **response** ile de çalışır.

* Uygulamanıza gelen her **request**'i alır.
* Ardından o **request** üzerinde bir işlem yapabilir veya gerekli herhangi bir kodu çalıştırabilir.
* Sonra **request**'i uygulamanın geri kalanı tarafından işlenmesi için iletir (bir *path operation* tarafından).
* Ardından uygulama tarafından üretilen **response**'u alır (bir *path operation* tarafından).
* Sonra o **response** üzerinde bir işlem yapabilir veya gerekli herhangi bir kodu çalıştırabilir.
* Son olarak **response**'u döndürür.

/// note | Teknik Detaylar

`yield` ile dependency'leriniz varsa, çıkış (exit) kodu middleware'den *sonra* çalışır.

Herhangi bir background task varsa ([Background Tasks](background-tasks.md) bölümünde ele alınıyor, ileride göreceksiniz), bunlar tüm middleware'ler *tamamlandıktan sonra* çalışır.

///

## Middleware Oluşturma { #create-a-middleware }

Bir middleware oluşturmak için bir fonksiyonun üzerine `@app.middleware("http")` decorator'ünü kullanırsınız.

Middleware fonksiyonu şunları alır:

* `request`.
* Parametre olarak `request` alacak bir `call_next` fonksiyonu.
    * Bu fonksiyon `request`'i ilgili *path operation*'a iletir.
    * Ardından ilgili *path operation* tarafından üretilen `response`'u döndürür.
* Sonrasında `response`'u döndürmeden önce ayrıca değiştirebilirsiniz.

{* ../../docs_src/middleware/tutorial001_py310.py hl[8:9,11,14] *}

/// tip | İpucu

Özel (proprietary) header'lar [`X-` prefix'i kullanılarak](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) eklenebilir, bunu aklınızda tutun.

Ancak tarayıcıdaki bir client'ın görebilmesini istediğiniz özel header'larınız varsa, bunları CORS konfigürasyonlarınıza ([CORS (Cross-Origin Resource Sharing)](cors.md)) eklemeniz gerekir. Bunun için, [Starlette'ın CORS dokümanlarında](https://www.starlette.dev/middleware/#corsmiddleware) belgelenen `expose_headers` parametresini kullanın.

///

/// note | Teknik Detaylar

`from starlette.requests import Request` da kullanabilirdiniz.

**FastAPI** bunu geliştirici olarak size kolaylık olsun diye sunar. Ancak doğrudan Starlette'tan gelir.

///

### `response`'tan Önce ve Sonra { #before-and-after-the-response }

Herhangi bir *path operation* `request`'i almadan önce, `request` ile birlikte çalışacak kod ekleyebilirsiniz.

Ayrıca `response` üretildikten sonra, geri döndürmeden önce de kod çalıştırabilirsiniz.

Örneğin, request'i işleyip response üretmenin kaç saniye sürdüğünü içeren `X-Process-Time` adlı özel bir header ekleyebilirsiniz:

{* ../../docs_src/middleware/tutorial001_py310.py hl[10,12:13] *}

/// tip | İpucu

Burada [`time.perf_counter()`](https://docs.python.org/3/library/time.html#time.perf_counter) yerine `time.time()` kullanıyoruz, çünkü bu kullanım senaryolarında daha hassas olabilir. 🤓

///

## Birden Fazla Middleware Çalıştırma Sırası { #multiple-middleware-execution-order }

`@app.middleware()` decorator'ü veya `app.add_middleware()` metodu ile birden fazla middleware eklediğinizde, eklenen her yeni middleware uygulamayı sarar ve bir stack oluşturur. En son eklenen middleware en *dıştaki* (outermost), ilk eklenen ise en *içteki* (innermost) olur.

Request tarafında önce en *dıştaki* middleware çalışır.

Response tarafında ise en son o çalışır.

Örneğin:

```Python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

Bu, aşağıdaki çalıştırma sırasını oluşturur:

* **Request**: MiddlewareB → MiddlewareA → route

* **Response**: route → MiddlewareA → MiddlewareB

Bu stack davranışı, middleware'lerin öngörülebilir ve kontrol edilebilir bir sırayla çalıştırılmasını sağlar.

## Diğer Middleware'ler { #other-middlewares }

Diğer middleware'ler hakkında daha fazlasını daha sonra [Advanced User Guide: Advanced Middleware](../advanced/middleware.md) bölümünde okuyabilirsiniz.

Bir sonraki bölümde, middleware ile <abbr title="Cross-Origin Resource Sharing - Çapraz Kaynak Paylaşımı">CORS</abbr>'un nasıl ele alınacağını göreceksiniz.
