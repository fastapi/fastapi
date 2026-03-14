# Form Models { #form-models }

آپ FastAPI میں **form fields** بیان کرنے کے لیے **Pydantic models** استعمال کر سکتے ہیں۔

/// info

Forms استعمال کرنے کے لیے پہلے [`python-multipart`](https://github.com/Kludex/python-multipart) انسٹال کریں۔

یقینی بنائیں کہ آپ ایک [virtual environment](../virtual-environments.md) بنائیں، اسے فعال کریں، اور پھر اسے انسٹال کریں، مثال کے طور پر:

```console
$ pip install python-multipart
```

///

/// note | نوٹ

یہ FastAPI version `0.113.0` سے تعاون یافتہ ہے۔ 🤓

///

## Forms کے لیے Pydantic Models { #pydantic-models-for-forms }

آپ کو صرف ایک **Pydantic model** بنانا ہوگا جس میں وہ fields ہوں جو آپ **form fields** کے طور پر وصول کرنا چاہتے ہیں، اور پھر parameter کو `Form` کے طور پر بیان کریں:

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI** request میں موجود **form data** سے **ہر field** کا data **نکالے** گا اور آپ کو آپ کا بیان کردہ Pydantic model دے گا۔

## Docs چیک کریں { #check-the-docs }

آپ `/docs` پر docs UI میں اس کی تصدیق کر سکتے ہیں:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## اضافی Form Fields پر پابندی لگائیں { #forbid-extra-form-fields }

کچھ خاص صورتوں میں (جو شاید عام نہیں ہیں)، آپ form fields کو صرف Pydantic model میں بیان کردہ fields تک **محدود** رکھنا چاہیں گے۔ اور کسی بھی **اضافی** fields کو **منع** کرنا چاہیں گے۔

/// note | نوٹ

یہ FastAPI version `0.114.0` سے تعاون یافتہ ہے۔ 🤓

///

آپ Pydantic کی model configuration استعمال کر کے کسی بھی `extra` fields کو `forbid` کر سکتے ہیں:

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

اگر کوئی client اضافی data بھیجنے کی کوشش کرے تو اسے **error** response ملے گا۔

مثال کے طور پر، اگر client یہ form fields بھیجنے کی کوشش کرے:

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

تو اسے ایک error response ملے گا جو بتائے گا کہ field `extra` کی اجازت نہیں ہے:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## خلاصہ { #summary }

آپ FastAPI میں form fields بیان کرنے کے لیے Pydantic models استعمال کر سکتے ہیں۔ 😎
