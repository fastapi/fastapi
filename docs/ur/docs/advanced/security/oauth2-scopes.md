# OAuth2 scopes { #oauth2-scopes }

آپ **FastAPI** کے ساتھ براہ راست OAuth2 scopes استعمال کر سکتے ہیں، یہ بغیر کسی رکاوٹ کے کام کرنے کے لیے مربوط ہیں۔

یہ آپ کو OAuth2 معیار کے مطابق، آپ کی OpenAPI ایپلیکیشن (اور API docs) میں مربوط، ایک زیادہ باریک بینی سے اجازتوں کا نظام رکھنے کی سہولت دے گا۔

OAuth2 with scopes وہ طریقہ کار ہے جو بہت سے بڑے authentication فراہم کنندگان استعمال کرتے ہیں، جیسے Facebook، Google، GitHub، Microsoft، X (Twitter) وغیرہ۔ وہ اسے صارفین اور ایپلیکیشنز کو مخصوص اجازتیں دینے کے لیے استعمال کرتے ہیں۔

جب بھی آپ Facebook، Google، GitHub، Microsoft، X (Twitter) کے ساتھ "log in" کرتے ہیں، وہ ایپلیکیشن OAuth2 with scopes استعمال کر رہی ہوتی ہے۔

اس حصے میں آپ دیکھیں گے کہ اپنی **FastAPI** ایپلیکیشن میں اسی OAuth2 with scopes کے ساتھ authentication اور authorization کیسے منظم کی جائے۔

/// warning | انتباہ

یہ ایک کم و بیش ایڈوانسڈ حصہ ہے۔ اگر آپ ابھی شروع کر رہے ہیں، تو آپ اسے چھوڑ سکتے ہیں۔

آپ کو لازمی طور پر OAuth2 scopes کی ضرورت نہیں، اور آپ authentication اور authorization جیسے چاہیں سنبھال سکتے ہیں۔

لیکن OAuth2 with scopes آپ کی API (OpenAPI کے ساتھ) اور آپ کے API docs میں اچھی طرح مربوط ہو سکتا ہے۔

بہرحال، آپ ان scopes، یا کسی بھی دوسری security/authorization ضرورت کو، اپنے کوڈ میں جیسے چاہیں نافذ کرتے ہیں۔

بہت سی صورتوں میں، OAuth2 with scopes ضرورت سے زیادہ ہو سکتا ہے۔

لیکن اگر آپ جانتے ہیں کہ آپ کو اس کی ضرورت ہے، یا آپ متجسس ہیں، تو پڑھتے رہیں۔

///

## OAuth2 scopes اور OpenAPI { #oauth2-scopes-and-openapi }

OAuth2 specification "scopes" کو خالی جگہوں سے الگ کیے گئے strings کی فہرست کے طور پر بیان کرتی ہے۔

ہر ایک string کا مواد کسی بھی شکل میں ہو سکتا ہے، لیکن اس میں خالی جگہیں نہیں ہونی چاہئیں۔

یہ scopes "اجازتوں" کی نمائندگی کرتے ہیں۔

OpenAPI (مثلاً API docs) میں، آپ "security schemes" بیان کر سکتے ہیں۔

جب ان میں سے کوئی security scheme OAuth2 استعمال کرے، تو آپ scopes بھی بیان اور استعمال کر سکتے ہیں۔

ہر "scope" بس ایک string ہے (بغیر خالی جگہوں کے)۔

یہ عام طور پر مخصوص security اجازتیں بیان کرنے کے لیے استعمال ہوتے ہیں، مثال کے طور پر:

* `users:read` یا `users:write` عام مثالیں ہیں۔
* `instagram_basic` Facebook / Instagram استعمال کرتا ہے۔
* `https://www.googleapis.com/auth/drive` Google استعمال کرتا ہے۔

/// info | معلومات

OAuth2 میں "scope" صرف ایک string ہے جو ایک مخصوص مطلوبہ اجازت بیان کرتی ہے۔

اس سے کوئی فرق نہیں پڑتا کہ اس میں `:` جیسے دوسرے حروف ہیں یا یہ URL ہے۔

یہ تفصیلات عمل درآمد کے لحاظ سے مخصوص ہیں۔

OAuth2 کے لیے یہ بس strings ہیں۔

///

## مجموعی نظارہ { #global-view }

