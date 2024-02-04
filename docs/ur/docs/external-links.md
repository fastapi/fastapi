# <div>بیرونی روابط اور مضامین</div>

<div>
    ایک عظیم کمیونٹی مسلسل بڑھ رہی ہے <b>FastAPI</b>۔
</div>

<br>
<div>
<b>FastAPI</b> سے متعلق بہت سی پوسٹس، مضامین، ٹولز اور پروجیکٹس ہیں.
</div>
<br>
<div>
    یہاں ان میں سے کچھ کی ایک نامکمل فہرست ہے۔
</div>
<br>
<div>
    !!! ٹپ اگر آپ کے پاس کوئی مضمون، پروجیکٹ، ٹول، یا FastAPI سے متعلق کوئی چیز ہے جو ابھی تک یہاں درج نہیں ہے، تو اسے شامل کرنے کے لیے <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank"> پل کی درخواست</a> بنائیں۔
</div>
<br>


{% for section_name, section_content in external_links.items() %}

## <div>{{ section_name }}</div>

{% for lang_name, lang_content in section_content.items() %}

### <div>{{ lang_name }}</div>

{% for item in lang_content %}

* <div><a href="{{ item.link }}" class="external-link" target="_blank">{{ item.title }}</a> by <a href="{{ item.author_link }}" class="external-link" target="_blank">{{ item.author }}</a>.</div>

{% endfor %}
{% endfor %}
{% endfor %}


## <div>پروجیکٹس</div>

<div>'fastapi' عنوان کے ساتھ تازہ ترین GitHub پروجیکٹس:</div>

<div class="github-topic-projects">
</div>
