# FastAPI dans des conteneurs - Docker { #fastapi-in-containers-docker }

Lors du déploiement d'applications FastAPI, une approche courante consiste à construire une **image de conteneur Linux**. C'est généralement fait avec <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a>. Vous pouvez ensuite déployer cette image de conteneur de plusieurs façons possibles.

L'utilisation de conteneurs Linux présente plusieurs avantages, notamment la **sécurité**, la **réplicabilité**, la **simplicité**, entre autres.

/// tip | Astuce

Vous êtes pressé et vous connaissez déjà tout ça ? Allez directement au [`Dockerfile` ci-dessous 👇](#build-a-docker-image-for-fastapi).

///

<details>
<summary>Aperçu du Dockerfile 👀</summary>

```Dockerfile
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# Si vous exécutez derrière un proxy comme Nginx ou Traefik, ajoutez --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

</details>

## Qu'est-ce qu'un conteneur { #what-is-a-container }

Les conteneurs (principalement les conteneurs Linux) sont un moyen très **léger** d'empaqueter des applications, y compris toutes leurs dépendances et les fichiers nécessaires, tout en les isolant des autres conteneurs (autres applications ou composants) dans le même système.

Les conteneurs Linux s'exécutent en utilisant le même noyau Linux que l'hôte (machine, machine virtuelle, serveur cloud, etc.). Cela signifie simplement qu'ils sont très légers (comparés à des machines virtuelles complètes émulant un système d'exploitation entier).

Ainsi, les conteneurs consomment **peu de ressources**, une quantité comparable à l'exécution directe des processus (alors qu'une machine virtuelle consommerait beaucoup plus).

Les conteneurs ont également leurs propres processus d'exécution **isolés** (généralement un seul processus), leur système de fichiers et leur réseau, ce qui simplifie le déploiement, la sécurité, le développement, etc.

## Qu'est-ce qu'une image de conteneur { #what-is-a-container-image }

Un **conteneur** s'exécute à partir d'une **image de conteneur**.

Une image de conteneur est une version **statique** de tous les fichiers, des variables d'environnement et de la commande/le programme par défaut devant être présents dans un conteneur. Ici, **statique** signifie que l'**image** du conteneur ne s'exécute pas, elle n'est pas en cours d'exécution, ce ne sont que les fichiers et métadonnées empaquetés.

Par opposition à une « **image de conteneur** » qui correspond aux contenus statiques stockés, un « **conteneur** » fait normalement référence à l'instance en cours d'exécution, la chose qui est **exécutée**.

Lorsque le **conteneur** est démarré et en cours d'exécution (démarré à partir d'une **image de conteneur**), il peut créer ou modifier des fichiers, des variables d'environnement, etc. Ces changements n'existeront que dans ce conteneur, mais ne persisteront pas dans l'image de conteneur sous-jacente (ils ne seront pas enregistrés sur le disque).

Une image de conteneur est comparable au **programme** et à ses contenus, par exemple `python` et un fichier `main.py`.

Et le **conteneur** lui-même (par opposition à l'**image de conteneur**) est l'instance en cours d'exécution réelle de l'image, comparable à un **processus**. En fait, un conteneur ne fonctionne que lorsqu'il a un **processus en cours d'exécution** (et normalement, il s'agit d'un seul processus). Le conteneur s'arrête lorsqu'aucun processus n'y est en cours d'exécution.

## Images de conteneur { #container-images }

Docker a été l'un des principaux outils pour créer et gérer des **images de conteneur** et des **conteneurs**.

Et il existe un <a href="https://hub.docker.com/" class="external-link" target="_blank">Docker Hub</a> public avec des **images de conteneur officielles** pré-construites pour de nombreux outils, environnements, bases de données et applications.

Par exemple, il existe une <a href="https://hub.docker.com/_/python" class="external-link" target="_blank">image Python officielle</a>.

Et il existe beaucoup d'autres images pour différentes choses comme des bases de données, par exemple :

* <a href="https://hub.docker.com/_/postgres" class="external-link" target="_blank">PostgreSQL</a>
* <a href="https://hub.docker.com/_/mysql" class="external-link" target="_blank">MySQL</a>
* <a href="https://hub.docker.com/_/mongo" class="external-link" target="_blank">MongoDB</a>
* <a href="https://hub.docker.com/_/redis" class="external-link" target="_blank">Redis</a>, etc.

En utilisant une image de conteneur pré-construite, il est très facile de **combiner** et d'utiliser différents outils. Par exemple, pour essayer une nouvelle base de données. Dans la plupart des cas, vous pouvez utiliser les **images officielles** et simplement les configurer avec des variables d'environnement.

Ainsi, dans de nombreux cas, vous pouvez apprendre les conteneurs et Docker et réutiliser ces connaissances avec de nombreux outils et composants différents.

Vous exécuteriez donc **plusieurs conteneurs** avec des éléments différents, comme une base de données, une application Python, un serveur web avec une application frontend React, et les connecter entre eux via leur réseau interne.

Tous les systèmes de gestion de conteneurs (comme Docker ou Kubernetes) disposent de ces fonctionnalités réseau intégrées.

## Conteneurs et processus { #containers-and-processes }

Une **image de conteneur** inclut normalement dans ses métadonnées le programme/la commande par défaut à exécuter lorsque le **conteneur** est démarré et les paramètres à transmettre à ce programme. Très similaire à ce que vous utiliseriez en ligne de commande.

Lorsqu'un **conteneur** est démarré, il exécutera cette commande/ce programme (bien que vous puissiez la/le remplacer et faire exécuter une autre commande/un autre programme).

Un conteneur fonctionne tant que le **processus principal** (commande ou programme) est en cours d'exécution.

Un conteneur a normalement un **seul processus**, mais il est aussi possible de démarrer des sous-processus à partir du processus principal, et ainsi vous aurez **plusieurs processus** dans le même conteneur.

Mais il n'est pas possible d'avoir un conteneur en cours d'exécution sans **au moins un processus en cours**. Si le processus principal s'arrête, le conteneur s'arrête.

## Construire une image Docker pour FastAPI { #build-a-docker-image-for-fastapi }

Très bien, construisons quelque chose maintenant ! 🚀

Je vais vous montrer comment construire une **image Docker** pour FastAPI **à partir de zéro**, basée sur l'image **officielle Python**.

C'est ce que vous voudrez faire dans **la plupart des cas**, par exemple :

* Utiliser **Kubernetes** ou des outils similaires
* Exécuter sur un **Raspberry Pi**
* Utiliser un service cloud qui exécuterait une image de conteneur pour vous, etc.

### Dépendances des paquets { #package-requirements }

Vous aurez normalement les **dépendances des paquets** de votre application dans un fichier.

Cela dépendra principalement de l'outil que vous utilisez pour **installer** ces dépendances.

La manière la plus courante consiste à avoir un fichier `requirements.txt` avec les noms des paquets et leurs versions, un par ligne.

Vous utiliserez bien sûr les mêmes idées que vous avez lues dans [À propos des versions de FastAPI](versions.md){.internal-link target=_blank} pour définir les plages de versions.

Par exemple, votre `requirements.txt` pourrait ressembler à :

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

Et vous installerez normalement ces dépendances de paquets avec `pip`, par exemple :

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

</div>

/// info

Il existe d'autres formats et outils pour définir et installer des dépendances de paquets.

///

### Créer le code **FastAPI** { #create-the-fastapi-code }

* Créez un répertoire `app` et entrez dedans.
* Créez un fichier vide `__init__.py`.
* Créez un fichier `main.py` avec :

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile { #dockerfile }

Maintenant, dans le même répertoire de projet, créez un fichier `Dockerfile` avec :

```{ .dockerfile .annotate }
# (1)!
FROM python:3.14

# (2)!
WORKDIR /code

# (3)!
COPY ./requirements.txt /code/requirements.txt

# (4)!
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)!
COPY ./app /code/app

