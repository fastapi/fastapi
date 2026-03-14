# WebSockets { #websockets }

آپ **FastAPI** کے ساتھ [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) استعمال کر سکتے ہیں۔

## `websockets` انسٹال کریں { #install-websockets }

یقینی بنائیں کہ آپ [virtual environment](../virtual-environments.md) بنائیں، اسے فعال کریں، اور `websockets` انسٹال کریں (ایک Python لائبریری جو "WebSocket" protocol کو آسانی سے استعمال کرنے کی سہولت دیتی ہے):

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## WebSockets client { #websockets-client }

### پروڈکشن میں { #in-production }

آپ کے پروڈکشن سسٹم میں، شاید آپ کے پاس React، Vue.js یا Angular جیسے جدید framework سے بنایا گیا frontend ہوگا۔

اور اپنے backend کے ساتھ WebSockets سے رابطہ کرنے کے لیے آپ شاید اپنے frontend کی utilities استعمال کریں گے۔

یا آپ کے پاس کوئی native mobile ایپلیکیشن ہو سکتی ہے جو براہ راست native code میں آپ کے WebSocket backend سے رابطہ کرتی ہو۔

یا آپ کے پاس WebSocket endpoint سے رابطہ کرنے کا کوئی اور طریقہ ہو سکتا ہے۔

---

لیکن اس مثال کے لیے، ہم کچھ JavaScript کے ساتھ ایک بہت سادہ HTML document استعمال کریں گے، سب ایک لمبی string کے اندر۔

یہ یقیناً بہترین طریقہ نہیں ہے اور آپ اسے پروڈکشن میں استعمال نہیں کریں گے۔

پروڈکشن میں آپ کے پاس اوپر بتائے گئے آپشنز میں سے ایک ہوگا۔

لیکن WebSockets کی server-side پر توجہ مرکوز کرنے اور ایک کام کرنے والی مثال رکھنے کا یہ سب سے آسان طریقہ ہے:

{* ../../docs_src/websockets_/tutorial001_py310.py hl[2,6:38,41:43] *}

## `websocket` بنائیں { #create-a-websocket }

اپنی **FastAPI** ایپلیکیشن میں، ایک `websocket` بنائیں:

{* ../../docs_src/websockets_/tutorial001_py310.py hl[1,46:47] *}

/// note | تکنیکی تفصیلات

آپ `from starlette.websockets import WebSocket` بھی استعمال کر سکتے ہیں۔

**FastAPI** آپ کی سہولت کے لیے وہی `WebSocket` براہ راست فراہم کرتا ہے۔ لیکن یہ براہ راست Starlette سے آتا ہے۔

///

## پیغامات کا انتظار کریں اور پیغامات بھیجیں { #await-for-messages-and-send-messages }

اپنے WebSocket route میں آپ پیغامات کا `await` کر سکتے ہیں اور پیغامات بھیج سکتے ہیں۔

{* ../../docs_src/websockets_/tutorial001_py310.py hl[48:52] *}

آپ binary، text، اور JSON ڈیٹا وصول اور بھیج سکتے ہیں۔

## آزمائیں { #try-it }

اپنا کوڈ `main.py` فائل میں رکھیں اور پھر اپنی ایپلیکیشن چلائیں:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

