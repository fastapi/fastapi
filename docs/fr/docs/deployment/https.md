# À propos de HTTPS { #about-https }

Il est facile de supposer que HTTPS est quelque chose qui est simplement « activé » ou non.

Mais c'est beaucoup plus complexe que cela.

/// tip | Astuce

Si vous êtes pressé ou si cela ne vous intéresse pas, continuez avec les sections suivantes pour obtenir des instructions étape par étape afin de tout configurer avec différentes techniques.

///

Pour apprendre les bases du HTTPS, du point de vue d'un utilisateur, consultez [https://howhttps.works/](https://howhttps.works/).

Maintenant, du point de vue d'un développeur, voici plusieurs choses à avoir en tête en pensant au HTTPS :

* Pour le HTTPS, **le serveur** doit **disposer de « certificats »** générés par une **tierce partie**.
    * Ces certificats sont en réalité **acquis** auprès de la tierce partie, et non « générés ».
* Les certificats ont une **durée de vie**.
    * Ils **expirent**.
    * Puis ils doivent être **renouvelés**, **acquis à nouveau** auprès de la tierce partie.
* Le cryptage de la connexion se fait au **niveau TCP**.
    * C'est une couche **en dessous de HTTP**.
    * Donc, la gestion du **certificat et du cryptage** est effectuée **avant HTTP**.
* **TCP ne connaît pas les « domaines »**. Il ne connaît que les adresses IP.
    * L'information sur le **domaine spécifique** demandé se trouve dans les **données HTTP**.
* Les **certificats HTTPS** « certifient » un **certain domaine**, mais le protocole et le cryptage se font au niveau TCP, **avant de savoir** quel domaine est traité.
* **Par défaut**, cela signifie que vous ne pouvez avoir qu'**un seul certificat HTTPS par adresse IP**.
    * Quelle que soit la taille de votre serveur ou la petitesse de chacune des applications qu'il contient.
    * Il existe cependant une **solution** à ce problème.
* Il existe une **extension** du protocole **TLS** (celui qui gère le cryptage au niveau TCP, avant HTTP) appelée **[<abbr title="Server Name Indication - Indication du nom du serveur">SNI</abbr>](https://en.wikipedia.org/wiki/Server_Name_Indication)**.
    * Cette extension SNI permet à un seul serveur (avec une **seule adresse IP**) d'avoir **plusieurs certificats HTTPS** et de servir **plusieurs domaines/applications HTTPS**.
    * Pour que cela fonctionne, un **seul** composant (programme) fonctionnant sur le serveur, écoutant sur l'**adresse IP publique**, doit avoir **tous les certificats HTTPS** du serveur.
* **Après** l'établissement d'une connexion sécurisée, le protocole de communication est **toujours HTTP**.
    * Le contenu est **crypté**, même s'il est envoyé avec le **protocole HTTP**.

Il est courant d'avoir **un seul programme/serveur HTTP** fonctionnant sur le serveur (la machine, l'hôte, etc.) et **gérant toutes les parties HTTPS** : recevoir les **requêtes HTTPS chiffrées**, envoyer les **requêtes HTTP déchiffrées** à l'application HTTP réelle fonctionnant sur le même serveur (l'application **FastAPI**, dans ce cas), prendre la **réponse HTTP** de l'application, la **chiffrer** en utilisant le **certificat HTTPS** approprié et la renvoyer au client en utilisant **HTTPS**. Ce serveur est souvent appelé un **[Proxy de terminaison TLS](https://en.wikipedia.org/wiki/TLS_termination_proxy)**.

Parmi les options que vous pourriez utiliser comme Proxy de terminaison TLS :

* Traefik (qui peut également gérer les renouvellements de certificats)
* Caddy (qui peut également gérer les renouvellements de certificats)
* Nginx
* HAProxy

## Let's Encrypt { #lets-encrypt }

Avant Let's Encrypt, ces **certificats HTTPS** étaient vendus par des tiers de confiance.

Le processus d'acquisition de l'un de ces certificats était auparavant lourd, nécessitait pas mal de paperasses et les certificats étaient assez chers.

