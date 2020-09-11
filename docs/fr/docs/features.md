# Fonctionnalités

## Fonctionnalités FastAPI

**FastAPI** vous offre les fonctionnalités suivantes :

### Basé sur des standards ouverts

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> pour la création d'API, inclus les déclarations de <abbr title="également connu sous le nom de : endpoints, routes">*path*</abbr> <abbr title="également connu sous le nom de méthodes HTTP : POST, GET, PUT, DELETE">*operations*</abbr>, paramètres, *body requests*, sécurité, etc.
* Génération de documentation automatique de modèles de données avec <a href="http://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (OpenAPI est lui-même basé sur JSON Schema).
* Designé autour de ces standards, après une méticuleuse analyse, plutôt que de couches rajoutées les unes après les autres après coup.
* Ceci permet également d'utiliser un **client de génération de code** automatique dans beaucoup de langages.

### Documentation Automatique

La documentation des API est interactive et son exploration se fait via des interfaces web.
Comme le framework est basé sur OpenAPI, de multiples possibilités s'offrent à vous pour interagir avec la documentation.
2 possibilités sont néammoins incluses par défaut.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, via une exploration interactive, vous permet d'appeler et de tester votre API directement à partir de votre navigateur.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Une documentation alternative existe également avec <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Juste du Python récent

Tout s'appuie sur les déclarations de **Python 3.6 type** (merci à Pydantic). Aucune nouvelle syntaxe à apprendre. Il suffit juste d'utiliser du Python standard dans une version récente.

Si vous avez besoin d'un petit rafraîchissement de 2 minutes sur comment utiliser les Python types (même si vous n'utilisez pas FastAPI), rendez-vous sur ce petit tutoriel : [Python Types](python-types.md){.internal-link target=_blank}.

Voici comment écrire du Python standard en utilisant les types :

