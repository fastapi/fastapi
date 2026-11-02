---
render_macros: false
---

# Templates { #templates }

Vous pouvez utiliser n'importe quel moteur de templates avec **FastAPI**.

Un choix courant est Jinja2, le même que celui utilisé par Flask et d'autres outils.

Il existe des utilitaires pour le configurer facilement que vous pouvez utiliser directement dans votre application **FastAPI** (fournis par Starlette).

## Installer les dépendances { #install-dependencies }

Ajoutez `jinja2` à votre projet :

<div class="termy">

```console
$ uv add jinja2

---> 100%
```

</div>

## Utiliser `Jinja2Templates` { #using-jinja2templates }

* Importez `Jinja2Templates`.
* Créez un objet `templates` que vous pourrez réutiliser par la suite.
* Déclarez un paramètre `Request` dans le *chemin d'accès* qui renverra un template.
* Utilisez l'objet `templates` que vous avez créé pour rendre et retourner une `TemplateResponse`, en transmettant le nom du template, l'objet de requête et un dictionnaire de « context » avec des paires clé-valeur à utiliser dans le template Jinja2.

{* ../../docs_src/templates/tutorial001_py310.py hl[4,11,15:18] *}

/// note | Remarque

Avant FastAPI 0.108.0 et Starlette 0.29.0, `name` était le premier paramètre.

De plus, auparavant, dans les versions précédentes, l'objet `request` faisait partie des paires clé-valeur du contexte pour Jinja2.

///

/// tip | Astuce

En déclarant `response_class=HTMLResponse`, l'interface de la documentation saura que la réponse sera en HTML.

///

/// note | Détails techniques

Vous pouvez aussi utiliser `from starlette.templating import Jinja2Templates`.

**FastAPI** expose le même `starlette.templating` sous `fastapi.templating` par simple commodité pour vous, développeur. Mais la plupart des réponses disponibles proviennent directement de Starlette. C'est également le cas pour `Request` et `StaticFiles`.

///

## Écrire des templates { #writing-templates }

Vous pouvez ensuite écrire un template dans `templates/item.html`, par exemple :

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### Valeurs de contexte du template { #template-context-values }

Dans le HTML qui contient :

```jinja
Item ID: {{ id }}
```

... il affichera l’`id` récupéré à partir du `dict` « context » que vous avez passé :

```Python
{"id": id}
```

Par exemple, avec un ID de `42`, cela rendrait :

```html
Item ID: 42
```

### Arguments de `url_for` dans le template { #template-url-for-arguments }

Vous pouvez aussi utiliser `url_for()` dans le template ; elle prend en paramètres les mêmes arguments que ceux utilisés par votre *fonction de chemin d'accès*.

Ainsi, la section suivante :

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

... générera un lien vers la même URL que celle gérée par la *fonction de chemin d'accès* `read_item(id=id)`.

`url_for()` renvoie une URL absolue, comprenant le schéma et l'hôte, basée sur la requête actuelle.

Par exemple, si votre application est servie à l'adresse `https://example.com`, avec un ID de `42`, cela rendrait :

```html
<a href="https://example.com/items/42">
```

### Chemins d'URL dans les templates { #url-paths-in-templates }

Pour les liens vers le même site, vous pouvez utiliser l'attribut `.path` pour obtenir uniquement le chemin de l'URL, par exemple, dans `templates/item_path.html` :

```jinja hl_lines="4 7"
{!../../docs_src/templates/templates/item_path.html!}
```

Passez le nom du template à `TemplateResponse` :

{* ../../docs_src/templates/tutorial002_py310.py ln[14:18] hl[17] *}

Avec le même exemple, le lien vers l'élément donnerait :

```html
<a href="/items/42">
```

Le `/` initial rend ce chemin relatif à la racine du site actuel.

L'attribut `.path` exclut le schéma, l'hôte, les paramètres de requête et le fragment. Utilisez l'URL complète pour les liens vers un autre hôte.

/// tip | Astuce

Si votre application est derrière un proxy, configurez les en-têtes transférés et `root_path` comme décrit dans [Derrière un proxy](behind-a-proxy.md).

///

## Templates et fichiers statiques { #templates-and-static-files }

Vous pouvez aussi utiliser `url_for()` dans le template, par exemple avec les `StaticFiles` que vous avez montés avec `name="static"`.

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

Dans cet exemple, cela créera un lien vers un fichier CSS `static/styles.css` avec :

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

Et comme vous utilisez `StaticFiles`, ce fichier CSS est servi automatiquement par votre application **FastAPI** à l’URL `/static/styles.css`.

## En savoir plus { #more-details }

Pour plus de détails, y compris sur la façon de tester des templates, consultez [les documents de Starlette sur les templates](https://starlette.dev/templates/).
