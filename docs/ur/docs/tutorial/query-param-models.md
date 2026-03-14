# Query Parameter Models { #query-parameter-models }

اگر آپ کے پاس ایک دوسرے سے متعلقہ **query parameters** کا گروپ ہے، تو آپ انہیں declare کرنے کے لیے ایک **Pydantic model** بنا سکتے ہیں۔

اس سے آپ کو **model کو کئی جگہوں پر دوبارہ استعمال** کرنے اور تمام parameters کے لیے validations اور metadata ایک ساتھ declare کرنے کی سہولت ملے گی۔ 😎

/// note | نوٹ

یہ FastAPI version `0.115.0` سے supported ہے۔ 🤓

///

## Pydantic Model کے ساتھ Query Parameters { #query-parameters-with-a-pydantic-model }

وہ **query parameters** جو آپ کو درکار ہیں انہیں ایک **Pydantic model** میں declare کریں، اور پھر parameter کو `Query` کے طور پر declare کریں:

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** request میں موجود **query parameters** سے **ہر field** کا ڈیٹا **extract** کرے گا اور آپ کو وہ Pydantic model دے گا جو آپ نے define کیا ہے۔

## Docs چیک کریں { #check-the-docs }

آپ `/docs` پر docs UI میں query parameters دیکھ سکتے ہیں:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## اضافی Query Parameters پر پابندی { #forbid-extra-query-parameters }

بعض خاص استعمال کے معاملات میں (شاید بہت عام نہیں)، آپ ان query parameters کو **محدود** کرنا چاہ سکتے ہیں جو آپ وصول کرنا چاہتے ہیں۔

آپ Pydantic کی model configuration استعمال کر کے کسی بھی `extra` fields کو `forbid` کر سکتے ہیں:

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

اگر کوئی client **query parameters** میں کچھ **اضافی** ڈیٹا بھیجنے کی کوشش کرے، تو اسے ایک **error** response ملے گا۔

مثال کے طور پر، اگر client `tool` query parameter کو `plumbus` کی قدر کے ساتھ بھیجنے کی کوشش کرے، جیسے:

```http
https://example.com/items/?limit=10&tool=plumbus
```

تو اسے ایک **error** response ملے گا جو بتائے گا کہ query parameter `tool` کی اجازت نہیں ہے:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## خلاصہ { #summary }

آپ **Pydantic models** استعمال کر کے **FastAPI** میں **query parameters** declare کر سکتے ہیں۔ 😎

/// tip | مشورہ

اسپائلر الرٹ: آپ Pydantic models کو cookies اور headers declare کرنے کے لیے بھی استعمال کر سکتے ہیں، لیکن اس کے بارے میں آپ tutorial میں آگے پڑھیں گے۔ 🤫

///
