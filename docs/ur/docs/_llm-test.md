# LLM ٹیسٹ فائل { #llm-test-file }

یہ document ٹیسٹ کرتا ہے کہ آیا <abbr title="Large Language Model">LLM</abbr>، جو documentation کا ترجمہ کرتا ہے، `scripts/translate.py` میں `general_prompt` اور `docs/{language code}/llm-prompt.md` میں زبان کے لیے مخصوص prompt کو سمجھتا ہے۔ زبان کے لیے مخصوص prompt، `general_prompt` کے ساتھ جوڑا جاتا ہے۔

یہاں شامل کیے گئے ٹیسٹ تمام زبان کے مخصوص prompt ڈیزائنرز کو نظر آئیں گے۔

اس طرح استعمال کریں:

* زبان کے لیے مخصوص prompt رکھیں - `docs/{language code}/llm-prompt.md`۔
* اس document کا اپنی مطلوبہ ہدف زبان میں تازہ ترجمہ کریں (مثلاً `translate.py` کا `translate-page` command دیکھیں)۔ یہ `docs/{language code}/docs/_llm-test.md` کے تحت ترجمہ بنائے گا۔
* چیک کریں کہ ترجمے میں سب ٹھیک ہے۔
* اگر ضروری ہو تو اپنے زبان کے مخصوص prompt، عمومی prompt، یا انگریزی document کو بہتر بنائیں۔
* پھر ترجمے میں باقی رہ جانے والے مسائل خود ٹھیک کریں، تاکہ یہ اچھا ترجمہ ہو۔
* اچھا ترجمہ موجود ہونے کے بعد دوبارہ ترجمہ کریں۔ مثالی نتیجہ یہ ہوگا کہ LLM ترجمے میں مزید کوئی تبدیلی نہ کرے۔ اس کا مطلب ہے کہ عمومی prompt اور آپ کا زبان کے مخصوص prompt اتنے اچھے ہیں جتنے ہو سکتے ہیں (یہ بعض اوقات کچھ بظاہر بے ترتیب تبدیلیاں کرے گا، اس کی وجہ یہ ہے کہ [LLMs deterministic algorithms نہیں ہیں](https://doublespeak.chat/#/handbook#deterministic-output))۔

ٹیسٹ:

## Code snippets { #code-snippets }

//// tab | Test

یہ ایک code snippet ہے: `foo`۔ اور یہ ایک اور code snippet ہے: `bar`۔ اور ایک اور: `baz quux`۔

////

//// tab | Info

Code snippets کا مواد جوں کا توں رہنا چاہیے۔

`scripts/translate.py` میں عمومی prompt کا سیکشن `### Content of code snippets` دیکھیں۔

////

## اقتباسات { #quotes }

//// tab | Test

کل میرے دوست نے لکھا: "If you spell incorrectly correctly, you have spelled it incorrectly"۔ جس پر میں نے جواب دیا: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"۔

/// note | نوٹ

LLM شاید اس کا ترجمہ غلط کرے گا۔ دلچسپ صرف یہ ہے کہ دوبارہ ترجمہ کرتے وقت یہ ٹھیک کیا گیا ترجمہ محفوظ رکھتا ہے یا نہیں۔

///

////

//// tab | Info

Prompt ڈیزائنر یہ فیصلہ کر سکتا ہے کہ آیا وہ neutral quotes کو typographic quotes میں تبدیل کرنا چاہتے ہیں۔ انہیں جوں کا توں چھوڑنا بھی ٹھیک ہے۔

مثال کے طور پر `docs/de/llm-prompt.md` میں سیکشن `### Quotes` دیکھیں۔

////

## Code snippets میں اقتباسات { #quotes-in-code-snippets }

//// tab | Test

`pip install "foo[bar]"`

Code snippets میں string literals کی مثالیں: `"this"`, `'that'`۔

Code snippets میں string literals کی مشکل مثال: `f"I like {'oranges' if orange else "apples"}"`

سخت ترین: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | Info

... تاہم، code snippets کے اندر اقتباسات جوں کے توں رہنے چاہئیں۔

////

## Code blocks { #code-blocks }

//// tab | Test

ایک Bash code مثال...

```bash
# Print a greeting to the universe
echo "Hello universe"
```

...اور ایک console code مثال...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

...اور ایک اور console code مثال...

```console
// "Code" نامی directory بنائیں
$ mkdir code
// اس directory میں جائیں
$ cd code
```

...اور ایک Python code مثال...

```Python
wont_work()  # This won't work 😱
works(foo="bar")  # This works 🎉
```

...اور بس۔

////

//// tab | Info

Code blocks میں code کو تبدیل نہیں کیا جانا چاہیے، سوائے تبصروں کے۔

`scripts/translate.py` میں عمومی prompt کا سیکشن `### Content of code blocks` دیکھیں۔

////

## Tabs اور رنگین خانے { #tabs-and-colored-boxes }

//// tab | Test

/// info | معلومات
کچھ متن
///

/// note | نوٹ
کچھ متن
///

/// note | تکنیکی تفصیلات
کچھ متن
///

/// check
کچھ متن
///

/// tip | مشورہ
کچھ متن
///

/// warning | انتباہ
کچھ متن
///

/// danger
کچھ متن
///

////

//// tab | Info

Tabs اور `Info`/`Note`/`Warning` وغیرہ بلاکس میں عمودی خط (`|`) کے بعد ان کے عنوان کا ترجمہ شامل ہونا چاہیے۔

`scripts/translate.py` میں عمومی prompt کے سیکشنز `### Special blocks` اور `### Tab blocks` دیکھیں۔

////

## Web اور اندرونی لنکس { #web-and-internal-links }

//// tab | Test

لنک کا متن ترجمہ ہونا چاہیے، لنک کا پتہ تبدیل نہیں ہونا چاہیے:

* [اوپر والی heading کا لنک](#code-snippets)
* [اندرونی لنک](index.md#installation)
* [بیرونی لنک](https://sqlmodel.tiangolo.com/)
* [ایک style کا لنک](https://fastapi.tiangolo.com/css/styles.css)
* [ایک script کا لنک](https://fastapi.tiangolo.com/js/logic.js)
* [ایک تصویر کا لنک](https://fastapi.tiangolo.com/img/foo.jpg)

لنک کا متن ترجمہ ہونا چاہیے، لنک کا پتہ ترجمے کی طرف اشارہ کرنا چاہیے:

* [FastAPI لنک](https://fastapi.tiangolo.com/)

////

//// tab | Info

لنکس کا ترجمہ ہونا چاہیے، لیکن ان کا پتہ تبدیل نہیں ہونا چاہیے۔ استثناء FastAPI documentation کے صفحات کے مطلق لنکس ہیں۔ اس صورت میں اسے ترجمے کی طرف لنک کرنا چاہیے۔

`scripts/translate.py` میں عمومی prompt کا سیکشن `### Links` دیکھیں۔

////

## HTML "abbr" عناصر { #html-abbr-elements }

//// tab | Test

یہاں HTML "abbr" عناصر میں لپٹی کچھ چیزیں ہیں (کچھ من گھڑت ہیں):

### abbr مکمل جملہ دیتا ہے { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done">GTD</abbr>
* <abbr title="less than"><code>lt</code></abbr>
* <abbr title="XML Web Token">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface">PSGI</abbr>

### abbr مکمل جملہ اور وضاحت دیتا ہے { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network: documentation for developers, written by the Firefox people">MDN</abbr>
* <abbr title="Input/Output: disk reading or writing, network communications.">I/O</abbr>.

////

//// tab | Info

"abbr" عناصر کی "title" attributes کا مخصوص ہدایات کے مطابق ترجمہ کیا جاتا ہے۔

تراجم اپنے "abbr" عناصر شامل کر سکتے ہیں جنہیں LLM نہیں ہٹانا چاہیے۔ مثلاً انگریزی الفاظ کی وضاحت کے لیے۔

`scripts/translate.py` میں عمومی prompt کا سیکشن `### HTML abbr elements` دیکھیں۔

////

## HTML "dfn" عناصر { #html-dfn-elements }

* <dfn title="A group of machines that are configured to be connected and work together in some way.">cluster</dfn>
* <dfn title="A method of machine learning that uses artificial neural networks with numerous hidden layers between input and output layers, thereby developing a comprehensive internal structure">Deep Learning</dfn>

## عنوانات { #headings }

//// tab | Test

### ایک webapp تیار کریں - ایک tutorial { #develop-a-webapp-a-tutorial }

ہیلو۔

### Type hints اور -annotations { #type-hints-and-annotations }

دوبارہ ہیلو۔

### Super- اور subclasses { #super-and-subclasses }

دوبارہ ہیلو۔

////

//// tab | Info

عنوانات کے لیے واحد سخت قاعدہ یہ ہے کہ LLM گھنگھریالے قوسین کے اندر hash حصے کو تبدیل نہ کرے، جو یقینی بناتا ہے کہ لنکس نہ ٹوٹیں۔

`scripts/translate.py` میں عمومی prompt کا سیکشن `### Headings` دیکھیں۔

کچھ زبان کے مخصوص ہدایات کے لیے، مثلاً `docs/de/llm-prompt.md` میں سیکشن `### Headings` دیکھیں۔

////

## Docs میں استعمال ہونے والی اصطلاحات { #terms-used-in-the-docs }

//// tab | Test

* you
* your

* e.g.
* etc.

* `foo` as an `int`
* `bar` as a `str`
* `baz` as a `list`

* the Tutorial - User guide
* the Advanced User Guide
* the SQLModel docs
* the API docs
* the automatic docs

* Data Science
* Deep Learning
* Machine Learning
* Dependency Injection
* HTTP Basic authentication
* HTTP Digest
* ISO format
* the JSON Schema standard
* the JSON schema
* the schema definition
* Password Flow
* Mobile

* deprecated
* designed
* invalid
* on the fly
* standard
* default
* case-sensitive
* case-insensitive

* to serve the application
* to serve the page

* the app
* the application

* the request
* the response
* the error response

* the path operation
* the path operation decorator
* the path operation function

* the body
* the request body
* the response body
* the JSON body
* the form body
* the file body
* the function body

* the parameter
* the body parameter
* the path parameter
* the query parameter
* the cookie parameter
* the header parameter
* the form parameter
* the function parameter

* the event
* the startup event
* the startup of the server
* the shutdown event
* the lifespan event

* the handler
* the event handler
* the exception handler
* to handle

* the model
* the Pydantic model
* the data model
* the database model
* the form model
* the model object

* the class
* the base class
* the parent class
* the subclass
* the child class
* the sibling class
* the class method

* the header
* the headers
* the authorization header
* the `Authorization` header
* the forwarded header

* the dependency injection system
* the dependency
* the dependable
* the dependant

* I/O bound
* CPU bound
* concurrency
* parallelism
* multiprocessing

* the env var
* the environment variable
* the `PATH`
* the `PATH` variable

* the authentication
* the authentication provider
* the authorization
* the authorization form
* the authorization provider
* the user authenticates
* the system authenticates the user

* the CLI
* the command line interface

* the server
* the client

* the cloud provider
* the cloud service

* the development
* the development stages

* the dict
* the dictionary
* the enumeration
* the enum
* the enum member

* the encoder
* the decoder
* to encode
* to decode

* the exception
* to raise

* the expression
* the statement

* the frontend
* the backend

* the GitHub discussion
* the GitHub issue

* the performance
* the performance optimization

* the return type
* the return value

* the security
* the security scheme

* the task
* the background task
* the task function

* the template
* the template engine

* the type annotation
* the type hint

* the server worker
* the Uvicorn worker
* the Gunicorn Worker
* the worker process
* the worker class
* the workload

* the deployment
* to deploy

* the SDK
* the software development kit

* the `APIRouter`
* the `requirements.txt`
* the Bearer Token
* the breaking change
* the bug
* the button
* the callable
* the code
* the commit
* the context manager
* the coroutine
* the database session
* the disk
* the domain
* the engine
* the fake X
* the HTTP GET method
* the item
* the library
* the lifespan
* the lock
* the middleware
* the mobile application
* the module
* the mounting
* the network
* the origin
* the override
* the payload
* the processor
* the property
* the proxy
* the pull request
* the query
* the RAM
* the remote machine
* the status code
* the string
* the tag
* the web framework
* the wildcard
* to return
* to validate

////

//// tab | Info

یہ docs میں نظر آنے والی (زیادہ تر) تکنیکی اصطلاحات کی ایک نامکمل اور غیر حتمی فہرست ہے۔ یہ prompt ڈیزائنر کے لیے مفید ہو سکتی ہے تاکہ معلوم ہو کہ کن اصطلاحات کے لیے LLM کو مدد کی ضرورت ہے۔ مثلاً جب یہ اچھے ترجمے کو بار بار کسی کمتر ترجمے میں واپس لے آئے۔ یا جب اسے آپ کی زبان میں کسی اصطلاح کو conjugate/declinate کرنے میں مسائل ہوں۔

مثال کے طور پر `docs/de/llm-prompt.md` میں سیکشن `### List of English terms and their preferred German translations` دیکھیں۔

////
