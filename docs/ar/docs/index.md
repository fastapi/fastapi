<div dir="rtl">

{!../../../docs/missing-translation.md!}

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>إطار FastAPI ، أداء عالٍ ، سهل التعلم ، سريع البرمجة ، جاهز للإنتاج</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---

**توثيق**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**مصدر الرمز**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI هو إطار عمل ويب حديث وسريع (عالي الأداء) لبناء واجهات برمجة التطبيقات باستخدام Python 3.6+ استنادًا إلى تلميحات نوع Python القياسية.

الميزات الرئيسية هي:

- **سريع**: أداء عالٍ جدًا ، على قدم المساواة مع **NodeJS** و **Go** (بفضل Starlette و Pydantic). [أحد أسرع أطر عمل بايثون المتاحة](#performance).

- **سريع في الكود**: زيادة سرعة تطوير الميزات بحوالي 200٪ إلى 300٪. \*
- **أخطاء أقل**: تقليل حوالي 40٪ من الأخطاء التي يسببها الإنسان (المطور). \*
- **حدسي**: دعم محرر رائع. <abbr title="also known as auto-complete, autocompletion, IntelliSense">إكمال</abbr> في كل مكان. وقت أقل في التصحيح.
- **سهل**: مصمم ليكون سهل الاستخدام والتعلم. وقت أقل في قراءة المستندات.
- **قصير**: قلل من تكرار الكود. ميزات متعددة من كل إعلان معلمة. عدد أقل من البق.
- **قوي**: احصل على رمز جاهز للإنتاج. مع التوثيق التفاعلي التلقائي.
- **قائم على المعايير**: استنادًا إلى (ومتوافق تمامًا مع) المعايير المفتوحة لواجهات برمجة التطبيقات: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (المعروف سابقًا باسم Swagger) و<a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>\*تقدير بناءً على اختبارات فريق التطوير الداخلي ، وبناء تطبيقات الإنتاج.</small>

## الرعاة الذهبيون

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">الرعاة الآخرين</a>

## Opinions

"_[...] I'm using **FastAPI** a ton these days. [...] I'm actually planning to use it for all of my team's **ML services at Microsoft**. Some of them are getting integrated into the core **Windows** product and some **Office** products._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_We adopted the **FastAPI** library to spawn a **REST** server that can be queried to obtain **predictions**. [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** is pleased to announce the open-source release of our **crisis management** orchestration framework: **Dispatch**! [built with **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_I’m over the moon excited about **FastAPI**. It’s so fun!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Honestly, what you've built looks super solid and polished. In many ways, it's what I wanted **Hug** to be - it's really inspiring to see someone build that._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_If you're looking to learn one **modern framework** for building REST APIs, check out **FastAPI** [...] It's fast, easy to use and easy to learn [...]_"

"_We've switched over to **FastAPI** for our **APIs** [...] I think you'll like it [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, the FastAPI of CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

إذا كنت تقوم ببناء ملف<abbr title="Command Line Interface">CLI</abbr> التطبيق ليتم استخدامه في المحطة بدلاً من واجهة برمجة تطبيقات الويب ، تحقق من <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** هو شقيق FastAPI الصغير. ومن المفترض أن يكون **FastAPI of CLIs**. ⌨️ 🚀

## متطلبات

Python 3.6+

يقف FastAPI على أكتاف العمالقة:

- <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> لأجزاء الويب.
- <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> لأجزاء البيانات.

## تنصيب

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

ستحتاج أيضًا إلى خادم ASGI للإنتاج مثل<a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> أو <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## مثال

### اصنعها

- قم بإنشاء ملف `main.py` مع:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>او استعمل <code>async def</code>...</summary>

إذا كان الرمز الخاص بك يستخدم `async` / `await`, استعمال `async def`:

```Python hl_lines="9 14"
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

**ملحوظة**:

إذا كنت لا تعرف ، فتحقق من _"In a hurry?"_ قسم حول <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` و `await` في المستندات</a>.

</details>

### شغلها

قم بتشغيل الخادم باستخدام:

<div class="termy">

```console
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>عن الأمر <code>uvicorn main:app --reload</code>...</summary>

الامر `uvicorn main:app` يعود الى:

- `main`:الملف `main.py` (وحدة Python).
- `app`: الكائن الذي تم إنشاؤه داخل`main.py` مع الخط `app = FastAPI()`.
- `--reload`: قم بإعادة تشغيل الخادم بعد تغيير الكود. افعل هذا فقط من أجل التنمية.

</details>

### افحصها

افتح المتصفح الخاص بك على<a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

سترى استجابة JSON على النحو التالي:

```JSON
{"item_id": 5, "q": "somequery"}
```

لقد قمت بالفعل بإنشاء واجهة برمجة تطبيقات:

- يتلقى طلبات HTTP في ملف _paths_ `/` و `/items/{item_id}`.
- كلاهما _paths_ يأخذ `GET` <em>عمليات</em> (المعروف أيضًا باسم HTTP _methods_).
- ال _path_ `/items/{item_id}` لديه _path parameter_ `item_id` يجب أن يكون `int`.
- ال _path_ `/items/{item_id}` اختياري `str` _query parameter_ `q`.

### مستندات API التفاعلية

اذهب الآن إلى <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

سترى وثائق API التفاعلية التلقائية (المقدمة بواسطة <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### بديل مستندات API

والآن ، اذهب إلى <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

سترى الوثائق التلقائية البديلة (المقدمة بواسطة <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## ترقية المثال

الآن قم بتعديل الملف `main.py` لتلقي جثة من أ `PUT` طلب.

قم بتعريف الجسم باستخدام أنواع Python القياسية ، وذلك بفضل Pydantic.

```Python hl_lines="4  9 10 11 12  25 26 27"
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

يجب إعادة تحميل الخادم تلقائيًا (لأنك أضفت`--reload` الى `uvicorn` الأمر أعلاه).

### ترقية مستندات API التفاعلية

اذهب الآن إلى <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

- سيتم تحديث وثائق API التفاعلية تلقائيًا ، بما في ذلك الهيكل الجديد:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

- انقر فوق الزر "جربه" ، فهو يسمح لك بملء المعلمات والتفاعل مباشرة مع واجهة برمجة التطبيقات:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

- ثم انقر فوق الزر "تنفيذ" ، ستتواصل واجهة المستخدم مع واجهة برمجة التطبيقات الخاصة بك ، وترسل المعلمات ، وتحصل على النتائج وتعرضها على الشاشة:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### ترقية مستندات API البديلة

والآن ، اذهب إلى <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

- ستعكس الوثائق البديلة أيضًا معامِل طلب البحث الجديد ونصه:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### خلاصة

باختصار ، تعلن **مرة واحدة** أنواع المعلمات والجسم وما إلى ذلك كمعلمات دالة.

يمكنك القيام بذلك باستخدام أنواع Python القياسية الحديثة.

لست مضطرًا إلى تعلم بناء جملة جديد ، أو طرق أو فئات مكتبة معينة ، وما إلى ذلك.

معيار فقط **Python 3.6 +**.

على سبيل المثال ، من أجل ملف `int`:

```Python
item_id: int
```

أو لأكثر تعقيدًا `Item` نموذج:

```Python
item: Item
```

...وبهذا الإعلان الوحيد تحصل على:

- دعم المحرر ، بما في ذلك:
  - إكمال.
  - نوع الشيكات.
- التحقق من صحة البيانات:
  - أخطاء تلقائية وواضحة عندما تكون البيانات غير صالحة.
  - التحقق من الصحة حتى بالنسبة لكائنات JSON المتداخلة بشدة.
- <abbr title="also known as: serialization, parsing, marshalling">تحويلات</abbr> من بيانات الإدخال: القادمة من الشبكة إلى بيانات وأنواع بايثون. القراءة من:
- JSON.
  - معلمات المسار.
  - معلمات الاستعلام.
  - بسكويت.
  - رؤوس.
  - نماذج.
  - الملفات.
- <abbr title="also known as: serialization, parsing, marshalling">تحويلات</abbr>من بيانات الإخراج: التحويل من بيانات وأنواع Python إلى بيانات الشبكة (مثل JSON):
  - تحويل أنواع بايثون (`str`, `int`, `float`, `bool`, `list`, إلخ).
  - `datetime` شيء.
  - `UUID` شيء.
  - نماذج قواعد البيانات.
  - ...و أكثر من ذلك بكثير.
- وثائق API تفاعلية تلقائية ، بما في ذلك واجهتان بديلتان للمستخدم:
  - Swagger UI.
  - ReDoc.

---

بالعودة إلى مثال الكود السابق ، **FastAPI**إرادة:

- تحقق من وجود ملف `item_id` في الطريق ل`GET` و `PUT` الطلبات.
- تحقق من أن ملف `item_id` من النوع `int` ل `GET` و `PUT` الطلبات.
  - إذا لم يكن كذلك ، سيرى العميل خطأ مفيد وواضح.
- تحقق مما إذا كان هناك معلمة استعلام اختيارية مسماة `q` (مثل `http://127.0.0.1:8000/items/foo?q=somequery`) ل `GET` الطلبات.
  - مثل`q` تم التصريح عن المعلمة مع `= None`,إنه اختياري.
  -بدون ال `None` سيكون مطلوبًا (كما هو الحال مع الجسم في الحالة `PUT`).
- ل `PUT` طلبات `/items/{item_id}`, اقرأ النص كـ JSON:
  - تحقق من أن لها سمة مطلوبة `name` يجب أن يكون `str`.
  - تحقق من أن لها سمة مطلوبة `price` يجب أن يكون `float`.
  - تحقق من أن لها سمة اختيارية `is_offer`, يجب أن يكون `bool`, إذا كان موجودا.
  - يعمل كل هذا أيضًا مع كائنات JSON المتداخلة بعمق.
- التحويل من وإلى JSON تلقائيًا.
- توثيق كل شيء باستخدام OpenAPI ، والذي يمكن استخدامه بواسطة:
  - أنظمة التوثيق التفاعلية.
  - أنظمة إنشاء كود العميل الآلي للعديد من اللغات.
- توفير واجهتي ويب تفاعليتين للتوثيق مباشرة.

---

لقد خدشنا السطح للتو ، لكنك حصلت بالفعل على فكرة عن كيفية عمل كل شيء.

حاول تغيير الخط بـ:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...من عند:

```Python
        ... "item_name": item.name ...
```

...ل:

```Python
        ... "item_price": item.price ...
```

... وشاهد كيف سيقوم المحرر الخاص بك بإكمال السمات تلقائيًا ومعرفة أنواعها:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

للحصول على مثال أكثر اكتمالاً بما في ذلك المزيد من الميزات ، راجع <a href="https://fastapi.tiangolo.com/tutorial/">البرنامج التعليمي - دليل المستخدم</a>.

**تنبيه المفسد**: البرنامج التعليمي - دليل المستخدم يتضمن:

- إعلان **المعلمات** من أماكن مختلفة أخرى مثل: **الرؤوس** ، **ملفات تعريف الارتباط** ، **حقول النموذج** و **الملفات**.
- كيفية تعيين **قيود التحقق** على أنها `maximum_length` أو `regex`.
- قوي جدا وسهل الاستخدام **<abbr title="also known as components, resources, providers, services, injectables">حقن التبعية</abbr>** النظام.
- الأمان والمصادقة ، بما في ذلك دعم ملفات **OAuth2** مع **JWT tokens** و **HTTP Basic** المصادقة.
- تقنيات أكثر تقدمًا (ولكن بنفس السهولة) للتصريح **نماذج JSON المتداخلة بعمق** (بفضل Pydantic).
- العديد من الميزات الإضافية (بفضل Starlette) مثل:
  - **WebSockets**
  - **GraphQL**
  - اختبارات سهلة للغاية تعتمد على `requests` و `pytest`
  - **CORS**
  - **Cookie Sessions**
  - ...و اكثر.

## أداء

تظهر معايير TechEmpower المستقلة **FastAPI** التطبيقات التي تعمل تحت Uvicorn مثل<a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">أحد أسرع أطر عمل Python المتاحة</a>, فقط أسفل Starlette و Uvicorn أنفسهم (المستخدمة داخليًا بواسطة FastAPI). (\*)

To understand more about it, see the section <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## التبعيات الاختيارية

استعمل من قبل Pydantic:

- <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - لـ JSON أسرع <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>.
- <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - للتحقق من صحة البريد الإلكتروني.

استعمل من قبل Starlette:

- <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - مطلوب إذا كنت تريد استخدام `TestClient`.
- <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - مطلوب إذا كنت تريد استخدام `FileResponse` أو `StaticFiles`.
- <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - مطلوب إذا كنت تريد استخدام تكوين القالب الافتراضي.
- <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - مطلوب إذا كنت تريد دعم النموذج <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>, مع `request.form()`.
- <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - مطلوب ل `SessionMiddleware` الدعم.
- <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - مطلوب ل Starlette's `SchemaGenerator` الدعم (ربما لا تحتاجه به FastAPI).
- <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - مطلوب ل `GraphQLApp` الدعم.
- <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - مطلوب إذا كنت تريد استخدام `UJSONResponse`.

استعمل من قبل FastAPI / Starlette:

- <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - للخادم الذي يقوم بتحميل التطبيق الخاص بك ويخدمه.
- <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - مطلوب إذا كنت تريد استخدام `ORJSONResponse`.

يمكنك تثبيت كل هذه مع `pip install fastapi[all]`.

## رخصة

هذا المشروع مرخص بموجب شروط ترخيص معهد ماساتشوستس للتكنولوجيا.

</div>
