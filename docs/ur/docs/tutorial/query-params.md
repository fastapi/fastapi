# Query Parameters { #query-parameters }

جب آپ دوسرے function parameters کا اعلان کرتے ہیں جو path parameters کا حصہ نہیں ہیں، تو وہ خودکار طور پر "query" parameters کے طور پر سمجھے جاتے ہیں۔

{* ../../docs_src/query_params/tutorial001_py310.py hl[9] *}

Query وہ key-value جوڑوں کا مجموعہ ہے جو URL میں `?` کے بعد آتے ہیں، `&` حروف سے الگ کیے گئے۔

مثال کے طور پر، اس URL میں:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...query parameters یہ ہیں:

* `skip`: قدر `0` کے ساتھ
* `limit`: قدر `10` کے ساتھ

چونکہ یہ URL کا حصہ ہیں، یہ "قدرتی طور پر" strings ہیں۔

لیکن جب آپ انہیں Python types کے ساتھ اعلان کرتے ہیں (اوپر کی مثال میں، `int` کے طور پر)، تو وہ اس قسم میں تبدیل اور اس کے خلاف توثیق ہو جاتے ہیں۔

وہ تمام عمل جو path parameters پر لاگو ہوتا ہے query parameters پر بھی لاگو ہوتا ہے:

* ایڈیٹر سپورٹ (ظاہر ہے)
* ڈیٹا <dfn title="converting the string that comes from an HTTP request into Python data">"parsing"</dfn>
* ڈیٹا کی توثیق
* خودکار دستاویزات

## طے شدہ اقدار { #defaults }

چونکہ query parameters path کا مقررہ حصہ نہیں ہیں، وہ اختیاری ہو سکتے ہیں اور طے شدہ اقدار رکھ سکتے ہیں۔

اوپر کی مثال میں ان کی طے شدہ اقدار `skip=0` اور `limit=10` ہیں۔

تو، اس URL پر جانا:

```
http://127.0.0.1:8000/items/
```

ایسا ہی ہوگا جیسے اس پر جانا:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

لیکن اگر آپ مثال کے طور پر اس پر جائیں:

```
http://127.0.0.1:8000/items/?skip=20
```

آپ کے function میں parameter اقدار ہوں گی:

* `skip=20`: کیونکہ آپ نے URL میں یہ سیٹ کیا
* `limit=10`: کیونکہ یہ طے شدہ قدر تھی

## اختیاری parameters { #optional-parameters }

اسی طرح، آپ اختیاری query parameters کا اعلان کر سکتے ہیں، ان کی طے شدہ قدر `None` سیٹ کر کے:

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

اس صورت میں، function parameter `q` اختیاری ہوگا، اور پہلے سے `None` ہوگا۔

/// check

یہ بھی نوٹ کریں کہ **FastAPI** اتنا ذہین ہے کہ وہ جان لے کہ path parameter `item_id` ایک path parameter ہے اور `q` نہیں ہے، لہذا یہ query parameter ہے۔

///

## Query parameter type کی تبدیلی { #query-parameter-type-conversion }

آپ `bool` types کا بھی اعلان کر سکتے ہیں، اور وہ تبدیل ہو جائیں گے:

{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

اس صورت میں، اگر آپ اس پر جائیں:

```
http://127.0.0.1:8000/items/foo?short=1
```

یا

```
http://127.0.0.1:8000/items/foo?short=True
```

یا

```
http://127.0.0.1:8000/items/foo?short=true
```

یا

```
http://127.0.0.1:8000/items/foo?short=on
```

یا

```
http://127.0.0.1:8000/items/foo?short=yes
```

یا کوئی بھی دوسری حروف کی تبدیلی (بڑے حروف، پہلا حرف بڑا وغیرہ)، آپ کا function `short` parameter کو `bool` قدر `True` کے ساتھ دیکھے گا۔ ورنہ `False`۔


## متعدد path اور query parameters { #multiple-path-and-query-parameters }

آپ ایک ساتھ متعدد path parameters اور query parameters کا اعلان کر سکتے ہیں، **FastAPI** جانتا ہے کون سا کون سا ہے۔

اور آپ کو انہیں کسی مخصوص ترتیب میں اعلان کرنے کی ضرورت نہیں۔

وہ نام سے پہچانے جائیں گے:

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## لازمی query parameters { #required-query-parameters }

جب آپ غیر path parameters (ابھی تک ہم نے صرف query parameters دیکھے ہیں) کے لیے طے شدہ قدر کا اعلان کرتے ہیں، تو یہ لازمی نہیں ہوتا۔

اگر آپ کوئی مخصوص قدر شامل نہیں کرنا چاہتے لیکن اسے اختیاری بنانا چاہتے ہیں، تو طے شدہ قدر `None` سیٹ کریں۔

لیکن جب آپ query parameter کو لازمی بنانا چاہتے ہیں، تو آپ کوئی طے شدہ قدر اعلان نہ کریں:

{* ../../docs_src/query_params/tutorial005_py310.py hl[6:7] *}

یہاں query parameter `needy` ایک لازمی query parameter ہے جس کی قسم `str` ہے۔

اگر آپ اپنے براؤزر میں یہ URL کھولیں:

```
http://127.0.0.1:8000/items/foo-item
```

...لازمی parameter `needy` شامل کیے بغیر، آپ کو یہ error نظر آئے گی:

```JSON
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "needy"
      ],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

چونکہ `needy` ایک لازمی parameter ہے، آپ کو اسے URL میں سیٹ کرنا ہوگا:

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

...یہ کام کرے گا:

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

اور یقیناً، آپ کچھ parameters کو لازمی، کچھ کو طے شدہ قدر کے ساتھ، اور کچھ کو مکمل طور پر اختیاری بنا سکتے ہیں:

{* ../../docs_src/query_params/tutorial006_py310.py hl[8] *}

اس صورت میں، 3 query parameters ہیں:

* `needy`، ایک لازمی `str`۔
* `skip`، ایک `int` جس کی طے شدہ قدر `0` ہے۔
* `limit`، ایک اختیاری `int`۔

/// tip | مشورہ

آپ `Enum`s بھی اسی طرح استعمال کر سکتے ہیں جیسے [Path Parameters](path-params.md#predefined-values) کے ساتھ۔

///
