# GraphQL { #graphql }

Оскільки FastAPI базується на стандарті ASGI, дуже просто інтегрувати будь-яку бібліотеку GraphQL, сумісну з ASGI.

Ви можете поєднувати звичайні *операції шляху* FastAPI з GraphQL в одному застосунку.

/// tip | Порада

GraphQL розв’язує деякі дуже специфічні сценарії використання.

Порівняно зі звичайними веб-API він має переваги та недоліки.

Переконайтеся, що переваги для вашого випадку використання переважають недоліки. 🤓

///

## Бібліотеки GraphQL { #graphql-libraries }

Ось деякі бібліотеки GraphQL з підтримкою ASGI. Ви можете використовувати їх із FastAPI:

* [Strawberry](https://strawberry.rocks/) 🍓
    * З [документацією для FastAPI](https://strawberry.rocks/docs/integrations/fastapi)
* [Ariadne](https://ariadnegraphql.org/)
    * З [документацією для FastAPI](https://ariadnegraphql.org/docs/fastapi-integration)
* [Tartiflette](https://tartiflette.io/)
    * З [Tartiflette ASGI](https://tartiflette.github.io/tartiflette-asgi/) для інтеграції з ASGI
* [Graphene](https://graphene-python.org/)
    * З [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3)

## GraphQL зі Strawberry { #graphql-with-strawberry }

Якщо вам потрібен або ви хочете використовувати GraphQL, [Strawberry](https://strawberry.rocks/) - рекомендована бібліотека, адже її дизайн найближчий до дизайну FastAPI; усе базується на анотаціях типів.

Залежно від вашого сценарію використання ви можете надати перевагу іншій бібліотеці, але якби ви запитали мене, я, ймовірно, порадив би спробувати Strawberry.

Ось невеликий приклад того, як інтегрувати Strawberry з FastAPI:

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

Більше про Strawberry ви можете дізнатися в [документації Strawberry](https://strawberry.rocks/).

І також [документацію про Strawberry з FastAPI](https://strawberry.rocks/docs/integrations/fastapi).

## Застарілий `GraphQLApp` зі Starlette { #older-graphqlapp-from-starlette }

Попередні версії Starlette містили клас `GraphQLApp` для інтеграції з [Graphene](https://graphene-python.org/).

Його вилучено з Starlette як застарілий, але якщо у вас є код, що його використовував, ви можете легко мігрувати на [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3), який покриває той самий сценарій використання та має майже ідентичний інтерфейс.

/// tip | Порада

Якщо вам потрібен GraphQL, я все ж рекомендую звернути увагу на [Strawberry](https://strawberry.rocks/), адже він базується на анотаціях типів, а не на власних класах і типах.

///

## Дізнайтеся більше { #learn-more }

Ви можете дізнатися більше про GraphQL в [офіційній документації GraphQL](https://graphql.org/).

Також ви можете почитати більше про кожну з цих бібліотек за наведеними посиланнями.
