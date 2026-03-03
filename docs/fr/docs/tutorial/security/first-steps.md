# Sécurité - Premiers pas { #security-first-steps }

Imaginons que vous ayez votre API de **backend** sur un certain domaine.

Et vous avez un **frontend** sur un autre domaine ou dans un chemin différent du même domaine (ou dans une application mobile).

Et vous voulez que le **frontend** puisse s'authentifier auprès du **backend**, en utilisant un **username** et un **password**.

Nous pouvons utiliser **OAuth2** pour construire cela avec **FastAPI**.

Mais épargnons-vous le temps de lire toute la spécification complète juste pour trouver les petites informations dont vous avez besoin.

Utilisons les outils fournis par **FastAPI** pour gérer la sécurité.

## Voir à quoi cela ressemble { #how-it-looks }

Commençons par utiliser le code et voir comment cela fonctionne, puis nous reviendrons pour comprendre ce qui se passe.

## Créer `main.py` { #create-main-py }

Copiez l'exemple dans un fichier `main.py` :

{* ../../docs_src/security/tutorial001_an_py310.py *}

## Exécuter { #run-it }

/// info

Le package <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> est installé automatiquement avec **FastAPI** lorsque vous exécutez la commande `pip install "fastapi[standard]"`.

Cependant, si vous utilisez la commande `pip install fastapi`, le package `python-multipart` n'est pas inclus par défaut.

Pour l'installer manuellement, vous devez vous assurer de créer un [environnement virtuel](../../virtual-environments.md){.internal-link target=_blank}, de l'activer, puis de l'installer avec :

```console
$ pip install python-multipart
```

Cela est dû au fait que **OAuth2** utilise des « form data » pour envoyer le `username` et le `password`.

///

Exécutez l'exemple avec :

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## Vérifier { #check-it }

Allez à la documentation interactive à l'adresse : <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vous verrez quelque chose comme ceci :

<img src="/img/tutorial/security/image01.png">

/// check | Bouton « Authorize » !

Vous avez déjà un tout nouveau bouton « Authorize ».

Et votre *chemin d'accès* a un petit cadenas dans le coin supérieur droit sur lequel vous pouvez cliquer.

///

Et si vous cliquez dessus, vous obtenez un petit formulaire d'autorisation pour saisir un `username` et un `password` (et d'autres champs optionnels) :

<img src="/img/tutorial/security/image02.png">

/// note | Remarque

Peu importe ce que vous saisissez dans le formulaire, cela ne fonctionnera pas encore. Mais nous y viendrons.

///

Ce n'est bien sûr pas le frontend pour les utilisateurs finaux, mais c'est un excellent outil automatique pour documenter de manière interactive toute votre API.

Il peut être utilisé par l'équipe frontend (qui peut aussi être vous-même).

Il peut être utilisé par des applications et des systèmes tiers.

Et il peut aussi être utilisé par vous-même, pour déboguer, vérifier et tester la même application.

## Le flux `password` { #the-password-flow }

Revenons un peu en arrière et comprenons de quoi il s'agit.

Le « flux » `password` est l'une des manières (« flows ») définies dans OAuth2 pour gérer la sécurité et l'authentification.

OAuth2 a été conçu pour que le backend ou l'API puisse être indépendant du serveur qui authentifie l'utilisateur.

Mais dans ce cas, la même application **FastAPI** gérera l'API et l'authentification.

Voyons cela selon ce point de vue simplifié :

- L'utilisateur saisit le `username` et le `password` dans le frontend, puis appuie sur Entrée.
- Le frontend (exécuté dans le navigateur de l'utilisateur) envoie ce `username` et ce `password` vers une URL spécifique de notre API (déclarée avec `tokenUrl="token"`).
- L'API vérifie ce `username` et ce `password`, et répond avec un « token » (nous n'avons encore rien implémenté de tout cela).
    - Un « token » n'est qu'une chaîne contenant des informations que nous pouvons utiliser plus tard pour vérifier cet utilisateur.
    - Normalement, un token est configuré pour expirer après un certain temps.
        - Ainsi, l'utilisateur devra se reconnecter à un moment donné.
        - Et si le token est volé, le risque est moindre. Ce n'est pas une clé permanente qui fonctionnerait indéfiniment (dans la plupart des cas).
- Le frontend stocke ce token temporairement quelque part.
- L'utilisateur clique dans le frontend pour aller vers une autre section de l'application web frontend.
- Le frontend doit récupérer d'autres données depuis l'API.
    - Mais cela nécessite une authentification pour cet endpoint spécifique.
    - Donc, pour s'authentifier auprès de notre API, il envoie un en-tête `Authorization` avec une valeur `Bearer ` suivie du token.
    - Si le token contient `foobar`, le contenu de l'en-tête `Authorization` serait : `Bearer foobar`.

