# Errors handle করা { #handling-errors }

অনেক অবস্থায় আপনার API ব্যবহার করা client-কে একটি error জানাতে হয়।

এই client হতে পারে frontend-সহ একটি browser, অন্য কারো লেখা code, একটি IoT device, ইত্যাদি।

হয়তো client-কে জানাতে হবে যে:

* ওই operation-এর জন্য client-এর যথেষ্ট privileges নেই।
* ওই resource-এ client-এর access নেই।
* client যে item access করার চেষ্টা করছিল, সেটা নেই।
* ইত্যাদি।

এসব ক্ষেত্রে সাধারণত **400**-এর range-এর (400 থেকে 499) একটি **HTTP status code** return করা হয়।

এটা 200-এর HTTP status codes-এর (200 থেকে 299) মতোই। ওই "200" status codes মানে request-এ কোনো না কোনোভাবে "success" হয়েছে।

400-এর range-এর status codes মানে client-এর দিক থেকে error হয়েছে।

ওই সব **"404 Not Found"** errors (আর jokes) মনে আছে?

## `HTTPException` ব্যবহার করুন { #use-httpexception }

client-কে errors সহ HTTP responses return করতে `HTTPException` ব্যবহার করা হয়।

### `HTTPException` import করুন { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[1] *}

### আপনার code-এ একটি `HTTPException` raise করুন { #raise-an-httpexception-in-your-code }

`HTTPException` হলো APIs-এর জন্য দরকারি বাড়তি data-সহ একটি সাধারণ Python exception।

যেহেতু এটা একটি Python exception, তাই এটা `return` করা হয় না, `raise` করা হয়।

এর মানে এটাও যে, আপনি যদি এমন একটি utility function-এর ভেতরে থাকেন যেটা আপনার *path operation function*-এর ভেতর থেকে call করা হচ্ছে, আর ওই utility function-এর ভেতর থেকে `HTTPException` raise করেন, তাহলে *path operation function*-এর বাকি code আর চলবে না, request-টা সাথে সাথেই শেষ হয়ে যাবে আর `HTTPException`-এর HTTP error client-এ পাঠানো হবে।

value return করার বদলে exception raise করার সুবিধা Dependencies আর Security-এর section-এ আরও পরিষ্কার হবে।

এই উদাহরণে, client যখন এমন একটি ID দিয়ে item request করে যেটা নেই, তখন status code `404` দিয়ে একটি exception raise করা হয়:

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[11] *}

### যে response পাওয়া যায় { #the-resulting-response }

client যদি `http://example.com/items/foo` request করে (`item_id` `"foo"`), তাহলে client পাবে HTTP status code 200, আর এই JSON response:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

কিন্তু client যদি `http://example.com/items/bar` request করে (না-থাকা `item_id` `"bar"`), তাহলে client পাবে HTTP status code 404 ("not found" error), আর এই JSON response:

```JSON
{
  "detail": "Item not found"
}
```

/// tip | Tip

`HTTPException` raise করার সময় `detail` parameter হিসেবে JSON-এ convert করা যায় এমন যেকোনো value দিতে পারেন, শুধু `str` নয়।

একটি `dict`, একটি `list`, ইত্যাদি দিতে পারেন।

**FastAPI** এগুলো নিজে থেকেই handle করে আর JSON-এ convert করে।

///

## Custom headers যোগ করুন { #add-custom-headers }

কিছু অবস্থায় HTTP error-এ custom headers যোগ করতে পারাটা কাজে লাগে। যেমন কিছু ধরনের security-র জন্য।

সম্ভবত আপনার code-এ সরাসরি এটা ব্যবহার করার দরকার হবে না।

কিন্তু কোনো advanced অবস্থায় দরকার হলে custom headers যোগ করতে পারেন:

{* ../../docs_src/handling_errors/tutorial002_py310.py hl[14] *}

## Custom exception handlers install করুন { #install-custom-exception-handlers }

[Starlette-এর একই exception utilities](https://starlette.dev/exceptions/) দিয়ে custom exception handlers যোগ করতে পারেন।

ধরুন আপনার একটি custom exception `UnicornException` আছে, যেটা আপনি (বা আপনার ব্যবহার করা কোনো library) `raise` করতে পারে।

আর আপনি FastAPI দিয়ে এই exception-টা globally handle করতে চান।

`@app.exception_handler()` দিয়ে একটি custom exception handler যোগ করতে পারেন:

{* ../../docs_src/handling_errors/tutorial003_py310.py hl[5:7,13:18,24] *}

এখানে `/unicorns/yolo` request করলে *path operation* একটি `UnicornException` `raise` করবে।

কিন্তু এটা handle করবে `unicorn_exception_handler`।

তাই আপনি পাবেন একটি পরিষ্কার error, HTTP status code `418` আর এই JSON content সহ:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | Technical Details

`from starlette.requests import Request` আর `from starlette.responses import JSONResponse`-ও ব্যবহার করতে পারেন।

**FastAPI** একই `starlette.responses`-কে `fastapi.responses` হিসেবে দেয়, শুধু আপনার, মানে developer-এর সুবিধার জন্য। কিন্তু available responses-এর বেশিরভাগই সরাসরি Starlette থেকে আসে। `Request`-এর ক্ষেত্রেও একই।

///

## Default exception handlers override করুন { #override-the-default-exception-handlers }

**FastAPI**-এর কিছু default exception handlers আছে।

আপনি যখন একটি `HTTPException` `raise` করেন, আর যখন request-এ invalid data থাকে, তখন default JSON responses return করার দায়িত্ব এই handlers-এর।

এই exception handlers আপনার নিজের handlers দিয়ে override করতে পারেন।

### Request validation exceptions override করুন { #override-request-validation-exceptions }

কোনো request-এ invalid data থাকলে **FastAPI** ভেতরে ভেতরে একটি `RequestValidationError` raise করে।

আর এর জন্য একটি default exception handler-ও রাখে।

এটা override করতে `RequestValidationError` import করুন, আর `@app.exception_handler(RequestValidationError)` দিয়ে exception handler-টা decorate করুন।

exception handler একটি `Request` আর exception-টা পাবে।

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[2,14:19] *}