پہلے آئیے جلدی سے ان حصوں کو دیکھیں جو مرکزی **ٹیوٹوریل - صارف گائیڈ** کی [OAuth2 with Password (and hashing), Bearer with JWT tokens](../../tutorial/security/oauth2-jwt.md) مثالوں سے تبدیل ہوتے ہیں۔ اب OAuth2 scopes استعمال کرتے ہوئے:

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,9,13,47,65,106,108:116,122:126,130:136,141,157] *}

اب آئیے ان تبدیلیوں کا قدم بہ قدم جائزہ لیتے ہیں۔

## OAuth2 Security scheme { #oauth2-security-scheme }

پہلی تبدیلی یہ ہے کہ اب ہم OAuth2 security scheme کو دو دستیاب scopes، `me` اور `items` کے ساتھ بیان کر رہے ہیں۔

`scopes` parameter ایک `dict` لیتا ہے جس میں ہر scope بطور key اور وضاحت بطور value ہوتی ہے:

{* ../../docs_src/security/tutorial005_an_py310.py hl[63:66] *}

چونکہ ہم اب ان scopes کو بیان کر رہے ہیں، یہ API docs میں جب آپ log-in/authorize کریں گے تو دکھائی دیں گے۔

اور آپ منتخب کر سکیں گے کہ آپ کون سے scopes تک رسائی دینا چاہتے ہیں: `me` اور `items`۔

یہ وہی طریقہ کار ہے جو Facebook، Google، GitHub وغیرہ کے ساتھ login کرتے وقت اجازتیں دیتے وقت استعمال ہوتا ہے:

<img src="/img/tutorial/security/image11.png">

## Scopes کے ساتھ JWT token { #jwt-token-with-scopes }

اب token *path operation* میں تبدیلی کریں تاکہ درخواست کیے گئے scopes واپس کیے جائیں۔

ہم ابھی بھی وہی `OAuth2PasswordRequestForm` استعمال کر رہے ہیں۔ اس میں `scopes` property شامل ہے جس میں `str` کی `list` ہوتی ہے، request میں موصول ہونے والے ہر scope کے ساتھ۔

اور ہم scopes کو JWT token کے حصے کے طور پر واپس کرتے ہیں۔

/// danger

سادگی کے لیے، یہاں ہم موصول ہونے والے scopes کو براہ راست token میں شامل کر رہے ہیں۔

لیکن آپ کی ایپلیکیشن میں، security کے لیے، آپ کو یقینی بنانا چاہیے کہ آپ صرف وہ scopes شامل کریں جو صارف واقعی رکھ سکتا ہے، یا جو آپ نے پہلے سے مقرر کیے ہیں۔

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[157] *}

## *path operations* اور dependencies میں scopes بیان کریں { #declare-scopes-in-path-operations-and-dependencies }

اب ہم بیان کرتے ہیں کہ `/users/me/items/` کے *path operation* کو scope `items` درکار ہے۔

اس کے لیے ہم `fastapi` سے `Security` import اور استعمال کرتے ہیں۔

آپ `Security` استعمال کر کے dependencies بیان کر سکتے ہیں (بالکل `Depends` کی طرح)، لیکن `Security` ایک اضافی parameter `scopes` بھی لیتا ہے جس میں scopes (strings) کی فہرست ہوتی ہے۔

اس صورت میں، ہم dependency function `get_current_active_user` کو `Security` میں دیتے ہیں (اسی طرح جیسے ہم `Depends` کے ساتھ کرتے)۔

لیکن ہم scopes کی ایک `list` بھی دیتے ہیں، اس صورت میں صرف ایک scope: `items` (اس میں مزید بھی ہو سکتے ہیں)۔

اور dependency function `get_current_active_user` بھی sub-dependencies بیان کر سکتا ہے، نہ صرف `Depends` کے ساتھ بلکہ `Security` کے ساتھ بھی۔ اپنا sub-dependency function (`get_current_user`) بیان کرتے ہوئے، اور مزید scope کی ضروریات۔

اس صورت میں، اسے scope `me` درکار ہے (اسے ایک سے زیادہ scopes بھی درکار ہو سکتے ہیں)۔

/// note | نوٹ

آپ کو لازمی طور پر مختلف جگہوں پر مختلف scopes شامل کرنے کی ضرورت نہیں۔

