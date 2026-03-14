# Response Model - Return Type { #response-model-return-type }

آپ *path operation function* کے **return type** کی annotation لگا کر response کے لیے استعمال ہونے والی type declare کر سکتے ہیں۔

آپ **type annotations** کو اسی طرح استعمال کر سکتے ہیں جیسے آپ function **parameters** میں input data کے لیے کرتے ہیں، آپ Pydantic models، lists، dictionaries، scalar values جیسے integers، booleans، وغیرہ استعمال کر سکتے ہیں۔

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

FastAPI اس return type کو ان مقاصد کے لیے استعمال کرے گا:

* واپس آنے والے ڈیٹا کی **تصدیق (Validate)** کرنا۔
    * اگر ڈیٹا غلط ہے (مثلاً کوئی field غائب ہے)، تو اس کا مطلب ہے کہ *آپ کے* ایپ کا code ٹوٹا ہوا ہے، جو واپس کرنا چاہیے وہ واپس نہیں کر رہا، اور غلط ڈیٹا واپس کرنے کی بجائے server error واپس کرے گا۔ اس طرح آپ اور آپ کے clients یقین رکھ سکتے ہیں کہ انہیں متوقع ڈیٹا اور ڈیٹا کی شکل ملے گی۔
* OpenAPI *path operation* میں response کے لیے **JSON Schema** شامل کرنا۔
    * یہ **خودکار docs** کے لیے استعمال ہوگا۔
    * یہ خودکار client code generation ٹولز بھی استعمال کریں گے۔
* Pydantic استعمال کر کے واپس آنے والے ڈیٹا کو JSON میں **Serialize** کرنا، جو **Rust** میں لکھا گیا ہے، اس لیے یہ **بہت تیز** ہوگا۔

لیکن سب سے اہم بات:

* یہ آؤٹ پٹ ڈیٹا کو return type میں جو define ہے اس تک **محدود اور فلٹر** کرے گا۔
    * یہ خاص طور پر **سیکیورٹی** کے لیے اہم ہے، اس کے بارے میں ہم نیچے مزید دیکھیں گے۔

## `response_model` Parameter { #response-model-parameter }

کچھ ایسے معاملات ہیں جہاں آپ کو ایسا ڈیٹا واپس کرنا ہوتا ہے جو بالکل وہی نہیں ہوتا جو type declare کرتی ہے۔

مثال کے طور پر، آپ ایک **dictionary** یا database object واپس کرنا چاہتے ہیں، لیکن **اسے Pydantic model کے طور پر declare** کرنا چاہتے ہیں۔ اس طرح Pydantic model آپ کے واپس کیے گئے object (مثلاً dictionary یا database object) کے لیے تمام ڈیٹا documentation، validation، وغیرہ کرے گا۔

اگر آپ نے return type annotation لگائی ہے، تو ٹولز اور editors ایک (درست) error کے ساتھ شکایت کریں گے کہ آپ کا function ایسی type واپس کر رہا ہے (مثلاً dict) جو آپ نے declare کی ہے (مثلاً Pydantic model) اس سے مختلف ہے۔

ان معاملات میں، آپ return type کی بجائے *path operation decorator* parameter `response_model` استعمال کر سکتے ہیں۔

آپ `response_model` parameter کو کسی بھی *path operation* میں استعمال کر سکتے ہیں:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* وغیرہ

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | نوٹ

نوٹ کریں کہ `response_model` "decorator" method (`get`، `post`، وغیرہ) کا parameter ہے۔ آپ کے *path operation function* کا نہیں، جیسے تمام parameters اور body۔

///

`response_model` وہی type قبول کرتا ہے جو آپ Pydantic model field کے لیے declare کرتے ہیں، لہذا یہ ایک Pydantic model ہو سکتا ہے، لیکن یہ مثلاً Pydantic models کی `list` بھی ہو سکتی ہے، جیسے `List[Item]`۔

FastAPI اس `response_model` کو تمام ڈیٹا documentation، validation، وغیرہ کے لیے استعمال کرے گا اور ساتھ ہی آؤٹ پٹ ڈیٹا کو اس کی type declaration کے مطابق **تبدیل اور فلٹر** بھی کرے گا۔

/// tip | مشورہ

