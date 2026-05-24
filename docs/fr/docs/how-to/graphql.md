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

* [Strawberry](https://strawberry.rocks/) 🍓
    * Avec [la documentation pour FastAPI](https://strawberry.rocks/docs/integrations/fastapi)
* [Ariadne](https://ariadnegraphql.org/)
    * Avec [la documentation pour FastAPI](https://ariadnegraphql.org/docs/fastapi-integration)
* [Tartiflette](https://tartiflette.io/)
    * Avec [Tartiflette ASGI](https://tartiflette.github.io/tartiflette-asgi/) pour fournir l'intégration ASGI
* [Graphene](https://graphene-python.org/)
    * Avec [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3)

## GraphQL avec Strawberry { #graphql-with-strawberry }

Si vous avez besoin ou souhaitez travailler avec **GraphQL**, [**Strawberry**](https://strawberry.rocks/) est la bibliothèque **recommandée** car sa conception est la plus proche de celle de **FastAPI**, tout est basé sur des **annotations de type**.

Selon votre cas d'utilisation, vous pourriez préférer une autre bibliothèque, mais si vous me le demandiez, je vous suggérerais probablement d'essayer **Strawberry**.

Voici un petit aperçu de la manière dont vous pouvez intégrer Strawberry avec FastAPI :

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

Vous pouvez en apprendre davantage sur Strawberry dans la [documentation de Strawberry](https://strawberry.rocks/).

Et également la documentation sur [Strawberry avec FastAPI](https://strawberry.rocks/docs/integrations/fastapi).

## Ancien `GraphQLApp` de Starlette { #older-graphqlapp-from-starlette }

Les versions précédentes de Starlette incluaient une classe `GraphQLApp` pour s'intégrer à [Graphene](https://graphene-python.org/).

Elle a été dépréciée dans Starlette, mais si vous avez du code qui l'utilisait, vous pouvez facilement **migrer** vers [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3), qui couvre le même cas d'utilisation et propose une **interface presque identique**.

/// tip | Astuce

Si vous avez besoin de GraphQL, je vous recommande tout de même de regarder [Strawberry](https://strawberry.rocks/), car il est basé sur des annotations de type plutôt que sur des classes et types personnalisés.

///

## En savoir plus { #learn-more }

Vous pouvez en apprendre davantage sur **GraphQL** dans la [documentation officielle de GraphQL](https://graphql.org/).

Vous pouvez également en lire davantage sur chacune des bibliothèques décrites ci-dessus via leurs liens.
