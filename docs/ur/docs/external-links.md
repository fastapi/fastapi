# بیرونی روابط اور مضامین


<div style="direction: ltr; text-align: right;">
    ایک عظیم کمیونٹی مسلسل بڑھ رہی ہے۔ <span style="margin-right: 0;"><b>FastAPI</b></span>
</div>

<br>
<div style="direction: ltr; text-align: right;">
سے متعلق بہت ساری پوسٹس، آرٹیکلز، ٹولز اور پروجیکٹس ہیں۔  <span style="margin-right: 0;"><b>FastAPI</b></span>
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


{% for section_name, section_content in external_links.items() %}

## <div style="text-align: right;">{{ section_name }}</div>

{% for lang_name, lang_content in section_content.items() %}

### <div style="text-align: right;">{{ lang_name }}</div>

{% for item in lang_content %}

* <div style="text-align: right;"><a href="{{ item.link }}" class="external-link" target="_blank">{{ item.title }}</a> by <a href="{{ item.author_link }}" class="external-link" target="_blank">{{ item.author }}</a>.</div>

{% endfor %}
{% endfor %}
{% endfor %}


## <div style="text-align: right;">پروجیکٹس</div>

<div style="text-align: right;">'fastapi' عنوان کے ساتھ تازہ ترین GitHub پروجیکٹس:</div>

<div class="github-topic-projects">
</div>
