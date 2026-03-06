# Response Cookie'leri { #response-cookies }

## Bir `Response` parametresi kullanın { #use-a-response-parameter }

*Path operation function* içinde `Response` tipinde bir parametre tanımlayabilirsiniz.

Ardından bu *geçici* response nesnesi üzerinde cookie'leri set edebilirsiniz.

{* ../../docs_src/response_cookies/tutorial002_py310.py hl[1, 8:9] *}

Sonrasında normalde yaptığınız gibi ihtiyaç duyduğunuz herhangi bir nesneyi döndürebilirsiniz (bir `dict`, bir veritabanı modeli vb.).

Ayrıca bir `response_model` tanımladıysanız, döndürdüğünüz nesneyi filtrelemek ve dönüştürmek için yine kullanılacaktır.

**FastAPI**, bu *geçici* response'u cookie'leri (ayrıca header'ları ve status code'u) çıkarmak için kullanır ve bunları, döndürdüğünüz değeri içeren nihai response'a ekler. Döndürdüğünüz değer, varsa `response_model` ile filtrelenmiş olur.

`Response` parametresini dependency'lerde de tanımlayıp, onların içinde cookie (ve header) set edebilirsiniz.

## Doğrudan bir `Response` döndürün { #return-a-response-directly }

Kodunuzda doğrudan bir `Response` döndürürken de cookie oluşturabilirsiniz.

Bunu yapmak için, [Doğrudan Response Döndürme](response-directly.md){.internal-link target=_blank} bölümünde anlatıldığı gibi bir response oluşturabilirsiniz.

Sonra bunun içinde Cookie'leri set edin ve response'u döndürün:

{* ../../docs_src/response_cookies/tutorial001_py310.py hl[10:12] *}

/// tip

`Response` parametresini kullanmak yerine doğrudan bir response döndürürseniz, FastAPI onu olduğu gibi (doğrudan) döndürür.

Bu yüzden, verinizin doğru tipte olduğundan emin olmanız gerekir. Örneğin `JSONResponse` döndürüyorsanız, verinin JSON ile uyumlu olması gerekir.

Ayrıca `response_model` tarafından filtrelenmesi gereken bir veriyi göndermediğinizden de emin olun.

///

### Daha fazla bilgi { #more-info }

/// note | Teknik Detaylar

`from starlette.responses import Response` veya `from starlette.responses import JSONResponse` da kullanabilirsiniz.

**FastAPI**, geliştirici olarak size kolaylık olması için `fastapi.responses` içinde `starlette.responses` ile aynı response sınıflarını sunar. Ancak mevcut response'ların büyük kısmı doğrudan Starlette'ten gelir.

Ve `Response`, header ve cookie set etmek için sık kullanıldığından, **FastAPI** bunu `fastapi.Response` olarak da sağlar.

///

Mevcut tüm parametreleri ve seçenekleri görmek için <a href="https://www.starlette.dev/responses/#set-cookie" class="external-link" target="_blank">Starlette dokümantasyonuna</a> bakın.
