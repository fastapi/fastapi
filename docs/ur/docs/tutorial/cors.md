# CORS (Cross-Origin Resource Sharing) { #cors-cross-origin-resource-sharing }

[CORS یا "Cross-Origin Resource Sharing"](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) ان صورتحال سے مراد ہے جب browser میں چلنے والا frontend JavaScript code کے ذریعے backend سے بات چیت کرتا ہے، اور backend frontend سے مختلف "origin" پر ہوتا ہے۔

## Origin { #origin }

ایک origin protocol (`http`, `https`)، domain (`myapp.com`, `localhost`, `localhost.tiangolo.com`)، اور port (`80`, `443`, `8080`) کا مجموعہ ہے۔

تو، یہ سب مختلف origins ہیں:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

اگرچہ یہ سب `localhost` پر ہیں، لیکن یہ مختلف protocols یا ports استعمال کرتے ہیں، اس لیے یہ مختلف "origins" ہیں۔

## مراحل { #steps }

تو، فرض کریں آپ کا frontend browser میں `http://localhost:8080` پر چل رہا ہے، اور اس کا JavaScript ایک backend سے بات چیت کرنے کی کوشش کر رہا ہے جو `http://localhost` پر چل رہا ہے (چونکہ ہم نے port نہیں بتایا، browser ڈیفالٹ port `80` فرض کرے گا)۔

پھر، browser `:80`-backend کو ایک HTTP `OPTIONS` request بھیجے گا، اور اگر backend مناسب headers بھیجتا ہے جو اس مختلف origin (`http://localhost:8080`) سے بات چیت کی اجازت دیتے ہیں تو `:8080`-browser frontend میں موجود JavaScript کو `:80`-backend کو اپنی request بھیجنے دے گا۔

اس کے لیے، `:80`-backend کے پاس "اجازت یافتہ origins" کی فہرست ہونی چاہیے۔

اس صورت میں، فہرست میں `http://localhost:8080` شامل ہونا ضروری ہے تاکہ `:8080`-frontend درست طریقے سے کام کرے۔

## Wildcards { #wildcards }

فہرست کو `"*"` (ایک "wildcard") قرار دینا بھی ممکن ہے تاکہ تمام origins کو اجازت دی جائے۔

لیکن یہ صرف مخصوص قسم کی بات چیت کی اجازت دے گا، credentials سے متعلق ہر چیز کو چھوڑ کر: Cookies، Authorization headers جیسے Bearer Tokens کے ساتھ استعمال ہونے والے، وغیرہ۔

تو، سب کچھ درست طریقے سے کام کرنے کے لیے، اجازت یافتہ origins کو واضح طور پر بیان کرنا بہتر ہے۔

## `CORSMiddleware` استعمال کریں { #use-corsmiddleware }

آپ اسے اپنی **FastAPI** application میں `CORSMiddleware` استعمال کرتے ہوئے configure کر سکتے ہیں۔

* `CORSMiddleware` import کریں۔
* اجازت یافتہ origins کی فہرست بنائیں (strings کے طور پر)۔
* اسے اپنی **FastAPI** application میں بطور "middleware" شامل کریں۔

آپ یہ بھی بتا سکتے ہیں کہ آپ کا backend اجازت دیتا ہے:

* Credentials (Authorization headers، Cookies، وغیرہ)۔
* مخصوص HTTP methods (`POST`, `PUT`) یا wildcard `"*"` سے سب۔
* مخصوص HTTP headers یا wildcard `"*"` سے سب۔

{* ../../docs_src/cors/tutorial001_py310.py hl[2,6:11,13:19] *}


`CORSMiddleware` implementation کے ذریعے استعمال ہونے والے ڈیفالٹ parameters پہلے سے پابندی والے ہیں، لہذا آپ کو واضح طور پر مخصوص origins، methods، یا headers کو فعال کرنا ہوگا تاکہ browsers کو Cross-Domain context میں انہیں استعمال کرنے کی اجازت ملے۔

درج ذیل arguments کی حمایت کی جاتی ہے:

* `allow_origins` - origins کی فہرست جنہیں cross-origin requests کرنے کی اجازت ہونی چاہیے۔ مثلاً `['https://example.org', 'https://www.example.org']`۔ آپ `['*']` استعمال کر سکتے ہیں کسی بھی origin کو اجازت دینے کے لیے۔
* `allow_origin_regex` - ایک regex string جو ان origins سے match کرے جنہیں cross-origin requests کرنے کی اجازت ہونی چاہیے۔ مثلاً `'https://.*\.example\.org'`۔
* `allow_methods` - HTTP methods کی فہرست جنہیں cross-origin requests کے لیے اجازت ہونی چاہیے۔ ڈیفالٹ `['GET']` ہے۔ آپ `['*']` استعمال کر سکتے ہیں تمام معیاری methods کی اجازت دینے کے لیے۔
* `allow_headers` - HTTP request headers کی فہرست جنہیں cross-origin requests کے لیے حمایت ملنی چاہیے۔ ڈیفالٹ `[]` ہے۔ آپ `['*']` استعمال کر سکتے ہیں تمام headers کی اجازت دینے کے لیے۔ `Accept`، `Accept-Language`، `Content-Language` اور `Content-Type` headers [سادہ CORS requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests) کے لیے ہمیشہ اجازت یافتہ ہیں۔
* `allow_credentials` - بتائیں کہ cross-origin requests کے لیے cookies کی حمایت ہونی چاہیے۔ ڈیفالٹ `False` ہے۔

    اگر `allow_credentials` کو `True` پر سیٹ کیا گیا ہے تو `allow_origins`، `allow_methods` اور `allow_headers` میں سے کسی کو بھی `['*']` پر سیٹ نہیں کیا جا سکتا۔ ان سب کو [واضح طور پر بیان](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#credentialed_requests_and_wildcards) کیا جانا چاہیے۔

* `expose_headers` - ان response headers کو بتائیں جو browser کے لیے قابل رسائی ہونے چاہئیں۔ ڈیفالٹ `[]` ہے۔
* `max_age` - browsers کے لیے CORS responses کو cache کرنے کا زیادہ سے زیادہ وقت سیکنڈز میں سیٹ کرتا ہے۔ ڈیفالٹ `600` ہے۔

middleware دو خاص قسم کی HTTP requests کا جواب دیتا ہے...

### CORS preflight requests { #cors-preflight-requests }

یہ کوئی بھی `OPTIONS` request ہے جس میں `Origin` اور `Access-Control-Request-Method` headers ہوں۔

اس صورت میں middleware آنے والی request کو روکے گا اور مناسب CORS headers کے ساتھ جواب دے گا، نیز معلوماتی مقاصد کے لیے `200` یا `400` response دے گا۔

### سادہ requests { #simple-requests }

کوئی بھی request جس میں `Origin` header ہو۔ اس صورت میں middleware request کو عام طریقے سے آگے بھیجے گا، لیکن response میں مناسب CORS headers شامل کرے گا۔

## مزید معلومات { #more-info }

<abbr title="Cross-Origin Resource Sharing">CORS</abbr> کے بارے میں مزید معلومات کے لیے، [Mozilla CORS دستاویزات](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) دیکھیں۔

/// note | تکنیکی تفصیلات

آپ `from starlette.middleware.cors import CORSMiddleware` بھی استعمال کر سکتے ہیں۔

**FastAPI** آپ کی سہولت کے لیے `fastapi.middleware` میں کئی middlewares فراہم کرتا ہے۔ لیکن دستیاب middlewares میں سے زیادہ تر براہ راست Starlette سے آتے ہیں۔

///
