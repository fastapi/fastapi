# استفاده از Dataclass ها

FastAPI براساس و روی امکانات **Pydantic** ساخته شده, و تا الان به شما نشون دادم که چطور  request ها و response های خود را بر اساس مدل های Pydantic بسازید.

اما FastAPI از گزینه  <a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a> به شکل مشابه پشتیبانی می کنه:

{* ../../docs_src/dataclasses/tutorial001.py hl[1,7:12,19:20] *}

این امکان هنوز با تکیه بر  **Pydantic** پشتیبانی میشه، با استفاده از امکان پیش فرض  <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">  `dataclasses`</a>.

بنابراین حتی با وجود اینکه کد بالا به صورت مستقیم از Pydantic استفاده نمی کنه، FastAPI از Pydantic استفاده می کنه تا Dataclass های استاندارد رو به Dataclass های سبک Pydantic تبدیل کنه.

و البته از امکانات مشابه هم پشتیبانی می کنه:

* اعتبار سنجی داده
* serialize کردن داده
* مستند کردن داده، و غیره...

این مشابه مدل های Pydantic کار می کنه. و با استفاده از Pydantic در لایه های پایین به روش مشابه این کارو انجام میده.

/// info

**نکته:**

به خاطر بسپار که Dataclass تمام قابلیت ها Pydantic رو نداره.

بنابراین شما ممکنه هنوز نیاز به استفاده از کلاس های Pydantic داشته باشین.

اما اگه از قبل چندتایی Dataclass دارین, ترفند خوبیه که برای وب API ازش استفاده کنین با تکیه بر FastAPI. 🤓

///

## استفاده از Dataclass ها در `response_model`

شما می توانید از  `ها dataclass` در پارامتر ورودی `response_model` هم استفاده کنید:

{* ../../docs_src/dataclasses/tutorial002.py hl[1,7:13,19] *}

با استفاده از روش بالا dataclass به صورت اتوماتیک تبدیل که dataclass عه Pydantic میشه.

با این روش طرح و ساختار خروجی توی رابط کاربری مستندات API نشون داده میشه:

<img src="/img/tutorial/dataclasses/image01.png">

## Dataclass ها در ساختار های داده تو در تو

همچنین برای ساختن ساختار های داده تو در تو شما می تونید `dataclass` ها رو با روش های دیگر نشانه گذاری داده ترکیب کنید.

در برخی موارد ممکنه شما هنوز نیاز به استفاده از  `dataclass` های نسخه Pydantic داشته باشید. برای نمونه، اگر خطایی با مستندات API که به طور اتوماتیک تولید میشه وجود داشته باشه.

در این مورد شما می تونید به راحتی `dataclasses` را با `pydantic.dataclasses`, جایگزین کنید، که در کل یک جایگزینی مستقیم است:

{* ../../docs_src/dataclasses/tutorial003.py hl[1,5,8:11,14:17,23:25,28] *}

1. ما هنوز `field` را از ماژول استاندارد `dataclasses` ایمپورت می کنیم.

2. `pydantic.dataclasses` یک جایگزینی بی دردسر برای `dataclasses` است.

3. dataclass عه `Author`  شامل لیستی از dataclass های `Item` است.

4. dataclass عه `Author` به عنوان پارامتر ورودی `response_model` استفاده شده.

5. شما می تونید از روش های دیگر نشانه گذاری داده همراه dataclass ها برای محتوای request استفاده کنید.

    در این مورد، لیست dataclass های `Item` است.

6. اینجا ما دیکشنری پایتون که شامل `items` هست رو باز می گردانیم که لیستی از dataclass  هاست.

    FastAPI هنوز قابلیت <abbr title="converting the data to a format that can be transmitted">serializing</abbr> داده به JSON را دارد.

7. اینجا `response_model` از نشانه گذاری list برای dataclass های `Author` استفاده می کنه.

    یاد آوری دوباره، شما می تونید `dataclasses` با نشانه گذاری استاندارد ترکیب کنید.

8. دقت کن *`get_authors()` <- path operation function* از کلمه کلیدی `def` به جای `async def` استفاده می کنه.

    طبق معمول, تو FastAPI شما می تونید دو حالت  `def` و `async def` در کنار هم براساس نیاز استفاده کنید.

    اگه نیاز به یادآوری داری که کدوم رو استفاده کنم, تو بخش  _"عجله دارم؟"_ در مستندات [`async` و `await`](../async.md#in-a-hurry){.internal-link target=_blank} رو چک کن.

9. این *path operation function* به عنوان خروجی dataclass ها رو بر نمی گردونه (با اینکه می تونه), اما به جاش لیستی از دیکشنری های پایتون با مقادیر dataclass رو بر می گردونه.

    FastAPI از پارامتر `response_model` برای تبدیل response استفاده خواهد کرد (شامل dataclass ها هم میشه).

شما می تونید `dataclasses` با انواع دیگه نشانه گذاری تو شکل ها و ساختار های مختلف ترکیب کنید تا ساختارهای داده پیچیده بسازید.

برای جزئیات بیشتر می تونید راهنماهای نشانه گذاری که داخل کد های بالایی هست رو بررسی کنین.

## یادگیری بیشتر

شما همچنین می تونید `dataclasses` رو با مدل های دیگر Pydantic ترکیب کنید، از اون ها ارث بری کنید، اونارو اضافه کنین به مدل های خودتون، و غیره

برای یاگیری بیشتر مراجعه کنید به  <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/" class="external-link" target="_blank">ها dataclass بخش Pydantic مستندات</a>.

## نسخه

این امکان از نسخه `0.67.0` FastAPI در دسترس و قابل استفاده است. 🔖

## لغت نامه

بعضی اصطلاحات معنی مستقیم ندارن، بیشتر یه مفهوم هستن تا یه ترجمه کلمه‌به‌کلمه. اینجا دقیق تر مفهوم رو تو محتوای برنامه نویسی و پایتون توضیح می دم.

type annotation: مفهومی است که برای اعتبار سنجی، تبدیل نوع داده و ازش تو تولید مستندات API و چند امکان دیگه استفاده میشه، این مفهوم ‍`نشانه گذاری` ترجمه شده.

path operation fucntion: یه فانکشن پایتون هست که وقتی به آدرس مثل ‍‍`/hello` تو مروگر درخواست داده میشه اون فانکشن اجرا میشه، برای مثال:

    @app.get('/hello')  -> path operation decorator
    def hello():        -> path operation function
       ...
