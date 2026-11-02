# Form Models { #form-models }

आप FastAPI में **form fields** declare करने के लिए **Pydantic models** का उपयोग कर सकते हैं।

/// note | नोट

forms का उपयोग करने के लिए, पहले [`python-multipart`](https://github.com/Kludex/python-multipart) install करें।

इसे अपने project में जोड़ें:

```console
$ uv add python-multipart
```

///

/// note | नोट

यह FastAPI version `0.113.0` से supported है। 🤓

///

## Forms के लिए Pydantic Models { #pydantic-models-for-forms }

आपको बस उन fields के साथ एक **Pydantic model** declare करना है जिन्हें आप **form fields** के रूप में receive करना चाहते हैं, और फिर parameter को `Form` के रूप में declare करना है:

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI** request में मौजूद **form data** से **हर field** के लिए data **extract** करेगा और आपको वह Pydantic model देगा जिसे आपने define किया है।

[HTML checkboxes](request-forms.md#boolean-form-fields) के लिए, boolean fields को `False` की default value के साथ declare करें।

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

## Form Models को संयोजित करें { #combine-form-models }

आप कई form models को अलग-अलग `Form` parameters के साथ संयोजित कर सकते हैं।

{* ../../docs_src/request_form_models/tutorial003_an_py310.py hl[9:14,19:21] *}

client `name`, `tags`, और `token` को form fields के रूप में भेजता है। हर model form fields को स्वतंत्र रूप से validate करता है।

हर model की `extra` configuration सभी form fields पर लागू होती है, जिनमें अन्य parameters या dependencies में declare किए गए fields और files भी शामिल हैं। `extra="forbid"` के साथ, उस model से बाहर का कोई भी field अस्वीकार कर दिया जाता है। `extra="allow"` के साथ, वे fields model extras के रूप में शामिल किए जाते हैं।

अगर कई declarations एक ही form field नाम का उपयोग करते हैं, तो हर declaration उस field की value को validate करता है। साझा fields के लिए संगत types और constraints का उपयोग करें ताकि OpenAPI schema उनका सुसंगत रूप से वर्णन कर सके।

## वैकल्पिक Form Models { #optional-form-models }

समूह को वैकल्पिक बनाने के लिए, form model को `| None` और `None` की default value के साथ declare करें।

{* ../../docs_src/request_form_models/tutorial005_an_py310.py hl[17] *}

अगर न तो `name` और न ही `age` भेजा जाता है, तो `profile` की value `None` होती है। अगर इनमें से कोई भी भेजा जाता है, तो FastAPI model को validate करता है और दोनों fields को required मानता है। खाली value सबमिट करना भी field प्रदान करना माना जाता है।

default value के बिना `| None` का उपयोग करने पर भी parameter required रहता है।

Extra fields model की `extra` configuration का पालन करते हैं। अनदेखा किए गए extras से model को मौजूद नहीं माना जाता।

केवल unchecked checkboxes वाला वैकल्पिक model छोड़ दिया जाता है। इसे स्पष्ट रूप से प्रदान करने के लिए `enabled=false` जैसी value भेजें।

## Form Models के वैकल्पिक Unions { #optional-unions-of-form-models }

आप models के वैकल्पिक union का भी उपयोग कर सकते हैं।

{* ../../docs_src/request_form_models/tutorial006_an_py310.py hl[9:16,21] *}

अगर कोई form fields नहीं भेजे जाते हैं, तो `contact` की value `None` होती है। `name` के साथ `kind=person`, या `company_name` के साथ `kind=company` भेजें। discriminator चुनता है कि किस model को validate करना है।

## Form Models के Unions को संयोजित करें { #combine-unions-of-form-models }

आप unions को अन्य form models, अलग-अलग `Form` parameters, और `File` parameters के साथ संयोजित कर सकते हैं। हर union को स्वतंत्र रूप से validate किया जाता है।

{* ../../docs_src/request_form_models/tutorial007_an_py310.py hl[31:35] *}

सभी fields एक ही form में भेजें। उदाहरण के लिए, `contact_type=person`, `name=Rick`, `notification_type=email`, `email=rick@example.com`, और `token=secret` भेजें।

`notification` की value `None` रखने के लिए notification fields छोड़ दें।

## Form Models और Files { #form-models-and-files }

आप form model को [file parameters](request-files.md) के साथ भी संयोजित कर सकते हैं।

{* ../../docs_src/request_form_models/tutorial004_an_py310.py hl[14] *}

यहाँ client `multipart/form-data` का उपयोग करके `name` field और `avatar` file भेजता है।

## सारांश { #summary }

आप FastAPI में form fields declare करने के लिए Pydantic models का उपयोग कर सकते हैं। 😎
