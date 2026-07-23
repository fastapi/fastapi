# Form Data { #form-data }

जब आपको JSON के बजाय form fields प्राप्त करने हों, तो आप `Form` का उपयोग कर सकते हैं।

/// note | नोट

forms का उपयोग करने के लिए, पहले [`python-multipart`](https://github.com/Kludex/python-multipart) install करें।

सुनिश्चित करें कि आप एक [virtual environment](../virtual-environments.md) बनाते हैं, उसे activate करते हैं, और फिर इसे install करते हैं, उदाहरण के लिए:

```console
$ pip install python-multipart
```

///

## `Form` Import करें { #import-form }

`fastapi` से `Form` import करें:

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[3] *}

## `Form` parameters परिभाषित करें { #define-form-parameters }

form parameters उसी तरह बनाएं जैसे आप `Body` या `Query` के लिए बनाते:

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[9] *}

उदाहरण के लिए, OAuth2 specification का उपयोग जिन तरीकों से किया जा सकता है उनमें से एक में (जिसे "password flow" कहा जाता है) `username` और `password` को form fields के रूप में भेजना required है।

<dfn title="specification">spec</dfn> के अनुसार fields के नाम बिल्कुल `username` और `password` होने चाहिए, और उन्हें JSON नहीं, बल्कि form fields के रूप में भेजा जाना चाहिए।

`Form` के साथ आप वही configurations declare कर सकते हैं जो `Body` (और `Query`, `Path`, `Cookie`) के साथ करते हैं, जिसमें validation, examples, alias (जैसे `username` के बजाय `user-name`), आदि शामिल हैं।

/// note | नोट

`Form` एक class है जो सीधे `Body` से inherit करती है।

///

/// tip | टिप

form bodies declare करने के लिए, आपको स्पष्ट रूप से `Form` का उपयोग करना होगा, क्योंकि इसके बिना parameters को query parameters या body (JSON) parameters के रूप में समझा जाएगा।

///

## "Form Fields" के बारे में { #about-form-fields }

HTML forms (`<form></form>`) आमतौर पर data को server पर भेजने के लिए उस data के लिए एक "special" encoding का उपयोग करते हैं, यह JSON से अलग होता है।

**FastAPI** यह सुनिश्चित करेगा कि उस data को JSON के बजाय सही जगह से पढ़ा जाए।

/// note | तकनीकी विवरण

forms से आने वाला data आमतौर पर "media type" `application/x-www-form-urlencoded` का उपयोग करके encoded होता है।

लेकिन जब form में files शामिल होती हैं, तो इसे `multipart/form-data` के रूप में encoded किया जाता है। files को handle करने के बारे में आप अगले chapter में पढ़ेंगे।

अगर आप इन encodings और form fields के बारे में अधिक पढ़ना चाहते हैं, तो [`POST` के लिए <abbr title="Mozilla Developer Network - मोज़िला डेवलपर नेटवर्क">MDN</abbr> web docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST) देखें।

///

/// warning | चेतावनी

आप एक *path operation* में कई `Form` parameters declare कर सकते हैं, लेकिन आप साथ में ऐसे `Body` fields declare नहीं कर सकते जिन्हें आप JSON के रूप में प्राप्त करने की उम्मीद करते हैं, क्योंकि request में body `application/json` के बजाय `application/x-www-form-urlencoded` का उपयोग करके encoded होगी।

यह **FastAPI** की limitation नहीं है, यह HTTP protocol का हिस्सा है।

///

## Recap { #recap }

form data input parameters declare करने के लिए `Form` का उपयोग करें।
