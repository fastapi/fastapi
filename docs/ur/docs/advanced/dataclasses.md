# Dataclasses کا استعمال { #using-dataclasses }

FastAPI **Pydantic** کے اوپر بنایا گیا ہے، اور میں آپ کو دکھاتا رہا ہوں کہ requests اور responses بیان کرنے کے لیے Pydantic models کیسے استعمال کریں۔

لیکن FastAPI [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) استعمال کرنے کی بھی اسی طرح سپورٹ کرتا ہے:

{* ../../docs_src/dataclasses_/tutorial001_py310.py hl[1,6:11,18:19] *}

یہ **Pydantic** کی بدولت اب بھی سپورٹ ہے، کیونکہ اس میں [`dataclasses` کی اندرونی سپورٹ](https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel) موجود ہے۔

تو، اوپر والے کوڈ میں بھی جو واضح طور پر Pydantic استعمال نہیں کرتا، FastAPI ان معیاری dataclasses کو Pydantic کے اپنے مخصوص dataclasses میں تبدیل کرنے کے لیے Pydantic استعمال کر رہا ہے۔

اور یقیناً، یہ وہی سب سپورٹ کرتا ہے:

* ڈیٹا validation
* ڈیٹا serialization
* ڈیٹا دستاویزات، وغیرہ۔

یہ Pydantic models کی طرح ہی کام کرتا ہے۔ اور یہ دراصل اندرونی طور پر اسی طرح حاصل کیا جاتا ہے، Pydantic استعمال کرتے ہوئے۔

/// info | معلومات

یاد رکھیں کہ dataclasses وہ سب کچھ نہیں کر سکتیں جو Pydantic models کر سکتے ہیں۔

تو، آپ کو پھر بھی Pydantic models استعمال کرنے کی ضرورت پڑ سکتی ہے۔

لیکن اگر آپ کے پاس بہت سی dataclasses پڑی ہیں تو FastAPI استعمال کر کے web API بنانے کے لیے انہیں استعمال کرنا ایک اچھی تدبیر ہے۔

///

## `response_model` میں Dataclasses { #dataclasses-in-response-model }

آپ `response_model` parameter میں بھی `dataclasses` استعمال کر سکتے ہیں:

{* ../../docs_src/dataclasses_/tutorial002_py310.py hl[1,6:12,18] *}

dataclass خود بخود Pydantic dataclass میں تبدیل ہو جائے گی۔

اس طرح، اس کا schema API docs user interface میں نظر آئے گا:

<img src="/img/tutorial/dataclasses/image01.png">

## نیسٹڈ ڈیٹا ڈھانچوں میں Dataclasses { #dataclasses-in-nested-data-structures }

آپ `dataclasses` کو دوسری type annotations کے ساتھ ملا کر نیسٹڈ ڈیٹا ڈھانچے بنا سکتے ہیں۔

بعض صورتوں میں، آپ کو پھر بھی Pydantic کے ورژن کی `dataclasses` استعمال کرنی ہو سکتی ہیں۔ مثال کے طور پر، اگر خود بخود بنائی گئی API دستاویزات میں غلطیاں ہوں۔

اس صورت میں، آپ معیاری `dataclasses` کو `pydantic.dataclasses` سے بدل سکتے ہیں، جو ایک متبادل ہے:

{* ../../docs_src/dataclasses_/tutorial003_py310.py hl[1,4,7:10,13:16,22:24,27] *}

1. ہم پھر بھی معیاری `dataclasses` سے `field` import کرتے ہیں۔

2. `pydantic.dataclasses` `dataclasses` کا متبادل ہے۔

3. `Author` dataclass میں `Item` dataclasses کی فہرست شامل ہے۔

4. `Author` dataclass `response_model` parameter کے طور پر استعمال ہوتی ہے۔

5. آپ dataclasses کے ساتھ دیگر معیاری type annotations کو request body کے طور پر استعمال کر سکتے ہیں۔

    اس صورت میں، یہ `Item` dataclasses کی فہرست ہے۔

6. یہاں ہم dictionary واپس کر رہے ہیں جس میں `items` ہے جو dataclasses کی فہرست ہے۔

    FastAPI پھر بھی ڈیٹا کو JSON میں <dfn title="ڈیٹا کو ایسی شکل میں تبدیل کرنا جو منتقل کی جا سکے">serialize</dfn> کرنے کے قابل ہے۔

7. یہاں `response_model` `Author` dataclasses کی فہرست کی type annotation استعمال کر رہا ہے۔

    دوبارہ، آپ `dataclasses` کو معیاری type annotations کے ساتھ ملا سکتے ہیں۔

8. غور کریں کہ یہ *path operation function* `async def` کی بجائے عام `def` استعمال کرتا ہے۔

    ہمیشہ کی طرح، FastAPI میں آپ `def` اور `async def` کو ضرورت کے مطابق ملا سکتے ہیں۔

    اگر آپ کو یاد دہانی چاہیے کہ کب کون سا استعمال کریں، تو [`async` اور `await`](../async.md#in-a-hurry) کی دستاویزات میں _"جلدی میں ہیں؟"_ سیکشن دیکھیں۔

9. یہ *path operation function* dataclasses واپس نہیں کر رہا (حالانکہ کر سکتا ہے)، بلکہ اندرونی ڈیٹا کے ساتھ dictionaries کی فہرست واپس کر رہا ہے۔

    FastAPI `response_model` parameter (جس میں dataclasses شامل ہیں) استعمال کرکے response تبدیل کرے گا۔

آپ `dataclasses` کو دیگر type annotations کے ساتھ بہت سے مختلف مجموعوں میں ملا کر پیچیدہ ڈیٹا ڈھانچے بنا سکتے ہیں۔

مزید مخصوص تفصیلات دیکھنے کے لیے اوپر کوڈ میں موجود annotation مشورے دیکھیں۔

## مزید جانیں { #learn-more }

آپ `dataclasses` کو دیگر Pydantic models کے ساتھ بھی ملا سکتے ہیں، ان سے inherit کر سکتے ہیں، انہیں اپنے models میں شامل کر سکتے ہیں، وغیرہ۔

مزید جاننے کے لیے، [dataclasses کے بارے میں Pydantic دستاویزات](https://docs.pydantic.dev/latest/concepts/dataclasses/) دیکھیں۔

## ورژن { #version }

یہ FastAPI ورژن `0.67.0` سے دستیاب ہے۔
