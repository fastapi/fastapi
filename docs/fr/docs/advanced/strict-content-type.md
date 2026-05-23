# Vérifier strictement le Content-Type { #strict-content-type-checking }

Par défaut, FastAPI applique une vérification stricte de l’en-tête `Content-Type` pour les corps de requêtes JSON ; cela signifie que les requêtes JSON doivent inclure un en-tête `Content-Type` valide (par ex. `application/json`) pour que le corps soit analysé comme JSON.

## Risque CSRF { #csrf-risk }

Ce comportement par défaut offre une protection contre une catégorie d’attaques de Cross-Site Request Forgery (CSRF) dans un scénario très spécifique.

Ces attaques exploitent le fait que les navigateurs permettent à des scripts d’envoyer des requêtes sans effectuer de pré-vérification CORS (preflight) lorsqu’ils :

* n’ont pas d’en-tête `Content-Type` (par ex. en utilisant `fetch()` avec un corps `Blob`)
* et n’envoient aucune information d’authentification.

Ce type d’attaque est surtout pertinent lorsque :

* l’application s’exécute localement (par ex. sur `localhost`) ou sur un réseau interne
* et l’application n’a aucun mécanisme d’authentification, elle part du principe que toute requête provenant du même réseau est fiable.

## Exemple d’attaque { #example-attack }

Imaginez que vous mettiez au point un moyen d’exécuter un agent IA local.

Il expose une API à l’adresse

```
http://localhost:8000/v1/agents/multivac
```

Il y a aussi un frontend à l’adresse

```
http://localhost:8000
```

/// tip | Astuce

Notez qu’ils ont le même hôte.

///

Vous pouvez alors, via le frontend, amener l’agent IA à effectuer des actions en votre nom.

Comme il s’exécute localement, et non sur l’Internet ouvert, vous décidez de ne mettre en place aucun mécanisme d’authentification, en vous fiant simplement à l’accès au réseau local.

Un de vos utilisateurs pourrait alors l’installer et l’exécuter localement.

Il pourrait ensuite ouvrir un site malveillant, par exemple quelque chose comme

```
https://evilhackers.example.com
```

Et ce site malveillant enverrait des requêtes en utilisant `fetch()` avec un corps `Blob` vers l’API locale à l’adresse

```
http://localhost:8000/v1/agents/multivac
```

Même si l’hôte du site malveillant et celui de l’application locale sont différents, le navigateur ne déclenchera pas de pré-vérification CORS (preflight) parce que :

* Elle s’exécute sans aucune authentification, il n’y a pas à envoyer d’informations d’authentification.
* Le navigateur pense qu’il n’envoie pas de JSON (faute d’en-tête `Content-Type`).

Le site malveillant pourrait alors amener l’agent IA local à envoyer des messages en colère à l’ancien patron de l’utilisateur ... ou pire. 😅

## Internet ouvert { #open-internet }

Si votre application est exposée sur l’Internet ouvert, vous ne « ferez pas confiance au réseau » et ne laisserez pas n’importe qui envoyer des requêtes privilégiées sans authentification.

Des attaquants pourraient simplement exécuter un script pour envoyer des requêtes à votre API, sans interaction avec le navigateur ; vous sécurisez donc probablement déjà tout endpoint privilégié.

Dans ce cas, cette attaque / ce risque ne vous concerne pas.

Ce risque et cette attaque sont surtout pertinents lorsque l’application s’exécute sur le réseau local et que c’est la seule protection supposée.

## Autoriser les requêtes sans Content-Type { #allowing-requests-without-content-type }

Si vous devez prendre en charge des clients qui n’envoient pas d’en-tête `Content-Type`, vous pouvez désactiver la vérification stricte en définissant `strict_content_type=False` :

{* ../../docs_src/strict_content_type/tutorial001_py310.py hl[4] *}

Avec ce paramètre, les requêtes sans en-tête `Content-Type` verront leur corps analysé comme JSON, ce qui correspond au comportement des anciennes versions de FastAPI.

/// info

Ce comportement et cette configuration ont été ajoutés dans FastAPI 0.132.0.

///
