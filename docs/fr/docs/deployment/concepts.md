# Concepts de déploiement { #deployments-concepts }

Lorsque vous déployez une application **FastAPI**, ou en fait n'importe quel type de web API, il existe plusieurs concepts qui vous importent probablement, et en les utilisant vous pouvez trouver la manière la **plus appropriée** de **déployer votre application**.

Parmi les concepts importants, on trouve :

* Sécurité - HTTPS
* Exécuter au démarrage
* Redémarrages
* Réplication (le nombre de processus en cours d'exécution)
* Mémoire
* Étapes préalables avant de démarrer

Nous allons voir comment ils affectent les **déploiements**.

Au final, l'objectif ultime est de pouvoir **servir vos clients d'API** de manière **sécurisée**, d'**éviter les interruptions**, et d'utiliser les **ressources de calcul** (par exemple des serveurs/VM distants) aussi efficacement que possible. 🚀

Je vais vous en dire un peu plus ici sur ces **concepts**, ce qui devrait vous donner l'**intuition** nécessaire pour décider comment déployer votre API dans des environnements très différents, voire même dans des environnements **futurs** qui n'existent pas encore.

En tenant compte de ces concepts, vous serez en mesure **d'évaluer et de concevoir** la meilleure façon de déployer **vos propres API**.

Dans les chapitres suivants, je vous donnerai des **recettes concrètes** pour déployer des applications FastAPI.

Mais pour l'instant, voyons ces **idées conceptuelles** importantes. Ces concepts s'appliquent aussi à tout autre type de web API. 💡

## Sécurité - HTTPS { #security-https }

Dans le [chapitre précédent à propos de HTTPS](https.md){.internal-link target=_blank}, nous avons vu comment HTTPS fournit le chiffrement pour votre API.

Nous avons également vu que HTTPS est normalement fourni par un composant **externe** à votre serveur d'application, un **TLS Termination Proxy**.

Et il doit y avoir quelque chose chargé de **renouveler les certificats HTTPS** ; cela peut être le même composant ou quelque chose de différent.

### Exemples d’outils pour HTTPS { #example-tools-for-https }

Parmi les outils que vous pourriez utiliser comme TLS Termination Proxy :

* Traefik
    * Gère automatiquement le renouvellement des certificats ✨
* Caddy
    * Gère automatiquement le renouvellement des certificats ✨
* Nginx
    * Avec un composant externe comme Certbot pour le renouvellement des certificats
* HAProxy
    * Avec un composant externe comme Certbot pour le renouvellement des certificats
* Kubernetes avec un Ingress Controller comme Nginx
    * Avec un composant externe comme cert-manager pour le renouvellement des certificats
* Pris en charge en interne par un fournisseur cloud dans le cadre de ses services (lisez ci-dessous 👇)

Une autre option consiste à utiliser un **service cloud** qui fait davantage de travail, y compris la mise en place de HTTPS. Il peut avoir certaines restrictions ou vous facturer davantage, etc. Mais dans ce cas, vous n'auriez pas à configurer vous‑même un TLS Termination Proxy.

Je vous montrerai des exemples concrets dans les prochains chapitres.

---

Les concepts suivants à considérer concernent tous le programme qui exécute votre API réelle (par ex. Uvicorn).

## Programme et processus { #program-and-process }

Nous allons beaucoup parler du « **processus** » en cours d'exécution, il est donc utile d'être clair sur ce que cela signifie, et sur la différence avec le mot « **programme** ».

### Qu'est-ce qu'un programme { #what-is-a-program }

Le mot **programme** est couramment utilisé pour décrire plusieurs choses :

* Le **code** que vous écrivez, les **fichiers Python**.
* Le **fichier** qui peut être **exécuté** par le système d'exploitation, par exemple : `python`, `python.exe` ou `uvicorn`.
* Un programme particulier lorsqu'il **s'exécute** sur le système d'exploitation, utilisant le CPU et stockant des choses en mémoire. On appelle aussi cela un **processus**.

### Qu'est-ce qu'un processus { #what-is-a-process }

Le mot **processus** est normalement utilisé de manière plus spécifique, en ne se référant qu'à l'élément qui s'exécute dans le système d'exploitation (comme dans le dernier point ci‑dessus) :

* Un programme particulier lorsqu'il **s'exécute** sur le système d'exploitation.
    * Cela ne se réfère ni au fichier, ni au code ; cela se réfère **spécifiquement** à l'élément qui est **exécuté** et géré par le système d'exploitation.
* N'importe quel programme, n'importe quel code, **ne peut faire des choses** que lorsqu'il est **exécuté**. Donc, lorsqu'il y a un **processus en cours**.
* Le processus peut être **arrêté** (ou « tué ») par vous ou par le système d'exploitation. À ce moment‑là, il cesse de s'exécuter/d'être exécuté, et il **ne peut plus rien faire**.
* Chaque application que vous avez en cours d'exécution sur votre ordinateur a un processus derrière elle, chaque programme lancé, chaque fenêtre, etc. Et il y a normalement de nombreux processus exécutés **en même temps** tant qu'un ordinateur est allumé.
* Il peut y avoir **plusieurs processus** du **même programme** exécutés simultanément.

Si vous ouvrez le « gestionnaire des tâches » ou le « moniteur système » (ou des outils similaires) de votre système d'exploitation, vous verrez nombre de ces processus en cours d'exécution.

Et, par exemple, vous verrez probablement qu'il y a plusieurs processus exécutant le même navigateur (Firefox, Chrome, Edge, etc.). Ils exécutent normalement un processus par onglet, plus quelques processus supplémentaires.

<img class="shadow" src="/img/deployment/concepts/image01.png">

---

Maintenant que nous connaissons la différence entre les termes **processus** et **programme**, continuons à parler des déploiements.

## Exécuter au démarrage { #running-on-startup }

Dans la plupart des cas, lorsque vous créez une web API, vous voulez qu'elle **tourne en permanence**, sans interruption, afin que vos clients puissent toujours y accéder. Bien sûr, sauf si vous avez une raison spécifique de ne vouloir l'exécuter que dans certaines situations, mais la plupart du temps vous la voulez constamment en cours et **disponible**.

### Sur un serveur distant { #in-a-remote-server }

Lorsque vous configurez un serveur distant (un serveur cloud, une machine virtuelle, etc.), la chose la plus simple à faire est d'utiliser `fastapi run` (qui utilise Uvicorn) ou quelque chose de similaire, manuellement, de la même manière que lorsque vous développez en local.

Et cela fonctionnera et sera utile **pendant le développement**.

Mais si votre connexion au serveur est coupée, le **processus en cours** va probablement s'arrêter.

Et si le serveur est redémarré (par exemple après des mises à jour, ou des migrations chez le fournisseur cloud) vous **ne le remarquerez probablement pas**. Et à cause de cela, vous ne saurez même pas que vous devez redémarrer le processus manuellement. Ainsi, votre API restera tout simplement à l'arrêt. 😱

### Lancer automatiquement au démarrage { #run-automatically-on-startup }

En général, vous voudrez probablement que le programme serveur (par ex. Uvicorn) soit démarré automatiquement au démarrage du serveur, et sans aucune **intervention humaine**, afin d'avoir en permanence un processus exécutant votre API (par ex. Uvicorn exécutant votre app FastAPI).

### Programme séparé { #separate-program }

Pour y parvenir, vous aurez normalement un **programme séparé** qui s'assure que votre application est lancée au démarrage. Et dans de nombreux cas, il s'assurera également que d'autres composants ou applications sont également lancés, par exemple une base de données.

### Exemples d’outils pour lancer au démarrage { #example-tools-to-run-at-startup }

Voici quelques exemples d'outils capables de faire ce travail :

* Docker
* Kubernetes
* Docker Compose
* Docker en mode Swarm
* Systemd
* Supervisor
* Pris en charge en interne par un fournisseur cloud dans le cadre de ses services
* Autres ...

Je vous donnerai des exemples plus concrets dans les prochains chapitres.

## Redémarrages { #restarts }

De la même manière que vous voulez vous assurer que votre application est lancée au démarrage, vous voulez probablement aussi vous assurer qu'elle est **redémarrée** après des échecs.

### Nous faisons des erreurs { #we-make-mistakes }

Nous, humains, faisons des **erreurs**, tout le temps. Les logiciels ont presque *toujours* des **bugs** cachés à différents endroits. 🐛

Et nous, développeurs, continuons à améliorer le code au fur et à mesure que nous trouvons ces bugs et que nous implémentons de nouvelles fonctionnalités (en ajoutant éventuellement de nouveaux bugs aussi 😅).

### Petites erreurs gérées automatiquement { #small-errors-automatically-handled }

Lors de la création de web API avec FastAPI, s'il y a une erreur dans notre code, FastAPI la contiendra normalement à la seule requête qui a déclenché l'erreur. 🛡

Le client recevra un **500 Internal Server Error** pour cette requête, mais l'application continuera de fonctionner pour les requêtes suivantes au lieu de simplement s'effondrer complètement.

### Erreurs plus importantes - plantages { #bigger-errors-crashes }

Néanmoins, il peut y avoir des cas où nous écrivons du code qui **fait planter l'application entière**, faisant planter Uvicorn et Python. 💥

Et malgré cela, vous ne voudrez probablement pas que l'application reste à l'arrêt parce qu'il y a eu une erreur à un endroit ; vous voudrez probablement qu'elle **continue de tourner**, au moins pour les *chemins d'accès* qui ne sont pas cassés.

### Redémarrer après un plantage { #restart-after-crash }

Mais dans ces cas avec de très mauvaises erreurs qui font planter le **processus** en cours, vous voudrez un composant externe chargé de **redémarrer** le processus, au moins quelques fois ...

/// tip | Astuce

... Bien que si l'application entière **plante immédiatement**, il n'est probablement pas logique de continuer à la redémarrer indéfiniment. Mais dans ces cas, vous le remarquerez probablement pendant le développement, ou au moins juste après le déploiement.

Concentrons‑nous donc sur les cas principaux, où elle pourrait planter entièrement dans certaines situations particulières **à l'avenir**, et où il est toujours logique de la redémarrer.

///

Vous voudrez probablement que l'élément chargé de redémarrer votre application soit un **composant externe**, car à ce stade, l'application elle‑même avec Uvicorn et Python a déjà planté, donc il n'y a rien dans le même code de la même app qui pourrait y faire quoi que ce soit.

### Exemples d’outils pour redémarrer automatiquement { #example-tools-to-restart-automatically }

Dans la plupart des cas, le même outil qui est utilisé pour **lancer le programme au démarrage** est également utilisé pour gérer les **redémarrages** automatiques.

Par exemple, cela peut être géré par :

* Docker
* Kubernetes
* Docker Compose
* Docker en mode Swarm
* Systemd
* Supervisor
* Pris en charge en interne par un fournisseur cloud dans le cadre de ses services
* Autres ...

## Réplication - Processus et mémoire { #replication-processes-and-memory }

Avec une application FastAPI, en utilisant un programme serveur comme la commande `fastapi` qui exécute Uvicorn, l'exécuter une fois dans **un processus** peut servir plusieurs clients simultanément.

Mais dans de nombreux cas, vous voudrez exécuter plusieurs processus de travail en même temps.

### Multiples processus - Workers { #multiple-processes-workers }

Si vous avez plus de clients que ce qu'un seul processus peut gérer (par exemple si la machine virtuelle n'est pas très grande) et que vous avez **plusieurs cœurs** dans le CPU du serveur, alors vous pouvez avoir **plusieurs processus** exécutant la même application simultanément, et distribuer toutes les requêtes entre eux.

