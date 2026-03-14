# ایڈوانسڈ Middleware { #advanced-middleware }

بنیادی ٹیوٹوریل میں آپ نے پڑھا کہ اپنی ایپلیکیشن میں [اپنی مرضی کا Middleware](../tutorial/middleware.md) کیسے شامل کریں۔

اور پھر آپ نے یہ بھی پڑھا کہ [`CORSMiddleware`](../tutorial/cors.md) سے CORS کو کیسے ہینڈل کریں۔

اس سیکشن میں ہم دیکھیں گے کہ دوسرے middleware کیسے استعمال کریں۔

## ASGI middleware شامل کرنا { #adding-asgi-middlewares }

چونکہ **FastAPI** Starlette پر مبنی ہے اور <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr> specification کو لاگو کرتا ہے، آپ کوئی بھی ASGI middleware استعمال کر سکتے ہیں۔

middleware کا FastAPI یا Starlette کے لیے مخصوص ہونا ضروری نہیں ہے، بس یہ ASGI spec کی پیروی کرے۔

عام طور پر، ASGI middleware ایسی classes ہوتی ہیں جو پہلے argument کے طور پر ASGI app وصول کرتی ہیں۔

تو، third-party ASGI middleware کی دستاویزات میں وہ شاید آپ کو کچھ اس طرح کرنے کا کہیں گے:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

لیکن FastAPI (دراصل Starlette) ایسا کرنے کا ایک آسان طریقہ فراہم کرتا ہے جو یقینی بناتا ہے کہ اندرونی middleware server errors اور حسب ضرورت exception handlers کو صحیح طریقے سے ہینڈل کریں۔

اس کے لیے، آپ `app.add_middleware()` استعمال کریں (جیسا کہ CORS کی مثال میں)۔

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` پہلے argument کے طور پر middleware class وصول کرتا ہے اور باقی اضافی arguments middleware کو پاس کر دیے جاتے ہیں۔

## شامل middleware { #integrated-middlewares }

**FastAPI** عام استعمال کے لیے کئی middleware شامل کرتا ہے، آگے ہم دیکھیں گے کہ انہیں کیسے استعمال کریں۔

/// note | تکنیکی تفصیلات

اگلی مثالوں کے لیے، آپ `from starlette.middleware.something import SomethingMiddleware` بھی استعمال کر سکتے ہیں۔

**FastAPI** آپ کی سہولت کے لیے `fastapi.middleware` میں کئی middleware فراہم کرتا ہے۔ لیکن زیادہ تر دستیاب middleware براہ راست Starlette سے آتے ہیں۔

///

## `HTTPSRedirectMiddleware` { #httpsredirectmiddleware }

یہ لازم کرتا ہے کہ تمام آنے والی requests `https` یا `wss` ہوں۔

`http` یا `ws` پر آنے والی کسی بھی request کو محفوظ scheme کی طرف redirect کر دیا جائے گا۔

{* ../../docs_src/advanced_middleware/tutorial001_py310.py hl[2,6] *}

## `TrustedHostMiddleware` { #trustedhostmiddleware }

یہ لازم کرتا ہے کہ تمام آنے والی requests میں `Host` header درست طریقے سے سیٹ ہو، تاکہ HTTP Host Header حملوں سے بچا جا سکے۔

{* ../../docs_src/advanced_middleware/tutorial002_py310.py hl[2,6:8] *}

درج ذیل arguments سپورٹ ہوتے ہیں:

* `allowed_hosts` - ان domain ناموں کی فہرست جنہیں hostname کے طور پر اجازت ہونی چاہیے۔ Wildcard domains جیسے `*.example.com` subdomains کی matching کے لیے سپورٹ ہوتے ہیں۔ کسی بھی hostname کو اجازت دینے کے لیے `allowed_hosts=["*"]` استعمال کریں یا middleware کو چھوڑ دیں۔
* `www_redirect` - اگر True پر سیٹ ہو تو، اجازت یافتہ hosts کے غیر www ورژنز کی requests ان کے www ہم منصبوں کی طرف redirect ہو جائیں گی۔ بطور ڈیفالٹ `True` ہے۔

اگر آنے والی request درست طریقے سے validate نہیں ہوتی تو `400` response بھیجا جائے گا۔

## `GZipMiddleware` { #gzipmiddleware }

GZip responses کو ہینڈل کرتا ہے ہر اس request کے لیے جس کے `Accept-Encoding` header میں `"gzip"` شامل ہو۔

یہ middleware معیاری اور streaming دونوں قسم کے responses کو ہینڈل کرے گا۔

{* ../../docs_src/advanced_middleware/tutorial003_py310.py hl[2,6] *}

درج ذیل arguments سپورٹ ہوتے ہیں:

* `minimum_size` - اس کم از کم سائز (bytes میں) سے چھوٹے responses کو GZip نہ کریں۔ بطور ڈیفالٹ `500` ہے۔
* `compresslevel` - GZip compression کے دوران استعمال ہوتا ہے۔ یہ 1 سے 9 تک کا integer ہے۔ بطور ڈیفالٹ `9` ہے۔ کم قدر تیز compression لیکن بڑے فائل سائز کا نتیجہ ہے، جبکہ زیادہ قدر سست compression لیکن چھوٹے فائل سائز کا نتیجہ ہے۔

## دوسرے middleware { #other-middlewares }

بہت سے دوسرے ASGI middleware موجود ہیں۔

مثال کے طور پر:

* [Uvicorn کا `ProxyHeadersMiddleware`](https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py)
* [MessagePack](https://github.com/florimondmanca/msgpack-asgi)

دوسرے دستیاب middleware دیکھنے کے لیے [Starlette کی Middleware دستاویزات](https://www.starlette.dev/middleware/) اور [ASGI Awesome List](https://github.com/florimondmanca/awesome-asgi) دیکھیں۔
