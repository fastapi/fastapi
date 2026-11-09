# Request Body { #request-body }

যখন কোনো client (ধরুন, একটি browser) থেকে আপনার API-তে data পাঠাতে হয়, তখন সেটা **request body** হিসেবে পাঠানো হয়।

**request** body হলো client থেকে আপনার API-তে পাঠানো data। **response** body হলো আপনার API থেকে client-এ পাঠানো data।

আপনার API-কে প্রায় সবসময়ই একটি **response** body পাঠাতে হয়। কিন্তু clients-কে সবসময় **request body** পাঠাতে হবে, এমন না। কখনো কখনো তারা শুধু একটি path request করে, হয়তো কিছু query parameters সহ, কিন্তু কোনো body পাঠায় না।

একটি **request** body declare করতে [Pydantic](https://pydantic.dev/docs/) models ব্যবহার করা হয়, এর সব শক্তি আর সুবিধা সহ।

/// note | Note

data পাঠাতে এগুলোর একটি ব্যবহার করা উচিত: `POST` (সবচেয়ে বেশি ব্যবহৃত), `PUT`, `DELETE` বা `PATCH`।

specifications অনুযায়ী `GET` request-এ body পাঠানোর behavior undefined, তবুও FastAPI এটা support করে, শুধু খুব জটিল বা extreme use cases-এর জন্য।

যেহেতু এটা করতে নিরুৎসাহিত করা হয়, তাই `GET` ব্যবহার করলে Swagger UI-এর interactive docs body-র documentation দেখাবে না, আর মাঝখানের proxies হয়তো এটা support করবে না।

///

## Pydantic-এর `BaseModel` import করুন { #import-pydantics-basemodel }

প্রথমে `pydantic` থেকে `BaseModel` import করতে হবে:

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## আপনার data model বানান { #create-your-data-model }

তারপর আপনার data model-টা `BaseModel` থেকে inherit করা একটি class হিসেবে declare করুন।

সব attributes-এর জন্য standard Python types ব্যবহার করুন:

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}


query parameters declare করার মতোই, কোনো model attribute-এর default value থাকলে সেটা required নয়। না থাকলে সেটা required। শুধু optional করতে চাইলে `None` ব্যবহার করুন।

যেমন, উপরের model-টা এরকম একটি JSON "`object`" (বা Python `dict`) declare করে:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...যেহেতু `description` আর `tax` optional (default value `None`), তাই এই JSON "`object`"-টাও valid হবে:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## এটাকে parameter হিসেবে declare করুন { #declare-it-as-a-parameter }

আপনার *path operation*-এ এটা যোগ করতে, path আর query parameters যেভাবে declare করেছিলেন, ঠিক সেভাবেই declare করুন:

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

...আর এর type হিসেবে আপনার বানানো model `Item` দিন।

## ফলাফল { #results }

শুধু ওই Python type declaration দিয়েই **FastAPI**:

* request-এর body JSON হিসেবে পড়বে।
* দরকার হলে সংশ্লিষ্ট types-এ convert করবে।
* data validate করবে।
    * data invalid হলে সুন্দর, পরিষ্কার একটি error return করবে, যেখানে ঠিক কোথায় আর কোন data ভুল ছিল, সেটা বলা থাকবে।
* পাওয়া data parameter `item`-এ আপনাকে দেবে।
    * যেহেতু function-এ এটাকে `Item` type হিসেবে declare করেছেন, তাই সব attributes আর তাদের types-এর জন্য পুরো editor support-ও (completion, ইত্যাদি) পাবেন।
