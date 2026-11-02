# Path Operation Configuration { #path-operation-configuration }

कई parameters हैं जिन्हें आप अपने *path operation decorator* को configure करने के लिए pass कर सकते हैं।

/// warning | चेतावनी

ध्यान दें कि ये parameters सीधे *path operation decorator* को pass किए जाते हैं, आपके *path operation function* को नहीं।

///

## Response Status Code { #response-status-code }

आप अपनी *path operation* की response में उपयोग किए जाने वाला (HTTP) `status_code` define कर सकते हैं।

आप सीधे `int` code pass कर सकते हैं, जैसे `404`।

लेकिन अगर आपको याद नहीं है कि हर number code किसके लिए है, तो आप `status` में shortcut constants का उपयोग कर सकते हैं:

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

वह status code response में उपयोग किया जाएगा और OpenAPI schema में जोड़ा जाएगा।

/// note | तकनीकी विवरण

आप `from starlette import status` भी उपयोग कर सकते हैं।

**FastAPI** आपकी सुविधा के लिए, developer के रूप में, वही `starlette.status` `fastapi.status` के रूप में प्रदान करता है। लेकिन यह सीधे Starlette से आता है।

///

## Tags { #tags }

आप अपनी *path operation* में tags जोड़ सकते हैं, parameter `tags` को `str` की `list` के साथ pass करें (आम तौर पर सिर्फ एक `str`):

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

वे OpenAPI schema में जोड़े जाएंगे और automatic documentation interfaces द्वारा उपयोग किए जाएंगे:

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Enums के साथ Tags { #tags-with-enums }

अगर आपके पास एक बड़ी application है, तो आप अंत में **कई tags** जमा कर सकते हैं, और आप यह सुनिश्चित करना चाहेंगे कि related *path operations* के लिए आप हमेशा **एक ही tag** का उपयोग करें।

इन मामलों में, tags को एक `Enum` में store करना समझदारी हो सकती है।

**FastAPI** इसे plain strings की तरह ही support करता है:

{* ../../docs_src/path_operation_configuration/tutorial002b_py310.py hl[1,8:10,13,18] *}

## Summary और description { #summary-and-description }

आप `summary` और `description` जोड़ सकते हैं:

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[17:18] *}

## Docstring से description { #description-from-docstring }

क्योंकि descriptions आम तौर पर लंबी होती हैं और कई lines में फैलती हैं, आप *path operation* की description को function <dfn title="documentation के लिए उपयोग की जाने वाली function के अंदर पहली expression के रूप में multi-line string (जो किसी भी variable को assign नहीं की गई होती)">docstring</dfn> में declare कर सकते हैं और **FastAPI** उसे वहीं से पढ़ेगा।

आप docstring में [Markdown](https://en.wikipedia.org/wiki/Markdown) लिख सकते हैं, इसे सही तरीके से interpret और display किया जाएगा (docstring indentation को ध्यान में रखते हुए)।

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

इसे interactive docs में उपयोग किया जाएगा:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## Response description { #response-description }

आप parameter `response_description` के साथ response description specify कर सकते हैं:

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[18] *}

/// note | नोट

ध्यान दें कि `response_description` विशेष रूप से response को refer करता है, जबकि `description` सामान्य रूप से *path operation* को refer करता है।

///

/// tip | सुझाव

OpenAPI specify करता है कि प्रत्येक *path operation* को response description required होती है।

इसलिए, अगर आप कोई provide नहीं करते, तो **FastAPI** अपने आप "Successful response" generate कर देगा।

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## एक *path operation* को Deprecated करें { #deprecate-a-path-operation }

अगर आपको किसी *path operation* को <dfn title="पुराना, इसका उपयोग न करने की सलाह दी जाती है">deprecated</dfn> के रूप में mark करना है, लेकिन उसे हटाना नहीं है, तो parameter `deprecated` pass करें:

{* ../../docs_src/path_operation_configuration/tutorial006_py310.py hl[16] *}

इसे interactive docs में स्पष्ट रूप से deprecated के रूप में mark किया जाएगा:

<img src="/img/tutorial/path-operation-configuration/image04.png">

देखें कि deprecated और non-deprecated *path operations* कैसे दिखते हैं:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## Recap { #recap }

आप *path operation decorators* को parameters pass करके अपनी *path operations* के लिए metadata आसानी से configure और add कर सकते हैं।
