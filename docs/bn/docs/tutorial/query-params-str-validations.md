# Query Parameters আর String Validations { #query-parameters-and-string-validations }

**FastAPI** দিয়ে আপনার parameters-এর জন্য বাড়তি তথ্য আর validation declare করতে পারেন।

উদাহরণ হিসেবে এই application-টা নেওয়া যাক:

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

query parameter `q`-এর type হলো `str | None`, মানে এটা `str` type-এর, কিন্তু `None`-ও হতে পারে, আর আসলেই এর default value `None`, তাই FastAPI জানবে এটা required নয়।

/// note | Note

default value `= None` থাকার কারণে FastAPI জানবে যে `q`-এর value required নয়।

`str | None` থাকলে আপনার editor আপনাকে আরও ভালো support দিতে আর errors ধরতে পারবে।

///

## বাড়তি validation { #additional-validation }

আমরা নিশ্চিত করব যে `q` optional হলেও, যখনই দেওয়া হবে, **এর length 50 characters-এর বেশি হবে না**।

### `Query` আর `Annotated` import করুন { #import-query-and-annotated }

এর জন্য প্রথমে import করুন:

* `fastapi` থেকে `Query`
* `typing` থেকে `Annotated`

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[1,3] *}

/// note | Note

FastAPI version 0.95.0-এ `Annotated`-এর support যোগ করেছে (আর এটা recommend করা শুরু করেছে)।

পুরোনো version থাকলে `Annotated` ব্যবহার করতে গেলে errors পাবেন।