* আপনার model-এর জন্য [JSON Schema](https://json-schema.org) definitions generate করবে, আপনার project-এ কাজে লাগলে এগুলো অন্য যেকোনো জায়গাতেও ব্যবহার করতে পারেন।
* এই schemas generate হওয়া OpenAPI schema-র অংশ হবে, আর automatic documentation <abbr title="User Interfaces">UIs</abbr> এগুলো ব্যবহার করবে।

## Automatic docs { #automatic-docs }

আপনার models-এর JSON Schemas generate হওয়া OpenAPI schema-র অংশ হবে, আর interactive API docs-এ দেখানো হবে:

<img src="/img/tutorial/body/image01.png">

আর যেসব *path operation*-এ এগুলো দরকার, সেগুলোর API docs-এর ভেতরেও ব্যবহার হবে:

<img src="/img/tutorial/body/image02.png">

## Editor support { #editor-support }

আপনার editor-এ, function-এর ভেতরে সব জায়গায় type hints আর completion পাবেন (Pydantic model-এর বদলে একটি `dict` পেলে এটা হতো না):

<img src="/img/tutorial/body/image03.png">

ভুল type operations-এর জন্য error checks-ও পাবেন:

<img src="/img/tutorial/body/image04.png">

এটা কাকতালীয় নয়, পুরো framework-টাই এই design-কে ঘিরে বানানো।

আর implementation শুরুর আগেই, design phase-এ এটা ভালোভাবে test করা হয়েছিল, যাতে সব editor-এ কাজ করে।

এটা support করার জন্য Pydantic-এও কিছু পরিবর্তন করা হয়েছিল।

আগের screenshots-গুলো [Visual Studio Code](https://code.visualstudio.com) দিয়ে নেওয়া।

কিন্তু [PyCharm](https://www.jetbrains.com/pycharm/) আর বেশিরভাগ অন্য Python editors-এও একই editor support পাবেন:

<img src="/img/tutorial/body/image05.png">

/// tip | Tip

editor হিসেবে [PyCharm](https://www.jetbrains.com/pycharm/) ব্যবহার করলে [Pydantic PyCharm Plugin](https://github.com/koxudaxi/pydantic-pycharm-plugin/) ব্যবহার করতে পারেন।

এটা Pydantic models-এর জন্য editor support আরও ভালো করে, যেমন:

* auto-completion
* type checks
* refactoring
* searching
* inspections

///

## Model-টা ব্যবহার করুন { #use-the-model }

function-এর ভেতরে model object-এর সব attributes সরাসরি access করতে পারবেন:

{* ../../docs_src/body/tutorial002_py310.py *}

## Request body + path parameters { #request-body-path-parameters }

একই সময়ে path parameters আর request body declare করতে পারেন।

**FastAPI** বুঝে নেবে যে path parameters-এর সাথে মেলে এমন function parameters **path থেকে নিতে হবে**, আর যেসব function parameters Pydantic models হিসেবে declare করা, সেগুলো **request body থেকে নিতে হবে**।

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}


## Request body + path + query parameters { #request-body-path-query-parameters }

**body**, **path** আর **query** parameters, সবগুলো একসাথেও declare করতে পারেন।

**FastAPI** প্রতিটাকে চিনে নেবে আর সঠিক জায়গা থেকে data নেবে।

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

function parameters এভাবে চেনা হবে:

* parameter-টা যদি **path**-এও declare করা থাকে, তাহলে এটা path parameter হিসেবে ব্যবহার হবে।
* parameter-টা যদি **singular type**-এর হয় (যেমন `int`, `float`, `str`, `bool`, ইত্যাদি), তাহলে এটা **query** parameter হিসেবে ধরা হবে।
* parameter-টা যদি একটি **Pydantic model**-এর type হিসেবে declare করা থাকে, তাহলে এটা request **body** হিসেবে ধরা হবে।

/// note | Note

default value `= None` থাকার কারণে FastAPI জানবে যে `q`-এর value required নয়।

value required নয়, এটা ঠিক করতে FastAPI `str | None` ব্যবহার করে না, এটা জানে কারণ এর default value `= None`।

তবে type annotations যোগ করলে আপনার editor আপনাকে আরও ভালো support দিতে আর errors ধরতে পারবে।

///

## Pydantic ছাড়া { #without-pydantic }

Pydantic models ব্যবহার করতে না চাইলে **Body** parameters-ও ব্যবহার করতে পারেন। [Body - Multiple Parameters: Singular values in body](body-multiple-params.md#singular-values-in-body)-এর docs দেখুন।
