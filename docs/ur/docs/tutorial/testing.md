# Testing { #testing }

[Starlette](https://www.starlette.dev/testclient/) کی بدولت، **FastAPI** applications کی testing آسان اور خوشگوار ہے۔

یہ [HTTPX](https://www.python-httpx.org) پر مبنی ہے، جو بدلے میں Requests کی بنیاد پر ڈیزائن کیا گیا ہے، تو یہ بہت مانوس اور بدیہی ہے۔

اس کے ساتھ، آپ [pytest](https://docs.pytest.org/) کو براہ راست **FastAPI** کے ساتھ استعمال کر سکتے ہیں۔

## `TestClient` استعمال کرنا { #using-testclient }

/// info | معلومات

`TestClient` استعمال کرنے کے لیے، پہلے [`httpx`](https://www.python-httpx.org) انسٹال کریں۔

یقینی بنائیں کہ آپ نے [virtual environment](../virtual-environments.md) بنایا ہے، اسے فعال کیا ہے، اور پھر اسے انسٹال کریں، مثال کے طور پر:

```console
$ pip install httpx
```

///

`TestClient` import کریں۔

اپنی **FastAPI** application کو اس میں منتقل کرتے ہوئے ایک `TestClient` بنائیں۔

`test_` سے شروع ہونے والے نام کے ساتھ functions بنائیں (یہ `pytest` کا معیاری طریقہ ہے)۔

`TestClient` object کو بالکل اسی طرح استعمال کریں جیسے آپ `httpx` استعمال کرتے ہیں۔

جن چیزوں کو چیک کرنا ہے ان کے لیے معیاری Python expressions کے ساتھ سادہ `assert` statements لکھیں (پھر سے، معیاری `pytest`)۔

{* ../../docs_src/app_testing/tutorial001_py310.py hl[2,12,15:18] *}

/// tip | مشورہ

دیکھیں کہ testing functions عام `def` ہیں، `async def` نہیں۔

اور client کی calls بھی عام calls ہیں، `await` استعمال نہیں کر رہیں۔

یہ آپ کو بغیر کسی پیچیدگی کے `pytest` براہ راست استعمال کرنے دیتا ہے۔

///

/// note | تکنیکی تفصیلات

آپ `from starlette.testclient import TestClient` بھی استعمال کر سکتے ہیں۔

**FastAPI** آپ کی سہولت کے لیے وہی `starlette.testclient` بطور `fastapi.testclient` فراہم کرتا ہے۔ لیکن یہ براہ راست Starlette سے آتا ہے۔

///

/// tip | مشورہ

اگر آپ اپنے tests میں FastAPI application کو requests بھیجنے کے علاوہ `async` functions call کرنا چاہتے ہیں (مثلاً asynchronous database functions)، تو advanced tutorial میں [Async Tests](../advanced/async-tests.md) دیکھیں۔

///

## Tests کو الگ کرنا { #separating-tests }

حقیقی application میں، آپ شاید اپنے tests ایک مختلف فائل میں رکھیں گے۔

اور آپ کی **FastAPI** application بھی کئی فائلوں/modules وغیرہ پر مشتمل ہو سکتی ہے۔

### **FastAPI** app فائل { #fastapi-app-file }

فرض کریں آپ کے پاس [Bigger Applications](bigger-applications.md) میں بیان کردہ فائل ساخت ہے:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

فائل `main.py` میں آپ کی **FastAPI** app ہے:

{* ../../docs_src/app_testing/app_a_py310/main.py *}

### Testing فائل { #testing-file }

پھر آپ کے پاس اپنے tests کے ساتھ ایک `test_main.py` فائل ہو سکتی ہے۔ یہ اسی Python package میں رہ سکتی ہے (وہی directory جس میں `__init__.py` فائل ہو):

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

چونکہ یہ فائل اسی package میں ہے، آپ `main` module (`main.py`) سے object `app` import کرنے کے لیے relative imports استعمال کر سکتے ہیں:

{* ../../docs_src/app_testing/app_a_py310/test_main.py hl[3] *}

...اور tests کا code پہلے کی طرح ہی ہوگا۔

## Testing: توسیعی مثال { #testing-extended-example }

اب آئیں اس مثال کو بڑھائیں اور مختلف حصوں کو test کرنے کا طریقہ دیکھنے کے لیے مزید تفصیلات شامل کریں۔

### توسیعی **FastAPI** app فائل { #extended-fastapi-app-file }

آئیں پہلے جیسی فائل ساخت جاری رکھتے ہیں:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

فرض کریں اب فائل `main.py` آپ کی **FastAPI** app کے ساتھ کچھ اور **path operations** رکھتی ہے۔

اس میں ایک `GET` operation ہے جو error واپس کر سکتا ہے۔

اس میں ایک `POST` operation ہے جو کئی errors واپس کر سکتا ہے۔

دونوں *path operations* کو ایک `X-Token` header درکار ہے۔

{* ../../docs_src/app_testing/app_b_an_py310/main.py *}

### توسیعی testing فائل { #extended-testing-file }

پھر آپ توسیعی tests کے ساتھ `test_main.py` اپ ڈیٹ کر سکتے ہیں:

{* ../../docs_src/app_testing/app_b_an_py310/test_main.py *}

جب بھی آپ کو client کی request میں معلومات منتقل کرنے کی ضرورت ہو اور آپ نہیں جانتے کہ کیسے، تو آپ (Google پر) تلاش کر سکتے ہیں کہ `httpx` میں یہ کیسے کیا جاتا ہے، یا `requests` میں بھی، کیونکہ HTTPX کا ڈیزائن Requests کے ڈیزائن پر مبنی ہے۔

پھر آپ اپنے tests میں بالکل وہی کریں۔

مثلاً:

* *path* یا *query* parameter منتقل کرنے کے لیے، اسے خود URL میں شامل کریں۔
* JSON body منتقل کرنے کے لیے، ایک Python object (مثلاً `dict`) `json` parameter میں دیں۔
* JSON کی بجائے اگر آپ کو *Form Data* بھیجنا ہے تو `data` parameter استعمال کریں۔
* *headers* منتقل کرنے کے لیے، `headers` parameter میں `dict` استعمال کریں۔
* *cookies* کے لیے، `cookies` parameter میں `dict`۔

Backend کو data منتقل کرنے کے بارے میں مزید معلومات (`httpx` یا `TestClient` استعمال کرتے ہوئے) کے لیے [HTTPX دستاویزات](https://www.python-httpx.org) دیکھیں۔

/// info | معلومات

نوٹ کریں کہ `TestClient` ایسا data وصول کرتا ہے جسے JSON میں تبدیل کیا جا سکے، Pydantic models نہیں۔

اگر آپ کے test میں Pydantic model ہے اور آپ testing کے دوران اس کا data application کو بھیجنا چاہتے ہیں، تو آپ [JSON Compatible Encoder](encoder.md) میں بیان کردہ `jsonable_encoder` استعمال کر سکتے ہیں۔

///

## اسے چلائیں { #run-it }

اس کے بعد، آپ کو صرف `pytest` انسٹال کرنا ہے۔

یقینی بنائیں کہ آپ نے [virtual environment](../virtual-environments.md) بنایا ہے، اسے فعال کیا ہے، اور پھر اسے انسٹال کریں، مثال کے طور پر:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

یہ خودکار طور پر فائلیں اور tests تلاش کرے گا، انہیں execute کرے گا، اور نتائج آپ کو بتائے گا۔

Tests اس طرح چلائیں:

<div class="termy">

```console
$ pytest

================ test session starts ================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/user/code/superawesome-cli/app
plugins: forked-1.1.3, xdist-1.31.0, cov-2.8.1
collected 6 items

---> 100%

test_main.py <span style="color: green; white-space: pre;">......                            [100%]</span>

<span style="color: green;">================= 1 passed in 0.03s =================</span>
```

</div>
