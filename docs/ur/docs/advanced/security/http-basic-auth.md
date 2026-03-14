# HTTP Basic Auth { #http-basic-auth }

سب سے سادہ صورتوں کے لیے، آپ HTTP Basic Auth استعمال کر سکتے ہیں۔

HTTP Basic Auth میں، ایپلیکیشن ایک ایسا header توقع کرتی ہے جس میں username اور password ہو۔

اگر اسے یہ نہیں ملتا، تو یہ HTTP 401 "Unauthorized" error واپس کرتی ہے۔

اور `WWW-Authenticate` header واپس کرتی ہے جس کی قدر `Basic` ہوتی ہے، اور ایک اختیاری `realm` parameter۔

اس سے browser کو username اور password کے لیے پہلے سے موجود prompt دکھانے کا اشارہ ملتا ہے۔

پھر جب آپ وہ username اور password ٹائپ کرتے ہیں، تو browser انہیں خودکار طور پر header میں بھیجتا ہے۔

## سادہ HTTP Basic Auth { #simple-http-basic-auth }

* `HTTPBasic` اور `HTTPBasicCredentials` import کریں۔
* `HTTPBasic` استعمال کر کے ایک "`security` scheme" بنائیں۔
* اس `security` کو اپنے *path operation* میں dependency کے ساتھ استعمال کریں۔
* یہ `HTTPBasicCredentials` قسم کا ایک object واپس کرتا ہے:
    * اس میں بھیجے گئے `username` اور `password` ہوتے ہیں۔

{* ../../docs_src/security/tutorial006_an_py310.py hl[4,8,12] *}

جب آپ پہلی بار URL کھولنے کی کوشش کریں گے (یا docs میں "Execute" بٹن پر کلک کریں گے) تو browser آپ سے username اور password پوچھے گا:

<img src="/img/tutorial/security/image12.png">

## Username چیک کریں { #check-the-username }

یہاں ایک زیادہ مکمل مثال ہے۔

username اور password درست ہیں یا نہیں یہ چیک کرنے کے لیے dependency استعمال کریں۔

اس کے لیے Python کا معیاری module [`secrets`](https://docs.python.org/3/library/secrets.html) استعمال کریں تاکہ username اور password چیک کیے جا سکیں۔

`secrets.compare_digest()` کو `bytes` یا ایسی `str` لینی ہوتی ہے جس میں صرف ASCII حروف ہوں (انگریزی والے)، اس کا مطلب ہے کہ یہ `á` جیسے حروف کے ساتھ کام نہیں کرے گا، جیسے `Sebastián` میں۔

اسے سنبھالنے کے لیے، ہم پہلے `username` اور `password` کو UTF-8 سے encode کر کے `bytes` میں تبدیل کرتے ہیں۔

پھر ہم `secrets.compare_digest()` استعمال کر سکتے ہیں تاکہ یقینی بنایا جا سکے کہ `credentials.username` `"stanleyjobson"` ہے، اور `credentials.password` `"swordfish"` ہے۔

{* ../../docs_src/security/tutorial007_an_py310.py hl[1,12:24] *}

یہ اس کے مشابہ ہوگا:

```Python
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # Return some error
    ...
```

لیکن `secrets.compare_digest()` استعمال کرنے سے یہ "timing attacks" نامی حملوں سے محفوظ رہے گا۔

### Timing Attacks { #timing-attacks }

لیکن "timing attack" کیا ہے؟

تصور کریں کہ کچھ حملہ آور username اور password کا اندازہ لگانے کی کوشش کر رہے ہیں۔

اور وہ username `johndoe` اور password `love123` کے ساتھ ایک request بھیجتے ہیں۔

پھر آپ کی ایپلیکیشن میں Python کوڈ کچھ اس طرح ہوگا:

```Python
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

لیکن جس لمحے Python `johndoe` کے پہلے `j` کا `stanleyjobson` کے پہلے `s` سے موازنہ کرتا ہے، یہ `False` واپس کر دے گا، کیونکہ اسے پہلے سے معلوم ہو جاتا ہے کہ یہ دونوں strings ایک جیسی نہیں ہیں، یہ سوچتے ہوئے کہ "باقی حروف کا موازنہ کرنے میں مزید وقت ضائع کرنے کی ضرورت نہیں"۔ اور آپ کی ایپلیکیشن کہے گی "غلط username یا password"۔

لیکن پھر حملہ آور username `stanleyjobsox` اور password `love123` کے ساتھ کوشش کرتے ہیں۔

اور آپ کی ایپلیکیشن کا کوڈ کچھ ایسا کرتا ہے:

```Python
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Python کو `stanleyjobsox` اور `stanleyjobson` دونوں میں پورا `stanleyjobso` موازنہ کرنا ہوگا اس سے پہلے کہ اسے پتا چلے کہ دونوں strings ایک جیسی نہیں ہیں۔ تو "غلط username یا password" جواب دینے میں کچھ اضافی مائیکرو سیکنڈز لگیں گے۔

#### جواب دینے کا وقت حملہ آوروں کی مدد کرتا ہے { #the-time-to-answer-helps-the-attackers }

اس مقام پر، یہ دیکھ کر کہ server نے "غلط username یا password" جواب بھیجنے میں کچھ مائیکرو سیکنڈز زیادہ لگائے، حملہ آوروں کو معلوم ہو جائے گا کہ انہوں نے _کچھ_ درست کیا، ابتدائی حروف میں سے کچھ صحیح تھے۔

اور پھر وہ دوبارہ کوشش کر سکتے ہیں یہ جانتے ہوئے کہ یہ شاید `johndoe` سے زیادہ `stanleyjobsox` سے ملتا جلتا ہے۔

#### ایک "پیشہ ورانہ" حملہ { #a-professional-attack }

یقیناً، حملہ آور یہ سب ہاتھ سے نہیں کریں گے، وہ ایک پروگرام لکھیں گے جو ممکنہ طور پر فی سیکنڈ ہزاروں یا لاکھوں ٹیسٹ کرے۔ اور وہ ایک وقت میں صرف ایک اضافی درست حرف حاصل کریں گے۔

لیکن ایسا کرنے سے، کچھ منٹوں یا گھنٹوں میں حملہ آوروں نے ہماری ایپلیکیشن کی "مدد" سے، صرف جواب دینے کا وقت استعمال کر کے، صحیح username اور password کا اندازہ لگا لیا ہوگا۔

#### `secrets.compare_digest()` سے ٹھیک کریں { #fix-it-with-secrets-compare-digest }

لیکن ہمارے کوڈ میں ہم دراصل `secrets.compare_digest()` استعمال کر رہے ہیں۔

مختصراً، `stanleyjobsox` کا `stanleyjobson` سے موازنہ کرنے میں اتنا ہی وقت لگے گا جتنا `johndoe` کا `stanleyjobson` سے موازنہ میں لگتا ہے۔ اور password کے لیے بھی ایسا ہی ہے۔

اس طرح، اپنی ایپلیکیشن کے کوڈ میں `secrets.compare_digest()` استعمال کرنے سے، یہ security حملوں کی اس پوری قسم سے محفوظ رہے گا۔

### Error واپس کریں { #return-the-error }

credentials غلط ہونے کا پتا لگنے کے بعد، status code 401 کے ساتھ ایک `HTTPException` واپس کریں (وہی جو credentials فراہم نہ ہونے پر واپس آتا ہے) اور `WWW-Authenticate` header شامل کریں تاکہ browser دوبارہ login prompt دکھائے:

{* ../../docs_src/security/tutorial007_an_py310.py hl[26:30] *}