# (6)!
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

1. Démarrer à partir de l'image de base Python officielle.

2. Définir le répertoire de travail courant sur `/code`.

    C'est là que nous placerons le fichier `requirements.txt` et le répertoire `app`.

3. Copier le fichier des dépendances vers le répertoire `/code`.

    Copier **uniquement** le fichier des dépendances en premier, pas le reste du code.

    Comme ce fichier **ne change pas souvent**, Docker le détectera et utilisera le **cache** pour cette étape, ce qui activera le cache pour l'étape suivante aussi.

4. Installer les dépendances listées dans le fichier des dépendances.

    L'option `--no-cache-dir` indique à `pip` de ne pas enregistrer localement les paquets téléchargés, car cela ne sert que si `pip` devait être relancé pour installer les mêmes paquets, mais ce n'est pas le cas lorsque l'on travaille avec des conteneurs.

    /// note | Remarque

    Le `--no-cache-dir` concerne uniquement `pip`, cela n'a rien à voir avec Docker ou les conteneurs.

    ///

    L'option `--upgrade` indique à `pip` de mettre à niveau les paquets s'ils sont déjà installés.

    Comme l'étape précédente de copie du fichier peut être détectée par le **cache Docker**, cette étape **utilisera également le cache Docker** lorsqu'il est disponible.

    L'utilisation du cache à cette étape vous **fera gagner** beaucoup de **temps** lors de la reconstruction de l'image encore et encore pendant le développement, au lieu de **télécharger et installer** toutes les dépendances **à chaque fois**.

