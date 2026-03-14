# بڑی Applications - متعدد فائلیں { #bigger-applications-multiple-files }

اگر آپ کوئی application یا web API بنا رہے ہیں، تو شاذ و نادر ہی ایسا ہوتا ہے کہ آپ سب کچھ ایک واحد فائل میں رکھ سکیں۔

**FastAPI** آپ کی application کی ساخت بنانے کے لیے ایک آسان tool فراہم کرتا ہے جبکہ تمام لچک برقرار رکھتا ہے۔

/// info | معلومات

اگر آپ Flask سے آئے ہیں، تو یہ Flask کے Blueprints کے مساوی ہوگا۔

///

## فائل کی ساخت کی مثال { #an-example-file-structure }

فرض کریں آپ کے پاس اس طرح کی فائل ساخت ہے:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

/// tip | مشورہ

کئی `__init__.py` فائلیں ہیں: ہر directory یا subdirectory میں ایک۔

یہی وہ چیز ہے جو ایک فائل سے دوسری میں code import کرنے کی اجازت دیتی ہے۔

مثال کے طور پر، `app/main.py` میں آپ کے پاس ایسی لائن ہو سکتی ہے:

```
from app.routers import items
```

///

* `app` directory میں سب کچھ ہے۔ اور اس میں ایک خالی فائل `app/__init__.py` ہے، تو یہ ایک "Python package" ہے (Python "modules" کا مجموعہ): `app`۔
* اس میں ایک `app/main.py` فائل ہے۔ چونکہ یہ ایک Python package (ایسی directory جس میں `__init__.py` فائل ہو) کے اندر ہے، یہ اس package کا ایک "module" ہے: `app.main`۔
* ایک `app/dependencies.py` فائل بھی ہے، بالکل `app/main.py` کی طرح، یہ ایک "module" ہے: `app.dependencies`۔
* ایک subdirectory `app/routers/` ہے جس میں ایک اور `__init__.py` فائل ہے، تو یہ ایک "Python subpackage" ہے: `app.routers`۔
* فائل `app/routers/items.py` ایک package `app/routers/` کے اندر ہے، تو یہ ایک submodule ہے: `app.routers.items`۔
* `app/routers/users.py` کے ساتھ بھی یہی ہے، یہ ایک اور submodule ہے: `app.routers.users`۔
* ایک subdirectory `app/internal/` بھی ہے جس میں ایک اور `__init__.py` فائل ہے، تو یہ ایک اور "Python subpackage" ہے: `app.internal`۔
* اور فائل `app/internal/admin.py` ایک اور submodule ہے: `app.internal.admin`۔

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

تبصروں کے ساتھ وہی فائل ساخت:

```bash
.
├── app                  # "app" is a Python package
│   ├── __init__.py      # this file makes "app" a "Python package"
│   ├── main.py          # "main" module, e.g. import app.main
│   ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
│   └── routers          # "routers" is a "Python subpackage"
│   │   ├── __init__.py  # makes "routers" a "Python subpackage"
│   │   ├── items.py     # "items" submodule, e.g. import app.routers.items
│   │   └── users.py     # "users" submodule, e.g. import app.routers.users
│   └── internal         # "internal" is a "Python subpackage"
│       ├── __init__.py  # makes "internal" a "Python subpackage"
│       └── admin.py     # "admin" submodule, e.g. import app.internal.admin
```

## `APIRouter` { #apirouter }

فرض کریں صرف users کو handle کرنے کے لیے وقف فائل submodule `/app/routers/users.py` میں ہے۔

آپ اپنے users سے متعلق *path operations* کو باقی code سے الگ رکھنا چاہتے ہیں، تاکہ اسے منظم رکھا جا سکے۔

لیکن یہ اب بھی اسی **FastAPI** application/web API کا حصہ ہے (یہ اسی "Python Package" کا حصہ ہے)۔

آپ `APIRouter` استعمال کر کے اس module کے لیے *path operations* بنا سکتے ہیں۔

### `APIRouter` import کریں { #import-apirouter }

آپ اسے import کریں اور بالکل اسی طرح ایک "instance" بنائیں جیسے آپ `FastAPI` class کے ساتھ بناتے:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[1,3] title["app/routers/users.py"] *}

