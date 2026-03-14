# Body - متعدد Parameters { #body-multiple-parameters }

اب جب ہم `Path` اور `Query` استعمال کرنا دیکھ چکے ہیں، آئیے request body اعلانات کے مزید جدید استعمال دیکھتے ہیں۔

## `Path`، `Query` اور body parameters کو ملائیں { #mix-path-query-and-body-parameters }

سب سے پہلے، یقیناً، آپ `Path`، `Query` اور request body parameter اعلانات کو آزادانہ طور پر ملا سکتے ہیں اور **FastAPI** جانے گا کیا کرنا ہے۔

اور آپ body parameters کو اختیاری بھی اعلان کر سکتے ہیں، طے شدہ قدر `None` سیٹ کر کے:

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note | نوٹ

غور کریں کہ، اس صورت میں، `item` جو body سے لیا جائے گا اختیاری ہے۔ کیونکہ اس کی `None` طے شدہ قدر ہے۔

///

## متعدد body parameters { #multiple-body-parameters }

پچھلی مثال میں، *path operations* ایک JSON body کی توقع کرتی تھیں جس میں `Item` کی attributes ہوں، جیسے:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

لیکن آپ متعدد body parameters بھی اعلان کر سکتے ہیں، مثلاً `item` اور `user`:

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}


اس صورت میں، **FastAPI** نوٹ کرے گا کہ function میں ایک سے زیادہ body parameter ہیں (دو parameters ہیں جو Pydantic models ہیں)۔

تو، یہ parameter کے ناموں کو body میں keys (فیلڈ ناموں) کے طور پر استعمال کرے گا، اور اس طرح کی body کی توقع کرے گا:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

/// note | نوٹ

غور کریں کہ اگرچہ `item` پہلے کی طرح ہی اعلان کیا گیا تھا، اب اس کی توقع body کے اندر key `item` کے ساتھ ہے۔

///

**FastAPI** request سے خودکار تبدیلی کرے گا، تاکہ parameter `item` کو اس کا مخصوص مواد ملے اور `user` کو بھی وہی۔

یہ مرکب ڈیٹا کی توثیق کرے گا، اور اسے OpenAPI schema اور خودکار docs کے لیے اسی طرح دستاویز کرے گا۔

## Body میں واحد اقدار { #singular-values-in-body }

اسی طرح جیسے query اور path parameters کے لیے اضافی ڈیٹا بیان کرنے کے لیے `Query` اور `Path` ہیں، **FastAPI** ایک مساوی `Body` فراہم کرتا ہے۔

مثال کے طور پر، پچھلے model کو بڑھاتے ہوئے، آپ فیصلہ کر سکتے ہیں کہ `item` اور `user` کے علاوہ اسی body میں ایک اور key `importance` چاہتے ہیں۔

اگر آپ اسے جیسا ہے اعلان کریں، چونکہ یہ واحد قدر ہے، **FastAPI** فرض کرے گا کہ یہ query parameter ہے۔

لیکن آپ **FastAPI** کو ہدایت دے سکتے ہیں کہ اسے `Body` استعمال کر کے ایک اور body key کے طور پر سمجھے:

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}


اس صورت میں، **FastAPI** اس طرح کی body کی توقع کرے گا:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

ایک بار پھر، یہ data types تبدیل کرے گا، توثیق کرے گا، دستاویز بنائے گا وغیرہ۔

## متعدد body params اور query { #multiple-body-params-and-query }

یقیناً، آپ کسی بھی body parameters کے علاوہ جب بھی ضرورت ہو اضافی query parameters بھی اعلان کر سکتے ہیں۔

چونکہ، پہلے سے، واحد اقدار query parameters کے طور پر سمجھی جاتی ہیں، آپ کو واضح طور پر `Query` شامل کرنے کی ضرورت نہیں، آپ بس یہ کر سکتے ہیں:

```Python
q: str | None = None
```

مثال کے طور پر:

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}


/// info | معلومات

`Body` میں بھی وہی تمام اضافی توثیق اور metadata parameters ہیں جو `Query`، `Path` اور دوسروں میں ہیں جو آپ بعد میں دیکھیں گے۔

///

## واحد body parameter کو embed کریں { #embed-a-single-body-parameter }

فرض کریں آپ کے پاس Pydantic model `Item` سے صرف ایک `item` body parameter ہے۔

پہلے سے، **FastAPI** اس کی body براہ راست توقع کرے گا۔

لیکن اگر آپ چاہتے ہیں کہ یہ ایک JSON کی توقع کرے جس میں key `item` ہو اور اس کے اندر model کا مواد، جیسا کہ اضافی body parameters اعلان کرنے پر ہوتا ہے، تو آپ خاص `Body` parameter `embed` استعمال کر سکتے ہیں:

```Python
item: Item = Body(embed=True)
```

جیسے:

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}


اس صورت میں **FastAPI** اس طرح کی body کی توقع کرے گا:

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

اس کی بجائے:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## خلاصہ { #recap }

آپ اپنے *path operation function* میں متعدد body parameters شامل کر سکتے ہیں، اگرچہ ایک request میں صرف ایک body ہو سکتی ہے۔

لیکن **FastAPI** اسے سنبھالے گا، آپ کو آپ کے function میں صحیح ڈیٹا دے گا، اور *path operation* میں صحیح schema کی توثیق اور دستاویز بنائے گا۔

آپ واحد اقدار کو body کے حصے کے طور پر وصول کرنے کا بھی اعلان کر سکتے ہیں۔

اور آپ **FastAPI** کو ہدایت دے سکتے ہیں کہ body کو ایک key میں embed کرے چاہے صرف ایک parameter اعلان کیا گیا ہو۔