5. Copier le répertoire `./app` dans le répertoire `/code`.

    Comme cela contient tout le code qui est ce qui **change le plus fréquemment**, le **cache** Docker ne sera pas facilement utilisé pour cette étape ou pour les **étapes suivantes**.

    Il est donc important de placer cela **vers la fin** du `Dockerfile`, pour optimiser les temps de construction de l'image de conteneur.

6. Définir la **commande** pour utiliser `fastapi run`, qui utilise Uvicorn sous le capot.

    `CMD` prend une liste de chaînes, chacune de ces chaînes correspond à ce que vous taperiez en ligne de commande séparé par des espaces.

    Cette commande sera exécutée à partir du **répertoire de travail courant**, le même répertoire `/code` que vous avez défini plus haut avec `WORKDIR /code`.

/// tip | Astuce

Passez en revue ce que fait chaque ligne en cliquant sur chaque bulle numérotée dans le code. 👆

///

/// warning | Alertes

Vous devez vous assurer d'utiliser **toujours** la **forme exec** de l'instruction `CMD`, comme expliqué ci-dessous.

///

#### Utiliser `CMD` - Forme Exec { #use-cmd-exec-form }

L'instruction Docker <a href="https://docs.docker.com/reference/dockerfile/#cmd" class="external-link" target="_blank">`CMD`</a> peut être écrite sous deux formes :

✅ Forme **Exec** :

```Dockerfile
# ✅ À faire
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ Forme **Shell** :

```Dockerfile
# ⛔️ À ne pas faire
CMD fastapi run app/main.py --port 80
```

Assurez-vous d'utiliser toujours la forme **exec** pour garantir que FastAPI peut s'arrêter proprement et que les [événements de cycle de vie](../advanced/events.md){.internal-link target=_blank} sont déclenchés.

Vous pouvez en lire davantage dans la <a href="https://docs.docker.com/reference/dockerfile/#shell-and-exec-form" class="external-link" target="_blank">documentation Docker sur les formes shell et exec</a>.

Cela peut être très visible lors de l'utilisation de `docker compose`. Voir cette section de la FAQ Docker Compose pour plus de détails techniques : <a href="https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop" class="external-link" target="_blank">Pourquoi mes services mettent-ils 10 secondes à se recréer ou à s'arrêter ?</a>.

#### Structure du répertoire { #directory-structure }

Vous devriez maintenant avoir une structure de répertoire comme :

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### Derrière un proxy de terminaison TLS { #behind-a-tls-termination-proxy }

Si vous exécutez votre conteneur derrière un proxy de terminaison TLS (load balancer) comme Nginx ou Traefik, ajoutez l'option `--proxy-headers`, cela indiquera à Uvicorn (via la CLI FastAPI) de faire confiance aux en-têtes envoyés par ce proxy lui indiquant que l'application s'exécute derrière HTTPS, etc.

```Dockerfile
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### Cache Docker { #docker-cache }

Il y a une astuce importante dans ce `Dockerfile`, nous copions d'abord **le fichier des dépendances seul**, pas le reste du code. Laissez-moi vous expliquer pourquoi.

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Docker et d'autres outils **construisent** ces images de conteneur **de manière incrémentale**, en ajoutant **une couche au-dessus de l'autre**, en commençant par le haut du `Dockerfile` et en ajoutant tous les fichiers créés par chacune des instructions du `Dockerfile`.

Docker et des outils similaires utilisent également un **cache interne** lors de la construction de l'image : si un fichier n'a pas changé depuis la dernière construction de l'image de conteneur, alors il va **réutiliser la même couche** créée la dernière fois, au lieu de recopier le fichier et créer une nouvelle couche à partir de zéro.

