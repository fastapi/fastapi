# विकल्प, प्रेरणा और तुलनाएँ { #alternatives-inspiration-and-comparisons }

**FastAPI** को किसने प्रेरित किया, यह विकल्पों की तुलना में कैसा है और इसने उनसे क्या सीखा।

## परिचय { #intro }

**FastAPI** दूसरों के पिछले काम के बिना अस्तित्व में नहीं आता।

पहले कई टूल्स बनाए गए हैं जिन्होंने इसके निर्माण को प्रेरित करने में मदद की।

मैं कई वर्षों तक एक नया framework बनाने से बचता रहा। पहले मैंने **FastAPI** द्वारा कवर किए गए सभी features को कई अलग-अलग frameworks, plug-ins और tools का उपयोग करके हल करने की कोशिश की।

लेकिन किसी बिंदु पर, ऐसा कुछ बनाने के अलावा कोई विकल्प नहीं बचा जो ये सभी features प्रदान करे, पिछले tools से सर्वश्रेष्ठ ideas ले और उन्हें सबसे अच्छे तरीके से जोड़े, उन language features का उपयोग करते हुए जो पहले उपलब्ध भी नहीं थे (Python 3.6+ type hints)।

## पिछले टूल्स { #previous-tools }

### [Django](https://www.djangoproject.com/) { #django }

यह सबसे लोकप्रिय Python framework है और व्यापक रूप से भरोसेमंद है। इसका उपयोग Instagram जैसे systems बनाने के लिए किया जाता है।

यह relational databases (जैसे MySQL या PostgreSQL) के साथ अपेक्षाकृत tightly coupled है, इसलिए, मुख्य store engine के रूप में NoSQL database (जैसे Couchbase, MongoDB, Cassandra, आदि) रखना बहुत आसान नहीं है।

इसे backend में HTML generate करने के लिए बनाया गया था, न कि modern frontend (जैसे React, Vue.js और Angular) या इसके साथ communicate करने वाले अन्य systems (जैसे <abbr title="Internet of Things - चीज़ों का इंटरनेट">IoT</abbr> devices) द्वारा उपयोग की जाने वाली APIs बनाने के लिए।

### [Django REST Framework](https://www.django-rest-framework.org/) { #django-rest-framework }

Django REST Framework को Django के ऊपर Web APIs बनाने के लिए एक flexible toolkit के रूप में बनाया गया था, ताकि इसकी API capabilities को बेहतर किया जा सके।

इसका उपयोग Mozilla, Red Hat और Eventbrite सहित कई companies करती हैं।

यह **automatic API documentation** के शुरुआती उदाहरणों में से एक था, और यही विशेष रूप से उन पहले ideas में से एक था जिसने **FastAPI** की "खोज" को प्रेरित किया।

/// note | नोट

Django REST Framework को Tom Christie ने बनाया था। वही creator जिन्होंने Starlette और Uvicorn बनाए, जिन पर **FastAPI** आधारित है।

///

/// tip | **FastAPI** को यह करने के लिए प्रेरित किया

एक automatic API documentation web user interface रखना।

///

### [Flask](https://flask.palletsprojects.com) { #flask }

Flask एक "microframework" है, इसमें database integrations या Django में default रूप से आने वाली कई चीजें शामिल नहीं हैं।

यह simplicity और flexibility मुख्य data storage system के रूप में NoSQL databases का उपयोग करने जैसी चीजें करने की अनुमति देती है।

क्योंकि यह बहुत सरल है, इसे सीखना अपेक्षाकृत intuitive है, हालांकि documentation कुछ जगहों पर थोड़ा technical हो जाता है।

इसका सामान्य रूप से उन अन्य applications के लिए भी उपयोग किया जाता है जिन्हें जरूरी नहीं कि database, user management, या Django में pre-built आने वाले कई features में से किसी की आवश्यकता हो। हालांकि इनमें से कई features plug-ins के साथ जोड़े जा सकते हैं।

Parts का यह decoupling, और एक ऐसा "microframework" होना जिसे बिल्कुल जरूरत के अनुसार extend किया जा सके, एक key feature था जिसे मैं बनाए रखना चाहता था।

