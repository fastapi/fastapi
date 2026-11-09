# Body - Fields { #body-fields }

`Query`, `Path` আর `Body` দিয়ে যেভাবে *path operation function* parameters-এ বাড়তি validation আর metadata declare করা যায়, ঠিক সেভাবেই Pydantic-এর `Field` দিয়ে Pydantic models-এর ভেতরে validation আর metadata declare করতে পারেন।

## `Field` import করুন { #import-field }

প্রথমে এটা import করতে হবে:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[4] *}


/// warning | Warning

খেয়াল করুন, `Field` সরাসরি `pydantic` থেকে import করা হয়, বাকিগুলোর (`Query`, `Path`, `Body`, ইত্যাদি) মতো `fastapi` থেকে নয়।

///

## Model attributes declare করুন { #declare-model-attributes }

তারপর model attributes-এর সাথে `Field` ব্যবহার করতে পারেন:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[11:14] *}

`Field`, `Query`, `Path` আর `Body`-এর মতোই কাজ করে, এর একই parameters আছে, ইত্যাদি।

/// note | Technical Details

আসলে `Query`, `Path` আর এর পরে যেগুলো দেখবেন, সেগুলো একটি common `Param` class-এর subclasses-এর objects বানায়, যেটা নিজেই Pydantic-এর `FieldInfo` class-এর একটি subclass।

আর Pydantic-এর `Field`-ও `FieldInfo`-এর একটি instance return করে।

`Body`-ও সরাসরি `FieldInfo`-এর একটি subclass-এর objects return করে। আর পরে আরও কিছু দেখবেন যেগুলো `Body` class-এর subclasses।

মনে রাখবেন, `fastapi` থেকে `Query`, `Path` আর অন্যগুলো import করলে, সেগুলো আসলে functions, যেগুলো special classes return করে।

///

/// tip | Tip

খেয়াল করুন, type, default value আর `Field`-সহ প্রতিটি model attribute-এর গঠন একটি *path operation function*-এর parameter-এর মতোই, শুধু `Path`, `Query` আর `Body`-এর বদলে `Field`।

///

## বাড়তি তথ্য যোগ করুন { #add-extra-information }

`Field`, `Query`, `Body`, ইত্যাদিতে `json_schema_extra` দিয়ে বাড়তি তথ্য declare করতে পারেন। আর সেটা generate হওয়া JSON Schema-তে থাকবে।

পরে docs-এ examples declare করা শেখার সময় বাড়তি তথ্য যোগ করা নিয়ে আরও শিখবেন।

/// warning | Warning

`json_schema_extra`-এ দেওয়া বাড়তি keys আপনার application-এর তৈরি হওয়া OpenAPI schema-তেও থাকবে।
যেহেতু এই keys OpenAPI specification-এর অংশ নাও হতে পারে, তাই কিছু OpenAPI tools, যেমন [OpenAPI validator](https://validator.swagger.io/), আপনার generate হওয়া schema-র সাথে কাজ নাও করতে পারে।

///

## Recap { #recap }

model attributes-এর জন্য বাড়তি validations আর metadata declare করতে Pydantic-এর `Field` ব্যবহার করতে পারেন।

বাড়তি JSON Schema metadata দিতে `json_schema_extra`-ও ব্যবহার করতে পারেন।
