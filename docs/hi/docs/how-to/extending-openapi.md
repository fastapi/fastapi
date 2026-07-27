# OpenAPI को विस्तारित करना { #extending-openapi }

कुछ मामलों में आपको generated OpenAPI schema को संशोधित करने की ज़रूरत हो सकती है।

इस section में आप देखेंगे कि कैसे।

## सामान्य process { #the-normal-process }

सामान्य (default) process इस प्रकार है।

एक `FastAPI` application (instance) में एक `.openapi()` method होता है, जिससे OpenAPI schema return करने की अपेक्षा की जाती है।

application object बनाने के हिस्से के रूप में, `/openapi.json` के लिए (या आपने अपने `openapi_url` में जो भी set किया है उसके लिए) एक *path operation* registered होता है।

यह बस application के `.openapi()` method के result के साथ एक JSON response return करता है।

Default रूप से, method `.openapi()` जो करता है वह यह है कि property `.openapi_schema` को check करता है कि उसमें contents हैं या नहीं, और उन्हें return करता है।

अगर नहीं हैं, तो यह उन्हें `fastapi.openapi.utils.get_openapi` में utility function का उपयोग करके generate करता है।

और वह function `get_openapi()` parameters के रूप में ये प्राप्त करता है:

* `title`: OpenAPI title, जो docs में दिखाया जाता है।
* `version`: आपके API का version, जैसे `2.5.0`।
* `openapi_version`: उपयोग की गई OpenAPI specification का version। Default रूप से, latest: `3.1.0`।
* `summary`: API का एक छोटा summary।
* `description`: आपके API का description, इसमें markdown शामिल हो सकता है और यह docs में दिखाया जाएगा।
* `routes`: application से routes, जो `app.routes` से लिए जाते हैं। FastAPI इन्हें registered *path operations* collect करने के लिए उपयोग करता है, जिनमें included routers से आने वाले भी शामिल हैं।

/// tip | तकनीकी विवरण

`app.routes` एक lower-level route tree है। इसमें route candidates शामिल हो सकते हैं जिन्हें FastAPI internally included routers के लिए उपयोग करता है, केवल final `APIRoute` objects ही नहीं।

आप फिर भी `app.routes` को `get_openapi()` में pass कर सकते हैं। FastAPI effective path operations collect करने के लिए उस route tree को traverse करेगा।

///

/// note | नोट

parameter `summary` OpenAPI 3.1.0 और उससे ऊपर में उपलब्ध है, जिसे FastAPI 0.99.0 और उससे ऊपर support करता है।

///

## Defaults को override करना { #overriding-the-defaults }

ऊपर दी गई जानकारी का उपयोग करके, आप OpenAPI schema generate करने और अपनी ज़रूरत के अनुसार प्रत्येक हिस्से को override करने के लिए उसी utility function का उपयोग कर सकते हैं।

उदाहरण के लिए, आइए [custom logo शामिल करने के लिए ReDoc का OpenAPI extension](https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo) जोड़ें।

### सामान्य **FastAPI** { #normal-fastapi }

सबसे पहले, अपनी पूरी **FastAPI** application सामान्य रूप से लिखें:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[1,4,7:9] *}

### OpenAPI schema generate करें { #generate-the-openapi-schema }

फिर, `custom_openapi()` function के अंदर, OpenAPI schema generate करने के लिए उसी utility function का उपयोग करें:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[2,15:21] *}

### OpenAPI schema को संशोधित करें { #modify-the-openapi-schema }

अब आप OpenAPI schema में `info` "object" में custom `x-logo` जोड़कर ReDoc extension जोड़ सकते हैं:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[22:24] *}

### OpenAPI schema को cache करें { #cache-the-openapi-schema }

आप अपनी generated schema store करने के लिए property `.openapi_schema` को "cache" के रूप में उपयोग कर सकते हैं।

इस तरह, जब भी कोई user आपके API docs खोलेगा, आपकी application को हर बार schema generate नहीं करना पड़ेगा।

यह केवल एक बार generate होगा, और फिर अगली requests के लिए वही cached schema उपयोग किया जाएगा।

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[13:14,25:26] *}

### Method को override करें { #override-the-method }

अब आप `.openapi()` method को अपने नए function से replace कर सकते हैं।

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[29] *}

### इसे check करें { #check-it }

जब आप [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) पर जाएंगे, तो आप देखेंगे कि आप अपना custom logo उपयोग कर रहे हैं (इस उदाहरण में, **FastAPI** का logo):

<img src="/img/tutorial/extending-openapi/image01.png">
