# पहले कदम { #first-steps }

सबसे सरल FastAPI file ऐसी दिख सकती है:

{* ../../docs_src/first_steps/tutorial001_py310.py *}

इसे `main.py` नाम की file में copy करें।

live server चलाएँ:

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

output में, कुछ ऐसी एक line होती है:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

यह line वह URL दिखाती है जहाँ आपकी app आपकी local machine पर serve की जा रही है।

### इसे जाँचें { #check-it }

अपने browser में [http://127.0.0.1:8000](http://127.0.0.1:8000) खोलें।

आपको JSON response इस तरह दिखेगा:

```JSON
{"message": "Hello World"}
```

### Interactive API docs { #interactive-api-docs }

अब [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) पर जाएँ।

आपको automatic interactive API documentation दिखेगी ([Swagger UI](https://github.com/swagger-api/swagger-ui) द्वारा प्रदान की गई):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### वैकल्पिक API docs { #alternative-api-docs }

और अब, [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) पर जाएँ।

आपको वैकल्पिक automatic documentation दिखेगी ([ReDoc](https://github.com/Rebilly/ReDoc) द्वारा प्रदान की गई):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI** APIs को define करने के लिए **OpenAPI** standard का उपयोग करके आपकी पूरी API के साथ एक "schema" generate करता है।

#### "Schema" { #schema }

"schema" किसी चीज़ की definition या description है। वह code नहीं जो इसे implement करता है, बल्कि सिर्फ़ एक abstract description है।

#### API "schema" { #api-schema }

इस मामले में, [OpenAPI](https://github.com/OAI/OpenAPI-Specification) एक specification है जो बताती है कि आपकी API का schema कैसे define करना है।

इस schema definition में आपकी API paths, उनके द्वारा लिए जा सकने वाले संभावित parameters आदि शामिल होते हैं।

#### Data "schema" { #data-schema }

"schema" शब्द कुछ data के आकार को भी refer कर सकता है, जैसे JSON content।

उस मामले में, इसका मतलब JSON attributes, और उनके data types आदि होगा।

#### OpenAPI और JSON Schema { #openapi-and-json-schema }

OpenAPI आपकी API के लिए API schema define करता है। और उस schema में **JSON Schema**, जो JSON data schemas के लिए standard है, का उपयोग करके आपकी API द्वारा भेजे और प्राप्त किए गए data की definitions (या "schemas") शामिल होती हैं।

#### `openapi.json` जाँचें { #check-the-openapi-json }

अगर आप यह जानने को उत्सुक हैं कि raw OpenAPI schema कैसा दिखता है, FastAPI आपकी पूरी API के descriptions के साथ अपने आप एक JSON (schema) generate करता है।

आप इसे सीधे यहाँ देख सकते हैं: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)।

यह कुछ ऐसे शुरू होने वाला JSON दिखाएगा:

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

#### OpenAPI किसलिए है { #what-is-openapi-for }

OpenAPI schema ही शामिल किए गए दो interactive documentation systems को power देता है।

और दर्जनों विकल्प हैं, सभी OpenAPI पर आधारित। आप **FastAPI** से बनी अपनी application में इनमें से कोई भी विकल्प आसानी से जोड़ सकते हैं।

आप इसका उपयोग उन clients के लिए अपने आप code generate करने के लिए भी कर सकते हैं जो आपकी API से communicate करते हैं। उदाहरण के लिए, frontend, mobile या IoT applications।

### `pyproject.toml` में app `entrypoint` configure करें { #configure-the-app-entrypoint-in-pyproject-toml }

आप `pyproject.toml` file में अपनी app कहाँ स्थित है, इसे इस तरह configure कर सकते हैं:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

वह `entrypoint` `fastapi` command को बताएगा कि उसे app को इस तरह import करना चाहिए:

```python
from main import app
```

अगर आपका code इस तरह structured था:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

तो आप `entrypoint` को इस तरह set करेंगे:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

जो इसके equivalent होगा:

```python
from backend.main import app
```

### `fastapi dev` path के साथ या `--entrypoint` CLI option के साथ { #fastapi-dev-with-path-or-with-entrypoint-cli-option }

आप `fastapi dev` command को file path भी pass कर सकते हैं, और यह उपयोग करने के लिए FastAPI app object का अनुमान लगा लेगा:

```console
$ fastapi dev main.py
```

या, आप `fastapi dev` command को `--entrypoint` option भी pass कर सकते हैं:

```console
$ fastapi dev --entrypoint main:app
```

लेकिन हर बार `fastapi` command call करते समय आपको सही path\entrypoint pass करना याद रखना होगा।

इसके अलावा, दूसरे tools इसे ढूँढ नहीं पाएँगे, उदाहरण के लिए [VS Code Extension](../editor-support.md) या [FastAPI Cloud](https://fastapicloud.com), इसलिए `pyproject.toml` में `entrypoint` का उपयोग करने की सलाह दी जाती है।

### अपनी app deploy करें (वैकल्पिक) { #deploy-your-app-optional }

आप वैकल्पिक रूप से अपनी FastAPI app को एक single command से [FastAPI Cloud](https://fastapicloud.com) पर deploy कर सकते हैं। 🚀

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

CLI आपकी FastAPI application को अपने आप detect करेगा और उसे cloud पर deploy करेगा। अगर आप logged in नहीं हैं, तो authentication process पूरा करने के लिए आपका browser खुलेगा।

बस इतना ही! अब आप उस URL पर अपनी app access कर सकते हैं। ✨

## Recap, चरण दर चरण { #recap-step-by-step }

### चरण 1: `FastAPI` import करें { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[1] *}

`FastAPI` एक Python class है जो आपकी API के लिए सारी functionality प्रदान करती है।

/// note | तकनीकी विवरण

`FastAPI` एक class है जो सीधे `Starlette` से inherit करती है।

आप `FastAPI` के साथ सारी [Starlette](https://www.starlette.dev/) functionality भी उपयोग कर सकते हैं।

///

### चरण 2: एक `FastAPI` "instance" बनाएँ { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[3] *}

यहाँ `app` variable class `FastAPI` का एक "instance" होगा।

यह आपकी पूरी API बनाने के लिए interaction का मुख्य point होगा।

### चरण 3: एक *path operation* बनाएँ { #step-3-create-a-path-operation }

#### Path { #path }

यहाँ "Path" URL के पहले `/` से शुरू होने वाले आख़िरी हिस्से को refer करता है।

तो, ऐसे URL में:

```
https://example.com/items/foo
```

...path होगा:

```
/items/foo
```

/// note | नोट

एक "path" को आमतौर पर "endpoint" या "route" भी कहा जाता है।

///

API बनाते समय, "path" "concerns" और "resources" को अलग करने का मुख्य तरीका है।

#### Operation { #operation }

यहाँ "Operation" HTTP "methods" में से किसी एक को refer करता है।

इनमें से एक:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...और कुछ अधिक असामान्य वाले:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

HTTP protocol में, आप इन "methods" में से एक (या अधिक) का उपयोग करके हर path से communicate कर सकते हैं।

---

APIs बनाते समय, आप आमतौर पर कोई specific action करने के लिए इन specific HTTP methods का उपयोग करते हैं।

आम तौर पर आप उपयोग करते हैं:

* `POST`: data बनाने के लिए।
* `GET`: data पढ़ने के लिए।
* `PUT`: data update करने के लिए।
* `DELETE`: data delete करने के लिए।

इसलिए, OpenAPI में, हर HTTP method को एक "operation" कहा जाता है।

हम उन्हें भी "**operations**" कहेंगे।

#### एक *path operation decorator* define करें { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[6] *}

`@app.get("/")` **FastAPI** को बताता है कि ठीक नीचे वाला function उन requests को handle करने का प्रभारी है जो यहाँ जाती हैं:

* path `/`
* <dfn title="एक HTTP GET method"><code>get</code> operation</dfn> का उपयोग करते हुए

/// note | `@decorator` जानकारी

Python में उस `@something` syntax को "decorator" कहा जाता है।

आप इसे किसी function के ऊपर लगाते हैं। जैसे एक सुंदर सजावटी टोपी (मुझे लगता है term वहीं से आया है)।

एक "decorator" नीचे वाले function को लेता है और उसके साथ कुछ करता है।

हमारे मामले में, यह decorator **FastAPI** को बताता है कि नीचे वाला function **path** `/` के साथ **operation** `get` से संबंधित है।

यह "**path operation decorator**" है।

///

आप दूसरे operations भी उपयोग कर सकते हैं:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

और कुछ अधिक असामान्य वाले:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | सुझाव

आप हर operation (HTTP method) को अपनी इच्छा के अनुसार उपयोग करने के लिए स्वतंत्र हैं।

**FastAPI** कोई specific अर्थ enforce नहीं करता।

यहाँ दी गई जानकारी guideline के रूप में प्रस्तुत की गई है, requirement के रूप में नहीं।

उदाहरण के लिए, GraphQL का उपयोग करते समय आप आम तौर पर सभी actions केवल `POST` operations का उपयोग करके करते हैं।

///

### चरण 4: **path operation function** define करें { #step-4-define-the-path-operation-function }

यह हमारा "**path operation function**" है:

* **path**: `/` है।
* **operation**: `get` है।
* **function**: "decorator" के नीचे वाला function है (`@app.get("/")` के नीचे)।

{* ../../docs_src/first_steps/tutorial001_py310.py hl[7] *}

यह एक Python function है।

जब भी **FastAPI** को `GET` operation का उपयोग करके URL "`/`" पर कोई request मिलती है, तो यह इसे call करेगा।

इस मामले में, यह एक `async` function है।

---

आप इसे `async def` के बजाय normal function के रूप में भी define कर सकते हैं:

{* ../../docs_src/first_steps/tutorial003_py310.py hl[7] *}

/// note | नोट

अगर आपको अंतर नहीं पता है, तो [Async: *"In a hurry?"*](../async.md#in-a-hurry) देखें।

///

### चरण 5: content return करें { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[8] *}

आप `dict`, `list`, `str`, `int` आदि जैसे singular values return कर सकते हैं।

आप Pydantic models भी return कर सकते हैं (इसके बारे में आप आगे और देखेंगे)।

कई अन्य objects और models हैं जिन्हें अपने आप JSON में convert किया जाएगा (ORMs आदि सहित)। अपने पसंदीदा ones उपयोग करके देखें, बहुत संभावना है कि वे पहले से supported हों।

### चरण 6: इसे Deploy करें { #step-6-deploy-it }

अपनी app को **[FastAPI Cloud](https://fastapicloud.com)** पर एक command से deploy करें: `fastapi deploy`। 🎉

#### FastAPI Cloud के बारे में { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** को **FastAPI** के पीछे मौजूद उसी author और team ने बनाया है।

यह कम से कम प्रयास के साथ API को **बनाने**, **deploy करने**, और **access करने** की process को streamlined करता है।

यह FastAPI के साथ apps बनाने जैसा ही **developer experience**, उन्हें cloud पर **deploy** करने में लाता है। 🎉

FastAPI Cloud *FastAPI and friends* open source projects का प्राथमिक sponsor और funding provider है। ✨

#### दूसरे cloud providers पर deploy करें { #deploy-to-other-cloud-providers }

FastAPI open source है और standards पर आधारित है। आप FastAPI apps को अपनी पसंद के किसी भी cloud provider पर deploy कर सकते हैं।

FastAPI apps को उनके साथ deploy करने के लिए अपने cloud provider की guides follow करें। 🤓

## Recap { #recap }

* `FastAPI` import करें।
* एक `app` instance बनाएँ।
* `@app.get("/")` जैसे decorators का उपयोग करके एक **path operation decorator** लिखें।
* एक **path operation function** define करें; उदाहरण के लिए, `def root(): ...`।
* `fastapi dev` command का उपयोग करके development server चलाएँ।
* वैकल्पिक रूप से अपनी app को `fastapi deploy` के साथ deploy करें।
