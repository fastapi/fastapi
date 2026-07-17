# Request Example Data घोषित करें { #declare-request-example-data }

आप उस data के examples घोषित कर सकते हैं जिसे आपका app receive कर सकता है।

इसे करने के कई तरीके यहाँ दिए गए हैं।

## Pydantic models में अतिरिक्त JSON Schema data { #extra-json-schema-data-in-pydantic-models }

आप किसी Pydantic model के लिए `examples` घोषित कर सकते हैं, जिन्हें generated JSON Schema में जोड़ा जाएगा।

{* ../../docs_src/schema_extra_example/tutorial001_py310.py hl[13:24] *}

वह अतिरिक्त जानकारी उस model के output **JSON Schema** में जैसी है वैसी ही जोड़ी जाएगी, और API docs में उपयोग की जाएगी।

आप `model_config` attribute का उपयोग कर सकते हैं, जो एक `dict` लेता है, जैसा कि [Pydantic के docs: Configuration](https://docs.pydantic.dev/latest/api/config/) में बताया गया है।

आप `"json_schema_extra"` को एक `dict` के साथ set कर सकते हैं जिसमें कोई भी अतिरिक्त data हो जिसे आप generated JSON Schema में दिखाना चाहते हैं, जिसमें `examples` भी शामिल हैं।

/// tip | सुझाव

आप इसी technique का उपयोग JSON Schema को extend करने और अपनी custom अतिरिक्त जानकारी जोड़ने के लिए कर सकते हैं।

उदाहरण के लिए, आप इसका उपयोग frontend user interface आदि के लिए metadata जोड़ने में कर सकते हैं।

///

/// note | नोट

OpenAPI 3.1.0 (FastAPI 0.99.0 से उपयोग किया गया) ने `examples` के लिए support जोड़ा, जो **JSON Schema** standard का हिस्सा है।

उससे पहले, यह केवल keyword `example` को एक single example के साथ support करता था। यह अभी भी OpenAPI 3.1.0 द्वारा supported है, लेकिन deprecated है और JSON Schema standard का हिस्सा नहीं है। इसलिए आपको `example` से `examples` पर migrate करने के लिए प्रोत्साहित किया जाता है। 🤓

आप इस page के अंत में और पढ़ सकते हैं।

///

## `Field` के अतिरिक्त arguments { #field-additional-arguments }

Pydantic models के साथ `Field()` का उपयोग करते समय, आप अतिरिक्त `examples` भी घोषित कर सकते हैं:

{* ../../docs_src/schema_extra_example/tutorial002_py310.py hl[2,8:11] *}

## JSON Schema - OpenAPI में `examples` { #examples-in-json-schema-openapi }

इनमें से किसी का भी उपयोग करते समय:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

आप अतिरिक्त जानकारी के साथ `examples` का एक group भी घोषित कर सकते हैं, जिसे **OpenAPI** के अंदर उनके **JSON Schemas** में जोड़ा जाएगा।

### `examples` के साथ `Body` { #body-with-examples }

यहाँ हम `Body()` में अपेक्षित data के एक example वाला `examples` pass करते हैं:

{* ../../docs_src/schema_extra_example/tutorial003_an_py310.py hl[22:29] *}

### docs UI में Example { #example-in-the-docs-ui }

ऊपर दिए गए किसी भी method के साथ यह `/docs` में इस तरह दिखेगा:

<img src="/img/tutorial/body-fields/image01.png">

### कई `examples` के साथ `Body` { #body-with-multiple-examples }

बेशक आप कई `examples` भी pass कर सकते हैं:

{* ../../docs_src/schema_extra_example/tutorial004_an_py310.py hl[23:38] *}

जब आप ऐसा करते हैं, तो examples उस body data के internal **JSON Schema** का हिस्सा होंगे।

फिर भी, <dfn title="2023-08-26">यह लिखते समय</dfn>, Swagger UI, वह tool जो docs UI दिखाने के लिए जिम्मेदार है, **JSON Schema** में data के लिए कई examples दिखाने को support नहीं करता। लेकिन workaround के लिए नीचे पढ़ें।

### OpenAPI-specific `examples` { #openapi-specific-examples }

**JSON Schema** द्वारा `examples` support किए जाने से पहले से ही, OpenAPI में एक अलग field के लिए support था जिसे `examples` भी कहा जाता था।

यह **OpenAPI-specific** `examples` OpenAPI specification में किसी अन्य section में जाता है। यह प्रत्येक JSON Schema के अंदर नहीं, बल्कि **प्रत्येक *path operation* के details** में जाता है।

और Swagger UI ने इस विशेष `examples` field को कुछ समय से support किया है। इसलिए, आप इसका उपयोग docs UI में अलग-अलग **examples दिखाने** के लिए कर सकते हैं।

इस OpenAPI-specific field `examples` का आकार एक `dict` है जिसमें **कई examples** होते हैं (`list` के बजाय), और प्रत्येक में अतिरिक्त जानकारी होती है जो **OpenAPI** में भी जोड़ी जाएगी।

यह OpenAPI में मौजूद प्रत्येक JSON Schema के अंदर नहीं जाता, यह बाहर, सीधे *path operation* में जाता है।

### `openapi_examples` Parameter का उपयोग { #using-the-openapi-examples-parameter }

आप FastAPI में OpenAPI-specific `examples` को parameter `openapi_examples` के साथ इनके लिए घोषित कर सकते हैं:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

`dict` की keys प्रत्येक example की पहचान करती हैं, और प्रत्येक value एक और `dict` होती है।

`examples` में प्रत्येक specific example `dict` में ये हो सकते हैं:

* `summary`: example के लिए छोटा description।
* `description`: एक लंबा description जिसमें Markdown text हो सकता है।
* `value`: यह दिखाया गया वास्तविक example है, जैसे एक `dict`।
* `externalValue`: `value` का alternative, example की ओर point करने वाला URL। हालांकि यह शायद `value` जितने tools द्वारा supported न हो।

आप इसे इस तरह use कर सकते हैं:

{* ../../docs_src/schema_extra_example/tutorial005_an_py310.py hl[23:49] *}

### Docs UI में OpenAPI Examples { #openapi-examples-in-the-docs-ui }

`Body()` में `openapi_examples` जोड़ने के साथ `/docs` इस तरह दिखेगा:

<img src="/img/tutorial/body-fields/image02.png">

## तकनीकी विवरण { #technical-details }

/// tip | सुझाव

यदि आप पहले से ही **FastAPI** version **0.99.0 या उससे ऊपर** का उपयोग कर रहे हैं, तो आप शायद ये details **skip** कर सकते हैं।

ये पुराने versions के लिए अधिक relevant हैं, OpenAPI 3.1.0 उपलब्ध होने से पहले।

आप इसे एक संक्षिप्त OpenAPI और JSON Schema **history lesson** मान सकते हैं। 🤓

///

/// warning | चेतावनी

ये standards **JSON Schema** और **OpenAPI** के बारे में बहुत technical details हैं।

यदि ऊपर दिए गए ideas आपके लिए पहले से ही काम कर रहे हैं, तो वह पर्याप्त हो सकता है, और शायद आपको इन details की जरूरत नहीं है, इन्हें skip करने के लिए स्वतंत्र महसूस करें।

///

OpenAPI 3.1.0 से पहले, OpenAPI ने **JSON Schema** के एक पुराने और modified version का उपयोग किया।

JSON Schema में `examples` नहीं था, इसलिए OpenAPI ने अपने स्वयं के modified version में अपना `example` field जोड़ा।

OpenAPI ने specification के अन्य हिस्सों में भी `example` और `examples` fields जोड़े:

* [`Parameter Object` (specification में)](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object) जिसका उपयोग FastAPI के इनसे किया गया:
    * `Path()`
    * `Query()`
    * `Header()`
    * `Cookie()`
* [`Request Body Object`, field `content` में, `Media Type Object` पर (specification में)](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object) जिसका उपयोग FastAPI के इनसे किया गया:
    * `Body()`
    * `File()`
    * `Form()`

/// note | नोट

यह पुराना OpenAPI-specific `examples` parameter अब FastAPI `0.103.0` से `openapi_examples` है।

///

### JSON Schema का `examples` field { #json-schemas-examples-field }

लेकिन फिर JSON Schema ने specification के एक नए version में एक [`examples`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5) field जोड़ा।

और फिर नया OpenAPI 3.1.0 latest version (JSON Schema 2020-12) पर आधारित था, जिसमें यह नया field `examples` शामिल था।

और अब यह नया `examples` field पुराने single (और custom) `example` field पर precedence लेता है, जो अब deprecated है।

JSON Schema में यह नया `examples` field OpenAPI में अन्य जगहों (ऊपर वर्णित) की तरह अतिरिक्त metadata वाला dict नहीं है, यह **सिर्फ एक `list`** है।

/// note | नोट

OpenAPI 3.1.0 के JSON Schema के साथ इस नए सरल integration के साथ release होने के बाद भी, कुछ समय तक, Swagger UI, वह tool जो automatic docs प्रदान करता है, OpenAPI 3.1.0 को support नहीं करता था (यह version 5.0.0 से करता है 🎉)।

इसी वजह से, 0.99.0 से पहले के FastAPI versions अभी भी OpenAPI के 3.1.0 से कम versions का उपयोग करते थे।

///

### Pydantic और FastAPI `examples` { #pydantic-and-fastapi-examples }

जब आप Pydantic model के अंदर `examples` जोड़ते हैं, `schema_extra` या `Field(examples=["something"])` का उपयोग करके, तो वह example उस Pydantic model के **JSON Schema** में जोड़ा जाता है।

और उस Pydantic model का **JSON Schema** आपकी API के **OpenAPI** में शामिल होता है, और फिर docs UI में उपयोग किया जाता है।

FastAPI के 0.99.0 से पहले के versions में (0.99.0 और ऊपर वाले नए OpenAPI 3.1.0 का उपयोग करते हैं), जब आप किसी भी अन्य utilities (`Query()`, `Body()`, आदि) के साथ `example` या `examples` का उपयोग करते थे, तो वे examples उस data का वर्णन करने वाले JSON Schema में नहीं जोड़े जाते थे (OpenAPI के JSON Schema के अपने version में भी नहीं), वे सीधे OpenAPI में *path operation* declaration में जोड़े जाते थे (OpenAPI के उन parts के बाहर जो JSON Schema का उपयोग करते हैं)।

लेकिन अब जबकि FastAPI 0.99.0 और ऊपर OpenAPI 3.1.0 का उपयोग करता है, जो JSON Schema 2020-12 का उपयोग करता है, और Swagger UI 5.0.0 और ऊपर, सब कुछ अधिक consistent है और examples JSON Schema में शामिल होते हैं।

### Swagger UI और OpenAPI-specific `examples` { #swagger-ui-and-openapi-specific-examples }

अब, क्योंकि Swagger UI कई JSON Schema examples को support नहीं करता था (2023-08-26 तक), users के पास docs में कई examples दिखाने का कोई तरीका नहीं था।

इसे solve करने के लिए, FastAPI `0.103.0` ने नए parameter `openapi_examples` के साथ उसी पुराने **OpenAPI-specific** `examples` field को घोषित करने के लिए **support जोड़ा**। 🤓

### Summary { #summary }

मैं कहा करता था कि मुझे history उतनी पसंद नहीं है... और अब मुझे देखिए, "tech history" lessons दे रहा हूँ। 😅

संक्षेप में, **FastAPI 0.99.0 या उससे ऊपर upgrade करें**, और चीजें बहुत अधिक **सरल, consistent, और intuitive** हैं, और आपको ये सारे historical details जानने की जरूरत नहीं है। 😎
