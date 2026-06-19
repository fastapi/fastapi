# विशेषताएँ { #features }

## FastAPI की विशेषताएँ { #fastapi-features }

**FastAPI** आपको निम्नलिखित देता है:

### खुले मानकों पर आधारित { #based-on-open-standards }

* API बनाने के लिए [**OpenAPI**](https://github.com/OAI/OpenAPI-Specification), जिसमें <dfn title="इन्हें भी कहा जाता है: endpoints, routes">पाथ</dfn> <dfn title="इन्हें HTTP methods भी कहा जाता है, जैसे POST, GET, PUT, DELETE">ऑपरेशन्स</dfn>, parameters, request bodies, security, आदि की घोषणाएँ शामिल हैं।
* [**JSON Schema**](https://json-schema.org/) के साथ automatic data model documentation (क्योंकि OpenAPI स्वयं JSON Schema पर आधारित है)।
* इन मानकों के इर्द-गिर्द डिज़ाइन किया गया, एक बहुत सावधानीपूर्वक अध्ययन के बाद। ऊपर से बाद में जोड़ी गई परत की तरह नहीं।
* यह कई भाषाओं में automatic **client code generation** का उपयोग करने की भी अनुमति देता है।

### Automatic docs { #automatic-docs }

Interactive API documentation और exploration web user interfaces। क्योंकि framework OpenAPI पर आधारित है, कई विकल्प हैं, जिनमें 2 default रूप से शामिल हैं।

* [**Swagger UI**](https://github.com/swagger-api/swagger-ui), interactive exploration के साथ, अपने API को सीधे browser से call और test करें।

![Swagger UI इंटरैक्शन](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* [**ReDoc**](https://github.com/Rebilly/ReDoc) के साथ वैकल्पिक API documentation।

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### सिर्फ़ आधुनिक Python { #just-modern-python }

यह सब standard **Python type** declarations पर आधारित है (Pydantic की बदौलत)। सीखने के लिए कोई नया syntax नहीं। सिर्फ़ standard modern Python।

अगर आपको Python types का उपयोग कैसे करें, इसका 2 मिनट का छोटा refresher चाहिए (भले ही आप FastAPI का उपयोग न करते हों), तो छोटा tutorial देखें: [Python Types](python-types.md)।

आप types के साथ standard Python लिखते हैं:

```Python
from datetime import date

from pydantic import BaseModel

# किसी वेरिएबल को str के रूप में घोषित करें
# और फ़ंक्शन के अंदर एडिटर सपोर्ट पाएँ
def main(user_id: str):
    return user_id


# एक Pydantic मॉडल
class User(BaseModel):
    id: int
    name: str
    joined: date
```

फिर उसे इस तरह उपयोग किया जा सकता है:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

/// note | नोट

`**second_user_data` का मतलब है:

`second_user_data` dict की keys और values को सीधे key-value arguments के रूप में पास करें, जो इसके बराबर है: `User(id=4, name="Mary", joined="2018-11-30")`

///

### एडिटर सपोर्ट { #editor-support }

पूरे framework को उपयोग में आसान और सहज बनाने के लिए डिज़ाइन किया गया था, विकास शुरू करने से पहले ही सभी निर्णयों को कई editors पर test किया गया, ताकि सबसे अच्छा development experience सुनिश्चित किया जा सके।

Python developer surveys में, यह स्पष्ट है [कि सबसे अधिक उपयोग की जाने वाली सुविधाओं में से एक "autocompletion" है](https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features)।

पूरा **FastAPI** framework इसे पूरा करने के लिए डिज़ाइन किया गया है। Autocompletion हर जगह काम करता है।

आपको शायद ही कभी docs पर वापस आने की आवश्यकता होगी।

यहाँ बताया गया है कि आपका editor आपकी कैसे मदद कर सकता है:

* [Visual Studio Code](https://code.visualstudio.com/) में:

![एडिटर सपोर्ट](https://fastapi.tiangolo.com/img/vscode-completion.png)

* [PyCharm](https://www.jetbrains.com/pycharm/) में:

![एडिटर सपोर्ट](https://fastapi.tiangolo.com/img/pycharm-completion.png)

आपको ऐसे code में completion मिलेगा जिसे आप पहले असंभव भी मान सकते थे। जैसे, किसी request से आने वाले JSON body (जो nested भी हो सकता था) के अंदर `price` key।

अब गलत key names टाइप करने, docs के बीच आगे-पीछे जाने, या यह खोजने के लिए ऊपर-नीचे scroll करने की ज़रूरत नहीं कि आपने आखिर `username` उपयोग किया था या `user_name`।

### संक्षिप्त { #short }

हर चीज़ के लिए इसके समझदार **defaults** हैं, और हर जगह optional configurations हैं। सभी parameters को आपकी ज़रूरत के अनुसार और आपकी ज़रूरत की API define करने के लिए fine-tune किया जा सकता है।

लेकिन default रूप से, सब कुछ **"बस काम करता है"**।

### Validation { #validation }

* अधिकांश (या सभी?) Python **data types** के लिए validation, जिनमें शामिल हैं:
    * JSON objects (`dict`)।
    * JSON array (`list`) जो item types define करता है।
    * String (`str`) fields, जिनमें min और max lengths define होती हैं।
    * Numbers (`int`, `float`) जिनमें min और max values, आदि।

* अधिक असामान्य types के लिए validation, जैसे:
    * URL।
    * Email।
    * UUID।
    * ...और अन्य।

सारी validation well-established और robust **Pydantic** द्वारा handle की जाती है।

### Security और authentication { #security-and-authentication }

Security और authentication integrated हैं। Databases या data models के साथ किसी भी compromise के बिना।

OpenAPI में define की गई सभी security schemes, जिनमें शामिल हैं:

* HTTP Basic।
* **OAuth2** (**JWT tokens** के साथ भी)। [OAuth2 with JWT](tutorial/security/oauth2-jwt.md) पर tutorial देखें।
* API keys:
    * Headers में।
    * Query parameters में।
    * Cookies में, आदि।

साथ ही Starlette की सभी security features (जिसमें **session cookies** भी शामिल हैं)।

सब reusable tools और components के रूप में बनाए गए हैं, जिन्हें आपके systems, data stores, relational और NoSQL databases, आदि के साथ integrate करना आसान है।

### Dependency Injection { #dependency-injection }

FastAPI में एक बेहद आसान, लेकिन बेहद शक्तिशाली <dfn title='इन्हें "components", "resources", "services", "providers" भी कहा जाता है'><strong>Dependency Injection</strong></dfn> system शामिल है।

* Dependencies की भी dependencies हो सकती हैं, जिससे dependencies की hierarchy या **"graph"** बनता है।
* सब कुछ framework द्वारा **automatically handled** होता है।
* सभी dependencies requests से data मांग सकती हैं और **path operation** constraints तथा automatic documentation को बढ़ा सकती हैं।
* Dependencies में define किए गए *path operation* parameters के लिए भी **automatic validation**।
* जटिल user authentication systems, **database connections**, आदि के लिए support।
* Databases, frontends, आदि के साथ **कोई compromise नहीं**। लेकिन उन सभी के साथ आसान integration।

### असीमित "plug-ins" { #unlimited-plug-ins }

या दूसरे शब्दों में, उनकी आवश्यकता नहीं है, अपनी ज़रूरत का code import करें और उपयोग करें।

किसी भी integration को (dependencies के साथ) उपयोग में इतना सरल बनाने के लिए डिज़ाइन किया गया है कि आप अपनी application के लिए उसी structure और syntax का उपयोग करके 2 lines of code में एक "plug-in" बना सकते हैं, जो आपके *path operations* के लिए उपयोग होता है।

### Tested { #tested }

* 100% <dfn title="code की वह मात्रा जो automatically test की जाती है">test coverage</dfn>।
* 100% <dfn title="Python type annotations, जिनसे आपका editor और external tools आपको बेहतर support दे सकते हैं">type annotated</dfn> code base।
* Production applications में उपयोग किया गया।

## Starlette की विशेषताएँ { #starlette-features }

**FastAPI** [**Starlette**](https://www.starlette.dev/) के साथ पूरी तरह compatible है (और उसी पर आधारित है)। इसलिए, आपके पास जो भी अतिरिक्त Starlette code है, वह भी काम करेगा।

`FastAPI` वास्तव में `Starlette` का एक sub-class है। इसलिए, अगर आप पहले से Starlette जानते हैं या उपयोग करते हैं, तो अधिकांश functionality उसी तरह काम करेगी।

**FastAPI** के साथ आपको **Starlette** की सभी features मिलती हैं (क्योंकि FastAPI मूलतः steroids पर Starlette है):

* सचमुच प्रभावशाली performance। यह [उपलब्ध सबसे तेज़ Python frameworks में से एक है, **NodeJS** और **Go** के बराबर](https://github.com/encode/starlette#performance)।
* **WebSocket** support।
* In-process background tasks।
* Startup और shutdown events।
* HTTPX पर बना test client।
* **CORS**, GZip, Static Files, Streaming responses।
* **Session और Cookie** support।
* 100% test coverage।
* 100% type annotated codebase।

## Pydantic की विशेषताएँ { #pydantic-features }

**FastAPI** [**Pydantic**](https://docs.pydantic.dev/) के साथ पूरी तरह compatible है (और उसी पर आधारित है)। इसलिए, आपके पास जो भी अतिरिक्त Pydantic code है, वह भी काम करेगा।

इसमें Pydantic पर आधारित external libraries भी शामिल हैं, जैसे databases के लिए <abbr title="Object-Relational Mapper - ऑब्जेक्ट-रिलेशनल मैपर">ORM</abbr>s और <abbr title="Object-Document Mapper - ऑब्जेक्ट-डॉक्यूमेंट मैपर">ODM</abbr>s।

इसका यह भी मतलब है कि कई मामलों में आप request से मिलने वाले उसी object को **सीधे database में** पास कर सकते हैं, क्योंकि सब कुछ automatically validated होता है।

उसी तरह उल्टा भी लागू होता है, कई मामलों में आप database से मिलने वाले object को **सीधे client को** पास कर सकते हैं।

**FastAPI** के साथ आपको **Pydantic** की सभी features मिलती हैं (क्योंकि FastAPI सभी data handling के लिए Pydantic पर आधारित है):

* **कोई brainfuck नहीं**:
    * सीखने के लिए कोई नई schema definition micro-language नहीं।
    * अगर आप Python types जानते हैं, तो आप जानते हैं कि Pydantic का उपयोग कैसे करना है।
* आपके **<abbr title="Integrated Development Environment - इंटीग्रेटेड डेवलपमेंट एनवायरनमेंट: code editor जैसा">IDE</abbr>/<dfn title="एक program जो code errors की जाँच करता है">लिंटर</dfn>/brain** के साथ अच्छी तरह काम करता है:
    * क्योंकि pydantic data structures केवल उन classes के instances होते हैं जिन्हें आप define करते हैं; auto-completion, linting, mypy और आपकी intuition, सभी आपके validated data के साथ सही ढंग से काम करने चाहिए।
* **Complex structures** validate करें:
    * Hierarchical Pydantic models, Python `typing` के `List` और `Dict`, आदि का उपयोग।
    * और validators complex data schemas को JSON Schema के रूप में स्पष्ट और आसानी से define, check और document करने देते हैं।
    * आपके पास deeply **nested JSON** objects हो सकते हैं और वे सभी validated और annotated हो सकते हैं।
* **Extensible**:
    * Pydantic custom data types को define करने देता है या आप validator decorator से decorated model पर methods के साथ validation extend कर सकते हैं।
* 100% test coverage।