Éviter simplement la copie des fichiers n'améliore pas nécessairement les choses de manière significative, mais comme il a utilisé le cache pour cette étape, il peut **utiliser le cache pour l'étape suivante**. Par exemple, il peut utiliser le cache pour l'instruction qui installe les dépendances avec :

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

Le fichier des dépendances **ne changera pas fréquemment**. Ainsi, en copiant uniquement ce fichier, Docker pourra **utiliser le cache** pour cette étape.

Et ensuite, Docker pourra **utiliser le cache pour l'étape suivante** qui télécharge et installe ces dépendances. Et c'est là que nous **gagnons beaucoup de temps**. ✨ ... et évitons l'ennui en attendant. 😪😆

Télécharger et installer les dépendances de paquets **peut prendre des minutes**, mais utiliser le **cache** ne **prendra que quelques secondes** au plus.

Et comme vous reconstruirez l'image de conteneur encore et encore pendant le développement pour vérifier que vos modifications de code fonctionnent, cela vous fera gagner beaucoup de temps cumulé.

Ensuite, vers la fin du `Dockerfile`, nous copions tout le code. Comme c'est ce qui **change le plus fréquemment**, nous le plaçons vers la fin, car presque toujours, tout ce qui suit cette étape ne pourra pas utiliser le cache.

```Dockerfile
COPY ./app /code/app
```

### Construire l'image Docker { #build-the-docker-image }

Maintenant que tous les fichiers sont en place, construisons l'image de conteneur.

* Allez dans le répertoire du projet (là où se trouve votre `Dockerfile`, contenant votre répertoire `app`).
* Construisez votre image FastAPI :

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

/// tip | Astuce

Remarquez le `.` à la fin, équivalent à `./`, il indique à Docker le répertoire à utiliser pour construire l'image de conteneur.

Dans ce cas, c'est le même répertoire courant (`.`).

///

### Démarrer le conteneur Docker { #start-the-docker-container }

* Exécutez un conteneur basé sur votre image :

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## Vérifier { #check-it }

Vous devriez pouvoir le vérifier via l'URL de votre conteneur Docker, par exemple : <a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> ou <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a> (ou équivalent, en utilisant votre hôte Docker).

Vous verrez quelque chose comme :

```JSON
{"item_id": 5, "q": "somequery"}
```

## Documentation interactive de l'API { #interactive-api-docs }

Vous pouvez maintenant aller sur <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> ou <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a> (ou équivalent, en utilisant votre hôte Docker).

Vous verrez la documentation interactive automatique de l'API (fournie par <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>) :

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## Documentation alternative de l'API { #alternative-api-docs }

Et vous pouvez aussi aller sur <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> ou <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a> (ou équivalent, en utilisant votre hôte Docker).

Vous verrez la documentation automatique alternative (fournie par <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>) :

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Construire une image Docker avec un FastAPI mono-fichier { #build-a-docker-image-with-a-single-file-fastapi }

Si votre FastAPI est un seul fichier, par exemple `main.py` sans répertoire `./app`, votre structure de fichiers pourrait ressembler à ceci :

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

Vous n'auriez alors qu'à changer les chemins correspondants pour copier le fichier dans le `Dockerfile` :

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)!
COPY ./main.py /code/

