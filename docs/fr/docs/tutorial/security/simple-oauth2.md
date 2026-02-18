# OAuth2 simple avec Password et Bearer { #simple-oauth2-with-password-and-bearer }

Construisons maintenant à partir du chapitre précédent et ajoutons les éléments manquants pour avoir un flux de sécurité complet.

## Obtenir `username` et `password` { #get-the-username-and-password }

Nous allons utiliser les utilitaires de sécurité de **FastAPI** pour obtenir `username` et `password`.

OAuth2 spécifie que lorsqu'on utilise le « password flow » (ce que nous utilisons), le client/utilisateur doit envoyer des champs `username` et `password` en tant que données de formulaire.

Et la spécification indique que les champs doivent porter exactement ces noms. Ainsi, `user-name` ou `email` ne fonctionneraient pas.

Mais ne vous inquiétez pas, vous pouvez l'afficher comme vous le souhaitez à vos utilisateurs finaux dans le frontend.

Et vos modèles de base de données peuvent utiliser les noms que vous voulez.

Mais pour le chemin d'accès de connexion, nous devons utiliser ces noms pour être compatibles avec la spécification (et pouvoir, par exemple, utiliser le système de documentation API intégré).

La spécification précise également que `username` et `password` doivent être envoyés en données de formulaire (donc pas de JSON ici).

### `scope` { #scope }

La spécification indique aussi que le client peut envoyer un autre champ de formulaire « scope ».

Le nom du champ de formulaire est `scope` (au singulier), mais il s'agit en fait d'une longue chaîne contenant des « scopes » séparés par des espaces.

Chaque « scope » n'est qu'une chaîne (sans espaces).

Ils sont normalement utilisés pour déclarer des permissions de sécurité spécifiques, par exemple :

* `users:read` ou `users:write` sont des exemples courants.
* `instagram_basic` est utilisé par Facebook / Instagram.
* `https://www.googleapis.com/auth/drive` est utilisé par Google.

/// info

En OAuth2, un « scope » est simplement une chaîne qui déclare une permission spécifique requise.

Peu importe s'il contient d'autres caractères comme `:` ou si c'est une URL.

Ces détails dépendent de l'implémentation.

Pour OAuth2, ce ne sont que des chaînes.

///

## Écrire le code pour obtenir `username` et `password` { #code-to-get-the-username-and-password }

Utilisons maintenant les utilitaires fournis par **FastAPI** pour gérer cela.

### `OAuth2PasswordRequestForm` { #oauth2passwordrequestform }

Tout d'abord, importez `OAuth2PasswordRequestForm`, et utilisez-la en tant que dépendance avec `Depends` dans le chemin d'accès pour `/token` :

{* ../../docs_src/security/tutorial003_an_py310.py hl[4,78] *}

`OAuth2PasswordRequestForm` est une dépendance de classe qui déclare un corps de formulaire avec :

* Le `username`.
* Le `password`.
* Un champ optionnel `scope` sous forme d'une grande chaîne, composée de chaînes séparées par des espaces.
* Un `grant_type` optionnel.

/// tip | Astuce

La spécification OAuth2 exige en réalité un champ `grant_type` avec la valeur fixe `password`, mais `OAuth2PasswordRequestForm` ne l'impose pas.

Si vous avez besoin de l'imposer, utilisez `OAuth2PasswordRequestFormStrict` au lieu de `OAuth2PasswordRequestForm`.

///

