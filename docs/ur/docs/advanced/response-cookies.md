# Response Cookies { #response-cookies }

## `Response` parameter استعمال کریں { #use-a-response-parameter }

آپ اپنے *path operation function* میں `Response` قسم کا parameter اعلان کر سکتے ہیں۔

اور پھر آپ اس *عارضی* response آبجیکٹ میں cookies مقرر کر سکتے ہیں۔

{* ../../docs_src/response_cookies/tutorial002_py310.py hl[1, 8:9] *}

اور پھر آپ جیسے عام طور پر کرتے ہیں، کوئی بھی آبجیکٹ واپس کر سکتے ہیں (ایک `dict`، database model وغیرہ)۔

اور اگر آپ نے `response_model` کا اعلان کیا ہے، تو اسے پھر بھی آپ کے واپس کردہ آبجیکٹ کو فلٹر اور تبدیل کرنے کے لیے استعمال کیا جائے گا۔

**FastAPI** اس *عارضی* response کو cookies (نیز headers اور status code) نکالنے کے لیے استعمال کرے گا، اور انہیں حتمی response میں ڈالے گا جس میں آپ کی واپس کردہ قدر ہوگی، کسی بھی `response_model` سے فلٹر شدہ۔

آپ dependencies میں بھی `Response` parameter کا اعلان کر سکتے ہیں، اور ان میں cookies (اور headers) مقرر کر سکتے ہیں۔

## براہ راست `Response` واپس کریں { #return-a-response-directly }

آپ اپنے کوڈ میں براہ راست `Response` واپس کرتے وقت بھی cookies بنا سکتے ہیں۔

ایسا کرنے کے لیے، آپ [براہ راست Response واپس کریں](response-directly.md) میں بیان کردہ طریقے سے response بنا سکتے ہیں۔

پھر اس میں Cookies مقرر کریں، اور پھر اسے واپس کریں:

{* ../../docs_src/response_cookies/tutorial001_py310.py hl[10:12] *}

/// tip | مشورہ

ذہن میں رکھیں کہ اگر آپ `Response` parameter استعمال کرنے کی بجائے براہ راست response واپس کرتے ہیں، تو FastAPI اسے براہ راست واپس کرے گا۔

لہذا، آپ کو یقینی بنانا ہوگا کہ آپ کا ڈیٹا صحیح قسم کا ہے۔ مثلاً اگر آپ `JSONResponse` واپس کر رہے ہیں تو یہ JSON کے موافق ہو۔

اور یہ بھی کہ آپ ایسا کوئی ڈیٹا نہیں بھیج رہے جو `response_model` سے فلٹر ہونا چاہیے تھا۔

///

### مزید معلومات { #more-info }

/// note | تکنیکی تفصیلات

آپ `from starlette.responses import Response` یا `from starlette.responses import JSONResponse` بھی استعمال کر سکتے ہیں۔

**FastAPI** وہی `starlette.responses` فراہم کرتا ہے جو `fastapi.responses` کے طور پر، بس آپ یعنی developer کی سہولت کے لیے۔ لیکن زیادہ تر دستیاب responses براہ راست Starlette سے آتے ہیں۔

اور چونکہ `Response` اکثر headers اور cookies مقرر کرنے کے لیے استعمال ہوتا ہے، **FastAPI** اسے `fastapi.Response` پر بھی فراہم کرتا ہے۔

///

تمام دستیاب parameters اور اختیارات دیکھنے کے لیے، [Starlette کی دستاویزات](https://www.starlette.dev/responses/#set-cookie) دیکھیں۔
