# कस्टम Response - HTML, Stream, File, अन्य { #custom-response-html-stream-file-others }

Default रूप से, **FastAPI** JSON responses लौटाएगा।

आप [सीधे Response लौटाएँ](response-directly.md) में दिखाए गए अनुसार सीधे `Response` लौटाकर इसे override कर सकते हैं।

लेकिन अगर आप सीधे `Response` लौटाते हैं (या कोई subclass, जैसे `JSONResponse`), तो data अपने आप convert नहीं होगा (भले ही आप `response_model` declare करें), और documentation अपने आप generate नहीं होगी (उदाहरण के लिए, generated OpenAPI के हिस्से के रूप में HTTP header `Content-Type` में specific "media type" शामिल करना)।

लेकिन आप *path operation decorator* में `response_class` parameter का उपयोग करके वह `Response` भी declare कर सकते हैं जिसे आप उपयोग करना चाहते हैं (जैसे कोई भी `Response` subclass)।

आप अपनी *path operation function* से जो contents लौटाते हैं, उन्हें उस `Response` के अंदर रख दिया जाएगा।

/// note | नोट

यदि आप बिना media type वाली response class का उपयोग करते हैं, तो FastAPI अपेक्षा करेगा कि आपके response में कोई content न हो, इसलिए यह अपने generated OpenAPI docs में response format को document नहीं करेगा।

///

## JSON Responses { #json-responses }

Default रूप से FastAPI JSON responses लौटाता है।

यदि आप [Response Model](../tutorial/response-model.md) declare करते हैं तो FastAPI Pydantic का उपयोग करके data को JSON में serialize करने के लिए उसका उपयोग करेगा।

यदि आप response model declare नहीं करते हैं, तो FastAPI [JSON Compatible Encoder](../tutorial/encoder.md) में समझाए गए `jsonable_encoder` का उपयोग करेगा और उसे `JSONResponse` में रखेगा।

यदि आप JSON media type (`application/json`) के साथ `response_class` declare करते हैं, जैसा कि `JSONResponse` के साथ होता है, तो आपके द्वारा लौटाया गया data आपकी *path operation decorator* में declare किए गए किसी भी Pydantic `response_model` के साथ अपने आप convert (और filter) हो जाएगा। लेकिन data Pydantic के साथ JSON bytes में serialize नहीं होगा, इसके बजाय इसे `jsonable_encoder` के साथ convert किया जाएगा और फिर `JSONResponse` class को pass किया जाएगा, जो Python की standard JSON library का उपयोग करके इसे bytes में serialize करेगी।

### JSON Performance { #json-performance }

संक्षेप में, यदि आप maximum performance चाहते हैं, तो [Response Model](../tutorial/response-model.md) का उपयोग करें और *path operation decorator* में `response_class` declare न करें।

{* ../../docs_src/response_model/tutorial001_01_py310.py ln[15:17] hl[16] *}

## HTML Response { #html-response }

**FastAPI** से सीधे HTML के साथ response लौटाने के लिए, `HTMLResponse` का उपयोग करें।

* `HTMLResponse` import करें।
* अपने *path operation decorator* के parameter `response_class` के रूप में `HTMLResponse` pass करें।

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// note | नोट

Parameter `response_class` का उपयोग response के "media type" को define करने के लिए भी किया जाएगा।

इस मामले में, HTTP header `Content-Type` को `text/html` पर set किया जाएगा।

और इसे OpenAPI में इसी तरह document किया जाएगा।

///

### `Response` लौटाएँ { #return-a-response }

जैसा कि [सीधे Response लौटाएँ](response-directly.md) में देखा गया है, आप अपनी *path operation* में response को सीधे लौटाकर भी override कर सकते हैं।

ऊपर वाला वही उदाहरण, जो `HTMLResponse` लौटाता है, इस तरह दिख सकता है:

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning | चेतावनी

आपकी *path operation function* द्वारा सीधे लौटाया गया `Response` OpenAPI में document नहीं होगा (उदाहरण के लिए, `Content-Type` document नहीं होगा) और automatic interactive docs में visible नहीं होगा।

///

/// note | नोट

बेशक, वास्तविक `Content-Type` header, status code, आदि, आपके द्वारा लौटाए गए `Response` object से आएँगे।

///

### OpenAPI में document करें और `Response` override करें { #document-in-openapi-and-override-response }

