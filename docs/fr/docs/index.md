<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, high performance, easy to learn, fast to code, ready for production</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---

**Documentation** : <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Code Source** : <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI est un framework web moderne et rapide (haute performance) pour la construction d'API avec Python 3.6+, basé sur des annotations de type Python standard.

Les principales fonctionnalités sont:

* **Rapide** : Très haute performance, à égalité avec **NodeJS** et **Go** (merci à Starlette et Pydantic). [L'un des framework Python les plus rapides disponibles](#performance).

* **Rapide à coder** : Augmenter la vitesse de développement des fonctionnalités d'environ 200 % à 300 %. *
* **Moins de bugs** : Réduire d'environ 40 % les erreurs humaines (de développement). *
* **Intuitif** : Excellente compatibilité avec les IDE. <abbr title="également connu sous le nom d'auto-complétion, autocomplétion, IntelliSense">Complétion</abbr> complète. Moins de temps pour le débogage.
* **Facile** : Conçu pour être facile à utiliser et à apprendre. Moins de temps à lire la documentation.
* **Concit** : Minimise la duplication des codes. Plusieurs fonctionnalités pour chaque déclaration de paramètres. Moins de bogues.
* **Robuste** : Obtenez un code prêt pour la production. Avec une documentation interactive automatique.
* **Basé sur des normes** : Basé sur (et entièrement compatible avec) les normes ouvertes pour les API : <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (précédemment connu sous le nom de Swagger) et <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* estimation basée sur des tests sur une équipe de développement interne, construisant des applications de production.</small>

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

"_[...] J'utilise énormément **FastAPI** ces jours-ci. [...] En fait, je compte l'utiliser dans mon équipe pour tous les **services de ML chez Microsoft**. Certains d'entre eux sont intégrés dans le produit de base **Windows** et dans certains produits **Office**._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_Nous avons adopté la bibliothèque **FastAPI** pour créer un serveur **REST** qui peut être interrogé pour obtenir des **prédictions**. [pour Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, et Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** a le plaisir d'annoncer la sortie en open-source de notre framework d'orchestration de **gestion de crise** : **Dispatch**! [construit avec **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Je suis aux anges avec **FastAPI**. C'est tellement amusant !_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> animateur de podcast</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Honnêtement, ce que vous avez construit a l'air super solide et poli. A bien des égards, c'est comme ça que je voulais que **Hug** soit - c'est vraiment inspirant de voir quelqu'un construire ça._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> créateur</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Si vous cherchez à apprendre un **framework moderne** pour la construction d'API REST, consultez **FastAPI** [...] C'est rapide, facile à utiliser et facile à apprendre [...]_"

"_Nous sommes passés à **FastAPI** pour nos **APIs** [...] Je pense que vous allez aimer [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> fondateurs - <a href="https://spacy.io" target="_blank">spaCy</a> créateurs</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, l'équivalent de FastAPI pour les CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Si vous construisez application <abbr title="Command Line Interface">CLI</abbr> à utiliser dans le terminal au lieu d'une API web, consultez <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** est le petit frère de FastAPI. Et il est destiné à être **l'équivalent de FastAPI pour les CLIs**. ⌨️ 🚀

## Prérequis

Python 3.6+

FastAPI se tient sur les épaules des géants:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> pour les parties web.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> pour les parties données.

## Installation

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Vous aurez également besoin d'un serveur ASGI, pour des productions telles que <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> ou <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## Exemple

### Créez-le

* Créez un fichier `main.py` avec:

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

```Python hl_lines="9 14"
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

**Note** :

Si vous ne savez pas, consultez la section _"Vous êtes pressé ?"_ <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">sur `async` et `await` dans la documentation</a>.

</details>

### Lancez-le

Exécutez le serveur avec :

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
<summary>À propos de la commande <code>uvicorn main:app --reload</code>...</summary>

La commande `uvicorn main:app` fait référence à :

* `main`: le fichier `main.py` (le module Python).
* `app`: l'objet créé à l'intérieur de `main.py` avec la ligne `app = FastAPI()`.
* `--reload`: fait redémarrer le serveur après les changements de code. Ne faites cela que pour le développement.

</details>

### Vérifiez le

Ouvrez votre navigateur à l'adresse <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Vous verrez la réponse JSON:

```JSON
{"item_id": 5, "q": "somequery"}
```

Vous avez déjà créé une API qui :

* Reçoit les requêtes HTTP sur les URL `/` et `/items/{item_id}`.
* Les deux _URL_ prennent `GET` <em>opérations</em> (également connu sous le nom de _méthodes_ HTTP).
* L'_URL_ `/items/{item_id}` a un paramètre `item_id` qui doit être un `int`.
* L' _URL_ `/items/{item_id}` a un _paramètre de requête_ `str` optionnel `q`.

### Documents API interactifs

Maintenant, rendez-vous sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vous verrez la documentation interactive automatique de l'API (fournie par <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentation alternative sur les API

Et maintenant, rendez-vous sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Vous verrez la documentation automatique alternative (fournie par <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Mise à jour de l'exemple

Maintenant, modifiez le fichier `main.py` pour recevoir le corps de la requête (body) à partir d'une requête `PUT`.

Déclarer le corps de la requête en utilisant les types de Python standard, grâce à Pydantic.

```Python hl_lines="4  9 10 11 12  25 26 27"
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

Le serveur devrait se recharger automatiquement (parce que vous avez ajouté `--reload` à la commande `uvicorn` ci-dessus).

### Mise à jour de la documentation interactive de l'API

Maintenant, rendez-vous sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* La documentation interactive de l'API sera automatiquement mise à jour, y compris le nouveau corps de la requête :

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Cliquez sur le bouton "Try it out", il vous permet de remplir les paramètres et d'interagir directement avec l'API :

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Cliquez ensuite sur le bouton "Execute", l'interface utilisateur communiquera avec votre API, enverra les paramètres, obtiendra les résultats et les affichera à l'écran :

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Mise à jour de la documentation alternative de l'API

Et maintenant, rendez-vous sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* La documentation alternative reflétera également le nouveau paramètre et le nouveau corps de la requête :

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Récapitulatif

En résumé, vous déclarez **une fois** les types de paramètres, le corps de la requête, etc. comme paramètres de fonction.

Vous faites cela avec des types Python standard modernes.

Vous n'avez pas à apprendre une nouvelle syntaxe, les méthodes ou les classes d'une bibliothèque spécifique, etc.

Juste du **Python 3.6+** standard.

Par exemple, pour un `int` :

```Python
item_id: int
```

ou pour un modèle `Item` plus complexe :

```Python
item: Item
```

...et avec cette déclaration unique, vous obtenez :

* La prise en charge de l'éditeur, notamment :
    * Complétion.
    * Contrôles de type.
* Validation des données :
    * Erreurs automatiques et claires lorsque les données ne sont pas valables.
    * Une validation même pour les objets JSON profondément imbriqués.
* <abbr title="également connu sous le nom de : serialization, parsing, marshalling">Conversion</abbr> des données d'entrée : provenant du réseau en données et types Python. Lecture à partir de :
    * JSON.
    * Path parameters.
    * Query parameters.
    * Cookies.
    * Headers.
    * Forms.
    * Files.
* <abbr title="également connu sous le nom de : serialization, parsing, marshalling">Conversion</abbr> des données de sortie : conversion de données et de types Python en données de réseau (JSON) :
    * Conversion des types Python (`str`, `int`, `float`, `bool`, `list`, etc).
    * objets `datetime`.
    * objets `UUID`.
    * Modèles de bases de données.
    * ...et bien d'autres encore.
* Documentation d'API interactive automatique, comprenant 2 interfaces utilisateur alternatives :
    * Swagger UI.
    * ReDoc.

---

Pour revenir à l'exemple de code précédent, **FastAPI** fera :

* La validation de la présence de `item_id` dans le chemin pour les requêtes `GET` et `PUT`.
* La validation que `item_id` est de type `int` pour les requêtes `GET` et `PUT`.
    * Si ce n'est pas le cas, le client verra une erreur utile et claire.
* La vérification qu'il existe un paramètre facultatif nommé `q` (comme sur `http://127.0.0.1:8000/items/foo?q=somequery`) pour les requêtes `GET`.
    * Comme le paramètre `q` est déclaré avec `= None`, il est optionnel.
    * Sans le `None`, il serait nécessaire (comme l'est le corps de la requête dans le cas du `PUT`).
* Pour les requêtes `PUT` sur `/items/{item_id}`, lit le corps de la requête comme du JSON :
    * Vérifiez qu'il possède un attribut requis `name` qui devrait être un `str`.
    * Vérifiez qu'il possède un attribut requis `price` qui devrait être un `float`.
    * Vérifiez qu'il possède un attribut optionnel `is_offer`, qui devrait être un `bool`, si il est présent.
    * Tout cela fonctionne également pour les objets JSON profondément imbriqués.
* Conversion automatique de et vers JSON.
* Documente tout avec OpenAPI, qui peut être utilisé par :
    * Les systèmes de documentation interactifs.
    * Les systèmes de génération automatique de code client, pour de nombreuses langues.
* Fournir directement deux interfaces web de documentation interactive.

---

Nous n'avons fait qu'effleurer la surface, mais vous avez déjà une idée de la façon dont tout cela fonctionne.

Essayez de changer la ligne avec :

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...de :

```Python
        ... "item_name": item.name ...
```

...vers :

```Python
        ... "item_price": item.price ...
```

...et voyez comment votre éditeur complétera automatiquement les attributs et connaîtra leurs types :

![compatibilité IDE](https://fastapi.tiangolo.com/img/vscode-completion.png)

Pour un exemple plus complet comprenant plus de fonctionnalités, voir le <a href="https://fastapi.tiangolo.com/tutorial/">Tutoriel - Guide utilisateur</a>.

**Spoiler alert** : le tutoriel - guide utilisateur inclut :

* Déclaration de **paramètres** à des endroits différents comme : **en-têtes**, **cookies**, **champs de formulaire** et **fichiers**.
* Comment définir les **contraintes de validation** comme `maximum_length` ou `regex`.
* Un system très puissant et facile à utiliser d'**<abbr title="également connu sous le nom de components, resources, providers, services, injectables">injection de dépendance</abbr>**.
* Sécurité et authentification, y compris la prise en charge de **OAuth2** avec les **JWT tokens** et l'authentification **HTTP Basic**.
* Des techniques plus avancées (mais tout aussi faciles) pour déclarer les **modèles JSON profondément imbriqués** (merci à Pydantic).
* De nombreuses fonctionnalités supplémentaires (merci à Starlette) comme :
    * **WebSockets**
    * **GraphQL**
    * des tests extrêmement faciles basés sur `requests` et `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...et plus encore.

## Performance

Des analyses comparatives indépendantes de TechEmpower montrent que les applications **FastAPI** fonctionnant sous Uvicorn ont <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">l'un des framework Python les plus rapides disponibles</a>, uniquement en dessous de Starlette et Uvicorn eux-mêmes (utilisé en interne par FastAPI). (*)

Pour en savoir plus, consultez la rubrique <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Dépendances facultatives

Utilisées par Pydantic :

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - pour un <abbr title="conversion de la chaîne qui provient d'une requête HTTP en données Python">parsing</abbr> JSON plus rapide.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - pour la validation d'une adresse électronique.

Utilisées par Starlette :

* <a href="https://docs.python-requests.org" target="_blank"><code>requests</code></a> - Requis si vous souhaitez utiliser le `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Requis si vous souhaitez utiliser la configuration de template par defaut.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Requis si vous voulez supporter le  <abbr title="la conversion de la chaîne qui provient d'une requête HTTP en données Python">parsing</abbr> des formulaires avec `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Requis pour le support de `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Requis pour le support de `SchemaGenerator` de Starlette (vous n'en avez probablement pas besoin avec FastAPI).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Requis pour le support de `GraphQLApp` .
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Requis si vous voulez utiliser `UJSONResponse`.

Utilisées par FastAPI / Starlette :

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - pour le serveur qui charge et sert votre application.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Requis si vous voulez utiliser `ORJSONResponse`.

Vous pouvez tout installer avec `pip install fastapi[all]`.

## Licence

Ce projet est soumis aux termes de la licence MIT.