### `APIRouter` کے ساتھ *Path operations* { #path-operations-with-apirouter }

اور پھر آپ اسے اپنے *path operations* declare کرنے کے لیے استعمال کریں۔

اسے بالکل اسی طرح استعمال کریں جیسے آپ `FastAPI` class استعمال کرتے:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[6,11,16] title["app/routers/users.py"] *}

آپ `APIRouter` کو ایک "چھوٹا `FastAPI`" class سمجھ سکتے ہیں۔

تمام اختیارات حمایت یافتہ ہیں۔

تمام وہی `parameters`، `responses`، `dependencies`، `tags`، وغیرہ۔

/// tip | مشورہ

اس مثال میں، variable کا نام `router` ہے، لیکن آپ اسے جو چاہیں نام دے سکتے ہیں۔

///

ہم اس `APIRouter` کو مرکزی `FastAPI` app میں شامل کریں گے، لیکن پہلے، آئیں dependencies اور ایک اور `APIRouter` دیکھتے ہیں۔

## Dependencies { #dependencies }

ہم دیکھتے ہیں کہ ہمیں application کے کئی مقامات پر استعمال ہونے والی کچھ dependencies کی ضرورت ہوگی۔

تو ہم انہیں ان کے اپنے `dependencies` module (`app/dependencies.py`) میں رکھتے ہیں۔

ہم اب ایک سادہ dependency استعمال کریں گے تاکہ ایک custom `X-Token` header پڑھا جا سکے:

{* ../../docs_src/bigger_applications/app_an_py310/dependencies.py hl[3,6:8] title["app/dependencies.py"] *}

/// tip | مشورہ

ہم اس مثال کو آسان بنانے کے لیے ایک فرضی header استعمال کر رہے ہیں۔

لیکن حقیقی صورتوں میں آپ کو مربوط [Security utilities](security/index.md) استعمال کرنے سے بہتر نتائج ملیں گے۔

///

## `APIRouter` کے ساتھ ایک اور module { #another-module-with-apirouter }

فرض کریں آپ کے پاس `app/routers/items.py` module میں "items" کو handle کرنے کے لیے وقف endpoints بھی ہیں۔

آپ کے پاس ان کے لیے *path operations* ہیں:

* `/items/`
* `/items/{item_id}`

یہ سب `app/routers/users.py` جیسی ہی ساخت ہے۔

لیکن ہم زیادہ ہوشیار بننا چاہتے ہیں اور code کو تھوڑا آسان بنانا چاہتے ہیں۔

ہم جانتے ہیں کہ اس module کے تمام *path operations* میں ایک جیسا ہے:

* Path `prefix`: `/items`۔
* `tags`: (صرف ایک tag: `items`)۔
* اضافی `responses`۔
* `dependencies`: ان سب کو وہ `X-Token` dependency چاہیے جو ہم نے بنائی۔

تو، ہر *path operation* میں یہ سب شامل کرنے کی بجائے، ہم اسے `APIRouter` میں شامل کر سکتے ہیں۔

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[5:10,16,21] title["app/routers/items.py"] *}

چونکہ ہر *path operation* کا path `/` سے شروع ہونا ضروری ہے، جیسے:

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...prefix میں آخری `/` شامل نہیں ہونا چاہیے۔

تو، اس صورت میں prefix `/items` ہے۔

ہم `tags` اور اضافی `responses` کی فہرست بھی شامل کر سکتے ہیں جو اس router میں شامل تمام *path operations* پر لاگو ہوں گے۔

اور ہم `dependencies` کی فہرست شامل کر سکتے ہیں جو router کے تمام *path operations* میں شامل ہوں گی اور ان کی ہر request کے لیے execute/solve ہوں گی۔

/// tip | مشورہ

یاد رکھیں، بالکل [dependencies in *path operation decorators*](dependencies/dependencies-in-path-operation-decorators.md) کی طرح، آپ کے *path operation function* کو کوئی قدر منتقل نہیں کی جائے گی۔

///

آخری نتیجہ یہ ہے کہ item paths اب ہیں:

* `/items/`
* `/items/{item_id}`

...جیسا کہ ہم چاہتے تھے۔