## Le `OAuth2PasswordBearer` de **FastAPI** { #fastapis-oauth2passwordbearer }

**FastAPI** fournit plusieurs outils, à différents niveaux d'abstraction, pour implémenter ces fonctionnalités de sécurité.

Dans cet exemple, nous allons utiliser **OAuth2**, avec le flux **Password**, en utilisant un token **Bearer**. Nous le faisons avec la classe `OAuth2PasswordBearer`.

/// info

Un token « bearer » n'est pas la seule option.

Mais c'est la meilleure pour notre cas d'utilisation.

Et cela pourrait être la meilleure pour la plupart des cas, sauf si vous êtes expert en OAuth2 et savez exactement pourquoi une autre option convient mieux à vos besoins.

Dans ce cas, **FastAPI** vous fournit aussi les outils pour la construire.

///

Lorsque nous créons une instance de la classe `OAuth2PasswordBearer`, nous passons le paramètre `tokenUrl`. Ce paramètre contient l'URL que le client (le frontend s'exécutant dans le navigateur de l'utilisateur) utilisera pour envoyer le `username` et le `password` afin d'obtenir un token.

{* ../../docs_src/security/tutorial001_an_py310.py hl[8] *}

/// tip | Astuce

Ici `tokenUrl="token"` fait référence à une URL relative `token` que nous n'avons pas encore créée. Comme c'est une URL relative, elle est équivalente à `./token`.

Parce que nous utilisons une URL relative, si votre API se trouvait à `https://example.com/`, alors elle ferait référence à `https://example.com/token`. Mais si votre API se trouvait à `https://example.com/api/v1/`, alors elle ferait référence à `https://example.com/api/v1/token`.

Utiliser une URL relative est important pour vous assurer que votre application continue de fonctionner même dans un cas d'usage avancé comme [Derrière un proxy](../../advanced/behind-a-proxy.md){.internal-link target=_blank}.

///

Ce paramètre ne crée pas cet endpoint / *chemin d'accès*, mais déclare que l'URL `/token` sera celle que le client doit utiliser pour obtenir le token. Cette information est utilisée dans OpenAPI, puis dans les systèmes de documentation API interactifs.

Nous créerons bientôt aussi le véritable chemin d'accès.

/// info

Si vous êtes un « Pythonista » très strict, vous pourriez ne pas apprécier le style du nom de paramètre `tokenUrl` au lieu de `token_url`.

C'est parce qu'il utilise le même nom que dans la spécification OpenAPI. Ainsi, si vous devez approfondir l'un de ces schémas de sécurité, vous pouvez simplement copier-coller pour trouver plus d'informations à ce sujet.

///

La variable `oauth2_scheme` est une instance de `OAuth2PasswordBearer`, mais c'est aussi un « callable ».

Elle pourrait être appelée ainsi :

```Python
oauth2_scheme(some, parameters)
```

Ainsi, elle peut être utilisée avec `Depends`.

### Utiliser { #use-it }

Vous pouvez maintenant passer ce `oauth2_scheme` en dépendance avec `Depends`.

{* ../../docs_src/security/tutorial001_an_py310.py hl[12] *}

Cette dépendance fournira une `str` qui est affectée au paramètre `token` de la fonction de *chemin d'accès*.

**FastAPI** saura qu'il peut utiliser cette dépendance pour définir un « schéma de sécurité » dans le schéma OpenAPI (et la documentation API automatique).

/// info | Détails techniques

**FastAPI** saura qu'il peut utiliser la classe `OAuth2PasswordBearer` (déclarée dans une dépendance) pour définir le schéma de sécurité dans OpenAPI parce qu'elle hérite de `fastapi.security.oauth2.OAuth2`, qui hérite à son tour de `fastapi.security.base.SecurityBase`.

Tous les utilitaires de sécurité qui s'intègrent à OpenAPI (et à la documentation API automatique) héritent de `SecurityBase`, c'est ainsi que **FastAPI** sait comment les intégrer dans OpenAPI.

///

## Ce que cela fait { #what-it-does }

Il va chercher dans la requête cet en-tête `Authorization`, vérifier si la valeur est `Bearer ` plus un token, et renverra le token en tant que `str`.

S'il ne voit pas d'en-tête `Authorization`, ou si la valeur n'a pas de token `Bearer `, il répondra directement avec une erreur de code d'état 401 (`UNAUTHORIZED`).

Vous n'avez même pas à vérifier si le token existe pour renvoyer une erreur. Vous pouvez être sûr que si votre fonction est exécutée, elle aura une `str` dans ce token.

Vous pouvez déjà l'essayer dans la documentation interactive :

<img src="/img/tutorial/security/image03.png">

Nous ne vérifions pas encore la validité du token, mais c'est déjà un début.

## Récapitulatif { #recap }

Ainsi, en seulement 3 ou 4 lignes supplémentaires, vous disposez déjà d'une forme primitive de sécurité.
