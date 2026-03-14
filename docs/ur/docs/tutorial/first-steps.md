# پہلے قدم { #first-steps }

سب سے سادہ FastAPI فائل کچھ ایسی ہو سکتی ہے:

{* ../../docs_src/first_steps/tutorial001_py310.py *}

اسے `main.py` فائل میں کاپی کریں۔

لائیو سرور چلائیں:

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

آؤٹ پٹ میں، ایک لائن کچھ ایسی ہوگی:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

یہ لائن وہ URL دکھاتی ہے جہاں آپ کی ایپ آپ کی مقامی مشین پر چل رہی ہے۔

### اسے چیک کریں { #check-it }

اپنا براؤزر [http://127.0.0.1:8000](http://127.0.0.1:8000) پر کھولیں۔

آپ JSON response اس طرح دیکھیں گے:

```JSON
{"message": "Hello World"}
```

### انٹرایکٹو API دستاویزات { #interactive-api-docs }

اب [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) پر جائیں۔

آپ خودکار انٹرایکٹو API دستاویزات دیکھیں گے (جو [Swagger UI](https://github.com/swagger-api/swagger-ui) کی طرف سے فراہم کی گئی ہیں):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### متبادل API دستاویزات { #alternative-api-docs }

اور اب، [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) پر جائیں۔

آپ متبادل خودکار دستاویزات دیکھیں گے (جو [ReDoc](https://github.com/Rebilly/ReDoc) کی طرف سے فراہم کی گئی ہیں):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI** آپ کی تمام API کا ایک "schema" تیار کرتا ہے، APIs کی تعریف کے لیے **OpenAPI** معیار استعمال کرتے ہوئے۔

#### "Schema" { #schema }

"Schema" کسی چیز کی تعریف یا وضاحت ہے۔ وہ کوڈ نہیں جو اسے نافذ کرتا ہے، بلکہ صرف ایک تجریدی وضاحت۔

#### API "Schema" { #api-schema }

اس صورت میں، [OpenAPI](https://github.com/OAI/OpenAPI-Specification) ایک تصریح ہے جو بتاتی ہے کہ آپ کی API کا schema کیسے بنایا جائے۔

اس schema کی تعریف میں آپ کی API کے paths، ممکنہ parameters جو وہ لیتے ہیں، وغیرہ شامل ہیں۔

#### ڈیٹا "Schema" { #data-schema }

اصطلاح "schema" کسی ڈیٹا کی شکل کا بھی حوالہ دے سکتی ہے، جیسے JSON مواد۔

اس صورت میں، اس کا مطلب ہوگا JSON attributes، اور ان کی data types وغیرہ۔

#### OpenAPI اور JSON Schema { #openapi-and-json-schema }

OpenAPI آپ کی API کے لیے ایک API schema بناتا ہے۔ اور اس schema میں آپ کی API کے ذریعے بھیجے اور وصول کیے جانے والے ڈیٹا کی تعریفات (یا "schemas") شامل ہیں جو **JSON Schema** استعمال کرتی ہیں، جو JSON ڈیٹا schemas کا معیار ہے۔

#### `openapi.json` چیک کریں { #check-the-openapi-json }

اگر آپ جاننا چاہتے ہیں کہ خام OpenAPI schema کیسا دکھتا ہے، تو FastAPI خودکار طور پر آپ کی تمام API کی وضاحتوں کے ساتھ ایک JSON (schema) تیار کرتا ہے۔

آپ اسے براہ راست یہاں دیکھ سکتے ہیں: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)۔

یہ ایک JSON دکھائے گا جو کچھ ایسے شروع ہوگا:

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

#### OpenAPI کس لیے ہے { #what-is-openapi-for }

OpenAPI schema وہ ہے جو شامل دو انٹرایکٹو دستاویزاتی نظاموں کو طاقت دیتا ہے۔

اور OpenAPI پر مبنی درجنوں متبادل موجود ہیں۔ آپ آسانی سے ان میں سے کوئی بھی متبادل اپنی **FastAPI** سے بنائی گئی ایپلیکیشن میں شامل کر سکتے ہیں۔

آپ اسے خودکار طور پر کوڈ بنانے کے لیے بھی استعمال کر سکتے ہیں، ان clients کے لیے جو آپ کی API سے بات چیت کرتے ہیں۔ مثال کے طور پر، frontend، موبائل یا IoT ایپلیکیشنز۔

### `pyproject.toml` میں ایپ `entrypoint` ترتیب دیں { #configure-the-app-entrypoint-in-pyproject-toml }

آپ `pyproject.toml` فائل میں ترتیب دے سکتے ہیں کہ آپ کی ایپ کہاں واقع ہے:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

یہ `entrypoint` `fastapi` کمانڈ کو بتائے گا کہ ایپ کو اس طرح import کرنا ہے:

```python
from main import app
```

اگر آپ کے کوڈ کی ساخت ایسی ہو:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

تو آپ `entrypoint` اس طرح سیٹ کریں گے:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

جو اس کے مساوی ہوگا:

```python
from backend.main import app
```

### path کے ساتھ `fastapi dev` { #fastapi-dev-with-path }

آپ `fastapi dev` کمانڈ کو فائل کا path بھی دے سکتے ہیں، اور یہ استعمال کرنے والے FastAPI app object کا اندازہ لگا لے گا:

```console
$ fastapi dev main.py
```

لیکن آپ کو ہر بار `fastapi` کمانڈ کال کرتے وقت صحیح path یاد رکھنا ہوگا۔

اس کے علاوہ، دوسرے ٹولز شاید اسے تلاش نہ کر سکیں، مثال کے طور پر [VS Code ایکسٹینشن](../editor-support.md) یا [FastAPI Cloud](https://fastapicloud.com)، اس لیے `pyproject.toml` میں `entrypoint` استعمال کرنا تجویز کیا جاتا ہے۔

### اپنی ایپ deploy کریں (اختیاری) { #deploy-your-app-optional }

آپ اختیاری طور پر اپنی FastAPI ایپ کو [FastAPI Cloud](https://fastapicloud.com) پر deploy کر سکتے ہیں، اگر آپ نے ابھی تک نہیں کیا تو ویٹنگ لسٹ میں شامل ہو جائیں۔

اگر آپ کے پاس پہلے سے **FastAPI Cloud** اکاؤنٹ ہے (ہم نے آپ کو ویٹنگ لسٹ سے دعوت دی ہے)، تو آپ ایک کمانڈ سے اپنی ایپلیکیشن deploy کر سکتے ہیں۔

deploy کرنے سے پہلے، یقینی بنائیں کہ آپ لاگ ان ہیں:

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

پھر اپنی ایپ deploy کریں:

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

بس! اب آپ اس URL پر اپنی ایپ تک رسائی حاصل کر سکتے ہیں۔

## خلاصہ، قدم بہ قدم { #recap-step-by-step }

### قدم 1: `FastAPI` import کریں { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[1] *}

`FastAPI` ایک Python class ہے جو آپ کی API کے لیے تمام فعالیت فراہم کرتی ہے۔

/// note | تکنیکی تفصیلات

`FastAPI` ایک class ہے جو براہ راست `Starlette` سے وراثت حاصل کرتی ہے۔

آپ **FastAPI** کے ساتھ [Starlette](https://www.starlette.dev/) کی تمام فعالیت بھی استعمال کر سکتے ہیں۔

///

### قدم 2: `FastAPI` کا "instance" بنائیں { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[3] *}

یہاں `app` متغیر `FastAPI` class کا ایک "instance" ہوگا۔

یہ آپ کی تمام API بنانے کے لیے تعامل کا بنیادی مقام ہوگا۔

### قدم 3: ایک *path operation* بنائیں { #step-3-create-a-path-operation }

#### Path { #path }

یہاں "Path" URL کے آخری حصے کا حوالہ دیتا ہے جو پہلے `/` سے شروع ہوتا ہے۔

تو، ایک URL جیسے:

```
https://example.com/items/foo
```

...میں path ہوگا:

```
/items/foo
```

/// info | معلومات

"Path" کو عام طور پر "endpoint" یا "route" بھی کہا جاتا ہے۔

///

API بناتے وقت، "path" "خدشات" اور "وسائل" کو الگ کرنے کا بنیادی طریقہ ہے۔

#### Operation { #operation }

یہاں "Operation" HTTP "methods" میں سے ایک کا حوالہ دیتا ہے۔

ان میں سے ایک:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...اور مزید غیر معمولی:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

HTTP پروٹوکول میں، آپ ان "methods" میں سے ایک (یا زیادہ) استعمال کر کے ہر path سے بات چیت کر سکتے ہیں۔

---

APIs بناتے وقت، آپ عام طور پر ایک مخصوص عمل انجام دینے کے لیے مخصوص HTTP methods استعمال کرتے ہیں۔

عام طور پر آپ استعمال کرتے ہیں:

* `POST`: ڈیٹا بنانے کے لیے۔
* `GET`: ڈیٹا پڑھنے کے لیے۔
* `PUT`: ڈیٹا اپ ڈیٹ کرنے کے لیے۔
* `DELETE`: ڈیٹا حذف کرنے کے لیے۔

تو، OpenAPI میں، ہر HTTP method کو "operation" کہا جاتا ہے۔

ہم بھی انہیں "**operations**" کہیں گے۔

#### ایک *path operation decorator* بنائیں { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[6] *}

`@app.get("/")` **FastAPI** کو بتاتا ہے کہ نیچے والا function ان requests کو سنبھالنے کا ذمہ دار ہے جو یہاں آتی ہیں:

* path `/`
* <dfn title="an HTTP GET method"><code>get</code> operation</dfn> استعمال کرتے ہوئے

/// info | `@decorator` معلومات

Python میں `@something` syntax کو "decorator" کہا جاتا ہے۔

آپ اسے function کے اوپر رکھتے ہیں۔ جیسے ایک خوبصورت آرائشی ٹوپی (مجھے لگتا ہے یہ اصطلاح وہیں سے آئی ہے)۔

"Decorator" نیچے والے function کو لیتا ہے اور اس کے ساتھ کچھ کرتا ہے۔

ہماری صورت میں، یہ decorator **FastAPI** کو بتاتا ہے کہ نیچے والا function **path** `/` کے ساتھ **operation** `get` سے مطابقت رکھتا ہے۔

یہ "**path operation decorator**" ہے۔

///

آپ دوسری operations بھی استعمال کر سکتے ہیں:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

اور مزید غیر معمولی:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | مشورہ

آپ ہر operation (HTTP method) کو جیسے چاہیں استعمال کرنے کے لیے آزاد ہیں۔

**FastAPI** کوئی مخصوص معنی نافذ نہیں کرتا۔

یہاں دی گئی معلومات ایک رہنمائی ہے، ضرورت نہیں۔

مثال کے طور پر، GraphQL استعمال کرتے وقت آپ عام طور پر تمام عمل صرف `POST` operations استعمال کر کے انجام دیتے ہیں۔

///

### قدم 4: **path operation function** بنائیں { #step-4-define-the-path-operation-function }

یہ ہمارا "**path operation function**" ہے:

* **path**: `/` ہے۔
* **operation**: `get` ہے۔
* **function**: "decorator" کے نیچے والا function ہے (`@app.get("/")` کے نیچے)۔

{* ../../docs_src/first_steps/tutorial001_py310.py hl[7] *}

یہ ایک Python function ہے۔

جب بھی **FastAPI** کو URL "`/`" پر `GET` operation استعمال کرتے ہوئے کوئی request ملے گی تو یہ اسے کال کرے گا۔

اس صورت میں، یہ ایک `async` function ہے۔

---

آپ اسے `async def` کی بجائے عام function کے طور پر بھی بنا سکتے ہیں:

{* ../../docs_src/first_steps/tutorial003_py310.py hl[7] *}

/// note | نوٹ

اگر آپ فرق نہیں جانتے، تو [Async: *"جلدی میں ہیں؟"*](../async.md#in-a-hurry) دیکھیں۔

///

### قدم 5: مواد واپس کریں { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[8] *}

آپ `dict`، `list`، واحد اقدار جیسے `str`، `int` وغیرہ واپس کر سکتے ہیں۔

آپ Pydantic models بھی واپس کر سکتے ہیں (آپ اس کے بارے میں بعد میں مزید دیکھیں گے)۔

بہت سی دوسری اشیاء اور models ہیں جو خودکار طور پر JSON میں تبدیل ہو جائیں گے (بشمول ORMs وغیرہ)۔ اپنے پسندیدہ استعمال کرنے کی کوشش کریں، بہت زیادہ امکان ہے کہ وہ پہلے سے تعاون یافتہ ہیں۔

### قدم 6: اسے Deploy کریں { #step-6-deploy-it }

اپنی ایپ کو **[FastAPI Cloud](https://fastapicloud.com)** پر ایک کمانڈ سے deploy کریں: `fastapi deploy`۔

#### FastAPI Cloud کے بارے میں { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** اسی مصنف اور ٹیم نے بنایا ہے جو **FastAPI** کے پیچھے ہے۔

یہ کم سے کم کوشش کے ساتھ API کو **بنانے**، **deploy کرنے**، اور **رسائی حاصل کرنے** کے عمل کو آسان بناتا ہے۔

یہ FastAPI کے ساتھ ایپس بنانے کا وہی **ڈیولپر تجربہ** انہیں کلاؤڈ پر **deploy کرنے** میں لاتا ہے۔

FastAPI Cloud *FastAPI اور دوستوں* کے اوپن سورس پراجیکٹس کا بنیادی اسپانسر اور فنڈنگ فراہم کنندہ ہے۔

#### دوسرے کلاؤڈ فراہم کنندگان پر deploy کریں { #deploy-to-other-cloud-providers }

FastAPI اوپن سورس ہے اور معیارات پر مبنی ہے۔ آپ FastAPI ایپس کو اپنی پسند کے کسی بھی کلاؤڈ فراہم کنندہ پر deploy کر سکتے ہیں۔

اپنے کلاؤڈ فراہم کنندہ کی گائیڈز کی پیروی کریں تاکہ ان کے ساتھ FastAPI ایپس deploy کر سکیں۔

## خلاصہ { #recap }

* `FastAPI` import کریں۔
* ایک `app` instance بنائیں۔
* ایک **path operation decorator** لکھیں جیسے `@app.get("/")`۔
* ایک **path operation function** بنائیں؛ مثال کے طور پر، `def root(): ...`۔
* `fastapi dev` کمانڈ استعمال کر کے ڈیولپمنٹ سرور چلائیں۔
* اختیاری طور پر اپنی ایپ `fastapi deploy` سے deploy کریں۔
