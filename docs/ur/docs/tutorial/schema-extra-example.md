# Request Example Data Declare کریں { #declare-request-example-data }

آپ اپنی ایپ کو موصول ہونے والے ڈیٹا کی مثالیں declare کر سکتے ہیں۔

یہاں ایسا کرنے کے کئی طریقے ہیں۔

## Pydantic models میں اضافی JSON Schema ڈیٹا { #extra-json-schema-data-in-pydantic-models }

آپ Pydantic model کے لیے `examples` declare کر سکتے ہیں جو تیار کردہ JSON Schema میں شامل ہوں گی۔

{* ../../docs_src/schema_extra_example/tutorial001_py310.py hl[13:24] *}

وہ اضافی معلومات جوں کی توں اس model کے آؤٹ پٹ **JSON Schema** میں شامل ہوں گی، اور API docs میں استعمال ہوں گی۔

آپ `model_config` attribute استعمال کر سکتے ہیں جو ایک `dict` لیتا ہے جیسا کہ [Pydantic کے docs: Configuration](https://docs.pydantic.dev/latest/api/config/) میں بیان ہے۔

آپ `"json_schema_extra"` کو ایک `dict` کے ساتھ سیٹ کر سکتے ہیں جس میں کوئی بھی اضافی ڈیٹا ہو جو آپ تیار کردہ JSON Schema میں دکھانا چاہتے ہیں، بشمول `examples`۔

/// tip | مشورہ

آپ اسی تکنیک کو JSON Schema کو بڑھانے اور اپنی مرضی کی اضافی معلومات شامل کرنے کے لیے استعمال کر سکتے ہیں۔

مثال کے طور پر آپ اسے frontend user interface کے لیے metadata شامل کرنے وغیرہ کے لیے استعمال کر سکتے ہیں۔

///

/// info | معلومات

OpenAPI 3.1.0 (جو FastAPI 0.99.0 سے استعمال ہو رہا ہے) نے `examples` کی سپورٹ شامل کی، جو **JSON Schema** معیار کا حصہ ہے۔

اس سے پہلے، یہ صرف `example` keyword کو ایک واحد مثال کے ساتھ سپورٹ کرتا تھا۔ یہ ابھی بھی OpenAPI 3.1.0 سے supported ہے، لیکن deprecated ہے اور JSON Schema معیار کا حصہ نہیں ہے۔ لہذا آپ کو `example` سے `examples` میں منتقل ہونے کی ترغیب دی جاتی ہے۔ 🤓

آپ اس صفحے کے آخر میں مزید پڑھ سکتے ہیں۔

///

## `Field` کے اضافی arguments { #field-additional-arguments }

Pydantic models کے ساتھ `Field()` استعمال کرتے وقت، آپ اضافی `examples` بھی declare کر سکتے ہیں:

{* ../../docs_src/schema_extra_example/tutorial002_py310.py hl[2,8:11] *}

## JSON Schema - OpenAPI میں `examples` { #examples-in-json-schema-openapi }

ان میں سے کوئی بھی استعمال کرتے وقت:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

آپ اضافی معلومات کے ساتھ `examples` کا ایک گروپ بھی declare کر سکتے ہیں جو **OpenAPI** کے اندر ان کے **JSON Schemas** میں شامل ہوں گے۔

### `examples` کے ساتھ `Body` { #body-with-examples }

یہاں ہم `Body()` میں متوقع ڈیٹا کی ایک مثال پر مشتمل `examples` پاس کر رہے ہیں:

{* ../../docs_src/schema_extra_example/tutorial003_an_py310.py hl[22:29] *}

### Docs UI میں مثال { #example-in-the-docs-ui }

اوپر کے کسی بھی طریقے سے یہ `/docs` میں اس طرح نظر آئے گا:

<img src="/img/tutorial/body-fields/image01.png">

### متعدد `examples` کے ساتھ `Body` { #body-with-multiple-examples }

آپ یقیناً متعدد `examples` بھی پاس کر سکتے ہیں:

{* ../../docs_src/schema_extra_example/tutorial004_an_py310.py hl[23:38] *}

جب آپ ایسا کریں، تو مثالیں اس body ڈیٹا کے اندرونی **JSON Schema** کا حصہ ہوں گی۔

تاہم، <dfn title="2023-08-26">اس تحریر کے وقت</dfn>، Swagger UI، جو docs UI دکھانے کا ذمہ دار ٹول ہے، **JSON Schema** میں ڈیٹا کی متعدد مثالیں دکھانے کی سپورٹ نہیں کرتا۔ لیکن ایک حل کے لیے نیچے پڑھیں۔

### OpenAPI-مخصوص `examples` { #openapi-specific-examples }

**JSON Schema** نے `examples` کی سپورٹ سے پہلے ہی OpenAPI میں ایک مختلف field جس کا نام بھی `examples` تھا، کی سپورٹ موجود تھی۔

یہ **OpenAPI-مخصوص** `examples` OpenAPI specification کے ایک اور حصے میں جاتا ہے۔ یہ **ہر *path operation* کی تفصیلات** میں جاتا ہے، ہر JSON Schema کے اندر نہیں۔

اور Swagger UI نے اس مخصوص `examples` field کو کافی عرصے سے سپورٹ کیا ہے۔ تو آپ اسے docs UI میں مختلف **مثالیں دکھانے** کے لیے استعمال کر سکتے ہیں۔

اس OpenAPI-مخصوص field `examples` کی شکل ایک `dict` ہے جس میں **متعدد مثالیں** ہیں (`list` کی بجائے)، ہر ایک میں اضافی معلومات جو **OpenAPI** میں بھی شامل ہوں گی۔

یہ OpenAPI میں موجود ہر JSON Schema کے اندر نہیں جاتا، بلکہ *path operation* میں براہ راست باہر جاتا ہے۔

### `openapi_examples` Parameter کا استعمال { #using-the-openapi-examples-parameter }

آپ FastAPI میں OpenAPI-مخصوص `examples` کو `openapi_examples` parameter کے ساتھ declare کر سکتے ہیں، ان کے لیے:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

`dict` کی keys ہر مثال کی شناخت کرتی ہیں، اور ہر قدر ایک اور `dict` ہے۔

`examples` میں ہر مخصوص مثال `dict` میں یہ شامل ہو سکتا ہے:

* `summary`: مثال کی مختصر وضاحت۔
* `description`: ایک تفصیلی وضاحت جس میں Markdown متن ہو سکتا ہے۔
* `value`: یہ اصل مثال ہے جو دکھائی جاتی ہے، مثلاً ایک `dict`۔
* `externalValue`: `value` کا متبادل، مثال کی طرف اشارہ کرنے والا URL۔ اگرچہ یہ شاید اتنے ٹولز سے supported نہ ہو جتنا `value` ہے۔

آپ اسے اس طرح استعمال کر سکتے ہیں:

{* ../../docs_src/schema_extra_example/tutorial005_an_py310.py hl[23:49] *}

### Docs UI میں OpenAPI مثالیں { #openapi-examples-in-the-docs-ui }

`Body()` میں `openapi_examples` شامل کرنے سے `/docs` اس طرح نظر آئے گا:

<img src="/img/tutorial/body-fields/image02.png">

## تکنیکی تفصیلات { #technical-details }

/// tip | مشورہ

اگر آپ پہلے سے **FastAPI** version **0.99.0 یا اس سے اوپر** استعمال کر رہے ہیں، تو شاید آپ ان تفصیلات کو **چھوڑ** سکتے ہیں۔

یہ پرانے versions کے لیے زیادہ متعلقہ ہیں، جب OpenAPI 3.1.0 دستیاب نہیں تھا۔

آپ اسے OpenAPI اور JSON Schema کی ایک مختصر **تاریخ کا سبق** سمجھ سکتے ہیں۔ 🤓

///

/// warning | انتباہ

یہ **JSON Schema** اور **OpenAPI** معیارات کے بارے میں بہت تکنیکی تفصیلات ہیں۔

اگر اوپر بیان کیے گئے خیالات آپ کے لیے پہلے سے کام کر رہے ہیں، تو یہ کافی ہو سکتا ہے، اور شاید آپ کو ان تفصیلات کی ضرورت نہ ہو، بلا جھجک انہیں چھوڑ دیں۔

///

OpenAPI 3.1.0 سے پہلے، OpenAPI **JSON Schema** کا ایک پرانا اور ترمیم شدہ ورژن استعمال کرتا تھا۔

JSON Schema میں `examples` نہیں تھا، اس لیے OpenAPI نے اپنے ترمیم شدہ ورژن میں اپنا `example` field شامل کیا۔

OpenAPI نے specification کے دوسرے حصوں میں بھی `example` اور `examples` fields شامل کیے:

* [`Parameter Object` (specification میں)](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object) جو FastAPI کے ان میں استعمال ہوتا تھا:
    * `Path()`
    * `Query()`
    * `Header()`
    * `Cookie()`
* [`Request Body Object`، `content` field میں، `Media Type Object` پر (specification میں)](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object) جو FastAPI کے ان میں استعمال ہوتا تھا:
    * `Body()`
    * `File()`
    * `Form()`

/// info | معلومات

یہ پرانا OpenAPI-مخصوص `examples` parameter اب FastAPI `0.103.0` سے `openapi_examples` ہے۔

///

### JSON Schema کا `examples` field { #json-schemas-examples-field }

لیکن پھر JSON Schema نے specification کے ایک نئے ورژن میں [`examples`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5) field شامل کیا۔

اور پھر نیا OpenAPI 3.1.0 تازہ ترین ورژن (JSON Schema 2020-12) پر مبنی تھا جس میں یہ نیا `examples` field شامل تھا۔

اور اب یہ نیا `examples` field پرانے واحد (اور حسب ضرورت) `example` field پر فوقیت رکھتا ہے، جو اب deprecated ہے۔

JSON Schema میں یہ نیا `examples` field **صرف ایک `list`** مثالوں کی ہے، نہ کہ اضافی metadata کے ساتھ dict جیسا OpenAPI کے دوسرے مقامات پر ہے (اوپر بیان کیا گیا)۔

/// info | معلومات

OpenAPI 3.1.0 ریلیز ہونے کے بعد بھی JSON Schema کے ساتھ اس نئے آسان انضمام کے ساتھ، کچھ عرصے تک Swagger UI، جو خودکار docs فراہم کرنے والا ٹول ہے، OpenAPI 3.1.0 سپورٹ نہیں کرتا تھا (یہ version 5.0.0 سے سپورٹ کرتا ہے 🎉)۔

اسی وجہ سے، 0.99.0 سے پہلے کے FastAPI versions ابھی بھی 3.1.0 سے نچلے OpenAPI versions استعمال کرتے تھے۔

///

### Pydantic اور FastAPI `examples` { #pydantic-and-fastapi-examples }

جب آپ Pydantic model کے اندر `examples` شامل کرتے ہیں، `schema_extra` یا `Field(examples=["something"])` استعمال کر کے، تو وہ مثال اس Pydantic model کے **JSON Schema** میں شامل ہو جاتی ہے۔

اور وہ Pydantic model کا **JSON Schema** آپ کی API کے **OpenAPI** میں شامل ہوتا ہے، اور پھر docs UI میں استعمال ہوتا ہے۔

0.99.0 سے پہلے کے FastAPI versions میں (0.99.0 اور اس سے اوپر نئے OpenAPI 3.1.0 استعمال کرتے ہیں) جب آپ کسی دوسری utilities (`Query()`، `Body()` وغیرہ) کے ساتھ `example` یا `examples` استعمال کرتے تھے تو وہ مثالیں JSON Schema میں شامل نہیں ہوتی تھیں جو اس ڈیٹا کو بیان کرتا ہے (نہ ہی OpenAPI کے اپنے JSON Schema ورژن میں)، بلکہ وہ OpenAPI میں *path operation* declaration میں براہ راست شامل ہوتی تھیں (JSON Schema استعمال کرنے والے OpenAPI حصوں سے باہر)۔

لیکن اب جب FastAPI 0.99.0 اور اس سے اوپر OpenAPI 3.1.0 استعمال کرتا ہے، جو JSON Schema 2020-12 استعمال کرتا ہے، اور Swagger UI 5.0.0 اور اس سے اوپر، سب کچھ زیادہ مستقل ہے اور مثالیں JSON Schema میں شامل ہیں۔

### Swagger UI اور OpenAPI-مخصوص `examples` { #swagger-ui-and-openapi-specific-examples }

اب، چونکہ Swagger UI متعدد JSON Schema مثالیں سپورٹ نہیں کرتا تھا (2023-08-26 تک)، صارفین کے پاس docs میں متعدد مثالیں دکھانے کا کوئی طریقہ نہیں تھا۔

اسے حل کرنے کے لیے، FastAPI `0.103.0` نے نئے parameter `openapi_examples` کے ساتھ اسی پرانے **OpenAPI-مخصوص** `examples` field کو declare کرنے کی **سپورٹ شامل** کی۔ 🤓

### خلاصہ { #summary }

میں کہا کرتا تھا کہ مجھے تاریخ زیادہ پسند نہیں... اور دیکھیں اب میں "ٹیک تاریخ" کے سبق دے رہا ہوں۔ 😅

مختصراً، **FastAPI 0.99.0 یا اس سے اوپر اپ گریڈ کریں**، اور چیزیں بہت **آسان، مستقل، اور بدیہی** ہیں، اور آپ کو یہ تمام تاریخی تفصیلات جاننے کی ضرورت نہیں ہے۔ 😎
