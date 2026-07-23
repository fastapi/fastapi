# Créer des applications plus grandes - Plusieurs fichiers { #bigger-applications-multiple-files }

Si vous créez une application ou une API web, il est rare que vous puissiez tout mettre dans un seul fichier.

**FastAPI** fournit un outil pratique pour structurer votre application tout en conservant toute la flexibilité.

/// note | Remarque

Si vous venez de Flask, cela équivaut aux Blueprints de Flask.

///

## Exemple de structure de fichiers { #an-example-file-structure }

Supposons que vous ayez une structure de fichiers comme ceci :

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

/// tip | Astuce

Il y a plusieurs fichiers `__init__.py` : un dans chaque répertoire ou sous-répertoire.

C'est cela qui permet d'importer du code d'un fichier dans un autre.

Par exemple, dans `app/main.py` vous pourriez avoir une ligne comme :

```
from app.routers import items
```

///

* Le répertoire `app` contient tout. Et il a un fichier vide `app/__init__.py`, c'est donc un « package Python » (une collection de « modules Python ») : `app`.
* Il contient un fichier `app/main.py`. Comme il se trouve dans un package Python (un répertoire avec un fichier `__init__.py`), c'est un « module » de ce package : `app.main`.
* Il y a aussi un fichier `app/dependencies.py`, tout comme `app/main.py`, c'est un « module » : `app.dependencies`.
* Il y a un sous-répertoire `app/routers/` avec un autre fichier `__init__.py`, c'est donc un « sous-package Python » : `app.routers`.
* Le fichier `app/routers/items.py` est dans un package, `app/routers/`, c'est donc un sous-module : `app.routers.items`.
* De même pour `app/routers/users.py`, c'est un autre sous-module : `app.routers.users`.
* Il y a aussi un sous-répertoire `app/internal/` avec un autre fichier `__init__.py`, c'est donc un autre « sous-package Python » : `app.internal`.
* Et le fichier `app/internal/admin.py` est un autre sous-module : `app.internal.admin`.

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

La même structure de fichiers avec des commentaires :

```bash
.
├── app                  # "app" est un package Python
│   ├── __init__.py      # ce fichier fait de "app" un "package Python"
│   ├── main.py          # module "main", ex. import app.main
│   ├── dependencies.py  # module "dependencies", ex. import app.dependencies
│   └── routers          # "routers" est un "sous-package Python"
│   │   ├── __init__.py  # fait de "routers" un "sous-package Python"
│   │   ├── items.py     # sous-module "items", ex. import app.routers.items
│   │   └── users.py     # sous-module "users", ex. import app.routers.users
│   └── internal         # "internal" est un "sous-package Python"
│       ├── __init__.py  # fait de "internal" un "sous-package Python"
│       └── admin.py     # sous-module "admin", ex. import app.internal.admin
```

## `APIRouter` { #apirouter }

Supposons que le fichier dédié à la gestion des utilisateurs soit le sous-module `/app/routers/users.py`.

Vous voulez séparer les *chemins d'accès* liés à vos utilisateurs du reste du code pour le garder organisé.

Mais cela fait toujours partie de la même application/API web **FastAPI** (cela fait partie du même « package Python »).

Vous pouvez créer les *chemins d'accès* pour ce module à l'aide de `APIRouter`.

### Importer `APIRouter` { #import-apirouter }

Vous l'importez et créez une « instance » de la même manière que vous le feriez avec la classe `FastAPI` :

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[1,3] title["app/routers/users.py"] *}

### Déclarer des *chemins d'accès* avec `APIRouter` { #path-operations-with-apirouter }

Puis vous l'utilisez pour déclarer vos *chemins d'accès*.

Utilisez-le de la même manière que vous utiliseriez la classe `FastAPI` :

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[6,11,16] title["app/routers/users.py"] *}

Vous pouvez considérer `APIRouter` comme une « mini `FastAPI` ».

Toutes les mêmes options sont prises en charge.

Tous les mêmes `parameters`, `responses`, `dependencies`, `tags`, etc.

/// tip | Astuce

Dans cet exemple, la variable s'appelle `router`, mais vous pouvez la nommer comme vous le souhaitez.

///

Nous allons inclure ce `APIRouter` dans l'application principale `FastAPI`, mais d'abord, examinons les dépendances et un autre `APIRouter`.

