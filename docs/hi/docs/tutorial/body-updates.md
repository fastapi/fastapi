# Body - अपडेट्स { #body-updates }

## `PUT` के साथ बदलकर अपडेट करना { #update-replacing-with-put }

किसी item को अपडेट करने के लिए आप [HTTP `PUT`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT) operation का उपयोग कर सकते हैं।

आप input data को ऐसे data में बदलने के लिए `jsonable_encoder` का उपयोग कर सकते हैं जिसे JSON के रूप में संग्रहीत किया जा सके (जैसे NoSQL database के साथ)। उदाहरण के लिए, `datetime` को `str` में बदलना।

{* ../../docs_src/body_updates/tutorial001_py310.py hl[28:33] *}

`PUT` का उपयोग ऐसा data प्राप्त करने के लिए किया जाता है जो मौजूदा data को बदल दे।

### बदलने के बारे में चेतावनी { #warning-about-replacing }

इसका मतलब है कि अगर आप item `bar` को `PUT` का उपयोग करके ऐसे body के साथ अपडेट करना चाहते हैं जिसमें यह हो:

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

क्योंकि इसमें पहले से संग्रहीत attribute `"tax": 20.2` शामिल नहीं है, input model `"tax": 10.5` की default value लेगा।

और data उस "नए" `tax` `10.5` के साथ सहेजा जाएगा।

## `PATCH` के साथ आंशिक अपडेट्स { #partial-updates-with-patch }

आप data को *आंशिक रूप से* अपडेट करने के लिए [HTTP `PATCH`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH) operation का भी उपयोग कर सकते हैं।

इसका मतलब है कि आप केवल वही data भेज सकते हैं जिसे आप अपडेट करना चाहते हैं, बाकी को वैसा ही छोड़ते हुए।

/// note | नोट

`PATCH`, `PUT` की तुलना में कम सामान्य रूप से उपयोग और जाना जाता है।

और कई teams आंशिक अपडेट्स के लिए भी केवल `PUT` का उपयोग करती हैं।

आप इन्हें जैसे चाहें वैसे उपयोग करने के लिए **स्वतंत्र** हैं, **FastAPI** कोई प्रतिबंध नहीं लगाता।

लेकिन यह गाइड आपको मोटे तौर पर दिखाती है कि इन्हें कैसे उपयोग करने का इरादा है।

///

### Pydantic के `exclude_unset` parameter का उपयोग करना { #using-pydantics-exclude-unset-parameter }

अगर आप आंशिक अपडेट्स प्राप्त करना चाहते हैं, तो Pydantic के model के `.model_dump()` में parameter `exclude_unset` का उपयोग करना बहुत उपयोगी है।

जैसे `item.model_dump(exclude_unset=True)`।

इससे केवल उस data के साथ एक `dict` बनेगा जो `item` model बनाते समय सेट किया गया था, default values को छोड़कर।

फिर आप इसका उपयोग केवल उस data के साथ एक `dict` बनाने के लिए कर सकते हैं जो सेट किया गया था (request में भेजा गया), default values को छोड़ते हुए:

{* ../../docs_src/body_updates/tutorial002_py310.py hl[32] *}

### Pydantic के `update` parameter का उपयोग करना { #using-pydantics-update-parameter }

अब, आप `.model_copy()` का उपयोग करके मौजूदा model की एक copy बना सकते हैं, और अपडेट करने के लिए data वाले `dict` के साथ `update` parameter पास कर सकते हैं।

जैसे `stored_item_model.model_copy(update=update_data)`:

{* ../../docs_src/body_updates/tutorial002_py310.py hl[33] *}

### आंशिक अपडेट्स Recap { #partial-updates-recap }

संक्षेप में, आंशिक अपडेट्स लागू करने के लिए आप:

* (वैकल्पिक रूप से) `PUT` के बजाय `PATCH` का उपयोग करें।
* संग्रहीत data प्राप्त करें।
* उस data को Pydantic model में रखें।
* input model से default values के बिना एक `dict` बनाएँ (`exclude_unset` का उपयोग करके)।
    * इस तरह आप केवल उन values को अपडेट कर सकते हैं जिन्हें वास्तव में user ने सेट किया है, बजाय इसके कि आपके model में पहले से संग्रहीत values को default values से override कर दें।
* संग्रहीत model की एक copy बनाएँ, और प्राप्त आंशिक अपडेट्स के साथ उसके attributes को अपडेट करें (`update` parameter का उपयोग करके)।
* copied model को ऐसी चीज़ में बदलें जिसे आपकी DB में संग्रहीत किया जा सके (उदाहरण के लिए, `jsonable_encoder` का उपयोग करके)।
    * यह model की `.model_dump()` method को फिर से उपयोग करने जैसा है, लेकिन यह सुनिश्चित करता है (और बदलता है) कि values ऐसे data types में हों जिन्हें JSON में बदला जा सके, उदाहरण के लिए, `datetime` को `str` में।
* data को अपनी DB में सहेजें।
* अपडेट किया गया model लौटाएँ।

{* ../../docs_src/body_updates/tutorial002_py310.py hl[28:35] *}

/// tip | टिप

आप वास्तव में इसी तकनीक का उपयोग HTTP `PUT` operation के साथ भी कर सकते हैं।

लेकिन यहाँ का उदाहरण `PATCH` का उपयोग करता है क्योंकि इसे इन्हीं use cases के लिए बनाया गया था।

///

/// note | नोट

ध्यान दें कि input model अभी भी validate किया जाता है।

इसलिए, अगर आप ऐसे आंशिक अपडेट्स प्राप्त करना चाहते हैं जो सभी attributes को छोड़ सकते हैं, तो आपको ऐसा model चाहिए जिसमें सभी attributes optional के रूप में चिह्नित हों (default values या `None` के साथ)।

**अपडेट्स** के लिए सभी optional values वाले models और **creation** के लिए required values वाले models में अंतर करने के लिए, आप [Extra Models](extra-models.md) में बताए गए विचारों का उपयोग कर सकते हैं।

///
