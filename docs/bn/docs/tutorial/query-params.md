# Query Parameters { #query-parameters }

path parameters-এর অংশ নয় এমন অন্য function parameters declare করলে, সেগুলো নিজে থেকেই "query" parameters হিসেবে ধরা হয়।

{* ../../docs_src/query_params/tutorial001_py310.py hl[9] *}

query হলো URL-এ `?`-এর পরে আসা key-value pairs-এর সেট, যেগুলো `&` দিয়ে আলাদা করা থাকে।

যেমন এই URL-এ:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...query parameters হলো:

* `skip`: value `0`
* `limit`: value `10`

যেহেতু এগুলো URL-এর অংশ, তাই "স্বাভাবিকভাবেই" এগুলো strings।

কিন্তু Python types দিয়ে declare করলে (উপরের উদাহরণে `int` হিসেবে), এগুলো ওই type-এ convert হয় আর সেই অনুযায়ী validate হয়।

path parameters-এর ক্ষেত্রে যা যা হয়, query parameters-এর ক্ষেত্রেও ঠিক তাই হয়:

* Editor support (অবশ্যই)
* Data <dfn title="HTTP request থেকে আসা string-কে Python data-তে convert করা">"parsing"</dfn>
* Data validation
* Automatic documentation

## Defaults { #defaults }

যেহেতু query parameters path-এর fixed অংশ নয়, তাই এগুলো optional হতে পারে আর এদের default values থাকতে পারে।

উপরের উদাহরণে এদের default values হলো `skip=0` আর `limit=10`।

তাই এই URL-এ যাওয়া:

```
http://127.0.0.1:8000/items/
```

আর এখানে যাওয়া একই কথা:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

কিন্তু যদি যান, ধরুন:

```
http://127.0.0.1:8000/items/?skip=20
```

তাহলে আপনার function-এ parameter values হবে:

* `skip=20`: কারণ আপনি URL-এ এটা set করেছেন
* `limit=10`: কারণ এটাই ছিল default value

## Optional parameters { #optional-parameters }

একইভাবে, default `None` set করে optional query parameters declare করতে পারেন:

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

এখানে function parameter `q` optional হবে, আর default-ভাবে `None` থাকবে।

/// tip | Tip

আরও খেয়াল করুন, **FastAPI** বেশ smart, এটা ঠিকই বুঝে নেয় যে `item_id` একটি path parameter আর `q` তা নয়, তাই সেটা একটি query parameter।

///

## Query parameter type conversion { #query-parameter-type-conversion }

`bool` types-ও declare করতে পারেন, সেগুলোও convert হবে:

{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

এখানে, যদি যান:

```
http://127.0.0.1:8000/items/foo?short=1
```

অথবা

```
http://127.0.0.1:8000/items/foo?short=True
```

অথবা

```
http://127.0.0.1:8000/items/foo?short=true
```

অথবা

```
http://127.0.0.1:8000/items/foo?short=on
```

অথবা

```
http://127.0.0.1:8000/items/foo?short=yes
```

অথবা যেকোনো case variation (uppercase, প্রথম অক্ষর uppercase, ইত্যাদি), আপনার function parameter `short`-কে `bool` value `True` হিসেবে পাবে।

`0`, `false`, `off`, আর `no`-এর মতো values (case variations সহ) `False`-এ convert হয়।

`short` না দিলে **FastAPI** এর default value ব্যবহার করে, যেটা এই উদাহরণে `False`।

খালি value (`?short=`) বা অচেনা value (যেমন `?short=maybe`) দিলে `422` validation error আসে।


## একসাথে অনেকগুলো path আর query parameters { #multiple-path-and-query-parameters }

একই সময়ে একাধিক path parameters আর query parameters declare করতে পারেন, **FastAPI** জানে কোনটা কী।

আর এগুলো কোনো নির্দিষ্ট ক্রমে declare করারও দরকার নেই।

নাম দেখে এগুলো চেনা হবে:

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## Required query parameters { #required-query-parameters }

path নয় এমন parameters-এর জন্য (আপাতত আমরা শুধু query parameters দেখেছি) default value declare করলে সেটা required থাকে না।

নির্দিষ্ট কোনো value না দিয়ে শুধু optional করতে চাইলে default হিসেবে `None` set করুন।

কিন্তু কোনো query parameter required করতে চাইলে কোনো default value declare না করলেই হলো:

{* ../../docs_src/query_params/tutorial005_py310.py hl[6:7] *}

এখানে query parameter `needy` হলো `str` type-এর একটি required query parameter।

browser-এ এরকম একটি URL খুললে:

```
http://127.0.0.1:8000/items/foo-item
```

...required parameter `needy` না দিলে এরকম একটি error দেখবেন:

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

যেহেতু `needy` একটি required parameter, তাই এটা URL-এ set করতে হবে:

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

...এটা কাজ করবে:

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

আর অবশ্যই, কিছু parameters required, কিছু default value-সহ, আর কিছু পুরোপুরি optional হিসেবে define করতে পারেন:

{* ../../docs_src/query_params/tutorial006_py310.py hl[8] *}

এখানে 3টি query parameters আছে:

* `needy`, একটি required `str`।
* `skip`, default value `0`-সহ একটি `int`।
* `limit`, একটি optional `int`।

/// tip | Tip

[Path Parameters](path-params.md#predefined-values)-এর মতো একইভাবে `Enum`-ও ব্যবহার করতে পারেন।

///
