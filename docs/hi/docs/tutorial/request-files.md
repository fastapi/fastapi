# Request Files { #request-files }

आप client द्वारा अपलोड की जाने वाली files को `File` का उपयोग करके परिभाषित कर सकते हैं।

/// note | नोट

अपलोड की गई files प्राप्त करने के लिए, पहले [`python-multipart`](https://github.com/Kludex/python-multipart) install करें।

सुनिश्चित करें कि आप एक [virtual environment](../virtual-environments.md) बनाते हैं, उसे activate करते हैं, और फिर इसे install करते हैं, उदाहरण के लिए:

```console
$ pip install python-multipart
```

ऐसा इसलिए है क्योंकि अपलोड की गई files "form data" के रूप में भेजी जाती हैं।

///

## `File` Import करें { #import-file }

`fastapi` से `File` और `UploadFile` import करें:

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[3] *}

## `File` Parameters परिभाषित करें { #define-file-parameters }

file parameters उसी तरह बनाएं जैसे आप `Body` या `Form` के लिए बनाते हैं:

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[9] *}

/// note | नोट

`File` एक class है जो सीधे `Form` से inherit करती है।

लेकिन याद रखें कि जब आप `fastapi` से `Query`, `Path`, `File` और अन्य import करते हैं, तो वे वास्तव में functions होते हैं जो विशेष classes return करते हैं।

///

/// tip | सुझाव

File bodies घोषित करने के लिए, आपको `File` का उपयोग करना होगा, क्योंकि अन्यथा parameters को query parameters या body (JSON) parameters के रूप में समझा जाएगा।

///

files "form data" के रूप में अपलोड की जाएंगी।

यदि आप अपने *path operation function* parameter का type `bytes` के रूप में घोषित करते हैं, तो **FastAPI** आपके लिए file पढ़ेगा और आपको सामग्री `bytes` के रूप में प्राप्त होगी।

ध्यान रखें कि इसका मतलब है कि पूरी सामग्री memory में संग्रहीत होगी। यह छोटी files के लिए अच्छी तरह काम करेगा।

लेकिन कई मामलों में आपको `UploadFile` का उपयोग करने से लाभ हो सकता है।

## `UploadFile` के साथ File Parameters { #file-parameters-with-uploadfile }

`UploadFile` type के साथ file parameter परिभाषित करें:

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[14] *}

`bytes` की तुलना में `UploadFile` का उपयोग करने के कई फायदे हैं:

* आपको parameter के default value में `File()` का उपयोग नहीं करना पड़ता।
* यह एक "spooled" file का उपयोग करता है:
    * एक file जो अधिकतम size limit तक memory में संग्रहीत होती है, और इस limit को पार करने के बाद disk पर संग्रहीत होती है।
