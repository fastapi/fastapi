# WebSockets { #websockets }

आप **FastAPI** के साथ [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) का उपयोग कर सकते हैं।

## `websockets` install करें { #install-websockets }

सुनिश्चित करें कि आप एक [virtual environment](../virtual-environments.md) बनाएँ, उसे activate करें, और `websockets` install करें (एक Python library जो "WebSocket" protocol का उपयोग आसान बनाती है):

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## WebSockets client { #websockets-client }

### production में { #in-production }

आपके production system में, संभवतः आपके पास React, Vue.js या Angular जैसे आधुनिक framework से बना frontend होगा।

और अपने backend के साथ WebSockets का उपयोग करके संवाद करने के लिए आप संभवतः अपने frontend की utilities का उपयोग करेंगे।

या आपके पास एक native mobile application हो सकती है जो सीधे native code में आपके WebSocket backend से संवाद करती हो।

या आपके पास WebSocket endpoint से संवाद करने का कोई और तरीका हो सकता है।

---

लेकिन इस उदाहरण के लिए, हम कुछ JavaScript के साथ एक बहुत सरल HTML document का उपयोग करेंगे, सब कुछ एक लंबी string के अंदर।

बेशक, यह optimal नहीं है और आप इसे production के लिए उपयोग नहीं करेंगे।

production में आपके पास ऊपर दिए गए विकल्पों में से एक होगा।

लेकिन WebSockets के server-side पर ध्यान केंद्रित करने और एक working उदाहरण पाने का यह सबसे सरल तरीका है:

{* ../../docs_src/websockets_/tutorial001_py310.py hl[2,6:38,41:43] *}

## एक `websocket` बनाएँ { #create-a-websocket }

अपने **FastAPI** application में, एक `websocket` बनाएँ:

{* ../../docs_src/websockets_/tutorial001_py310.py hl[1,46:47] *}

/// note | तकनीकी विवरण

आप `from starlette.websockets import WebSocket` का भी उपयोग कर सकते हैं।

**FastAPI** वही `WebSocket` सीधे उपलब्ध कराता है, सिर्फ़ आपकी सुविधा के लिए, developer के रूप में। लेकिन यह सीधे Starlette से आता है।

///

## messages का await करें और messages भेजें { #await-for-messages-and-send-messages }

अपने WebSocket route में आप messages के लिए `await` कर सकते हैं और messages भेज सकते हैं।

{* ../../docs_src/websockets_/tutorial001_py310.py hl[48:52] *}

आप binary, text, और JSON data receive और send कर सकते हैं।

## इसे आज़माएँ { #try-it }

अपना code `main.py` file में रखें और फिर अपना application चलाएँ:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

अपने browser में [http://127.0.0.1:8000](http://127.0.0.1:8000) खोलें।

आपको ऐसा एक सरल page दिखेगा:

<img src="/img/tutorial/websockets/image01.png">

आप input box में messages टाइप कर सकते हैं, और उन्हें भेज सकते हैं:

<img src="/img/tutorial/websockets/image02.png">

और WebSockets के साथ आपका **FastAPI** application जवाब देगा:

<img src="/img/tutorial/websockets/image03.png">

आप कई messages भेज (और receive कर) सकते हैं:

<img src="/img/tutorial/websockets/image04.png">

और वे सभी उसी WebSocket connection का उपयोग करेंगे।

## `Depends` और अन्य का उपयोग { #using-depends-and-others }

WebSocket endpoints में आप `fastapi` से import कर सकते हैं और उपयोग कर सकते हैं:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

वे अन्य FastAPI endpoints/*path operations* की तरह ही काम करते हैं:

{* ../../docs_src/websockets_/tutorial002_an_py310.py hl[68:69,82] *}

/// note | नोट

क्योंकि यह एक WebSocket है, इसलिए `HTTPException` raise करना वास्तव में उचित नहीं है, इसके बजाय हम `WebSocketException` raise करते हैं।

आप [specification में परिभाषित valid codes](https://tools.ietf.org/html/rfc6455#section-7.4.1) में से एक closing code का उपयोग कर सकते हैं।

///

### dependencies के साथ WebSockets आज़माएँ { #try-the-websockets-with-dependencies }

अपना application चलाएँ:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

अपने browser में [http://127.0.0.1:8000](http://127.0.0.1:8000) खोलें।

वहाँ आप सेट कर सकते हैं:

* path में उपयोग किया गया "Item ID"।
* query parameter के रूप में उपयोग किया गया "Token"।

/// tip | सुझाव

ध्यान दें कि query `token` को एक dependency द्वारा handle किया जाएगा।

///

इसके साथ आप WebSocket connect कर सकते हैं और फिर messages भेज और receive कर सकते हैं:

<img src="/img/tutorial/websockets/image05.png">

## disconnections और कई clients को handle करना { #handling-disconnections-and-multiple-clients }

जब WebSocket connection बंद होता है, तो `await websocket.receive_text()` एक `WebSocketDisconnect` exception raise करेगा, जिसे आप इस उदाहरण की तरह catch और handle कर सकते हैं।

{* ../../docs_src/websockets_/tutorial003_py310.py hl[79:81] *}

इसे आज़माने के लिए:

* app को कई browser tabs में खोलें।
* उनसे messages लिखें।
* फिर tabs में से एक को बंद करें।

इससे `WebSocketDisconnect` exception raise होगा, और बाकी सभी clients को ऐसा message मिलेगा:

```
Client #1596980209979 left the chat
```

/// tip | सुझाव

ऊपर दिया गया app एक minimal और सरल उदाहरण है, जो दिखाता है कि कई WebSocket connections को messages कैसे handle और broadcast किए जाएँ।

लेकिन ध्यान रखें कि, चूँकि सब कुछ memory में, एक ही list में handle किया जाता है, यह केवल तब तक काम करेगा जब तक process चल रहा है, और केवल एक single process के साथ काम करेगा।

अगर आपको कुछ ऐसा चाहिए जिसे FastAPI के साथ integrate करना आसान हो लेकिन जो अधिक robust हो, Redis, PostgreSQL या अन्य द्वारा supported हो, तो [encode/broadcaster](https://github.com/encode/broadcaster) देखें।

///

## अधिक जानकारी { #more-info }

विकल्पों के बारे में अधिक जानने के लिए, इनके लिए Starlette का documentation देखें:

* [`WebSocket` class](https://www.starlette.dev/websockets/)।
* [Class-based WebSocket handling](https://www.starlette.dev/endpoints/#websocketendpoint)।
