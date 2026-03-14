# Lifespan Events { #lifespan-events }

آپ ایسی منطق (کوڈ) بیان کر سکتے ہیں جو ایپلیکیشن **شروع ہونے** سے پہلے عمل میں آئے۔ اس کا مطلب ہے کہ یہ کوڈ ایپلیکیشن کے **requests وصول کرنا شروع** کرنے سے **پہلے**، **ایک بار** عمل میں آئے گا۔

اسی طرح، آپ ایسی منطق (کوڈ) بیان کر سکتے ہیں جو ایپلیکیشن کے **بند ہونے** کے وقت عمل میں آئے۔ اس صورت میں، یہ کوڈ ممکنہ طور پر **بہت سی requests** ہینڈل کرنے کے **بعد**، **ایک بار** عمل میں آئے گا۔

چونکہ یہ کوڈ ایپلیکیشن کے requests لینا **شروع** کرنے سے پہلے عمل میں آتا ہے، اور requests ہینڈل کرنا **ختم** کرنے کے فوراً بعد، یہ پوری ایپلیکیشن کی **lifespan** کا احاطہ کرتا ہے (لفظ "lifespan" ایک لمحے میں اہم ہوگا)۔

یہ ایسے **وسائل** سیٹ اپ کرنے کے لیے بہت مفید ہو سکتا ہے جو آپ کو پوری ایپ میں استعمال کرنے ہیں، اور جو requests کے درمیان **مشترک** ہیں، اور/یا جنہیں آپ کو بعد میں **صاف** کرنا ہے۔ مثال کے طور پر، database connection pool، یا مشترکہ machine learning model لوڈ کرنا۔

## استعمال کی صورت { #use-case }

آئیے ایک مثال **استعمال کی صورت** سے شروع کریں اور پھر دیکھیں کہ اسے کیسے حل کیا جائے۔

فرض کریں کہ آپ کے پاس کچھ **machine learning models** ہیں جو آپ requests ہینڈل کرنے کے لیے استعمال کرنا چاہتے ہیں۔

وہی models requests کے درمیان مشترک ہیں، تو یہ ہر request کے لیے ایک model نہیں، یا ہر صارف کے لیے ایک یا اس جیسی کوئی بات نہیں۔

فرض کریں کہ model لوڈ کرنے میں **کافی وقت** لگ سکتا ہے، کیونکہ اسے **ڈسک سے بہت سا ڈیٹا** پڑھنا ہوتا ہے۔ تو آپ ہر request پر یہ نہیں کرنا چاہتے۔

آپ اسے module/فائل کی اعلیٰ سطح پر لوڈ کر سکتے ہیں، لیکن اس کا مطلب یہ بھی ہوگا کہ اگر آپ صرف ایک سادہ خودکار ٹیسٹ چلا رہے ہیں تو بھی یہ **model لوڈ** کرے گا، پھر وہ ٹیسٹ **سست** ہوگا کیونکہ اسے کوڈ کا آزاد حصہ چلانے سے پہلے model لوڈ ہونے کا انتظار کرنا ہوگا۔

یہی ہم حل کریں گے، requests ہینڈل ہونے سے پہلے model لوڈ کریں، لیکن صرف ایپلیکیشن کے requests وصول کرنا شروع کرنے سے ٹھیک پہلے، نہ کہ جب کوڈ لوڈ ہو رہا ہو۔

## Lifespan { #lifespan }

آپ `FastAPI` ایپ کے `lifespan` parameter اور ایک "context manager" استعمال کرکے یہ *startup* اور *shutdown* منطق بیان کر سکتے ہیں (میں آپ کو ایک لمحے میں بتاؤں گا کہ یہ کیا ہے)۔

آئیے ایک مثال سے شروع کریں اور پھر تفصیل سے دیکھیں۔

ہم `yield` کے ساتھ ایک async function `lifespan()` اس طرح بناتے ہیں:

{* ../../docs_src/events/tutorial003_py310.py hl[16,19] *}