Quand vous exécutez **plusieurs processus** du même programme d'API, on les appelle couramment des **workers**.

### Processus workers et ports { #worker-processes-and-ports }

Rappelez‑vous, d'après les documents [À propos de HTTPS](https.md){.internal-link target=_blank}, qu'un seul processus peut écouter une combinaison de port et d'adresse IP sur un serveur ?

C'est toujours vrai.

Donc, pour pouvoir avoir **plusieurs processus** en même temps, il doit y avoir un **seul processus à l'écoute sur un port** qui transmet ensuite la communication à chaque processus worker d'une manière ou d'une autre.

### Mémoire par processus { #memory-per-process }

Maintenant, lorsque le programme charge des choses en mémoire, par exemple, un modèle de machine learning dans une variable, ou le contenu d'un gros fichier dans une variable, tout cela **consomme une partie de la mémoire (RAM)** du serveur.

Et plusieurs processus **ne partagent normalement pas de mémoire**. Cela signifie que chaque processus en cours a ses propres éléments, variables et mémoire. Et si vous consommez une grande quantité de mémoire dans votre code, **chaque processus** consommera une quantité équivalente de mémoire.

### Mémoire du serveur { #server-memory }

Par exemple, si votre code charge un modèle de Machine Learning de **1 Go**, lorsque vous exécutez un processus avec votre API, il consommera au moins 1 Go de RAM. Et si vous démarrez **4 processus** (4 workers), chacun consommera 1 Go de RAM. Donc au total, votre API consommera **4 Go de RAM**.

