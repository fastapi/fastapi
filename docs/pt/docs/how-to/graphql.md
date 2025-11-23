# GraphQL { #graphql }

Como o **FastAPI** é baseado no padrão **ASGI**, é muito fácil integrar qualquer biblioteca **GraphQL** também compatível com ASGI.

Você pode combinar *operações de rota* normais do FastAPI com GraphQL na mesma aplicação.

/// tip | Dica

**GraphQL** resolve alguns casos de uso muito específicos.

Ele tem **vantagens** e **desvantagens** quando comparado a **web APIs** comuns.

Certifique-se de avaliar se os **benefícios** para o seu caso de uso compensam as **desvantagens**. 🤓

///

## Bibliotecas GraphQL { #graphql-libraries }

Aqui estão algumas das bibliotecas **GraphQL** que têm suporte **ASGI**. Você pode usá-las com **FastAPI**:

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * Com <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">docs para FastAPI</a>
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * Com <a href="https://ariadnegraphql.org/docs/fastapi-integration" class="external-link" target="_blank">docs para FastAPI</a>
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * Com <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> para fornecer integração ASGI
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * Com <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>

## GraphQL com Strawberry { #graphql-with-strawberry }

Se você precisar ou quiser trabalhar com **GraphQL**, <a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a> é a biblioteca **recomendada** pois tem o design mais próximo ao design do **FastAPI**, ela é toda baseada em **anotações de tipo**.

Dependendo do seu caso de uso, você pode preferir usar uma biblioteca diferente, mas se você me perguntasse, eu provavelmente sugeriria que você experimentasse o **Strawberry**.

Aqui está uma pequena prévia de como você poderia integrar Strawberry com FastAPI:

{* ../../docs_src/graphql/tutorial001.py hl[3,22,25] *}

Você pode aprender mais sobre Strawberry na <a href="https://strawberry.rocks/" class="external-link" target="_blank">documentação do Strawberry</a>.

E também na documentação sobre <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">Strawberry com FastAPI</a>.

## Antigo `GraphQLApp` do Starlette { #older-graphqlapp-from-starlette }

Versões anteriores do Starlette incluiam uma classe `GraphQLApp` para integrar com <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>.

Ela foi descontinuada do Starlette, mas se você tem código que a utilizava, você pode facilmente **migrar** para <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>, que cobre o mesmo caso de uso e tem uma **interface quase idêntica**.

/// tip | Dica

Se você precisa de GraphQL, eu ainda recomendaria que você desse uma olhada no <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>, pois ele é baseado em anotações de tipo em vez de classes e tipos personalizados.

///

## Saiba Mais { #learn-more }

Você pode aprender mais sobre **GraphQL** na <a href="https://graphql.org/" class="external-link" target="_blank">documentação oficial do GraphQL</a>.

Você também pode ler mais sobre cada uma das bibliotecas descritas acima em seus links.
