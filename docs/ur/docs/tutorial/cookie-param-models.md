# Cookie Parameter Models { #cookie-parameter-models }

اگر آپ کے پاس ایک دوسرے سے متعلقہ **cookies** کا گروپ ہے، تو آپ انہیں declare کرنے کے لیے ایک **Pydantic model** بنا سکتے ہیں۔ 🍪

اس سے آپ کو **model کو کئی جگہوں پر دوبارہ استعمال** کرنے اور تمام parameters کے لیے validations اور metadata ایک ساتھ declare کرنے کی سہولت ملے گی۔ 😎

/// note | نوٹ

یہ FastAPI version `0.115.0` سے supported ہے۔ 🤓

///

/// tip | مشورہ

یہی تکنیک `Query`، `Cookie`، اور `Header` پر بھی لاگو ہوتی ہے۔ 😎

///

## Pydantic Model کے ساتھ Cookies { #cookies-with-a-pydantic-model }

وہ **cookie** parameters جو آپ کو درکار ہیں انہیں ایک **Pydantic model** میں declare کریں، اور پھر parameter کو `Cookie` کے طور پر declare کریں:

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI** request میں موصول ہونے والی **cookies** سے **ہر field** کا ڈیٹا **extract** کرے گا اور آپ کو وہ Pydantic model دے گا جو آپ نے define کیا ہے۔

## Docs چیک کریں { #check-the-docs }

آپ `/docs` پر docs UI میں defined cookies دیکھ سکتے ہیں:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// info | معلومات

یہ بات ذہن میں رکھیں کہ **browsers cookies** کو خاص طریقے سے اور پردے کے پیچھے handle کرتے ہیں، اور وہ **JavaScript** کو آسانی سے انہیں چھونے **نہیں** دیتے۔

اگر آپ `/docs` پر **API docs UI** میں جائیں تو آپ اپنی *path operations* کے لیے cookies کی **documentation** دیکھ سکیں گے۔

لیکن اگر آپ **ڈیٹا بھریں** اور "Execute" پر کلک کریں، تو چونکہ docs UI **JavaScript** کے ساتھ کام کرتا ہے، cookies بھیجی نہیں جائیں گی، اور آپ کو ایک **error** پیغام نظر آئے گا جیسے آپ نے کوئی قدر نہیں لکھی۔

///

## اضافی Cookies پر پابندی { #forbid-extra-cookies }

بعض خاص استعمال کے معاملات میں (شاید بہت عام نہیں)، آپ ان cookies کو **محدود** کرنا چاہ سکتے ہیں جو آپ وصول کرنا چاہتے ہیں۔

آپ کی API کے پاس اب اپنی <dfn title="This is a joke, just in case. It has nothing to do with cookie consents, but it's funny that even the API can now reject the poor cookies. Have a cookie. 🍪">cookie consent</dfn> کو کنٹرول کرنے کی طاقت ہے۔ 🤪🍪

آپ Pydantic کی model configuration استعمال کر کے کسی بھی `extra` fields کو `forbid` کر سکتے ہیں:

{* ../../docs_src/cookie_param_models/tutorial002_an_py310.py hl[10] *}

اگر کوئی client کچھ **اضافی cookies** بھیجنے کی کوشش کرے، تو اسے ایک **error** response ملے گا۔

بیچارے cookie banners جنہوں نے آپ کی رضامندی حاصل کرنے کی اتنی محنت کی تاکہ <dfn title="This is another joke. Don't pay attention to me. Have some coffee for your cookie. ☕">API اسے رد کر دے</dfn>۔ 🍪

مثال کے طور پر، اگر client `santa_tracker` cookie کو `good-list-please` کی قدر کے ساتھ بھیجنے کی کوشش کرے، تو client کو ایک **error** response ملے گا جو بتائے گا کہ `santa_tracker` <dfn title="Santa disapproves the lack of cookies. 🎅 Okay, no more cookie jokes.">cookie کی اجازت نہیں ہے</dfn>:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
```

## خلاصہ { #summary }

آپ **Pydantic models** استعمال کر کے **FastAPI** میں <dfn title="Have a last cookie before you go. 🍪">**cookies**</dfn> declare کر سکتے ہیں۔ 😎