Et si votre serveur distant ou votre machine virtuelle n'a que 3 Go de RAM, essayer de charger plus de 4 Go de RAM posera problème. 🚨

### Multiples processus - Un exemple { #multiple-processes-an-example }

Dans cet exemple, il y a un **processus gestionnaire** qui démarre et contrôle deux **processus workers**.

Ce processus gestionnaire serait probablement celui qui écoute sur le **port** de l'IP. Et il transmettrait toute la communication aux processus workers.

Ces processus workers seraient ceux qui exécutent votre application, ils effectueraient les calculs principaux pour recevoir une **requête** et renvoyer une **réponse**, et ils chargeraient tout ce que vous mettez dans des variables en RAM.

<img src="/img/deployment/concepts/process-ram.drawio.svg">

Et bien sûr, la même machine aurait probablement **d'autres processus** en cours d'exécution également, en plus de votre application.

Un détail intéressant est que le pourcentage de **CPU utilisé** par chaque processus peut **varier** fortement dans le temps, mais la **mémoire (RAM)** reste normalement plus ou moins **stable**.

Si vous avez une API qui effectue une quantité comparable de calculs à chaque fois et que vous avez beaucoup de clients, alors l'**utilisation du CPU** sera probablement *également stable* (au lieu de monter et descendre rapidement en permanence).

