# Classes بطور Dependencies { #classes-as-dependencies }

**Dependency Injection** نظام میں مزید گہرائی میں جانے سے پہلے، آئیے پچھلی مثال کو بہتر بناتے ہیں۔

## پچھلی مثال سے ایک `dict` { #a-dict-from-the-previous-example }

پچھلی مثال میں، ہم اپنی dependency ("dependable") سے ایک `dict` واپس کر رہے تھے:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[9] *}

لیکن پھر ہمیں *path operation function* کے parameter `commons` میں ایک `dict` ملتا ہے۔

اور ہم جانتے ہیں کہ editors `dict` کے لیے زیادہ مدد (جیسے completion) فراہم نہیں کر سکتے، کیونکہ وہ ان کی keys اور value types نہیں جان سکتے۔

ہم بہتر کر سکتے ہیں...

## Dependency کس چیز سے بنتی ہے { #what-makes-a-dependency }

اب تک آپ نے dependencies کو functions کے طور پر declare ہوتے دیکھا ہے۔

لیکن dependencies declare کرنے کا یہ واحد طریقہ نہیں ہے (حالانکہ یہ غالباً سب سے عام طریقہ ہوگا)۔

اہم بات یہ ہے کہ dependency ایک "callable" ہونی چاہیے۔

Python میں **"callable"** وہ چیز ہے جسے Python ایک function کی طرح "call" کر سکے۔

تو، اگر آپ کے پاس ایک object `something` ہے (جو شاید function _نہ_ ہو) اور آپ اسے اس طرح "call" (execute) کر سکتے ہیں:

```Python
something()
```

یا

```Python
something(some_argument, some_keyword_argument="foo")
```

تو یہ "callable" ہے۔

## Classes بطور dependencies { #classes-as-dependencies_1 }

آپ نے شاید محسوس کیا ہوگا کہ Python class کا instance بنانے کے لیے بھی وہی syntax استعمال ہوتا ہے۔

مثال کے طور پر:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

اس صورت میں، `fluffy` class `Cat` کا ایک instance ہے۔

اور `fluffy` بنانے کے لیے، آپ `Cat` کو "call" کر رہے ہیں۔

تو، Python class بھی ایک **callable** ہے۔

پھر، **FastAPI** میں، آپ Python class کو dependency کے طور پر استعمال کر سکتے ہیں۔

FastAPI دراصل یہ چیک کرتا ہے کہ یہ "callable" ہے (function، class یا کوئی بھی اور چیز) اور اس میں define کیے گئے parameters۔

اگر آپ **FastAPI** میں dependency کے طور پر "callable" پاس کرتے ہیں، تو یہ اس "callable" کے parameters کا تجزیہ کرے گا، اور انہیں اسی طرح process کرے گا جیسے *path operation function* کے parameters کو۔ بشمول sub-dependencies۔

یہ بغیر کسی parameter والے callables پر بھی لاگو ہوتا ہے۔ بالکل ویسے ہی جیسے بغیر parameters والے *path operation functions* کے ساتھ ہوتا ہے۔

پھر، ہم dependency "dependable" `common_parameters` کو اوپر سے class `CommonQueryParams` میں تبدیل کر سکتے ہیں:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[11:15] *}

`__init__` method پر توجہ دیں جو class کا instance بنانے کے لیے استعمال ہوتا ہے:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[12] *}

...اس میں ہمارے پچھلے `common_parameters` جیسے ہی parameters ہیں:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8] *}

یہ parameters وہ ہیں جو **FastAPI** dependency کو "حل" کرنے کے لیے استعمال کرے گا۔

دونوں صورتوں میں، اس میں ہوگا:

* ایک اختیاری `q` query parameter جو `str` ہے۔
* ایک `skip` query parameter جو `int` ہے، جس کی default value `0` ہے۔
* ایک `limit` query parameter جو `int` ہے، جس کی default value `100` ہے۔

دونوں صورتوں میں data convert، validate، OpenAPI schema پر document ہوگا، وغیرہ۔

## اسے استعمال کریں { #use-it }

اب آپ اس class کا استعمال کرتے ہوئے اپنی dependency declare کر سکتے ہیں۔

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[19] *}

