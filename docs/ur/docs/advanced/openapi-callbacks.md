# OpenAPI Callbacks { #openapi-callbacks }

آپ ایک ایسا API بنا سکتے ہیں جس میں *path operation* کسی *بیرونی API* کو request بھیجنے کا عمل شروع کرے جو کسی اور نے بنایا ہو (شاید وہی ڈویلپر جو آپ کا API *استعمال* کر رہا ہو)۔

جب آپ کا API ایپ *بیرونی API* کو کال کرتا ہے تو اس عمل کو "callback" کہتے ہیں۔ کیونکہ بیرونی ڈویلپر کا سافٹ ویئر آپ کے API کو request بھیجتا ہے اور پھر آپ کا API *واپس کال کرتا ہے*، *بیرونی API* کو request بھیج کر (جو شاید اسی ڈویلپر نے بنایا ہو)۔

اس صورت میں، آپ یہ دستاویز کرنا چاہیں گے کہ وہ بیرونی API *کیسا* ہونا چاہیے۔ اس کی *path operation* کیا ہونی چاہیے، اسے کیا body توقع کرنا چاہیے، کیا response واپس کرنا چاہیے، وغیرہ۔

## Callbacks والی ایپ { #an-app-with-callbacks }

آئیے یہ سب ایک مثال سے دیکھتے ہیں۔

فرض کریں آپ ایک ایسی ایپ بناتے ہیں جو invoices بنانے کی اجازت دیتی ہے۔

ان invoices میں `id`، `title` (اختیاری)، `customer`، اور `total` ہوگا۔

آپ کے API کا صارف (بیرونی ڈویلپر) آپ کے API میں POST request کے ساتھ invoice بنائے گا۔

پھر آپ کا API (فرض کریں):

* بیرونی ڈویلپر کے کسی کسٹمر کو invoice بھیجے گا۔
* رقم وصول کرے گا۔
* API صارف (بیرونی ڈویلپر) کو واپس اطلاع بھیجے گا۔
    * یہ (*آپ کے API* سے) بیرونی ڈویلپر کی فراہم کردہ *بیرونی API* کو POST request بھیج کر کیا جائے گا (یہ "callback" ہے)۔

## عام **FastAPI** ایپ { #the-normal-fastapi-app }

آئیے پہلے دیکھیں کہ callback شامل کرنے سے پہلے عام API ایپ کیسی ہوگی۔

اس میں ایک *path operation* ہوگی جو `Invoice` body وصول کرے گی، اور ایک query parameter `callback_url` جس میں callback کا URL ہوگا۔

یہ حصہ کافی عام ہے، زیادہ تر کوڈ شاید آپ کو پہلے سے مانوس ہوگا:

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[7:11,34:51] *}

/// tip | مشورہ