* انہیں ایک واحد string `"items"` پر مشتمل tags کی فہرست سے نشان زد کیا جائے گا۔
    * یہ "tags" خاص طور پر خودکار interactive documentation systems (OpenAPI استعمال کرتے ہوئے) کے لیے مفید ہیں۔
* ان سب میں پہلے سے define شدہ `responses` شامل ہوں گے۔
* ان تمام *path operations* سے پہلے `dependencies` کی فہرست evaluate/execute ہوگی۔
    * اگر آپ کسی مخصوص *path operation* میں بھی dependencies declare کرتے ہیں، **تو وہ بھی execute ہوں گی**۔
    * Router dependencies پہلے execute ہوتی ہیں، پھر [decorator میں `dependencies`](dependencies/dependencies-in-path-operation-decorators.md)، اور پھر عام parameter dependencies۔
    * آپ [`Security` dependencies بمع `scopes`](../advanced/security/oauth2-scopes.md) بھی شامل کر سکتے ہیں۔

/// tip | مشورہ

`APIRouter` میں `dependencies` رکھنا استعمال کیا جا سکتا ہے، مثال کے طور پر، *path operations* کے پورے گروپ کے لیے authentication لازمی بنانے کے لیے۔ چاہے dependencies انفرادی طور پر ہر ایک میں شامل نہ کی گئی ہوں۔

///

/// check

`prefix`، `tags`، `responses`، اور `dependencies` parameters (جیسا کہ بہت سی دوسری صورتوں میں) code کی تکرار سے بچنے میں **FastAPI** کی طرف سے ایک آسانی ہے۔

///

### Dependencies import کریں { #import-the-dependencies }

یہ code module `app.routers.items` میں ہے، فائل `app/routers/items.py`۔

اور ہمیں module `app.dependencies` سے dependency function حاصل کرنی ہے، فائل `app/dependencies.py`۔

تو ہم dependencies کے لیے `..` کے ساتھ relative import استعمال کرتے ہیں:

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[3] title["app/routers/items.py"] *}

#### Relative imports کیسے کام کرتے ہیں { #how-relative-imports-work }

/// tip | مشورہ

اگر آپ imports کے کام کرنے کے طریقے کو بخوبی جانتے ہیں، تو نیچے اگلے سیکشن پر جائیں۔

///

ایک واحد ڈاٹ `.`، جیسے:

```Python
from .dependencies import get_token_header
```

کا مطلب ہوگا:

* اسی package سے شروع کریں جس میں یہ module (فائل `app/routers/items.py`) موجود ہے (directory `app/routers/`)...
* `dependencies` module تلاش کریں (ایک فرضی فائل `app/routers/dependencies.py` پر)...
* اور اس سے function `get_token_header` import کریں۔

لیکن وہ فائل موجود نہیں ہے، ہماری dependencies `app/dependencies.py` پر ایک فائل میں ہیں۔

یاد رکھیں ہماری app/فائل کی ساخت کیسی ہے:

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

---

دو ڈاٹ `..`، جیسے:

```Python
from ..dependencies import get_token_header
```

کا مطلب ہے:

* اسی package سے شروع کریں جس میں یہ module (فائل `app/routers/items.py`) موجود ہے (directory `app/routers/`)...
* parent package (directory `app/`) پر جائیں...
* اور وہاں، `dependencies` module تلاش کریں (فائل `app/dependencies.py`)...
* اور اس سے function `get_token_header` import کریں۔

یہ درست طریقے سے کام کرتا ہے! 🎉

---

اسی طرح، اگر ہم تین ڈاٹ `...` استعمال کرتے، جیسے:

```Python
from ...dependencies import get_token_header
```

تو اس کا مطلب ہوتا:

* اسی package سے شروع کریں جس میں یہ module (فائل `app/routers/items.py`) موجود ہے (directory `app/routers/`)...
* parent package (directory `app/`) پر جائیں...
* پھر اس package کے parent پر جائیں (کوئی parent package نہیں ہے، `app` سب سے اوپر کی سطح ہے 😱)...
* اور وہاں، `dependencies` module تلاش کریں (فائل `app/dependencies.py`)...
* اور اس سے function `get_token_header` import کریں۔

یہ `app/` سے اوپر کسی package سے مراد ہوگا، جس کی اپنی `__init__.py` فائل ہو، وغیرہ۔ لیکن ہمارے پاس ایسا نہیں ہے۔ تو، یہ ہماری مثال میں error دے گا۔ 🚨

