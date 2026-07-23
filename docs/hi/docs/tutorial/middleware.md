# Middleware { #middleware }

आप **FastAPI** applications में middleware जोड़ सकते हैं।

"middleware" एक function है जो हर **request** के साथ काम करता है, इससे पहले कि उसे किसी विशेष *path operation* द्वारा process किया जाए। और हर **response** के साथ भी, उसे लौटाने से पहले।

* यह आपके application में आने वाली हर **request** लेता है।
* फिर यह उस **request** के साथ कुछ कर सकता है या कोई required code चला सकता है।
* फिर यह **request** को application के बाकी हिस्से द्वारा process होने के लिए आगे भेजता है (किसी *path operation* द्वारा)।
* फिर यह application द्वारा generate किया गया **response** लेता है (किसी *path operation* द्वारा)।
* यह उस **response** के साथ कुछ कर सकता है या कोई required code चला सकता है।
* फिर यह **response** लौटाता है।

/// note | तकनीकी विवरण

अगर आपके पास `yield` वाली dependencies हैं, तो exit code middleware के *बाद* चलेगा।

अगर कोई background tasks थे ([Background Tasks](background-tasks.md) section में कवर किया गया है, आप इसे बाद में देखेंगे), तो वे सभी middleware के *बाद* चलेंगे।

///

## Middleware बनाएं { #create-a-middleware }

middleware बनाने के लिए आप किसी function के ऊपर decorator `@app.middleware("http")` का उपयोग करते हैं।

middleware function को मिलता है:

* `request`।
* एक function `call_next` जो `request` को parameter के रूप में प्राप्त करेगा।
    * यह function `request` को संबंधित *path operation* तक पास करेगा।
    * फिर यह संबंधित *path operation* द्वारा generate किया गया `response` लौटाता है।
* फिर आप `response` लौटाने से पहले उसे और modify कर सकते हैं।

{* ../../docs_src/middleware/tutorial001_py310.py hl[8:9,11,14] *}

/// tip | सुझाव

ध्यान रखें कि custom proprietary headers को [`X-` prefix का उपयोग करके](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) जोड़ा जा सकता है।

लेकिन अगर आपके पास custom headers हैं जिन्हें आप browser में client को दिखाना चाहते हैं, तो आपको उन्हें अपने CORS configurations ([CORS (Cross-Origin Resource Sharing)](cors.md)) में `expose_headers` parameter का उपयोग करके जोड़ना होगा, जैसा कि [Starlette के CORS docs](https://www.starlette.dev/middleware/#corsmiddleware) में documented है।

///

/// note | तकनीकी विवरण

आप `from starlette.requests import Request` भी उपयोग कर सकते हैं।

**FastAPI** इसे आपके लिए, developer की सुविधा के रूप में provide करता है। लेकिन यह सीधे Starlette से आता है।

///

### `response` से पहले और बाद में { #before-and-after-the-response }

आप `request` के साथ चलाने के लिए code जोड़ सकते हैं, इससे पहले कि कोई *path operation* उसे प्राप्त करे।

और `response` generate होने के बाद भी, उसे लौटाने से पहले।

उदाहरण के लिए, आप एक custom header `X-Process-Time` जोड़ सकते हैं जिसमें seconds में वह time हो जो request को process करने और response generate करने में लगा:

{* ../../docs_src/middleware/tutorial001_py310.py hl[10,12:13] *}

/// tip | सुझाव

यहाँ हम `time.time()` के बजाय [`time.perf_counter()`](https://docs.python.org/3/library/time.html#time.perf_counter) का उपयोग करते हैं क्योंकि यह इन use cases के लिए अधिक precise हो सकता है। 🤓

///

## कई middleware का execution order { #multiple-middleware-execution-order }

जब आप `@app.middleware()` decorator या `app.add_middleware()` method का उपयोग करके कई middleware जोड़ते हैं, तो हर नया middleware application को wrap करता है, जिससे एक stack बनता है। जो middleware अंत में जोड़ा जाता है वह *outermost* होता है, और पहला *innermost* होता है।

request path पर, *outermost* middleware पहले चलता है।

response path पर, यह अंत में चलता है।

उदाहरण के लिए:

```Python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

इससे execution order यह होता है:

* **Request**: MiddlewareB → MiddlewareA → route

* **Response**: route → MiddlewareA → MiddlewareB

यह stacking behavior सुनिश्चित करता है कि middleware एक predictable और controllable order में execute हों।

## अन्य middleware { #other-middlewares }

आप बाद में [Advanced User Guide: Advanced Middleware](../advanced/middleware.md) में अन्य middleware के बारे में और पढ़ सकते हैं।

आप अगले section में middleware के साथ <abbr title="Cross-Origin Resource Sharing - क्रॉस-ओरिजिन रिसोर्स शेयरिंग">CORS</abbr> को handle करने के बारे में पढ़ेंगे।
