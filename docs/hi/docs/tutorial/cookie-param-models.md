# Cookie Parameter Models { #cookie-parameter-models }

अगर आपके पास संबंधित **cookies** का एक समूह है, तो आप उन्हें declare करने के लिए एक **Pydantic model** बना सकते हैं। 🍪

यह आपको **model को फिर से उपयोग** करने की अनुमति देगा, **कई जगहों** पर, और साथ ही सभी parameters के लिए validations और metadata एक साथ declare करने की भी। 😎

/// note | नोट

यह FastAPI version `0.115.0` से supported है। 🤓

///

/// tip | सुझाव

यही तकनीक `Query`, `Cookie`, और `Header` पर लागू होती है। 😎

///

## Pydantic Model के साथ Cookies { #cookies-with-a-pydantic-model }

जिन **cookie** parameters की आपको ज़रूरत है, उन्हें एक **Pydantic model** में declare करें, और फिर parameter को `Cookie` के रूप में declare करें:

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI** request में प्राप्त **cookies** से **हर field** के लिए data **extract** करेगा और आपको वह Pydantic model देगा जिसे आपने define किया है।

## Docs देखें { #check-the-docs }

आप `/docs` पर docs UI में defined cookies देख सकते हैं:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// note | नोट

ध्यान रखें कि, क्योंकि **browsers cookies को** विशेष तरीकों से और पर्दे के पीछे handle करते हैं, वे **JavaScript** को आसानी से उन्हें छूने की अनुमति **नहीं** देते।

अगर आप `/docs` पर **API docs UI** पर जाते हैं, तो आप अपने *path operations* के लिए cookies की **documentation** देख पाएँगे।

लेकिन भले ही आप **data भरें** और "Execute" पर क्लिक करें, क्योंकि docs UI **JavaScript** के साथ काम करता है, cookies नहीं भेजे जाएँगे, और आपको एक **error** message दिखाई देगा जैसे कि आपने कोई values लिखी ही न हों।

///

## Extra Cookies को forbid करें { #forbid-extra-cookies }

कुछ विशेष use cases में (शायद बहुत आम नहीं), आप उन cookies को **restrict** करना चाह सकते हैं जिन्हें आप प्राप्त करना चाहते हैं।

आपकी API के पास अब अपनी खुद की <dfn title="यह एक मज़ाक है, बस स्पष्ट करने के लिए। इसका cookie सहमति से कोई लेना-देना नहीं है, लेकिन यह मज़ेदार है कि अब API भी बेचारे cookies को reject कर सकती है। एक cookie लीजिए। 🍪">cookie सहमति</dfn> को control करने की शक्ति है। 🤪🍪

आप Pydantic के model configuration का उपयोग करके किसी भी `extra` fields को `forbid` कर सकते हैं:

{* ../../docs_src/cookie_param_models/tutorial002_an_py310.py hl[10] *}

अगर कोई client कुछ **extra cookies** भेजने की कोशिश करता है, तो उन्हें एक **error** response मिलेगा।

बेचारे cookie banners, जो <dfn title="यह एक और मज़ाक है। मेरी बात पर ध्यान न दें। अपनी cookie के लिए कुछ coffee लीजिए। ☕">API द्वारा उसे reject किए जाने</dfn> के लिए आपकी सहमति पाने में इतनी मेहनत करते हैं। 🍪

उदाहरण के लिए, अगर client `good-list-please` value के साथ एक `santa_tracker` cookie भेजने की कोशिश करता है, तो client को एक **error** response मिलेगा जो बताएगा कि `santa_tracker` <dfn title="Santa cookies की कमी को पसंद नहीं करता। 🎅 ठीक है, अब और cookie jokes नहीं।">cookie की अनुमति नहीं है</dfn>:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
```

## सारांश { #summary }

आप **FastAPI** में <dfn title="जाने से पहले एक आखिरी cookie लीजिए। 🍪">**cookies**</dfn> declare करने के लिए **Pydantic models** का उपयोग कर सकते हैं। 😎
