# Body - Multiple Parameters { #body-multiple-parameters }

এখন যেহেতু `Path` আর `Query` কীভাবে ব্যবহার করতে হয় দেখেছি, চলুন request body declarations-এর আরও advanced ব্যবহার দেখি।

## `Path`, `Query` আর body parameters মেশান { #mix-path-query-and-body-parameters }

প্রথমত, অবশ্যই `Path`, `Query` আর request body parameter declarations ইচ্ছামতো মেশাতে পারেন, আর **FastAPI** জানবে কী করতে হবে।

আর default `None` set করে body parameters-কেও optional হিসেবে declare করতে পারেন:

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note | Note

খেয়াল করুন, এখানে body থেকে যে `item` নেওয়া হবে সেটা optional। কারণ এর default value `None`।

///

## Multiple body parameters { #multiple-body-parameters }

আগের উদাহরণে *path operations* একটি `Item`-এর attributes-সহ একটি JSON body আশা করত, এরকম:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

কিন্তু একাধিক body parameters-ও declare করতে পারেন, যেমন `item` আর `user`:

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}


এখানে **FastAPI** খেয়াল করবে যে function-এ একাধিক body parameter আছে (দুটো parameters আছে যেগুলো Pydantic models)।

তাই এটা parameter names-গুলো body-তে keys (field names) হিসেবে ব্যবহার করবে, আর এরকম একটি body আশা করবে:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

/// note | Note

খেয়াল করুন, `item` আগের মতো একইভাবে declare করা হলেও, এখন এটাকে body-র ভেতরে `item` key-সহ আশা করা হচ্ছে।

///

**FastAPI** request থেকে automatic conversion করবে, যাতে parameter `item` নিজের নির্দিষ্ট content পায়, আর `user`-এর ক্ষেত্রেও একই।

এটা যৌগিক data-এর validation করবে, আর OpenAPI schema আর automatic docs-এর জন্য সেভাবেই document করবে।

## Body-তে singular values { #singular-values-in-body }

query আর path parameters-এর জন্য বাড়তি data define করতে যেভাবে `Query` আর `Path` আছে, সেভাবেই **FastAPI** এর সমান একটি `Body` দেয়।

যেমন, আগের model-টা বাড়িয়ে আপনি ঠিক করতে পারেন যে `item` আর `user`-এর পাশাপাশি একই body-তে আরেকটি key `importance` রাখতে চান।

এটা যেমন আছে তেমন declare করলে, যেহেতু এটা একটি singular value, **FastAPI** ধরে নেবে এটা একটি query parameter।

কিন্তু `Body` ব্যবহার করে **FastAPI**-কে বলতে পারেন এটাকে আরেকটি body key হিসেবে ধরতে:

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}


এখানে **FastAPI** এরকম একটি body আশা করবে:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

আবারও, এটা data types convert করবে, validate করবে, document করবে, ইত্যাদি।

## Multiple body params আর query { #multiple-body-params-and-query }

অবশ্যই, যখনই দরকার, যেকোনো body parameters-এর পাশাপাশি বাড়তি query parameters-ও declare করতে পারেন।

যেহেতু default-ভাবে singular values query parameters হিসেবে ধরা হয়, তাই স্পষ্টভাবে `Query` যোগ করার দরকার নেই, শুধু এভাবে করতে পারেন:

```Python
q: str | None = None
```

যেমন:

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}


/// note | Note

`Body`-তেও `Query`, `Path` আর পরে যেগুলো দেখবেন, সেগুলোর মতো একই বাড়তি validation আর metadata parameters আছে।

///

## একটি single body parameter embed করুন { #embed-a-single-body-parameter }

ধরুন আপনার শুধু একটি Pydantic model `Item` থেকে একটি single `item` body parameter আছে।

default-ভাবে **FastAPI** তখন সরাসরি এর body আশা করবে।

কিন্তু আপনি যদি চান এটা `item` key-সহ একটি JSON আশা করুক, যার ভেতরে model-এর contents থাকবে, যেমনটা বাড়তি body parameters declare করলে হয়, তাহলে special `Body` parameter `embed` ব্যবহার করতে পারেন:

```Python
item: Annotated[Item, Body(embed=True)]
```

যেমন:

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}


এখানে **FastAPI** এরকম একটি body আশা করবে:

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

এর বদলে:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## Recap { #recap }

আপনার *path operation function*-এ একাধিক body parameters যোগ করতে পারেন, যদিও একটি request-এ শুধু একটিই body থাকতে পারে।

কিন্তু **FastAPI** এটা handle করবে, আপনার function-এ সঠিক data দেবে, আর *path operation*-এ সঠিক schema validate ও document করবে।

singular values-ও body-র অংশ হিসেবে নেওয়ার জন্য declare করতে পারেন।

আর শুধু একটি parameter declare করা থাকলেও **FastAPI**-কে body-টা একটি key-এর ভেতরে embed করতে বলতে পারেন।
