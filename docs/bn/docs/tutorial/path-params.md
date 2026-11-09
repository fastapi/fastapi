# Path Parameters { #path-parameters }

Python format strings-এ যে syntax ব্যবহার করা হয়, ঠিক সেই syntax দিয়েই path "parameters" বা "variables" declare করতে পারেন:

{* ../../docs_src/path_params/tutorial001_py310.py hl[6:7] *}

path parameter `item_id`-এর value আপনার function-এ `item_id` argument হিসেবে পাঠানো হবে।

তাই এই উদাহরণ চালিয়ে [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo)-এ গেলে এই response দেখবেন:

```JSON
{"item_id":"foo"}
```

## Types সহ path parameters { #path-parameters-with-types }

standard Python type annotations ব্যবহার করে function-এর ভেতরেই path parameter-এর type declare করতে পারেন:

{* ../../docs_src/path_params/tutorial002_py310.py hl[7] *}

এখানে `item_id`-কে একটি `int` হিসেবে declare করা হয়েছে।

/// tip | Tip

এতে আপনার function-এর ভেতরে editor support পাবেন: error checks, completion, ইত্যাদি।

///

## Data <dfn title="এগুলো নামেও পরিচিত: serialization, parsing, marshalling">conversion</dfn> { #data-conversion }

