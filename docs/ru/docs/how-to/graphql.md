# GraphQL

Так как **FastAPI** основан на стандарте **ASGI**, интегрировать любую библиотеку **GraphQL**, совместимую с ASGI, очень просто.

Вы можете комбинировать обычные *маршруты* FastAPI с GraphQL в одном приложении.

/// tip | Совет

**GraphQL** решает некоторые очень специфичные случаи использования.

Он имеет **преимущества** и **недостатки** по сравнению с обычными **веб API**.

Убедитесь, что вы оценили, компенсируют ли **преимущества** для вашего случая использования **недостатки**. 🤓

///

## Библиотеки GraphQL

Вот некоторые из библиотек **GraphQL**, которые поддерживают **ASGI**. Вы можете использовать их с **FastAPI**:

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * С <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">документацией по FastAPI</a>
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * С <a href="https://ariadnegraphql.org/docs/fastapi-integration" class="external-link" target="_blank">документацией по FastAPI</a>
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * С <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> для интеграции с ASGI
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * С <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>

## GraphQL с Strawberry

Если вам нужно или вы хотите работать с **GraphQL**, <a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a> — это **рекомендуемая** библиотека, так как она имеет дизайн, близкий к дизайну **FastAPI**, и основана на **аннотациях типов**.

В зависимости от вашего случая использования, вы можете предпочесть другую библиотеку, но если спросите меня, я скорее всего предложу вам попробовать **Strawberry**.

Вот небольшой пример того, как вы можете интегрировать Strawberry с FastAPI:

{* ../../docs_src/graphql/tutorial001.py hl[3,22,25] *}

Вы можете узнать больше о Strawberry в <a href="https://strawberry.rocks/" class="external-link" target="_blank">документации Strawberry</a>.

Также обратите внимание на документацию о <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">Strawberry с FastAPI</a>.

## Более старая `GraphQLApp` из Starlette

Предыдущие версии Starlette включали класс `GraphQLApp` для интеграции с <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>.

Он был исключен из Starlette, но если у вас есть код, который его использует, вы можете легко **мигрировать** на <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>, которая охватывает тот же случай использования и имеет **почти идентичный интерфейс**.

/// tip | Совет

Если вам нужен GraphQL, я все же рекомендую вам обратить внимание на <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>, так как он основан на аннотациях типов, а не на пользовательских классах и типах.

///

## Узнать больше

Вы можете узнать больше о **GraphQL** в <a href="https://graphql.org/" class="external-link" target="_blank">официальной документации GraphQL</a>.

Вы также можете прочитать больше о каждой из упомянутых выше библиотек по предоставленным ссылкам.
