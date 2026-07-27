# Path Parameters { #path-parameters }

आप Python format strings द्वारा इस्तेमाल किए जाने वाले समान syntax के साथ path "parameters" या "variables" declare कर सकते हैं:

{* ../../docs_src/path_params/tutorial001_py310.py hl[6:7] *}

path parameter `item_id` की value आपके function को argument `item_id` के रूप में pass की जाएगी।

इसलिए, अगर आप यह example run करते हैं और [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo) पर जाते हैं, तो आपको ऐसा response दिखाई देगा:

```JSON
{"item_id":"foo"}
```

## Types के साथ Path parameters { #path-parameters-with-types }

आप standard Python type annotations का उपयोग करके function में किसी path parameter का type declare कर सकते हैं:

{* ../../docs_src/path_params/tutorial002_py310.py hl[7] *}

इस मामले में, `item_id` को `int` declare किया गया है।

/// tip | सुझाव

इससे आपको अपने function के अंदर editor support मिलेगा, जिसमें error checks, completion आदि शामिल हैं।

///

## Data <dfn title="इसके नाम से भी जाना जाता है: serialization, parsing, marshalling">conversion</dfn> { #data-conversion }

अगर आप यह example run करते हैं और अपने browser में [http://127.0.0.1:8000/items/3](http://127.0.0.1:8000/items/3) खोलते हैं, तो आपको ऐसा response दिखाई देगा:

```JSON
{"item_id":3}
```

/// tip | सुझाव

ध्यान दें कि आपके function ने जो value प्राप्त की (और return की) वह `3` है, Python `int` के रूप में, न कि string `"3"`।

तो, उस type declaration के साथ, **FastAPI** आपको automatic request <dfn title="HTTP request से आने वाली string को Python data में बदलना">"parsing"</dfn> देता है।

///

## Data validation { #data-validation }

लेकिन अगर आप browser में [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo) पर जाते हैं, तो आपको ऐसा अच्छा HTTP error दिखाई देगा:

```JSON
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo"
    }
  ]
}
```

क्योंकि path parameter `item_id` की value `"foo"` थी, जो कि `int` नहीं है।

अगर आपने `int` के बजाय `float` दिया, तो भी वही error दिखाई देगा, जैसे: [http://127.0.0.1:8000/items/4.2](http://127.0.0.1:8000/items/4.2)

/// tip | सुझाव

तो, उसी Python type declaration के साथ, **FastAPI** आपको data validation देता है।

ध्यान दें कि error यह भी स्पष्ट रूप से बताता है कि validation किस जगह pass नहीं हुआ।

यह आपके API के साथ interact करने वाले code को develop और debug करते समय बेहद मददगार होता है।

///

## Documentation { #documentation }

और जब आप अपने browser में [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) खोलते हैं, तो आपको ऐसा automatic, interactive, API documentation दिखाई देगा:

<img src="/img/tutorial/path-params/image01.png">

/// tip | सुझाव

फिर से, बस उसी Python type declaration के साथ, **FastAPI** आपको automatic, interactive documentation देता है (Swagger UI को integrate करते हुए)।

ध्यान दें कि path parameter को integer के रूप में declare किया गया है।

///

## Standard-आधारित लाभ, वैकल्पिक documentation { #standards-based-benefits-alternative-documentation }

और क्योंकि generate किया गया schema [OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md) standard से है, इसलिए कई compatible tools हैं।

इसी वजह से, **FastAPI** स्वयं एक वैकल्पिक API documentation प्रदान करता है (ReDoc का उपयोग करते हुए), जिसे आप [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) पर access कर सकते हैं:

<img src="/img/tutorial/path-params/image02.png">

इसी तरह, कई compatible tools हैं। इनमें कई भाषाओं के लिए code generation tools भी शामिल हैं।

## Pydantic { #pydantic }

सारा data validation अंदरूनी तौर पर [Pydantic](https://docs.pydantic.dev/) द्वारा किया जाता है, इसलिए आपको इसके सभी लाभ मिलते हैं। और आप जानते हैं कि आप अच्छे हाथों में हैं।

आप `str`, `float`, `bool` और कई अन्य जटिल data types के साथ वही type declarations इस्तेमाल कर सकते हैं।

इनमें से कई को tutorial के अगले chapters में explore किया गया है।

## क्रम मायने रखता है { #order-matters }

*path operations* बनाते समय, आपको ऐसी स्थितियाँ मिल सकती हैं जहाँ आपके पास एक fixed path हो।

जैसे `/users/me`, मान लें कि यह current user के बारे में data प्राप्त करने के लिए है।

और फिर आपके पास `/users/{user_id}` path भी हो सकता है, किसी specific user के बारे में किसी user ID से data प्राप्त करने के लिए।

क्योंकि *path operations* का evaluation क्रम में किया जाता है, आपको यह सुनिश्चित करना होगा कि `/users/me` के लिए path, `/users/{user_id}` वाले path से पहले declare किया गया हो:

{* ../../docs_src/path_params/tutorial003_py310.py hl[6,11] *}

अन्यथा, `/users/{user_id}` के लिए path `/users/me` से भी match करेगा, यह "सोचते हुए" कि उसे `user_id` parameter मिल रहा है जिसकी value `"me"` है।

इसी तरह, आप किसी path operation को फिर से define नहीं कर सकते:

{* ../../docs_src/path_params/tutorial003b_py310.py hl[6,11] *}

पहला वाला हमेशा इस्तेमाल किया जाएगा क्योंकि path पहले match करता है।

## पहले से तय values { #predefined-values }

अगर आपके पास ऐसा *path operation* है जो एक *path parameter* प्राप्त करता है, लेकिन आप चाहते हैं कि संभव valid *path parameter* values पहले से तय हों, तो आप standard Python <abbr title="Enumeration">`Enum`</abbr> का उपयोग कर सकते हैं।

### एक `Enum` class बनाएं { #create-an-enum-class }

`Enum` import करें और एक sub-class बनाएं जो `str` और `Enum` से inherit करती हो।

`str` से inherit करने पर API docs यह जान पाएंगे कि values का type `string` होना चाहिए और उन्हें सही तरह से render कर पाएंगे।

फिर fixed values के साथ class attributes बनाएं, जो उपलब्ध valid values होंगी:

{* ../../docs_src/path_params/tutorial005_py310.py hl[1,6:9] *}

/// tip | सुझाव

अगर आप सोच रहे हैं, "AlexNet", "ResNet", और "LeNet" बस Machine Learning <dfn title="तकनीकी रूप से, Deep Learning model architectures">models</dfn> के नाम हैं।

///

### एक *path parameter* declare करें { #declare-a-path-parameter }

फिर आपके द्वारा बनाई गई enum class (`ModelName`) का उपयोग करके type annotation के साथ एक *path parameter* बनाएं:

{* ../../docs_src/path_params/tutorial005_py310.py hl[16] *}

### Docs देखें { #check-the-docs }

क्योंकि *path parameter* के लिए उपलब्ध values पहले से तय हैं, interactive docs उन्हें अच्छे से दिखा सकते हैं:

<img src="/img/tutorial/path-params/image03.png">

### Python *enumerations* के साथ काम करना { #working-with-python-enumerations }

*path parameter* की value एक *enumeration member* होगी।

#### *Enumeration members* की तुलना करें { #compare-enumeration-members }

आप इसकी तुलना अपने बनाए हुए enum `ModelName` में मौजूद *enumeration member* से कर सकते हैं:

{* ../../docs_src/path_params/tutorial005_py310.py hl[17] *}

#### *Enumeration value* प्राप्त करें { #get-the-enumeration-value }

आप `model_name.value` का उपयोग करके actual value (इस मामले में एक `str`) प्राप्त कर सकते हैं, या सामान्य रूप से, `your_enum_member.value`:

{* ../../docs_src/path_params/tutorial005_py310.py hl[20] *}

/// tip | सुझाव

आप `ModelName.lenet.value` के साथ value `"lenet"` भी access कर सकते हैं।

///

#### *Enumeration members* return करें { #return-enumeration-members }

आप अपने *path operation* से *enum members* return कर सकते हैं, यहाँ तक कि JSON body में nested भी (जैसे एक `dict`)।

Client को return करने से पहले उन्हें उनकी संबंधित values (इस मामले में strings) में convert कर दिया जाएगा:

{* ../../docs_src/path_params/tutorial005_py310.py hl[18,21,23] *}

अपने client में आपको ऐसा JSON response मिलेगा:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Paths रखने वाले Path parameters { #path-parameters-containing-paths }

मान लें आपके पास path `/files/{file_path}` के साथ एक *path operation* है।

लेकिन आपको `file_path` में स्वयं एक *path* रखना है, जैसे `home/johndoe/myfile.txt`।

तो, उस file के लिए URL कुछ ऐसा होगा: `/files/home/johndoe/myfile.txt`।

### OpenAPI support { #openapi-support }

OpenAPI किसी *path parameter* को उसके अंदर एक *path* रखने के लिए declare करने का तरीका support नहीं करता, क्योंकि इससे ऐसे scenarios बन सकते हैं जिन्हें test और define करना कठिन हो।

फिर भी, आप **FastAPI** में Starlette के internal tools में से एक का उपयोग करके यह कर सकते हैं।

और docs फिर भी काम करेंगे, हालांकि ऐसा कोई documentation नहीं जोड़ेंगे जो बताए कि parameter में path होना चाहिए।

### Path convertor { #path-convertor }

Starlette से सीधे एक option का उपयोग करके, आप इस तरह के URL का उपयोग करते हुए एक *path* रखने वाला *path parameter* declare कर सकते हैं:

```
/files/{file_path:path}
```

इस मामले में, parameter का नाम `file_path` है, और आखिरी हिस्सा, `:path`, इसे बताता है कि parameter किसी भी *path* से match करना चाहिए।

तो, आप इसे इसके साथ इस्तेमाल कर सकते हैं:

{* ../../docs_src/path_params/tutorial004_py310.py hl[6] *}

/// tip | सुझाव

आपको parameter में `/home/johndoe/myfile.txt` रखना पड़ सकता है, leading slash (`/`) के साथ।

उस मामले में, URL होगा: `/files//home/johndoe/myfile.txt`, `files` और `home` के बीच double slash (`//`) के साथ।

///

## Recap { #recap }

**FastAPI** के साथ, छोटे, सहज और standard Python type declarations का उपयोग करके, आपको मिलता है:

* Editor support: error checks, autocompletion आदि।
* Data "<dfn title="HTTP request से आने वाली string को Python data में बदलना">parsing</dfn>"
* Data validation
* API annotation और automatic documentation

और आपको इन्हें केवल एक बार declare करना होता है।

वैकल्पिक frameworks की तुलना में **FastAPI** का शायद यही मुख्य दिखने वाला लाभ है (raw performance के अलावा)।
