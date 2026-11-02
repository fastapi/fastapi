# Query Parameters { #query-parameters }

जब आप ऐसे दूसरे function parameters declare करते हैं जो path parameters का हिस्सा नहीं हैं, तो उन्हें अपने-आप "query" parameters के रूप में समझा जाता है।

{* ../../docs_src/query_params/tutorial001_py310.py hl[9] *}

query उन key-value pairs का सेट है जो URL में `?` के बाद आते हैं, और `&` characters से अलग किए जाते हैं।

उदाहरण के लिए, इस URL में:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...query parameters हैं:

* `skip`: `0` value के साथ
* `limit`: `10` value के साथ

क्योंकि वे URL का हिस्सा हैं, वे "स्वाभाविक रूप से" strings होते हैं।

लेकिन जब आप उन्हें Python types के साथ declare करते हैं (ऊपर दिए गए उदाहरण में, `int` के रूप में), तो उन्हें उस type में convert किया जाता है और उसके अनुसार validate किया जाता है।

path parameters पर लागू होने वाली सभी वही प्रक्रियाएँ query parameters पर भी लागू होती हैं:

* Editor support (स्पष्ट रूप से)
* Data <dfn title="HTTP request से आने वाली string को Python data में बदलना">"parsing"</dfn>
* Data validation
* Automatic documentation

## Defaults { #defaults }

क्योंकि query parameters किसी path का fixed हिस्सा नहीं होते, वे optional हो सकते हैं और उनके default values हो सकते हैं।

ऊपर दिए गए उदाहरण में उनके default values `skip=0` और `limit=10` हैं।

तो, इस URL पर जाना:

```
http://127.0.0.1:8000/items/
```

इस पर जाने जैसा ही होगा:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

लेकिन अगर आप, उदाहरण के लिए, इस पर जाते हैं:

```
http://127.0.0.1:8000/items/?skip=20
```

तो आपके function में parameter values होंगी:

* `skip=20`: क्योंकि आपने इसे URL में सेट किया है
* `limit=10`: क्योंकि वह default value था

## Optional parameters { #optional-parameters }

उसी तरह, आप optional query parameters declare कर सकते हैं, उनका default `None` सेट करके:

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

इस मामले में, function parameter `q` optional होगा, और default रूप से `None` होगा।

/// tip | सुझाव

यह भी ध्यान दें कि **FastAPI** इतना smart है कि यह पहचान लेता है कि path parameter `item_id` एक path parameter है और `q` नहीं है, इसलिए, यह एक query parameter है।

///

## Query parameter type conversion { #query-parameter-type-conversion }

आप `bool` types भी declare कर सकते हैं, और वे convert हो जाएँगे:

{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

इस मामले में, अगर आप इस पर जाते हैं:

```
http://127.0.0.1:8000/items/foo?short=1
```

या

```
http://127.0.0.1:8000/items/foo?short=True
```

या

```
http://127.0.0.1:8000/items/foo?short=true
```

या

```
http://127.0.0.1:8000/items/foo?short=on
```

या

```
http://127.0.0.1:8000/items/foo?short=yes
```

या कोई भी दूसरी case variation (uppercase, पहले अक्षर को uppercase, आदि), आपका function parameter `short` को `True` के `bool` value के साथ देखेगा। अन्यथा `False` के रूप में।


## कई path और query parameters { #multiple-path-and-query-parameters }

आप एक ही समय में कई path parameters और query parameters declare कर सकते हैं, **FastAPI** जानता है कि कौन सा कौन है।

और आपको उन्हें किसी विशेष order में declare करने की ज़रूरत नहीं है।

उन्हें नाम से detect किया जाएगा:

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## Required query parameters { #required-query-parameters }

जब आप non-path parameters के लिए default value declare करते हैं (अभी तक, हमने केवल query parameters देखे हैं), तो वह required नहीं होता।

अगर आप कोई specific value नहीं जोड़ना चाहते लेकिन बस उसे optional बनाना चाहते हैं, तो default को `None` के रूप में सेट करें।

लेकिन जब आप किसी query parameter को required बनाना चाहते हैं, तो आप बस कोई default value declare न करें:

{* ../../docs_src/query_params/tutorial005_py310.py hl[6:7] *}

यहाँ query parameter `needy` type `str` का एक required query parameter है।

अगर आप अपने browser में इस तरह का URL खोलते हैं:

```
http://127.0.0.1:8000/items/foo-item
```

...required parameter `needy` जोड़े बिना, तो आपको इस तरह की error दिखाई देगी:

```JSON
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "needy"
      ],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

क्योंकि `needy` एक required parameter है, आपको इसे URL में सेट करना होगा:

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

...यह काम करेगा:

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

और निश्चित रूप से, आप कुछ parameters को required, कुछ को default value वाला, और कुछ को पूरी तरह optional define कर सकते हैं:

{* ../../docs_src/query_params/tutorial006_py310.py hl[8] *}

इस मामले में, 3 query parameters हैं:

* `needy`, एक required `str`.
* `skip`, default value `0` के साथ एक `int`.
* `limit`, एक optional `int`.

/// tip | सुझाव

आप `Enum`s को भी उसी तरह use कर सकते हैं जैसे [Path Parameters](path-params.md#predefined-values) के साथ।

///
