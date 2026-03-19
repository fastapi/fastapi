# Doğrudan Bir Response Döndürme { #return-a-response-directly }

**FastAPI** ile bir *path operation* oluşturduğunuzda, normalde ondan herhangi bir veri döndürebilirsiniz: bir `dict`, bir `list`, bir Pydantic model, bir veritabanı modeli vb.

Varsayılan olarak **FastAPI**, döndürdüğünüz bu değeri [JSON Uyumlu Encoder](../tutorial/encoder.md){.internal-link target=_blank} bölümünde anlatılan `jsonable_encoder` ile otomatik olarak JSON'a çevirir.

Ardından perde arkasında, JSON-uyumlu bu veriyi (ör. bir `dict`) client'a response göndermek için kullanılacak bir `JSONResponse` içine yerleştirir.

Ancak *path operation*'larınızdan doğrudan bir `JSONResponse` döndürebilirsiniz.

Bu, örneğin özel header'lar veya cookie'ler döndürmek istediğinizde faydalı olabilir.

## Bir `Response` Döndürme { #return-a-response }

Aslında herhangi bir `Response` veya onun herhangi bir alt sınıfını döndürebilirsiniz.

/// tip | İpucu

`JSONResponse` zaten `Response`'un bir alt sınıfıdır.

///

Bir `Response` döndürdüğünüzde, **FastAPI** bunu olduğu gibi doğrudan iletir.

Pydantic model'leriyle herhangi bir veri dönüşümü yapmaz, içeriği başka bir tipe çevirmez vb.

Bu size ciddi bir esneklik sağlar. Herhangi bir veri türü döndürebilir, herhangi bir veri deklarasyonunu veya validasyonunu override edebilirsiniz.

## Bir `Response` İçinde `jsonable_encoder` Kullanma { #using-the-jsonable-encoder-in-a-response }

**FastAPI**, sizin döndürdüğünüz `Response` üzerinde hiçbir değişiklik yapmadığı için, içeriğinin gönderilmeye hazır olduğundan emin olmanız gerekir.

Örneğin, bir Pydantic model'i, önce JSON-uyumlu tiplere çevrilmeden (`datetime`, `UUID` vb.) doğrudan bir `JSONResponse` içine koyamazsınız. Önce tüm veri tipleri JSON-uyumlu hale gelecek şekilde `dict`'e çevrilmesi gerekir.

Bu gibi durumlarda, response'a vermeden önce verinizi dönüştürmek için `jsonable_encoder` kullanabilirsiniz:

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | Teknik Detaylar

`from starlette.responses import JSONResponse` da kullanabilirsiniz.

**FastAPI**, geliştirici olarak size kolaylık olması için `starlette.responses` içeriğini `fastapi.responses` üzerinden de sunar. Ancak mevcut response'ların çoğu doğrudan Starlette'tan gelir.

///

## Özel Bir `Response` Döndürme { #returning-a-custom-response }

Yukarıdaki örnek ihtiyaç duyduğunuz tüm parçaları gösteriyor, ancak henüz çok kullanışlı değil. Çünkü `item`'ı zaten doğrudan döndürebilirdiniz ve **FastAPI** varsayılan olarak onu sizin için bir `JSONResponse` içine koyup `dict`'e çevirirdi vb.

Şimdi bunu kullanarak nasıl özel bir response döndürebileceğinize bakalım.

Diyelim ki <a href="https://en.wikipedia.org/wiki/XML" class="external-link" target="_blank">XML</a> response döndürmek istiyorsunuz.

XML içeriğinizi bir string içine koyabilir, onu bir `Response` içine yerleştirip döndürebilirsiniz:

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## Notlar { #notes }

Bir `Response`'u doğrudan döndürdüğünüzde, verisi otomatik olarak validate edilmez, dönüştürülmez (serialize edilmez) veya dokümante edilmez.

Ancak yine de [OpenAPI'de Ek Response'lar](additional-responses.md){.internal-link target=_blank} bölümünde anlatıldığı şekilde dokümante edebilirsiniz.

İlerleyen bölümlerde, otomatik veri dönüşümü, dokümantasyon vb. özellikleri korurken bu özel `Response`'ları nasıl kullanıp declare edebileceğinizi göreceksiniz.
