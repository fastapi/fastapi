# Événements de cycle de vie { #lifespan-events }

Vous pouvez définir une logique (du code) qui doit être exécutée avant que l'application ne **démarre**. Cela signifie que ce code sera exécuté **une seule fois**, **avant** que l'application ne **commence à recevoir des requêtes**.

De la même manière, vous pouvez définir une logique (du code) qui doit être exécutée lorsque l'application **s'arrête**. Dans ce cas, ce code sera exécuté **une seule fois**, **après** avoir traité potentiellement **de nombreuses requêtes**.

Comme ce code est exécuté avant que l'application ne **commence** à recevoir des requêtes, et juste après qu'elle **termine** de les traiter, il couvre tout le **cycle de vie** de l'application (le mot « lifespan » va être important dans un instant 😉).

Cela peut être très utile pour configurer des **ressources** dont vous avez besoin pour l'ensemble de l'application, qui sont **partagées** entre les requêtes, et/ou que vous devez **nettoyer** ensuite. Par exemple, un pool de connexions à une base de données, ou le chargement d'un modèle d'apprentissage automatique partagé.

## Cas d'utilisation { #use-case }

Commençons par un exemple de **cas d'utilisation**, puis voyons comment le résoudre avec ceci.

Imaginons que vous ayez des **modèles d'apprentissage automatique** que vous souhaitez utiliser pour traiter des requêtes. 🤖

Les mêmes modèles sont partagés entre les requêtes, ce n'est donc pas un modèle par requête, ni un par utilisateur, ou quelque chose de similaire.

Imaginons que le chargement du modèle puisse **prendre pas mal de temps**, car il doit lire beaucoup de **données depuis le disque**. Vous ne voulez donc pas le faire pour chaque requête.

Vous pourriez le charger au niveau supérieur du module/fichier, mais cela signifierait aussi qu'il **chargerait le modèle** même si vous exécutez simplement un test automatisé simple ; ce test serait alors **lent** car il devrait attendre le chargement du modèle avant de pouvoir exécuter une partie indépendante du code.

C'est ce que nous allons résoudre : chargeons le modèle avant que les requêtes ne soient traitées, mais seulement juste avant que l'application ne commence à recevoir des requêtes, pas pendant le chargement du code.

## Cycle de vie { #lifespan }

