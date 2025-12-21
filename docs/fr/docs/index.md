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

**Documentation** : <a href="https://fastapi.tiangolo.com/fr" target="_blank">https://fastapi.tiangolo.com/fr</a>

**Code source** : <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI est un framework web moderne et rapide (haute performance) pour la création d’API avec Python, basé sur les annotations de type standard de Python.

Les principales fonctionnalités sont :

* **Rapide** : Très hautes performances, au niveau de **NodeJS** et **Go** (grâce à Starlette et Pydantic). [L’un des frameworks Python les plus rapides](#performance).
* **Rapide à coder** : Augmente la vitesse de développement des fonctionnalités d’environ 200 % à 300 %. *
* **Moins de bugs** : Réduit d’environ 40 % les erreurs induites par le développeur. *
* **Intuitif** : Excellente prise en charge par les éditeurs. <abbr title="également connu sous le nom d’auto-complétion, autocomplétion, IntelliSense">Complétion</abbr> partout. Moins de temps passé à déboguer.
* **Facile** : Conçu pour être facile à utiliser et à apprendre. Moins de temps passé à lire la documentation.
* **Concis** : Minimise la duplication de code. Plusieurs fonctionnalités à partir de chaque déclaration de paramètre. Moins de bugs.
* **Robuste** : Obtenez du code prêt pour la production. Avec une documentation interactive automatique.
* **Basé sur des standards** : Basé sur (et entièrement compatible avec) les standards ouverts pour les API : <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (anciennement connu sous le nom de Swagger) et <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* estimation basée sur des tests d’une équipe de développement interne, construisant des applications de production.</small>

## Sponsors { #sponsors }

<!-- sponsors -->

### Sponsor clé de voûte { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### Sponsors Or et Argent { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fr/fastapi-people/#sponsors" class="external-link" target="_blank">Autres sponsors</a>

## Opinions { #opinions }

«_[...] J’utilise beaucoup **FastAPI** ces derniers temps. [...] Je prévois de l’utiliser dans mon équipe pour tous les **services de ML chez Microsoft**. Certains d’entre eux seront intégrés dans le cœur de **Windows** et dans certains produits **Office**._»

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

«_Nous avons adopté la bibliothèque **FastAPI** pour créer un serveur **REST** qui peut être interrogé pour obtenir des **prédictions**. [pour Ludwig]_»

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin et Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

«_**Netflix** a le plaisir d’annoncer la sortie en open-source de notre framework d’orchestration de **gestion de crise** : **Dispatch** ! [construit avec **FastAPI**]_»

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

«_Je suis très enthousiaste à propos de **FastAPI**. C’est un bonheur !_»

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong>Animateur du podcast <a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a></strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

«_Honnêtement, ce que vous avez construit a l’air super solide et élégant. À bien des égards, c’est comme ça que je voulais que **Hug** soit — c’est vraiment inspirant de voir quelqu’un construire ça._»

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong>Créateur de <a href="https://github.com/hugapi/hug" target="_blank">Hug</a></strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

«_Si vous cherchez à apprendre un **framework moderne** pour créer des API REST, regardez **FastAPI** [...] C’est rapide, facile à utiliser et à apprendre [...]_»

«_Nous sommes passés à **FastAPI** pour nos **API** [...] Je pense que vous l’aimerez [...]_»

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong>Fondateurs de <a href="https://explosion.ai" target="_blank">Explosion AI</a> — Créateurs de <a href="https://spacy.io" target="_blank">spaCy</a></strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

«_Si quelqu’un cherche à construire une API Python de production, je recommande vivement **FastAPI**. Il est **bien conçu**, **simple à utiliser** et **très évolutif**, il est devenu un **composant clé** dans notre stratégie de développement API first et il est à l’origine de nombreux automatismes et services tels que notre ingénieur virtuel TAC._»

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, le FastAPI des <abbr title="Command Line Interface – Interface en ligne de commande">CLI</abbr> { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Si vous souhaitez construire une application <abbr title="Command Line Interface – Interface en ligne de commande">CLI</abbr> utilisable dans un terminal au lieu d’une API web, regardez <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** est le petit frère de FastAPI. Et il est destiné à être le **FastAPI des CLI**. ⌨️ 🚀

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

**Remarque** : Assurez-vous de mettre «fastapi[standard]» entre guillemets pour garantir que cela fonctionne dans tous les terminaux.

## Exemple { #example }

### Créer { #create-it }

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

Si vous ne savez pas, consultez la section _«In a hurry?»_ à propos de <a href="https://fastapi.tiangolo.com/fr/async/#in-a-hurry" target="_blank">`async` et `await` dans la documentation</a>.

</details>

### Lancer { #run-it }

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

La commande `fastapi dev` lit votre fichier `main.py`, détecte l’application **FastAPI** qu’il contient et démarre un serveur avec <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>.

Par défaut, `fastapi dev` démarre avec le rechargement automatique activé pour le développement local.

Vous pouvez en lire davantage dans la <a href="https://fastapi.tiangolo.com/fr/fastapi-cli/" target="_blank">documentation de la CLI FastAPI</a>.

</details>

### Vérifier { #check-it }

Ouvrez votre navigateur à l’adresse <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Vous verrez la réponse JSON :

```JSON
{"item_id": 5, "q": "somequery"}
```

Vous avez déjà créé une API qui :

* Reçoit des requêtes HTTP pour les _chemins_ `/` et `/items/{item_id}`.
* Les deux _chemins_ acceptent des <em>opérations</em> `GET` (également connues comme _méthodes_ HTTP).
* Le _chemin_ `/items/{item_id}` a un _paramètre de chemin_ `item_id` qui doit être un `int`.
* Le _chemin_ `/items/{item_id}` a un _paramètre de requête_ optionnel `q` de type `str`.

### Documentation API interactive { #interactive-api-docs }

Maintenant, allez sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vous verrez la documentation API interactive automatique (fournie par <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>) :

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentation API alternative { #alternative-api-docs }

Et maintenant, allez sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Vous verrez la documentation automatique alternative (fournie par <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>) :

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Exemple de mise à niveau { #example-upgrade }

Modifiez maintenant le fichier `main.py` pour recevoir le corps d’une requête `PUT`.

Déclarez le corps en utilisant les types Python standards, grâce à Pydantic.

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

### Mise à niveau de la documentation API interactive { #interactive-api-docs-upgrade }

Maintenant, allez sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* La documentation API interactive sera automatiquement mise à jour, y compris le nouveau corps :

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Cliquez sur le bouton «Try it out», il vous permet de renseigner les paramètres et d’interagir directement avec l’API :

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Cliquez ensuite sur le bouton «Execute», l’interface utilisateur communiquera avec votre API, enverra les paramètres, obtiendra les résultats et les affichera à l’écran :

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Mise à niveau de la documentation API alternative { #alternative-api-docs-upgrade }

Et maintenant, allez sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* La documentation alternative reflètera également le nouveau paramètre de requête et le nouveau corps :

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Récapitulatif { #recap }

En résumé, vous déclarez **une fois** les types de paramètres, le corps, etc. comme paramètres de fonction.

Vous faites cela avec les types Python modernes standards.

Vous n’avez pas à apprendre une nouvelle syntaxe, les méthodes ou classes d’une bibliothèque spécifique, etc.

Juste du **Python** standard.

Par exemple, pour un `int` :

```Python
item_id: int
```

ou pour un modèle `Item` plus complexe :

```Python
item: Item
```

... et avec cette seule déclaration vous obtenez :

* Assistance de l’éditeur, notamment :
    * Complétion.
    * Vérifications de type.
* Validation des données :
    * Des erreurs automatiques et claires lorsque les données ne sont pas valides.
    * Une validation même pour des objets JSON profondément imbriqués.
* <abbr title="également connu sous le nom de : sérialisation, analyse, marshalling">Conversion</abbr> des données d’entrée : depuis le réseau vers les données et types Python. Lecture depuis :
    * JSON.
    * Paramètres de chemin.
    * Paramètres de requête.
    * Cookies.
    * En-têtes.
    * Formulaires.
    * Fichiers.
* <abbr title="également connu sous le nom de : sérialisation, analyse, marshalling">Conversion</abbr> des données de sortie : conversion des données et types Python en données réseau (au format JSON) :
    * Conversion des types Python (`str`, `int`, `float`, `bool`, `list`, etc).
    * Objets `datetime`.
    * Objets `UUID`.
    * Modèles de base de données.
    * ... et bien plus.
* Documentation API interactive automatique, avec 2 interfaces utilisateur alternatives :
    * Swagger UI.
    * ReDoc.

---

Pour revenir à l’exemple de code précédent, **FastAPI** va :

* Valider la présence d’un `item_id` dans le chemin pour les requêtes `GET` et `PUT`.
* Valider que `item_id` est de type `int` pour les requêtes `GET` et `PUT`.
    * Si ce n’est pas le cas, le client verra une erreur utile et claire.
* Vérifier s’il existe un paramètre de requête optionnel nommé `q` (comme dans `http://127.0.0.1:8000/items/foo?q=somequery`) pour les requêtes `GET`.
    * Comme le paramètre `q` est déclaré avec `= None`, il est optionnel.
    * Sans le `None`, il serait requis (comme l’est le corps dans le cas du `PUT`).
* Pour les requêtes `PUT` vers `/items/{item_id}`, lire le corps en JSON :
    * Vérifier qu’il possède un attribut obligatoire `name` qui doit être un `str`.
    * Vérifier qu’il possède un attribut obligatoire `price` qui doit être un `float`.
    * Vérifier qu’il possède un attribut optionnel `is_offer`, qui doit être un `bool`, s’il est présent.
    * Tout cela fonctionnerait également pour des objets JSON profondément imbriqués.
* Convertir depuis et vers JSON automatiquement.
* Tout documenter avec OpenAPI, qui peut être utilisé par :
    * Des systèmes de documentation interactive.
    * Des systèmes de génération automatique de code client, pour de nombreuses langues.
* Fournir directement 2 interfaces web de documentation interactive.

---

Nous n’avons fait qu’effleurer la surface, mais vous comprenez déjà l’idée de fonctionnement général.

Essayez de changer la ligne :

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

... et voyez comment votre éditeur complètera automatiquement les attributs et connaîtra leurs types :

![compatibilité éditeur](https://fastapi.tiangolo.com/img/vscode-completion.png)

Pour un exemple plus complet incluant davantage de fonctionnalités, voir le <a href="https://fastapi.tiangolo.com/fr/tutorial/">Tutoriel - Guide utilisateur</a>.

**Alerte spoiler** : le tutoriel - guide utilisateur inclut :

* Déclaration de **paramètres** provenant d’autres endroits tels que : **en-têtes**, **cookies**, **champs de formulaire** et **fichiers**.
* Comment définir des **contraintes de validation** comme `maximum_length` ou `regex`.
* Un système de **<abbr title="également connu sous le nom de composants, ressources, fournisseurs, services, injectables">Injection de dépendances</abbr>** très puissant et facile à utiliser.
* Sécurité et authentification, y compris la prise en charge de **OAuth2** avec les **jetons <abbr title="JSON Web Tokens">JWT</abbr>** et l’authentification **HTTP Basic**.
* Des techniques plus avancées (mais tout aussi simples) pour déclarer des **modèles JSON profondément imbriqués** (grâce à Pydantic).
* Intégration **GraphQL** avec <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> et d’autres bibliothèques.
* De nombreuses fonctionnalités supplémentaires (grâce à Starlette) comme :
    * **WebSockets**
    * des tests extrêmement faciles basés sur HTTPX et `pytest`
    * **CORS**
    * **Sessions Cookie**
    * ... et plus encore.

### Déployer votre application (optionnel) { #deploy-your-app-optional }

Vous pouvez éventuellement déployer votre application FastAPI sur <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>, allez vous inscrire sur la liste d’attente si ce n’est pas déjà fait. 🚀

Si vous avez déjà un compte **FastAPI Cloud** (nous vous avons invité depuis la liste d’attente 😉), vous pouvez déployer votre application avec une seule commande.

Avant de déployer, assurez-vous d’être connecté :

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

Puis déployez votre application :

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

C’est tout ! Vous pouvez maintenant accéder à votre application à cette URL. ✨

#### À propos de FastAPI Cloud { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>** est créé par le même auteur et la même équipe derrière **FastAPI**.

Il simplifie le processus de **construction**, de **déploiement** et d’**accès** à une API avec un minimum d’efforts.

Il apporte la même **expérience développeur** de la création d’applications avec FastAPI au **déploiement** dans le cloud. 🎉

FastAPI Cloud est le sponsor principal et le financeur des projets open source *FastAPI and friends*. ✨

#### Déployer sur d’autres fournisseurs cloud { #deploy-to-other-cloud-providers }

FastAPI est open source et basé sur des standards. Vous pouvez déployer des applications FastAPI sur n’importe quel fournisseur cloud de votre choix.

Suivez les guides de votre fournisseur cloud pour y déployer des applications FastAPI. 🤓

## Performance { #performance }

Les benchmarks indépendants TechEmpower montrent que les applications **FastAPI** s’exécutant sous Uvicorn sont <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">parmi les frameworks Python les plus rapides</a>, juste derrière Starlette et Uvicorn eux-mêmes (utilisés en interne par FastAPI). (*)

Pour en savoir plus, consultez la section <a href="https://fastapi.tiangolo.com/fr/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Dépendances { #dependencies }

FastAPI dépend de Pydantic et Starlette.

### Dépendances `standard` { #standard-dependencies }

Lorsque vous installez FastAPI avec `pip install "fastapi[standard]"`, cela inclut le groupe `standard` de dépendances optionnelles :

Utilisées par Pydantic :

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> — pour la validation des adresses email.

Utilisées par Starlette :

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> — requis si vous souhaitez utiliser `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> — requis si vous souhaitez utiliser la configuration de template par défaut.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> — requis si vous souhaitez prendre en charge l’<abbr title="conversion de la chaîne provenant d’une requête HTTP en données Python">«décodage»</abbr> de formulaires avec `request.form()`.

Utilisées par FastAPI :

* <a href="https://www.uvicorn.dev" target="_blank"><code>uvicorn</code></a> — pour le serveur qui charge et sert votre application. Cela inclut `uvicorn[standard]`, qui comprend certaines dépendances (par ex. `uvloop`) nécessaires pour un service à haute performance.
* `fastapi-cli[standard]` — pour fournir la commande `fastapi`.
    * Cela inclut `fastapi-cloud-cli`, qui vous permet de déployer votre application FastAPI sur <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>.

### Sans dépendances `standard` { #without-standard-dependencies }

Si vous ne souhaitez pas inclure les dépendances optionnelles `standard`, vous pouvez installer avec `pip install fastapi` au lieu de `pip install "fastapi[standard]"`.

### Sans `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

Si vous souhaitez installer FastAPI avec les dépendances standard mais sans `fastapi-cloud-cli`, vous pouvez installer avec `pip install "fastapi[standard-no-fastapi-cloud-cli]"`.

### Autres dépendances optionnelles { #additional-optional-dependencies }

Il existe des dépendances supplémentaires que vous pourriez vouloir installer.

Dépendances optionnelles supplémentaires pour Pydantic :

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> — pour la gestion des paramètres.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> — pour des types supplémentaires à utiliser avec Pydantic.

Dépendances optionnelles supplémentaires pour FastAPI :

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> — requis si vous souhaitez utiliser `ORJSONResponse`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> — requis si vous souhaitez utiliser `UJSONResponse`.

## Licence { #license }

Ce projet est soumis aux termes de la licence MIT.
