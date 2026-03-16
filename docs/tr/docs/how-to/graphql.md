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

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">FastAPI dokümantasyonu</a> ile
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * <a href="https://ariadnegraphql.org/docs/fastapi-integration" class="external-link" target="_blank">FastAPI dokümantasyonu</a> ile
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * ASGI entegrasyonu sağlamak için <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> ile
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a> ile

## Strawberry ile GraphQL { #graphql-with-strawberry }

**GraphQL** ile çalışmanız gerekiyorsa ya da bunu istiyorsanız, <a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a> önerilen kütüphanedir; çünkü tasarımı **FastAPI**'nin tasarımına en yakındır ve her şey **type annotation**'lar üzerine kuruludur.

Kullanım senaryonuza göre farklı bir kütüphaneyi tercih edebilirsiniz; ancak bana sorarsanız muhtemelen **Strawberry**'yi denemenizi önerirdim.

Strawberry'yi FastAPI ile nasıl entegre edebileceğinize dair küçük bir ön izleme:

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

Strawberry hakkında daha fazlasını <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry dokümantasyonunda</a> öğrenebilirsiniz.

Ayrıca <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">FastAPI ile Strawberry</a> dokümanlarına da göz atın.

## Starlette'teki Eski `GraphQLApp` { #older-graphqlapp-from-starlette }

Starlette'in önceki sürümlerinde <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a> ile entegrasyon için bir `GraphQLApp` sınıfı vardı.

Bu sınıf Starlette'te kullanımdan kaldırıldı (deprecated). Ancak bunu kullanan bir kodunuz varsa, aynı kullanım senaryosunu kapsayan ve **neredeyse aynı bir interface** sağlayan <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>'e kolayca **migrate** edebilirsiniz.

/// tip | İpucu

GraphQL'e ihtiyacınız varsa, custom class ve type'lar yerine type annotation'lara dayandığı için yine de <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>'yi incelemenizi öneririm.

///

## Daha Fazlasını Öğrenin { #learn-more }

**GraphQL** hakkında daha fazlasını <a href="https://graphql.org/" class="external-link" target="_blank">resmi GraphQL dokümantasyonunda</a> öğrenebilirsiniz.

Ayrıca yukarıda bahsedilen kütüphanelerin her biri hakkında, kendi bağlantılarından daha fazla bilgi okuyabilirsiniz.
