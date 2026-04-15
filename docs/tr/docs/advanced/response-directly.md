# Doğrudan Bir Response Döndürme { #return-a-response-directly }

**FastAPI** ile bir *path operation* oluşturduğunuzda, normalde ondan herhangi bir veri döndürebilirsiniz: bir `dict`, bir `list`, bir Pydantic model, bir veritabanı modeli vb.

Bir [Response Model](../tutorial/response-model.md) deklare ederseniz, FastAPI veriyi Pydantic kullanarak JSON'a serialize etmek için bunu kullanır.

Bir response model deklare etmezseniz, FastAPI [JSON Uyumlu Encoder](../tutorial/encoder.md)'da anlatılan `jsonable_encoder`'ı kullanır ve bunu bir `JSONResponse` içine koyar.

Ayrıca doğrudan bir `JSONResponse` oluşturup döndürebilirsiniz.

/// tip | İpucu

[Response Model](../tutorial/response-model.md) kullanmak, doğrudan `JSONResponse` döndürmeye kıyasla genellikle çok daha iyi performans sağlar; çünkü veriyi Pydantic ile, Rust tarafında serialize eder.

///

## Bir `Response` Döndürme { #return-a-response }

Aslında herhangi bir `Response` veya onun herhangi bir alt sınıfını döndürebilirsiniz.

/// info | Bilgi

`JSONResponse` zaten `Response`'un bir alt sınıfıdır.

///

Bir `Response` döndürdüğünüzde, **FastAPI** bunu olduğu gibi doğrudan iletir.

Pydantic model'leriyle herhangi bir veri dönüşümü yapmaz, içeriği başka bir tipe çevirmez vb.

Bu size ciddi bir esneklik sağlar. Herhangi bir veri türü döndürebilir, herhangi bir veri deklarasyonunu veya validasyonunu override edebilirsiniz.

Bu aynı zamanda size ciddi bir sorumluluk yükler. Döndürdüğünüz verinin doğru, doğru formatta, serialize edilebilir vb. olduğundan emin olmanız gerekir.

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

Diyelim ki [XML](https://en.wikipedia.org/wiki/XML) response döndürmek istiyorsunuz.

XML içeriğinizi bir string içine koyabilir, onu bir `Response` içine yerleştirip döndürebilirsiniz:

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## Bir Response Model Nasıl Çalışır { #how-a-response-model-works }

Bir path operation içinde [Response Model - Dönüş Tipi](../tutorial/response-model.md) deklare ettiğinizde, **FastAPI** veriyi Pydantic kullanarak JSON'a serialize etmek için bunu kullanır.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

Bu işlem Rust tarafında gerçekleştiği için, sıradan Python ve `JSONResponse` sınıfıyla yapılmasına kıyasla performans çok daha iyi olacaktır.

Bir `response_model` veya dönüş tipi kullandığınızda, FastAPI veriyi dönüştürmek için (daha yavaş olacağı için) `jsonable_encoder`'ı ya da `JSONResponse` sınıfını kullanmaz.

Bunun yerine, response model'i (veya dönüş tipini) kullanarak Pydantic ile üretilen JSON baytlarını alır ve doğrudan JSON için doğru medya tipiyle (`application/json`) bir `Response` döndürür.

## Notlar { #notes }

Bir `Response`'u doğrudan döndürdüğünüzde, verisi otomatik olarak validate edilmez, dönüştürülmez (serialize edilmez) veya dokümante edilmez.

Ancak yine de [OpenAPI'de Ek Response'lar](additional-responses.md) bölümünde anlatıldığı şekilde dokümante edebilirsiniz.

İlerleyen bölümlerde, otomatik veri dönüşümü, dokümantasyon vb. özellikleri korurken bu özel `Response`'ları nasıl kullanıp declare edebileceğinizi göreceksiniz.
