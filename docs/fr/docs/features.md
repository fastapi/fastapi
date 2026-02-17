# Fonctionnalités { #features }

## Fonctionnalités de FastAPI { #fastapi-features }

**FastAPI** vous offre les éléments suivants :

### Basé sur des standards ouverts { #based-on-open-standards }

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> pour la création d'API, incluant la déclaration de <dfn title="aussi connu comme : endpoints, routes">chemin</dfn> <dfn title="aussi connu comme méthodes HTTP, comme POST, GET, PUT, DELETE">opérations</dfn>, paramètres, corps de requêtes, sécurité, etc.
* Documentation automatique des modèles de données avec <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (puisque OpenAPI est lui-même basé sur JSON Schema).
* Conçu autour de ces standards, après une étude méticuleuse. Plutôt qu'une couche ajoutée après coup.
* Cela permet également d'utiliser la **génération automatique de code client** dans de nombreux langages.

### Documentation automatique { #automatic-docs }

Documentation d'API interactive et interfaces web d'exploration. Comme le framework est basé sur OpenAPI, plusieurs options existent, 2 incluses par défaut.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, avec exploration interactive, appelez et testez votre API directement depuis le navigateur.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Documentation d'API alternative avec <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Uniquement du Python moderne { #just-modern-python }

Tout est basé sur les déclarations de **types Python** standard (grâce à Pydantic). Aucune nouvelle syntaxe à apprendre. Juste du Python moderne standard.