ہم یہاں یہ دکھانے کے لیے کر رہے ہیں کہ **FastAPI** مختلف سطحوں پر بیان کیے گئے scopes کو کیسے سنبھالتا ہے۔

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,141,172] *}

/// info | تکنیکی تفصیلات

`Security` دراصل `Depends` کی ایک subclass ہے، اور اس میں صرف ایک اضافی parameter ہے جو ہم بعد میں دیکھیں گے۔

لیکن `Depends` کی بجائے `Security` استعمال کرنے سے، **FastAPI** جان لے گا کہ وہ security scopes بیان کر سکتا ہے، انہیں اندرونی طور پر استعمال کر سکتا ہے، اور API کو OpenAPI کے ساتھ دستاویز بنا سکتا ہے۔

لیکن جب آپ `fastapi` سے `Query`، `Path`، `Depends`، `Security` اور دیگر import کرتے ہیں، تو یہ دراصل ایسے functions ہیں جو خصوصی classes واپس کرتے ہیں۔

///

## `SecurityScopes` استعمال کریں { #use-securityscopes }

اب dependency `get_current_user` کو اپ ڈیٹ کریں۔

یہ وہی ہے جسے اوپر کی dependencies استعمال کرتی ہیں۔

یہاں ہم وہی OAuth2 scheme استعمال کر رہے ہیں جو ہم نے پہلے بنایا تھا، اسے dependency کے طور پر بیان کرتے ہوئے: `oauth2_scheme`۔

چونکہ اس dependency function کو خود کسی scope کی ضرورت نہیں، ہم `Depends` کو `oauth2_scheme` کے ساتھ استعمال کر سکتے ہیں، جب ہمیں security scopes بیان کرنے کی ضرورت نہ ہو تو `Security` استعمال کرنا ضروری نہیں۔

ہم `fastapi.security` سے import کیا ہوا `SecurityScopes` قسم کا ایک خصوصی parameter بھی بیان کرتے ہیں۔

یہ `SecurityScopes` class `Request` سے ملتی جلتی ہے (`Request` براہ راست request object حاصل کرنے کے لیے استعمال ہوتا تھا)۔

{* ../../docs_src/security/tutorial005_an_py310.py hl[9,106] *}

## `scopes` استعمال کریں { #use-the-scopes }

`security_scopes` parameter کی قسم `SecurityScopes` ہوگی۔

اس میں `scopes` property ہوگی جس میں خود اور تمام dependencies جو اسے sub-dependency کے طور پر استعمال کرتی ہیں، کے درکار تمام scopes کی فہرست ہوگی۔ یعنی تمام "dependants"... یہ الجھا دینے والا لگ سکتا ہے، نیچے اسے دوبارہ سمجھایا گیا ہے۔

`security_scopes` object (`SecurityScopes` class کا) ایک `scope_str` attribute بھی فراہم کرتا ہے جس میں ان scopes پر مشتمل ایک واحد string ہوتی ہے، خالی جگہوں سے الگ (ہم اسے استعمال کریں گے)۔

ہم ایک `HTTPException` بناتے ہیں جسے ہم بعد میں کئی مقامات پر دوبارہ استعمال (`raise`) کر سکتے ہیں۔

اس exception میں، ہم درکار scopes (اگر کوئی ہوں) خالی جگہوں سے الگ string کے طور پر (`scope_str` استعمال کرتے ہوئے) شامل کرتے ہیں۔ ہم scopes پر مشتمل وہ string `WWW-Authenticate` header میں ڈالتے ہیں (یہ specification کا حصہ ہے)۔

{* ../../docs_src/security/tutorial005_an_py310.py hl[106,108:116] *}

## `username` اور ڈیٹا کی شکل کی تصدیق کریں { #verify-the-username-and-data-shape }

ہم تصدیق کرتے ہیں کہ ہمیں `username` ملا ہے، اور scopes نکالتے ہیں۔

اور پھر ہم اس ڈیٹا کی Pydantic model سے تصدیق کرتے ہیں (`ValidationError` exception پکڑتے ہوئے)، اور اگر JWT token پڑھنے یا Pydantic سے ڈیٹا کی تصدیق کرنے میں کوئی error آئے، تو ہم وہ `HTTPException` raise کرتے ہیں جو ہم نے پہلے بنایا تھا۔

اس کے لیے، ہم Pydantic model `TokenData` کو ایک نئی property `scopes` کے ساتھ اپ ڈیٹ کرتے ہیں۔

