# Security - پہلے قدم { #security-first-steps }

آئیے تصور کریں کہ آپ کی **backend** API کسی domain پر ہے۔

اور آپ کا **frontend** کسی اور domain پر یا اسی domain کے کسی مختلف path پر ہے (یا کسی mobile application میں)۔

اور آپ چاہتے ہیں کہ frontend، backend کے ساتھ **username** اور **password** استعمال کرتے ہوئے authenticate کر سکے۔

ہم **FastAPI** کے ساتھ **OAuth2** استعمال کرکے یہ بنا سکتے ہیں۔

لیکن آئیے آپ کا وقت بچاتے ہیں کہ آپ کو پوری لمبی specification پڑھنے کی ضرورت نہ پڑے صرف ان چھوٹی سی معلومات کے لیے جو آپ کو چاہئیں۔

آئیے **FastAPI** کی طرف سے فراہم کردہ tools استعمال کرتے ہیں security کو سنبھالنے کے لیے۔

## یہ کیسا دکھتا ہے { #how-it-looks }

آئیے پہلے صرف code استعمال کریں اور دیکھیں کہ یہ کیسے کام کرتا ہے، اور پھر ہم واپس آ کر سمجھیں گے کہ کیا ہو رہا ہے۔

## `main.py` بنائیں { #create-main-py }

مثال کو ایک فائل `main.py` میں کاپی کریں:

{* ../../docs_src/security/tutorial001_an_py310.py *}

## اسے چلائیں { #run-it }

/// info | معلومات

[`python-multipart`](https://github.com/Kludex/python-multipart) package خودکار طور پر **FastAPI** کے ساتھ install ہو جاتا ہے جب آپ `pip install "fastapi[standard]"` command چلاتے ہیں۔

تاہم، اگر آپ `pip install fastapi` command استعمال کرتے ہیں، تو `python-multipart` package بطور default شامل نہیں ہوتا۔

اسے دستی طور پر install کرنے کے لیے، یقینی بنائیں کہ آپ ایک [virtual environment](../../virtual-environments.md) بنائیں، اسے activate کریں، اور پھر اسے install کریں:

```console
$ pip install python-multipart
```

یہ اس لیے ہے کیونکہ **OAuth2** `username` اور `password` بھیجنے کے لیے "form data" استعمال کرتا ہے۔

///

مثال کو اس طرح چلائیں:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## اسے چیک کریں { #check-it }

Interactive docs پر جائیں: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)۔

آپ کو کچھ ایسا نظر آئے گا:

<img src="/img/tutorial/security/image01.png">

/// check | Authorize بٹن!

آپ کے پاس پہلے سے ایک چمکدار نیا "Authorize" بٹن ہے۔

اور آپ کے *path operation* میں اوپر دائیں کونے میں ایک چھوٹا سا تالے کا نشان ہے جس پر آپ کلک کر سکتے ہیں۔

///

اور اگر آپ اس پر کلک کریں، تو آپ کو ایک چھوٹا سا authorization فارم ملے گا جس میں `username` اور `password` (اور دیگر اختیاری فیلڈز) ٹائپ کر سکتے ہیں:

<img src="/img/tutorial/security/image02.png">

/// note | نوٹ

اس سے کوئی فرق نہیں پڑتا کہ آپ فارم میں کیا ٹائپ کریں، یہ ابھی کام نہیں کرے گا۔ لیکن ہم وہاں پہنچ جائیں گے۔

///

یہ یقیناً حتمی صارفین کے لیے frontend نہیں ہے، لیکن یہ آپ کی پوری API کو interactively document کرنے کے لیے ایک بہترین خودکار tool ہے۔

یہ frontend ٹیم استعمال کر سکتی ہے (جو آپ خود بھی ہو سکتے ہیں)۔

یہ third party applications اور systems استعمال کر سکتے ہیں۔

اور آپ خود بھی اسی application کو debug، check اور test کرنے کے لیے استعمال کر سکتے ہیں۔

## `password` flow { #the-password-flow }

اب آئیے تھوڑا پیچھے جائیں اور سمجھیں کہ یہ سب کیا ہے۔

`password` "flow" OAuth2 میں بیان کردہ security اور authentication کو سنبھالنے کے طریقوں ("flows") میں سے ایک ہے۔

OAuth2 اس طرح ڈیزائن کیا گیا تھا کہ backend یا API اس server سے آزاد ہو سکے جو صارف کو authenticate کرتا ہے۔

