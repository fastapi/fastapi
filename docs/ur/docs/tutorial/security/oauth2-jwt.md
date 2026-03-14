# Password (اور hashing) کے ساتھ OAuth2، JWT tokens کے ساتھ Bearer { #oauth2-with-password-and-hashing-bearer-with-jwt-tokens }

اب جبکہ ہمارے پاس پورا security flow ہے، آئیے <abbr title="JSON Web Tokens">JWT</abbr> tokens اور محفوظ password hashing استعمال کرکے application کو حقیقتاً محفوظ بنائیں۔

یہ code وہ ہے جو آپ حقیقت میں اپنی application میں استعمال کر سکتے ہیں، password hashes اپنے database میں محفوظ کر سکتے ہیں، وغیرہ۔

ہم وہاں سے شروع کریں گے جہاں ہم نے پچھلے باب میں چھوڑا تھا اور اسے بڑھائیں گے۔

## JWT کے بارے میں { #about-jwt }

JWT کا مطلب ہے "JSON Web Tokens"۔

یہ ایک JSON object کو ایک لمبی گھنی string میں بغیر خالی جگہوں کے encode کرنے کا معیار ہے۔ یہ کچھ ایسا دکھتا ہے:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

یہ encrypted نہیں ہے، تو کوئی بھی مواد سے معلومات حاصل کر سکتا ہے۔

لیکن یہ signed ہے۔ تو، جب آپ کو وہ token ملے جو آپ نے جاری کیا تھا، آپ تصدیق کر سکتے ہیں کہ آپ نے واقعی اسے جاری کیا تھا۔

اس طرح، آپ مثلاً 1 ہفتے کی expiration کے ساتھ token بنا سکتے ہیں۔ اور پھر جب صارف اگلے دن token کے ساتھ واپس آئے، تو آپ جانتے ہیں کہ وہ صارف ابھی بھی آپ کے system میں logged in ہے۔

ایک ہفتے کے بعد، token expire ہو جائے گا اور صارف authorized نہیں ہوگا اور اسے نیا token حاصل کرنے کے لیے دوبارہ sign in کرنا ہوگا۔ اور اگر صارف (یا کسی third party) نے expiration تبدیل کرنے کے لیے token میں ترمیم کرنے کی کوشش کی، تو آپ اسے دریافت کر سکیں گے، کیونکہ signatures میل نہیں کھائیں گے۔

