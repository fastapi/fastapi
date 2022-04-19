
{!../../../docs/missing-translation.md!}


<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI یک فریمورک با کارایی بالا، یادگیری آسان، کدنویسی سریع، آماده برای تولید است.</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**مستندات**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**کد منبع**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI یک فریمورک وب مدرن، سریع (با کارایی بالا) برای ساخت API با پایتون بالاتر از ۳.۶ بر اساس تایپ های کمکی استاندار پایتون است.

ویژگی های کلیدی:

* **سریع**: عملکرد بسیار بالا در حد **NodeJS** و **Go** (با تشکر از Starlette و Pydantic). [یکی از سریع ترین چارچوب های پایتون موجود است](#performance).

* **سریع در کد**: سرعت توسعه ویژگی ها را تا ۲۰۰٪ تا ۳۰۰٪ افزایش می‌دهد. *
* **باگ های کمتر**: حدود 40 درصد از خطاهای انسانی (توسعه دهندگان) را کاهش می دهد. *
* **شهودی**: پشتیبانی عالی از. <abbr title="همچنین با نام های auto-complete, autocompletion, IntelliSense نیز شناخته می‌شود">Completion</abbr> ویرایشگر ها در همه جا. زبان کمتری برای دیباگ کردن نیاز است. *
* **ساده**: طراحی شده تا استفاده و یادگیری آسان باشد. زمان کمتری برای خواندن اسناد نیاز است.
* **کوتاه**: تکرار کد را به حداقل برسانید. ویژگی های متعدد از هر اعلان پارامتر. اشکالات کمتر.
* **قدرتمند**: کد آماده تولید همراه اسناد تعاملی خودکار دریافت کنید.
* **Standards-based**: بر اساس (و کاملاً سازگار با) استانداردهای باز برای APIها: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (قبلا با نام Swagger شناخته می شد) و <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* تخمین بر اساس آزمایشات روی تیم توسعه داخلی، ساخت برنامه های تولید.</small>

## حامیان

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">سایر حامیان</a>

## نظرات

"_[...] من از **FastAPI** استفاده میکنم. اکثر روز ها [...] من درواقع میخواهم از آن برای همه تیمم **ML services at Microsoft** استفاده کنم. برخی از آنها در محصول اصلی **ویندوز** و برخی محصولات **آفیس** ادغام می شوند._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(منبع)</small></a></div>

---

"_ما از کتابخانه **FastAPI** استفاده کردیم تا یک سرور **REST** ایجاد کنیم که می توان برای به دست آوردن **پیش بینی**ها، کوئری ارسال کرد. [برای Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(منبع)</small></a></div>

---

"**Netflix** خوشحال است که انتشار متن باز چارچوب ارکستراسیون **مدیریت بحران** ما را اعلام کند:! [ساخته شده با **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(منبع)</small></a></div>

---

"_من بر روی ماه هیجان زده هستم. **FastAPI** خیلی جالبه!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(منبع)</small></a></div>

---

"_راستش را بخواهید، چیزی که ساخته اید فوق العاده محکم و با جلا به نظر می رسد. از بسیاری جهات، این همان چیزی است که می‌خواستم در **hug** باشد - دیدن کسی که آن را می‌سازد واقعاً الهام‌بخش است._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(منبع)</small></a></div>

---

"_اگر به دنبال یادگیری یک **فریمورک مدرن** برای ساخت API های REST هستید، **FastAPI** را بررسی کنید [...] استفاده از آن سریع و یادگیری آن آسان است. [...]_"

"_ما برای **API** های خود را به **FastAPI** تغییر داده ایم [...] فکر می کنم شما آن را دوست داشته باشید [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(منبع)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(منبع)</small></a></div>

---

## **Typer** رابط خط فرمان FastAPI

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

اگر شما یک برنامه <abbr title="Command Line Interface">CLI</abbr> میسازید، برنامه مورد استفاده در ترمینال به جای وب API ها، <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a> بررسی کنید.

**Typer** برادر کوچک FastAPI است. و قرار است **FastAPI CLI** باشد. ⌨️ 🚀

## پیش نیاز ها

پایتون ۳.۶+

FastAPI بر روی شانه های غول ها ایستاده است:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> برای بخش های وب است.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> برای بخش های مربوط به داده است.

## نصب

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

شما همچنین به یک سرور ASGI برای تولید مانند <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> یا <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a> نیاز دارید.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## مثال

### آن را ایجاد کنید

* فایل `main.py` را با محتویات زیر ایجاد کنید:

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
<summary>یا از <code>async def</code>... استفاده کنید</summary>

اگر از `async` یا `await` در کدتان استفاده کردید، از `async def` استفاده کنید:

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

**یاداشت**:

اگر نمی‌دانید، بخش _"عجله دارید؟" را در <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank"> برای `async` و `await` در مستندات بررسی کنید</a>.

</details>

### اجرا کنید

سرور را با دستور زیر اجرا کنید:

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
<summary>درباره این دستور <code>uvicorn main:app --reload</code>...</summary>

دستور `uvicorn main:app` به این موارد اشاره دارد:

* `main`: فایل `main.py` (`ماژول` پایتون).
* `app`: شی در `main.py` با خط `app = FastAPI()` می‌شود.
* `--reload`: سرور را پس از تغییر کد راه اندازی مجدد می کند. این کار را فقط برای توسعه انجام دهید.

</details>

### بررسی کنید

این را در مرورگر خودتان باز کنید <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

شما یک پاسخ JSON خواهید دید:

```JSON
{"item_id": 5, "q": "somequery"}
```

شما قبلا یک API ایجاد کرده اید که:

* درخواست های HTTP را در _paths_ `/` و `/items/{item_id}` دریافت می کند.
* هر دو مسیر _GET <em>عملیات</em> را انجام می‌دهند (همچنین به عنوان HTTP _methods_ شناخته می‌شوند).
* مسیر _ `/items/{item_id}` دارای یک پارامتر _path_ `item_id` است که باید `int` باشد.
* مسیر _ `/items/{item_id}` دارای یک پارامتر اختیاری `str` _query_ `q` است.

### اسناد API تعاملی

حالا به اینجا بروید <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

اسناد API تعاملی خودکار را خواهید دید(تهیه شده توسط <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### اسناد API جایگزین

و اکنون، به بروید <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

اسناد خودکار جایگزین را خواهید دید (ساخته شده توسط <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## مثال ارتقا

اکنون فایل `main.py` را تغییر دهید تا بدنه ای از درخواست `PUT` دریافت کند.

به لطف Pydantic، بدنه را با استفاده از تایپ های استاندارد پایتون اعلام کنید.

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

سرور باید به طور خودکار بارگیری مجدد شود (زیرا شما `--reload` را به دستور `uvicorn` در بالا اضافه کردید).

### ارتقاء اسناد API تعاملی

حالا به  <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> بروید.

* اسناد API تعاملی، از جمله بدنه جدید، به طور خودکار به روز می شود:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* روی دکمه "Try it out" کلیک کنید، این به شما امکان می دهد پارامترها را پر کنید و مستقیماً با API تعامل کنید:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* سپس بر روی دکمه "Execute" کلیک کنید، رابط کاربری با API شما ارتباط برقرار می کند، پارامترها را ارسال می کند، نتایج را دریافت می کند و آنها را روی صفحه نمایش می دهد.:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### ارتقاء اسناد API جایگزین

و الان به <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> بروید.

*اسناد جایگزین همچنین پارامتر و بدنه پرس و جو جدید را منعکس می کند:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### خلاصه

به طور خلاصه، شما **یک بار** انواع پارامترها، بدنه و ... را به عنوان پارامترهای تابع اعلام می کنید.

شما این کار را با تایپ استاندارد پایتون مدرن انجام می دهید.

لازم نیست یک نحو جدید، روش ها یا کلاس های یک کتابخانه خاص و غیره را یاد بگیرید.

فقط استاندارد ** Python 3.6+**.

به عنوان مثال، برای `int`:

```Python
item_id: int
```

یا برای یک مدل `item` پیچیده تر:

```Python
item: Item
```

...و با آن اعلان واحد دریافت می کنید:

* پشتیبانی از ویرایشگر، از جمله:
    * تکمیل.
    * نوع چک
* اعتبارسنجی داده ها:
    * خطاهای خودکار و پاک زمانی که داده ها نامعتبر است.
    * اعتبارسنجی حتی برای اشیاء JSON عمیق تو در تو.
* <abbr title="همچنین به عنوان: serialization, parsing, marshalling">تبدیل</abbr> داده‌های ورودی: از شبکه به داده‌ها و انواع Python شناخته می‌شود. خواندن از:
    * JSON.
    * پارامترهای مسیر
    * پارامترهای پرس و جو
    * کوکی ها
    * هدر ها
    * فرم ها
    * فایل ها
* <abbr title="همچنین شناخته شده به عنوان: serialization, parsing, marshalling">تبدیل</abbr> داده های خروجی: تبدیل از داده ها و انواع Python به داده های شبکه (به عنوان JSON):
    * تبدیل تایپ های پایتون (`str`، `int`، `float`، `bool`، `list` و غیره).
    * اشیاء "date"
    * اشیاء "UUID".
    * مدل های پایگاه داده
    * ...و خیلی بیشتر.
* اسناد API تعاملی خودکار، از جمله 2 رابط کاربری جایگزین:
    * UI Swagger.
    * ReDoc.

---

با بازگشت به مثال کد قبلی، **FastAPI**:

* تأیید کنید که یک `id_id` در مسیر درخواست‌های `GET` و `PUT` وجود دارد.
* تأیید کنید که `id_id` برای درخواست‌های `GET` و `PUT` از نوع `int` است.
    * اگر اینطور نباشد، کلاینت یک خطای مفید و واضح را مشاهده خواهد کرد.
* بررسی کنید که آیا یک پارامتر درخواست اختیاری به نام `q` (مانند `http://127.0.0.1:8000/items/foo?q=somequery`) برای درخواست‌های `GET` وجود دارد.
    * از آنجایی که پارامتر "q" با "= هیچ" اعلام می شود، اختیاری است.
    * بدون `None` لازم است (همانطور که بدنه در مورد `PUT` است).
* برای درخواست‌های `PUT` به `/items/{item_id}`، متن را به‌عنوان JSON بخوانید:
    * بررسی کنید که دارای یک ویژگی `name` باشد که باید `str` باشد.
    * بررسی کنید که دارای یک ویژگی `price` باشد که باید `float` باشد.
    * بررسی کنید که دارای یک ویژگی اختیاری `is_offer` باشد، که در صورت وجود باید `bool` باشد.
    * همه اینها برای اشیاء JSON عمیق تو در تو نیز کار می کند.
* تبدیل از و به JSON به صورت خودکار.
* همه چیز را با OpenAPI مستند کنید، که می تواند توسط:
    * سیستم های اسناد تعاملی.
    * سیستم های تولید کد خودکار مشتری، برای بسیاری از زبان ها.
* 2 رابط وب اسناد تعاملی را به طور مستقیم ارائه می دهد.
---

ما فقط سطحی بررسی کردیم، اما شما در حال حاضر این ایده را دریافت کرده اید که چگونه کار می کند.

سعی کنید خط را با عوض کنید:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...این را:

```Python
        ... "item_name": item.name ...
```

...به:

```Python
        ... "item_price": item.price ...
```

و ببینید که چگونه ویرایشگر شما ویژگی ها را به طور خودکار تکمیل می کند و انواع آنها را می شناسد:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

برای مثال کامل تر از جمله ویژگی های بیشتر، به ادامه <a href="https://fastapi.tiangolo.com/tutorial/">آموزش - راهنمای کاربر</a> مراجعه کنید.

**هشدار اسپویل**: آموزش - راهنمای کاربر شامل:

* اعلام **پارامترها** از جاهای مختلف دیگر مانند: **سرصفحه**، **کوکی**، **فیلدهای فرم** و **فایل**.
* نحوه تنظیم **محدودیت های اعتبارسنجی** به عنوان "حداکثر_طول" یا "regex".
* یک سیستم بسیار قدرتمند و آسان برای استفاده **<abbr title="همچنین به عنوان اجزاء، منابع، ارائه دهندگان، خدمات، تزریقات">تزریق وابستگی</abbr>** شناخته می شود.
* امنیت و احراز هویت، از جمله پشتیبانی از **OAuth2** با **توکن های JWT** و **HTTP Basic**.
* تکنیک های پیشرفته تر (اما به همان اندازه آسان) برای اعلان **مدل های JSON عمیق تو در تو** (به لطف Pydantic).
* **GraphQL** ادغام با <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> و کتابخانه های دیگر.
* بسیاری از ویژگی های اضافی (به لطف Starlette) مانند:
    * **وب سوکت**
    * تست های بسیار آسان بر اساس "درخواست ها" و "pytest".
    * **CORS**
    * **جلسات کوکی**
    * ...و بیشتر

## کارایی

بنچمارک های مستقل TechEmpower برنامه های **FastAPI** را نشان می دهد که تحت Uvicorn اجرا می شوند که <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">یکی از سریع ترین چارچوب های پایتون موجود است</a>, فقط زیر خود Starlette و Uvicorn (در داخل توسط FastAPI استفاده می شود). (*)

برای درک بیشتر در مورد آن، بخش را ببینید <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## وابستگی های اختیاری

مورد استفاده Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - برای JSON سریعتر <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - برای اعتبار سنجی ایمیل.

مورد استفاده Starlette:

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - اگر می‌خواهید از `TestClient` استفاده کنید، لازم است.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - اگر می خواهید از پیکربندی قالب پیش فرض استفاده کنید، لازم است.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> -اگر می خواهید از فرم پشتیبانی کنید، لازم است <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>, با `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - برای پشتیبانی از `SessionMiddleware` مورد نیاز است.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - برای پشتیبانی از `SchemaGenerator` Starlette مورد نیاز است (شما احتمالاً با FastAPI به آن نیاز ندارید).
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - اگر می‌خواهید از `UJSONResponse` استفاده کنید، الزامی است.

استفاده شده توسط FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - برای سروری که برنامه شما را بارگیری و ارائه می کند.

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - اگر میخواهید از `ORJSONResponse` استفاده کنید الزامی است.

شما می توانید همه اینها را با `pip install "fastapi[all]"` نصب کنید.

## مجوز

این پروژه تحت شرایط مجوز MIT مجوز دارد.
