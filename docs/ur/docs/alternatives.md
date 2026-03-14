# متبادل، تحریک اور موازنے { #alternatives-inspiration-and-comparisons }

**FastAPI** کو کس چیز نے تحریک دی، یہ متبادل سے کیسے موازنہ کرتا ہے اور اس نے ان سے کیا سیکھا۔

## تعارف { #intro }

**FastAPI** موجود نہ ہوتا اگر دوسروں کا پچھلا کام نہ ہوتا۔

پہلے بہت سے tools بنائے گئے ہیں جنہوں نے اس کی تخلیق کی تحریک دی۔

میں کئی سالوں سے نیا framework بنانے سے گریز کرتا رہا۔ پہلے میں نے **FastAPI** کی تمام features کو بہت سے مختلف frameworks، plug-ins، اور tools استعمال کرکے حل کرنے کی کوشش کی۔

لیکن کسی وقت، کوئی اور راستہ نہیں تھا سوائے اس کے کہ کچھ ایسا بنایا جائے جو یہ تمام features فراہم کرے، پچھلے tools سے بہترین آئیڈیاز لے کر، اور انہیں بہترین ممکنہ طریقے سے ملا کر، زبان کی ان features کو استعمال کرتے ہوئے جو پہلے دستیاب نہیں تھیں (Python 3.6+ type hints)۔

## پچھلے tools { #previous-tools }

### [Django](https://www.djangoproject.com/) { #django }

یہ سب سے مقبول Python framework ہے اور وسیع پیمانے پر قابل اعتماد ہے۔ اسے Instagram جیسے systems بنانے کے لیے استعمال کیا جاتا ہے۔

یہ relational databases (جیسے MySQL یا PostgreSQL) کے ساتھ نسبتاً مضبوطی سے جڑا ہوا ہے، تو NoSQL database (جیسے Couchbase، MongoDB، Cassandra وغیرہ) کو بنیادی storage engine کے طور پر رکھنا بہت آسان نہیں ہے۔

یہ backend میں HTML بنانے کے لیے بنایا گیا تھا، نہ کہ جدید frontend (جیسے React، Vue.js اور Angular) یا دوسرے systems (جیسے <abbr title="Internet of Things">IoT</abbr> devices) کے ذریعے استعمال ہونے والی APIs بنانے کے لیے۔

### [Django REST Framework](https://www.django-rest-framework.org/) { #django-rest-framework }

Django REST framework اس لیے بنایا گیا تاکہ Django کے نیچے استعمال کرتے ہوئے Web APIs بنانے کا ایک لچکدار toolkit فراہم کیا جائے، تاکہ اس کی API صلاحیتوں کو بہتر بنایا جا سکے۔

اسے Mozilla، Red Hat اور Eventbrite سمیت بہت سی کمپنیاں استعمال کرتی ہیں۔

یہ **خودکار API documentation** کی پہلی مثالوں میں سے ایک تھا، اور یہ خاص طور پر ان پہلے آئیڈیاز میں سے ایک تھا جنہوں نے **FastAPI** کی "تلاش" کی تحریک دی۔

/// note | نوٹ

Django REST Framework Tom Christie نے بنایا تھا۔ Starlette اور Uvicorn کے وہی بانی، جن پر **FastAPI** مبنی ہے۔

///

/// check | **FastAPI** کو تحریک دی

خودکار API documentation web user interface رکھنے کی۔

///

### [Flask](https://flask.palletsprojects.com) { #flask }

Flask ایک "microframework" ہے، اس میں database integrations یا وہ بہت سی چیزیں شامل نہیں ہیں جو Django میں بطور default آتی ہیں۔

اس سادگی اور لچک کی وجہ سے NoSQL databases کو بنیادی data storage system کے طور پر استعمال کرنا ممکن ہوتا ہے۔

چونکہ یہ بہت سادہ ہے، سیکھنا نسبتاً بدیہی ہے، حالانکہ documentation کچھ مقامات پر تکنیکی ہو جاتی ہے۔

اسے عام طور پر ان applications کے لیے بھی استعمال کیا جاتا ہے جن کو ضروری نہیں کہ database، user management، یا Django میں پہلے سے بنی بہت سی features کی ضرورت ہو۔ حالانکہ ان میں سے بہت سی features plug-ins کے ساتھ شامل کی جا سکتی ہیں۔

