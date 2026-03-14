# براہ راست Response واپس کریں { #return-a-response-directly }

جب آپ **FastAPI** *path operation* بناتے ہیں تو آپ عام طور پر اس سے کوئی بھی ڈیٹا واپس کر سکتے ہیں: ایک `dict`، ایک `list`، ایک Pydantic model، database model وغیرہ۔

اگر آپ [Response Model](../tutorial/response-model.md) کا اعلان کرتے ہیں تو FastAPI اسے Pydantic استعمال کر کے ڈیٹا کو JSON میں serialize کرنے کے لیے استعمال کرے گا۔

اگر آپ response model کا اعلان نہیں کرتے، تو FastAPI [JSON Compatible Encoder](../tutorial/encoder.md) میں بیان کردہ `jsonable_encoder` استعمال کرے گا اور اسے `JSONResponse` میں ڈالے گا۔

آپ براہ راست `JSONResponse` بنا کر بھی واپس کر سکتے ہیں۔

/// tip | مشورہ

`JSONResponse` براہ راست واپس کرنے کی بجائے [Response Model](../tutorial/response-model.md) استعمال کرنے سے آپ کو عام طور پر بہت بہتر کارکردگی ملے گی، کیونکہ اس طرح یہ Pydantic کا استعمال کرتے ہوئے Rust میں ڈیٹا کو serialize کرتا ہے۔

///

## `Response` واپس کریں { #return-a-response }

آپ `Response` یا اس کی کوئی بھی sub-class واپس کر سکتے ہیں۔

/// info | معلومات

`JSONResponse` خود `Response` کی ایک sub-class ہے۔

///

اور جب آپ `Response` واپس کرتے ہیں، **FastAPI** اسے براہ راست منتقل کرے گا۔

یہ Pydantic models کے ساتھ کوئی ڈیٹا تبدیلی نہیں کرے گا، مواد کو کسی قسم میں تبدیل نہیں کرے گا وغیرہ۔

یہ آپ کو بہت زیادہ **لچک** دیتا ہے۔ آپ کسی بھی ڈیٹا قسم کو واپس کر سکتے ہیں، کسی بھی ڈیٹا اعلان یا توثیق کو تبدیل کر سکتے ہیں وغیرہ۔

یہ آپ کو بہت زیادہ **ذمہ داری** بھی دیتا ہے۔ آپ کو یقینی بنانا ہوگا کہ آپ جو ڈیٹا واپس کر رہے ہیں وہ درست ہے، صحیح فارمیٹ میں ہے، serialize ہو سکتا ہے وغیرہ۔

## `Response` میں `jsonable_encoder` استعمال کرنا { #using-the-jsonable-encoder-in-a-response }

چونکہ **FastAPI** آپ کے واپس کردہ `Response` میں کوئی تبدیلی نہیں کرتا، آپ کو یقینی بنانا ہوگا کہ اس کا مواد اس کے لیے تیار ہے۔

مثال کے طور پر، آپ Pydantic model کو `JSONResponse` میں پہلے اسے `dict` میں تبدیل کیے بغیر نہیں ڈال سکتے، جس میں تمام ڈیٹا اقسام (جیسے `datetime`، `UUID` وغیرہ) JSON کے موافق اقسام میں تبدیل ہوں۔

ان صورتوں میں، آپ `jsonable_encoder` استعمال کر سکتے ہیں اپنے ڈیٹا کو response میں دینے سے پہلے تبدیل کرنے کے لیے:

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | تکنیکی تفصیلات

آپ `from starlette.responses import JSONResponse` بھی استعمال کر سکتے ہیں۔

**FastAPI** وہی `starlette.responses` فراہم کرتا ہے جو `fastapi.responses` کے طور پر، بس آپ یعنی developer کی سہولت کے لیے۔ لیکن زیادہ تر دستیاب responses براہ راست Starlette سے آتے ہیں۔

///

## حسب ضرورت `Response` واپس کرنا { #returning-a-custom-response }

اوپر کی مثال تمام ضروری حصے دکھاتی ہے، لیکن ابھی بہت مفید نہیں ہے، کیونکہ آپ صرف `item` براہ راست واپس کر سکتے تھے، اور **FastAPI** اسے آپ کے لیے `JSONResponse` میں ڈال دیتا، اسے `dict` میں تبدیل کر دیتا وغیرہ۔ یہ سب پہلے سے طے شدہ طور پر ہوتا ہے۔

اب، آئیں دیکھتے ہیں کہ آپ اسے حسب ضرورت response واپس کرنے کے لیے کیسے استعمال کر سکتے ہیں۔

فرض کریں کہ آپ [XML](https://en.wikipedia.org/wiki/XML) response واپس کرنا چاہتے ہیں۔

آپ اپنا XML مواد ایک string میں رکھ سکتے ہیں، اسے `Response` میں ڈال سکتے ہیں، اور واپس کر سکتے ہیں:

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## Response Model کیسے کام کرتا ہے { #how-a-response-model-works }

جب آپ path operation میں [Response Model - Return Type](../tutorial/response-model.md) کا اعلان کرتے ہیں، **FastAPI** اسے Pydantic استعمال کر کے ڈیٹا کو JSON میں serialize کرنے کے لیے استعمال کرے گا۔

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

چونکہ یہ Rust کی طرف ہوگا، کارکردگی عام Python اور `JSONResponse` class سے بہت بہتر ہوگی۔

`response_model` یا return type استعمال کرتے وقت، FastAPI ڈیٹا کو تبدیل کرنے کے لیے `jsonable_encoder` (جو سست ہوتا) اور نہ `JSONResponse` class استعمال کرے گا۔

اس کی بجائے یہ response model (یا return type) استعمال کر کے Pydantic سے تیار شدہ JSON bytes لیتا ہے اور JSON کے لیے صحیح media type (`application/json`) کے ساتھ براہ راست `Response` واپس کرتا ہے۔

## نوٹس { #notes }

جب آپ براہ راست `Response` واپس کرتے ہیں تو اس کا ڈیٹا خود بخود توثیق، تبدیل (serialize) یا دستاویزی نہیں ہوتا۔

لیکن آپ پھر بھی اسے دستاویزی شکل دے سکتے ہیں جیسا کہ [OpenAPI میں اضافی Responses](additional-responses.md) میں بیان کیا گیا ہے۔

آنے والے حصوں میں آپ دیکھ سکتے ہیں کہ خودکار ڈیٹا تبدیلی، دستاویزات وغیرہ رکھتے ہوئے ان حسب ضرورت `Response` کو کیسے استعمال/اعلان کیا جائے۔
