
{!../../../docs/missing-translation.md!}


<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>Framework FastAPI, haute performance, facile à apprendre, rapide à coder, prêt pour la production</em>
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

**Documentation**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Code source**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI est un framework Web moderne, rapide (hautes performances) pour la création d'API avec Python 3.6+ basé sur le type hints de  Python standard.

Ces caractéristiques clés sont :

* **Rapide**: De trê hautes performances , à égalité avec **NodeJS** et **Go** (grace à Starlette et Pydantic). [l'une des framorks python les plus rapides](#performance).

* **Rapide à coder**: augmente ta productivité jusqu'a 200% à 300%. *
* **moins de bugs**: Réduis environ 40 % des erreurs induites par le développeur *
* **Intuitive**: Excellent support pour les éditeurs de code. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Complétiton</abbr> partout. moins de temps pour le débogage.
* **Facile**: conçu pour être facile à apprendre et à utiliser.moins de temps pour lire la documentation.
* **court**: diminue la duplication de code.plusie Fonctionnalités multiples de chaque déclaration de paramètre. moins de bugs.
* **Robuste**: code prêt pour la production. avec une documentation interactive automatique(Openapi).
* **Basé sur des normes**:  basé sur le norme de the open standards for APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (plus connu sous le nom de Swagger) and <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* estimation basée sur des tests sur une équipe de développement interne, construction d'applications de production.</small>

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

"_[...] J'utilise beaucoup **FastAPI** ces derniers jours. [...] j'envisage de le faire utiliser avec mon équipe **ML services chez Microsoft**. Certains d'entre eux s'intègrent avec les produits **Windows** et **Office** "

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_We adopted the **FastAPI** library to spawn a **REST** server that can be queried to obtain **predictions**. [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** a le plaisir d'annoncer la sortie open source de notre structure d'orchestration de **gestion de crise** : **Dispatch** ! [construit avec **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---
"_Je suis sur la lune enthousiasmé par **FastAPI**. C'est tellement amusant !_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---


"_Honnêtement, ce que vous avez construit a l'air super solide et poli. À bien des égards, c'est ce que je voulais que **Hug** soit - c'est vraiment inspirant de voir quelqu'un construire ça._"


<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Si vous cherchez à apprendre un **framework moderne** pour créer des API REST, consultez **FastAPI** [...] C'est rapide, facile à utiliser et facile à apprendre [...]_"

"_Nous sommes passés à **FastAPI** pour nos **API** [...] Je pense que vous l'aimerez [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> foundateur - <a href="https://spacy.io" target="_blank">spaCy</a> créateurs</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, le FastAPI des CLI(command line integration)

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Si vous créez une  <abbr title="Command Line Interface"> CLI </abbr> application à utiliser dans le terminal au lieu d'une API Web, consultez <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** est le petit frère de FastAPI. Et il est destiné à être le **FastAPI des CLI*

prérequis

Python 3.6+

FastAPI repose sur les épaules de géants :

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> pour la partie web.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> pour la partie donnée.

## Installation

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Vous aurez également besoin d'un serveur ASGI, pour la production telle que <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> ou <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## Exemple

### Crée le

* crée un fichier `main.py` avec:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Ou utilise <code>async def</code>...</summary>

si ton code utilise `async` / `await`, utilise `async def`:

```Python hl_lines="9 14"
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

**Note**:

Si vous ne le savez pas, consultez la section _"in a hurry?"_
 à propos de <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` et `await` dans les docs</a>.

</details>

### Démarre le

Démarre le server avec:

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
<summary>à propos de la commande <code>uvicorn main:app --reload</code>...</summary>

la commande `uvicorn main:app` fait référence à:

* `main`: le fichier `main.py` (the Python "module").
* `app`: l'objet crée dans `main.py` avec la ligne `app = FastAPI()`.
* `--reload`: faire redémarrer le serveur après les changements de code. Ne le faites que pour le développement.

</details>

### Check it

Ouvrez votre navigateur sur <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Vous verrez la réponse JSON comme :
```JSON
{"item_id": 5, "q": "somequery"}
```

Vous avez déjà créé une API qui :

* Reçoit les requêtes HTTP dans les _paths_ `/` et `/items/{item_id}`.
* Les deux _chemins_ acceptent les <em>operations</em> (également connu sous le nom de méthode HTTP).
* le _chemin_ `/items/{item_id}` à un paramétre `item_id` qui doit être un `int`.
* le _chemin_ `/items/{item_id}` a un paramétre optionnel `q`.

### Interactive API docs

Now go to <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

You will see the automatic interactive API documentation (provided by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API docs

Et maintenant, allez à <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Vous verrez la documentation automatique alternative (provided by <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Exemple de mise à niveau

Modifiez maintenant le fichier `main.py` pour recevoir un corps d'une requête `PUT`.

Déclarez le corps en utilisant les types Python standards, grâce à Pydantic.

```Python hl_lines="4  9 10 11 12  25 26 27"
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Le serveur devrait se recharger automatiquement (parce que vous avez ajouté `--reload` à la commande `uvicorn` ci-dessus).

### Mise à niveau interactive de la documentation de l'API


Et maintenant, allez à <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* La documentation interactive de l'API sera automatiquement mise à jour, y compris le nouveau corps :

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Cliquez sur le bouton "Try it out", il vous permet de renseigner les paramètres et d'interagir directement avec l'API :


![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Cliquez ensuite sur le bouton « Exécuter », l'interface utilisateur communiquera avec votre API, enverra les paramètres, obtiendra les résultats et les affichera à l'écran :


![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Mise à niveau de la documentation API alternative

Et maintenant, allez à <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* La documentation alternative reflétera également le nouveau paramètre de requête et le nouveau corps :

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Recap

En résumé, vous déclarez **une fois** les types de paramètres, corps, etc. en tant que paramètres de fonction.

Vous faites cela avec les types Python modernes standard.

Vous n'avez pas besoin d'apprendre une nouvelle syntaxe, les méthodes ou les classes d'une bibliothèque spécifique, etc.

Juste standard **Python 3.6+**.

par exemple, pour un `int`:

```Python
item_id: int
```

ou pour un modèle 'Item' plus complexe :

```Python
item: Item
```

...et avec cette seule déclaration vous obtenez 

* Assistance à l'éditeur, notamment :
    * auto-complétion.
    * verification des types.
* Validation des données :
    * Erreurs automatiques et claires lorsque les données ne sont pas valides.
    * Validation même pour les objets JSON profondément imbriqués.
* <abbr title="also known as: serialization, parsing, marshalling">Conversion</abbr> des données d'entrée : provenant du réseau vers les données et types Python. Lecture de :
    *  JSON.
    * Paramètres de chemin.
    * Paramètres de requête.
    * cookies.
    * headers.
    * Formulaires.
    * Fichiers.

* <abbr title="also known as: serialization, parsing, marshalling">Conversion</abbr> des données de sortie : conversion des données et types Python en données réseau (au format JSON) :
    * Convertir les types Python (`str`, `int`, `float`, `bool`, `list`, etc.).
    * objets `datetime`.
    * Objets `UUID`.
    * Modèles de base de données.
    * ...et beaucoup plus.
* Documentation API interactive automatique, comprenant 2 interfaces utilisateur alternatives :
    * Interface utilisateur Swagger.
    * Redoc.

---

Pour revenir à l'exemple de code précédent, **FastAPI** :

* Validez qu'il y a un `item_id` dans le chemin pour les requêtes `GET` et `PUT`.
* Validez que le `item_id` est de type `int` pour les requêtes `GET` et `PUT`.
    * Si ce n'est pas le cas, le client verra une erreur utile et claire.
* Vérifiez s'il existe un paramètre de requête facultatif nommé `q` (comme dans `http://127.0.0.1:8000/items/foo?q=somequery`) pour les requêtes `GET`.
    * Comme le paramètre `q` est déclaré avec `= None`, il est facultatif.
    * Sans le `None` il serait nécessaire (comme c'est le cas dans le cas avec `PUT`).
* Pour les requêtes `PUT` vers `/items/{item_id}`, lisez le corps en JSON :
* Vérifiez qu'il a un attribut obligatoire `name` qui devrait être un `str`.
    * Vérifiez qu'il a un attribut obligatoire « prix » qui doit être un « flotteur ».
    * Vérifiez qu'il a un attribut facultatif `is_offer`, qui devrait être un `bool`, s'il est présent.
    * Tout cela fonctionnerait également pour les objets JSON profondément imbriqués.
* Convertir de et vers JSON automatiquement.
* Documentez tout avec OpenAPI, qui peut être utilisé par :
    * Systèmes de documentation interactifs.
    * Systèmes de génération automatique de code client, pour de nombreuses langues.
* Fournir directement 2 interfaces web de documentation interactive.


---

Nous venons de gratter la surface, mais vous avez déjà une idée de la façon dont tout cela fonctionne.

Essayez de changer la ligne avec :

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...from:

```Python
        ... "item_name": item.name ...
```

...to:

```Python
        ... "item_price": item.price ...
```

...et voyez comment votre éditeur complétera automatiquement les attributs et connaîtra leurs types :

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)
Pour un exemple plus complet incluant plus de fonctionnalités, voir le <a href="https://fastapi.tiangolo.com/tutorial/">Tutoriel - User Guide</a>.

**Spoiler alert**: le tutoriel - user guide inclu:

* Déclaration de **paramètres** provenant d'autres endroits différents comme : **en-têtes**, **cookies**, **champs de formulaire** et **fichiers**.
* Comment définir les **contraintes de validation** comme `maximum_length` ou `regex`.
* Un très puissant et facile à utiliser **<abbr title="also known as components, resources, providers, services, injectables">Systéme d'injection de dépendance </abbr>** .
* Sécurité et authentification, y compris la prise en charge de **OAuth2** avec **jetons JWT** et **HTTP Basic** auth.
* Des techniques plus avancées (mais tout aussi simples) pour déclarer des **modèles JSON profondément imbriqués** (grâce à Pydantic).
* De nombreuses fonctionnalités supplémentaires (grâce à Starlette) comme:
    * **WebSockets**
    * **GraphQL**
    * tests extrêmement faciles basés sur `requests` et `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...et plus encore.

## Performance

Les benchmarks TechEmpower indépendants montrent les applications **FastAPI** s'exécutant sous Uvicorn comme <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank"> l'un des frameworks Python les plus rapides disponibles </a>, uniquement en dessous de Starlette et Uvicorn eux-mêmes (utilisés en interne par FastAPI). (*)


Pour en savoir plus, consultez la section <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Dépendances facultatives

Utilisé par Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - pour un JSON plus rapide <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - pour la validation d'e-mail.

Utilisé par Starlette :

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - Obligatoire si vous souhaitez utiliser le `TestClient`.
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - Obligatoire si vous souhaitez utiliser `FileResponse` ou `StaticFiles`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Obligatoire si vous souhaitez utiliser la configuration de modèle par défaut.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Obligatoire si vous souhaitez supporter le <abbr title="convertit la chaine de caractère d'une requête HTTP en donnée Python">"décodage"</abbr> de formulaire, avec `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Requis pour la prise en charge de `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Requis pour le support `SchemaGenerator` de Starlette (vous n'en avez probablement pas besoin avec FastAPI).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Requis pour la prise en charge de `GraphQLApp`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Obligatoire si vous souhaitez utiliser `UJSONResponse`.

Utilisé par FastAPI / Starlette :

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - pour le serveur qui charge et sert votre application.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Obligatoire si vous souhaitez utiliser `ORJSONResponse`.

Vous pouvez installer tout cela avec `pip install fastapi[all]`.

## Licence


Ce projet est concédé sous licence selon les termes de la licence MIT.
