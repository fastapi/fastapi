<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>Framework FastAPI, haute performance, facile à apprendre, rapide à coder, prêt pour la production</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation** : <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Code Source** : <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI est un framework web moderne et rapide (haute performance) pour la création d'API avec Python 3.7+, basé sur les annotations de type standard de Python.

Les principales fonctionnalités sont :

* **Rapidité** : De très hautes performances, au niveau de **NodeJS** et **Go** (grâce à Starlette et Pydantic). [L'un des frameworks Python les plus rapides](#performance).
* **Rapide à coder** : Augmente la vitesse de développement des fonctionnalités d'environ 200 % à 300 %. *
* **Moins de bugs** : Réduit d'environ 40 % les erreurs induites par le développeur. *
* **Intuitif** : Excellente compatibilité avec les IDE. <abbr title="également connu sous le nom d'auto-complétion, autocomplétion, IntelliSense">Complétion</abbr> complète. Moins de temps passé à déboguer.
* **Facile** : Conçu pour être facile à utiliser et à apprendre. Moins de temps passé à lire la documentation.
* **Concis** : Diminue la duplication de code. De nombreuses fonctionnalités liées à la déclaration de chaque paramètre. Moins de bugs.
* **Robuste** : Obtenez un code prêt pour la production. Avec une documentation interactive automatique.
* **Basé sur des normes** : Basé sur (et entièrement compatible avec) les standards ouverts pour les APIs : <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (précédemment connu sous le nom de Swagger) et <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* estimation basée sur des tests d'une équipe de développement interne, construisant des applications de production.</small>

## Sponsors

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Other sponsors</a>

## Opinions

"_[...] J'utilise beaucoup **FastAPI** ces derniers temps. [...] Je prévois de l'utiliser dans mon équipe pour tous les **services de ML chez Microsoft**. Certains d'entre eux seront intégrés dans le coeur de **Windows** et dans certains produits **Office**._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_Nous avons adopté la bibliothèque **FastAPI** pour créer un serveur **REST** qui peut être interrogé pour obtenir des **prédictions**. [pour Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin et Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** a le plaisir d'annoncer la sortie en open-source de notre framework d'orchestration de **gestion de crise** : **Dispatch** ! [construit avec **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Je suis très enthousiaste à propos de **FastAPI**. C'est un bonheur !_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong>Auteur du podcast <a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a></strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Honnêtement, ce que vous avez construit a l'air super solide et élégant. A bien des égards, c'est comme ça que je voulais que **Hug** soit - c'est vraiment inspirant de voir quelqu'un construire ça._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong> Créateur de <a href="https://www.hug.rest/" target="_blank">Hug</a></strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Si vous cherchez à apprendre un **framework moderne** pour créer des APIs REST, regardez **FastAPI** [...] C'est rapide, facile à utiliser et à apprendre [...]_"

"_Nous sommes passés à **FastAPI** pour nos **APIs** [...] Je pense que vous l'aimerez [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong>Fondateurs de <a href="https://explosion.ai" target="_blank">Explosion AI</a> - Créateurs de <a href="https://spacy.io" target="_blank">spaCy</a></strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_Si quelqu'un cherche à construire une API Python de production, je recommande vivement **FastAPI**. Il est **bien conçu**, **simple à utiliser** et **très évolutif**. Il est devenu un **composant clé** dans notre stratégie de développement API first et il est à l'origine de nombreux automatismes et services tels que notre ingénieur virtuel TAC._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, le FastAPI des <abbr title="Command Line Interface">CLI</abbr>

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Si vous souhaitez construire une application <abbr title="Command Line Interface">CLI</abbr> utilisable dans un terminal au lieu d'une API web, regardez <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** est le petit frère de FastAPI. Et il est destiné à être le **FastAPI des <abbr title="Command Line Interface">CLI</abbr>**. ⌨️ 🚀

## Prérequis

Python 3.7+

FastAPI repose sur les épaules de géants :

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> pour les parties web.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> pour les parties données.

## Installation

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Vous aurez également besoin d'un serveur ASGI pour la production tel que <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> ou <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## Exemple

### Créez

* Créez un fichier `main.py` avec :

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
<summary>Ou utilisez <code>async def</code> ...</summary>

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

**Note**

Si vous n'êtes pas familier avec cette notion, consultez la section _"Vous êtes pressés ?"_ à propos de <a href="https://fastapi.tiangolo.com/fr/async/#vous-etes-presses" target="_blank">`async` et `await` dans la documentation</a>.

</details>

### Lancez

Lancez le serveur avec :

<div class="termy">

```console
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>À propos de la commande <code>uvicorn main:app --reload</code> ...</summary>

La commande `uvicorn main:app` fait référence à :

* `main` : le fichier `main.py` (le "module" Python).
* `app` : l'objet créé à l'intérieur de `main.py` avec la ligne `app = FastAPI()`.
* `--reload` : fait redémarrer le serveur après des changements de code. À n'utiliser que pour le développement.

</details>

### Vérifiez

Ouvrez votre navigateur à l'adresse <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Vous obtenez alors cette réponse <abbr title="JavaScript Object Notation">JSON</abbr> :

```JSON
{"item_id": 5, "q": "somequery"}
```

Vous venez de créer une API qui :

* Reçoit les requêtes HTTP pour les _chemins_ `/` et `/items/{item_id}`.
* Les deux _chemins_ acceptent des <em>opérations</em> `GET` (également connu sous le nom de _méthodes_ HTTP).
* Le _chemin_ `/items/{item_id}` a un  _<abbr title="en anglais : path parameter">paramètre</abbr>_ `item_id` qui doit être un `int`.
* Le _chemin_ `/items/{item_id}` a un _<abbr title="en anglais : query param">paramètre de requête</abbr>_ optionnel `q` de type `str`.

### Documentation API interactive

Maintenant, rendez-vous sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vous verrez la documentation interactive automatique de l'API (fournie par <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>) :

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentation API alternative

Et maintenant, rendez-vous sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Vous verrez la documentation interactive automatique de l'API (fournie par <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>) :

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Exemple plus poussé

Maintenant, modifiez le fichier `main.py` pour recevoir <abbr title="en anglais : body">le corps</abbr> d'une requête `PUT`.

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

Le serveur se recharge normalement automatiquement (car vous avez pensé à `--reload` dans la commande `uvicorn` ci-dessus).

### Plus loin avec la documentation API interactive

Maintenant, rendez-vous sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* La documentation interactive de l'API sera automatiquement mise à jour, y compris le nouveau corps de la requête :

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Cliquez sur le bouton "Try it out", il vous permet de renseigner les paramètres et d'interagir directement avec l'API :

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Cliquez ensuite sur le bouton "Execute", l'interface utilisateur communiquera avec votre API, enverra les paramètres, obtiendra les résultats et les affichera à l'écran :

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Plus loin avec la documentation API alternative

Et maintenant, rendez-vous sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* La documentation alternative reflétera également le nouveau paramètre de requête et le nouveau corps :

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### En résumé

En résumé, vous déclarez **une fois** les types de paramètres, <abbr title="en anglais : body">le corps</abbr>  de la requête, etc. en tant que paramètres de fonction.

Vous faites cela avec les types Python standard modernes.

Vous n'avez pas à apprendre une nouvelle syntaxe, les méthodes ou les classes d'une bibliothèque spécifique, etc.

Juste du **Python 3.7+** standard.

Par exemple, pour un `int`:

```Python
item_id: int
```

ou pour un modèle `Item` plus complexe :

```Python
item: Item
```

... et avec cette déclaration unique, vous obtenez :

* Une assistance dans votre IDE, notamment :
    * la complétion.
    * la vérification des types.
* La validation des données :
    * des erreurs automatiques et claires lorsque les données ne sont pas valides.
    * une validation même pour les objets <abbr title="JavaScript Object Notation">JSON</abbr> profondément imbriqués.
* <abbr title="aussi connu sous le nom de : serialization, parsing, marshalling">Une conversion</abbr> des données d'entrée : venant du réseau et allant vers les données et types de Python, permettant de lire :
    * le <abbr title="JavaScript Object Notation">JSON</abbr>.
    * <abbr title="en anglais : path parameters">les paramètres du chemin</abbr>.
    * <abbr title="en anglais : query parameters">les paramètres de la requête</abbr>.
    * les cookies.
    * <abbr title="en anglais : headers">les en-têtes</abbr>.
    * <abbr title="en anglais : forms">les formulaires</abbr>.
    * <abbr title="en anglais : files">les fichiers</abbr>.
* <abbr title="aussi connu sous le nom de : serialization, parsing, marshalling">La conversion</abbr> des données de sortie : conversion des données et types Python en données réseau (au format <abbr title="JavaScript Object Notation">JSON</abbr>), permettant de convertir :
    * les types Python (`str`, `int`, `float`, `bool`, `list`, etc).
    * les objets `datetime`.
    * les objets `UUID`.
    * les modèles de base de données.
    * ... et beaucoup plus.
* La documentation API interactive automatique, avec 2 interfaces utilisateur au choix :
    * Swagger UI.
    * ReDoc.

---

Pour revenir à l'exemple de code précédent, **FastAPI** permet de :

* Valider que `item_id` existe dans le chemin des requêtes `GET` et `PUT`.
* Valider que `item_id` est de type `int` pour les requêtes `GET` et `PUT`.
    * Si ce n'est pas le cas, le client voit une erreur utile et claire.
* Vérifier qu'il existe un paramètre de requête facultatif nommé `q` (comme dans `http://127.0.0.1:8000/items/foo?q=somequery`) pour les requêtes `GET`.
    * Puisque le paramètre `q` est déclaré avec `= None`, il est facultatif.
    * Sans le `None`, il serait nécessaire (comme l'est <abbr title="en anglais : body">le corps</abbr> de la requête dans le cas du `PUT`).
* Pour les requêtes `PUT` vers `/items/{item_id}`, de lire <abbr title="en anglais : body">le corps</abbr>  en <abbr title="JavaScript Object Notation">JSON</abbr> :
    * Vérifier qu'il a un attribut obligatoire `name` qui devrait être un `str`.
    * Vérifier qu'il a un attribut obligatoire `prix` qui doit être un `float`.
    * Vérifier qu'il a un attribut facultatif `is_offer`, qui devrait être un `bool`, s'il est présent.
    * Tout cela fonctionnerait également pour les objets <abbr title="JavaScript Object Notation">JSON</abbr> profondément imbriqués.
* Convertir de et vers <abbr title="JavaScript Object Notation">JSON</abbr> automatiquement.
* Documenter tout avec OpenAPI, qui peut être utilisé par :
    * Les systèmes de documentation interactifs.
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

![compatibilité IDE](https://fastapi.tiangolo.com/img/vscode-completion.png)

Pour un exemple plus complet comprenant plus de fonctionnalités, voir le <a href="https://fastapi.tiangolo.com/fr/tutorial/">Tutoriel - Guide utilisateur</a>.

**Spoiler alert** : le tutoriel - guide utilisateur inclut :

* Déclaration de **paramètres** provenant d'autres endroits différents comme : **<abbr title="en anglais : headers">en-têtes</abbr>.**, **cookies**, **champs de formulaire** et **fichiers**.
* L'utilisation de **contraintes de validation** comme `maximum_length` ou `regex`.
* Un **<abbr title="aussi connu sous le nom de composants, ressources, fournisseurs, services, injectables">systéme d'injection de dépendance </abbr>** très puissant et facile à utiliser .
* Sécurité et authentification, y compris la prise en charge de **OAuth2** avec les **<abbr title="en anglais : JWT tokens">jetons <abbr title="JSON Web Tokens">JWT</abbr></abbr>** et l'authentification **HTTP Basic**.
* Des techniques plus avancées (mais tout aussi faciles) pour déclarer les **modèles <abbr title="JavaScript Object Notation">JSON</abbr> profondément imbriqués** (grâce à Pydantic).
* Intégration de **GraphQL** avec <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> et d'autres bibliothèques.
* D'obtenir de nombreuses fonctionnalités supplémentaires (grâce à  Starlette) comme :
    * **WebSockets**
    * de tester le code très facilement avec `requests` et `pytest`
    * **<abbr title="Cross-Origin Resource Sharing">CORS</abbr>**
    * **Cookie Sessions**
    * ... et plus encore.

## Performance

Les benchmarks TechEmpower indépendants montrent que les applications **FastAPI** s'exécutant sous Uvicorn sont <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank"> parmi les frameworks existants en Python les plus rapides </a>, juste derrière Starlette et Uvicorn (utilisés en interne par FastAPI). (*)

Pour en savoir plus, consultez la section <a href="https://fastapi.tiangolo.com/fr/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Dépendances facultatives

Utilisées par Pydantic:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - pour la validation des adresses email.

Utilisées par Starlette :

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - Obligatoire si vous souhaitez utiliser `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Obligatoire si vous souhaitez utiliser la configuration de template par defaut.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Obligatoire si vous souhaitez supporter le <abbr title="convertit la chaine de caractère d'une requête HTTP en donnée Python">"décodage"</abbr> de formulaire avec `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Obligatoire pour la prise en charge de `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Obligatoire pour le support `SchemaGenerator` de Starlette (vous n'en avez probablement pas besoin avec FastAPI).
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Obligatoire si vous souhaitez utiliser `UJSONResponse`.

Utilisées par FastAPI / Starlette :

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - Pour le serveur qui charge et sert votre application.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Obligatoire si vous voulez utiliser `ORJSONResponse`.

Vous pouvez tout installer avec `pip install fastapi[all]`.

## Licence

Ce projet est soumis aux termes de la licence MIT.
