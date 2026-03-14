# مشروط OpenAPI { #conditional-openapi }

اگر آپ کو ضرورت ہو، تو آپ settings اور environment variables استعمال کر کے ماحول کے مطابق OpenAPI کو مشروط طور پر ترتیب دے سکتے ہیں، اور یہاں تک کہ اسے مکمل طور پر غیر فعال بھی کر سکتے ہیں۔

## سیکیورٹی، APIs، اور docs کے بارے میں { #about-security-apis-and-docs }

اپنے documentation user interfaces کو production میں چھپانا آپ کی API کو محفوظ کرنے کا *صحیح طریقہ نہیں* ہونا چاہیے۔

یہ آپ کی API میں کوئی اضافی سیکیورٹی نہیں جوڑتا، *path operations* اب بھی وہیں دستیاب رہیں گی جہاں وہ ہیں۔

اگر آپ کے کوڈ میں کوئی سیکیورٹی خامی ہے، تو وہ پھر بھی موجود رہے گی۔

Documentation چھپانا صرف آپ کی API کے ساتھ تعامل کو سمجھنا مشکل بنا دیتا ہے، اور production میں اسے debug کرنا بھی مشکل ہو سکتا ہے۔ اسے سادہ طور پر [Security through obscurity](https://en.wikipedia.org/wiki/Security_through_obscurity) کی ایک شکل سمجھا جا سکتا ہے۔

اگر آپ اپنی API کو محفوظ کرنا چاہتے ہیں، تو کئی بہتر چیزیں ہیں جو آپ کر سکتے ہیں، مثال کے طور پر:

* یقینی بنائیں کہ آپ کے request bodies اور responses کے لیے اچھی طرح سے defined Pydantic models ہیں۔
* Dependencies استعمال کر کے تمام مطلوبہ permissions اور roles ترتیب دیں۔
* کبھی بھی سادہ متن میں passwords ذخیرہ نہ کریں، صرف password hashes ذخیرہ کریں۔
* معروف cryptographic ٹولز استعمال کریں اور لاگو کریں، جیسے pwdlib اور JWT tokens وغیرہ۔
* جہاں ضرورت ہو OAuth2 scopes کے ساتھ مزید تفصیلی permission controls شامل کریں۔
* ...وغیرہ۔

بہرحال، آپ کا کوئی بہت مخصوص استعمال کا معاملہ ہو سکتا ہے جہاں آپ کو واقعی کسی ماحول (مثلاً production) کے لیے یا environment variables کی ترتیبات کے مطابق API docs کو غیر فعال کرنا ہو۔

## Settings اور env vars سے مشروط OpenAPI { #conditional-openapi-from-settings-and-env-vars }

آپ آسانی سے وہی Pydantic settings استعمال کر سکتے ہیں اپنے تیار کردہ OpenAPI اور docs UIs کو ترتیب دینے کے لیے۔

مثال کے طور پر:

{* ../../docs_src/conditional_openapi/tutorial001_py310.py hl[6,11] *}

یہاں ہم `openapi_url` setting کو `"/openapi.json"` کی اسی default قدر کے ساتھ declare کرتے ہیں۔

اور پھر ہم اسے `FastAPI` app بناتے وقت استعمال کرتے ہیں۔

پھر آپ `OPENAPI_URL` environment variable کو خالی string پر سیٹ کر کے OpenAPI (بشمول UI docs) کو غیر فعال کر سکتے ہیں، اس طرح:

<div class="termy">

```console
$ OPENAPI_URL= uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

پھر اگر آپ `/openapi.json`، `/docs`، یا `/redoc` کے URLs پر جائیں تو آپ کو صرف `404 Not Found` error ملے گا جیسے:

```JSON
{
    "detail": "Not Found"
}
```
