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

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * З <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">документацією для FastAPI</a>
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * З <a href="https://ariadnegraphql.org/docs/fastapi-integration" class="external-link" target="_blank">документацією для FastAPI</a>
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * З <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> для інтеграції з ASGI
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * З <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>

## GraphQL зі Strawberry { #graphql-with-strawberry }

Якщо вам потрібен або ви хочете використовувати GraphQL, <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> - рекомендована бібліотека, адже її дизайн найближчий до дизайну FastAPI; усе базується на анотаціях типів.

Залежно від вашого сценарію використання ви можете надати перевагу іншій бібліотеці, але якби ви запитали мене, я, ймовірно, порадив би спробувати Strawberry.

Ось невеликий приклад того, як інтегрувати Strawberry з FastAPI:

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

Більше про Strawberry ви можете дізнатися в <a href="https://strawberry.rocks/" class="external-link" target="_blank">документації Strawberry</a>.

І також <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">документацію про Strawberry з FastAPI</a>.

## Застарілий `GraphQLApp` зі Starlette { #older-graphqlapp-from-starlette }

Попередні версії Starlette містили клас `GraphQLApp` для інтеграції з <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>.

Його вилучено з Starlette як застарілий, але якщо у вас є код, що його використовував, ви можете легко мігрувати на <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>, який покриває той самий сценарій використання та має майже ідентичний інтерфейс.

/// tip | Порада

Якщо вам потрібен GraphQL, я все ж рекомендую звернути увагу на <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>, адже він базується на анотаціях типів, а не на власних класах і типах.

///

## Дізнайтеся більше { #learn-more }

Ви можете дізнатися більше про GraphQL в <a href="https://graphql.org/" class="external-link" target="_blank">офіційній документації GraphQL</a>.

Також ви можете почитати більше про кожну з цих бібліотек за наведеними посиланнями.
