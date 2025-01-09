# FastAPI

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em> إطار عمل FastAPI, عالي الأداء, سهل التعلم, سريع في البرمجة وجاهز للإطلاق</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**الوثائق**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**كود المصدر**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI هو إطار عمل ويب حديث, سريع (عالي الأداء), لإنشاء واجهة برمجة التطبيقات (APIs) باستخدام لغة بايثون (Python), معتمدًا على تلميحات النوع القياسية في Python.


المميزات الرئيسية:

* **سريع**: أداء عالي جداً, يضاهي **NodeJS** و **Go** (بفضل Starlette و Pydantic). [أحد اسرع أُطر العمل في بايثون](#_11).
* **سريع في البرمحة**: زيادة سرعة تطوير الميزات بحوالي 200% إلى 300%. *
* **أخطاء أقل**: تقليل حوالي 40% من الأخطاء التي يسببها الإنسان (المطور). *
* **بديهي**: دعم محرر رائع. الإكمال التلقائي <abbr title="معروف أيضاً بـ auto-complete, autocompletion, IntelliSense">(Completion)</abbr> في أي مكان. وقت أقل في حل الأخطاء.
* **سهل**: صُمم ليكون سهل الاستخدام والتعلم. وقت أقل لقراءة الوثائق.
* **مختصر**: تقليل تكرار الأكواد. ميزات متعددة عند تعريف كل معلمة (parameter). أخطاء أقل.
* **قوي**: أحصل على كود جاهز للإطلاق. مع وثائق تفاعلية تلقائية.
* **مبني على المعايير**: مبنية بناءاً على (ومتوافقة كلياً مع) المعايير المفتوحة لـ APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (معروفة مسبقاً بـ Swagger) و <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* تقديرات بناءً على اختبارات لفريق تطوير داخلي قام ببناء تطبيقات إنتاجية.</small>

## الرعاة

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">الرعاة الآخرون</a>

## الآراء

"_[...] أنا استخدم **FastAPI** بشكل مكثف هذه الأيام. [...] في الواقع أخطط لاستخدامه في جميع خدمات **تعلم الآلة التي يقدمها فريقي في مايكروسوفت**. يتم دمج بعضها في منتج **Windows** وبعض منتجات **Office**._"

<div style="text-align: right; margin-right: 10%;">كبير خان - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(المرجع)</small></a></div>

---

"_لقد اعتمدنا مكتبة **FastAPI** لإنشاء خادم **REST** يمكن الاستعلام منه للحصول على **التنبؤات**. [لـ Ludwig]_"

<div style="text-align: right; margin-right: 10%;">بيرو مولينو, ياروسلاف دودين,  وساي سومانت ميرالا - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(المرجع)</small></a></div>

---

"_يسر **Netflix** أن تعلن عن إصدار مفتوح المصدر لإطار عمل **إدارة الأزمات**: **Dispatch**! [تم بناؤه باستخدام **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">كيفن جليسون, مارك فيلانوفا, وفورست مونسن - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(المرجع)</small></a></div>

---

"_أنا متحمس للغاية بشأن **FastAPI**. إنه ممتع جدًا!_"

<div style="text-align: right; margin-right: 10%;">برايان أوكن - <strong>مضيف بودكاست <a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a></strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(المرجع)</small></a></div>

---

"_بصراحة، ما قمت ببنائه يبدو متينًا ومصقولًا للغاية. من نواحٍ عديدة, إنه ما كنت أرغب أن يكون عليه **Hug** - من الملهم حقًا رؤية شخص ما يبني شيئًا كهذا._"

<div style="text-align: right; margin-right: 10%;">تيموثي كروسلي - <strong>مبتكر <a href="https://github.com/hugapi/hug" target="_blank">Hug</a></strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(المرجع)</small></a></div>

---

"_إذا كنت تبحث عن تعلم **إطار عمل حديث** لبناء واجهات REST APIs, عليك التحقق من **FastAPI** [...] إنه سريع وسهل الاستخدام وسهل التعلم [...]_"

"_لقد انتقلنا إلى استخدام **FastAPI** في **واجهاتنا البرمجية** [...] أعتقد أنك ستحبه [...]_"

<div style="text-align: right; margin-right: 10%;">إينيس مونتاني - ماثيو هونيبال - <strong>مؤسسو <a href="https://explosion.ai" target="_blank">Explosion AI</a> - مبتكرو <a href="https://spacy.io" target="_blank">spaCy</a></strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(المرجع)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(المرجع)</small></a></div>

---

"_إذا كان أي شخص يبحث عن بناء واجهات برمجية (API) للإنتاج باستخدام Python, أوصي بشدة بـ **FastAPI**. إنه **مصمم بشكل جميل**, و**سهل الاستخدام** و **قابل للتوسع بشكل كبير**, لقد أصبح **عنصراً أساسياً** في استراتيجيتنا التطويرية الأولى الخاصة بـ API ويقود العديد من الأتمتة والخدمات مثل Virtual TAC Engineer الخاص بنا._"

<div style="text-align: right; margin-right: 10%;">ديون بيلزبري - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(المرجع)</small></a></div>

---

## **Typer**, يعتبر FastAPI الخاص بواجهات الأوامر النصية (CLIs)

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

إذا كنت تقوم ببناء تطبيق واجهة أوامر نصية <abbr title="Command Line Interface">(CLI)</abbr> للاستخدام في الـ (terminal) بدلاً من API لتطبيقات ويب، يمكنك التحقق من <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** هو الأخ الأصغر لـ FastAPI. وهو مصمم ليكون **FastAPI لواجهة الأوامر النصية (CLI)**. ⌨️ 🚀

## المتطلبات

يعتمد FastAPI على المكتبات القوية:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> لجانب الويب.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> لجانب البيانات.

## التثبيت

قم بإنشاء وتفعيل <a href="https://fastapi.tiangolo.com/virtual-environments/" class="external-link" target="_blank">بيئة افتراضية (virtual environment)</a> وبعد ذلك قم بتثبيت FastAPI:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**ملاحظة**: تحقق من وضع `"fastapi[standard]"` بين علامتين تنصيص للتأكد أنها تعمل في جميع الـ (terminals).

## مثال

### قم بإنشائه

* أنشء ملف `main.py` به:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>أو <code>async def</code>...</summary>

إذا كان برنامجك يستخدم `async` / `await`, قم باستخدام `async def`:

```Python hl_lines="9  14"
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

**ملاحظة**:

إذا كنت لا تعرف, تحقق من قسم _"على عجلة؟"_ حول <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` و `await` في المستندات</a>.

</details>

### قم بتشغيله

قم بتشغيل الخادم باستخدام:

<div class="termy">

```console
$ fastapi dev main.py

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
<summary>عن الأمر <code>fastapi dev main.py</code>...</summary>

الأمر `fastapi dev` يقوم بقراءة الملف `main.py`, يتعرف على تطبيق **FastAPI** الموجود بداخله, ويقوم بتشغيل الخادم بـ <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>.

بشكل افتراضي, `fastapi dev` ستبدأ مع auto-reload (إعادة التحميل التلقائية) مفعلة للبيئة المحلية.

يمكنك قراءة المزيد على <a href="https://fastapi.tiangolo.com/fastapi-cli/" target="_blank">مستندات FastAPI CLI</a>.

</details>

### تحقق من النتيجة

افتح المتصفح على <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

سترى استجابة JSON بالشكل التالي:

```JSON
{"item_id": 5, "q": "somequery"}
```

لقد قمت بالفعل بإنشاء واجهة برمجة تطبيقات (API) تقوم بـ:

* استقبال طلبات HTTP على _المسارين_ `/` و `/items/{item_id}`.
* كلا المسارين يدعمان <em>عمليات</em> `GET` (معروفة أيضا باسم HTTP _methods_).
* _المسار_ `/items/{item_id}` يحتوي على _معلمة مسار_ `item_id` التي يجب أن تكون من النوع `int`.
* _المسار_ `/items/{item_id}` يحتوي على _معلمة استعلام_ اختيارية `q` من النوع `str`.

### وثائق API التفاعلية

الآن انتقل إلى <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

سترى وثائق API التفاعلية التلقائية (مقدمة بواسطة <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### وثائق API البديلة

والآن, انتقل إلى الرابط <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

سترى الوثائق التلقائية البديلة (مقدمة بواسطة <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## تحديث المثال

قم بتعديل الملف `main.py` ليتمكن من استقبال جسم (body) من طلب `PUT`.

يمكنك تعريف الجسم باستخدام الأنواع القياسية في Python بفضل مكتبة Pydantic.

```Python hl_lines="4  9-12  25-27"
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

الأمر `fastapi dev` يجعل الخادم يقوم بإعادة التحميل تلقائياً.

### تحديث وثائق API التفاعلية 

انتقل الآن إلى <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* ستكون وثائق API التفاعلية قد تم تحديثها تلقائياً, متضمنةً الجسم (body) الجديد.

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* أضغط على الزر "Try it out", الذي يتيح لك تعبئة المعلمات (parameters) والتفاعل مباشرة مع API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* بعد ذلك قم بضغط الزر "Execute", ستقوم واجهة المستخدم بالتواصل مع واجهة برمجة التطبيقات (API) الخاصة بك, إرسال المعلمات (parameters), واستلام النتائج، وعرضها على الشاشة:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### تحديث وثائق API البديلة

الآن انتقل إلى الرابط <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* الوثائق البديلة أيضا ستظهر المعلمة (parameter) الجديدة والجسم (body) الجديد:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### الملخص

باختصار، يمكنك تحديد أنواع المعلمات (parameters) والجسم (body) وغيرها **مرة واحدة** كمعلمات للدالة (function).

يتم ذلك باستخدام الأنواع (types) القياسية الحديثة في Python

لا حاجة لتعلم صياغة (syntax) جديدة أو استخدام methods أو classes خاصة بمكتبة معينة.

فقط استخدم **Python** القياسي.

على سبيل المثال, لتعريف عدد صحيح `int`:

```Python
item_id: int
```

أو تعريف نموذج (model) معقد مثل `Item`:

```Python
item: Item
```

...وباستخدام هذا التحديد البسيط، تحصل على:

* دعم المحرر, ويتضمن:
    * الإكمال التلقائي (Completion).
    * فحص الأنواع (Type checks).
* التحقق من صحة البيانات:
    * أخطاء تلقائية وواضحة عند وجود بيانات غير صالحة.
    * تحقق من البيانات حتى في JSON المتداخلة بعمق (nested JSON).
* تحويل <abbr title="معروف أيضاً بـ: serialization, parsing, marshalling">(Conversion)</abbr> البيانات المدخلة: القادمة من الشبكة إلى بيانات وأنواع Python. والتي يتم قراءتها من:
    * JSON.
    * معلمات المسار (Path parameters).
    * معلمات الاستعلامات (Query parameters).
    * قراءة من ملفات تعريف الارتباط (Cookies).
    * قراءة من رؤوس الطلبات (Headers).
    * قراءة من النماذج (Forms).
    * قراءة من الملفات (Files).
* تحويل <abbr title="معروف أيضاً بـ: serialization, parsing, marshalling">(Conversion)</abbr> البيانات المخرجة: تحويل من بيانات وأنواع Python إلى بيانات الشبكة (مثل JSON):
    * تحويل أنواع (types) Python (`str`, `int`, `float`, `bool`, `list`, إلخ).
    * كائنات `datetime`.
    * كائنات `UUID`.
    * نماذج قواعد البيانات (Database models).
    * ...والكثير غيرها.
* وثائق API التفاعلي التلقائي, متضمناً واجهتي مستخدم:
    * Swagger UI.
    * ReDoc.

---

بالعودة إلى مثال الكود السابق, **FastAPI** سيقوم بما يلي:

* التحقق من وجود `item_id` في المسار لطلبات `GET` و `PUT`.
* التأكد من أن `item_id` هو من النوع `int` في طلبات `GET` و `PUT`.
    * إذا لم تكن كذلك, سيظهر للعميل خطأ واضح ومفيد.
* التحقق من وجود معلمة (parameter) الاستعلام الاختياري `q` (كما في `http://127.0.0.1:8000/items/foo?q=somequery`) في طلبات `GET`.
    * بما أن المعلمة `q` تم تعريفها بقيمة افتراضية `= None`, إذا هي اختيارية.
    * بدون `None` ستكون هذه المعلمة مطلوبة (كما هو الحال مع الجسم (body) في طلبات `PUT`).
* في طلبات `PUT` لـ `/items/{item_id}`, قراءة الجسم كـ JSON:
    * التأكد من وجود الصفة (attribute) المطلوبة `name` والتي يجب أن تكون من نوع `str`.
    * التأكد من وجود الصفة (attribute) المطلوبة `price` والتي يجب أن تكون من نوع `float`.
    * التأكد من وجود الصفة (attribute) الاختيارية `is_offer`, والتي يجب أن تكون من نوع `bool`, إذا كانت موجودة.
    * كل هذا سيعمل مع كائنات JSON المتداخلة بشكل عميق (deeply nested JSON).
* التحويل من والى JSON تلقائياً.
* توثيق كل شيء بـ OpenAPI, والذي يمكن استخدامه بواسطة:
    * أنظمة التوثيق التفاعلية.
    * أنظمة إنشاء أكواد العميل تلقائيًا, للغات متعددة.
* توفر مباشرة واجهتي ويب للتوثيق التفاعلي.

---

لم نخدش سوى السطح فقط، لكنك أصبحت تفهم بالفعل الفكرة العامة عن كيفية عمل كل شيء.

جرب تغيير السطر التالي:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...من:

```Python
        ... "item_name": item.name ...
```

...إلى:

```Python
        ... "item_price": item.price ...
```

...وستلاحظ كيف أن محررك سيكمل تلقائياً الخصائص (attributes) ويعرف أنواعها:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

لمثال أكثر اكتمالا ويتضمن المزيد من الخصائص, قم بزيارة <a href="https://fastapi.tiangolo.com/tutorial/">البرنامج التعليمي - دليل المستخدم</a>.

**تنبيه الكبح**: يتضمن البرنامَج التعليمي - دليل المستخدم:

* تعريف **المعلمات (parameters)** من أماكن أخرى مثل: **headers**, **cookies**, **form** و **files**.
* كيفية ضبط **قيود التحقق** مثل `maximum_length` أو `regex` (استخدام التعبيرات النمطية).
* نظام قوي وسهل الاستخدام لـ **حقن التبعيات <abbr title="معروف ايضا بـ components, resources, providers, services, injectables">(Dependency Injection)</abbr>**.
* الأمان والمصادقة (Security and authentication), يتضمن دعم **OAuth2** مع مصادقة **JWT tokens** و **HTTP Basic**.
* تقنيات متقدمة (بنفس السهولة) لتعريف **نماذج JSON المتداخلة بعمق (deeply nested JSON models)** (بفضل Pydantic).
* تكامل **GraphQL** مع مكتبة <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> والمكتبات الأخرى.
* ميزات إضافية أخرى (بفضل Starlette) مثل:
    * **WebSockets**
    * اختبارات (tests) سهلة للغاية تعتمد على HTTPX و `pytest`
    * **CORS**
    * **جلسات الكوكيز (Cookie Sessions)**
    * ...والمزيد.

## الأداء

تظهر معايير TechEmpower المستقلة أن تطبيقات **FastAPI** التي تعمل تحت Uvicorn <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">واحدة من أسرع أطر العمل المتاحة في Python</a>, مباشرة بعد Starlette و Uvicorn (مستخدمان داخلياً بواسطة FastAPI). (*)

لفهم المزيد عن هذا, يمكنك الاطلاع على القسم <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">المعايير (Benchmarks)</a>.

## التبعيات (Dependencies)

يعتمد FastAPI على Pydantic و Starlette.

### تبعيات `standard` (التبعيات القياسية)

عند تثبيت FastAPI بالأمر `pip install "fastapi[standard]"` فإنها تتضمن مجموعة التبعيات الاختيارية القياسية (`standard`):

تستخدم بواسطة Pydantic:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - للتحقق من صحة عناوين البريد الإلكتروني.

تستخدم بواسطة Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - مطلوبة إذا كنت تريد استخدام `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - مطلوبة إذا كنت تريد استخدام تكوين القالب الافتراضي.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - مطلوب لدعم تحليل  <abbr title="تحويل النصوص التي تأتي من طلب HTTP إلى بيانات Python">"(parsing)"</abbr> النماذج, باستخدام `request.form()`.

تستخدم بواسطة FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - الخادم الذي يُحمّل ويخدم تطبيقك. يتضمن `uvicorn[standard]`, مع تبعيات إضافية (مثل `uvloop`) لتحسين الأداء.
* `fastapi-cli` - لتوفير أوامر `fastapi`.

### بدون تبعيات `standard` (بدون التبعيات القياسية)

إذا كنت لا تريد تضمين التبعيات القياسية (`standard`) الاختيارية, يمكنك التثبيت بالأمر `pip install fastapi` بدلاً عن `pip install "fastapi[standard]"`.

### تبعيات اختيارية إضافية

قد ترغب في تثبيت بعض التبعيات الإضافية وفقًا لاحتياجاتك.

تبعيات إضافية لـ Pydantic:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - لإدارة الإعدادات.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - لأنواع إضافية يمكن استخدامها مع Pydantic.

تبعيات إضافية لـ FastAPI:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - مطلوب إذا كنت تريد استخدام `ORJSONResponse`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - مطلوب إذا كنت تريد استخدام `UJSONResponse`.

## الترخيص

هذا المشروع مرخص بموجب شروط رخصة MIT.
