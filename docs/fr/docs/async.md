# Concurrence et async / await { #concurrency-and-async-await }

Détails sur la syntaxe `async def` pour les *fonctions de chemin d'accès* et quelques rappels sur le code asynchrone, la concurrence et le parallélisme.

## Vous êtes pressés ? { #in-a-hurry }

<abbr title="too long; didn't read - trop long ; pas lu"><strong>TL;DR :</strong></abbr>

Si vous utilisez des bibliothèques tierces qui nécessitent d'être appelées avec `await`, telles que :

```Python
results = await some_library()
```

Alors, déclarez vos *fonctions de chemin d'accès* avec `async def` comme ceci :

```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

/// note | Remarque

Vous pouvez uniquement utiliser `await` dans les fonctions créées avec `async def`.

///

---

Si vous utilisez une bibliothèque externe qui communique avec quelque chose (une base de données, une API, le système de fichiers, etc.) et qui ne supporte pas l'utilisation d'`await` (ce qui est actuellement le cas pour la majorité des bibliothèques de base de données), alors déclarez vos *fonctions de chemin d'accès* normalement, avec le classique `def`, comme ceci :

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

Si votre application (d'une certaine manière) n'a pas à communiquer avec une autre chose et à attendre sa réponse, utilisez `async def`, même si vous n'avez pas besoin d'utiliser `await` à l'intérieur.

---

Si vous ne savez pas, utilisez un `def` normal.

---

**Remarque** : vous pouvez mélanger `def` et `async def` dans vos *fonctions de chemin d'accès* autant que nécessaire, et définir chacune avec l’option la plus adaptée pour vous. FastAPI fera ce qu'il faut avec elles.

Au final, peu importe le cas parmi ceux ci-dessus, FastAPI fonctionnera de manière asynchrone et sera extrêmement rapide.

Mais si vous suivez bien les étapes ci-dessus, il pourra effectuer quelques optimisations de performance.

## Détails techniques { #technical-details }

Les versions modernes de Python supportent le **« code asynchrone »** en utilisant quelque chose appelé **« coroutines »**, avec la syntaxe **`async` et `await`**.

Analysons les différentes parties de cette phrase dans les sections suivantes :

* **Code asynchrone**
* **`async` et `await`**
* **Coroutines**

## Code asynchrone { #asynchronous-code }

Faire du code asynchrone signifie que le langage 💬 est capable de dire à l'ordinateur / au programme 🤖 qu'à un moment du code, il 🤖 devra attendre que *quelque chose d'autre* se termine autre part. Disons que ce *quelque chose d'autre* est appelé « slow-file » 📝.

Donc, pendant ce temps, l'ordinateur pourra effectuer d'autres tâches, pendant que « slow-file » 📝 se termine.

Ensuite l'ordinateur / le programme 🤖 reviendra à chaque fois qu'il en a la chance, parce qu'il attend à nouveau, ou quand il 🤖 a fini tout le travail qu'il avait à faire à ce moment-là. Et il 🤖 regardera si des tâches qu'il attendait ont déjà terminé, en faisant ce qu'il devait faire.

Ensuite, il 🤖 prendra la première tâche à finir (disons, notre « slow-file » 📝) et continuera à faire avec cette dernière ce qu'il était censé.

Ce « attendre quelque chose d'autre » fait généralement référence à des opérations <abbr title="Input and Output - Entrées et sorties">I/O</abbr> qui sont relativement « lentes » (comparées à la vitesse du processeur et de la mémoire RAM) telles qu'attendre que :

* de la donnée soit envoyée par le client à travers le réseau
* de la donnée envoyée depuis votre programme soit reçue par le client à travers le réseau
* le contenu d'un fichier sur le disque soit lu par le système et passé à votre programme
* le contenu que votre programme a passé au système soit écrit sur le disque
* une opération effectuée à distance par une API
* une opération en base de données se termine
* une requête à une base de données renvoie un résultat
* etc.

Le temps d'exécution étant consommé majoritairement par l'attente d'opérations <abbr title="Input and Output - Entrées et sorties">I/O</abbr>, on appelle ceci des opérations « I/O bound ».

Ce concept se nomme « asynchrone » car l'ordinateur / le programme n'a pas besoin d'être « synchronisé » avec la tâche lente, attendant le moment exact où cette dernière se terminera en ne faisant rien, pour être capable de récupérer le résultat de la tâche et l'utiliser dans la suite des opérations.

À la place, en étant un système « asynchrone », une fois terminée, la tâche peut attendre un peu dans la file (quelques microsecondes) que l'ordinateur / le programme finisse ce qu'il était en train de faire, puis revienne récupérer les résultats et continue à travailler avec eux.

Pour parler de tâches « synchrones » (en opposition à « asynchrones »), on utilise souvent aussi le terme « séquentiel », car l'ordinateur / le programme va effectuer toutes les étapes d'une tâche séquentiellement avant de passer à une autre tâche, même si ces étapes impliquent de l'attente.

### Concurrence et Burgers { #concurrency-and-burgers }

L'idée de code **asynchrone** décrite ci-dessus est parfois aussi appelée **« concurrence »**. Ce qui est différent du **« parallélisme »**.

La **concurrence** et le **parallélisme** sont tous deux liés à l'idée de « différentes choses arrivant plus ou moins au même moment ».

Mais les détails entre la *concurrence* et le *parallélisme* sont assez différents.

Pour expliquer la différence, imaginez l'histoire suivante à propos de burgers :

### Burgers concurrents { #concurrent-burgers }

Vous allez avec votre crush chercher de la nourriture dans un fast food, vous faites la queue pendant que le caissier prend les commandes des personnes devant vous. 😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

Puis vient votre tour, vous commandez alors 2 burgers très sophistiqués pour votre crush et vous. 🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

Le caissier dit quelque chose au cuisinier dans la cuisine pour qu'il sache qu'il doit préparer vos burgers (bien qu'il soit déjà en train de préparer ceux des clients précédents).

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

Vous payez. 💸

Le caissier vous donne le numéro de votre tour.

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

Pendant que vous attendez, vous allez choisir une table avec votre crush, vous vous asseyez et discutez avec votre crush pendant un long moment (vos burgers étant très sophistiqués, ils prennent du temps à préparer).

Pendant que vous êtes assis à table avec votre crush, en attendant les burgers, vous pouvez passer ce temps à admirer à quel point votre crush est géniale, mignonne et intelligente ✨😍✨.

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

Pendant que vous attendez et discutez avec votre crush, de temps en temps, vous jetez un coup d’œil au nombre affiché au-dessus du comptoir pour savoir si c'est déjà votre tour.

Puis, à un moment, c'est enfin votre tour. Vous allez au comptoir, récupérez vos burgers et revenez à votre table.

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

Vous et votre crush mangez les burgers et passez un bon moment. ✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

/// note | Remarque

Belles illustrations par [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot). 🎨

///

---

Imaginez que vous êtes l'ordinateur / le programme 🤖 dans cette histoire.

Pendant que vous faites la queue, vous êtes simplement inactif 😴, attendant votre tour, ne faisant rien de très « productif ». Mais la queue est rapide car le caissier prend seulement les commandes (et ne les prépare pas), donc tout va bien.

Ensuite, quand c'est votre tour, vous faites du vrai travail « productif », vous étudiez le menu, décidez ce que vous voulez, demandez à votre crush son choix, payez, vérifiez que vous donnez le bon billet ou la bonne carte, vérifiez que le montant débité est correct, vérifiez que la commande contient les bons produits, etc.

Mais ensuite, même si vous n'avez toujours pas vos burgers, votre travail avec le caissier est « en pause » ⏸, car vous devez attendre 🕙 que vos burgers soient prêts.

Mais lorsque vous vous écartez du comptoir et vous asseyez à table avec un numéro pour votre tour, vous pouvez tourner 🔀 votre attention vers votre crush, et « travailler » ⏯ 🤓 là-dessus. Vous êtes donc à nouveau en train de faire quelque chose de très « productif », comme flirter avec votre crush 😍.

Puis le caissier 💁 dit « J'ai fini de faire les burgers » en mettant votre numéro sur l'affichage du comptoir, mais vous ne sautez pas comme un fou immédiatement quand le numéro affiché change pour devenir votre numéro. Vous savez que personne ne volera vos burgers car vous avez le numéro de votre tour, et les autres ont le leur.

Vous attendez donc que votre crush finisse son histoire (termine le travail actuel ⏯ / la tâche en cours de traitement 🤓), souriez gentiment et dites que vous allez chercher les burgers ⏸.

Puis vous allez au comptoir 🔀, vers la tâche initiale qui est désormais terminée ⏯, récupérez les burgers, remerciez et ramenez les burgers à votre table. Ceci termine l'étape / la tâche d'interaction avec le comptoir ⏹. Ce qui ensuite crée une nouvelle tâche, « manger les burgers » 🔀 ⏯, mais la précédente, « récupérer les burgers », est terminée ⏹.

### Burgers parallèles { #parallel-burgers }

Imaginons désormais que ce ne sont pas des « Burgers concurrents » mais des « Burgers parallèles ».

Vous allez avec votre crush chercher de la nourriture dans un fast food parallèle.

Vous attendez pendant que plusieurs (disons 8) caissiers qui sont en même temps cuisiniers prennent les commandes des personnes devant vous.

Chaque personne devant vous attend que son burger soit prêt avant de quitter le comptoir car chacun des 8 caissiers va préparer le burger directement avant de prendre la commande suivante.

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

Puis c'est enfin votre tour, vous commandez 2 burgers très sophistiqués pour vous et votre crush.

Vous payez 💸.

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

Le caissier va dans la cuisine.

Vous attendez, debout devant le comptoir 🕙, afin que personne d'autre ne prenne vos burgers avant vous, vu qu'il n'y a pas de numéros pour les tours.

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

Vous et votre crush étant occupés à ne laisser personne passer devant vous et prendre vos burgers au moment où ils arriveront, vous ne pouvez pas prêter attention à votre crush. 😞

C'est du travail « synchrone », vous être « synchronisés » avec le caissier/cuisinier 👨‍🍳. Vous devez attendre 🕙 et être présent au moment exact où le caissier/cuisinier 👨‍🍳 finira les burgers et vous les donnera, sinon quelqu'un d'autre risque de vous les prendre.

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

Puis votre caissier/cuisinier 👨‍🍳 revient enfin avec vos burgers, après un long moment d'attente 🕙 devant le comptoir.

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

Vous prenez vos burgers et allez à une table avec votre crush.

Vous les mangez simplement, et vous avez terminé. ⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

Il n'y a pas eu beaucoup de discussions ou de flirts car la plupart du temps a été passé à attendre 🕙 devant le comptoir. 😞

/// note | Remarque

Belles illustrations par [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot). 🎨

///

---

Dans ce scénario de burgers parallèles, vous êtes un ordinateur / programme 🤖 avec deux processeurs (vous et votre crush), tous deux attendant 🕙 et dédiant leur attention ⏯ à « attendre devant le comptoir » 🕙 pour une longue durée.

Le fast food a 8 processeurs (caissiers/cuisiniers). Alors que le fast food de burgers concurrents aurait pu n'en avoir que 2 (un caissier et un cuisinier).

Mais tout de même, l'expérience finale n'est pas la meilleure. 😞

---

Ce serait donc l'histoire équivalente parallèle pour les burgers. 🍔

Pour un exemple plus « vie réelle », imaginez une banque.

Jusqu'à récemment, la plupart des banques avaient plusieurs caissiers 👨‍💼👨‍💼👨‍💼👨‍💼 et une grande file d'attente 🕙🕙🕙🕙🕙🕙🕙🕙.

Tous les caissiers faisaient tout le travail avec chaque client avant de passer au suivant 👨‍💼⏯.

Et vous devez attendre 🕙 dans la file pendant un long moment ou vous perdez votre tour.

Vous n'auriez donc probablement pas envie d'amener votre crush 😍 avec vous pour faire des démarches à la banque 🏦.

### Conclusion sur les burgers { #burger-conclusion }

Dans ce scénario des « burgers de fast food avec votre crush », comme il y a beaucoup d'attente 🕙, il est beaucoup plus logique d'avoir un système concurrent ⏸🔀⏯.

C'est le cas pour la plupart des applications web.

De très, très nombreux utilisateurs, mais votre serveur attend 🕙 que leur connexion pas très bonne envoie leurs requêtes.

Puis attend 🕙 de nouveau que les réponses reviennent.

Cette « attente » 🕙 se mesure en microsecondes, mais tout de même, en les cumulant toutes, cela fait beaucoup d'attente au final.

C'est pourquoi il est très logique d'utiliser du code asynchrone ⏸🔀⏯ pour des APIs web.

Ce type d'asynchronicité est ce qui a rendu NodeJS populaire (bien que NodeJS ne soit pas parallèle) et c'est la force de Go en tant que langage de programmation.

Et c'est le même niveau de performance que celui obtenu avec **FastAPI**.

Et comme on peut avoir du parallélisme et de l'asynchronicité en même temps, on obtient des performances plus hautes que la plupart des frameworks NodeJS testés et égales à celles du Go, qui est un langage compilé plus proche du C [(tout ça grâce à Starlette)](https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1).

### Est-ce que la concurrence est mieux que le parallélisme ? { #is-concurrency-better-than-parallelism }

Nope ! Ce n'est pas la morale de l'histoire.

La concurrence est différente du parallélisme. Et c'est mieux dans des scénarios **spécifiques** qui impliquent beaucoup d'attente. À cause de ça, c'est généralement bien meilleur que le parallélisme pour le développement d'applications web. Mais pas pour tout.

Donc pour équilibrer tout ça, imaginez l'histoire courte suivante :

> Vous devez nettoyer une grande et sale maison.

*Oui, c'est toute l'histoire*.

---

Il n'y a plus d'attente 🕙 nulle part, juste beaucoup de travail à effectuer, dans différentes pièces de la maison.

Vous pourriez avoir des tours comme dans l'exemple des burgers, d'abord le salon, puis la cuisine, mais comme vous n'attendez 🕙 rien, vous ne faites que nettoyer et nettoyer, les tours ne changeraient rien.

Cela prendrait autant de temps pour finir avec ou sans tours (concurrence) et vous auriez effectué la même quantité de travail.

Mais dans ce cas, si vous pouviez amener les 8 ex-caissiers/cuisiniers/désormais-nettoyeurs, et que chacun d'eux (plus vous) pouvait prendre une zone de la maison pour la nettoyer, vous pourriez faire tout le travail en **parallèle**, avec l'aide supplémentaire, et finir beaucoup plus tôt.

Dans ce scénario, chacun des nettoyeurs (vous y compris) serait un processeur, faisant sa partie du travail.

Et comme la plupart du temps d'exécution est pris par du vrai travail (et non de l'attente), et que le travail dans un ordinateur est fait par un <abbr title="Central Processing Unit - Unité centrale de traitement">CPU</abbr>, ce sont des problèmes dits « CPU bound ».

---

Des exemples communs d'opérations CPU bound sont les choses qui requièrent des traitements mathématiques complexes.

Par exemple :

* Traitements d'**audio** ou d'**images**.
* **Computer vision** : une image est composée de millions de pixels, chaque pixel ayant 3 valeurs / couleurs, les traiter nécessite normalement d'effectuer des calculs sur ces pixels, tous en même temps.
* **Machine Learning** : cela nécessite normalement de nombreuses multiplications de « matrices » et de « vecteurs ». Imaginez une énorme feuille de calcul remplie de nombres et les multiplier tous ensemble au même moment.
* **Deep Learning** : c'est un sous-domaine du Machine Learning, donc les mêmes raisons s'appliquent. C'est juste qu'il n'y a pas une unique feuille de calcul de nombres à multiplier, mais une énorme quantité d'entre elles, et dans de nombreux cas, on utilise un processeur spécial pour construire et / ou utiliser ces modèles.

### Concurrence + Parallélisme : Web + Machine Learning { #concurrency-parallelism-web-machine-learning }

Avec **FastAPI** vous pouvez bénéficier de la concurrence qui est très courante en développement web (le même attrait principal de NodeJS).

Mais vous pouvez aussi profiter du parallélisme et du multiprocessing (plusieurs processus s'exécutant en parallèle) afin de gérer des charges **CPU bound** comme celles des systèmes de Machine Learning.

Ça, ajouté au simple fait que Python soit le langage principal pour la **Data Science**, le Machine Learning et surtout le Deep Learning, fait de FastAPI un très bon choix pour les APIs web et applications de Data Science / Machine Learning (entre autres).

Pour comprendre comment mettre en place ce parallélisme en production, consultez la section sur le [Déploiement](deployment/index.md).

## `async` et `await` { #async-and-await }

Les versions modernes de Python ont une manière très intuitive de définir le code asynchrone. Cela le fait ressembler à du code « séquentiel » normal et effectue l'« attente » pour vous aux bons moments.

Pour une opération qui nécessite de l'attente avant de donner un résultat et qui supporte ces nouvelles fonctionnalités Python, vous pouvez l'écrire comme ceci :

```Python
burgers = await get_burgers(2)
```

Le mot-clé important ici est `await`. Il informe Python qu'il faut attendre ⏸ que `get_burgers(2)` finisse d'effectuer ses opérations 🕙 avant de stocker les résultats dans la variable `burgers`. Grâce à cela, Python saura qu'il peut aller effectuer d'autres opérations 🔀 ⏯ pendant ce temps (comme par exemple recevoir une autre requête).

Pour que `await` fonctionne, il doit être placé dans une fonction qui supporte cette asynchronicité. Pour que ça soit le cas, il faut déclarer cette dernière avec `async def` :

```Python hl_lines="1"
async def get_burgers(number: int):
    # Opérations asynchrones pour créer les burgers
    return burgers
