# <div style="text-align: right;">بیرونی روابط اور مضامین</div>

<div style="direction: rtl;">
    <div style="direction: ltr; text-align: right;">
        ایک عظیم کمیونٹی مسلسل بڑھ رہی ہے۔ <span style="margin-right: 0;"><b>FastAPI</b></span>
    </div>
</div>
<br>
<div style="direction: rtl;">
    <div style="direction: ltr; text-align: right;">
    سے متعلق بہت ساری پوسٹس، آرٹیکلز، ٹولز اور پروجیکٹس ہیں۔  <span style="margin-right: 0;"><b>FastAPI</b></span>
    </div>
</div>
<br>
<div style="text-align: right;">
    یہاں ان میں سے کچھ کی ایک نامکمل فہرست ہے۔
</div>
<br>
<div style="text-align: right;">
    !!! ٹپ اگر آپ کے پاس کوئی مضمون، پروجیکٹ، ٹول، یا FastAPI سے متعلق کوئی چیز ہے جو ابھی تک یہاں درج نہیں ہے، تو اسے شامل کرنے کے لیے <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank"> پل کی درخواست</a> بنائیں۔
</div>
<br>

## <div style="text-align: right;">مضامین</div>
### <div style="text-align: right;">انگریزی</div>

{% if external_links %}
<ul style="direction: rtl;">
{% for article in external_links.articles.english %}
 <li><div style="text-align: right;"><a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> کی طرف سے <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.</div></li>
{% endfor %}
</ul>
{% endif %}

### <div style="text-align: right;">جاپانی</div>

{% if external_links %}
<ul style="direction: rtl;">
{% for article in external_links.articles.japanese %}
<li><div style="text-align: right;"><a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> کی طرف سے <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.</div></li>
{% endfor %}
</ul>
{% endif %}

### <div style="text-align: right;">ویتنامی</div>

{% if external_links %}
<ul style="direction: rtl;">
{% for article in external_links.articles.vietnamese %}
<li><div style="text-align: right;"><a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> کی طرف سے <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.</div></li>
{% endfor %}
</ul>
{% endif %}

### <div style="text-align: right;">روسی</div>

{% if external_links %}
<ul style="direction: rtl;">
{% for article in external_links.articles.russian %}
<li><div style="text-align: right;"><a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> کی طرف سے <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.</div></li>
{% endfor %}
</ul>
{% endif %}


### <div style="text-align: right;">جرمن</div>

{% if external_links %}
<ul style="direction: rtl;">
{% for article in external_links.articles.german %}
<li><div style="text-align: right;"><a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> کی طرف سے <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.</div></li>
{% endfor %}
</ul>
{% endif %}

### <div style="text-align: right;">تائیوانی</div>

{% if external_links %}
<ul style="direction: rtl;">
{% for article in external_links.articles.taiwanese %}
<li><div style="text-align: right;"><a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> کی طرف سے <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.</div></li>
{% endfor %}
</ul>
{% endif %}

## <div style="text-align: right;">پوڈکاسٹ</div>

{% if external_links %}
<ul style="direction: rtl;">
{% for article in external_links.podcasts.english %}
<li><div style="text-align: right;"><a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> کی طرف سے <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.</div></li>
{% endfor %}
</ul>
{% endif %}

## <div style="text-align: right;">بات چیت</div>

{% if external_links %}
<ul style="direction: rtl;">
{% for article in external_links.talks.english %}
<li><div style="text-align: right;"><a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> کی طرف سے <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.</div></li>
{% endfor %}
</ul>
{% endif %}


## <div style="text-align: right;">پروجیکٹس</div>

<div style="text-align: right;">'fastapi' عنوان کے ساتھ تازہ ترین GitHub پروجیکٹس:</div>

<div class="github-topic-projects">
</div>
