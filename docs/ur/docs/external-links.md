# بیرونی لنکس

**FastAPI** کی ایک شاندار کمیونٹی ہے جو مسلسل بڑھ رہی ہے۔

**FastAPI** سے متعلق بہت سے مضامین، مقالات، tools، اور projects ہیں۔

آپ آسانی سے search engine یا video platform استعمال کرکے FastAPI سے متعلق بہت سے وسائل تلاش کر سکتے ہیں۔

/// info | معلومات

پہلے، اس صفحے پر بیرونی مضامین کے لنکس درج کیے جاتے تھے۔

لیکن اب جب FastAPI تمام زبانوں میں سب سے زیادہ GitHub stars والا backend framework ہے، اور Python میں سب سے زیادہ starred اور استعمال ہونے والا framework ہے، تو اس کے بارے میں لکھے گئے تمام مضامین درج کرنے کی کوشش کرنا اب مناسب نہیں رہا۔

///

## GitHub Repositories

سب سے زیادہ starred [`fastapi` topic والی GitHub repositories](https://github.com/topics/fastapi):

{% for repo in topic_repos %}

<a href={{repo.html_url}} target="_blank">★ {{repo.stars}} - {{repo.name}}</a> by <a href={{repo.owner_html_url}} target="_blank">@{{repo.owner_login}}</a>.

{% endfor %}
