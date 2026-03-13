# Hataları Yönetme { #handling-errors }

API’nizi kullanan bir client’a hata bildirmek zorunda olduğunuz pek çok durum vardır.

Bu client; frontend’i olan bir tarayıcı, başka birinin yazdığı bir kod, bir IoT cihazı vb. olabilir.

Client’a şunları söylemeniz gerekebilir:

* Client’ın bu işlem için yeterli yetkisi yok.
* Client’ın bu kaynağa erişimi yok.
* Client’ın erişmeye çalıştığı öğe mevcut değil.
* vb.

Bu durumlarda genellikle **400** aralığında (**400** ile **499** arası) bir **HTTP status code** döndürürsünüz.

Bu, 200 HTTP status code’larına (200 ile 299 arası) benzer. Bu "200" status code’ları, request’in bir şekilde "başarılı" olduğunu ifade eder.

400 aralığındaki status code’lar ise hatanın client tarafından kaynaklandığını gösterir.

Şu meşhur **"404 Not Found"** hatalarını (ve şakalarını) hatırlıyor musunuz?

## `HTTPException` Kullanma { #use-httpexception }

Client’a hata içeren HTTP response’ları döndürmek için `HTTPException` kullanırsınız.

### `HTTPException`’ı Import Etme { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[1] *}

### Kodunuzda Bir `HTTPException` Raise Etme { #raise-an-httpexception-in-your-code }

`HTTPException`, API’lerle ilgili ek veriler içeren normal bir Python exception’ıdır.

Python exception’ı olduğu için `return` etmezsiniz, `raise` edersiniz.

Bu aynı zamanda şunu da ifade eder: *path operation function*’ınızın içinde çağırdığınız bir yardımcı (utility) fonksiyonun içindeyken `HTTPException` raise ederseniz, *path operation function* içindeki kodun geri kalanı çalışmaz; request’i hemen sonlandırır ve `HTTPException` içindeki HTTP hatasını client’a gönderir.

Bir değer döndürmek yerine exception raise etmenin faydası, Dependencies ve Security bölümünde daha da netleşecektir.

Bu örnekte, client var olmayan bir ID ile bir item istediğinde, `404` status code’u ile bir exception raise edelim:

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[11] *}

### Ortaya Çıkan Response { #the-resulting-response }

Client `http://example.com/items/foo` (bir `item_id` `"foo"`) isterse, HTTP status code olarak 200 ve şu JSON response’u alır:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

Ancak client `http://example.com/items/bar` (mevcut olmayan bir `item_id` `"bar"`) isterse, HTTP status code olarak 404 ("not found" hatası) ve şu JSON response’u alır:

```JSON
{
  "detail": "Item not found"
}
```

/// tip | İpucu

Bir `HTTPException` raise ederken, `detail` parametresine sadece `str` değil, JSON’a dönüştürülebilen herhangi bir değer geçebilirsiniz.

Örneğin `dict`, `list` vb. geçebilirsiniz.

Bunlar **FastAPI** tarafından otomatik olarak işlenir ve JSON’a dönüştürülür.

///

## Özel Header’lar Eklemek { #add-custom-headers }

Bazı durumlarda HTTP hata response’una özel header’lar eklemek faydalıdır. Örneğin bazı güvenlik türlerinde.

Muhtemelen bunu doğrudan kendi kodunuzda kullanmanız gerekmeyecek.

Ama ileri seviye bir senaryo için ihtiyaç duyarsanız, özel header’lar ekleyebilirsiniz:

{* ../../docs_src/handling_errors/tutorial002_py310.py hl[14] *}

## Özel Exception Handler’ları Kurmak { #install-custom-exception-handlers }

<a href="https://www.starlette.dev/exceptions/" class="external-link" target="_blank">Starlette’in aynı exception yardımcı araçlarıyla</a> özel exception handler’lar ekleyebilirsiniz.

Diyelim ki sizin (ya da kullandığınız bir kütüphanenin) `raise` edebileceği `UnicornException` adında özel bir exception’ınız var.

Ve bu exception’ı FastAPI ile global olarak handle etmek istiyorsunuz.

`@app.exception_handler()` ile özel bir exception handler ekleyebilirsiniz:

{* ../../docs_src/handling_errors/tutorial003_py310.py hl[5:7,13:18,24] *}

Burada `/unicorns/yolo` için request atarsanız, *path operation* bir `UnicornException` `raise` eder.

Ancak bu, `unicorn_exception_handler` tarafından handle edilir.

Böylece HTTP status code’u `418` olan, JSON içeriği şu şekilde temiz bir hata response’u alırsınız:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | Teknik Detaylar

`from starlette.requests import Request` ve `from starlette.responses import JSONResponse` da kullanabilirsiniz.

**FastAPI**, geliştirici olarak size kolaylık olsun diye `starlette.responses` içeriğini `fastapi.responses` olarak da sunar. Ancak mevcut response’ların çoğu doğrudan Starlette’ten gelir. `Request` için de aynısı geçerlidir.