### Exemples d’outils et de stratégies de réplication { #examples-of-replication-tools-and-strategies }

Il peut y avoir plusieurs approches pour y parvenir, et je vous en dirai plus sur des stratégies spécifiques dans les prochains chapitres, par exemple en parlant de Docker et des conteneurs.

La principale contrainte à considérer est qu'il doit y avoir un **seul** composant gérant le **port** sur l'**IP publique**. Et il doit ensuite avoir un moyen de **transmettre** la communication aux **processus/workers** répliqués.

Voici quelques combinaisons et stratégies possibles :

* **Uvicorn** avec `--workers`
    * Un **gestionnaire de processus** Uvicorn écouterait sur l'**IP** et le **port**, et il démarrerait **plusieurs processus workers Uvicorn**.
* **Kubernetes** et autres systèmes **de conteneurs** distribués
    * Quelque chose dans la couche **Kubernetes** écouterait sur l'**IP** et le **port**. La réplication se ferait en ayant **plusieurs conteneurs**, chacun avec **un processus Uvicorn** en cours.
* **Services cloud** qui s'en chargent pour vous
    * Le service cloud **gérera probablement la réplication pour vous**. Il vous permettra éventuellement de définir **un processus à exécuter**, ou une **image de conteneur** à utiliser ; dans tous les cas, ce sera très probablement **un seul processus Uvicorn**, et le service cloud sera chargé de le répliquer.

/// tip | Astuce

Ne vous inquiétez pas si certains de ces éléments concernant les **conteneurs**, Docker ou Kubernetes ne sont pas encore très clairs.

Je vous en dirai plus sur les images de conteneurs, Docker, Kubernetes, etc. dans un chapitre à venir : [FastAPI dans des conteneurs - Docker](docker.md){.internal-link target=_blank}.

///

## Étapes préalables avant de démarrer { #previous-steps-before-starting }

Il existe de nombreux cas où vous souhaitez effectuer certaines étapes **avant de démarrer** votre application.

Par exemple, vous pourriez vouloir exécuter des **migrations de base de données**.

Mais dans la plupart des cas, vous voudrez effectuer ces étapes **une seule fois**.

Vous voudrez donc avoir un **processus unique** pour effectuer ces **étapes préalables**, avant de démarrer l'application.

Et vous devez vous assurer que c'est un processus unique qui exécute ces étapes préalables *même si*, ensuite, vous démarrez **plusieurs processus** (plusieurs workers) pour l'application elle‑même. Si ces étapes étaient exécutées par **plusieurs processus**, ils **dupliqueraient** le travail en l'exécutant **en parallèle**, et si les étapes étaient délicates comme une migration de base de données, elles pourraient entrer en conflit les unes avec les autres.

