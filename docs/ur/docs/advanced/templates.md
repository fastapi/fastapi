# Templates { #templates }

آپ **FastAPI** کے ساتھ کوئی بھی template engine استعمال کر سکتے ہیں۔

ایک عام انتخاب Jinja2 ہے، وہی جو Flask اور دیگر ٹولز میں استعمال ہوتا ہے۔

اسے آسانی سے ترتیب دینے کے لیے utilities موجود ہیں جو آپ اپنی **FastAPI** ایپلیکیشن میں براہ راست استعمال کر سکتے ہیں (Starlette کی فراہم کردہ)۔

## Dependencies انسٹال کریں { #install-dependencies }

یقینی بنائیں کہ آپ [virtual environment](../virtual-environments.md) بنائیں، اسے فعال کریں، اور `jinja2` انسٹال کریں:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## `Jinja2Templates` استعمال کرنا { #using-jinja2templates }

* `Jinja2Templates` import کریں۔
* ایک `templates` آبجیکٹ بنائیں جو آپ بعد میں دوبارہ استعمال کر سکیں۔
* *path operation* میں `Request` parameter بیان کریں جو template واپس کرے گا۔
* اپنے بنائے ہوئے `templates` کو render کرنے اور `TemplateResponse` واپس کرنے کے لیے استعمال کریں، template کا نام، request آبجیکٹ، اور Jinja2 template کے اندر استعمال ہونے والے key-value جوڑوں کے ساتھ ایک "context" dictionary پاس کریں۔

{* ../../docs_src/templates/tutorial001_py310.py hl[4,11,15:18] *}

/// note | نوٹ

FastAPI 0.108.0 اور Starlette 0.29.0 سے پہلے، `name` پہلا parameter تھا۔

نیز، اس سے پہلے، پچھلے ورژنز میں، `request` آبجیکٹ Jinja2 کے لیے context میں key-value جوڑوں کے حصے کے طور پر پاس کیا جاتا تھا۔

///

/// tip | مشورہ

`response_class=HTMLResponse` بیان کرنے سے docs UI جان سکے گا کہ response HTML ہوگا۔

///

/// note | تکنیکی تفصیلات

آپ `from starlette.templating import Jinja2Templates` بھی استعمال کر سکتے ہیں۔

**FastAPI** آپ کی سہولت کے لیے `starlette.templating` کو `fastapi.templating` کے طور پر فراہم کرتا ہے۔ لیکن زیادہ تر دستیاب responses براہ راست Starlette سے آتے ہیں۔ `Request` اور `StaticFiles` کے ساتھ بھی ایسا ہی ہے۔

///

## Templates لکھنا { #writing-templates }

پھر آپ `templates/item.html` پر ایک template لکھ سکتے ہیں، مثال کے طور پر:

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### Template Context Values { #template-context-values }

HTML میں جو یہ رکھتا ہے:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...یہ آپ کی پاس کردہ "context" `dict` سے لیا گیا `id` دکھائے گا:

```Python
{"id": id}
```

مثال کے طور پر، ID `42` کے ساتھ، یہ اس طرح render ہوگا:

```html
Item ID: 42
```

### Template `url_for` Arguments { #template-url-for-arguments }

آپ template کے اندر `url_for()` بھی استعمال کر سکتے ہیں، یہ وہی arguments لیتا ہے جو آپ کے *path operation function* میں استعمال ہوتے۔

تو، یہ حصہ:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...اسی URL کا لنک بنائے گا جو *path operation function* `read_item(id=id)` کے ذریعے ہینڈل ہوگا۔

مثال کے طور پر، ID `42` کے ساتھ، یہ اس طرح render ہوگا:

```html
<a href="/items/42">
```

## Templates اور static فائلیں { #templates-and-static-files }

آپ template کے اندر `url_for()` بھی استعمال کر سکتے ہیں، اور اسے مثال کے طور پر، `name="static"` کے ساتھ mount کی گئی `StaticFiles` کے ساتھ استعمال کر سکتے ہیں۔

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

اس مثال میں، یہ `static/styles.css` پر CSS فائل سے لنک کرے گا:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

اور چونکہ آپ `StaticFiles` استعمال کر رہے ہیں، وہ CSS فائل آپ کی **FastAPI** ایپلیکیشن کے ذریعے `/static/styles.css` URL پر خود بخود serve ہوگی۔

## مزید تفصیلات { #more-details }

مزید تفصیلات کے لیے، بشمول templates کی جانچ کا طریقہ، [Starlette کی templates دستاویزات](https://www.starlette.dev/templates/) دیکھیں۔