```

... au lieu de `def` :

```Python hl_lines="2"
# Ceci n'est pas asynchrone
def get_sequential_burgers(number: int):
    # Opérations séquentielles pour créer les burgers
    return burgers
```

Avec `async def`, Python sait que dans cette fonction il doit prendre en compte les expressions `await`, et qu'il peut mettre en pause ⏸ l'exécution de la fonction pour aller faire autre chose 🔀 avant de revenir.

Lorsque vous voulez appeler une fonction `async def`, vous devez l'« attendre ». Donc ceci ne marche pas :

```Python
# Ceci ne fonctionne pas, car get_burgers a été défini avec : async def
burgers = get_burgers(2)
```

---

Donc, si vous utilisez une bibliothèque qui vous indique que vous pouvez l'appeler avec `await`, vous devez créer les *fonctions de chemin d'accès* qui l'utilisent avec `async def`, comme dans :

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### Plus de détails techniques { #more-technical-details }

Vous avez peut-être remarqué que `await` peut seulement être utilisé dans des fonctions définies avec `async def`.

Mais en même temps, les fonctions définies avec `async def` doivent être « attendues ». Donc, les fonctions avec `async def` peuvent seulement être appelées à l'intérieur de fonctions définies elles aussi avec `async def`.

Donc, à propos de l'œuf et de la poule, comment appelle-t-on la première fonction `async` ?

Si vous utilisez **FastAPI**, pas besoin de vous en inquiéter, car cette « première » fonction sera votre *fonction de chemin d'accès*, et FastAPI saura comment faire ce qu'il faut.

Mais si vous souhaitez utiliser `async` / `await` sans FastAPI, vous pouvez également le faire.

### Écrire votre propre code async { #write-your-own-async-code }

Starlette (et **FastAPI**) s’appuie sur [AnyIO](https://anyio.readthedocs.io/en/stable/), ce qui le rend compatible à la fois avec la bibliothèque standard [asyncio](https://docs.python.org/3/library/asyncio-task.html) de Python et avec [Trio](https://trio.readthedocs.io/en/stable/).

En particulier, vous pouvez utiliser directement [AnyIO](https://anyio.readthedocs.io/en/stable/) pour vos cas d’usage de concurrence avancés qui nécessitent des schémas plus élaborés dans votre propre code.

Et même si vous n’utilisiez pas FastAPI, vous pourriez aussi écrire vos propres applications async avec [AnyIO](https://anyio.readthedocs.io/en/stable/) pour une grande compatibilité et pour bénéficier de ses avantages (par ex. la *structured concurrency*).

J’ai créé une autre bibliothèque au-dessus d’AnyIO, comme une fine surcouche, pour améliorer un peu les annotations de type et obtenir une meilleure **autocomplétion**, des **erreurs en ligne**, etc. Elle propose également une introduction et un tutoriel accessibles pour vous aider à **comprendre** et écrire **votre propre code async** : [Asyncer](https://asyncer.tiangolo.com/). Elle sera particulièrement utile si vous devez **combiner du code async avec du code classique** (bloquant/synchrone).

### Autres formes de code asynchrone { #other-forms-of-asynchronous-code }

L'utilisation d'`async` et `await` est relativement nouvelle dans ce langage.

Mais cela rend la programmation asynchrone bien plus simple.

Cette même syntaxe (ou presque) a aussi été incluse récemment dans les versions modernes de JavaScript (dans le navigateur et NodeJS).

Mais avant ça, gérer du code asynchrone était bien plus complexe et difficile.

Dans les versions précédentes de Python, vous auriez pu utiliser des threads ou [Gevent](https://www.gevent.org/). Mais le code est bien plus difficile à comprendre, débugger, et concevoir.

Dans les versions précédentes de NodeJS / JavaScript de navigateur, vous auriez utilisé des « callbacks ». Ce qui mène au « callback hell ».

## Coroutines { #coroutines }

**Coroutine** est juste un terme élaboré pour désigner ce qui est retourné par une fonction définie avec `async def`. Python sait que c'est comme une fonction, qui peut démarrer et qui se terminera à un moment, mais qu'elle peut aussi être mise en pause ⏸ en interne, quand il y a un `await` à l'intérieur.

Mais toutes ces fonctionnalités d'utilisation de code asynchrone avec `async` et `await` sont souvent résumées comme l'utilisation des « coroutines ». On peut comparer cela à la principale fonctionnalité clé de Go, les « Goroutines ».

## Conclusion { #conclusion }

Reprenons la même phrase ci-dessus :

> Les versions modernes de Python supportent le **« code asynchrone »** en utilisant quelque chose appelé **« coroutines »**, avec la syntaxe **`async` et `await`**.

Ceci devrait être plus compréhensible désormais. ✨

Tout ceci est donc ce qui donne sa force à FastAPI (à travers Starlette) et lui permet d'avoir une performance aussi impressionnante.

## Détails très techniques { #very-technical-details }

/// warning | Alertes

Vous pouvez probablement ignorer cela.

Ce sont des détails très poussés sur comment **FastAPI** fonctionne en arrière-plan.

Si vous avez de bonnes connaissances techniques (coroutines, threads, code bloquant, etc.) et êtes curieux de comment FastAPI gère `async def` versus le `def` classique, cette partie est faite pour vous.

///

### Fonctions de chemin d'accès { #path-operation-functions }

Quand vous déclarez une *fonction de chemin d'accès* avec un `def` normal et non `async def`, elle est exécutée dans une threadpool externe qui est ensuite attendue, plutôt que d'être appelée directement (car cela bloquerait le serveur).

Si vous venez d'un autre framework async qui ne fonctionne pas de la façon décrite ci-dessus et que vous êtes habitué à définir des *fonctions de chemin d'accès* triviales faisant uniquement du calcul avec un simple `def` pour un faible gain de performance (environ 100 nanosecondes), veuillez noter que dans **FastAPI**, l'effet serait plutôt contraire. Dans ces cas-là, il vaut mieux utiliser `async def` à moins que vos *fonctions de chemin d'accès* utilisent du code qui effectue des opérations <abbr title="Input/Output - Entrées/Sorties: lecture ou écriture sur le disque, communications réseau.">I/O</abbr> bloquantes.

Au final, dans les deux situations, il est fort probable que **FastAPI** soit [tout de même plus rapide](index.md#performance) que (ou au moins comparable à) votre framework précédent.

### Dépendances { #dependencies }

La même chose s'applique aux [dépendances](tutorial/dependencies/index.md). Si une dépendance est une fonction standard `def` plutôt qu'`async def`, elle est exécutée dans la threadpool externe.

### Sous-dépendances { #sub-dependencies }

Vous pouvez avoir de multiples dépendances et [sous-dépendances](tutorial/dependencies/sub-dependencies.md) dépendant les unes des autres (en tant que paramètres des définitions des fonctions), certaines créées avec `async def` et d'autres avec un `def` normal. Cela fonctionnerait aussi, et celles définies avec un `def` normal seraient appelées sur un thread externe (venant de la threadpool) plutôt que d'être « attendues ».

### Autres fonctions utilitaires { #other-utility-functions }

Toute autre fonction utilitaire que vous appelez directement peut être créée avec un classique `def` ou avec `async def` et FastAPI n'aura pas d'impact sur la façon dont vous l'appelez.

Contrairement aux fonctions que FastAPI appelle pour vous : les *fonctions de chemin d'accès* et dépendances.

Si votre fonction utilitaire est une fonction classique définie avec `def`, elle sera appelée directement (telle qu'écrite dans votre code), pas dans une threadpool ; si la fonction est définie avec `async def` alors vous devez `await` cette fonction lorsque vous l'appelez dans votre code.

---

Encore une fois, ce sont des détails très techniques qui peuvent être utiles si vous venez ici les chercher.

Sinon, les instructions de la section ci-dessus sont largement suffisantes : <a href="#in-a-hurry">Vous êtes pressés ?</a>.