## Gérer les dépendances { #dependencies }

Nous voyons que nous allons avoir besoin de certaines dépendances utilisées à plusieurs endroits de l'application.

Nous les mettons donc dans leur propre module `dependencies` (`app/dependencies.py`).

Nous allons maintenant utiliser une dépendance simple pour lire un en-tête personnalisé `X-Token` :

{* ../../docs_src/bigger_applications/app_an_py310/dependencies.py hl[3,6:8] title["app/dependencies.py"] *}

/// tip | Astuce

Nous utilisons un en-tête inventé pour simplifier cet exemple.

Mais dans les cas réels, vous obtiendrez de meilleurs résultats en utilisant les [utilitaires de sécurité](security/index.md) intégrés.

///

## Créer un autre module avec `APIRouter` { #another-module-with-apirouter }

Supposons que vous ayez également les endpoints dédiés à la gestion des « items » de votre application dans le module `app/routers/items.py`.

Vous avez des *chemins d'accès* pour :

* `/items/`
* `/items/{item_id}`

C'est exactement la même structure que pour `app/routers/users.py`.

Mais nous voulons être plus malins et simplifier un peu le code.

Nous savons que tous les *chemins d'accès* de ce module ont les mêmes éléments :

* Préfixe de chemin `prefix` : `/items`.
* `tags` : (un seul tag : `items`).
* `responses` supplémentaires.
* `dependencies` : ils ont tous besoin de la dépendance `X-Token` que nous avons créée.

Donc, au lieu d'ajouter tout cela à chaque *chemin d'accès*, nous pouvons l'ajouter au `APIRouter`.

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[5:10,16,21] title["app/routers/items.py"] *}

Comme le chemin de chaque *chemin d'accès* doit commencer par `/`, comme dans :

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

... le préfixe ne doit pas inclure un `/` final.

Ainsi, le préfixe dans ce cas est `/items`.

Nous pouvons également ajouter une liste de `tags` et des `responses` supplémentaires qui seront appliqués à tous les *chemins d'accès* inclus dans ce routeur.

Et nous pouvons ajouter une liste de `dependencies` qui seront ajoutées à tous les *chemins d'accès* du routeur et seront exécutées/résolues pour chaque requête qui leur est faite.

/// tip | Astuce

Notez que, tout comme pour les [dépendances dans les décorateurs de *chemin d'accès*](dependencies/dependencies-in-path-operation-decorators.md), aucune valeur ne sera transmise à votre *fonction de chemin d'accès*.

///

Le résultat final est que les chemins d'item sont désormais :

* `/items/`
* `/items/{item_id}`

... comme prévu.

* Ils seront marqués avec une liste de tags qui contient une seule chaîne « items ».
    * Ces « tags » sont particulièrement utiles pour les systèmes de documentation interactive automatique (utilisant OpenAPI).
* Ils incluront tous les `responses` prédéfinies.
* Tous ces *chemins d'accès* auront la liste des `dependencies` évaluées/exécutées avant eux.
    * Si vous déclarez également des dépendances dans un *chemin d'accès* spécifique, **elles seront aussi exécutées**.
    * Les dépendances du routeur sont exécutées en premier, puis les [`dependencies` dans le décorateur](dependencies/dependencies-in-path-operation-decorators.md), puis les dépendances des paramètres normaux.
    * Vous pouvez également ajouter des [`Security` dependencies avec des `scopes`](../advanced/security/oauth2-scopes.md).

/// tip | Astuce

Avoir des `dependencies` dans le `APIRouter` peut servir, par exemple, à exiger une authentification pour tout un groupe de *chemins d'accès*. Même si les dépendances ne sont pas ajoutées individuellement à chacun d'eux.

///

/// tip | Astuce

Les paramètres `prefix`, `tags`, `responses` et `dependencies` sont (comme dans de nombreux autres cas) simplement une fonctionnalité de **FastAPI** pour vous aider à éviter la duplication de code.

///

### Importer les dépendances { #import-the-dependencies }

Ce code se trouve dans le module `app.routers.items`, le fichier `app/routers/items.py`.

Et nous devons récupérer la fonction de dépendance depuis le module `app.dependencies`, le fichier `app/dependencies.py`.

Nous utilisons donc un import relatif avec `..` pour les dépendances :

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[3] title["app/routers/items.py"] *}