اگر آپ کے editor، mypy، وغیرہ میں سخت type checks ہیں، تو آپ function return type کو `Any` declare کر سکتے ہیں۔

اس طرح آپ editor کو بتاتے ہیں کہ آپ جان بوجھ کر کچھ بھی واپس کر رہے ہیں۔ لیکن FastAPI پھر بھی `response_model` کے ساتھ ڈیٹا documentation، validation، filtering وغیرہ کرے گا۔

///

### `response_model` کی ترجیح { #response-model-priority }

اگر آپ return type اور `response_model` دونوں declare کریں، تو `response_model` کو ترجیح ملے گی اور FastAPI اسے استعمال کرے گا۔

اس طرح آپ اپنے functions میں درست type annotations لگا سکتے ہیں چاہے آپ response model سے مختلف type واپس کر رہے ہوں، تاکہ editor اور mypy جیسے ٹولز استعمال ہو سکیں۔ اور پھر بھی FastAPI `response_model` استعمال کر کے ڈیٹا validation، documentation وغیرہ کرے گا۔

آپ `response_model=None` بھی استعمال کر سکتے ہیں تاکہ اس *path operation* کے لیے response model بنانا بند ہو، آپ کو ایسا کرنا پڑ سکتا ہے اگر آپ ایسی چیزوں کے لیے type annotations لگا رہے ہیں جو درست Pydantic fields نہیں ہیں، نیچے کسی حصے میں آپ اس کی مثال دیکھیں گے۔

## وہی input ڈیٹا واپس کریں { #return-the-same-input-data }

یہاں ہم ایک `UserIn` model declare کر رہے ہیں، جس میں سادہ متن کا password ہوگا:

{* ../../docs_src/response_model/tutorial002_py310.py hl[7,9] *}

/// info | معلومات

