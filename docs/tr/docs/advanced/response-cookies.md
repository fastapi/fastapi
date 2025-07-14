# Yanıt Çerezleri

## Bir `Response` Parametresi Kullanın

*yol operasyonu fonksiyonunuzda* `Response` türünde bir parametre belirleyebilirsiniz.

Ardından *geçici* yanıt nesnesinde çerezleri belirleyebilirsiniz.

{* ../../docs_src/response_cookies/tutorial002.py hl[1, 8:9] *}

Sonunda normalde döndürdüğünüz gibi herhangi bir nesneyi döndürebilirsiniz (bir `dict`, bir veritabanı modeli, vb).

Eğer bir `response_model` belirlediyseniz, döndürdüğünüz nesneyi filtrelemek ve dönüştürmek için kullanılacaktır.

**FastAPI** bu *geçici* yanıtı çerezleri (ayrıca durum kodunu ve başlıkları) çıkarmak için kullanacak ve döndürdüğünüz değeri herhangi bir `response_model` tarafından filtreleyerek son yanıta koyacaktır.

Bağımlılıklarda da `Response` parametresini belirtebilir ve çezerlezi belirleyebilirsiniz.

## Bir `Response`'u Doğrudan Döndürün

Doğrudan bir `Response` döndürürken çerezler oluşturabilirsiniz.

Bunun için [Return a Response Directly](response-directly.md){.internal-link target=_blank} sayfasında açıklandığı gibi bir yanıt oluşturabilirsiniz.

Ardından çerezleri belirleyin ve yanıtı döndürün:

{* ../../docs_src/response_cookies/tutorial001.py hl[10:12] *}

/// tip | İpucu

`Response` parametresini kullanmak yerine yanıtı doğrudan döndürürseniz, FastAPI yanıtı doğrudan döndürecektir.

Yanıtı doğrudan döndürürken, verinizin doğru türde olduğundan emin olmalısınız. Örneğin, bir `JSONResponse` döndürüyorsanız, verinizin JSON ile uyumlu olduğundan emin olmalısınız.

Ayrıca, bir `response_model` tarafından filtrelenmesi gereken verileri göndermediğinizden emin olmalısınız.

///

## Daha Fazla Bilgi

/// note | Teknik Detaylar

Projenize dahil etmek için `from starlette.responses import Response` veya `from starlette.responses import JSONResponse` kullanabilirsiniz.

**FastAPI**, geliştiricilere kolaylık sağlamak amacıyla `starlette.responses`'ı `fastapi.responses` olarak sağlar. Ancak mevcut yanıtların çoğu doğrudan Starlette'den gelir. Aynı durum `status` için de geçerlidir.

`Response` sıklıkla başlıkları ve çerezleri belirlemek için kullanılabileceği için, **FastAPI** ayrıca `fastapi.Response`'ı da sağlar.

///

Tüm mevcut parametreleri ve seçenekleri görmek için <a href="https://www.starlette.io/responses/#set-cookie" class="external-link" target="_blank">Starlette dokümantasyonunu</a> incelleyin.