لیکن اب آپ جانتے ہیں کہ یہ کیسے کام کرتا ہے، تو آپ اپنی apps میں relative imports استعمال کر سکتے ہیں چاہے وہ کتنی بھی پیچیدہ ہوں۔ 🤓

### کچھ custom `tags`، `responses`، اور `dependencies` شامل کریں { #add-some-custom-tags-responses-and-dependencies }

ہم ہر *path operation* میں `/items` prefix یا `tags=["items"]` شامل نہیں کر رہے ہیں کیونکہ ہم نے انہیں `APIRouter` میں شامل کر دیا ہے۔

لیکن ہم پھر بھی _مزید_ `tags` شامل کر سکتے ہیں جو کسی مخصوص *path operation* پر لاگو ہوں گے، اور اس *path operation* کے لیے مخصوص کچھ اضافی `responses` بھی:

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[30:31] title["app/routers/items.py"] *}

/// tip | مشورہ

اس آخری path operation میں tags کا مجموعہ ہوگا: `["items", "custom"]`۔

اور documentation میں اس کے دونوں responses ہوں گے، ایک `404` کے لیے اور ایک `403` کے لیے۔

///

## مرکزی `FastAPI` { #the-main-fastapi }

اب، آئیں `app/main.py` module دیکھتے ہیں۔

یہاں آپ `FastAPI` class import اور استعمال کرتے ہیں۔

یہ آپ کی application کی مرکزی فائل ہوگی جو سب کچھ جوڑتی ہے۔

اور چونکہ آپ کی زیادہ تر logic اب اپنے مخصوص module میں ہوگی، مرکزی فائل کافی سادہ ہوگی۔

### `FastAPI` import کریں { #import-fastapi }

آپ `FastAPI` class کو عام طریقے سے import اور بنائیں۔

اور ہم [global dependencies](dependencies/global-dependencies.md) بھی declare کر سکتے ہیں جو ہر `APIRouter` کی dependencies کے ساتھ مل جائیں گی:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[1,3,7] title["app/main.py"] *}

### `APIRouter` import کریں { #import-the-apirouter }

اب ہم دوسرے submodules import کرتے ہیں جن میں `APIRouter`s ہیں:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[4:5] title["app/main.py"] *}

چونکہ فائلیں `app/routers/users.py` اور `app/routers/items.py` submodules ہیں جو اسی Python package `app` کا حصہ ہیں، ہم ایک واحد ڈاٹ `.` سے "relative imports" استعمال کرتے ہوئے انہیں import کر سکتے ہیں۔

### Import کیسے کام کرتا ہے { #how-the-importing-works }

یہ سیکشن:

```Python
from .routers import items, users
```

کا مطلب ہے:

* اسی package سے شروع کریں جس میں یہ module (فائل `app/main.py`) موجود ہے (directory `app/`)...
* subpackage `routers` تلاش کریں (directory `app/routers/`)...
* اور اس سے submodule `items` (فائل `app/routers/items.py`) اور `users` (فائل `app/routers/users.py`) import کریں...

Module `items` میں ایک variable `router` ہوگا (`items.router`)۔ یہ وہی ہے جو ہم نے فائل `app/routers/items.py` میں بنایا تھا، یہ ایک `APIRouter` object ہے۔

اور پھر ہم module `users` کے لیے بھی ایسا ہی کرتے ہیں۔

ہم انہیں اس طرح بھی import کر سکتے تھے:

```Python
from app.routers import items, users
```

/// info | معلومات

پہلا ورژن "relative import" ہے:

```Python
from .routers import items, users
```

دوسرا ورژن "absolute import" ہے:

```Python
from app.routers import items, users
```

Python Packages اور Modules کے بارے میں مزید جاننے کے لیے [Modules کے بارے میں سرکاری Python دستاویزات](https://docs.python.org/3/tutorial/modules.html) پڑھیں۔

///

### نام کے ٹکراؤ سے بچیں { #avoid-name-collisions }

ہم صرف اس کا variable `router` import کرنے کی بجائے submodule `items` کو براہ راست import کر رہے ہیں۔

اس کی وجہ یہ ہے کہ ہمارے پاس submodule `users` میں بھی `router` نام کا ایک اور variable ہے۔

اگر ہم ایک کے بعد دوسرا import کرتے، جیسے:

```Python
from .routers.items import router
from .routers.users import router
```

تو `users` کا `router` `items` والے کو overwrite کر دیتا اور ہم دونوں کو ایک ساتھ استعمال نہ کر پاتے۔

تو، دونوں کو ایک ہی فائل میں استعمال کرنے کے لیے، ہم submodules کو براہ راست import کرتے ہیں:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[5] title["app/main.py"] *}

