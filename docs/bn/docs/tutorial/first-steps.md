# প্রথম ধাপ { #first-steps }

সবচেয়ে সহজ FastAPI file দেখতে এরকম হতে পারে:

{* ../../docs_src/first_steps/tutorial001_py310.py *}

এটা একটি `main.py` file-এ copy করুন।

/// tip | Tip

FastAPI-এর একটি [VS Code-এর official extension](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode) আছে (Cursor-এর জন্যও), যেটাতে অনেক feature আছে: path operation explorer, path operation search, tests-এ CodeLens navigation (tests থেকে সরাসরি definition-এ যাওয়া), আর FastAPI Cloud deployment ও logs, সবকিছু আপনার editor থেকেই।

///

live server চালান:

<div class="termy">

```console
$ <font color="#4E9A06">uv run fastapi</font> dev

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

Output-এ এরকম একটা line থাকবে:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

এই line-টা দেখায় আপনার local machine-এ app কোন URL-এ serve হচ্ছে।

### ফলাফল দেখুন { #check-it }

আপনার browser-এ খুলুন [http://127.0.0.1:8000](http://127.0.0.1:8000)।

আপনি এই JSON response দেখতে পাবেন:

```JSON
{"message": "Hello World"}
```

### Interactive API docs { #interactive-api-docs }

এবার যান [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)-এ।

আপনি automatic interactive API documentation দেখতে পাবেন ([Swagger UI](https://github.com/swagger-api/swagger-ui) দিয়ে তৈরি):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### বিকল্প API docs { #alternative-api-docs }

আর এবার যান [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)-এ।

আপনি আরেকটি automatic documentation দেখতে পাবেন ([ReDoc](https://github.com/Redocly/redoc) দিয়ে তৈরি):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI** API define করার **OpenAPI** standard ব্যবহার করে আপনার পুরো API-এর একটি "schema" generate করে।

#### "Schema" { #schema }

"schema" হলো কোনো কিছুর definition বা বর্ণনা। এটা সেই জিনিসটা implement করার code নয়, শুধু একটা abstract বর্ণনা।

#### API "schema" { #api-schema }

এখানে, [OpenAPI](https://github.com/OAI/OpenAPI-Specification) হলো একটি specification, যেটা ঠিক করে দেয় আপনার API-এর schema কীভাবে define করতে হবে।

এই schema definition-এ আপনার API paths, সেগুলো কী কী parameters নিতে পারে, ইত্যাদি থাকে।

#### Data "schema" { #data-schema }

"schema" বলতে কোনো data-এর গঠনও বোঝাতে পারে, যেমন একটি JSON content।

সেক্ষেত্রে এর মানে হবে JSON attributes, সেগুলোর data types, ইত্যাদি।

#### OpenAPI আর JSON Schema { #openapi-and-json-schema }

OpenAPI আপনার API-এর জন্য একটি API schema define করে। আর সেই schema-তে আপনার API যে data পাঠায় ও নেয়, সেগুলোর definitions (বা "schemas") থাকে **JSON Schema** দিয়ে, যেটা JSON data schemas-এর standard।

#### `openapi.json` দেখুন { #check-the-openapi-json }

raw OpenAPI schema দেখতে কেমন, সেটা জানতে ইচ্ছা হলে: FastAPI নিজে থেকেই আপনার পুরো API-এর বর্ণনা দিয়ে একটি JSON (schema) generate করে।

এটা সরাসরি দেখতে পারেন এখানে: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)।

এটা এরকম দিয়ে শুরু হওয়া একটি JSON দেখাবে:

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

#### OpenAPI কীসের জন্য { #what-is-openapi-for }

সাথে যে দুটি interactive documentation system আছে, সেগুলো চলে এই OpenAPI schema দিয়েই।

আর OpenAPI-ভিত্তিক আরও ডজনখানেক বিকল্প আছে। **FastAPI** দিয়ে বানানো আপনার application-এ এগুলোর যেকোনোটা সহজেই যোগ করতে পারেন।

আপনার API-এর সাথে যোগাযোগ করা clients-এর জন্য নিজে থেকে code generate করতেও এটা ব্যবহার করতে পারেন। যেমন frontend, mobile বা IoT applications।

### `pyproject.toml`-এ app-এর `entrypoint` configure করুন { #configure-the-app-entrypoint-in-pyproject-toml }

আপনার app কোথায় আছে, সেটা একটি `pyproject.toml` file-এ এভাবে configure করতে পারেন:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

এই `entrypoint` `fastapi` command-কে জানিয়ে দেবে যে app-টা এভাবে import করতে হবে:

```python
from main import app
```

আপনার code যদি এভাবে সাজানো থাকে:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

তাহলে `entrypoint` set করবেন এভাবে:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

যেটা এর সমান:

```python
from backend.main import app
```

### path দিয়ে বা `--entrypoint` CLI option দিয়ে `fastapi dev` { #fastapi-dev-with-path-or-with-entrypoint-cli-option }

`fastapi dev` command-এ file path-ও দিতে পারেন, তখন এটা নিজেই আন্দাজ করে নেবে কোন FastAPI app object ব্যবহার করতে হবে:

```console
$ uv run fastapi dev main.py
```

অথবা `fastapi dev` command-এ `--entrypoint` option-ও দিতে পারেন:

```console
$ uv run fastapi dev --entrypoint main:app
```

কিন্তু তখন প্রতিবার `fastapi` command চালানোর সময় সঠিক path\entrypoint দেওয়ার কথা মনে রাখতে হবে।

তাছাড়া অন্য tools হয়তো এটা খুঁজে পাবে না, যেমন [VS Code Extension](../editor-support.md) বা [FastAPI Cloud](https://fastapicloud.com), তাই `pyproject.toml`-এ `entrypoint` ব্যবহার করাই recommended।

### আপনার app deploy করুন (optional) { #deploy-your-app-optional }

আপনি চাইলে একটি মাত্র command দিয়ে আপনার FastAPI app [FastAPI Cloud](https://fastapicloud.com)-এ deploy করতে পারেন। 🚀

<div class="termy">

```console
$ uv run fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

