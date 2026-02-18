# Özel Response - HTML, Stream, File ve Diğerleri { #custom-response-html-stream-file-others }

Varsayılan olarak **FastAPI**, response'ları `JSONResponse` kullanarak döndürür.

Bunu, [Doğrudan bir Response döndür](response-directly.md){.internal-link target=_blank} bölümünde gördüğünüz gibi doğrudan bir `Response` döndürerek geçersiz kılabilirsiniz.

Ancak doğrudan bir `Response` döndürürseniz (veya `JSONResponse` gibi herhangi bir alt sınıfını), veri otomatik olarak dönüştürülmez (bir `response_model` tanımlamış olsanız bile) ve dokümantasyon da otomatik üretilmez (örneğin, üretilen OpenAPI’nin parçası olarak HTTP header `Content-Type` içindeki ilgili "media type" dahil edilmez).

Bununla birlikte, *path operation decorator* içinde `response_class` parametresini kullanarak hangi `Response`’un (örn. herhangi bir `Response` alt sınıfı) kullanılacağını da ilan edebilirsiniz.

*path operation function*’ınızdan döndürdüğünüz içerik, o `Response`’un içine yerleştirilir.

Ve eğer bu `Response` ( `JSONResponse` ve `UJSONResponse`’ta olduğu gibi) bir JSON media type’a (`application/json`) sahipse, döndürdüğünüz veri; *path operation decorator* içinde tanımladığınız herhangi bir Pydantic `response_model` ile otomatik olarak dönüştürülür (ve filtrelenir).

/// note | Not

Media type’ı olmayan bir response class kullanırsanız, FastAPI response’unuzun content içermediğini varsayar; bu yüzden ürettiği OpenAPI dokümanında response formatını dokümante etmez.

///

## `ORJSONResponse` Kullan { #use-orjsonresponse }

Örneğin performansı sıkıştırmaya çalışıyorsanız, <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> kurup kullanabilir ve response’u `ORJSONResponse` olarak ayarlayabilirsiniz.

Kullanmak istediğiniz `Response` class’ını (alt sınıfını) import edin ve *path operation decorator* içinde tanımlayın.

Büyük response'larda, doğrudan bir `Response` döndürmek bir dictionary döndürmekten çok daha hızlıdır.

Çünkü varsayılan olarak FastAPI, içindeki her item’ı inceleyip JSON olarak serialize edilebilir olduğundan emin olur; tutorial’da anlatılan aynı [JSON Compatible Encoder](../tutorial/encoder.md){.internal-link target=_blank} mekanizmasını kullanır. Bu da örneğin veritabanı modelleri gibi **keyfi objeleri** döndürebilmenizi sağlar.

Ancak döndürdüğünüz içeriğin **JSON ile serialize edilebilir** olduğundan eminseniz, onu doğrudan response class’ına verebilir ve FastAPI’nin response class’ına vermeden önce dönüş içeriğinizi `jsonable_encoder` içinden geçirirken oluşturacağı ek yükten kaçınabilirsiniz.

{* ../../docs_src/custom_response/tutorial001b_py310.py hl[2,7] *}

/// info | Bilgi

`response_class` parametresi, response’un "media type"’ını tanımlamak için de kullanılır.

Bu durumda HTTP header `Content-Type`, `application/json` olarak ayarlanır.

Ve OpenAPI’de de bu şekilde dokümante edilir.

///

/// tip | İpucu

`ORJSONResponse` yalnızca FastAPI’de vardır, Starlette’te yoktur.

///

## HTML Response { #html-response }

**FastAPI**’den doğrudan HTML içeren bir response döndürmek için `HTMLResponse` kullanın.

* `HTMLResponse` import edin.
* *path operation decorator*’ınızın `response_class` parametresi olarak `HTMLResponse` verin.

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// info | Bilgi

`response_class` parametresi, response’un "media type"’ını tanımlamak için de kullanılır.

Bu durumda HTTP header `Content-Type`, `text/html` olarak ayarlanır.

Ve OpenAPI’de de bu şekilde dokümante edilir.

///

### Bir `Response` Döndür { #return-a-response }

[Doğrudan bir Response döndür](response-directly.md){.internal-link target=_blank} bölümünde görüldüğü gibi, *path operation* içinde doğrudan bir response döndürerek response’u override edebilirsiniz.

Yukarıdaki örneğin aynısı, bu sefer bir `HTMLResponse` döndürerek, şöyle görünebilir:

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning | Uyarı

*path operation function*’ınızın doğrudan döndürdüğü bir `Response`, OpenAPI’de dokümante edilmez (örneğin `Content-Type` dokümante edilmez) ve otomatik interaktif dokümanlarda görünmez.

