# OAuth2 avec mot de passe (et hachage), Bearer avec des jetons JWT { #oauth2-with-password-and-hashing-bearer-with-jwt-tokens }

Maintenant que nous avons tout le flux de sécurité, rendons réellement l'application sécurisée, en utilisant des jetons <abbr title="JSON Web Tokens">JWT</abbr> et un hachage de mot de passe sécurisé.

Ce code est utilisable dans votre application, enregistrez les hachages de mots de passe dans votre base de données, etc.

Nous allons repartir d'où nous nous sommes arrêtés dans le chapitre précédent et l'enrichir.

## À propos de JWT { #about-jwt }

JWT signifie « JSON Web Tokens ».

C'est une norme pour coder un objet JSON dans une longue chaîne compacte sans espaces. Cela ressemble à ceci :

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

Il n'est pas chiffré ; ainsi, n'importe qui peut récupérer les informations à partir de son contenu.

Mais il est signé. Ainsi, quand vous recevez un jeton que vous avez émis, vous pouvez vérifier que vous l'avez bien émis.

De cette façon, vous pouvez créer un jeton avec une expiration d'une semaine, par exemple. Et quand l'utilisateur revient le lendemain avec ce jeton, vous savez qu'il est toujours connecté à votre système.

Après une semaine, le jeton aura expiré et l'utilisateur ne sera pas autorisé et devra se reconnecter pour obtenir un nouveau jeton. Et si l'utilisateur (ou un tiers) essayait de modifier le jeton pour changer l'expiration, vous pourriez le détecter, car les signatures ne correspondraient pas.

Si vous voulez expérimenter avec des jetons JWT et voir comment ils fonctionnent, consultez <a href="https://jwt.io/" class="external-link" target="_blank">https://jwt.io</a>.

## Installer `PyJWT` { #install-pyjwt }

Nous devons installer `PyJWT` pour générer et vérifier les jetons JWT en Python.

Assurez-vous de créer un [environnement virtuel](../../virtual-environments.md){.internal-link target=_blank}, de l'activer, puis d'installer `pyjwt` :

<div class="termy">

```console
$ pip install pyjwt

---> 100%
```

</div>

/// info

Si vous prévoyez d'utiliser des algorithmes de signature numérique comme RSA ou ECDSA, vous devez installer la dépendance de bibliothèque de cryptographie `pyjwt[crypto]`.

Vous pouvez en lire davantage dans la <a href="https://pyjwt.readthedocs.io/en/latest/installation.html" class="external-link" target="_blank">documentation d'installation de PyJWT</a>.

///

## Hachage de mot de passe { #password-hashing }

« Hachage » signifie convertir un contenu (un mot de passe dans ce cas) en une séquence d'octets (juste une chaîne) qui ressemble à du charabia.

Chaque fois que vous fournissez exactement le même contenu (exactement le même mot de passe), vous obtenez exactement le même charabia.

Mais vous ne pouvez pas convertir le charabia en sens inverse vers le mot de passe.

### Pourquoi utiliser le hachage de mot de passe { #why-use-password-hashing }

Si votre base de données est volée, le voleur n'aura pas les mots de passe en clair de vos utilisateurs, seulement les hachages.

Ainsi, le voleur ne pourra pas essayer d'utiliser ce mot de passe dans un autre système (comme beaucoup d'utilisateurs utilisent le même mot de passe partout, ce serait dangereux).

## Installer `pwdlib` { #install-pwdlib }

pwdlib est un excellent package Python pour gérer les hachages de mots de passe.

Il prend en charge de nombreux algorithmes de hachage sécurisés et des utilitaires pour travailler avec eux.

L'algorithme recommandé est « Argon2 ».

Assurez-vous de créer un [environnement virtuel](../../virtual-environments.md){.internal-link target=_blank}, de l'activer, puis d'installer pwdlib avec Argon2 :

<div class="termy">

```console
$ pip install "pwdlib[argon2]"

---> 100%
```

</div>

/// tip | Astuce

Avec `pwdlib`, vous pouvez même le configurer pour pouvoir lire des mots de passe créés par **Django**, un plug-in de sécurité **Flask** ou bien d'autres.