`EmailStr` استعمال کرنے کے لیے، پہلے [`email-validator`](https://github.com/JoshData/python-email-validator) install کریں۔

یقینی بنائیں کہ آپ ایک [virtual environment](../virtual-environments.md) بنائیں، اسے activate کریں، اور پھر اسے install کریں، مثال کے طور پر:

```console
$ pip install email-validator
```

یا اس کے ساتھ:

```console
$ pip install "pydantic[email]"
```

///

اور ہم اسی model کو اپنے input اور اسی model کو اپنے output declare کرنے کے لیے استعمال کر رہے ہیں:

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

اب، جب بھی کوئی browser password کے ساتھ user بنائے گا، API اسی password کو response میں واپس کرے گا۔

اس صورت میں، شاید یہ مسئلہ نہ ہو، کیونکہ وہی user password بھیج رہا ہے۔

لیکن اگر ہم کسی اور *path operation* کے لیے وہی model استعمال کریں، تو ہم اپنے user کے passwords ہر client کو بھیج سکتے ہیں۔

/// danger

کبھی بھی user کا سادہ password ذخیرہ نہ کریں اور نہ ہی اسے اس طرح response میں بھیجیں، جب تک کہ آپ تمام خطرات سے واقف نہ ہوں اور جانتے ہوں کہ آپ کیا کر رہے ہیں۔

///

## آؤٹ پٹ model شامل کریں { #add-an-output-model }

ہم اس کی بجائے ایک input model سادہ متن کے password کے ساتھ اور ایک output model بغیر password کے بنا سکتے ہیں:

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

یہاں، اگرچہ ہمارا *path operation function* وہی input user واپس کر رہا ہے جس میں password ہے:

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

...ہم نے `response_model` کو اپنے model `UserOut` کے طور پر declare کیا ہے، جس میں password شامل نہیں ہے:

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

تو، **FastAPI** آؤٹ پٹ model میں declare نہ کیے گئے تمام ڈیٹا کو فلٹر کر دے گا (Pydantic استعمال کر کے)۔

### `response_model` یا Return Type { #response-model-or-return-type }

اس صورت میں، چونکہ دونوں models مختلف ہیں، اگر ہم function return type کو `UserOut` annotate کریں، تو editor اور ٹولز شکایت کریں گے کہ ہم غلط type واپس کر رہے ہیں، کیونکہ یہ مختلف classes ہیں۔

اسی لیے اس مثال میں ہمیں اسے `response_model` parameter میں declare کرنا پڑتا ہے۔

...لیکن نیچے پڑھتے رہیں تاکہ دیکھیں اس پر کیسے قابو پایا جائے۔

## Return Type اور ڈیٹا Filtering { #return-type-and-data-filtering }

آئیے پچھلی مثال سے آگے بڑھتے ہیں۔ ہم **function کو ایک type سے annotate** کرنا چاہتے تھے، لیکن ہم function سے ایسی چیز واپس کرنا چاہتے تھے جس میں دراصل **مزید ڈیٹا** شامل ہو۔

ہم چاہتے ہیں کہ FastAPI response model استعمال کر کے ڈیٹا **فلٹر** کرتا رہے۔ تاکہ اگرچہ function مزید ڈیٹا واپس کرے، response میں صرف وہی fields شامل ہوں جو response model میں declare ہیں۔

پچھلی مثال میں، چونکہ classes مختلف تھیں، ہمیں `response_model` parameter استعمال کرنا پڑا۔ لیکن اس کا مطلب یہ بھی ہے کہ ہمیں function return type کی جانچ کے لیے editor اور ٹولز کی سہولت نہیں ملتی۔

لیکن زیادہ تر معاملات میں جہاں ہمیں ایسا کچھ کرنا ہوتا ہے، ہم چاہتے ہیں کہ model صرف اس مثال کی طرح کچھ ڈیٹا **فلٹر/ہٹا** دے۔

اور ان معاملات میں، ہم classes اور inheritance استعمال کر کے function **type annotations** کا فائدہ اٹھا سکتے ہیں تاکہ editor اور ٹولز میں بہتر سہولت ملے، اور ساتھ ہی FastAPI **ڈیٹا filtering** بھی ہو۔

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

اس سے ہمیں editors اور mypy سے ٹولنگ سپورٹ ملتی ہے کیونکہ types کے لحاظ سے یہ code درست ہے، لیکن ہمیں FastAPI سے ڈیٹا filtering بھی ملتی ہے۔

یہ کیسے کام کرتا ہے؟ آئیے دیکھتے ہیں۔ 🤓

### Type Annotations اور ٹولنگ { #type-annotations-and-tooling }

پہلے دیکھتے ہیں کہ editors، mypy اور دیگر ٹولز اسے کیسے دیکھیں گے۔

`BaseUser` میں بنیادی fields ہیں۔ پھر `UserIn` `BaseUser` سے inherit کرتی ہے اور `password` field شامل کرتی ہے، تو اس میں دونوں models کے تمام fields شامل ہوں گے۔

ہم function return type کو `BaseUser` annotate کرتے ہیں، لیکن دراصل ایک `UserIn` instance واپس کر رہے ہیں۔

Editor، mypy، اور دیگر ٹولز اس پر شکایت نہیں کریں گے کیونکہ، typing کے لحاظ سے، `UserIn` `BaseUser` کی subclass ہے، جس کا مطلب ہے کہ جہاں `BaseUser` متوقع ہو وہاں یہ ایک *درست* type ہے۔

### FastAPI ڈیٹا Filtering { #fastapi-data-filtering }

اب، FastAPI return type دیکھے گا اور یقینی بنائے گا کہ آپ جو واپس کریں اس میں **صرف** وہ fields شامل ہوں جو type میں declare ہیں۔

FastAPI اندرونی طور پر Pydantic کے ساتھ کئی چیزیں کرتا ہے تاکہ یقینی بنایا جا سکے کہ class inheritance کے وہی قواعد واپس آنے والے ڈیٹا کی filtering کے لیے استعمال نہ ہوں، ورنہ آپ توقع سے بہت زیادہ ڈیٹا واپس کر سکتے ہیں۔

اس طرح، آپ کو دونوں جہانوں کا بہترین مل سکتا ہے: **ٹولنگ سپورٹ** کے ساتھ type annotations اور **ڈیٹا filtering**۔

## Docs میں دیکھیں { #see-it-in-the-docs }

جب آپ خودکار docs دیکھیں، تو آپ چیک کر سکتے ہیں کہ input model اور output model دونوں کا اپنا JSON Schema ہوگا:

<img src="/img/tutorial/response-model/image01.png">

اور دونوں models انٹرایکٹو API documentation میں استعمال ہوں گے:

<img src="/img/tutorial/response-model/image02.png">

## دیگر Return Type Annotations { #other-return-type-annotations }

ایسے معاملات ہو سکتے ہیں جہاں آپ کوئی ایسی چیز واپس کرتے ہیں جو درست Pydantic field نہیں ہے اور آپ اسے function میں صرف ٹولنگ (editor، mypy، وغیرہ) سے سہولت حاصل کرنے کے لیے annotate کرتے ہیں۔

### براہ راست Response واپس کریں { #return-a-response-directly }

سب سے عام معاملہ [براہ راست Response واپس کرنا ہوگا جیسا کہ بعد میں ایڈوانسڈ docs میں بیان ہوا ہے](../advanced/response-directly.md)۔

{* ../../docs_src/response_model/tutorial003_02_py310.py hl[8,10:11] *}

یہ سادہ معاملہ FastAPI خودکار طور پر handle کرتا ہے کیونکہ return type annotation وہ class (یا `Response` کی subclass) ہے۔

اور ٹولز بھی خوش ہوں گے کیونکہ `RedirectResponse` اور `JSONResponse` دونوں `Response` کی subclasses ہیں، تو type annotation درست ہے۔

### Response Subclass Annotate کریں { #annotate-a-response-subclass }

آپ type annotation میں `Response` کی subclass بھی استعمال کر سکتے ہیں:

{* ../../docs_src/response_model/tutorial003_03_py310.py hl[8:9] *}

یہ بھی کام کرے گا کیونکہ `RedirectResponse` `Response` کی subclass ہے، اور FastAPI خودکار طور پر اس سادہ معاملے کو handle کرے گا۔

### غلط Return Type Annotations { #invalid-return-type-annotations }

لیکن جب آپ کوئی اور اختیاری object واپس کرتے ہیں جو درست Pydantic type نہیں ہے (مثلاً database object) اور آپ اسے function میں اسی طرح annotate کرتے ہیں، تو FastAPI اس type annotation سے Pydantic response model بنانے کی کوشش کرے گا، اور ناکام ہو جائے گا۔

یہی ہوگا اگر آپ کے پاس مختلف types کے درمیان <dfn title='A union between multiple types means "any of these types".'>union</dfn> ہو جہاں ایک یا زیادہ درست Pydantic types نہ ہوں، مثلاً یہ ناکام ہو جائے گا 💥:

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

...یہ اس لیے ناکام ہوتا ہے کیونکہ type annotation ایک Pydantic type نہیں ہے اور صرف ایک `Response` class یا subclass بھی نہیں ہے، یہ `Response` اور `dict` کے درمیان union (دونوں میں سے کوئی ایک) ہے۔

### Response Model غیر فعال کریں { #disable-response-model }

اوپر کی مثال سے آگے بڑھتے ہوئے، شاید آپ وہ ڈیفالٹ ڈیٹا validation، documentation، filtering وغیرہ نہ چاہیں جو FastAPI کرتا ہے۔

لیکن آپ شاید function میں return type annotation رکھنا چاہیں تاکہ editors اور type checkers (مثلاً mypy) جیسے ٹولز سے سہولت ملتی رہے۔

اس صورت میں، آپ `response_model=None` سیٹ کر کے response model generation غیر فعال کر سکتے ہیں:

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

اس سے FastAPI response model generation چھوڑ دے گا اور اس طرح آپ جو بھی return type annotations چاہیں رکھ سکتے ہیں بغیر اس کے کہ آپ کی FastAPI application متاثر ہو۔ 🤓

## Response Model encoding parameters { #response-model-encoding-parameters }

آپ کے response model میں default values ہو سکتی ہیں، جیسے:

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None` (یا Python 3.10 میں `str | None = None`) کی default `None` ہے۔
* `tax: float = 10.5` کی default `10.5` ہے۔
* `tags: List[str] = []` کی default خالی list ہے: `[]`۔

لیکن آپ انہیں نتیجے سے خارج کرنا چاہ سکتے ہیں اگر وہ دراصل ذخیرہ نہیں کیے گئے تھے۔

مثال کے طور پر، اگر آپ کے پاس NoSQL database میں بہت سے optional attributes والے models ہیں، لیکن آپ default values سے بھرے بہت لمبے JSON responses نہیں بھیجنا چاہتے۔

### `response_model_exclude_unset` parameter استعمال کریں { #use-the-response-model-exclude-unset-parameter }

آپ *path operation decorator* parameter `response_model_exclude_unset=True` سیٹ کر سکتے ہیں:

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

اور وہ default values response میں شامل نہیں ہوں گی، صرف وہ قدریں شامل ہوں گی جو واقعی سیٹ کی گئی تھیں۔

تو اگر آپ اس *path operation* کو ID `foo` والے item کے لیے request بھیجیں، تو response (default values شامل کیے بغیر) یہ ہوگا:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// info | معلومات

آپ یہ بھی استعمال کر سکتے ہیں:

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

جیسا کہ [Pydantic docs](https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict) میں `exclude_defaults` اور `exclude_none` کے لیے بیان ہے۔

///

#### Default values والے fields کے لیے ڈیٹا { #data-with-values-for-fields-with-defaults }

لیکن اگر آپ کے ڈیٹا میں model کے default values والے fields کے لیے قدریں ہیں، جیسے ID `bar` والا item:

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

تو وہ response میں شامل ہوں گی۔

#### Defaults جیسی ہی قدروں والا ڈیٹا { #data-with-the-same-values-as-the-defaults }

اگر ڈیٹا میں default values جیسی ہی قدریں ہیں، جیسے ID `baz` والا item:

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPI اتنا ذہین ہے (دراصل Pydantic اتنا ذہین ہے) کہ سمجھ لے کہ، اگرچہ `description`، `tax`، اور `tags` کی قدریں defaults جیسی ہیں، وہ واضح طور پر سیٹ کی گئی تھیں (defaults سے نہیں لی گئیں)۔

تو، وہ JSON response میں شامل ہوں گی۔

/// tip | مشورہ

نوٹ کریں کہ default values کچھ بھی ہو سکتی ہیں، صرف `None` نہیں۔

وہ ایک list (`[]`)، `10.5` کی `float`، وغیرہ ہو سکتی ہیں۔

///

### `response_model_include` اور `response_model_exclude` { #response-model-include-and-response-model-exclude }

آپ *path operation decorator* parameters `response_model_include` اور `response_model_exclude` بھی استعمال کر سکتے ہیں۔

یہ `str` کا ایک `set` لیتے ہیں جن میں شامل کرنے (باقی چھوڑنے) یا خارج کرنے (باقی شامل کرنے) والے attributes کے نام ہوتے ہیں۔

اگر آپ کے پاس صرف ایک Pydantic model ہے اور آپ آؤٹ پٹ سے کچھ ڈیٹا ہٹانا چاہتے ہیں تو اسے فوری شارٹ کٹ کے طور پر استعمال کیا جا سکتا ہے۔

/// tip | مشورہ

لیکن پھر بھی مشورہ یہ ہے کہ ان parameters کی بجائے اوپر بیان کیے گئے خیالات استعمال کریں، یعنی متعدد classes۔

اس کی وجہ یہ ہے کہ آپ کی ایپ کے OpenAPI میں تیار ہونے والا JSON Schema (اور docs) پھر بھی مکمل model کا ہوگا، چاہے آپ `response_model_include` یا `response_model_exclude` استعمال کر کے کچھ attributes ہٹا دیں۔

یہ `response_model_by_alias` پر بھی لاگو ہوتا ہے جو اسی طرح کام کرتا ہے۔

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | مشورہ

`{"name", "description"}` کی ترکیب ان دو قدروں کے ساتھ ایک `set` بناتی ہے۔

یہ `set(["name", "description"])` کے برابر ہے۔

///

#### `set`s کی بجائے `list`s کا استعمال { #using-lists-instead-of-sets }

اگر آپ `set` استعمال کرنا بھول جائیں اور `list` یا `tuple` استعمال کر لیں، تو FastAPI پھر بھی اسے `set` میں تبدیل کرے گا اور درست طریقے سے کام کرے گا:

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## خلاصہ { #recap }

*path operation decorator* کا parameter `response_model` استعمال کریں تاکہ response models define کریں اور خاص طور پر نجی ڈیٹا فلٹر ہونا یقینی بنائیں۔

صرف واضح طور پر سیٹ کی گئی قدریں واپس کرنے کے لیے `response_model_exclude_unset` استعمال کریں۔
