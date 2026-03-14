# Input اور Output کے لیے الگ OpenAPI Schemas یا نہیں { #separate-openapi-schemas-for-input-and-output-or-not }

**Pydantic v2** کی ریلیز کے بعد سے، تیار کردہ OpenAPI پہلے سے کچھ زیادہ درست اور **صحیح** ہے۔ 😎

درحقیقت، بعض صورتوں میں، ایک ہی Pydantic model کے لیے OpenAPI میں **دو JSON Schemas** ہوں گے، input اور output کے لیے، اس بات پر منحصر ہے کہ آیا ان میں **default values** ہیں۔

آئیے دیکھتے ہیں کہ یہ کیسے کام کرتا ہے اور اگر آپ کو ضرورت ہو تو اسے کیسے تبدیل کیا جائے۔

## Input اور Output کے لیے Pydantic Models { #pydantic-models-for-input-and-output }

فرض کریں کہ آپ کے پاس default values کے ساتھ ایک Pydantic model ہے، جیسے یہ:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:7] hl[7] *}

### Input کے لیے Model { #model-for-input }

اگر آپ اس model کو اس طرح input کے طور پر استعمال کرتے ہیں:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:15] hl[14] *}

...تو `description` field **ضروری نہیں** ہوگا۔ کیونکہ اس کی default value `None` ہے۔

### Docs میں Input Model { #input-model-in-docs }

آپ docs میں تصدیق کر سکتے ہیں، `description` field پر **سرخ ستارہ** نہیں ہے، اسے ضروری نشان زد نہیں کیا گیا:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image01.png">
</div>

### Output کے لیے Model { #model-for-output }

لیکن اگر آپ وہی model output کے طور پر استعمال کرتے ہیں، جیسے یہاں:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py hl[19] *}

...تو چونکہ `description` کی default value ہے، اگر آپ اس field کے لیے **کچھ واپس نہیں کرتے**، تو اس میں پھر بھی وہ **default value** ہوگی۔

### Output Response ڈیٹا کے لیے Model { #model-for-output-response-data }

اگر آپ docs کے ساتھ تعامل کریں اور response چیک کریں، حالانکہ کوڈ نے `description` fields میں سے کسی ایک میں کچھ نہیں ڈالا، JSON response میں default value (`null`) موجود ہے:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image02.png">
</div>

اس کا مطلب ہے کہ اس میں **ہمیشہ ایک قدر** ہوگی، بس بعض اوقات قدر `None` (یا JSON میں `null`) ہو سکتی ہے۔

اس کا مطلب ہے کہ، آپ کی API استعمال کرنے والے clients کو یہ جانچنے کی ضرورت نہیں کہ قدر موجود ہے یا نہیں، وہ **فرض کر سکتے ہیں کہ field ہمیشہ موجود رہے گا**، بس بعض صورتوں میں اس کی default value `None` ہوگی۔

OpenAPI میں اس کی وضاحت کا طریقہ یہ ہے کہ اس field کو **ضروری** نشان زد کیا جائے، کیونکہ یہ ہمیشہ موجود رہے گا۔

اس وجہ سے، کسی model کا JSON Schema اس بات پر منحصر ہو کر مختلف ہو سکتا ہے کہ یہ **input یا output** کے لیے استعمال ہو رہا ہے:

* **input** کے لیے `description` **ضروری نہیں** ہوگا
* **output** کے لیے یہ **ضروری** ہوگا (اور ممکنہ طور پر `None` ہو، یا JSON کی اصطلاح میں `null`)

### Docs میں Output کے لیے Model { #model-for-output-in-docs }

آپ docs میں output model بھی چیک کر سکتے ہیں، `name` اور `description` **دونوں** **سرخ ستارے** کے ساتھ **ضروری** نشان زد ہیں:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image03.png">
</div>

### Docs میں Input اور Output کے لیے Model { #model-for-input-and-output-in-docs }

اور اگر آپ OpenAPI میں تمام دستیاب Schemas (JSON Schemas) چیک کریں، تو آپ دیکھیں گے کہ دو ہیں، ایک `Item-Input` اور ایک `Item-Output`۔

`Item-Input` کے لیے، `description` **ضروری نہیں** ہے، اس پر سرخ ستارہ نہیں ہے۔

لیکن `Item-Output` کے لیے، `description` **ضروری** ہے، اس پر سرخ ستارہ ہے۔

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image04.png">
</div>

**Pydantic v2** کی اس خصوصیت کے ساتھ، آپ کی API documentation زیادہ **درست** ہے، اور اگر آپ کے پاس خود کار طریقے سے تیار کردہ clients اور SDKs ہیں، تو وہ بھی زیادہ درست ہوں گے، بہتر **developer experience** اور consistency کے ساتھ۔ 🎉

## Schemas کو الگ نہ کریں { #do-not-separate-schemas }

اب، کچھ ایسے معاملات ہیں جہاں آپ input اور output کے لیے **ایک ہی schema** رکھنا چاہ سکتے ہیں۔

شاید اس کا سب سے اہم استعمال یہ ہے کہ اگر آپ کے پاس پہلے سے کچھ خود کار طریقے سے تیار کردہ client کوڈ/SDKs ہیں اور آپ ابھی تمام خود کار تیار کردہ client کوڈ/SDKs کو اپ ڈیٹ نہیں کرنا چاہتے، آپ شاید کسی وقت یہ کرنا چاہیں گے، لیکن شاید ابھی نہیں۔

اس صورت میں، آپ **FastAPI** میں یہ خصوصیت `separate_input_output_schemas=False` parameter کے ساتھ غیر فعال کر سکتے ہیں۔

/// info | معلومات

`separate_input_output_schemas` کی سپورٹ FastAPI `0.102.0` میں شامل کی گئی تھی۔ 🤓

///

{* ../../docs_src/separate_openapi_schemas/tutorial002_py310.py hl[10] *}

### Docs میں Input اور Output Models کے لیے ایک ہی Schema { #same-schema-for-input-and-output-models-in-docs }

اور اب input اور output کے لیے model کا ایک ہی schema ہوگا، صرف `Item`، اور اس میں `description` **ضروری نہیں** ہوگا:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image05.png">
</div>