Pydantic سے ڈیٹا کی تصدیق کر کے ہم یقینی بنا سکتے ہیں کہ ہمارے پاس، مثال کے طور پر، scopes کے ساتھ بالکل `str` کی `list` ہے اور `username` کے ساتھ ایک `str`۔

مثال کے طور پر، `dict` یا کچھ اور کی بجائے، کیونکہ یہ بعد میں کسی مقام پر ایپلیکیشن کو توڑ سکتا ہے، جو اسے security کا خطرہ بنا دے گا۔

ہم یہ بھی تصدیق کرتے ہیں کہ اس username کا صارف موجود ہے، اور اگر نہیں، تو وہی exception raise کرتے ہیں جو ہم نے پہلے بنایا تھا۔

{* ../../docs_src/security/tutorial005_an_py310.py hl[47,117:129] *}

## `scopes` کی تصدیق کریں { #verify-the-scopes }

اب ہم تصدیق کرتے ہیں کہ اس dependency اور تمام dependants (بشمول *path operations*) کے لیے درکار تمام scopes، موصول ہونے والے token میں فراہم کیے گئے scopes میں شامل ہیں، بصورت دیگر `HTTPException` raise کرتے ہیں۔

اس کے لیے ہم `security_scopes.scopes` استعمال کرتے ہیں، جس میں ان تمام scopes کی `list` `str` کے طور پر ہوتی ہے۔

{* ../../docs_src/security/tutorial005_an_py310.py hl[130:136] *}

## Dependency tree اور scopes { #dependency-tree-and-scopes }

آئیے اس dependency tree اور scopes کا دوبارہ جائزہ لیتے ہیں۔

چونکہ `get_current_active_user` dependency کی `get_current_user` پر sub-dependency ہے، اس لیے `get_current_active_user` میں بیان کیا گیا scope `"me"` `get_current_user` کو دیے گئے `security_scopes.scopes` میں درکار scopes کی فہرست میں شامل ہوگا۔

*path operation* خود بھی ایک scope بیان کرتا ہے، `"items"`، تو یہ بھی `get_current_user` کو دیے گئے `security_scopes.scopes` کی فہرست میں ہوگا۔

یہاں dependencies اور scopes کا درجہ بندی کا نظارہ ہے:

* *path operation* `read_own_items` میں ہے:
    * درکار scopes `["items"]` dependency کے ساتھ:
    * `get_current_active_user`:
        * dependency function `get_current_active_user` میں ہے:
            * درکار scopes `["me"]` dependency کے ساتھ:
            * `get_current_user`:
                * dependency function `get_current_user` میں ہے:
                    * خود کوئی scopes درکار نہیں۔
                    * `oauth2_scheme` استعمال کرنے والی dependency۔
                    * `SecurityScopes` قسم کا `security_scopes` parameter:
                        * اس `security_scopes` parameter میں `scopes` property ہے جس میں اوپر بیان کیے گئے تمام scopes کی `list` ہے، تو:
                            * `security_scopes.scopes` *path operation* `read_own_items` کے لیے `["me", "items"]` ہوگا۔
                            * `security_scopes.scopes` *path operation* `read_users_me` کے لیے `["me"]` ہوگا، کیونکہ یہ dependency `get_current_active_user` میں بیان کیا گیا ہے۔
                            * `security_scopes.scopes` *path operation* `read_system_status` کے لیے `[]` (خالی) ہوگا، کیونکہ اس نے `scopes` کے ساتھ کوئی `Security` بیان نہیں کیا، اور اس کی dependency `get_current_user` بھی کوئی `scopes` بیان نہیں کرتی۔

/// tip | مشورہ

یہاں اہم اور "جادوئی" بات یہ ہے کہ `get_current_user` ہر *path operation* کے لیے چیک کرنے کے لیے scopes کی مختلف فہرست رکھے گا۔

سب کا انحصار ہر *path operation* میں اور اس مخصوص *path operation* کے لیے dependency tree میں ہر dependency میں بیان کیے گئے `scopes` پر ہے۔

///

## `SecurityScopes` کے بارے میں مزید تفصیلات { #more-details-about-securityscopes }

آپ `SecurityScopes` کسی بھی مقام پر، اور متعدد جگہوں پر استعمال کر سکتے ہیں، یہ ضروری نہیں کہ "root" dependency پر ہو۔

