# Request Body { #request-body }

जब आपको किसी client (मान लें, एक browser) से अपनी API को data भेजना होता है, तो आप उसे **request body** के रूप में भेजते हैं।

**request** body वह data है जो client आपकी API को भेजता है। **response** body वह data है जो आपकी API client को भेजती है।

आपकी API को लगभग हमेशा **response** body भेजनी होती है। लेकिन clients को हर समय **request bodies** भेजने की ज़रूरत नहीं होती, कभी-कभी वे केवल एक path request करते हैं, शायद कुछ query parameters के साथ, लेकिन body नहीं भेजते।

**request** body घोषित करने के लिए, आप [Pydantic](https://docs.pydantic.dev/) models का उनकी पूरी शक्ति और लाभों के साथ उपयोग करते हैं।

/// note | नोट

Data भेजने के लिए, आपको इनमें से किसी एक का उपयोग करना चाहिए: `POST` (सबसे आम), `PUT`, `DELETE` या `PATCH`.

`GET` request के साथ body भेजने का व्यवहार specifications में undefined है, फिर भी, FastAPI इसे support करता है, केवल बहुत जटिल/चरम use cases के लिए।

क्योंकि इसे discouraged किया जाता है, Swagger UI वाले interactive docs `GET` का उपयोग करते समय body के लिए documentation नहीं दिखाएँगे, और बीच में मौजूद proxies इसे support नहीं कर सकते।

///

## Pydantic के `BaseModel` को import करें { #import-pydantics-basemodel }

सबसे पहले, आपको `pydantic` से `BaseModel` import करना होगा:

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## अपना data model बनाएँ { #create-your-data-model }

फिर आप अपने data model को एक class के रूप में घोषित करते हैं जो `BaseModel` से inherit करती है।

सभी attributes के लिए standard Python types का उपयोग करें:

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}


Query parameters घोषित करते समय की तरह, जब किसी model attribute का default value होता है, तो वह required नहीं होता। अन्यथा, वह required होता है। उसे केवल optional बनाने के लिए `None` का उपयोग करें।

उदाहरण के लिए, ऊपर दिया गया यह model इस तरह का JSON "`object`" (या Python `dict`) घोषित करता है:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...क्योंकि `description` और `tax` optional हैं (`None` के default value के साथ), यह JSON "`object`" भी valid होगा:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## इसे एक parameter के रूप में घोषित करें { #declare-it-as-a-parameter }

इसे अपनी *path operation* में जोड़ने के लिए, इसे उसी तरह घोषित करें जैसे आपने path और query parameters घोषित किए थे:

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

...और इसके type को आपके बनाए हुए model, `Item`, के रूप में घोषित करें।

## परिणाम { #results }

सिर्फ उस Python type declaration के साथ, **FastAPI** यह करेगा:

* request के body को JSON के रूप में पढ़ेगा।
* संबंधित types को convert करेगा (यदि ज़रूरत हो)।
* data को validate करेगा।
    * यदि data invalid है, तो यह एक अच्छा और स्पष्ट error return करेगा, जो ठीक-ठीक बताएगा कि गलत data कहाँ और क्या था।
* आपको प्राप्त data parameter `item` में देगा।
    * क्योंकि आपने इसे function में `Item` type का घोषित किया है, आपको इसके सभी attributes और उनके types के लिए पूरा editor support (completion, आदि) भी मिलेगा।
