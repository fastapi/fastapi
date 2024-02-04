# بیرونی روابط اور مضامین

ایک عظیم کمیونٹی مسلسل بڑھ رہی ہے <b>FastAPI</b>۔
<br>
<b>FastAPI</b> سے متعلق بہت سی پوسٹس، مضامین، ٹولز اور پروجیکٹس ہیں.
<br>
یہاں ان میں سے کچھ کی ایک نامکمل فہرست ہے۔
<br>
    !!! ٹپ اگر آپ کے پاس کوئی مضمون، پروجیکٹ، ٹول، یا FastAPI سے متعلق کوئی چیز ہے جو ابھی تک یہاں درج نہیں ہے، تو اسے شامل کرنے کے لیے <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank"> پل کی درخواست</a> بنائیں۔
<br>
{% for section_name, section_content in external_links.items() %}

## {{ section_name }}

{% for lang_name, lang_content in section_content.items() %}

### {{ lang_name }}

{% for item in lang_content %}

* <a href="{{ item.link }}" class="external-link" target="_blank">{{ item.title }}</a> by <a href="{{ item.author_link }}" class="external-link" target="_blank">{{ item.author }}</a>.

{% endfor %}
{% endfor %}
{% endfor %}


## پروجیکٹس
تازہ ترین GitHub پروجیکٹس موضوع کے ساتھ `fastapi`:

<div class="github-topic-projects">
</div>
