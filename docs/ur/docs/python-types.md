# Python Types کا تعارف { #python-types-intro }

Python میں اختیاری "type hints" (جنہیں "type annotations" بھی کہا جاتا ہے) کی سپورٹ موجود ہے۔

یہ **"type hints"** یا annotations ایک خاص syntax ہیں جو کسی variable کی <dfn title="for example: str, int, float, bool">type</dfn> بیان کرنے کی اجازت دیتے ہیں۔

اپنے variables کے لیے types بیان کر کے، ایڈیٹرز اور ٹولز آپ کو بہتر سپورٹ فراہم کر سکتے ہیں۔

یہ صرف Python type hints کے بارے میں ایک **فوری tutorial / جائزہ** ہے۔ یہ صرف اتنا کم سے کم احاطہ کرتا ہے جتنا **FastAPI** کے ساتھ استعمال کے لیے ضروری ہے... جو دراصل بہت تھوڑا ہے۔

**FastAPI** مکمل طور پر ان type hints پر مبنی ہے، یہ اسے بہت سے فوائد اور فائدے دیتے ہیں۔

لیکن اگر آپ کبھی بھی **FastAPI** استعمال نہ کریں، تب بھی ان کے بارے میں تھوڑا سیکھنا آپ کے لیے فائدہ مند ہوگا۔

/// note | نوٹ

اگر آپ Python کے ماہر ہیں، اور آپ type hints کے بارے میں پہلے سے سب کچھ جانتے ہیں، تو اگلے باب پر جائیں۔

///

## مقصد { #motivation }

آئیے ایک سادہ مثال سے شروع کرتے ہیں:

{* ../../docs_src/python_types/tutorial001_py310.py *}

اس پروگرام کو چلانے سے یہ نتیجہ آتا ہے:

```
John Doe
```

function یہ کرتا ہے:

* ایک `first_name` اور `last_name` لیتا ہے۔
* ہر ایک کے پہلے حرف کو `title()` کے ساتھ بڑے حرف میں تبدیل کرتا ہے۔
* درمیان میں خالی جگہ کے ساتھ انہیں <dfn title="Puts them together, as one. With the contents of one after the other.">جوڑتا</dfn> ہے۔

{* ../../docs_src/python_types/tutorial001_py310.py hl[2] *}

### اس میں ترمیم کریں { #edit-it }

یہ ایک بہت سادہ پروگرام ہے۔

لیکن اب تصور کریں کہ آپ اسے شروع سے لکھ رہے تھے۔

کسی وقت آپ نے function کی تعریف شروع کی ہوگی، parameters تیار تھے...

لیکن پھر آپ کو "وہ method کال کرنا ہے جو پہلے حرف کو بڑے حرف میں تبدیل کرتا ہے"۔

کیا وہ `upper` تھا؟ `uppercase`؟ `first_uppercase`؟ `capitalize`؟

پھر، آپ پرانے پروگرامر کے دوست، ایڈیٹر autocompletion سے مدد لیتے ہیں۔

آپ function کا پہلا parameter `first_name` ٹائپ کرتے ہیں، پھر ایک ڈاٹ (`.`) اور پھر `Ctrl+Space` دبا کر completion شروع کرتے ہیں۔

لیکن، افسوس، آپ کو کچھ مفید نہیں ملتا:

<img src="/img/python-types/image01.png">

### Types شامل کریں { #add-types }

آئیے پچھلے ورژن کی ایک لائن تبدیل کرتے ہیں۔

ہم بالکل یہ حصہ تبدیل کریں گے، function کے parameters، اس سے:

```Python
    first_name, last_name
```

اس میں:

```Python
    first_name: str, last_name: str
```

بس اتنا ہی۔

یہ ہیں "type hints":

{* ../../docs_src/python_types/tutorial002_py310.py hl[1] *}

یہ وہی نہیں ہے جو default values بیان کرنا ہوتا جیسے:

```Python
    first_name="john", last_name="doe"
```

یہ ایک الگ چیز ہے۔

ہم colons (`:`) استعمال کر رہے ہیں، نہ کہ equals (`=`)۔

اور type hints شامل کرنے سے عام طور پر وہ نہیں بدلتا جو ان کے بغیر ہوتا۔

لیکن اب، تصور کریں کہ آپ پھر سے وہ function بنا رہے ہیں، لیکن type hints کے ساتھ۔

