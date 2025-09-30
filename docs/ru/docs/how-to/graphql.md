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

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * С <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">документацией для FastAPI</a>
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * С <a href="https://ariadnegraphql.org/docs/fastapi-integration" class="external-link" target="_blank">документацией для FastAPI</a>
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * С <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> для интеграции с ASGI
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * С <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>

## GraphQL со Strawberry { #graphql-with-strawberry }

Если вам нужно или хочется работать с **GraphQL**, <a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a> — **рекомендуемая** библиотека, так как её дизайн ближе всего к дизайну **FastAPI**, всё основано на **аннотациях типов**.

В зависимости от вашего сценария использования вы можете предпочесть другую библиотеку, но если бы вы спросили меня, я, скорее всего, предложил бы попробовать **Strawberry**.

Вот небольшой пример того, как можно интегрировать Strawberry с FastAPI:

{* ../../docs_src/graphql/tutorial001.py hl[3,22,25] *}

Подробнее о Strawberry можно узнать в <a href="https://strawberry.rocks/" class="external-link" target="_blank">документации Strawberry</a>.

А также в документации по <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">интеграции Strawberry с FastAPI</a>.

## Устаревший `GraphQLApp` из Starlette { #older-graphqlapp-from-starlette }

В предыдущих версиях Starlette был класс `GraphQLApp` для интеграции с <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>.

Он был объявлен устаревшим в Starlette, но если у вас есть код, который его использовал, вы можете легко **мигрировать** на <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>, который решает ту же задачу и имеет **почти идентичный интерфейс**.

/// tip | Совет

Если вам нужен GraphQL, я всё же рекомендую посмотреть <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>, так как он основан на аннотациях типов, а не на пользовательских классах и типах.

///

## Подробнее { #learn-more }

Подробнее о **GraphQL** вы можете узнать в <a href="https://graphql.org/" class="external-link" target="_blank">официальной документации GraphQL</a>.

Также можно почитать больше о каждой из указанных выше библиотек по приведённым ссылкам.
