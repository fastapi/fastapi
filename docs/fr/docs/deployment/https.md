# À propos de HTTPS { #about-https }

Il est facile de supposer que HTTPS est quelque chose qui est simplement « activé » ou non.

Mais c'est bien plus complexe que cela.

/// tip | Astuce

Si vous êtes pressé ou si cela ne vous intéresse pas, continuez avec les sections suivantes pour obtenir des instructions étape par étape afin de tout configurer avec différentes techniques.

///

Pour **apprendre les bases de HTTPS**, du point de vue d'un utilisateur, consultez <a href="https://howhttps.works/" class="external-link" target="_blank">https://howhttps.works/</a>.

Maintenant, du point de vue d'un développeur, voici plusieurs choses à garder à l'esprit en pensant à HTTPS :

* Pour HTTPS, **le serveur** doit **avoir des « certificats »** générés par une **tierce partie**.
    * Ces certificats sont en fait **acquis** auprès de la tierce partie, et non « générés ».
* Les certificats ont une **durée de vie**.
    * Ils **expirent**.
    * Et ensuite ils doivent être **renouvelés**, **acquis à nouveau** auprès de la tierce partie.
* Le chiffrement de la connexion se fait au **niveau TCP**.
    * C'est une couche **en dessous de HTTP**.
    * Donc, la gestion du **certificat et du chiffrement** est faite **avant HTTP**.
* **TCP ne connaît pas les « domaines »**. Seulement les adresses IP.
    * L'information sur le **domaine spécifique** demandé se trouve dans les **données HTTP**.
* Les **certificats HTTPS** « certifient » un **certain domaine**, mais le protocole et le chiffrement se font au niveau TCP, **avant de savoir** quel domaine est traité.
* **Par défaut**, cela signifierait que vous ne pouvez avoir qu'**un seul certificat HTTPS par adresse IP**.
    * Peu importe la taille de votre serveur ou à quel point chaque application que vous avez dessus peut être petite.
    * Il existe cependant une **solution** à ce problème.
* Il existe une **extension** du protocole **TLS** (celui qui gère le chiffrement au niveau TCP, avant HTTP) appelée **<a href="https://en.wikipedia.org/wiki/Server_Name_Indication" class="external-link" target="_blank"><abbr title="Server Name Indication - Indication du nom du serveur">SNI</abbr></a>**.
    * Cette extension SNI permet à un seul serveur (avec une **seule adresse IP**) d'avoir **plusieurs certificats HTTPS** et de servir **plusieurs domaines/applications HTTPS**.
    * Pour que cela fonctionne, un **seul** composant (programme) fonctionnant sur le serveur, écoutant sur l'**adresse IP publique**, doit avoir **tous les certificats HTTPS** du serveur.
* **Après** avoir obtenu une connexion sécurisée, le protocole de communication est **toujours HTTP**.
    * Le contenu est **chiffré**, même s'il est envoyé avec le **protocole HTTP**.

Il est courant d'avoir **un seul programme/serveur HTTP** fonctionnant sur le serveur (la machine, l'hôte, etc.) et **gérant toutes les parties HTTPS** : recevoir les **requêtes HTTPS chiffrées**, envoyer les **requêtes HTTP déchiffrées** à l'application HTTP réelle fonctionnant sur le même serveur (l'application **FastAPI**, dans ce cas), prendre la **réponse HTTP** de l'application, la **chiffrer** en utilisant le **certificat HTTPS** approprié et la renvoyer au client en utilisant **HTTPS**. Ce serveur est souvent appelé un **<a href="https://en.wikipedia.org/wiki/TLS_termination_proxy" class="external-link" target="_blank">Proxy de terminaison TLS</a>**.

Certaines des options que vous pouvez utiliser comme Proxy de terminaison TLS sont :

* Traefik (qui peut aussi gérer les renouvellements de certificats)
* Caddy (qui peut aussi gérer les renouvellements de certificats)
* Nginx
* HAProxy

## Let's Encrypt { #lets-encrypt }

Avant Let's Encrypt, ces **certificats HTTPS** étaient vendus par des tiers de confiance.

Le processus d'acquisition d'un de ces certificats était auparavant lourd, nécessitait pas mal de paperasses et les certificats étaient assez chers.