#### Comprendre le fonctionnement des imports relatifs { #how-relative-imports-work }

/// tip | Astuce

Si vous savez parfaitement comment fonctionnent les imports, passez à la section suivante ci-dessous.

///

Un seul point `.`, comme dans :

```Python
from .dependencies import get_token_header
```

signifierait :

* En partant du même package dans lequel vit ce module (le fichier `app/routers/items.py`) (le répertoire `app/routers/`)...
* trouver le module `dependencies` (un fichier imaginaire `app/routers/dependencies.py`)...
* et en importer la fonction `get_token_header`.

Mais ce fichier n'existe pas, nos dépendances sont dans un fichier `app/dependencies.py`.

Rappelez-vous à quoi ressemble la structure de notre app/fichiers :

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

---

Les deux points `..`, comme dans :

```Python
from ..dependencies import get_token_header
```

veulent dire :

* En partant du même package dans lequel vit ce module (le fichier `app/routers/items.py`) (le répertoire `app/routers/`)...
* aller au package parent (le répertoire `app/`)...
* et là, trouver le module `dependencies` (le fichier `app/dependencies.py`)...
* et en importer la fonction `get_token_header`.

Cela fonctionne correctement ! 🎉

---

De la même manière, si nous avions utilisé trois points `...`, comme dans :

```Python
from ...dependencies import get_token_header
```

cela voudrait dire :

* En partant du même package dans lequel vit ce module (le fichier `app/routers/items.py`) (le répertoire `app/routers/`)...
* aller au package parent (le répertoire `app/`)...
* puis aller au parent de ce package (il n'y a pas de package parent, `app` est le niveau supérieur 😱)...
* et là, trouver le module `dependencies` (le fichier `app/dependencies.py`)...
* et en importer la fonction `get_token_header`.

Cela ferait référence à un package au-dessus de `app/`, avec son propre fichier `__init__.py`, etc. Mais nous n'avons pas cela. Donc, cela lèverait une erreur dans notre exemple. 🚨

Mais maintenant vous savez comment cela fonctionne, vous pouvez donc utiliser des imports relatifs dans vos propres applications, aussi complexes soient-elles. 🤓

### Ajouter des `tags`, `responses` et `dependencies` personnalisés { #add-some-custom-tags-responses-and-dependencies }

Nous n'ajoutons pas le préfixe `/items` ni `tags=["items"]` à chaque *chemin d'accès* parce que nous les avons ajoutés au `APIRouter`.

Mais nous pouvons toujours ajouter _davantage_ de `tags` qui seront appliqués à un *chemin d'accès* spécifique, ainsi que des `responses` supplémentaires propres à ce *chemin d'accès* :

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[30:31] title["app/routers/items.py"] *}

/// tip | Astuce

Ce dernier chemin d'accès aura la combinaison de tags : `["items", "custom"]`.

Et il aura également les deux réponses dans la documentation, une pour `404` et une pour `403`.

///

## Créer l'application `FastAPI` principale { #the-main-fastapi }

Voyons maintenant le module `app/main.py`.

C'est ici que vous importez et utilisez la classe `FastAPI`.

Ce sera le fichier principal de votre application qui reliera tout ensemble.

Et comme la plupart de votre logique vivra désormais dans son propre module, le fichier principal sera assez simple.

### Importer `FastAPI` { #import-fastapi }

Vous importez et créez une classe `FastAPI` comme d'habitude.

Et nous pouvons même déclarer des [dépendances globales](dependencies/global-dependencies.md) qui seront combinées avec les dépendances de chaque `APIRouter` :

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[1,3,7] title["app/main.py"] *}

### Importer les `APIRouter` { #import-the-apirouter }

Nous importons maintenant les autres sous-modules qui ont des `APIRouter` :

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[4:5] title["app/main.py"] *}

Comme les fichiers `app/routers/users.py` et `app/routers/items.py` sont des sous-modules qui font partie du même package Python `app`, nous pouvons utiliser un seul point `.` pour les importer en utilisant des « imports relatifs ».

### Comprendre le fonctionnement de l'import { #how-the-importing-works }

La section :

```Python
from .routers import items, users
```

signifie :

* En partant du même package dans lequel vit ce module (le fichier `app/main.py`) (le répertoire `app/`)...
* chercher le sous-package `routers` (le répertoire `app/routers/`)...
* et en importer le sous-module `items` (le fichier `app/routers/items.py`) et `users` (le fichier `app/routers/users.py`)...

