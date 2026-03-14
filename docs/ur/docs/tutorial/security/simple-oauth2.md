# Password اور Bearer کے ساتھ سادہ OAuth2 { #simple-oauth2-with-password-and-bearer }

اب آئیے پچھلے باب سے آگے بڑھتے ہیں اور مکمل security flow کے لیے باقی حصے شامل کرتے ہیں۔

## `username` اور `password` حاصل کریں { #get-the-username-and-password }

ہم `username` اور `password` حاصل کرنے کے لیے **FastAPI** security utilities استعمال کریں گے۔

OAuth2 متعین کرتا ہے کہ "password flow" (جو ہم استعمال کر رہے ہیں) استعمال کرتے وقت client/صارف کو `username` اور `password` فیلڈز بطور form data بھیجنے ہوں گے۔

اور spec کہتی ہے کہ فیلڈز کے نام بالکل ایسے ہی ہونے چاہئیں۔ تو `user-name` یا `email` کام نہیں کرے گا۔

لیکن فکر نہ کریں، آپ اسے frontend میں اپنے حتمی صارفین کو جیسے چاہیں دکھا سکتے ہیں۔

اور آپ کے database models جو بھی نام چاہیں استعمال کر سکتے ہیں۔

لیکن login *path operation* کے لیے، ہمیں spec کے مطابق ان ناموں کا استعمال کرنا ہوگا (اور مثال کے طور پر، integrated API documentation system استعمال کرنے کے قابل ہونا)۔

Spec یہ بھی کہتی ہے کہ `username` اور `password` بطور form data بھیجے جائیں (تو، یہاں JSON نہیں)۔

### `scope` { #scope }

Spec یہ بھی کہتی ہے کہ client ایک اور form field "`scope`" بھیج سکتا ہے۔

Form field کا نام `scope` (واحد) ہے، لیکن یہ حقیقت میں ایک لمبی string ہے جس میں "scopes" خالی جگہوں سے الگ ہوتے ہیں۔

ہر "scope" بس ایک string ہے (بغیر خالی جگہوں کے)۔

یہ عام طور پر مخصوص security permissions declare کرنے کے لیے استعمال ہوتے ہیں، مثال کے طور پر:

* `users:read` یا `users:write` عام مثالیں ہیں۔
* `instagram_basic` Facebook / Instagram استعمال کرتا ہے۔
* `https://www.googleapis.com/auth/drive` Google استعمال کرتا ہے۔

/// info | معلومات

OAuth2 میں ایک "scope" بس ایک string ہے جو ایک مخصوص مطلوبہ permission declare کرتی ہے۔

اس سے کوئی فرق نہیں پڑتا کہ اس میں `:` جیسے دوسرے حروف ہوں یا یہ ایک URL ہو۔

یہ تفصیلات implementation پر منحصر ہیں۔

OAuth2 کے لیے یہ بس strings ہیں۔

///

## `username` اور `password` حاصل کرنے کا code { #code-to-get-the-username-and-password }

اب آئیے **FastAPI** کی فراہم کردہ utilities استعمال کرتے ہیں۔

### `OAuth2PasswordRequestForm` { #oauth2passwordrequestform }

پہلے، `OAuth2PasswordRequestForm` import کریں، اور اسے `/token` کے *path operation* میں `Depends` کے ساتھ بطور dependency استعمال کریں:

{* ../../docs_src/security/tutorial003_an_py310.py hl[4,78] *}

`OAuth2PasswordRequestForm` ایک class dependency ہے جو ایک form body declare کرتی ہے جس میں:

* `username`۔
* `password`۔
* ایک اختیاری `scope` فیلڈ بطور ایک بڑی string، جو خالی جگہوں سے الگ strings پر مشتمل ہو۔
* ایک اختیاری `grant_type`۔

/// tip | مشورہ

OAuth2 spec دراصل ایک فیلڈ `grant_type` *مطلوب* کرتی ہے جس کی مقررہ value `password` ہو، لیکن `OAuth2PasswordRequestForm` اسے لازمی نہیں بناتا۔

اگر آپ کو اسے لازمی بنانا ہے تو `OAuth2PasswordRequestForm` کی بجائے `OAuth2PasswordRequestFormStrict` استعمال کریں۔

///

* ایک اختیاری `client_id` (ہماری مثال کے لیے اس کی ضرورت نہیں)۔
* ایک اختیاری `client_secret` (ہماری مثال کے لیے اس کی ضرورت نہیں)۔

/// info | معلومات

`OAuth2PasswordRequestForm` **FastAPI** کے لیے `OAuth2PasswordBearer` کی طرح کوئی خاص class نہیں ہے۔

`OAuth2PasswordBearer` **FastAPI** کو بتاتا ہے کہ یہ ایک security scheme ہے۔ اس لیے اسے اس طریقے سے OpenAPI میں شامل کیا جاتا ہے۔

