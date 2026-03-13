# İleri Seviye Middleware { #advanced-middleware }

Ana tutorial'da uygulamanıza [Özel Middleware](../tutorial/middleware.md){.internal-link target=_blank} eklemeyi gördünüz.

Ardından [`CORSMiddleware` ile CORS'u yönetmeyi](../tutorial/cors.md){.internal-link target=_blank} de okudunuz.

Bu bölümde diğer middleware'leri nasıl kullanacağımıza bakacağız.

## ASGI middleware'leri ekleme { #adding-asgi-middlewares }

**FastAPI**, Starlette üzerine kurulu olduğu ve <abbr title="Asynchronous Server Gateway Interface - Asenkron Sunucu Ağ Geçidi Arayüzü">ASGI</abbr> spesifikasyonunu uyguladığı için, herhangi bir ASGI middleware'ini kullanabilirsiniz.

Bir middleware'in çalışması için özellikle FastAPI ya da Starlette için yazılmış olması gerekmez; ASGI spec'ine uyduğu sürece yeterlidir.

Genel olarak ASGI middleware'leri, ilk argüman olarak bir ASGI app almayı bekleyen class'lar olur.

Dolayısıyla üçüncü taraf ASGI middleware'lerinin dokümantasyonunda muhtemelen şöyle bir şey yapmanızı söylerler:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

Ancak FastAPI (aslında Starlette) bunu yapmanın daha basit bir yolunu sunar; böylece dahili middleware'ler server hatalarını doğru şekilde ele alır ve özel exception handler'lar düzgün çalışır.

Bunun için `app.add_middleware()` kullanırsınız (CORS örneğindeki gibi).

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` ilk argüman olarak bir middleware class'ı alır ve middleware'e aktarılacak ek argümanları da kabul eder.

## Entegre middleware'ler { #integrated-middlewares }

**FastAPI**, yaygın kullanım senaryoları için birkaç middleware içerir; şimdi bunları nasıl kullanacağımıza bakacağız.

/// note | Teknik Detaylar

Bir sonraki örneklerde `from starlette.middleware.something import SomethingMiddleware` kullanmanız da mümkündür.

**FastAPI**, size (geliştirici olarak) kolaylık olsun diye `fastapi.middleware` içinde bazı middleware'leri sağlar. Ancak mevcut middleware'lerin çoğu doğrudan Starlette'ten gelir.

///

## `HTTPSRedirectMiddleware` { #httpsredirectmiddleware }

Gelen tüm request'lerin `https` veya `wss` olmasını zorunlu kılar.

`http` veya `ws` olarak gelen herhangi bir request, bunun yerine güvenli şemaya redirect edilir.

{* ../../docs_src/advanced_middleware/tutorial001_py310.py hl[2,6] *}

## `TrustedHostMiddleware` { #trustedhostmiddleware }

HTTP Host Header saldırılarına karşı korunmak için, gelen tüm request'lerde `Host` header'ının doğru ayarlanmış olmasını zorunlu kılar.

{* ../../docs_src/advanced_middleware/tutorial002_py310.py hl[2,6:8] *}

Aşağıdaki argümanlar desteklenir:

* `allowed_hosts` - Hostname olarak izin verilmesi gereken domain adlarının listesi. `*.example.com` gibi wildcard domain'ler subdomain eşleştirmesi için desteklenir. Herhangi bir hostname'e izin vermek için `allowed_hosts=["*"]` kullanın veya middleware'i hiç eklemeyin.
* `www_redirect` - True olarak ayarlanırsa, izin verilen host'ların www olmayan sürümlerine gelen request'ler www sürümlerine redirect edilir. Varsayılanı `True`'dur.

Gelen bir request doğru şekilde doğrulanmazsa `400` response gönderilir.

## `GZipMiddleware` { #gzipmiddleware }

`Accept-Encoding` header'ında `"gzip"` içeren herhangi bir request için GZip response'larını yönetir.

Middleware hem standart hem de streaming response'ları ele alır.

{* ../../docs_src/advanced_middleware/tutorial003_py310.py hl[2,6] *}

Aşağıdaki argümanlar desteklenir:

* `minimum_size` - Bayt cinsinden bu minimum boyuttan küçük response'lara GZip uygulama. Varsayılanı `500`'dür.
* `compresslevel` - GZip sıkıştırması sırasında kullanılır. 1 ile 9 arasında bir tamsayıdır. Varsayılanı `9`'dur. Daha düşük değer daha hızlı sıkıştırma ama daha büyük dosya boyutları üretir; daha yüksek değer daha yavaş sıkıştırma ama daha küçük dosya boyutları üretir.

## Diğer middleware'ler { #other-middlewares }

Başka birçok ASGI middleware'i vardır.

Örneğin:

* <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">Uvicorn'un `ProxyHeadersMiddleware`'i</a>
* <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

Diğer mevcut middleware'leri görmek için <a href="https://www.starlette.dev/middleware/" class="external-link" target="_blank">Starlette'in Middleware dokümanlarına</a> ve <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">ASGI Awesome List</a> listesine bakın.