यदि आप function के अंदर से response को override करना चाहते हैं लेकिन साथ ही OpenAPI में "media type" document करना चाहते हैं, तो आप `response_class` parameter का उपयोग कर सकते हैं और `Response` object भी लौटा सकते हैं।

तब `response_class` का उपयोग केवल OpenAPI *path operation* को document करने के लिए किया जाएगा, लेकिन आपका `Response` जैसा है वैसा ही उपयोग किया जाएगा।

#### सीधे `HTMLResponse` लौटाएँ { #return-an-htmlresponse-directly }

उदाहरण के लिए, यह कुछ ऐसा हो सकता है:

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

इस उदाहरण में, function `generate_html_response()` पहले से ही HTML को `str` में लौटाने के बजाय `Response` generate करके लौटाता है।

`generate_html_response()` को call करने का result लौटाकर, आप पहले से ही एक `Response` लौटा रहे हैं जो default **FastAPI** behavior को override करेगा।

लेकिन क्योंकि आपने `response_class` में भी `HTMLResponse` pass किया है, **FastAPI** को पता होगा कि इसे OpenAPI और interactive docs में `text/html` के साथ HTML के रूप में कैसे document करना है:

<img src="/img/tutorial/custom-response/image01.png">

## उपलब्ध responses { #available-responses }

यहाँ कुछ उपलब्ध responses दिए गए हैं।

ध्यान रखें कि आप कुछ और लौटाने के लिए `Response` का उपयोग कर सकते हैं, या custom sub-class भी बना सकते हैं।

/// note | तकनीकी विवरण

आप `from starlette.responses import HTMLResponse` भी उपयोग कर सकते हैं।

**FastAPI** आपकी सुविधा के लिए, developer के रूप में, वही `starlette.responses` `fastapi.responses` के रूप में प्रदान करता है। लेकिन अधिकांश उपलब्ध responses सीधे Starlette से आते हैं।

///

### `Response` { #response }

मुख्य `Response` class, बाकी सभी responses इससे inherit करते हैं।

आप इसे सीधे लौटा सकते हैं।

यह निम्नलिखित parameters accept करता है:

* `content` - एक `str` या `bytes`।
* `status_code` - एक `int` HTTP status code।
* `headers` - strings का एक `dict`।
* `media_type` - media type बताने वाला एक `str`। उदाहरण के लिए `"text/html"`।

FastAPI (असल में Starlette) अपने आप एक Content-Length header शामिल करेगा। यह `media_type` के आधार पर Content-Type header भी शामिल करेगा और text types के लिए charset append करेगा।

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

कुछ text या bytes लेता है और HTML response लौटाता है, जैसा आपने ऊपर पढ़ा।

### `PlainTextResponse` { #plaintextresponse }

कुछ text या bytes लेता है और plain text response लौटाता है।

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

कुछ data लेता है और `application/json` encoded response लौटाता है।

जैसा आपने ऊपर पढ़ा, यह **FastAPI** में उपयोग किया जाने वाला default response है।

/// note | तकनीकी विवरण

लेकिन यदि आप response model या return type declare करते हैं, तो उसका उपयोग सीधे data को JSON में serialize करने के लिए किया जाएगा, और JSON के लिए सही media type वाला response सीधे लौटाया जाएगा, `JSONResponse` class का उपयोग किए बिना।

यह best performance पाने का ideal तरीका है।

///

### `RedirectResponse` { #redirectresponse }

HTTP redirect लौटाता है। Default रूप से 307 status code (Temporary Redirect) का उपयोग करता है।

आप सीधे `RedirectResponse` लौटा सकते हैं:

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

या आप इसे `response_class` parameter में उपयोग कर सकते हैं:


{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

यदि आप ऐसा करते हैं, तो आप अपनी *path operation* function से URL सीधे लौटा सकते हैं।

इस मामले में, उपयोग किया गया `status_code` `RedirectResponse` के लिए default वाला होगा, जो `307` है।

---

आप `status_code` parameter को `response_class` parameter के साथ combine करके भी उपयोग कर सकते हैं:

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

एक async generator या सामान्य generator/iterator (`yield` वाली function) लेता है और response body को stream करता है।

{* ../../docs_src/custom_response/tutorial007_py310.py hl[3,16] *}

/// note | तकनीकी विवरण

एक `async` task केवल तब cancel किया जा सकता है जब वह किसी `await` तक पहुँचता है। यदि कोई `await` नहीं है, तो generator (`yield` वाली function) ठीक से cancel नहीं हो सकता और cancellation request किए जाने के बाद भी चलना जारी रख सकता है।

चूँकि इस छोटे उदाहरण को किसी `await` statement की आवश्यकता नहीं है, हम event loop को cancellation handle करने का अवसर देने के लिए `await anyio.sleep(0)` जोड़ते हैं।

यह बड़े या infinite streams के साथ और भी अधिक महत्वपूर्ण होगा।

///

/// tip | टिप

सीधे `StreamingResponse` लौटाने के बजाय, आपको शायद [Stream Data](./stream-data.md) में दिए गए style का पालन करना चाहिए, यह कहीं अधिक सुविधाजनक है और आपके लिए पर्दे के पीछे cancellation handle करता है।

यदि आप JSON Lines stream कर रहे हैं, तो [Stream JSON Lines](../tutorial/stream-json-lines.md) tutorial का पालन करें।

///

### `FileResponse` { #fileresponse }

एक file को response के रूप में asynchronously stream करता है।

Instantiate करने के लिए अन्य response types की तुलना में अलग set of arguments लेता है:

* `path` - stream की जाने वाली file का file path।
* `headers` - dictionary के रूप में शामिल किए जाने वाले कोई भी custom headers।
* `media_type` - media type बताने वाली string। यदि unset है, तो media type infer करने के लिए filename या path का उपयोग किया जाएगा।
* `filename` - यदि set है, तो इसे response `Content-Disposition` में शामिल किया जाएगा।

File responses में उपयुक्त `Content-Length`, `Last-Modified` और `ETag` headers शामिल होंगे।

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

आप `response_class` parameter का उपयोग भी कर सकते हैं:

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

इस मामले में, आप अपनी *path operation* function से file path सीधे लौटा सकते हैं।

## Custom response class { #custom-response-class }

आप `Response` से inherit करके और उसका उपयोग करके अपनी खुद की custom response class बना सकते हैं।

उदाहरण के लिए, मान लें कि आप कुछ settings के साथ [`orjson`](https://github.com/ijl/orjson) का उपयोग करना चाहते हैं।

मान लें आप चाहते हैं कि यह indented और formatted JSON लौटाए, इसलिए आप orjson option `orjson.OPT_INDENT_2` का उपयोग करना चाहते हैं।

आप `CustomORJSONResponse` बना सकते हैं। आपको मुख्य रूप से `Response.render(content)` method बनाना है जो content को `bytes` के रूप में लौटाता है:

{* ../../docs_src/custom_response/tutorial009c_py310.py hl[9:14,17] *}

अब यह लौटाने के बजाय:

```json
{"message": "Hello World"}
```

...यह response लौटाएगा:

```json
{
  "message": "Hello World"
}
```

बेशक, JSON formatting की तुलना में इसका लाभ उठाने के लिए आपको शायद कहीं बेहतर तरीके मिलेंगे। 😉

### `orjson` या Response Model { #orjson-or-response-model }

यदि आप performance खोज रहे हैं, तो शायद `orjson` response की तुलना में [Response Model](../tutorial/response-model.md) का उपयोग करना आपके लिए बेहतर होगा।

Response model के साथ, FastAPI data को JSON में serialize करने के लिए Pydantic का उपयोग करेगा, intermediate steps के बिना, जैसे `jsonable_encoder` के साथ convert करना, जो किसी भी अन्य मामले में होता।

और अंदर से, Pydantic JSON में serialize करने के लिए `orjson` जैसे ही underlying Rust mechanisms का उपयोग करता है, इसलिए response model के साथ आपको पहले से ही best performance मिल जाएगी।

## Default response class { #default-response-class }

**FastAPI** class instance या `APIRouter` बनाते समय आप specify कर सकते हैं कि default रूप से कौन-सी response class उपयोग करनी है।

इसे define करने वाला parameter `default_response_class` है।

नीचे दिए गए उदाहरण में, **FastAPI** सभी *path operations* में JSON के बजाय default रूप से `HTMLResponse` का उपयोग करेगा।

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | टिप

आप पहले की तरह *path operations* में अब भी `response_class` override कर सकते हैं।

///

## अतिरिक्त documentation { #additional-documentation }

आप `responses` का उपयोग करके OpenAPI में media type और कई अन्य details भी declare कर सकते हैं: [OpenAPI में अतिरिक्त Responses](additional-responses.md)।
