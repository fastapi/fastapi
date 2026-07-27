# Testing { #testing }

[Starlette](https://www.starlette.dev/testclient/) की बदौलत, **FastAPI** applications की testing आसान और आनंददायक है।

यह [HTTPX](https://www.python-httpx.org) पर आधारित है, जो बदले में Requests के आधार पर design किया गया है, इसलिए यह बहुत परिचित और intuitive है।

इसके साथ, आप **FastAPI** के साथ सीधे [pytest](https://docs.pytest.org/) का उपयोग कर सकते हैं।

## `TestClient` का उपयोग करना { #using-testclient }

/// note | नोट

`TestClient` का उपयोग करने के लिए, पहले [`httpx`](https://www.python-httpx.org) install करें।

सुनिश्चित करें कि आप एक [virtual environment](../virtual-environments.md) बनाते हैं, उसे activate करते हैं, और फिर इसे install करते हैं, उदाहरण के लिए:

```console
$ pip install httpx
```

///

`TestClient` import करें।

अपनी **FastAPI** application को इसमें pass करके एक `TestClient` बनाएँ।

ऐसी functions बनाएँ जिनका नाम `test_` से शुरू होता हो (यह एक standard `pytest` convention है)।

`TestClient` object का उपयोग उसी तरह करें जैसे आप `httpx` के साथ करते हैं।

जिन चीज़ों की आपको जाँच करनी है उनके लिए standard Python expressions के साथ सरल `assert` statements लिखें (फिर से, standard `pytest`)।

{* ../../docs_src/app_testing/tutorial001_py310.py hl[2,12,15:18] *}

/// tip | टिप

ध्यान दें कि testing functions सामान्य `def` हैं, `async def` नहीं।

और client को की जाने वाली calls भी सामान्य calls हैं, `await` का उपयोग नहीं करतीं।

यह आपको बिना जटिलताओं के सीधे `pytest` का उपयोग करने देता है।

///

/// note | तकनीकी विवरण

आप `from starlette.testclient import TestClient` का भी उपयोग कर सकते हैं।

**FastAPI** आपकी सुविधा के लिए, developer के रूप में, उसी `starlette.testclient` को `fastapi.testclient` के रूप में प्रदान करता है। लेकिन यह सीधे Starlette से आता है।

///

/// tip | टिप

अगर आप अपनी FastAPI application को requests भेजने के अलावा अपने tests में `async` functions call करना चाहते हैं (जैसे asynchronous database functions), तो advanced tutorial में [Async Tests](../advanced/async-tests.md) देखें।

///

## Tests को अलग करना { #separating-tests }

एक वास्तविक application में, आपके tests शायद किसी अलग file में होंगे।

और आपकी **FastAPI** application भी कई files/modules आदि से मिलकर बनी हो सकती है।

### **FastAPI** app file { #fastapi-app-file }

मान लीजिए आपके पास [Bigger Applications](bigger-applications.md) में बताए गए अनुसार एक file structure है:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

`main.py` file में आपकी **FastAPI** app है:


{* ../../docs_src/app_testing/app_a_py310/main.py *}

### Testing file { #testing-file }

फिर आपके पास अपने tests के साथ एक file `test_main.py` हो सकती है। यह उसी Python package में हो सकती है (वही directory जिसमें `__init__.py` file है):

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

क्योंकि यह file उसी package में है, आप `main` module (`main.py`) से object `app` को import करने के लिए relative imports का उपयोग कर सकते हैं:

{* ../../docs_src/app_testing/app_a_py310/test_main.py hl[3] *}


...और tests के लिए code पहले जैसा ही रख सकते हैं।

## Testing: विस्तृत उदाहरण { #testing-extended-example }

अब इस उदाहरण को आगे बढ़ाते हैं और अलग-अलग हिस्सों की testing कैसे करनी है यह देखने के लिए और विवरण जोड़ते हैं।

### विस्तारित **FastAPI** app file { #extended-fastapi-app-file }

आइए पहले जैसी ही file structure के साथ जारी रखें:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

मान लीजिए अब आपकी **FastAPI** app वाली file `main.py` में कुछ अन्य **path operations** हैं।

इसमें एक `GET` operation है जो error return कर सकता है।

इसमें एक `POST` operation है जो कई errors return कर सकता है।

दोनों *path operations* को `X-Token` header required है।

{* ../../docs_src/app_testing/app_b_an_py310/main.py *}

### विस्तारित testing file { #extended-testing-file }

फिर आप विस्तारित tests के साथ `test_main.py` को update कर सकते हैं:

{* ../../docs_src/app_testing/app_b_an_py310/test_main.py *}


जब भी आपको client से request में जानकारी pass करवानी हो और आपको पता न हो कि कैसे, तो आप खोज (Google) सकते हैं कि इसे `httpx` में कैसे करें, या यहाँ तक कि `requests` के साथ कैसे करें, क्योंकि HTTPX का design Requests के design पर आधारित है।

फिर आप अपने tests में वही करते हैं।

उदाहरण के लिए:

* *path* या *query* parameter pass करने के लिए, इसे URL में ही जोड़ें।
* JSON body pass करने के लिए, `json` parameter में एक Python object (जैसे `dict`) pass करें।
* अगर आपको JSON के बजाय *Form Data* भेजना है, तो इसके बजाय `data` parameter का उपयोग करें।
* *headers* pass करने के लिए, `headers` parameter में एक `dict` का उपयोग करें।
* *cookies* के लिए, `cookies` parameter में एक `dict`।

backend को data कैसे pass करें (`httpx` या `TestClient` का उपयोग करके) इसके बारे में अधिक जानकारी के लिए [HTTPX documentation](https://www.python-httpx.org) देखें।

/// note | नोट

ध्यान दें कि `TestClient` ऐसा data receive करता है जिसे JSON में convert किया जा सकता है, Pydantic models नहीं।

अगर आपके test में एक Pydantic model है और आप testing के दौरान उसका data application को भेजना चाहते हैं, तो आप [JSON Compatible Encoder](encoder.md) में बताए गए `jsonable_encoder` का उपयोग कर सकते हैं।

///

## इसे चलाएँ { #run-it }

उसके बाद, आपको बस `pytest` install करना है।

सुनिश्चित करें कि आप एक [virtual environment](../virtual-environments.md) बनाते हैं, उसे activate करते हैं, और फिर इसे install करते हैं, उदाहरण के लिए:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

यह files और tests को automatically detect करेगा, उन्हें execute करेगा, और results आपको वापस report करेगा।

Tests चलाएँ:

<div class="termy">

```console
$ pytest

================ test session starts ================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/user/code/superawesome-cli/app
plugins: forked-1.1.3, xdist-1.31.0, cov-2.8.1
collected 6 items

---> 100%

test_main.py <span style="color: green; white-space: pre;">......                            [100%]</span>

<span style="color: green;">================= 1 passed in 0.03s =================</span>
```

</div>
