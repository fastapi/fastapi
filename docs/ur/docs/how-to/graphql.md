# GraphQL { #graphql }

چونکہ **FastAPI** کی بنیاد **ASGI** standard پر ہے، اس لیے ASGI کے ساتھ ہم آہنگ کسی بھی **GraphQL** لائبریری کو آسانی سے شامل کیا جا سکتا ہے۔

آپ ایک ہی application میں عام FastAPI *path operations* کو GraphQL کے ساتھ ملا سکتے ہیں۔

/// tip | مشورہ

**GraphQL** کچھ بہت مخصوص استعمال کے معاملات حل کرتا ہے۔

عام **web APIs** کے مقابلے میں اس کے **فوائد** اور **نقصانات** ہیں۔

یقینی بنائیں کہ آپ کے استعمال کے معاملے کے لیے **فوائد** کیا **نقصانات** کی تلافی کرتے ہیں۔ 🤓

///

## GraphQL لائبریریاں { #graphql-libraries }

یہاں کچھ **GraphQL** لائبریریاں ہیں جن میں **ASGI** سپورٹ موجود ہے۔ آپ انہیں **FastAPI** کے ساتھ استعمال کر سکتے ہیں:

* [Strawberry](https://strawberry.rocks/) 🍓
    * [FastAPI کے لیے دستاویزات](https://strawberry.rocks/docs/integrations/fastapi) کے ساتھ
* [Ariadne](https://ariadnegraphql.org/)
    * [FastAPI کے لیے دستاویزات](https://ariadnegraphql.org/docs/fastapi-integration) کے ساتھ
* [Tartiflette](https://tartiflette.io/)
    * ASGI integration فراہم کرنے کے لیے [Tartiflette ASGI](https://tartiflette.github.io/tartiflette-asgi/) کے ساتھ
* [Graphene](https://graphene-python.org/)
    * [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3) کے ساتھ

## Strawberry کے ساتھ GraphQL { #graphql-with-strawberry }

اگر آپ کو **GraphQL** کے ساتھ کام کرنے کی ضرورت ہے یا آپ چاہتے ہیں، تو [**Strawberry**](https://strawberry.rocks/) **تجویز کردہ** لائبریری ہے کیونکہ اس کا ڈیزائن **FastAPI** کے ڈیزائن سے سب سے قریب ہے، یہ سب **type annotations** پر مبنی ہے۔

آپ کے استعمال کے معاملے کے مطابق، آپ کسی مختلف لائبریری کو ترجیح دے سکتے ہیں، لیکن اگر آپ مجھ سے پوچھیں، تو میں غالباً **Strawberry** آزمانے کا مشورہ دوں گا۔

یہاں ایک مختصر جائزہ ہے کہ آپ Strawberry کو FastAPI کے ساتھ کیسے شامل کر سکتے ہیں:

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

آپ Strawberry کے بارے میں مزید [Strawberry دستاویزات](https://strawberry.rocks/) میں جان سکتے ہیں۔

اور [Strawberry with FastAPI](https://strawberry.rocks/docs/integrations/fastapi) کی دستاویزات بھی دیکھیں۔

## Starlette سے پرانا `GraphQLApp` { #older-graphqlapp-from-starlette }

Starlette کے پچھلے ورژنز میں [Graphene](https://graphene-python.org/) کے ساتھ integration کے لیے `GraphQLApp` class شامل تھی۔

اسے Starlette سے deprecated کر دیا گیا تھا، لیکن اگر آپ کے پاس ایسا کوڈ ہے جو اسے استعمال کرتا تھا، تو آپ آسانی سے [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3) پر **منتقل** ہو سکتے ہیں، جو وہی استعمال کے معاملے کا احاطہ کرتا ہے اور **تقریباً ایک جیسا interface** رکھتا ہے۔

/// tip | مشورہ

اگر آپ کو GraphQL کی ضرورت ہے، تو میں پھر بھی تجویز کروں گا کہ آپ [Strawberry](https://strawberry.rocks/) دیکھیں، کیونکہ یہ custom classes اور types کی بجائے type annotations پر مبنی ہے۔

///

## مزید جانیں { #learn-more }

آپ **GraphQL** کے بارے میں مزید [GraphQL کی سرکاری دستاویزات](https://graphql.org/) میں جان سکتے ہیں۔

آپ اوپر بیان کردہ ہر لائبریری کے بارے میں ان کے لنکس میں مزید پڑھ سکتے ہیں۔