এই উদাহরণ চালিয়ে browser-এ [http://127.0.0.1:8000/items/3](http://127.0.0.1:8000/items/3) খুললে এই response দেখবেন:

```JSON
{"item_id":3}
```

/// tip | Tip

খেয়াল করুন, আপনার function যে value পেয়েছে (এবং return করেছে) সেটা `3`, একটি Python `int` হিসেবে, string `"3"` নয়।

তাই ওই type declaration দিয়েই **FastAPI** আপনাকে automatic request <dfn title="HTTP request থেকে আসা string-কে Python data-তে convert করা">"parsing"</dfn> দেয়।

///

## Data validation { #data-validation }

কিন্তু browser-এ [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo)-এ গেলে সুন্দর একটি HTTP error দেখবেন:

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

কারণ path parameter `item_id`-এর value ছিল `"foo"`, যেটা একটি `int` নয়।

`int`-এর বদলে একটি `float` দিলেও একই error আসবে, যেমন: [http://127.0.0.1:8000/items/4.2](http://127.0.0.1:8000/items/4.2)

/// tip | Tip

তাই একই Python type declaration দিয়েই **FastAPI** আপনাকে data validation দেয়।

খেয়াল করুন, error-টা ঠিক কোন জায়গায় validation pass করেনি, সেটাও পরিষ্কার করে বলে দেয়।

আপনার API-এর সাথে কাজ করা code develop আর debug করার সময় এটা দারুণ কাজে লাগে।

///

## Documentation { #documentation }

আর browser-এ [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) খুললে এরকম একটি automatic, interactive API documentation দেখবেন:

<img src="/img/tutorial/path-params/image01.png">

/// tip | Tip

আবারও, শুধু ওই একই Python type declaration দিয়েই **FastAPI** আপনাকে automatic, interactive documentation দেয় (Swagger UI integrate করে)।

খেয়াল করুন, path parameter-টা একটি integer হিসেবে declare করা আছে।

///

## Standards-ভিত্তিক সুবিধা, বিকল্প documentation { #standards-based-benefits-alternative-documentation }

যেহেতু generate হওয়া schema-টা [OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md) standard থেকে আসে, তাই অনেক compatible tools আছে।

এই কারণেই **FastAPI** নিজেই একটি বিকল্প API documentation দেয় (ReDoc দিয়ে), যেটা পাবেন [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)-এ:

<img src="/img/tutorial/path-params/image02.png">

একইভাবে আরও অনেক compatible tools আছে, অনেক language-এর জন্য code generation tools সহ।

## Pydantic { #pydantic }

সব data validation ভেতরে ভেতরে [Pydantic](https://pydantic.dev/docs/) করে, তাই এর সব সুবিধা আপনি পাবেন। আর জানবেন, আপনি নিরাপদ হাতে আছেন।

`str`, `float`, `bool` আর আরও অনেক জটিল data types দিয়েও একই type declarations ব্যবহার করতে পারেন।

এগুলোর কয়েকটা tutorial-এর পরের chapters-এ দেখানো হয়েছে।

## Order গুরুত্বপূর্ণ { #order-matters }

*path operations* বানানোর সময় এমন অবস্থা আসতে পারে যেখানে একটি fixed path থাকে।

যেমন `/users/me`, ধরা যাক এটা বর্তমান user-এর data পাওয়ার জন্য।

আবার কোনো নির্দিষ্ট user-এর data user ID দিয়ে পাওয়ার জন্য `/users/{user_id}` path-ও থাকতে পারে।

যেহেতু *path operations* ক্রম অনুযায়ী evaluate হয়, তাই নিশ্চিত করতে হবে যে `/users/me`-এর path `/users/{user_id}`-এর আগে declare করা আছে:

{* ../../docs_src/path_params/tutorial003_py310.py hl[6,11] *}

না হলে `/users/{user_id}`-এর path `/users/me`-এর সাথেও match করে যাবে, "ভাববে" এটা `"me"` value-সহ একটি `user_id` parameter পাচ্ছে।

একইভাবে, একটি path operation দ্বিতীয়বার define করা যায় না:

{* ../../docs_src/path_params/tutorial003b_py310.py hl[6,11] *}

সবসময় প্রথমটাই ব্যবহার হবে, কারণ path আগে সেটার সাথেই match করে।

## আগে থেকে ঠিক করা values { #predefined-values }

আপনার যদি এমন একটি *path operation* থাকে যেটা একটি *path parameter* নেয়, কিন্তু আপনি চান সেই *path parameter*-এর সম্ভাব্য valid values আগে থেকেই ঠিক করা থাকুক, তাহলে একটি standard Python <abbr title="Enumeration">`Enum`</abbr> ব্যবহার করতে পারেন।

### একটি `Enum` class বানান { #create-an-enum-class }

`Enum` import করুন, আর `str` ও `Enum` থেকে inherit করে এমন একটি sub-class বানান।

`str` থেকে inherit করলে API docs বুঝতে পারবে যে values অবশ্যই `string` type-এর হবে, আর ঠিকভাবে render করতে পারবে।

তারপর fixed values দিয়ে class attributes বানান, এগুলোই হবে available valid values:

{* ../../docs_src/path_params/tutorial005_py310.py hl[1,6:9] *}

/// tip | Tip

ভাবছেন হয়তো, "AlexNet", "ResNet" আর "LeNet" শুধু Machine Learning <dfn title="আসলে বললে, Deep Learning model architectures">models</dfn>-এর নাম।

///

### একটি *path parameter* declare করুন { #declare-a-path-parameter }

তারপর আপনার বানানো enum class (`ModelName`) দিয়ে type annotation সহ একটি *path parameter* বানান:

{* ../../docs_src/path_params/tutorial005_py310.py hl[16] *}

### Docs দেখুন { #check-the-docs }

যেহেতু *path parameter*-এর available values আগে থেকে ঠিক করা, তাই interactive docs সেগুলো সুন্দরভাবে দেখাতে পারে:

<img src="/img/tutorial/path-params/image03.png">

### Python *enumerations* নিয়ে কাজ করা { #working-with-python-enumerations }

*path parameter*-এর value হবে একটি *enumeration member*।

#### *enumeration members* compare করুন { #compare-enumeration-members }

আপনার বানানো enum `ModelName`-এর *enumeration member*-এর সাথে এটা compare করতে পারেন:

{* ../../docs_src/path_params/tutorial005_py310.py hl[17] *}

#### *enumeration value* নিন { #get-the-enumeration-value }

আসল value (এখানে একটি `str`) পেতে পারেন `model_name.value` দিয়ে, বা সাধারণভাবে `your_enum_member.value` দিয়ে:

{* ../../docs_src/path_params/tutorial005_py310.py hl[20] *}

/// tip | Tip

`ModelName.lenet.value` দিয়েও value `"lenet"` পেতে পারেন।

///

#### *enumeration members* return করুন { #return-enumeration-members }

আপনার *path operation* থেকে *enum members* return করতে পারেন, এমনকি একটি JSON body-র ভেতরে nested অবস্থাতেও (যেমন একটি `dict`)।

client-এ return করার আগে এগুলো তাদের নিজ নিজ values-এ (এখানে strings) convert হয়ে যাবে:

{* ../../docs_src/path_params/tutorial005_py310.py hl[18,21,23] *}

আপনার client-এ এরকম একটি JSON response পাবেন:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Paths ধারণ করা path parameters { #path-parameters-containing-paths }

ধরুন আপনার একটি *path operation* আছে, যার path `/files/{file_path}`।

কিন্তু আপনার দরকার `file_path`-এর ভেতরেই একটি *path* থাকুক, যেমন `home/johndoe/myfile.txt`।

তাহলে ওই file-এর URL হবে এরকম: `/files/home/johndoe/myfile.txt`।

### OpenAPI support { #openapi-support }

OpenAPI-তে এমনভাবে *path parameter* declare করার উপায় নেই যার ভেতরে একটি *path* থাকবে, কারণ এতে এমন অবস্থা তৈরি হতে পারে যা test আর define করা কঠিন।

তবুও **FastAPI**-তে Starlette-এর একটি internal tool দিয়ে এটা করা যায়।

আর docs-ও কাজ করবে, যদিও parameter-টার ভেতরে যে একটি path থাকা উচিত, সেটা docs-এ লেখা থাকবে না।

### Path convertor { #path-convertor }

Starlette-এর একটি option সরাসরি ব্যবহার করে, এরকম একটি URL দিয়ে *path* ধারণ করা *path parameter* declare করতে পারেন:

```
/files/{file_path:path}
```

এখানে parameter-এর নাম `file_path`, আর শেষ অংশ `:path` বলে দেয় যে parameter-টা যেকোনো *path*-এর সাথে match করবে।

তাই এটা এভাবে ব্যবহার করতে পারেন:

{* ../../docs_src/path_params/tutorial004_py310.py hl[6] *}

/// tip | Tip

হয়তো আপনার দরকার parameter-টায় শুরুতে একটি slash (`/`) সহ `/home/johndoe/myfile.txt` থাকুক।

সেক্ষেত্রে URL হবে: `/files//home/johndoe/myfile.txt`, `files` আর `home`-এর মাঝে double slash (`//`) সহ।

///

## Recap { #recap }

**FastAPI**-তে ছোট, সহজে বোঝা যায় এমন standard Python type declarations ব্যবহার করে আপনি পাবেন:

* Editor support: error checks, autocompletion, ইত্যাদি।
* Data "<dfn title="HTTP request থেকে আসা string-কে Python data-তে convert করা">parsing</dfn>"
* Data validation
* API annotation আর automatic documentation

আর এগুলো আপনাকে শুধু একবারই declare করতে হবে।

বিকল্প frameworks-এর তুলনায় এটাই সম্ভবত **FastAPI**-এর সবচেয়ে চোখে পড়ার মতো সুবিধা (raw performance বাদ দিলে)।
