# Doğrudan Bir Yanıt Döndürme

Bir **FastAPI** *yol operasyonu* oluşturduğunuzda bir `dict`, bir `list`, bir Pydantic modeli, bir veritabanı modeli vb. gibi herhangi bir veriyi döndürebilirsiniz.

**FastAPI** varsayılan olarak, döndürülen bu değeri [JSON Compatible Encoder](../tutorial/encoder.md){.internal-link target=_blank} sayfasında açıklanan `jsonable_encoder`'ı kullanarak JSON'a otomatik olarak dönüştürür.

Arka planda, bu JSON uyumlu veriyi (örneğin bir `dict`) bir `JSONResponse` içine koyar ve bu, yanıtı istemciye göndermek için kullanılır.

Ancak *yol operasyonları*nda doğrudan bir `JSONResponse` döndürebilirsiniz.

Bu kullanım kullanışlı olabilir, örneğin özel başlıklar veya çerezler döndürmek için.

## Bir `Response` Döndürme

Aslında herhangi bir `Response`'ı veya onun herhangi bir alt sınıfını döndürebilirsiniz.

!!! tip "İpucu"
    `JSONResponse` sınıfı, `Response` sınıfının bir alt sınıfıdır.

Bir `Response` döndürdüğünüzde, **FastAPI** bu yanıtı doğrudan döndürülecektir.

Bu yanıt herhangi bir pydantic modeliyle dönüştürülme işlemine tabi tutulmayacaktır ve hiçbir içeriği herhangi bir türe dönüştürmeyecektir.

Bu sayede çok esnek bir şekilde çalışabilirsiniz. Herhangi bir veri türünü döndürebilir, herhangi bir veri tanımlamasını veya doğrulamasını geçersiz kılabilirsiniz, vb.

## Bir `Response` İçinde `jsonable_encoder`'ı Kullanma

**FastAPI** herhangi bir dönüşüm yapmadığı için, döndürdüğünüz `Response`'ın içeriğinin buna hazır olduğundan emin olmalısınız.

Mesela, bir Pydantic modelini, içindeki tüm veri türlerini (örneğin `datetime`, `UUID`, vb.) JSON uyumlu türlere dönüştürerek bir `dict` içine koymadan bir `JSONResponse` içinde kullanamazsınız.

Bu durumlar için, verinizi bir yanıta geçirmeden önce dönüştürmek için `jsonable_encoder`'ı kullanabilirsiniz:

```Python hl_lines="6-7  21-22"
{!../../../docs_src/response_directly/tutorial001.py!}
```

!!! note "Teknik Detaylar"
    Projenize dahil etmek için `from starlette.responses import JSONResponse` kullanabilirsiniz.

    **FastAPI**, geliştiricilere kolaylık sağlamak amacıyla `starlette.responses`'ı `fastapi.responses` olarak sağlar. Ancak mevcut yanıtların çoğu doğrudan Starlette'den gelir.

## Özelleştirilmiş Bir `Response` Döndürme

Yukarıdaki örnek, ihtiyacınız olan her şeyi açıklıyor ancak henüz çok kullanışlı değil, çünkü `item`'ı doğrudan döndürebilir ve **FastAPI** bunu sizin için bir `dict`'e dönüştürerek `JSONResponse` içine koyabilir, vb. Tüm bunlar varsayılan olarak yapılır.

Şimdi, özelleştirilmiş bir yanıt döndürmek için `Response`'ı nasıl kullanabileceğinizi görelim.

Diyelim ki bir <a href="https://en.wikipedia.org/wiki/XML" class="external-link" target="_blank">XML</a> yanıtı döndürmek istiyorsunuz.

Bu XML içeriğinizi bir `string` içine koyabilir ve bu `string`'i bir `Response` içine koyarak döndürebilirsiniz:

```Python hl_lines="1  18"
{!../../../docs_src/response_directly/tutorial002.py!}
```

## Notlar

Doğrudan bir `Response` döndürdüğünüzde, veriniz otomatik olarak doğrulanmaz, dönüştürülmez (serileştirilmez) ve dokümantasyonu yapılmaz.

Ancak, [Additional Responses in OpenAPI](additional-responses.md){.internal-link target=_blank} sayfasında açıklandığı gibi dokümantasyonunu yapabilirsiniz

İlerleyen bölümlerde, bu özel `Response`'ları kullanırken otomatik veri dönüşümü, dokümantasyon vb. özelliklere sahip olabileceğinizi görebilirsiniz.