اسی مقام پر، آپ `Ctrl+Space` سے autocomplete شروع کرتے ہیں اور آپ دیکھتے ہیں:

<img src="/img/python-types/image02.png">

اس کے ساتھ، آپ سکرول کر سکتے ہیں، اختیارات دیکھتے ہوئے، جب تک وہ نہ ملے جو "یاد آتا ہے":

<img src="/img/python-types/image03.png">

## مزید مقصد { #more-motivation }

یہ function دیکھیں، اس میں پہلے سے type hints ہیں:

{* ../../docs_src/python_types/tutorial003_py310.py hl[1] *}

کیونکہ ایڈیٹر variables کی types جانتا ہے، آپ کو صرف completion ہی نہیں ملتی، بلکہ error checks بھی ملتی ہیں:

<img src="/img/python-types/image04.png">

اب آپ جانتے ہیں کہ آپ کو اسے ٹھیک کرنا ہے، `age` کو `str(age)` سے string میں تبدیل کرنا ہے:

{* ../../docs_src/python_types/tutorial004_py310.py hl[2] *}

## Types بیان کرنا { #declaring-types }

آپ نے ابھی type hints بیان کرنے کی اصل جگہ دیکھی۔ Function parameters کے طور پر۔

یہ وہ اصل جگہ بھی ہے جہاں آپ انہیں **FastAPI** کے ساتھ استعمال کریں گے۔

### سادہ types { #simple-types }

آپ تمام معیاری Python types بیان کر سکتے ہیں، نہ صرف `str`۔

آپ استعمال کر سکتے ہیں، مثال کے طور پر:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py310.py hl[1] *}

### `typing` module { #typing-module }

کچھ اضافی استعمال کے معاملات کے لیے، آپ کو معیاری لائبریری `typing` module سے کچھ چیزیں import کرنی پڑ سکتی ہیں، مثال کے طور پر جب آپ بیان کرنا چاہیں کہ کسی چیز کی "کوئی بھی type" ہے، تو آپ `typing` سے `Any` استعمال کر سکتے ہیں:

```python
from typing import Any


def some_function(data: Any):
    print(data)
```

### Generic types { #generic-types }

کچھ types اپنے اندرونی types بیان کرنے کے لیے مربع بریکٹس میں "type parameters" لے سکتی ہیں، مثال کے طور پر "strings کی list" کو `list[str]` لکھا جائے گا۔

وہ types جو type parameters لے سکتی ہیں، انہیں **Generic types** یا **Generics** کہا جاتا ہے۔

آپ وہی بلٹ ان types بطور generics استعمال کر سکتے ہیں (مربع بریکٹس اور اندر types کے ساتھ):

* `list`
* `tuple`
* `set`
* `dict`

#### List { #list }

مثال کے طور پر، آئیے ایک variable کو `str` کی `list` کے طور پر بیان کرتے ہیں۔

اسی colon (`:`) syntax کے ساتھ variable بیان کریں۔

Type کے طور پر `list` رکھیں۔

چونکہ list ایک ایسی type ہے جس میں کچھ اندرونی types ہیں، آپ انہیں مربع بریکٹس میں رکھتے ہیں:

{* ../../docs_src/python_types/tutorial006_py310.py hl[1] *}

/// info | معلومات

مربع بریکٹس میں وہ اندرونی types "type parameters" کہلاتی ہیں۔

اس صورت میں، `str` وہ type parameter ہے جو `list` کو دیا گیا ہے۔

///

اس کا مطلب ہے: "variable `items` ایک `list` ہے، اور اس list کا ہر آئٹم ایک `str` ہے"۔

ایسا کرنے سے، آپ کا ایڈیٹر list سے آئٹمز پر عمل کرتے ہوئے بھی سپورٹ فراہم کر سکتا ہے:

<img src="/img/python-types/image05.png">

Types کے بغیر، یہ تقریباً ناممکن ہے۔

غور کریں کہ variable `item` list `items` کے عناصر میں سے ایک ہے۔

اور پھر بھی، ایڈیٹر جانتا ہے کہ یہ ایک `str` ہے، اور اس کے لیے سپورٹ فراہم کرتا ہے۔

#### Tuple اور Set { #tuple-and-set }

`tuple` اور `set` بیان کرنے کے لیے بھی آپ ایسا ہی کریں گے:

