# Path Parameters { #path-parameters }

آپ Python format strings کی طرح syntax استعمال کر کے path "parameters" یا "variables" کا اعلان کر سکتے ہیں:

{* ../../docs_src/path_params/tutorial001_py310.py hl[6:7] *}

Path parameter `item_id` کی قدر آپ کے function میں argument `item_id` کے طور پر دی جائے گی۔

تو، اگر آپ یہ مثال چلائیں اور [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo) پر جائیں، آپ کو یہ response نظر آئے گا:

```JSON
{"item_id":"foo"}
```

## اقسام کے ساتھ Path parameters { #path-parameters-with-types }

آپ معیاری Python type annotations استعمال کر کے function میں path parameter کی قسم کا اعلان کر سکتے ہیں:

{* ../../docs_src/path_params/tutorial002_py310.py hl[7] *}

اس صورت میں، `item_id` کو `int` ہونے کا اعلان کیا گیا ہے۔

/// check

یہ آپ کو function کے اندر ایڈیٹر سپورٹ دے گا، error checks، completion وغیرہ کے ساتھ۔

///

## ڈیٹا <dfn title="also known as: serialization, parsing, marshalling">تبدیلی</dfn> { #data-conversion }

اگر آپ یہ مثال چلائیں اور اپنا براؤزر [http://127.0.0.1:8000/items/3](http://127.0.0.1:8000/items/3) پر کھولیں، آپ کو یہ response نظر آئے گا:

```JSON
{"item_id":3}
```

/// check

غور کریں کہ آپ کے function نے جو قدر وصول کی (اور واپس کی) وہ `3` ہے، بطور Python `int`، نہ کہ string `"3"`۔

تو، اس type declaration کے ساتھ، **FastAPI** آپ کو خودکار request <dfn title="converting the string that comes from an HTTP request into Python data">"parsing"</dfn> دیتا ہے۔

///

## ڈیٹا کی توثیق { #data-validation }

لیکن اگر آپ براؤزر میں [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo) پر جائیں، تو آپ کو ایک اچھی HTTP error نظر آئے گی:

```JSON
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo"
    }
  ]
}
```

کیونکہ path parameter `item_id` کی قدر `"foo"` تھی، جو `int` نہیں ہے۔

وہی error ظاہر ہوگی اگر آپ `int` کی بجائے `float` فراہم کریں، جیسے: [http://127.0.0.1:8000/items/4.2](http://127.0.0.1:8000/items/4.2)

/// check

تو، اسی Python type declaration کے ساتھ، **FastAPI** آپ کو ڈیٹا کی توثیق فراہم کرتا ہے۔

غور کریں کہ error واضح طور پر بتاتی ہے کہ توثیق بالکل کس مقام پر ناکام ہوئی۔

یہ آپ کی API کے ساتھ تعامل کرنے والے کوڈ کو تیار کرتے اور debug کرتے وقت ناقابل یقین حد تک مددگار ہے۔

///

## دستاویزات { #documentation }

اور جب آپ اپنا براؤزر [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) پر کھولیں، آپ کو ایک خودکار، انٹرایکٹو API دستاویز نظر آئے گی جیسے:

<img src="/img/tutorial/path-params/image01.png">

/// check

ایک بار پھر، صرف اسی Python type declaration کے ساتھ، **FastAPI** آپ کو خودکار، انٹرایکٹو دستاویزات فراہم کرتا ہے (Swagger UI کو مربوط کرتے ہوئے)۔

غور کریں کہ path parameter کو integer ہونے کا اعلان کیا گیا ہے۔

///

## معیارات پر مبنی فوائد، متبادل دستاویزات { #standards-based-benefits-alternative-documentation }

اور چونکہ تیار کردہ schema [OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md) معیار سے ہے، بہت سے مطابق ٹولز موجود ہیں۔

اسی وجہ سے، **FastAPI** خود ایک متبادل API دستاویز فراہم کرتا ہے (ReDoc استعمال کرتے ہوئے)، جسے آپ [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) پر دیکھ سکتے ہیں:

<img src="/img/tutorial/path-params/image02.png">

اسی طرح، بہت سے مطابق ٹولز ہیں۔ بشمول بہت سی زبانوں کے لیے کوڈ جنریشن ٹولز۔

## Pydantic { #pydantic }

تمام ڈیٹا کی توثیق پردے کے پیچھے [Pydantic](https://docs.pydantic.dev/) کے ذریعے کی جاتی ہے، لہذا آپ کو اس سے تمام فوائد ملتے ہیں۔ اور آپ جانتے ہیں کہ آپ اچھے ہاتھوں میں ہیں۔

آپ `str`، `float`، `bool` اور بہت سی دیگر پیچیدہ data types کے ساتھ وہی type declarations استعمال کر سکتے ہیں۔

ان میں سے کئی ٹیوٹوریل کے اگلے ابواب میں دریافت کیے گئے ہیں۔

## ترتیب اہم ہے { #order-matters }

*Path operations* بناتے وقت، آپ کو ایسے حالات مل سکتے ہیں جہاں آپ کا ایک مقررہ path ہے۔

جیسے `/users/me`، فرض کریں کہ یہ موجودہ صارف کا ڈیٹا حاصل کرنے کے لیے ہے۔

اور پھر آپ کے پاس `/users/{user_id}` path بھی ہو سکتا ہے جو کسی مخصوص صارف کا ڈیٹا کسی user ID سے حاصل کرے۔

چونکہ *path operations* ترتیب سے جانچے جاتے ہیں، آپ کو یقینی بنانا ہوگا کہ `/users/me` کا path `/users/{user_id}` سے پہلے اعلان کیا گیا ہے:

{* ../../docs_src/path_params/tutorial003_py310.py hl[6,11] *}

ورنہ، `/users/{user_id}` کا path `/users/me` کے لیے بھی مماثل ہوگا، یہ "سوچتے" ہوئے کہ اسے `"me"` قدر کے ساتھ parameter `user_id` مل رہا ہے۔

اسی طرح، آپ path operation کو دوبارہ بیان نہیں کر سکتے:

{* ../../docs_src/path_params/tutorial003b_py310.py hl[6,11] *}

پہلا ہمیشہ استعمال ہوگا کیونکہ path پہلے مماثل ہوتا ہے۔

## پہلے سے طے شدہ اقدار { #predefined-values }

اگر آپ کے پاس ایک *path operation* ہے جو *path parameter* وصول کرتا ہے، لیکن آپ چاہتے ہیں کہ ممکنہ درست *path parameter* اقدار پہلے سے طے شدہ ہوں، تو آپ معیاری Python <abbr title="Enumeration">`Enum`</abbr> استعمال کر سکتے ہیں۔

### ایک `Enum` class بنائیں { #create-an-enum-class }

`Enum` import کریں اور ایک ذیلی class بنائیں جو `str` اور `Enum` سے وراثت حاصل کرے۔

`str` سے وراثت حاصل کرنے سے API docs جان سکیں گے کہ اقدار `string` قسم کی ہونی چاہییں اور صحیح طریقے سے ظاہر ہو سکیں گی۔

پھر مقررہ اقدار کے ساتھ class attributes بنائیں، جو دستیاب درست اقدار ہوں گی:

{* ../../docs_src/path_params/tutorial005_py310.py hl[1,6:9] *}

/// tip | مشورہ

اگر آپ سوچ رہے ہیں، "AlexNet"، "ResNet"، اور "LeNet" بس Machine Learning <dfn title="Technically, Deep Learning model architectures">models</dfn> کے نام ہیں۔

///

### ایک *path parameter* کا اعلان کریں { #declare-a-path-parameter }

پھر آپ نے بنائی ہوئی enum class (`ModelName`) کو type annotation کے طور پر استعمال کرتے ہوئے ایک *path parameter* بنائیں:

{* ../../docs_src/path_params/tutorial005_py310.py hl[16] *}

### دستاویزات چیک کریں { #check-the-docs }

چونکہ *path parameter* کے لیے دستیاب اقدار پہلے سے طے شدہ ہیں، انٹرایکٹو docs انہیں اچھے طریقے سے دکھا سکتے ہیں:

<img src="/img/tutorial/path-params/image03.png">

### Python *enumerations* کے ساتھ کام کرنا { #working-with-python-enumerations }

*Path parameter* کی قدر ایک *enumeration member* ہوگی۔

#### *Enumeration members* کا موازنہ کریں { #compare-enumeration-members }

آپ اس کا موازنہ اپنی بنائی ہوئی enum `ModelName` میں *enumeration member* سے کر سکتے ہیں:

{* ../../docs_src/path_params/tutorial005_py310.py hl[17] *}

#### *Enumeration value* حاصل کریں { #get-the-enumeration-value }

آپ `model_name.value` استعمال کر کے اصل قدر (اس صورت میں `str`) حاصل کر سکتے ہیں، یا عمومی طور پر، `your_enum_member.value`:

{* ../../docs_src/path_params/tutorial005_py310.py hl[20] *}

/// tip | مشورہ

آپ `"lenet"` قدر تک `ModelName.lenet.value` سے بھی رسائی حاصل کر سکتے ہیں۔

///

#### *Enumeration members* واپس کریں { #return-enumeration-members }

آپ اپنے *path operation* سے *enum members* واپس کر سکتے ہیں، یہاں تک کہ JSON body میں nested (مثلاً ایک `dict`)۔

انہیں client کو واپس کرنے سے پہلے ان کی متعلقہ اقدار (اس صورت میں strings) میں تبدیل کیا جائے گا:

{* ../../docs_src/path_params/tutorial005_py310.py hl[18,21,23] *}

آپ کے client کو JSON response کچھ ایسا ملے گا:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Path parameters جن میں paths ہوں { #path-parameters-containing-paths }

فرض کریں آپ کے پاس ایک *path operation* ہے جس کا path `/files/{file_path}` ہے۔

لیکن آپ چاہتے ہیں کہ `file_path` میں خود ایک *path* ہو، جیسے `home/johndoe/myfile.txt`۔

تو، اس فائل کا URL کچھ ایسا ہوگا: `/files/home/johndoe/myfile.txt`۔

### OpenAPI سپورٹ { #openapi-support }

OpenAPI میں *path parameter* کے اندر *path* رکھنے کا اعلان کرنے کا کوئی طریقہ نہیں ہے، کیونکہ اس سے ایسے منظرنامے پیدا ہو سکتے ہیں جنہیں ٹیسٹ اور بیان کرنا مشکل ہو۔

بہرحال، آپ اسے **FastAPI** میں پھر بھی کر سکتے ہیں، Starlette کے اندرونی ٹولز میں سے ایک استعمال کر کے۔

اور docs پھر بھی کام کریں گے، اگرچہ کوئی دستاویز شامل نہیں ہوگی جو بتائے کہ parameter میں path ہونا چاہیے۔

### Path convertor { #path-convertor }

Starlette سے براہ راست ایک آپشن استعمال کرتے ہوئے آپ *path parameter* کا اعلان کر سکتے ہیں جس میں *path* ہو، اس طرح کے URL کے ساتھ:

```
/files/{file_path:path}
```

اس صورت میں، parameter کا نام `file_path` ہے، اور آخری حصہ، `:path`، بتاتا ہے کہ parameter کو کسی بھی *path* سے مماثل ہونا چاہیے۔

تو، آپ اسے اس طرح استعمال کر سکتے ہیں:

{* ../../docs_src/path_params/tutorial004_py310.py hl[6] *}

/// tip | مشورہ

آپ کو parameter میں `/home/johndoe/myfile.txt` رکھنے کی ضرورت ہو سکتی ہے، ابتدائی سلیش (`/`) کے ساتھ۔

اس صورت میں، URL ہوگا: `/files//home/johndoe/myfile.txt`، `files` اور `home` کے درمیان ڈبل سلیش (`//`) کے ساتھ۔

///

## خلاصہ { #recap }

**FastAPI** کے ساتھ، مختصر، بدیہی اور معیاری Python type declarations استعمال کر کے، آپ کو ملتا ہے:

* ایڈیٹر سپورٹ: error checks، autocompletion وغیرہ۔
* ڈیٹا "<dfn title="converting the string that comes from an HTTP request into Python data">parsing</dfn>"
* ڈیٹا کی توثیق
* API تشریح اور خودکار دستاویزات

اور آپ کو انہیں صرف ایک بار اعلان کرنا ہوتا ہے۔

یہ شاید متبادل frameworks کے مقابلے میں **FastAPI** کا سب سے نمایاں فائدہ ہے (خام کارکردگی کے علاوہ)۔