اگر آپ JWT tokens کے ساتھ کھیلنا اور دیکھنا چاہتے ہیں کہ یہ کیسے کام کرتے ہیں، تو [https://jwt.io](https://jwt.io/) دیکھیں۔

## `PyJWT` install کریں { #install-pyjwt }

ہمیں Python میں JWT tokens بنانے اور تصدیق کرنے کے لیے `PyJWT` install کرنا ہوگا۔

یقینی بنائیں کہ آپ ایک [virtual environment](../../virtual-environments.md) بنائیں، اسے activate کریں، اور پھر `pyjwt` install کریں:

<div class="termy">

```console
$ pip install pyjwt

---> 100%
```

</div>

/// info | معلومات

اگر آپ RSA یا ECDSA جیسے digital signature algorithms استعمال کرنے کا ارادہ رکھتے ہیں، تو آپ کو cryptography library dependency `pyjwt[crypto]` install کرنی چاہیے۔

آپ اس کے بارے میں مزید [PyJWT Installation docs](https://pyjwt.readthedocs.io/en/latest/installation.html) میں پڑھ سکتے ہیں۔

///

## Password hashing { #password-hashing }

"Hashing" کا مطلب ہے کسی مواد (اس معاملے میں password) کو bytes کی ایک ترتیب (بس ایک string) میں تبدیل کرنا جو بے معنی سی لگتی ہے۔

جب بھی آپ بالکل وہی مواد (بالکل وہی password) دیں گے، آپ کو بالکل وہی بے معنی نتیجہ ملے گا۔

لیکن آپ اس بے معنی نتیجے سے واپس password حاصل نہیں کر سکتے۔

### Password hashing کیوں استعمال کریں { #why-use-password-hashing }

اگر آپ کا database چوری ہو جائے، تو چور کے پاس آپ کے صارفین کے سادہ متن کے passwords نہیں ہوں گے، صرف hashes ہوں گے۔

تو، چور اس password کو کسی اور system میں استعمال نہیں کر سکے گا (چونکہ بہت سے صارف ہر جگہ ایک ہی password استعمال کرتے ہیں، یہ خطرناک ہوتا)۔

## `pwdlib` install کریں { #install-pwdlib }

pwdlib password hashes کو سنبھالنے کے لیے ایک بہترین Python package ہے۔

یہ بہت سے محفوظ hashing algorithms اور ان کے ساتھ کام کرنے کی utilities کو سپورٹ کرتا ہے۔

تجویز کردہ algorithm "Argon2" ہے۔

یقینی بنائیں کہ آپ ایک [virtual environment](../../virtual-environments.md) بنائیں، اسے activate کریں، اور پھر Argon2 کے ساتھ pwdlib install کریں:

<div class="termy">

```console
$ pip install "pwdlib[argon2]"

---> 100%
```

</div>

/// tip | مشورہ

`pwdlib` کے ساتھ، آپ اسے **Django**، **Flask** security plug-in یا بہت سے دوسروں کی طرف سے بنائے گئے passwords پڑھنے کے قابل بھی بنا سکتے ہیں۔

تو، آپ مثال کے طور پر Django application سے database میں وہی data FastAPI application کے ساتھ شیئر کر سکتے ہیں۔ یا آسانی سے Django application کو اسی database کا استعمال کرتے ہوئے منتقل کر سکتے ہیں۔

اور آپ کے صارف آپ کی Django app یا آپ کی **FastAPI** app سے بیک وقت login کر سکیں گے۔

///

## Passwords کو hash اور verify کریں { #hash-and-verify-the-passwords }

`pwdlib` سے درکار tools import کریں۔

تجویز کردہ settings کے ساتھ ایک PasswordHash instance بنائیں - یہ passwords کو hash اور verify کرنے کے لیے استعمال ہوگا۔

/// tip | مشورہ

pwdlib bcrypt hashing algorithm کو بھی سپورٹ کرتا ہے لیکن legacy algorithms شامل نہیں کرتا - پرانے hashes کے ساتھ کام کرنے کے لیے passlib library استعمال کرنے کی سفارش کی جاتی ہے۔

مثال کے طور پر، آپ اسے کسی اور system (جیسے Django) کی طرف سے بنائے گئے passwords پڑھنے اور verify کرنے کے لیے استعمال کر سکتے ہیں لیکن نئے passwords کو Argon2 یا Bcrypt جیسے مختلف algorithm سے hash کر سکتے ہیں۔

اور ان سب کے ساتھ بیک وقت مطابقت پذیر رہ سکتے ہیں۔

///

صارف سے آنے والے password کو hash کرنے کے لیے ایک utility function بنائیں۔

اور ایک اور موصول ہونے والے password کی تصدیق کرنے کے لیے کہ آیا یہ محفوظ hash سے ملتا ہے۔

اور ایک اور صارف کو authenticate کرنے اور واپس کرنے کے لیے۔

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,51,58:59,62:63,72:79] *}

جب `authenticate_user` کو ایسے username کے ساتھ call کیا جاتا ہے جو database میں موجود نہیں ہے، تو ہم پھر بھی ایک dummy hash کے خلاف `verify_password` چلاتے ہیں۔

یہ اس بات کو یقینی بناتا ہے کہ endpoint کو جواب دینے میں تقریباً اتنا ہی وقت لگے چاہے username درست ہو یا نہ ہو، **timing attacks** کو روکتا ہے جو موجود usernames کی شناخت کے لیے استعمال ہو سکتے ہیں۔

/// note | نوٹ

اگر آپ نیا (جعلی) database `fake_users_db` چیک کریں، تو آپ دیکھیں گے کہ hashed password اب کیسا دکھتا ہے: `"$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"`۔

///

## JWT tokens کو سنبھالیں { #handle-jwt-tokens }

Install شدہ modules import کریں۔

ایک random secret key بنائیں جو JWT tokens پر sign کرنے کے لیے استعمال ہوگی۔

محفوظ random secret key بنانے کے لیے یہ command استعمال کریں:

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

