# À propos de HTTPS

Il est facile de penser que HTTPS peut simplement être "activé" ou non.

Mais c'est beaucoup plus complexe que cela.

/// tip

Si vous êtes pressé ou si cela ne vous intéresse pas, passez aux sections suivantes pour obtenir des instructions étape par étape afin de tout configurer avec différentes techniques.

///

Pour apprendre les bases du HTTPS, du point de vue d'un utilisateur, consultez <a href="https://howhttps.works/"
class="external-link" target="_blank">https://howhttps.works/</a>.

Maintenant, du point de vue d'un développeur, voici plusieurs choses à avoir en tête en pensant au HTTPS :

* Pour le HTTPS, le serveur a besoin de "certificats" générés par une tierce partie.
    * Ces certificats sont en fait acquis auprès de la tierce partie, et non "générés".
* Les certificats ont une durée de vie.
    * Ils expirent.
    * Puis ils doivent être renouvelés et acquis à nouveau auprès de la tierce partie.
* Le cryptage de la connexion se fait au niveau du protocole TCP.
    * C'est une couche en dessous de HTTP.
    * Donc, le certificat et le traitement du cryptage sont faits avant HTTP.
* TCP ne connaît pas les "domaines", seulement les adresses IP.
    * L'information sur le domaine spécifique demandé se trouve dans les données HTTP.
* Les certificats HTTPS "certifient" un certain domaine, mais le protocole et le cryptage se font au niveau TCP, avant de savoir quel domaine est traité.
* Par défaut, cela signifie que vous ne pouvez avoir qu'un seul certificat HTTPS par adresse IP.
    * Quelle que soit la taille de votre serveur ou la taille de chacune des applications qu'il contient.
    * Il existe cependant une solution à ce problème.
* Il existe une extension du protocole TLS (celui qui gère le cryptage au niveau TCP, avant HTTP) appelée <a
  href="https://fr.wikipedia.org/wiki/Server_Name_Indication" class="external-link" target="_blank"><abbr
  title="Server Name Indication (indication du nom du serveur)">SNI (indication du nom du serveur)</abbr></a>.
    * Cette extension SNI permet à un seul serveur (avec une seule adresse IP) d'avoir plusieurs certificats HTTPS et de servir plusieurs domaines/applications HTTPS.
    * Pour que cela fonctionne, un seul composant (programme) fonctionnant sur le serveur, écoutant sur l'adresse IP publique, doit avoir tous les certificats HTTPS du serveur.
* Après avoir obtenu une connexion sécurisée, le protocole de communication est toujours HTTP.
    * Le contenu est crypté, même s'il est envoyé avec le protocole HTTP.

Il est courant d'avoir un seul programme/serveur HTTP fonctionnant sur le serveur (la machine, l'hôte, etc.) et
gérant toutes les parties HTTPS : envoyer les requêtes HTTP décryptées à l'application HTTP réelle fonctionnant sur
le même serveur (dans ce cas, l'application **FastAPI**), prendre la réponse HTTP de l'application, la crypter en utilisant le certificat approprié et la renvoyer au client en utilisant HTTPS. Ce serveur est souvent appelé un <a href="https://en.wikipedia.org/wiki/TLS_termination_proxy" class="external-link" target="_blank">Proxy de terminaison TLS</a>.

## Let's Encrypt

Avant Let's Encrypt, ces certificats HTTPS étaient vendus par des tiers de confiance.

Le processus d'acquisition d'un de ces certificats était auparavant lourd, nécessitait pas mal de paperasses et les certificats étaient assez chers.

Mais ensuite, <a href="https://letsencrypt.org/" class="external-link" target="_blank">Let's Encrypt</a> a été créé.

Il s'agit d'un projet de la Fondation Linux. Il fournit des certificats HTTPS gratuitement. De manière automatisée. Ces certificats utilisent toutes les sécurités cryptographiques standard et ont une durée de vie courte (environ 3 mois), de sorte que la sécurité est en fait meilleure en raison de leur durée de vie réduite.

Les domaines sont vérifiés de manière sécurisée et les certificats sont générés automatiquement. Cela permet également d'automatiser le renouvellement de ces certificats.

L'idée est d'automatiser l'acquisition et le renouvellement de ces certificats, afin que vous puissiez disposer d'un HTTPS sécurisé, gratuitement et pour toujours.
