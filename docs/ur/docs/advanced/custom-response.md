# حسب ضرورت Response - HTML, Stream, File, اور دیگر { #custom-response-html-stream-file-others }

پہلے سے طے شدہ طور پر، **FastAPI** JSON responses واپس کرے گا۔

آپ اسے براہ راست `Response` واپس کر کے تبدیل کر سکتے ہیں جیسا کہ [براہ راست Response واپس کریں](response-directly.md) میں بتایا گیا ہے۔

لیکن اگر آپ براہ راست `Response` واپس کرتے ہیں (یا کوئی بھی subclass، جیسے `JSONResponse`)، تو ڈیٹا خود بخود تبدیل نہیں ہوگا (چاہے آپ نے `response_model` کا اعلان کیا ہو)، اور دستاویزات خود بخود تیار نہیں ہوں گی (مثال کے طور پر، مخصوص "media type" شامل کرنا، HTTP header `Content-Type` میں، تیار شدہ OpenAPI کے حصے کے طور پر)۔

لیکن آپ وہ `Response` بھی اعلان کر سکتے ہیں جو آپ استعمال کرنا چاہتے ہیں (مثلاً کوئی بھی `Response` subclass)، *path operation decorator* میں `response_class` parameter استعمال کر کے۔

آپ کے *path operation function* سے واپس آنے والا مواد اس `Response` میں ڈالا جائے گا۔

/// note | نوٹ

اگر آپ بغیر media type والی response class استعمال کرتے ہیں، تو FastAPI توقع کرے گا کہ آپ کے response میں کوئی مواد نہیں ہے، لہذا یہ تیار شدہ OpenAPI docs میں response format کو دستاویزی شکل نہیں دے گا۔

///

## JSON Responses { #json-responses }

پہلے سے طے شدہ طور پر FastAPI JSON responses واپس کرتا ہے۔

اگر آپ [Response Model](../tutorial/response-model.md) کا اعلان کرتے ہیں تو FastAPI اسے Pydantic استعمال کر کے ڈیٹا کو JSON میں serialize کرنے کے لیے استعمال کرے گا۔

اگر آپ response model کا اعلان نہیں کرتے، تو FastAPI [JSON Compatible Encoder](../tutorial/encoder.md) میں بیان کردہ `jsonable_encoder` استعمال کرے گا اور اسے `JSONResponse` میں ڈالے گا۔

اگر آپ JSON media type (`application/json`) والی `response_class` کا اعلان کرتے ہیں، جیسا کہ `JSONResponse` کے معاملے میں ہے، تو آپ کا واپس کردہ ڈیٹا خود بخود Pydantic `response_model` کے ساتھ تبدیل (اور فلٹر) ہوگا جو آپ نے *path operation decorator* میں اعلان کیا تھا۔ لیکن ڈیٹا کو Pydantic کے ذریعے JSON bytes میں serialize نہیں کیا جائے گا، بلکہ اسے `jsonable_encoder` سے تبدیل کیا جائے گا اور پھر `JSONResponse` class کو دیا جائے گا، جو اسے Python کی معیاری JSON library استعمال کر کے bytes میں serialize کرے گی۔

### JSON کارکردگی { #json-performance }

مختصراً، اگر آپ زیادہ سے زیادہ کارکردگی چاہتے ہیں تو [Response Model](../tutorial/response-model.md) استعمال کریں اور *path operation decorator* میں `response_class` کا اعلان نہ کریں۔

{* ../../docs_src/response_model/tutorial001_01_py310.py ln[15:17] hl[16] *}

## HTML Response { #html-response }

**FastAPI** سے براہ راست HTML کے ساتھ response واپس کرنے کے لیے، `HTMLResponse` استعمال کریں۔

* `HTMLResponse` import کریں۔
* اپنے *path operation decorator* کے parameter `response_class` میں `HTMLResponse` دیں۔

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// info | معلومات

parameter `response_class` کو response کی "media type" کی تعریف کے لیے بھی استعمال کیا جائے گا۔