حصوں کی یہ علیحدگی، اور ایک "microframework" ہونا جسے بالکل ضرورت کے مطابق بڑھایا جا سکے، ایک اہم خصوصیت تھی جسے میں برقرار رکھنا چاہتا تھا۔

Flask کی سادگی کو دیکھتے ہوئے، یہ APIs بنانے کے لیے اچھا انتخاب لگا۔ اگلی چیز Flask کے لیے ایک "Django REST Framework" تلاش کرنا تھی۔

/// check | **FastAPI** کو تحریک دی

ایک micro-framework ہونے کی۔ ضرورت کے مطابق tools اور حصوں کو ملانا آسان بنانے کی۔

سادہ اور استعمال میں آسان routing system رکھنے کی۔

///

### [Requests](https://requests.readthedocs.io) { #requests }

**FastAPI** دراصل **Requests** کا متبادل نہیں ہے۔ ان کا دائرہ کار بہت مختلف ہے۔

درحقیقت FastAPI application کے *اندر* Requests استعمال کرنا عام ہوگا۔

لیکن پھر بھی، FastAPI نے Requests سے کافی تحریک لی۔

**Requests** APIs کے ساتھ *تعامل* کرنے (بطور client) کی library ہے، جبکہ **FastAPI** APIs *بنانے* (بطور server) کی library ہے۔

وہ کم و بیش مخالف سروں پر ہیں، ایک دوسرے کی تکمیل کرتے ہیں۔

Requests کا بہت سادہ اور بدیہی ڈیزائن ہے، یہ استعمال میں بہت آسان ہے، معقول defaults کے ساتھ۔ لیکن ساتھ ہی، یہ بہت طاقتور اور حسب ضرورت بنانے کے قابل ہے۔

اسی لیے، جیسا کہ سرکاری ویب سائٹ پر کہا گیا ہے:

> Requests ہر وقت کے سب سے زیادہ download کیے جانے والے Python packages میں سے ایک ہے

اسے استعمال کرنے کا طریقہ بہت سادہ ہے۔ مثال کے طور پر، `GET` request کرنے کے لیے، آپ یہ لکھیں گے:

```Python
response = requests.get("http://example.com/some/url")
```

FastAPI کا مساوی API *path operation* اس طرح نظر آ سکتا ہے:

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

`requests.get(...)` اور `@app.get(...)` میں مماثلت دیکھیں۔

/// check | **FastAPI** کو تحریک دی

* سادہ اور بدیہی API رکھنے کی۔
* HTTP method names (operations) کو براہ راست، سیدھے اور بدیہی طریقے سے استعمال کرنے کی۔
* معقول defaults رکھنے کی، لیکن طاقتور customizations کے ساتھ۔

///

### [Swagger](https://swagger.io/) / [OpenAPI](https://github.com/OAI/OpenAPI-Specification/) { #swagger-openapi }

Django REST Framework سے مجھے جو بنیادی feature چاہیے تھا وہ خودکار API documentation تھا۔

پھر مجھے پتا چلا کہ JSON (یا YAML، JSON کی ایک extension) استعمال کرکے APIs کو document کرنے کا ایک standard ہے جسے Swagger کہتے ہیں۔

اور Swagger APIs کے لیے ایک web user interface پہلے سے بنایا گیا تھا۔ تو، کسی API کے لیے Swagger documentation بنا سکنے سے اس web user interface کو خودکار طور پر استعمال کرنا ممکن ہو جائے گا۔

کسی وقت، Swagger کو Linux Foundation کو دے دیا گیا، اور اس کا نام OpenAPI رکھا گیا۔

اسی لیے ورژن 2.0 کے بارے میں بات کرتے وقت عام طور پر "Swagger" کہا جاتا ہے، اور ورژن 3+ کے لیے "OpenAPI"۔

/// check | **FastAPI** کو تحریک دی

API specifications کے لیے ایک کھلا standard اپنانے اور استعمال کرنے کی، حسب ضرورت schema کی بجائے۔

اور standards پر مبنی user interface tools کو مربوط کرنے کی:

