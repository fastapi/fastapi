# Générer des SDK { #generating-sdks }

Parce que **FastAPI** est basé sur la spécification **OpenAPI**, ses API peuvent être décrites dans un format standard compris par de nombreux outils.

Cela facilite la génération de **documentation** à jour, de bibliothèques clientes (<abbr title="Software Development Kits - Kits de développement logiciel">**SDKs**</abbr>) dans plusieurs langages, ainsi que de **tests** ou de **workflows d’automatisation** qui restent synchronisés avec votre code.

Dans ce guide, vous apprendrez à générer un **SDK TypeScript** pour votre backend FastAPI.

## Générateurs de SDK open source { #open-source-sdk-generators }

Une option polyvalente est le [OpenAPI Generator](https://openapi-generator.tech/), qui prend en charge **de nombreux langages de programmation** et peut générer des SDK à partir de votre spécification OpenAPI.

Pour les **clients TypeScript**, [Hey API](https://heyapi.dev/) est une solution dédiée, offrant une expérience optimisée pour l’écosystème TypeScript.

Vous pouvez découvrir davantage de générateurs de SDK sur [OpenAPI.Tools](https://openapi.tools/#sdk).

/// tip | Astuce

FastAPI génère automatiquement des spécifications **OpenAPI 3.1**, donc tout outil que vous utilisez doit prendre en charge cette version.

///

## Générateurs de SDK par les sponsors de FastAPI { #sdk-generators-from-fastapi-sponsors }

Cette section met en avant des solutions **soutenues par des fonds** et **par des entreprises** qui sponsorisent FastAPI. Ces produits offrent **des fonctionnalités supplémentaires** et **des intégrations** en plus de SDK de haute qualité générés.

En ✨ [**sponsorisant FastAPI**](../help-fastapi.md#sponsor-the-author) ✨, ces entreprises contribuent à garantir que le framework et son **écosystème** restent sains et **durables**.

Leur sponsoring démontre également un fort engagement envers la **communauté** FastAPI (vous), montrant qu’elles se soucient non seulement d’offrir un **excellent service**, mais aussi de soutenir un **framework robuste et florissant**, FastAPI. 🙇

Par exemple, vous pourriez essayer :

* [Speakeasy](https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship)
* [Stainless](https://www.stainless.com/?utm_source=fastapi&utm_medium=referral)
* [liblab](https://developers.liblab.com/tutorials/sdk-for-fastapi?utm_source=fastapi)

Certaines de ces solutions peuvent aussi être open source ou proposer des niveaux gratuits, afin que vous puissiez les essayer sans engagement financier. D’autres générateurs de SDK commerciaux existent et peuvent être trouvés en ligne. 🤓

## Créer un SDK TypeScript { #create-a-typescript-sdk }

Commençons par une application FastAPI simple :

{* ../../docs_src/generate_clients/tutorial001_py310.py hl[7:9,12:13,16:17,21] *}

Remarquez que les *chemins d'accès* définissent les modèles qu’ils utilisent pour le payload de requête et le payload de réponse, en utilisant les modèles `Item` et `ResponseMessage`.

### Documentation de l’API { #api-docs }

Si vous allez sur `/docs`, vous verrez qu’elle contient les **schémas** pour les données à envoyer dans les requêtes et reçues dans les réponses :

<img src="/img/tutorial/generate-clients/image01.png">

Vous voyez ces schémas parce qu’ils ont été déclarés avec les modèles dans l’application.

Ces informations sont disponibles dans le **schéma OpenAPI** de l’application, puis affichées dans la documentation de l’API.

Ces mêmes informations issues des modèles, incluses dans OpenAPI, peuvent être utilisées pour **générer le code client**.

### Hey API { #hey-api }

Une fois que vous avez une application FastAPI avec les modèles, vous pouvez utiliser Hey API pour générer un client TypeScript. Le moyen le plus rapide de le faire est via npx.

```sh
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

Cela générera un SDK TypeScript dans `./src/client`.

Vous pouvez apprendre à [installer `@hey-api/openapi-ts`](https://heyapi.dev/openapi-ts/get-started) et lire à propos du [résultat généré](https://heyapi.dev/openapi-ts/output) sur leur site.

### Utiliser le SDK { #using-the-sdk }

Vous pouvez maintenant importer et utiliser le code client. Cela pourrait ressembler à ceci, remarquez que vous obtenez l’autocomplétion pour les méthodes :

<img src="/img/tutorial/generate-clients/image02.png">

Vous obtiendrez également l’autocomplétion pour le payload à envoyer :

<img src="/img/tutorial/generate-clients/image03.png">

/// tip | Astuce

Remarquez l’autocomplétion pour `name` et `price`, qui a été définie dans l’application FastAPI, dans le modèle `Item`.

///

Vous aurez des erreurs en ligne pour les données que vous envoyez :

<img src="/img/tutorial/generate-clients/image04.png">

L’objet de réponse aura également l’autocomplétion :

<img src="/img/tutorial/generate-clients/image05.png">

## Application FastAPI avec des tags { #fastapi-app-with-tags }

Dans de nombreux cas, votre application FastAPI sera plus grande, et vous utiliserez probablement des tags pour séparer différents groupes de *chemins d'accès*.

Par exemple, vous pourriez avoir une section pour les **items** et une autre section pour les **users**, et elles pourraient être séparées par des tags :

{* ../../docs_src/generate_clients/tutorial002_py310.py hl[21,26,34] *}

### Générer un client TypeScript avec des tags { #generate-a-typescript-client-with-tags }

Si vous générez un client pour une application FastAPI utilisant des tags, il séparera normalement aussi le code client en fonction des tags.

De cette façon, vous pourrez avoir les éléments ordonnés et correctement groupés côté client :

<img src="/img/tutorial/generate-clients/image06.png">

Dans ce cas, vous avez :

* `ItemsService`
* `UsersService`

### Noms des méthodes du client { #client-method-names }

À l’heure actuelle, les noms de méthodes générés comme `createItemItemsPost` ne sont pas très propres :

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

... c’est parce que le générateur de client utilise l’**operation ID** interne OpenAPI pour chaque *chemin d'accès*.

OpenAPI exige que chaque operation ID soit unique parmi tous les *chemins d'accès*, donc FastAPI utilise le **nom de la fonction**, le **chemin**, et la **méthode/opération HTTP** pour générer cet operation ID, car de cette façon il peut s’assurer que les operation IDs sont uniques.

Mais je vais vous montrer comment améliorer cela ensuite. 🤓

## IDs d’opération personnalisés et meilleurs noms de méthodes { #custom-operation-ids-and-better-method-names }

Vous pouvez **modifier** la façon dont ces operation IDs sont **générés** pour les simplifier et obtenir des **noms de méthodes plus simples** dans les clients.

Dans ce cas, vous devez vous assurer que chaque operation ID est **unique** d’une autre manière.

Par exemple, vous pouvez vous assurer que chaque *chemin d'accès* a un tag, puis générer l’operation ID à partir du **tag** et du **nom** du *chemin d'accès* (le nom de la fonction).

### Fonction personnalisée de génération d’ID unique { #custom-generate-unique-id-function }

FastAPI utilise un **ID unique** pour chaque *chemin d'accès*, qui est utilisé pour l’**operation ID** et également pour les noms des modèles personnalisés nécessaires, pour les requêtes ou les réponses.

Vous pouvez personnaliser cette fonction. Elle prend un `APIRoute` et retourne une chaîne.

Par exemple, ici elle utilise le premier tag (vous n’en aurez probablement qu’un) et le nom du *chemin d'accès* (le nom de la fonction).

Vous pouvez ensuite passer cette fonction personnalisée à **FastAPI** via le paramètre `generate_unique_id_function` :

{* ../../docs_src/generate_clients/tutorial003_py310.py hl[6:7,10] *}

### Générer un client TypeScript avec des IDs d’opération personnalisés { #generate-a-typescript-client-with-custom-operation-ids }

Maintenant, si vous régénérez le client, vous verrez qu’il possède des noms de méthodes améliorés :

<img src="/img/tutorial/generate-clients/image07.png">

Comme vous le voyez, les noms de méthodes contiennent maintenant le tag puis le nom de la fonction ; ils n’incluent plus d’informations provenant du chemin d’URL et de l’opération HTTP.

### Prétraiter la spécification OpenAPI pour le générateur de client { #preprocess-the-openapi-specification-for-the-client-generator }

Le code généré contient encore des **informations dupliquées**.

Nous savons déjà que cette méthode est liée aux **items** parce que ce mot figure dans `ItemsService` (issu du tag), mais nous avons encore le nom du tag préfixé dans le nom de la méthode. 😕

Nous voudrons probablement le conserver pour OpenAPI en général, car cela garantira que les operation IDs sont **uniques**.

Mais pour le client généré, nous pourrions **modifier** les operation IDs d’OpenAPI juste avant de générer les clients, simplement pour rendre ces noms de méthodes plus agréables et **plus clairs**.

Nous pourrions télécharger le JSON OpenAPI dans un fichier `openapi.json` puis **supprimer ce tag préfixé** avec un script comme celui-ci :

{* ../../docs_src/generate_clients/tutorial004_py310.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

Avec cela, les operation IDs seraient renommés de `items-get_items` en simplement `get_items`, de sorte que le générateur de client puisse produire des noms de méthodes plus simples.

### Générer un client TypeScript avec l’OpenAPI prétraité { #generate-a-typescript-client-with-the-preprocessed-openapi }

Puisque le résultat final se trouve maintenant dans un fichier `openapi.json`, vous devez mettre à jour l’emplacement d’entrée :

```sh
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

Après avoir généré le nouveau client, vous aurez désormais des **noms de méthodes propres**, avec toute l’**autocomplétion**, les **erreurs en ligne**, etc. :

<img src="/img/tutorial/generate-clients/image08.png">

## Avantages { #benefits }

En utilisant les clients générés automatiquement, vous obtiendrez de l’**autocomplétion** pour :

* Méthodes.
* Payloads de requête dans le corps, paramètres de requête, etc.
* Payloads de réponse.

Vous auriez également des **erreurs en ligne** pour tout.

Et chaque fois que vous mettez à jour le code du backend et **régénérez** le frontend, il inclura les nouveaux *chemins d'accès* disponibles en tant que méthodes, supprimera les anciens, et tout autre changement sera reflété dans le code généré. 🤓

Cela signifie aussi que si quelque chose change, cela sera **reflété** automatiquement dans le code client. Et si vous **bâtissez** le client, il échouera en cas de **discordance** dans les données utilisées.

Ainsi, vous **détecterez de nombreuses erreurs** très tôt dans le cycle de développement au lieu d’attendre qu’elles apparaissent pour vos utilisateurs finaux en production puis de tenter de déboguer l’origine du problème. ✨
