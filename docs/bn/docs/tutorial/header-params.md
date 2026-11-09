# Header Parameters { #header-parameters }

`Query`, `Path` আর `Cookie` parameters যেভাবে define করেন, Header parameters-ও সেভাবেই define করতে পারেন।

## `Header` import করুন { #import-header }

প্রথমে `Header` import করুন:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[3] *}

## `Header` parameters declare করুন { #declare-header-parameters }

তারপর `Path`, `Query` আর `Cookie`-এর মতো একই গঠনে header parameters declare করুন।

default value আর সব বাড়তি validation বা annotation parameters define করতে পারেন:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[9] *}

/// note | Technical Details

`Header` হলো `Path`, `Query` আর `Cookie`-এর একটি "বোন" class। এটাও একই common `Param` class থেকে inherit করে।

কিন্তু মনে রাখবেন, `fastapi` থেকে `Query`, `Path`, `Header` আর অন্যগুলো import করলে, সেগুলো আসলে functions, যেগুলো special classes return করে।

///

/// note | Note

headers declare করতে `Header` ব্যবহার করতে হবে, না হলে parameters query parameters হিসেবে ধরা হবে।

///

## Automatic conversion { #automatic-conversion }

`Path`, `Query` আর `Cookie` যা দেয়, তার উপরে `Header`-এর একটু বাড়তি functionality আছে।

বেশিরভাগ standard headers একটি "hyphen" character দিয়ে আলাদা করা থাকে, যেটা "minus symbol" (`-`) নামেও পরিচিত।

কিন্তু `user-agent`-এর মতো একটি variable Python-এ invalid।

তাই default-ভাবে, headers বের করতে আর document করতে `Header` parameter names-এর characters underscore (`_`) থেকে hyphen (`-`)-এ convert করে।

তাছাড়া HTTP headers case-insensitive, তাই এগুলো standard Python style-এ (যেটা "snake_case" নামেও পরিচিত) declare করতে পারেন।

তাই `User_Agent` বা এরকম কিছু লিখে প্রথম অক্ষরগুলো capital করার দরকার নেই, Python code-এ সাধারণত যেভাবে লেখেন সেভাবেই `user_agent` ব্যবহার করতে পারেন।

কোনো কারণে underscores থেকে hyphens-এ automatic conversion বন্ধ করতে হলে, `Header`-এর `convert_underscores` parameter `False` set করুন:

{* ../../docs_src/header_params/tutorial002_an_py310.py hl[10] *}

/// warning | Warning

`convert_underscores` `False` set করার আগে মনে রাখবেন, কিছু HTTP proxies আর servers underscores-সহ headers ব্যবহার করতে দেয় না।

///

## Duplicate headers { #duplicate-headers }

duplicate headers পাওয়া সম্ভব। মানে, একই header-এর একাধিক values।

type declaration-এ একটি list ব্যবহার করে এসব ক্ষেত্র define করতে পারেন।

duplicate header-এর সব values একটি Python `list` হিসেবে পাবেন।

যেমন, একাধিকবার আসতে পারে এমন একটি `X-Token` header declare করতে লিখতে পারেন:

{* ../../docs_src/header_params/tutorial003_an_py310.py hl[9] *}

ওই *path operation*-এর সাথে যদি এরকম দুটো HTTP headers পাঠিয়ে যোগাযোগ করেন:

```
X-Token: foo
X-Token: bar
```

response হবে এরকম:

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## Recap { #recap }

`Query`, `Path` আর `Cookie`-এর মতো একই common pattern মেনে `Header` দিয়ে headers declare করুন।

আর আপনার variables-এর underscores নিয়ে চিন্তা করবেন না, **FastAPI** এগুলো convert করার দায়িত্ব নেবে।
