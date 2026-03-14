# Body - Nested Models { #body-nested-models }

**FastAPI** کے ساتھ، آپ من مانی گہرائی سے nested models بنا سکتے، توثیق کر سکتے، دستاویز بنا سکتے اور استعمال کر سکتے ہیں (Pydantic کی بدولت)۔

## List fields { #list-fields }

آپ کسی attribute کو ذیلی قسم کے طور پر بنا سکتے ہیں۔ مثال کے طور پر، Python `list`:

{* ../../docs_src/body_nested_models/tutorial001_py310.py hl[12] *}

یہ `tags` کو list بنائے گا، اگرچہ یہ list کے عناصر کی قسم اعلان نہیں کرتا۔

## Type parameter کے ساتھ List fields { #list-fields-with-type-parameter }

لیکن Python میں اندرونی اقسام، یا "type parameters" کے ساتھ lists اعلان کرنے کا ایک مخصوص طریقہ ہے:

### Type parameter کے ساتھ `list` اعلان کریں { #declare-a-list-with-a-type-parameter }

ایسی اقسام اعلان کرنے کے لیے جن میں type parameters (اندرونی اقسام) ہوں، جیسے `list`، `dict`، `tuple`،
اندرونی قسم(قسمیں) "type parameters" کے طور پر مربع بریکٹ استعمال کر کے دیں: `[` اور `]`

```Python
my_list: list[str]
```

یہ سب معیاری Python syntax ہے type declarations کے لیے۔

اندرونی اقسام کے ساتھ model attributes کے لیے وہی معیاری syntax استعمال کریں۔

تو، ہماری مثال میں، ہم `tags` کو خاص طور پر "strings کی list" بنا سکتے ہیں:

{* ../../docs_src/body_nested_models/tutorial002_py310.py hl[12] *}

## Set types { #set-types }

لیکن پھر ہم سوچتے ہیں اور محسوس کرتے ہیں کہ tags دہرائے نہیں جانے چاہییں، وہ شاید منفرد strings ہوں گے۔

اور Python میں منفرد آئٹمز کے sets کے لیے ایک خاص data type ہے، `set`۔

پھر ہم `tags` کو strings کے set کے طور پر اعلان کر سکتے ہیں:

{* ../../docs_src/body_nested_models/tutorial003_py310.py hl[12] *}

اس کے ساتھ، چاہے آپ کو نقل شدہ ڈیٹا کے ساتھ request ملے، اسے منفرد آئٹمز کے set میں تبدیل کر دیا جائے گا۔

اور جب بھی آپ وہ ڈیٹا نکالیں گے، چاہے ماخذ میں نقل ہو، اسے منفرد آئٹمز کے set کے طور پر نکالا جائے گا۔

اور اس کے مطابق تشریح / دستاویز بھی بنائی جائے گی۔

## Nested Models { #nested-models }

Pydantic model کی ہر attribute کی ایک قسم ہوتی ہے۔

لیکن وہ قسم خود بھی ایک اور Pydantic model ہو سکتی ہے۔

تو، آپ مخصوص attribute ناموں، اقسام اور validations کے ساتھ گہرے nested JSON "objects" اعلان کر سکتے ہیں۔

یہ سب، من مانی گہرائی سے nested۔

### ذیلی model بنائیں { #define-a-submodel }

مثال کے طور پر، ہم ایک `Image` model بنا سکتے ہیں:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[7:9] *}

### ذیلی model کو بطور قسم استعمال کریں { #use-the-submodel-as-a-type }

اور پھر ہم اسے کسی attribute کی قسم کے طور پر استعمال کر سکتے ہیں:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[18] *}

اس کا مطلب ہوگا کہ **FastAPI** اس طرح کی body کی توقع کرے گا:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

ایک بار پھر، صرف وہ اعلان کر کے، **FastAPI** کے ساتھ آپ کو ملتا ہے:

* Nested models کے لیے بھی ایڈیٹر سپورٹ (completion وغیرہ)
* ڈیٹا کی تبدیلی
* ڈیٹا کی توثیق
* خودکار دستاویزات

## خاص اقسام اور توثیق { #special-types-and-validation }

عام واحد اقسام جیسے `str`، `int`، `float` وغیرہ کے علاوہ آپ مزید پیچیدہ واحد اقسام استعمال کر سکتے ہیں جو `str` سے وراثت حاصل کرتی ہیں۔

