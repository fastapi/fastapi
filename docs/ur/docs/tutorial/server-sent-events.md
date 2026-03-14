# Server-Sent Events (SSE) { #server-sent-events-sse }

آپ **Server-Sent Events** (SSE) استعمال کرتے ہوئے client کو data stream کر سکتے ہیں۔

یہ [Stream JSON Lines](stream-json-lines.md) سے ملتا جلتا ہے، لیکن `text/event-stream` format استعمال کرتا ہے، جو browsers میں [`EventSource` API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) کے ذریعے مقامی طور پر حمایت یافتہ ہے۔

/// info | معلومات

FastAPI 0.135.0 میں شامل کیا گیا۔

///

## Server-Sent Events کیا ہیں؟ { #what-are-server-sent-events }

SSE HTTP پر server سے client کو data stream کرنے کا ایک معیار ہے۔

ہر event ایک چھوٹا text block ہوتا ہے جس میں `data`، `event`، `id`، اور `retry` جیسے "fields" ہوتے ہیں، جو خالی لائنوں سے الگ ہوتے ہیں۔

یہ اس طرح نظر آتا ہے:

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE عام طور پر AI chat streaming، لائیو notifications، logs اور observability، اور دیگر صورتوں کے لیے استعمال ہوتا ہے جہاں server client کو updates بھیجتا ہے۔

/// tip | مشورہ

اگر آپ binary data stream کرنا چاہتے ہیں، مثلاً video یا audio، تو advanced گائیڈ دیکھیں: [Stream Data](../advanced/stream-data.md)۔

///

## FastAPI کے ساتھ SSE Stream کریں { #stream-sse-with-fastapi }

FastAPI کے ساتھ SSE stream کرنے کے لیے، اپنے *path operation function* میں `yield` استعمال کریں اور `response_class=EventSourceResponse` سیٹ کریں۔

`fastapi.sse` سے `EventSourceResponse` import کریں:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

ہر yield شدہ آئٹم JSON کے طور پر encode ہو کر SSE event کے `data:` field میں بھیجا جاتا ہے۔

اگر آپ return type کو `AsyncIterable[Item]` declare کرتے ہیں، تو FastAPI اسے Pydantic استعمال کرتے ہوئے data کو **validate**، **document**، اور **serialize** کرنے کے لیے استعمال کرے گا۔

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip | مشورہ

چونکہ Pydantic اسے **Rust** کی طرف سے serialize کرے گا، آپ کو return type declare نہ کرنے کی نسبت بہت زیادہ **performance** ملے گی۔

///

### غیر async *path operation functions* { #non-async-path-operation-functions }

آپ عام `def` functions (بغیر `async`) بھی استعمال کر سکتے ہیں، اور اسی طرح `yield` استعمال کر سکتے ہیں۔

FastAPI یقینی بنائے گا کہ یہ درست طریقے سے چلے تاکہ event loop block نہ ہو۔

اس صورت میں چونکہ function async نہیں ہے، صحیح return type `Iterable[Item]` ہوگا:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### بغیر Return Type { #no-return-type }

آپ return type بھی چھوڑ سکتے ہیں۔ FastAPI data کو تبدیل کرنے اور بھیجنے کے لیے [`jsonable_encoder`](./encoder.md) استعمال کرے گا۔

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

اگر آپ کو SSE fields جیسے `event`، `id`، `retry`، یا `comment` سیٹ کرنے کی ضرورت ہے، تو آپ سادہ data کی بجائے `ServerSentEvent` objects yield کر سکتے ہیں۔

`fastapi.sse` سے `ServerSentEvent` import کریں:

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

`data` field ہمیشہ JSON کے طور پر encode ہوتا ہے۔ آپ JSON کے طور پر serialize ہونے کے قابل کوئی بھی قدر دے سکتے ہیں، بشمول Pydantic models۔

## Raw Data { #raw-data }

اگر آپ کو JSON encoding **کے بغیر** data بھیجنے کی ضرورت ہے، تو `data` کی بجائے `raw_data` استعمال کریں۔

یہ پہلے سے فارمیٹ شدہ text، log lines، یا خاص <dfn title="ایک قدر جو کسی خاص حالت یا کیفیت کو ظاہر کرنے کے لیے استعمال ہو">"sentinel"</dfn> قدروں جیسے `[DONE]` بھیجنے کے لیے مفید ہے۔

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note | نوٹ

`data` اور `raw_data` باہمی طور پر خارج ہیں۔ آپ ہر `ServerSentEvent` میں ان میں سے صرف ایک سیٹ کر سکتے ہیں۔

///

## `Last-Event-ID` کے ساتھ دوبارہ شروع کرنا { #resuming-with-last-event-id }

جب connection ٹوٹنے کے بعد browser دوبارہ connect ہوتا ہے، تو وہ آخری وصول شدہ `id` کو `Last-Event-ID` header میں بھیجتا ہے۔

آپ اسے ایک header parameter کے طور پر پڑھ سکتے ہیں اور اسے استعمال کر کے stream کو وہیں سے دوبارہ شروع کر سکتے ہیں جہاں client نے چھوڑا تھا:

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## POST کے ساتھ SSE { #sse-with-post }

SSE **کسی بھی HTTP method** کے ساتھ کام کرتا ہے، صرف `GET` ہی نہیں۔

یہ [MCP](https://modelcontextprotocol.io) جیسے protocols کے لیے مفید ہے جو `POST` پر SSE stream کرتے ہیں:

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## تکنیکی تفصیلات { #technical-details }

FastAPI کچھ SSE بہترین طریقے خود بخود لاگو کرتا ہے۔

* جب کوئی پیغام نہ ہو تو ہر 15 سیکنڈ بعد **"keep alive" `ping` comment** بھیجتا ہے، تاکہ بعض proxies کو connection بند کرنے سے روکا جا سکے، جیسا کہ [HTML specification: Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes) میں تجویز کیا گیا ہے۔
* Stream کی **caching روکنے** کے لیے `Cache-Control: no-cache` header سیٹ کرتا ہے۔
* Nginx جیسے بعض proxies میں **buffering روکنے** کے لیے ایک خاص header `X-Accel-Buffering: no` سیٹ کرتا ہے۔

آپ کو اس بارے میں کچھ نہیں کرنا، یہ خود بخود کام کرتا ہے۔ 🤓
