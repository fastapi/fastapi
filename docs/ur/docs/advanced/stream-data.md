# ڈیٹا Stream کرنا { #stream-data }

اگر آپ ایسا ڈیٹا stream کرنا چاہتے ہیں جو JSON کے طور پر ترتیب دیا جا سکے، تو آپ کو [Stream JSON Lines](../tutorial/stream-json-lines.md) استعمال کرنا چاہیے۔

لیکن اگر آپ **خالص binary ڈیٹا** یا strings stream کرنا چاہتے ہیں، تو یہ طریقہ ہے۔

/// info | معلومات

FastAPI 0.134.0 میں شامل کیا گیا۔

///

## استعمال کی صورتیں { #use-cases }

آپ اسے استعمال کر سکتے ہیں اگر آپ خالص strings stream کرنا چاہیں، مثلاً براہ راست **AI LLM** سروس کے آؤٹ پٹ سے۔

آپ اسے **بڑی binary فائلیں** stream کرنے کے لیے بھی استعمال کر سکتے ہیں، جہاں آپ ڈیٹا کا ہر ٹکڑا پڑھتے ہوئے stream کرتے ہیں، بغیر اسے ایک ساتھ پوری memory میں پڑھے۔

آپ اس طریقے سے **ویڈیو** یا **آڈیو** بھی stream کر سکتے ہیں، یہ بھی بنایا جا سکتا ہے جب آپ پروسیس اور بھیج رہے ہوں۔

## `yield` کے ساتھ `StreamingResponse` { #a-streamingresponse-with-yield }

اگر آپ اپنے *path operation function* میں `response_class=StreamingResponse` بیان کریں تو آپ `yield` استعمال کر کے ڈیٹا کا ہر ٹکڑا باری باری بھیج سکتے ہیں۔

{* ../../docs_src/stream_data/tutorial001_py310.py ln[1:23] hl[20,23] *}

FastAPI ڈیٹا کا ہر ٹکڑا `StreamingResponse` کو جوں کا توں دے گا، یہ اسے JSON میں تبدیل کرنے یا ایسی کوئی چیز نہیں کرے گا۔

### غیر async *path operation functions* { #non-async-path-operation-functions }

آپ عام `def` functions (بغیر `async`) بھی استعمال کر سکتے ہیں، اور `yield` اسی طرح استعمال کر سکتے ہیں۔

{* ../../docs_src/stream_data/tutorial001_py310.py ln[26:29] hl[27] *}

### بغیر Annotation { #no-annotation }

Streaming binary ڈیٹا کے لیے آپ کو واقعی return type annotation بیان کرنے کی ضرورت نہیں ہے۔

چونکہ FastAPI Pydantic کے ساتھ ڈیٹا کو JSON میں تبدیل کرنے یا کسی طرح serialize کرنے کی کوشش نہیں کرے گا، اس صورت میں type annotation صرف آپ کے editor اور tools کے استعمال کے لیے ہے، FastAPI اسے استعمال نہیں کرے گا۔

{* ../../docs_src/stream_data/tutorial001_py310.py ln[32:35] hl[33] *}

اس کا مطلب یہ بھی ہے کہ `StreamingResponse` کے ساتھ آپ کو ڈیٹا bytes بالکل اسی طرح بنانے اور encode کرنے کی **آزادی** اور **ذمہ داری** ہے جیسے آپ انہیں بھیجنا چاہتے ہیں، type annotations سے آزاد۔

### Bytes Stream کریں { #stream-bytes }

اہم استعمال کی صورتوں میں سے ایک strings کی بجائے `bytes` stream کرنا ہے، آپ یقیناً ایسا کر سکتے ہیں۔

{* ../../docs_src/stream_data/tutorial001_py310.py ln[44:47] hl[47] *}

## حسب ضرورت `PNGStreamingResponse` { #a-custom-pngstreamingresponse }

اوپر کی مثالوں میں، ڈیٹا bytes stream کیے گئے لیکن response میں `Content-Type` header نہیں تھا، اس لیے client نہیں جانتا تھا کہ وہ کس قسم کا ڈیٹا وصول کر رہا ہے۔

آپ `StreamingResponse` کی حسب ضرورت sub-class بنا سکتے ہیں جو `Content-Type` header کو آپ کے stream کیے جانے والے ڈیٹا کی قسم پر سیٹ کرے۔

