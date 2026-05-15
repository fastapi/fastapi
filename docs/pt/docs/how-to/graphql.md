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

* [Strawberry](https://strawberry.rocks/) 🍓
    * Com [documentação para FastAPI](https://strawberry.rocks/docs/integrations/fastapi)
* [Ariadne](https://ariadnegraphql.org/)
    * Com [documentação para FastAPI](https://ariadnegraphql.org/docs/fastapi-integration)
* [Tartiflette](https://tartiflette.io/)
    * Com [Tartiflette ASGI](https://tartiflette.github.io/tartiflette-asgi/) para fornecer integração ASGI
* [Graphene](https://graphene-python.org/)
    * Com [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3)

## GraphQL com Strawberry { #graphql-with-strawberry }

Se você precisar ou quiser trabalhar com **GraphQL**, [**Strawberry**](https://strawberry.rocks/) é a biblioteca **recomendada** pois tem o design mais próximo ao design do **FastAPI**, ela é toda baseada em **anotações de tipo**.

Dependendo do seu caso de uso, você pode preferir usar uma biblioteca diferente, mas se você me perguntasse, eu provavelmente sugeriria que você experimentasse o **Strawberry**.

Aqui está uma pequena prévia de como você poderia integrar Strawberry com FastAPI:

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

Você pode aprender mais sobre Strawberry na [documentação do Strawberry](https://strawberry.rocks/).

E também na documentação sobre [Strawberry com FastAPI](https://strawberry.rocks/docs/integrations/fastapi).

## Antigo `GraphQLApp` do Starlette { #older-graphqlapp-from-starlette }

Versões anteriores do Starlette incluiam uma classe `GraphQLApp` para integrar com [Graphene](https://graphene-python.org/).

Ela foi descontinuada do Starlette, mas se você tem código que a utilizava, você pode facilmente **migrar** para [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3), que cobre o mesmo caso de uso e tem uma **interface quase idêntica**.

/// tip | Dica

Se você precisa de GraphQL, eu ainda recomendaria que você desse uma olhada no [Strawberry](https://strawberry.rocks/), pois ele é baseado em anotações de tipo em vez de classes e tipos personalizados.

///

## Saiba Mais { #learn-more }

Você pode aprender mais sobre **GraphQL** na [documentação oficial do GraphQL](https://graphql.org/).

Você também pode ler mais sobre cada uma das bibliotecas descritas acima em seus links.
