# Custom Request और APIRoute class { #custom-request-and-apiroute-class }

कुछ मामलों में, आप `Request` और `APIRoute` classes द्वारा उपयोग किए जाने वाले logic को override करना चाह सकते हैं।

विशेष रूप से, यह middleware में logic का एक अच्छा विकल्प हो सकता है।

उदाहरण के लिए, अगर आप request body को आपके application द्वारा process किए जाने से पहले पढ़ना या manipulate करना चाहते हैं।

/// danger | खतरा

यह एक "advanced" feature है।

अगर आप अभी-अभी **FastAPI** के साथ शुरुआत कर रहे हैं, तो शायद आप इस section को छोड़ना चाहेंगे।

///

## Use cases { #use-cases }

कुछ use cases में शामिल हैं:

* non-JSON request bodies को JSON में convert करना (जैसे [`msgpack`](https://msgpack.org/index.html)).
* gzip-compressed request bodies को decompress करना।
* सभी request bodies को automatically log करना।

## Custom request body encodings को संभालना { #handling-custom-request-body-encodings }

आइए देखें कि gzip requests को decompress करने के लिए custom `Request` subclass का उपयोग कैसे करें।

और उस custom request class का उपयोग करने के लिए एक `APIRoute` subclass।

### Custom `GzipRequest` class बनाएँ { #create-a-custom-gziprequest-class }

/// tip | सुझाव

यह दिखाने के लिए एक सरल उदाहरण है कि यह कैसे काम करता है, अगर आपको Gzip support चाहिए, तो आप दिए गए [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware) का उपयोग कर सकते हैं।

///

सबसे पहले, हम एक `GzipRequest` class बनाते हैं, जो उपयुक्त header की मौजूदगी में body को decompress करने के लिए `Request.body()` method को overwrite करेगी।

अगर header में `gzip` नहीं है, तो यह body को decompress करने की कोशिश नहीं करेगी।

इस तरह, वही route class gzip compressed या uncompressed requests को संभाल सकती है।

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[9:16] *}

### Custom `GzipRoute` class बनाएँ { #create-a-custom-gziproute-class }

इसके बाद, हम `fastapi.routing.APIRoute` की एक custom subclass बनाते हैं जो `GzipRequest` का उपयोग करेगी।

इस बार, यह `APIRoute.get_route_handler()` method को overwrite करेगी।

यह method एक function return करता है। और वही function एक request प्राप्त करेगा और response return करेगा।

यहाँ हम इसका उपयोग original request से `GzipRequest` बनाने के लिए करते हैं।

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[19:27] *}

/// note | तकनीकी विवरण

एक `Request` में `request.scope` attribute होता है, जो बस एक Python `dict` है जिसमें request से संबंधित metadata होता है।

एक `Request` में `request.receive` भी होता है, जो request की body को "receive" करने के लिए एक function है।

`scope` `dict` और `receive` function दोनों ASGI specification का हिस्सा हैं।

और ये दो चीजें, `scope` और `receive`, नई `Request` instance बनाने के लिए आवश्यक हैं।

`Request` के बारे में अधिक जानने के लिए [Requests के बारे में Starlette के docs](https://www.starlette.dev/requests/) देखें।

///

`GzipRequest.get_route_handler` द्वारा return किए गए function का केवल एक अलग काम है: `Request` को `GzipRequest` में convert करना।

ऐसा करने से, हमारा `GzipRequest` data को हमारे *path operations* तक पास करने से पहले decompress करने का ध्यान रखेगा (अगर आवश्यक हो)।

उसके बाद, processing logic सब वही रहता है।

लेकिन `GzipRequest.body` में हमारे बदलावों की वजह से, request body जरूरत पड़ने पर **FastAPI** द्वारा load किए जाने पर automatically decompress हो जाएगी।

## Exception handler में request body तक पहुँचना { #accessing-the-request-body-in-an-exception-handler }

/// tip | सुझाव

इसी समस्या को हल करने के लिए, `RequestValidationError` के custom handler में `body` का उपयोग करना शायद बहुत आसान है ([Errors संभालना](../tutorial/handling-errors.md#use-the-requestvalidationerror-body))।

लेकिन यह उदाहरण अभी भी valid है और यह दिखाता है कि internal components के साथ कैसे interact करें।

///

हम इसी approach का उपयोग exception handler में request body तक पहुँचने के लिए भी कर सकते हैं।

हमें बस request को `try`/`except` block के अंदर संभालना है:

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[14,16] *}

अगर कोई exception होता है, तो `Request` instance अभी भी scope में होगी, इसलिए error संभालते समय हम request body को पढ़ सकते हैं और उसका उपयोग कर सकते हैं:

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[17:19] *}

## Router में custom `APIRoute` class { #custom-apiroute-class-in-a-router }

आप `APIRouter` का `route_class` parameter भी set कर सकते हैं:

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[26] *}

इस उदाहरण में, `router` के अंतर्गत *path operations* custom `TimedRoute` class का उपयोग करेंगे, और response में एक अतिरिक्त `X-Response-Time` header होगा जिसमें response generate करने में लगा समय होगा:

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[13:20] *}