{* ../../docs_src/python_types/tutorial007_py310.py hl[1] *}

اس کا مطلب ہے:

* Variable `items_t` ایک `tuple` ہے جس میں 3 آئٹمز ہیں، ایک `int`، ایک اور `int`، اور ایک `str`۔
* Variable `items_s` ایک `set` ہے، اور اس کا ہر آئٹم `bytes` type کا ہے۔

#### Dict { #dict }

`dict` بیان کرنے کے لیے، آپ کوما سے الگ کر کے 2 type parameters دیتے ہیں۔

پہلا type parameter `dict` کی keys کے لیے ہے۔

دوسرا type parameter `dict` کی values کے لیے ہے:

{* ../../docs_src/python_types/tutorial008_py310.py hl[1] *}

اس کا مطلب ہے:

* Variable `prices` ایک `dict` ہے:
    * اس `dict` کی keys `str` type کی ہیں (فرض کریں، ہر آئٹم کا نام)۔
    * اس `dict` کی values `float` type کی ہیں (فرض کریں، ہر آئٹم کی قیمت)۔

#### Union { #union }

آپ بیان کر سکتے ہیں کہ ایک variable **کئی types** میں سے کوئی بھی ہو سکتا ہے، مثال کے طور پر، ایک `int` یا ایک `str`۔

اسے بیان کرنے کے لیے آپ دونوں types کو الگ کرنے کے لیے <dfn title='also called "bitwise or operator", but that meaning is not relevant here'>عمودی بار (`|`)</dfn> استعمال کرتے ہیں۔

اسے "union" کہا جاتا ہے، کیونکہ variable ان دو types کے مجموعے میں سے کچھ بھی ہو سکتا ہے۔

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

اس کا مطلب ہے کہ `item` ایک `int` یا ایک `str` ہو سکتا ہے۔

#### ممکنہ طور پر `None` { #possibly-none }

آپ بیان کر سکتے ہیں کہ کسی value کی type ہو سکتی ہے، جیسے `str`، لیکن یہ `None` بھی ہو سکتی ہے۔

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

صرف `str` کے بجائے `str | None` استعمال کرنے سے ایڈیٹر آپ کو ان غلطیوں کا پتہ لگانے میں مدد کر سکے گا جہاں آپ فرض کر رہے ہوں کہ کوئی value ہمیشہ `str` ہے، جبکہ یہ دراصل `None` بھی ہو سکتی ہے۔

### بطور types Classes { #classes-as-types }

آپ کسی class کو بھی variable کی type کے طور پر بیان کر سکتے ہیں۔

فرض کریں آپ کے پاس ایک `Person` class ہے، جس میں ایک name ہے:

{* ../../docs_src/python_types/tutorial010_py310.py hl[1:3] *}

پھر آپ ایک variable کو `Person` type کا بیان کر سکتے ہیں:

{* ../../docs_src/python_types/tutorial010_py310.py hl[6] *}

اور پھر، آپ کو دوبارہ تمام ایڈیٹر سپورٹ ملتی ہے:

<img src="/img/python-types/image06.png">

غور کریں کہ اس کا مطلب ہے "`one_person` class `Person` کی ایک **instance** ہے"۔

اس کا مطلب یہ نہیں کہ "`one_person` وہ **class** ہے جو `Person` کہلاتی ہے"۔

## Pydantic models { #pydantic-models }