Ainsi, vous seriez par exemple en mesure de partager les mêmes données d'une application Django dans une base de données avec une application FastAPI. Ou de migrer progressivement une application Django en utilisant la même base de données.

Et vos utilisateurs pourraient se connecter depuis votre application Django ou depuis votre application **FastAPI**, en même temps.

///

## Hacher et vérifier les mots de passe { #hash-and-verify-the-passwords }

Importez les outils nécessaires depuis `pwdlib`.

Créez une instance PasswordHash avec les réglages recommandés ; elle sera utilisée pour hacher et vérifier les mots de passe.

/// tip | Astuce

pwdlib prend également en charge l'algorithme de hachage bcrypt, mais n'inclut pas les algorithmes hérités. Pour travailler avec des hachages obsolètes, il est recommandé d'utiliser la bibliothèque passlib.

Par exemple, vous pourriez l'utiliser pour lire et vérifier des mots de passe générés par un autre système (comme Django), mais hacher tous les nouveaux mots de passe avec un autre algorithme comme Argon2 ou Bcrypt.

Et rester compatible avec tous en même temps.

///

Créez une fonction utilitaire pour hacher un mot de passe fourni par l'utilisateur.

Et une autre pour vérifier si un mot de passe reçu correspond au hachage stocké.

Et une autre pour authentifier et renvoyer un utilisateur.

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,51,58:59,62:63,72:79] *}

Lorsque `authenticate_user` est appelée avec un nom d'utilisateur qui n'existe pas dans la base de données, nous exécutons tout de même `verify_password` contre un hachage factice.

Cela garantit que le point de terminaison met approximativement le même temps à répondre que le nom d'utilisateur soit valide ou non, empêchant des **attaques temporelles** qui pourraient être utilisées pour énumérer les noms d'utilisateur existants.

/// note | Remarque

Si vous consultez la nouvelle (fausse) base de données `fake_users_db`, vous verrez à quoi ressemble maintenant le mot de passe haché : `"$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"`.

///

## Gérer les jetons JWT { #handle-jwt-tokens }

Importez les modules installés.

Créez une clé secrète aléatoire qui sera utilisée pour signer les jetons JWT.

Pour générer une clé secrète aléatoire sécurisée, utilisez la commande :

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

Et copiez la sortie dans la variable `SECRET_KEY` (n'utilisez pas celle de l'exemple).

Créez une variable `ALGORITHM` avec l'algorithme utilisé pour signer le jeton JWT, et définissez-la à `"HS256"`.

Créez une variable pour l'expiration du jeton.

Définissez un modèle Pydantic qui sera utilisé dans le point de terminaison du jeton pour la réponse.

Créez une fonction utilitaire pour générer un nouveau jeton d'accès.

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,82:90] *}

## Mettre à jour les dépendances { #update-the-dependencies }

Mettez à jour `get_current_user` pour recevoir le même jeton qu'auparavant, mais cette fois en utilisant des jetons JWT.

Décodez le jeton reçu, vérifiez-le, et renvoyez l'utilisateur courant.

Si le jeton est invalide, renvoyez immédiatement une erreur HTTP.

{* ../../docs_src/security/tutorial004_an_py310.py hl[93:110] *}

## Mettre à jour le *chemin d'accès* `/token` { #update-the-token-path-operation }

Créez un `timedelta` avec la durée d'expiration du jeton.

Créez un véritable jeton d'accès JWT et renvoyez-le.

{* ../../docs_src/security/tutorial004_an_py310.py hl[121:136] *}

### Détails techniques au sujet du « subject » JWT `sub` { #technical-details-about-the-jwt-subject-sub }

La spécification JWT indique qu'il existe une clé `sub`, contenant le sujet du jeton.

Son utilisation est facultative, mais c'est là que vous placeriez l'identifiant de l'utilisateur ; nous l'utilisons donc ici.

Les JWT peuvent être utilisés pour d'autres choses que l'identification d'un utilisateur et l'autorisation d'effectuer des opérations directement sur votre API.

Par exemple, vous pourriez identifier une « voiture » ou un « article de blog ».

Vous pourriez ensuite ajouter des permissions sur cette entité, comme « conduire » (pour la voiture) ou « modifier » (pour le blog).