لیکن اس معاملے میں، وہی **FastAPI** application API اور authentication دونوں کو سنبھالے گی۔

تو، آئیے اسے اس آسان نقطہ نظر سے دیکھتے ہیں:

* صارف frontend میں `username` اور `password` ٹائپ کرتا ہے، اور `Enter` دباتا ہے۔
* Frontend (صارف کے browser میں چل رہا) وہ `username` اور `password` ہماری API میں ایک مخصوص URL پر بھیجتا ہے (جو `tokenUrl="token"` کے ساتھ declare کیا گیا ہے)۔
* API وہ `username` اور `password` چیک کرتی ہے، اور ایک "token" کے ساتھ جواب دیتی ہے (ہم نے ابھی تک اس میں سے کچھ بھی implement نہیں کیا)۔
    * ایک "token" بس ایک string ہے جس میں کچھ مواد ہوتا ہے جسے ہم بعد میں اس صارف کی تصدیق کے لیے استعمال کر سکتے ہیں۔
    * عام طور پر، ایک token کچھ وقت بعد expire ہونے کے لیے سیٹ کیا جاتا ہے۔
        * تو، صارف کو کسی وقت بعد دوبارہ login کرنا ہوگا۔
        * اور اگر token چوری ہو جائے، تو خطرہ کم ہے۔ یہ کسی مستقل key کی طرح نہیں جو ہمیشہ کام کرے (زیادہ تر معاملات میں)۔
* Frontend وہ token عارضی طور پر کہیں محفوظ کرتا ہے۔
* صارف frontend میں کلک کرتا ہے تاکہ frontend web app کے کسی اور سیکشن میں جائے۔
* Frontend کو API سے مزید data لانا ہوتا ہے۔
    * لیکن اسے اس مخصوص endpoint کے لیے authentication کی ضرورت ہوتی ہے۔
    * تو، ہماری API کے ساتھ authenticate کرنے کے لیے، یہ ایک header `Authorization` بھیجتا ہے جس کی value `Bearer ` ہوتی ہے اور اس کے ساتھ token ہوتا ہے۔
    * اگر token میں `foobar` ہو، تو `Authorization` header کا مواد ہوگا: `Bearer foobar`۔

## **FastAPI** کا `OAuth2PasswordBearer` { #fastapis-oauth2passwordbearer }

**FastAPI** مختلف سطحوں کی abstraction پر، ان security features کو implement کرنے کے لیے کئی tools فراہم کرتا ہے۔

اس مثال میں ہم **OAuth2** استعمال کریں گے، **Password** flow کے ساتھ، **Bearer** token استعمال کرتے ہوئے۔ ہم یہ `OAuth2PasswordBearer` class استعمال کرکے کرتے ہیں۔

/// info | معلومات

"bearer" token واحد آپشن نہیں ہے۔

لیکن ہمارے استعمال کے لیے یہ بہترین ہے۔

اور زیادہ تر استعمال کے معاملات کے لیے یہ بہترین ہو سکتا ہے، جب تک کہ آپ OAuth2 ماہر نہ ہوں اور آپ کو بالکل معلوم نہ ہو کہ کوئی اور آپشن آپ کی ضروریات کے لیے بہتر ہے۔

اس صورت میں، **FastAPI** آپ کو اسے بنانے کے tools بھی فراہم کرتا ہے۔

///

جب ہم `OAuth2PasswordBearer` class کی ایک instance بناتے ہیں تو ہم `tokenUrl` parameter پاس کرتے ہیں۔ یہ parameter وہ URL رکھتا ہے جو client (صارف کے browser میں چل رہا frontend) token حاصل کرنے کے لیے `username` اور `password` بھیجنے کے لیے استعمال کرے گا۔

{* ../../docs_src/security/tutorial001_an_py310.py hl[8] *}

/// tip | مشورہ

یہاں `tokenUrl="token"` ایک relative URL `token` کی طرف اشارہ کرتا ہے جو ہم نے ابھی بنایا نہیں ہے۔ چونکہ یہ ایک relative URL ہے، یہ `./token` کے مساوی ہے۔

کیونکہ ہم relative URL استعمال کر رہے ہیں، اگر آپ کی API `https://example.com/` پر تھی، تو یہ `https://example.com/token` کی طرف اشارہ کرے گا۔ لیکن اگر آپ کی API `https://example.com/api/v1/` پر تھی، تو یہ `https://example.com/api/v1/token` کی طرف اشارہ کرے گا۔

