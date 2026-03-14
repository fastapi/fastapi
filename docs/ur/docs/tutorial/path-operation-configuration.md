# Path Operation Configuration { #path-operation-configuration }

آپ اپنے *path operation decorator* کو configure کرنے کے لیے اس میں کئی parameters دے سکتے ہیں۔

/// warning | انتباہ

نوٹ کریں کہ یہ parameters براہ راست *path operation decorator* کو دیے جاتے ہیں، آپ کے *path operation function* کو نہیں۔

///

## Response Status Code { #response-status-code }

آپ اپنے *path operation* کے response میں استعمال ہونے والا (HTTP) `status_code` بیان کر سکتے ہیں۔

آپ براہ راست `int` code دے سکتے ہیں، جیسے `404`۔

لیکن اگر آپ کو یاد نہیں کہ ہر نمبر code کس لیے ہے تو آپ `status` میں شارٹ کٹ constants استعمال کر سکتے ہیں:

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

وہ status code response میں استعمال ہوگا اور OpenAPI schema میں شامل کیا جائے گا۔

/// note | تکنیکی تفصیلات

آپ `from starlette import status` بھی استعمال کر سکتے ہیں۔

**FastAPI** آپ کی سہولت کے لیے وہی `starlette.status` بطور `fastapi.status` فراہم کرتا ہے۔ لیکن یہ براہ راست Starlette سے آتا ہے۔

///

## Tags { #tags }

آپ اپنے *path operation* میں tags شامل کر سکتے ہیں، `tags` parameter میں `str` کی ایک `list` دیں (عام طور پر صرف ایک `str`):

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

یہ OpenAPI schema میں شامل کیے جائیں گے اور خودکار documentation interfaces میں استعمال ہوں گے:

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Enums کے ساتھ Tags { #tags-with-enums }

اگر آپ کی ایک بڑی application ہے تو آپ کے پاس **کئی tags** جمع ہو سکتے ہیں، اور آپ یقینی بنانا چاہیں گے کہ متعلقہ *path operations* کے لیے ہمیشہ **وہی tag** استعمال کریں۔

ان صورتوں میں، tags کو ایک `Enum` میں محفوظ کرنا مناسب ہو سکتا ہے۔

**FastAPI** اسے سادہ strings کی طرح ہی تعاون کرتا ہے:

{* ../../docs_src/path_operation_configuration/tutorial002b_py310.py hl[1,8:10,13,18] *}

## Summary اور description { #summary-and-description }

آپ `summary` اور `description` شامل کر سکتے ہیں:

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[17:18] *}

## Docstring سے Description { #description-from-docstring }

چونکہ descriptions طویل ہوتی ہیں اور متعدد سطروں پر پھیلی ہوتی ہیں، آپ *path operation* کی description function کے <dfn title="a multi-line string as the first expression inside a function (not assigned to any variable) used for documentation">docstring</dfn> میں بیان کر سکتے ہیں اور **FastAPI** اسے وہاں سے پڑھے گا۔

آپ docstring میں [Markdown](https://en.wikipedia.org/wiki/Markdown) لکھ سکتے ہیں، اسے صحیح طریقے سے سمجھا اور دکھایا جائے گا (docstring indentation کو مدنظر رکھتے ہوئے)۔

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

یہ interactive docs میں استعمال ہوگا:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## Response description { #response-description }

آپ `response_description` parameter کے ساتھ response کی description بیان کر سکتے ہیں:

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[18] *}

/// info | معلومات

نوٹ کریں کہ `response_description` خاص طور پر response سے متعلق ہے، `description` عمومی طور پر *path operation* سے متعلق ہے۔

///

/// check

OpenAPI بتاتا ہے کہ ہر *path operation* کے لیے response description ضروری ہے۔

تو اگر آپ کوئی فراہم نہیں کرتے تو **FastAPI** خودکار طور پر "Successful response" بنا دے گا۔

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## *path operation* کو Deprecate کریں { #deprecate-a-path-operation }

اگر آپ کو کسی *path operation* کو <dfn title="obsolete, recommended not to use it">deprecated</dfn> نشان زد کرنا ہو، لیکن اسے ہٹائے بغیر، تو `deprecated` parameter دیں:

{* ../../docs_src/path_operation_configuration/tutorial006_py310.py hl[16] *}

یہ interactive docs میں واضح طور پر deprecated نشان زد ہوگا:

<img src="/img/tutorial/path-operation-configuration/image04.png">

دیکھیں کہ deprecated اور غیر deprecated *path operations* کیسے نظر آتے ہیں:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## خلاصہ { #recap }

آپ *path operation decorators* میں parameters دے کر آسانی سے اپنے *path operations* کے لیے metadata configure اور شامل کر سکتے ہیں۔
