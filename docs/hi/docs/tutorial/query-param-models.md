# Query Parameter Models { #query-parameter-models }

अगर आपके पास संबंधित **query parameters** का एक समूह है, तो आप उन्हें declare करने के लिए एक **Pydantic model** बना सकते हैं।

इससे आप **model को फिर से उपयोग** कर पाएँगे, **कई जगहों** पर, और साथ ही सभी parameters के लिए validations और metadata एक साथ declare कर पाएँगे। 😎

/// note | नोट

यह FastAPI version `0.115.0` से supported है। 🤓

///

## Pydantic Model के साथ Query Parameters { #query-parameters-with-a-pydantic-model }

जिन **query parameters** की आपको ज़रूरत है उन्हें एक **Pydantic model** में declare करें, और फिर parameter को `Query` के रूप में declare करें:

{* ../../docs_src/query_param_models/tutorial001.py hl[9:13,17] *}

**FastAPI** request में मौजूद **query parameters** से **हर field** के लिए data **extract** करेगा और आपको वह Pydantic model देगा जिसे आपने define किया है।

## Docs देखें { #check-the-docs }

आप `/docs` पर docs UI में query parameters देख सकते हैं:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Extra Query Parameters को Forbid करें { #forbid-extra-query-parameters }

कुछ विशेष use cases में (शायद बहुत आम नहीं), आप उन query parameters को **restrict** करना चाह सकते हैं जिन्हें आप receive करना चाहते हैं।

आप किसी भी `extra` fields को `forbid` करने के लिए Pydantic की model configuration का उपयोग कर सकते हैं:

{* ../../docs_src/query_param_models/tutorial002.py hl[10] *}

अगर कोई client **query parameters** में कुछ **extra** data भेजने की कोशिश करता है, तो उसे एक **error** response मिलेगा।

उदाहरण के लिए, अगर client `plumbus` value के साथ `tool` query parameter भेजने की कोशिश करता है, जैसे:

```http
https://example.com/items/?limit=10&tool=plumbus
```

उसे एक **error** response मिलेगा जो बताएगा कि query parameter `tool` allowed नहीं है:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## Parameter Models को साथ में उपयोग करें { #combine-parameter-models }

आप कई query parameter models declare कर सकते हैं, और उन्हें अलग-अलग query parameters या dependencies के साथ उपयोग कर सकते हैं।

{* ../../docs_src/query_param_models/tutorial003.py hl[9:15,20:22] *}

request parameters एक ही स्तर पर रहते हैं।

```http
https://example.com/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt
```

query string में `pagination` या `filters` keys नहीं होती हैं। हर model अपने default values, field validators और model validators के साथ query parameters को स्वतंत्र रूप से validate करता है। यही बात तब भी लागू होती है जब models या अलग-अलग parameters dependencies में declare किए जाते हैं।

अगर models किसी parameter नाम या alias को साझा करते हैं, तो हर model उस request parameter को स्वतंत्र रूप से validate करता है। स्वतंत्र values के लिए अलग-अलग नाम या aliases का उपयोग करें। OpenAPI साझा parameter को एक बार सूचीबद्ध करता है, जैसे वह dependencies के साथ साझा किए गए parameters के लिए करता है, इसलिए साझा declarations में एक ही type और constraints का वर्णन होना चाहिए।

हर model की `extra` configuration सभी query parameters पर लागू होती है, जिनमें अन्य models या dependencies में declare किए गए parameters भी शामिल हैं। `extra="forbid"` के साथ, उस model के बाहर का कोई भी parameter अस्वीकार कर दिया जाता है। `extra="allow"` के साथ, वे parameters model extras के रूप में शामिल किए जाते हैं।

यह `Header` और `Cookie` models के लिए भी काम करता है।

## वैकल्पिक Query Parameter Models { #optional-query-parameter-models }

समूह को वैकल्पिक बनाने के लिए query parameter model को `| None` और `None` की default value के साथ declare करें।

{* ../../docs_src/query_param_models/tutorial004.py hl[18] *}

अगर न तो `start` और न ही `end` भेजा जाता है, तो `date_range` की value `None` होती है। अगर इनमें से कोई भी भेजा जाता है, तो FastAPI model को validate करता है और दोनों fields को required मानता है।

default के बिना `| None` का उपयोग करने पर parameter फिर भी required रहता है।

अतिरिक्त parameters model की `extra` configuration का पालन करते हैं। अनदेखा किए गए अतिरिक्त parameters से model को मौजूद नहीं माना जाता।

OpenAPI समूह के fields को अलग-अलग सूचीबद्ध करता है और उन्हें वैकल्पिक के रूप में चिह्नित करता है।

आप वैकल्पिक [header parameter models](header-param-models.md#optional-header-parameter-models) और [cookie parameter models](cookie-param-models.md#optional-cookie-parameter-models) भी declare कर सकते हैं।

## सारांश { #summary }

आप **FastAPI** में **query parameters** declare करने के लिए **Pydantic models** का उपयोग कर सकते हैं। 😎

/// tip | सुझाव

Spoiler alert: आप cookies और headers declare करने के लिए भी Pydantic models का उपयोग कर सकते हैं, लेकिन आप इसके बारे में tutorial में बाद में पढ़ेंगे। 🤫

///
