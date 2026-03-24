# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/fr"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>Framework FastAPI, haute performance, facile à apprendre, rapide à coder, prêt pour la production</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation** : [https://fastapi.tiangolo.com/fr](https://fastapi.tiangolo.com/fr)

**Code Source** : [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI est un framework web moderne et rapide (haute performance) pour la création d'API avec Python, basé sur les annotations de type standard de Python.

Les principales fonctionnalités sont :

* **Rapide** : très hautes performances, au niveau de **NodeJS** et **Go** (grâce à Starlette et Pydantic). [L'un des frameworks Python les plus rapides](#performance).
* **Rapide à coder** : augmente la vitesse de développement des fonctionnalités d'environ 200 % à 300 %. *
* **Moins de bugs** : réduit d'environ 40 % les erreurs induites par le développeur. *
* **Intuitif** : excellente compatibilité avec les éditeurs. <dfn title="également connu sous le nom de : auto-complétion, autocomplétion, IntelliSense">Autocomplétion</dfn> partout. Moins de temps passé à déboguer.
* **Facile** : conçu pour être facile à utiliser et à apprendre. Moins de temps passé à lire les documents.
* **Concis** : diminue la duplication de code. Plusieurs fonctionnalités à partir de chaque déclaration de paramètre. Moins de bugs.
* **Robuste** : obtenez un code prêt pour la production. Avec une documentation interactive automatique.
* **Basé sur des normes** : basé sur (et entièrement compatible avec) les standards ouverts pour les APIs : [OpenAPI](https://github.com/OAI/OpenAPI-Specification) (précédemment connu sous le nom de Swagger) et [JSON Schema](https://json-schema.org/).

<small>* estimation basée sur des tests d'une équipe de développement interne, construisant des applications de production.</small>

## Sponsors { #sponsors }

<!-- sponsors -->

### Sponsor clé de voûte { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### Sponsors Or et Argent { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

[Autres sponsors](https://fastapi.tiangolo.com/fr/fastapi-people/#sponsors)

## Opinions { #opinions }

« _[...] J'utilise beaucoup **FastAPI** ces derniers temps. [...] Je prévois de l'utiliser dans mon équipe pour tous les **services de ML chez Microsoft**. Certains d'entre eux sont intégrés au cœur de **Windows** et à certains produits **Office**._ »

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(ref)</small></a></div>

---

« _Nous avons adopté la bibliothèque **FastAPI** pour créer un serveur **REST** qui peut être interrogé pour obtenir des **prédictions**. [pour Ludwig]_ »

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, et Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/"><small>(ref)</small></a></div>

---

« _**Netflix** est heureux d'annoncer la publication en open source de notre framework d'orchestration de **gestion de crise** : **Dispatch** ! [construit avec **FastAPI**]_ »

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(ref)</small></a></div>

---

« _Je suis plus qu'enthousiaste à propos de **FastAPI**. C'est tellement fun !_ »

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong>Animateur du podcast [Python Bytes](https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855)</strong> <a href="https://x.com/brianokken/status/1112220079972728832"><small>(ref)</small></a></div>

---

« _Honnêtement, ce que vous avez construit a l'air super solide et soigné. À bien des égards, c'est ce que je voulais que **Hug** soit — c'est vraiment inspirant de voir quelqu'un construire ça._ »

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong>Créateur de [Hug](https://github.com/hugapi/hug)</strong> <a href="https://news.ycombinator.com/item?id=19455465"><small>(ref)</small></a></div>

---

« _Si vous cherchez à apprendre un **framework moderne** pour créer des APIs REST, regardez **FastAPI** [...] C'est rapide, facile à utiliser et facile à apprendre [...]_ »

« _Nous sommes passés à **FastAPI** pour nos **APIs** [...] Je pense que vous l'aimerez [...]_ »

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong>Fondateurs de [Explosion AI](https://explosion.ai) - Créateurs de [spaCy](https://spacy.io)</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680"><small>(ref)</small></a></div>

---

« _Si quelqu'un cherche à construire une API Python de production, je recommande vivement **FastAPI**. Il est **magnifiquement conçu**, **simple à utiliser** et **hautement scalable**. Il est devenu un **composant clé** de notre stratégie de développement API-first et alimente de nombreuses automatisations et services tels que notre ingénieur TAC virtuel._ »

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(ref)</small></a></div>

---

## Mini documentaire FastAPI { #fastapi-mini-documentary }

Un [mini documentaire FastAPI](https://www.youtube.com/watch?v=mpR8ngthqiE) est sorti fin 2025, vous pouvez le regarder en ligne :

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**, le FastAPI des CLIs { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Si vous construisez une application <abbr title="Command Line Interface - Interface en ligne de commande">CLI</abbr> à utiliser dans un terminal au lieu d'une API web, regardez [**Typer**](https://typer.tiangolo.com/).

**Typer** est le petit frère de FastAPI. Et il est destiné à être le **FastAPI des CLIs**. ⌨️ 🚀

## Prérequis { #requirements }

FastAPI repose sur les épaules de géants :

* [Starlette](https://www.starlette.dev/) pour les parties web.
* [Pydantic](https://docs.pydantic.dev/) pour les parties données.

## Installation { #installation }

Créez et activez un [environnement virtuel](https://fastapi.tiangolo.com/fr/virtual-environments/) puis installez FastAPI :

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Remarque** : Vous devez vous assurer de mettre « fastapi[standard] » entre guillemets pour garantir que cela fonctionne dans tous les terminaux.

## Exemple { #example }

### Créer { #create-it }

Créez un fichier `main.py` avec :

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Ou utilisez <code>async def</code>...</summary>

Si votre code utilise `async` / `await`, utilisez `async def` :

```Python hl_lines="7  12"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

**Remarque** :

Si vous ne savez pas, consultez la section « Vous êtes pressés ? » à propos de [`async` et `await` dans la documentation](https://fastapi.tiangolo.com/fr/async/#in-a-hurry).

</details>

### Lancer { #run-it }

Lancez le serveur avec :

<div class="termy">

```console
$ fastapi dev

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>À propos de la commande <code>fastapi dev</code>...</summary>

La commande `fastapi dev` lit automatiquement votre fichier `main.py`, détecte l'application **FastAPI** qu'il contient et lance un serveur avec [Uvicorn](https://www.uvicorn.dev).

Par défaut, `fastapi dev` démarre avec le rechargement automatique activé pour le développement local.

Vous pouvez en savoir plus dans la [documentation de la CLI FastAPI](https://fastapi.tiangolo.com/fr/fastapi-cli/).

</details>

### Vérifier { #check-it }

Ouvrez votre navigateur à l'adresse [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery).

Vous verrez la réponse JSON :

```JSON
{"item_id": 5, "q": "somequery"}
```

Vous avez déjà créé une API qui :

* Reçoit des requêtes HTTP sur les _chemins_ `/` et `/items/{item_id}`.
* Les deux _chemins_ acceptent des <em>opérations</em> `GET` (également connues sous le nom de _méthodes_ HTTP).
* Le _chemin_ `/items/{item_id}` a un _paramètre de chemin_ `item_id` qui doit être un `int`.
* Le _chemin_ `/items/{item_id}` a un _paramètre de requête_ optionnel `q` de type `str`.

### Documentation API interactive { #interactive-api-docs }

Maintenant, rendez-vous sur [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Vous verrez la documentation interactive automatique de l'API (fournie par [Swagger UI](https://github.com/swagger-api/swagger-ui)) :

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentation API alternative { #alternative-api-docs }

Et maintenant, rendez-vous sur [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

Vous verrez la documentation alternative automatique (fournie par [ReDoc](https://github.com/Rebilly/ReDoc)) :

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Mettre à niveau l'exemple { #example-upgrade }

Modifiez maintenant le fichier `main.py` pour recevoir un corps depuis une requête `PUT`.

Déclarez le corps en utilisant les types Python standard, grâce à Pydantic.

```Python hl_lines="2  7-10 23-25"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Le serveur `fastapi dev` devrait se recharger automatiquement.

### Mettre à niveau la documentation API interactive { #interactive-api-docs-upgrade }

Maintenant, rendez-vous sur [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

* La documentation interactive de l'API sera automatiquement mise à jour, y compris le nouveau corps :

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Cliquez sur le bouton « Try it out », il vous permet de renseigner les paramètres et d'interagir directement avec l'API :

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Cliquez ensuite sur le bouton « Execute », l'interface utilisateur communiquera avec votre API, enverra les paramètres, obtiendra les résultats et les affichera à l'écran :

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Mettre à niveau la documentation API alternative { #alternative-api-docs-upgrade }

Et maintenant, rendez-vous sur [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

* La documentation alternative reflètera également le nouveau paramètre de requête et le nouveau corps :

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### En résumé { #recap }

En résumé, vous déclarez **une fois** les types de paramètres, le corps, etc. en tant que paramètres de fonction.

Vous faites cela avec les types Python standard modernes.

Vous n'avez pas à apprendre une nouvelle syntaxe, les méthodes ou les classes d'une bibliothèque spécifique, etc.

Juste du **Python** standard.

Par exemple, pour un `int` :

```Python
item_id: int
```

ou pour un modèle `Item` plus complexe :

```Python
item: Item
```

... et avec cette déclaration unique, vous obtenez :

* Une assistance dans l'éditeur, notamment :
    * l'autocomplétion.
    * la vérification des types.
* La validation des données :
    * des erreurs automatiques et claires lorsque les données ne sont pas valides.
    * une validation même pour les objets JSON profondément imbriqués.
* <dfn title="également connu sous le nom de : sérialisation, parsing, marshalling">Conversion</dfn> des données d'entrée : venant du réseau vers les données et types Python. Lecture depuis :
    * JSON.
    * Paramètres de chemin.
    * Paramètres de requête.
    * Cookies.
    * En-têtes.
    * Formulaires.
    * Fichiers.
* <dfn title="également connu sous le nom de : sérialisation, parsing, marshalling">Conversion</dfn> des données de sortie : conversion des données et types Python en données réseau (au format JSON) :
    * Conversion des types Python (`str`, `int`, `float`, `bool`, `list`, etc).
    * Objets `datetime`.
    * Objets `UUID`.
    * Modèles de base de données.
    * ... et bien plus.
* Documentation API interactive automatique, avec 2 interfaces utilisateur au choix :
    * Swagger UI.
    * ReDoc.

---

Pour revenir à l'exemple de code précédent, **FastAPI** va :

* Valider la présence d'un `item_id` dans le chemin pour les requêtes `GET` et `PUT`.
* Valider que `item_id` est de type `int` pour les requêtes `GET` et `PUT`.
    * Si ce n'est pas le cas, le client verra une erreur utile et claire.
* Vérifier s'il existe un paramètre de requête optionnel nommé `q` (comme dans `http://127.0.0.1:8000/items/foo?q=somequery`) pour les requêtes `GET`.
    * Comme le paramètre `q` est déclaré avec `= None`, il est optionnel.
    * Sans le `None`, il serait requis (comme l'est le corps dans le cas de `PUT`).
* Pour les requêtes `PUT` vers `/items/{item_id}`, lire le corps au format JSON :
    * Vérifier qu'il a un attribut obligatoire `name` qui doit être un `str`.
    * Vérifier qu'il a un attribut obligatoire `price` qui doit être un `float`.
    * Vérifier qu'il a un attribut optionnel `is_offer`, qui doit être un `bool`, s'il est présent.
    * Tout cela fonctionne également pour les objets JSON profondément imbriqués.
* Convertir automatiquement depuis et vers JSON.
* Tout documenter avec OpenAPI, qui peut être utilisé par :
    * des systèmes de documentation interactive.
    * des systèmes de génération automatique de clients, pour de nombreux langages.
* Fournir directement 2 interfaces web de documentation interactive.

---

Nous n'avons fait qu'effleurer la surface, mais vous avez déjà une idée de la façon dont tout fonctionne.

Essayez de changer la ligne contenant :

```Python
    return {"item_name": item.name, "item_id": item_id}
```

... de :

```Python
        ... "item_name": item.name ...
```

... à :

```Python
        ... "item_price": item.price ...
```

... et voyez comment votre éditeur complète automatiquement les attributs et connaît leurs types :

![compatibilité éditeur](https://fastapi.tiangolo.com/img/vscode-completion.png)

Pour un exemple plus complet comprenant plus de fonctionnalités, voir le <a href="https://fastapi.tiangolo.com/fr/tutorial/">Tutoriel - Guide utilisateur</a>.

**Alerte spoiler** : le tutoriel - guide utilisateur inclut :

* Déclaration de **paramètres** provenant d'autres emplacements comme : **en-têtes**, **cookies**, **champs de formulaire** et **fichiers**.
* Comment définir des **contraintes de validation** comme `maximum_length` ou `regex`.
* Un système **<dfn title="également connu sous le nom de : composants, ressources, fournisseurs, services, injectables">d'injection de dépendances</dfn>** très puissant et facile à utiliser.
* Sécurité et authentification, y compris la prise en charge de **OAuth2** avec des **JWT tokens** et l'authentification **HTTP Basic**.
* Des techniques plus avancées (mais tout aussi faciles) pour déclarer des **modèles JSON profondément imbriqués** (grâce à Pydantic).
* Intégration **GraphQL** avec [Strawberry](https://strawberry.rocks) et d'autres bibliothèques.
* De nombreuses fonctionnalités supplémentaires (grâce à Starlette) comme :
    * **WebSockets**
    * des tests extrêmement faciles basés sur HTTPX et `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ... et plus encore.

### Déployer votre application (optionnel) { #deploy-your-app-optional }

Vous pouvez, si vous le souhaitez, déployer votre application FastAPI sur [FastAPI Cloud](https://fastapicloud.com), allez vous inscrire sur la liste d'attente si ce n'est pas déjà fait. 🚀

Si vous avez déjà un compte **FastAPI Cloud** (nous vous avons invité depuis la liste d'attente 😉), vous pouvez déployer votre application avec une seule commande.

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

C'est tout ! Vous pouvez maintenant accéder à votre application à cette URL. ✨

#### À propos de FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** est construit par le même auteur et la même équipe derrière **FastAPI**.

Il simplifie le processus de **construction**, de **déploiement** et **d'accès** à une API avec un effort minimal.

Il apporte la même **expérience développeur** de la création d'applications avec FastAPI au **déploiement** dans le cloud. 🎉

FastAPI Cloud est le principal sponsor et financeur des projets open source *FastAPI and friends*. ✨

#### Déployer sur d'autres fournisseurs cloud { #deploy-to-other-cloud-providers }

FastAPI est open source et basé sur des standards. Vous pouvez déployer des applications FastAPI sur n'importe quel fournisseur cloud de votre choix.

Suivez les guides de votre fournisseur cloud pour y déployer des applications FastAPI. 🤓

## Performance { #performance }

Les benchmarks TechEmpower indépendants montrent que les applications **FastAPI** s'exécutant sous Uvicorn sont [parmi les frameworks Python les plus rapides](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7), juste derrière Starlette et Uvicorn eux-mêmes (utilisés en interne par FastAPI). (*)

Pour en savoir plus, consultez la section [Benchmarks](https://fastapi.tiangolo.com/fr/benchmarks/).

## Dépendances { #dependencies }

FastAPI dépend de Pydantic et Starlette.

### Dépendances `standard` { #standard-dependencies }

Lorsque vous installez FastAPI avec `pip install "fastapi[standard]"`, il inclut le groupe `standard` de dépendances optionnelles :

Utilisées par Pydantic :

* [`email-validator`](https://github.com/JoshData/python-email-validator) - pour la validation des adresses e-mail.

Utilisées par Starlette :

* [`httpx`](https://www.python-httpx.org) - Obligatoire si vous souhaitez utiliser le `TestClient`.
* [`jinja2`](https://jinja.palletsprojects.com) - Obligatoire si vous souhaitez utiliser la configuration de template par défaut.
* [`python-multipart`](https://github.com/Kludex/python-multipart) - Obligatoire si vous souhaitez prendre en charge l’<dfn title="convertir la chaîne issue d'une requête HTTP en données Python">« parsing »</dfn> de formulaires avec `request.form()`.

Utilisées par FastAPI :

* [`uvicorn`](https://www.uvicorn.dev) - pour le serveur qui charge et sert votre application. Cela inclut `uvicorn[standard]`, qui comprend certaines dépendances (par ex. `uvloop`) nécessaires pour une haute performance.
* `fastapi-cli[standard]` - pour fournir la commande `fastapi`.
    * Cela inclut `fastapi-cloud-cli`, qui vous permet de déployer votre application FastAPI sur [FastAPI Cloud](https://fastapicloud.com).

### Sans les dépendances `standard` { #without-standard-dependencies }

Si vous ne souhaitez pas inclure les dépendances optionnelles `standard`, vous pouvez installer avec `pip install fastapi` au lieu de `pip install "fastapi[standard]"`.

### Sans `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

Si vous souhaitez installer FastAPI avec les dépendances standard mais sans `fastapi-cloud-cli`, vous pouvez installer avec `pip install "fastapi[standard-no-fastapi-cloud-cli]"`.

### Dépendances optionnelles supplémentaires { #additional-optional-dependencies }

Il existe des dépendances supplémentaires que vous pourriez vouloir installer.

Dépendances optionnelles supplémentaires pour Pydantic :

* [`pydantic-settings`](https://docs.pydantic.dev/latest/usage/pydantic_settings/) - pour la gestion des paramètres.
* [`pydantic-extra-types`](https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/) - pour des types supplémentaires à utiliser avec Pydantic.

Dépendances optionnelles supplémentaires pour FastAPI :

* [`orjson`](https://github.com/ijl/orjson) - Obligatoire si vous souhaitez utiliser `ORJSONResponse`.
* [`ujson`](https://github.com/esnme/ultrajson) - Obligatoire si vous souhaitez utiliser `UJSONResponse`.

## Licence { #license }

Ce projet est soumis aux termes de la licence MIT.
