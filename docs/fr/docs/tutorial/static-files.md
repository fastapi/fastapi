# Fichiers statiques { #static-files }

Vous pouvez servir des fichiers statiques automatiquement à partir d'un répertoire en utilisant `StaticFiles`.

## Utiliser `StaticFiles` { #use-staticfiles }

- Importer `StaticFiles`.
- « Mount » une instance `StaticFiles()` sur un chemin spécifique.

{* ../../docs_src/static_files/tutorial001_py310.py hl[2,6] *}

/// note | Détails techniques

Vous pouvez également utiliser `from starlette.staticfiles import StaticFiles`.

**FastAPI** fournit le même `starlette.staticfiles` sous le nom `fastapi.staticfiles` uniquement pour votre commodité, en tant que développeur. Mais cela provient en réalité directement de Starlette.

///

### Qu'est-ce que « Mounting » { #what-is-mounting }

« Mounting » signifie ajouter une application complète « indépendante » sur un chemin spécifique, qui se chargera ensuite de gérer tous les sous-chemins.

Cela diffère de l'utilisation d'un `APIRouter`, car une application montée est complètement indépendante. L'OpenAPI et les documents de votre application principale n'incluront rien provenant de l'application montée, etc.

Vous pouvez en lire davantage à ce sujet dans le [Guide utilisateur avancé](../advanced/index.md){.internal-link target=_blank}.

## Détails { #details }

Le premier `"/static"` fait référence au sous-chemin sur lequel cette « sous-application » sera « montée ». Ainsi, tout chemin qui commence par `"/static"` sera géré par elle.

Le `directory="static"` fait référence au nom du répertoire qui contient vos fichiers statiques.

Le `name="static"` lui donne un nom utilisable en interne par **FastAPI**.

Tous ces paramètres peuvent être différents de « `static` », adaptez-les aux besoins et aux détails spécifiques de votre propre application.

## Plus d'informations { #more-info }

Pour plus de détails et d'options, consultez la <a href="https://www.starlette.dev/staticfiles/" class="external-link" target="_blank">documentation de Starlette sur les fichiers statiques</a>.
