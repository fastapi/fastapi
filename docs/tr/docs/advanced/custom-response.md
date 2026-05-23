# Özel Response - HTML, Stream, File ve Diğerleri { #custom-response-html-stream-file-others }

Varsayılan olarak **FastAPI**, JSON response'lar döndürür.

Bunu, [Doğrudan bir Response döndür](response-directly.md) bölümünde gördüğünüz gibi doğrudan bir `Response` döndürerek geçersiz kılabilirsiniz.

Ancak doğrudan bir `Response` döndürürseniz (veya `JSONResponse` gibi herhangi bir alt sınıfını), veri otomatik olarak dönüştürülmez (bir `response_model` tanımlamış olsanız bile) ve dokümantasyon da otomatik üretilmez (örneğin, üretilen OpenAPI’nin parçası olarak HTTP header `Content-Type` içindeki ilgili "media type" dahil edilmez).

Bununla birlikte, *path operation decorator* içinde `response_class` parametresini kullanarak hangi `Response`’un (örn. herhangi bir `Response` alt sınıfı) kullanılacağını da ilan edebilirsiniz.

*path operation function*’ınızdan döndürdüğünüz içerik, o `Response`’un içine yerleştirilir.

/// note | Not

Media type’ı olmayan bir response class kullanırsanız, FastAPI response’unuzun content içermediğini varsayar; bu yüzden ürettiği OpenAPI dokümanında response formatını dokümante etmez.

///

## JSON Response'lar { #json-responses }

Varsayılan olarak FastAPI JSON response'lar döndürür.

Bir [Response Model](../tutorial/response-model.md) tanımlarsanız, FastAPI veriyi Pydantic kullanarak JSON’a serialize eder.

Bir response modeli tanımlamazsanız, FastAPI [JSON Compatible Encoder](../tutorial/encoder.md) bölümünde açıklanan `jsonable_encoder`’ı kullanır ve sonucu bir `JSONResponse` içine koyar.

`JSONResponse` örneğinde olduğu gibi JSON media type’ına (`application/json`) sahip bir `response_class` tanımlarsanız, döndürdüğünüz veri; *path operation decorator* içinde tanımladığınız herhangi bir Pydantic `response_model` ile otomatik olarak dönüştürülür (ve filtrelenir). Ancak veri Pydantic ile JSON bytes’a serialize edilmez; bunun yerine `jsonable_encoder` ile dönüştürülür ve ardından Python’un standart JSON kütüphanesini kullanarak bytes’a serialize edecek olan `JSONResponse` class’ına iletilir.

### JSON Performansı { #json-performance }

Kısaca, en yüksek performansı istiyorsanız bir [Response Model](../tutorial/response-model.md) kullanın ve *path operation decorator* içinde `response_class` tanımlamayın.

{* ../../docs_src/response_model/tutorial001_01_py310.py ln[15:17] hl[16] *}

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

[Doğrudan bir Response döndür](response-directly.md) bölümünde görüldüğü gibi, *path operation* içinde doğrudan bir response döndürerek response’u override edebilirsiniz.

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

/// note | Teknik Detaylar

Ancak bir response modeli veya dönüş tipi (return type) tanımlarsanız, veri doğrudan JSON’a serialize edilir ve JSON için doğru media type’a sahip bir response, `JSONResponse` class’ı kullanılmadan doğrudan döndürülür.

Bu, en iyi performansı elde etmenin ideal yoludur.

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

Bir async generator veya normal generator/iterator (içinde `yield` olan bir fonksiyon) alır ve response body’yi stream eder.

{* ../../docs_src/custom_response/tutorial007_py310.py hl[3,16] *}

/// note | Teknik Detaylar

Bir `async` görev, yalnızca bir `await` noktasına geldiğinde iptal edilebilir. Eğer hiç `await` yoksa, generator (içinde `yield` olan fonksiyon) düzgün şekilde iptal edilemez ve iptal istendikten sonra bile çalışmaya devam edebilir.

Bu küçük örneğin `await` ifadesine ihtiyacı olmadığı için, event loop’un iptali ele alabilmesi adına `await anyio.sleep(0)` ekliyoruz.

Büyük veya sonsuz akışlarda bu daha da önemlidir.

///

/// tip | İpucu

Doğrudan bir `StreamingResponse` döndürmek yerine, muhtemelen [Veri Stream Etme](./stream-data.md) bölümündeki tarzı takip etmelisiniz; çok daha kullanışlıdır ve iptali arka planda sizin için halleder.

JSON Lines stream ediyorsanız, [JSON Lines Stream Etme](../tutorial/stream-json-lines.md) kılavuzunu izleyin.

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

Örneğin, bazı ayarlarla [`orjson`](https://github.com/ijl/orjson) kullanmak istediğinizi varsayalım.

Diyelim ki girintili ve biçimlendirilmiş JSON döndürmek istiyorsunuz; bunun için orjson seçeneği `orjson.OPT_INDENT_2`’yi kullanmak istiyorsunuz.

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

### `orjson` mı Response Model mi { #orjson-or-response-model }

Aradığınız şey performans ise, büyük olasılıkla bir `orjson` response’tan ziyade bir [Response Model](../tutorial/response-model.md) kullanmak daha iyi olacaktır.

Bir response modeliyle FastAPI, veriyi JSON’a serialize etmek için Pydantic’i kullanır; böylece diğer durumlarda olacağı gibi `jsonable_encoder` ile ara dönüşümlere gerek kalmaz.

Ve kaputun altında, Pydantic JSON’a serialize etmek için `orjson` ile aynı Rust tabanlı mekanizmaları kullanır; bu nedenle bir response modeliyle zaten en iyi performansı elde edersiniz.

## Varsayılan response class { #default-response-class }

Bir **FastAPI** class instance’ı veya bir `APIRouter` oluştururken, varsayılan olarak hangi response class’ının kullanılacağını belirtebilirsiniz.

Bunu tanımlayan parametre `default_response_class`’tır.

Aşağıdaki örnekte **FastAPI**, tüm *path operations* için varsayılan olarak JSON yerine `HTMLResponse` kullanır.

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | İpucu

Daha önce olduğu gibi, *path operations* içinde `response_class`’ı yine override edebilirsiniz.

///

## Ek dokümantasyon { #additional-documentation }

OpenAPI’de media type’ı ve daha birçok detayı `responses` kullanarak da tanımlayabilirsiniz: [OpenAPI’de Ek Response'lar](additional-responses.md).