Mais ensuite **<a href="https://letsencrypt.org/" class="external-link" target="_blank">Let's Encrypt</a>** a été créé.

Il s'agit d'un projet de la Linux Foundation. Il fournit des **certificats HTTPS gratuitement**, de manière automatisée. Ces certificats utilisent toutes les sécurités cryptographiques standard, et ont une durée de vie courte (environ 3 mois), de sorte que la **sécurité est en fait meilleure** en raison de leur durée de vie réduite.

Les domaines sont vérifiés de manière sécurisée et les certificats sont générés automatiquement. Cela permet également d'automatiser le renouvellement de ces certificats.

L'idée est d'automatiser l'acquisition et le renouvellement de ces certificats, afin que vous puissiez disposer d'un **HTTPS sécurisé, gratuitement, pour toujours**.

## HTTPS pour les développeurs { #https-for-developers }

Voici un exemple de ce à quoi une API HTTPS pourrait ressembler, étape par étape, en faisant attention principalement aux idées importantes pour les développeurs.

### Nom de domaine { #domain-name }

Cela commencerait probablement par le fait que vous **acquérez** un **nom de domaine**. Ensuite, vous le configureriez dans un serveur DNS (éventuellement votre même fournisseur cloud).

Vous obtiendriez probablement un serveur cloud (une machine virtuelle) ou quelque chose de similaire, et il aurait une adresse IP publique <abbr title="That doesn't change - Qui ne change pas">fixed</abbr>.

Dans le(s) serveur(s) DNS vous configureriez un enregistrement (un « `A record` ») pour faire pointer **votre domaine** vers l'**adresse IP publique de votre serveur**.

Vous feriez probablement cela une seule fois, la première fois, lorsque vous mettez tout en place.

/// tip | Astuce

Cette partie « nom de domaine » se situe bien avant HTTPS, mais comme tout dépend du domaine et de l'adresse IP, cela vaut la peine de le mentionner ici.

///

### DNS { #dns }

Maintenant, concentrons-nous sur toutes les parties réellement liées à HTTPS.

D'abord, le navigateur vérifierait auprès des **serveurs DNS** quelle est l'**IP du domaine**, dans ce cas, `someapp.example.com`.

Les serveurs DNS diraient au navigateur d'utiliser une **adresse IP** spécifique. Ce serait l'adresse IP publique utilisée par votre serveur, que vous avez configurée dans les serveurs DNS.

<img src="/img/deployment/https/https01.drawio.svg">

### Début du handshake TLS { #tls-handshake-start }

Le navigateur communiquerait ensuite avec cette adresse IP sur le **port 443** (le port HTTPS).

La première partie de la communication consiste simplement à établir la connexion entre le client et le serveur et à décider des clés cryptographiques qu'ils utiliseront, etc.

<img src="/img/deployment/https/https02.drawio.svg">

Cette interaction entre le client et le serveur pour établir la connexion TLS s'appelle le **handshake TLS**.

### TLS avec l'extension SNI { #tls-with-sni-extension }

**Un seul process** sur le serveur peut écouter sur un **port** spécifique sur une **adresse IP** spécifique. Il peut y avoir d'autres process écoutant sur d'autres ports sur la même adresse IP, mais un seul pour chaque combinaison d'adresse IP et de port.

TLS (HTTPS) utilise par défaut le port spécifique `443`. Donc c'est ce port dont nous avons besoin.

Comme un seul process peut écouter sur ce port, le process qui le ferait serait le **Proxy de terminaison TLS**.

Le Proxy de terminaison TLS aurait accès à un ou plusieurs **certificats TLS** (certificats HTTPS).

En utilisant l'**extension SNI** mentionnée ci-dessus, le Proxy de terminaison TLS vérifierait lequel des certificats TLS (HTTPS) disponibles il doit utiliser pour cette connexion, en utilisant celui qui correspond au domaine attendu par le client.

Dans ce cas, il utiliserait le certificat pour `someapp.example.com`.

<img src="/img/deployment/https/https03.drawio.svg">