* आपके model के लिए [JSON Schema](https://json-schema.org) definitions generate करेगा, यदि आपके project के लिए उचित हो तो आप उन्हें कहीं और भी उपयोग कर सकते हैं।
* वे schemas generated OpenAPI schema का हिस्सा होंगे, और automatic documentation <abbr title="User Interfaces - उपयोगकर्ता इंटरफ़ेस">UIs</abbr> द्वारा उपयोग किए जाएँगे।

## स्वचालित docs { #automatic-docs }

आपके models के JSON Schemas आपके OpenAPI generated schema का हिस्सा होंगे, और interactive API docs में दिखाए जाएँगे:

<img src="/img/tutorial/body/image01.png">

और वे API docs में हर उस *path operation* के अंदर भी उपयोग किए जाएँगे जिसे उनकी ज़रूरत है:

<img src="/img/tutorial/body/image02.png">

## Editor support { #editor-support }

अपने editor में, अपने function के अंदर आपको हर जगह type hints और completion मिलेंगे (यदि आपको Pydantic model के बजाय `dict` मिला होता, तो ऐसा नहीं होता):

<img src="/img/tutorial/body/image03.png">

आपको incorrect type operations के लिए error checks भी मिलते हैं:

<img src="/img/tutorial/body/image04.png">

यह संयोग से नहीं है, पूरा framework इसी design के इर्द-गिर्द बनाया गया था।

और किसी भी implementation से पहले, design phase में इसे पूरी तरह test किया गया था, ताकि सुनिश्चित किया जा सके कि यह सभी editors के साथ काम करेगा।

इसे support करने के लिए Pydantic में भी कुछ बदलाव किए गए थे।

पिछले screenshots [Visual Studio Code](https://code.visualstudio.com) के साथ लिए गए थे।

लेकिन आपको [PyCharm](https://www.jetbrains.com/pycharm/) और अधिकांश अन्य Python editors के साथ भी वही editor support मिलेगा:

<img src="/img/tutorial/body/image05.png">

/// tip | सुझाव

यदि आप [PyCharm](https://www.jetbrains.com/pycharm/) को अपने editor के रूप में उपयोग करते हैं, तो आप [Pydantic PyCharm Plugin](https://github.com/koxudaxi/pydantic-pycharm-plugin/) का उपयोग कर सकते हैं।

यह Pydantic models के लिए editor support को बेहतर बनाता है, इन चीज़ों के साथ:

* auto-completion
* type checks
* refactoring
* searching
* inspections

///

## model का उपयोग करें { #use-the-model }

Function के अंदर, आप model object के सभी attributes को सीधे access कर सकते हैं:

{* ../../docs_src/body/tutorial002_py310.py *}

## Request body + path parameters { #request-body-path-parameters }

आप path parameters और request body को एक ही समय में घोषित कर सकते हैं।

**FastAPI** पहचानेगा कि वे function parameters जो path parameters से match करते हैं, उन्हें **path से लिया जाना चाहिए**, और वे function parameters जो Pydantic models के रूप में घोषित हैं, उन्हें **request body से लिया जाना चाहिए**।

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}


## Request body + path + query parameters { #request-body-path-query-parameters }

आप **body**, **path** और **query** parameters को भी एक ही समय में घोषित कर सकते हैं।

**FastAPI** उनमें से प्रत्येक को पहचानेगा और data को सही जगह से लेगा।

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

Function parameters को इस प्रकार पहचाना जाएगा:

* यदि parameter **path** में भी घोषित है, तो उसे path parameter के रूप में उपयोग किया जाएगा।
* यदि parameter **singular type** का है (जैसे `int`, `float`, `str`, `bool`, आदि), तो उसे **query** parameter के रूप में interpret किया जाएगा।
* यदि parameter को **Pydantic model** के type का घोषित किया गया है, तो उसे request **body** के रूप में interpret किया जाएगा।

/// note | नोट

FastAPI जान जाएगा कि `q` का value required नहीं है क्योंकि उसका default value `= None` है।

`str | None` का उपयोग FastAPI यह निर्धारित करने के लिए नहीं करता कि value required नहीं है, वह जान जाएगा कि यह required नहीं है क्योंकि इसका default value `= None` है।

लेकिन type annotations जोड़ने से आपका editor आपको बेहतर support दे सकेगा और errors detect कर सकेगा।

///

## Pydantic के बिना { #without-pydantic }

यदि आप Pydantic models का उपयोग नहीं करना चाहते, तो आप **Body** parameters का भी उपयोग कर सकते हैं। [Body - Multiple Parameters: Singular values in body](body-multiple-params.md#singular-values-in-body) के docs देखें।
