# Response Status Code { #response-status-code }

جس طرح آپ response model بیان کر سکتے ہیں، اسی طرح آپ کسی بھی *path operation* میں `status_code` parameter کے ساتھ response کے لیے استعمال ہونے والا HTTP status code بھی بیان کر سکتے ہیں:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* وغیرہ۔

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

/// note | نوٹ

نوٹ کریں کہ `status_code` "decorator" method (`get`، `post` وغیرہ) کا parameter ہے۔ آپ کے *path operation function* کا نہیں، جیسے کہ تمام parameters اور body ہیں۔

///

`status_code` parameter ایک نمبر وصول کرتا ہے جس میں HTTP status code ہوتا ہے۔

/// info | معلومات

`status_code` متبادل طور پر ایک `IntEnum` بھی قبول کر سکتا ہے، جیسے Python کا [`http.HTTPStatus`](https://docs.python.org/3/library/http.html#http.HTTPStatus)۔

///

یہ:

* Response میں وہ status code واپس کرے گا۔
* OpenAPI schema میں اسے اسی طرح document کرے گا (اور اس طرح، user interfaces میں بھی):

<img src="/img/tutorial/response-status-code/image01.png">

/// note | نوٹ

کچھ response codes (اگلا سیکشن دیکھیں) یہ ظاہر کرتے ہیں کہ response میں کوئی body نہیں ہے۔

FastAPI یہ جانتا ہے، اور OpenAPI docs تیار کرے گا جو بتائیں گے کہ response body نہیں ہے۔

///

## HTTP status codes کے بارے میں { #about-http-status-codes }

/// note | نوٹ

اگر آپ پہلے سے جانتے ہیں کہ HTTP status codes کیا ہیں تو اگلے سیکشن پر جائیں۔

///

HTTP میں، آپ response کے حصے کے طور پر 3 ہندسوں کا ایک عددی status code بھیجتے ہیں۔

ان status codes کا ایک نام ہوتا ہے جو انہیں پہچاننے کے لیے ہے، لیکن اہم حصہ نمبر ہے۔

مختصراً:

* `100 - 199` "معلومات" کے لیے ہیں۔ آپ انہیں شاذ و نادر ہی براہ راست استعمال کرتے ہیں۔ ان status codes والے responses میں body نہیں ہو سکتا۔
* **`200 - 299`** "کامیاب" responses کے لیے ہیں۔ آپ انہیں سب سے زیادہ استعمال کریں گے۔
    * `200` پہلے سے طے شدہ status code ہے، جس کا مطلب ہے سب کچھ "ٹھیک" تھا۔
    * ایک اور مثال `201`، "Created" ہے۔ یہ عام طور پر database میں نیا record بنانے کے بعد استعمال ہوتا ہے۔
    * ایک خاص صورت `204`، "No Content" ہے۔ یہ response تب استعمال ہوتا ہے جب client کو واپس کرنے کے لیے کوئی مواد نہ ہو، اس لیے response میں body نہیں ہونا چاہیے۔
* **`300 - 399`** "Redirection" کے لیے ہیں۔ ان status codes والے responses میں body ہو بھی سکتا ہے اور نہیں بھی، سوائے `304`، "Not Modified" کے، جس میں body نہیں ہونا چاہیے۔
* **`400 - 499`** "Client error" responses کے لیے ہیں۔ یہ دوسری قسم ہے جو آپ شاید سب سے زیادہ استعمال کریں گے۔
    * ایک مثال `404` ہے، "Not Found" response کے لیے۔
    * Client کی عمومی errors کے لیے آپ صرف `400` استعمال کر سکتے ہیں۔
* `500 - 599` server errors کے لیے ہیں۔ آپ تقریباً کبھی انہیں براہ راست استعمال نہیں کرتے۔ جب آپ کے application code یا server میں کسی حصے میں کچھ غلط ہو جاتا ہے تو یہ خودکار طور پر ان میں سے ایک status code واپس کرے گا۔

/// tip | مشورہ

ہر status code کے بارے میں مزید جاننے کے لیے اور کون سا code کس کے لیے ہے، [<abbr title="Mozilla Developer Network">MDN</abbr> documentation about HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) دیکھیں۔

///

## نام یاد رکھنے کا آسان طریقہ { #shortcut-to-remember-the-names }

آئیے پچھلی مثال دوبارہ دیکھتے ہیں:

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

`201` "Created" کا status code ہے۔

لیکن آپ کو ان میں سے ہر ایک code کا مطلب یاد رکھنے کی ضرورت نہیں۔

آپ `fastapi.status` سے آسان variables استعمال کر سکتے ہیں۔

{* ../../docs_src/response_status_code/tutorial002_py310.py hl[1,6] *}

یہ صرف ایک سہولت ہے، ان میں وہی نمبر ہے، لیکن اس طرح آپ انہیں تلاش کرنے کے لیے editor کا autocomplete استعمال کر سکتے ہیں:

<img src="/img/tutorial/response-status-code/image02.png">

/// note | تکنیکی تفصیلات

آپ `from starlette import status` بھی استعمال کر سکتے ہیں۔

**FastAPI** آپ کی سہولت کے لیے وہی `starlette.status` بطور `fastapi.status` فراہم کرتا ہے۔ لیکن یہ براہ راست Starlette سے آتا ہے۔

///

## پہلے سے طے شدہ کو تبدیل کرنا { #changing-the-default }

بعد میں، [Advanced User Guide](../advanced/response-change-status-code.md) میں، آپ دیکھیں گے کہ یہاں بیان کردہ پہلے سے طے شدہ status code سے مختلف status code کیسے واپس کیا جائے۔