لیکن `OAuth2PasswordRequestForm` بس ایک class dependency ہے جو آپ خود بھی لکھ سکتے تھے، یا آپ براہ راست `Form` parameters declare کر سکتے تھے۔

لیکن چونکہ یہ ایک عام استعمال کا معاملہ ہے، اسے آسان بنانے کے لیے **FastAPI** براہ راست فراہم کرتا ہے۔

///

### Form data استعمال کریں { #use-the-form-data }

/// tip | مشورہ

Dependency class `OAuth2PasswordRequestForm` کی instance میں `scope` attribute نہیں ہوگا جس میں خالی جگہوں سے الگ لمبی string ہو، بلکہ اس میں `scopes` attribute ہوگا جس میں بھیجے گئے ہر scope کے لیے strings کی اصل list ہوگی۔

ہم اس مثال میں `scopes` استعمال نہیں کر رہے، لیکن اگر آپ کو ضرورت ہو تو یہ فعالیت موجود ہے۔

///

اب، form field سے `username` استعمال کرتے ہوئے (جعلی) database سے صارف کا data حاصل کریں۔

اگر ایسا کوئی صارف نہیں ہے، تو ہم "Incorrect username or password" کی error واپس کرتے ہیں۔

Error کے لیے، ہم exception `HTTPException` استعمال کرتے ہیں:

{* ../../docs_src/security/tutorial003_an_py310.py hl[3,79:81] *}

### Password چیک کریں { #check-the-password }

اس وقت ہمارے پاس اپنے database سے صارف کا data ہے، لیکن ہم نے password چیک نہیں کیا ہے۔

آئیے پہلے اس data کو Pydantic `UserInDB` model میں ڈالتے ہیں۔

آپ کو کبھی بھی سادہ متن کے passwords محفوظ نہیں کرنے چاہئیں، تو ہم (جعلی) password hashing system استعمال کریں گے۔

اگر passwords میل نہیں کھاتے، تو ہم وہی error واپس کرتے ہیں۔

#### Password hashing { #password-hashing }

"Hashing" کا مطلب ہے: کسی مواد (اس معاملے میں password) کو bytes کی ایک ترتیب (بس ایک string) میں تبدیل کرنا جو بے معنی سی لگتی ہے۔

جب بھی آپ بالکل وہی مواد (بالکل وہی password) دیں گے، آپ کو بالکل وہی بے معنی نتیجہ ملے گا۔

لیکن آپ اس بے معنی نتیجے سے واپس password حاصل نہیں کر سکتے۔

##### Password hashing کیوں استعمال کریں { #why-use-password-hashing }

اگر آپ کا database چوری ہو جائے، تو چور کے پاس آپ کے صارفین کے سادہ متن کے passwords نہیں ہوں گے، صرف hashes ہوں گے۔

تو، چور ان passwords کو کسی اور system میں استعمال نہیں کر سکے گا (چونکہ بہت سے صارف ہر جگہ ایک ہی password استعمال کرتے ہیں، یہ خطرناک ہوتا)۔

{* ../../docs_src/security/tutorial003_an_py310.py hl[82:85] *}

#### `**user_dict` کے بارے میں { #about-user-dict }

`UserInDB(**user_dict)` کا مطلب ہے:

*`user_dict` کی keys اور values کو براہ راست key-value arguments کے طور پر پاس کریں، جو اس کے مساوی ہے:*

```Python
UserInDB(
    username = user_dict["username"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    disabled = user_dict["disabled"],
    hashed_password = user_dict["hashed_password"],
)
```

/// info | معلومات

