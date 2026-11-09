# Query Parameter Models { #query-parameter-models }

আপনার যদি পরস্পর সম্পর্কিত একগুচ্ছ **query parameters** থাকে, তাহলে সেগুলো declare করতে একটি **Pydantic model** বানাতে পারেন।

এতে **model-টা আবার ব্যবহার** করতে পারবেন **অনেক জায়গায়**, আর সব parameters-এর জন্য একসাথে validations আর metadata-ও declare করতে পারবেন। 😎

/// note | Note

FastAPI version `0.115.0` থেকে এটা supported। 🤓

///

## Pydantic Model দিয়ে Query Parameters { #query-parameters-with-a-pydantic-model }

আপনার দরকারি **query parameters** একটি **Pydantic model**-এ declare করুন, তারপর parameter-টা `Query` হিসেবে declare করুন:

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** request-এর **query parameters** থেকে **প্রতিটি field**-এর data **বের করে** আপনার define করা Pydantic model-টা আপনাকে দেবে।

## Docs দেখুন { #check-the-docs }

`/docs`-এ docs UI-তে query parameters দেখতে পাবেন:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## বাড়তি Query Parameters নিষেধ করুন { #forbid-extra-query-parameters }

কিছু বিশেষ ক্ষেত্রে (সম্ভবত খুব একটা প্রচলিত না) আপনি হয়তো যে query parameters নিতে চান, সেগুলো **সীমিত** করতে চাইবেন।

যেকোনো `extra` fields `forbid` করতে Pydantic-এর model configuration ব্যবহার করতে পারেন:

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

কোনো client **query parameters**-এ কিছু **বাড়তি** data পাঠানোর চেষ্টা করলে, সে একটি **error** response পাবে।

যেমন, client যদি `plumbus` value-সহ একটি `tool` query parameter পাঠানোর চেষ্টা করে, এভাবে:

```http
https://example.com/items/?limit=10&tool=plumbus
```

সে একটি **error** response পাবে, যেটা বলবে query parameter `tool` allowed নয়:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## Parameter Models একসাথে ব্যবহার করুন { #combine-parameter-models }

একাধিক query parameter models declare করতে পারেন, আর আলাদা আলাদা query parameters বা dependencies-এর সাথে সেগুলো মিলিয়ে ব্যবহার করতে পারেন।

{* ../../docs_src/query_param_models/tutorial003_an_py310.py hl[9:15,20:22] *}

request parameters একই level-এ থাকে।

```http
https://example.com/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt
```

query string-এ কোনো `pagination` বা `filters` keys নেই। প্রতিটি model query parameters আলাদাভাবে validate করে, নিজের defaults, field validators আর model validators দিয়ে। models বা আলাদা parameters dependencies-এ declare করা থাকলেও একই কথা খাটে।

models যদি একই parameter name বা alias share করে, তাহলে প্রতিটি model ওই request parameter আলাদাভাবে validate করে। আলাদা values-এর জন্য আলাদা names বা aliases ব্যবহার করুন। dependencies-এর সাথে share করা parameters-এর মতোই OpenAPI একটি shared parameter একবারই দেখায়, তাই shared declarations-এ একই type আর constraints থাকা উচিত।

প্রতিটি model-এর `extra` configuration সব query parameters-এর উপর খাটে, অন্য models বা dependencies-এ declare করাগুলো সহ। `extra="forbid"` থাকলে ওই model-এর বাইরের যেকোনো parameter reject হয়। `extra="allow"` থাকলে ওই parameters model extras হিসেবে যোগ হয়।

এটা `Header` আর `Cookie` models-এর জন্যও কাজ করে।

## Optional Query Parameter Models { #optional-query-parameter-models }

group-টাকে optional করতে `| None` আর default `None` দিয়ে একটি query parameter model declare করুন।

{* ../../docs_src/query_param_models/tutorial004_an_py310.py hl[18] *}

`start` বা `end` কোনোটাই না পাঠালে `date_range` হবে `None`। যেকোনো একটা পাঠালে FastAPI model-টা validate করে, আর দুটো fields-ই চায়।

default ছাড়া `| None` ব্যবহার করলেও parameter-টা required থাকে।

বাড়তি parameters model-এর `extra` configuration মেনে চলে। উপেক্ষা করা extras-এর কারণে model-টা present ধরা হয় না।

OpenAPI group-এর fields আলাদা আলাদা করে দেখায়, আর সেগুলোকে optional হিসেবে চিহ্নিত করে।

optional [header parameter models](header-param-models.md#optional-header-parameter-models) আর [cookie parameter models](cookie-param-models.md#optional-cookie-parameter-models)-ও declare করতে পারেন।

## সারসংক্ষেপ { #summary }

**FastAPI**-তে **query parameters** declare করতে **Pydantic models** ব্যবহার করতে পারেন। 😎

/// tip | Tip

Spoiler alert: cookies আর headers declare করতেও Pydantic models ব্যবহার করতে পারেন, কিন্তু এ নিয়ে tutorial-এর পরে পড়বেন। 🤫

///
