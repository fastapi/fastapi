# خصوصیات { #features }

## FastAPI کی خصوصیات { #fastapi-features }

**FastAPI** آپ کو درج ذیل فراہم کرتا ہے:

### کھلے معیارات پر مبنی { #based-on-open-standards }

* API بنانے کے لیے [**OpenAPI**](https://github.com/OAI/OpenAPI-Specification)، جس میں <dfn title="also known as: endpoints, routes">path</dfn> <dfn title="also known as HTTP methods, as POST, GET, PUT, DELETE">operations</dfn>، parameters، request bodies، security وغیرہ کے اعلانات شامل ہیں۔
* [**JSON Schema**](https://json-schema.org/) کے ساتھ خودکار data model دستاویزات (کیونکہ OpenAPI خود JSON Schema پر مبنی ہے)۔
* ان معیارات کے گرد ڈیزائن کیا گیا، بغور مطالعے کے بعد۔ بعد میں شامل کی گئی تہہ کے بجائے۔
* یہ کئی زبانوں میں خودکار **client code generation** کا استعمال بھی ممکن بناتا ہے۔

### خودکار دستاویزات { #automatic-docs }

تعاملی API دستاویزات اور ایکسپلوریشن ویب یوزر انٹرفیسز۔ چونکہ framework OpenAPI پر مبنی ہے، اس لیے کئی اختیارات موجود ہیں، جن میں سے 2 بطور ڈیفالٹ شامل ہیں۔

* [**Swagger UI**](https://github.com/swagger-api/swagger-ui)، تعاملی ایکسپلوریشن کے ساتھ، براؤزر سے براہ راست اپنی API کو کال اور ٹیسٹ کریں۔

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* [**ReDoc**](https://github.com/Rebilly/ReDoc) کے ساتھ متبادل API دستاویزات۔

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### صرف جدید Python { #just-modern-python }

یہ سب معیاری **Python type** اعلانات پر مبنی ہے (Pydantic کی بدولت)۔ کوئی نئی syntax سیکھنے کی ضرورت نہیں۔ بس معیاری جدید Python۔

اگر آپ کو Python types استعمال کرنے کا 2 منٹ کا جائزہ چاہیے (چاہے آپ FastAPI استعمال نہ کریں)، تو مختصر tutorial دیکھیں: [Python Types](python-types.md)۔

آپ types کے ساتھ معیاری Python لکھتے ہیں:

```Python
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

جسے پھر اس طرح استعمال کیا جا سکتا ہے:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

/// info | معلومات

`**second_user_data` کا مطلب ہے:

`second_user_data` dict کی keys اور values کو براہ راست key-value arguments کے طور پر پاس کریں، جو اس کے برابر ہے: `User(id=4, name="Mary", joined="2018-11-30")`

///

### ایڈیٹر سپورٹ { #editor-support }

پورا framework آسان اور بدیہی استعمال کے لیے ڈیزائن کیا گیا ہے، تمام فیصلے ترقی شروع کرنے سے پہلے ہی متعدد ایڈیٹرز پر آزمائے گئے تھے، تاکہ بہترین ترقیاتی تجربہ یقینی بنایا جا سکے۔

Python ڈویلپر سروے میں، یہ واضح ہے [کہ سب سے زیادہ استعمال ہونے والی خصوصیات میں سے ایک "autocompletion" ہے](https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features)۔

پورا **FastAPI** framework اسی کو پورا کرنے کے لیے بنایا گیا ہے۔ Autocompletion ہر جگہ کام کرتی ہے۔

آپ کو شاذ و نادر ہی دستاویزات کی طرف واپس آنا پڑے گا۔

یہاں آپ کا ایڈیٹر آپ کی مدد کیسے کر سکتا ہے:

* [Visual Studio Code](https://code.visualstudio.com/) میں:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* [PyCharm](https://www.jetbrains.com/pycharm/) میں:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

آپ کو ایسے code میں بھی completion ملے گی جو آپ پہلے ناممکن سمجھتے تھے۔ مثال کے طور پر، request سے آنے والے JSON body (جو nested ہو سکتا تھا) کے اندر `price` key۔

غلط key نام ٹائپ کرنا، دستاویزات میں آگے پیچھے جانا، یا اوپر نیچے سکرول کرنا کہ آخرکار آپ نے `username` استعمال کیا یا `user_name`، اب ایسا نہیں ہوگا۔

### مختصر { #short }

ہر چیز کے لیے سمجھدار **defaults** ہیں، ہر جگہ اختیاری ترتیبات کے ساتھ۔ تمام parameters کو آپ کی ضرورت کے مطابق ایڈجسٹ کیا جا سکتا ہے اور آپ جو API چاہیں اس کی تعریف کر سکتے ہیں۔

لیکن بطور ڈیفالٹ، سب کچھ **"بس کام کرتا ہے"**۔

### توثیق { #validation }

* زیادہ تر (یا تمام؟) Python **data types** کے لیے توثیق، بشمول:
    * JSON objects (`dict`)۔
    * JSON array (`list`) آئٹم types کی تعریف کے ساتھ۔
    * String (`str`) فیلڈز، کم از کم اور زیادہ سے زیادہ طوالت کی تعریف کے ساتھ۔
    * Numbers (`int`, `float`) کم از کم اور زیادہ سے زیادہ اقدار کے ساتھ، وغیرہ۔

* مزید غیر معمولی types کے لیے توثیق، جیسے:
    * URL۔
    * Email۔
    * UUID۔
    * ...اور دیگر۔

تمام توثیق معروف اور مضبوط **Pydantic** کے ذریعے ہینڈل ہوتی ہے۔

### سیکیورٹی اور تصدیق { #security-and-authentication }

سیکیورٹی اور تصدیق مربوط ہے۔ ڈیٹابیسز یا data models کے ساتھ کسی سمجھوتے کے بغیر۔

OpenAPI میں بیان کردہ تمام security schemes، بشمول:

* HTTP Basic۔
* **OAuth2** (بشمول **JWT tokens**)۔ [OAuth2 with JWT](tutorial/security/oauth2-jwt.md) کا tutorial دیکھیں۔
* API keys بذریعہ:
    * Headers۔
    * Query parameters۔
    * Cookies، وغیرہ۔

نیز Starlette کی تمام security خصوصیات (بشمول **session cookies**)۔

سب کچھ دوبارہ قابل استعمال ٹولز اور اجزاء کے طور پر بنایا گیا ہے جو آپ کے سسٹمز، data stores، relational اور NoSQL ڈیٹابیسز وغیرہ کے ساتھ آسانی سے مربوط ہو سکتے ہیں۔

### Dependency Injection { #dependency-injection }

FastAPI میں انتہائی آسان لیکن انتہائی طاقتور <dfn title='also known as "components", "resources", "services", "providers"'><strong>Dependency Injection</strong></dfn> سسٹم شامل ہے۔

* Dependencies کی بھی dependencies ہو سکتی ہیں، جو ایک درجہ بندی یا **dependencies کا "graph"** بناتی ہیں۔
* سب کچھ framework کے ذریعے **خودکار طور پر ہینڈل** ہوتا ہے۔
* تمام dependencies requests سے ڈیٹا مانگ سکتی ہیں اور **path operation** کی حدود اور خودکار دستاویزات کو **بہتر** بنا سکتی ہیں۔
* dependencies میں بیان کردہ *path operation* parameters کے لیے بھی **خودکار توثیق**۔
* پیچیدہ user authentication سسٹمز، **database connections** وغیرہ کی سپورٹ۔
* ڈیٹابیسز، frontends وغیرہ کے ساتھ **کوئی سمجھوتا نہیں**۔ لیکن ان سب کے ساتھ آسان انضمام۔

### لامحدود "plug-ins" { #unlimited-plug-ins }

یا دوسرے لفظوں میں، ان کی کوئی ضرورت نہیں، جو code چاہیے import کریں اور استعمال کریں۔

کوئی بھی انضمام اتنا سادہ بنایا گیا ہے (dependencies کے ساتھ) کہ آپ اپنی ایپلیکیشن کے لیے 2 لائنوں کے code میں ایک "plug-in" بنا سکتے ہیں، وہی ساخت اور syntax استعمال کرتے ہوئے جو آپ کی *path operations* کے لیے استعمال ہوتی ہے۔

### آزمایا ہوا { #tested }

* 100% <dfn title="The amount of code that is automatically tested">test coverage</dfn>۔
* 100% <dfn title="Python type annotations, with this your editor and external tools can give you better support">type annotated</dfn> code base۔
* پروڈکشن ایپلیکیشنز میں استعمال ہو رہا ہے۔

## Starlette کی خصوصیات { #starlette-features }

**FastAPI** مکمل طور پر [**Starlette**](https://www.starlette.dev/) کے ساتھ ہم آہنگ (اور اس پر مبنی) ہے۔ لہٰذا، آپ کا کوئی بھی اضافی Starlette code بھی کام کرے گا۔

`FastAPI` دراصل `Starlette` کی ایک sub-class ہے۔ لہٰذا، اگر آپ پہلے سے Starlette جانتے ہیں یا استعمال کرتے ہیں، تو زیادہ تر فعالیت اسی طرح کام کرے گی۔

**FastAPI** کے ساتھ آپ کو **Starlette** کی تمام خصوصیات ملتی ہیں (کیونکہ FastAPI بنیادی طور پر Starlette کا بہتر ورژن ہے):

* سنجیدگی سے متاثر کن کارکردگی۔ یہ [دستیاب تیز ترین Python frameworks میں سے ایک ہے، **NodeJS** اور **Go** کے برابر](https://github.com/encode/starlette#performance)۔
* **WebSocket** سپورٹ۔
* In-process background tasks۔
* Startup اور shutdown events۔
* HTTPX پر مبنی test client۔
* **CORS**، GZip، Static Files، Streaming responses۔
* **Session اور Cookie** سپورٹ۔
* 100% test coverage۔
* 100% type annotated codebase۔

## Pydantic کی خصوصیات { #pydantic-features }

**FastAPI** مکمل طور پر [**Pydantic**](https://docs.pydantic.dev/) کے ساتھ ہم آہنگ (اور اس پر مبنی) ہے۔ لہٰذا، آپ کا کوئی بھی اضافی Pydantic code بھی کام کرے گا۔

بشمول Pydantic پر مبنی بیرونی لائبریریاں، جیسے ڈیٹابیسز کے لیے <abbr title="Object-Relational Mapper">ORM</abbr>s، <abbr title="Object-Document Mapper">ODM</abbr>s۔

اس کا مطلب یہ بھی ہے کہ بہت سے معاملات میں آپ request سے ملنے والی وہی object **براہ راست ڈیٹابیس کو** بھیج سکتے ہیں، کیونکہ ہر چیز خودکار طور پر توثیق شدہ ہوتی ہے۔

یہی بات دوسری طرف بھی لاگو ہوتی ہے، بہت سے معاملات میں آپ ڈیٹابیس سے ملنے والی object **براہ راست client کو** بھیج سکتے ہیں۔

**FastAPI** کے ساتھ آپ کو **Pydantic** کی تمام خصوصیات ملتی ہیں (کیونکہ FastAPI تمام data handling کے لیے Pydantic پر مبنی ہے):

* **کوئی الجھن نہیں**:
    * سیکھنے کے لیے کوئی نئی schema definition مائیکرو زبان نہیں۔
    * اگر آپ Python types جانتے ہیں تو آپ Pydantic استعمال کرنا جانتے ہیں۔
* آپ کے **<abbr title="Integrated Development Environment: similar to a code editor">IDE</abbr>/<dfn title="A program that checks for code errors">linter</dfn>/دماغ** کے ساتھ اچھی طرح کام کرتا ہے:
    * کیونکہ pydantic data structures صرف آپ کی بیان کردہ classes کی instances ہیں؛ auto-completion، linting، mypy اور آپ کی بصیرت سب آپ کے توثیق شدہ ڈیٹا کے ساتھ صحیح طریقے سے کام کریں گے۔
* **پیچیدہ ساختوں** کی توثیق کریں:
    * درجہ بند Pydantic models، Python `typing` کی `List` اور `Dict` وغیرہ کا استعمال۔
    * اور validators پیچیدہ data schemas کو واضح اور آسانی سے بیان، جانچ اور JSON Schema کے طور پر دستاویز کرنے کی اجازت دیتے ہیں۔
    * آپ کے پاس گہرائی سے **nested JSON** objects ہو سکتے ہیں اور ان سب کی توثیق اور تشریح ہو سکتی ہے۔
* **قابل توسیع**:
    * Pydantic حسب ضرورت data types بیان کرنے کی اجازت دیتا ہے یا آپ validator decorator سے مزین model پر methods کے ساتھ توثیق بڑھا سکتے ہیں۔
* 100% test coverage۔
