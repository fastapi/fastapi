# विकल्प, प्रेरणा और तुलनाएँ { #alternatives-inspiration-and-comparisons }

**FastAPI** को किससे प्रेरणा मिली, यह विकल्पों की तुलना में कैसा है और उनसे इसने क्या सीखा।

## परिचय { #intro }

दूसरों के पिछले काम के बिना **FastAPI** अस्तित्व में नहीं होता।

इससे पहले कई tools बनाए गए हैं जिन्होंने इसके निर्माण को प्रेरित करने में मदद की।

मैं कई वर्षों तक एक नया framework बनाने से बचता रहा। पहले मैंने **FastAPI** द्वारा कवर किए गए सभी features को कई अलग-अलग frameworks, plug-ins और tools का उपयोग करके हल करने की कोशिश की।

लेकिन एक समय ऐसा आया जब ऐसा कुछ बनाने के अलावा कोई विकल्प नहीं था जो ये सभी features प्रदान करे, पिछले tools से सर्वोत्तम विचारों को लेकर, और उन्हें सबसे अच्छे तरीके से मिलाकर, उन language features का उपयोग करते हुए जो पहले उपलब्ध भी नहीं थे (Python 3.6+ type hints)।

## पिछले tools { #previous-tools }

### [Django](https://www.djangoproject.com/) { #django }

यह सबसे लोकप्रिय Python framework है और व्यापक रूप से भरोसेमंद है। इसका उपयोग Instagram जैसे systems बनाने के लिए किया जाता है।

यह relational databases (जैसे MySQL या PostgreSQL) के साथ अपेक्षाकृत tightly coupled है, इसलिए मुख्य store engine के रूप में NoSQL database (जैसे Couchbase, MongoDB, Cassandra, आदि) रखना बहुत आसान नहीं है।

इसे backend में HTML generate करने के लिए बनाया गया था, न कि किसी modern frontend (जैसे React, Vue.js और Angular) या इसके साथ संचार करने वाले अन्य systems (जैसे <abbr title="Internet of Things - चीज़ों का इंटरनेट">IoT</abbr> devices) द्वारा उपयोग की जाने वाली APIs बनाने के लिए।

### [Django REST Framework](https://www.django-rest-framework.org/) { #django-rest-framework }

Django REST Framework को Django के ऊपर Web APIs बनाने के लिए एक flexible toolkit के रूप में बनाया गया था, ताकि इसकी API क्षमताओं में सुधार हो सके।

इसका उपयोग Mozilla, Red Hat और Eventbrite सहित कई कंपनियाँ करती हैं।

यह **automatic API documentation** के पहले उदाहरणों में से एक था, और यह विशेष रूप से उन पहले विचारों में से एक था जिसने **FastAPI** की "खोज" को प्रेरित किया।

/// note | नोट

Django REST Framework को Tom Christie ने बनाया था। वही Starlette और Uvicorn के creator हैं, जिन पर **FastAPI** आधारित है।

///

/// tip | **FastAPI** को इससे प्रेरणा मिली कि

एक automatic API documentation web user interface हो।

///

### [Flask](https://flask.palletsprojects.com) { #flask }

Flask एक "microframework" है, इसमें database integrations या Django में default रूप से आने वाली कई चीज़ें शामिल नहीं हैं।

यह simplicity और flexibility मुख्य data storage system के रूप में NoSQL databases का उपयोग करने जैसी चीज़ें करने की अनुमति देती है।

क्योंकि यह बहुत सरल है, इसे सीखना अपेक्षाकृत सहज है, हालांकि documentation कुछ बिंदुओं पर थोड़ा technical हो जाता है।

इसका उपयोग आमतौर पर उन अन्य applications के लिए भी किया जाता है जिन्हें जरूरी नहीं कि database, user management, या Django में पहले से built-in आने वाले कई features की आवश्यकता हो। हालांकि इनमें से कई features plug-ins के साथ जोड़े जा सकते हैं।

Parts का यह decoupling, और एक "microframework" होना जिसे ठीक वही कवर करने के लिए extend किया जा सके जिसकी आवश्यकता है, एक key feature था जिसे मैं बनाए रखना चाहता था।

Flask की simplicity को देखते हुए, यह APIs बनाने के लिए अच्छा match लगा। अगली चीज़ जो खोजनी थी वह Flask के लिए एक "Django REST Framework" था।