* [Swagger UI](https://github.com/swagger-api/swagger-ui)
* [ReDoc](https://github.com/Rebilly/ReDoc)

یہ دونوں کافی مقبول اور مستحکم ہونے کی وجہ سے منتخب کیے گئے، لیکن تیز تلاش سے آپ OpenAPI کے لیے درجنوں متبادل user interfaces تلاش کر سکتے ہیں (جنہیں آپ **FastAPI** کے ساتھ استعمال کر سکتے ہیں)۔

///

### Flask REST frameworks { #flask-rest-frameworks }

کئی Flask REST frameworks ہیں، لیکن ان کی تحقیق میں وقت اور محنت لگانے کے بعد، میں نے پایا کہ بہت سے بند یا ترک کر دیے گئے ہیں، کئی کھڑے مسائل کے ساتھ جو انہیں ناموزوں بناتے ہیں۔

### [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) { #marshmallow }

API systems کی ایک بنیادی ضرورت data "<dfn title="also called marshalling, conversion">serialization</dfn>" ہے جو code (Python) سے data لے کر اسے network پر بھیجی جا سکنے والی چیز میں تبدیل کرتی ہے۔ مثلاً، database سے data رکھنے والے object کو JSON object میں تبدیل کرنا۔ `datetime` objects کو strings میں تبدیل کرنا، وغیرہ۔

APIs کی ایک اور بڑی ضرورت data validation ہے، یہ یقینی بنانا کہ data درست ہے مخصوص parameters کے مطابق۔ مثلاً، کوئی field `int` ہے نہ کہ کوئی random string۔ یہ آنے والے data کے لیے خاص طور پر مفید ہے۔

Data validation system کے بغیر، آپ کو code میں تمام checks خود کرنے ہوں گے۔

یہی features ہیں جو Marshmallow فراہم کرنے کے لیے بنایا گیا تھا۔ یہ ایک بہترین library ہے، اور میں نے اسے پہلے بہت استعمال کیا ہے۔

لیکن یہ Python type hints سے پہلے بنایا گیا تھا۔ تو ہر <dfn title="the definition of how data should be formed">schema</dfn> define کرنے کے لیے Marshmallow کی فراہم کردہ مخصوص utils اور classes استعمال کرنی ہوتی ہیں۔

/// check | **FastAPI** کو تحریک دی

Data types اور validation فراہم کرنے والے "schemas" define کرنے کے لیے code استعمال کرنے کی، خودکار طور پر۔

///

### [Webargs](https://webargs.readthedocs.io/en/latest/) { #webargs }

APIs کی ایک اور بڑی ضرورت آنے والی requests سے data <dfn title="reading and converting to Python data">parsing</dfn> ہے۔

Webargs ایک tool ہے جو کئی frameworks بشمول Flask کے اوپر یہ سہولت فراہم کرنے کے لیے بنایا گیا تھا۔

یہ data validation کے لیے Marshmallow استعمال کرتا ہے۔ اور اسے انہی developers نے بنایا تھا۔

یہ ایک بہترین tool ہے اور میں نے اسے بھی **FastAPI** سے پہلے بہت استعمال کیا ہے۔

/// info | معلومات

Webargs وہی Marshmallow developers نے بنایا تھا۔

///

/// check | **FastAPI** کو تحریک دی

آنے والے request data کی خودکار validation رکھنے کی۔

///

### [APISpec](https://apispec.readthedocs.io/en/stable/) { #apispec }

Marshmallow اور Webargs plug-ins کے طور پر validation، parsing اور serialization فراہم کرتے ہیں۔

لیکن documentation ابھی بھی نہیں تھی۔ پھر APISpec بنایا گیا۔

یہ بہت سے frameworks کے لیے plug-in ہے (اور Starlette کے لیے بھی ایک plug-in ہے)۔

یہ اس طرح کام کرتا ہے کہ آپ route handle کرنے والے ہر function کی docstring میں YAML فارمیٹ استعمال کرکے schema کی definition لکھتے ہیں۔

اور یہ OpenAPI schemas بناتا ہے۔

Flask، Starlette، Responder وغیرہ میں یہی طریقہ ہے۔

لیکن پھر، ہمارے پاس دوبارہ Python string (ایک بڑا YAML) کے اندر ایک micro-syntax کا مسئلہ ہے۔

Editor اس میں زیادہ مدد نہیں کر سکتا۔ اور اگر ہم parameters یا Marshmallow schemas تبدیل کریں اور وہ YAML docstring بھی اپڈیٹ کرنا بھول جائیں، تو بنایا گیا schema متروک ہو جائے گا۔

/// info | معلومات

APISpec وہی Marshmallow developers نے بنایا تھا۔

///

/// check | **FastAPI** کو تحریک دی

APIs کے لیے کھلے standard، OpenAPI، کی حمایت کرنے کی۔

///

### [Flask-apispec](https://flask-apispec.readthedocs.io/en/latest/) { #flask-apispec }

یہ ایک Flask plug-in ہے، جو Webargs، Marshmallow اور APISpec کو جوڑتا ہے۔

یہ Webargs اور Marshmallow سے معلومات استعمال کرکے APISpec کے ذریعے خودکار OpenAPI schemas بناتا ہے۔

یہ ایک بہترین tool ہے، بہت کم قدردانی حاصل۔ اسے وہاں بہت سے Flask plug-ins سے زیادہ مقبول ہونا چاہیے۔ اس کی وجہ شاید اس کی documentation کا بہت مختصر اور تجریدی ہونا ہے۔

اس نے Python docstrings کے اندر YAML (ایک اور syntax) لکھنے کا مسئلہ حل کیا۔

Flask، Flask-apispec بمع Marshmallow اور Webargs کا یہ مجموعہ **FastAPI** بنانے تک میرا پسندیدہ backend stack تھا۔

اسے استعمال کرنے سے کئی Flask full-stack generators بنے۔ یہ وہ بنیادی stacks ہیں جو میں (اور کئی بیرونی ٹیمیں) اب تک استعمال کرتے رہے ہیں:

* [https://github.com/tiangolo/full-stack](https://github.com/tiangolo/full-stack)
* [https://github.com/tiangolo/full-stack-flask-couchbase](https://github.com/tiangolo/full-stack-flask-couchbase)
* [https://github.com/tiangolo/full-stack-flask-couchdb](https://github.com/tiangolo/full-stack-flask-couchdb)

اور یہی full-stack generators [**FastAPI** Project Generators](project-generation.md) کی بنیاد تھے۔

/// info | معلومات

Flask-apispec وہی Marshmallow developers نے بنایا تھا۔

///

/// check | **FastAPI** کو تحریک دی

اسی code سے جو serialization اور validation define کرتا ہے، خودکار طور پر OpenAPI schema بنانے کی۔

///

### [NestJS](https://nestjs.com/) (اور [Angular](https://angular.io/)) { #nestjs-and-angular }

یہ Python بھی نہیں ہے، NestJS ایک JavaScript (TypeScript) NodeJS framework ہے جو Angular سے تحریک یافتہ ہے۔

یہ کچھ حد تک ایسا ہی حاصل کرتا ہے جو Flask-apispec سے کیا جا سکتا ہے۔

اس میں Angular 2 سے تحریک یافتہ ایک مربوط dependency injection system ہے۔ اسے "injectables" کو پہلے سے register کرنا ضروری ہے (جیسے میں جانتا ہوں تمام dependency injection systems)، تو یہ طوالت اور code کی تکرار میں اضافہ کرتا ہے۔

چونکہ parameters TypeScript types سے بیان کیے جاتے ہیں (Python type hints کی طرح)، editor support کافی اچھا ہے۔

لیکن چونکہ TypeScript data JavaScript میں compile ہونے کے بعد محفوظ نہیں رہتا، یہ validation، serialization اور documentation ایک ساتھ define کرنے کے لیے types پر انحصار نہیں کر سکتا۔ اس اور کچھ design فیصلوں کی وجہ سے، validation، serialization اور خودکار schema generation حاصل کرنے کے لیے بہت سی جگہوں پر decorators شامل کرنے ہوتے ہیں۔ تو یہ کافی طویل ہو جاتا ہے۔

یہ nested models کو بہت اچھی طرح سنبھال نہیں سکتا۔ تو اگر request میں JSON body ایک JSON object ہے جس میں اندر کے fields بدلے میں nested JSON objects ہیں، تو اسے ٹھیک سے document اور validate نہیں کیا جا سکتا۔

/// check | **FastAPI** کو تحریک دی

بہترین editor support حاصل کرنے کے لیے Python types استعمال کرنے کی۔

طاقتور dependency injection system رکھنے کی۔ Code کی تکرار کم کرنے کا طریقہ ڈھونڈنے کی۔

///

### [Sanic](https://sanic.readthedocs.io/en/latest/) { #sanic }

یہ `asyncio` پر مبنی انتہائی تیز Python frameworks میں سے پہلے تھا۔ اسے Flask سے بہت ملتا جلتا بنایا گیا تھا۔

/// note | تکنیکی تفصیلات

اس نے default Python `asyncio` loop کی بجائے [`uvloop`](https://github.com/MagicStack/uvloop) استعمال کیا۔ یہی اسے اتنا تیز بنایا۔

اس نے واضح طور پر Uvicorn اور Starlette کو تحریک دی، جو فی الحال کھلے benchmarks میں Sanic سے تیز ہیں۔

///

/// check | **FastAPI** کو تحریک دی

زبردست performance حاصل کرنے کا طریقہ ڈھونڈنے کی۔

اسی لیے **FastAPI** Starlette پر مبنی ہے، کیونکہ یہ دستیاب تیز ترین framework ہے (third-party benchmarks سے ٹیسٹ شدہ)۔

///

### [Falcon](https://falconframework.org/) { #falcon }

Falcon ایک اور اعلیٰ performance Python framework ہے، اسے کم سے کم ہونے کے لیے ڈیزائن کیا گیا ہے، اور دوسرے frameworks جیسے Hug کی بنیاد کے طور پر کام کرنے کے لیے۔

اسے ایسے functions رکھنے کے لیے ڈیزائن کیا گیا ہے جو دو parameters وصول کرتے ہیں، ایک "request" اور ایک "response"۔ پھر آپ request سے حصے "پڑھتے" ہیں، اور response میں حصے "لکھتے" ہیں۔ اس ڈیزائن کی وجہ سے، function parameters کے طور پر standard Python type hints کے ساتھ request parameters اور bodies declare کرنا ممکن نہیں ہے۔

تو data validation، serialization، اور documentation code میں کرنی ہوتی ہے، خودکار طور پر نہیں۔ یا انہیں Falcon کے اوپر framework کے طور پر implement کرنا ہوتا ہے، جیسے Hug۔ یہی فرق ان دوسرے frameworks میں ہوتا ہے جو Falcon کے ڈیزائن سے تحریک یافتہ ہیں، ایک request object اور ایک response object بطور parameters رکھنے کا۔

/// check | **FastAPI** کو تحریک دی

بہترین performance حاصل کرنے کے طریقے ڈھونڈنے کی۔

Hug کے ساتھ مل کر (چونکہ Hug، Falcon پر مبنی ہے) **FastAPI** کو functions میں `response` parameter declare کرنے کی تحریک دی۔

حالانکہ FastAPI میں یہ اختیاری ہے، اور بنیادی طور پر headers، cookies، اور متبادل status codes سیٹ کرنے کے لیے استعمال ہوتا ہے۔

///

### [Molten](https://moltenframework.com/) { #molten }

میں نے **FastAPI** بنانے کے ابتدائی مراحل میں Molten دریافت کیا۔ اور اس کے کافی ملتے جلتے آئیڈیاز ہیں:

* Python type hints پر مبنی۔
* ان types سے validation اور documentation۔
* Dependency Injection system۔

یہ Pydantic جیسی data validation، serialization اور documentation third-party library استعمال نہیں کرتا، بلکہ اس کی اپنی ہے۔ تو یہ data type definitions آسانی سے دوبارہ استعمال نہیں ہوتیں۔

اسے تھوڑی زیادہ verbose configurations کی ضرورت ہے۔ اور چونکہ یہ WSGI (ASGI کی بجائے) پر مبنی ہے، اسے Uvicorn، Starlette اور Sanic جیسے tools کی اعلیٰ performance کا فائدہ اٹھانے کے لیے ڈیزائن نہیں کیا گیا۔

Dependency injection system dependencies کو پہلے سے register کرنے اور declare کیے گئے types کی بنیاد پر resolve کرنے کی ضرورت ہے۔ تو ایک مخصوص type فراہم کرنے والے ایک سے زیادہ "component" declare کرنا ممکن نہیں ہے۔

Routes ایک ہی جگہ declare کیے جاتے ہیں، دوسری جگہوں پر declare کیے گئے functions کا استعمال کرتے ہوئے (endpoint handle کرنے والے function کے بالکل اوپر رکھے جا سکنے والے decorators استعمال کرنے کی بجائے)۔ یہ Django کے طریقے سے زیادہ قریب ہے بنسبت Flask (اور Starlette) کے۔ یہ code میں ان چیزوں کو الگ کرتا ہے جو نسبتاً مضبوطی سے جڑی ہوتی ہیں۔

/// check | **FastAPI** کو تحریک دی

Model attributes کی "default" value استعمال کرکے data types کے لیے اضافی validations define کرنے کی۔ اس سے editor support بہتر ہوا، اور یہ پہلے Pydantic میں دستیاب نہیں تھا۔

اس نے دراصل Pydantic کے حصے اپڈیٹ کرنے کی تحریک دی، تاکہ وہی validation declaration style سہولت فراہم ہو (یہ ساری functionality اب پہلے سے Pydantic میں دستیاب ہے)۔

///

### [Hug](https://github.com/hugapi/hug) { #hug }

Hug ان پہلے frameworks میں سے ایک تھا جنہوں نے Python type hints استعمال کرکے API parameter types declare کرنا implement کیا۔ یہ ایک زبردست آئیڈیا تھا جس نے دوسرے tools کو بھی ایسا کرنے کی تحریک دی۔

اس نے اپنی declarations میں standard Python types کی بجائے custom types استعمال کیے، لیکن یہ پھر بھی آگے کی طرف ایک بڑا قدم تھا۔

یہ JSON میں API کی پوری declaration کا ایک custom schema بنانے والے پہلے frameworks میں سے بھی تھا۔

یہ OpenAPI اور JSON Schema جیسے standard پر مبنی نہیں تھا۔ تو اسے Swagger UI جیسے دوسرے tools کے ساتھ مربوط کرنا سیدھا نہیں ہوتا۔ لیکن پھر بھی، یہ ایک بہت اختراعی آئیڈیا تھا۔

اس میں ایک دلچسپ، غیر معمولی feature ہے: ایک ہی framework استعمال کرکے APIs اور CLIs دونوں بنانا ممکن ہے۔

چونکہ یہ synchronous Python web frameworks کے پچھلے standard (WSGI) پر مبنی ہے، یہ Websockets اور دوسری چیزیں سنبھال نہیں سکتا، حالانکہ اس کی performance بھی اعلیٰ ہے۔

/// info | معلومات

Hug Timothy Crosley نے بنایا تھا، [`isort`](https://github.com/timothycrosley/isort) کے وہی بانی، Python فائلوں میں imports کو خودکار ترتیب دینے کا ایک بہترین tool۔

///

/// check | **FastAPI** کو تحریک دینے والے آئیڈیاز

Hug نے APIStar کے حصوں کی تحریک دی، اور وہ tools میں سے ایک تھا جو مجھے APIStar کے ساتھ سب سے زیادہ امید افزا لگا۔

Hug نے **FastAPI** کو Python type hints استعمال کرکے parameters declare کرنے، اور API define کرنے والا schema خودکار بنانے کی تحریک دی۔

Hug نے **FastAPI** کو functions میں `response` parameter declare کرنے کی تحریک دی تاکہ headers اور cookies سیٹ کیے جا سکیں۔

///

### [APIStar](https://github.com/encode/apistar) (<= 0.5) { #apistar-0-5 }

**FastAPI** بنانے کا فیصلہ کرنے سے ٹھیک پہلے مجھے **APIStar** server ملا۔ اس میں تقریباً وہ سب کچھ تھا جو میں تلاش کر رہا تھا اور اس کا ایک بہترین ڈیزائن تھا۔

یہ parameters اور requests declare کرنے کے لیے Python type hints استعمال کرنے والے framework کے پہلے implementations میں سے ایک تھا جو میں نے کبھی دیکھا (NestJS اور Molten سے پہلے)۔ مجھے یہ تقریباً Hug کے ساتھ ہی ملا۔ لیکن APIStar نے OpenAPI standard استعمال کیا۔

اس میں کئی جگہوں پر ایک ہی type hints کی بنیاد پر خودکار data validation، data serialization اور OpenAPI schema generation تھی۔

Body schema definitions Pydantic کی طرح وہی Python type hints استعمال نہیں کرتی تھیں، یہ Marshmallow سے زیادہ ملتی جلتی تھیں، تو editor support اتنا اچھا نہ ہوتا، لیکن پھر بھی APIStar دستیاب بہترین آپشن تھا۔

اس وقت اس کے بہترین performance benchmarks تھے (صرف Starlette سے پیچھے)۔

شروع میں، اس کے پاس خودکار API documentation web UI نہیں تھا، لیکن مجھے معلوم تھا کہ میں اس میں Swagger UI شامل کر سکتا ہوں۔

اس کا dependency injection system تھا۔ اسے components کو پہلے سے register کرنا ضروری تھا، جیسے اوپر بیان کیے گئے دوسرے tools۔ لیکن پھر بھی، یہ ایک بہترین feature تھا۔

میں اسے کسی مکمل project میں استعمال نہیں کر سکا، کیونکہ اس میں security integration نہیں تھا، تو میں Flask-apispec پر مبنی full-stack generators کی تمام features کو replace نہیں کر سکتا تھا۔ میرے projects کے backlog میں وہ functionality شامل کرنے والی pull request بنانا تھا۔

لیکن پھر، project کی توجہ بدل گئی۔

یہ اب API web framework نہیں رہا، کیونکہ بانی کو Starlette پر توجہ مرکوز کرنی تھی۔

اب APIStar OpenAPI specifications کو validate کرنے والے tools کا مجموعہ ہے، web framework نہیں۔

/// info | معلومات

APIStar Tom Christie نے بنایا تھا۔ وہی شخص جس نے بنایا:

* Django REST Framework
* Starlette (جس پر **FastAPI** مبنی ہے)
* Uvicorn (جو Starlette اور **FastAPI** استعمال کرتے ہیں)

///

/// check | **FastAPI** کو تحریک دی

موجود ہونے کی۔

ایک ہی Python types کے ساتھ متعدد چیزیں (data validation، serialization اور documentation) declare کرنے کا آئیڈیا، جو ساتھ ہی بہترین editor support بھی فراہم کرے، ایک شاندار آئیڈیا تھا۔

اور لمبے عرصے تک ملتا جلتا framework تلاش کرنے اور بہت سے مختلف متبادل ٹیسٹ کرنے کے بعد، APIStar دستیاب بہترین آپشن تھا۔

پھر APIStar ایک server کے طور پر بند ہو گیا اور Starlette بنایا گیا، اور ایسے system کے لیے ایک نئی بہتر بنیاد تھا۔ یہ **FastAPI** بنانے کی حتمی تحریک تھی۔

میں **FastAPI** کو APIStar کا "روحانی جانشین" سمجھتا ہوں، جبکہ ان تمام پچھلے tools سے سیکھے گئے سبق کی بنیاد پر features، typing system، اور دوسرے حصوں کو بہتر اور بڑھاتے ہوئے۔

///

## **FastAPI** کے ذریعے استعمال شدہ { #used-by-fastapi }

### [Pydantic](https://docs.pydantic.dev/) { #pydantic }

Pydantic ایک library ہے جو Python type hints کی بنیاد پر data validation، serialization اور documentation (JSON Schema استعمال کرتے ہوئے) define کرتی ہے۔

یہ اسے انتہائی بدیہی بناتا ہے۔

یہ Marshmallow سے قابل موازنہ ہے۔ حالانکہ benchmarks میں یہ Marshmallow سے تیز ہے۔ اور چونکہ یہ وہی Python type hints پر مبنی ہے، editor support بہترین ہے۔

/// check | **FastAPI** اسے استعمال کرتا ہے

تمام data validation، data serialization اور خودکار model documentation (JSON Schema پر مبنی) سنبھالنے کے لیے۔

**FastAPI** پھر وہ JSON Schema data لے کر OpenAPI میں ڈالتا ہے، اس کے علاوہ جو کچھ اور یہ کرتا ہے۔

///

### [Starlette](https://www.starlette.dev/) { #starlette }

Starlette ایک ہلکا پھلکا <dfn title="The new standard for building asynchronous Python web applications">ASGI</dfn> framework/toolkit ہے، جو اعلیٰ performance asyncio services بنانے کے لیے مثالی ہے۔

یہ بہت سادہ اور بدیہی ہے۔ اسے آسانی سے قابل توسیع، اور ماڈیولر اجزاء کے ساتھ ڈیزائن کیا گیا ہے۔

اس کے پاس ہے:

* سنجیدگی سے شاندار performance۔
* WebSocket support۔
* In-process background tasks۔
* Startup اور shutdown events۔
* HTTPX پر مبنی Test client۔
* CORS، GZip، Static Files، Streaming responses۔
* Session اور Cookie support۔
* 100% test coverage۔
* 100% type annotated codebase۔
* بہت کم hard dependencies۔

Starlette فی الحال ٹیسٹ شدہ تیز ترین Python framework ہے۔ صرف Uvicorn سے پیچھے، جو framework نہیں بلکہ server ہے۔

Starlette تمام بنیادی web microframework functionality فراہم کرتا ہے۔

لیکن یہ خودکار data validation، serialization یا documentation فراہم نہیں کرتا۔

یہ ان بنیادی چیزوں میں سے ایک ہے جو **FastAPI** اوپر سے شامل کرتا ہے، سب Python type hints پر مبنی (Pydantic استعمال کرتے ہوئے)۔ یہ، اور dependency injection system، security utilities، OpenAPI schema generation وغیرہ۔

/// note | تکنیکی تفصیلات

ASGI ایک نیا "standard" ہے جو Django core ٹیم کے ممبران develop کر رہے ہیں۔ یہ ابھی تک "Python standard" (PEP) نہیں ہے، حالانکہ وہ اس کے عمل میں ہیں۔

تاہم، یہ پہلے سے کئی tools کے ذریعے "standard" کے طور پر استعمال ہو رہا ہے۔ یہ interoperability کو بہت بہتر بناتا ہے، کیونکہ آپ Uvicorn کو کسی بھی دوسرے ASGI server (جیسے Daphne یا Hypercorn) سے بدل سکتے ہیں، یا ASGI compatible tools شامل کر سکتے ہیں، جیسے `python-socketio`۔

///

/// check | **FastAPI** اسے استعمال کرتا ہے

تمام بنیادی web حصوں کو سنبھالنے کے لیے۔ اوپر features شامل کرتے ہوئے۔

`FastAPI` class خود براہ راست `Starlette` class سے inherit کرتی ہے۔

تو جو کچھ بھی آپ Starlette کے ساتھ کر سکتے ہیں، آپ براہ راست **FastAPI** کے ساتھ کر سکتے ہیں، کیونکہ یہ بنیادی طور پر Starlette ہے مگر طاقتور۔

///

### [Uvicorn](https://www.uvicorn.dev/) { #uvicorn }

Uvicorn ایک بجلی کی رفتار والا ASGI server ہے، uvloop اور httptools پر مبنی۔

یہ web framework نہیں بلکہ server ہے۔ مثلاً، یہ paths سے routing کے tools فراہم نہیں کرتا۔ یہ وہ چیز ہے جو Starlette (یا **FastAPI**) جیسا framework اوپر فراہم کرتا ہے۔

یہ Starlette اور **FastAPI** کے لیے تجویز کردہ server ہے۔

/// check | **FastAPI** اسے تجویز کرتا ہے بطور

**FastAPI** applications چلانے کا بنیادی web server۔

آپ `--workers` command line option بھی استعمال کر سکتے ہیں تاکہ asynchronous multi-process server ہو۔

مزید تفصیلات [Deployment](deployment/index.md) سیکشن میں دیکھیں۔

///

## Benchmarks اور رفتار { #benchmarks-and-speed }

Uvicorn، Starlette اور FastAPI کے درمیان فرق سمجھنے، موازنہ کرنے اور دیکھنے کے لیے [Benchmarks](benchmarks.md) کا سیکشن دیکھیں۔
