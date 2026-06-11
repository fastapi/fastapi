# विशेषताएँ { #features }

## FastAPI की विशेषताएँ { #fastapi-features }

**FastAPI** आपको निम्नलिखित सुविधाएँ देता है:

### खुले मानकों पर आधारित { #based-on-open-standards }

* API निर्माण के लिए [**OpenAPI**](https://github.com/OAI/OpenAPI-Specification), जिसमें <dfn title="जिन्हें endpoints, routes भी कहते हैं">path</dfn> <dfn title="जिन्हें HTTP methods भी कहते हैं, जैसे POST, GET, PUT, DELETE">operations</dfn>, parameters, request bodies, security आदि की घोषणाएँ शामिल हैं।
* [**JSON Schema**](https://json-schema.org/) के साथ स्वचालित data model documentation (क्योंकि OpenAPI स्वयं JSON Schema पर आधारित है)।
* इन मानकों को ध्यानपूर्वक अध्ययन के बाद डिज़ाइन किया गया है — बाद में जोड़ी गई परत के रूप में नहीं।
* इससे कई भाषाओं में स्वचालित **client code generation** भी संभव होती है।

### स्वचालित दस्तावेज़ीकरण { #automatic-docs }

इंटरैक्टिव API documentation और exploration के लिए web user interfaces। चूँकि framework OpenAPI पर आधारित है, इसलिए कई विकल्प उपलब्ध हैं — डिफ़ॉल्ट रूप से 2 शामिल हैं।

* [**Swagger UI**](https://github.com/swagger-api/swagger-ui), जिससे आप सीधे browser से अपनी API को explore, call और test कर सकते हैं।

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* वैकल्पिक API documentation [**ReDoc**](https://github.com/Rebilly/ReDoc) के साथ।

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### सिर्फ आधुनिक Python { #just-modern-python }

यह सब standard **Python type** declarations पर आधारित है (Pydantic की बदौलत)। कोई नया syntax सीखने की ज़रूरत नहीं। बस standard आधुनिक Python।

अगर आपको Python types के उपयोग का 2 मिनट का refresher चाहिए (भले ही आप FastAPI न उपयोग करें), तो यह छोटा tutorial देखें: [Python Types](python-types.md)।

आप types के साथ standard Python लिखते हैं:

```Python
from datetime import date

from pydantic import BaseModel

# एक variable को str के रूप में declare करें
# और function के अंदर editor support पाएँ
def main(user_id: str):
    return user_id


# एक Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

जिसे इस तरह उपयोग किया जा सकता है:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

/// note

`**second_user_data` का अर्थ है:

`second_user_data` dict की keys और values को सीधे key-value arguments के रूप में pass करें, जो इसके समतुल्य है: `User(id=4, name="Mary", joined="2018-11-30")`

///

### Editor support { #editor-support }

पूरा framework उपयोग में आसान और सहज होने के लिए डिज़ाइन किया गया है। Development शुरू करने से पहले ही सभी निर्णयों को कई editors पर test किया गया, ताकि बेहतरीन development experience सुनिश्चित हो सके।

Python developer surveys में यह स्पष्ट है कि ["autocompletion" सबसे अधिक उपयोग की जाने वाली विशेषताओं में से एक है](https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features)।

पूरा **FastAPI** framework इसी को पूरा करने के लिए बनाया गया है। Autocompletion हर जगह काम करती है।

आपको शायद ही कभी docs की तरफ वापस जाना पड़े।

आपका editor आपकी इस तरह मदद कर सकता है:

* [Visual Studio Code](https://code.visualstudio.com/) में:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* [PyCharm](https://www.jetbrains.com/pycharm/) में:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

आपको ऐसे code में भी completion मिलेगी जिसे आप पहले असंभव समझते थे। उदाहरण के लिए, किसी request से आने वाले JSON body (जो nested भी हो सकता है) के अंदर `price` key।

अब न गलत key names टाइप करने की ज़रूरत, न docs के बीच आगे-पीछे जाने की, न यह ढूंढने की कि आपने `username` उपयोग किया या `user_name`।

### संक्षिप्त { #short }

हर चीज़ के लिए समझदार **defaults** हैं, और हर जगह optional configurations उपलब्ध हैं। सभी parameters को आपकी ज़रूरत के अनुसार fine-tune किया जा सकता है।

लेकिन default रूप से, सब कुछ **"बस काम करता है"**।

### Validation { #validation }

* अधिकांश (या सभी?) Python **data types** के लिए validation, जिसमें शामिल हैं:
    * JSON objects (`dict`)।
    * JSON array (`list`) जिसमें item types परिभाषित हों।
    * String (`str`) fields, जिनमें minimum और maximum lengths परिभाषित हों।
    * Numbers (`int`, `float`) जिनमें minimum और maximum values हों, आदि।

* अधिक विशिष्ट types के लिए भी validation, जैसे:
    * URL।
    * Email।
    * UUID।
    * ...और अन्य।

सारी validation सुप्रसिद्ध और मज़बूत **Pydantic** द्वारा संभाली जाती है।

### Security और authentication { #security-and-authentication }

Security और authentication को बिना किसी समझौते के databases या data models के साथ integrate किया गया है।

OpenAPI में परिभाषित सभी security schemes, जिनमें शामिल हैं:

* HTTP Basic।
* **OAuth2** (**JWT tokens** के साथ भी)। [OAuth2 with JWT](tutorial/security/oauth2-jwt.md) tutorial देखें।
* API keys:
    * Headers में।
    * Query parameters में।
    * Cookies में, आदि।

साथ ही Starlette की सभी security विशेषताएँ (**session cookies** सहित)।

सब कुछ reusable tools और components के रूप में बना है जो आपके systems, data stores, relational और NoSQL databases आदि के साथ आसानी से integrate होते हैं।

### Dependency Injection { #dependency-injection }

FastAPI में एक अत्यंत आसान लेकिन अत्यंत शक्तिशाली <dfn title='"components", "resources", "services", "providers" के नाम से भी जाना जाता है'><strong>Dependency Injection</strong></dfn> system शामिल है।

* Dependencies की भी अपनी dependencies हो सकती हैं, जिससे dependencies का एक hierarchy या **"graph"** बनता है।
* सब कुछ framework द्वारा **स्वचालित रूप से संभाला** जाता है।
* सभी dependencies requests से data माँग सकती हैं और **path operation** constraints तथा automatic documentation को बेहतर बना सकती हैं।
* Dependencies में परिभाषित *path operation* parameters के लिए भी **स्वचालित validation**।
* जटिल user authentication systems, **database connections** आदि के लिए support।
* Databases, frontends आदि के साथ **कोई समझौता नहीं**, लेकिन सभी के साथ आसान integration।

### असीमित "plug-ins" { #unlimited-plug-ins }

या दूसरे शब्दों में, इनकी ज़रूरत ही नहीं — बस उस code को import करें और उपयोग करें जो आपको चाहिए।

कोई भी integration इतनी सरल होने के लिए डिज़ाइन की गई है (dependencies के साथ) कि आप अपने *path operations* जैसी ही structure और syntax उपयोग करके 2 lines of code में अपने application के लिए एक "plug-in" बना सकते हैं।

### परीक्षित { #tested }

* 100% <dfn title="जितने code को स्वचालित रूप से test किया गया है">test coverage</dfn>।
* 100% <dfn title="Python type annotations, जिससे आपका editor और बाहरी tools आपको बेहतर support दे सकें">type annotated</dfn> code base।
* Production applications में उपयोग किया जा रहा है।

## Starlette की विशेषताएँ { #starlette-features }

**FastAPI** [**Starlette**](https://www.starlette.dev/) के साथ पूरी तरह compatible है (और उस पर आधारित है)। इसलिए आपका कोई भी अतिरिक्त Starlette code भी काम करेगा।

`FastAPI` वास्तव में `Starlette` का एक sub-class है। इसलिए अगर आप पहले से Starlette जानते या उपयोग करते हैं, तो अधिकांश functionality उसी तरह काम करेगी।

**FastAPI** के साथ आपको **Starlette** की सभी विशेषताएँ मिलती हैं (क्योंकि FastAPI Starlette का ही उन्नत रूप है):

* वास्तव में प्रभावशाली performance। यह [सबसे तेज़ Python frameworks में से एक है, **NodeJS** और **Go** के बराबर](https://github.com/encode/starlette#performance)।
* **WebSocket** support।
* In-process background tasks।
* Startup और shutdown events।
* HTTPX पर बना test client।
* **CORS**, GZip, Static Files, Streaming responses।
* **Session और Cookie** support।
* 100% test coverage।
* 100% type annotated codebase।

## Pydantic की विशेषताएँ { #pydantic-features }

**FastAPI** [**Pydantic**](https://docs.pydantic.dev/) के साथ पूरी तरह compatible है (और उस पर आधारित है)। इसलिए आपका कोई भी अतिरिक्त Pydantic code भी काम करेगा।

इसमें Pydantic पर आधारित बाहरी libraries भी शामिल हैं, जैसे <abbr title="Object-Relational Mapper">ORM</abbr>s और <abbr title="Object-Document Mapper">ODM</abbr>s।

इसका अर्थ यह भी है कि कई मामलों में आप request से मिले object को **सीधे database में** pass कर सकते हैं, क्योंकि सब कुछ स्वचालित रूप से validated होता है।

यही बात उल्टे direction में भी लागू होती है — कई मामलों में database से मिले object को **सीधे client को** भेज सकते हैं।

**FastAPI** के साथ आपको **Pydantic** की सभी विशेषताएँ मिलती हैं (क्योंकि FastAPI data handling के लिए Pydantic पर आधारित है):

* **कोई जटिलता नहीं**:
    * कोई नई schema definition micro-language सीखने की ज़रूरत नहीं।
    * अगर आप Python types जानते हैं तो Pydantic उपयोग करना जानते हैं।
* आपके **<abbr title="Integrated Development Environment: code editor जैसा">IDE</abbr>/<dfn title="code errors जाँचने वाला program">linter</dfn>/दिमाग** के साथ अच्छी तरह काम करता है:
    * क्योंकि Pydantic data structures आपकी परिभाषित classes के instances हैं, auto-completion, linting, mypy और आपकी intuition सभी validated data के साथ सही से काम करती हैं।
* **जटिल structures** को validate करें:
    * Hierarchical Pydantic models, Python `typing` के `List` और `Dict` आदि का उपयोग।
    * Validators से जटिल data schemas को स्पष्ट और आसानी से define, check और JSON Schema के रूप में document किया जा सकता है।
    * आप गहरे **nested JSON** objects रख सकते हैं और उन सभी को validated और annotated करवा सकते हैं।
* **Extensible**:
    * Pydantic आपको custom data types define करने देता है, या आप validator decorator से decorated model methods के ज़रिए validation को extend कर सकते हैं।
* 100% test coverage।