اور output کو variable `SECRET_KEY` میں کاپی کریں (مثال والی key استعمال نہ کریں)۔

ایک variable `ALGORITHM` بنائیں جس میں JWT token پر sign کرنے کے لیے استعمال ہونے والا algorithm ہو اور اسے `"HS256"` پر سیٹ کریں۔

Token کی expiration کے لیے ایک variable بنائیں۔

ایک Pydantic Model بیان کریں جو token endpoint میں response کے لیے استعمال ہوگا۔

نیا access token بنانے کے لیے ایک utility function بنائیں۔

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,82:90] *}

## Dependencies کو اپ ڈیٹ کریں { #update-the-dependencies }

`get_current_user` کو اپ ڈیٹ کریں تاکہ پہلے کی طرح وہی token وصول کرے، لیکن اس بار JWT tokens استعمال کرتے ہوئے۔

موصول ہونے والے token کو decode کریں، اس کی تصدیق کریں، اور موجودہ صارف واپس کریں۔

اگر token غلط ہے، تو فوری طور پر HTTP error واپس کریں۔

{* ../../docs_src/security/tutorial004_an_py310.py hl[93:110] *}

## `/token` *path operation* کو اپ ڈیٹ کریں { #update-the-token-path-operation }

Token کی expiration وقت کے ساتھ ایک `timedelta` بنائیں۔

ایک حقیقی JWT access token بنائیں اور اسے واپس کریں۔

{* ../../docs_src/security/tutorial004_an_py310.py hl[121:136] *}

### JWT "subject" `sub` کے بارے میں تکنیکی تفصیلات { #technical-details-about-the-jwt-subject-sub }

JWT specification کہتی ہے کہ ایک key `sub` ہے، جس میں token کا subject ہوتا ہے۔

اسے استعمال کرنا اختیاری ہے، لیکن یہ وہ جگہ ہے جہاں آپ صارف کی شناخت رکھیں گے، اس لیے ہم اسے یہاں استعمال کر رہے ہیں۔

JWT صارف کی شناخت اور انہیں آپ کی API پر براہ راست operations انجام دینے کی اجازت دینے کے علاوہ دوسرے کاموں کے لیے بھی استعمال ہو سکتا ہے۔

مثال کے طور پر، آپ ایک "car" یا "blog post" کی شناخت کر سکتے ہیں۔

پھر آپ اس entity کے بارے میں permissions شامل کر سکتے ہیں، جیسے "drive" (car کے لیے) یا "edit" (blog post کے لیے)۔

اور پھر، آپ وہ JWT token کسی صارف (یا bot) کو دے سکتے ہیں، اور وہ ان actions کو انجام دینے کے لیے استعمال کر سکتے ہیں (car چلانا، یا blog post میں ترمیم کرنا) بغیر account رکھے، صرف اس JWT token کے ساتھ جو آپ کی API نے بنایا ہے۔

ان خیالات کا استعمال کرتے ہوئے، JWT بہت زیادہ نفیس منظرناموں کے لیے استعمال ہو سکتا ہے۔

ان معاملات میں، ان میں سے کئی entities کا ایک ہی ID ہو سکتا ہے، مثلاً `foo` (ایک صارف `foo`، ایک car `foo`، اور ایک blog post `foo`)۔

تو، ID کے ٹکراؤ سے بچنے کے لیے، JWT token بناتے وقت صارف کے لیے، آپ `sub` key کی value میں prefix لگا سکتے ہیں، مثلاً `username:` کے ساتھ۔ تو، اس مثال میں، `sub` کی value ہو سکتی تھی: `username:johndoe`۔

یاد رکھنے کی اہم بات یہ ہے کہ `sub` key کے پاس پوری application میں ایک منفرد شناخت کنندہ ہونا چاہیے، اور یہ ایک string ہونی چاہیے۔

## اسے چیک کریں { #check-it }

Server چلائیں اور docs پر جائیں: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)۔

آپ کو اس طرح کا user interface نظر آئے گا:

<img src="/img/tutorial/security/image07.png">

Application کو پہلے کی طرح authorize کریں۔

یہ credentials استعمال کریں:

Username: `johndoe`
Password: `secret`

