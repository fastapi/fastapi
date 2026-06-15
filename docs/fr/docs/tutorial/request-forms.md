# Données de formulaire { #form-data }

Lorsque vous devez recevoir des champs de formulaire au lieu de JSON, vous pouvez utiliser `Form`.

/// note | Remarque

Pour utiliser les formulaires, installez d'abord [`python-multipart`](https://github.com/Kludex/python-multipart).

Vous devez créer un [environnement virtuel](../virtual-environments.md), l'activer, puis installer le paquet, par exemple :

```console
$ pip install python-multipart
```

///

## Importer `Form` { #import-form }

Importez `Form` depuis `fastapi` :

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[3] *}

## Définir les paramètres `Form` { #define-form-parameters }

Créez des paramètres de formulaire comme vous le feriez pour `Body` ou `Query` :

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[9] *}

Par exemple, dans l'une des manières dont la spécification OAuth2 peut être utilisée (appelée « password flow »), il est requis d'envoyer un `username` et un `password` comme champs de formulaire.

La <dfn title="spécification">spécification</dfn> exige que les champs soient exactement nommés `username` et `password`, et qu'ils soient envoyés en tant que champs de formulaire, pas en JSON.

Avec `Form`, vous pouvez déclarer les mêmes configurations que pour `Body` (ainsi que `Query`, `Path`, `Cookie`), y compris la validation, des exemples, un alias (p. ex. `user-name` au lieu de `username`), etc.

/// note | Remarque

`Form` est une classe qui hérite directement de `Body`.

///

/// tip | Astuce

Pour déclarer des corps de formulaire, vous devez utiliser `Form` explicitement, car sinon les paramètres seraient interprétés comme des paramètres de requête ou des paramètres de corps (JSON).

///

## À propos des « champs de formulaire » { #about-form-fields }

La manière dont les formulaires HTML (`<form></form>`) envoient les données au serveur utilise normalement un encodage « spécial » pour ces données, différent de JSON.

**FastAPI** s'assure de lire ces données au bon endroit au lieu de JSON.

/// note | Détails techniques

Les données issues des formulaires sont normalement encodées avec le « type de média » `application/x-www-form-urlencoded`.

Mais lorsque le formulaire inclut des fichiers, il est encodé en `multipart/form-data`. Vous lirez la gestion des fichiers dans le chapitre suivant.

Si vous voulez en savoir plus sur ces encodages et les champs de formulaire, consultez la [<abbr title="Mozilla Developer Network - Réseau des développeurs Mozilla">MDN</abbr> web docs pour `POST`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST).

///

/// warning | Alertes

Vous pouvez déclarer plusieurs paramètres `Form` dans un chemin d'accès, mais vous ne pouvez pas aussi déclarer des champs `Body` que vous vous attendez à recevoir en JSON, car la requête aura le corps encodé en `application/x-www-form-urlencoded` au lieu de `application/json`.

Ce n'est pas une limitation de **FastAPI**, cela fait partie du protocole HTTP.

///

## Récapitulatif { #recap }

Utilisez `Form` pour déclarer les paramètres d'entrée des données de formulaire.
