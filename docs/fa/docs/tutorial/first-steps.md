# گام های اولیه

ساده ترین پروژه FastAPI می تواند به شکل زیر باشد:

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

لطفاً کد زیر را در یک فایل با نام main.py قرار دهید.

برای اجرا به صورت live server ، کد را اجرا کنید.

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

!!! نکته
    دستور 'uvicorn main:app' به این موارد اشاره دارد:

    * فایل "main": فایل "main.py" ("ماژول" پایتون).
    * برنامه "app": شی ایجاد شده در "main.py" با خط "app = FastAPI()".
    * دستور "--reload": سرور را پس از تغییر کد راه اندازی مجدد کنید. فقط برای توسعه استفاده کنید.


در خروجی، یک خط با چیزی مانند زیر خواهید دید:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

این خط نشان می‌دهد که برنامه شما در local machine شما در چه آدرسی قرار گرفته است و از چه URLی برای دسترسی به برنامه استفاده می کنید.

### بررسی کنید

مرورگر خود را در آدرس <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a> باز کنید.

شما پاسخ JSON را به شکل زیر مشاهده خواهید کرد:

```JSON
{"message": "Hello World"}
```

### اسناد API تعاملی (Interactive API docs)

اکنون به <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> بروید.

اسناد API تعاملی خودکار را خواهید دید (ارائه شده توسط <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a >):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### اسناد API جایگزین (Alternative API docs)

و اکنون به <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> بروید .

اسناد خودکار جایگزین را خواهید دید (ارائه شده توسط <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):
![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)


### اسناد OpenAPI

فریم ورک **FastAPI** با استفاده از استاندارد **OpenAPI** برای تعریف APIها، یک "schema" با تمام API شما ایجاد می کند.

#### (طرحواره) "schema"

اصطلاح "schema" تعریف یا توصیف چیزی است. نه کدی که آن را پیاده سازی می کند، بلکه فقط یک توضیح انتزاعی است.

#### اسناد "schema" API

در این مورد، <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> مشخصاتی است که نحوه تعریف یک شمای API شما

این تعریف schema شامل مسیرهای API شما، پارامترهای احتمالی آنها و غیره است.


#### اصطلاح  "schema" داده

اصطلاح "schema" ممکن است به شکل برخی از داده‌ها مانند محتوای JSON نیز اشاره داشته باشد.

در آن صورت، این به معنای ویژگی‌های JSON، و انواع داده‌های آنها و غیره است.

#### اسناد OpenAPI و JSON Schema

اسناد OpenAPI یک schema API برای API شما تعریف می کند. و این schema شامل تعاریف (یا "schema ها") داده های ارسال و دریافت شده توسط API شما با استفاده از **JSON Schema**، استاندارد schema های داده JSON است.


#### فایل «openapi.json» را بررسی کنید

اگر کنجکاو هستید که schema OpenAPI خام چگونه به نظر می رسد، FastAPI به طور خودکار یک JSON (شما) با توضیحات همه API شما تولید می کند.

می‌توانید مستقیماً آن را در: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi ببینید .json</a>.

یک JSON را نشان می دهد که با چیزی شبیه به:

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

#### اسناد OpenAPI برای چیست

اسناد schema OpenAPI همان چیزی است که دو سیستم اسناد تعاملی را شامل می شود.

و ده ها گزینه جایگزین وجود دارد که همه بر اساس OpenAPI هستند. شما به راحتی می توانید هر یک از آن جایگزین ها را به برنامه خود که با **FastAPI** ساخته شده است اضافه کنید.

همچنین می توانید از آن برای تولید کد به صورت خودکار برای کلاینت هایی که با API شما ارتباط برقرار می کنند استفاده کنید. به عنوان مثال، برنامه های frontend، تلفن همراه یا IoT.

### مرحله ۱: import `FastAPI`

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

فریم ورک "FastAPI" یک کلاس پایتون است که تمام عملکردها را برای API شما فراهم می کند.


!!! توجه "جزئیات فنی"
  فریم ورک "FastAPI" کلاسی است که مستقیماً از «Starlette» به ارث می‌برد.
       می‌توانید با "FastAPI" نیز از همه قابلیت‌های <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> استفاده کنید.

### مرحله۲ : یک 'instance' از "FastAPI" ایجاد کنید
```"Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```


در اینجا، متغیر 'app' یک "نمونه" (instance) از کلاس 'FastAPI' خواهد بود.

این نمونه اصلی تعامل شما برای ایجاد تمام (API) خواهد بود.

این "app" همان متغیری است که توسط 'uvicorn' در دستور زیر مورد اشاره قرار می‌گیرد:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>


اگر برنامه خود را مانند زیر ایجاد کنید:

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

و آن را در یک فایل به نام 'main.py' قرار دهید، سپس می‌توانید 'uvicorn' را به صورت زیر فراخوانی کنید:


<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### مرحله ۳: ایجاد یک *path operation* (عملیات مسیر)