* Un `client_id` optionnel (nous n'en avons pas besoin pour notre exemple).
* Un `client_secret` optionnel (nous n'en avons pas besoin pour notre exemple).

/// info

La classe `OAuth2PasswordRequestForm` n'est pas une classe spéciale pour **FastAPI** comme l'est `OAuth2PasswordBearer`.

`OAuth2PasswordBearer` indique à **FastAPI** qu'il s'agit d'un schéma de sécurité. Il est donc ajouté de cette façon à OpenAPI.

Mais `OAuth2PasswordRequestForm` est simplement une dépendance de classe que vous auriez pu écrire vous‑même, ou vous auriez pu déclarer des paramètres `Form` directement.

Mais comme c'est un cas d'usage courant, elle est fournie directement par **FastAPI**, simplement pour vous faciliter la vie.

///

### Utiliser les données du formulaire { #use-the-form-data }

/// tip | Astuce

L'instance de la classe de dépendance `OAuth2PasswordRequestForm` n'aura pas d'attribut `scope` contenant la longue chaîne séparée par des espaces ; elle aura plutôt un attribut `scopes` avec la liste réelle des chaînes pour chaque scope envoyé.

Nous n'utilisons pas `scopes` dans cet exemple, mais la fonctionnalité est disponible si vous en avez besoin.

///

Récupérez maintenant les données utilisateur depuis la (fausse) base de données, en utilisant le `username` du champ de formulaire.

S'il n'existe pas d'utilisateur, nous renvoyons une erreur indiquant « Incorrect username or password ».

Pour l'erreur, nous utilisons l'exception `HTTPException` :

{* ../../docs_src/security/tutorial003_an_py310.py hl[3,79:81] *}

### Vérifier le mot de passe { #check-the-password }

À ce stade, nous avons les données utilisateur depuis notre base, mais nous n'avons pas encore vérifié le mot de passe.

Mettons d'abord ces données dans le modèle Pydantic `UserInDB`.

Vous ne devez jamais enregistrer des mots de passe en clair ; nous allons donc utiliser le système (factice) de hachage de mot de passe.

Si les mots de passe ne correspondent pas, nous renvoyons la même erreur.

#### Hachage de mot de passe { #password-hashing }

Le « hachage » signifie : convertir un contenu (un mot de passe, dans ce cas) en une séquence d'octets (juste une chaîne) qui ressemble à du charabia.

Chaque fois que vous fournissez exactement le même contenu (exactement le même mot de passe), vous obtenez exactement le même charabia.

Mais vous ne pouvez pas convertir ce charabia pour retrouver le mot de passe.

##### Pourquoi utiliser le hachage de mot de passe { #why-use-password-hashing }

Si votre base de données est volée, le voleur n'aura pas les mots de passe en clair de vos utilisateurs, seulement les hachages.

Ainsi, il ne pourra pas essayer d'utiliser ces mêmes mots de passe dans un autre système (comme beaucoup d'utilisateurs utilisent le même mot de passe partout, ce serait dangereux).

{* ../../docs_src/security/tutorial003_an_py310.py hl[82:85] *}

#### À propos de `**user_dict` { #about-user-dict }

`UserInDB(**user_dict)` signifie :

Passez les clés et valeurs de `user_dict` directement comme arguments clé‑valeur, équivalent à :

```Python
UserInDB(
    username = user_dict["username"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    disabled = user_dict["disabled"],
    hashed_password = user_dict["hashed_password"],
)
```

/// info

Pour une explication plus complète de `**user_dict`, consultez [la documentation pour **Modèles supplémentaires**](../extra-models.md#about-user-in-dict){.internal-link target=_blank}.

///

## Renvoyer le jeton { #return-the-token }

La réponse de l'endpoint `token` doit être un objet JSON.

Il doit contenir un `token_type`. Dans notre cas, comme nous utilisons des jetons « Bearer », le type de jeton doit être « bearer ».

Et il doit contenir un `access_token`, avec une chaîne contenant notre jeton d'accès.

Pour cet exemple simple, nous allons faire quelque chose de complètement non sécurisé et renvoyer le même `username` comme jeton.

/// tip | Astuce

Dans le prochain chapitre, vous verrez une véritable implémentation sécurisée, avec du hachage de mot de passe et des jetons <abbr title="JSON Web Tokens">JWT</abbr>.

Mais pour l'instant, concentrons‑nous sur les détails spécifiques dont nous avons besoin.

///

{* ../../docs_src/security/tutorial003_an_py310.py hl[87] *}

/// tip | Astuce

D'après la spécification, vous devez renvoyer un JSON avec un `access_token` et un `token_type`, comme dans cet exemple.

C'est quelque chose que vous devez faire vous‑même dans votre code, et vous devez vous assurer d'utiliser ces clés JSON.

C'est presque la seule chose que vous devez vous rappeler de faire correctement vous‑même pour être conforme aux spécifications.

Pour le reste, **FastAPI** s'en charge pour vous.

///

## Mettre à jour les dépendances { #update-the-dependencies }

Nous allons maintenant mettre à jour nos dépendances.

Nous voulons obtenir `current_user` uniquement si cet utilisateur est actif.

Nous créons donc une dépendance supplémentaire `get_current_active_user` qui utilise à son tour `get_current_user` comme dépendance.

Ces deux dépendances renverront simplement une erreur HTTP si l'utilisateur n'existe pas, ou s'il est inactif.

Ainsi, dans notre endpoint, nous n'obtiendrons un utilisateur que si l'utilisateur existe, a été correctement authentifié et est actif :

{* ../../docs_src/security/tutorial003_an_py310.py hl[58:66,69:74,94] *}

/// info

L'en‑tête supplémentaire `WWW-Authenticate` avec la valeur `Bearer` que nous renvoyons ici fait également partie de la spécification.

Il est prévu qu'un code d'état HTTP (d'erreur) 401 « UNAUTHORIZED » renvoie également un en‑tête `WWW-Authenticate`.

Dans le cas des jetons bearer (notre cas), la valeur de cet en‑tête doit être `Bearer`.

Vous pouvez en réalité omettre cet en‑tête supplémentaire et cela fonctionnerait quand même.

Mais il est fourni ici pour être conforme aux spécifications.

De plus, il peut exister des outils qui l'attendent et l'utilisent (maintenant ou à l'avenir) et cela pourrait vous être utile, à vous ou à vos utilisateurs, maintenant ou à l'avenir.

C'est l'avantage des standards ...

///

## Voir en action { #see-it-in-action }

Ouvrez la documentation interactive : <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

### S'authentifier { #authenticate }

Cliquez sur le bouton « Authorize ».

Utilisez les identifiants :

Utilisateur : `johndoe`

Mot de passe : `secret`

<img src="/img/tutorial/security/image04.png">

Après vous être authentifié dans le système, vous verrez ceci :

<img src="/img/tutorial/security/image05.png">

### Obtenir vos propres données utilisateur { #get-your-own-user-data }

Utilisez maintenant l'opération `GET` avec le chemin `/users/me`.

Vous obtiendrez les données de votre utilisateur, par exemple :

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
```

<img src="/img/tutorial/security/image06.png">

Si vous cliquez sur l'icône de cadenas et vous vous déconnectez, puis réessayez la même opération, vous obtiendrez une erreur HTTP 401 :

```JSON
{
  "detail": "Not authenticated"
}
```

### Utilisateur inactif { #inactive-user }

Essayez maintenant avec un utilisateur inactif, authentifiez‑vous avec :

Utilisateur : `alice`

Mot de passe : `secret2`

Et essayez d'utiliser l'opération `GET` avec le chemin `/users/me`.

Vous obtiendrez une erreur « Inactive user », par exemple :

```JSON
{
  "detail": "Inactive user"
}
```

## Récapitulatif { #recap }

Vous avez maintenant les outils pour implémenter un système de sécurité complet basé sur `username` et `password` pour votre API.

En utilisant ces outils, vous pouvez rendre le système de sécurité compatible avec n'importe quelle base de données et avec n'importe quel modèle d'utilisateur ou de données.

Le seul détail manquant est qu'il n'est pas encore réellement « sécurisé ».

Dans le prochain chapitre, vous verrez comment utiliser une bibliothèque de hachage de mot de passe sécurisée et des jetons <abbr title="JSON Web Tokens">JWT</abbr>.