Bien sûr, il y a des cas où il n'y a aucun problème à exécuter les étapes préalables plusieurs fois ; dans ce cas, c'est beaucoup plus simple à gérer.

/// tip | Astuce

Gardez aussi à l'esprit que selon votre configuration, dans certains cas vous **n'aurez peut‑être même pas besoin d'étapes préalables** avant de démarrer votre application.

Dans ce cas, vous n'auriez pas à vous soucier de tout cela. 🤷

///

### Exemples de stratégies pour les étapes préalables { #examples-of-previous-steps-strategies }

Cela **dépendra fortement** de la manière dont vous **déployez votre système**, et sera probablement lié à votre manière de démarrer les programmes, de gérer les redémarrages, etc.

Voici quelques idées possibles :

* Un « Init Container » dans Kubernetes qui s'exécute avant votre conteneur d'application
* Un script bash qui exécute les étapes préalables puis démarre votre application
    * Vous aurez toujours besoin d'un moyen de démarrer/redémarrer *ce* script bash, de détecter les erreurs, etc.

/// tip | Astuce

Je vous donnerai des exemples plus concrets pour faire cela avec des conteneurs dans un chapitre à venir : [FastAPI dans des conteneurs - Docker](docker.md){.internal-link target=_blank}.

///

## Utilisation des ressources { #resource-utilization }

Votre ou vos serveurs constituent une **ressource** que vos programmes peuvent consommer ou **utiliser** : le temps de calcul des CPU et la mémoire RAM disponible.

Quelle quantité des ressources système voulez‑vous consommer/utiliser ? Il peut être facile de penser « pas beaucoup », mais en réalité, vous voudrez probablement consommer **le plus possible sans planter**.

Si vous payez pour 3 serveurs mais que vous n'utilisez qu'un petit peu de leur RAM et CPU, vous **gaspillez probablement de l'argent** 💸, et **gaspillez probablement l'électricité des serveurs** 🌎, etc.

Dans ce cas, il pourrait être préférable de n'avoir que 2 serveurs et d'utiliser un pourcentage plus élevé de leurs ressources (CPU, mémoire, disque, bande passante réseau, etc.).

À l'inverse, si vous avez 2 serveurs et que vous utilisez **100 % de leur CPU et de leur RAM**, à un moment donné un processus demandera plus de mémoire, et le serveur devra utiliser le disque comme « mémoire » (ce qui peut être des milliers de fois plus lent), voire **planter**. Ou un processus pourrait avoir besoin de faire un calcul et devrait attendre que le CPU soit à nouveau libre.

Dans ce cas, il serait préférable d'obtenir **un serveur supplémentaire** et d'y exécuter certains processus afin qu'ils aient tous **suffisamment de RAM et de temps CPU**.

Il est également possible que, pour une raison quelconque, vous ayez un **pic** d'utilisation de votre API. Peut‑être qu'elle devient virale, ou peut‑être que d'autres services ou bots commencent à l'utiliser. Et vous voudrez peut‑être disposer de ressources supplémentaires pour être en sécurité dans ces cas.

Vous pouvez définir un **chiffre arbitraire** comme cible, par exemple **entre 50 % et 90 %** d'utilisation des ressources. L'idée est que ce sont probablement les principaux éléments que vous voudrez mesurer et utiliser pour ajuster vos déploiements.

Vous pouvez utiliser des outils simples comme `htop` pour voir le CPU et la RAM utilisés sur votre serveur ou la quantité utilisée par chaque processus. Ou vous pouvez utiliser des outils de supervision plus complexes, éventuellement distribués sur plusieurs serveurs, etc.

## Récapitulatif { #recap }

Vous venez de lire ici certains des principaux concepts que vous devrez probablement garder à l'esprit lorsque vous décidez comment déployer votre application :

* Sécurité - HTTPS
* Exécuter au démarrage
* Redémarrages
* Réplication (le nombre de processus en cours d'exécution)
* Mémoire
* Étapes préalables avant de démarrer

Comprendre ces idées et comment les appliquer devrait vous donner l'intuition nécessaire pour prendre toutes les décisions lors de la configuration et de l'ajustement de vos déploiements. 🤓

Dans les sections suivantes, je vous donnerai des exemples plus concrets de stratégies possibles à suivre. 🚀
