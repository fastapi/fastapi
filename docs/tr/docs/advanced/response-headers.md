# Response Header'ları { #response-headers }

## Bir `Response` parametresi kullanın { #use-a-response-parameter }

*Path operation function* içinde (cookie'lerde yapabildiğiniz gibi) tipi `Response` olan bir parametre tanımlayabilirsiniz.

Sonra da bu *geçici* response nesnesi üzerinde header'ları ayarlayabilirsiniz.

{* ../../docs_src/response_headers/tutorial002_py310.py hl[1, 7:8] *}

Ardından normalde yaptığınız gibi ihtiyacınız olan herhangi bir nesneyi döndürebilirsiniz (bir `dict`, bir veritabanı modeli vb.).

Eğer bir `response_model` tanımladıysanız, döndürdüğünüz nesneyi filtrelemek ve dönüştürmek için yine kullanılacaktır.

**FastAPI**, header'ları (aynı şekilde cookie'leri ve status code'u) bu *geçici* response'dan alır ve döndürdüğünüz değeri (varsa bir `response_model` ile filtrelenmiş hâliyle) içeren nihai response'a ekler.

`Response` parametresini dependency'lerde de tanımlayıp, onların içinde header (ve cookie) ayarlayabilirsiniz.

## Doğrudan bir `Response` döndürün { #return-a-response-directly }

Doğrudan bir `Response` döndürdüğünüzde de header ekleyebilirsiniz.

[Bir Response'u Doğrudan Döndürün](response-directly.md){.internal-link target=_blank} bölümünde anlatıldığı gibi bir response oluşturun ve header'ları ek bir parametre olarak geçin:

{* ../../docs_src/response_headers/tutorial001_py310.py hl[10:12] *}

/// note | Teknik Detaylar

`from starlette.responses import Response` veya `from starlette.responses import JSONResponse` da kullanabilirsiniz.

**FastAPI**, geliştirici olarak size kolaylık olsun diye `starlette.responses` içeriğini `fastapi.responses` olarak da sunar. Ancak mevcut response'ların çoğu doğrudan Starlette'ten gelir.

Ayrıca `Response` header ve cookie ayarlamak için sık kullanıldığından, **FastAPI** bunu `fastapi.Response` altında da sağlar.

///

## Özel Header'lar { #custom-headers }

Özel/proprietary header'ların <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">`X-` prefix'i kullanılarak</a> eklenebileceğini unutmayın.

Ancak tarayıcıdaki bir client'ın görebilmesini istediğiniz özel header'larınız varsa, bunları CORS ayarlarınıza eklemeniz gerekir ([CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md){.internal-link target=_blank} bölümünde daha fazla bilgi), bunun için <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette'in CORS dokümanında</a> açıklanan `expose_headers` parametresini kullanın.
