# استفاده از Dataclass ها

FastAPI براساس و روی امکانات **Pydantic** ساخته شده, و تا به اینجا من به شما نشان می دادم که چگونه  request ها و response های خود را بر اساس مدل های Pydantic بسازید.

اما فست از گزینه  <a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a> به شکل مشابه پشتیبانی می کنه:

{* ../../docs_src/dataclasses/tutorial001.py hl[1,7:12,19:20] *}

این امکان هنوز با تکیه بر  **Pydantic** پشتیبانی میشه, با استفاده از امکان پیش فرض  <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">  `ها dataclass`</a>.

بنابراین حتی با وجود اینکه کد بالا به صورت مستقیم از Pydantic استفاده نمی کنه , FastAPI از Pydantic استفاده می کنه تا Dataclass های استاندارد رو به Dataclass های سبک Pydantic تبدیل کنه.

و البته از امکانات مشابه پشتیبانی می کنه:

* اعتبار سنجی داده
* serialize کردن داده
* مستند کردن داده، و غیره...

این مشابه مدل های Pydantic کار می کنه. و با استفاده از Pydantic و در لایه های پایین به روش مشابه این کارو انجام میده.

/// info 

به خاطر بسپار که Dataclass تمام قابلیت ها Pydantic رو نداره.

بنابراین شما ممکنه هنوز نیاز به استفاده از کلاس های Pydantic داشته باشین.

اما اگه از قبل چندتایی Dataclass دارین, ترفند خوبیه که برای وب API ازش استفاده کنین با تکیه بر FastAPI. 🤓

///

## استفاده از Dataclass ها در `response_model`

شما می توانید از  `ها dataclass` در پارامتر ورودی `response_model` هم استفاده کنید:

{* ../../docs_src/dataclasses/tutorial002.py hl[1,7:13,19] *}

The dataclass will be automatically converted to a Pydantic dataclass.

This way, its schema will show up in the API docs user interface:

<img src="/img/tutorial/dataclasses/image01.png">

## Dataclasses in Nested Data Structures

You can also combine `dataclasses` with other type annotations to make nested data structures.

In some cases, you might still have to use Pydantic's version of `dataclasses`. For example, if you have errors with the automatically generated API documentation.

In that case, you can simply swap the standard `dataclasses` with `pydantic.dataclasses`, which is a drop-in replacement:

{* ../../docs_src/dataclasses/tutorial003.py hl[1,5,8:11,14:17,23:25,28] *}

1. We still import `field` from standard `dataclasses`.

2. `pydantic.dataclasses` is a drop-in replacement for `dataclasses`.

3. The `Author` dataclass includes a list of `Item` dataclasses.

4. The `Author` dataclass is used as the `response_model` parameter.

5. You can use other standard type annotations with dataclasses as the request body.

    In this case, it's a list of `Item` dataclasses.

6. Here we are returning a dictionary that contains `items` which is a list of dataclasses.

    FastAPI is still capable of <abbr title="converting the data to a format that can be transmitted">serializing</abbr> the data to JSON.

7. Here the `response_model` is using a type annotation of a list of `Author` dataclasses.

    Again, you can combine `dataclasses` with standard type annotations.

8. Notice that this *path operation function* uses regular `def` instead of `async def`.

    As always, in FastAPI you can combine `def` and `async def` as needed.

    If you need a refresher about when to use which, check out the section _"In a hurry?"_ in the docs about [`async` and `await`](../async.md#in-a-hurry){.internal-link target=_blank}.

9. This *path operation function* is not returning dataclasses (although it could), but a list of dictionaries with internal data.

    FastAPI will use the `response_model` parameter (that includes dataclasses) to convert the response.

You can combine `dataclasses` with other type annotations in many different combinations to form complex data structures.

Check the in-code annotation tips above to see more specific details.

## Learn More

You can also combine `dataclasses` with other Pydantic models, inherit from them, include them in your own models, etc.

To learn more, check the <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/" class="external-link" target="_blank">Pydantic docs about dataclasses</a>.

## Version

This is available since FastAPI version `0.67.0`. 🔖
