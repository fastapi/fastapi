# Errors کو سنبھالنا { #handling-errors }

بہت سے حالات ایسے ہوتے ہیں جن میں آپ کو اپنی API استعمال کرنے والے client کو error کی اطلاع دینی ہوتی ہے۔

یہ client ایک browser ہو سکتا ہے جس میں frontend ہو، کسی اور کا code ہو سکتا ہے، کوئی IoT device ہو سکتی ہے، وغیرہ۔

آپ کو client کو بتانا پڑ سکتا ہے کہ:

* Client کے پاس اس عمل کے لیے کافی اختیارات نہیں ہیں۔
* Client کو اس resource تک رسائی نہیں ہے۔
* جس item تک client رسائی حاصل کرنا چاہتا تھا وہ موجود نہیں ہے۔
* وغیرہ۔

ان صورتوں میں، آپ عام طور پر **400** کی حد میں (400 سے 499 تک) ایک **HTTP status code** واپس کریں گے۔

یہ 200 HTTP status codes (200 سے 299 تک) کی طرح ہے۔ وہ "200" status codes یہ ظاہر کرتے ہیں کہ request میں کسی نہ کسی طرح "کامیابی" ہوئی۔

400 کی حد میں status codes یہ ظاہر کرتے ہیں کہ client کی جانب سے کوئی error ہوا۔

وہ تمام **"404 Not Found"** errors (اور لطیفے) یاد ہیں؟

## `HTTPException` استعمال کریں { #use-httpexception }

Client کو errors کے ساتھ HTTP responses واپس کرنے کے لیے آپ `HTTPException` استعمال کرتے ہیں۔

### `HTTPException` کو Import کریں { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[1] *}

### اپنے code میں `HTTPException` raise کریں { #raise-an-httpexception-in-your-code }

`HTTPException` ایک عام Python exception ہے جس میں APIs سے متعلق اضافی data شامل ہوتا ہے۔

چونکہ یہ ایک Python exception ہے، آپ اسے `return` نہیں کرتے، بلکہ `raise` کرتے ہیں۔

اس کا یہ بھی مطلب ہے کہ اگر آپ کسی utility function کے اندر ہیں جسے آپ اپنے *path operation function* کے اندر سے call کر رہے ہیں، اور آپ اس utility function کے اندر سے `HTTPException` raise کرتے ہیں، تو یہ *path operation function* کا باقی code نہیں چلائے گا، بلکہ فوری طور پر اس request کو ختم کر دے گا اور `HTTPException` سے HTTP error client کو بھیج دے گا۔

Exception raise کرنے کا value واپس کرنے پر فائدہ Dependencies اور Security کے سیکشن میں مزید واضح ہوگا۔

اس مثال میں، جب client ایسے ID کے ذریعے کوئی item طلب کرتا ہے جو موجود نہیں ہے تو `404` status code کے ساتھ exception raise کریں:

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[11] *}

### نتیجے میں ملنے والا response { #the-resulting-response }

اگر client `http://example.com/items/foo` کی درخواست کرتا ہے (ایک `item_id` `"foo"`) تو اس client کو HTTP status code 200 ملے گا، اور ایک JSON response:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

لیکن اگر client `http://example.com/items/bar` کی درخواست کرتا ہے (ایک غیر موجود `item_id` `"bar"`) تو اس client کو HTTP status code 404 ("not found" error) ملے گا، اور ایک JSON response:

```JSON
{
  "detail": "Item not found"
}
```

/// tip | مشورہ

`HTTPException` raise کرتے وقت، آپ `detail` parameter کے طور پر کوئی بھی value دے سکتے ہیں جو JSON میں تبدیل ہو سکے، صرف `str` نہیں۔

آپ ایک `dict`، ایک `list` وغیرہ دے سکتے ہیں۔

یہ **FastAPI** کے ذریعے خودکار طور پر سنبھالے جاتے ہیں اور JSON میں تبدیل کیے جاتے ہیں۔

///

## حسب ضرورت headers شامل کریں { #add-custom-headers }