### `users` اور `items` کے `APIRouter`s شامل کریں { #include-the-apirouters-for-users-and-items }

اب، آئیں submodules `users` اور `items` سے `router`s شامل کرتے ہیں:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[10:11] title["app/main.py"] *}

/// info | معلومات

`users.router` فائل `app/routers/users.py` کے اندر `APIRouter` پر مشتمل ہے۔

اور `items.router` فائل `app/routers/items.py` کے اندر `APIRouter` پر مشتمل ہے۔

///

`app.include_router()` کے ذریعے ہم ہر `APIRouter` کو مرکزی `FastAPI` application میں شامل کر سکتے ہیں۔

یہ اس router کے تمام routes کو اس کے حصے کے طور پر شامل کرے گا۔

/// note | تکنیکی تفصیلات

یہ دراصل اندرونی طور پر `APIRouter` میں declare کیے گئے ہر *path operation* کے لیے ایک *path operation* بنائے گا۔

تو، پردے کے پیچھے، یہ دراصل ایسے کام کرے گا جیسے سب کچھ ایک ہی واحد app ہو۔

///

/// check

آپ کو routers شامل کرتے وقت performance کی فکر کرنے کی ضرورت نہیں۔

اس میں microseconds لگیں گے اور یہ صرف startup پر ہوگا۔

تو اس سے performance متاثر نہیں ہوگی۔ ⚡

///

### Custom `prefix`، `tags`، `responses`، اور `dependencies` کے ساتھ `APIRouter` شامل کریں { #include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies }

اب، تصور کریں آپ کی تنظیم نے آپ کو `app/internal/admin.py` فائل دی ہے۔

اس میں کچھ admin *path operations* والا ایک `APIRouter` ہے جو آپ کی تنظیم کئی projects میں share کرتی ہے۔

اس مثال کے لیے یہ بہت سادہ ہوگا۔ لیکن فرض کریں کہ چونکہ یہ تنظیم کے دوسرے projects کے ساتھ share ہوتا ہے، ہم اسے تبدیل نہیں کر سکتے اور براہ راست `APIRouter` میں `prefix`، `dependencies`، `tags` وغیرہ شامل نہیں کر سکتے:

{* ../../docs_src/bigger_applications/app_an_py310/internal/admin.py hl[3] title["app/internal/admin.py"] *}

لیکن ہم پھر بھی `APIRouter` شامل کرتے وقت custom `prefix` سیٹ کرنا چاہتے ہیں تاکہ اس کے تمام *path operations* `/admin` سے شروع ہوں، ہم اسے اس project کے لیے پہلے سے موجود `dependencies` سے محفوظ بنانا چاہتے ہیں، اور ہم `tags` اور `responses` شامل کرنا چاہتے ہیں۔

ہم اصل `APIRouter` کو تبدیل کیے بغیر یہ سب declare کر سکتے ہیں ان parameters کو `app.include_router()` میں منتقل کر کے:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[14:17] title["app/main.py"] *}

اس طرح، اصل `APIRouter` غیر تبدیل شدہ رہے گا، تو ہم اب بھی وہی `app/internal/admin.py` فائل تنظیم کے دوسرے projects کے ساتھ share کر سکتے ہیں۔

نتیجہ یہ ہے کہ ہماری app میں، `admin` module کے ہر *path operation* میں ہوگا:

* `/admin` prefix۔
* `admin` tag۔
* `get_token_header` dependency۔
* `418` response۔ 🍵

لیکن یہ صرف ہماری app میں اس `APIRouter` پر اثر ڈالے گا، کسی دوسرے code پر نہیں جو اسے استعمال کرتا ہو۔

تو، مثال کے طور پر، دوسرے projects اسی `APIRouter` کو مختلف authentication method کے ساتھ استعمال کر سکتے ہیں۔

