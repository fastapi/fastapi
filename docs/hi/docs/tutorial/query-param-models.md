# Query Parameter Models { #query-parameter-models }

अगर आपके पास संबंधित **query parameters** का एक समूह है, तो आप उन्हें declare करने के लिए एक **Pydantic model** बना सकते हैं।

इससे आप **model को फिर से उपयोग** कर पाएँगे, **कई जगहों** पर, और साथ ही सभी parameters के लिए validations और metadata एक साथ declare कर पाएँगे। 😎

/// note | नोट

यह FastAPI version `0.115.0` से supported है। 🤓

///

## Pydantic Model के साथ Query Parameters { #query-parameters-with-a-pydantic-model }

जिन **query parameters** की आपको ज़रूरत है उन्हें एक **Pydantic model** में declare करें, और फिर parameter को `Query` के रूप में declare करें:

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** request में मौजूद **query parameters** से **हर field** के लिए data **extract** करेगा और आपको वह Pydantic model देगा जिसे आपने define किया है।

## Docs देखें { #check-the-docs }

आप `/docs` पर docs UI में query parameters देख सकते हैं:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Extra Query Parameters को Forbid करें { #forbid-extra-query-parameters }

कुछ विशेष use cases में (शायद बहुत आम नहीं), आप उन query parameters को **restrict** करना चाह सकते हैं जिन्हें आप receive करना चाहते हैं।

आप किसी भी `extra` fields को `forbid` करने के लिए Pydantic की model configuration का उपयोग कर सकते हैं:

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

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

## सारांश { #summary }

आप **FastAPI** में **query parameters** declare करने के लिए **Pydantic models** का उपयोग कर सकते हैं। 😎

/// tip | सुझाव

Spoiler alert: आप cookies और headers declare करने के लिए भी Pydantic models का उपयोग कर सकते हैं, लेकिन आप इसके बारे में tutorial में बाद में पढ़ेंगे। 🤫

///