Vous pouvez définir cette logique de *démarrage* et d'*arrêt* en utilisant le paramètre `lifespan` de l'application `FastAPI`, et un « gestionnaire de contexte » (je vais vous montrer ce que c'est dans un instant).

Commençons par un exemple, puis voyons-le en détail.

Nous créons une fonction async `lifespan()` avec `yield` comme ceci :

{* ../../docs_src/events/tutorial003_py310.py hl[16,19] *}

Ici, nous simulons l'opération de *démarrage* coûteuse de chargement du modèle en plaçant la fonction (factice) du modèle dans le dictionnaire avec les modèles d'apprentissage automatique avant le `yield`. Ce code sera exécuté **avant** que l'application ne **commence à recevoir des requêtes**, pendant le *démarrage*.

Puis, juste après le `yield`, nous déchargeons le modèle. Ce code sera exécuté **après** que l'application **a fini de traiter les requêtes**, juste avant l'*arrêt*. Cela pourrait, par exemple, libérer des ressources comme la mémoire ou un GPU.

/// tip | Astuce

Le `shutdown` se produit lorsque vous **arrêtez** l'application.

Peut-être devez-vous démarrer une nouvelle version, ou vous en avez simplement assez de l'exécuter. 🤷

///

### Fonction de cycle de vie { #lifespan-function }

La première chose à remarquer est que nous définissons une fonction async avec `yield`. C'est très similaire aux Dépendances avec `yield`.

{* ../../docs_src/events/tutorial003_py310.py hl[14:19] *}

La première partie de la fonction, avant le `yield`, sera exécutée **avant** le démarrage de l'application.

Et la partie après le `yield` sera exécutée **après** que l'application a terminé.

### Gestionnaire de contexte asynchrone { #async-context-manager }

Si vous regardez, la fonction est décorée avec `@asynccontextmanager`.

Cela convertit la fonction en quelque chose appelé un « **gestionnaire de contexte asynchrone** ».

{* ../../docs_src/events/tutorial003_py310.py hl[1,13] *}

Un **gestionnaire de contexte** en Python est quelque chose que vous pouvez utiliser dans une instruction `with`. Par exemple, `open()` peut être utilisé comme gestionnaire de contexte :

```Python
with open("file.txt") as file:
    file.read()
```

Dans les versions récentes de Python, il existe aussi un **gestionnaire de contexte asynchrone**. Vous l'utiliseriez avec `async with` :

```Python
async with lifespan(app):
    await do_stuff()
```

Quand vous créez un gestionnaire de contexte ou un gestionnaire de contexte asynchrone comme ci-dessus, ce qu'il fait, c'est qu'avant d'entrer dans le bloc `with`, il exécute le code avant le `yield`, et après être sorti du bloc `with`, il exécute le code après le `yield`.

Dans notre exemple de code ci-dessus, nous ne l'utilisons pas directement, mais nous le transmettons à FastAPI pour qu'il l'utilise.

Le paramètre `lifespan` de l'application `FastAPI` accepte un **gestionnaire de contexte asynchrone**, nous pouvons donc lui passer notre nouveau gestionnaire de contexte asynchrone `lifespan`.

{* ../../docs_src/events/tutorial003_py310.py hl[22] *}

## Événements alternatifs (déprécié) { #alternative-events-deprecated }

/// warning | Alertes

La méthode recommandée pour gérer le *démarrage* et l'*arrêt* est d'utiliser le paramètre `lifespan` de l'application `FastAPI` comme décrit ci-dessus. Si vous fournissez un paramètre `lifespan`, les gestionnaires d'événements `startup` et `shutdown` ne seront plus appelés. C'est soit tout en `lifespan`, soit tout en événements, pas les deux.

Vous pouvez probablement passer cette partie.

///

Il existe une autre manière de définir cette logique à exécuter au *démarrage* et à l'*arrêt*.

Vous pouvez définir des gestionnaires d'événements (fonctions) qui doivent être exécutés avant le démarrage de l'application, ou lorsque l'application s'arrête.

Ces fonctions peuvent être déclarées avec `async def` ou un `def` normal.

### Événement `startup` { #startup-event }

Pour ajouter une fonction qui doit être exécutée avant le démarrage de l'application, déclarez-la avec l'événement « startup » :

{* ../../docs_src/events/tutorial001_py310.py hl[8] *}

Dans ce cas, la fonction gestionnaire de l'événement `startup` initialisera la « base de données » des items (juste un `dict`) avec quelques valeurs.

Vous pouvez ajouter plusieurs fonctions de gestion d'événements.

Et votre application ne commencera pas à recevoir des requêtes avant que tous les gestionnaires de l'événement `startup` aient terminé.

### Événement `shutdown` { #shutdown-event }

Pour ajouter une fonction qui doit être exécutée lorsque l'application s'arrête, déclarez-la avec l'événement « shutdown » :

{* ../../docs_src/events/tutorial002_py310.py hl[6] *}

Ici, la fonction gestionnaire de l'événement `shutdown` écrira une ligne de texte « Application shutdown » dans un fichier `log.txt`.

/// info

Dans la fonction `open()`, le `mode="a"` signifie « append » (ajouter) ; la ligne sera donc ajoutée après ce qui se trouve déjà dans ce fichier, sans écraser le contenu précédent.

///

/// tip | Astuce

Notez que dans ce cas, nous utilisons une fonction Python standard `open()` qui interagit avec un fichier.

Cela implique des E/S (input/output), qui nécessitent « d'attendre » que des choses soient écrites sur le disque.

Mais `open()` n'utilise pas `async` et `await`.

Nous déclarons donc la fonction gestionnaire d'événement avec un `def` standard plutôt qu'avec `async def`.

///

### `startup` et `shutdown` ensemble { #startup-and-shutdown-together }

Il y a de fortes chances que la logique de votre *démarrage* et de votre *arrêt* soit liée : vous pourriez vouloir démarrer quelque chose puis le terminer, acquérir une ressource puis la libérer, etc.

Faire cela dans des fonctions séparées qui ne partagent pas de logique ni de variables est plus difficile, car vous devriez stocker des valeurs dans des variables globales ou recourir à des astuces similaires.

Pour cette raison, il est désormais recommandé d'utiliser plutôt le `lifespan` comme expliqué ci-dessus.

## Détails techniques { #technical-details }

Juste un détail technique pour les nerds curieux. 🤓

Sous le capot, dans la spécification technique ASGI, cela fait partie du [protocole Lifespan](https://asgi.readthedocs.io/en/latest/specs/lifespan.html), et il y définit des événements appelés `startup` et `shutdown`.

/// info

Vous pouvez en lire plus sur les gestionnaires `lifespan` de Starlette dans la [documentation « Lifespan » de Starlette](https://www.starlette.dev/lifespan/).

Y compris comment gérer l'état de cycle de vie qui peut être utilisé dans d'autres parties de votre code.

///

## Sous-applications { #sub-applications }

🚨 Gardez à l'esprit que ces événements de cycle de vie (démarrage et arrêt) ne seront exécutés que pour l'application principale, pas pour [Sous-applications - Montages](sub-applications.md).