Le client **fait déjà confiance** à l'entité qui a généré ce certificat TLS (dans ce cas Let's Encrypt, mais nous verrons cela plus tard), il peut donc **vérifier** que le certificat est valide.

Ensuite, en utilisant le certificat, le client et le Proxy de terminaison TLS **décident comment chiffrer** le reste de la **communication TCP**. Cela complète la partie **Handshake TLS**.

Après cela, le client et le serveur ont une **connexion TCP chiffrée**, c'est ce que fournit TLS. Et ensuite ils peuvent utiliser cette connexion pour démarrer la véritable **communication HTTP**.

Et c'est ce qu'est **HTTPS**, c'est simplement du **HTTP** à l'intérieur d'une **connexion TLS sécurisée** au lieu d'une connexion TCP pure (non chiffrée).

/// tip | Astuce

Notez que le chiffrement de la communication se produit au **niveau TCP**, pas au niveau HTTP.

///

### Requête HTTPS { #https-request }

Maintenant que le client et le serveur (spécifiquement le navigateur et le Proxy de terminaison TLS) ont une **connexion TCP chiffrée**, ils peuvent démarrer la **communication HTTP**.

Ainsi, le client envoie une **requête HTTPS**. Il s'agit simplement d'une requête HTTP via une connexion TLS chiffrée.

<img src="/img/deployment/https/https04.drawio.svg">

### Déchiffrer la requête { #decrypt-the-request }

Le Proxy de terminaison TLS utiliserait le chiffrement convenu pour **déchiffrer la requête**, et transmettrait la **requête HTTP en clair (déchiffrée)** au process exécutant l'application (par exemple un process avec Uvicorn exécutant l'application FastAPI).

<img src="/img/deployment/https/https05.drawio.svg">

### Réponse HTTP { #http-response }

L'application traiterait la requête et enverrait une **réponse HTTP en clair (non chiffrée)** au Proxy de terminaison TLS.

<img src="/img/deployment/https/https06.drawio.svg">

### Réponse HTTPS { #https-response }

Le Proxy de terminaison TLS **chiffrerait ensuite la réponse** en utilisant la cryptographie convenue auparavant (qui a commencé avec le certificat pour `someapp.example.com`), et la renverrait au navigateur.

Ensuite, le navigateur vérifierait que la réponse est valide et chiffrée avec la bonne clé cryptographique, etc. Il **déchiffrerait ensuite la réponse** et la traiterait.

<img src="/img/deployment/https/https07.drawio.svg">

Le client (navigateur) saura que la réponse provient du bon serveur parce qu'il utilise la cryptographie qu'ils ont convenue en utilisant le **certificat HTTPS** auparavant.

### Applications multiples { #multiple-applications }

Sur le même serveur (ou les mêmes serveurs), il pourrait y avoir **plusieurs applications**, par exemple d'autres programmes d'API ou une base de données.

Un seul process peut gérer la combinaison spécifique d'IP et de port (le Proxy de terminaison TLS dans notre exemple) mais les autres applications/process peuvent également s'exécuter sur le(s) serveur(s), tant qu'ils n'essaient pas d'utiliser la même **combinaison d'IP publique et de port**.

<img src="/img/deployment/https/https08.drawio.svg">

De cette façon, le Proxy de terminaison TLS pourrait gérer HTTPS et les certificats pour **plusieurs domaines**, pour plusieurs applications, puis transmettre les requêtes à la bonne application dans chaque cas.

### Renouvellement des certificats { #certificate-renewal }

À un moment donné dans le futur, chaque certificat **expirerait** (environ 3 mois après son acquisition).

Et ensuite, il y aurait un autre programme (dans certains cas c'est un autre programme, dans certains cas cela pourrait être le même Proxy de terminaison TLS) qui parlerait à Let's Encrypt, et renouvellerait le(s) certificat(s).

<img src="/img/deployment/https/https.drawio.svg">

Les **certificats TLS** sont **associés à un nom de domaine**, pas à une adresse IP.

Ainsi, pour renouveler les certificats, le programme de renouvellement doit **prouver** à l'autorité (Let's Encrypt) qu'il **« possède » et contrôle effectivement ce domaine**.

Pour ce faire, et pour répondre à différents besoins applicatifs, il existe plusieurs façons de procéder. Voici quelques méthodes populaires :

