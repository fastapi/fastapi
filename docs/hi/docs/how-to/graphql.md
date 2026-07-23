# GraphQL { #graphql }

क्योंकि **FastAPI** **ASGI** standard पर आधारित है, इसलिए ASGI के साथ compatible किसी भी **GraphQL** library को integrate करना बहुत आसान है।

आप उसी application में सामान्य FastAPI *path operations* को GraphQL के साथ combine कर सकते हैं।

/// tip | सुझाव

**GraphQL** कुछ बहुत specific use cases को solve करता है।

Common **web APIs** की तुलना में इसके **advantages** और **disadvantages** हैं।

सुनिश्चित करें कि आप evaluate करें कि आपके use case के लिए **benefits**, **drawbacks** की भरपाई करते हैं या नहीं। 🤓

///

## GraphQL Libraries { #graphql-libraries }

यहाँ कुछ **GraphQL** libraries हैं जिनमें **ASGI** support है। आप उन्हें **FastAPI** के साथ उपयोग कर सकते हैं:

* [Strawberry](https://strawberry.rocks/) 🍓
    * [FastAPI के लिए docs](https://strawberry.rocks/docs/integrations/fastapi) के साथ
* [Ariadne](https://ariadnegraphql.org/)
    * [FastAPI के लिए docs](https://ariadnegraphql.org/docs/fastapi-integration) के साथ
* [Tartiflette](https://tartiflette.io/)
    * ASGI integration प्रदान करने के लिए [Tartiflette ASGI](https://tartiflette.github.io/tartiflette-asgi/) के साथ
* [Graphene](https://graphene-python.org/)
    * [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3) के साथ

## Strawberry के साथ GraphQL { #graphql-with-strawberry }

यदि आपको **GraphQL** के साथ काम करने की ज़रूरत है या आप करना चाहते हैं, तो [**Strawberry**](https://strawberry.rocks/) **recommended** library है क्योंकि इसका design **FastAPI** के design के सबसे करीब है, यह पूरी तरह **type annotations** पर आधारित है।

आपके use case के आधार पर, आप कोई अलग library उपयोग करना पसंद कर सकते हैं, लेकिन अगर आप मुझसे पूछें, तो मैं शायद सुझाव दूँगा कि आप **Strawberry** आज़माएँ।

यहाँ एक छोटा preview है कि आप Strawberry को FastAPI के साथ कैसे integrate कर सकते हैं:

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

आप [Strawberry documentation](https://strawberry.rocks/) में Strawberry के बारे में और जान सकते हैं।

और [FastAPI के साथ Strawberry](https://strawberry.rocks/docs/integrations/fastapi) के बारे में docs भी।

## Starlette से पुराना `GraphQLApp` { #older-graphqlapp-from-starlette }

Starlette के पिछले versions में [Graphene](https://graphene-python.org/) के साथ integrate करने के लिए एक `GraphQLApp` class शामिल थी।

इसे Starlette से deprecated कर दिया गया था, लेकिन यदि आपके पास ऐसा code है जो इसका उपयोग करता था, तो आप आसानी से [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3) पर **migrate** कर सकते हैं, जो वही use case cover करता है और जिसका **लगभग identical interface** है।

/// tip | सुझाव

यदि आपको GraphQL की ज़रूरत है, तो मैं फिर भी recommend करूँगा कि आप [Strawberry](https://strawberry.rocks/) देखें, क्योंकि यह custom classes और types की बजाय type annotations पर आधारित है।

///

## और जानें { #learn-more }

आप [official GraphQL documentation](https://graphql.org/) में **GraphQL** के बारे में और जान सकते हैं।

आप ऊपर वर्णित उन libraries में से प्रत्येक के बारे में उनके links में और भी पढ़ सकते हैं।