کچھ حالات ایسے ہیں جن میں HTTP error میں حسب ضرورت headers شامل کرنا مفید ہوتا ہے۔ مثال کے طور پر، کچھ قسم کی security کے لیے۔

آپ کو شاید اپنے code میں اسے براہ راست استعمال کرنے کی ضرورت نہیں پڑے گی۔

لیکن اگر آپ کو کسی پیچیدہ منظرنامے کے لیے اس کی ضرورت ہو تو آپ حسب ضرورت headers شامل کر سکتے ہیں:

{* ../../docs_src/handling_errors/tutorial002_py310.py hl[14] *}

## حسب ضرورت exception handlers انسٹال کریں { #install-custom-exception-handlers }

آپ [Starlette سے ملتی جلتی exception utilities](https://www.starlette.dev/exceptions/) کے ساتھ حسب ضرورت exception handlers شامل کر سکتے ہیں۔

فرض کریں کہ آپ کے پاس ایک حسب ضرورت exception `UnicornException` ہے جسے آپ (یا آپ کی استعمال کردہ library) `raise` کر سکتی ہے۔

اور آپ اس exception کو FastAPI کے ساتھ عالمی سطح پر سنبھالنا چاہتے ہیں۔

آپ `@app.exception_handler()` کے ساتھ ایک حسب ضرورت exception handler شامل کر سکتے ہیں:

{* ../../docs_src/handling_errors/tutorial003_py310.py hl[5:7,13:18,24] *}

یہاں، اگر آپ `/unicorns/yolo` کی درخواست کرتے ہیں تو *path operation* ایک `UnicornException` `raise` کرے گی۔

لیکن اسے `unicorn_exception_handler` سنبھالے گا۔

تو آپ کو ایک صاف error ملے گا، HTTP status code `418` کے ساتھ اور ایک JSON مواد:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | تکنیکی تفصیلات

آپ `from starlette.requests import Request` اور `from starlette.responses import JSONResponse` بھی استعمال کر سکتے ہیں۔

**FastAPI** آپ کی سہولت کے لیے وہی `starlette.responses` بطور `fastapi.responses` فراہم کرتا ہے۔ لیکن زیادہ تر دستیاب responses براہ راست Starlette سے آتے ہیں۔ `Request` کے ساتھ بھی یہی معاملہ ہے۔

///

## پہلے سے طے شدہ exception handlers کو تبدیل کریں { #override-the-default-exception-handlers }

**FastAPI** کے کچھ پہلے سے طے شدہ exception handlers ہیں۔

یہ handlers جب آپ `HTTPException` `raise` کرتے ہیں اور جب request میں غلط data ہوتا ہے تو پہلے سے طے شدہ JSON responses واپس کرنے کے ذمہ دار ہوتے ہیں۔

آپ ان exception handlers کو اپنے handlers سے تبدیل کر سکتے ہیں۔

### Request validation exceptions کو تبدیل کریں { #override-request-validation-exceptions }

جب کسی request میں غلط data ہوتا ہے تو **FastAPI** اندرونی طور پر ایک `RequestValidationError` raise کرتا ہے۔

اور اس کے لیے ایک پہلے سے طے شدہ exception handler بھی شامل ہے۔

اسے تبدیل کرنے کے لیے `RequestValidationError` کو import کریں اور اسے `@app.exception_handler(RequestValidationError)` کے ساتھ exception handler کو decorate کرنے کے لیے استعمال کریں۔

Exception handler ایک `Request` اور exception وصول کرے گا۔

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[2,14:19] *}

اب اگر آپ `/items/foo` پر جائیں تو پہلے سے طے شدہ JSON error کی بجائے:

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

آپ کو ایک text version ملے گا:

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### `HTTPException` error handler کو تبدیل کریں { #override-the-httpexception-error-handler }

اسی طرح، آپ `HTTPException` handler کو بھی تبدیل کر سکتے ہیں۔

مثال کے طور پر، آپ ان errors کے لیے JSON کی بجائے سادہ text response واپس کرنا چاہ سکتے ہیں:

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[3:4,9:11,25] *}

