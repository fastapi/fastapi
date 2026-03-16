# Utiliser Request directement { #using-the-request-directly }

Jusqu'à présent, vous avez déclaré les parties de la requête dont vous avez besoin, avec leurs types.

En récupérant des données depuis :

* Le chemin, sous forme de paramètres.
* En-têtes.
* Cookies.
* etc.

Et ce faisant, **FastAPI** valide ces données, les convertit et génère automatiquement la documentation de votre API.

Mais il existe des situations où vous pouvez avoir besoin d'accéder directement à l'objet `Request`.

## Détails sur l'objet `Request` { #details-about-the-request-object }

Comme **FastAPI** est en fait **Starlette** en dessous, avec une couche de plusieurs outils au-dessus, vous pouvez utiliser directement l'objet <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">`Request`</a> de Starlette lorsque vous en avez besoin.

Cela signifie aussi que si vous récupérez des données directement à partir de l'objet `Request` (par exemple, lire le corps), elles ne seront pas validées, converties ni documentées (avec OpenAPI, pour l'interface utilisateur automatique de l'API) par FastAPI.

En revanche, tout autre paramètre déclaré normalement (par exemple, le corps avec un modèle Pydantic) sera toujours validé, converti, annoté, etc.

Mais il existe des cas spécifiques où il est utile d'obtenir l'objet `Request`.

## Utiliser l'objet `Request` directement { #use-the-request-object-directly }

Imaginons que vous souhaitiez obtenir l'adresse IP/l'hôte du client dans votre fonction de chemin d'accès.

Pour cela, vous devez accéder directement à la requête.

{* ../../docs_src/using_request_directly/tutorial001_py310.py hl[1,7:8] *}

En déclarant un paramètre de fonction de chemin d'accès de type `Request`, **FastAPI** saura passer la `Request` dans ce paramètre.

/// tip | Astuce

Notez que, dans ce cas, nous déclarons un paramètre de chemin en plus du paramètre de requête.

Ainsi, le paramètre de chemin sera extrait, validé, converti vers le type spécifié et annoté avec OpenAPI.

De la même façon, vous pouvez déclarer tout autre paramètre normalement, et en plus, obtenir aussi la `Request`.

///

## Documentation de `Request` { #request-documentation }

Vous pouvez lire plus de détails sur <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">l'objet `Request` sur le site de documentation officiel de Starlette</a>.

/// note | Détails techniques

Vous pouvez également utiliser `from starlette.requests import Request`.

**FastAPI** le fournit directement pour votre commodité, en tant que développeur. Mais il provient directement de Starlette.

///