Flask की simplicity को देखते हुए, यह APIs बनाने के लिए एक अच्छा match लगा। अगली चीज़ जो ढूंढनी थी वह Flask के लिए एक "Django REST Framework" था।

/// tip | **FastAPI** को यह करने के लिए प्रेरित किया

एक micro-framework होना। जरूरत के tools और parts को mix and match करना आसान बनाना।

एक simple और उपयोग में आसान routing system रखना।

///

### [Requests](https://requests.readthedocs.io) { #requests }

**FastAPI** वास्तव में **Requests** का विकल्प नहीं है। उनका scope बहुत अलग है।

वास्तव में FastAPI application के *अंदर* Requests का उपयोग करना आम बात होगी।

फिर भी, FastAPI ने Requests से काफी प्रेरणा ली।

**Requests** APIs के साथ *interact* करने (client के रूप में) के लिए एक library है, जबकि **FastAPI** APIs *build* करने (server के रूप में) के लिए एक library है।

वे कमोबेश विपरीत छोरों पर हैं, एक-दूसरे को complement करते हुए।

Requests का design बहुत simple और intuitive है, sensible defaults के साथ इसका उपयोग बहुत आसान है। लेकिन साथ ही, यह बहुत powerful और customizable है।

इसीलिए, जैसा कि official website में कहा गया है:

> Requests is one of the most downloaded Python packages of all time

आप इसका उपयोग जिस तरह करते हैं वह बहुत सरल है। उदाहरण के लिए, `GET` request करने के लिए, आप लिखेंगे:

```Python
response = requests.get("http://example.com/some/url")
```

FastAPI counterpart API *path operation* कुछ इस तरह दिख सकता है:

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

`requests.get(...)` और `@app.get(...)` में समानताएँ देखें।

/// tip | **FastAPI** को यह करने के लिए प्रेरित किया

* एक simple और intuitive API रखना।
* HTTP method names (operations) को सीधे, सरल और intuitive तरीके से उपयोग करना।
* Sensible defaults रखना, लेकिन powerful customizations के साथ।

///

### [Swagger](https://swagger.io/) / [OpenAPI](https://github.com/OAI/OpenAPI-Specification/) { #swagger-openapi }

Django REST Framework से मुझे जो मुख्य feature चाहिए था वह automatic API documentation था।

फिर मुझे पता चला कि APIs को document करने के लिए एक standard था, JSON (या YAML, जो JSON का extension है) का उपयोग करते हुए, जिसे Swagger कहा जाता था।

और Swagger APIs के लिए एक web user interface पहले से बनाया हुआ था। इसलिए, किसी API के लिए Swagger documentation generate कर पाना इस web user interface को automatically उपयोग करने की अनुमति देता।

किसी समय, Swagger को Linux Foundation को दे दिया गया, ताकि इसका नाम OpenAPI रखा जाए।

इसीलिए version 2.0 के बारे में बात करते समय "Swagger" कहना आम है, और version 3+ के लिए "OpenAPI"।

/// tip | **FastAPI** को यह करने के लिए प्रेरित किया

Custom schema के बजाय API specifications के लिए एक open standard अपनाना और उपयोग करना।

और standards-based user interface tools को integrate करना:

