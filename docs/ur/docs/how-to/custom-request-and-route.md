# حسب ضرورت Request اور APIRoute class { #custom-request-and-apiroute-class }

بعض صورتوں میں، آپ `Request` اور `APIRoute` classes کی منطق کو override کرنا چاہ سکتے ہیں۔

خاص طور پر، یہ middleware میں منطق رکھنے کا ایک اچھا متبادل ہو سکتا ہے۔

مثال کے طور پر، اگر آپ request body کو آپ کی application کی طرف سے process ہونے سے پہلے پڑھنا یا تبدیل کرنا چاہتے ہیں۔

/// danger

یہ ایک "advanced" خصوصیت ہے۔

اگر آپ ابھی **FastAPI** شروع کر رہے ہیں تو شاید آپ اس حصے کو چھوڑنا چاہیں گے۔

///

## استعمال کے معاملات { #use-cases }

کچھ استعمال کے معاملات میں شامل ہیں:

* غیر JSON request bodies کو JSON میں تبدیل کرنا (مثلاً [`msgpack`](https://msgpack.org/index.html))۔
* gzip سے compress شدہ request bodies کو decompress کرنا۔
* تمام request bodies کو خود کار طریقے سے log کرنا۔

## حسب ضرورت request body encodings کو سنبھالنا { #handling-custom-request-body-encodings }

آئیے دیکھتے ہیں کہ gzip requests کو decompress کرنے کے لیے حسب ضرورت `Request` subclass کیسے استعمال کی جائے۔

اور اس حسب ضرورت request class کو استعمال کرنے کے لیے `APIRoute` subclass کیسے بنائی جائے۔

### حسب ضرورت `GzipRequest` class بنائیں { #create-a-custom-gziprequest-class }

/// tip | مشورہ

یہ ایک مثال ہے جو دکھاتی ہے کہ یہ کیسے کام کرتا ہے، اگر آپ کو Gzip سپورٹ کی ضرورت ہے، تو آپ فراہم کردہ [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware) استعمال کر سکتے ہیں۔

///

سب سے پہلے، ہم ایک `GzipRequest` class بناتے ہیں، جو مناسب header کی موجودگی میں body کو decompress کرنے کے لیے `Request.body()` method کو overwrite کرے گی۔

اگر header میں `gzip` نہیں ہے، تو یہ body کو decompress کرنے کی کوشش نہیں کرے گی۔

اس طرح، ایک ہی route class gzip سے compress شدہ یا بغیر compress شدہ requests کو سنبھال سکتی ہے۔

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[9:16] *}

### حسب ضرورت `GzipRoute` class بنائیں { #create-a-custom-gziproute-class }

اس کے بعد، ہم `fastapi.routing.APIRoute` کی ایک حسب ضرورت subclass بناتے ہیں جو `GzipRequest` استعمال کرے گی۔

اس بار، یہ `APIRoute.get_route_handler()` method کو overwrite کرے گی۔

یہ method ایک function واپس کرتا ہے۔ اور وہ function ہی ہے جو request وصول کرے گا اور response واپس کرے گا۔

یہاں ہم اسے اصل request سے `GzipRequest` بنانے کے لیے استعمال کرتے ہیں۔

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[19:27] *}

/// note | تکنیکی تفصیلات

ایک `Request` میں `request.scope` attribute ہوتا ہے، جو صرف ایک Python `dict` ہے جس میں request سے متعلق metadata ہوتا ہے۔

ایک `Request` میں `request.receive` بھی ہوتا ہے، جو request کی body کو "وصول" کرنے کا function ہے۔

`scope` `dict` اور `receive` function دونوں ASGI specification کا حصہ ہیں۔

اور یہ دو چیزیں، `scope` اور `receive`، نئی `Request` instance بنانے کے لیے درکار ہیں۔

`Request` کے بارے میں مزید جاننے کے لیے [Starlette کی Requests کے بارے میں دستاویزات](https://www.starlette.dev/requests/) دیکھیں۔

///

`GzipRequest.get_route_handler` کی واپس کردہ function صرف اتنا مختلف کام کرتی ہے کہ `Request` کو `GzipRequest` میں تبدیل کرتی ہے۔

ایسا کرنے سے، ہماری `GzipRequest` ہماری *path operations* کو بھیجنے سے پہلے ڈیٹا کو decompress (اگر ضروری ہو) کا خیال رکھے گی۔

اس کے بعد، تمام processing کی منطق ایک جیسی ہی ہے۔

لیکن ہماری `GzipRequest.body` میں تبدیلیوں کی وجہ سے، request body خود بخود decompress ہو جائے گی جب **FastAPI** اسے ضرورت کے وقت load کرے گا۔

## Exception handler میں request body تک رسائی { #accessing-the-request-body-in-an-exception-handler }

/// tip | مشورہ

اسی مسئلے کو حل کرنے کے لیے، `RequestValidationError` کے لیے حسب ضرورت handler میں `body` استعمال کرنا شاید بہت آسان ہے ([Handling Errors](../tutorial/handling-errors.md#use-the-requestvalidationerror-body))۔

لیکن یہ مثال اب بھی درست ہے اور یہ دکھاتی ہے کہ اندرونی اجزاء کے ساتھ کیسے تعامل کیا جائے۔

///

ہم اسی طریقے کو exception handler میں request body تک رسائی کے لیے بھی استعمال کر سکتے ہیں۔

ہمیں بس request کو `try`/`except` block کے اندر سنبھالنا ہے:

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[14,16] *}

اگر کوئی exception واقع ہو، تو `Request` instance ابھی بھی scope میں ہوگی، تو ہم error کو سنبھالتے وقت request body کو پڑھ اور استعمال کر سکتے ہیں:

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[17:19] *}

## Router میں حسب ضرورت `APIRoute` class { #custom-apiroute-class-in-a-router }

آپ `APIRouter` کا `route_class` parameter بھی سیٹ کر سکتے ہیں:

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[26] *}

اس مثال میں، `router` کے تحت *path operations* حسب ضرورت `TimedRoute` class استعمال کریں گی، اور response میں ایک اضافی `X-Response-Time` header ہوگا جس میں response تیار کرنے میں لگنے والا وقت ہوگا:

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[13:20] *}