### ایک *path operation* شامل کریں { #include-a-path-operation }

ہم براہ راست `FastAPI` app میں بھی *path operations* شامل کر سکتے ہیں۔

یہاں ہم ایسا کرتے ہیں... صرف یہ دکھانے کے لیے کہ ہم کر سکتے ہیں 🤷:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[21:23] title["app/main.py"] *}

اور یہ درست طریقے سے کام کرے گا، `app.include_router()` کے ذریعے شامل کیے گئے تمام دوسرے *path operations* کے ساتھ مل کر۔

/// info | انتہائی تکنیکی تفصیلات

**نوٹ**: یہ ایک انتہائی تکنیکی تفصیل ہے جسے آپ شاید **چھوڑ سکتے ہیں**۔

---

`APIRouter`s "mount" نہیں ہوتے، وہ باقی application سے الگ نہیں ہوتے۔

اس کی وجہ یہ ہے کہ ہم ان کے *path operations* کو OpenAPI schema اور user interfaces میں شامل کرنا چاہتے ہیں۔

چونکہ ہم انہیں صرف الگ کر کے باقی سے آزادانہ طور پر "mount" نہیں کر سکتے، *path operations* "clone" کیے جاتے ہیں (دوبارہ بنائے جاتے ہیں)، براہ راست شامل نہیں کیے جاتے۔

///

## `pyproject.toml` میں `entrypoint` configure کریں { #configure-the-entrypoint-in-pyproject-toml }

چونکہ آپ کا FastAPI `app` object `app/main.py` میں ہے، آپ اپنی `pyproject.toml` فائل میں `entrypoint` اس طرح configure کر سکتے ہیں:

```toml
[tool.fastapi]
entrypoint = "app.main:app"
```

جو اس طرح import کرنے کے مساوی ہے:

```python
from app.main import app
```

اس طرح `fastapi` command کو پتہ چلے گا کہ آپ کی app کہاں ملے گی۔

/// Note

آپ command میں path بھی دے سکتے ہیں، جیسے:

```console
$ fastapi dev app/main.py
```

لیکن آپ کو ہر بار `fastapi` command چلاتے وقت درست path یاد رکھنا ہوگا۔

اس کے علاوہ، دوسرے tools شاید اسے نہ ڈھونڈ سکیں، مثلاً [VS Code Extension](../editor-support.md) یا [FastAPI Cloud](https://fastapicloud.com)، تو `pyproject.toml` میں `entrypoint` استعمال کرنا تجویز کیا جاتا ہے۔

///

## خودکار API docs چیک کریں { #check-the-automatic-api-docs }

اب، اپنی app چلائیں:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

اور [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) پر docs کھولیں۔

آپ خودکار API docs دیکھیں گے، جن میں تمام submodules کے paths شامل ہیں، درست paths (اور prefixes) اور درست tags کے ساتھ:

<img src="/img/tutorial/bigger-applications/image01.png">

## مختلف `prefix` کے ساتھ وہی router کئی بار شامل کریں { #include-the-same-router-multiple-times-with-different-prefix }

آپ مختلف prefixes استعمال کرتے ہوئے *ایک ہی* router کے ساتھ `.include_router()` کئی بار بھی استعمال کر سکتے ہیں۔

یہ مفید ہو سکتا ہے، مثلاً، ایک ہی API کو مختلف prefixes پر expose کرنے کے لیے، جیسے `/api/v1` اور `/api/latest`۔

یہ ایک جدید استعمال ہے جس کی آپ کو شاید واقعی ضرورت نہ ہو، لیکن ضرورت پڑنے پر یہ موجود ہے۔

## ایک `APIRouter` کو دوسرے میں شامل کریں { #include-an-apirouter-in-another }

بالکل اسی طرح جیسے آپ `FastAPI` application میں ایک `APIRouter` شامل کر سکتے ہیں، آپ ایک `APIRouter` کو دوسرے `APIRouter` میں شامل کر سکتے ہیں:

```Python
router.include_router(other_router)
```

یقینی بنائیں کہ آپ یہ `router` کو `FastAPI` app میں شامل کرنے سے پہلے کریں، تاکہ `other_router` کے *path operations* بھی شامل ہوں۔