اس صورت میں، HTTP header `Content-Type` کو `text/html` پر مقرر کیا جائے گا۔

اور اسے OpenAPI میں اسی طرح دستاویزی شکل دی جائے گی۔

///

### `Response` واپس کریں { #return-a-response }

جیسا کہ [براہ راست Response واپس کریں](response-directly.md) میں بتایا گیا ہے، آپ اپنے *path operation* میں response کو براہ راست واپس کر کے بھی تبدیل کر سکتے ہیں۔

اوپر والی مثال، `HTMLResponse` واپس کرتے ہوئے، اس طرح دکھ سکتی ہے:

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning | انتباہ

آپ کے *path operation function* سے براہ راست واپس کیا گیا `Response` OpenAPI میں دستاویزی شکل نہیں دیا جائے گا (مثال کے طور پر، `Content-Type` دستاویزی نہیں ہوگا) اور خودکار انٹرایکٹو docs میں نظر نہیں آئے گا۔

///

/// info | معلومات

یقیناً، اصل `Content-Type` header، status code وغیرہ آپ کے واپس کردہ `Response` آبجیکٹ سے آئیں گے۔

///

### OpenAPI میں دستاویز بنائیں اور `Response` کو تبدیل کریں { #document-in-openapi-and-override-response }

اگر آپ function کے اندر سے response کو تبدیل کرنا چاہتے ہیں لیکن ساتھ ہی OpenAPI میں "media type" کو دستاویزی شکل دینا چاہتے ہیں، تو آپ `response_class` parameter استعمال کر سکتے ہیں اور ساتھ ہی `Response` آبجیکٹ واپس کر سکتے ہیں۔

`response_class` پھر صرف OpenAPI *path operation* کی دستاویز بنانے کے لیے استعمال ہوگی، لیکن آپ کا `Response` جیسا ہے ویسا ہی استعمال ہوگا۔

#### براہ راست `HTMLResponse` واپس کریں { #return-an-htmlresponse-directly }

مثال کے طور پر، یہ کچھ اس طرح ہو سکتا ہے:

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

اس مثال میں، function `generate_html_response()` پہلے سے ہی HTML کو `str` میں واپس کرنے کی بجائے `Response` تیار اور واپس کرتا ہے۔

`generate_html_response()` کو کال کرنے کا نتیجہ واپس کر کے، آپ پہلے سے ہی ایک `Response` واپس کر رہے ہیں جو **FastAPI** کے پہلے سے طے شدہ رویے کو تبدیل کر دے گا۔

لیکن چونکہ آپ نے `HTMLResponse` کو `response_class` میں بھی دیا ہے، **FastAPI** جانے گا کہ اسے OpenAPI اور انٹرایکٹو docs میں HTML کے طور پر `text/html` کے ساتھ دستاویزی شکل کیسے دینی ہے:

<img src="/img/tutorial/custom-response/image01.png">

## دستیاب responses { #available-responses }

یہاں کچھ دستیاب responses ہیں۔

ذہن میں رکھیں کہ آپ `Response` استعمال کر کے کچھ بھی واپس کر سکتے ہیں، یا حتی کہ اپنی مرضی کی sub-class بنا سکتے ہیں۔

/// note | تکنیکی تفصیلات

آپ `from starlette.responses import HTMLResponse` بھی استعمال کر سکتے ہیں۔

**FastAPI** وہی `starlette.responses` فراہم کرتا ہے جو `fastapi.responses` کے طور پر، بس آپ یعنی developer کی سہولت کے لیے۔ لیکن زیادہ تر دستیاب responses براہ راست Starlette سے آتے ہیں۔

///

### `Response` { #response }

بنیادی `Response` class، باقی تمام responses اس سے وراثت میں ملتے ہیں۔

آپ اسے براہ راست واپس کر سکتے ہیں۔

یہ درج ذیل parameters قبول کرتا ہے:

