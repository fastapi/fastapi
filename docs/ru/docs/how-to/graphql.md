# GraphQL

Так как **FastAPI** основан на стандарте **ASGI**, очень легко интегрировать любую библиотеку **GraphQL**, также совместимую с ASGI.

Вы можете комбинировать обычные *операции пути* FastAPI с GraphQL в одном и том же приложении.

/// tip | Совет

**GraphQL** решает некоторые очень специфические случаи использования.

У него есть **преимущества** и **недостатки** по сравнению с обычными **веб API**.

Убедитесь, что вы оценили, компенсируют ли **выгоды** для вашего случая использования **недостатки**. 🤓

///

## Библиотеки GraphQL

Вот некоторые из библиотек **GraphQL**, которые поддерживают **ASGI**. Вы можете использовать их с **FastAPI**:

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * С <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">документацией для FastAPI</a>
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * С <a href="https://ariadnegraphql.org/docs/fastapi-integration" class="external-link" target="_blank">документацией для FastAPI</a>
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * С <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> для обеспечения интеграции с ASGI
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * С <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>

## GraphQL с использованием Strawberry

Если вам нужно или вы хотите работать с **GraphQL**, библиотека <a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a> является **рекомендуемой**, так как ее дизайн наиболее близок к дизайну **FastAPI**, и всё основано на **аннотациях типов**.

В зависимости от вашего случая использования, вы можете предпочесть другую библиотеку, но если бы вы спросили меня, я бы, вероятно, предложил попробовать **Strawberry**.

Вот небольшой пример того, как можно интегрировать Strawberry с FastAPI:

{* ../../docs_src/graphql/tutorial001.py hl[3,22,25] *}

Вы можете узнать больше о Strawberry в <a href="https://strawberry.rocks/" class="external-link" target="_blank">документации Strawberry</a>.

А также документацию о <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">Strawberry с FastAPI</a>.

## Устаревший `GraphQLApp` от Starlette

В предыдущих версиях Starlette включалась класс `GraphQLApp` для интеграции с <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>.

Он был исключен из Starlette, но если у вас есть код, который использует его, вы можете легко **мигрировать** на <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>, который покрывает тот же случай использования и имеет **почти идентичный интерфейс**.

/// tip | Совет

Если вам нужен GraphQL, я всё же рекомендую обратить внимание на <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>, так как он основан на аннотациях типов, а не на кастомных классах и типах.

///

## Узнать больше

Вы можете узнать больше о **GraphQL** в <a href="https://graphql.org/" class="external-link" target="_blank">официальной документации GraphQL</a>.

Также вы можете прочитать больше о каждой из описанных выше библиотек по предоставленным ссылкам.
