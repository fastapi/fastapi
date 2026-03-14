# Request کا براہ راست استعمال { #using-the-request-directly }

اب تک، آپ request کے ان حصوں کو ان کی اقسام کے ساتھ بیان کرتے رہے ہیں جن کی آپ کو ضرورت ہے۔

ڈیٹا لے رہے ہیں:

* Path سے بطور parameters۔
* Headers سے۔
* Cookies سے۔
* وغیرہ۔

اور ایسا کرنے سے، **FastAPI** اس ڈیٹا کو validate کر رہا ہے، اسے تبدیل کر رہا ہے اور آپ کے API کے لیے خود بخود دستاویزات بنا رہا ہے۔

لیکن ایسے حالات ہیں جہاں آپ کو `Request` آبجیکٹ تک براہ راست رسائی کی ضرورت ہو سکتی ہے۔

## `Request` آبجیکٹ کی تفصیلات { #details-about-the-request-object }

چونکہ **FastAPI** دراصل اوپر کئی ٹولز کی تہہ کے ساتھ **Starlette** ہے، آپ Starlette کے [`Request`](https://www.starlette.dev/requests/) آبجیکٹ کو ضرورت پڑنے پر براہ راست استعمال کر سکتے ہیں۔

اس کا مطلب یہ بھی ہوگا کہ اگر آپ `Request` آبجیکٹ سے براہ راست ڈیٹا حاصل کریں (مثلاً body پڑھیں) تو اسے FastAPI کے ذریعے validate، تبدیل یا دستاویز (OpenAPI کے ساتھ، خودکار API user interface کے لیے) نہیں کیا جائے گا۔

حالانکہ عام طور پر بیان کردہ کوئی بھی دوسرا parameter (مثلاً Pydantic model کے ساتھ body) پھر بھی validate، تبدیل، annotate وغیرہ ہوگا۔

لیکن مخصوص صورتیں ہیں جہاں `Request` آبجیکٹ حاصل کرنا مفید ہے۔

## `Request` آبجیکٹ کا براہ راست استعمال { #use-the-request-object-directly }

فرض کریں آپ اپنے *path operation function* کے اندر client کا IP address/host حاصل کرنا چاہتے ہیں۔

اس کے لیے آپ کو request تک براہ راست رسائی درکار ہے۔

{* ../../docs_src/using_request_directly/tutorial001_py310.py hl[1,7:8] *}

*path operation function* parameter کی قسم `Request` بیان کرنے سے **FastAPI** جان لے گا کہ اس parameter میں `Request` پاس کرنا ہے۔

/// tip | مشورہ

غور کریں کہ اس صورت میں، ہم request parameter کے ساتھ ساتھ path parameter بھی بیان کر رہے ہیں۔

تو، path parameter نکالا جائے گا، validate ہوگا، مخصوص قسم میں تبدیل ہوگا اور OpenAPI کے ساتھ annotate ہوگا۔

اسی طرح، آپ عام طریقے سے کوئی بھی دوسرا parameter بیان کر سکتے ہیں، اور اس کے ساتھ `Request` بھی حاصل کر سکتے ہیں۔

///

## `Request` دستاویزات { #request-documentation }

آپ [`Request` آبجیکٹ کے بارے میں مزید تفصیلات Starlette کی سرکاری دستاویزات سائٹ](https://www.starlette.dev/requests/) پر پڑھ سکتے ہیں۔

/// note | تکنیکی تفصیلات

آپ `from starlette.requests import Request` بھی استعمال کر سکتے ہیں۔

**FastAPI** اسے آپ کی سہولت کے لیے براہ راست فراہم کرتا ہے۔ لیکن یہ براہ راست Starlette سے آتا ہے۔

///