CLI নিজে থেকেই আপনার FastAPI application খুঁজে নিয়ে cloud-এ deploy করবে। login করা না থাকলে authentication শেষ করার জন্য আপনার browser খুলে যাবে।

ব্যস, এতটুকুই! এখন ওই URL-এ গিয়ে আপনার app ব্যবহার করতে পারবেন। ✨

## Recap, ধাপে ধাপে { #recap-step-by-step }

### ধাপ 1: `FastAPI` import করুন { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[1] *}

`FastAPI` হলো একটি Python class, যেটা আপনার API-এর সব functionality দেয়।

/// note | Technical Details

`FastAPI` হলো একটি class, যেটা সরাসরি `Starlette` থেকে inherit করে।

`FastAPI` দিয়েও আপনি [Starlette](https://starlette.dev/)-এর সব functionality ব্যবহার করতে পারবেন।

///

### ধাপ 2: একটি `FastAPI` "instance" বানান { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[3] *}

এখানে `app` variable-টা হবে `FastAPI` class-এর একটি "instance"।

আপনার পুরো API বানানোর জন্য এটাই হবে interaction-এর মূল জায়গা।

### ধাপ 3: একটি *path operation* বানান { #step-3-create-a-path-operation }

#### Path { #path }

এখানে "Path" বলতে URL-এর শেষ অংশ বোঝায়, প্রথম `/` থেকে শুরু করে।

তাই এরকম একটি URL-এ:

```
https://example.com/items/foo
```

...path হবে:

```
/items/foo
```

/// note | Note

"path"-কে সাধারণত "endpoint" বা "route"-ও বলা হয়।

///

API বানানোর সময় "concerns" আর "resources" আলাদা করার মূল উপায় হলো "path"।

#### Operation { #operation }

এখানে "Operation" বলতে HTTP "methods"-এর কোনো একটি বোঝায়।

এগুলোর একটি:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...আর একটু কম ব্যবহৃতগুলো:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

HTTP protocol-এ এই "methods"-এর একটি (বা একাধিক) দিয়ে প্রতিটি path-এর সাথে যোগাযোগ করা যায়।

---

API বানানোর সময় সাধারণত নির্দিষ্ট কাজের জন্য নির্দিষ্ট HTTP methods ব্যবহার করা হয়।

সাধারণত ব্যবহার করা হয়:

* `POST`: data বানাতে।
* `GET`: data পড়তে।
* `PUT`: data update করতে।
* `DELETE`: data delete করতে।

তাই OpenAPI-তে প্রতিটি HTTP method-কে বলা হয় একটি "operation"।

আমরাও এগুলোকে "**operations**" বলব।

#### একটি *path operation decorator* define করুন { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[6] *}

`@app.get("/")` **FastAPI**-কে জানায় যে ঠিক নিচের function-টা সেই requests handle করার দায়িত্বে, যেগুলো যায়:

* path `/`-এ
* একটি <dfn title="একটি HTTP GET method"><code>get</code> operation</dfn> দিয়ে

/// note | `@decorator` সম্পর্কে

Python-এর এই `@something` syntax-কে বলে "decorator"।

এটা একটি function-এর উপরে বসানো হয়। ঠিক একটা সুন্দর সাজানো টুপির মতো (আমার ধারণা, term-টা এখান থেকেই এসেছে)।

একটি "decorator" নিচের function-টা নিয়ে সেটার সাথে কিছু একটা করে।

আমাদের ক্ষেত্রে, এই decorator **FastAPI**-কে জানায় যে নিচের function-টা **path** `/` আর **operation** `get`-এর সাথে যুক্ত।

এটাই হলো "**path operation decorator**"।

///

অন্য operations-ও ব্যবহার করতে পারেন:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

আর একটু কম ব্যবহৃতগুলো:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | Tip

প্রতিটি operation (HTTP method) নিজের ইচ্ছামতো ব্যবহার করতে পারেন।

**FastAPI** কোনো নির্দিষ্ট অর্থ চাপিয়ে দেয় না।

এখানের তথ্যগুলো guideline হিসেবে দেওয়া, বাধ্যতামূলক নয়।

যেমন GraphQL ব্যবহার করলে সাধারণত সব কাজ শুধু `POST` operations দিয়েই করা হয়।

///

### ধাপ 4: **path operation function** define করুন { #step-4-define-the-path-operation-function }

এটাই আমাদের "**path operation function**":

* **path**: হলো `/`।
* **operation**: হলো `get`।
* **function**: হলো "decorator"-এর নিচের function-টা (`@app.get("/")`-এর নিচে)।

{* ../../docs_src/first_steps/tutorial001_py310.py hl[7] *}

এটা একটি Python function।

যখনই **FastAPI** URL "`/`"-এ `GET` operation দিয়ে কোনো request পাবে, তখনই এটা call করবে।

এখানে এটা একটি `async` function।

---

`async def`-এর বদলে একে সাধারণ function হিসেবেও define করতে পারেন:

{* ../../docs_src/first_steps/tutorial003_py310.py hl[7] *}

/// note | Note

পার্থক্যটা না জানলে [Async: *"In a hurry?"*](../async.md#in-a-hurry) দেখুন।

///

### ধাপ 5: content return করুন { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[8] *}

আপনি একটি `dict`, `list`, `str`, `int`-এর মতো একক values, ইত্যাদি return করতে পারেন।

Pydantic models-ও return করতে পারেন (এ নিয়ে পরে আরও দেখবেন)।

আরও অনেক objects আর models আছে, যেগুলো নিজে থেকেই JSON-এ convert হয়ে যায় (ORMs সহ, ইত্যাদি)। আপনার পছন্দেরগুলো ব্যবহার করে দেখুন, খুব সম্ভবত সেগুলো আগে থেকেই supported।

### ধাপ 6: Deploy করুন { #step-6-deploy-it }

একটি command দিয়ে আপনার app **[FastAPI Cloud](https://fastapicloud.com)**-এ deploy করুন: `fastapi deploy`। 🎉

#### FastAPI Cloud সম্পর্কে { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** বানিয়েছেন **FastAPI**-এর সেই একই author আর team।

খুব কম ঝামেলায় একটি API-এর **building**, **deploying** আর **accessing** সহজ করে দেয়।

FastAPI দিয়ে app বানানোর যে **developer experience**, সেটাই এটা cloud-এ **deploy** করার সময়ও এনে দেয়। 🎉

FastAPI Cloud হলো *FastAPI and friends* open source project-গুলোর প্রধান sponsor এবং funding provider। ✨

#### অন্যান্য cloud provider-এ deploy করুন { #deploy-to-other-cloud-providers }

FastAPI open source এবং standards-ভিত্তিক। আপনার পছন্দের যেকোনো cloud provider-এ FastAPI apps deploy করতে পারবেন।

আপনার cloud provider-এর guide দেখে সেখানে FastAPI apps deploy করুন। 🤓

## Recap { #recap }

* `FastAPI` import করুন।
* একটি `app` instance বানান।
* `@app.get("/")`-এর মতো decorators দিয়ে একটি **path operation decorator** লিখুন।
* একটি **path operation function** define করুন; যেমন, `def root(): ...`।
* `fastapi dev` command দিয়ে development server চালান।
* চাইলে `fastapi deploy` দিয়ে আপনার app deploy করুন।
