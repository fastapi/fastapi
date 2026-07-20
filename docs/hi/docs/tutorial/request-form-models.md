# Form Models { #form-models }

आप FastAPI में **form fields** declare करने के लिए **Pydantic models** का उपयोग कर सकते हैं।

/// note | नोट

forms का उपयोग करने के लिए, पहले [`python-multipart`](https://github.com/Kludex/python-multipart) install करें।

सुनिश्चित करें कि आप एक [virtual environment](../virtual-environments.md) बनाते हैं, उसे activate करते हैं, और फिर इसे install करते हैं, उदाहरण के लिए:

```console
$ pip install python-multipart
```

///

/// note | नोट

यह FastAPI version `0.113.0` से supported है। 🤓

///

## Forms के लिए Pydantic Models { #pydantic-models-for-forms }

आपको बस उन fields के साथ एक **Pydantic model** declare करना है जिन्हें आप **form fields** के रूप में receive करना चाहते हैं, और फिर parameter को `Form` के रूप में declare करना है:

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI** request में मौजूद **form data** से **हर field** के लिए data **extract** करेगा और आपको वह Pydantic model देगा जिसे आपने define किया है।

## Docs जाँचें { #check-the-docs }

आप इसे `/docs` पर docs UI में verify कर सकते हैं:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Extra Form Fields को मना करें { #forbid-extra-form-fields }

कुछ खास use cases में (शायद बहुत आम नहीं), आप form fields को केवल उन तक **restrict** करना चाह सकते हैं जो Pydantic model में declare किए गए हैं। और किसी भी **extra** fields को **forbid** करना चाह सकते हैं।

/// note | नोट

यह FastAPI version `0.114.0` से supported है। 🤓

///

आप किसी भी `extra` fields को `forbid` करने के लिए Pydantic की model configuration का उपयोग कर सकते हैं:

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

अगर कोई client कुछ extra data भेजने की कोशिश करता है, तो उन्हें एक **error** response मिलेगा।

उदाहरण के लिए, अगर client ये form fields भेजने की कोशिश करता है:

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

तो उन्हें एक error response मिलेगा जो बताएगा कि field `extra` allowed नहीं है:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## सारांश { #summary }

आप FastAPI में form fields declare करने के लिए Pydantic models का उपयोग कर सकते हैं। 😎