Si vous avez besoin d'un rappel de 2 minutes sur l'utilisation des types en Python (même si vous n'utilisez pas FastAPI), consultez le court tutoriel : [Types Python](python-types.md){.internal-link target=_blank}.

Vous écrivez du Python standard avec des types :

```Python
from datetime import date

from pydantic import BaseModel

# Déclarez une variable comme étant une str
# et profitez de l'aide de l'éditeur dans cette fonction
def main(user_id: str):
    return user_id


# Un modèle Pydantic
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Qui peuvent ensuite être utilisés comme ceci :

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

/// info

`**second_user_data` signifie :

Passez les clés et valeurs du dictionnaire `second_user_data` directement comme arguments clé-valeur, équivalent à : `User(id=4, name="Mary", joined="2018-11-30")`

///

### Support des éditeurs { #editor-support }

Tout le framework a été conçu pour être facile et intuitif à utiliser, toutes les décisions ont été testées sur plusieurs éditeurs avant même de commencer le développement, pour assurer la meilleure expérience de développement.

Dans les enquêtes auprès des développeurs Python, il est clair <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">que l’une des fonctionnalités les plus utilisées est « autocomplétion »</a>.

L'ensemble du framework **FastAPI** est conçu pour satisfaire cela. L'autocomplétion fonctionne partout.

Vous aurez rarement besoin de revenir aux documents.

Voici comment votre éditeur peut vous aider :

* dans <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a> :

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* dans <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> :

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Vous obtiendrez de l'autocomplétion dans du code que vous auriez pu considérer impossible auparavant. Par exemple, la clé `price` à l'intérieur d'un corps JSON (qui aurait pu être imbriqué) provenant d'une requête.

Fini de taper des noms de clés erronés, de faire des allers-retours entre les documents, ou de faire défiler vers le haut et vers le bas pour savoir si vous avez finalement utilisé `username` ou `user_name`.

### Court { #short }

Des **valeurs par défaut** sensées pour tout, avec des configurations optionnelles partout. Tous les paramètres peuvent être ajustés finement pour faire ce dont vous avez besoin et définir l'API dont vous avez besoin.

Mais par défaut, tout **« just works »**.

### Validation { #validation }

* Validation pour la plupart (ou tous ?) des **types de données** Python, y compris :
    * objets JSON (`dict`).
    * tableaux JSON (`list`) définissant les types d'éléments.
    * champs String (`str`), définition des longueurs minimale et maximale.
    * nombres (`int`, `float`) avec valeurs minimale et maximale, etc.

* Validation pour des types plus exotiques, comme :
    * URL.
    * Email.
    * UUID.
    * ... et autres.

Toutes les validations sont gérées par le **Pydantic** bien établi et robuste.

### Sécurité et authentification { #security-and-authentication }

Sécurité et authentification intégrées. Sans aucun compromis avec les bases de données ou les modèles de données.

Tous les schémas de sécurité définis dans OpenAPI, y compris :

* HTTP Basic.
* **OAuth2** (également avec des **tokens JWT**). Consultez le tutoriel [OAuth2 avec JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* Clés d'API dans :
    * les en-têtes.
    * les paramètres de requête.
    * les cookies, etc.

Plus toutes les fonctionnalités de sécurité de Starlette (y compris les **cookies de session**).

Le tout construit comme des outils et composants réutilisables, faciles à intégrer à vos systèmes, magasins de données, bases de données relationnelles et NoSQL, etc.

### Injection de dépendances { #dependency-injection }

FastAPI inclut un système d’<dfn title='aussi connu sous le nom de « composants », « ressources », « services », « fournisseurs »'><strong>Injection de dépendances</strong></dfn> extrêmement simple à utiliser, mais extrêmement puissant.

* Même les dépendances peuvent avoir des dépendances, créant une hiérarchie ou un **« graphe » de dépendances**.
* Le tout **géré automatiquement** par le framework.
* Toutes les dépendances peuvent exiger des données des requêtes et **augmenter les contraintes du chemin d'accès** ainsi que la documentation automatique.
* **Validation automatique** même pour les paramètres de *chemin d'accès* définis dans les dépendances.
* Prise en charge des systèmes d'authentification d'utilisateurs complexes, des **connexions de base de données**, etc.
* **Aucun compromis** avec les bases de données, les frontends, etc. Mais une intégration facile avec tous.

### « Plug-ins » illimités { #unlimited-plug-ins }

Ou, autrement dit, pas besoin d'eux, importez et utilisez le code dont vous avez besoin.

Toute intégration est conçue pour être si simple à utiliser (avec des dépendances) que vous pouvez créer un « plug-in » pour votre application en 2 lignes de code en utilisant la même structure et la même syntaxe que pour vos *chemins d'accès*.

### Testé { #tested }

* 100 % de <dfn title="La quantité de code testée automatiquement">couverture de test</dfn>.
* 100 % de base de code <dfn title="Annotations de type Python ; avec cela votre éditeur et les outils externes peuvent vous offrir un meilleur support">annotée avec des types</dfn>.
* Utilisé dans des applications en production.

## Fonctionnalités de Starlette { #starlette-features }

**FastAPI** est entièrement compatible avec (et basé sur) <a href="https://www.starlette.dev/" class="external-link" target="_blank"><strong>Starlette</strong></a>. Donc, tout code Starlette additionnel que vous avez fonctionnera aussi.

`FastAPI` est en fait une sous-classe de `Starlette`. Ainsi, si vous connaissez ou utilisez déjà Starlette, la plupart des fonctionnalités fonctionneront de la même manière.

Avec **FastAPI** vous obtenez toutes les fonctionnalités de **Starlette** (puisque FastAPI est juste Starlette sous stéroïdes) :

* Des performances vraiment impressionnantes. C'est <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">l’un des frameworks Python les plus rapides disponibles, à l’égal de **NodeJS** et **Go**</a>.
* Prise en charge des **WebSocket**.
* Tâches d'arrière-plan dans le processus.
* Évènements de démarrage et d'arrêt.
* Client de test basé sur HTTPX.
* **CORS**, GZip, fichiers statiques, réponses en streaming.
* Prise en charge des **Sessions et Cookies**.
* Couverture de test à 100 %.
* Base de code annotée à 100 % avec des types.

## Fonctionnalités de Pydantic { #pydantic-features }

**FastAPI** est entièrement compatible avec (et basé sur) <a href="https://docs.pydantic.dev/" class="external-link" target="_blank"><strong>Pydantic</strong></a>. Donc, tout code Pydantic additionnel que vous avez fonctionnera aussi.

Y compris des bibliothèques externes également basées sur Pydantic, servant d’<abbr title="Object-Relational Mapper - Mappeur objet-relationnel">ORM</abbr>, d’<abbr title="Object-Document Mapper - Mappeur objet-document">ODM</abbr> pour les bases de données.

Cela signifie également que, dans de nombreux cas, vous pouvez passer l'objet que vous recevez d'une requête **directement à la base de données**, puisque tout est validé automatiquement.

L’inverse est également vrai, dans de nombreux cas, vous pouvez simplement passer l'objet que vous récupérez de la base de données **directement au client**.

Avec **FastAPI** vous obtenez toutes les fonctionnalités de **Pydantic** (puisque FastAPI est basé sur Pydantic pour toute la gestion des données) :

* **Pas de prise de tête** :
    * Pas de micro-langage de définition de schéma à apprendre.
    * Si vous connaissez les types Python vous savez utiliser Pydantic.
* Fonctionne bien avec votre **<abbr title="Integrated Development Environment - Environnement de développement intégré: similaire à un éditeur de code">IDE</abbr>/<dfn title="Programme qui vérifie les erreurs de code">linter</dfn>/cerveau** :
    * Parce que les structures de données de Pydantic sont simplement des instances de classes que vous définissez ; l'autocomplétion, le linting, mypy et votre intuition devraient tous bien fonctionner avec vos données validées.
* Valider des **structures complexes** :
    * Utilisation de modèles Pydantic hiérarchiques, de `List` et `Dict` du `typing` Python, etc.
    * Et les validateurs permettent de définir, vérifier et documenter clairement et facilement des schémas de données complexes en tant que JSON Schema.
    * Vous pouvez avoir des objets **JSON fortement imbriqués** et les faire tous valider et annoter.
* **Extensible** :
    * Pydantic permet de définir des types de données personnalisés ou vous pouvez étendre la validation avec des méthodes sur un modèle décoré avec le décorateur de validation.
* Couverture de test à 100 %.
