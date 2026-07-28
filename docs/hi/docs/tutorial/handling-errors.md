# Errors को हैंडल करना { #handling-errors }

ऐसी कई स्थितियाँ होती हैं जिनमें आपको अपनी API का उपयोग कर रहे client को error report करना पड़ता है।

यह client frontend वाला कोई browser, किसी और का code, कोई IoT device आदि हो सकता है।

आपको client को यह बताने की ज़रूरत पड़ सकती है कि:

* client के पास उस operation के लिए पर्याप्त privileges नहीं हैं।
* client के पास उस resource का access नहीं है।
* जिस item को client access करने की कोशिश कर रहा था, वह मौजूद नहीं है।
* आदि।

इन मामलों में, आप सामान्यतः **400** की range (400 से 499 तक) में एक **HTTP status code** return करेंगे।

यह 200 HTTP status codes (200 से 299 तक) जैसा ही है। वे "200" status codes का मतलब है कि request में किसी तरह "success" हुआ था।

400 range के status codes का मतलब है कि client की तरफ़ से कोई error था।

वे सभी **"404 Not Found"** errors (और jokes) याद हैं?

## `HTTPException` का उपयोग करें { #use-httpexception }

Client को errors वाली HTTP responses return करने के लिए आप `HTTPException` का उपयोग करते हैं।

### `HTTPException` import करें { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[1] *}

### अपने code में `HTTPException` raise करें { #raise-an-httpexception-in-your-code }

`HTTPException` APIs के लिए प्रासंगिक अतिरिक्त data के साथ एक सामान्य Python exception है।

क्योंकि यह एक Python exception है, आप इसे `return` नहीं करते, आप इसे `raise` करते हैं।

इसका यह भी मतलब है कि अगर आप किसी utility function के अंदर हैं जिसे आप अपनी *path operation function* के अंदर call कर रहे हैं, और आप उस utility function के अंदर से `HTTPException` raise करते हैं, तो यह *path operation function* में बाकी code नहीं चलाएगा, यह उस request को तुरंत समाप्त कर देगा और `HTTPException` से HTTP error client को भेज देगा।

किसी value को return करने के बजाय exception raise करने का लाभ Dependencies और Security वाले section में अधिक स्पष्ट होगा।

इस example में, जब client किसी ऐसे ID से item request करता है जो मौजूद नहीं है, तो `404` के status code के साथ exception raise करें:

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[11] *}

### परिणामी response { #the-resulting-response }

अगर client `http://example.com/items/foo` (एक `item_id` `"foo"`) request करता है, तो उस client को 200 का HTTP status code और यह JSON response मिलेगा:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

लेकिन अगर client `http://example.com/items/bar` (एक non-existent `item_id` `"bar"`) request करता है, तो उस client को 404 का HTTP status code ("not found" error) और यह JSON response मिलेगा:

```JSON
{
  "detail": "Item not found"
}
```

/// tip | सुझाव

`HTTPException` raise करते समय, आप `detail` parameter के रूप में ऐसी कोई भी value pass कर सकते हैं जिसे JSON में convert किया जा सकता हो, केवल `str` ही नहीं।

आप `dict`, `list` आदि pass कर सकते हैं।

इन्हें **FastAPI** अपने आप handle करता है और JSON में convert करता है।

///

## custom headers जोड़ें { #add-custom-headers }

कुछ स्थितियाँ ऐसी होती हैं जहाँ HTTP error में custom headers जोड़ पाना उपयोगी होता है। उदाहरण के लिए, कुछ प्रकार की security के लिए।

आपको शायद अपने code में सीधे इसका उपयोग करने की ज़रूरत नहीं होगी।

लेकिन अगर किसी advanced scenario में आपको इसकी ज़रूरत पड़े, तो आप custom headers जोड़ सकते हैं:

{* ../../docs_src/handling_errors/tutorial002_py310.py hl[14] *}

## custom exception handlers install करें { #install-custom-exception-handlers }