* [Swagger UI](https://github.com/swagger-api/swagger-ui)
* [ReDoc](https://github.com/Rebilly/ReDoc)

इन दोनों को इसलिए चुना गया क्योंकि ये काफी popular और stable थे, लेकिन एक quick search करके, आप OpenAPI के लिए दर्जनों alternative user interfaces पा सकते हैं (जिन्हें आप **FastAPI** के साथ उपयोग कर सकते हैं)।

///

### Flask REST frameworks { #flask-rest-frameworks }

कई Flask REST frameworks हैं, लेकिन उन्हें investigate करने में समय और काम लगाने के बाद, मैंने पाया कि कई discontinued या abandoned हैं, जिनमें कई pending issues थे जो उन्हें अनुपयुक्त बनाते थे।

### [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) { #marshmallow }

API systems के लिए आवश्यक मुख्य features में से एक data "<dfn title="मार्शलिंग, रूपांतरण भी कहा जाता है">serialization</dfn>" है, जो code (Python) से data लेकर उसे ऐसी चीज़ में convert करता है जिसे network के माध्यम से भेजा जा सके। उदाहरण के लिए, database से data रखने वाले object को JSON object में convert करना। `datetime` objects को strings में convert करना, आदि।

APIs के लिए आवश्यक एक और बड़ा feature data validation है, यह सुनिश्चित करना कि data कुछ parameters के अनुसार valid है। उदाहरण के लिए, कोई field `int` है, न कि कोई random string। यह incoming data के लिए विशेष रूप से उपयोगी है।

Data validation system के बिना, आपको code में सभी checks हाथ से करने पड़ेंगे।

ये features वही हैं जिन्हें प्रदान करने के लिए Marshmallow बनाया गया था। यह एक बेहतरीन library है, और मैंने पहले इसका बहुत उपयोग किया है।

लेकिन इसे Python type hints के अस्तित्व में आने से पहले बनाया गया था। इसलिए, हर <dfn title="डेटा कैसे गठित होना चाहिए इसकी परिभाषा">schema</dfn> define करने के लिए आपको Marshmallow द्वारा प्रदान किए गए specific utils और classes का उपयोग करना पड़ता है।

/// tip | **FastAPI** को यह करने के लिए प्रेरित किया

"schemas" define करने के लिए code का उपयोग करना, जो data types और validation automatically प्रदान करते हैं।

///

### [Webargs](https://webargs.readthedocs.io/en/latest/) { #webargs }

APIs के लिए आवश्यक एक और बड़ा feature incoming requests से data की <dfn title="Python data में पढ़ना और convert करना">parsing</dfn> है।

Webargs एक tool है जिसे Flask सहित कई frameworks के ऊपर यह प्रदान करने के लिए बनाया गया था।

यह data validation करने के लिए अंदर से Marshmallow का उपयोग करता है। और इसे उन्हीं developers ने बनाया था।

यह एक बेहतरीन tool है और **FastAPI** से पहले मैंने इसका भी बहुत उपयोग किया है।

/// note | नोट

Webargs को उन्हीं Marshmallow developers ने बनाया था।

///

/// tip | **FastAPI** को यह करने के लिए प्रेरित किया

Incoming request data का automatic validation रखना।

///

### [APISpec](https://apispec.readthedocs.io/en/stable/) { #apispec }

Marshmallow और Webargs validation, parsing और serialization को plug-ins के रूप में प्रदान करते हैं।

लेकिन documentation अभी भी missing है। फिर APISpec बनाया गया।

यह कई frameworks के लिए एक plug-in है (और Starlette के लिए भी एक plug-in है)।

यह जिस तरह काम करता है वह यह है कि आप route handle करने वाली प्रत्येक function के docstring के अंदर YAML format का उपयोग करके schema की definition लिखते हैं।

और यह OpenAPI schemas generate करता है।

Flask, Starlette, Responder, आदि में यह इसी तरह काम करता है।

लेकिन फिर, हमारे पास फिर से Python string (एक बड़ा YAML) के अंदर micro-syntax होने की समस्या आती है।

Editor इसमें ज्यादा मदद नहीं कर सकता। और अगर हम parameters या Marshmallow schemas को modify करते हैं और उस YAML docstring को भी modify करना भूल जाते हैं, तो generated schema obsolete हो जाएगा।

/// note | नोट

APISpec को उन्हीं Marshmallow developers ने बनाया था।

///

/// tip | **FastAPI** को यह करने के लिए प्रेरित किया

APIs के लिए open standard, OpenAPI को support करना।

///

### [Flask-apispec](https://flask-apispec.readthedocs.io/en/latest/) { #flask-apispec }

यह एक Flask plug-in है, जो Webargs, Marshmallow और APISpec को साथ जोड़ता है।

यह APISpec का उपयोग करके, Webargs और Marshmallow की जानकारी से automatically OpenAPI schemas generate करता है।

यह एक बेहतरीन tool है, बहुत underrated। यह मौजूद कई Flask plug-ins से कहीं अधिक popular होना चाहिए। शायद इसका कारण इसकी documentation का बहुत concise और abstract होना है।

इसने Python docstrings के अंदर YAML (एक और syntax) लिखने की जरूरत को हल कर दिया।

Flask, Flask-apispec के साथ Marshmallow और Webargs का यह combination **FastAPI** बनाने तक मेरा favorite backend stack था।

इसका उपयोग करने से कई Flask full-stack generators बने। ये मुख्य stacks हैं जिनका मैं (और कई external teams) अब तक उपयोग करते रहे हैं:

* [https://github.com/tiangolo/full-stack](https://github.com/tiangolo/full-stack)
* [https://github.com/tiangolo/full-stack-flask-couchbase](https://github.com/tiangolo/full-stack-flask-couchbase)
* [https://github.com/tiangolo/full-stack-flask-couchdb](https://github.com/tiangolo/full-stack-flask-couchdb)

और यही full-stack generators [**FastAPI** Project Generators](project-generation.md) का आधार थे।

/// note | नोट

Flask-apispec को उन्हीं Marshmallow developers ने बनाया था।

///

/// tip | **FastAPI** को यह करने के लिए प्रेरित किया

OpenAPI schema को automatically generate करना, उसी code से जो serialization और validation define करता है।

///

### [NestJS](https://nestjs.com/) (और [Angular](https://angular.io/)) { #nestjs-and-angular }

यह Python भी नहीं है, NestJS एक JavaScript (TypeScript) NodeJS framework है जो Angular से inspired है।

यह कुछ हद तक वही हासिल करता है जो Flask-apispec के साथ किया जा सकता है।

इसमें Angular 2 से inspired एक integrated dependency injection system है। इसके लिए "injectables" (मेरी जानकारी के सभी अन्य dependency injection systems की तरह) को pre-register करना आवश्यक है, इसलिए यह verbosity और code repetition बढ़ाता है।

क्योंकि parameters को TypeScript types (Python type hints के समान) के साथ describe किया जाता है, editor support काफी अच्छा है।

लेकिन क्योंकि TypeScript data JavaScript में compilation के बाद preserved नहीं रहता, यह validation, serialization और documentation को एक साथ define करने के लिए types पर भरोसा नहीं कर सकता। इसके कारण और कुछ design decisions के कारण, validation, serialization और automatic schema generation पाने के लिए, कई जगह decorators जोड़ना आवश्यक होता है। इसलिए, यह काफी verbose हो जाता है।

यह nested models को बहुत अच्छी तरह handle नहीं कर सकता। इसलिए, अगर request में JSON body एक JSON object है जिसमें inner fields हैं जो बदले में nested JSON objects हैं, तो उसे properly documented और validated नहीं किया जा सकता।

/// tip | **FastAPI** को यह करने के लिए प्रेरित किया

बेहतरीन editor support के लिए Python types का उपयोग करना।

एक powerful dependency injection system रखना। Code repetition को minimize करने का तरीका खोजना।

///

### [Sanic](https://sanic.readthedocs.io/en/latest/) { #sanic }

यह `asyncio` पर आधारित पहले बेहद तेज़ Python frameworks में से एक था। इसे Flask के बहुत समान बनाने के लिए बनाया गया था।

/// note | तकनीकी विवरण

इसने default Python `asyncio` loop के बजाय [`uvloop`](https://github.com/MagicStack/uvloop) का उपयोग किया। यही इसे इतना तेज़ बनाता था।

इसने स्पष्ट रूप से Uvicorn और Starlette को प्रेरित किया, जो वर्तमान में open benchmarks में Sanic से तेज़ हैं।

///

/// tip | **FastAPI** को यह करने के लिए प्रेरित किया

बेहद शानदार performance पाने का तरीका खोजना।

इसीलिए **FastAPI** Starlette पर आधारित है, क्योंकि यह उपलब्ध सबसे तेज़ framework है (third-party benchmarks द्वारा tested)।

///

### [Falcon](https://falconframework.org/) { #falcon }

Falcon एक और high performance Python framework है, इसे minimal होने और Hug जैसे अन्य frameworks की foundation के रूप में काम करने के लिए design किया गया है।

इसे ऐसी functions रखने के लिए design किया गया है जो दो parameters receive करती हैं, एक "request" और एक "response"। फिर आप request से parts "read" करते हैं, और response में parts "write" करते हैं। इस design के कारण, standard Python type hints के साथ function parameters के रूप में request parameters और bodies declare करना संभव नहीं है।

इसलिए, data validation, serialization और documentation को code में करना पड़ता है, automatically नहीं। या उन्हें Falcon के ऊपर Hug जैसे framework के रूप में implement करना पड़ता है। यही distinction Falcon के design से inspired अन्य frameworks में भी होता है, जिसमें parameters के रूप में एक request object और एक response object होता है।

/// tip | **FastAPI** को यह करने के लिए प्रेरित किया

बेहतरीन performance पाने के तरीके खोजना।

Hug के साथ (क्योंकि Hug Falcon पर आधारित है) इसने **FastAPI** को functions में `response` parameter declare करने के लिए प्रेरित किया।

हालांकि FastAPI में यह optional है, और मुख्य रूप से headers, cookies और alternative status codes set करने के लिए उपयोग किया जाता है।

///

### [Molten](https://moltenframework.com/) { #molten }

मैंने **FastAPI** बनाने के शुरुआती stages में Molten खोजा। और इसमें काफी similar ideas हैं:

* Python type hints पर आधारित।
* इन types से validation और documentation।
* Dependency Injection system।

यह Pydantic जैसी data validation, serialization और documentation third-party library का उपयोग नहीं करता, इसकी अपनी है। इसलिए, ये data type definitions उतनी आसानी से reusable नहीं होंगी।

इसके लिए थोड़ी अधिक verbose configurations की आवश्यकता होती है। और क्योंकि यह WSGI (ASGI के बजाय) पर आधारित है, इसे Uvicorn, Starlette और Sanic जैसे tools द्वारा प्रदान की जाने वाली high performance का लाभ उठाने के लिए design नहीं किया गया है।

Dependency injection system dependencies की pre-registration की मांग करता है और dependencies declared types के आधार पर solve की जाती हैं। इसलिए, एक निश्चित type प्रदान करने वाले एक से अधिक "component" declare करना संभव नहीं है।

Routes को एक single place में declare किया जाता है, उन functions का उपयोग करते हुए जो अन्य places में declared होती हैं (decorators का उपयोग करने के बजाय जिन्हें endpoint handle करने वाली function के ठीक ऊपर रखा जा सकता है)। यह Flask (और Starlette) के तरीके की तुलना में Django के तरीके के अधिक करीब है। यह code में उन चीज़ों को अलग करता है जो अपेक्षाकृत tightly coupled हैं।

/// tip | **FastAPI** को यह करने के लिए प्रेरित किया

Model attributes के "default" value का उपयोग करके data types के लिए extra validations define करना। इससे editor support बेहतर होता है, और यह पहले Pydantic में उपलब्ध नहीं था।

इसने वास्तव में Pydantic के parts को update करने के लिए प्रेरित किया, ताकि वही validation declaration style support की जा सके (यह सारी functionality अब पहले से ही Pydantic में उपलब्ध है)।

///

### [Hug](https://github.com/hugapi/hug) { #hug }

Hug उन पहले frameworks में से एक था जिसने Python type hints का उपयोग करके API parameter types की declaration implement की। यह एक बेहतरीन idea था जिसने अन्य tools को भी ऐसा करने के लिए प्रेरित किया।

इसने अपनी declarations में standard Python types के बजाय custom types का उपयोग किया, लेकिन यह फिर भी एक बहुत बड़ा कदम था।

यह JSON में पूरी API declare करने वाला custom schema generate करने वाले पहले frameworks में से भी एक था।

यह OpenAPI और JSON Schema जैसे standard पर आधारित नहीं था। इसलिए इसे Swagger UI जैसे अन्य tools के साथ integrate करना straightforward नहीं होता। लेकिन फिर भी, यह एक बहुत innovative idea था।

इसमें एक interesting, uncommon feature है: उसी framework का उपयोग करके APIs और CLIs भी बनाना संभव है।

क्योंकि यह synchronous Python web frameworks (WSGI) के पिछले standard पर आधारित है, यह Websockets और अन्य चीज़ों को handle नहीं कर सकता, हालांकि इसका performance भी high है।

/// note | नोट

Hug को Timothy Crosley ने बनाया था, जो [`isort`](https://github.com/timothycrosley/isort) के भी creator हैं, Python files में imports को automatically sort करने का एक बेहतरीन tool।

///

/// tip | **FastAPI** को प्रेरित करने वाले ideas

Hug ने APIStar के parts को प्रेरित किया, और APIStar के साथ-साथ यह उन tools में से एक था जो मुझे सबसे promising लगे।

Hug ने **FastAPI** को parameters declare करने के लिए Python type hints का उपयोग करने, और API को automatically define करने वाला schema generate करने के लिए प्रेरित करने में मदद की।

Hug ने **FastAPI** को headers और cookies set करने के लिए functions में `response` parameter declare करने के लिए प्रेरित किया।

///

### [APIStar](https://github.com/encode/apistar) (<= 0.5) { #apistar-0-5 }

**FastAPI** बनाने का निर्णय लेने से ठीक पहले मुझे **APIStar** server मिला। इसमें लगभग वह सब कुछ था जिसकी मुझे तलाश थी और इसका design बेहतरीन था।

यह उन पहले framework implementations में से एक था जिसे मैंने कभी देखा, जिसमें parameters और requests declare करने के लिए Python type hints का उपयोग किया गया था (NestJS और Molten से पहले)। मुझे यह लगभग Hug के साथ ही मिला। लेकिन APIStar ने OpenAPI standard का उपयोग किया।

इसमें कई जगहों पर उन्हीं type hints के आधार पर automatic data validation, data serialization और OpenAPI schema generation था।

Body schema definitions ने Pydantic जैसी Python type hints का उपयोग नहीं किया, यह Marshmallow के थोड़ा अधिक समान था, इसलिए, editor support उतना अच्छा नहीं होता, लेकिन फिर भी, APIStar सबसे अच्छा उपलब्ध विकल्प था।

उस समय इसके performance benchmarks सबसे अच्छे थे (केवल Starlette से पीछे)।

शुरुआत में, इसमें automatic API documentation web UI नहीं था, लेकिन मुझे पता था कि मैं इसमें Swagger UI जोड़ सकता हूँ।

इसमें dependency injection system था। इसे ऊपर चर्चा किए गए अन्य tools की तरह components की pre-registration की आवश्यकता थी। लेकिन फिर भी, यह एक बेहतरीन feature था।

मैं इसे कभी full project में उपयोग नहीं कर सका, क्योंकि इसमें security integration नहीं था, इसलिए, मैं Flask-apispec पर आधारित full-stack generators के साथ मिलने वाले सभी features को replace नहीं कर सकता था। मेरे projects backlog में वह functionality जोड़ने के लिए एक pull request बनाने का काम था।

लेकिन फिर, project का focus बदल गया।

यह अब API web framework नहीं रहा, क्योंकि creator को Starlette पर focus करने की आवश्यकता थी।

अब APIStar OpenAPI specifications को validate करने के लिए tools का एक set है, web framework नहीं।

/// note | नोट

APIStar को Tom Christie ने बनाया था। वही व्यक्ति जिन्होंने बनाया:

* Django REST Framework
* Starlette (जिस पर **FastAPI** आधारित है)
* Uvicorn (Starlette और **FastAPI** द्वारा उपयोग किया जाता है)

///

/// tip | **FastAPI** को यह करने के लिए प्रेरित किया

अस्तित्व में आना।

उसी Python types के साथ कई चीज़ें (data validation, serialization और documentation) declare करने का idea, जो साथ ही बेहतरीन editor support प्रदान करता था, मुझे एक शानदार idea लगा।

और एक similar framework की लंबे समय तक खोज और कई अलग-अलग alternatives test करने के बाद, APIStar सबसे अच्छा उपलब्ध विकल्प था।

फिर APIStar server के रूप में अस्तित्व में नहीं रहा और Starlette बनाया गया, और यह ऐसे system के लिए एक नई बेहतर foundation था। यही **FastAPI** बनाने की अंतिम प्रेरणा थी।

मैं **FastAPI** को APIStar का "spiritual successor" मानता हूँ, जबकि features, typing system और अन्य parts को बेहतर और विस्तृत करता हूँ, इन सभी पिछले tools से मिली सीख के आधार पर।

///

## **FastAPI** द्वारा उपयोग किए गए { #used-by-fastapi }

### [Pydantic](https://docs.pydantic.dev/) { #pydantic }

Pydantic Python type hints के आधार पर data validation, serialization और documentation (JSON Schema का उपयोग करके) define करने के लिए एक library है।

यह इसे बेहद intuitive बनाता है।

यह Marshmallow से comparable है। हालांकि benchmarks में यह Marshmallow से तेज़ है। और क्योंकि यह उन्हीं Python type hints पर आधारित है, editor support बेहतरीन है।

/// tip | **FastAPI** इसका उपयोग यह करने के लिए करता है

सभी data validation, data serialization और automatic model documentation (JSON Schema पर आधारित) को handle करना।

फिर **FastAPI** उस JSON Schema data को लेकर OpenAPI में डालता है, इसके द्वारा की जाने वाली बाकी सभी चीज़ों के अलावा।

///

### [Starlette](https://www.starlette.dev/) { #starlette }

Starlette एक lightweight <dfn title="असिंक्रोनस Python web applications बनाने के लिए नया standard">ASGI</dfn> framework/toolkit है, जो high-performance asyncio services बनाने के लिए आदर्श है।

यह बहुत simple और intuitive है। इसे आसानी से extensible होने और modular components रखने के लिए design किया गया है।

इसमें है:

* सचमुच प्रभावशाली performance।
* WebSocket support।
* In-process background tasks।
* Startup और shutdown events।
* HTTPX पर built test client।
* CORS, GZip, Static Files, Streaming responses।
* Session और Cookie support।
* 100% test coverage।
* 100% type annotated codebase।
* कम hard dependencies।

Starlette वर्तमान में tested सबसे तेज़ Python framework है। केवल Uvicorn इससे आगे है, जो framework नहीं, बल्कि server है।

Starlette सभी basic web microframework functionality प्रदान करता है।

लेकिन यह automatic data validation, serialization या documentation प्रदान नहीं करता।

यही उन मुख्य चीज़ों में से एक है जो **FastAPI** ऊपर से जोड़ता है, सब Python type hints (Pydantic का उपयोग करके) पर आधारित। इसके साथ dependency injection system, security utilities, OpenAPI schema generation, आदि।

/// note | तकनीकी विवरण

ASGI एक नया "standard" है जिसे Django core team members द्वारा develop किया जा रहा है। यह अभी भी "Python standard" (एक PEP) नहीं है, हालांकि वे ऐसा करने की प्रक्रिया में हैं।

फिर भी, इसे पहले से ही कई tools द्वारा "standard" के रूप में उपयोग किया जा रहा है। इससे interoperability बहुत बेहतर होती है, क्योंकि आप Uvicorn को किसी अन्य ASGI server (जैसे Daphne या Hypercorn) से बदल सकते हैं, या आप `python-socketio` जैसे ASGI compatible tools जोड़ सकते हैं।

///

/// tip | **FastAPI** इसका उपयोग यह करने के लिए करता है

सभी core web parts को handle करना। ऊपर से features जोड़ना।

Class `FastAPI` खुद सीधे class `Starlette` से inherit करती है।

इसलिए, आप Starlette के साथ जो कुछ भी कर सकते हैं, आप उसे सीधे **FastAPI** के साथ कर सकते हैं, क्योंकि यह मूल रूप से steroids पर Starlette है।

///

### [Uvicorn](https://www.uvicorn.dev/) { #uvicorn }

Uvicorn एक lightning-fast ASGI server है, जो uvloop और httptools पर built है।

यह web framework नहीं, बल्कि server है। उदाहरण के लिए, यह paths द्वारा routing के लिए tools प्रदान नहीं करता। यह ऐसी चीज़ है जो Starlette (या **FastAPI**) जैसा framework ऊपर से प्रदान करेगा।

यह Starlette और **FastAPI** के लिए recommended server है।

/// tip | **FastAPI** इसे इस रूप में recommend करता है

**FastAPI** applications चलाने के लिए main web server।

आप asynchronous multi-process server पाने के लिए `--workers` command line option का भी उपयोग कर सकते हैं।

अधिक विवरण [Deployment](deployment/index.md) section में देखें।

///

## Benchmarks और speed { #benchmarks-and-speed }

Uvicorn, Starlette और FastAPI के बीच अंतर समझने, compare करने और देखने के लिए, [Benchmarks](benchmarks.md) के बारे में section देखें।
