# Templates { #templates }

आप **FastAPI** के साथ अपनी पसंद का कोई भी template engine उपयोग कर सकते हैं।

एक आम विकल्प Jinja2 है, वही जिसे Flask और अन्य tools उपयोग करते हैं।

इसे आसानी से configure करने के लिए utilities उपलब्ध हैं जिन्हें आप सीधे अपने **FastAPI** application में उपयोग कर सकते हैं (Starlette द्वारा प्रदान की गई)।

## Dependencies install करें { #install-dependencies }

सुनिश्चित करें कि आप एक [virtual environment](../virtual-environments.md) बनाएँ, उसे activate करें, और `jinja2` install करें:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## `Jinja2Templates` का उपयोग करना { #using-jinja2templates }

* `Jinja2Templates` import करें।
* एक `templates` object बनाएँ जिसे आप बाद में फिर से उपयोग कर सकें।
* उस *path operation* में एक `Request` parameter declare करें जो एक template return करेगा।
* आपने जो `templates` बनाया है, उसका उपयोग करके एक `TemplateResponse` render और return करें; template का नाम, request object, और key-value pairs वाली एक "context" dictionary pass करें, जिनका उपयोग Jinja2 template के अंदर किया जाएगा।

{* ../../docs_src/templates/tutorial001_py310.py hl[4,11,15:18] *}

/// note | नोट

FastAPI 0.108.0, Starlette 0.29.0 से पहले, `name` पहला parameter था।

साथ ही, उससे पहले के versions में, `request` object को Jinja2 के context में key-value pairs के हिस्से के रूप में pass किया जाता था।

///

/// tip | सुझाव

`response_class=HTMLResponse` declare करने से docs UI यह जान पाएगा कि response HTML होगा।

///

/// note | तकनीकी विवरण

आप `from starlette.templating import Jinja2Templates` भी उपयोग कर सकते हैं।

**FastAPI** आपकी सुविधा के लिए, developer के रूप में, वही `starlette.templating` `fastapi.templating` के रूप में प्रदान करता है। लेकिन उपलब्ध अधिकांश responses सीधे Starlette से आते हैं। `Request` और `StaticFiles` के साथ भी यही है।

///

## Templates लिखना { #writing-templates }

फिर आप `templates/item.html` पर एक template लिख सकते हैं, उदाहरण के लिए:

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### Template Context Values { #template-context-values }

उस HTML में जिसमें यह शामिल है:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...यह आपके द्वारा pass किए गए "context" `dict` से लिया गया `id` दिखाएगा:

```Python
{"id": id}
```

उदाहरण के लिए, `42` की ID के साथ, यह render होगा:

```html
Item ID: 42
```

### Template `url_for` Arguments { #template-url-for-arguments }

आप template के अंदर `url_for()` का भी उपयोग कर सकते हैं, यह arguments के रूप में वही arguments लेता है जो आपके *path operation function* द्वारा उपयोग किए जाते।

इसलिए, इस section के साथ:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...यह उसी URL का link generate करेगा जिसे *path operation function* `read_item(id=id)` handle करेगा।

उदाहरण के लिए, `42` की ID के साथ, यह render होगा:

```html
<a href="/items/42">
```

## Templates और static files { #templates-and-static-files }

आप template के अंदर `url_for()` का भी उपयोग कर सकते हैं, और इसे, उदाहरण के लिए, उन `StaticFiles` के साथ उपयोग कर सकते हैं जिन्हें आपने `name="static"` के साथ mount किया है।

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

इस उदाहरण में, यह `static/styles.css` पर मौजूद CSS file से link करेगा:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

और क्योंकि आप `StaticFiles` उपयोग कर रहे हैं, वह CSS file आपके **FastAPI** application द्वारा URL `/static/styles.css` पर automatic रूप से serve की जाएगी।

## अधिक विवरण { #more-details }

अधिक विवरण के लिए, जिसमें templates को test करना भी शामिल है, [templates पर Starlette के docs](https://www.starlette.dev/templates/) देखें।