Relative URL استعمال کرنا اہم ہے تاکہ آپ کی application ایک جدید استعمال کے معاملے جیسے [Behind a Proxy](../../advanced/behind-a-proxy.md) میں بھی کام کرتی رہے۔

///

یہ parameter وہ endpoint / *path operation* نہیں بناتا، بلکہ یہ declare کرتا ہے کہ URL `/token` وہ ہوگا جو client کو token حاصل کرنے کے لیے استعمال کرنا چاہیے۔ یہ معلومات OpenAPI میں، اور پھر interactive API documentation systems میں استعمال ہوتی ہیں۔

ہم جلد ہی اصل path operation بھی بنائیں گے۔

/// info | معلومات

اگر آپ بہت سخت "Pythonista" ہیں تو آپ کو parameter کے نام `tokenUrl` کا انداز `token_url` کی بجائے ناپسند ہو سکتا ہے۔

یہ اس لیے ہے کیونکہ یہ وہی نام استعمال کر رہا ہے جو OpenAPI spec میں ہے۔ تاکہ اگر آپ کو ان میں سے کسی security scheme کے بارے میں مزید تحقیق کرنی ہو تو آپ اسے کاپی اور پیسٹ کرکے مزید معلومات حاصل کر سکیں۔

///

`oauth2_scheme` variable `OAuth2PasswordBearer` کی ایک instance ہے، لیکن یہ ایک "callable" بھی ہے۔

اسے اس طرح call کیا جا سکتا ہے:

```Python
oauth2_scheme(some, parameters)
```

تو، اسے `Depends` کے ساتھ استعمال کیا جا سکتا ہے۔

### اسے استعمال کریں { #use-it }

اب آپ اس `oauth2_scheme` کو `Depends` کے ساتھ ایک dependency میں پاس کر سکتے ہیں۔

{* ../../docs_src/security/tutorial001_an_py310.py hl[12] *}

یہ dependency ایک `str` فراہم کرے گی جو *path operation function* کے parameter `token` کو assign ہوگی۔

**FastAPI** کو معلوم ہوگا کہ وہ اس dependency کو OpenAPI schema (اور خودکار API docs) میں ایک "security scheme" کی تعریف کے لیے استعمال کر سکتا ہے۔

/// info | تکنیکی تفصیلات

**FastAPI** کو معلوم ہوگا کہ وہ class `OAuth2PasswordBearer` (جو ایک dependency میں declare کی گئی ہے) کو OpenAPI میں security scheme کی تعریف کے لیے استعمال کر سکتا ہے کیونکہ یہ `fastapi.security.oauth2.OAuth2` سے inherit ہوتی ہے، جو بدلے میں `fastapi.security.base.SecurityBase` سے inherit ہوتی ہے۔

تمام security utilities جو OpenAPI (اور خودکار API docs) کے ساتھ integrate ہوتی ہیں `SecurityBase` سے inherit ہوتی ہیں، اسی طرح **FastAPI** جانتا ہے کہ انہیں OpenAPI میں کیسے integrate کرنا ہے۔

///

## یہ کیا کرتا ہے { #what-it-does }

یہ request میں `Authorization` header تلاش کرے گا، چیک کرے گا کہ value `Bearer ` ہے اور اس کے ساتھ کوئی token ہے، اور token کو `str` کے طور پر واپس کرے گا۔

اگر اسے `Authorization` header نظر نہیں آتا، یا value میں `Bearer ` token نہیں ہے، تو یہ براہ راست 401 status code error (`UNAUTHORIZED`) کے ساتھ جواب دے گا۔

آپ کو یہ بھی چیک کرنے کی ضرورت نہیں کہ token موجود ہے یا نہیں تاکہ error واپس کریں۔ آپ یقین رکھ سکتے ہیں کہ اگر آپ کی function execute ہوتی ہے، تو اس token میں ایک `str` ہوگی۔

آپ اسے interactive docs میں ابھی آزما سکتے ہیں:

<img src="/img/tutorial/security/image03.png">

ہم ابھی تک token کی validity کی تصدیق نہیں کر رہے، لیکن یہ ایک شروعات ہے۔

## خلاصہ { #recap }

تو، صرف 3 یا 4 اضافی لائنوں میں، آپ کے پاس پہلے سے security کی ایک بنیادی شکل موجود ہے۔