आप [Starlette से वही exception utilities](https://www.starlette.dev/exceptions/) के साथ custom exception handlers जोड़ सकते हैं।

मान लीजिए आपके पास एक custom exception `UnicornException` है जिसे आप (या कोई library जिसका आप उपयोग करते हैं) `raise` कर सकते हैं।

और आप इस exception को FastAPI के साथ globally handle करना चाहते हैं।

आप `@app.exception_handler()` के साथ custom exception handler जोड़ सकते हैं:

{* ../../docs_src/handling_errors/tutorial003_py310.py hl[5:7,13:18,24] *}

यहाँ, अगर आप `/unicorns/yolo` request करते हैं, तो *path operation* एक `UnicornException` `raise` करेगा।

लेकिन इसे `unicorn_exception_handler` द्वारा handle किया जाएगा।

इसलिए, आपको `418` के HTTP status code और इस JSON content के साथ एक साफ़ error मिलेगा:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | Technical Details

आप `from starlette.requests import Request` और `from starlette.responses import JSONResponse` का भी उपयोग कर सकते हैं।

**FastAPI** आपकी, developer की, सुविधा के लिए `starlette.responses` को `fastapi.responses` के रूप में उपलब्ध कराता है। लेकिन उपलब्ध अधिकांश responses सीधे Starlette से आते हैं। `Request` के साथ भी यही है।

///

## default exception handlers को override करें { #override-the-default-exception-handlers }

**FastAPI** में कुछ default exception handlers होते हैं।

ये handlers default JSON responses return करने के लिए ज़िम्मेदार होते हैं, जब आप `HTTPException` `raise` करते हैं और जब request में invalid data होता है।

आप इन exception handlers को अपने खुद के handlers से override कर सकते हैं।

### request validation exceptions को override करें { #override-request-validation-exceptions }

जब किसी request में invalid data होता है, तो **FastAPI** internally एक `RequestValidationError` raise करता है।

और इसमें इसके लिए एक default exception handler भी शामिल होता है।

इसे override करने के लिए, `RequestValidationError` import करें और exception handler को decorate करने के लिए इसे `@app.exception_handler(RequestValidationError)` के साथ उपयोग करें।

Exception handler को एक `Request` और exception मिलेगा।

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[2,14:19] *}

अब, अगर आप `/items/foo` पर जाते हैं, तो default JSON error पाने के बजाय:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

आपको text version मिलेगा, जिसमें होगा:

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### `HTTPException` error handler को override करें { #override-the-httpexception-error-handler }

उसी तरह, आप `HTTPException` handler को override कर सकते हैं।

उदाहरण के लिए, आप इन errors के लिए JSON के बजाय plain text response return करना चाह सकते हैं:

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[3:4,9:11,25] *}

/// note | Technical Details

आप `from starlette.responses import PlainTextResponse` का भी उपयोग कर सकते हैं।

**FastAPI** आपकी, developer की, सुविधा के लिए `starlette.responses` को `fastapi.responses` के रूप में उपलब्ध कराता है। लेकिन उपलब्ध अधिकांश responses सीधे Starlette से आते हैं।

///

/// warning | चेतावनी

ध्यान रखें कि `RequestValidationError` में file name और उस line की जानकारी होती है जहाँ validation error होता है, ताकि अगर आप चाहें तो relevant जानकारी के साथ उसे अपने logs में दिखा सकें।

लेकिन इसका मतलब है कि अगर आप इसे केवल string में convert करके वह जानकारी सीधे return कर देते हैं, तो आप अपने system के बारे में थोड़ी जानकारी leak कर सकते हैं, इसलिए यहाँ code हर error को अलग-अलग extract करके दिखाता है।

///

### `RequestValidationError` body का उपयोग करें { #use-the-requestvalidationerror-body }

`RequestValidationError` में वह `body` होता है जो इसे invalid data के साथ मिला था।

आप अपनी app develop करते समय body को log और debug करने, user को return करने आदि के लिए इसका उपयोग कर सकते हैं।

{* ../../docs_src/handling_errors/tutorial005_py310.py hl[14] *}

अब ऐसा invalid item भेजकर देखें:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

आपको एक response मिलेगा जो बताता है कि data invalid है और जिसमें received body शामिल होगा:

```JSON hl_lines="12-15"
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
```

#### FastAPI का `HTTPException` बनाम Starlette का `HTTPException` { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI** का अपना `HTTPException` है।

और **FastAPI** की `HTTPException` error class, Starlette की `HTTPException` error class से inherit करती है।

केवल अंतर यह है कि **FastAPI** का `HTTPException`, `detail` field के लिए कोई भी JSON-able data accept करता है, जबकि Starlette का `HTTPException` इसके लिए केवल strings accept करता है।

इसलिए, आप अपने code में सामान्य रूप से **FastAPI** का `HTTPException` raise करते रह सकते हैं।

लेकिन जब आप exception handler register करते हैं, तो आपको उसे Starlette के `HTTPException` के लिए register करना चाहिए।

इस तरह, अगर Starlette के internal code का कोई हिस्सा, या कोई Starlette extension या plug-in, Starlette `HTTPException` raise करता है, तो आपका handler उसे catch और handle कर पाएगा।

इस example में, एक ही code में दोनों `HTTPException`s रखने के लिए, Starlette के exceptions को `StarletteHTTPException` नाम दिया गया है:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### **FastAPI** के exception handlers का फिर से उपयोग करें { #reuse-fastapis-exception-handlers }

अगर आप **FastAPI** के उन्हीं default exception handlers के साथ exception का उपयोग करना चाहते हैं, तो आप `fastapi.exception_handlers` से default exception handlers import करके उनका फिर से उपयोग कर सकते हैं:

{* ../../docs_src/handling_errors/tutorial006_py310.py hl[2:5,15,21] *}

इस example में आप केवल error को बहुत expressive message के साथ print कर रहे हैं, लेकिन आप बात समझ गए। आप exception का उपयोग कर सकते हैं और फिर बस default exception handlers का फिर से उपयोग कर सकते हैं।