Mais ensuite, **[Let's Encrypt](https://letsencrypt.org/)** a été créé.

Il s'agit d'un projet de la Fondation Linux. Il fournit **des certificats HTTPS gratuitement**, de manière automatisée. Ces certificats utilisent toutes les sécurités cryptographiques standard et ont une durée de vie courte (environ 3 mois), de sorte que la **sécurité est en fait meilleure** en raison de leur durée de vie réduite.

Les domaines sont vérifiés de manière sécurisée et les certificats sont générés automatiquement. Cela permet également d'automatiser le renouvellement de ces certificats.

L'idée est d'automatiser l'acquisition et le renouvellement de ces certificats, afin que vous puissiez disposer d'un **HTTPS sécurisé, gratuitement et pour toujours**.

## HTTPS pour les développeurs { #https-for-developers }

Voici un exemple de ce à quoi pourrait ressembler une API HTTPS, étape par étape, en portant principalement attention aux idées importantes pour les développeurs.

### Nom de domaine { #domain-name }

Tout commencerait probablement par le fait que vous **acquériez** un **nom de domaine**. Ensuite, vous le configureriez dans un serveur DNS (possiblement le même que votre fournisseur cloud).

Vous obtiendriez probablement un serveur cloud (une machine virtuelle) ou quelque chose de similaire, et il aurait une adresse IP publique <dfn title="Ne change pas dans le temps. Pas dynamique.">fixe</dfn>.

Dans le ou les serveurs DNS, vous configureriez un enregistrement (un « `A record` ») pour faire pointer **votre domaine** vers l'**adresse IP publique de votre serveur**.

Vous feriez probablement cela une seule fois, la première fois, lors de la mise en place de l'ensemble.

/// tip | Astuce

Cette partie relative au nom de domaine intervient bien avant HTTPS, mais comme tout dépend du domaine et de l'adresse IP, il vaut la peine de la mentionner ici.

///

### DNS { #dns }

Concentrons-nous maintenant sur toutes les parties réellement liées à HTTPS.

D'abord, le navigateur vérifierait auprès des **serveurs DNS** quelle est l'**IP du domaine**, dans ce cas, `someapp.example.com`.

Les serveurs DNS indiqueraient au navigateur d'utiliser une **adresse IP** spécifique. Ce serait l'adresse IP publique utilisée par votre serveur, celle que vous avez configurée dans les serveurs DNS.

<img src="/img/deployment/https/https01.drawio.svg">

### Début de la négociation TLS (Handshake) { #tls-handshake-start }

Le navigateur communiquerait ensuite avec cette adresse IP sur le **port 443** (le port HTTPS).

La première partie de la communication consiste simplement à établir la connexion entre le client et le serveur et à décider des clés cryptographiques qu'ils utiliseront, etc.

<img src="/img/deployment/https/https02.drawio.svg">

Cette interaction entre le client et le serveur pour établir la connexion TLS s'appelle la **négociation TLS (TLS handshake)**.

### TLS avec l'extension SNI { #tls-with-sni-extension }

**Un seul processus** sur le serveur peut écouter sur un **port** spécifique d'une **adresse IP** spécifique. Il pourrait y avoir d'autres processus écoutant sur d'autres ports de la même adresse IP, mais un seul pour chaque combinaison d'adresse IP et de port.

TLS (HTTPS) utilise par défaut le port spécifique `443`. C'est donc le port dont nous aurions besoin.

Comme un seul processus peut écouter sur ce port, le processus qui le ferait serait le **Proxy de terminaison TLS**.

Le Proxy de terminaison TLS aurait accès à un ou plusieurs **certificats TLS** (certificats HTTPS).

En utilisant l'**extension SNI** mentionnée plus haut, le Proxy de terminaison TLS vérifierait lequel des certificats TLS (HTTPS) disponibles il devrait utiliser pour cette connexion, en choisissant celui qui correspond au domaine attendu par le client.

Dans ce cas, il utiliserait le certificat pour `someapp.example.com`.

<img src="/img/deployment/https/https03.drawio.svg">

Le client **fait déjà confiance** à l'entité qui a généré ce certificat TLS (dans ce cas Let's Encrypt, mais nous y reviendrons plus tard), il peut donc **vérifier** que le certificat est valide.