Le module `items` aura une variable `router` (`items.router`). C'est celle que nous avons créée dans le fichier `app/routers/items.py`, c'est un objet `APIRouter`.

Nous faisons ensuite la même chose pour le module `users`.

Nous pourrions aussi les importer ainsi :

```Python
from app.routers import items, users
```

/// note | Remarque

La première version est un « import relatif » :

```Python
from .routers import items, users
```

La deuxième version est un « import absolu » :

```Python
from app.routers import items, users
```

Pour en savoir plus sur les Packages et Modules Python, lisez [la documentation officielle de Python sur les modules](https://docs.python.org/3/tutorial/modules.html).

///

### Éviter les collisions de noms { #avoid-name-collisions }

Nous importons le sous-module `items` directement, au lieu d'importer uniquement sa variable `router`.

C'est parce que nous avons également une autre variable nommée `router` dans le sous-module `users`.

Si nous les avions importées l'une après l'autre, comme :

```Python
from .routers.items import router
from .routers.users import router
```

le `router` de `users` écraserait celui de `items` et nous ne pourrions pas les utiliser en même temps.

Donc, pour pouvoir utiliser les deux dans le même fichier, nous importons directement les sous-modules :

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[5] title["app/main.py"] *}

### Inclure les `APIRouter` pour `users` et `items` { #include-the-apirouters-for-users-and-items }

Incluons maintenant les `router` des sous-modules `users` et `items` :

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[10:11] title["app/main.py"] *}

/// note | Remarque

`users.router` contient le `APIRouter` à l'intérieur du fichier `app/routers/users.py`.

Et `items.router` contient le `APIRouter` à l'intérieur du fichier `app/routers/items.py`.

///

Avec `app.include_router()`, nous pouvons ajouter chaque `APIRouter` à l'application principale `FastAPI`.

Cela inclura toutes les routes de ce routeur comme faisant partie de l'application.

/// note | Détails techniques

FastAPI conserve le `APIRouter` original et ses `APIRoute` actifs lorsque le routeur est inclus dans l'application principale.

Cela signifie que des sous-classes personnalisées de `APIRouter` et `APIRoute` peuvent toujours intervenir après l'inclusion du routeur.

///

/// tip | Astuce

Vous n'avez pas à vous soucier de la performance lors de l'inclusion de routeurs.

C'est conçu pour être léger et pour éviter d'ajouter une surcharge à chaque requête.

Donc cela n'affectera pas la performance. ⚡

///

### Inclure un `APIRouter` avec un `prefix`, des `tags`, des `responses` et des `dependencies` personnalisés { #include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies }

Imaginons maintenant que votre organisation vous ait fourni le fichier `app/internal/admin.py`.

Il contient un `APIRouter` avec quelques *chemins d'accès* d'administration que votre organisation partage entre plusieurs projets.

Pour cet exemple, il sera très simple. Mais supposons que, parce qu'il est partagé avec d'autres projets de l'organisation, nous ne puissions pas le modifier et ajouter un `prefix`, des `dependencies`, des `tags`, etc. directement au `APIRouter` :

{* ../../docs_src/bigger_applications/app_an_py310/internal/admin.py hl[3] title["app/internal/admin.py"] *}

Mais nous voulons quand même définir un `prefix` personnalisé lors de l'inclusion du `APIRouter` afin que tous ses *chemins d'accès* commencent par `/admin`, nous voulons le sécuriser avec les `dependencies` que nous avons déjà pour ce projet, et nous voulons inclure des `tags` et des `responses`.

Nous pouvons déclarer tout cela sans avoir à modifier le `APIRouter` d'origine en passant ces paramètres à `app.include_router()` :

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[14:17] title["app/main.py"] *}

De cette façon, le `APIRouter` original restera inchangé, afin que nous puissions toujours partager ce même fichier `app/internal/admin.py` avec d'autres projets de l'organisation.

Le résultat est que, dans notre application, chacun des *chemins d'accès* du module `admin` aura :

* Le préfixe `/admin`.
* Le tag `admin`.
* La dépendance `get_token_header`.
* La réponse `418`. 🍵

Mais cela n'affectera que ce `APIRouter` dans notre application, pas dans tout autre code qui l'utilise.

