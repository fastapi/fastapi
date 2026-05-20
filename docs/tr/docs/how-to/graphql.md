# GraphQL { #graphql }

**FastAPI**, **ASGI** standardını temel aldığı için ASGI ile uyumlu herhangi bir **GraphQL** kütüphanesini entegre etmek oldukça kolaydır.

Aynı uygulama içinde normal FastAPI *path operation*'larını GraphQL ile birlikte kullanabilirsiniz.

/// tip | İpucu

**GraphQL** bazı çok özel kullanım senaryolarını çözer.

Yaygın **web API**'lerle karşılaştırıldığında **avantajları** ve **dezavantajları** vardır.

Kendi senaryonuz için **faydaların**, **olumsuz yönleri** telafi edip etmediğini mutlaka değerlendirin. 🤓

///

## GraphQL Kütüphaneleri { #graphql-libraries }

Aşağıda **ASGI** desteği olan bazı **GraphQL** kütüphaneleri var. Bunları **FastAPI** ile kullanabilirsiniz:

* [Strawberry](https://strawberry.rocks/) 🍓
    * [FastAPI dokümantasyonu](https://strawberry.rocks/docs/integrations/fastapi) ile
* [Ariadne](https://ariadnegraphql.org/)
    * [FastAPI dokümantasyonu](https://ariadnegraphql.org/docs/fastapi-integration) ile
* [Tartiflette](https://tartiflette.io/)
    * ASGI entegrasyonu sağlamak için [Tartiflette ASGI](https://tartiflette.github.io/tartiflette-asgi/) ile
* [Graphene](https://graphene-python.org/)
    * [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3) ile

## Strawberry ile GraphQL { #graphql-with-strawberry }

**GraphQL** ile çalışmanız gerekiyorsa ya da bunu istiyorsanız, [**Strawberry**](https://strawberry.rocks/) önerilen kütüphanedir; çünkü tasarımı **FastAPI**'nin tasarımına en yakındır ve her şey **type annotation**'lar üzerine kuruludur.

Kullanım senaryonuza göre farklı bir kütüphaneyi tercih edebilirsiniz; ancak bana sorarsanız muhtemelen **Strawberry**'yi denemenizi önerirdim.

Strawberry'yi FastAPI ile nasıl entegre edebileceğinize dair küçük bir ön izleme:

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

Strawberry hakkında daha fazlasını [Strawberry dokümantasyonunda](https://strawberry.rocks/) öğrenebilirsiniz.

Ayrıca [FastAPI ile Strawberry](https://strawberry.rocks/docs/integrations/fastapi) dokümanlarına da göz atın.

## Starlette'teki Eski `GraphQLApp` { #older-graphqlapp-from-starlette }

Starlette'in önceki sürümlerinde [Graphene](https://graphene-python.org/) ile entegrasyon için bir `GraphQLApp` sınıfı vardı.

Bu sınıf Starlette'te kullanımdan kaldırıldı (deprecated). Ancak bunu kullanan bir kodunuz varsa, aynı kullanım senaryosunu kapsayan ve **neredeyse aynı bir interface** sağlayan [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3)'e kolayca **migrate** edebilirsiniz.

/// tip | İpucu

GraphQL'e ihtiyacınız varsa, custom class ve type'lar yerine type annotation'lara dayandığı için yine de [Strawberry](https://strawberry.rocks/)'yi incelemenizi öneririm.

///

## Daha Fazlasını Öğrenin { #learn-more }

**GraphQL** hakkında daha fazlasını [resmi GraphQL dokümantasyonunda](https://graphql.org/) öğrenebilirsiniz.

Ayrıca yukarıda bahsedilen kütüphanelerin her biri hakkında, kendi bağlantılarından daha fazla bilgi okuyabilirsiniz.
