# OpenAPI کی توسیع { #extending-openapi }

کچھ ایسے معاملات ہیں جہاں آپ کو تیار کردہ OpenAPI schema میں ترمیم کرنے کی ضرورت ہو سکتی ہے۔

اس حصے میں آپ دیکھیں گے کہ یہ کیسے کریں۔

## عام عمل { #the-normal-process }

عام (default) عمل درج ذیل ہے۔

ایک `FastAPI` application (instance) میں `.openapi()` method ہوتا ہے جس سے OpenAPI schema واپس آنے کی توقع ہوتی ہے۔

Application object بنانے کے حصے کے طور پر، `/openapi.json` (یا جو بھی آپ نے اپنا `openapi_url` سیٹ کیا ہو) کے لیے ایک *path operation* رجسٹر ہوتی ہے۔

یہ صرف application کے `.openapi()` method کے نتیجے کے ساتھ JSON response واپس کرتی ہے۔

بطور default، `.openapi()` method `.openapi_schema` property کو چیک کرتی ہے کہ آیا اس میں مواد ہے اور اسے واپس کرتی ہے۔

اگر نہیں ہے، تو یہ `fastapi.openapi.utils.get_openapi` پر موجود utility function کا استعمال کرتے ہوئے انہیں تیار کرتی ہے۔

اور وہ `get_openapi()` function بطور parameters یہ وصول کرتا ہے:

* `title`: OpenAPI کا عنوان، docs میں دکھایا جاتا ہے۔
* `version`: آپ کی API کا ورژن، مثلاً `2.5.0`۔
* `openapi_version`: استعمال شدہ OpenAPI specification کا ورژن۔ بطور default، تازہ ترین: `3.1.0`۔
* `summary`: API کا مختصر خلاصہ۔
* `description`: آپ کی API کی تفصیل، اس میں markdown شامل ہو سکتا ہے اور docs میں دکھایا جائے گا۔
* `routes`: Routes کی فہرست، یہ ہر ایک رجسٹر شدہ *path operations* ہیں۔ یہ `app.routes` سے لیے جاتے ہیں۔

/// info | معلومات

`summary` parameter OpenAPI 3.1.0 اور اس سے اوپر میں دستیاب ہے، جسے FastAPI 0.99.0 اور اس سے اوپر سپورٹ کرتا ہے۔

///

## Defaults کو override کرنا { #overriding-the-defaults }

اوپر دی گئی معلومات کا استعمال کرتے ہوئے، آپ اسی utility function کو OpenAPI schema تیار کرنے کے لیے استعمال کر سکتے ہیں اور ہر اس حصے کو override کر سکتے ہیں جس کی آپ کو ضرورت ہے۔

مثال کے طور پر، آئیے [ReDoc کی OpenAPI extension شامل کریں تاکہ حسب ضرورت logo شامل ہو](https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo)۔

### عام **FastAPI** { #normal-fastapi }

سب سے پہلے، اپنی تمام **FastAPI** application معمول کے مطابق لکھیں:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[1,4,7:9] *}

### OpenAPI schema تیار کریں { #generate-the-openapi-schema }

پھر، `custom_openapi()` function کے اندر OpenAPI schema تیار کرنے کے لیے وہی utility function استعمال کریں:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[2,15:21] *}

### OpenAPI schema میں ترمیم کریں { #modify-the-openapi-schema }

اب آپ ReDoc extension شامل کر سکتے ہیں، OpenAPI schema میں `info` "object" میں حسب ضرورت `x-logo` شامل کر کے:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[22:24] *}

### OpenAPI schema کو cache کریں { #cache-the-openapi-schema }

آپ `.openapi_schema` property کو "cache" کے طور پر استعمال کر سکتے ہیں، اپنا تیار کردہ schema ذخیرہ کرنے کے لیے۔

اس طرح، آپ کی application کو ہر بار جب کوئی صارف آپ کے API docs کھولے schema دوبارہ تیار نہیں کرنا پڑے گا۔

یہ صرف ایک بار تیار ہوگا، اور پھر اگلی requests کے لیے وہی cached schema استعمال ہوگا۔

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[13:14,25:26] *}

### Method کو override کریں { #override-the-method }

اب آپ `.openapi()` method کو اپنے نئے function سے تبدیل کر سکتے ہیں۔

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[29] *}

### جانچ کریں { #check-it }

جب آپ [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) پر جائیں گے تو آپ دیکھیں گے کہ آپ اپنا حسب ضرورت logo استعمال کر رہے ہیں (اس مثال میں، **FastAPI** کا logo):

<img src="/img/tutorial/extending-openapi/image01.png">