এবার `/items/foo`-এ গেলে, default JSON error-এর বদলে:

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

একটি text version পাবেন:

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### `HTTPException` error handler override করুন { #override-the-httpexception-error-handler }

একইভাবে `HTTPException` handler-ও override করতে পারেন।

যেমন, এই errors-এর জন্য হয়তো JSON-এর বদলে plain text response return করতে চাইবেন:

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[3:4,9:11,25] *}

/// note | Technical Details

`from starlette.responses import PlainTextResponse`-ও ব্যবহার করতে পারেন।

**FastAPI** একই `starlette.responses`-কে `fastapi.responses` হিসেবে দেয়, শুধু আপনার, মানে developer-এর সুবিধার জন্য। কিন্তু available responses-এর বেশিরভাগই সরাসরি Starlette থেকে আসে।

///

/// warning | Warning

মনে রাখবেন, `RequestValidationError`-এ কোন file name আর line-এ validation error হয়েছে, সেই তথ্য থাকে, যাতে চাইলে আপনার logs-এ প্রাসঙ্গিক তথ্য সহ দেখাতে পারেন।

কিন্তু এর মানে, শুধু এটাকে string-এ convert করে সরাসরি return করলে আপনার system সম্পর্কে কিছুটা তথ্য বাইরে চলে যেতে পারে, সেজন্যই এখানে code প্রতিটা error আলাদা করে বের করে দেখায়।

///

### `RequestValidationError` body ব্যবহার করুন { #use-the-requestvalidationerror-body }

`RequestValidationError`-এ invalid data-সহ যে `body` পাওয়া গেছে, সেটা থাকে।

app develop করার সময় body log করে debug করতে, user-কে return করতে, ইত্যাদি কাজে এটা ব্যবহার করতে পারেন।

{* ../../docs_src/handling_errors/tutorial005_py310.py hl[14] *}

এবার এরকম একটি invalid item পাঠিয়ে দেখুন:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

আপনি একটি response পাবেন, যেটা বলবে data invalid, আর তাতে পাওয়া body-টাও থাকবে:

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

#### FastAPI-এর `HTTPException` বনাম Starlette-এর `HTTPException` { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI**-এর নিজস্ব `HTTPException` আছে।

আর **FastAPI**-এর `HTTPException` error class, Starlette-এর `HTTPException` error class থেকে inherit করে।

একমাত্র পার্থক্য হলো, **FastAPI**-এর `HTTPException` `detail` field-এর জন্য JSON-এ convert করা যায় এমন যেকোনো data নেয়, আর Starlette-এর `HTTPException` এর জন্য শুধু strings নেয়।

তাই আপনার code-এ স্বাভাবিকভাবেই **FastAPI**-এর `HTTPException` raise করতে থাকুন।

কিন্তু exception handler register করার সময় সেটা Starlette-এর `HTTPException`-এর জন্য register করা উচিত।

এভাবে, Starlette-এর internal code-এর কোনো অংশ, বা কোনো Starlette extension বা plug-in যদি Starlette-এর `HTTPException` raise করে, আপনার handler সেটা ধরে handle করতে পারবে।

এই উদাহরণে, একই code-এ দুটো `HTTPException` রাখার জন্য Starlette-এর exception-এর নাম বদলে `StarletteHTTPException` রাখা হয়েছে:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### **FastAPI**-এর exception handlers আবার ব্যবহার করুন { #reuse-fastapis-exception-handlers }

**FastAPI**-এর একই default exception handlers-এর সাথে exception-টা ব্যবহার করতে চাইলে `fastapi.exception_handlers` থেকে default exception handlers import করে আবার ব্যবহার করতে পারেন:

{* ../../docs_src/handling_errors/tutorial006_py310.py hl[2:5,15,21] *}

এই উদাহরণে শুধু খুব বর্ণনামূলক একটি message দিয়ে error print করা হচ্ছে, কিন্তু idea-টা নিশ্চয়ই বুঝেছেন। exception-টা ব্যবহার করে তারপর default exception handlers আবার ব্যবহার করতে পারেন।