Vous pourriez alors donner ce jeton JWT à un utilisateur (ou un bot), et il pourrait l'utiliser pour effectuer ces actions (conduire la voiture, ou modifier l'article de blog) sans même avoir besoin d'avoir un compte, uniquement avec le jeton JWT que votre API a généré pour cela.

En utilisant ces idées, les JWT peuvent servir à des scénarios bien plus sophistiqués.

Dans ces cas, plusieurs de ces entités peuvent avoir le même identifiant, disons `foo` (un utilisateur `foo`, une voiture `foo`, et un article de blog `foo`).

Donc, pour éviter les collisions d'identifiants, lors de la création du jeton JWT pour l'utilisateur, vous pouvez préfixer la valeur de la clé `sub`, par exemple avec `username:`. Ainsi, dans cet exemple, la valeur de `sub` aurait pu être : `username:johndoe`.

L'important à garder à l'esprit est que la clé `sub` doit contenir un identifiant unique dans toute l'application, et ce doit être une chaîne de caractères.

## Vérifier { #check-it }

Lancez le serveur et allez à la documentation : <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vous verrez l'interface utilisateur suivante :

<img src="/img/tutorial/security/image07.png">

Autorisez l'application de la même manière qu'auparavant.

En utilisant les identifiants :

Nom d'utilisateur : `johndoe`
Mot de passe : `secret`

/// check | Vérifications

Remarquez qu'à aucun endroit du code le mot de passe en clair « secret » n'apparaît, nous n'avons que la version hachée.

///

<img src="/img/tutorial/security/image08.png">

Appelez le point de terminaison `/users/me/`, vous obtiendrez la réponse suivante :

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

Si vous ouvrez les outils de développement, vous pouvez voir que les données envoyées n'incluent que le jeton ; le mot de passe n'est envoyé que dans la première requête pour authentifier l'utilisateur et obtenir ce jeton d'accès, mais plus ensuite :

<img src="/img/tutorial/security/image10.png">

/// note | Remarque

Remarquez l'en-tête `Authorization`, avec une valeur qui commence par `Bearer `.

///

## Utilisation avancée avec `scopes` { #advanced-usage-with-scopes }

OAuth2 comporte la notion de « scopes ».

Vous pouvez les utiliser pour ajouter un ensemble spécifique d'autorisations à un jeton JWT.

Vous pouvez ensuite donner ce jeton directement à un utilisateur ou à un tiers, pour interagir avec votre API avec un ensemble de restrictions.

Vous pouvez apprendre à les utiliser et comment ils sont intégrés à **FastAPI** plus tard dans le **Guide de l'utilisateur avancé**.

## Récapitulatif { #recap }

Avec ce que vous avez vu jusqu'à présent, vous pouvez configurer une application **FastAPI** sécurisée en utilisant des standards comme OAuth2 et JWT.

Dans presque n'importe quel framework, la gestion de la sécurité devient assez rapidement un sujet plutôt complexe.

De nombreux packages qui la simplifient beaucoup doivent faire de nombreux compromis avec le modèle de données, la base de données et les fonctionnalités disponibles. Et certains de ces packages qui simplifient trop les choses comportent en fait des failles de sécurité sous-jacentes.

---

**FastAPI** ne fait aucun compromis avec une base de données, un modèle de données ni un outil.

Il vous donne toute la flexibilité pour choisir ceux qui conviennent le mieux à votre projet.

Et vous pouvez utiliser directement de nombreux packages bien maintenus et largement utilisés comme `pwdlib` et `PyJWT`, car **FastAPI** n'exige aucun mécanisme complexe pour intégrer des packages externes.

Mais il vous fournit les outils pour simplifier le processus autant que possible sans compromettre la flexibilité, la robustesse ou la sécurité.

Et vous pouvez utiliser et implémenter des protocoles sécurisés et standard, comme OAuth2, de manière relativement simple.

Vous pouvez en apprendre davantage dans le **Guide de l'utilisateur avancé** sur la façon d'utiliser les « scopes » OAuth2, pour un système d'autorisations plus fin, en suivant ces mêmes standards. OAuth2 avec scopes est le mécanisme utilisé par de nombreux grands fournisseurs d'authentification, comme Facebook, Google, GitHub, Microsoft, X (Twitter), etc., pour autoriser des applications tierces à interagir avec leurs API au nom de leurs utilisateurs.