/// note | تکنیکی تفصیلات

آپ `from starlette.responses import PlainTextResponse` بھی استعمال کر سکتے ہیں۔

**FastAPI** آپ کی سہولت کے لیے وہی `starlette.responses` بطور `fastapi.responses` فراہم کرتا ہے۔ لیکن زیادہ تر دستیاب responses براہ راست Starlette سے آتے ہیں۔

///

/// warning | انتباہ

ذہن میں رکھیں کہ `RequestValidationError` میں اس file کا نام اور لائن کی معلومات شامل ہوتی ہیں جہاں validation error ہوا تاکہ آپ چاہیں تو اپنے logs میں متعلقہ معلومات کے ساتھ اسے دکھا سکیں۔

لیکن اس کا مطلب ہے کہ اگر آپ اسے صرف string میں تبدیل کر کے وہ معلومات براہ راست واپس کریں تو آپ اپنے سسٹم کے بارے میں کچھ معلومات ظاہر کر سکتے ہیں، اسی لیے یہاں code ہر error کو الگ سے نکال کر دکھاتا ہے۔

///

### `RequestValidationError` کا body استعمال کریں { #use-the-requestvalidationerror-body }

`RequestValidationError` میں وہ `body` شامل ہوتا ہے جو غلط data کے ساتھ موصول ہوا تھا۔

آپ اسے اپنی app بناتے وقت body کو log کرنے اور debug کرنے، user کو واپس کرنے وغیرہ کے لیے استعمال کر سکتے ہیں۔

{* ../../docs_src/handling_errors/tutorial005_py310.py hl[14] *}

اب ایک غلط item بھیجنے کی کوشش کریں جیسے:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

آپ کو ایک response ملے گا جو بتائے گا کہ data غلط ہے اور اس میں موصول شدہ body شامل ہوگا:

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

#### FastAPI کا `HTTPException` بمقابلہ Starlette کا `HTTPException` { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI** کا اپنا `HTTPException` ہے۔

اور **FastAPI** کی `HTTPException` error class، Starlette کی `HTTPException` error class سے inherit ہوتی ہے۔

فرق صرف یہ ہے کہ **FastAPI** کا `HTTPException`، `detail` field کے لیے کوئی بھی JSON میں قابل تبدیل data قبول کرتا ہے، جبکہ Starlette کا `HTTPException` صرف strings قبول کرتا ہے۔

تو آپ **FastAPI** کا `HTTPException` عام طریقے سے اپنے code میں raise کرتے رہ سکتے ہیں۔

لیکن جب آپ exception handler رجسٹر کریں تو اسے Starlette کے `HTTPException` کے لیے رجسٹر کریں۔

اس طرح، اگر Starlette کے اندرونی code کا کوئی حصہ، یا کوئی Starlette extension یا plug-in، Starlette کا `HTTPException` raise کرے تو آپ کا handler اسے پکڑ کر سنبھال سکے گا۔

اس مثال میں، ایک ہی code میں دونوں `HTTPException` رکھنے کے لیے، Starlette کے exception کا نام `StarletteHTTPException` رکھا گیا ہے:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### **FastAPI** کے exception handlers دوبارہ استعمال کریں { #reuse-fastapis-exception-handlers }

اگر آپ exception کو **FastAPI** کے پہلے سے طے شدہ exception handlers کے ساتھ استعمال کرنا چاہتے ہیں تو آپ `fastapi.exception_handlers` سے پہلے سے طے شدہ exception handlers import اور دوبارہ استعمال کر سکتے ہیں:

{* ../../docs_src/handling_errors/tutorial006_py310.py hl[2:5,15,21] *}

اس مثال میں آپ بہت واضح پیغام کے ساتھ error print کر رہے ہیں، لیکن آپ کو خیال آ گیا ہوگا۔ آپ exception استعمال کر سکتے ہیں اور پھر صرف پہلے سے طے شدہ exception handlers کو دوبارہ استعمال کر سکتے ہیں۔