Ainsi, par exemple, d'autres projets pourraient utiliser le même `APIRouter` avec une méthode d'authentification différente.

### Inclure un *chemin d'accès* { #include-a-path-operation }

Nous pouvons également ajouter des *chemins d'accès* directement à l'application `FastAPI`.

Ici, nous le faisons ... juste pour montrer que nous le pouvons 🤷 :

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[21:23] title["app/main.py"] *}

et cela fonctionnera correctement, avec tous les autres *chemins d'accès* ajoutés avec `app.include_router()`.

/// note | Détails très techniques

**Remarque** : c'est un détail très technique que vous pouvez probablement **simplement ignorer**.

---

Les `APIRouter` ne sont pas « montés », ils ne sont pas isolés du reste de l'application.

C'est parce que nous voulons inclure leurs *chemins d'accès* dans le schéma OpenAPI et les interfaces utilisateur.

FastAPI conserve les routeurs et chemins d'accès originaux actifs, et combine les préfixes de routeur, dépendances, tags, réponses et autres métadonnées lors du traitement des requêtes et de la génération d'OpenAPI.

///

## Configurer l'`entrypoint` dans `pyproject.toml` { #configure-the-entrypoint-in-pyproject-toml }

Comme votre objet FastAPI `app` vit dans `app/main.py`, vous pouvez configurer l'`entrypoint` dans votre fichier `pyproject.toml` comme ceci :

```toml
[tool.fastapi]
entrypoint = "app.main:app"
```

ce qui équivaut à importer ainsi :

```python
from app.main import app
```

De cette façon, la commande `fastapi` saura où trouver votre app.

/// Note | Remarque

Vous pourriez aussi passer le chemin à la commande, comme :

```console
$ fastapi dev app/main.py
```

Mais vous devez vous rappeler de passer le bon chemin à chaque fois que vous appelez la commande `fastapi`.

En outre, d'autres outils pourraient ne pas être en mesure de la trouver, par exemple l'[Extension VS Code](../editor-support.md) ou [FastAPI Cloud](https://fastapicloud.com), il est donc recommandé d'utiliser l'`entrypoint` dans `pyproject.toml`.

///

## Consulter les documents d'API automatiques { #check-the-automatic-api-docs }

Maintenant, exécutez votre application :

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Et ouvrez les documents à [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Vous verrez les documents d'API automatiques, incluant les chemins de tous les sous-modules, utilisant les bons chemins (et préfixes) et les bons tags :

<img src="/img/tutorial/bigger-applications/image01.png">

## Inclure le même routeur plusieurs fois avec des `prefix` différents { #include-the-same-router-multiple-times-with-different-prefix }

Vous pouvez aussi utiliser `.include_router()` plusieurs fois avec le même routeur en utilisant des préfixes différents.

Cela peut être utile, par exemple, pour exposer la même API sous des préfixes différents, p. ex. `/api/v1` et `/api/latest`.

C'est un usage avancé dont vous n'aurez peut-être pas vraiment besoin, mais il est là au cas où.

## Inclure un `APIRouter` dans un autre { #include-an-apirouter-in-another }

De la même manière que vous pouvez inclure un `APIRouter` dans une application `FastAPI`, vous pouvez inclure un `APIRouter` dans un autre `APIRouter` en utilisant :

```Python
router.include_router(other_router)
```

Vous pouvez le faire avant ou après avoir inclus `router` dans l'application `FastAPI`. FastAPI inclura quand même les *chemins d'accès* de `other_router` dans le routage et dans OpenAPI.

Il en va de même pour les *chemins d'accès* ajoutés plus tard aux routeurs. Ils seront visibles via l'inclusion antérieure également.

/// warning | Détails techniques

Évitez de modifier directement `router.routes` après avoir inclus un routeur. FastAPI considère l'inclusion d'un routeur comme « en direct », de sorte que le routeur original et ses routes restent utilisés pour le routage et la génération d'OpenAPI.

Utilisez les API documentées comme les décorateurs de *chemin d'accès* et `.include_router()` pour ajouter des routes et des routeurs.

Considérez `router.routes` comme un arbre de routes de plus bas niveau pouvant contenir des définitions de routes et des routeurs inclus, et évitez de vous y fier comme à une liste plate de *chemins d'accès* finaux.

///
