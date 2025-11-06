# ویژگی ها

## ویژگی های FastAPI

**FastAPI** موارد زیر را به شما ارائه میدهد:

### برپایه استاندارد های باز

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> برای ساخت API, شامل مشخص سازی <abbr title="که علاوه بر path, به عنوان endpoint و route نیز شناخته میشود">path</abbr> <abbr title="که به عنوان متودهای HTTP یعنی POST,GET,PUT,DELETE و ... شناخته میشوند">operation</abbr> ها, <abbr title="parameters">پارامترها</abbr>, body request ها, امنیت و غیره.
* مستندسازی خودکار data model با <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (همانطور که OpenAPI خود نیز مبتنی بر JSON Schema است).
* طراحی شده بر اساس استاندارد هایی که پس از یک مطالعه دقیق بدست آمده اند بجای طرحی ناپخته و بدون فکر.
* همچنین به شما اجازه میدهد تا از تولید خودکار client code در بسیاری از زبان ها استفاده کنید.

### مستندات خودکار

مستندات API تعاملی و ایجاد رابط کاربری وب. از آنجایی که این فریم ورک برپایه OpenAPI میباشد، آپشن های متعددی وجود دارد که ۲ مورد بصورت پیش فرض گنجانده شده اند.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>، با <abbr title="interactive exploration">کاوش تعاملی</abbr>، API خود را مستقیما از طریق مرورگر صدازده و تست کنید.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* مستندات API جایگزین با <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### فقط پایتون مدرن

همه اینها برپایه type declaration های **پایتون ۳.۶** استاندارد (به لطف Pydantic) میباشند. سینتکس جدیدی درکار نیست. تنها پایتون مدرن استاندارد.

اگر به یک یادآوری ۲ دقیقه ای در مورد نحوه استفاده از تایپ های پایتون دارید (حتی اگر از FastAPI استفاده نمیکنید) این آموزش کوتاه را بررسی کنید: [Python Types](python-types.md){.internal-link target=\_blank}.

شما پایتون استاندارد را با استفاده از تایپ ها مینویسید:

```Python
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

که سپس میتوان به این شکل از آن استفاده کرد:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

/// info

`**second_user_data` یعنی:

کلید ها و مقادیر دیکشنری `second_user_data` را مستقیما به عنوان ارگومان های key-value بفرست، که معادل است با : `User(id=4, name="Mary", joined="2018-11-30")`

///

### پشتیبانی ویرایشگر

تمام فریم ورک به گونه ای طراحی شده که استفاده از آن آسان و شهودی باشد، تمام تصمیمات حتی قبل از شروع توسعه بر روی چندین ویرایشگر آزمایش شده اند، تا از بهترین تجربه توسعه اطمینان حاصل شود.

در آخرین نظرسنجی توسعه دهندگان پایتون کاملا مشخص بود که <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">بیشترین ویژگی مورد استفاده از "<abbr title="autocompletion">تکمیل خودکار</abbr>" است</a>.

تمام فریم ورک **FastAPI** برپایه ای برای براورده کردن این نیاز نیز ایجاد گشته است. تکمیل خودکار در همه جا کار میکند.

شما به ندرت نیاز به بازگشت به مستندات را خواهید داشت.

ببینید که چگونه ویرایشگر شما ممکن است به شما کمک کند:

* در <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* در <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

شما پیشنهاد های تکمیل خودکاری را خواهید گرفت که حتی ممکن است قبلا آن را غیرممکن تصور میکردید. به عنوان مثال کلید `price` در داخل بدنه JSON (که میتوانست تودرتو نیز باشد) که از یک درخواست آمده است.

دیگر خبری از تایپ کلید اشتباهی، برگشتن به مستندات یا پایین بالا رفتن برای فهمیدن اینکه شما از `username` یا `user_name` استفاده کرده اید نیست.

### مختصر

FastAPI **پیش فرض** های معقولی برای همه چیز دارد، با قابلیت تنظیمات اختیاری در همه جا. تمام پارامترها را میتوانید برای انجام انچه نیاز دارید و برای تعریف API مورد نیاز خود به خوبی تنظیم کنید.

اما به طور پیش فرض، همه چیز **کار میکند**.

### اعتبارسنجی

* اعتبارسنجی برای بیشتر (یا همه؟) **data type** های پایتون، شامل:

    * JSON objects (`dict`)
    * آرایه های (‍‍‍‍`list`) JSON با قابلیت مشخص سازی تایپ ایتم های درون لیست.
    * فیلد های رشته (`str`)، به همراه مشخص سازی حداقل و حداکثر طول رشته.
    * اعداد (‍‍`int`,`float`) با حداقل و حداکثر مقدار و غیره.

* اعتبارسنجی برای تایپ های عجیب تر، مثل:
    * URL.
    * Email.
    * UUID.
    * و غیره.

تمام اعتبارسنجی ها توسط کتابخانه اثبات شده و قدرتمند **Pydantic** انجام میشود.

### <abbr title="Security and authentication">امنیت و احراز هویت</abbr>

امنیت و احرازهویت بدون هیچگونه ارتباط و مصالحه ای با پایگاه های داده یا مدل های داده ایجاد شده اند.

تمام طرح های امنیتی در OpenAPI تعریف شده اند، از جمله:

* .
* **OAuth2** (همچنین با **JWT tokens**). آموزش را در [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=\_blank} مشاهده کنید.
* کلید های API:
    * <abbr title="سرصفحه ها">Headers</abbr>
    * <abbr title="پارامترهای پرسمان">Query parameters</abbr>
    * <abbr title="کوکی ها">Cookies</abbr>، و غیره.

به علاوه تمام ویژگی های امنیتی از **Statlette** (شامل **<abbr title="کوکی های جلسه">session cookies</abbr>**)

همه اینها به عنوان ابزارها و اجزای قابل استفاده ای ساخته شده اند که به راحتی با سیستم های شما، مخازن داده، پایگاه های داده رابطه ای و NoSQL و غیره ادغام میشوند.

### <abbr title="تزریق وابستگی">Dependency Injection</abbr>

FastAPI شامل یک سیستم <abbr title='همچنین به عنوان "components", "resources", "services" و "providers" شناخته میشود'><strong>Dependency Injection</strong></abbr> بسیار آسان اما بسیار قدرتمند است.

* حتی وابستگی ها نیز میتوانند وابستگی هایی داشته باشند و یک سلسله مراتب یا **"گرافی" از وابستگی ها** ایجاد کنند.

* همه چیز توسط فریم ورک **به طور خودکار اداره میشود**

* همه وابستگی ها میتوانند به داده های request ها نیاز داشته باشند و مستندات خودکار و محدودیت های <abbr title="عملیات مسیر">path operation</abbr> را **افزایش** دهند.

* با قابلیت **اعتبارسنجی خودکار** حتی برای path operation parameter های تعریف شده در وابستگی ها.

* پشتیبانی از سیستم های پیچیده احرازهویت کاربر، **اتصالات پایگاه داده** و غیره.

* بدون هیچ ارتباطی با دیتابیس ها، فرانت اند و غیره. اما ادغام آسان و راحت با همه آنها.

### پلاگین های نامحدود

یا به عبارت دیگر، هیچ نیازی به آنها نیست، کد موردنیاز خود را وارد و استفاده کنید.

هر یکپارچه سازی به گونه ای طراحی شده است که استفاده از آن بسیار ساده باشد (با وابستگی ها) که میتوانید با استفاده از همان ساختار و روشی که برای _path operation_ های خود استفاده کرده اید تنها در ۲ خط کد "پلاگین" برنامه خودتان را ایجاد کنید.

### تست شده

* 100% <abbr title="مقدار کدی که به طور خودکار تست شده است">پوشش تست</abbr>.

* 100% کد بر اساس <abbr title="حاشیه نویسی تایپ های پایتون (Python type annotations)، با استفاده از آن ویرایشگر و ابزارهای خارجی شما می توانند پشتیبانی بهتری از شما ارائه دهند">type annotate ها</abbr>.

* استفاده شده در اپلیکیشن های تولید

## ویژگی های Starlette

**FastAPI** کاملا (و براساس) با <a href="https://www.starlette.dev/" class="external-link" target="_blank"><strong>Starlette</strong></a> سازگار است. بنابراین، هرکد اضافی Starlette که دارید، نیز کار خواهد کرد.

‍‍`FastAPI` در واقع یک زیرکلاس از `Starlette` است. بنابراین اگر از قبل Starlette را میشناسید یا با آن کار کرده اید، بیشتر قابلیت ها به همین روش کار خواهد کرد.

با **FastAPI** شما تمام ویژگی های **Starlette** را خواهید داشت (زیرا FastAPI یک نسخه و نمونه به تمام معنا از Starlette است):

* عملکرد به طورجدی چشمگیر. <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">این یکی از سریعترین فریم ورک های موجود در پایتون است که همتراز با **نود جی اس** و **گو**</a> است.
* پشتیبانی از **WebSocket**.
* <abbr title="In-process background tasks">تسک های درجریان در پس زمینه</abbr>.
* <abbr title="Startup and shutdown events">رویداد های راه اندازی و متوفق شدن<abbr>.
* تست کلاینت ساخته شده به روی HTTPX.
* **CORS**, GZip, فایل های استاتیک, <abbr title="Streaming responses">پاسخ های جریانی</abbr>.
* پشتیبانی از **نشست ها و کوکی ها**.
* 100% پوشش با تست.
* 100% کد براساس type annotate ها.

## ویژگی های Pydantic

**FastAPI** کاملا (و براساس) با <a href="https://docs.pydantic.dev/" class="external-link" target="_blank"><strong>Pydantic</strong></a> سازگار است. بنابراین هرکد Pydantic اضافی که داشته باشید، نیز کار خواهد کرد.

از جمله کتابخانه های خارجی نیز مبتنی بر Pydantic میتوان به <abbr title="Object-Relational Mapper">ORM</abbr> و <abbr title="Object-Document Mapper">ODM</abbr> ها برای دیتابیس ها اشاره کرد.

این همچنین به این معناست که در خیلی از موارد میتوانید همان ابجکتی که از request میگیرید را **مستقیما به دیتابیس** بفرستید زیرا همه چیز به طور خودکار تأیید میشود.

همین امر برعکس نیز صدق می‌کند، در بسیاری از موارد شما می‌توانید ابجکتی را که از پایگاه داده دریافت می‌کنید را **مستقیماً به کاربر** ارسال کنید.

با FastAPI شما تمام ویژگی های Pydantic را دراختیار دارید (زیرا FastAPI برای تمام بخش مدیریت دیتا بر اساس Pydantic عمل میکند):

* **خبری از گیج شدن نیست**:
    * هیچ <abbr title="micro-language">زبان خردی</abbr> برای یادگیری تعریف طرحواره های جدید وجود ندارد.
    * اگر تایپ های پایتون را میشناسید، نحوه استفاده از Pydantic را نیز میدانید.
* به خوبی با **<abbr title="همان Integrated Development Environment, شبیه به ویرایشگر کد">IDE</abbr>/<abbr title="برنامه ای که خطاهای کد را بررسی می کند">linter</abbr>/مغز** شما عمل میکند:
    * به این دلیل که ساختار داده Pydantic فقط نمونه هایی از کلاس هایی هستند که شما تعریف میکنید، تکمیل خودکار، mypy، linting و مشاهده شما باید به درستی با داده های معتبر شما کار کنند.
* اعتبار سنجی **ساختارهای پیچیده**:
    * استفاده از مدل های سلسله مراتبی Pydantic, `List` و `Dict` کتابخانه `typing` پایتون و غیره.
    * و اعتبارسنج ها اجازه میدهند که طرحواره های داده پیچیده به طور واضح و آسان تعریف، بررسی و بر پایه JSON مستند شوند.
    * شما میتوانید ابجکت های عمیقا تودرتو JSON را که همگی تایید شده و annotated شده اند را داشته باشید.
* **قابل توسعه**:
    * Pydantic اجازه میدهد تا data type های سفارشی تعریف شوند یا میتوانید اعتبارسنجی را با روش هایی به روی مدل ها با <abbr title="دکوریتور های اعتبارسنج">validator decorator</abbr> گسترش دهید.
* 100% پوشش با تست.