# (2)!
CMD ["fastapi", "run", "main.py", "--port", "80"]
```

1. Copier le fichier `main.py` directement dans le répertoire `/code` (sans répertoire `./app`).

2. Utiliser `fastapi run` pour servir votre application dans le fichier unique `main.py`.

Lorsque vous passez le fichier à `fastapi run`, il détectera automatiquement qu'il s'agit d'un fichier unique et non d'un package et saura comment l'importer et servir votre application FastAPI. 😎

## Concepts de déploiement { #deployment-concepts }

Parlons à nouveau de certains des mêmes [Concepts de déploiement](concepts.md){.internal-link target=_blank} en termes de conteneurs.

Les conteneurs sont principalement un outil pour simplifier le processus de **construction et de déploiement** d'une application, mais ils n'imposent pas une approche particulière pour gérer ces **concepts de déploiement**, et il existe plusieurs stratégies possibles.

La **bonne nouvelle**, c'est qu'avec chaque stratégie différente, il existe un moyen de couvrir tous les concepts de déploiement. 🎉

Passons en revue ces **concepts de déploiement** en termes de conteneurs :

* HTTPS
* Exécution au démarrage
* Redémarrages
* Réplication (le nombre de processus en cours d'exécution)
* Mémoire
* Étapes préalables au démarrage

## HTTPS { #https }

Si l'on se concentre uniquement sur l'**image de conteneur** pour une application FastAPI (et plus tard sur le **conteneur** en cours d'exécution), HTTPS serait normalement géré **à l'extérieur** par un autre outil.

Cela pourrait être un autre conteneur, par exemple avec <a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a>, gérant **HTTPS** et l'acquisition **automatique** des **certificats**.

/// tip | Astuce

Traefik s'intègre avec Docker, Kubernetes, et d'autres, donc il est très facile de configurer HTTPS pour vos conteneurs avec lui.

///

Alternativement, HTTPS pourrait être géré par un fournisseur cloud comme l'un de leurs services (tout en exécutant l'application dans un conteneur).

## Exécution au démarrage et redémarrages { #running-on-startup-and-restarts }

Il y a normalement un autre outil chargé de **démarrer et exécuter** votre conteneur.

Cela pourrait être **Docker** directement, **Docker Compose**, **Kubernetes**, un **service cloud**, etc.

Dans la plupart (ou toutes) des situations, il existe une option simple pour activer l'exécution du conteneur au démarrage et activer les redémarrages en cas d'échec. Par exemple, dans Docker, c'est l'option de ligne de commande `--restart`.

Sans utiliser de conteneurs, faire en sorte que les applications s'exécutent au démarrage et avec redémarrages peut être fastidieux et difficile. Mais en **travaillant avec des conteneurs**, dans la plupart des cas, cette fonctionnalité est incluse par défaut. ✨

## Réplication - Nombre de processus { #replication-number-of-processes }

Si vous avez un <dfn title="Groupe de machines configurées pour être connectées et fonctionner ensemble d'une certaine manière.">cluster</dfn> de machines avec **Kubernetes**, Docker Swarm Mode, Nomad, ou un autre système complexe similaire pour gérer des conteneurs distribués sur plusieurs machines, alors vous voudrez probablement **gérer la réplication** au **niveau du cluster** plutôt que d'utiliser un **gestionnaire de processus** (comme Uvicorn avec workers) dans chaque conteneur.

L'un de ces systèmes de gestion de conteneurs distribués comme Kubernetes dispose normalement d'une manière intégrée de gérer la **réplication des conteneurs** tout en supportant l'**équilibrage de charge** des requêtes entrantes. Le tout au **niveau du cluster**.

Dans ces cas, vous voudrez probablement construire une **image Docker à partir de zéro** comme [expliqué ci-dessus](#dockerfile), en installant vos dépendances et en exécutant **un seul processus Uvicorn** au lieu d'utiliser plusieurs workers Uvicorn.

### Équilibreur de charge { #load-balancer }

Lors de l'utilisation de conteneurs, vous aurez normalement un composant **à l'écoute sur le port principal**. Cela pourrait être un autre conteneur qui est également un **proxy de terminaison TLS** pour gérer **HTTPS** ou un outil similaire.

Comme ce composant prend la **charge** des requêtes et la distribue entre les workers de façon (espérons-le) **équilibrée**, on l'appelle également communément un **équilibreur de charge**.

/// tip | Astuce

Le même composant de **proxy de terminaison TLS** utilisé pour HTTPS sera probablement aussi un **équilibreur de charge**.

///

Et en travaillant avec des conteneurs, le même système que vous utilisez pour les démarrer et les gérer dispose déjà d'outils internes pour transmettre la **communication réseau** (par ex. les requêtes HTTP) depuis cet **équilibreur de charge** (qui peut aussi être un **proxy de terminaison TLS**) vers le ou les conteneurs avec votre application.

### Un équilibreur de charge - Plusieurs conteneurs worker { #one-load-balancer-multiple-worker-containers }

Lorsque vous travaillez avec **Kubernetes** ou des systèmes de gestion de conteneurs distribués similaires, l'utilisation de leurs mécanismes réseau internes permet au **seul équilibreur de charge** à l'écoute sur le **port** principal de transmettre la communication (les requêtes) vers potentiellement **plusieurs conteneurs** exécutant votre application.

Chacun de ces conteneurs exécutant votre application aura normalement **un seul processus** (par ex. un processus Uvicorn exécutant votre application FastAPI). Ils seront tous des **conteneurs identiques**, exécutant la même chose, mais chacun avec son propre processus, sa mémoire, etc. De cette façon, vous profiterez de la **parallélisation** sur **différents cœurs** du CPU, voire sur **différentes machines**.

Et le système de conteneurs distribués avec l'**équilibreur de charge** **distribuera les requêtes** à chacun des conteneurs exécutant votre application **à tour de rôle**. Ainsi, chaque requête pourrait être traitée par l'un des multiples **conteneurs répliqués** exécutant votre application.

Et normalement cet **équilibreur de charge** pourra gérer des requêtes qui vont vers *d'autres* applications dans votre cluster (par ex. vers un autre domaine, ou sous un autre préfixe de chemin d'URL), et transmettra cette communication aux bons conteneurs pour *cette autre* application s'exécutant dans votre cluster.

### Un processus par conteneur { #one-process-per-container }

Dans ce type de scénario, vous voudrez probablement avoir **un seul processus (Uvicorn) par conteneur**, puisque vous gérez déjà la réplication au niveau du cluster.

Donc, dans ce cas, vous **ne voudrez pas** avoir plusieurs workers dans le conteneur, par exemple avec l'option de ligne de commande `--workers`. Vous voudrez avoir **un seul processus Uvicorn** par conteneur (mais probablement plusieurs conteneurs).

Avoir un autre gestionnaire de processus à l'intérieur du conteneur (comme ce serait le cas avec plusieurs workers) n'ajouterait que de la **complexité inutile** que vous gérez très probablement déjà avec votre système de cluster.

### Conteneurs avec plusieurs processus et cas particuliers { #containers-with-multiple-processes-and-special-cases }

Bien sûr, il existe des **cas particuliers** où vous pourriez vouloir avoir **un conteneur** avec plusieurs **processus worker Uvicorn** à l'intérieur.

Dans ces cas, vous pouvez utiliser l'option de ligne de commande `--workers` pour définir le nombre de workers que vous souhaitez exécuter :

```{ .dockerfile .annotate }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1. Ici, nous utilisons l'option de ligne de commande `--workers` pour définir le nombre de workers à 4.