**FastAPI** `CommonQueryParams` class کو call کرتا ہے۔ اس سے اس class کا ایک "instance" بنتا ہے اور وہ instance آپ کے function میں parameter `commons` کے طور پر پاس ہوتا ہے۔

## Type annotation بمقابلہ `Depends` { #type-annotation-vs-depends }

دھیان دیں کہ اوپر کے code میں ہم `CommonQueryParams` دو بار لکھ رہے ہیں:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | مشورہ

ممکن ہو تو `Annotated` version استعمال کریں۔

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

آخری `CommonQueryParams`، اس میں:

```Python
... Depends(CommonQueryParams)
```

...یہ وہ ہے جسے **FastAPI** دراصل dependency جاننے کے لیے استعمال کرے گا۔

اسی سے FastAPI declare کیے گئے parameters نکالے گا اور اسی کو FastAPI دراصل call کرے گا۔

---

اس صورت میں، پہلا `CommonQueryParams`، اس میں:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, ...
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | مشورہ

ممکن ہو تو `Annotated` version استعمال کریں۔

///

```Python
commons: CommonQueryParams ...
```

////

...**FastAPI** کے لیے کوئی خاص معنی نہیں رکھتا۔ FastAPI اسے data conversion، validation، وغیرہ کے لیے استعمال نہیں کرے گا (کیونکہ یہ اس کے لیے `Depends(CommonQueryParams)` استعمال کر رہا ہے)۔

آپ دراصل صرف یہ بھی لکھ سکتے ہیں:

//// tab | Python 3.10+

```Python
commons: Annotated[Any, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | مشورہ

ممکن ہو تو `Annotated` version استعمال کریں۔

///

```Python
commons = Depends(CommonQueryParams)
```

////

...جیسے:

{* ../../docs_src/dependencies/tutorial003_an_py310.py hl[19] *}

لیکن type declare کرنے کی حوصلہ افزائی کی جاتی ہے کیونکہ اس طرح آپ کا editor جانے گا کہ parameter `commons` کے طور پر کیا پاس ہوگا، اور پھر یہ code completion، type checks، وغیرہ میں آپ کی مدد کر سکتا ہے:

<img src="/img/tutorial/dependencies/image02.png">

## شارٹ کٹ { #shortcut }

لیکن آپ دیکھتے ہیں کہ یہاں کچھ code تکرار ہو رہی ہے، `CommonQueryParams` دو بار لکھنا:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | مشورہ

ممکن ہو تو `Annotated` version استعمال کریں۔

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

**FastAPI** ان صورتوں کے لیے ایک شارٹ کٹ فراہم کرتا ہے، جہاں dependency *خاص طور پر* ایک class ہے جسے **FastAPI** خود class کا instance بنانے کے لیے "call" کرے گا۔

ان مخصوص صورتوں کے لیے، آپ یہ کر سکتے ہیں:

یہ لکھنے کے بجائے:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | مشورہ

ممکن ہو تو `Annotated` version استعمال کریں۔

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

...آپ یہ لکھیں:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends()]
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | مشورہ

ممکن ہو تو `Annotated` version استعمال کریں۔

///

```Python
commons: CommonQueryParams = Depends()
```

////

آپ dependency کو parameter کی type کے طور پر declare کرتے ہیں، اور `Depends()` کو بغیر کسی parameter کے استعمال کرتے ہیں، `Depends(CommonQueryParams)` کے اندر پوری class *دوبارہ* لکھنے کے بجائے۔

وہی مثال پھر اس طرح نظر آئے گی:

{* ../../docs_src/dependencies/tutorial004_an_py310.py hl[19] *}

...اور **FastAPI** جانے گا کہ کیا کرنا ہے۔

/// tip | مشورہ

اگر یہ مدد سے زیادہ الجھن لگے، تو اسے نظرانداز کریں، آپ کو اس کی *ضرورت* نہیں ہے۔

یہ صرف ایک شارٹ کٹ ہے۔ کیونکہ **FastAPI** code کی تکرار کم کرنے میں آپ کی مدد کرنے کا خیال رکھتا ہے۔

///
