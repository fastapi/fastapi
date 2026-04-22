# Bases de données SQL (relationnelles) { #sql-relational-databases }

**FastAPI** ne vous oblige pas à utiliser une base de données SQL (relationnelle). Mais vous pouvez utiliser **n'importe quelle base de données** que vous voulez.

Ici, nous allons voir un exemple utilisant [SQLModel](https://sqlmodel.tiangolo.com/).

**SQLModel** est construit au-dessus de [SQLAlchemy](https://www.sqlalchemy.org/) et de Pydantic. Il a été créé par le même auteur que **FastAPI** pour être l'accord parfait pour les applications FastAPI qui ont besoin d'utiliser des **bases de données SQL**.

/// tip | Astuce

Vous pouvez utiliser toute autre bibliothèque SQL ou NoSQL que vous voulez (dans certains cas appelées <abbr title="Object Relational Mapper - Mappeur objet-relationnel: un terme sophistiqué pour une bibliothèque où certaines classes représentent des tables SQL et les instances représentent des lignes dans ces tables">« ORMs »</abbr>), FastAPI ne vous impose rien. 😎

///

Comme SQLModel est basé sur SQLAlchemy, vous pouvez facilement utiliser **toute base prise en charge** par SQLAlchemy (ce qui les rend également prises en charge par SQLModel), comme :

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server, etc.

Dans cet exemple, nous utiliserons **SQLite**, car il utilise un seul fichier et Python a un support intégré. Ainsi, vous pouvez copier cet exemple et l'exécuter tel quel.

Plus tard, pour votre application de production, vous voudrez peut-être utiliser un serveur de base de données comme **PostgreSQL**.

/// tip | Astuce

Il existe un générateur de projet officiel avec **FastAPI** et **PostgreSQL**, incluant un frontend et plus d'outils : [https://github.com/fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)

///

Il s'agit d'un tutoriel très simple et court ; si vous souhaitez apprendre sur les bases de données en général, sur SQL, ou des fonctionnalités plus avancées, allez voir la [documentation SQLModel](https://sqlmodel.tiangolo.com/).

## Installer `SQLModel` { #install-sqlmodel }

D'abord, assurez-vous de créer votre [environnement virtuel](../virtual-environments.md), de l'activer, puis d'installer `sqlmodel` :

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## Créer l'application avec un modèle unique { #create-the-app-with-a-single-model }

Nous allons d'abord créer la première version la plus simple de l'application avec un seul modèle **SQLModel**.

Ensuite, nous l'améliorerons en augmentant la sécurité et la polyvalence avec **plusieurs modèles** ci-dessous. 🤓

### Créer les modèles { #create-models }

Importez `SQLModel` et créez un modèle de base de données :

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

La classe `Hero` est très similaire à un modèle Pydantic (en fait, en dessous, c'est réellement un modèle Pydantic).

Il y a quelques différences :

* `table=True` indique à SQLModel qu'il s'agit d'un *modèle de table*, il doit représenter une **table** dans la base SQL, ce n'est pas seulement un *modèle de données* (comme le serait n'importe quelle autre classe Pydantic classique).

* `Field(primary_key=True)` indique à SQLModel que `id` est la **clé primaire** dans la base SQL (vous pouvez en savoir plus sur les clés primaires SQL dans la documentation SQLModel).

    Remarque : nous utilisons `int | None` pour le champ clé primaire afin qu'en Python nous puissions *créer un objet sans `id`* (`id=None`), en supposant que la base *le génère à l'enregistrement*. SQLModel comprend que la base fournira l'`id` et *définit la colonne comme un `INTEGER` non nul* dans le schéma de base. Voir la [documentation SQLModel sur les clés primaires](https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#primary-key-id) pour plus de détails.

* `Field(index=True)` indique à SQLModel qu'il doit créer un **index SQL** pour cette colonne, ce qui permettra des recherches plus rapides dans la base lors de la lecture de données filtrées par cette colonne.

    SQLModel saura que quelque chose déclaré comme `str` sera une colonne SQL de type `TEXT` (ou `VARCHAR`, selon la base).

### Créer un engine { #create-an-engine }

Un `engine` SQLModel (en dessous c'est en fait un `engine` SQLAlchemy) est ce qui **détient les connexions** à la base de données.

Vous devez avoir **un seul objet `engine`** pour tout votre code afin de se connecter à la même base.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

L'utilisation de `check_same_thread=False` permet à FastAPI d'utiliser la même base SQLite dans différents threads. C'est nécessaire car **une seule requête** peut utiliser **plus d'un thread** (par exemple dans des dépendances).

Ne vous inquiétez pas, avec la structure du code, nous nous assurerons d'utiliser **une seule *session* SQLModel par requête** plus loin, c'est en fait ce que `check_same_thread` essaie d'assurer.

### Créer les tables { #create-the-tables }

Nous ajoutons ensuite une fonction qui utilise `SQLModel.metadata.create_all(engine)` pour **créer les tables** pour tous les *modèles de table*.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### Créer une dépendance de session { #create-a-session-dependency }

Une **`Session`** est ce qui stocke les **objets en mémoire** et suit les modifications nécessaires des données, puis **utilise l'`engine`** pour communiquer avec la base.

Nous allons créer une **dépendance** FastAPI avec `yield` qui fournira une nouvelle `Session` pour chaque requête. C'est ce qui garantit que nous utilisons une seule session par requête. 🤓

Puis nous créons une dépendance `Annotated` `SessionDep` pour simplifier le reste du code qui utilisera cette dépendance.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### Créer les tables de base au démarrage { #create-database-tables-on-startup }

Nous allons créer les tables de base de données au démarrage de l'application.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

Ici, nous créons les tables lors d'un événement de démarrage de l'application.

En production, vous utiliseriez probablement un script de migration qui s'exécute avant de démarrer votre application. 🤓

/// tip | Astuce

SQLModel aura des utilitaires de migration enveloppant Alembic, mais pour l'instant, vous pouvez utiliser [Alembic](https://alembic.sqlalchemy.org/en/latest/) directement.

///

### Créer un héros { #create-a-hero }

Comme chaque modèle SQLModel est aussi un modèle Pydantic, vous pouvez l'utiliser dans les mêmes **annotations de type** que vous utiliseriez pour des modèles Pydantic.

Par exemple, si vous déclarez un paramètre de type `Hero`, il sera lu depuis le **corps JSON**.

De la même manière, vous pouvez le déclarer comme **type de retour** de la fonction, et alors la forme des données apparaîtra dans l'UI automatique de documentation de l'API.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

Ici, nous utilisons la dépendance `SessionDep` (une `Session`) pour ajouter le nouveau `Hero` à l'instance de `Session`, valider les changements dans la base, rafraîchir les données dans `hero`, puis le retourner.

### Lire les héros { #read-heroes }

Nous pouvons **lire** des `Hero` depuis la base en utilisant un `select()`. Nous pouvons inclure une `limit` et un `offset` pour paginer les résultats.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### Lire un héros { #read-one-hero }

Nous pouvons **lire** un seul `Hero`.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### Supprimer un héros { #delete-a-hero }

Nous pouvons aussi **supprimer** un `Hero`.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### Exécuter l'application { #run-the-app }

Vous pouvez exécuter l'application :

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Ensuite, allez sur l'UI `/docs`, vous verrez que **FastAPI** utilise ces **modèles** pour **documenter** l'API, et les utilisera aussi pour **sérialiser** et **valider** les données.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## Mettre à jour l'application avec plusieurs modèles { #update-the-app-with-multiple-models }

Maintenant, **refactorisons** un peu cette application pour augmenter la **sécurité** et la **polyvalence**.

Si vous vérifiez l'application précédente, dans l'UI vous pouvez voir que, jusqu'à présent, elle laisse le client décider de l'`id` du `Hero` à créer. 😱

Nous ne devrions pas laisser cela se produire, ils pourraient écraser un `id` que nous avons déjà attribué dans la base. Décider de l'`id` doit être fait par le **backend** ou la **base**, **pas par le client**.

De plus, nous créons un `secret_name` pour le héros, mais jusqu'ici, nous le renvoyons partout, ce n'est pas très « secret » ... 😅

Nous allons corriger ces choses en ajoutant quelques **modèles supplémentaires**. C'est là que SQLModel brille. ✨

### Créer plusieurs modèles { #create-multiple-models }

Dans **SQLModel**, toute classe de modèle qui a `table=True` est un **modèle de table**.

Et toute classe de modèle qui n'a pas `table=True` est un **modèle de données**, ceux-ci sont en réalité juste des modèles Pydantic (avec deux petites fonctionnalités en plus). 🤓

Avec SQLModel, nous pouvons utiliser **l'héritage** pour **éviter de dupliquer** tous les champs dans tous les cas.

#### `HeroBase` - la classe de base { #herobase-the-base-class }

Commençons avec un modèle `HeroBase` qui a tous les **champs partagés** par tous les modèles :

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - le *modèle de table* { #hero-the-table-model }

Créons ensuite `Hero`, le *modèle de table* proprement dit, avec les **champs supplémentaires** qui ne sont pas toujours dans les autres modèles :

* `id`
* `secret_name`

Comme `Hero` hérite de `HeroBase`, il **a aussi** les **champs** déclarés dans `HeroBase`, donc tous les champs de `Hero` sont :

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - le *modèle de données* public { #heropublic-the-public-data-model }

Ensuite, nous créons un modèle `HeroPublic`, c'est celui qui sera **retourné** aux clients de l'API.

Il a les mêmes champs que `HeroBase`, il n'inclura donc pas `secret_name`.

Enfin, l'identité de nos héros est protégée ! 🥷

Il redéclare aussi `id: int`. Ce faisant, nous faisons un **contrat** avec les clients de l'API, afin qu'ils puissent toujours s'attendre à ce que `id` soit présent et soit un `int` (il ne sera jamais `None`).

/// tip | Astuce

Avoir le modèle de retour qui garantit qu'une valeur est toujours disponible et toujours `int` (pas `None`) est très utile pour les clients de l'API, ils peuvent écrire un code beaucoup plus simple avec cette certitude.

De plus, les **clients générés automatiquement** auront des interfaces plus simples, afin que les développeurs qui communiquent avec votre API puissent travailler bien plus facilement avec votre API. 😎

///

Tous les champs de `HeroPublic` sont les mêmes que dans `HeroBase`, avec `id` déclaré comme `int` (pas `None`) :

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - le *modèle de données* pour créer un héros { #herocreate-the-data-model-to-create-a-hero }

Nous créons maintenant un modèle `HeroCreate`, c'est celui qui **validera** les données provenant des clients.

Il a les mêmes champs que `HeroBase`, et il a aussi `secret_name`.

Maintenant, lorsque les clients **créent un nouveau héros**, ils enverront `secret_name`, il sera stocké dans la base, mais ces noms secrets ne seront pas renvoyés dans l'API aux clients.

/// tip | Astuce

C'est ainsi que vous géreriez les **mots de passe**. Les recevoir, mais ne pas les renvoyer dans l'API.

Vous **hacherez** aussi les valeurs des mots de passe avant de les stocker, **ne les stockez jamais en texte en clair**.

///

Les champs de `HeroCreate` sont :

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - le *modèle de données* pour mettre à jour un héros { #heroupdate-the-data-model-to-update-a-hero }

Nous n'avions pas de moyen de **mettre à jour un héros** dans la version précédente de l'application, mais maintenant avec **plusieurs modèles**, nous pouvons le faire. 🎉

Le *modèle de données* `HeroUpdate` est un peu spécial, il a **tous les mêmes champs** qui seraient nécessaires pour créer un nouveau héros, mais tous les champs sont **optionnels** (ils ont tous une valeur par défaut). Ainsi, lorsque vous mettez à jour un héros, vous pouvez n'envoyer que les champs que vous souhaitez mettre à jour.

Comme tous les **champs changent réellement** (le type inclut désormais `None` et ils ont maintenant une valeur par défaut de `None`), nous devons les **redéclarer**.

Nous n'avons pas vraiment besoin d'hériter de `HeroBase` puisque nous redéclarons tous les champs. Je le laisse hériter juste pour la cohérence, mais ce n'est pas nécessaire. C'est plutôt une question de goût personnel. 🤷

Les champs de `HeroUpdate` sont :

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### Créer avec `HeroCreate` et retourner un `HeroPublic` { #create-with-herocreate-and-return-a-heropublic }

Maintenant que nous avons **plusieurs modèles**, nous pouvons mettre à jour les parties de l'application qui les utilisent.

Nous recevons dans la requête un *modèle de données* `HeroCreate`, et à partir de celui-ci, nous créons un *modèle de table* `Hero`.

Ce nouveau *modèle de table* `Hero` aura les champs envoyés par le client, et aura aussi un `id` généré par la base.

Nous retournons ensuite le même *modèle de table* `Hero` tel quel depuis la fonction. Mais comme nous déclarons le `response_model` avec le *modèle de données* `HeroPublic`, **FastAPI** utilisera `HeroPublic` pour valider et sérialiser les données.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | Astuce

Nous utilisons maintenant `response_model=HeroPublic` au lieu de l'**annotation de type de retour** `-> HeroPublic` car la valeur que nous renvoyons n'est en réalité *pas* un `HeroPublic`.

Si nous avions déclaré `-> HeroPublic`, votre éditeur et votre linter se plaindraient (à juste titre) que vous retournez un `Hero` au lieu d'un `HeroPublic`.

En le déclarant dans `response_model`, nous disons à **FastAPI** de faire son travail, sans interférer avec les annotations de type et l'aide de votre éditeur et d'autres outils.

///

### Lire des héros avec `HeroPublic` { #read-heroes-with-heropublic }

Nous pouvons faire la même chose qu'avant pour **lire** des `Hero`, à nouveau, nous utilisons `response_model=list[HeroPublic]` pour garantir que les données sont correctement validées et sérialisées.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### Lire un héros avec `HeroPublic` { #read-one-hero-with-heropublic }

Nous pouvons **lire** un héros unique :

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### Mettre à jour un héros avec `HeroUpdate` { #update-a-hero-with-heroupdate }

Nous pouvons **mettre à jour un héros**. Pour cela, nous utilisons une opération HTTP `PATCH`.

Et dans le code, nous obtenons un `dict` avec toutes les données envoyées par le client, **uniquement les données envoyées par le client**, en excluant toute valeur qui serait là simplement parce que c'est la valeur par défaut. Pour ce faire, nous utilisons `exclude_unset=True`. C'est l'astuce principale. 🪄

Nous utilisons ensuite `hero_db.sqlmodel_update(hero_data)` pour mettre à jour `hero_db` avec les données de `hero_data`.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### Supprimer un héros (bis) { #delete-a-hero-again }

**Supprimer** un héros reste pratiquement identique.

Nous n'allons pas céder à l'envie de tout refactoriser pour celui-ci. 😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### Exécuter l'application à nouveau { #run-the-app-again }

Vous pouvez exécuter l'application à nouveau :

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Si vous allez sur l'UI `/docs` de l'API, vous verrez qu'elle est maintenant à jour, et qu'elle n'attendra plus de recevoir l'`id` du client lors de la création d'un héros, etc.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## Récapitulatif { #recap }

Vous pouvez utiliser [**SQLModel**](https://sqlmodel.tiangolo.com/) pour interagir avec une base SQL et simplifier le code avec des *modèles de données* et des *modèles de table*.

Vous pouvez en apprendre beaucoup plus dans la documentation **SQLModel**, il y a un mini [tutoriel plus long sur l'utilisation de SQLModel avec **FastAPI**](https://sqlmodel.tiangolo.com/tutorial/fastapi/). 🚀