`**user_dict` کی مزید مکمل وضاحت کے لیے [**Extra Models** کی دستاویزات](../extra-models.md#about-user-in-dict) دیکھیں۔

///

## Token واپس کریں { #return-the-token }

`token` endpoint کا response ایک JSON object ہونا چاہیے۔

اس میں ایک `token_type` ہونا چاہیے۔ ہمارے معاملے میں، چونکہ ہم "Bearer" tokens استعمال کر رہے ہیں، token type "`bearer`" ہونی چاہیے۔

اور اس میں ایک `access_token` ہونا چاہیے، ایک string جس میں ہمارا access token ہو۔

اس سادہ مثال کے لیے، ہم بالکل غیر محفوظ طریقے سے وہی `username` بطور token واپس کریں گے۔

/// tip | مشورہ

اگلے باب میں، آپ password hashing اور <abbr title="JSON Web Tokens">JWT</abbr> tokens کے ساتھ ایک حقیقی محفوظ implementation دیکھیں گے۔

لیکن ابھی کے لیے، آئیے ان مخصوص تفصیلات پر توجہ مرکوز کرتے ہیں جو ہمیں چاہئیں۔

///

{* ../../docs_src/security/tutorial003_an_py310.py hl[87] *}

/// tip | مشورہ

Spec کے مطابق، آپ کو ایک JSON واپس کرنا چاہیے جس میں `access_token` اور `token_type` ہو، بالکل اسی مثال کی طرح۔

یہ وہ چیز ہے جو آپ کو اپنے code میں خود کرنی ہوگی، اور یقینی بنائیں کہ آپ وہ JSON keys استعمال کریں۔

specifications کے مطابق رہنے کے لیے یہ تقریباً واحد چیز ہے جو آپ کو خود درست طریقے سے کرنا یاد رکھنا ہوگا۔

باقی سب کے لیے، **FastAPI** آپ کے لیے سنبھال لیتا ہے۔

///

## Dependencies کو اپ ڈیٹ کریں { #update-the-dependencies }

اب ہم اپنی dependencies کو اپ ڈیٹ کریں گے۔

ہم `current_user` *صرف* اس وقت حاصل کرنا چاہتے ہیں جب یہ صارف active ہو۔

تو، ہم ایک اضافی dependency `get_current_active_user` بناتے ہیں جو بدلے میں `get_current_user` کو بطور dependency استعمال کرتی ہے۔

یہ دونوں dependencies HTTP error واپس کریں گی اگر صارف موجود نہ ہو، یا غیر فعال ہو۔

تو، ہمارے endpoint میں، ہمیں صارف صرف اسی صورت میں ملے گا جب صارف موجود ہو، درست طریقے سے authenticated ہو، اور active ہو:

{* ../../docs_src/security/tutorial003_an_py310.py hl[58:66,69:74,94] *}

/// info | معلومات

اضافی header `WWW-Authenticate` جس کی value `Bearer` ہے جو ہم یہاں واپس کر رہے ہیں، وہ بھی spec کا حصہ ہے۔

کسی بھی HTTP (error) status code 401 "UNAUTHORIZED" کو بھی `WWW-Authenticate` header واپس کرنا چاہیے۔

Bearer tokens کے معاملے میں (ہمارا معاملہ)، اس header کی value `Bearer` ہونی چاہیے۔

آپ حقیقت میں اس اضافی header کو چھوڑ سکتے ہیں اور یہ پھر بھی کام کرے گا۔

لیکن یہ یہاں specifications کے مطابق رہنے کے لیے فراہم کیا گیا ہے۔

نیز، ایسے tools ہو سکتے ہیں جو اسے توقع رکھتے ہیں اور استعمال کرتے ہیں (ابھی یا مستقبل میں) اور یہ آپ یا آپ کے صارفین کے لیے مفید ہو سکتے ہیں، ابھی یا مستقبل میں۔

معیارات کا یہی فائدہ ہے...

///

## اسے عمل میں دیکھیں { #see-it-in-action }

Interactive docs کھولیں: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)۔

### Authenticate کریں { #authenticate }

"Authorize" بٹن پر کلک کریں۔

یہ credentials استعمال کریں:

User: `johndoe`

Password: `secret`

<img src="/img/tutorial/security/image04.png">

System میں authenticate ہونے کے بعد، آپ اسے اس طرح دیکھیں گے:

<img src="/img/tutorial/security/image05.png">

### اپنا صارف data حاصل کریں { #get-your-own-user-data }

اب operation `GET` path `/users/me` کے ساتھ استعمال کریں۔

آپ کو اپنے صارف کا data ملے گا، جیسے:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
```

<img src="/img/tutorial/security/image06.png">

اگر آپ lock آئیکن پر کلک کریں اور logout کریں، اور پھر وہی operation دوبارہ آزمائیں، تو آپ کو HTTP 401 error ملے گی:

```JSON
{
  "detail": "Not authenticated"
}
```

### غیر فعال صارف { #inactive-user }

اب ایک غیر فعال صارف کے ساتھ آزمائیں، اس سے authenticate کریں:

User: `alice`

Password: `secret2`

اور operation `GET` path `/users/me` کے ساتھ استعمال کرنے کی کوشش کریں۔

آپ کو "Inactive user" error ملے گی، جیسے:

```JSON
{
  "detail": "Inactive user"
}
```

## خلاصہ { #recap }

اب آپ کے پاس اپنی API کے لیے `username` اور `password` پر مبنی مکمل security system بنانے کے tools ہیں۔

ان tools کا استعمال کرتے ہوئے، آپ security system کو کسی بھی database اور کسی بھی صارف یا data model کے ساتھ مطابقت پذیر بنا سکتے ہیں۔

بس ایک تفصیل باقی ہے کہ یہ حقیقت میں ابھی "محفوظ" نہیں ہے۔

اگلے باب میں آپ دیکھیں گے کہ ایک محفوظ password hashing library اور <abbr title="JSON Web Tokens">JWT</abbr> tokens کیسے استعمال کریں۔