`callback_url` query parameter Pydantic [Url](https://docs.pydantic.dev/latest/api/networks/) قسم استعمال کرتا ہے۔

///

واحد نئی چیز `callbacks=invoices_callback_router.routes` ہے بطور *path operation decorator* کے argument۔ ہم اگلے حصے میں دیکھیں گے کہ یہ کیا ہے۔

## Callback کی دستاویزات { #documenting-the-callback }

اصل callback کوڈ آپ کی اپنی API ایپ پر بہت زیادہ منحصر ہوگا۔

اور یہ شاید ایک ایپ سے دوسری تک بہت مختلف ہوگا۔

یہ صرف ایک یا دو لائنیں کوڈ ہو سکتی ہیں، جیسے:

```Python
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

لیکن شاید callback کا سب سے اہم حصہ یہ یقینی بنانا ہے کہ آپ کے API صارف (بیرونی ڈویلپر) *بیرونی API* کو درست طریقے سے بنائیں، اس ڈیٹا کے مطابق جو *آپ کا API* callback کی request body میں بھیجے گا، وغیرہ۔

تو، اگلا ہم وہ کوڈ شامل کریں گے جو دستاویز کرے کہ وہ *بیرونی API* *آپ کے API* سے callback وصول کرنے کے لیے کیسی ہونی چاہیے۔

وہ دستاویزات آپ کے API میں `/docs` پر Swagger UI میں نظر آئیں گی، اور بیرونی ڈویلپرز کو بتائیں گی کہ *بیرونی API* کیسے بنائیں۔

یہ مثال خود callback لاگو نہیں کرتی (وہ صرف کوڈ کی ایک لائن ہو سکتا ہے)، صرف دستاویزات والا حصہ۔

/// tip | مشورہ

اصل callback صرف ایک HTTP request ہے۔

خود callback لاگو کرتے وقت، آپ [HTTPX](https://www.python-httpx.org) یا [Requests](https://requests.readthedocs.io/) جیسی کوئی چیز استعمال کر سکتے ہیں۔

///

## Callback دستاویزات کا کوڈ لکھیں { #write-the-callback-documentation-code }

یہ کوڈ آپ کی ایپ میں عمل میں نہیں آئے گا، ہمیں اس کی صرف اس *بیرونی API* کی دستاویزات کے لیے ضرورت ہے۔

لیکن، آپ پہلے سے جانتے ہیں کہ **FastAPI** کے ساتھ API کے لیے خودکار دستاویزات آسانی سے کیسے بنائیں۔

تو ہم اسی علم کو استعمال کرتے ہوئے دستاویز کریں گے کہ *بیرونی API* کیسی ہونی چاہیے... وہ *path operation(s)* بنا کر جو بیرونی API کو لاگو کرنی چاہییں (جنہیں آپ کا API کال کرے گا)۔

/// tip | مشورہ

callback کی دستاویزات کا کوڈ لکھتے وقت، یہ تصور کرنا مفید ہو سکتا ہے کہ آپ وہ *بیرونی ڈویلپر* ہیں۔ اور آپ اس وقت *بیرونی API* لاگو کر رہے ہیں، نہ کہ *آپ کا API*۔

عارضی طور پر یہ نقطہ نظر (*بیرونی ڈویلپر* کا) اپنانے سے آپ کو یہ زیادہ واضح محسوس ہو سکتا ہے کہ اس *بیرونی API* کے لیے parameters، Pydantic model body کے لیے، response کے لیے، وغیرہ کہاں رکھیں۔

///

### Callback `APIRouter` بنائیں { #create-a-callback-apirouter }

سب سے پہلے ایک نیا `APIRouter` بنائیں جس میں ایک یا زیادہ callbacks ہوں۔

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[1,23] *}

### Callback *path operation* بنائیں { #create-the-callback-path-operation }

callback *path operation* بنانے کے لیے اوپر بنایا گیا وہی `APIRouter` استعمال کریں۔

یہ عام FastAPI *path operation* جیسا ہی ہونا چاہیے:

* اس میں شاید body کی بیان ہونی چاہیے جو اسے وصول کرنا ہے، مثلاً `body: InvoiceEvent`۔
* اور اس میں response کی بیان بھی ہو سکتی ہے جو اسے واپس کرنا چاہیے، مثلاً `response_model=InvoiceEventReceived`۔

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[14:16,19:20,26:30] *}

عام *path operation* سے 2 اہم فرق ہیں:

* اس میں کوئی اصل کوڈ ہونے کی ضرورت نہیں، کیونکہ آپ کی ایپ کبھی یہ کوڈ نہیں بلائے گی۔ یہ صرف *بیرونی API* کی دستاویزات کے لیے استعمال ہوتا ہے۔ تو، function میں صرف `pass` ہو سکتا ہے۔
* *path* میں [OpenAPI 3 expression](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression) ہو سکتا ہے (نیچے مزید دیکھیں) جہاں یہ *آپ کے API* کو بھیجی گئی اصل request کے parameters اور حصوں سے variables استعمال کر سکتا ہے۔

### Callback path expression { #the-callback-path-expression }

callback *path* میں [OpenAPI 3 expression](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression) ہو سکتا ہے جس میں *آپ کے API* کو بھیجی گئی اصل request کے حصے شامل ہوں۔

اس صورت میں، یہ `str` ہے:

```Python
"{$callback_url}/invoices/{$request.body.id}"
```

تو، اگر آپ کے API کا صارف (بیرونی ڈویلپر) *آپ کے API* کو اس پر request بھیجے:

```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

JSON body کے ساتھ:

```JSON
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

تو پھر *آپ کا API* invoice پروسیس کرے گا، اور کچھ وقت بعد، callback request `callback_url` (وہ *بیرونی API*) کو بھیجے گا:

```
https://www.external.org/events/invoices/2expen51ve
```

JSON body کے ساتھ جس میں کچھ ایسا ہوگا:

```JSON
{
    "description": "Payment celebration",
    "paid": true
}
```

اور یہ اس *بیرونی API* سے JSON body کے ساتھ اس طرح کا response توقع کرے گا:

```JSON
{
    "ok": true
}
```

/// tip | مشورہ

غور کریں کہ callback URL میں query parameter `callback_url` میں وصول شدہ URL (`https://www.external.org/events`) اور JSON body کے اندر سے invoice `id` (`2expen51ve`) دونوں شامل ہیں۔

///

### Callback router شامل کریں { #add-the-callback-router }

اس مقام پر آپ کے پاس اوپر بنائے گئے callback router میں ضروری *callback path operation(s)* موجود ہیں (جو *بیرونی ڈویلپر* کو *بیرونی API* میں لاگو کرنی چاہییں)۔

اب *آپ کے API کے path operation decorator* میں `callbacks` parameter استعمال کریں اور اس callback router سے attribute `.routes` (جو دراصل routes/*path operations* کی `list` ہے) پاس کریں:

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[33] *}

/// tip | مشورہ

غور کریں کہ آپ خود router (`invoices_callback_router`) کو `callback=` میں پاس نہیں کر رہے، بلکہ attribute `.routes`، یعنی `invoices_callback_router.routes` پاس کر رہے ہیں۔

///

### Docs چیک کریں { #check-the-docs }

اب آپ اپنی ایپ شروع کر سکتے ہیں اور [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) پر جائیں۔

آپ کو اپنے docs میں اپنی *path operation* کے لیے "Callbacks" سیکشن نظر آئے گا جو دکھائے گا کہ *بیرونی API* کیسی ہونی چاہیے:

<img src="/img/tutorial/openapi-callbacks/image01.png">
