# Yanıt Başlıkları

## Bir `Response` Parametresi Kullanın

*yol operasyonu fonksiyonunuzda* `Response` türünde bir parametre belirleyebilirsiniz (tıpkı çerezlerde olduğu gibi).

Ardından *geçici* yanıt nesnesinde başlıkları belirleyebilirsiniz.

{* ../../docs_src/response_headers/tutorial002.py hl[1, 7:8] *}

Sonunda normalde döndürdüğünüz gibi herhangi bir nesneyi döndürebilirsiniz (bir `dict`, bir veritabanı modeli, vb).

Eğer bir `response_model` belirlediyseniz, döndürdüğünüz nesneyi filtrelemek ve dönüştürmek için kullanılacaktır.

**FastAPI** bu *geçici* yanıtı başlıkları (ayrıca durum kodunu ve çerezleri) çıkarmak için kullanacak ve döndürdüğünüz değeri herhangi bir `response_model` tarafından filtreleyerek son yanıta koyacaktır.

Bağımlılıklarda da `Response` parametresini belirtebilir ve başlıkları belirleyebilirsiniz.

## Bir `Response`'u Doğrudan Döndürün

Doğrudan bir `Response` döndürürken başlıklar oluşturabilirsiniz.

Bunun için [Return a Response Directly](response-directly.md){.internal-link target=_blank} sayfasında açıklandığı gibi bir yanıt oluşturup başlıkları ekleyin:

{* ../../docs_src/response_headers/tutorial001.py hl[10:12] *}

/// note | "Teknik Detaylar"
    Projenize dahil etmek için `from starlette.responses import Response` veya `from starlette.responses import JSONResponse` kullanabilirsiniz.

    **FastAPI**, geliştiricilere kolaylık sağlamak amacıyla `starlette.responses`'ı `fastapi.responses` olarak sağlar. Ancak mevcut yanıtların çoğu doğrudan Starlette'den gelir. Aynı durum `status` için de geçerlidir.

    `Response` sıklıkla başlıkları ve çerezleri belirlemek için kullanılabileceği için, **FastAPI** ayrıca `fastapi.Response`'ı da sağlar.

///

## Özelleştirilmiş Başlıklar

Aklınızda bulundurun ki özel başlıklar, <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">'X-' öneki kullanılarak</a> eklenmelidir.

Tarayıcıdaki bir istemcinin görüntüleyebilmesini istediğiniz özel başlıklarınız varsa, bunları <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette'in CORS dokümantasyonunda</a> belirtildiği gibi  `expose_headers` parametresini kullanarak CORS yapılandırmalarınıza eklemeniz gerekir (daha fazlasını [CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md){.internal-link target=_blank} sayfasında okuyabilirsiniz),.
