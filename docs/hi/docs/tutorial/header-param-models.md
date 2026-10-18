# Header Parameter Models { #header-parameter-models }

अगर आपके पास संबंधित **header parameters** का एक समूह है, तो आप उन्हें declare करने के लिए एक **Pydantic model** बना सकते हैं।

इससे आप **model को फिर से उपयोग** कर पाएंगे, **कई जगहों** पर, और साथ ही सभी parameters के लिए validations और metadata एक साथ declare कर पाएंगे। 😎

/// note | नोट

यह FastAPI version `0.115.0` से समर्थित है। 🤓

///

## Pydantic Model के साथ Header Parameters { #header-parameters-with-a-pydantic-model }

जिन **header parameters** की आपको ज़रूरत है, उन्हें एक **Pydantic model** में declare करें, और फिर parameter को `Header` के रूप में declare करें:

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI** request में **headers** से **हर field** का data **extract** करेगा और आपको वह Pydantic model देगा जिसे आपने define किया है।

## Docs देखें { #check-the-docs }

आप `/docs` पर docs UI में required headers देख सकते हैं:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## Extra Headers को मना करें { #forbid-extra-headers }

कुछ विशेष use cases में (शायद बहुत आम नहीं), आप उन headers को **restrict** करना चाह सकते हैं जिन्हें आप receive करना चाहते हैं।

आप Pydantic की model configuration का उपयोग करके किसी भी `extra` fields को `forbid` कर सकते हैं:

{* ../../docs_src/header_param_models/tutorial002_an_py310.py hl[10] *}

अगर कोई client कुछ **extra headers** भेजने की कोशिश करता है, तो उन्हें एक **error** response मिलेगा।

उदाहरण के लिए, अगर client `plumbus` के value के साथ एक `tool` header भेजने की कोशिश करता है, तो उन्हें एक **error** response मिलेगा जो बताएगा कि header parameter `tool` की अनुमति नहीं है:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## Convert Underscores को Disable करें { #disable-convert-underscores }

नियमित header parameters की तरह ही, जब parameter names में underscore characters होते हैं, तो वे **स्वचालित रूप से hyphens में convert** हो जाते हैं।

उदाहरण के लिए, अगर आपके code में header parameter `save_data` है, तो अपेक्षित HTTP header `save-data` होगा, और docs में भी वह इसी तरह दिखाई देगा।

अगर किसी कारण से आपको इस automatic conversion को disable करना है, तो आप header parameters के लिए Pydantic models में भी ऐसा कर सकते हैं।

{* ../../docs_src/header_param_models/tutorial003_an_py310.py hl[19] *}

/// warning | चेतावनी

`convert_underscores` को `False` पर set करने से पहले, ध्यान रखें कि कुछ HTTP proxies और servers underscores वाले headers के उपयोग की अनुमति नहीं देते।

///

## सारांश { #summary }

आप **FastAPI** में **headers** declare करने के लिए **Pydantic models** का उपयोग कर सकते हैं। 😎