یہاں ہم model لوڈ کرنے کے مہنگے *startup* عمل کی نقل کر رہے ہیں (جعلی) model function کو `yield` سے پہلے machine learning models کی dictionary میں رکھ کر۔ یہ کوڈ ایپلیکیشن کے **requests لینا شروع** کرنے سے **پہلے**، *startup* کے دوران عمل میں آئے گا۔

اور پھر، `yield` کے فوراً بعد، ہم model کو unload کرتے ہیں۔ یہ کوڈ ایپلیکیشن کے **requests ہینڈل کرنا ختم** کرنے کے **بعد**، *shutdown* سے ٹھیک پہلے عمل میں آئے گا۔ یہ مثال کے طور پر، memory یا GPU جیسے وسائل آزاد کر سکتا ہے۔

/// tip | مشورہ

`shutdown` تب ہوگا جب آپ ایپلیکیشن **بند** کر رہے ہوں۔

شاید آپ کو نیا ورژن شروع کرنا ہو، یا آپ بس اسے چلاتے چلاتے تھک گئے ہوں۔

///

### Lifespan function { #lifespan-function }

سب سے پہلے غور کریں کہ ہم `yield` کے ساتھ ایک async function بیان کر رہے ہیں۔ یہ `yield` والی Dependencies سے بہت ملتا جلتا ہے۔

{* ../../docs_src/events/tutorial003_py310.py hl[14:19] *}

function کا پہلا حصہ، `yield` سے پہلے، ایپلیکیشن شروع ہونے سے **پہلے** عمل میں آئے گا۔

اور `yield` کے بعد والا حصہ ایپلیکیشن ختم ہونے کے **بعد** عمل میں آئے گا۔

### Async Context Manager { #async-context-manager }

اگر آپ دیکھیں، تو function کو `@asynccontextmanager` سے decorate کیا گیا ہے۔

یہ function کو "**async context manager**" نامی چیز میں تبدیل کرتا ہے۔

{* ../../docs_src/events/tutorial003_py310.py hl[1,13] *}

Python میں **context manager** وہ چیز ہے جسے آپ `with` statement میں استعمال کر سکتے ہیں، مثال کے طور پر، `open()` context manager کے طور پر استعمال ہو سکتا ہے:

```Python
with open("file.txt") as file:
    file.read()
```

Python کے حالیہ ورژنز میں، ایک **async context manager** بھی ہے۔ آپ اسے `async with` کے ساتھ استعمال کریں گے:

```Python
async with lifespan(app):
    await do_stuff()
```

جب آپ اوپر کی طرح context manager یا async context manager بناتے ہیں، تو یہ `with` بلاک میں داخل ہونے سے پہلے `yield` سے پہلے والا کوڈ عمل میں لائے گا، اور `with` بلاک سے باہر نکلنے کے بعد `yield` کے بعد والا کوڈ عمل میں لائے گا۔

ہماری اوپر والی کوڈ مثال میں، ہم اسے براہ راست استعمال نہیں کرتے، بلکہ FastAPI کو استعمال کرنے کے لیے پاس کرتے ہیں۔

`FastAPI` ایپ کا `lifespan` parameter ایک **async context manager** لیتا ہے، تو ہم اپنا نیا `lifespan` async context manager اسے پاس کر سکتے ہیں۔

{* ../../docs_src/events/tutorial003_py310.py hl[22] *}

## متبادل Events (deprecated) { #alternative-events-deprecated }

/// warning | انتباہ

*startup* اور *shutdown* کو ہینڈل کرنے کا تجویز کردہ طریقہ اوپر بیان کردہ `FastAPI` ایپ کا `lifespan` parameter استعمال کرنا ہے۔ اگر آپ `lifespan` parameter فراہم کریں تو `startup` اور `shutdown` event handlers مزید نہیں بلائے جائیں گے۔ یہ یا تو سب `lifespan` ہے یا سب events، دونوں نہیں۔

آپ شاید اس حصے کو چھوڑ سکتے ہیں۔

///

*startup* اور *shutdown* کے دوران عمل میں آنے والی منطق بیان کرنے کا ایک متبادل طریقہ ہے۔

