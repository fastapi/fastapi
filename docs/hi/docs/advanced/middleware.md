# उन्नत Middleware { #advanced-middleware }

मुख्य tutorial में आपने पढ़ा कि अपनी application में [Custom Middleware](../tutorial/middleware.md) कैसे जोड़ें।

और फिर आपने यह भी पढ़ा कि [`CORSMiddleware` के साथ CORS](../tutorial/cors.md) को कैसे handle करें।

इस section में हम देखेंगे कि अन्य middleware का उपयोग कैसे करें।

## ASGI middleware जोड़ना { #adding-asgi-middlewares }

क्योंकि **FastAPI** Starlette पर आधारित है और <abbr title="Asynchronous Server Gateway Interface - asynchronous सर्वर गेटवे इंटरफ़ेस">ASGI</abbr> specification को implement करता है, आप कोई भी ASGI middleware उपयोग कर सकते हैं।

किसी middleware को काम करने के लिए FastAPI या Starlette के लिए बना होना required नहीं है, जब तक वह ASGI spec का पालन करता है।

सामान्यतः, ASGI middleware ऐसी classes होती हैं जो पहले argument के रूप में एक ASGI app प्राप्त करने की अपेक्षा करती हैं।

इसलिए, third-party ASGI middleware के documentation में वे शायद आपको कुछ ऐसा करने के लिए कहेंगे:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

लेकिन FastAPI (वास्तव में Starlette) इसे करने का एक सरल तरीका प्रदान करता है, जो सुनिश्चित करता है कि internal middleware server errors को handle करें और custom exception handlers सही तरीके से काम करें।

इसके लिए, आप `app.add_middleware()` का उपयोग करते हैं (जैसे CORS के उदाहरण में)।

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` पहले argument के रूप में एक middleware class प्राप्त करता है और middleware को pass किए जाने वाले कोई भी अतिरिक्त arguments भी प्राप्त करता है।

## एकीकृत middleware { #integrated-middlewares }

**FastAPI** common use cases के लिए कई middleware शामिल करता है, आगे हम देखेंगे कि उनका उपयोग कैसे करें।

/// note | तकनीकी विवरण

अगले उदाहरणों के लिए, आप `from starlette.middleware.something import SomethingMiddleware` भी उपयोग कर सकते हैं।

**FastAPI** `fastapi.middleware` में कई middleware सिर्फ आपकी, developer की, सुविधा के लिए प्रदान करता है। लेकिन उपलब्ध अधिकांश middleware सीधे Starlette से आते हैं।

///

## `HTTPSRedirectMiddleware` { #httpsredirectmiddleware }

यह enforce करता है कि सभी incoming requests या तो `https` या `wss` हों।

`http` या `ws` पर आने वाली कोई भी incoming request इसके बजाय secure scheme पर redirect कर दी जाएगी।

{* ../../docs_src/advanced_middleware/tutorial001_py310.py hl[2,6] *}

## `TrustedHostMiddleware` { #trustedhostmiddleware }

यह enforce करता है कि सभी incoming requests में `Host` header सही तरीके से set हो, ताकि HTTP Host Header attacks से बचाव हो सके।

{* ../../docs_src/advanced_middleware/tutorial002_py310.py hl[2,6:8] *}

निम्नलिखित arguments supported हैं:

* `allowed_hosts` - domain names की एक सूची जिन्हें hostnames के रूप में allow किया जाना चाहिए। `*.example.com` जैसे Wildcard domains subdomains को match करने के लिए supported हैं। किसी भी hostname को allow करने के लिए या तो `allowed_hosts=["*"]` उपयोग करें या middleware को omit करें।
* `www_redirect` - यदि True पर set किया गया है, तो allowed hosts के non-www versions पर आने वाली requests उनके www counterparts पर redirect कर दी जाएँगी। Default `True` है।

यदि कोई incoming request सही तरीके से validate नहीं होती है तो `400` response भेजा जाएगा।

## `GZipMiddleware` { #gzipmiddleware }

ऐसी किसी भी request के लिए GZip responses handle करता है जिसमें `Accept-Encoding` header में `"gzip"` शामिल हो।

middleware standard और streaming दोनों responses को handle करेगा।

{* ../../docs_src/advanced_middleware/tutorial003_py310.py hl[2,6] *}

निम्नलिखित arguments supported हैं:

* `minimum_size` - इस minimum size से छोटे responses को GZip न करें, size bytes में है। Default `500` है।
* `compresslevel` - GZip compression के दौरान उपयोग किया जाता है। यह 1 से 9 तक की range में एक integer है। Default `9` है। कम value से compression तेज़ होता है लेकिन file sizes बड़ी होती हैं, जबकि अधिक value से compression धीमा होता है लेकिन file sizes छोटी होती हैं।

## अन्य middleware { #other-middlewares }

कई अन्य ASGI middleware हैं।

उदाहरण के लिए:

* [Uvicorn का `ProxyHeadersMiddleware`](https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py)
* [MessagePack](https://github.com/florimondmanca/msgpack-asgi)

अन्य उपलब्ध middleware देखने के लिए [Starlette के Middleware docs](https://www.starlette.dev/middleware/) और [ASGI Awesome List](https://github.com/florimondmanca/awesome-asgi) देखें।