Ensuite, en utilisant le certificat, le client et le Proxy de terminaison TLS **décident comment chiffrer** le reste de la **communication TCP**. Cela termine la partie **négociation TLS**.

Après cela, le client et le serveur disposent d'une **connexion TCP chiffrée**, c'est ce que fournit TLS. Ils peuvent alors utiliser cette connexion pour démarrer la **communication HTTP** proprement dite.

Et c'est ce qu'est **HTTPS** : c'est simplement du **HTTP** à l'intérieur d'une **connexion TLS sécurisée** au lieu d'une connexion TCP pure (non chiffrée).

/// tip | Astuce

Remarquez que le cryptage de la communication se produit au **niveau TCP**, pas au niveau HTTP.

///

### Requête HTTPS { #https-request }

Maintenant que le client et le serveur (spécifiquement le navigateur et le Proxy de terminaison TLS) ont une **connexion TCP chiffrée**, ils peuvent démarrer la **communication HTTP**.

Ainsi, le client envoie une **requête HTTPS**. Ce n'est qu'une requête HTTP à travers une connexion TLS chiffrée.

<img src="/img/deployment/https/https04.drawio.svg">

### Déchiffrer la requête { #decrypt-the-request }

Le Proxy de terminaison TLS utiliserait le chiffrement convenu pour **déchiffrer la requête**, et transmettrait la **requête HTTP en clair (déchiffrée)** au processus exécutant l'application (par exemple un processus avec Uvicorn exécutant l'application FastAPI).

<img src="/img/deployment/https/https05.drawio.svg">

### Réponse HTTP { #http-response }

L'application traiterait la requête et enverrait une **réponse HTTP en clair (non chiffrée)** au Proxy de terminaison TLS.

<img src="/img/deployment/https/https06.drawio.svg">

### Réponse HTTPS { #https-response }

Le Proxy de terminaison TLS **chiffrerait ensuite la réponse** en utilisant la cryptographie convenue auparavant (qui a commencé avec le certificat pour `someapp.example.com`), et la renverrait au navigateur.

Ensuite, le navigateur vérifierait que la réponse est valide et chiffrée avec la bonne clé cryptographique, etc. Il **déchiffrerait la réponse** et la traiterait.

<img src="/img/deployment/https/https07.drawio.svg">

Le client (navigateur) saura que la réponse provient du bon serveur parce qu'elle utilise la cryptographie convenue auparavant à l'aide du **certificat HTTPS**.

### Applications multiples { #multiple-applications }

Sur le même serveur (ou les mêmes serveurs), il pourrait y avoir **plusieurs applications**, par exemple d'autres programmes d'API ou une base de données.

Un seul processus peut gérer l'adresse IP et le port spécifiques (le Proxy de terminaison TLS dans notre exemple), mais les autres applications/processus peuvent également s'exécuter sur le ou les serveurs, tant qu'ils n'essaient pas d'utiliser la même **combinaison d'adresse IP publique et de port**.

<img src="/img/deployment/https/https08.drawio.svg">

De cette façon, le Proxy de terminaison TLS pourrait gérer HTTPS et les certificats pour **plusieurs domaines**, pour plusieurs applications, puis transmettre les requêtes à la bonne application dans chaque cas.

### Renouvellement des certificats { #certificate-renewal }

À un moment donné dans le futur, chaque certificat **expirerait** (environ 3 mois après son acquisition).

Ensuite, il y aurait un autre programme (dans certains cas c'est un autre programme, dans d'autres cas cela pourrait être le même Proxy de terminaison TLS) qui communiquerait avec Let's Encrypt et renouvellerait le ou les certificats.

<img src="/img/deployment/https/https.drawio.svg">

Les **certificats TLS** sont **associés à un nom de domaine**, pas à une adresse IP.

Ainsi, pour renouveler les certificats, le programme de renouvellement doit **prouver** à l'autorité (Let's Encrypt) qu'il **« possède » et contrôle ce domaine**.

