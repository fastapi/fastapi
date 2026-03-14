# حسب ضرورت Docs UI Static Assets (Self-Hosting) { #custom-docs-ui-static-assets-self-hosting }

API docs **Swagger UI** اور **ReDoc** استعمال کرتے ہیں، اور ان میں سے ہر ایک کو کچھ JavaScript اور CSS فائلوں کی ضرورت ہوتی ہے۔

بطور default، وہ فائلیں ایک <abbr title="Content Delivery Network: ایک سروس، جو عام طور پر کئی servers پر مشتمل ہوتی ہے، جو static فائلیں فراہم کرتی ہے، جیسے JavaScript اور CSS۔ یہ عام طور پر client کے قریب ترین server سے فائلیں فراہم کرنے کے لیے استعمال ہوتی ہے، جو کارکردگی بہتر بناتی ہے۔">CDN</abbr> سے فراہم کی جاتی ہیں۔

لیکن اسے اپنی مرضی کے مطابق بنانا ممکن ہے، آپ کوئی مخصوص CDN سیٹ کر سکتے ہیں، یا فائلیں خود فراہم کر سکتے ہیں۔

## JavaScript اور CSS کے لیے حسب ضرورت CDN { #custom-cdn-for-javascript-and-css }

فرض کریں کہ آپ ایک مختلف <abbr title="Content Delivery Network">CDN</abbr> استعمال کرنا چاہتے ہیں، مثال کے طور پر آپ `https://unpkg.com/` استعمال کرنا چاہتے ہیں۔

یہ مفید ہو سکتا ہے اگر مثلاً آپ کسی ایسے ملک میں رہتے ہیں جو کچھ URLs پر پابندی لگاتا ہے۔

### خود کار docs غیر فعال کریں { #disable-the-automatic-docs }

پہلا مرحلہ خود کار docs کو غیر فعال کرنا ہے، کیونکہ بطور default، وہ default CDN استعمال کرتے ہیں۔

انہیں غیر فعال کرنے کے لیے، اپنی `FastAPI` app بناتے وقت ان کے URLs کو `None` پر سیٹ کریں:

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[8] *}

### حسب ضرورت docs شامل کریں { #include-the-custom-docs }

اب آپ حسب ضرورت docs کے لیے *path operations* بنا سکتے ہیں۔

آپ docs کے لیے HTML صفحات بنانے کے لیے FastAPI کے اندرونی functions دوبارہ استعمال کر سکتے ہیں، اور انہیں مطلوبہ arguments پاس کر سکتے ہیں:

* `openapi_url`: وہ URL جہاں سے docs کا HTML صفحہ آپ کی API کا OpenAPI schema حاصل کر سکتا ہے۔ آپ یہاں `app.openapi_url` attribute استعمال کر سکتے ہیں۔
* `title`: آپ کی API کا عنوان۔
* `oauth2_redirect_url`: آپ default استعمال کرنے کے لیے یہاں `app.swagger_ui_oauth2_redirect_url` استعمال کر سکتے ہیں۔
* `swagger_js_url`: وہ URL جہاں سے آپ کے Swagger UI docs کا HTML **JavaScript** فائل حاصل کر سکتا ہے۔ یہ حسب ضرورت CDN URL ہے۔
* `swagger_css_url`: وہ URL جہاں سے آپ کے Swagger UI docs کا HTML **CSS** فائل حاصل کر سکتا ہے۔ یہ حسب ضرورت CDN URL ہے۔

اور اسی طرح ReDoc کے لیے...

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[2:6,11:19,22:24,27:33] *}

/// tip | مشورہ

`swagger_ui_redirect` کے لیے *path operation* اس وقت کام آتا ہے جب آپ OAuth2 استعمال کرتے ہیں۔

اگر آپ اپنی API کو کسی OAuth2 provider کے ساتھ integrate کرتے ہیں، تو آپ authenticate ہو کر حاصل کردہ credentials کے ساتھ API docs پر واپس آ سکیں گے۔ اور حقیقی OAuth2 authentication کا استعمال کرتے ہوئے اس کے ساتھ تعامل کر سکیں گے۔

Swagger UI پردے کے پیچھے آپ کے لیے اسے سنبھالے گا، لیکن اسے اس "redirect" helper کی ضرورت ہے۔

///

### جانچ کے لیے *path operation* بنائیں { #create-a-path-operation-to-test-it }

اب، سب کچھ کام کر رہا ہے یہ جانچنے کے لیے، ایک *path operation* بنائیں:

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[36:38] *}

### جانچ کریں { #test-it }

اب، آپ اپنے docs پر [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) جا کر صفحہ دوبارہ load کر سکتے ہیں، یہ نئے CDN سے assets load کرے گا۔

## Docs کے لیے JavaScript اور CSS خود host کریں { #self-hosting-javascript-and-css-for-docs }

JavaScript اور CSS خود host کرنا مفید ہو سکتا ہے اگر، مثال کے طور پر، آپ کو اپنی app کو آف لائن بھی کام کرتے رہنے کی ضرورت ہے، بغیر کسی Internet رسائی کے، یا مقامی network میں۔

یہاں آپ دیکھیں گے کہ ان فائلوں کو اسی FastAPI app میں خود کیسے فراہم کیا جائے، اور docs کو ان کا استعمال کرنے کے لیے کیسے ترتیب دیا جائے۔

### پروجیکٹ کی فائل ساخت { #project-file-structure }

فرض کریں آپ کے پروجیکٹ کی فائل ساخت اس طرح نظر آتی ہے:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