تمام دستیاب آپشنز دیکھنے کے لیے، [Pydantic کا Type Overview](https://docs.pydantic.dev/latest/concepts/types/) دیکھیں۔ آپ اگلے باب میں کچھ مثالیں دیکھیں گے۔

مثال کے طور پر، جیسے `Image` model میں ہمارے پاس `url` فیلڈ ہے، ہم `str` کی بجائے Pydantic کے `HttpUrl` کا اعلان کر سکتے ہیں:

{* ../../docs_src/body_nested_models/tutorial005_py310.py hl[2,8] *}

String کو درست URL ہونے کے لیے جانچا جائے گا، اور JSON Schema / OpenAPI میں اسی طرح دستاویز بنائی جائے گی۔

## ذیلی models کی lists والی Attributes { #attributes-with-lists-of-submodels }

آپ Pydantic models کو `list`، `set` وغیرہ کی ذیلی اقسام کے طور پر بھی استعمال کر سکتے ہیں:

{* ../../docs_src/body_nested_models/tutorial006_py310.py hl[18] *}

یہ اس طرح کی JSON body کی توقع کرے گا (تبدیل، توثیق، دستاویز وغیرہ):

```JSON hl_lines="11"
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
```

/// info | معلومات

غور کریں کہ `images` key میں اب image objects کی list ہے۔

///

## گہرے nested models { #deeply-nested-models }

آپ من مانی گہرائی سے nested models بنا سکتے ہیں:

{* ../../docs_src/body_nested_models/tutorial007_py310.py hl[7,12,18,21,25] *}

/// info | معلومات

غور کریں کہ `Offer` میں `Item`s کی list ہے، جن میں بدلے میں اختیاری `Image`s کی list ہے۔

///

## خالص lists کی Bodies { #bodies-of-pure-lists }

اگر آپ جس JSON body کی توقع کر رہے ہیں اس کی اعلیٰ ترین قدر JSON `array` (Python `list`) ہے، تو آپ function کے parameter میں قسم کا اعلان کر سکتے ہیں، بالکل Pydantic models کی طرح:

```Python
images: list[Image]
```

جیسے:

{* ../../docs_src/body_nested_models/tutorial008_py310.py hl[13] *}

## ہر جگہ ایڈیٹر سپورٹ { #editor-support-everywhere }

اور آپ کو ہر جگہ ایڈیٹر سپورٹ ملتی ہے۔

یہاں تک کہ lists کے اندر آئٹمز کے لیے بھی:

<img src="/img/tutorial/body-nested-models/image01.png">

اگر آپ Pydantic models کی بجائے براہ راست `dict` کے ساتھ کام کر رہے ہوتے تو آپ کو اس طرح کی ایڈیٹر سپورٹ نہیں ملتی۔

لیکن آپ کو ان کی فکر کرنے کی ضرورت نہیں، آنے والے dicts خودکار طور پر تبدیل ہو جاتے ہیں اور آپ کا آؤٹ پٹ بھی خودکار طور پر JSON میں تبدیل ہو جاتا ہے۔

## من مانی `dict`s کی Bodies { #bodies-of-arbitrary-dicts }

آپ body کو ایسے `dict` کے طور پر بھی اعلان کر سکتے ہیں جس کی keys کسی قسم کی ہوں اور values کسی اور قسم کی۔

اس طرح، آپ کو پہلے سے معلوم ہونے کی ضرورت نہیں کہ درست فیلڈ/attribute نام کیا ہیں (جیسا کہ Pydantic models کی صورت میں ہوتا)۔

یہ مفید ہوگا اگر آپ ایسی keys وصول کرنا چاہتے ہیں جو آپ پہلے سے نہیں جانتے۔

---

ایک اور مفید صورت یہ ہے جب آپ کسی اور قسم (مثلاً `int`) کی keys رکھنا چاہیں۔

یہی ہم یہاں دیکھنے والے ہیں۔

اس صورت میں، آپ کوئی بھی `dict` قبول کریں گے بشرطیکہ اس میں `int` keys ہوں اور `float` values ہوں:

{* ../../docs_src/body_nested_models/tutorial009_py310.py hl[7] *}

/// tip | مشورہ

یاد رکھیں کہ JSON صرف `str` کو keys کے طور پر تعاون کرتا ہے۔

لیکن Pydantic میں خودکار ڈیٹا تبدیلی ہے۔

اس کا مطلب ہے کہ، اگرچہ آپ کے API clients صرف strings بطور keys بھیج سکتے ہیں، جب تک وہ strings خالص integers رکھتی ہیں، Pydantic انہیں تبدیل اور توثیق کرے گا۔

اور جو `dict` آپ `weights` کے طور پر وصول کریں گے اس میں دراصل `int` keys اور `float` values ہوں گی۔

///

## خلاصہ { #recap }

**FastAPI** کے ساتھ آپ کو Pydantic models کی فراہم کردہ زیادہ سے زیادہ لچک ملتی ہے، جبکہ آپ کا کوڈ سادہ، مختصر اور خوبصورت رہتا ہے۔

تمام فوائد کے ساتھ:

* ایڈیٹر سپورٹ (ہر جگہ completion!)
* ڈیٹا کی تبدیلی (جسے parsing / serialization بھی کہتے ہیں)
* ڈیٹا کی توثیق
* Schema دستاویزات
* خودکار docs