Pour ce faire, et pour s'adapter aux différents besoins des applications, il existe plusieurs façons de procéder. Parmi les plus courantes :

* **Modifier certains enregistrements DNS**.
    * Pour cela, le programme de renouvellement doit prendre en charge les API du fournisseur DNS ; ainsi, selon le fournisseur DNS que vous utilisez, cela peut être ou non une option.
* **S'exécuter comme un serveur** (au moins pendant le processus d'acquisition du certificat) sur l'adresse IP publique associée au domaine.
    * Comme nous l'avons dit plus haut, un seul processus peut écouter sur une adresse IP et un port spécifiques.
    * C'est l'une des raisons pour lesquelles il est très utile que le même Proxy de terminaison TLS prenne également en charge le processus de renouvellement des certificats.
    * Sinon, vous pourriez avoir à arrêter le Proxy de terminaison TLS momentanément, démarrer le programme de renouvellement pour acquérir les certificats, puis les configurer avec le Proxy de terminaison TLS, et ensuite redémarrer le Proxy de terminaison TLS. Ce n'est pas idéal, car votre/vos application(s) ne seront pas disponibles pendant le temps où le Proxy de terminaison TLS est arrêté.

Tout ce processus de renouvellement, tout en continuant à servir l'application, est l'une des principales raisons pour lesquelles vous voudriez avoir un **système séparé pour gérer HTTPS** avec un Proxy de terminaison TLS, au lieu d'utiliser directement les certificats TLS avec le serveur d'application (par exemple Uvicorn).

## En-têtes Proxy Forwarded { #proxy-forwarded-headers }

Lorsque vous utilisez un proxy pour gérer HTTPS, votre **serveur d'application** (par exemple Uvicorn via FastAPI CLI) ne connaît rien du processus HTTPS, il communique en HTTP en clair avec le **Proxy de terminaison TLS**.

Ce **proxy** définirait normalement certains en-têtes HTTP à la volée avant de transmettre la requête au **serveur d'application**, pour informer le serveur d'application que la requête est **transmise** par le proxy.

/// note | Détails techniques

Les en-têtes du proxy sont :

* [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For)
* [X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto)
* [X-Forwarded-Host](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host)

///

Néanmoins, comme le **serveur d'application** ne sait pas qu'il se trouve derrière un **proxy** de confiance, par défaut, il ne ferait pas confiance à ces en-têtes.

Mais vous pouvez configurer le **serveur d'application** pour qu'il fasse confiance aux en-têtes transmis (*forwarded*) envoyés par le **proxy**. Si vous utilisez FastAPI CLI, vous pouvez utiliser l'*option CLI* `--forwarded-allow-ips` pour lui indiquer à partir de quelles IP il doit faire confiance à ces en-têtes transmis.

Par exemple, si le **serveur d'application** ne reçoit des communications que du **proxy** de confiance, vous pouvez définir `--forwarded-allow-ips="*"` pour lui faire faire confiance à toutes les IP entrantes, puisqu'il ne recevra des requêtes que depuis l'IP utilisée par le **proxy**.

De cette façon, l'application sera en mesure de savoir quelle est sa propre URL publique, si elle utilise HTTPS, le domaine, etc.

Cela serait utile, par exemple, pour gérer correctement les redirections.

/// tip | Astuce

Vous pouvez en savoir plus dans la documentation [Derrière un proxy - Activer les en-têtes transmis par le proxy](../advanced/behind-a-proxy.md#enable-proxy-forwarded-headers)

///

## Récapitulatif { #recap }

Disposer de **HTTPS** est très important, et assez **critique** dans la plupart des cas. La majeure partie de l'effort que vous, en tant que développeur, devez fournir autour de HTTPS consiste simplement à **comprendre ces concepts** et leur fonctionnement.

Mais une fois que vous connaissez les informations de base sur **HTTPS pour les développeurs**, vous pouvez facilement combiner et configurer différents outils pour vous aider à tout gérer simplement.

Dans certains des prochains chapitres, je vous montrerai plusieurs exemples concrets de configuration de **HTTPS** pour des applications **FastAPI**. 🔒