اس میں ہمیشہ موجودہ `Security` dependencies اور **اس مخصوص** *path operation* اور **اس مخصوص** dependency tree کے تمام dependants میں بیان کیے گئے security scopes ہوں گے۔

چونکہ `SecurityScopes` میں dependants کی طرف سے بیان کیے گئے تمام scopes ہوں گے، آپ اسے ایک مرکزی dependency function میں استعمال کر سکتے ہیں تاکہ تصدیق کی جا سکے کہ token میں درکار scopes موجود ہیں، اور پھر مختلف *path operations* میں مختلف scope کی ضروریات بیان کریں۔

ہر *path operation* کے لیے آزادانہ طور پر چیک کیے جائیں گے۔

## اسے چیک کریں { #check-it }

اگر آپ API docs کھولیں، تو آپ authenticate کر سکتے ہیں اور بتا سکتے ہیں کہ آپ کون سے scopes authorize کرنا چاہتے ہیں۔

<img src="/img/tutorial/security/image11.png">

اگر آپ کوئی scope منتخب نہیں کرتے، تو آپ "authenticated" ہوں گے، لیکن جب آپ `/users/me/` یا `/users/me/items/` تک رسائی حاصل کرنے کی کوشش کریں گے تو آپ کو ایک error ملے گا کہ آپ کے پاس کافی اجازتیں نہیں ہیں۔ آپ پھر بھی `/status/` تک رسائی حاصل کر سکیں گے۔

اور اگر آپ scope `me` منتخب کرتے ہیں لیکن scope `items` نہیں، تو آپ `/users/me/` تک رسائی حاصل کر سکیں گے لیکن `/users/me/items/` تک نہیں۔

یہ وہی ہوگا جو کسی تیسرے فریق کی ایپلیکیشن کے ساتھ ہوتا جو صارف کی طرف سے فراہم کیے گئے token کے ساتھ ان *path operations* میں سے کسی تک رسائی حاصل کرنے کی کوشش کرتی، اس پر منحصر کہ صارف نے ایپلیکیشن کو کتنی اجازتیں دیں۔

## تیسرے فریق کی integrations کے بارے میں { #about-third-party-integrations }

اس مثال میں ہم OAuth2 "password" flow استعمال کر رہے ہیں۔

یہ اس وقت مناسب ہے جب ہم اپنی خود کی ایپلیکیشن میں login کر رہے ہوں، شاید اپنے خود کے frontend کے ساتھ۔

کیونکہ ہم `username` اور `password` وصول کرنے پر اعتماد کر سکتے ہیں، کیونکہ ہم اسے کنٹرول کرتے ہیں۔

لیکن اگر آپ ایسی OAuth2 ایپلیکیشن بنا رہے ہیں جس سے دوسرے جڑیں گے (یعنی اگر آپ Facebook، Google، GitHub وغیرہ کے مساوی authentication فراہم کنندہ بنا رہے ہیں) تو آپ کو دوسرے flows میں سے کوئی استعمال کرنا چاہیے۔

سب سے عام implicit flow ہے۔

سب سے محفوظ code flow ہے، لیکن اسے عمل میں لانا زیادہ پیچیدہ ہے کیونکہ اس میں مزید مراحل درکار ہیں۔ چونکہ یہ زیادہ پیچیدہ ہے، بہت سے فراہم کنندگان implicit flow تجویز کرتے ہیں۔

/// note | نوٹ

یہ عام ہے کہ ہر authentication فراہم کنندہ اپنے flows کو مختلف ناموں سے پکارتا ہے، تاکہ اسے اپنے برانڈ کا حصہ بنا سکے۔

لیکن آخر میں، وہ وہی OAuth2 معیار نافذ کر رہے ہیں۔

///

**FastAPI** ان تمام OAuth2 authentication flows کے لیے `fastapi.security.oauth2` میں utilities شامل کرتا ہے۔

## Decorator `dependencies` میں `Security` { #security-in-decorator-dependencies }

جس طرح آپ decorator کے `dependencies` parameter میں `Depends` کی `list` بیان کر سکتے ہیں (جیسا کہ [Dependencies in path operation decorators](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md) میں سمجھایا گیا ہے)، اسی طرح آپ وہاں `scopes` کے ساتھ `Security` بھی استعمال کر سکتے ہیں۔
