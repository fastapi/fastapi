# Header Parameter Models { #header-parameter-models }

اگر آپ کے پاس ایک دوسرے سے متعلقہ **header parameters** کا گروپ ہے، تو آپ انہیں declare کرنے کے لیے ایک **Pydantic model** بنا سکتے ہیں۔

اس سے آپ کو **model کو کئی جگہوں پر دوبارہ استعمال** کرنے اور تمام parameters کے لیے validations اور metadata ایک ساتھ declare کرنے کی سہولت ملے گی۔ 😎

/// note | نوٹ

یہ FastAPI version `0.115.0` سے supported ہے۔ 🤓

///

## Pydantic Model کے ساتھ Header Parameters { #header-parameters-with-a-pydantic-model }

وہ **header parameters** جو آپ کو درکار ہیں انہیں ایک **Pydantic model** میں declare کریں، اور پھر parameter کو `Header` کے طور پر declare کریں:

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI** request میں موجود **headers** سے **ہر field** کا ڈیٹا **extract** کرے گا اور آپ کو وہ Pydantic model دے گا جو آپ نے define کیا ہے۔

## Docs چیک کریں { #check-the-docs }

آپ `/docs` پر docs UI میں مطلوبہ headers دیکھ سکتے ہیں:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## اضافی Headers پر پابندی { #forbid-extra-headers }

بعض خاص استعمال کے معاملات میں (شاید بہت عام نہیں)، آپ ان headers کو **محدود** کرنا چاہ سکتے ہیں جو آپ وصول کرنا چاہتے ہیں۔

آپ Pydantic کی model configuration استعمال کر کے کسی بھی `extra` fields کو `forbid` کر سکتے ہیں:

{* ../../docs_src/header_param_models/tutorial002_an_py310.py hl[10] *}

اگر کوئی client کچھ **اضافی headers** بھیجنے کی کوشش کرے، تو اسے ایک **error** response ملے گا۔

مثال کے طور پر، اگر client `tool` header کو `plumbus` کی قدر کے ساتھ بھیجنے کی کوشش کرے، تو اسے ایک **error** response ملے گا جو بتائے گا کہ header parameter `tool` کی اجازت نہیں ہے:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## Underscores کی تبدیلی بند کریں { #disable-convert-underscores }

عام header parameters کی طرح، جب آپ کے parameter ناموں میں underscore حروف ہوتے ہیں، تو وہ **خودکار طور پر hyphens میں تبدیل** ہو جاتے ہیں۔

مثال کے طور پر، اگر آپ کے code میں `save_data` نام کا header parameter ہے، تو متوقع HTTP header `save-data` ہوگا، اور docs میں بھی اسی طرح دکھایا جائے گا۔

اگر کسی وجہ سے آپ کو یہ خودکار تبدیلی بند کرنی ہو، تو آپ header parameters کے Pydantic models کے لیے بھی ایسا کر سکتے ہیں۔

{* ../../docs_src/header_param_models/tutorial003_an_py310.py hl[19] *}

/// warning | انتباہ

`convert_underscores` کو `False` پر سیٹ کرنے سے پہلے، یہ ذہن میں رکھیں کہ بعض HTTP proxies اور servers underscores والے headers کے استعمال کی اجازت نہیں دیتے۔

///

## خلاصہ { #summary }

آپ **Pydantic models** استعمال کر کے **FastAPI** میں **headers** declare کر سکتے ہیں۔ 😎