* इसका मतलब है कि यह images, videos, बड़े binaries आदि जैसी बड़ी files के लिए सारी memory का उपयोग किए बिना अच्छी तरह काम करेगा।
* आप अपलोड की गई file से metadata प्राप्त कर सकते हैं।
* इसमें [file-like](https://docs.python.org/3/glossary.html#term-file-like-object) `async` interface है।
* यह एक वास्तविक Python [`SpooledTemporaryFile`](https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile) object expose करता है जिसे आप सीधे अन्य libraries को पास कर सकते हैं जो file-like object की अपेक्षा करती हैं।

### `UploadFile` { #uploadfile }

`UploadFile` में निम्नलिखित attributes होते हैं:

* `filename`: मूल file name के साथ एक `str` जो अपलोड किया गया था (जैसे `myimage.jpg`)।
* `content_type`: content type (MIME type / media type) के साथ एक `str` (जैसे `image/jpeg`)।
* `file`: एक [`SpooledTemporaryFile`](https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile) (एक [file-like](https://docs.python.org/3/glossary.html#term-file-like-object) object)। यह वास्तविक Python file object है जिसे आप सीधे अन्य functions या libraries को पास कर सकते हैं जो "file-like" object की अपेक्षा करती हैं।

`UploadFile` में निम्नलिखित `async` methods होते हैं। ये सभी अंदर से संबंधित file methods को call करते हैं (internal `SpooledTemporaryFile` का उपयोग करके)।

* `write(data)`: `data` (`str` या `bytes`) को file में लिखता है।
* `read(size)`: file के `size` (`int`) bytes/characters पढ़ता है।
* `seek(offset)`: file में byte position `offset` (`int`) पर जाता है।
    * उदाहरण के लिए, `await myfile.seek(0)` file की शुरुआत पर जाएगा।
    * यह विशेष रूप से तब उपयोगी है जब आप एक बार `await myfile.read()` चलाते हैं और फिर सामग्री को दोबारा पढ़ने की आवश्यकता होती है।
* `close()`: file को बंद करता है।

क्योंकि ये सभी methods `async` methods हैं, आपको उन्हें "await" करना होगा।

उदाहरण के लिए, एक `async` *path operation function* के अंदर आप सामग्री इस तरह प्राप्त कर सकते हैं:

```Python
contents = await myfile.read()
```

यदि आप एक सामान्य `def` *path operation function* के अंदर हैं, तो आप सीधे `UploadFile.file` access कर सकते हैं, उदाहरण के लिए:

```Python
contents = myfile.file.read()
```

/// note | `async` तकनीकी विवरण

जब आप `async` methods का उपयोग करते हैं, तो **FastAPI** file methods को threadpool में चलाता है और उनके लिए await करता है।

///

/// note | Starlette तकनीकी विवरण

**FastAPI** का `UploadFile` सीधे **Starlette** के `UploadFile` से inherit करता है, लेकिन **Pydantic** और FastAPI के अन्य भागों के साथ इसे compatible बनाने के लिए कुछ आवश्यक हिस्से जोड़ता है।

///

## "Form Data" क्या है { #what-is-form-data }

HTML forms (`<form></form>`) सामान्यतः data को server पर भेजने के लिए उस data के लिए एक "special" encoding का उपयोग करते हैं, यह JSON से अलग होता है।

**FastAPI** यह सुनिश्चित करेगा कि उस data को JSON के बजाय सही जगह से पढ़ा जाए।

/// note | तकनीकी विवरण

forms से data सामान्यतः "media type" `application/x-www-form-urlencoded` का उपयोग करके encoded होता है जब इसमें files शामिल नहीं होतीं।

लेकिन जब form में files शामिल होती हैं, तो यह `multipart/form-data` के रूप में encoded होता है। यदि आप `File` का उपयोग करते हैं, तो **FastAPI** जान जाएगा कि उसे body के सही भाग से files प्राप्त करनी हैं।

यदि आप इन encodings और form fields के बारे में अधिक पढ़ना चाहते हैं, तो [`POST` के लिए <abbr title="Mozilla Developer Network - मोज़िला डेवलपर नेटवर्क">MDN</abbr> web docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST) पर जाएं।

///

/// warning | चेतावनी

आप एक *path operation* में कई `File` और `Form` parameters घोषित कर सकते हैं, लेकिन आप ऐसे `Body` fields भी घोषित नहीं कर सकते जिन्हें आप JSON के रूप में प्राप्त करने की अपेक्षा करते हैं, क्योंकि request में body `application/json` के बजाय `multipart/form-data` का उपयोग करके encoded होगी।

यह **FastAPI** की limitation नहीं है, यह HTTP protocol का हिस्सा है।

///

## Optional File Upload { #optional-file-upload }

आप standard type annotations का उपयोग करके और default value `None` set करके file को optional बना सकते हैं:

{* ../../docs_src/request_files/tutorial001_02_an_py310.py hl[9,17] *}

## अतिरिक्त Metadata के साथ `UploadFile` { #uploadfile-with-additional-metadata }

आप `UploadFile` के साथ `File()` का भी उपयोग कर सकते हैं, उदाहरण के लिए, अतिरिक्त metadata set करने के लिए:

{* ../../docs_src/request_files/tutorial001_03_an_py310.py hl[9,15] *}

## Multiple File Uploads { #multiple-file-uploads }

एक ही समय में कई files अपलोड करना संभव है।

वे "form data" का उपयोग करके भेजे गए उसी "form field" से संबंधित होंगी।

इसका उपयोग करने के लिए, `bytes` या `UploadFile` की list घोषित करें:

{* ../../docs_src/request_files/tutorial002_an_py310.py hl[10,15] *}

आपको, जैसा घोषित किया गया है, `bytes` या `UploadFile`s की एक `list` प्राप्त होगी।

/// note | तकनीकी विवरण

आप `from starlette.responses import HTMLResponse` का भी उपयोग कर सकते हैं।

**FastAPI** आपकी सुविधा के लिए, developer के रूप में, वही `starlette.responses` को `fastapi.responses` के रूप में प्रदान करता है। लेकिन उपलब्ध अधिकांश responses सीधे Starlette से आते हैं।

///

### अतिरिक्त Metadata के साथ Multiple File Uploads { #multiple-file-uploads-with-additional-metadata }

और पहले की तरह ही, आप अतिरिक्त parameters set करने के लिए `File()` का उपयोग कर सकते हैं, यहां तक कि `UploadFile` के लिए भी:

{* ../../docs_src/request_files/tutorial003_an_py310.py hl[11,18:20] *}

## Recap { #recap }

request में अपलोड की जाने वाली files घोषित करने के लिए `File`, `bytes`, और `UploadFile` का उपयोग करें, जिन्हें form data के रूप में भेजा जाता है।
