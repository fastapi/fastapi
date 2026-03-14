# Request Body { #request-body }

جب آپ کو client (مثلاً براؤزر) سے اپنی API کو ڈیٹا بھیجنا ہو، تو آپ اسے **request body** کے طور پر بھیجتے ہیں۔

**Request** body وہ ڈیٹا ہے جو client آپ کی API کو بھیجتا ہے۔ **Response** body وہ ڈیٹا ہے جو آپ کی API client کو بھیجتی ہے۔

آپ کی API کو تقریباً ہمیشہ **response** body بھیجنا ہوتا ہے۔ لیکن clients کو ہمیشہ **request bodies** بھیجنے کی ضرورت نہیں ہوتی، بعض اوقات وہ صرف ایک path request کرتے ہیں، شاید کچھ query parameters کے ساتھ، لیکن body نہیں بھیجتے۔

**Request** body کا اعلان کرنے کے لیے، آپ [Pydantic](https://docs.pydantic.dev/) models استعمال کرتے ہیں ان کی تمام طاقت اور فوائد کے ساتھ۔

/// info | معلومات

ڈیٹا بھیجنے کے لیے، آپ کو ان میں سے ایک استعمال کرنا چاہیے: `POST` (سب سے عام)، `PUT`، `DELETE` یا `PATCH`۔

`GET` request کے ساتھ body بھیجنا تصریحات میں غیر متعین رویہ رکھتا ہے، بہرحال، FastAPI اسے صرف بہت پیچیدہ/انتہائی استعمال کے معاملات کے لیے تعاون کرتا ہے۔

چونکہ اس کی حوصلہ شکنی کی جاتی ہے، Swagger UI کے ساتھ انٹرایکٹو docs `GET` استعمال کرتے وقت body کی دستاویزات نہیں دکھائیں گے، اور درمیان میں proxies شاید اسے تعاون نہ کریں۔

///

## Pydantic کا `BaseModel` import کریں { #import-pydantics-basemodel }

سب سے پہلے، آپ کو `pydantic` سے `BaseModel` import کرنا ہوگا:

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## اپنا ڈیٹا model بنائیں { #create-your-data-model }

پھر آپ اپنا ڈیٹا model ایک class کے طور پر اعلان کریں جو `BaseModel` سے وراثت حاصل کرے۔

تمام attributes کے لیے معیاری Python types استعمال کریں:

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}


Query parameters کا اعلان کرتے وقت جیسا ہوتا ہے، ویسے ہی جب model attribute کی طے شدہ قدر ہو، یہ لازمی نہیں ہوتا۔ ورنہ، یہ لازمی ہے۔ اسے محض اختیاری بنانے کے لیے `None` استعمال کریں۔

مثال کے طور پر، اوپر والا model ایک JSON "`object`" (یا Python `dict`) کا اعلان کرتا ہے جیسے:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...چونکہ `description` اور `tax` اختیاری ہیں (`None` کی طے شدہ قدر کے ساتھ)، یہ JSON "`object`" بھی درست ہوگا:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## اسے parameter کے طور پر اعلان کریں { #declare-it-as-a-parameter }

اسے اپنے *path operation* میں شامل کرنے کے لیے، اسے اسی طرح اعلان کریں جیسے آپ نے path اور query parameters کا اعلان کیا:

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

...اور اس کی قسم آپ کے بنائے ہوئے model، `Item` کے طور پر اعلان کریں۔

## نتائج { #results }

صرف اس Python type declaration کے ساتھ، **FastAPI** یہ کرے گا:

* Request کی body کو JSON کے طور پر پڑھے گا۔
* متعلقہ اقسام کو تبدیل کرے گا (اگر ضرورت ہو)۔
* ڈیٹا کی توثیق کرے گا۔
    * اگر ڈیٹا غلط ہے، تو یہ ایک اچھی اور واضح error واپس کرے گا، بالکل بتاتے ہوئے کہ غلط ڈیٹا کہاں اور کیا تھا۔
* آپ کو وصول شدہ ڈیٹا parameter `item` میں دے گا۔
    * چونکہ آپ نے function میں اسے `Item` قسم کا اعلان کیا ہے، آپ کو تمام attributes اور ان کی اقسام کے لیے ایڈیٹر سپورٹ (completion وغیرہ) بھی ملے گی۔
