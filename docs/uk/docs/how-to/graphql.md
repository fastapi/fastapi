# GraphQL { #graphql }

Оскільки **FastAPI** базується на стандарті **ASGI**, дуже легко інтегрувати будь-яку бібліотеку **GraphQL**, яка також сумісна з ASGI.

Ви можете поєднувати звичайні FastAPI *операції шляху* з GraphQL в одному застосунку.

/// tip | Порада

**GraphQL** розв’язує деякі дуже специфічні випадки використання.

Він має **переваги** та **недоліки** порівняно зі звичними **web API**.

Переконайтеся, що ви оцінили, чи **переваги** для вашого випадку використання компенсують **недоліки**. 🤓

///

## Бібліотеки GraphQL { #graphql-libraries }

Ось деякі бібліотеки **GraphQL**, які мають підтримку **ASGI**. Ви можете використовувати їх із **FastAPI**:

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * З <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">документацією для FastAPI</a>
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * З <a href="https://ariadnegraphql.org/docs/fastapi-integration" class="external-link" target="_blank">документацією для FastAPI</a>
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * Із <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> для забезпечення інтеграції з ASGI
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * Із <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>

## GraphQL зі Strawberry { #graphql-with-strawberry }

Якщо вам потрібно або ви хочете працювати з **GraphQL**, <a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a> — **рекомендована** бібліотека, адже її дизайн найближчий до дизайну **FastAPI**: усе базується на **анотаціях типів**.

Залежно від вашого випадку використання, ви можете віддати перевагу іншій бібліотеці, але якби ви запитали мене, я б, імовірно, порадив вам спробувати **Strawberry**.

Ось невеликий приклад того, як ви можете інтегрувати Strawberry з FastAPI:

{* ../../docs_src/graphql_/tutorial001_py39.py hl[3,22,25] *}

Докладніше про Strawberry можна дізнатися в <a href="https://strawberry.rocks/" class="external-link" target="_blank">документації Strawberry</a>.

А також у документації про <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">Strawberry з FastAPI</a>.

## Старий `GraphQLApp` зі Starlette { #older-graphqlapp-from-starlette }

Попередні версії Starlette містили клас `GraphQLApp` для інтеграції з <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>.

Його позначили застарілим у Starlette, але якщо у вас є код, який його використовував, ви можете легко **мігрувати** на <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>, що покриває той самий випадок використання та має **майже ідентичний інтерфейс**.

/// tip | Порада

Якщо вам потрібен GraphQL, я все одно рекомендую вам звернути увагу на <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>, адже він базується на анотаціях типів, а не на власних класах і типах.

///

## Дізнатися більше { #learn-more }

Детальніше про **GraphQL** можна дізнатися в <a href="https://graphql.org/" class="external-link" target="_blank">офіційній документації GraphQL</a>.

Ви також можете прочитати більше про кожну з бібліотек, описаних вище, за наведеними посиланнями.