* **Modifier certains enregistrements DNS**.
    * Pour cela, le programme de renouvellement doit prendre en charge les API du fournisseur DNS, donc, selon le fournisseur DNS que vous utilisez, cela peut ou non être une option.
* **S'exécuter comme un serveur** (au moins pendant le processus d'acquisition du certificat) sur l'adresse IP publique associée au domaine.
    * Comme nous l'avons dit ci-dessus, un seul process peut écouter sur une IP et un port spécifiques.
    * C'est l'une des raisons pour lesquelles il est très utile que le même Proxy de terminaison TLS s'occupe aussi du processus de renouvellement des certificats.
    * Sinon, vous devrez peut-être arrêter momentanément le Proxy de terminaison TLS, démarrer le programme de renouvellement pour acquérir les certificats, puis les configurer avec le Proxy de terminaison TLS, et ensuite redémarrer le Proxy de terminaison TLS. Ce n'est pas idéal, car votre/vos app(s) ne seront pas disponibles pendant le temps où le Proxy de terminaison TLS est arrêté.

Tout ce processus de renouvellement, tout en continuant de servir l'app, est l'une des principales raisons pour lesquelles vous voulez avoir un **système séparé pour gérer HTTPS** avec un Proxy de terminaison TLS au lieu de simplement utiliser les certificats TLS directement avec le serveur d'application (par ex. Uvicorn).

## En-têtes de proxy transférés { #proxy-forwarded-headers }

Lorsque vous utilisez un proxy pour gérer HTTPS, votre **serveur d'application** (par exemple Uvicorn via la FastAPI CLI) ne sait rien du processus HTTPS, il communique en HTTP en clair avec le **Proxy de terminaison TLS**.

Ce **proxy** définirait normalement certains en-têtes HTTP à la volée avant de transmettre la requête au **serveur d'application**, pour indiquer au serveur d'application que la requête est **transférée** par le proxy.

/// note | Détails techniques

Les en-têtes du proxy sont :

* <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For" class="external-link" target="_blank">X-Forwarded-For</a>
* <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto" class="external-link" target="_blank">X-Forwarded-Proto</a>
* <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host" class="external-link" target="_blank">X-Forwarded-Host</a>

///

Néanmoins, comme le **serveur d'application** ne sait pas qu'il est derrière un **proxy** de confiance, par défaut, il ne ferait pas confiance à ces en-têtes.

Mais vous pouvez configurer le **serveur d'application** pour faire confiance aux en-têtes *forwarded* envoyés par le **proxy**. Si vous utilisez la FastAPI CLI, vous pouvez utiliser l'*option CLI* `--forwarded-allow-ips` pour lui indiquer depuis quelles IP il doit faire confiance à ces en-têtes *forwarded*.

Par exemple, si le **serveur d'application** ne reçoit la communication que du **proxy** de confiance, vous pouvez le définir sur `--forwarded-allow-ips="*"` pour lui faire confiance pour toutes les IP entrantes, car il ne recevra des requêtes que depuis l'adresse IP utilisée par le **proxy**.

De cette façon, l'application serait capable de connaître sa propre URL publique, si elle utilise HTTPS, le domaine, etc.

Ce serait utile par exemple pour gérer correctement les redirections.

/// tip | Astuce

Vous pouvez en apprendre davantage à ce sujet dans la documentation pour [Derrière un proxy - Activer les en-têtes Proxy Forwarded](../advanced/behind-a-proxy.md#enable-proxy-forwarded-headers){.internal-link target=_blank}

///

## Récapitulatif { #recap }

Avoir **HTTPS** est très important, et assez **critique** dans la plupart des cas. La plupart des efforts que vous, en tant que développeur, devez fournir autour de HTTPS consistent simplement à **comprendre ces concepts** et comment ils fonctionnent.

Mais une fois que vous connaissez les informations de base sur **HTTPS pour les développeurs** vous pouvez facilement combiner et configurer différents outils pour vous aider à tout gérer de manière simple.

Dans certains des prochains chapitres, je vais vous montrer plusieurs exemples concrets de configuration de **HTTPS** pour des applications **FastAPI**. 🔒
