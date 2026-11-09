# Path Parameters আর Numeric Validations { #path-parameters-and-numeric-validations }

`Query` দিয়ে যেভাবে query parameters-এর জন্য আরও validations আর metadata declare করা যায়, ঠিক সেভাবেই `Path` দিয়ে path parameters-এর জন্য একই ধরনের validations আর metadata declare করতে পারেন।

## `Path` import করুন { #import-path }

প্রথমে `fastapi` থেকে `Path` import করুন, আর `Annotated` import করুন:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// note | Note

FastAPI version 0.95.0-এ `Annotated`-এর support যোগ করেছে (আর এটা recommend করা শুরু করেছে)।

পুরোনো version থাকলে `Annotated` ব্যবহার করতে গেলে errors পাবেন।

`Annotated` ব্যবহারের আগে [FastAPI version upgrade করে](../deployment/versions.md#upgrading-the-fastapi-versions) অন্তত 0.95.1 করে নিন।

///

## Metadata declare করুন { #declare-metadata }

`Query`-এর জন্য যেসব parameters declare করা যায়, সেগুলো সবই এখানে declare করতে পারেন।

যেমন, path parameter `item_id`-এর জন্য একটি `title` metadata value declare করতে লিখতে পারেন:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note | Note

একটি path parameter সবসময় required, কারণ এটাকে URL path-এর অংশ হতেই হবে। এর type-এ `None` যোগ করলেও এটা optional হয় না। `Path` দিয়ে declare করা parameter-এর default value থাকতে পারে না।

///

## দরকারমতো parameters সাজান { #order-the-parameters-as-you-need }

/// tip | Tip

`Annotated` ব্যবহার করলে এটা সম্ভবত অতটা গুরুত্বপূর্ণ বা দরকারি না।

///

ধরুন আপনি query parameter `q`-কে একটি required `str` হিসেবে declare করতে চান।

আর ওই parameter-এর জন্য আর কিছু declare করার দরকার নেই, তাই আসলে `Query` ব্যবহার করারও দরকার নেই।

কিন্তু `item_id` path parameter-এর জন্য তবুও `Path` ব্যবহার করতে হবে। আর কোনো কারণে আপনি `Annotated` ব্যবহার করতে চান না।

"default" নেই এমন একটি value-এর আগে "default"-সহ একটি value বসালে Python আপত্তি করবে।

কিন্তু এগুলোর ক্রম বদলে নিতে পারেন, default ছাড়া value-টা (query parameter `q`) আগে রেখে।

**FastAPI**-এর কাছে এতে কিছু যায় আসে না। এটা parameters চেনে তাদের নাম, types আর default declarations (`Query`, `Path`, ইত্যাদি) দেখে, ক্রম নিয়ে মাথা ঘামায় না।

তাই আপনার function এভাবে declare করতে পারেন:

{* ../../docs_src/path_params_numeric_validations/tutorial002_py310.py hl[7] *}

তবে মনে রাখবেন, `Annotated` ব্যবহার করলে এই সমস্যা হবে না, কারণ তখন `Query()` বা `Path()`-এর জন্য function parameter default values ব্যবহার করছেন না।

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py310.py *}

## দরকারমতো parameters সাজানো, কিছু কৌশল { #order-the-parameters-as-you-need-tricks }

/// tip | Tip

`Annotated` ব্যবহার করলে এটা সম্ভবত অতটা গুরুত্বপূর্ণ বা দরকারি না।

///

এখানে একটি **ছোট কৌশল** আছে যেটা কাজে লাগতে পারে, কিন্তু খুব বেশি দরকার হবে না।

যদি আপনি চান:

* `q` query parameter-টা `Query` বা কোনো default value ছাড়াই declare করতে
* path parameter `item_id`-টা `Path` দিয়ে declare করতে
* এগুলো অন্য ক্রমে রাখতে
* `Annotated` ব্যবহার না করতে

...তাহলে Python-এ এর জন্য একটু বিশেষ syntax আছে।