/// check | اضافی معلومات

دھیان دیں کہ code میں کہیں بھی سادہ متن کا password "`secret`" نہیں ہے، ہمارے پاس صرف hashed version ہے۔

///

<img src="/img/tutorial/security/image08.png">

Endpoint `/users/me/` call کریں، آپ کو یہ response ملے گا:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

اگر آپ developer tools کھولیں، تو آپ دیکھ سکتے ہیں کہ بھیجا گیا data صرف token پر مشتمل ہے، password صرف پہلی request میں بھیجا جاتا ہے تاکہ صارف کو authenticate کیا جائے اور وہ access token حاصل کیا جائے، لیکن اس کے بعد نہیں:

<img src="/img/tutorial/security/image10.png">

/// note | نوٹ

`Authorization` header کو دیکھیں، جس کی value `Bearer ` سے شروع ہوتی ہے۔

///

## `scopes` کے ساتھ جدید استعمال { #advanced-usage-with-scopes }

OAuth2 میں "scopes" کا تصور ہے۔

آپ انہیں JWT token میں permissions کا ایک مخصوص مجموعہ شامل کرنے کے لیے استعمال کر سکتے ہیں۔

پھر آپ یہ token کسی صارف کو براہ راست یا کسی third party کو دے سکتے ہیں، تاکہ وہ آپ کی API کے ساتھ پابندیوں کے ایک مجموعے کے ساتھ تعامل کر سکے۔

آپ **Advanced User Guide** میں بعد میں سیکھ سکتے ہیں کہ انہیں کیسے استعمال کریں اور یہ **FastAPI** میں کیسے integrated ہیں۔

## خلاصہ { #recap }

جو آپ نے اب تک دیکھا ہے اس سے، آپ OAuth2 اور JWT جیسے معیارات کا استعمال کرتے ہوئے ایک محفوظ **FastAPI** application ترتیب دے سکتے ہیں۔

تقریباً ہر framework میں security کو سنبھالنا بہت جلد ایک پیچیدہ موضوع بن جاتا ہے۔

بہت سے packages جو اسے بہت آسان بناتے ہیں انہیں data model، database، اور دستیاب features کے ساتھ بہت سے سمجھوتے کرنے پڑتے ہیں۔ اور ان میں سے کچھ packages جو چیزوں کو بہت زیادہ آسان بنا دیتے ہیں ان میں حقیقت میں اندرونی طور پر security کی خامیاں ہوتی ہیں۔

---

**FastAPI** کسی بھی database، data model یا tool کے ساتھ کوئی سمجھوتا نہیں کرتا۔

یہ آپ کو پوری لچک دیتا ہے کہ آپ وہ چنیں جو آپ کے پروجیکٹ کے لیے بہترین ہوں۔

اور آپ بہت سے اچھی طرح سے برقرار رکھے جانے والے اور وسیع پیمانے پر استعمال ہونے والے packages جیسے `pwdlib` اور `PyJWT` براہ راست استعمال کر سکتے ہیں، کیونکہ **FastAPI** بیرونی packages کو integrate کرنے کے لیے کسی پیچیدہ طریقہ کار کی ضرورت نہیں رکھتا۔

لیکن یہ آپ کو لچک، مضبوطی، یا security سے سمجھوتہ کیے بغیر عمل کو زیادہ سے زیادہ آسان بنانے کے tools فراہم کرتا ہے۔

اور آپ OAuth2 جیسے محفوظ، معیاری protocols کو نسبتاً آسان طریقے سے استعمال اور implement کر سکتے ہیں۔

آپ **Advanced User Guide** میں مزید سیکھ سکتے ہیں کہ OAuth2 "scopes" کو کیسے استعمال کریں، مزید باریک بینی سے permissions کے نظام کے لیے، انہی معیارات کی پیروی کرتے ہوئے۔ OAuth2 with scopes وہ طریقہ کار ہے جو بہت سے بڑے authentication providers، جیسے Facebook، Google، GitHub، Microsoft، X (Twitter) وغیرہ، اپنے صارفین کی جانب سے third party applications کو اپنی APIs کے ساتھ تعامل کرنے کی اجازت دینے کے لیے استعمال کرتے ہیں۔