اپنا browser [http://127.0.0.1:8000](http://127.0.0.1:8000) پر کھولیں۔

آپ کو ایک سادہ صفحہ نظر آئے گا:

<img src="/img/tutorial/websockets/image01.png">

آپ input باکس میں پیغامات ٹائپ کر کے بھیج سکتے ہیں:

<img src="/img/tutorial/websockets/image02.png">

اور آپ کی WebSockets والی **FastAPI** ایپلیکیشن واپس جواب دے گی:

<img src="/img/tutorial/websockets/image03.png">

آپ بہت سے پیغامات بھیج (اور وصول کر) سکتے ہیں:

<img src="/img/tutorial/websockets/image04.png">

اور یہ سب ایک ہی WebSocket connection استعمال کریں گے۔

## `Depends` اور دیگر کا استعمال { #using-depends-and-others }

WebSocket endpoints میں آپ `fastapi` سے import کر کے استعمال کر سکتے ہیں:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

یہ دوسرے FastAPI endpoints/*path operations* کی طرح ہی کام کرتے ہیں:

{* ../../docs_src/websockets_/tutorial002_an_py310.py hl[68:69,82] *}

/// info | معلومات

چونکہ یہ WebSocket ہے تو `HTTPException` raise کرنا واقعی مناسب نہیں ہے، اس کی بجائے ہم `WebSocketException` raise کرتے ہیں۔

آپ [specification میں بیان کردہ درست codes](https://tools.ietf.org/html/rfc6455#section-7.4.1) سے closing code استعمال کر سکتے ہیں۔

///

### Dependencies کے ساتھ WebSockets آزمائیں { #try-the-websockets-with-dependencies }

اپنی ایپلیکیشن چلائیں:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

اپنا browser [http://127.0.0.1:8000](http://127.0.0.1:8000) پر کھولیں۔

وہاں آپ سیٹ کر سکتے ہیں:

* "Item ID"، جو path میں استعمال ہوتا ہے۔
* "Token" جو query parameter کے طور پر استعمال ہوتا ہے۔

/// tip | مشورہ

غور کریں کہ query `token` کو dependency کے ذریعے ہینڈل کیا جائے گا۔

///

اس کے ساتھ آپ WebSocket سے جڑ سکتے ہیں اور پھر پیغامات بھیج اور وصول کر سکتے ہیں:

<img src="/img/tutorial/websockets/image05.png">

## منقطع ہونے اور متعدد clients کو سنبھالنا { #handling-disconnections-and-multiple-clients }

جب WebSocket connection بند ہوتا ہے تو `await websocket.receive_text()` ایک `WebSocketDisconnect` exception raise کرتا ہے، جسے آپ اس مثال کی طرح پکڑ کر ہینڈل کر سکتے ہیں۔

{* ../../docs_src/websockets_/tutorial003_py310.py hl[79:81] *}

آزمانے کے لیے:

* ایپ کو کئی browser tabs میں کھولیں۔
* ان سے پیغامات لکھیں۔
* پھر ان میں سے ایک tab بند کریں۔

اس سے `WebSocketDisconnect` exception raise ہوگا، اور باقی تمام clients کو اس طرح کا پیغام ملے گا:

```
Client #1596980209979 left the chat
```

/// tip | مشورہ

اوپر والی ایپ ایک کم سے کم اور سادہ مثال ہے جو یہ ظاہر کرتی ہے کہ کئی WebSocket connections پر پیغامات کیسے ہینڈل اور broadcast کیے جائیں۔

لیکن یاد رکھیں کہ، چونکہ سب کچھ memory میں ایک واحد فہرست میں ہینڈل ہو رہا ہے، یہ صرف اس وقت تک کام کرے گا جب تک process چل رہا ہے، اور صرف ایک واحد process کے ساتھ کام کرے گا۔

اگر آپ کو کچھ ایسا چاہیے جو FastAPI کے ساتھ آسانی سے integrate ہو لیکن زیادہ مضبوط ہو، Redis، PostgreSQL یا دیگر کی سپورٹ رکھتا ہو، تو [encode/broadcaster](https://github.com/encode/broadcaster) دیکھیں۔

///

## مزید معلومات { #more-info }

آپشنز کے بارے میں مزید جاننے کے لیے، Starlette کی دستاویزات دیکھیں:

* [`WebSocket` class](https://www.starlette.dev/websockets/)
* [Class پر مبنی WebSocket ہینڈلنگ](https://www.starlette.dev/endpoints/#websocketendpoint)
