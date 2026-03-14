# Async Tests { #async-tests }

آپ پہلے ہی دیکھ چکے ہیں کہ فراہم کیے گئے `TestClient` کا استعمال کرتے ہوئے اپنی **FastAPI** ایپلیکیشنز کی جانچ کیسے کی جائے۔ اب تک آپ نے صرف synchronous ٹیسٹ لکھنا دیکھا ہے، بغیر `async` functions کے استعمال کے۔

اپنے ٹیسٹوں میں asynchronous functions استعمال کر سکنا مفید ہو سکتا ہے، مثال کے طور پر، جب آپ اپنے database سے asynchronously query کر رہے ہوں۔ تصور کریں کہ آپ اپنی FastAPI ایپلیکیشن کو requests بھیجنا چاہتے ہیں اور پھر تصدیق کرنا چاہتے ہیں کہ آپ کے backend نے database میں درست ڈیٹا لکھا ہے، ایک async database library استعمال کرتے ہوئے۔

آئیے دیکھتے ہیں کہ ہم یہ کیسے کر سکتے ہیں۔

## pytest.mark.anyio { #pytest-mark-anyio }

اگر ہم اپنے ٹیسٹوں میں asynchronous functions call کرنا چاہتے ہیں، تو ہمارے test functions کو asynchronous ہونا ہوگا۔ AnyIO اس کے لیے ایک عمدہ plugin فراہم کرتا ہے، جو ہمیں یہ بتانے دیتا ہے کہ کچھ test functions asynchronously call کیے جائیں۔

## HTTPX { #httpx }

اگر آپ کی **FastAPI** ایپلیکیشن `async def` کی بجائے عام `def` functions استعمال کرتی ہے، تب بھی یہ اندرونی طور پر ایک `async` ایپلیکیشن ہے۔

`TestClient` اندرونی طور پر کچھ خاص عمل کرتا ہے تاکہ آپ کے عام `def` test functions میں asynchronous FastAPI ایپلیکیشن کو call کیا جا سکے، معیاری pytest استعمال کرتے ہوئے۔ لیکن وہ خاص عمل asynchronous functions کے اندر استعمال ہونے پر مزید کام نہیں کرتا۔ اپنے ٹیسٹ asynchronously چلانے سے، ہم اپنے test functions کے اندر `TestClient` مزید استعمال نہیں کر سکتے۔

`TestClient` [HTTPX](https://www.python-httpx.org) پر مبنی ہے، اور خوش قسمتی سے، ہم اسے براہ راست API کی جانچ کے لیے استعمال کر سکتے ہیں۔

## مثال { #example }

ایک سادہ مثال کے لیے، آئیے ایسا فائل ڈھانچہ لیتے ہیں جو [Bigger Applications](../tutorial/bigger-applications.md) اور [Testing](../tutorial/testing.md) میں بیان کیے گئے سے ملتا جلتا ہو:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

`main.py` فائل میں ہوگا:

{* ../../docs_src/async_tests/app_a_py310/main.py *}

`test_main.py` فائل میں `main.py` کے ٹیسٹ ہوں گے، یہ اب کچھ اس طرح نظر آ سکتی ہے:

{* ../../docs_src/async_tests/app_a_py310/test_main.py *}

## اسے چلائیں { #run-it }

آپ اپنے ٹیسٹ حسب معمول اس طرح چلا سکتے ہیں:

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## تفصیل سے { #in-detail }

`@pytest.mark.anyio` marker pytest کو بتاتا ہے کہ یہ test function asynchronously call کیا جانا چاہیے:

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[7] *}

/// tip | مشورہ

نوٹ کریں کہ test function اب `async def` ہے نہ کہ پہلے کی طرح صرف `def` جب `TestClient` استعمال ہوتا تھا۔

///

پھر ہم app کے ساتھ ایک `AsyncClient` بنا سکتے ہیں، اور `await` استعمال کرتے ہوئے اسے async requests بھیج سکتے ہیں۔

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[9:12] *}

یہ اس کے مساوی ہے:

```Python
response = client.get('/')
```

...جو ہم `TestClient` کے ساتھ اپنی requests بنانے کے لیے استعمال کرتے تھے۔

/// tip | مشورہ

نوٹ کریں کہ ہم نئے `AsyncClient` کے ساتھ async/await استعمال کر رہے ہیں - request asynchronous ہے۔

///

/// warning | انتباہ

اگر آپ کی ایپلیکیشن lifespan events پر انحصار کرتی ہے، تو `AsyncClient` ان events کو trigger نہیں کرے گا۔ ان کو trigger ہونا یقینی بنانے کے لیے، [florimondmanca/asgi-lifespan](https://github.com/florimondmanca/asgi-lifespan#usage) سے `LifespanManager` استعمال کریں۔

///

## دیگر Asynchronous Function Calls { #other-asynchronous-function-calls }

چونکہ testing function اب asynchronous ہے، آپ اب اپنی FastAPI ایپلیکیشن کو requests بھیجنے کے علاوہ دیگر `async` functions بھی call (اور `await`) کر سکتے ہیں، بالکل اسی طرح جیسے آپ انہیں اپنے کوڈ میں کہیں بھی call کرتے۔

/// tip | مشورہ

اگر آپ کو اپنے ٹیسٹوں میں asynchronous function calls integrate کرتے وقت `RuntimeError: Task attached to a different loop` آئے (مثلاً [MongoDB کا MotorClient](https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop) استعمال کرتے وقت)، تو یاد رکھیں کہ event loop کی ضرورت رکھنے والے objects صرف async functions کے اندر بنائیں، مثلاً `@app.on_event("startup")` callback۔

///
