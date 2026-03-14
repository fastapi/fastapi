# Query Parameters اور String Validations { #query-parameters-and-string-validations }

**FastAPI** آپ کو اپنے parameters کے لیے اضافی معلومات اور توثیق کا اعلان کرنے کی اجازت دیتا ہے۔

آئیے اس ایپلیکیشن کو بطور مثال لیتے ہیں:

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

Query parameter `q` کی قسم `str | None` ہے، جس کا مطلب ہے کہ یہ `str` قسم کا ہے لیکن `None` بھی ہو سکتا ہے، اور درحقیقت، طے شدہ قدر `None` ہے، تو FastAPI جان لے گا کہ یہ لازمی نہیں ہے۔

/// note | نوٹ

FastAPI جان لے گا کہ `q` کی قدر لازمی نہیں ہے کیونکہ طے شدہ قدر `= None` ہے۔

`str | None` رکھنے سے آپ کے ایڈیٹر کو بہتر سپورٹ فراہم ہوگی اور errors کا پتہ لگانے میں مدد ملے گی۔

///

## اضافی توثیق { #additional-validation }

ہم یہ نافذ کرنے والے ہیں کہ اگرچہ `q` اختیاری ہے، جب بھی یہ فراہم کیا جائے، **اس کی لمبائی 50 حروف سے زیادہ نہ ہو**۔

### `Query` اور `Annotated` import کریں { #import-query-and-annotated }

اس کے لیے، پہلے import کریں:

* `fastapi` سے `Query`
* `typing` سے `Annotated`

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[1,3] *}

/// info | معلومات

FastAPI نے ورژن 0.95.0 میں `Annotated` کی تعاون شامل کی (اور اسے تجویز کرنا شروع کیا)۔

اگر آپ کے پاس پرانا ورژن ہے، تو `Annotated` استعمال کرنے کی کوشش کرنے پر errors آئیں گی۔

