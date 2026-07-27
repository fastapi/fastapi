# Sécurité { #security }

Il existe de nombreuses façons de gérer la sécurité, l'authentification et l'autorisation.

Et c'est normalement un sujet complexe et « difficile ».

Dans de nombreux frameworks et systèmes, le simple fait de gérer la sécurité et l'authentification demande beaucoup d'efforts et de code (dans de nombreux cas, cela peut représenter 50 % ou plus de tout le code écrit).

**FastAPI** fournit plusieurs outils pour vous aider à gérer la **Sécurité** facilement, rapidement, de manière standard, sans avoir à étudier et apprendre toutes les spécifications de sécurité.

Mais d'abord, voyons quelques notions.

## Pressé ? { #in-a-hurry }

Si ces termes ne vous intéressent pas et que vous avez simplement besoin d'ajouter une sécurité avec une authentification basée sur un nom d'utilisateur et un mot de passe immédiatement, passez aux chapitres suivants.

## OAuth2 { #oauth2 }

OAuth2 est une spécification qui définit plusieurs façons de gérer l'authentification et l'autorisation.

C'est une spécification assez vaste qui couvre plusieurs cas d'utilisation complexes.

Elle inclut des moyens de s'authentifier en utilisant un « tiers ».

C'est ce que tous les systèmes avec « connexion avec Facebook, Google, X (Twitter), GitHub » utilisent en arrière-plan.

### OAuth 1 { #oauth-1 }

Il y a eu un OAuth 1, très différent d'OAuth2, et plus complexe, car il incluait des spécifications directes sur la manière de chiffrer la communication.

Il n'est plus très populaire ni utilisé de nos jours.

OAuth2 ne spécifie pas comment chiffrer la communication ; il suppose que votre application est servie en HTTPS.

/// tip | Astuce

Dans la section sur le déploiement, vous verrez comment configurer HTTPS gratuitement, en utilisant Traefik et Let's Encrypt.

///

## OpenID Connect { #openid-connect }

OpenID Connect est une autre spécification, basée sur **OAuth2**.

Elle étend simplement OAuth2 en précisant certains points relativement ambigus dans OAuth2, afin d'essayer de la rendre plus interopérable.

Par exemple, la connexion Google utilise OpenID Connect (qui, en arrière-plan, utilise OAuth2).

Mais la connexion Facebook ne prend pas en charge OpenID Connect. Elle a sa propre variante d'OAuth2.

### OpenID (pas « OpenID Connect ») { #openid-not-openid-connect }

Il y avait aussi une spécification « OpenID ». Elle essayait de résoudre la même chose qu'**OpenID Connect**, mais n'était pas basée sur OAuth2.

C'était donc un système totalement distinct.

Il n'est plus très populaire ni utilisé de nos jours.

## OpenAPI { #openapi }

OpenAPI (précédemment connu sous le nom de Swagger) est la spécification ouverte pour construire des API (désormais partie de la Linux Foundation).

**FastAPI** est basé sur **OpenAPI**.

C'est ce qui rend possibles plusieurs interfaces de documentation interactive automatiques, la génération de code, etc.

OpenAPI propose une manière de définir plusieurs « schémas » de sécurité.

En les utilisant, vous pouvez tirer parti de tous ces outils basés sur des standards, y compris ces systèmes de documentation interactive.

OpenAPI définit les schémas de sécurité suivants :

* `apiKey` : une clé spécifique à l'application qui peut provenir :
    * D'un paramètre de requête.
    * D'un en-tête.
    * D'un cookie.
* `http` : des systèmes d'authentification HTTP standards, notamment :
    * `bearer` : un en-tête `Authorization` avec une valeur `Bearer ` plus un jeton. Hérité d'OAuth2.
    * Authentification HTTP Basic.
    * HTTP Digest, etc.
* `oauth2` : toutes les méthodes OAuth2 pour gérer la sécurité (appelées « flows »).
    * Plusieurs de ces flows conviennent pour construire un fournisseur d'authentification OAuth 2.0 (comme Google, Facebook, X (Twitter), GitHub, etc.) :
        * `implicit`
        * `clientCredentials`
        * `authorizationCode`
    * Mais il existe un « flow » spécifique qui peut parfaitement être utilisé pour gérer l'authentification directement dans la même application :
        * `password` : certains des prochains chapitres couvriront des exemples à ce sujet.
* `openIdConnect` : propose un moyen de définir comment découvrir automatiquement les données d'authentification OAuth2.
    * Cette découverte automatique est ce qui est défini dans la spécification OpenID Connect.


/// tip | Astuce

Intégrer d'autres fournisseurs d'authentification/autorisation comme Google, Facebook, X (Twitter), GitHub, etc. est également possible et relativement facile.

Le problème le plus complexe est de construire un fournisseur d'authentification/autorisation comme ceux-là, mais **FastAPI** vous donne les outils pour le faire facilement, tout en effectuant le gros du travail pour vous.

///

## Outils **FastAPI** { #fastapi-utilities }

FastAPI propose plusieurs outils pour chacun de ces schémas de sécurité dans le module fastapi.security qui simplifient l'utilisation de ces mécanismes de sécurité.

Dans les prochains chapitres, vous verrez comment ajouter de la sécurité à votre API en utilisant ces outils fournis par **FastAPI**.

Et vous verrez aussi comment cela s'intègre automatiquement au système de documentation interactive.