```Python
from typing import List, Dict
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Cela peut être utilisé de la façon suivante :

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! info
    `**second_user_data` signifie :

    Passe les keys et values du dictionnaire `second_user_data` directement comme des arguments key-value.  
    Cela revient à faire : `User(id=4, name="Mary", joined="2018-11-30")`

### Support pour les éditeurs de code

Tout le framework a été designé pour être simple et intuitif à utiliser.  
Toutes les décisions ont été testées sur de nombreux éditeurs de code, et ce même parfois avant de commencer les développements, afin de fournir la meilleure expérience de développement possible.

Dans le dernier sondage 'Python Developer' il était clair <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">que la fonctionnalité la plus utilisée est "l'autocompletion"</a>.

La totalité du framework **FastAPI** est basée sur cette fonctionnalité. L'autocompletion fonctionne partout.

Vous aurez rarement besoin de revenir à vos documentations.

Voici comment votre éditeur de code peut vous aider :

* in <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* in <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

La completion de code apparait dans des parties ou vous ne soupçonniez même pas que cela était possible il y a peu.  
Par exemple, la `price` key à l'intérieur du JSON body (qui pourrait être imbriqué) provient d'une requête.

Plus d'erreur en tapant le mauvais nom de key, plus besoin de faire  des allers et retours avec la documentation, ou de scroller dans le code dans tous les sens pour finallement utiliser `username` ou `user_name`.

### Efficace

Il existe des comportements par **défaut** pour tout, avec des configurations optionnelles partout. Tous les paramètres peuvent être réglés 'aux petits oignons' pour faire ce dont vous avez besoin et pour définir les API dont vous avez besoin.

Mais par défaut, ça **fonctionne tout simplement !**.

### Validation

* Validation pour la plupart (ou tous?) les **data types** Python, comme par exemple :
    * JSON objects (`dict`).
    * JSON array (`list`) définissant des types d'item.
    * Les champs String (`str`) définissant des longueurs min et max.
    * Nombres (`int`, `float`) avec des valeurs min et max, etc.

* Validation de types plus exotiques comme par exemple :
    * URL.
    * Email.
    * UUID.
    * ...et bien d'autres.

L'ensemble des validations est effectué par le très connu et robuste **Pydantic**.

### Sécurité et authentification

La Sécurité et l'authentification sont intégrées. Aucun compromis avec les bases de données et les modèles de données.

Tous les schémas de sécurité sont définis dans OpenAPI, comme par exemple :

* HTTP Basic.
* **OAuth2** (également avec **JWT tokens**). Rendez-vous avec le tutoriel [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* API keys à tous les étages :
    * Headers.
    * Query parameters.
    * Cookies, etc.

Ajoutez à cela les fonctionnalités de sécurité de Starlette (comme par exemple les **session cookies**).

Toutes ces fonctionnalités sont contenues dans des outils et composents réutilisables qui sont simples à intégrer dans vos systèmes, stockage de données, bases de données relationnelles et NoSQL, etc.

### Injection de dépendances

FastAPI inclus un système extrèmement simple d'utilisation, mais aussi extrêmement puissant, d'<abbr title='également connu sous le nom de "components", "resources", "services", "providers"'><strong>Injection des dépendances</strong></abbr>.

* Même si les dépendances ont elles-même des dépendances, création d'une hiérarchie ou d'un **"graphe" des dépendances**.
* Tout est **automatiquement piloté** par le framework.
* Toutes les dépendances peuvent nécessiter des données en provenance de requêtes et générer des contraintes liées aux **path operation** ainsi que de la documentation.
* **Validation automatique** même pour les paramètres *path operation* définis dans les dépendances.
* Support pour les systèmes complexes d'authentification des utilisateurs, **connexions aux bases de données**, etc.
* **Aucun compromis** avec les bases de données, frontends, etc. Cependant l'intégration est simplifiée.

### "Plug-ins" illimités

En d'autres termes, importez et utilisez le code dont vous avez besoin.

Toute intégration est définie pour être simple à utiliser (avec ses dépendances).  
Vous pouvez alors créer un 'plug-in' pour votre application en 2 lignes de code en utilisant la même structure et de syntaxe utilisée pour vos *path operation*.

### Testé

* 100% <abbr title="La quantité de code est automatiquement testée">de test de couverture</abbr>.
* 100% <abbr title="Python type annotations, avec eux votre éditeur de code et des outils externes peuvent vous fournir un meilleur support">des types du code FastAPI sont annotés</abbr>.
* Utilisé par des application en production.

## Fonctionnalités Starlette

**FastAPI** est entièrement compatible avec <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong></a>. Pour information, FastAPI utilise Startlette.  
Ainsi, tout code additionnel Starlette que vous avez fonctionnera également.

`FastAPI` est actuellement une sous-classe de `Starlette`. Par conséquent, si vous connaissez ou savez utiliser Starlette, la plupart des fonctionnalités fonctionneront de la même façon.

Avec **FastAPI** vous avez toutes les fonctionnalités de **Starlette** (FastAPI est juste un Starlette sous stéroïdes):

* Performance sérieusement impressionnante. Il est <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">l'un des plus rapide framework Python disponible, et sur un pied d'égalité avec **NodeJS** et **Go**</a>.
* Support **WebSocket**.
* Support **GraphQL**.
* Processus de tâches de fond.
* Evènements de démarrage et d'arrêt.
* Les tests client sont construits directement à partir des `requêtes`.
* **CORS**, GZip, Static Files, Streaming responses.
* Support sur les **Sessions et Cookies**.
* 100% de tests de couverture.
* 100% du code possède des types annotés.

## Fonctionnalités Pydantic

**FastAPI** est totalement compatible avec (puisque basé sur) <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a>. Ainsi, tout code additionnel Pydantic que vous avez, fonctionnera également.

Vous pouvez également ajouter des librairies externes basées sur Pydantic, comme des <abbr title="Object-Relational Mapper">ORM</abbr>s, <abbr title="Object-Document Mapper">ODM</abbr>s pour bases de données.

Ceci signifie également que dans la plupart des cas, vous pouvez passer le même objet que vous avez récupéré à partir d'une requête effectuée **directement à une base de données**. En effet tout est automatiquement validé.

En conséquence, vous pouvez passer le même objet que vous avez récupéré d'une base de données **directement au client**.

Avec **FastAPI** vous avez toutes les fonctionnalités **Pydantic** (FastAPI utilie Pydantic pour toutes les manipulations de données):

* **Pas de prise de tête** :
    * Pas de définition de schéma dans un nouveau micro-langage à apprendre.
    * Si vous connaissez les Python types, vous savez comment utiliser Pydantic.

* S'intègre en douceur avec les **<abbr title="Integrated Development Environment, similaire à un éditeur de code">IDE </abbr>/<abbr title="Un programme qui analyse les erreurs de code"> linter </abbr>/ et votre cerveau** :
    * Les structures de données de pydantic sont des instances des classes que vous définissez. Du coup, l'auto-completion, le linting, mypy ainsi que votre intuition devraient opérer efficacement sur vos données validées.
* **Rapide** :
    * Dans les <a href="https://pydantic-docs.helpmanual.io/#benchmarks-tag" class="external-link" target="_blank">benchmarks</a> Pydantic est plus rapide que toutes les autres librairies testées.
* Valider les **structures complexes** :
    * Utilise les modèles Pydantic hiérarchiques, les Python `typing`’s `List` and `Dict`, etc.
    * Les validateurs permettent de définir des schémas de données complexes simplement, de les analyser et de les documenter en tant que schémas JSON.
    * Vous pouvez définir de gros objets **JSON imbriqués**. Ils seront validés et annotés.
* **Extension** :
    * Pydantic permet de définir des types de données personnalisées ou de personnaliser la validation des données avec des méthodes basées sur un modèle décoré avec le validator decorator.
* 100% de test de couverture.