`Annotated` استعمال کرنے سے پہلے یقینی بنائیں کہ آپ [FastAPI ورژن اپ گریڈ کریں](../deployment/versions.md#upgrading-the-fastapi-versions) کم از کم 0.95.1 تک۔

///

## `q` parameter کی type میں `Annotated` استعمال کریں { #use-annotated-in-the-type-for-the-q-parameter }

یاد کریں میں نے آپ کو پہلے بتایا تھا کہ `Annotated` کو [Python Types تعارف](../python-types.md#type-hints-with-metadata-annotations) میں آپ کے parameters میں metadata شامل کرنے کے لیے استعمال کیا جا سکتا ہے؟

اب اسے FastAPI کے ساتھ استعمال کرنے کا وقت ہے۔

ہمارے پاس یہ type annotation تھی:

```Python
q: str | None = None
```

ہم اسے `Annotated` میں لپیٹیں گے، تو یہ بن جائے گا:

```Python
q: Annotated[str | None] = None
```

دونوں ورژنز کا مطلب ایک ہی ہے، `q` ایک parameter ہے جو `str` یا `None` ہو سکتا ہے، اور پہلے سے، یہ `None` ہے۔

اب آئیے دلچسپ حصے کی طرف چلتے ہیں۔

## `q` parameter میں `Annotated` میں `Query` شامل کریں { #add-query-to-annotated-in-the-q-parameter }

اب جب ہمارے پاس `Annotated` ہے جہاں ہم مزید معلومات رکھ سکتے ہیں (اس صورت میں کچھ اضافی توثیق)، `Annotated` کے اندر `Query` شامل کریں، اور parameter `max_length` کو `50` سیٹ کریں:

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

غور کریں کہ طے شدہ قدر اب بھی `None` ہے، تو parameter اب بھی اختیاری ہے۔

لیکن اب، `Annotated` کے اندر `Query(max_length=50)` رکھ کر، ہم FastAPI کو بتا رہے ہیں کہ ہم چاہتے ہیں کہ اس قدر کی **اضافی توثیق** ہو، ہم چاہتے ہیں کہ اس میں زیادہ سے زیادہ 50 حروف ہوں۔

/// tip | مشورہ

یہاں ہم `Query()` استعمال کر رہے ہیں کیونکہ یہ ایک **query parameter** ہے۔ بعد میں ہم دوسرے دیکھیں گے جیسے `Path()`، `Body()`، `Header()`، اور `Cookie()`، جو `Query()` جیسے ہی arguments قبول کرتے ہیں۔

///

FastAPI اب یہ کرے گا:

* ڈیٹا کی **توثیق** کرے گا اور یقینی بنائے گا کہ زیادہ سے زیادہ لمبائی 50 حروف ہے
* جب ڈیٹا درست نہ ہو تو client کو **واضح error** دکھائے گا
* OpenAPI schema *path operation* میں parameter کی **دستاویز** بنائے گا (تو یہ **خودکار docs UI** میں ظاہر ہوگا)

## متبادل (پرانا): `Query` بطور طے شدہ قدر { #alternative-old-query-as-the-default-value }

FastAPI کے پرانے ورژنز (ورژن <dfn title="before 2023-03">0.95.0</dfn> سے پہلے) آپ سے `Query` کو `Annotated` میں رکھنے کی بجائے اپنے parameter کی طے شدہ قدر کے طور پر استعمال کرنے کا تقاضا کرتے تھے، اس بات کا بہت زیادہ امکان ہے کہ آپ کو اسے استعمال کرتا ہوا کوڈ نظر آئے، تو میں آپ کو اس کی وضاحت کرتا ہوں۔

/// tip | مشورہ

نئے کوڈ اور جب بھی ممکن ہو، اوپر بتائے گئے `Annotated` استعمال کریں۔ اس کے متعدد فوائد ہیں (نیچے بتائے گئے ہیں) اور کوئی نقصان نہیں۔

///

اس طرح آپ `Query()` کو اپنے function parameter کی طے شدہ قدر کے طور پر استعمال کریں گے، parameter `max_length` کو `50` سیٹ کرتے ہوئے:

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

چونکہ اس صورت میں (`Annotated` استعمال کیے بغیر) ہمیں function میں طے شدہ قدر `None` کو `Query()` سے بدلنا ہے، ہمیں اب `Query(default=None)` parameter سے طے شدہ قدر سیٹ کرنی ہوگی، یہ وہی مقصد پورا کرتا ہے جو اس طے شدہ قدر کی تعریف کا ہے (کم از کم FastAPI کے لیے)۔

تو:

```Python
q: str | None = Query(default=None)
```

...parameter کو اختیاری بناتا ہے، `None` کی طے شدہ قدر کے ساتھ، جیسا کہ:

```Python
q: str | None = None
```

لیکن `Query` ورژن واضح طور پر اسے query parameter ہونے کا اعلان کرتا ہے۔

پھر، ہم `Query` کو مزید parameters دے سکتے ہیں۔ اس صورت میں، `max_length` parameter جو strings پر لاگو ہوتا ہے:

```Python
q: str | None = Query(default=None, max_length=50)
```

یہ ڈیٹا کی توثیق کرے گا، جب ڈیٹا درست نہ ہو تو واضح error دکھائے گا، اور OpenAPI schema *path operation* میں parameter کی دستاویز بنائے گا۔

### `Query` بطور طے شدہ قدر یا `Annotated` میں { #query-as-the-default-value-or-in-annotated }

یاد رکھیں کہ `Annotated` کے اندر `Query` استعمال کرتے وقت آپ `Query` کے `default` parameter کو استعمال نہیں کر سکتے۔

اس کی بجائے، function parameter کی اصل طے شدہ قدر استعمال کریں۔ ورنہ، یہ متضاد ہوگا۔

مثال کے طور پر، یہ اجازت نہیں ہے:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

...کیونکہ یہ واضح نہیں ہے کہ طے شدہ قدر `"rick"` ہونی چاہیے یا `"morty"`۔

تو، آپ استعمال کریں گے (ترجیحاً):

```Python
q: Annotated[str, Query()] = "rick"
```

...یا پرانے کوڈ میں آپ کو یہ ملے گا:

```Python
q: str = Query(default="rick")
```

### `Annotated` کے فوائد { #advantages-of-annotated }

**`Annotated` استعمال کرنا تجویز کیا جاتا ہے** function parameters میں طے شدہ قدر کی بجائے، یہ کئی وجوہات کی بنا پر **بہتر** ہے۔

**Function parameter** کی **طے شدہ** قدر **اصل طے شدہ** قدر ہے، جو عمومی طور پر Python کے ساتھ زیادہ بدیہی ہے۔

آپ وہی function **دوسری جگہوں** پر FastAPI کے بغیر **کال** کر سکتے ہیں، اور یہ **متوقع طور پر کام** کرے گا۔ اگر کوئی **لازمی** parameter ہے (بغیر طے شدہ قدر کے)، آپ کا **ایڈیٹر** آپ کو error سے آگاہ کرے گا، **Python** بھی شکایت کرے گا اگر آپ لازمی parameter دیے بغیر اسے چلائیں۔

جب آپ `Annotated` استعمال نہیں کرتے اور اس کی بجائے **(پرانی) طے شدہ قدر طرز** استعمال کرتے ہیں، اگر آپ اس function کو FastAPI کے بغیر **دوسری جگہوں** پر کال کرتے ہیں، تو آپ کو function کے لیے arguments صحیح طریقے سے دینا **یاد رکھنا** ہوگا تاکہ یہ صحیح کام کرے، ورنہ اقدار آپ کی توقع سے مختلف ہوں گی (مثلاً `str` کی بجائے `QueryInfo` یا کچھ ایسا)۔ اور آپ کا ایڈیٹر شکایت نہیں کرے گا، اور Python بھی وہ function چلاتے وقت شکایت نہیں کرے گا، صرف اس وقت جب اندر کے عمل error دیں۔

چونکہ `Annotated` میں ایک سے زیادہ metadata annotations ہو سکتے ہیں، آپ اب وہی function دوسرے ٹولز کے ساتھ بھی استعمال کر سکتے ہیں، جیسے [Typer](https://typer.tiangolo.com/)۔

## مزید validations شامل کریں { #add-more-validations }

آپ ایک `min_length` parameter بھی شامل کر سکتے ہیں:

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## Regular expressions شامل کریں { #add-regular-expressions }

آپ ایک <dfn title="A regular expression, regex or regexp is a sequence of characters that define a search pattern for strings.">regular expression</dfn> `pattern` بنا سکتے ہیں جس سے parameter کو مماثل ہونا چاہیے:

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

یہ مخصوص regular expression pattern جانچتا ہے کہ وصول شدہ parameter کی قدر:

* `^`: مندرجہ ذیل حروف سے شروع ہوتی ہے، پہلے کوئی حروف نہیں ہیں۔
* `fixedquery`: بالکل `fixedquery` قدر رکھتی ہے۔
* `$`: یہاں ختم ہوتی ہے، `fixedquery` کے بعد مزید کوئی حروف نہیں ہیں۔

اگر آپ ان تمام **"regular expression"** تصورات سے پریشان محسوس کر رہے ہیں، تو فکر نہ کریں۔ یہ بہت سے لوگوں کے لیے مشکل موضوع ہے۔ آپ ابھی بھی regular expressions کی ضرورت کے بغیر بہت کچھ کر سکتے ہیں۔

اب آپ جانتے ہیں کہ جب بھی آپ کو ان کی ضرورت ہو آپ انہیں **FastAPI** میں استعمال کر سکتے ہیں۔

## طے شدہ اقدار { #default-values }

آپ یقیناً `None` کے علاوہ طے شدہ اقدار استعمال کر سکتے ہیں۔

فرض کریں کہ آپ `q` query parameter کا `min_length` `3` رکھنا چاہتے ہیں، اور طے شدہ قدر `"fixedquery"` رکھنا چاہتے ہیں:

{* ../../docs_src/query_params_str_validations/tutorial005_an_py310.py hl[9] *}

/// note | نوٹ

کسی بھی قسم کی طے شدہ قدر رکھنا، بشمول `None`، parameter کو اختیاری بناتا ہے (لازمی نہیں)۔

///

## لازمی parameters { #required-parameters }

جب ہمیں مزید validations یا metadata اعلان کرنے کی ضرورت نہ ہو، ہم `q` query parameter کو صرف طے شدہ قدر اعلان نہ کر کے لازمی بنا سکتے ہیں، جیسے:

```Python
q: str
```

اس کی بجائے:

```Python
q: str | None = None
```

لیکن اب ہم اسے `Query` کے ساتھ اعلان کر رہے ہیں، مثال کے طور پر:

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

تو، جب آپ کو `Query` استعمال کرتے ہوئے کسی قدر کو لازمی قرار دینا ہو، آپ بس طے شدہ قدر اعلان نہ کریں:

{* ../../docs_src/query_params_str_validations/tutorial006_an_py310.py hl[9] *}

### لازمی، `None` ہو سکتا ہے { #required-can-be-none }

آپ اعلان کر سکتے ہیں کہ parameter `None` قبول کر سکتا ہے، لیکن یہ پھر بھی لازمی ہے۔ یہ clients کو مجبور کرے گا کہ وہ قدر بھیجیں، چاہے قدر `None` ہی ہو۔

ایسا کرنے کے لیے، آپ `None` کو درست قسم کے طور پر اعلان کر سکتے ہیں لیکن طے شدہ قدر اعلان نہ کریں:

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

## Query parameter list / متعدد اقدار { #query-parameter-list-multiple-values }

جب آپ `Query` کے ساتھ واضح طور پر query parameter بناتے ہیں تو آپ اسے اقدار کی list وصول کرنے کا بھی اعلان کر سکتے ہیں، یا دوسرے الفاظ میں، متعدد اقدار وصول کرنے کا۔

مثال کے طور پر، query parameter `q` کا اعلان کرنے کے لیے جو URL میں متعدد بار ظاہر ہو سکتا ہے، آپ لکھ سکتے ہیں:

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

پھر، اس طرح کے URL کے ساتھ:

```
http://localhost:8000/items/?q=foo&q=bar
```

آپ کو متعدد `q` *query parameters* کی اقدار (`foo` اور `bar`) Python `list` میں آپ کے *path operation function* کے *function parameter* `q` میں ملیں گی۔

تو، اس URL کا response ہوگا:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | مشورہ

`list` قسم کے query parameter کا اعلان کرنے کے لیے، جیسا کہ اوپر کی مثال میں، آپ کو واضح طور پر `Query` استعمال کرنا ہوگا، ورنہ اسے request body سمجھا جائے گا۔

///

انٹرایکٹو API docs اس کے مطابق اپ ڈیٹ ہوں گے، متعدد اقدار کی اجازت دیتے ہوئے:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### Query parameter list / طے شدہ اقدار کے ساتھ متعدد اقدار { #query-parameter-list-multiple-values-with-defaults }

اگر کوئی فراہم نہ کی جائے تو آپ اقدار کی طے شدہ `list` بھی بنا سکتے ہیں:

{* ../../docs_src/query_params_str_validations/tutorial012_an_py310.py hl[9] *}

اگر آپ یہاں جائیں:

```
http://localhost:8000/items/
```

`q` کی طے شدہ قدر ہوگی: `["foo", "bar"]` اور آپ کا response ہوگا:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### صرف `list` استعمال کرنا { #using-just-list }

آپ `list[str]` کی بجائے براہ راست `list` بھی استعمال کر سکتے ہیں:

{* ../../docs_src/query_params_str_validations/tutorial013_an_py310.py hl[9] *}

/// note | نوٹ

یاد رکھیں کہ اس صورت میں، FastAPI list کے مندرجات کی جانچ نہیں کرے گا۔

مثال کے طور پر، `list[int]` جانچے گا (اور دستاویز بنائے گا) کہ list کے مندرجات integers ہیں۔ لیکن اکیلا `list` ایسا نہیں کرے گا۔

///

## مزید metadata اعلان کریں { #declare-more-metadata }

آپ parameter کے بارے میں مزید معلومات شامل کر سکتے ہیں۔

وہ معلومات تیار کردہ OpenAPI میں شامل ہوں گی اور دستاویزاتی صارف انٹرفیسز اور بیرونی ٹولز کے ذریعے استعمال ہوں گی۔

/// note | نوٹ

یاد رکھیں کہ مختلف ٹولز میں OpenAPI تعاون کی مختلف سطحیں ہو سکتی ہیں۔

ان میں سے کچھ شاید ابھی تک تمام اعلان کردہ اضافی معلومات نہ دکھائیں، اگرچہ زیادہ تر صورتوں میں، غائب خصوصیت پہلے سے ترقی کے لیے منصوبہ بند ہے۔

///

آپ `title` شامل کر سکتے ہیں:

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

اور `description`:

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## Alias parameters { #alias-parameters }

تصور کریں کہ آپ چاہتے ہیں کہ parameter `item-query` ہو۔

جیسے:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

لیکن `item-query` ایک درست Python variable نام نہیں ہے۔

سب سے قریب ترین `item_query` ہوگا۔

لیکن آپ کو ابھی بھی اسے بالکل `item-query` ہونا چاہیے...

تو آپ ایک `alias` اعلان کر سکتے ہیں، اور وہ alias parameter کی قدر تلاش کرنے کے لیے استعمال ہوگا:

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## Parameters کو deprecated کرنا { #deprecating-parameters }

فرض کریں آپ کو یہ parameter اب پسند نہیں۔

آپ کو اسے کچھ وقت کے لیے رکھنا ہوگا کیونکہ clients اسے استعمال کر رہے ہیں، لیکن آپ چاہتے ہیں کہ docs واضح طور پر اسے <dfn title="obsolete, recommended not to use it">deprecated</dfn> دکھائیں۔

پھر `Query` کو `deprecated=True` parameter دیں:

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

Docs اسے اس طرح دکھائیں گے:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## OpenAPI سے parameters خارج کریں { #exclude-parameters-from-openapi }

تیار کردہ OpenAPI schema سے query parameter کو خارج کرنے کے لیے (اور اس طرح، خودکار دستاویزاتی نظاموں سے)، `Query` کا `include_in_schema` parameter `False` سیٹ کریں:

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## حسب ضرورت Validation { #custom-validation }

ایسے معاملات ہو سکتے ہیں جہاں آپ کو **حسب ضرورت توثیق** کی ضرورت ہو جو اوپر دکھائے گئے parameters سے نہیں ہو سکتی۔

ان صورتوں میں، آپ ایک **حسب ضرورت validator function** استعمال کر سکتے ہیں جو عام توثیق کے بعد لاگو ہوتا ہے (مثلاً یہ توثیق کرنے کے بعد کہ قدر `str` ہے)۔

آپ `Annotated` کے اندر [Pydantic کا `AfterValidator`](https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator) استعمال کر کے یہ حاصل کر سکتے ہیں۔

/// tip | مشورہ

Pydantic میں [`BeforeValidator`](https://docs.pydantic.dev/latest/concepts/validators/#field-before-validator) اور دوسرے بھی ہیں۔

///

مثال کے طور پر، یہ حسب ضرورت validator جانچتا ہے کہ item ID <abbr title="International Standard Book Number">ISBN</abbr> کتاب نمبر کے لیے `isbn-` سے یا <abbr title="Internet Movie Database: a website with information about movies">IMDB</abbr> فلم URL ID کے لیے `imdb-` سے شروع ہوتا ہے:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py hl[5,16:19,24] *}

/// info | معلومات

یہ Pydantic ورژن 2 یا اس سے اوپر کے ساتھ دستیاب ہے۔

///

/// tip | مشورہ

اگر آپ کو کسی ایسی توثیق کی ضرورت ہے جس کے لیے کسی **بیرونی جزو** سے بات چیت کرنی ہو، جیسے ڈیٹابیس یا کوئی اور API، تو آپ کو اس کی بجائے **FastAPI Dependencies** استعمال کرنی چاہییں، آپ ان کے بارے میں بعد میں سیکھیں گے۔

یہ حسب ضرورت validators ان چیزوں کے لیے ہیں جو **صرف** request میں فراہم کردہ **اسی ڈیٹا** سے جانچی جا سکتی ہیں۔

///

### اس کوڈ کو سمجھیں { #understand-that-code }

اہم نکتہ بس **`Annotated` کے اندر function کے ساتھ `AfterValidator`** استعمال کرنا ہے۔ اس حصے کو چھوڑنے میں کوئی حرج نہیں۔

---

لیکن اگر آپ اس مخصوص کوڈ مثال کے بارے میں جاننا چاہتے ہیں، تو یہاں کچھ اضافی تفصیلات ہیں۔

#### `value.startswith()` کے ساتھ String { #string-with-value-startswith }

کیا آپ نے غور کیا؟ `value.startswith()` استعمال کرنے والی string ایک tuple لے سکتی ہے، اور یہ tuple میں ہر قدر کو جانچے گی:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[16:19] hl[17] *}

#### ایک بے ترتیب آئٹم { #a-random-item }

`data.items()` سے ہمیں ایک <dfn title="Something we can iterate on with a for loop, like a list, set, etc.">iterable object</dfn> ملتا ہے جس میں ہر dictionary آئٹم کے لیے key اور value پر مشتمل tuples ہوتے ہیں۔

ہم اس iterable object کو `list(data.items())` سے صحیح `list` میں تبدیل کرتے ہیں۔

پھر `random.choice()` سے ہم list سے ایک **بے ترتیب قدر** حاصل کر سکتے ہیں، تو ہمیں `(id, name)` کے ساتھ ایک tuple ملتا ہے۔ یہ کچھ ایسا ہوگا جیسے `("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy")`۔

پھر ہم tuple کی وہ **دو اقدار** متغیرات `id` اور `name` کو **تفویض** کرتے ہیں۔

تو، اگر صارف نے item ID فراہم نہیں کی، تو انہیں پھر بھی ایک بے ترتیب تجویز ملے گی۔

...ہم یہ سب ایک **سادہ لائن** میں کرتے ہیں۔ کیا آپ کو Python پسند نہیں؟

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[22:30] hl[29] *}

## خلاصہ { #recap }

آپ اپنے parameters کے لیے اضافی validations اور metadata اعلان کر سکتے ہیں۔

عمومی validations اور metadata:

* `alias`
* `title`
* `description`
* `deprecated`

Strings کے لیے مخصوص validations:

* `min_length`
* `max_length`
* `pattern`

`AfterValidator` استعمال کر کے حسب ضرورت validations۔

ان مثالوں میں آپ نے دیکھا کہ `str` اقدار کے لیے validations کیسے اعلان کیے جائیں۔

اگلے ابواب دیکھیں تاکہ جانیں کہ دوسری اقسام، جیسے نمبروں کے لیے validations کیسے اعلان کیے جائیں۔
