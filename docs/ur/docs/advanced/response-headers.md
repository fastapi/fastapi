# Response Headers { #response-headers }

## `Response` parameter استعمال کریں { #use-a-response-parameter }

آپ اپنے *path operation function* میں `Response` قسم کا parameter اعلان کر سکتے ہیں (جیسا کہ آپ cookies کے لیے کر سکتے ہیں)۔

اور پھر آپ اس *عارضی* response آبجیکٹ میں headers مقرر کر سکتے ہیں۔

{* ../../docs_src/response_headers/tutorial002_py310.py hl[1, 7:8] *}

اور پھر آپ جیسے عام طور پر کرتے ہیں، کوئی بھی آبجیکٹ واپس کر سکتے ہیں (ایک `dict`، database model وغیرہ)۔

اور اگر آپ نے `response_model` کا اعلان کیا ہے، تو اسے پھر بھی آپ کے واپس کردہ آبجیکٹ کو فلٹر اور تبدیل کرنے کے لیے استعمال کیا جائے گا۔

**FastAPI** اس *عارضی* response کو headers (نیز cookies اور status code) نکالنے کے لیے استعمال کرے گا، اور انہیں حتمی response میں ڈالے گا جس میں آپ کی واپس کردہ قدر ہوگی، کسی بھی `response_model` سے فلٹر شدہ۔

آپ dependencies میں بھی `Response` parameter کا اعلان کر سکتے ہیں، اور ان میں headers (اور cookies) مقرر کر سکتے ہیں۔

## براہ راست `Response` واپس کریں { #return-a-response-directly }

آپ براہ راست `Response` واپس کرتے وقت بھی headers شامل کر سکتے ہیں۔

[براہ راست Response واپس کریں](response-directly.md) میں بیان کردہ طریقے سے response بنائیں اور headers کو اضافی parameter کے طور پر دیں:

{* ../../docs_src/response_headers/tutorial001_py310.py hl[10:12] *}

/// note | تکنیکی تفصیلات

آپ `from starlette.responses import Response` یا `from starlette.responses import JSONResponse` بھی استعمال کر سکتے ہیں۔

**FastAPI** وہی `starlette.responses` فراہم کرتا ہے جو `fastapi.responses` کے طور پر، بس آپ یعنی developer کی سہولت کے لیے۔ لیکن زیادہ تر دستیاب responses براہ راست Starlette سے آتے ہیں۔

اور چونکہ `Response` اکثر headers اور cookies مقرر کرنے کے لیے استعمال ہوتا ہے، **FastAPI** اسے `fastapi.Response` پر بھی فراہم کرتا ہے۔

///

## حسب ضرورت Headers { #custom-headers }

ذہن میں رکھیں کہ حسب ضرورت ملکیتی headers [`X-` سابقہ استعمال کر کے](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) شامل کیے جا سکتے ہیں۔

لیکن اگر آپ کے پاس حسب ضرورت headers ہیں جو آپ چاہتے ہیں کہ براؤزر میں ایک client انہیں دیکھ سکے، تو آپ کو انہیں اپنی CORS ترتیبات میں شامل کرنا ہوگا ([CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md) میں مزید پڑھیں)، [Starlette کی CORS دستاویزات](https://www.starlette.dev/middleware/#corsmiddleware) میں بیان کردہ `expose_headers` parameter استعمال کرتے ہوئے۔
