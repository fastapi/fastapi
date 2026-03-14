# SDKs بنانا { #generating-sdks }

چونکہ **FastAPI** **OpenAPI** specification پر مبنی ہے، اس کے APIs کو ایک معیاری فارمیٹ میں بیان کیا جا سکتا ہے جسے بہت سے ٹولز سمجھتے ہیں۔

اس سے تازہ ترین **دستاویزات**، متعدد زبانوں میں client لائبریریاں (<abbr title="Software Development Kits">**SDKs**</abbr>)، اور **testing** یا **automation workflows** بنانا آسان ہو جاتا ہے جو آپ کے کوڈ کے ساتھ ہم آہنگ رہتے ہیں۔

اس گائیڈ میں، آپ سیکھیں گے کہ اپنے FastAPI backend کے لیے **TypeScript SDK** کیسے بنائیں۔

## اوپن سورس SDK Generators { #open-source-sdk-generators }

ایک ورسٹائل آپشن [OpenAPI Generator](https://openapi-generator.tech/) ہے، جو **بہت سی پروگرامنگ زبانوں** کو سپورٹ کرتا ہے اور آپ کی OpenAPI specification سے SDKs بنا سکتا ہے۔

**TypeScript clients** کے لیے، [Hey API](https://heyapi.dev/) ایک مقصد کے لیے بنایا گیا حل ہے، جو TypeScript ایکو سسٹم کے لیے بہترین تجربہ فراہم کرتا ہے۔

آپ [OpenAPI.Tools](https://openapi.tools/#sdk) پر مزید SDK generators دریافت کر سکتے ہیں۔

/// tip | مشورہ

FastAPI خود بخود **OpenAPI 3.1** specifications بناتا ہے، لہذا آپ جو بھی ٹول استعمال کریں اسے اس ورژن کو سپورٹ کرنا ضروری ہے۔

///

## FastAPI کے اسپانسرز سے SDK Generators { #sdk-generators-from-fastapi-sponsors }

یہ سیکشن FastAPI کے اسپانسر کمپنیوں کے **وینچر بیکڈ** اور **کمپنی سپورٹ یافتہ** حل نمایاں کرتا ہے۔ یہ پروڈکٹس اعلیٰ معیار کی بنائی گئی SDKs کے ساتھ **اضافی خصوصیات** اور **integrations** فراہم کرتے ہیں۔

**FastAPI** کو ✨ [**اسپانسر**](../help-fastapi.md#sponsor-the-author) ✨ کرکے، یہ کمپنیاں framework اور اس کے **ایکو سسٹم** کو صحت مند اور **پائیدار** رکھنے میں مدد کرتی ہیں۔

ان کی اسپانسرشپ FastAPI **کمیونٹی** (آپ) کے ساتھ مضبوط وابستگی بھی ظاہر کرتی ہے، یہ دکھاتے ہوئے کہ وہ نہ صرف **بہترین سروس** فراہم کرنے بلکہ ایک **مضبوط اور ترقی پذیر framework**، FastAPI، کو سپورٹ کرنے میں بھی دلچسپی رکھتے ہیں۔

مثال کے طور پر، آپ آزما سکتے ہیں:

* [Speakeasy](https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship)
* [Stainless](https://www.stainless.com/?utm_source=fastapi&utm_medium=referral)
* [liblab](https://developers.liblab.com/tutorials/sdk-for-fastapi?utm_source=fastapi)

ان میں سے کچھ حل اوپن سورس بھی ہو سکتے ہیں یا مفت درجے پیش کر سکتے ہیں، تو آپ انہیں بغیر مالی وابستگی کے آزما سکتے ہیں۔ دیگر تجارتی SDK generators بھی دستیاب ہیں اور آن لائن مل سکتے ہیں۔

## TypeScript SDK بنائیں { #create-a-typescript-sdk }

آئیے ایک سادہ FastAPI ایپلیکیشن سے شروع کریں:

{* ../../docs_src/generate_clients/tutorial001_py310.py hl[7:9,12:13,16:17,21] *}

غور کریں کہ *path operations* اپنے استعمال شدہ models کو request payload اور response payload کے لیے بیان کرتے ہیں، `Item` اور `ResponseMessage` models استعمال کرتے ہوئے۔

### API Docs { #api-docs }

اگر آپ `/docs` پر جائیں تو آپ دیکھیں گے کہ اس میں requests میں بھیجے جانے والے اور responses میں وصول ہونے والے ڈیٹا کے **schemas** موجود ہیں:

<img src="/img/tutorial/generate-clients/image01.png">

آپ وہ schemas اس لیے دیکھ سکتے ہیں کیونکہ وہ ایپ میں models کے ساتھ بیان کیے گئے تھے۔

وہ معلومات ایپ کے **OpenAPI schema** میں دستیاب ہیں، اور پھر API docs میں دکھائی جاتی ہیں۔

OpenAPI میں شامل models کی وہی معلومات **client کوڈ بنانے** کے لیے استعمال ہو سکتی ہیں۔

### Hey API { #hey-api }

جب ہمارے پاس models والی FastAPI ایپ ہو تو ہم TypeScript client بنانے کے لیے Hey API استعمال کر سکتے ہیں۔ اس کا سب سے تیز طریقہ npx کے ذریعے ہے۔

```sh
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

یہ `./src/client` میں TypeScript SDK بنائے گا۔

آپ [`@hey-api/openapi-ts` انسٹال کرنے](https://heyapi.dev/openapi-ts/get-started) اور [بنائے گئے output](https://heyapi.dev/openapi-ts/output) کے بارے میں ان کی ویب سائٹ پر پڑھ سکتے ہیں۔

### SDK استعمال کرنا { #using-the-sdk }

اب آپ client کوڈ import اور استعمال کر سکتے ہیں۔ یہ کچھ اس طرح نظر آ سکتا ہے، غور کریں کہ آپ کو methods کے لیے autocompletion ملتا ہے:

<img src="/img/tutorial/generate-clients/image02.png">

آپ کو بھیجے جانے والے payload کے لیے بھی autocompletion ملے گا:

<img src="/img/tutorial/generate-clients/image03.png">

/// tip | مشورہ

`name` اور `price` کے لیے autocompletion غور کریں، جو FastAPI ایپلیکیشن میں `Item` model میں بیان کیے گئے تھے۔

///

آپ کو بھیجے جانے والے ڈیٹا کے لیے inline errors بھی ملیں گے:

<img src="/img/tutorial/generate-clients/image04.png">

response آبجیکٹ میں بھی autocompletion ہوگا:

<img src="/img/tutorial/generate-clients/image05.png">

## Tags کے ساتھ FastAPI ایپ { #fastapi-app-with-tags }

بہت سے معاملات میں، آپ کی FastAPI ایپ بڑی ہوگی، اور آپ شاید *path operations* کے مختلف گروپس الگ کرنے کے لیے tags استعمال کریں گے۔

مثال کے طور پر، آپ کے پاس **items** کا سیکشن اور **users** کا الگ سیکشن ہو سکتا ہے، اور وہ tags سے الگ ہو سکتے ہیں:

{* ../../docs_src/generate_clients/tutorial002_py310.py hl[21,26,34] *}

### Tags کے ساتھ TypeScript Client بنائیں { #generate-a-typescript-client-with-tags }

اگر آپ tags استعمال کرنے والی FastAPI ایپ کے لیے client بنائیں، تو یہ عام طور پر tags کی بنیاد پر client کوڈ کو الگ بھی کرے گا۔

اس طریقے سے، آپ کو client کوڈ میں چیزیں درست ترتیب اور گروپنگ میں ملیں گی:

<img src="/img/tutorial/generate-clients/image06.png">

اس صورت میں، آپ کے پاس ہیں:

* `ItemsService`
* `UsersService`

### Client Method کے نام { #client-method-names }

اس وقت، بنائے گئے method کے نام جیسے `createItemItemsPost` بہت صاف نہیں لگتے:

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...اس کی وجہ یہ ہے کہ client generator ہر *path operation* کے لیے OpenAPI کا اندرونی **operation ID** استعمال کرتا ہے۔

OpenAPI تقاضا کرتا ہے کہ ہر operation ID تمام *path operations* میں منفرد ہو، اس لیے FastAPI اس operation ID کو بنانے کے لیے **function کا نام**، **path**، اور **HTTP method/operation** استعمال کرتا ہے، کیونکہ اس طرح یہ یقینی بنا سکتا ہے کہ operation IDs منفرد ہیں۔

لیکن میں آپ کو اگلے حصے میں دکھاؤں گا کہ اسے کیسے بہتر بنائیں۔

## حسب ضرورت Operation IDs اور بہتر Method نام { #custom-operation-ids-and-better-method-names }

آپ ان operation IDs کی **بنانے کے طریقے کو تبدیل** کر سکتے ہیں تاکہ وہ آسان ہوں اور clients میں **آسان method نام** ہوں۔

اس صورت میں، آپ کو یقینی بنانا ہوگا کہ ہر operation ID کسی اور طریقے سے **منفرد** ہو۔

مثال کے طور پر، آپ یقینی بنا سکتے ہیں کہ ہر *path operation* میں ایک tag ہو، اور پھر **tag** اور *path operation* کے **نام** (function نام) کی بنیاد پر operation ID بنائیں۔

### حسب ضرورت Unique ID Function بنائیں { #custom-generate-unique-id-function }

FastAPI ہر *path operation* کے لیے ایک **unique ID** استعمال کرتا ہے، جو **operation ID** کے لیے اور requests یا responses کے لیے کسی ضروری حسب ضرورت models کے ناموں کے لیے بھی استعمال ہوتا ہے۔

آپ اس function کو حسب ضرورت بنا سکتے ہیں۔ یہ ایک `APIRoute` لیتا ہے اور string واپس کرتا ہے۔

مثال کے طور پر، یہاں یہ پہلا tag (آپ کے پاس شاید صرف ایک tag ہوگا) اور *path operation* کا نام (function نام) استعمال کر رہا ہے۔

پھر آپ اس حسب ضرورت function کو **FastAPI** کو `generate_unique_id_function` parameter کے طور پر پاس کر سکتے ہیں:

{* ../../docs_src/generate_clients/tutorial003_py310.py hl[6:7,10] *}

### حسب ضرورت Operation IDs کے ساتھ TypeScript Client بنائیں { #generate-a-typescript-client-with-custom-operation-ids }

اب، اگر آپ دوبارہ client بنائیں تو آپ دیکھیں گے کہ اس میں بہتر method نام ہیں:

<img src="/img/tutorial/generate-clients/image07.png">

جیسا کہ آپ دیکھ سکتے ہیں، method ناموں میں اب tag اور پھر function نام ہے، اب ان میں URL path اور HTTP operation کی معلومات شامل نہیں ہیں۔

### Client Generator کے لیے OpenAPI Specification پری پروسیس کریں { #preprocess-the-openapi-specification-for-the-client-generator }

بنائے گئے کوڈ میں ابھی بھی کچھ **دہرائی ہوئی معلومات** ہیں۔

ہم پہلے ہی جانتے ہیں کہ یہ method **items** سے متعلق ہے کیونکہ وہ لفظ `ItemsService` (tag سے لیا گیا) میں ہے، لیکن method نام میں بھی tag نام prefix ہے۔

ہم شاید اسے عام طور پر OpenAPI کے لیے رکھنا چاہیں گے، کیونکہ یہ یقینی بنائے گا کہ operation IDs **منفرد** ہیں۔

لیکن بنائے گئے client کے لیے، ہم clients بنانے سے بالکل پہلے OpenAPI operation IDs **تبدیل** کر سکتے ہیں، تاکہ وہ method نام بہتر اور **صاف** ہوں۔

ہم OpenAPI JSON کو `openapi.json` فائل میں ڈاؤن لوڈ کر سکتے ہیں اور پھر اس script سے **وہ prefix tag ہٹا** سکتے ہیں:

{* ../../docs_src/generate_clients/tutorial004_py310.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

اس سے، operation IDs `items-get_items` جیسی چیزوں سے صرف `get_items` میں تبدیل ہو جائیں گے، اس طریقے سے client generator آسان method نام بنا سکتا ہے۔

### پری پروسیس شدہ OpenAPI کے ساتھ TypeScript Client بنائیں { #generate-a-typescript-client-with-the-preprocessed-openapi }

چونکہ آخری نتیجہ اب `openapi.json` فائل میں ہے، آپ کو اپنی input location اپ ڈیٹ کرنی ہوگی:

```sh
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

نیا client بنانے کے بعد، آپ کے پاس اب **صاف method نام** ہوں گے، تمام **autocompletion**، **inline errors** وغیرہ کے ساتھ:

<img src="/img/tutorial/generate-clients/image08.png">

## فوائد { #benefits }

خود بخود بنائے گئے clients استعمال کرتے وقت آپ کو **autocompletion** ملے گا:

* Methods کے لیے۔
* Body میں Request payloads، query parameters وغیرہ کے لیے۔
* Response payloads کے لیے۔

آپ کو ہر چیز کے لیے **inline errors** بھی ملیں گے۔

اور جب بھی آپ backend کوڈ اپ ڈیٹ کریں، اور frontend **دوبارہ بنائیں**، اس میں تمام نئی *path operations* methods کے طور پر دستیاب ہوں گی، پرانی ہٹ جائیں گی، اور کوئی بھی تبدیلی بنائے گئے کوڈ میں ظاہر ہوگی۔

اس کا مطلب یہ بھی ہے کہ اگر کچھ بدلا تو یہ خود بخود client کوڈ میں **ظاہر** ہوگا۔ اور اگر آپ client **بلڈ** کریں تو اگر استعمال شدہ ڈیٹا میں کوئی **مماثلت نہ ہو** تو غلطی آئے گی۔

تو، آپ ترقیاتی عمل میں بہت جلد **بہت سی غلطیاں پکڑ** لیں گے بجائے اس کے کہ غلطیاں پروڈکشن میں آپ کے آخری صارفین کو نظر آئیں اور پھر آپ مسئلے کی تشخیص کرنے کی کوشش کریں۔
