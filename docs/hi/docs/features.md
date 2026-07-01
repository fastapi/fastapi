# विशेषताएँ { #features }

## FastAPI की विशेषताएँ { #fastapi-features }

**FastAPI** आपको निम्नलिखित देता है:

### खुले standards पर आधारित { #based-on-open-standards }

* API बनाने के लिए [**OpenAPI**](https://github.com/OAI/OpenAPI-Specification), जिसमें <dfn title="इन्हें भी कहते हैं: endpoints, routes">path</dfn> <dfn title="इन्हें HTTP methods भी कहा जाता है, जैसे POST, GET, PUT, DELETE">operations</dfn>, parameters, request bodies, security, आदि की declarations शामिल हैं।
* [**JSON Schema**](https://json-schema.org/) के साथ अपने-आप data model documentation (क्योंकि OpenAPI खुद JSON Schema पर आधारित है)।
* इन standards के इर्द-गिर्द, गहन अध्ययन के बाद design किया गया। ऊपर से जोड़ी गई बाद की layer की तरह नहीं।
* इससे कई भाषाओं में automatic **client code generation** का उपयोग भी संभव होता है।

### Automatic docs { #automatic-docs }

Interactive API documentation और exploration web user interfaces। चूँकि framework OpenAPI पर आधारित है, कई options हैं, जिनमें से 2 default रूप से शामिल हैं।

* [**Swagger UI**](https://github.com/swagger-api/swagger-ui), interactive exploration के साथ, browser से सीधे अपनी API को call और test करें।

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* [**ReDoc**](https://github.com/Rebilly/ReDoc) के साथ वैकल्पिक API documentation।

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### बस Modern Python { #just-modern-python }

यह सब standard **Python type** declarations पर आधारित है (Pydantic के कारण)। सीखने के लिए कोई नया syntax नहीं। बस standard modern Python।

अगर आपको Python types का उपयोग कैसे करना है इसका 2 मिनट का refresher चाहिए (भले ही आप FastAPI का उपयोग न करते हों), तो यह छोटा tutorial देखें: [Python Types](python-types.md)।

आप types के साथ standard Python लिखते हैं:

```Python
from datetime import date

from pydantic import BaseModel

# किसी variable को str के रूप में declare करें
# और function के अंदर editor support पाएँ
def main(user_id: str):
    return user_id


# एक Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

जिसे फिर इस तरह उपयोग किया जा सकता है:

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

`**second_user_data` का अर्थ है:

`second_user_data` dict की keys और values को सीधे key-value arguments के रूप में पास करें, जो इसके बराबर है: `User(id=4, name="Mary", joined="2018-11-30")`

///

### Editor support { #editor-support }

पूरे framework को उपयोग में आसान और intuitive बनाने के लिए design किया गया था, और development शुरू करने से पहले ही सभी decisions को कई editors पर test किया गया, ताकि बेहतरीन development experience सुनिश्चित हो सके।

Python developer surveys में यह स्पष्ट है [कि सबसे अधिक उपयोग की जाने वाली features में से एक "autocompletion" है](https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features)।

पूरा **FastAPI** framework इसे पूरा करने के लिए design किया गया है। Autocompletion हर जगह काम करता है।

आपको शायद ही कभी docs पर वापस आना पड़ेगा।

आपका editor आपकी मदद इस तरह कर सकता है:

* [Visual Studio Code](https://code.visualstudio.com/) में:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* [PyCharm](https://www.jetbrains.com/pycharm/) में:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

आपको ऐसे code में भी completion मिलेगा जिसे आप पहले शायद असंभव समझते। उदाहरण के लिए, किसी request से आने वाले JSON body (जो nested भी हो सकता था) के अंदर `price` key।

अब गलत key names type करना, docs के बीच बार-बार आना-जाना, या यह खोजने के लिए ऊपर-नीचे scroll करना नहीं कि आपने आखिर `username` इस्तेमाल किया था या `user_name`।

### संक्षिप्त { #short }

इसमें हर चीज़ के लिए समझदारी भरे **defaults** हैं, और हर जगह optional configurations हैं। सभी parameters को आपकी जरूरत के अनुसार और आपकी API को define करने के लिए fine-tune किया जा सकता है।

लेकिन default रूप से, सब कुछ **"बस काम करता है"**।

### Validation { #validation }

* अधिकांश (या सभी?) Python **data types** के लिए validation, जिनमें शामिल हैं:
    * JSON objects (`dict`)।
    * JSON array (`list`) जो item types define करता है।
    * String (`str`) fields, जिनमें min और max lengths define होती हैं।
    * Numbers (`int`, `float`) जिनमें min और max values, आदि होती हैं।

* अधिक exotic types के लिए validation, जैसे:
    * URL।
    * Email।
    * UUID।
    * ...और अन्य।

सारा validation अच्छी तरह स्थापित और मजबूत **Pydantic** द्वारा संभाला जाता है।

### Security और authentication { #security-and-authentication }

Security और authentication integrated हैं। Databases या data models के साथ किसी समझौते के बिना।

OpenAPI में define की गई सभी security schemes, जिनमें शामिल हैं:

* HTTP Basic।
* **OAuth2** (**JWT tokens** के साथ भी)। [OAuth2 with JWT](tutorial/security/oauth2-jwt.md) पर tutorial देखें।
* API keys:
    * Headers में।
    * Query parameters में।
    * Cookies में, आदि।

साथ ही Starlette की सभी security features (**session cookies** सहित)।

सब कुछ reusable tools और components के रूप में बनाया गया है जिन्हें आपके systems, data stores, relational और NoSQL databases, आदि के साथ integrate करना आसान है।

### Dependency Injection { #dependency-injection }

FastAPI में एक बेहद आसान उपयोग वाला, लेकिन बेहद शक्तिशाली <dfn title='इन्हें "components", "resources", "services", "providers" भी कहा जाता है'><strong>Dependency Injection</strong></dfn> system शामिल है।

* Dependencies की भी dependencies हो सकती हैं, जिससे dependencies की hierarchy या **"graph"** बनता है।
* सब कुछ framework द्वारा **अपने-आप संभाला जाता है**।
* सभी dependencies requests से data मांग सकती हैं और **path operation** constraints और automatic documentation को augment कर सकती हैं।
* Dependencies में define किए गए *path operation* parameters के लिए भी **automatic validation**।
* Complex user authentication systems, **database connections**, आदि के लिए support।
* Databases, frontends, आदि के साथ **कोई समझौता नहीं**। लेकिन उन सभी के साथ आसान integration।

### असीमित "plug-ins" { #unlimited-plug-ins }

या दूसरे शब्दों में, उनकी जरूरत ही नहीं, अपनी जरूरत का code import करें और उपयोग करें।

कोई भी integration इतना सरल उपयोग करने योग्य design किया गया है (dependencies के साथ) कि आप अपनी application के लिए उसी structure और syntax का उपयोग करते हुए 2 lines के code में एक "plug-in" बना सकते हैं, जो आपकी *path operations* के लिए उपयोग होता है।

### Tested { #tested }

* 100% <dfn title="अपने-आप test किए जाने वाले code की मात्रा">test coverage</dfn>।
* 100% <dfn title="Python type annotations, जिनसे आपका editor और external tools आपको बेहतर support दे सकते हैं">type annotated</dfn> code base।
* Production applications में उपयोग किया गया।

## Starlette की विशेषताएँ { #starlette-features }

**FastAPI** [**Starlette**](https://www.starlette.dev/) के साथ पूरी तरह compatible है (और उसी पर आधारित है)। इसलिए, आपके पास जो भी अतिरिक्त Starlette code है, वह भी काम करेगा।

`FastAPI` वास्तव में `Starlette` का sub-class है। इसलिए, अगर आप पहले से Starlette जानते हैं या उपयोग करते हैं, तो अधिकांश functionality उसी तरह काम करेगी।

**FastAPI** के साथ आपको **Starlette** की सभी features मिलती हैं (क्योंकि FastAPI, steroids पर Starlette जैसा है):

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

Pydantic पर आधारित external libraries भी शामिल हैं, जैसे databases के लिए <abbr title="Object-Relational Mapper - ऑब्जेक्ट-रिलेशनल मैपर">ORM</abbr>s और <abbr title="Object-Document Mapper - ऑब्जेक्ट-डॉक्यूमेंट मैपर">ODM</abbr>s।

इसका अर्थ यह भी है कि कई मामलों में आप request से मिले उसी object को **सीधे database में** पास कर सकते हैं, क्योंकि सब कुछ अपने-आप validate हो जाता है।

दूसरी दिशा में भी यही लागू होता है, कई मामलों में आप database से मिले object को **सीधे client को** पास कर सकते हैं।

**FastAPI** के साथ आपको **Pydantic** की सभी features मिलती हैं (क्योंकि FastAPI सभी data handling के लिए Pydantic पर आधारित है):

* **कोई brainfuck नहीं**:
    * सीखने के लिए कोई नई schema definition micro-language नहीं।
    * अगर आप Python types जानते हैं तो आप जानते हैं कि Pydantic का उपयोग कैसे करना है।
* आपके **<abbr title="Integrated Development Environment - एकीकृत विकास वातावरण: code editor जैसा">IDE</abbr>/<dfn title="एक program जो code errors की जाँच करता है">linter</dfn>/दिमाग** के साथ अच्छा काम करता है:
    * क्योंकि pydantic data structures केवल उन classes के instances हैं जिन्हें आप define करते हैं; auto-completion, linting, mypy और आपकी intuition—सबको आपके validated data के साथ ठीक से काम करना चाहिए।
* **Complex structures** validate करें:
    * Hierarchical Pydantic models, Python `typing` के `List` और `Dict`, आदि का उपयोग।
    * और validators complex data schemas को स्पष्ट और आसानी से define, check और JSON Schema के रूप में document करने देते हैं।
    * आपके पास गहराई तक **nested JSON** objects हो सकते हैं और वे सभी validate और annotate किए जा सकते हैं।
* **Extensible**:
    * Pydantic custom data types define करने देता है या आप validator decorator से decorated model methods के साथ validation extend कर सकते हैं।
* 100% test coverage।
