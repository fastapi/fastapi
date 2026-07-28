# Request Forms और Files { #request-forms-and-files }

आप `File` और `Form` का उपयोग करके files और form fields को एक ही समय में define कर सकते हैं।

/// note | नोट

अपलोड की गई files और/या form data प्राप्त करने के लिए, पहले [`python-multipart`](https://github.com/Kludex/python-multipart) install करें।

सुनिश्चित करें कि आप एक [virtual environment](../virtual-environments.md) बनाएँ, उसे activate करें, और फिर इसे install करें, उदाहरण के लिए:

```console
$ pip install python-multipart
```

///

## `File` और `Form` Import करें { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[3] *}

## `File` और `Form` parameters define करें { #define-file-and-form-parameters }

file और form parameters उसी तरह बनाएँ जैसे आप `Body` या `Query` के लिए बनाते हैं:

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[10:12] *}

files और form fields, form data के रूप में अपलोड किए जाएँगे और आपको files और form fields प्राप्त होंगे।

और आप कुछ files को `bytes` के रूप में और कुछ को `UploadFile` के रूप में declare कर सकते हैं।

/// warning | चेतावनी

आप एक *path operation* में कई `File` और `Form` parameters declare कर सकते हैं, लेकिन आप साथ ही ऐसे `Body` fields declare नहीं कर सकते जिन्हें आप JSON के रूप में प्राप्त करने की अपेक्षा करते हैं, क्योंकि request में body `application/json` के बजाय `multipart/form-data` का उपयोग करके encoded होगी।

यह **FastAPI** की कोई सीमा नहीं है, यह HTTP protocol का हिस्सा है।

///

## Recap { #recap }

जब आपको एक ही request में data और files प्राप्त करने की आवश्यकता हो, तो `File` और `Form` को साथ में उपयोग करें।