آپ ایسے event handler functions بیان کر سکتے ہیں جو ایپلیکیشن شروع ہونے سے پہلے، یا بند ہوتے وقت عمل میں آنے چاہییں۔

یہ functions `async def` یا عام `def` کے ساتھ بیان کیے جا سکتے ہیں۔

### `startup` event { #startup-event }

ایسا function شامل کرنے کے لیے جو ایپلیکیشن شروع ہونے سے پہلے چلے، اسے `"startup"` event کے ساتھ بیان کریں:

{* ../../docs_src/events/tutorial001_py310.py hl[8] *}

اس صورت میں، `startup` event handler function آئٹمز کے "database" (صرف ایک `dict`) کو کچھ اقدار سے شروع کرے گا۔

آپ ایک سے زیادہ event handler functions شامل کر سکتے ہیں۔

اور آپ کی ایپلیکیشن تب تک requests وصول کرنا شروع نہیں کرے گی جب تک تمام `startup` event handlers مکمل نہیں ہو جاتے۔

### `shutdown` event { #shutdown-event }

ایسا function شامل کرنے کے لیے جو ایپلیکیشن بند ہوتے وقت چلے، اسے `"shutdown"` event کے ساتھ بیان کریں:

{* ../../docs_src/events/tutorial002_py310.py hl[6] *}

یہاں، `shutdown` event handler function `log.txt` فائل میں ایک ٹیکسٹ لائن `"Application shutdown"` لکھے گا۔

/// info | معلومات

`open()` function میں، `mode="a"` کا مطلب "append" ہے، تو لائن فائل میں پہلے سے موجود مواد کو مٹائے بغیر آخر میں شامل ہوگی۔

///

/// tip | مشورہ

غور کریں کہ اس صورت میں ہم معیاری Python `open()` function استعمال کر رہے ہیں جو فائل کے ساتھ بات چیت کرتا ہے۔

تو، اس میں I/O (input/output) شامل ہے، جس کے لیے ڈسک پر لکھے جانے کا "انتظار" کرنا ہوتا ہے۔

لیکن `open()` `async` اور `await` استعمال نہیں کرتا۔

تو، ہم event handler function کو `async def` کی بجائے معیاری `def` کے ساتھ بیان کرتے ہیں۔

///

### `startup` اور `shutdown` ایک ساتھ { #startup-and-shutdown-together }

بہت زیادہ امکان ہے کہ آپ کی *startup* اور *shutdown* منطق آپس میں جڑی ہوئی ہے، آپ شاید کچھ شروع کرنا اور پھر ختم کرنا چاہیں، کوئی وسیلہ حاصل کرنا اور پھر آزاد کرنا چاہیں وغیرہ۔

یہ الگ functions میں کرنا جو منطق یا متغیرات شیئر نہیں کرتے، زیادہ مشکل ہے کیونکہ آپ کو اقدار global variables یا اسی طرح کی تدبیروں میں محفوظ کرنی ہوں گی۔

اسی لیے، اب تجویز یہ ہے کہ اوپر بیان کردہ `lifespan` استعمال کریں۔

## تکنیکی تفصیلات { #technical-details }

متجسس لوگوں کے لیے صرف ایک تکنیکی تفصیل۔

اندرونی طور پر، ASGI تکنیکی specification میں، یہ [Lifespan Protocol](https://asgi.readthedocs.io/en/latest/specs/lifespan.html) کا حصہ ہے، اور یہ `startup` اور `shutdown` نامی events بیان کرتا ہے۔

/// info | معلومات

آپ Starlette کے `lifespan` handlers کے بارے میں مزید [Starlette کی Lifespan دستاویزات](https://www.starlette.dev/lifespan/) میں پڑھ سکتے ہیں۔

بشمول یہ کہ lifespan state کو کیسے ہینڈل کریں جو آپ کے کوڈ کے دوسرے حصوں میں استعمال ہو سکتا ہے۔

///

## Sub Applications { #sub-applications }

یاد رکھیں کہ یہ lifespan events (startup اور shutdown) صرف مرکزی ایپلیکیشن کے لیے عمل میں آئیں گے، [Sub Applications - Mounts](sub-applications.md) کے لیے نہیں۔
