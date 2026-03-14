# Security { #security }

Security، authentication اور authorization کو سنبھالنے کے بہت سے طریقے ہیں۔

اور یہ عام طور پر ایک پیچیدہ اور "مشکل" موضوع ہوتا ہے۔

بہت سے frameworks اور systems میں صرف security اور authentication کو سنبھالنے میں بہت زیادہ محنت اور code لگتا ہے (بہت سے معاملات میں یہ لکھے گئے کل code کا 50% یا اس سے زیادہ ہو سکتا ہے)۔

**FastAPI** آپ کو **Security** کو آسانی سے، تیزی سے، ایک معیاری طریقے سے سنبھالنے میں مدد کرنے کے لیے کئی tools فراہم کرتا ہے، بغیر اس کے کہ آپ کو تمام security specifications کا مطالعہ اور سیکھنا پڑے۔

لیکن پہلے، آئیے کچھ چھوٹے تصورات کو سمجھتے ہیں۔

## جلدی میں ہیں؟ { #in-a-hurry }

اگر آپ کو ان میں سے کسی بھی اصطلاح سے کوئی سروکار نہیں اور آپ کو صرف username اور password پر مبنی authentication کے ساتھ security ابھی شامل کرنی ہے، تو اگلے ابواب پر چلے جائیں۔

## OAuth2 { #oauth2 }

OAuth2 ایک specification ہے جو authentication اور authorization کو سنبھالنے کے کئی طریقے بیان کرتی ہے۔

یہ کافی وسیع specification ہے اور کئی پیچیدہ استعمال کے معاملات کا احاطہ کرتی ہے۔

اس میں "third party" کا استعمال کرتے ہوئے authenticate کرنے کے طریقے شامل ہیں۔

یہی وہ چیز ہے جو "Facebook، Google، X (Twitter)، GitHub سے login کریں" والے تمام systems اندرونی طور پر استعمال کرتے ہیں۔

### OAuth 1 { #oauth-1 }

ایک OAuth 1 بھی تھا، جو OAuth2 سے بہت مختلف اور زیادہ پیچیدہ ہے، کیونکہ اس میں communication کو encrypt کرنے کے طریقے کی براہ راست specifications شامل تھیں۔

یہ آج کل زیادہ مقبول یا استعمال نہیں ہوتا۔

OAuth2 communication کو encrypt کرنے کا طریقہ متعین نہیں کرتا، یہ توقع کرتا ہے کہ آپ کی application HTTPS کے ساتھ سرو ہو رہی ہو۔

/// tip | مشورہ

**deployment** کے سیکشن میں آپ دیکھیں گے کہ Traefik اور Let's Encrypt کا استعمال کرتے ہوئے مفت میں HTTPS کیسے سیٹ اپ کریں۔

///

## OpenID Connect { #openid-connect }

OpenID Connect ایک اور specification ہے، جو **OAuth2** پر مبنی ہے۔

یہ OAuth2 کو بس اتنا بڑھاتی ہے کہ OAuth2 میں جو چیزیں نسبتاً مبہم ہیں انہیں متعین کرتی ہے، تاکہ اسے زیادہ interoperable بنایا جا سکے۔

مثال کے طور پر، Google login OpenID Connect استعمال کرتا ہے (جو اندرونی طور پر OAuth2 استعمال کرتا ہے)۔

لیکن Facebook login OpenID Connect کو سپورٹ نہیں کرتا۔ اس کا OAuth2 کا اپنا انداز ہے۔

### OpenID ("OpenID Connect" نہیں) { #openid-not-openid-connect }

ایک "OpenID" specification بھی تھی۔ اس نے **OpenID Connect** جیسا ہی مسئلہ حل کرنے کی کوشش کی، لیکن OAuth2 پر مبنی نہیں تھی۔

لہذا، یہ ایک مکمل الگ system تھا۔

یہ آج کل زیادہ مقبول یا استعمال نہیں ہوتا۔

## OpenAPI { #openapi }

OpenAPI (پہلے Swagger کے نام سے جانا جاتا تھا) APIs بنانے کے لیے ایک open specification ہے (اب Linux Foundation کا حصہ ہے)۔

**FastAPI** **OpenAPI** پر مبنی ہے۔

یہی وہ چیز ہے جو متعدد خودکار interactive documentation interfaces، code generation وغیرہ کو ممکن بناتی ہے۔

OpenAPI متعدد security "schemes" کی تعریف کرنے کا ایک طریقہ رکھتا ہے۔

انہیں استعمال کرکے، آپ ان تمام معیار پر مبنی tools کا فائدہ اٹھا سکتے ہیں، بشمول یہ interactive documentation systems۔

OpenAPI درج ذیل security schemes کی تعریف کرتا ہے:

* `apiKey`: ایک application مخصوص key جو آ سکتی ہے:
    * ایک query parameter سے۔
    * ایک header سے۔
    * ایک cookie سے۔
* `http`: معیاری HTTP authentication systems، بشمول:
    * `bearer`: ایک header `Authorization` جس کی value `Bearer ` ہو اور اس کے ساتھ ایک token ہو۔ یہ OAuth2 سے وراثت میں ملا ہے۔
    * HTTP Basic authentication۔
    * HTTP Digest، وغیرہ۔
* `oauth2`: security کو سنبھالنے کے تمام OAuth2 طریقے (جنہیں "flows" کہتے ہیں)۔
    * ان میں سے کئی flows OAuth 2.0 authentication provider بنانے کے لیے موزوں ہیں (جیسے Google، Facebook، X (Twitter)، GitHub، وغیرہ):
        * `implicit`
        * `clientCredentials`
        * `authorizationCode`
    * لیکن ایک مخصوص "flow" ہے جو براہ راست اسی application میں authentication کو سنبھالنے کے لیے بالکل درست استعمال ہو سکتا ہے:
        * `password`: آنے والے کچھ ابواب میں اس کی مثالیں دی جائیں گی۔
* `openIdConnect`: OAuth2 authentication data کو خودکار طور پر دریافت کرنے کا طریقہ بیان کرتا ہے۔
    * یہ خودکار دریافت OpenID Connect specification میں متعین ہے۔


/// tip | مشورہ

Google، Facebook، X (Twitter)، GitHub وغیرہ جیسے دوسرے authentication/authorization providers کو integrate کرنا بھی ممکن اور نسبتاً آسان ہے۔

سب سے پیچیدہ مسئلہ ان جیسا authentication/authorization provider بنانا ہے، لیکن **FastAPI** آپ کو یہ آسانی سے کرنے کے tools دیتا ہے، جبکہ بھاری کام آپ کے لیے خود کرتا ہے۔

///

## **FastAPI** utilities { #fastapi-utilities }

FastAPI ان میں سے ہر security scheme کے لیے `fastapi.security` module میں کئی tools فراہم کرتا ہے جو ان security mechanisms کو استعمال کرنا آسان بناتے ہیں۔

آنے والے ابواب میں آپ دیکھیں گے کہ **FastAPI** کی طرف سے فراہم کردہ ان tools کا استعمال کرتے ہوئے اپنی API میں security کیسے شامل کریں۔

اور آپ یہ بھی دیکھیں گے کہ یہ خودکار طور پر interactive documentation system میں کیسے شامل ہو جاتی ہے۔
