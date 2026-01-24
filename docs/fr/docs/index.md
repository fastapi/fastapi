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
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation** : <a href="https://fastapi.tiangolo.com/fr" target="_blank">https://fastapi.tiangolo.com</a>

**Code Source** : <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI est un framework web moderne et rapide (haute performance) pour la création d'API avec Python, basé sur les annotations de type standard de Python.

Les principales fonctionnalités sont :

* **Rapidité** : De très hautes performances, au niveau de **NodeJS** et **Go** (grâce à Starlette et Pydantic). [L'un des frameworks Python les plus rapides](#performance).
* **Rapide à coder** : Augmente la vitesse de développement des fonctionnalités d'environ 200 % à 300 %. *
* **Moins de bugs** : Réduit d'environ 40 % les erreurs induites par le développeur. *
* **Intuitif** : Excellente compatibilité avec les IDE. <abbr title="également connu sous le nom d'auto-complétion, autocomplétion, IntelliSense">Complétion</abbr> complète. Moins de temps passé à déboguer.
* **Facile** : Conçu pour être facile à utiliser et à apprendre. Moins de temps passé à lire les documents.
* **Concis** : Diminue la duplication de code. De nombreuses fonctionnalités liées à la déclaration de chaque paramètre. Moins de bugs.
* **Robuste** : Obtenez un code prêt pour la production. Avec une documentation interactive automatique.
* **Basé sur des normes** : Basé sur (et entièrement compatible avec) les standards ouverts pour les APIs : <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (précédemment connu sous le nom de Swagger) et <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* estimation basée sur des tests d'une équipe de développement interne, construisant des applications de production.</small>

## Sponsors { #sponsors }

<!-- sponsors -->

### Sponsor Keystone { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### Sponsors Gold et Silver { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fr/fastapi-people/#sponsors" class="external-link" target="_blank">Autres sponsors</a>

## Opinions { #opinions }

"_[...] I'm using **FastAPI** a ton these days. [...] I'm actually planning to use it for all of my team's **ML services at Microsoft**. Some of them are getting integrated into the core **Windows** product and some **Office** products._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_We adopted the **FastAPI** library to spawn a **REST** server that can be queried to obtain **predictions**. [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** is pleased to announce the open-source release of our **crisis management** orchestration framework: **Dispatch**! [built with **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_I’m over the moon excited about **FastAPI**. It’s so fun!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Honestly, what you've built looks super solid and polished. In many ways, it's what I wanted **Hug** to be - it's really inspiring to see someone build that._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_If you're looking to learn one **modern framework** for building REST APIs, check out **FastAPI** [...] It's fast, easy to use and easy to learn [...]_"

"_We've switched over to **FastAPI** for our **APIs** [...] I think you'll like it [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_If anyone is looking to build a production Python API, I would highly recommend **FastAPI**. It is **beautifully designed**, **simple to use** and **highly scalable**, it has become a **key component** in our API first development strategy and is driving many automations and services such as our Virtual TAC Engineer._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## Mini-documentaire FastAPI { #fastapi-mini-documentary }

Il existe un <a href="https://www.youtube.com/watch?v=mpR8ngthqiE" class="external-link" target="_blank">mini-documentaire FastAPI</a> sorti à la fin de 2025, vous pouvez le regarder en ligne :

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE" target="_blank"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**, le FastAPI des <abbr title="Command Line Interface">CLI</abbr> { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Si vous construisez une application <abbr title="Command Line Interface">CLI</abbr> utilisable dans un terminal au lieu d'une API web, regardez <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** est le petit frère de FastAPI. Et il est destiné à être le **FastAPI des <abbr title="Command Line Interface">CLI</abbr>**. ⌨️ 🚀

## Prérequis { #requirements }

FastAPI repose sur les épaules de géants :

* <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> pour les parties web.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> pour les parties données.

## Installation { #installation }

Créez et activez un <a href="https://fastapi.tiangolo.com/fr/virtual-environments/" class="external-link" target="_blank">environnement virtuel</a> puis installez FastAPI :

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Remarque** : vous devez mettre `"fastapi[standard]"` entre guillemets pour vous assurer que cela fonctionne dans tous les terminaux.

## Exemple { #example }

### Créez-le { #create-it }

Créez un fichier `main.py` avec :

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Ou utilisez <code>async def</code>...</summary>

Si votre code utilise `async` / `await`, utilisez `async def` :

```Python hl_lines="9  14"
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

**Remarque** :

Si vous ne savez pas, consultez la section _« In a hurry? »_ à propos de <a href="https://fastapi.tiangolo.com/fr/async/#in-a-hurry" target="_blank">`async` et `await` dans les documents</a>.

</details>

### Lancez-le { #run-it }

Lancez le serveur avec :

<div class="termy">

```console
$ fastapi dev main.py

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
<summary>À propos de la commande <code>fastapi dev main.py</code>...</summary>

La commande `fastapi dev` lit votre fichier `main.py`, détecte l'app **FastAPI** qu'il contient et démarre un serveur en utilisant <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>.

Par défaut, `fastapi dev` démarre avec l'auto-reload activé pour le développement local.

Vous pouvez en savoir plus dans <a href="https://fastapi.tiangolo.com/fr/fastapi-cli/" target="_blank">la documentation de FastAPI CLI</a>.

</details>

### Vérifiez-le { #check-it }

Ouvrez votre navigateur à l'adresse <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Vous verrez la réponse JSON comme suit :

```JSON
{"item_id": 5, "q": "somequery"}
```

Vous venez de créer une API qui :

* Reçoit les requêtes HTTP pour les _chemins_ `/` et `/items/{item_id}`.
* Les deux _chemins_ acceptent des <em>opérations</em> `GET` (également connu sous le nom de _méthodes_ HTTP).
* Le _chemin_ `/items/{item_id}` a un paramètre de chemin `item_id` qui doit être un `int`.
* Le _chemin_ `/items/{item_id}` a un paramètre de requête optionnel `q` de type `str`.

### Documentation API interactive { #interactive-api-docs }

Maintenant, rendez-vous sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vous verrez la documentation interactive automatique de l'API (fournie par <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>) :

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentation API alternative { #alternative-api-docs }

Et maintenant, rendez-vous sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Vous verrez la documentation automatique alternative (fournie par <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>) :

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Mettre à niveau l'exemple { #example-upgrade }

Maintenant, modifiez le fichier `main.py` pour recevoir un corps à partir d'une requête `PUT`.

Déclarez ce corps en utilisant les types Python standards, grâce à Pydantic.

```Python hl_lines="4  9-12  25-27"
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Le serveur `fastapi dev` devrait se recharger automatiquement.

### Mettre à niveau la documentation API interactive { #interactive-api-docs-upgrade }

Maintenant, rendez-vous sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* La documentation interactive de l'API sera automatiquement mise à jour, y compris le nouveau corps :

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Cliquez sur le bouton « Try it out », il vous permet de renseigner les paramètres et d'interagir directement avec l'API :

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Cliquez ensuite sur le bouton « Execute », l'interface utilisateur communiquera avec votre API, enverra les paramètres, obtiendra les résultats et les affichera à l'écran :

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Mettre à niveau la documentation API alternative { #alternative-api-docs-upgrade }

Et maintenant, rendez-vous sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* La documentation alternative reflétera également le nouveau paramètre de requête et le corps :

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### En résumé { #recap }

En résumé, vous déclarez **une fois** les types de paramètres, le corps, etc. en tant que paramètres de fonction.

Vous faites cela avec les types Python standard modernes.

Vous n'avez pas à apprendre une nouvelle syntaxe, les méthodes ou les classes d'une bibliothèque spécifique, etc.

Juste du **Python** standard.

Par exemple, pour un `int`:

```Python
item_id: int
```

ou pour un modèle `Item` plus complexe :

```Python
item: Item
```

... et avec cette déclaration unique, vous obtenez :

* Une assistance dans votre éditeur, notamment :
    * la complétion.
    * la vérification des types.
* La validation des données :
    * des erreurs automatiques et claires lorsque les données ne sont pas valides.
    * une validation même pour les objets JSON profondément imbriqués.
* <abbr title="also known as: serialization, parsing, marshalling">Conversion</abbr> des données d'entrée : venant du réseau et allant vers les données et types de Python. Lecture de :
    * JSON.
    * Les paramètres de chemin.
    * Les paramètres de requête.
    * Les cookies.
    * Les en-têtes.
    * Les formulaires.
    * Les fichiers.
* <abbr title="also known as: serialization, parsing, marshalling">Conversion</abbr> des données de sortie : conversion des données et types Python en données réseau (au format JSON) :
    * Convertir les types Python (`str`, `int`, `float`, `bool`, `list`, etc).
    * les objets `datetime`.
    * les objets `UUID`.
    * les modèles de base de données.
    * ... et beaucoup plus.
* La documentation API interactive automatique, incluant 2 interfaces utilisateur alternatives :
    * Swagger UI.
    * ReDoc.

---

Pour revenir à l'exemple de code précédent, **FastAPI** va :

* Valider que `item_id` existe dans le chemin des requêtes `GET` et `PUT`.
* Valider que `item_id` est de type `int` pour les requêtes `GET` et `PUT`.
    * Si ce n'est pas le cas, le client verra une erreur utile et claire.
* Vérifier qu'il existe un paramètre de requête optionnel nommé `q` (comme dans `http://127.0.0.1:8000/items/foo?q=somequery`) pour les requêtes `GET`.
    * Puisque le paramètre `q` est déclaré avec `= None`, il est optionnel.
    * Sans le `None`, il serait nécessaire (comme l'est le corps dans le cas du `PUT`).
* Pour les requêtes `PUT` vers `/items/{item_id}`, lire le corps en JSON :
    * Vérifier qu'il a un attribut obligatoire `name` qui devrait être un `str`.
    * Vérifier qu'il a un attribut obligatoire `price` qui doit être un `float`.
    * Vérifier qu'il a un attribut facultatif `is_offer`, qui devrait être un `bool`, s'il est présent.
    * Tout cela fonctionnerait également pour les objets JSON profondément imbriqués.
* Convertir automatiquement depuis et vers JSON.
* Documenter tout avec OpenAPI, qui peut être utilisé par :
    * Les systèmes de documentation interactive.
    * Les systèmes de génération automatique de code client, pour de nombreuses langues.
* Fournir directement 2 interfaces web de documentation interactive.

---

Nous n'avons fait qu'effleurer la surface, mais vous avez déjà une idée de la façon dont tout cela fonctionne.

Essayez de changer la ligne contenant :

```Python
    return {"item_name": item.name, "item_id": item_id}
```

... de :

```Python
        ... "item_name": item.name ...
```

... vers :

```Python
        ... "item_price": item.price ...
```

... et voyez comment votre éditeur complétera automatiquement les attributs et connaîtra leurs types :

![compatibilité éditeur](https://fastapi.tiangolo.com/img/vscode-completion.png)

Pour un exemple plus complet comprenant plus de fonctionnalités, voir le <a href="https://fastapi.tiangolo.com/fr/tutorial/">Tutoriel - Guide utilisateur</a>.

**Spoiler alert** : le tutoriel - guide utilisateur inclut :

* Déclaration de **paramètres** provenant d'autres endroits différents comme : **en-têtes**, **cookies**, **champs de formulaire** et **fichiers**.
* Comment définir des **contraintes de validation** comme `maximum_length` ou `regex`.
* Un **système <abbr title="also known as components, resources, providers, services, injectables">Dependency Injection</abbr>** très puissant et facile à utiliser.
* Sécurité et authentification, y compris la prise en charge de **OAuth2** avec des **JWT tokens** et l'authentification **HTTP Basic**.
* Des techniques plus avancées (mais tout aussi faciles) pour déclarer des **modèles JSON profondément imbriqués** (grâce à Pydantic).
* Intégration de **GraphQL** avec <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> et d'autres bibliothèques.
* De nombreuses fonctionnalités supplémentaires (grâce à Starlette) comme :
    * **WebSockets**
    * des tests extrêmement simples basés sur HTTPX et `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ... et plus encore.

### Déployer votre app (optionnel) { #deploy-your-app-optional }

Vous pouvez éventuellement déployer votre app FastAPI sur <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>, allez vous inscrire sur la liste d'attente si ce n'est pas déjà fait. 🚀

Si vous avez déjà un compte **FastAPI Cloud** (nous vous avons invité depuis la liste d'attente 😉), vous pouvez déployer votre application avec une commande.

Avant de déployer, assurez-vous que vous êtes connecté :

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

Puis déployez votre app :

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

C'est tout ! Vous pouvez maintenant accéder à votre app à cette URL. ✨

#### À propos de FastAPI Cloud { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>** est construit par le même auteur et la même équipe derrière **FastAPI**.

Il rationalise le processus de **construction**, de **déploiement** et d'**accès** à une API avec un minimum d'effort.

Il apporte la même **expérience développeur** de construction d'apps avec FastAPI au **déploiement** dans le cloud. 🎉

FastAPI Cloud est le sponsor principal et le fournisseur de financement des projets open source *FastAPI and friends*. ✨

#### Déployer sur d'autres fournisseurs cloud { #deploy-to-other-cloud-providers }

FastAPI est open source et basé sur des normes. Vous pouvez déployer des apps FastAPI sur n'importe quel fournisseur cloud de votre choix.

Suivez les guides de votre fournisseur cloud pour y déployer des apps FastAPI. 🤓

## Performance { #performance }

Les benchmarks TechEmpower indépendants montrent que les applications **FastAPI** s'exécutant sous Uvicorn sont <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">parmi les frameworks Python disponibles les plus rapides</a>, juste derrière Starlette et Uvicorn eux-mêmes (utilisés en interne par FastAPI). (*)

Pour en savoir plus, consultez la section <a href="https://fastapi.tiangolo.com/fr/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Dépendances { #dependencies }

FastAPI dépend de Pydantic et de Starlette.

### Dépendances `standard` { #standard-dependencies }

Quand vous installez FastAPI avec `pip install "fastapi[standard]"`, il est fourni avec le groupe `standard` de dépendances optionnelles :

Utilisées par Pydantic :

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - pour la validation des adresses email.

Utilisées par Starlette :

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Obligatoire si vous souhaitez utiliser `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Obligatoire si vous souhaitez utiliser la configuration de template par défaut.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - Obligatoire si vous souhaitez supporter le <abbr title="conversion de la chaîne qui provient d'une requête HTTP en données Python">« parsing »</abbr> de formulaire, avec `request.form()`.

Utilisées par FastAPI :

* <a href="https://www.uvicorn.dev" target="_blank"><code>uvicorn</code></a> - pour le serveur qui charge et sert votre application. Cela inclut `uvicorn[standard]`, qui inclut certaines dépendances (par exemple `uvloop`) nécessaires pour un service à haute performance.
* `fastapi-cli[standard]` - pour fournir la commande `fastapi`.
    * Cela inclut `fastapi-cloud-cli`, qui vous permet de déployer votre application FastAPI sur <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>.

### Sans les dépendances `standard` { #without-standard-dependencies }

Si vous ne voulez pas inclure les dépendances optionnelles `standard`, vous pouvez installer avec `pip install fastapi` au lieu de `pip install "fastapi[standard]"`.

### Sans `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

Si vous voulez installer FastAPI avec les dépendances standard mais sans `fastapi-cloud-cli`, vous pouvez installer avec `pip install "fastapi[standard-no-fastapi-cloud-cli]"`.

### Dépendances optionnelles supplémentaires { #additional-optional-dependencies }

Il y a quelques dépendances supplémentaires que vous pourriez vouloir installer.

Dépendances optionnelles Pydantic supplémentaires :

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - pour la gestion des paramètres.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - pour les types supplémentaires à utiliser avec Pydantic.

Dépendances optionnelles FastAPI supplémentaires :

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Obligatoire si vous voulez utiliser `ORJSONResponse`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Obligatoire si vous voulez utiliser `UJSONResponse`.

## Licence { #license }

Ce projet est soumis aux termes de la licence MIT.
