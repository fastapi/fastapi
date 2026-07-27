# Response Status Code { #response-status-code }

जिस तरह आप response model specify कर सकते हैं, उसी तरह आप किसी भी *path operations* में parameter `status_code` के साथ response के लिए इस्तेमाल किया जाने वाला HTTP status code भी declare कर सकते हैं:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* आदि।

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

/// note | नोट

ध्यान दें कि `status_code`, "decorator" method (`get`, `post`, आदि) का parameter है। यह आपके *path operation function* का parameter नहीं है, जैसे बाकी सभी parameters और body होते हैं।

///

`status_code` parameter HTTP status code वाला एक number receive करता है।

/// note | नोट

`status_code` वैकल्पिक रूप से एक `IntEnum` भी receive कर सकता है, जैसे Python का [`http.HTTPStatus`](https://docs.python.org/3/library/http.html#http.HTTPStatus).

///

यह:

* response में वह status code return करेगा।
* उसे OpenAPI schema में उसी तरह document करेगा (और इसलिए, user interfaces में भी):

<img src="/img/tutorial/response-status-code/image01.png">

/// note | नोट

कुछ response codes (अगला section देखें) यह indicate करते हैं कि response में body नहीं होती।

FastAPI यह जानता है, और ऐसे OpenAPI docs बनाएगा जो बताते हैं कि कोई response body नहीं है।

///

## HTTP status codes के बारे में { #about-http-status-codes }

/// note | नोट

अगर आप पहले से जानते हैं कि HTTP status codes क्या होते हैं, तो अगले section पर जाएँ।

///

HTTP में, आप response के हिस्से के रूप में 3 digits का एक numeric status code भेजते हैं।

इन status codes के साथ एक associated name होता है जिससे उन्हें पहचानने में मदद मिलती है, लेकिन महत्वपूर्ण हिस्सा number होता है।

संक्षेप में:

* `100 - 199` "Information" के लिए होते हैं। आप इन्हें सीधे बहुत कम इस्तेमाल करते हैं। इन status codes वाले responses में body नहीं हो सकती।
* **`200 - 299`** "Successful" responses के लिए होते हैं। ये वे हैं जिन्हें आप सबसे ज़्यादा इस्तेमाल करेंगे।
    * `200` default status code है, जिसका मतलब है कि सब कुछ "OK" था।
    * एक और उदाहरण `201`, "Created" होगा। इसे आमतौर पर database में नया record बनाने के बाद इस्तेमाल किया जाता है।
    * एक विशेष case `204`, "No Content" है। यह response तब इस्तेमाल होता है जब client को return करने के लिए कोई content नहीं होता, और इसलिए response में body नहीं होनी चाहिए।
* **`300 - 399`** "Redirection" के लिए होते हैं। इन status codes वाले responses में body हो भी सकती है और नहीं भी, सिवाय `304`, "Not Modified" के, जिसमें body नहीं होनी चाहिए।
* **`400 - 499`** "Client error" responses के लिए होते हैं। ये दूसरा type है जिसे आप शायद सबसे ज़्यादा इस्तेमाल करेंगे।
    * एक उदाहरण `404` है, "Not Found" response के लिए।
    * client से आने वाली generic errors के लिए, आप सिर्फ़ `400` इस्तेमाल कर सकते हैं।
* `500 - 599` server errors के लिए होते हैं। आप इन्हें लगभग कभी सीधे इस्तेमाल नहीं करते। जब आपके application code या server के किसी हिस्से में कुछ गड़बड़ होती है, तो यह अपने-आप इन status codes में से एक return करेगा।

/// tip | सुझाव

हर status code के बारे में और कौन-सा code किसके लिए है, यह जानने के लिए [HTTP status codes के बारे में <abbr title="Mozilla Developer Network">MDN</abbr> documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) देखें।

///

## नाम याद रखने का shortcut { #shortcut-to-remember-the-names }

आइए पिछले example को फिर से देखें:

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

`201` "Created" के लिए status code है।

लेकिन आपको यह याद रखने की ज़रूरत नहीं है कि इनमें से हर code का क्या मतलब है।

आप `fastapi.status` से convenience variables इस्तेमाल कर सकते हैं।

{* ../../docs_src/response_status_code/tutorial002_py310.py hl[1,6] *}

वे सिर्फ़ एक सुविधा हैं, उनमें वही number होता है, लेकिन इस तरह आप उन्हें खोजने के लिए editor के autocomplete का इस्तेमाल कर सकते हैं:

<img src="/img/tutorial/response-status-code/image02.png">

/// note | तकनीकी विवरण

आप `from starlette import status` भी इस्तेमाल कर सकते हैं।

**FastAPI** आपकी सुविधा के लिए, developer के रूप में, वही `starlette.status` `fastapi.status` के रूप में provide करता है। लेकिन यह सीधे Starlette से आता है।

///

## default बदलना { #changing-the-default }

बाद में, [Advanced User Guide](../advanced/response-change-status-code.md) में, आप देखेंगे कि यहाँ declare किए जा रहे default से अलग status code कैसे return किया जाता है।