Voici quelques exemples où cela pourrait avoir du sens :

#### Une application simple { #a-simple-app }

Vous pourriez vouloir un gestionnaire de processus dans le conteneur si votre application est **suffisamment simple** pour s'exécuter sur un **seul serveur**, pas un cluster.

#### Docker Compose { #docker-compose }

Vous pourriez déployer sur un **seul serveur** (pas un cluster) avec **Docker Compose**, donc vous n'auriez pas un moyen simple de gérer la réplication des conteneurs (avec Docker Compose) tout en préservant le réseau partagé et l'**équilibrage de charge**.

Vous pourriez alors vouloir avoir **un seul conteneur** avec un **gestionnaire de processus** qui démarre **plusieurs processus worker** à l'intérieur.

---

L'idée principale est que **rien** de tout cela ne sont des **règles gravées dans la pierre** que vous devez suivre aveuglément. Vous pouvez utiliser ces idées pour **évaluer votre propre cas d'usage** et décider de la meilleure approche pour votre système, en vérifiant comment gérer les concepts suivants :

* Sécurité - HTTPS
* Exécution au démarrage
* Redémarrages
* Réplication (le nombre de processus en cours d'exécution)
* Mémoire
* Étapes préalables au démarrage

## Mémoire { #memory }

Si vous exécutez **un seul processus par conteneur**, vous aurez une quantité de mémoire consommée plus ou moins bien définie, stable et limitée par chacun de ces conteneurs (plus d'un s'ils sont répliqués).

Vous pouvez alors définir ces mêmes limites et exigences de mémoire dans vos configurations pour votre système de gestion de conteneurs (par exemple dans **Kubernetes**). De cette façon, il pourra **répliquer les conteneurs** sur les **machines disponibles** en tenant compte de la quantité de mémoire dont ils ont besoin et de la quantité disponible sur les machines du cluster.

Si votre application est **simple**, cela ne sera probablement **pas un problème**, et vous n'aurez peut-être pas besoin de spécifier des limites de mémoire strictes. Mais si vous **utilisez beaucoup de mémoire** (par exemple avec des modèles de **machine learning**), vous devez vérifier combien de mémoire vous consommez et ajuster le **nombre de conteneurs** qui s'exécutent sur **chaque machine** (et peut-être ajouter plus de machines à votre cluster).

Si vous exécutez **plusieurs processus par conteneur**, vous devez vous assurer que le nombre de processus démarrés ne **consomme pas plus de mémoire** que ce qui est disponible.

## Étapes préalables au démarrage et conteneurs { #previous-steps-before-starting-and-containers }

Si vous utilisez des conteneurs (par ex. Docker, Kubernetes), alors il existe deux approches principales que vous pouvez utiliser.

### Plusieurs conteneurs { #multiple-containers }

Si vous avez **plusieurs conteneurs**, probablement chacun exécutant un **seul processus** (par exemple, dans un cluster **Kubernetes**), alors vous voudrez probablement avoir un **conteneur séparé** effectuant le travail des **étapes préalables** dans un seul conteneur, exécutant un seul processus, **avant** d'exécuter les conteneurs worker répliqués.

/// info

Si vous utilisez Kubernetes, ce sera probablement un <a href="https://kubernetes.io/docs/concepts/workloads/pods/init-containers/" class="external-link" target="_blank">Init Container</a>.

///

Si, dans votre cas d'usage, il n'y a pas de problème à exécuter ces étapes préalables **plusieurs fois en parallèle** (par exemple si vous n'exécutez pas de migrations de base de données, mais vérifiez simplement si la base de données est prête), alors vous pourriez aussi simplement les mettre dans chaque conteneur juste avant de démarrer le processus principal.

### Un seul conteneur { #single-container }

Si vous avez une configuration simple, avec **un seul conteneur** qui démarre ensuite plusieurs **processus worker** (ou un seul processus aussi), vous pouvez alors exécuter ces étapes préalables dans le même conteneur, juste avant de démarrer le processus avec l'application.

### Image Docker de base { #base-docker-image }

Il existait une image Docker officielle FastAPI : <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>. Mais elle est désormais dépréciée. ⛔️

Vous ne devriez probablement **pas** utiliser cette image Docker de base (ni aucune autre similaire).

Si vous utilisez **Kubernetes** (ou autres) et que vous définissez déjà la **réplication** au niveau du cluster, avec plusieurs **conteneurs**. Dans ces cas, il est préférable de **construire une image à partir de zéro** comme décrit ci-dessus : [Construire une image Docker pour FastAPI](#build-a-docker-image-for-fastapi).

Et si vous devez avoir plusieurs workers, vous pouvez simplement utiliser l'option de ligne de commande `--workers`.

/// note | Détails techniques

L'image Docker a été créée à une époque où Uvicorn ne supportait pas la gestion et le redémarrage des workers morts, il fallait donc utiliser Gunicorn avec Uvicorn, ce qui ajoutait pas mal de complexité, uniquement pour que Gunicorn gère et redémarre les processus worker Uvicorn.

Mais maintenant qu'Uvicorn (et la commande `fastapi`) supporte l'usage de `--workers`, il n'y a plus de raison d'utiliser une image Docker de base au lieu de construire la vôtre (c'est à peu près la même quantité de code 😅).

///

## Déployer l'image de conteneur { #deploy-the-container-image }

Après avoir une image de conteneur (Docker), il existe plusieurs façons de la déployer.

Par exemple :

* Avec **Docker Compose** sur un seul serveur
* Avec un cluster **Kubernetes**
* Avec un cluster Docker Swarm Mode
* Avec un autre outil comme Nomad
* Avec un service cloud qui prend votre image de conteneur et la déploie

## Image Docker avec `uv` { #docker-image-with-uv }

Si vous utilisez <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">uv</a> pour installer et gérer votre projet, vous pouvez suivre leur <a href="https://docs.astral.sh/uv/guides/integration/docker/" class="external-link" target="_blank">guide Docker pour uv</a>.

## Récapitulatif { #recap }

Avec les systèmes de conteneurs (par ex. avec **Docker** et **Kubernetes**), il devient assez simple de gérer tous les **concepts de déploiement** :

* HTTPS
* Exécution au démarrage
* Redémarrages
* Réplication (le nombre de processus en cours d'exécution)
* Mémoire
* Étapes préalables au démarrage

Dans la plupart des cas, vous ne voudrez probablement pas utiliser d'image de base, et au contraire **construire une image de conteneur à partir de zéro** basée sur l'image Docker Python officielle.

En prenant soin de l'**ordre** des instructions dans le `Dockerfile` et du **cache Docker**, vous pouvez **minimiser les temps de construction**, maximiser votre productivité (et éviter l'ennui). 😎
