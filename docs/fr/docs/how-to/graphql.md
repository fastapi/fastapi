# GraphQL { #graphql }

Comme **FastAPI** est basé sur la norme **ASGI**, il est très facile d'intégrer toute bibliothèque **GraphQL** également compatible avec ASGI.

Vous pouvez combiner des *chemins d'accès* FastAPI classiques avec GraphQL dans la même application.

/// tip | Astuce

**GraphQL** résout des cas d'utilisation très spécifiques.

Il présente des **avantages** et des **inconvénients** par rapport aux **API web** classiques.

Assurez-vous d'évaluer si les **bénéfices** pour votre cas d'utilisation compensent les **inconvénients**. 🤓

///

## Bibliothèques GraphQL { #graphql-libraries }

Voici quelques bibliothèques **GraphQL** qui prennent en charge **ASGI**. Vous pouvez les utiliser avec **FastAPI** :

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * Avec <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">la documentation pour FastAPI</a>
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * Avec <a href="https://ariadnegraphql.org/docs/fastapi-integration" class="external-link" target="_blank">la documentation pour FastAPI</a>
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * Avec <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> pour fournir l'intégration ASGI
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * Avec <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>

## GraphQL avec Strawberry { #graphql-with-strawberry }

Si vous avez besoin ou souhaitez travailler avec **GraphQL**, <a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a> est la bibliothèque **recommandée** car sa conception est la plus proche de celle de **FastAPI**, tout est basé sur des **annotations de type**.

Selon votre cas d'utilisation, vous pourriez préférer une autre bibliothèque, mais si vous me le demandiez, je vous suggérerais probablement d'essayer **Strawberry**.

Voici un petit aperçu de la manière dont vous pouvez intégrer Strawberry avec FastAPI :

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

Vous pouvez en apprendre davantage sur Strawberry dans la <a href="https://strawberry.rocks/" class="external-link" target="_blank">documentation de Strawberry</a>.

Et également la documentation sur <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">Strawberry avec FastAPI</a>.

## Ancien `GraphQLApp` de Starlette { #older-graphqlapp-from-starlette }

Les versions précédentes de Starlette incluaient une classe `GraphQLApp` pour s'intégrer à <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>.

Elle a été dépréciée dans Starlette, mais si vous avez du code qui l'utilisait, vous pouvez facilement **migrer** vers <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>, qui couvre le même cas d'utilisation et propose une **interface presque identique**.

/// tip | Astuce

Si vous avez besoin de GraphQL, je vous recommande tout de même de regarder <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>, car il est basé sur des annotations de type plutôt que sur des classes et types personnalisés.

///

## En savoir plus { #learn-more }

Vous pouvez en apprendre davantage sur **GraphQL** dans la <a href="https://graphql.org/" class="external-link" target="_blank">documentation officielle de GraphQL</a>.

Vous pouvez également en lire davantage sur chacune des bibliothèques décrites ci-dessus via leurs liens.
