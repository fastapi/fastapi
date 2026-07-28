# Async Tests { #async-tests }

आपने पहले ही देखा है कि दिए गए `TestClient` का उपयोग करके अपनी **FastAPI** applications को कैसे test किया जाता है। अब तक, आपने केवल synchronous tests लिखना देखा है, `async` functions का उपयोग किए बिना।

अपने tests में asynchronous functions का उपयोग कर पाना उपयोगी हो सकता है, उदाहरण के लिए, जब आप अपने database को asynchronously query कर रहे हों। कल्पना करें कि आप अपनी FastAPI application को requests भेजना test करना चाहते हैं और फिर verify करना चाहते हैं कि आपके backend ने async database library का उपयोग करते हुए database में सही data सफलतापूर्वक लिखा है।

आइए देखें कि हम इसे कैसे काम करवा सकते हैं।

## pytest.mark.anyio { #pytest-mark-anyio }

अगर हम अपने tests में asynchronous functions call करना चाहते हैं, तो हमारे test functions asynchronous होने चाहिए। AnyIO इसके लिए एक अच्छा plugin प्रदान करता है, जो हमें specify करने देता है कि कुछ test functions को asynchronously call किया जाना है।

## HTTPX { #httpx }

भले ही आपकी **FastAPI** application `async def` के बजाय सामान्य `def` functions का उपयोग करती हो, यह अंदर से फिर भी एक `async` application होती है।

`TestClient` अंदर कुछ magic करता है ताकि standard pytest का उपयोग करते हुए आपकी सामान्य `def` test functions में asynchronous FastAPI application को call किया जा सके। लेकिन जब हम इसे asynchronous functions के अंदर उपयोग करते हैं, तो वह magic अब काम नहीं करता। अपने tests को asynchronously चलाने पर, हम अपने test functions के अंदर `TestClient` का उपयोग नहीं कर सकते।

`TestClient` [HTTPX](https://www.python-httpx.org) पर आधारित है, और सौभाग्य से, हम API को test करने के लिए इसे सीधे उपयोग कर सकते हैं।

## उदाहरण { #example }

एक सरल उदाहरण के लिए, आइए [बड़ी Applications](../tutorial/bigger-applications.md) और [Testing](../tutorial/testing.md) में वर्णित file structure जैसी एक structure पर विचार करें:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

file `main.py` में यह होगा:

{* ../../docs_src/async_tests/app_a_py310/main.py *}

file `test_main.py` में `main.py` के लिए tests होंगे, यह अब कुछ ऐसा दिख सकता है:

{* ../../docs_src/async_tests/app_a_py310/test_main.py *}

## इसे चलाएँ { #run-it }

आप अपने tests को हमेशा की तरह इस तरह चला सकते हैं:

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## विस्तार से { #in-detail }

marker `@pytest.mark.anyio` pytest को बताता है कि इस test function को asynchronously call किया जाना चाहिए:

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[7] *}

/// tip | सुझाव

ध्यान दें कि test function अब पहले की तरह `TestClient` का उपयोग करते समय केवल `def` नहीं, बल्कि `async def` है।

///

फिर हम app के साथ एक `AsyncClient` बना सकते हैं, और `await` का उपयोग करते हुए इसमें async requests भेज सकते हैं।

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[9:12] *}

यह इसके बराबर है:

```Python
response = client.get('/')
```

...जिसका उपयोग हम `TestClient` के साथ अपनी requests बनाने के लिए करते थे।

/// tip | सुझाव

ध्यान दें कि हम नए `AsyncClient` के साथ async/await का उपयोग कर रहे हैं - request asynchronous है।

///

/// warning | चेतावनी

अगर आपकी application lifespan events पर निर्भर करती है, तो `AsyncClient` इन events को trigger नहीं करेगा। यह सुनिश्चित करने के लिए कि वे trigger हों, [florimondmanca/asgi-lifespan](https://github.com/florimondmanca/asgi-lifespan#usage) से `LifespanManager` का उपयोग करें।

///

## अन्य asynchronous function calls { #other-asynchronous-function-calls }

क्योंकि testing function अब asynchronous है, आप अब अपने tests में अपनी FastAPI application को requests भेजने के अलावा अन्य `async` functions को भी call (और `await`) कर सकते हैं, ठीक वैसे ही जैसे आप उन्हें अपने code में कहीं और call करते हैं।

/// tip | सुझाव

अगर अपने tests में asynchronous function calls integrate करते समय आपको `RuntimeError: Task attached to a different loop` मिलता है (जैसे [MongoDB's MotorClient](https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop) का उपयोग करते समय), तो याद रखें कि जिन objects को event loop की जरूरत होती है, उन्हें केवल async functions के भीतर ही instantiate करें, जैसे कि `@app.on_event("startup")` callback।

///
