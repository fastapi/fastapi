# Middleware { #middleware }

آپ **FastAPI** applications میں middleware شامل کر سکتے ہیں۔

"middleware" ایک function ہے جو ہر **request** کے ساتھ کام کرتا ہے اس سے پہلے کہ اسے کسی مخصوص *path operation* سے process کیا جائے۔ اور ساتھ ہی ہر **response** کے ساتھ بھی اسے واپس بھیجنے سے پہلے کام کرتا ہے۔

* یہ آپ کی application پر آنے والی ہر **request** کو لیتا ہے۔
* پھر یہ اس **request** کے ساتھ کچھ کر سکتا ہے یا کوئی ضروری code چلا سکتا ہے۔
* پھر یہ **request** کو باقی application (کسی *path operation*) کو process کرنے کے لیے آگے بھیجتا ہے۔
* پھر یہ application (کسی *path operation*) کی طرف سے بنایا گیا **response** لیتا ہے۔
* یہ اس **response** کے ساتھ کچھ کر سکتا ہے یا کوئی ضروری code چلا سکتا ہے۔
* پھر یہ **response** واپس بھیجتا ہے۔

/// note | تکنیکی تفصیلات

اگر آپ کے پاس `yield` والی dependencies ہیں، تو exit code middleware کے *بعد* چلے گا۔

اگر کوئی background tasks تھے (جن کا ذکر [Background Tasks](background-tasks.md) سیکشن میں ہے، آپ اسے بعد میں دیکھیں گے)، تو وہ تمام middleware کے *بعد* چلیں گے۔

///

## ایک middleware بنائیں { #create-a-middleware }

middleware بنانے کے لیے آپ ایک function کے اوپر `@app.middleware("http")` decorator استعمال کریں۔

middleware function یہ وصول کرتا ہے:

* `request`۔
* ایک function `call_next` جو `request` کو parameter کے طور پر وصول کرے گا۔
    * یہ function `request` کو متعلقہ *path operation* تک پہنچائے گا۔
    * پھر یہ متعلقہ *path operation* کی طرف سے بنایا گیا `response` واپس کرے گا۔
* پھر آپ `response` کو واپس بھیجنے سے پہلے مزید تبدیل کر سکتے ہیں۔

{* ../../docs_src/middleware/tutorial001_py310.py hl[8:9,11,14] *}

/// tip | مشورہ

یاد رکھیں کہ custom proprietary headers ["`X-` prefix" استعمال کرتے ہوئے](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) شامل کیے جا سکتے ہیں۔

لیکن اگر آپ کے پاس ایسے custom headers ہیں جو آپ چاہتے ہیں کہ browser میں موجود client دیکھ سکے، تو آپ کو انہیں اپنی CORS configurations ([CORS (Cross-Origin Resource Sharing)](cors.md)) میں `expose_headers` parameter استعمال کرتے ہوئے شامل کرنا ہوگا جیسا کہ [Starlette کی CORS دستاویزات](https://www.starlette.dev/middleware/#corsmiddleware) میں بیان کیا گیا ہے۔

///

/// note | تکنیکی تفصیلات

آپ `from starlette.requests import Request` بھی استعمال کر سکتے ہیں۔

**FastAPI** اسے آپ کی سہولت کے لیے فراہم کرتا ہے۔ لیکن یہ براہ راست Starlette سے آتا ہے۔

///

### `response` سے پہلے اور بعد { #before-and-after-the-response }

آپ `request` کے ساتھ چلنے کے لیے code شامل کر سکتے ہیں، کسی بھی *path operation* کو وصول کرنے سے پہلے۔

اور ساتھ ہی `response` بننے کے بعد، اسے واپس بھیجنے سے پہلے بھی۔

مثال کے طور پر، آپ ایک custom header `X-Process-Time` شامل کر سکتے ہیں جس میں request کو process کرنے اور response بنانے میں لگنے والا وقت سیکنڈز میں ہو:

{* ../../docs_src/middleware/tutorial001_py310.py hl[10,12:13] *}

/// tip | مشورہ

یہاں ہم `time.time()` کی بجائے [`time.perf_counter()`](https://docs.python.org/3/library/time.html#time.perf_counter) استعمال کر رہے ہیں کیونکہ یہ ان استعمالات کے لیے زیادہ درست ہو سکتا ہے۔ 🤓

///

## متعدد middleware کی عمل درآمد ترتیب { #multiple-middleware-execution-order }

جب آپ `@app.middleware()` decorator یا `app.add_middleware()` method استعمال کرتے ہوئے متعدد middlewares شامل کرتے ہیں، تو ہر نیا middleware application کو wrap کرتا ہے اور ایک stack بناتا ہے۔ آخری شامل کیا گیا middleware *سب سے باہر* ہوتا ہے، اور پہلا *سب سے اندر*۔

Request کے راستے پر، *سب سے باہر والا* middleware پہلے چلتا ہے۔

Response کے راستے پر، یہ آخر میں چلتا ہے۔

مثال کے طور پر:

```Python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

اس کا نتیجہ یہ عمل درآمد ترتیب ہے:

* **Request**: MiddlewareB → MiddlewareA → route

* **Response**: route → MiddlewareA → MiddlewareB

یہ stacking رویہ اس بات کو یقینی بناتا ہے کہ middlewares ایک قابل پیشگوئی اور قابل کنٹرول ترتیب میں چلیں۔

## دیگر middlewares { #other-middlewares }

آپ دیگر middlewares کے بارے میں بعد میں [Advanced User Guide: Advanced Middleware](../advanced/middleware.md) میں مزید پڑھ سکتے ہیں۔

آپ اگلے سیکشن میں پڑھیں گے کہ middleware کے ذریعے <abbr title="Cross-Origin Resource Sharing">CORS</abbr> کو کیسے handle کیا جائے۔
