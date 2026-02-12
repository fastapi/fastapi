# Histoire, conception et avenir

Il y a quelque temps, <a href="https://github.com/fastapi/fastapi/issues/3#issuecomment-454956920" class="external-link" target="_blank">un utilisateur de **FastAPI** a demandé</a> :

> Quelle est l'histoire de ce projet ? Il semble être sorti de nulle part et est devenu génial en quelques semaines [...].

Voici un petit bout de cette histoire.

## Alternatives

Je crée des API avec des exigences complexes depuis plusieurs années (Machine Learning, systèmes distribués, jobs asynchrones, bases de données NoSQL, etc), en dirigeant plusieurs équipes de développeurs.

Dans ce cadre, j'ai dû étudier, tester et utiliser de nombreuses alternatives.

L'histoire de **FastAPI** est en grande partie l'histoire de ses prédécesseurs.

Comme dit dans la section [Alternatives](alternatives.md){.internal-link target=\_blank} :

<blockquote markdown="1">

**FastAPI** n'existerait pas sans le travail antérieur d'autres personnes.

Il y a eu de nombreux outils créés auparavant qui ont contribué à inspirer sa création.

J'ai évité la création d'un nouveau framework pendant plusieurs années. J'ai d'abord essayé de résoudre toutes les fonctionnalités couvertes par **FastAPI** en utilisant de nombreux frameworks, plug-ins et outils différents.

Mais à un moment donné, il n'y avait pas d'autre option que de créer quelque chose qui offre toutes ces fonctionnalités, en prenant les meilleures idées des outils précédents, et en les combinant de la meilleure façon possible, en utilisant des fonctionnalités du langage qui n'étaient même pas disponibles auparavant (annotations de type pour Python 3.6+).

</blockquote>

## Recherche

En utilisant toutes les alternatives précédentes, j'ai eu la chance d'apprendre de toutes, de prendre des idées, et de les combiner de la meilleure façon que j'ai pu trouver pour moi-même et les équipes de développeurs avec lesquelles j'ai travaillé.

Par exemple, il était clair que l'idéal était de se baser sur les annotations de type Python standard.

De plus, la meilleure approche était d'utiliser des normes déjà existantes.

Ainsi, avant même de commencer à coder **FastAPI**, j'ai passé plusieurs mois à étudier les spécifications d'OpenAPI, JSON Schema, OAuth2, etc. Comprendre leurs relations, leurs similarités et leurs différences.

## Conception

Ensuite, j'ai passé du temps à concevoir l'"API" de développeur que je voulais avoir en tant qu'utilisateur (en tant que développeur utilisant FastAPI).

J'ai testé plusieurs idées dans les éditeurs Python les plus populaires : PyCharm, VS Code, les éditeurs basés sur Jedi.

D'après la dernière <a href="https://www.jetbrains.com/research/python-developers-survey-2018/#development-tools" class="external-link" target="_blank">Enquête Développeurs Python</a>, cela couvre environ 80% des utilisateurs.

Cela signifie que **FastAPI** a été spécifiquement testé avec les éditeurs utilisés par 80% des développeurs Python. Et comme la plupart des autres éditeurs ont tendance à fonctionner de façon similaire, tous ses avantages devraient fonctionner pour pratiquement tous les éditeurs.

Ainsi, j'ai pu trouver les meilleurs moyens de réduire autant que possible la duplication du code, d'avoir la complétion partout, les contrôles de type et d'erreur, etc.

Le tout de manière à offrir la meilleure expérience de développement à tous les développeurs.

## Exigences

Après avoir testé plusieurs alternatives, j'ai décidé que j'allais utiliser <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">**Pydantic**</a> pour ses avantages.

J'y ai ensuite contribué, pour le rendre entièrement compatible avec JSON Schema, pour supporter différentes manières de définir les déclarations de contraintes, et pour améliorer le support des éditeurs (vérifications de type, autocomplétion) sur la base des tests effectués dans plusieurs éditeurs.

Pendant le développement, j'ai également contribué à <a href="https://www.starlette.dev/" class="external-link" target="_blank">**Starlette**</a>, l'autre exigence clé.

## Développement

Au moment où j'ai commencé à créer **FastAPI** lui-même, la plupart des pièces étaient déjà en place, la conception était définie, les exigences et les outils étaient prêts, et la connaissance des normes et des spécifications était claire et fraîche.

## Futur

À ce stade, il est déjà clair que **FastAPI** et ses idées sont utiles pour de nombreuses personnes.

Elle a été préférée aux solutions précédentes parce qu'elle convient mieux à de nombreux cas d'utilisation.

De nombreux développeurs et équipes dépendent déjà de **FastAPI** pour leurs projets (y compris moi et mon équipe).

Mais il y a encore de nombreuses améliorations et fonctionnalités à venir.

**FastAPI** a un grand avenir devant lui.

Et [votre aide](help-fastapi.md){.internal-link target=\_blank} est grandement appréciée.
