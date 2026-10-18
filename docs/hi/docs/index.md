---
include_yaml:
  sponsors: data/sponsors.yml
---

# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/hi"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, उच्च प्रदर्शन, सीखने में आसान, कोड लिखने में तेज़, production के लिए तैयार</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="टेस्ट">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="कवरेज">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="package संस्करण">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="समर्थित Python संस्करण">
</a>
</p>

---

**दस्तावेज़**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com/hi)

**स्रोत कोड**: [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI एक आधुनिक, तेज़ (उच्च-प्रदर्शन) web framework है जो standard Python type hints के आधार पर Python से APIs बनाने के लिए है।

मुख्य विशेषताएँ:

* **तेज़**: बहुत उच्च प्रदर्शन, **NodeJS** और **Go** के समकक्ष (Starlette और Pydantic की बदौलत)। [उपलब्ध सबसे तेज़ Python frameworks में से एक](#performance)।
* **कोड लिखने में तेज़**: features विकसित करने की गति लगभग 200% से 300% तक बढ़ाएँ। *
* **कम बग्स**: मानवीय (developer) त्रुटियों में लगभग 40% की कमी। *
* **सहज**: बेहतरीन editor support। हर जगह <dfn title="जिसे auto-complete, autocompletion, IntelliSense भी कहा जाता है">Completion</dfn>। डिबगिंग में कम समय।
* **आसान**: इस्तेमाल और सीखने में आसान होने के लिए डिज़ाइन किया गया। docs पढ़ने में कम समय।
* **संक्षिप्त**: कोड डुप्लीकेशन को न्यूनतम करें। प्रत्येक parameter declaration से कई features। कम बग्स।
* **मजबूत**: production-ready कोड प्राप्त करें। स्वतः इंटरैक्टिव दस्तावेज़ीकरण के साथ।
* **standards-आधारित**: APIs के open standards पर आधारित (और पूर्णतः अनुकूल): [OpenAPI](https://github.com/OAI/OpenAPI-Specification) (जिसे पहले Swagger कहा जाता था) और [JSON Schema](https://json-schema.org/)।

<small>* आंतरिक development team द्वारा production applications बनाते समय किए गए परीक्षणों के आधार पर अनुमान।</small>

## प्रायोजक { #sponsors }

<!-- sponsors -->

### कीस्टोन प्रायोजक { #keystone-sponsor }

<div class="fastapi-sponsors fastapi-sponsors--keystone">
{% for sponsor in sponsors.keystone -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--keystone" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}"></a>
{% endfor -%}
</div>

### गोल्ड प्रायोजक { #gold-sponsors }

<div class="fastapi-sponsors fastapi-sponsors--gold">
{% for sponsor in sponsors.gold -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--gold" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}" loading="lazy"></a>
{% endfor -%}
</div>

### सिल्वर प्रायोजक { #silver-sponsors }

<div class="fastapi-sponsors fastapi-sponsors--silver">
{% for sponsor in sponsors.silver -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--silver" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}" loading="lazy"></a>
{% endfor %}
</div>

<!-- /sponsors -->

[अन्य प्रायोजक](https://fastapi.tiangolo.com/hi/fastapi-people/#sponsors)

## विचार { #opinions }

<!-- only-mkdocs -->
<div class="fastapi-opinions" data-fastapi-opinions>
  <div class="fastapi-opinions__tabs" role="tablist" aria-label="Companies using FastAPI">
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-microsoft" aria-controls="fo-panel-microsoft" aria-selected="true" tabindex="0">
      <span class="fastapi-opinions__mark"><img src="/img/logos/microsoft.svg" alt="Microsoft" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-uber" aria-controls="fo-panel-uber" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/uber.svg" alt="Uber" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-netflix" aria-controls="fo-panel-netflix" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/netflix.svg" alt="Netflix" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-cisco" aria-controls="fo-panel-cisco" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/cisco.svg" alt="Cisco" loading="lazy"></span>
    </button>
  </div>

  <div class="fastapi-opinions__panel" id="fo-panel-microsoft" role="tabpanel" aria-labelledby="fo-tab-microsoft" tabindex="0">
    <blockquote class="fastapi-opinions__quote">"मैं इन दिनों <strong>FastAPI</strong> का बहुत उपयोग कर रहा/रही हूँ। वास्तव में मैं अपनी team की <strong>Microsoft में ML सेवाओं</strong> के लिए इसे उपयोग करने की योजना बना रहा/रही हूँ। इनमें से कुछ को मुख्य <strong>Windows</strong> product और कुछ <strong>Office</strong> products में इंटीग्रेट किया जा रहा है।"</blockquote>
    <div class="fastapi-opinions__attr">— कबीर खान, <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26">(संदर्भ)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-uber" role="tabpanel" aria-labelledby="fo-tab-uber" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">"हमने <strong>FastAPI</strong> लाइब्रेरी अपनाई ताकि एक <strong>REST</strong> सर्वर स्पॉन किया जा सके जिसे <strong>अन्दाज़ों/अनुमानों</strong> को प्राप्त करने के लिए query किया जा सके।" <em>[Ludwig के लिए]</em></blockquote>
    <div class="fastapi-opinions__attr">— पिएरो मोलिनो, यारोस्लाव डुडिन, साई सुमंत मिर्याला, <strong>Uber</strong> <a href="https://www.uber.com/us/en/blog/ludwig-v0-2/">(संदर्भ)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-netflix" role="tabpanel" aria-labelledby="fo-tab-netflix" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">"<strong>Netflix</strong> हमारे <strong>संकट प्रबंधन</strong> ऑर्केस्ट्रेशन framework: <strong>Dispatch</strong> के ओपन-सोर्स रिलीज़ की घोषणा करते हुए प्रसन्न है!" <em>[FastAPI के साथ बनाया गया]</em></blockquote>
    <div class="fastapi-opinions__attr">— केविन ग्लिसन, मार्क विलानोवा, फॉरेस्ट मॉन्सेन, <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072">(संदर्भ)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-cisco" role="tabpanel" aria-labelledby="fo-tab-cisco" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">"यदि कोई production Python API बनाना चाहता है, तो मैं <strong>FastAPI</strong> की अत्यधिक अनुशंसा करूंगा/करूंगी। यह <strong>सुंदरता से डिज़ाइन</strong> किया गया है, <strong>उपयोग में सरल</strong> है और <strong>बेहद स्केलेबल</strong> है — यह हमारी API-फर्स्ट development रणनीति का <strong>मुख्य घटक</strong> बन गया है।"</blockquote>
    <div class="fastapi-opinions__attr">— डीयोन पिल्सबरी, <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/">(संदर्भ)</a></div>
  </div>
</div>
<!-- /only-mkdocs -->

<div class="only-github" markdown="1">

"_[...] मैं इन दिनों **FastAPI** का बहुत उपयोग कर रहा/रही हूँ। [...] वास्तव में मैं अपनी team की **Microsoft में ML सेवाओं** के लिए इसे उपयोग करने की योजना बना रहा/रही हूँ। इनमें से कुछ को मुख्य **Windows** product और कुछ **Office** products में इंटीग्रेट किया जा रहा है._"

<div style="text-align: right; margin-right: 10%;">कबीर खान - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(संदर्भ)</small></a></div>

---

"_हमने **FastAPI** लाइब्रेरी अपनाई ताकि एक **REST** सर्वर स्पॉन किया जा सके जिसे **अनुमानों** को प्राप्त करने के लिए query किया जा सके। [Ludwig के लिए]_"

<div style="text-align: right; margin-right: 10%;">पिएरो मोलिनो, यारोस्लाव डुडिन, और साई सुमंत मिर्याला - <strong>Uber</strong> <a href="https://www.uber.com/us/en/blog/ludwig-v0-2/"><small>(संदर्भ)</small></a></div>

---

"_**Netflix** हमारे **संकट प्रबंधन** ऑर्केस्ट्रेशन framework: **Dispatch** के ओपन-सोर्स रिलीज़ की घोषणा करते हुए प्रसन्न है! [**FastAPI** के साथ बनाया गया]_"

<div style="text-align: right; margin-right: 10%;">केविन ग्लिसन, मार्क विलानोवा, फॉरेस्ट मॉन्सेन - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(संदर्भ)</small></a></div>

---

"_यदि कोई production Python API बनाना चाहता है, तो मैं **FastAPI** की अत्यधिक अनुशंसा करूंगा/करूंगी। यह **सुंदरता से डिज़ाइन** किया गया है, **उपयोग में सरल** है और **बेहद स्केलेबल** है, यह हमारी API first development रणनीति का **मुख्य घटक** बन गया है और हमारे Virtual TAC Engineer जैसे कई ऑटोमेशन्स और सेवाओं को चला रहा है._"

<div style="text-align: right; margin-right: 10%;">डीयोन पिल्सबरी - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(संदर्भ)</small></a></div>

---

</div>

## FastAPI मिनी डॉक्यूमेंट्री { #fastapi-mini-documentary }

साल 2025 के अंत में एक [FastAPI मिनी डॉक्यूमेंट्री](https://www.youtube.com/watch?v=mpR8ngthqiE) रिलीज़ हुई, आप इसे ऑनलाइन देख सकते हैं:

<a class="fastapi-feature-banner" href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI मिनी डॉक्यूमेंट्री"></a>

## **Typer**, CLIs का FastAPI { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

यदि आप web API के बजाय टर्मिनल में उपयोग होने वाला <abbr title="Command Line Interface - कमांड लाइन इंटरफ़ेस">CLI</abbr> ऐप बना रहे हैं, तो [**Typer**](https://typer.tiangolo.com/) देखें।

**Typer**, FastAPI का छोटा भाई/बहन है। और इसका उद्देश्य **CLIs का FastAPI** होना है। ⌨️ 🚀

## आवश्यकताएँ { #requirements }

FastAPI दिग्गजों के कंधों पर खड़ा है:

* web हिस्सों के लिए [Starlette](https://starlette.dev/)।
* data हिस्सों के लिए [Pydantic](https://pydantic.dev/docs/)।

## Installation { #installation }

पहले, [`uv` install करें](https://docs.astral.sh/uv/getting-started/installation/), और फिर अपने project में FastAPI जोड़ें:

<div class="termy">

```console
$ uv add "fastapi[standard]"

---> 100%
```

</div>

**नोट**: सुनिश्चित करें कि आप सभी टर्मिनलों में काम करने के लिए `"fastapi[standard]"` को उद्धरण-चिह्नों में रखें।

यदि आप `pip` का उपयोग करना पसंद करते हैं, तो virtual environment के अंदर `fastapi[standard]` install करें। वैकल्पिक चरणों के लिए [installation guide](tutorial/#install-fastapi) देखें।

## उदाहरण { #example }

### इसे बनाएँ { #create-it }

`main.py` file बनाएँ, जिसमें:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>या <code>async def</code> का उपयोग करें...</summary>

यदि आपका कोड `async` / `await` का उपयोग करता है, तो `async def` का उपयोग करें:

```Python hl_lines="7  12"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

**नोट**:

यदि आप नहीं जानते, तो docs में [`async` और `await`](https://fastapi.tiangolo.com/hi/async/#in-a-hurry) के बारे में _"जल्दी में?"_ section देखें।

</details>

### इसे चलाएँ { #run-it }

सर्वर को इस कमांड से चलाएँ:

<div class="termy">

```console
$ uv run fastapi dev

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary><code>fastapi dev</code> कमांड के बारे में...</summary>

`fastapi dev` कमांड आपका `main.py` file स्वतः पढ़ता है, उसमें **FastAPI** ऐप का पता लगाता है, और [Uvicorn](https://uvicorn.dev) का उपयोग करके सर्वर शुरू करता है।

default रूप से, `fastapi dev` लोकल development के लिए auto-reload सक्षम करके शुरू होगा।

आप इसके बारे में और पढ़ सकते हैं: [FastAPI CLI docs](https://fastapi.tiangolo.com/hi/fastapi-cli/) में।

</details>

### इसे जाँचें { #check-it }

अपने ब्राउज़र में [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery) खोलें।

आपको JSON response इस प्रकार दिखेगी:

```JSON
{"item_id": 5, "q": "somequery"}
```

आपने पहले ही एक API बना ली है जो:

* _paths_ `/` और `/items/{item_id}` पर HTTP requests स्वीकार करती है।
* दोनों _paths_ `GET` <em>operations</em> लेती हैं (जिन्हें HTTP _methods_ भी कहा जाता है)।
* _path_ `/items/{item_id}` में एक _path parameter_ `item_id` है जो `int` होना चाहिए।
* _path_ `/items/{item_id}` में एक वैकल्पिक `str` _query parameter_ `q` है।

### इंटरैक्टिव API दस्तावेज़ { #interactive-api-docs }

अब [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) पर जाएँ।

आपको स्वचालित इंटरैक्टिव API दस्तावेज़ीकरण दिखेगा (जो [Swagger UI](https://github.com/swagger-api/swagger-ui) द्वारा प्रदान किया जाता है):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### वैकल्पिक API दस्तावेज़ { #alternative-api-docs }

और अब, [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) पर जाएँ।

आपको वैकल्पिक स्वचालित दस्तावेज़ीकरण दिखेगा (जो [ReDoc](https://github.com/Redocly/redoc) द्वारा प्रदान किया जाता है):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## उदाहरण उन्नयन { #example-upgrade }

अब `PUT` request से body प्राप्त करने के लिए `main.py` file संशोधित करें।

Pydantic की बदौलत, body को standard Python प्रकारों से घोषित करें।

```Python hl_lines="2  7-10 23-25"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

`fastapi dev` सर्वर स्वतः रीलोड होना चाहिए।

### इंटरैक्टिव API दस्तावेज़ उन्नयन { #interactive-api-docs-upgrade }

अब [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) पर जाएँ।

* इंटरैक्टिव API दस्तावेज़ स्वतः अपडेट हो जाएगा, नए body सहित:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* "Try it out" बटन पर क्लिक करें, यह आपको parameters भरने और सीधे API के साथ इंटरेक्ट करने की अनुमति देता है:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* फिर "Execute" बटन पर क्लिक करें, यूज़र इंटरफ़ेस आपकी API से संवाद करेगा, parameters भेजेगा, परिणाम प्राप्त करेगा और उन्हें स्क्रीन पर दिखाएगा:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### वैकल्पिक API दस्तावेज़ उन्नयन { #alternative-api-docs-upgrade }

और अब, [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) पर जाएँ।

* वैकल्पिक दस्तावेज़ भी नए query parameter और body को दर्शाएगा:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Recap { #recap }

संक्षेप में, आप parameters, body, आदि के प्रकार function parameters के रूप में **एक बार** घोषित करते हैं।

आप यह standard आधुनिक Python प्रकारों से करते हैं।

आपको किसी नई सिंटैक्स, किसी विशेष लाइब्रेरी के methods या classes, आदि सीखने की आवश्यकता नहीं है।

बस standard **Python**।

उदाहरण के लिए, एक `int` के लिए:

```Python
item_id: int
```

या एक अधिक जटिल `Item` model के लिए:

```Python
item: Item
```

...और केवल उसी एक घोषणा के साथ आपको मिलता है:

* Editor support, जिसमें शामिल है:
    * Completion।
    * Type checks।
* data का वैधीकरण:
    * जब data अमान्य हो तो स्वतः और स्पष्ट त्रुटियाँ।
    * गहराई से nested JSON objects के लिए भी वैधीकरण।
* इनपुट data का <dfn title="जिसे serialization, parsing, marshalling भी कहा जाता है">Conversion</dfn>: नेटवर्क से Python data और प्रकारों में। इनमें से पढ़ना:
    * JSON।
    * Path parameters।
    * Query parameters।
    * Cookies।
    * Headers।
    * Forms।
    * Files।
* आउटपुट data का <dfn title="जिसे serialization, parsing, marshalling भी कहा जाता है">Conversion</dfn>: Python data और प्रकारों से नेटवर्क data (JSON के रूप में) में:
    * Python प्रकारों का conversion (`str`, `int`, `float`, `bool`, `list`, आदि)।
    * `datetime` ऑब्जेक्ट्स।
    * `UUID` ऑब्जेक्ट्स।
    * डेटाबेस models।
    * ...और बहुत कुछ।
* स्वचालित इंटरैक्टिव API दस्तावेज़ीकरण, जिनमें 2 वैकल्पिक यूज़र इंटरफ़ेस शामिल हैं:
    * Swagger UI।
    * ReDoc।

---

पिछले कोड उदाहरण पर लौटते हुए, **FastAPI** यह करेगा:

* `GET` और `PUT` requests के लिए path में `item_id` है, यह सत्यापित करेगा।
* `GET` और `PUT` requests के लिए `item_id` का प्रकार `int` है, यह सत्यापित करेगा।
    * यदि नहीं है, तो क्लाइंट को एक उपयोगी, स्पष्ट त्रुटि दिखाई देगी।
* `GET` requests के लिए यह जाँच करेगा कि `q` नाम का एक वैकल्पिक query parameter है (जैसे `http://127.0.0.1:8000/items/foo?q=somequery`)।
    * क्योंकि `q` parameter `= None` के साथ घोषित है, यह वैकल्पिक है।
    * `None` के बिना यह required होता (जैसे `PUT` के मामले में body required है)।
* `/items/{item_id}` पर `PUT` requests के लिए, body को JSON के रूप में पढ़ेगा:
    * यह जाँचेगा कि एक required attribute `name` है जो `str` होना चाहिए।
    * यह जाँचेगा कि एक required attribute `price` है जो `float` होना चाहिए।
    * यह जाँचेगा कि एक वैकल्पिक attribute `is_offer` है, जो यदि मौजूद है तो `bool` होना चाहिए।
    * यह सब गहराई से nested JSON objects के लिए भी काम करेगा।
* JSON से और JSON में स्वतः convert करेगा।
* हर चीज़ को OpenAPI के साथ दस्तावेज़ित करेगा, जिसे निम्न द्वारा उपयोग किया जा सकता है:
    * इंटरैक्टिव दस्तावेज़ीकरण प्रणालियाँ।
    * कई भाषाओं के लिए स्वचालित क्लाइंट कोड जनरेशन प्रणालियाँ।
* सीधे 2 इंटरैक्टिव दस्तावेज़ीकरण web interfaces प्रदान करेगा।

---

हमने केवल सतह को छुआ है, लेकिन आपको पहले ही समझ आ गया होगा कि यह सब कैसे काम करता है।

इस पंक्ति को बदलकर देखें:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...यहाँ से:

```Python
        ... "item_name": item.name ...
```

...यहाँ तक:

```Python
        ... "item_price": item.price ...
```

...और देखें कि आपका editor attributes को कैसे auto-complete करेगा और उनके प्रकार जानेगा:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

अधिक features सहित एक अधिक सम्पूर्ण उदाहरण के लिए, <a href="https://fastapi.tiangolo.com/hi/tutorial/">ट्यूटोरियल - यूज़र गाइड</a> देखें।

**स्पॉइलर अलर्ट**: ट्यूटोरियल - यूज़र गाइड में शामिल है:

* विभिन्न स्थानों से **parameters** की घोषणा: **headers**, **cookies**, **form fields** और **files**।
* `maximum_length` या `regex` जैसी **validation constraints** कैसे सेट करें।
* एक बहुत शक्तिशाली और उपयोग में आसान **<dfn title="जिन्हें components, resources, providers, services, injectables भी कहा जाता है">Dependency Injection</dfn>** सिस्टम।
* सुरक्षा और प्रमाणीकरण, जिसमें **OAuth2** के साथ **JWT tokens** और **HTTP Basic** auth का समर्थन शामिल है।
* **गहराई से nested JSON models** घोषित करने की अधिक उन्नत (पर समान रूप से आसान) तकनीकें (Pydantic की बदौलत)।
* [Strawberry](https://strawberry.rocks) और अन्य लाइब्रेरीज़ के साथ **GraphQL** एकीकरण।
* कई अतिरिक्त features (Starlette की बदौलत) जैसे:
    * **WebSockets**
    * HTTPX और `pytest` पर आधारित अत्यंत आसान टेस्ट्स
    * **CORS**
    * **Cookie Sessions**
    * ...आदि।

### अपनी ऐप deploy करें (वैकल्पिक) { #deploy-your-app-optional }

आप वैकल्पिक रूप से अपनी FastAPI ऐप को [FastAPI Cloud](https://fastapicloud.com) पर एक ही कमांड से deploy कर सकते हैं। 🚀

<div class="termy">

```console
$ uv run fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

CLI आपकी FastAPI application को स्वतः पहचान लेगा और उसे क्लाउड पर deploy करेगा। यदि आप logged in नहीं हैं, तो प्रमाणीकरण प्रक्रिया पूरी करने के लिए आपका ब्राउज़र खुलेगा।

बस इतना ही! अब आप उस URL पर अपनी ऐप एक्सेस कर सकते हैं। ✨

#### FastAPI Cloud के बारे में { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** को **FastAPI** के ही लेखक और team ने बनाया है।

यह न्यूनतम प्रयास में किसी API को **बनाने**, **deploy** करने और **एक्सेस** करने की प्रक्रिया को सरल बनाता है।

यह FastAPI के साथ ऐप्स बनाने के उसी **developer experience** को उन्हें क्लाउड में **deploy** करने तक लाता है। 🎉

FastAPI Cloud, *FastAPI and friends* ओपन सोर्स projects के लिए मुख्य प्रायोजक और फंडिंग प्रदाता है। ✨

#### अन्य क्लाउड प्रदाताओं पर deploy करें { #deploy-to-other-cloud-providers }

FastAPI ओपन सोर्स है और standards पर आधारित है। आप FastAPI ऐप्स को किसी भी क्लाउड प्रदाता पर deploy कर सकते हैं।

अपने क्लाउड प्रदाता के गाइड्स का पालन करें और उनके साथ FastAPI ऐप्स deploy करें। 🤓

## प्रदर्शन { #performance }

स्वतंत्र TechEmpower बेंचमार्क दिखाते हैं कि Uvicorn के तहत चलने वाले **FastAPI** applications [उपलब्ध सबसे तेज़ Python frameworks में से एक](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7) हैं, केवल Starlette और Uvicorn (जो FastAPI द्वारा आंतरिक रूप से उपयोग किए जाते हैं) से नीचे। (*)

इसके बारे में अधिक समझने के लिए, [बेंचमार्क्स](https://fastapi.tiangolo.com/hi/benchmarks/) section देखें।

## निर्भरताएँ { #dependencies }

FastAPI, Pydantic और Starlette पर निर्भर करता है।

### `standard` निर्भरताएँ { #standard-dependencies }

जब आप `uv add "fastapi[standard]"` के साथ FastAPI install करते हैं, तो यह `standard` समूह की वैकल्पिक निर्भरताओं के साथ आता है:

Pydantic द्वारा उपयोग किया गया:

* [`email-validator`](https://github.com/JoshData/python-email-validator) - ईमेल वैधीकरण के लिए।

Starlette द्वारा उपयोग किया गया:

* [`httpx`](https://www.python-httpx.org) - यदि आप `TestClient` का उपयोग करना चाहते हैं तो required।
* [`jinja2`](https://jinja.palletsprojects.com) - यदि आप default टेम्पलेट कॉन्फ़िगरेशन का उपयोग करना चाहते हैं तो required।
* [`python-multipart`](https://github.com/Kludex/python-multipart) - यदि आप form <dfn title="HTTP request से आने वाली string को Python data में convert करना">"parsing"</dfn> का समर्थन करना चाहते हैं, `request.form()` के साथ, तो required।

FastAPI द्वारा उपयोग किया गया:

* [`uvicorn`](https://uvicorn.dev) - उस सर्वर के लिए जो आपकी application को लोड और सर्व करता है। इसमें `uvicorn[standard]` शामिल है, जिसमें high performance serving के लिए कुछ निर्भरताएँ (जैसे `uvloop`) शामिल हैं।
* `fastapi-cli[standard]` - `fastapi` कमांड प्रदान करने के लिए।
    * इसमें `fastapi-cloud-cli` शामिल है, जो आपको अपनी FastAPI application को [FastAPI Cloud](https://fastapicloud.com) पर deploy करने की अनुमति देता है।

### `standard` निर्भरताओं के बिना { #without-standard-dependencies }

यदि आप `standard` वैकल्पिक निर्भरताओं को शामिल नहीं करना चाहते, तो आप `uv add "fastapi[standard]"` के बजाय `uv add fastapi` के साथ install कर सकते हैं।

### `fastapi-cloud-cli` के बिना { #without-fastapi-cloud-cli }

यदि आप standard निर्भरताओं के साथ लेकिन `fastapi-cloud-cli` के बिना FastAPI install करना चाहते हैं, तो `uv add "fastapi[standard-no-fastapi-cloud-cli]"` के साथ install कर सकते हैं।

### अतिरिक्त वैकल्पिक निर्भरताएँ { #additional-optional-dependencies }

कुछ अतिरिक्त निर्भरताएँ हैं जिन्हें आप install करना चाहेंगे।

अतिरिक्त वैकल्पिक Pydantic निर्भरताएँ:

* [`pydantic-settings`](https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/) - सेटिंग्स प्रबंधन के लिए।
* [`pydantic-extra-types`](https://github.com/pydantic/pydantic-extra-types) - Pydantic के साथ उपयोग करने के लिए अतिरिक्त प्रकारों हेतु।

अतिरिक्त वैकल्पिक FastAPI निर्भरताएँ:

* [`orjson`](https://github.com/ijl/orjson) - यदि आप `ORJSONResponse` उपयोग करना चाहते हैं तो required।
* [`ujson`](https://github.com/ultrajson/ultrajson) - यदि आप `UJSONResponse` उपयोग करना चाहते हैं तो required।

## लाइसेंस { #license }

यह project MIT license की शर्तों के अंतर्गत लाइसेंस प्राप्त है।