اب ان static فائلوں کو ذخیرہ کرنے کے لیے ایک directory بنائیں۔

آپ کی نئی فائل ساخت اس طرح نظر آ سکتی ہے:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### فائلیں ڈاؤن لوڈ کریں { #download-the-files }

Docs کے لیے ضروری static فائلیں ڈاؤن لوڈ کریں اور انہیں اس `static/` directory میں رکھیں۔

آپ غالباً ہر لنک پر right-click کر کے "Save link as..." جیسا آپشن منتخب کر سکتے ہیں۔

**Swagger UI** یہ فائلیں استعمال کرتا ہے:

* [`swagger-ui-bundle.js`](https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js)
* [`swagger-ui.css`](https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css)

اور **ReDoc** یہ فائل استعمال کرتا ہے:

* [`redoc.standalone.js`](https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js)

اس کے بعد، آپ کی فائل ساخت اس طرح نظر آ سکتی ہے:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

### Static فائلیں فراہم کریں { #serve-the-static-files }

* `StaticFiles` import کریں۔
* ایک مخصوص path پر `StaticFiles()` instance "Mount" کریں۔

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[7,11] *}

### Static فائلوں کی جانچ کریں { #test-the-static-files }

اپنی application شروع کریں اور [http://127.0.0.1:8000/static/redoc.standalone.js](http://127.0.0.1:8000/static/redoc.standalone.js) پر جائیں۔

آپ کو **ReDoc** کے لیے ایک بہت لمبی JavaScript فائل نظر آنی چاہیے۔

یہ کچھ اس طرح شروع ہو سکتی ہے:

```JavaScript
/*! For license information please see redoc.standalone.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("null")):
...
```

یہ تصدیق کرتا ہے کہ آپ اپنی app سے static فائلیں فراہم کر سکتے ہیں، اور آپ نے docs کی static فائلیں صحیح جگہ رکھی ہیں۔

اب ہم app کو ان static فائلوں کو docs کے لیے استعمال کرنے کے لیے ترتیب دے سکتے ہیں۔

### Static فائلوں کے لیے خود کار docs غیر فعال کریں { #disable-the-automatic-docs-for-static-files }

حسب ضرورت CDN استعمال کرنے کی طرح، پہلا مرحلہ خود کار docs کو غیر فعال کرنا ہے، کیونکہ وہ بطور default CDN استعمال کرتے ہیں۔

انہیں غیر فعال کرنے کے لیے، اپنی `FastAPI` app بناتے وقت ان کے URLs کو `None` پر سیٹ کریں:

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[9] *}

### Static فائلوں کے لیے حسب ضرورت docs شامل کریں { #include-the-custom-docs-for-static-files }

اور حسب ضرورت CDN کی طرح، اب آپ حسب ضرورت docs کے لیے *path operations* بنا سکتے ہیں۔

دوبارہ، آپ docs کے لیے HTML صفحات بنانے کے لیے FastAPI کے اندرونی functions دوبارہ استعمال کر سکتے ہیں، اور انہیں مطلوبہ arguments پاس کر سکتے ہیں:

* `openapi_url`: وہ URL جہاں سے docs کا HTML صفحہ آپ کی API کا OpenAPI schema حاصل کر سکتا ہے۔ آپ یہاں `app.openapi_url` attribute استعمال کر سکتے ہیں۔
* `title`: آپ کی API کا عنوان۔
* `oauth2_redirect_url`: آپ default استعمال کرنے کے لیے یہاں `app.swagger_ui_oauth2_redirect_url` استعمال کر سکتے ہیں۔
* `swagger_js_url`: وہ URL جہاں سے آپ کے Swagger UI docs کا HTML **JavaScript** فائل حاصل کر سکتا ہے۔ **یہ وہی ہے جو آپ کی اپنی app اب فراہم کر رہی ہے**۔
* `swagger_css_url`: وہ URL جہاں سے آپ کے Swagger UI docs کا HTML **CSS** فائل حاصل کر سکتا ہے۔ **یہ وہی ہے جو آپ کی اپنی app اب فراہم کر رہی ہے**۔

اور اسی طرح ReDoc کے لیے...

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[2:6,14:22,25:27,30:36] *}

/// tip | مشورہ

`swagger_ui_redirect` کے لیے *path operation* اس وقت کام آتا ہے جب آپ OAuth2 استعمال کرتے ہیں۔

اگر آپ اپنی API کو کسی OAuth2 provider کے ساتھ integrate کرتے ہیں، تو آپ authenticate ہو کر حاصل کردہ credentials کے ساتھ API docs پر واپس آ سکیں گے۔ اور حقیقی OAuth2 authentication کا استعمال کرتے ہوئے اس کے ساتھ تعامل کر سکیں گے۔

Swagger UI پردے کے پیچھے آپ کے لیے اسے سنبھالے گا، لیکن اسے اس "redirect" helper کی ضرورت ہے۔

///

### Static فائلوں کی جانچ کے لیے *path operation* بنائیں { #create-a-path-operation-to-test-static-files }

اب، سب کچھ کام کر رہا ہے یہ جانچنے کے لیے، ایک *path operation* بنائیں:

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[39:41] *}

### Static فائلوں کے UI کی جانچ { #test-static-files-ui }

اب، آپ اپنا WiFi بند کر کے اپنے docs پر [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) جا سکتے ہیں اور صفحہ دوبارہ load کر سکتے ہیں۔

اور Internet کے بغیر بھی، آپ اپنی API کے docs دیکھ سکیں گے اور اس کے ساتھ تعامل کر سکیں گے۔