`Annotated` ব্যবহারের আগে [FastAPI version upgrade করে](../deployment/versions.md#upgrading-the-fastapi-versions) অন্তত 0.95.1 করে নিন।

///

## `q` parameter-এর type-এ `Annotated` ব্যবহার করুন { #use-annotated-in-the-type-for-the-q-parameter }

মনে আছে, আগে [Python Types Intro](../python-types.md#type-hints-with-metadata-annotations)-এ বলেছিলাম যে আপনার parameters-এ metadata যোগ করতে `Annotated` ব্যবহার করা যায়?

এবার FastAPI-এর সাথে এটা ব্যবহার করার সময়। 🚀

আমাদের এই type annotation ছিল:

```Python
q: str | None = None
```

আমরা এটাকে `Annotated` দিয়ে মুড়ে দেব, তাহলে এটা হবে:

```Python
q: Annotated[str | None] = None
```

দুটো version-এর মানে একই, `q` একটি parameter যেটা `str` বা `None` হতে পারে, আর default-ভাবে এটা `None`।

এবার মজার অংশে যাওয়া যাক। 🎉

## `q` parameter-এর `Annotated`-এ `Query` যোগ করুন { #add-query-to-annotated-in-the-q-parameter }

এখন যেহেতু আমাদের এই `Annotated` আছে যেখানে আরও তথ্য (এখানে কিছু বাড়তি validation) রাখা যায়, তাই `Annotated`-এর ভেতরে `Query` যোগ করুন, আর `max_length` parameter `50` set করুন:

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

খেয়াল করুন, default value এখনো `None`, তাই parameter-টা এখনো optional।

কিন্তু এখন `Annotated`-এর ভেতরে `Query(max_length=50)` রেখে আমরা FastAPI-কে বলছি যে এই value-এর জন্য **বাড়তি validation** চাই, এটা সর্বোচ্চ 50 characters হবে। 😎

/// tip | Tip

এখানে `Query()` ব্যবহার করছি কারণ এটা একটি **query parameter**। পরে `Path()`, `Body()`, `Header()`, আর `Cookie()`-এর মতো অন্যগুলোও দেখব, যেগুলো `Query()`-এর মতোই একই arguments নেয়।

///

FastAPI এখন:

* data **validate** করবে, নিশ্চিত করবে যে max length 50 characters
* data valid না হলে client-কে একটি **পরিষ্কার error** দেখাবে
* OpenAPI schema *path operation*-এ parameter-টা **document** করবে (তাই এটা **automatic docs UI**-তে দেখা যাবে)

## বিকল্প (পুরোনো): default value হিসেবে `Query` { #alternative-old-query-as-the-default-value }

FastAPI-এর আগের versions-এ (<dfn title="2023-03-এর আগে">0.95.0</dfn>-এর আগে) `Query`-কে `Annotated`-এ না রেখে parameter-এর default value হিসেবে ব্যবহার করতে হতো। খুব সম্ভবত আশেপাশে এভাবে লেখা code দেখবেন, তাই এটা বুঝিয়ে বলছি।

/// tip | Tip

নতুন code-এ, আর যখনই সম্ভব, উপরে যেভাবে বলা হলো সেভাবে `Annotated` ব্যবহার করুন। এর অনেকগুলো সুবিধা আছে (নিচে বলা হয়েছে) আর কোনো অসুবিধা নেই। 🍰

///

function parameter-এর default value হিসেবে `Query()` ব্যবহার করে, `max_length` parameter 50 set করলে এরকম হবে:

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

যেহেতু এখানে (`Annotated` ব্যবহার না করে) function-এর default value `None`-কে `Query()` দিয়ে বদলাতে হয়, তাই এখন default value set করতে হবে `Query(default=None)` parameter দিয়ে, এটা ওই default value define করার একই কাজ করে (অন্তত FastAPI-এর জন্য)।

তাই:

```Python
q: str | None = Query(default=None)
```

...parameter-টাকে optional করে, default value `None`-সহ, ঠিক এটার মতো:


```Python
q: str | None = None
```

কিন্তু `Query` version-টা স্পষ্টভাবে declare করে যে এটা একটি query parameter।

তারপর `Query`-তে আরও parameters দিতে পারি। এখানে `max_length` parameter, যেটা strings-এর জন্য খাটে:

```Python
q: str | None = Query(default=None, max_length=50)
```

এটা data validate করবে, data valid না হলে পরিষ্কার error দেখাবে, আর OpenAPI schema *path operation*-এ parameter-টা document করবে।

### default value হিসেবে `Query` নাকি `Annotated`-এ { #query-as-the-default-value-or-in-annotated }

মনে রাখবেন, `Annotated`-এর ভেতরে `Query` ব্যবহার করলে `Query`-এর `default` parameter ব্যবহার করা যায় না।

এর বদলে function parameter-এর আসল default value ব্যবহার করুন। না হলে ব্যাপারটা অসংগত হয়ে যাবে।

যেমন, এটা allowed নয়:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

...কারণ পরিষ্কার না default value `"rick"` হবে নাকি `"morty"`।

তাই ব্যবহার করবেন (এটাই ভালো):

```Python
q: Annotated[str, Query()] = "rick"
```

...অথবা পুরোনো code bases-এ পাবেন:

```Python
q: str = Query(default="rick")
```

### `Annotated`-এর সুবিধা { #advantages-of-annotated }

function parameters-এ default value-এর বদলে **`Annotated` ব্যবহার করাই recommended**, অনেক কারণে এটা **ভালো**। 🤓

**function parameter**-এর **default** value-ই হলো **আসল default** value, সাধারণভাবে Python-এর সাথে এটাই বেশি স্বাভাবিক। 😌

ওই একই function FastAPI ছাড়া **অন্য জায়গাতেও call** করতে পারেন, আর এটা **ঠিকঠাক কাজ করবে**। কোনো **required** parameter (default value ছাড়া) থাকলে আপনার **editor** error দিয়ে জানিয়ে দেবে, আর required parameter না দিয়ে চালালে **Python**-ও আপত্তি করবে।

`Annotated` ব্যবহার না করে **(পুরোনো) default value style** ব্যবহার করলে, ওই function FastAPI ছাড়া **অন্য জায়গায়** call করার সময় ঠিকমতো কাজ করানোর জন্য function-এ arguments দেওয়ার কথা **মনে রাখতে** হবে, না হলে values আপনার আশার চেয়ে আলাদা হবে (যেমন `str`-এর বদলে `QueryInfo` বা এরকম কিছু)। আর আপনার editor আপত্তি করবে না, ওই function চালালে Python-ও আপত্তি করবে না, শুধু ভেতরের operations-এ error হলে বোঝা যাবে।

যেহেতু `Annotated`-এ একাধিক metadata annotation থাকতে পারে, তাই এখন এমনকি একই function অন্য tools-এর সাথেও ব্যবহার করতে পারেন, যেমন [Typer](https://typer.tiangolo.com/)। 🚀

## আরও validations যোগ করুন { #add-more-validations }

একটি `min_length` parameter-ও যোগ করতে পারেন:

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## Regular expressions যোগ করুন { #add-regular-expressions }

একটি <dfn title="regular expression, regex বা regexp হলো characters-এর একটি sequence, যেটা strings-এর জন্য একটি search pattern define করে।">regular expression</dfn> `pattern` define করতে পারেন, যেটার সাথে parameter-কে match করতে হবে:

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

এই নির্দিষ্ট regular expression pattern দেখে যে পাওয়া parameter value:

* `^`: নিচের characters দিয়ে শুরু হয়, আগে কোনো characters নেই।
* `fixedquery`: ঠিক `fixedquery` value-টাই আছে।
* `$`: ওখানেই শেষ, `fixedquery`-এর পরে আর কোনো characters নেই।

এই সব **"regular expression"** idea নিয়ে হারিয়ে গেলে চিন্তা করবেন না। অনেকের কাছেই এটা কঠিন topic। regular expressions ছাড়াও আপাতত অনেক কিছু করতে পারবেন।

এখন আপনি জানেন যে যখনই দরকার হবে, **FastAPI**-তে এগুলো ব্যবহার করতে পারবেন।

## Default values { #default-values }

অবশ্যই `None` ছাড়া অন্য default values-ও ব্যবহার করতে পারেন।

ধরুন আপনি `q` query parameter-এর `min_length` `3` আর default value `"fixedquery"` declare করতে চান:

{* ../../docs_src/query_params_str_validations/tutorial005_an_py310.py hl[9] *}

/// note | Note

যেকোনো type-এর default value থাকলে, `None` সহ, parameter-টা optional হয়ে যায় (required নয়)।

///

## Required parameters { #required-parameters }

যখন আরও validations বা metadata declare করার দরকার নেই, তখন শুধু default value declare না করেই `q` query parameter-কে required করতে পারি, এভাবে:

```Python
q: str
```

এর বদলে:

```Python
q: str | None = None
```

কিন্তু এখন আমরা এটাকে `Query` দিয়ে declare করছি, যেমন এভাবে:

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

তাই `Query` ব্যবহার করার সময় কোনো value required হিসেবে declare করতে হলে, শুধু default value declare না করলেই হলো:

{* ../../docs_src/query_params_str_validations/tutorial006_an_py310.py hl[9] *}

### Required parameters আর `None` { #required-parameters-and-none }

`str | None` type Python value হিসেবে `None` allow করে, কিন্তু এটা query parameter-কে optional করে না। default value ছাড়া parameter-টা এখনো required:

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

Query parameter values আসে strings হিসেবে, আর এদের মধ্যে `None`-এর নিজস্ব কোনো রূপ নেই। `?q=None` বা `?q=null` পাঠালে যথাক্রমে strings `"None"` আর `"null"` পাঠানো হয়। `?q=` পাঠালে একটি empty string যায়, যেটা এই উদাহরণে `min_length=3` validation-এ fail করে।

clients যাতে `q` বাদ দিতে পারে আর এর value হিসেবে `None` ব্যবহার হয়, সেজন্য এর default `None` দিন:

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

query parameters-এর মতো না, JSON request bodies-এ স্পষ্টভাবে `null` value থাকতে পারে।

## Query parameter list / multiple values { #query-parameter-list-multiple-values }

`Query` দিয়ে স্পষ্টভাবে একটি query parameter define করলে, এটাকে values-এর একটি list নেওয়ার জন্যও declare করতে পারেন, অন্যভাবে বললে, multiple values নেওয়ার জন্য।

যেমন, URL-এ একাধিকবার আসতে পারে এমন একটি query parameter `q` declare করতে লিখতে পারেন:

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

তাহলে এরকম একটি URL দিয়ে:

```
http://localhost:8000/items/?q=foo&q=bar
```

আপনার *path operation function*-এর ভেতরে, *function parameter* `q`-এ, multiple `q` *query parameters*-এর values (`foo` আর `bar`) একটি Python `list`-এ পাবেন।

তাই ওই URL-এর response হবে:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | Tip

উপরের উদাহরণের মতো `list` type-এর একটি query parameter declare করতে স্পষ্টভাবে `Query` ব্যবহার করতে হবে, না হলে এটা request body হিসেবে ধরা হবে।

///

interactive API docs সেই অনুযায়ী update হবে, multiple values allow করার জন্য:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### Defaults-সহ query parameter list / multiple values { #query-parameter-list-multiple-values-with-defaults }

কোনো value না দিলে ব্যবহারের জন্য values-এর একটি default `list`-ও define করতে পারেন:

{* ../../docs_src/query_params_str_validations/tutorial012_an_py310.py hl[9] *}

যদি যান:

```
http://localhost:8000/items/
```

তাহলে `q`-এর default হবে: `["foo", "bar"]` আর আপনার response হবে:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### শুধু `list` ব্যবহার করা { #using-just-list }

`list[str]`-এর বদলে সরাসরি `list`-ও ব্যবহার করতে পারেন:

{* ../../docs_src/query_params_str_validations/tutorial013_an_py310.py hl[9] *}

/// note | Note

মনে রাখবেন, এক্ষেত্রে FastAPI list-এর contents check করবে না।

যেমন, `list[int]` check করবে (আর document করবে) যে list-এর contents integers। কিন্তু শুধু `list` তা করবে না।

///

## আরও metadata declare করুন { #declare-more-metadata }

parameter সম্পর্কে আরও তথ্য যোগ করতে পারেন।

ওই তথ্য generate হওয়া OpenAPI-তে থাকবে, আর documentation user interfaces ও external tools ব্যবহার করবে।

/// note | Note

মনে রাখবেন, বিভিন্ন tools-এর OpenAPI support-এর level আলাদা হতে পারে।

এদের কিছু হয়তো এখনো declare করা সব বাড়তি তথ্য দেখায় না, যদিও বেশিরভাগ ক্ষেত্রে বাদ পড়া feature-টা development-এর জন্য আগে থেকেই plan করা আছে।

///

একটি `title` যোগ করতে পারেন:

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

আর একটি `description`:

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## Alias parameters { #alias-parameters }

ধরুন আপনি চান parameter-টা হোক `item-query`।

এরকম:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

কিন্তু `item-query` একটি valid Python variable name নয়।

সবচেয়ে কাছাকাছি হবে `item_query`।

কিন্তু আপনার তবুও এটা ঠিক `item-query`-ই দরকার...

তাহলে একটি `alias` declare করতে পারেন, আর parameter value খুঁজতে ওই alias-টাই ব্যবহার হবে:

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## Parameters deprecate করা { #deprecating-parameters }

এবার ধরুন এই parameter-টা আপনার আর পছন্দ না।

কিছু clients এটা ব্যবহার করছে বলে কিছুদিন এটা রেখে দিতে হবে, কিন্তু আপনি চান docs-এ এটাকে স্পষ্টভাবে <dfn title="পুরোনো হয়ে গেছে, ব্যবহার না করার পরামর্শ দেওয়া হয়">deprecated</dfn> হিসেবে দেখানো হোক।

তাহলে `Query`-তে `deprecated=True` parameter দিন:

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

docs-এ এটা এভাবে দেখাবে:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## OpenAPI থেকে parameters বাদ দিন { #exclude-parameters-from-openapi }

generate হওয়া OpenAPI schema থেকে (আর তাই automatic documentation systems থেকেও) একটি query parameter বাদ দিতে, `Query`-এর `include_in_schema` parameter `False` set করুন:

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## Custom Validation { #custom-validation }

এমন অবস্থা আসতে পারে যেখানে কিছু **custom validation** দরকার, যেটা উপরে দেখানো parameters দিয়ে করা যায় না।

সেক্ষেত্রে একটি **custom validator function** ব্যবহার করতে পারেন, যেটা স্বাভাবিক validation-এর পরে চলে (যেমন value-টা একটি `str` কিনা validate করার পরে)।

এটা করতে পারেন `Annotated`-এর ভেতরে [Pydantic-এর `AfterValidator`](https://pydantic.dev/docs/validation/latest/concepts/validators/#field-after-validator) ব্যবহার করে।

/// tip | Tip

Pydantic-এ [`BeforeValidator`](https://pydantic.dev/docs/validation/latest/concepts/validators/#field-before-validator) আর অন্যগুলোও আছে। 🤓

///

যেমন, এই custom validator check করে যে item ID একটি <abbr title="International Standard Book Number">ISBN</abbr> book number-এর জন্য `isbn-` দিয়ে, বা একটি <abbr title="Internet Movie Database: movies নিয়ে তথ্যের একটি website">IMDB</abbr> movie URL ID-এর জন্য `imdb-` দিয়ে শুরু হয়:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py hl[5,16:19,24] *}

/// note | Note

এটা Pydantic version 2 বা তার উপরে পাওয়া যায়। 😎

///

/// tip | Tip

যদি এমন কোনো validation করতে হয় যেটার জন্য কোনো **external component**-এর সাথে যোগাযোগ করতে হয়, যেমন একটি database বা অন্য কোনো API, তাহলে এর বদলে **FastAPI Dependencies** ব্যবহার করা উচিত, পরে এগুলো শিখবেন।

এই custom validators সেই জিনিসগুলোর জন্য, যেগুলো request-এ দেওয়া **শুধু** **একই data** দিয়ে check করা যায়।

///

### Code-টা বুঝুন { #understand-that-code }

গুরুত্বপূর্ণ ব্যাপার শুধু **`Annotated`-এর ভেতরে একটি function সহ `AfterValidator`** ব্যবহার করা। চাইলে এই অংশটা বাদ দিতে পারেন। 🤸

---

কিন্তু এই নির্দিষ্ট code উদাহরণ নিয়ে কৌতূহল থাকলে আর এখনো মজা পাচ্ছেন, তাহলে এখানে কিছু বাড়তি details আছে।

#### `value.startswith()`-সহ string { #string-with-value-startswith }

খেয়াল করেছেন? `value.startswith()` ব্যবহার করা একটি string একটি tuple নিতে পারে, আর এটা tuple-এর প্রতিটা value check করবে:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[16:19] hl[17] *}

#### একটি Random Item { #a-random-item }

`data.items()` দিয়ে আমরা একটি <dfn title="এমন কিছু যার উপর for loop দিয়ে iterate করা যায়, যেমন একটি list, set, ইত্যাদি।">iterable object</dfn> পাই, যেখানে প্রতিটি dictionary item-এর key আর value-সহ tuples থাকে।

`list(data.items())` দিয়ে এই iterable object-টাকে একটি সত্যিকারের `list`-এ convert করি।

তারপর `random.choice()` দিয়ে list থেকে একটি **random value** পেতে পারি, তাই আমরা `(id, name)`-সহ একটি tuple পাই। এটা হবে এরকম কিছু: `("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy")`।

তারপর tuple-এর **ওই দুটো values** variables `id` আর `name`-এ **বসিয়ে দিই**।

তাই user কোনো item ID না দিলেও একটি random suggestion পাবেন।

...এই সবকিছু আমরা করি **একটি মাত্র সহজ line**-এ। 🤯 Python ভালো লাগে না? 🐍

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[22:30] hl[29] *}

## Recap { #recap }

আপনার parameters-এর জন্য বাড়তি validations আর metadata declare করতে পারেন।

সাধারণ validations আর metadata:

* `alias`
* `title`
* `description`
* `deprecated`

শুধু strings-এর জন্য validations:

* `min_length`
* `max_length`
* `pattern`

`AfterValidator` দিয়ে custom validations।

এই উদাহরণগুলোতে দেখলেন `str` values-এর জন্য কীভাবে validations declare করতে হয়।

numbers-এর মতো অন্য types-এর জন্য কীভাবে validations declare করতে হয়, সেটা শিখতে পরের chapters দেখুন।