///

## Varsayılan Exception Handler’ları Override Etmek { #override-the-default-exception-handlers }

**FastAPI** bazı varsayılan exception handler’lara sahiptir.

Bu handler’lar, `HTTPException` `raise` ettiğinizde ve request geçersiz veri içerdiğinde varsayılan JSON response’ları döndürmekten sorumludur.

Bu exception handler’ları kendi handler’larınızla override edebilirsiniz.

### Request Validation Exception’larını Override Etmek { #override-request-validation-exceptions }

Bir request geçersiz veri içerdiğinde, **FastAPI** içeride `RequestValidationError` raise eder.

Ve bunun için varsayılan bir exception handler da içerir.

Override etmek için `RequestValidationError`’ı import edin ve exception handler’ı `@app.exception_handler(RequestValidationError)` ile decorate edin.

Exception handler, bir `Request` ve exception’ı alır.

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[2,14:19] *}

Artık `/items/foo`’ya giderseniz, şu varsayılan JSON hatası yerine:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

şu şekilde bir metin (text) versiyonu alırsınız:

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### `HTTPException` Hata Handler’ını Override Etmek { #override-the-httpexception-error-handler }

Benzer şekilde `HTTPException` handler’ını da override edebilirsiniz.

Örneğin bu hatalar için JSON yerine plain text response döndürmek isteyebilirsiniz:

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[3:4,9:11,25] *}

/// note | Teknik Detaylar

`from starlette.responses import PlainTextResponse` da kullanabilirsiniz.

**FastAPI**, geliştirici olarak size kolaylık olsun diye `starlette.responses` içeriğini `fastapi.responses` olarak da sunar. Ancak mevcut response’ların çoğu doğrudan Starlette’ten gelir.

///

/// warning | Uyarı

`RequestValidationError`, validation hatasının gerçekleştiği dosya adı ve satır bilgilerini içerir; isterseniz bunu log’larınıza ilgili bilgilerle birlikte yazdırabilirsiniz.

Ancak bu, eğer sadece string’e çevirip bu bilgiyi doğrudan response olarak döndürürseniz sisteminiz hakkında bir miktar bilgi sızdırabileceğiniz anlamına gelir. Bu yüzden burada kod, her bir hatayı ayrı ayrı çıkarıp gösterir.

///

### `RequestValidationError` Body’sini Kullanmak { #use-the-requestvalidationerror-body }

`RequestValidationError`, geçersiz veriyle aldığı `body`’yi içerir.

Uygulamanızı geliştirirken body’yi log’lamak, debug etmek, kullanıcıya döndürmek vb. için bunu kullanabilirsiniz.

{* ../../docs_src/handling_errors/tutorial005_py310.py hl[14] *}

Şimdi şu gibi geçersiz bir item göndermeyi deneyin:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

Aldığınız body’yi de içeren, verinin geçersiz olduğunu söyleyen bir response alırsınız:

```JSON hl_lines="12-15"
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
```

#### FastAPI’nin `HTTPException`’ı vs Starlette’in `HTTPException`’ı { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI**’nin kendi `HTTPException`’ı vardır.

Ve **FastAPI**’nin `HTTPException` hata sınıfı, Starlette’in `HTTPException` hata sınıfından kalıtım alır (inherit).

Tek fark şudur: **FastAPI**’nin `HTTPException`’ı `detail` alanı için JSON’a çevrilebilir herhangi bir veri kabul ederken, Starlette’in `HTTPException`’ı burada sadece string kabul eder.

Bu yüzden kodunuzda her zamanki gibi **FastAPI**’nin `HTTPException`’ını raise etmeye devam edebilirsiniz.

Ancak bir exception handler register ederken, bunu Starlette’in `HTTPException`’ı için register etmelisiniz.

Böylece Starlette’in internal kodunun herhangi bir bölümü ya da bir Starlette extension/plug-in’i Starlette `HTTPException` raise ederse, handler’ınız bunu yakalayıp (catch) handle edebilir.

Bu örnekte, iki `HTTPException`’ı da aynı kodda kullanabilmek için Starlette’in exception’ı `StarletteHTTPException` olarak yeniden adlandırılıyor:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### **FastAPI**’nin Exception Handler’larını Yeniden Kullanmak { #reuse-fastapis-exception-handlers }

Exception’ı, **FastAPI**’nin aynı varsayılan exception handler’larıyla birlikte kullanmak isterseniz, varsayılan exception handler’ları `fastapi.exception_handlers` içinden import edip yeniden kullanabilirsiniz:

{* ../../docs_src/handling_errors/tutorial006_py310.py hl[2:5,15,21] *}

Bu örnekte sadece oldukça açıklayıcı bir mesajla hatayı yazdırıyorsunuz; ama fikir anlaşılıyor. Exception’ı kullanıp ardından varsayılan exception handler’ları olduğu gibi yeniden kullanabilirsiniz.