* `content` - ایک `str` یا `bytes`۔
* `status_code` - ایک `int` HTTP status code۔
* `headers` - strings کی ایک `dict`۔
* `media_type` - media type دینے والی ایک `str`۔ مثلاً `"text/html"`۔

FastAPI (دراصل Starlette) خود بخود Content-Length header شامل کرے گا۔ یہ Content-Type header بھی شامل کرے گا، `media_type` کی بنیاد پر اور متنی اقسام کے لیے charset شامل کرے گا۔

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

کچھ متن یا bytes لیتا ہے اور HTML response واپس کرتا ہے، جیسا کہ آپ نے اوپر پڑھا۔

### `PlainTextResponse` { #plaintextresponse }

کچھ متن یا bytes لیتا ہے اور سادہ متنی response واپس کرتا ہے۔

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

کچھ ڈیٹا لیتا ہے اور `application/json` encoded response واپس کرتا ہے۔

یہ **FastAPI** میں استعمال ہونے والا پہلے سے طے شدہ response ہے، جیسا کہ آپ نے اوپر پڑھا۔

/// note | تکنیکی تفصیلات

لیکن اگر آپ response model یا return type کا اعلان کرتے ہیں، تو اسے ڈیٹا کو JSON میں براہ راست serialize کرنے کے لیے استعمال کیا جائے گا، اور JSON کے لیے صحیح media type والا response براہ راست واپس کیا جائے گا، `JSONResponse` class استعمال کیے بغیر۔

یہ بہترین کارکردگی حاصل کرنے کا مثالی طریقہ ہے۔

///

### `RedirectResponse` { #redirectresponse }

HTTP redirect واپس کرتا ہے۔ پہلے سے طے شدہ طور پر 307 status code (Temporary Redirect) استعمال کرتا ہے۔

آپ براہ راست `RedirectResponse` واپس کر سکتے ہیں:

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

یا آپ اسے `response_class` parameter میں استعمال کر سکتے ہیں:

{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

اگر آپ ایسا کرتے ہیں، تو آپ اپنے *path operation* function سے براہ راست URL واپس کر سکتے ہیں۔

اس صورت میں، استعمال ہونے والا `status_code` `RedirectResponse` کا پہلے سے طے شدہ ہوگا، جو `307` ہے۔

---

آپ `status_code` parameter کو `response_class` parameter کے ساتھ بھی استعمال کر سکتے ہیں:

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

ایک async generator یا عام generator/iterator (ایک function جس میں `yield` ہو) لیتا ہے اور response body کو stream کرتا ہے۔

{* ../../docs_src/custom_response/tutorial007_py310.py hl[3,16] *}

/// note | تکنیکی تفصیلات

ایک `async` task صرف اس وقت منسوخ ہو سکتا ہے جب یہ `await` پر پہنچتا ہے۔ اگر `await` نہیں ہے، تو generator (function جس میں `yield` ہو) صحیح طریقے سے منسوخ نہیں ہو سکتا اور منسوخی کی درخواست کے بعد بھی چلتا رہ سکتا ہے۔

چونکہ اس چھوٹی مثال کو کسی `await` statement کی ضرورت نہیں ہے، ہم `await anyio.sleep(0)` شامل کرتے ہیں تاکہ event loop کو منسوخی سنبھالنے کا موقع مل سکے۔

بڑے یا لامحدود streams کے ساتھ یہ اور بھی اہم ہوگا۔

///

/// tip | مشورہ

براہ راست `StreamingResponse` واپس کرنے کی بجائے، آپ کو شاید [Stream Data](./stream-data.md) میں دیے گئے طریقے پر عمل کرنا چاہیے، یہ بہت زیادہ آسان ہے اور پس پردہ منسوخی کو آپ کے لیے سنبھالتا ہے۔

اگر آپ JSON Lines stream کر رہے ہیں، تو [Stream JSON Lines](../tutorial/stream-json-lines.md) ٹیوٹوریل دیکھیں۔

///

### `FileResponse` { #fileresponse }

فائل کو غیر ہم وقتی (asynchronously) response کے طور پر stream کرتا ہے۔

دوسری response اقسام سے مختلف arguments لیتا ہے:

* `path` - فائل کا path جو stream کرنی ہے۔
* `headers` - شامل کرنے کے لیے کوئی بھی حسب ضرورت headers، بطور dictionary۔
* `media_type` - media type دینے والی ایک string۔ اگر مقرر نہ ہو تو فائل نام یا path سے media type کا اندازہ لگایا جائے گا۔
* `filename` - اگر مقرر ہو تو یہ response `Content-Disposition` میں شامل ہوگا۔

File responses میں مناسب `Content-Length`، `Last-Modified` اور `ETag` headers شامل ہوں گے۔

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

آپ `response_class` parameter بھی استعمال کر سکتے ہیں:

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

اس صورت میں، آپ اپنے *path operation* function سے براہ راست فائل کا path واپس کر سکتے ہیں۔

## حسب ضرورت response class { #custom-response-class }

آپ `Response` سے وراثت میں لے کر اپنی مرضی کی response class بنا سکتے ہیں اور اسے استعمال کر سکتے ہیں۔

مثال کے طور پر، فرض کریں کہ آپ [`orjson`](https://github.com/ijl/orjson) کو کچھ ترتیبات کے ساتھ استعمال کرنا چاہتے ہیں۔

فرض کریں آپ چاہتے ہیں کہ یہ indented اور formatted JSON واپس کرے، لہذا آپ orjson آپشن `orjson.OPT_INDENT_2` استعمال کرنا چاہتے ہیں۔

آپ `CustomORJSONResponse` بنا سکتے ہیں۔ سب سے اہم بات یہ ہے کہ آپ کو ایک `Response.render(content)` method بنانا ہے جو مواد کو `bytes` کے طور پر واپس کرے:

{* ../../docs_src/custom_response/tutorial009c_py310.py hl[9:14,17] *}

اب واپس کرنے کی بجائے:

```json
{"message": "Hello World"}
```

...یہ response واپس کرے گا:

```json
{
  "message": "Hello World"
}
```

یقیناً، آپ کو JSON فارمیٹنگ سے کہیں بہتر طریقے مل جائیں گے اس سے فائدہ اٹھانے کے لیے۔

### `orjson` یا Response Model { #orjson-or-response-model }

اگر آپ کارکردگی کی تلاش میں ہیں تو شاید `orjson` response سے بہتر یہ ہے کہ آپ [Response Model](../tutorial/response-model.md) استعمال کریں۔

Response model کے ساتھ، FastAPI ڈیٹا کو JSON میں serialize کرنے کے لیے Pydantic استعمال کرے گا، بغیر درمیانی مراحل کے، جیسے اسے `jsonable_encoder` سے تبدیل کرنا، جو کسی بھی اور صورت میں ہوتا۔

اور پس پردہ، Pydantic JSON میں serialize کرنے کے لیے `orjson` جیسے ہی بنیادی Rust میکانزم استعمال کرتا ہے، لہذا response model کے ساتھ آپ کو پہلے سے ہی بہترین کارکردگی مل جائے گی۔

## پہلے سے طے شدہ response class { #default-response-class }

**FastAPI** class instance یا `APIRouter` بناتے وقت آپ بتا سکتے ہیں کہ پہلے سے طے شدہ طور پر کون سی response class استعمال ہو۔

اسے بیان کرنے والا parameter `default_response_class` ہے۔

نیچے دی گئی مثال میں، **FastAPI** تمام *path operations* میں JSON کی بجائے پہلے سے طے شدہ طور پر `HTMLResponse` استعمال کرے گا۔

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | مشورہ

آپ پہلے کی طرح *path operations* میں `response_class` کو تبدیل کر سکتے ہیں۔

///

## اضافی دستاویزات { #additional-documentation }

آپ OpenAPI میں media type اور بہت سی دوسری تفصیلات کا بھی `responses` استعمال کر کے اعلان کر سکتے ہیں: [OpenAPI میں اضافی Responses](additional-responses.md)۔
