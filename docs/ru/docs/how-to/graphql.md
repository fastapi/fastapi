# GraphQL { #graphql }

Так как **FastAPI** основан на стандарте **ASGI**, очень легко интегрировать любую библиотеку **GraphQL**, также совместимую с ASGI.

Вы можете комбинировать обычные *операции пути* FastAPI с GraphQL в одном приложении.

/// tip | Совет

**GraphQL** решает некоторые очень специфические задачи.

У него есть как **преимущества**, так и **недостатки** по сравнению с обычными **веб-API**.

Убедитесь, что **выгоды** для вашего случая использования перевешивают **недостатки**. 🤓

///

## Библиотеки GraphQL { #graphql-libraries }

Ниже приведены некоторые библиотеки **GraphQL** с поддержкой **ASGI**. Их можно использовать с **FastAPI**:

* [Strawberry](https://strawberry.rocks/) 🍓
    * С [документацией для FastAPI](https://strawberry.rocks/docs/integrations/fastapi)
* [Ariadne](https://ariadnegraphql.org/)
    * С [документацией для FastAPI](https://ariadnegraphql.org/docs/fastapi-integration)
* [Tartiflette](https://tartiflette.io/)
    * С [Tartiflette ASGI](https://tartiflette.github.io/tartiflette-asgi/) для интеграции с ASGI
* [Graphene](https://graphene-python.org/)
    * С [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3)

## GraphQL со Strawberry { #graphql-with-strawberry }

Если вам нужно или хочется работать с **GraphQL**, [**Strawberry**](https://strawberry.rocks/) — **рекомендуемая** библиотека, так как её дизайн ближе всего к дизайну **FastAPI**, всё основано на **аннотациях типов**.

В зависимости от вашего сценария использования вы можете предпочесть другую библиотеку, но если бы вы спросили меня, я, скорее всего, предложил бы попробовать **Strawberry**.

Вот небольшой пример того, как можно интегрировать Strawberry с FastAPI:

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

Подробнее о Strawberry можно узнать в [документации Strawberry](https://strawberry.rocks/).

А также в документации по [интеграции Strawberry с FastAPI](https://strawberry.rocks/docs/integrations/fastapi).

## Устаревший `GraphQLApp` из Starlette { #older-graphqlapp-from-starlette }

В предыдущих версиях Starlette был класс `GraphQLApp` для интеграции с [Graphene](https://graphene-python.org/).

Он был объявлен устаревшим в Starlette, но если у вас есть код, который его использовал, вы можете легко **мигрировать** на [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3), который решает ту же задачу и имеет **почти идентичный интерфейс**.

/// tip | Совет

Если вам нужен GraphQL, я всё же рекомендую посмотреть [Strawberry](https://strawberry.rocks/), так как он основан на аннотациях типов, а не на пользовательских классах и типах.

///

## Подробнее { #learn-more }

Подробнее о **GraphQL** вы можете узнать в [официальной документации GraphQL](https://graphql.org/).

Также можно почитать больше о каждой из указанных выше библиотек по приведённым ссылкам.