/// tip | **FastAPI** को इससे प्रेरणा मिली कि

एक micro-framework हो। आवश्यक tools और parts को mix and match करना आसान बनाया जाए।

एक simple और उपयोग में आसान routing system हो।

///

### [Requests](https://requests.readthedocs.io) { #requests }

**FastAPI** वास्तव में **Requests** का विकल्प नहीं है। उनका scope बहुत अलग है।

वास्तव में FastAPI application के *अंदर* Requests का उपयोग करना सामान्य बात होगी।

लेकिन फिर भी, FastAPI को Requests से काफी प्रेरणा मिली।

**Requests** APIs के साथ *interact* करने के लिए (client के रूप में) एक library है, जबकि **FastAPI** APIs *बनाने* के लिए (server के रूप में) एक library है।

वे कमोबेश विपरीत सिरों पर हैं, एक-दूसरे को पूरक करते हुए।

Requests का design बहुत simple और intuitive है, sensible defaults के साथ इसका उपयोग करना बहुत आसान है। लेकिन साथ ही, यह बहुत powerful और customizable है।

इसीलिए, जैसा कि official website में कहा गया है:

> Requests अब तक के सबसे अधिक downloaded Python packages में से एक है

आप इसे जिस तरह उपयोग करते हैं वह बहुत सरल है। उदाहरण के लिए, `GET` request करने के लिए, आप लिखेंगे:

```Python
response = requests.get("http://example.com/some/url")
```

FastAPI में इसके समकक्ष API *path operation* इस तरह दिख सकता है:

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

`requests.get(...)` और `@app.get(...)` में समानताएँ देखें।

/// tip | **FastAPI** को इससे प्रेरणा मिली कि

* एक simple और intuitive API हो।
* HTTP method names (operations) को सीधे, straightforward और intuitive तरीके से उपयोग किया जाए।
* sensible defaults हों, लेकिन powerful customizations भी हों।

///

### [Swagger](https://swagger.io/) / [OpenAPI](https://github.com/OAI/OpenAPI-Specification/) { #swagger-openapi }

Django REST Framework से जो मुख्य feature मैं चाहता था वह automatic API documentation था।

फिर मुझे पता चला कि APIs को document करने के लिए JSON (या YAML, JSON का एक extension) का उपयोग करने वाला एक standard था, जिसे Swagger कहा जाता था।

और Swagger APIs के लिए एक web user interface पहले से बनाया जा चुका था। इसलिए, किसी API के लिए Swagger documentation generate कर पाना इस web user interface का automatically उपयोग करने की अनुमति देता।

एक समय पर, Swagger को Linux Foundation को दे दिया गया, ताकि उसका नाम बदलकर OpenAPI रखा जा सके।

इसीलिए version 2.0 के बारे में बात करते समय "Swagger" कहना आम है, और version 3+ के लिए "OpenAPI"।

/// tip | **FastAPI** को इससे प्रेरणा मिली कि

Custom schema के बजाय API specifications के लिए एक open standard अपनाया और उपयोग किया जाए।

और standards-based user interface tools को integrate किया जाए:

* [Swagger UI](https://github.com/swagger-api/swagger-ui)
* [ReDoc](https://github.com/Rebilly/ReDoc)

इन दोनों को इसलिए चुना गया क्योंकि ये काफी popular और stable थे, लेकिन एक quick search करने पर, आप OpenAPI के लिए दर्जनों alternative user interfaces पा सकते हैं (जिन्हें आप **FastAPI** के साथ उपयोग कर सकते हैं)।

///

### Flask REST frameworks { #flask-rest-frameworks }

कई Flask REST frameworks हैं, लेकिन उनकी जाँच में समय और काम लगाने के बाद, मैंने पाया कि कई discontinue या abandon हो चुके हैं, और उनमें कई unresolved issues हैं जिन्होंने उन्हें अनुपयुक्त बना दिया।

### [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) { #marshmallow }

API systems द्वारा आवश्यक मुख्य features में से एक data "<dfn title="marshalling, conversion भी कहा जाता है">serialization</dfn>" है, जिसमें code (Python) से data लेकर उसे ऐसी चीज़ में बदला जाता है जिसे network के माध्यम से भेजा जा सके। उदाहरण के लिए, database से data रखने वाले object को JSON object में बदलना। `datetime` objects को strings में बदलना, आदि।

APIs द्वारा आवश्यक एक और बड़ा feature data validation है, यह सुनिश्चित करना कि data निश्चित parameters के अनुसार valid है। उदाहरण के लिए, कोई field `int` है, कोई random string नहीं। यह incoming data के लिए विशेष रूप से उपयोगी है।

Data validation system के बिना, आपको सभी checks हाथ से, code में करने पड़ते।

ये features वही हैं जिन्हें प्रदान करने के लिए Marshmallow बनाया गया था। यह एक बेहतरीन library है, और मैंने पहले इसका बहुत उपयोग किया है।

लेकिन इसे Python type hints के अस्तित्व में आने से पहले बनाया गया था। इसलिए, हर <dfn title="data कैसे बना होना चाहिए इसकी परिभाषा">schema</dfn> को define करने के लिए आपको Marshmallow द्वारा प्रदान किए गए specific utils और classes का उपयोग करना पड़ता है।

/// tip | **FastAPI** को इससे प्रेरणा मिली कि

"schemas" को define करने के लिए code का उपयोग किया जाए जो data types और validation, automatically प्रदान करे।

///

### [Webargs](https://webargs.readthedocs.io/en/latest/) { #webargs }

APIs द्वारा आवश्यक एक और बड़ा feature incoming requests से data <dfn title="Python data में पढ़ना और बदलना">parsing</dfn> करना है।

Webargs एक tool है जिसे Flask सहित कई frameworks के ऊपर यह प्रदान करने के लिए बनाया गया था।

यह data validation करने के लिए नीचे Marshmallow का उपयोग करता है। और इसे उन्हीं developers ने बनाया था।

यह एक बेहतरीन tool है और **FastAPI** से पहले मैंने इसका भी बहुत उपयोग किया था।

/// note | नोट

Webargs को उन्हीं Marshmallow developers ने बनाया था।

///

/// tip | **FastAPI** को इससे प्रेरणा मिली कि

Incoming request data का automatic validation हो।

///

### [APISpec](https://apispec.readthedocs.io/en/stable/) { #apispec }

Marshmallow और Webargs plug-ins के रूप में validation, parsing और serialization प्रदान करते हैं।

लेकिन documentation अभी भी missing है। फिर APISpec बनाया गया।

यह कई frameworks के लिए एक plug-in है (और Starlette के लिए भी एक plug-in है)।

यह जिस तरह काम करता है वह यह है कि आप route handle करने वाली प्रत्येक function की docstring के अंदर YAML format का उपयोग करके schema की definition लिखते हैं।

और यह OpenAPI schemas generate करता है।

Flask, Starlette, Responder, आदि में यह इसी तरह काम करता है।

लेकिन फिर, हमारे पास फिर से Python string (एक बड़ा YAML) के अंदर micro-syntax होने की समस्या है।

Editor इसमें ज्यादा मदद नहीं कर सकता। और अगर हम parameters या Marshmallow schemas modify करते हैं और उस YAML docstring को भी modify करना भूल जाते हैं, तो generated schema obsolete हो जाएगा।

/// note | नोट

APISpec को उन्हीं Marshmallow developers ने बनाया था।

///

/// tip | **FastAPI** को इससे प्रेरणा मिली कि

APIs के लिए open standard, OpenAPI को support किया जाए।

///

### [Flask-apispec](https://flask-apispec.readthedocs.io/en/latest/) { #flask-apispec }

यह एक Flask plug-in है, जो Webargs, Marshmallow और APISpec को एक साथ जोड़ता है।

यह APISpec का उपयोग करके OpenAPI schemas automatically generate करने के लिए Webargs और Marshmallow की जानकारी का उपयोग करता है।

यह एक बेहतरीन tool है, बहुत underrated। इसे वहाँ मौजूद कई Flask plug-ins से कहीं अधिक popular होना चाहिए। यह शायद इसकी documentation के बहुत concise और abstract होने के कारण हो सकता है।

इसने Python docstrings के अंदर YAML (एक और syntax) लिखने की आवश्यकता को हल कर दिया।

Flask, Flask-apispec को Marshmallow और Webargs के साथ मिलाकर यह combination **FastAPI** बनाने तक मेरा पसंदीदा backend stack था।

इसका उपयोग करने से कई Flask full-stack generators बने। ये वे main stacks हैं जिन्हें मैं (और कई external teams) अब तक उपयोग कर रहे हैं:

* [https://github.com/tiangolo/full-stack](https://github.com/tiangolo/full-stack)
* [https://github.com/tiangolo/full-stack-flask-couchbase](https://github.com/tiangolo/full-stack-flask-couchbase)
* [https://github.com/tiangolo/full-stack-flask-couchdb](https://github.com/tiangolo/full-stack-flask-couchdb)

और यही full-stack generators [**FastAPI** Project Generators](project-generation.md) का base थे।

/// note | नोट

Flask-apispec को उन्हीं Marshmallow developers ने बनाया था।

///

/// tip | **FastAPI** को इससे प्रेरणा मिली कि

OpenAPI schema को automatically generate किया जाए, उसी code से जो serialization और validation define करता है।

///

### [NestJS](https://nestjs.com/) (और [Angular](https://angular.io/)) { #nestjs-and-angular }

यह Python भी नहीं है, NestJS Angular से प्रेरित एक JavaScript (TypeScript) NodeJS framework है।

यह कुछ ऐसा हासिल करता है जो Flask-apispec के साथ किए जा सकने वाले काम जैसा है।

इसमें Angular 2 से प्रेरित एक integrated dependency injection system है। इसमें "injectables" को pre-register करना आवश्यक है (जैसे मुझे ज्ञात सभी अन्य dependency injection systems में), इसलिए, यह verbosity और code repetition बढ़ाता है।

क्योंकि parameters को TypeScript types (Python type hints के समान) के साथ describe किया जाता है, editor support काफी अच्छा है।

लेकिन क्योंकि TypeScript data compilation के बाद JavaScript में preserve नहीं रहता, यह validation, serialization और documentation को एक ही समय पर define करने के लिए types पर निर्भर नहीं हो सकता। इसके कारण और कुछ design decisions के कारण, validation, serialization और automatic schema generation पाने के लिए, कई जगह decorators जोड़ने की आवश्यकता होती है। इसलिए, यह काफी verbose हो जाता है।

यह nested models को बहुत अच्छी तरह handle नहीं कर सकता। इसलिए, अगर request में JSON body एक JSON object है जिसमें inner fields हैं जो खुद nested JSON objects हैं, तो इसे ठीक से document और validate नहीं किया जा सकता।

/// tip | **FastAPI** को इससे प्रेरणा मिली कि

बेहतरीन editor support के लिए Python types का उपयोग किया जाए।

एक powerful dependency injection system हो। Code repetition को minimize करने का तरीका खोजा जाए।

///

### [Sanic](https://sanic.readthedocs.io/en/latest/) { #sanic }

यह `asyncio` पर आधारित पहले बेहद तेज़ Python frameworks में से एक था। इसे Flask के बहुत समान बनाया गया था।

/// note | तकनीकी विवरण

इसने default Python `asyncio` loop के बजाय [`uvloop`](https://github.com/MagicStack/uvloop) का उपयोग किया। यही इसे इतना तेज़ बनाता था।

इसने स्पष्ट रूप से Uvicorn और Starlette को प्रेरित किया, जो वर्तमान में open benchmarks में Sanic से तेज़ हैं।

///

/// tip | **FastAPI** को इससे प्रेरणा मिली कि

बेहद तेज़ performance हासिल करने का तरीका खोजा जाए।

इसीलिए **FastAPI** Starlette पर आधारित है, क्योंकि यह उपलब्ध सबसे तेज़ framework है (third-party benchmarks द्वारा tested)।

///

### [Falcon](https://falconframework.org/) { #falcon }

Falcon एक और high performance Python framework है, इसे minimal होने और Hug जैसे अन्य frameworks की foundation के रूप में काम करने के लिए design किया गया है।

इसे ऐसी functions रखने के लिए design किया गया है जो दो parameters receive करती हैं, एक "request" और एक "response"। फिर आप request से parts "read" करते हैं, और response में parts "write" करते हैं। इस design के कारण, standard Python type hints के साथ function parameters के रूप में request parameters और bodies declare करना संभव नहीं है।

इसलिए, data validation, serialization, और documentation को code में करना पड़ता है, automatically नहीं। या उन्हें Falcon के ऊपर एक framework के रूप में implement करना पड़ता है, जैसे Hug। यही अंतर उन अन्य frameworks में भी होता है जो Falcon के design से प्रेरित हैं, जहाँ parameters के रूप में एक request object और एक response object होता है।

/// tip | **FastAPI** को इससे प्रेरणा मिली कि

बेहतरीन performance पाने के तरीके खोजे जाएँ।

Hug के साथ (क्योंकि Hug Falcon पर आधारित है) इसने **FastAPI** को functions में `response` parameter declare करने के लिए प्रेरित किया।

हालांकि FastAPI में यह optional है, और मुख्य रूप से headers, cookies, और alternative status codes set करने के लिए उपयोग किया जाता है।

///

### [Molten](https://moltenframework.com/) { #molten }

मैंने **FastAPI** बनाने के शुरुआती चरणों में Molten खोजा। और इसमें काफी समान विचार हैं:

* Python type hints पर आधारित।
* इन types से validation और documentation।
* Dependency Injection system।

यह Pydantic जैसी data validation, serialization और documentation third-party library का उपयोग नहीं करता, इसकी अपनी library है। इसलिए, ये data type definitions उतनी आसानी से reusable नहीं होंगी।

इसे थोड़ी अधिक verbose configurations की आवश्यकता होती है। और क्योंकि यह WSGI (ASGI के बजाय) पर आधारित है, इसे Uvicorn, Starlette और Sanic जैसे tools द्वारा प्रदान किए गए high performance का लाभ उठाने के लिए design नहीं किया गया है।

Dependency injection system को dependencies की pre-registration की आवश्यकता होती है और dependencies declared types के आधार पर solve की जाती हैं। इसलिए, किसी निश्चित type को provide करने वाले एक से अधिक "component" declare करना संभव नहीं है।

Routes एक ही जगह declare किए जाते हैं, दूसरी जगहों पर declared functions का उपयोग करके (decorators का उपयोग करने के बजाय जिन्हें endpoint handle करने वाली function के ठीक ऊपर रखा जा सकता है)। यह Flask (और Starlette) के तरीके की तुलना में Django के तरीके के अधिक करीब है। यह code में उन चीज़ों को अलग करता है जो अपेक्षाकृत tightly coupled हैं।

/// tip | **FastAPI** को इससे प्रेरणा मिली कि

Model attributes के "default" value का उपयोग करके data types के लिए extra validations define किए जाएँ। यह editor support को बेहतर बनाता है, और यह पहले Pydantic में उपलब्ध नहीं था।

इसने वास्तव में Pydantic के parts को update करने के लिए प्रेरित किया, ताकि वही validation declaration style support किया जा सके (यह सारी functionality अब Pydantic में पहले से उपलब्ध है)।

///

### [Hug](https://github.com/hugapi/hug) { #hug }

Hug उन पहले frameworks में से एक था जिसने Python type hints का उपयोग करके API parameter types की declaration implement की। यह एक बेहतरीन विचार था जिसने अन्य tools को भी ऐसा ही करने के लिए प्रेरित किया।

इसने अपनी declarations में standard Python types के बजाय custom types का उपयोग किया, लेकिन फिर भी यह एक बहुत बड़ा कदम आगे था।

यह पूरे API को JSON में declare करने वाला custom schema generate करने वाले पहले frameworks में से भी एक था।

यह OpenAPI और JSON Schema जैसे standard पर आधारित नहीं था। इसलिए इसे Swagger UI जैसे अन्य tools के साथ integrate करना straightforward नहीं होता। लेकिन फिर भी, यह एक बहुत innovative idea था।

इसमें एक दिलचस्प, uncommon feature है: उसी framework का उपयोग करके APIs और CLIs भी बनाना संभव है।

क्योंकि यह synchronous Python web frameworks (WSGI) के पिछले standard पर आधारित है, यह Websockets और अन्य चीज़ों को handle नहीं कर सकता, हालांकि इसका performance भी high है।

/// note | नोट

Hug को Timothy Crosley ने बनाया था, वही [`isort`](https://github.com/timothycrosley/isort) के creator हैं, जो Python files में imports को automatically sort करने के लिए एक बेहतरीन tool है।

///

/// tip | **FastAPI** को प्रेरित करने वाले विचार

Hug ने APIStar के parts को प्रेरित किया, और APIStar के साथ-साथ यह उन tools में से एक था जो मुझे सबसे promising लगे।

Hug ने **FastAPI** को parameters declare करने के लिए Python type hints का उपयोग करने, और API को automatically define करने वाला schema generate करने के लिए प्रेरित किया।

Hug ने **FastAPI** को headers और cookies set करने के लिए functions में `response` parameter declare करने के लिए प्रेरित किया।

///

### [APIStar](https://github.com/encode/apistar) (<= 0.5) { #apistar-0-5 }

**FastAPI** बनाने का निर्णय लेने से ठीक पहले मुझे **APIStar** server मिला। इसमें लगभग वह सब कुछ था जिसकी मुझे तलाश थी और इसका design बेहतरीन था।

यह उन पहले implementations में से एक था जो मैंने कभी देखे, जिसमें parameters और requests declare करने के लिए Python type hints का उपयोग करने वाला framework था (NestJS और Molten से पहले)। मुझे यह Hug के लगभग उसी समय मिला। लेकिन APIStar ने OpenAPI standard का उपयोग किया।

इसमें कई जगहों पर उन्हीं type hints के आधार पर automatic data validation, data serialization और OpenAPI schema generation था।

Body schema definitions Pydantic जैसे Python type hints का उपयोग नहीं करती थीं, यह Marshmallow के थोड़ा अधिक समान था, इसलिए editor support उतना अच्छा नहीं होता, लेकिन फिर भी, APIStar उपलब्ध सबसे अच्छा विकल्प था।

उस समय इसके performance benchmarks सबसे अच्छे थे (सिर्फ Starlette ने surpass किया था)।

शुरुआत में, इसमें automatic API documentation web UI नहीं था, लेकिन मुझे पता था कि मैं इसमें Swagger UI जोड़ सकता हूँ।

इसमें dependency injection system था। ऊपर चर्चा किए गए अन्य tools की तरह, इसमें components की pre-registration आवश्यक थी। लेकिन फिर भी, यह एक बेहतरीन feature था।

मैं कभी भी इसे full project में उपयोग नहीं कर पाया, क्योंकि इसमें security integration नहीं था, इसलिए मैं Flask-apispec पर आधारित full-stack generators के साथ मौजूद सभी features को replace नहीं कर सका। मेरे projects backlog में उस functionality को जोड़ने वाला pull request बनाने का विचार था।

लेकिन फिर, project का focus shift हो गया।

यह अब API web framework नहीं रहा, क्योंकि creator को Starlette पर focus करना था।

अब APIStar OpenAPI specifications validate करने के लिए tools का एक set है, web framework नहीं।

/// note | नोट

APIStar को Tom Christie ने बनाया था। वही व्यक्ति जिन्होंने बनाया:

* Django REST Framework
* Starlette (जिस पर **FastAPI** आधारित है)
* Uvicorn (Starlette और **FastAPI** द्वारा उपयोग किया जाता है)

///

/// tip | **FastAPI** को इससे प्रेरणा मिली कि

अस्तित्व में आए।

एक ही Python types के साथ कई चीज़ें (data validation, serialization और documentation) declare करने का विचार, जो साथ ही बेहतरीन editor support भी देता था, मुझे एक शानदार विचार लगा।

और लंबे समय तक समान framework की खोज करने और कई अलग-अलग alternatives को test करने के बाद, APIStar उपलब्ध सबसे अच्छा विकल्प था।

फिर APIStar ने server के रूप में अस्तित्व में रहना बंद कर दिया और Starlette बनाया गया, और यह ऐसे system के लिए एक नई बेहतर foundation था। यही **FastAPI** बनाने की अंतिम प्रेरणा थी।

मैं **FastAPI** को APIStar का "spiritual successor" मानता हूँ, जो इन सभी पिछले tools से मिली सीख के आधार पर features, typing system, और अन्य parts को improve और increase करता है।

///

## **FastAPI** द्वारा उपयोग किया गया { #used-by-fastapi }

### [Pydantic](https://docs.pydantic.dev/) { #pydantic }

Pydantic Python type hints के आधार पर data validation, serialization और documentation (JSON Schema का उपयोग करके) define करने के लिए एक library है।

यह इसे बेहद intuitive बनाता है।

यह Marshmallow से comparable है। हालांकि benchmarks में यह Marshmallow से तेज़ है। और क्योंकि यह उन्हीं Python type hints पर आधारित है, editor support बेहतरीन है।

/// tip | **FastAPI** इसे इन कामों के लिए उपयोग करता है

सभी data validation, data serialization और automatic model documentation (JSON Schema पर आधारित) handle करना।

फिर **FastAPI** उस JSON Schema data को लेता है और उसे OpenAPI में डालता है, उन सभी अन्य चीज़ों के अलावा जो यह करता है।

///

### [Starlette](https://www.starlette.dev/) { #starlette }

Starlette एक lightweight <dfn title="asynchronous Python web applications बनाने के लिए नया standard">ASGI</dfn> framework/toolkit है, जो high-performance asyncio services बनाने के लिए ideal है।

यह बहुत simple और intuitive है। इसे आसानी से extensible होने और modular components रखने के लिए design किया गया है।

इसमें है:

* बहुत प्रभावशाली performance.
* WebSocket support.
* In-process background tasks.
* Startup और shutdown events.
* HTTPX पर built test client.
* CORS, GZip, Static Files, Streaming responses.
* Session और Cookie support.
* 100% test coverage.
* 100% type annotated codebase.
* कुछ hard dependencies.

Starlette वर्तमान में tested सबसे तेज़ Python framework है। केवल Uvicorn ने इसे surpass किया है, जो framework नहीं, बल्कि server है।

Starlette सभी basic web microframework functionality प्रदान करता है।

लेकिन यह automatic data validation, serialization या documentation प्रदान नहीं करता।

यह उन मुख्य चीज़ों में से एक है जो **FastAPI** ऊपर से जोड़ता है, सब Python type hints (Pydantic का उपयोग करके) पर आधारित। इसके साथ dependency injection system, security utilities, OpenAPI schema generation, आदि।

/// note | तकनीकी विवरण

ASGI एक नया "standard" है जिसे Django core team members द्वारा develop किया जा रहा है। यह अभी भी "Python standard" (एक PEP) नहीं है, हालांकि वे ऐसा करने की प्रक्रिया में हैं।

फिर भी, इसे पहले से ही कई tools द्वारा "standard" के रूप में उपयोग किया जा रहा है। यह interoperability को बहुत बेहतर बनाता है, क्योंकि आप Uvicorn को किसी अन्य ASGI server (जैसे Daphne या Hypercorn) से switch कर सकते हैं, या आप ASGI compatible tools, जैसे `python-socketio`, जोड़ सकते हैं।

///

/// tip | **FastAPI** इसे इन कामों के लिए उपयोग करता है

सभी core web parts को handle करना। ऊपर से features जोड़ना।

Class `FastAPI` खुद सीधे class `Starlette` से inherit करती है।

इसलिए, जो कुछ भी आप Starlette के साथ कर सकते हैं, उसे आप सीधे **FastAPI** के साथ कर सकते हैं, क्योंकि यह मूल रूप से steroids पर Starlette है।

///

### [Uvicorn](https://www.uvicorn.dev/) { #uvicorn }

Uvicorn एक lightning-fast ASGI server है, जो uvloop और httptools पर बना है।

यह web framework नहीं, बल्कि server है। उदाहरण के लिए, यह paths द्वारा routing के लिए tools प्रदान नहीं करता। यह ऐसी चीज़ है जो Starlette (या **FastAPI**) जैसा framework ऊपर से प्रदान करेगा।

यह Starlette और **FastAPI** के लिए recommended server है।

/// tip | **FastAPI** इसे इस रूप में अनुशंसित करता है

**FastAPI** applications चलाने के लिए main web server।

आप asynchronous multi-process server पाने के लिए `--workers` command line option का भी उपयोग कर सकते हैं।

अधिक विवरण [Deployment](deployment/index.md) section में देखें।

///

## Benchmarks और speed { #benchmarks-and-speed }

Uvicorn, Starlette और FastAPI के बीच समझने, तुलना करने, और अंतर देखने के लिए, [Benchmarks](benchmarks.md) के बारे में section देखें।