#### مسیر-path

مسیر یا همان "path" در اینجا به آخرین قسمت URL که از '/' اول شروع می‌شود، اشاره دارد.

بنابراین، در یک URL مانند:


```
https://example.com/items/foo
```

... مسیر این گونه خواهد بود:


```
/items/foo
```

!!! اطلاعات
     یک "path" معمولاً "endpoint" یا "route" نیز نامیده می شود.

هنگام ساختن یک API، «مسیر» راه اصلی برای جداسازی «resources» و «concerns» است.

#### عملیات-Operation

عملیات-"Operation" در اینجا به یکی از «روش‌های HTTP» اشاره دارد.

یکی از:
* `POST`
* `GET`
* `PUT`
* `DELETE`

...و موارد خاص تر:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

در پروتکل HTTP، شما می‌توانید با استفاده از یک یا چند "روش" (method) از این مسیرها برای برقراری ارتباط استفاده کنید.

---

هنگام ساختن API، معمولاً از این روش های خاص HTTP برای انجام یک عمل خاص استفاده می کنید.

به طور معمول شما استفاده می کنید:

متد* `POST`: برای ثبت اطلاعات
متد* `GET`: برای خواندن اطلاعات
متد* `PUT`: برای بروزرسانی اطلاعات
متد* `DELETE`: برای پاک کردن اطلاعات

بنابراین، در OpenAPI، به هر یک از متدهای HTTP "operation" گفته می شود.

ما قصد داریم آنها را "**operation ها**" نیز بنامیم.

#### یک *path operation decorator* را تعریف کنید

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

در این کد'@app.get("/")' به **FastAPI** می‌گوید که تابعی که در زیر آن قرار دارد، مسئول پاسخگویی به درخواست‌هایی است که به این آدرس ارسال می‌شوند:

* (مسیر) path  `/`
* با استفاده از یک operation <abbr title="an HTTP GET"><code>دریافت</code></abbr>

!!! اطلاعات "اطلاعات `@decorator`"
     به آن نحو «@something» در پایتون «دکوراتور» می‌گویند.

     شما آن را در بالای یک تابع قرار می دهید. مانند یک کلاه تزئینی زیبا (حدس می‌زنم این اصطلاح از اینجا آمده است).

     یک "decorator" تابع زیر را می گیرد و کاری با آن انجام می دهد.

     در مورد ما، این دکوراتور به **FastAPI** می گوید که تابع زیر با **path** `/` با **operation** 'get' مطابقت دارد.

     این "**path operation decorator**" است.

همچنین می توانید از operation های دیگر استفاده کنید:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

و موارد خاص تر:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

!!! نکته

شما آزاد هستید که از هر operation (method HTTP) به دلخواه خود استفاده کنید.

     فریم ورک **FastAPI** هیچ معنای خاصی را اعمال نمی کند.

     اطلاعات در اینجا به عنوان یک دستورالعمل ارائه شده است، نه یک الزام.

     به عنوان مثال، هنگام استفاده از GraphQL، معمولاً تمام اقدامات را فقط با استفاده از operation «POST» انجام می دهید.

### مرحله ۴: تعریف **path operation function**

این "**path operation function**" ما است:

* **مسیر**: «/» است.
متد* **operation**: "POST" است.
* **تابع**: تابع زیر "decorator" است (زیر `@app.get("/")`).

```"Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

این یک تابع پایتون است.

هر زمان که درخواستی به URL "`/`" با استفاده از operation "GET" دریافت کند، توسط **FastAPI** فراخوانی می شود.

در این مورد، یک تابع `async` است.

---

همچنین می‌توانید آن را به‌جای «async def» به‌عنوان یک تابع عادی تعریف کنید:

```"Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! توجه داشته باشید
     اگر تفاوت را نمی دانید، [Async: *"عجله دارید؟"*](../async.md#in-a-hurry){.internal-link target=_blank} را بررسی کنید.

### مرحله ۵: محتوا را برگردانید

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```


می‌توانید مقادیر مانند "list" و "dict" و همچنین مقادیر تکی مثل "str" و "int" را برگردانید.

همچنین می توانید مدل های Pydantic را برگردانید (در ادامه بیشتر در مورد آن خواهید دید).

بسیاری از اشیاء و مدل های دیگر وجود دارند که به طور خودکار به JSON تبدیل می شوند (از جمله ORM ها و غیره). سعی کنید از موارد مورد علاقه خود استفاده کنید، به احتمال زیاد آنها قبلاً از پشتیبانی می شوند.

##خلاصه

فریم ورک* "FastAPI" را وارد کنید.
* یک نمونه "app" ایجاد کنید.
* یک **path operation decorator** بنویسید (مانند `@app.get("/")`).
* یک **path operation function** بنویسید (مانند 'def root(: ...' در زیر آن).
* سرور توسعه را اجرا کنید (مانند 'uvicorn main:app --reload').