function-এর প্রথম parameter হিসেবে `*` দিন।

Python ওই `*` নিয়ে কিছুই করবে না, কিন্তু এটা জানবে যে এর পরের সব parameters keyword arguments (key-value pairs) হিসেবে call করতে হবে, যেগুলো <abbr title="From: K-ey W-ord Arg-uments"><code>kwargs</code></abbr> নামেও পরিচিত। এমনকি সেগুলোর default value না থাকলেও।

{* ../../docs_src/path_params_numeric_validations/tutorial003_py310.py hl[7] *}

### `Annotated` দিয়ে আরও ভালো { #better-with-annotated }

মনে রাখবেন, `Annotated` ব্যবহার করলে, যেহেতু function parameter default values ব্যবহার করছেন না, তাই এই সমস্যা হবে না, আর সম্ভবত `*` ব্যবহার করারও দরকার হবে না।

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py310.py hl[10] *}

## Number validations: greater than or equal { #number-validations-greater-than-or-equal }

`Query` আর `Path` দিয়ে (আর পরে যেগুলো দেখবেন সেগুলো দিয়েও) number constraints declare করতে পারেন।

এখানে `ge=1` দিয়ে, `item_id`-কে এমন একটি integer number হতে হবে যেটা `1`-এর "`g`reater than or `e`qual"।

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py310.py hl[10] *}

## Number validations: greater than and less than or equal { #number-validations-greater-than-and-less-than-or-equal }

এগুলোর ক্ষেত্রেও একই কথা:

* `gt`: `g`reater `t`han
* `le`: `l`ess than or `e`qual

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py310.py hl[10] *}

## Number validations: floats, greater than and less than { #number-validations-floats-greater-than-and-less-than }

Number validations `float` values-এর জন্যও কাজ করে।

এখানেই শুধু <abbr title="greater than or equal"><code>ge</code></abbr> নয়, <abbr title="greater than"><code>gt</code></abbr> declare করতে পারাটা গুরুত্বপূর্ণ হয়ে ওঠে। কারণ এটা দিয়ে আপনি চাইতে পারেন, যেমন, একটি value অবশ্যই `0`-এর চেয়ে বড় হবে, `1`-এর চেয়ে ছোট হলেও।

তাই `0.5` একটি valid value হবে। কিন্তু `0.0` বা `0` হবে না।

আর <abbr title="less than"><code>lt</code></abbr>-এর ক্ষেত্রেও একই।

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py310.py hl[13] *}

## Recap { #recap }

`Query`, `Path` (আর অন্যগুলো যেগুলো এখনো দেখেননি) দিয়ে metadata আর string validations declare করতে পারেন, [Query Parameters and String Validations](query-params-str-validations.md)-এর মতো একইভাবে।

আর numeric validations-ও declare করতে পারেন:

* `gt`: `g`reater `t`han
* `ge`: `g`reater than or `e`qual
* `lt`: `l`ess `t`han
* `le`: `l`ess than or `e`qual

/// note | Note

`Query`, `Path`, আর পরে যেসব classes দেখবেন, সেগুলো একটি common `Param` class-এর subclasses।

এরা সবাই বাড়তি validation আর metadata-এর জন্য একই parameters share করে, যেগুলো আপনি দেখেছেন।

///

/// note | Technical Details

`fastapi` থেকে `Query`, `Path` আর অন্যগুলো import করলে, এগুলো আসলে functions।

যেগুলো call করলে একই নামের classes-এর instances return করে।

তাই আপনি `Query` import করেন, যেটা একটি function। আর এটা call করলে এটা `Query` নামেরই একটি class-এর instance return করে।

এই functions রাখা হয়েছে (সরাসরি classes ব্যবহার না করে) যাতে আপনার editor এদের types নিয়ে errors না দেখায়।

এভাবে ওই errors উপেক্ষা করার জন্য custom configuration যোগ না করেই আপনার স্বাভাবিক editor আর coding tools ব্যবহার করতে পারবেন।

///
