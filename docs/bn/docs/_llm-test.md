# LLM test file { #llm-test-file }

এই document test করে যে documentation অনুবাদকারী <abbr title="Large Language Model">LLM</abbr> `scripts/translate.py`-এর `general_prompt` এবং `docs/{language code}/llm-prompt.md`-এর language-specific prompt বুঝতে পারছে কিনা। language-specific prompt-টি `general_prompt`-এর শেষে যুক্ত করা হয়।

এখানে যোগ করা tests language-specific prompt-এর সব designer দেখতে পাবেন।

এভাবে ব্যবহার করুন:

* একটি language-specific prompt রাখুন - `docs/{language code}/llm-prompt.md`।
* আপনার পছন্দের target language-এ এই document-এর একটি নতুন অনুবাদ করুন (উদাহরণস্বরূপ `translate.py`-এর `translate-page` command দেখুন)। এটি `docs/{language code}/docs/_llm-test.md`-এ অনুবাদটি তৈরি করবে।
* অনুবাদে সবকিছু ঠিক আছে কিনা দেখুন।
* প্রয়োজন হলে, আপনার language-specific prompt, general prompt, অথবা English document উন্নত করুন।
* তারপর অনুবাদে বাকি থাকা সমস্যাগুলো হাতে ঠিক করুন, যাতে এটি একটি ভালো অনুবাদ হয়।
* ভালো অনুবাদটি রেখে আবার অনুবাদ করুন। সবচেয়ে ভালো ফলাফল হলো, LLM অনুবাদে আর কিছুই বদলাবে না। তার মানে general prompt এবং আপনার language-specific prompt যতটা ভালো হওয়া সম্ভব ততটাই ভালো (মাঝে মাঝে এটা দেখতে এলোমেলো কিছু পরিবর্তন করবে, কারণ [LLMs deterministic algorithms নয়](https://doublespeak.chat/#/handbook#deterministic-output))।

Tests:

## Code snippets { #code-snippets }

//// tab | Test

এটি একটি code snippet: `foo`। আর এটি আরেকটি code snippet: `bar`। আর আরও একটি: `baz quux`।

////

//// tab | Info

Code snippets-এর content যেমন আছে তেমনই রাখা উচিত।

`scripts/translate.py`-এর general prompt-এ `### Content of code snippets` section দেখুন।

////

## Quotes { #quotes }

//// tab | Test

গতকাল আমার বন্ধু লিখেছিল: "If you spell incorrectly correctly, you have spelled it incorrectly"। আমি উত্তরে বলেছিলাম: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"।

/// note | Note

LLM সম্ভবত এটা ভুল অনুবাদ করবে। দেখার বিষয় শুধু এটুকু: আবার অনুবাদ করার সময় এটা ঠিক করা অনুবাদটা রেখে দেয় কিনা।

///

////

//// tab | Info

prompt designer ঠিক করতে পারেন, তিনি neutral quotes-কে typographic quotes-এ convert করতে চান কিনা। যেমন আছে তেমন রেখে দেওয়াও ঠিক আছে।

উদাহরণস্বরূপ `docs/de/llm-prompt.md`-এর `### Quotes` section দেখুন।

////

## Code snippets-এর ভেতরে quotes { #quotes-in-code-snippets }

//// tab | Test

`pip install "foo[bar]"`

Code snippets-এ string literals-এর উদাহরণ: `"this"`, `'that'`।

Code snippets-এ string literals-এর একটি কঠিন উদাহরণ: `f"I like {'oranges' if orange else "apples"}"`

Hardcore: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | Info

... তবে code snippets-এর ভেতরের quotes অবশ্যই যেমন আছে তেমন থাকবে।

////

## code blocks { #code-blocks }

//// tab | Test

একটি Bash code উদাহরণ...

```bash
# মহাবিশ্বকে একটি শুভেচ্ছা print করুন
echo "Hello universe"
```

...এবং একটি console code উদাহরণ...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

...এবং আরেকটি console code উদাহরণ...

```console
// "Code" নামে একটি directory তৈরি করুন
$ mkdir code
// সেই directory-তে যান
$ cd code
```

...এবং একটি Python code উদাহরণ...

```Python
wont_work()  # এটি কাজ করবে না 😱
works(foo="bar")  # এটি কাজ করে 🎉
```

...এই পর্যন্তই।

////

//// tab | Info

Code blocks-এর code পরিবর্তন করা উচিত নয়, শুধু comments ছাড়া।

`scripts/translate.py`-এর general prompt-এ `### Content of code blocks` section দেখুন।

////

## Tabs এবং রঙিন boxes { #tabs-and-colored-boxes }

//// tab | Test

/// note | Note
কিছু লেখা
///

/// note | Technical Details
কিছু লেখা
///

/// tip | Tip
কিছু লেখা
///

/// warning | Warning
কিছু লেখা
///

/// danger | Danger
কিছু লেখা
///

////

//// tab | Info

Tabs এবং `Info`/`Note`/`Warning`/ইত্যাদি blocks-এর title-এর অনুবাদ একটি vertical bar (`|`)-এর পরে যোগ করা উচিত।

`scripts/translate.py`-এর general prompt-এ `### Special blocks` এবং `### Tab blocks` section দেখুন।

////

## Web- এবং internal links { #web-and-internal-links }

//// tab | Test

Link text অনুবাদ হবে, link address বদলাবে না:

* [উপরের heading-এর link](#code-snippets)
* [Internal link](index.md#installation)
* [External link](https://sqlmodel.tiangolo.com/)
* [একটি style-এর link](https://fastapi.tiangolo.com/css/styles.css)
* [একটি script-এর link](https://fastapi.tiangolo.com/js/logic.js)
* [একটি image-এর link](https://fastapi.tiangolo.com/img/foo.jpg)

Link text অনুবাদ হওয়া উচিত, link address অনুবাদের দিকে point করবে:

* [FastAPI link](https://fastapi.tiangolo.com/bn/)

////

//// tab | Info

Links অনুবাদ করা উচিত, কিন্তু তাদের address বদলাবে না। ব্যতিক্রম হলো FastAPI documentation-এর pages-এর absolute links। সেক্ষেত্রে এটি অনুবাদের দিকে link করবে।

`scripts/translate.py`-এর general prompt-এ `### Links` section দেখুন।

////

## HTML "abbr" elements { #html-abbr-elements }

//// tab | Test

এখানে HTML "abbr" elements-এ মোড়ানো কিছু জিনিস আছে (কিছু বানানো):

### abbr একটি পূর্ণ phrase দেয় { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done">GTD</abbr>
* <abbr title="less than - এর চেয়ে কম"><code>lt</code></abbr>
* <abbr title="XML Web Token">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface">PSGI</abbr>

### abbr একটি পূর্ণ phrase এবং একটি ব্যাখ্যা দেয় { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network: developer-দের জন্য documentation, Firefox-এর নির্মাতাদের লেখা">MDN</abbr>
* <abbr title="Input/Output: disk পড়া বা লেখা, network communication।">I/O</abbr>।

////

//// tab | Info

"abbr" elements-এর "title" attributes কিছু নির্দিষ্ট নির্দেশনা মেনে অনুবাদ করা হয়।

অনুবাদে নিজস্ব "abbr" elements যোগ করা যেতে পারে, যেগুলো LLM-এর মুছে ফেলা উচিত নয়। যেমন English শব্দ ব্যাখ্যা করার জন্য।

`scripts/translate.py`-এর general prompt-এ `### HTML abbr elements` section দেখুন।

////

## HTML "dfn" elements { #html-dfn-elements }

* <dfn title="কিছু machine-এর একটি group, যেগুলো এমনভাবে configure করা যে সেগুলো যুক্ত থেকে কোনোভাবে একসাথে কাজ করে।">cluster</dfn>
* <dfn title="machine learning-এর একটি পদ্ধতি, যা input এবং output layers-এর মাঝে অনেকগুলো hidden layers সহ artificial neural networks ব্যবহার করে, এবং এভাবে একটি বিস্তৃত internal structure গড়ে তোলে">Deep Learning</dfn>

## Headings { #headings }

//// tab | Test

### একটি webapp develop করুন - একটি tutorial { #develop-a-webapp-a-tutorial }

হ্যালো।

### Type hints এবং -annotations { #type-hints-and-annotations }

আবারও হ্যালো।

### Super- এবং subclasses { #super-and-subclasses }

আবারও হ্যালো।

////

//// tab | Info

Headings-এর জন্য একমাত্র কঠোর নিয়ম হলো, LLM curly brackets-এর ভেতরের hash অংশ বদলাবে না, যাতে links ভেঙে না যায়।

`scripts/translate.py`-এর general prompt-এ `### Headings` section দেখুন।

কিছু language-specific নির্দেশনার জন্য, উদাহরণস্বরূপ `docs/de/llm-prompt.md`-এর `### Headings` section দেখুন।

////

## Docs-এ ব্যবহৃত terms { #terms-used-in-the-docs }

//// tab | Test

* আপনি
* আপনার

* যেমন
* ইত্যাদি

* `foo` একটি `int` হিসেবে
* `bar` একটি `str` হিসেবে
* `baz` একটি `list` হিসেবে

* Tutorial - User guide
* Advanced User Guide
* SQLModel docs
* API docs
* automatic docs

* Data Science
* Deep Learning
* Machine Learning
* Dependency Injection
* HTTP Basic authentication
* HTTP Digest
* ISO format
* JSON Schema standard
* JSON schema
* schema definition
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

* application serve করা
* page serve করা

* app
* application

* request
* response
* error response

* path operation
* path operation decorator
* path operation function

* body
* request body
* response body
* JSON body
* form body
* file body
* function body

* parameter
* body parameter
* path parameter
* query parameter
* cookie parameter
* header parameter
* form parameter
* function parameter

* event
* startup event
* server-এর startup
* shutdown event
* lifespan event

* handler
* event handler
* exception handler
* handle করা

* model
* Pydantic model
* data model
* database model
* form model
* model object

* class
* base class
* parent class
* subclass
* child class
* sibling class
* class method

* header
* headers
* authorization header
* `Authorization` header
* forwarded header

* dependency injection system
* dependency
* dependable
* dependant

* I/O bound
* CPU bound
* concurrency
* parallelism
* multiprocessing

* env var
* environment variable
* `PATH`
* `PATH` variable

* authentication
* authentication provider
* authorization
* authorization form
* authorization provider
* user authenticate করে
* system user-কে authenticate করে

* CLI
* command line interface

* server
* client

* cloud provider
* cloud service

* development
* development stages

* dict
* dictionary
* enumeration
* enum
* enum member

* encoder
* decoder
* encode করা
* decode করা

* exception
* raise করা

* expression
* statement

* frontend
* backend

* GitHub discussion
* GitHub issue

* performance
* performance optimization

* return type
* return value

* security
* security scheme

* task
* background task
* task function

* template
* template engine

* type annotation
* type hint

* server worker
* Uvicorn worker
* Gunicorn Worker
* worker process
* worker class
* workload

* deployment
* deploy করা

* SDK
* software development kit

* `APIRouter`
* `requirements.txt`
* Bearer Token
* breaking change
* bug
* button
* callable
* code
* commit
* context manager
* coroutine
* database session
* disk
* domain
* engine
* fake X
* HTTP GET method
* item
* library
* lifespan
* lock
* middleware
* mobile application
* module
* mounting
* network
* origin
* override
* payload
* processor
* property
* proxy
* pull request
* query
* RAM
* remote machine
* status code
* string
* tag
* web framework
* wildcard
* return করা
* validate করা

////

//// tab | Info

এটা docs-এ দেখা (বেশিরভাগ) technical terms-এর কোনো পুরো বা বাধ্যতামূলক তালিকা নয়। এটি prompt designer-কে বুঝতে সাহায্য করতে পারে, কোন terms-এর জন্য LLM-এর সাহায্য দরকার। যেমন যখন এটি বারবার একটি ভালো অনুবাদকে কম ভালো অনুবাদে ফিরিয়ে দেয়। অথবা যখন আপনার language-এ কোনো term-এর সাথে বিভক্তি বা suffix লাগাতে এটার সমস্যা হয়।

উদাহরণস্বরূপ `docs/de/llm-prompt.md`-এর `### List of English terms and their preferred German translations` section দেখুন।

////