[Pydantic](https://docs.pydantic.dev/) data validation کے لیے ایک Python لائبریری ہے۔

آپ ڈیٹا کی "شکل" attributes والی classes کے طور پر بیان کرتے ہیں۔

اور ہر attribute کی ایک type ہوتی ہے۔

پھر آپ کچھ values کے ساتھ اس class کی ایک instance بناتے ہیں اور یہ values کی توثیق کرے گا، انہیں مناسب type میں تبدیل کرے گا (اگر ایسا ہو) اور آپ کو تمام ڈیٹا کے ساتھ ایک object دے گا۔

اور آپ کو اس نتیجے میں ملنے والی object کے ساتھ تمام ایڈیٹر سپورٹ ملتی ہے۔

سرکاری Pydantic دستاویزات سے ایک مثال:

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info | معلومات

[Pydantic کے بارے میں مزید جاننے کے لیے، اس کی دستاویزات دیکھیں](https://docs.pydantic.dev/)۔

///

**FastAPI** مکمل طور پر Pydantic پر مبنی ہے۔

آپ [Tutorial - User Guide](tutorial/index.md) میں عملی طور پر یہ سب بہت زیادہ دیکھیں گے۔

## Metadata Annotations کے ساتھ Type Hints { #type-hints-with-metadata-annotations }

Python میں ایک خصوصیت بھی ہے جو `Annotated` استعمال کر کے ان type hints میں **اضافی <dfn title="Data about the data, in this case, information about the type, e.g. a description.">metadata</dfn>** رکھنے کی اجازت دیتی ہے۔

آپ `typing` سے `Annotated` import کر سکتے ہیں۔

{* ../../docs_src/python_types/tutorial013_py310.py hl[1,4] *}

Python خود اس `Annotated` کے ساتھ کچھ نہیں کرتا۔ اور ایڈیٹرز اور دیگر ٹولز کے لیے، type ابھی بھی `str` ہے۔

لیکن آپ `Annotated` میں اس جگہ کو **FastAPI** کو اضافی metadata فراہم کرنے کے لیے استعمال کر سکتے ہیں کہ آپ اپنی ایپلیکیشن کو کیسے چلانا چاہتے ہیں۔

یاد رکھنے کی اہم بات یہ ہے کہ `Annotated` کو دیا جانے والا **پہلا *type parameter*** ہی **اصل type** ہے۔ باقی سب دوسرے ٹولز کے لیے صرف metadata ہے۔

ابھی کے لیے، آپ کو بس یہ جاننا ہے کہ `Annotated` موجود ہے، اور یہ معیاری Python ہے۔ 😎

بعد میں آپ دیکھیں گے کہ یہ کتنا **طاقتور** ہو سکتا ہے۔

/// tip | مشورہ

یہ حقیقت کہ یہ **معیاری Python** ہے اس کا مطلب ہے کہ آپ کو اپنے ایڈیٹر میں ابھی بھی **بہترین ممکنہ ڈویلپر تجربہ** ملے گا، ان ٹولز کے ساتھ جو آپ code کا تجزیہ اور refactor کرنے کے لیے استعمال کرتے ہیں، وغیرہ۔ ✨

اور یہ بھی کہ آپ کا code بہت سے دیگر Python ٹولز اور لائبریریز کے ساتھ بہت ہم آہنگ ہوگا۔ 🚀

///

## **FastAPI** میں Type hints { #type-hints-in-fastapi }

**FastAPI** ان type hints کا فائدہ اٹھاتا ہے کئی کام کرنے کے لیے۔

**FastAPI** کے ساتھ آپ type hints کے ساتھ parameters بیان کرتے ہیں اور آپ کو ملتا ہے:

* **ایڈیٹر سپورٹ**۔
* **Type checks**۔

...اور **FastAPI** انہی اعلانات کو استعمال کرتا ہے:

* **ضروریات بیان کرنے** کے لیے: request path parameters، query parameters، headers، bodies، dependencies وغیرہ سے۔
* **ڈیٹا تبدیل کرنے** کے لیے: request سے مطلوبہ type میں۔
* **ڈیٹا کی توثیق** کے لیے: ہر request سے آنے والے:
    * ڈیٹا غلط ہونے پر client کو واپس بھیجی جانے والی **خودکار غلطیاں** بنانا۔
* OpenAPI استعمال کرتے ہوئے API کی **دستاویزات** بنانا:
    * جو پھر خودکار تعاملی دستاویزات کے یوزر انٹرفیسز استعمال کرتی ہیں۔

یہ سب خلاصہ لگ سکتا ہے۔ فکر نہ کریں۔ آپ [Tutorial - User Guide](tutorial/index.md) میں یہ سب عمل میں دیکھیں گے۔

اہم بات یہ ہے کہ معیاری Python types استعمال کر کے، ایک ہی جگہ پر (مزید classes، decorators وغیرہ شامل کرنے کے بجائے)، **FastAPI** آپ کا بہت سا کام خود کر لے گا۔

/// info | معلومات

اگر آپ پورا tutorial پڑھ چکے ہیں اور types کے بارے میں مزید جاننے واپس آئے ہیں، تو ایک اچھا ذریعہ [`mypy` کی "cheat sheet"](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html) ہے۔

///
