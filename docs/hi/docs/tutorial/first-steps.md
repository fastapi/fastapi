# पहले कदम { #first-steps }

सबसे सरल FastAPI फ़ाइल कुछ इस तरह दिख सकती है:

{* ../../docs_src/first_steps/tutorial001_py310.py *}

इसे एक फ़ाइल `main.py` में कॉपी करें।

लाइव सर्वर चलाएँ:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

आउटपुट में, कुछ इस तरह की एक लाइन होगी:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

वह लाइन वो URL दिखाती है जहाँ आपका ऐप आपकी लोकल मशीन पर सर्व हो रहा है।

### इसे जाँचें { #check-it }

अपना ब्राउज़र [http://127.0.0.1:8000](http://127.0.0.1:8000) पर खोलें।

आपको JSON रिस्पॉन्स इस तरह दिखेगा:

```JSON
{"message": "Hello World"}
```

### इंटरैक्टिव API डॉक्स { #interactive-api-docs }

अब [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) पर जाएँ।

आपको ऑटोमैटिक इंटरैक्टिव API डॉक्यूमेंटेशन दिखेगा (जो [Swagger UI](https://github.com/swagger-api/swagger-ui) द्वारा प्रदान किया गया है):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### वैकल्पिक API डॉक्स { #alternative-api-docs }

और अब, [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) पर जाएँ।

आपको वैकल्पिक ऑटोमैटिक डॉक्यूमेंटेशन दिखेगा (जो [ReDoc](https://github.com/Rebilly/ReDoc) द्वारा प्रदान किया गया है):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI** आपके सभी API का एक "schema" जनरेट करता है, जो API को परिभाषित करने के लिए **OpenAPI** स्टैंडर्ड का उपयोग करता है।

#### "Schema" { #schema }

"Schema" किसी चीज़ की परिभाषा या विवरण है। यह उसे लागू करने वाला कोड नहीं है, बल्कि सिर्फ एक ऐब्स्ट्रैक्ट विवरण है।

#### API "Schema" { #api-schema }

इस मामले में, [OpenAPI](https://github.com/OAI/OpenAPI-Specification) एक स्पेसिफिकेशन है जो यह तय करता है कि आपके API का schema कैसे परिभाषित किया जाए।

इस schema परिभाषा में आपके API paths, उनके संभावित पैरामीटर्स आदि शामिल हैं।

#### Data "Schema" { #data-schema }

"Schema" शब्द किसी डेटा के आकार को भी संदर्भित कर सकता है, जैसे JSON कंटेंट।

उस स्थिति में, इसका मतलब JSON एट्रिब्यूट्स और उनके डेटा टाइप्स आदि होगा।

#### OpenAPI और JSON Schema { #openapi-and-json-schema }

OpenAPI आपके API के लिए एक API schema परिभाषित करता है। और उस schema में आपके API द्वारा भेजे और प्राप्त किए गए डेटा की परिभाषाएँ (या "schemas") शामिल हैं, जो **JSON Schema** का उपयोग करती हैं — JSON डेटा schemas के लिए स्टैंडर्ड।

#### `openapi.json` देखें { #check-the-openapi-json }

अगर आप जानना चाहते हैं कि रॉ OpenAPI schema कैसा दिखता है, तो FastAPI ऑटोमैटिकली आपके सभी API के विवरण के साथ एक JSON (schema) जनरेट करता है।

आप इसे सीधे यहाँ देख सकते हैं: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)।

यह कुछ इस तरह शुरू होने वाला JSON दिखाएगा:

```JSON
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### OpenAPI किसके लिए है { #what-is-openapi-for }

OpenAPI schema वही है जो शामिल किए गए दोनों इंटरैक्टिव डॉक्यूमेंटेशन सिस्टम को पावर करता है।

और OpenAPI पर आधारित दर्जनों विकल्प मौजूद हैं। आप **FastAPI** से बने अपने एप्लिकेशन में उनमें से किसी को भी आसानी से जोड़ सकते हैं।

आप इसका उपयोग अपने API से कम्यूनिकेट करने वाले क्लाइंट्स के लिए ऑटोमैटिकली कोड जनरेट करने में भी कर सकते हैं। उदाहरण के लिए, फ्रंटएंड, मोबाइल या IoT एप्लिकेशन।

### `pyproject.toml` में ऐप `entrypoint` कॉन्फ़िगर करें { #configure-the-app-entrypoint-in-pyproject-toml }

आप `pyproject.toml` फ़ाइल में अपने ऐप की लोकेशन इस तरह कॉन्फ़िगर कर सकते हैं:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

वह `entrypoint`, `fastapi` कमांड को बताएगा कि उसे ऐप को इस तरह इम्पोर्ट करना चाहिए:

```python
from main import app
```

अगर आपके कोड का स्ट्रक्चर इस तरह है:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

तो आप `entrypoint` इस तरह सेट करेंगे:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

जो इसके बराबर होगा:

```python
from backend.main import app
```

### `fastapi dev` path के साथ या `--entrypoint` CLI ऑप्शन के साथ { #fastapi-dev-with-path-or-with-entrypoint-cli-option }

आप `fastapi dev` कमांड को फ़ाइल पाथ भी पास कर सकते हैं, और यह उपयोग करने के लिए FastAPI ऐप ऑब्जेक्ट का अनुमान लगाएगा:

```console
$ fastapi dev main.py
```

या, आप `fastapi dev` कमांड को `--entrypoint` ऑप्शन भी पास कर सकते हैं:

```console
$ fastapi dev --entrypoint main:app
```

लेकिन आपको हर बार `fastapi` कमांड चलाते समय सही path\entrypoint पास करना याद रखना होगा।

इसके अलावा, अन्य टूल्स इसे ढूंढ़ नहीं पाएंगे, उदाहरण के लिए [VS Code Extension](../editor-support.md) या [FastAPI Cloud](https://fastapicloud.com), इसलिए `pyproject.toml` में `entrypoint` का उपयोग करना अनुशंसित है।

### अपना ऐप डिप्लॉय करें (वैकल्पिक) { #deploy-your-app-optional }

आप वैकल्पिक रूप से अपने FastAPI ऐप को [FastAPI Cloud](https://fastapicloud.com) पर एक ही कमांड से डिप्लॉय कर सकते हैं। 🚀

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

CLI ऑटोमैटिकली आपके FastAPI एप्लिकेशन का पता लगाएगा और इसे क्लाउड पर डिप्लॉय करेगा। अगर आप लॉग इन नहीं हैं, तो ऑथेंटिकेशन प्रक्रिया पूरी करने के लिए आपका ब्राउज़र खुलेगा।

बस इतना ही! अब आप उस URL पर अपना ऐप एक्सेस कर सकते हैं। ✨

## संक्षेप, कदम दर कदम { #recap-step-by-step }

### चरण 1: `FastAPI` इम्पोर्ट करें { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[1] *}

`FastAPI` एक Python क्लास है जो आपके API के लिए सभी फंक्शनैलिटी प्रदान करती है।

/// note | तकनीकी विवरण

`FastAPI` एक क्लास है जो सीधे `Starlette` से इनहेरिट करती है।

आप `FastAPI` के साथ [Starlette](https://www.starlette.dev/) की सभी फंक्शनैलिटी का उपयोग कर सकते हैं।

///

### चरण 2: एक `FastAPI` "इंस्टेंस" बनाएँ { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[3] *}

यहाँ `app` वेरिएबल `FastAPI` क्लास का एक "इंस्टेंस" होगा।

यह आपके सभी API बनाने के लिए इंटरैक्शन का मुख्य पॉइंट होगा।

### चरण 3: एक *path operation* बनाएँ { #step-3-create-a-path-operation }

#### Path { #path }

यहाँ "Path" का मतलब URL के अंतिम भाग से है जो पहले `/` से शुरू होता है।

तो, इस तरह के URL में:

```
https://example.com/items/foo
```

...path यह होगा:

```
/items/foo
```

/// note

"Path" को आमतौर पर "endpoint" या "route" भी कहा जाता है।

///

API बनाते समय, "path" "concerns" और "resources" को अलग करने का मुख्य तरीका है।

#### Operation { #operation }

यहाँ "Operation" का मतलब HTTP "methods" में से एक है।

इनमें से एक:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...और अधिक दुर्लभ:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

HTTP प्रोटोकॉल में, आप इन "methods" में से एक (या अधिक) का उपयोग करके प्रत्येक path से कम्यूनिकेट कर सकते हैं।

---

API बनाते समय, आप आमतौर पर एक विशिष्ट कार्य करने के लिए इन विशिष्ट HTTP methods का उपयोग करते हैं।

सामान्यतः आप उपयोग करते हैं:

* `POST`: डेटा बनाने के लिए।
* `GET`: डेटा पढ़ने के लिए।
* `PUT`: डेटा अपडेट करने के लिए।
* `DELETE`: डेटा हटाने के लिए।

तो, OpenAPI में, प्रत्येक HTTP method को एक "operation" कहा जाता है।

हम भी इन्हें "**operations**" कहेंगे।

#### एक *path operation decorator* परिभाषित करें { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[6] *}

`@app.get("/")` **FastAPI** को बताता है कि नीचे वाला फंक्शन इन रिक्वेस्ट्स को हैंडल करने के लिए ज़िम्मेदार है जो यहाँ जाती हैं:

* path `/`
* <dfn title="an HTTP GET method"><code>get</code> operation</dfn> का उपयोग करके

/// note | `@decorator` जानकारी

Python में वो `@something` सिंटैक्स "decorator" कहलाता है।

आप इसे एक फंक्शन के ऊपर रखते हैं। जैसे एक सुंदर सजावटी टोपी (मुझे लगता है कि यह नाम वहीं से आया है)।

एक "decorator" नीचे वाले फंक्शन को लेता है और उसके साथ कुछ करता है।

हमारे मामले में, यह decorator **FastAPI** को बताता है कि नीचे वाला फंक्शन **path** `/` और **operation** `get` से संबंधित है।

यह "**path operation decorator**" है।

///

आप अन्य operations का भी उपयोग कर सकते हैं:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

और अधिक दुर्लभ:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip

आप प्रत्येक operation (HTTP method) का जैसे चाहें उपयोग कर सकते हैं।

**FastAPI** कोई विशिष्ट अर्थ लागू नहीं करता।

यहाँ दी गई जानकारी एक दिशानिर्देश के रूप में प्रस्तुत की गई है, आवश्यकता नहीं।

उदाहरण के लिए, GraphQL का उपयोग करते समय आप सामान्यतः सभी कार्य केवल `POST` operations का उपयोग करके करते हैं।

///

### चरण 4: **path operation function** परिभाषित करें { #step-4-define-the-path-operation-function }

यह हमारा "**path operation function**" है:

* **path**: `/` है।
* **operation**: `get` है।
* **function**: "decorator" के नीचे वाला फंक्शन है (`@app.get("/")` के नीचे)।

{* ../../docs_src/first_steps/tutorial001_py310.py hl[7] *}

यह एक Python फंक्शन है।

जब भी **FastAPI** को `GET` operation का उपयोग करके URL "`/`" पर रिक्वेस्ट मिलेगी, तब यह इस फंक्शन को कॉल करेगा।

इस मामले में, यह एक `async` फंक्शन है।

---

आप इसे `async def` के बजाय एक सामान्य फंक्शन के रूप में भी परिभाषित कर सकते हैं:

{* ../../docs_src/first_steps/tutorial003_py310.py hl[7] *}

/// note

अगर आपको अंतर नहीं पता, तो [Async: *"जल्दी में?"*](../async.md#in-a-hurry) देखें।

///

### चरण 5: कंटेंट रिटर्न करें { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[8] *}

आप `dict`, `list`, सिंगुलर वैल्यूज़ जैसे `str`, `int`, आदि रिटर्न कर सकते हैं।

आप Pydantic मॉडल्स भी रिटर्न कर सकते हैं (इसके बारे में आप बाद में और जानेंगे)।

कई अन्य ऑब्जेक्ट्स और मॉडल्स हैं जो ऑटोमैटिकली JSON में कन्वर्ट हो जाएंगे (ORMs सहित, आदि)। अपने पसंदीदा का उपयोग करके देखें, बहुत संभव है कि वे पहले से सपोर्टेड हैं।

### चरण 6: इसे डिप्लॉय करें { #step-6-deploy-it }

अपने ऐप को **[FastAPI Cloud](https://fastapicloud.com)** पर एक कमांड से डिप्लॉय करें: `fastapi deploy`। 🎉

#### FastAPI Cloud के बारे में { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** उसी लेखक और टीम द्वारा बनाया गया है जो **FastAPI** के पीछे है।

यह न्यूनतम प्रयास के साथ API को **बनाने**, **डिप्लॉय करने** और **एक्सेस करने** की प्रक्रिया को सरल बनाता है।

यह FastAPI के साथ ऐप्स बनाने का वही **डेवलपर अनुभव** क्लाउड पर **डिप्लॉय करने** में लाता है। 🎉

FastAPI Cloud, *FastAPI and friends* ओपन सोर्स प्रोजेक्ट्स का प्राथमिक स्पॉन्सर और फंडिंग प्रदाता है। ✨

#### अन्य क्लाउड प्रोवाइडर्स पर डिप्लॉय करें { #deploy-to-other-cloud-providers }

FastAPI ओपन सोर्स है और स्टैंडर्ड्स पर आधारित है। आप FastAPI ऐप्स को अपनी पसंद के किसी भी क्लाउड प्रोवाइडर पर डिप्लॉय कर सकते हैं।

FastAPI ऐप्स को उनके साथ डिप्लॉय करने के लिए अपने क्लाउड प्रोवाइडर की गाइड्स का पालन करें। 🤓

## संक्षेप { #recap }

* `FastAPI` इम्पोर्ट करें।
* एक `app` इंस्टेंस बनाएँ।
* `@app.get("/")` जैसे decorators का उपयोग करके एक **path operation decorator** लिखें।
* एक **path operation function** परिभाषित करें; उदाहरण के लिए, `def root(): ...`।
* `fastapi dev` कमांड का उपयोग करके डेवलपमेंट सर्वर चलाएँ।
* वैकल्पिक रूप से `fastapi deploy` से अपना ऐप डिप्लॉय करें।