* آپ کے model کے لیے [JSON Schema](https://json-schema.org) تعریفات تیار کرے گا، آپ انہیں کہیں بھی استعمال کر سکتے ہیں اگر یہ آپ کے پراجیکٹ کے لیے مناسب ہو۔
* وہ schemas تیار کردہ OpenAPI schema کا حصہ ہوں گے، اور خودکار دستاویزاتی <abbr title="User Interfaces">UIs</abbr> کے ذریعے استعمال ہوں گے۔

## خودکار دستاویزات { #automatic-docs }

آپ کے models کے JSON Schemas آپ کے OpenAPI تیار کردہ schema کا حصہ ہوں گے، اور انٹرایکٹو API docs میں دکھائے جائیں گے:

<img src="/img/tutorial/body/image01.png">

اور ہر *path operation* کے اندر API docs میں بھی استعمال ہوں گے جنہیں ان کی ضرورت ہو:

<img src="/img/tutorial/body/image02.png">

## ایڈیٹر سپورٹ { #editor-support }

آپ کے ایڈیٹر میں، آپ کے function کے اندر آپ کو ہر جگہ type hints اور completion ملے گی (یہ نہیں ہوتا اگر آپ Pydantic model کی بجائے `dict` وصول کرتے):

<img src="/img/tutorial/body/image03.png">

آپ کو غلط type operations کے لیے error checks بھی ملتے ہیں:

<img src="/img/tutorial/body/image04.png">

یہ اتفاق سے نہیں ہے، پورا framework اسی ڈیزائن کے گرد بنایا گیا تھا۔

اور کسی بھی عملدرآمد سے پہلے، ڈیزائن مرحلے میں ہی اس کی مکمل جانچ کی گئی تھی، تاکہ یقینی بنایا جا سکے کہ یہ تمام ایڈیٹرز کے ساتھ کام کرے گا۔

یہاں تک کہ اس کی تعاون کے لیے خود Pydantic میں بھی کچھ تبدیلیاں کی گئیں۔

پچھلے screenshots [Visual Studio Code](https://code.visualstudio.com) سے لیے گئے تھے۔

لیکن آپ کو [PyCharm](https://www.jetbrains.com/pycharm/) اور زیادہ تر دوسرے Python ایڈیٹرز کے ساتھ بھی وہی ایڈیٹر سپورٹ ملے گی:

<img src="/img/tutorial/body/image05.png">

/// tip | مشورہ

اگر آپ [PyCharm](https://www.jetbrains.com/pycharm/) کو اپنے ایڈیٹر کے طور پر استعمال کرتے ہیں، تو آپ [Pydantic PyCharm Plugin](https://github.com/koxudaxi/pydantic-pycharm-plugin/) استعمال کر سکتے ہیں۔

یہ Pydantic models کے لیے ایڈیٹر سپورٹ بہتر کرتا ہے، اس کے ساتھ:

* auto-completion
* type checks
* refactoring
* تلاش
* inspections

///

## Model استعمال کریں { #use-the-model }

Function کے اندر، آپ model object کے تمام attributes تک براہ راست رسائی حاصل کر سکتے ہیں:

{* ../../docs_src/body/tutorial002_py310.py *}

## Request body + path parameters { #request-body-path-parameters }

آپ path parameters اور request body ایک ساتھ اعلان کر سکتے ہیں۔

**FastAPI** پہچان لے گا کہ وہ function parameters جو path parameters سے مماثل ہیں **path سے لیے جائیں**، اور وہ function parameters جو Pydantic models کے طور پر اعلان کیے گئے ہیں **request body سے لیے جائیں**۔

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}


## Request body + path + query parameters { #request-body-path-query-parameters }

آپ **body**، **path** اور **query** parameters سب ایک ساتھ بھی اعلان کر سکتے ہیں۔

**FastAPI** ہر ایک کو پہچان لے گا اور صحیح جگہ سے ڈیٹا لے گا۔

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

Function parameters کو اس طرح پہچانا جائے گا:

* اگر parameter **path** میں بھی اعلان کیا گیا ہے، تو اسے path parameter کے طور پر استعمال کیا جائے گا۔
* اگر parameter **واحد قسم** (جیسے `int`، `float`، `str`، `bool` وغیرہ) کا ہے تو اسے **query** parameter سمجھا جائے گا۔
* اگر parameter **Pydantic model** کی قسم کا اعلان کیا گیا ہے، تو اسے request **body** سمجھا جائے گا۔

/// note | نوٹ

FastAPI جان لے گا کہ `q` کی قدر لازمی نہیں ہے کیونکہ اس کی طے شدہ قدر `= None` ہے۔

`str | None` FastAPI کے ذریعے یہ تعین کرنے کے لیے استعمال نہیں ہوتا کہ قدر لازمی نہیں ہے، یہ جانتا ہے کہ لازمی نہیں ہے کیونکہ اس کی طے شدہ قدر `= None` ہے۔

لیکن type annotations شامل کرنے سے آپ کا ایڈیٹر آپ کو بہتر سپورٹ دے سکے گا اور errors کا پتہ لگا سکے گا۔

///

## Pydantic کے بغیر { #without-pydantic }

اگر آپ Pydantic models استعمال نہیں کرنا چاہتے، تو آپ **Body** parameters بھی استعمال کر سکتے ہیں۔ دستاویزات دیکھیں [Body - Multiple Parameters: Body میں واحد اقدار](body-multiple-params.md#singular-values-in-body)۔
