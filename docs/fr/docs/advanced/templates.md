# Templates { #templates }

Vous pouvez utiliser n'importe quel moteur de templates avec **FastAPI**.

Un choix courant est Jinja2, le même que celui utilisé par Flask et d'autres outils.

Il existe des utilitaires pour le configurer facilement que vous pouvez utiliser directement dans votre application **FastAPI** (fournis par Starlette).

## Installer les dépendances { #install-dependencies }

Vous devez créer un [environnement virtuel](../virtual-environments.md){.internal-link target=_blank}, l'activer, puis installer `jinja2` :

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## Utiliser `Jinja2Templates` { #using-jinja2templates }

- Importez `Jinja2Templates`.
- Créez un objet `templates` que vous pourrez réutiliser par la suite.
- Déclarez un paramètre `Request` dans le *chemin d'accès* qui renverra un template.
- Utilisez l'objet `templates` que vous avez créé pour rendre et retourner une `TemplateResponse`, en transmettant le nom du template, l'objet de requête et un dictionnaire de « context » avec des paires clé-valeur à utiliser dans le template Jinja2.

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

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

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

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

... générera un lien vers la même URL que celle gérée par la *fonction de chemin d'accès* `read_item(id=id)`.

Par exemple, avec un ID de `42`, cela rendrait :

```html
<a href="/items/42">
```

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

Pour plus de détails, y compris sur la façon de tester des templates, consultez <a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">la documentation de Starlette sur les templates</a>.