مثال کے طور پر، آپ `PNGStreamingResponse` بنا سکتے ہیں جو `media_type` attribute استعمال کرتے ہوئے `Content-Type` header کو `image/png` پر سیٹ کرے:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[6,19:20] hl[20] *}

پھر آپ اس نئی class کو اپنے *path operation function* میں `response_class=PNGStreamingResponse` میں استعمال کر سکتے ہیں:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[23:27] hl[23] *}

### فائل کی نقل { #simulate-a-file }

اس مثال میں، ہم `io.BytesIO` کے ساتھ فائل کی نقل کر رہے ہیں، جو صرف memory میں رہنے والا file-like آبجیکٹ ہے، لیکن وہی interface استعمال کرنے دیتا ہے۔

مثال کے طور پر، ہم اس کا مواد حاصل کرنے کے لیے اس پر iterate کر سکتے ہیں، جیسا کہ ہم فائل کے ساتھ کر سکتے ہیں۔

{* ../../docs_src/stream_data/tutorial002_py310.py ln[1:27] hl[3,12:13,25] *}

/// note | تکنیکی تفصیلات

دوسرے دو variables، `image_base64` اور `binary_image`، Base64 میں encoded تصویر ہیں، اور پھر bytes میں تبدیل کی گئی ہیں، تاکہ `io.BytesIO` کو پاس کی جا سکیں۔

صرف اس لیے کہ یہ اسی فائل میں رہ سکے اس مثال کے لیے اور آپ اسے کاپی کر کے جوں کا توں چلا سکیں۔

///

`with` بلاک استعمال کر کے، ہم یقینی بناتے ہیں کہ generator function (`yield` والا function) مکمل ہونے کے بعد file-like آبجیکٹ بند ہو جائے۔ تو، response بھیجنے کے بعد۔

اس مخصوص مثال میں یہ اتنا اہم نہیں ہوگا کیونکہ یہ memory میں جعلی فائل ہے (`io.BytesIO` کے ساتھ)، لیکن اصلی فائل کے ساتھ یہ اہم ہوگا کہ کام مکمل ہونے کے بعد فائل بند ہو۔

### فائلیں اور Async { #files-and-async }

زیادہ تر صورتوں میں، file-like آبجیکٹ بطور ڈیفالٹ async اور await کے ساتھ مطابقت نہیں رکھتے۔

مثلاً، ان کے پاس `await file.read()` نہیں ہوتا، یا `async for chunk in file`۔

اور بہت سی صورتوں میں، انہیں پڑھنا blocking عمل ہوگا (جو event loop کو بلاک کر سکتا ہے)، کیونکہ وہ ڈسک یا نیٹ ورک سے پڑھے جاتے ہیں۔

/// info | معلومات

اوپر والی مثال دراصل ایک استثناء ہے، کیونکہ `io.BytesIO` آبجیکٹ پہلے سے memory میں ہے، تو اسے پڑھنا کچھ بلاک نہیں کرے گا۔

لیکن بہت سی صورتوں میں فائل یا file-like آبجیکٹ پڑھنا بلاک کرے گا۔

///

event loop کو بلاک ہونے سے بچانے کے لیے، آپ *path operation function* کو `async def` کی بجائے عام `def` کے ساتھ بیان کر سکتے ہیں، اس طرح FastAPI اسے threadpool worker پر چلائے گا، مرکزی loop کو بلاک ہونے سے بچاتے ہوئے۔

{* ../../docs_src/stream_data/tutorial002_py310.py ln[30:34] hl[31] *}

/// tip | مشورہ

اگر آپ کو async function کے اندر سے blocking کوڈ بلانے کی ضرورت ہو، یا blocking function کے اندر سے async function بلانی ہو، تو آپ [Asyncer](https://asyncer.tiangolo.com) استعمال کر سکتے ہیں، جو FastAPI کی ایک ہم خواہر لائبریری ہے۔

///

### `yield from` { #yield-from }

جب آپ کسی چیز پر iterate کر رہے ہوں، جیسے file-like آبجیکٹ، اور پھر ہر آئٹم کے لیے `yield` کر رہے ہوں، تو آپ `yield from` بھی استعمال کر سکتے ہیں تاکہ ہر آئٹم کو براہ راست yield کریں اور `for` loop سے بچیں۔

یہ FastAPI کے لیے مخصوص نہیں ہے، بس Python ہے، لیکن جاننے کے لیے ایک اچھی تدبیر ہے۔

{* ../../docs_src/stream_data/tutorial002_py310.py ln[37:40] hl[40] *}