///

/// info | Bilgi

Elbette gerçek `Content-Type` header’ı, status code vb. değerler, döndürdüğünüz `Response` objesinden gelir.

///

### OpenAPI’de Dokümante Et ve `Response`’u Override Et { #document-in-openapi-and-override-response }

Response’u fonksiyonun içinden override etmek ama aynı zamanda OpenAPI’de "media type"’ı dokümante etmek istiyorsanız, `response_class` parametresini kullanıp ayrıca bir `Response` objesi döndürebilirsiniz.

Bu durumda `response_class` sadece OpenAPI *path operation*’ını dokümante etmek için kullanılır; sizin `Response`’unuz ise olduğu gibi kullanılır.

#### Doğrudan bir `HTMLResponse` Döndür { #return-an-htmlresponse-directly }

Örneğin şöyle bir şey olabilir:

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

Bu örnekte `generate_html_response()` fonksiyonu, HTML’i bir `str` olarak döndürmek yerine zaten bir `Response` üretip döndürmektedir.

`generate_html_response()` çağrısının sonucunu döndürerek, varsayılan **FastAPI** davranışını override edecek bir `Response` döndürmüş olursunuz.

Ama `response_class` içinde `HTMLResponse` da verdiğiniz için **FastAPI**, bunu OpenAPI’de ve interaktif dokümanlarda `text/html` ile HTML olarak nasıl dokümante edeceğini bilir:

<img src="/img/tutorial/custom-response/image01.png">

## Mevcut Response'lar { #available-responses }

Mevcut response'lardan bazıları aşağıdadır.

Unutmayın: `Response` ile başka herhangi bir şeyi döndürebilir, hatta özel bir alt sınıf da oluşturabilirsiniz.

/// note | Teknik Detaylar

`from starlette.responses import HTMLResponse` da kullanabilirsiniz.

**FastAPI**, geliştirici için kolaylık olsun diye `starlette.responses` içindekileri `fastapi.responses` olarak da sağlar. Ancak mevcut response'ların çoğu doğrudan Starlette’ten gelir.

///

### `Response` { #response }

Ana `Response` class’ıdır; diğer tüm response'lar bundan türetilir.

Bunu doğrudan döndürebilirsiniz.

Şu parametreleri kabul eder:

* `content` - Bir `str` veya `bytes`.
* `status_code` - Bir `int` HTTP status code.
* `headers` - String’lerden oluşan bir `dict`.
* `media_type` - Media type’ı veren bir `str`. Örn. `"text/html"`.

FastAPI (aslında Starlette) otomatik olarak bir Content-Length header’ı ekler. Ayrıca `media_type`’a göre bir Content-Type header’ı ekler ve text türleri için sona bir charset ekler.

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

Yukarıda okuduğunuz gibi, bir miktar text veya bytes alır ve HTML response döndürür.

### `PlainTextResponse` { #plaintextresponse }

Bir miktar text veya bytes alır ve düz metin response döndürür.

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

Bir miktar veri alır ve `application/json` olarak encode edilmiş bir response döndürür.

Yukarıda okuduğunuz gibi, **FastAPI**’de varsayılan response budur.

### `ORJSONResponse` { #orjsonresponse }

Yukarıda okuduğunuz gibi <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> kullanan hızlı bir alternatif JSON response.

/// info | Bilgi

Bunun için `orjson` kurulmalıdır; örneğin `pip install orjson`.

///

### `UJSONResponse` { #ujsonresponse }

<a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a> kullanan alternatif bir JSON response.

/// info | Bilgi

Bunun için `ujson` kurulmalıdır; örneğin `pip install ujson`.

///

/// warning | Uyarı

`ujson`, bazı edge-case’leri ele alma konusunda Python’un built-in implementasyonu kadar dikkatli değildir.

///

{* ../../docs_src/custom_response/tutorial001_py310.py hl[2,7] *}

/// tip | İpucu

`ORJSONResponse` daha hızlı bir alternatif olabilir.

///

### `RedirectResponse` { #redirectresponse }

HTTP redirect döndürür. Varsayılan olarak 307 status code (Temporary Redirect) kullanır.

`RedirectResponse`’u doğrudan döndürebilirsiniz:

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

Veya `response_class` parametresi içinde kullanabilirsiniz:

{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

Bunu yaparsanız, *path operation* function’ınızdan doğrudan URL döndürebilirsiniz.

Bu durumda kullanılan `status_code`, `RedirectResponse` için varsayılan olan `307` olur.

---

Ayrıca `status_code` parametresini `response_class` parametresiyle birlikte kullanabilirsiniz:

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

Bir async generator veya normal generator/iterator alır ve response body’yi stream eder.

{* ../../docs_src/custom_response/tutorial007_py310.py hl[2,14] *}

#### `StreamingResponse`’u file-like objelerle kullanma { #using-streamingresponse-with-file-like-objects }

Bir <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> objeniz varsa (örn. `open()`’ın döndürdüğü obje), o file-like obje üzerinde iterate eden bir generator function oluşturabilirsiniz.

Böylece önce hepsini memory’ye okumak zorunda kalmazsınız; bu generator function’ı `StreamingResponse`’a verip döndürebilirsiniz.

Buna cloud storage ile etkileşime giren, video işleyen ve benzeri birçok kütüphane dahildir.

{* ../../docs_src/custom_response/tutorial008_py310.py hl[2,10:12,14] *}

1. Bu generator function’dır. İçinde `yield` ifadeleri olduğu için "generator function" denir.
2. Bir `with` bloğu kullanarak, generator function bittiğinde file-like objenin kapandığından emin oluruz. Yani response göndermeyi bitirdikten sonra kapanır.
3. Bu `yield from`, fonksiyona `file_like` isimli şeyi iterate etmesini söyler. Ardından iterate edilen her parça için, o parçayı bu generator function’dan (`iterfile`) geliyormuş gibi yield eder.

    Yani, içerdeki "üretme" (generating) işini başka bir şeye devreden bir generator function’dır.

    Bunu bu şekilde yaptığımızda `with` bloğu içinde tutabilir ve böylece iş bitince file-like objenin kapanmasını garanti edebiliriz.

/// tip | İpucu

Burada `async` ve `await` desteklemeyen standart `open()` kullandığımız için path operation’ı normal `def` ile tanımlarız.

///

### `FileResponse` { #fileresponse }

Asenkron olarak bir dosyayı response olarak stream eder.

Diğer response türlerine göre instantiate ederken farklı argümanlar alır:

* `path` - Stream edilecek dosyanın dosya path'i.
* `headers` - Eklenecek özel header’lar; dictionary olarak.
* `media_type` - Media type’ı veren string. Ayarlanmazsa, dosya adı veya path kullanılarak media type tahmin edilir.
* `filename` - Ayarlanırsa response içindeki `Content-Disposition`’a dahil edilir.

File response'ları uygun `Content-Length`, `Last-Modified` ve `ETag` header’larını içerir.

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

`response_class` parametresini de kullanabilirsiniz:

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

Bu durumda *path operation* function’ınızdan doğrudan dosya path'ini döndürebilirsiniz.

## Özel response class { #custom-response-class }

`Response`’dan türeterek kendi özel response class’ınızı oluşturabilir ve kullanabilirsiniz.

Örneğin, dahil gelen `ORJSONResponse` class’ında kullanılmayan bazı özel ayarlarla <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> kullanmak istediğinizi varsayalım.

Diyelim ki girintili ve biçimlendirilmiş JSON döndürmek istiyorsunuz; bunun için `orjson.OPT_INDENT_2` seçeneğini kullanmak istiyorsunuz.

Bir `CustomORJSONResponse` oluşturabilirsiniz. Burada yapmanız gereken temel şey, content’i `bytes` olarak döndüren bir `Response.render(content)` metodu yazmaktır:

{* ../../docs_src/custom_response/tutorial009c_py310.py hl[9:14,17] *}

Artık şunu döndürmek yerine:

```json
{"message": "Hello World"}
```

...bu response şunu döndürür:

```json
{
  "message": "Hello World"
}
```

Elbette JSON’u formatlamaktan çok daha iyi şekillerde bundan faydalanabilirsiniz. 😉

## Varsayılan response class { #default-response-class }

Bir **FastAPI** class instance’ı veya bir `APIRouter` oluştururken, varsayılan olarak hangi response class’ının kullanılacağını belirtebilirsiniz.

Bunu tanımlayan parametre `default_response_class`’tır.

Aşağıdaki örnekte **FastAPI**, tüm *path operations* için varsayılan olarak `JSONResponse` yerine `ORJSONResponse` kullanır.

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | İpucu

Daha önce olduğu gibi, *path operations* içinde `response_class`’ı yine override edebilirsiniz.

///

## Ek dokümantasyon { #additional-documentation }

OpenAPI’de media type’ı ve daha birçok detayı `responses` kullanarak da tanımlayabilirsiniz: [OpenAPI’de Ek Response'lar](additional-responses.md){.internal-link target=_blank}.
