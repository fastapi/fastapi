# Metadata اور Docs URLs { #metadata-and-docs-urls }

آپ اپنی **FastAPI** application میں کئی metadata configurations کو حسب ضرورت بنا سکتے ہیں۔

## API کے لیے Metadata { #metadata-for-api }

آپ درج ذیل fields سیٹ کر سکتے ہیں جو OpenAPI specification اور خودکار API docs UIs میں استعمال ہوتے ہیں:

| Parameter | Type | تفصیل |
|------------|------|-------------|
| `title` | `str` | API کا عنوان۔ |
| `summary` | `str` | API کا مختصر خلاصہ۔ <small>OpenAPI 3.1.0 سے دستیاب، FastAPI 0.99.0۔</small> |
| `description` | `str` | API کی مختصر تفصیل۔ یہ Markdown استعمال کر سکتی ہے۔ |
| `version` | `string` | API کا ورژن۔ یہ آپ کی اپنی application کا ورژن ہے، OpenAPI کا نہیں۔ مثلاً `2.5.0`۔ |
| `terms_of_service` | `str` | API کی Terms of Service کا URL۔ اگر فراہم کیا جائے تو یہ URL ہونا ضروری ہے۔ |
| `contact` | `dict` | API کی رابطہ معلومات۔ اس میں کئی fields ہو سکتے ہیں۔ <details><summary><code>contact</code> fields</summary><table><thead><tr><th>Parameter</th><th>Type</th><th>تفصیل</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>رابطہ شخص/تنظیم کا شناختی نام۔</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>رابطہ معلومات کی طرف اشارہ کرنے والا URL۔ URL کی شکل میں ہونا ضروری ہے۔</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>رابطہ شخص/تنظیم کا email پتہ۔ email پتے کی شکل میں ہونا ضروری ہے۔</td></tr></tbody></table></details> |
| `license_info` | `dict` | API کی license معلومات۔ اس میں کئی fields ہو سکتے ہیں۔ <details><summary><code>license_info</code> fields</summary><table><thead><tr><th>Parameter</th><th>Type</th><th>تفصیل</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>ضروری</strong> (اگر <code>license_info</code> سیٹ ہو)۔ API کے لیے استعمال شدہ license کا نام۔</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>API کے لیے ایک [SPDX](https://spdx.org/licenses/) license expression۔ <code>identifier</code> field <code>url</code> field سے باہمی طور پر خارج ہے۔ <small>OpenAPI 3.1.0 سے دستیاب، FastAPI 0.99.0۔</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>API کے لیے استعمال شدہ license کا URL۔ URL کی شکل میں ہونا ضروری ہے۔</td></tr></tbody></table></details> |

آپ انہیں اس طرح سیٹ کر سکتے ہیں:

{* ../../docs_src/metadata/tutorial001_py310.py hl[3:16, 19:32] *}

/// tip | مشورہ

آپ `description` field میں Markdown لکھ سکتے ہیں اور یہ output میں render ہوگا۔

///

اس configuration کے ساتھ، خودکار API docs اس طرح نظر آئیں گے:

<img src="/img/tutorial/metadata/image01.png">

## License identifier { #license-identifier }

OpenAPI 3.1.0 اور FastAPI 0.99.0 سے، آپ `license_info` کو `url` کی بجائے `identifier` کے ساتھ بھی سیٹ کر سکتے ہیں۔

مثال کے طور پر:

{* ../../docs_src/metadata/tutorial001_1_py310.py hl[31] *}

## Tags کے لیے Metadata { #metadata-for-tags }

آپ `openapi_tags` parameter کے ذریعے اپنے path operations کو گروپ کرنے کے لیے استعمال ہونے والے مختلف tags کے لیے اضافی metadata بھی شامل کر سکتے ہیں۔

یہ ایک فہرست لیتا ہے جس میں ہر tag کے لیے ایک dictionary ہوتی ہے۔

ہر dictionary میں یہ ہو سکتا ہے:

* `name` (**ضروری**): ایک `str` جس میں وہی tag نام ہو جو آپ اپنے *path operations* اور `APIRouter`s میں `tags` parameter میں استعمال کرتے ہیں۔
* `description`: ایک `str` جس میں tag کی مختصر تفصیل ہو۔ اس میں Markdown ہو سکتا ہے اور docs UI میں دکھایا جائے گا۔
* `externalDocs`: ایک `dict` جو بیرونی دستاویزات بیان کرے:
    * `description`: ایک `str` جس میں بیرونی docs کی مختصر تفصیل ہو۔
    * `url` (**ضروری**): ایک `str` جس میں بیرونی دستاویزات کا URL ہو۔

### Tags کے لیے metadata بنائیں { #create-metadata-for-tags }

آئیں اسے `users` اور `items` کے tags کی مثال میں آزمائیں۔

اپنے tags کے لیے metadata بنائیں اور اسے `openapi_tags` parameter کو دیں:

{* ../../docs_src/metadata/tutorial004_py310.py hl[3:16,18] *}

دیکھیں کہ آپ descriptions کے اندر Markdown استعمال کر سکتے ہیں، مثلاً "login" بولڈ میں دکھایا جائے گا (**login**) اور "fancy" اٹالک میں (_fancy_)۔

/// tip | مشورہ

آپ کو ہر اس tag کے لیے metadata شامل کرنے کی ضرورت نہیں جو آپ استعمال کرتے ہیں۔

///

### اپنے tags استعمال کریں { #use-your-tags }

اپنے *path operations* (اور `APIRouter`s) کے ساتھ `tags` parameter استعمال کریں تاکہ انہیں مختلف tags میں تقسیم کریں:

{* ../../docs_src/metadata/tutorial004_py310.py hl[21,26] *}

/// info | معلومات

Tags کے بارے میں مزید [Path Operation Configuration](path-operation-configuration.md#tags) میں پڑھیں۔

///

### Docs چیک کریں { #check-the-docs }

اب، اگر آپ docs چیک کریں، تو وہ تمام اضافی metadata دکھائیں گے:

<img src="/img/tutorial/metadata/image02.png">

### Tags کی ترتیب { #order-of-tags }

ہر tag metadata dictionary کی ترتیب docs UI میں دکھائی جانے والی ترتیب کو بھی define کرتی ہے۔

مثال کے طور پر، اگرچہ `users` حروف تہجی کی ترتیب میں `items` کے بعد آتا ہے، یہ ان سے پہلے دکھایا جاتا ہے، کیونکہ ہم نے ان کا metadata فہرست میں پہلی dictionary کے طور پر شامل کیا ہے۔

## OpenAPI URL { #openapi-url }

بطور ڈیفالٹ، OpenAPI schema `/openapi.json` پر serve ہوتا ہے۔

لیکن آپ اسے `openapi_url` parameter سے configure کر سکتے ہیں۔

مثال کے طور پر، اسے `/api/v1/openapi.json` پر serve کرنے کے لیے:

{* ../../docs_src/metadata/tutorial002_py310.py hl[3] *}

اگر آپ OpenAPI schema کو مکمل طور پر غیر فعال کرنا چاہتے ہیں تو آپ `openapi_url=None` سیٹ کر سکتے ہیں، اس سے وہ documentation user interfaces بھی غیر فعال ہو جائیں گی جو اسے استعمال کرتے ہیں۔

## Docs URLs { #docs-urls }

آپ شامل کیے گئے دو documentation user interfaces کو configure کر سکتے ہیں:

* **Swagger UI**: `/docs` پر serve ہوتا ہے۔
    * آپ `docs_url` parameter سے اس کا URL سیٹ کر سکتے ہیں۔
    * آپ `docs_url=None` سیٹ کر کے اسے غیر فعال کر سکتے ہیں۔
* **ReDoc**: `/redoc` پر serve ہوتا ہے۔
    * آپ `redoc_url` parameter سے اس کا URL سیٹ کر سکتے ہیں۔
    * آپ `redoc_url=None` سیٹ کر کے اسے غیر فعال کر سکتے ہیں۔

مثال کے طور پر، Swagger UI کو `/documentation` پر serve کرنے اور ReDoc کو غیر فعال کرنے کے لیے:

{* ../../docs_src/metadata/tutorial003_py310.py hl[3] *}
