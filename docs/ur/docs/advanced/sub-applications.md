# Sub Applications - Mounts { #sub-applications-mounts }

اگر آپ کو دو آزاد FastAPI ایپلیکیشنز رکھنی ہوں، جن کے اپنے آزاد OpenAPI اور اپنے docs UIs ہوں، تو آپ ایک مرکزی ایپ رکھ سکتے ہیں اور ایک (یا زیادہ) sub-application(s) "mount" کر سکتے ہیں۔

## **FastAPI** ایپلیکیشن mount کرنا { #mounting-a-fastapi-application }

"Mounting" کا مطلب ہے ایک مکمل طور پر "آزاد" ایپلیکیشن کو کسی مخصوص path پر شامل کرنا، جو پھر اس path کے نیچے سب کچھ ہینڈل کرتی ہے، اس sub-application میں بیان کردہ _path operations_ کے ساتھ۔

### اعلیٰ سطح کی ایپلیکیشن { #top-level-application }

سب سے پہلے، مرکزی، اعلیٰ سطح کی **FastAPI** ایپلیکیشن بنائیں، اور اس کی *path operations*:

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[3, 6:8] *}

### Sub-application { #sub-application }

پھر، اپنی sub-application بنائیں، اور اس کی *path operations*۔

یہ sub-application صرف ایک اور معیاری FastAPI ایپلیکیشن ہے، لیکن یہ وہ ہے جو "mount" ہوگی:

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 14:16] *}

### Sub-application mount کریں { #mount-the-sub-application }

اپنی اعلیٰ سطح کی ایپلیکیشن `app` میں، sub-application `subapi` کو mount کریں۔

اس صورت میں، یہ path `/subapi` پر mount ہوگی:

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 19] *}

### خودکار API docs چیک کریں { #check-the-automatic-api-docs }

اب، `fastapi` کمانڈ چلائیں:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

اور docs کو [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) پر کھولیں۔

آپ مرکزی ایپ کی خودکار API docs دیکھیں گے، جس میں صرف اس کی اپنی _path operations_ شامل ہوں گی:

<img src="/img/tutorial/sub-applications/image01.png">

اور پھر، sub-application کی docs [http://127.0.0.1:8000/subapi/docs](http://127.0.0.1:8000/subapi/docs) پر کھولیں۔

آپ sub-application کی خودکار API docs دیکھیں گے، جس میں صرف اس کی اپنی _path operations_ شامل ہوں گی، سب درست sub-path prefix `/subapi` کے نیچے:

<img src="/img/tutorial/sub-applications/image02.png">

اگر آپ دونوں user interfaces میں سے کسی کے ساتھ بات چیت کرنے کی کوشش کریں، تو وہ درست طریقے سے کام کریں گے، کیونکہ browser ہر مخصوص ایپ یا sub-app سے بات کر سکے گا۔

### تکنیکی تفصیلات: `root_path` { #technical-details-root-path }

جب آپ اوپر بیان کردہ طریقے سے sub-application mount کرتے ہیں، FastAPI ASGI specification کے ایک مکینزم جسے `root_path` کہتے ہیں، استعمال کرکے sub-application کے mount path کو منتقل کرنے کا خیال رکھتا ہے۔

اس طریقے سے، sub-application کو docs UI کے لیے اس path prefix کو استعمال کرنے کا علم ہوگا۔

اور sub-application کی اپنی بھی mount شدہ sub-applications ہو سکتی ہیں اور سب کچھ درست طریقے سے کام کرے گا، کیونکہ FastAPI ان تمام `root_path`s کو خود بخود ہینڈل کرتا ہے۔

آپ `root_path` اور اسے واضح طور پر استعمال کرنے کے بارے میں مزید [Proxy کے پیچھے](behind-a-proxy.md) سیکشن میں جانیں گے۔
