# Scopes OAuth2 { #oauth2-scopes }

Vous pouvez utiliser des scopes OAuth2 directement avec **FastAPI**, ils sont intégrés pour fonctionner de manière transparente.

Cela vous permettrait d’avoir un système d’autorisations plus fin, conforme au standard OAuth2, intégré à votre application OpenAPI (et à la documentation de l’API).

OAuth2 avec scopes est le mécanisme utilisé par de nombreux grands fournisseurs d’authentification, comme Facebook, Google, GitHub, Microsoft, X (Twitter), etc. Ils l’utilisent pour fournir des permissions spécifiques aux utilisateurs et aux applications.

Chaque fois que vous « log in with » Facebook, Google, GitHub, Microsoft, X (Twitter), cette application utilise OAuth2 avec scopes.

Dans cette section, vous verrez comment gérer l’authentification et l’autorisation avec le même OAuth2 avec scopes dans votre application **FastAPI**.

/// warning | Alertes

C’est une section plus ou moins avancée. Si vous débutez, vous pouvez la passer.

Vous n’avez pas nécessairement besoin des scopes OAuth2, et vous pouvez gérer l’authentification et l’autorisation comme vous le souhaitez.

Mais OAuth2 avec scopes peut s’intégrer élégamment à votre API (avec OpenAPI) et à votre documentation d’API.

Néanmoins, c’est toujours à vous de faire appliquer ces scopes, ou toute autre exigence de sécurité/autorisation, selon vos besoins, dans votre code.

Dans de nombreux cas, OAuth2 avec scopes peut être excessif.

Mais si vous savez que vous en avez besoin, ou si vous êtes curieux, continuez à lire.

///

## Scopes OAuth2 et OpenAPI { #oauth2-scopes-and-openapi }

La spécification OAuth2 définit des « scopes » comme une liste de chaînes séparées par des espaces.

Le contenu de chacune de ces chaînes peut avoir n’importe quel format, mais ne doit pas contenir d’espaces.

Ces scopes représentent des « permissions ».

Dans OpenAPI (par ex. la documentation de l’API), vous pouvez définir des « schémas de sécurité ».

Lorsqu’un de ces schémas de sécurité utilise OAuth2, vous pouvez aussi déclarer et utiliser des scopes.

Chaque « scope » est juste une chaîne (sans espaces).

Ils sont généralement utilisés pour déclarer des permissions de sécurité spécifiques, par exemple :

* `users:read` ou `users:write` sont des exemples courants.
* `instagram_basic` est utilisé par Facebook / Instagram.
* `https://www.googleapis.com/auth/drive` est utilisé par Google.

/// info

Dans OAuth2, un « scope » est simplement une chaîne qui déclare une permission spécifique requise.

Peu importe s’il contient d’autres caractères comme `:` ou si c’est une URL.

Ces détails dépendent de l’implémentation.

Pour OAuth2, ce ne sont que des chaînes.

///

## Vue d’ensemble { #global-view }

Voyons d’abord rapidement les parties qui changent par rapport aux exemples du **Tutoriel - Guide utilisateur** pour [OAuth2 avec mot de passe (et hachage), Bearer avec jetons JWT](../../tutorial/security/oauth2-jwt.md){.internal-link target=_blank}. Cette fois, en utilisant des scopes OAuth2 :

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,9,13,47,65,106,108:116,122:126,130:136,141,157] *}

Passons maintenant en revue ces changements étape par étape.

## Déclarer le schéma de sécurité OAuth2 { #oauth2-security-scheme }

Le premier changement est que nous déclarons maintenant le schéma de sécurité OAuth2 avec deux scopes disponibles, `me` et `items`.

Le paramètre `scopes` reçoit un `dict` avec chaque scope en clé et la description en valeur :

{* ../../docs_src/security/tutorial005_an_py310.py hl[63:66] *}

Comme nous déclarons maintenant ces scopes, ils apparaîtront dans la documentation de l’API lorsque vous vous authentifiez/autorisez.

Et vous pourrez sélectionner à quels scopes vous souhaitez accorder l’accès : `me` et `items`.

C’est le même mécanisme utilisé lorsque vous donnez des permissions en vous connectant avec Facebook, Google, GitHub, etc. :

<img src="/img/tutorial/security/image11.png">

## Jeton JWT avec scopes { #jwt-token-with-scopes }

Modifiez maintenant le *chemin d’accès* du jeton pour renvoyer les scopes demandés.

Nous utilisons toujours le même `OAuth2PasswordRequestForm`. Il inclut une propriété `scopes` avec une `list` de `str`, contenant chaque scope reçu dans la requête.

Et nous renvoyons les scopes comme partie du jeton JWT.

/// danger | Danger

Pour simplifier, ici nous ajoutons directement au jeton les scopes reçus.

Mais dans votre application, pour la sécurité, vous devez vous assurer de n’ajouter que les scopes que l’utilisateur est réellement autorisé à avoir, ou ceux que vous avez prédéfinis.

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[157] *}

## Déclarer des scopes dans les chemins d’accès et les dépendances { #declare-scopes-in-path-operations-and-dependencies }

Nous déclarons maintenant que le *chemin d’accès* `/users/me/items/` nécessite le scope `items`.

Pour cela, nous importons et utilisons `Security` depuis `fastapi`.

Vous pouvez utiliser `Security` pour déclarer des dépendances (comme `Depends`), mais `Security` reçoit aussi un paramètre `scopes` avec une liste de scopes (chaînes).

Dans ce cas, nous passons une fonction de dépendance `get_current_active_user` à `Security` (de la même manière que nous le ferions avec `Depends`).

Mais nous passons aussi une `list` de scopes, ici avec un seul scope : `items` (il pourrait y en avoir plus).

Et la fonction de dépendance `get_current_active_user` peut également déclarer des sous-dépendances, non seulement avec `Depends` mais aussi avec `Security`. En déclarant sa propre fonction de sous-dépendance (`get_current_user`), et davantage d’exigences de scopes.

Dans ce cas, elle nécessite le scope `me` (elle pourrait en exiger plusieurs).

/// note | Remarque

Vous n’avez pas nécessairement besoin d’ajouter des scopes différents à différents endroits.

Nous le faisons ici pour montrer comment **FastAPI** gère des scopes déclarés à différents niveaux.

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,141,172] *}

/// info | Détails techniques

`Security` est en réalité une sous-classe de `Depends`, et elle n’a qu’un paramètre supplémentaire que nous verrons plus tard.

Mais en utilisant `Security` au lieu de `Depends`, **FastAPI** saura qu’il peut déclarer des scopes de sécurité, les utiliser en interne et documenter l’API avec OpenAPI.

Cependant, lorsque vous importez `Query`, `Path`, `Depends`, `Security` et d’autres depuis `fastapi`, ce sont en fait des fonctions qui renvoient des classes spéciales.

///

## Utiliser `SecurityScopes` { #use-securityscopes }

Mettez maintenant à jour la dépendance `get_current_user`.

C’est celle utilisée par les dépendances ci-dessus.

C’est ici que nous utilisons le même schéma OAuth2 que nous avons créé auparavant, en le déclarant comme dépendance : `oauth2_scheme`.

Comme cette fonction de dépendance n’a pas elle-même d’exigences de scope, nous pouvons utiliser `Depends` avec `oauth2_scheme`, nous n’avons pas à utiliser `Security` quand nous n’avons pas besoin de spécifier des scopes de sécurité.

Nous déclarons également un paramètre spécial de type `SecurityScopes`, importé de `fastapi.security`.

Cette classe `SecurityScopes` est similaire à `Request` (`Request` servait à obtenir directement l’objet requête).

{* ../../docs_src/security/tutorial005_an_py310.py hl[9,106] *}

## Utiliser les `scopes` { #use-the-scopes }

Le paramètre `security_scopes` sera de type `SecurityScopes`.

Il aura une propriété `scopes` avec une liste contenant tous les scopes requis par lui-même et par toutes les dépendances qui l’utilisent comme sous-dépendance. Cela signifie, tous les « dépendants » ... cela peut paraître déroutant, c’est expliqué à nouveau plus bas.

L’objet `security_scopes` (de classe `SecurityScopes`) fournit aussi un attribut `scope_str` avec une chaîne unique, contenant ces scopes séparés par des espaces (nous allons l’utiliser).

Nous créons une `HTTPException` que nous pouvons réutiliser (`raise`) plus tard à plusieurs endroits.

Dans cette exception, nous incluons les scopes requis (le cas échéant) sous forme de chaîne séparée par des espaces (en utilisant `scope_str`). Nous plaçons cette chaîne contenant les scopes dans l’en-tête `WWW-Authenticate` (cela fait partie de la spécification).

{* ../../docs_src/security/tutorial005_an_py310.py hl[106,108:116] *}

## Vérifier le `username` et la structure des données { #verify-the-username-and-data-shape }

Nous vérifions que nous obtenons un `username`, et extrayons les scopes.

Nous validons ensuite ces données avec le modèle Pydantic (en capturant l’exception `ValidationError`), et si nous obtenons une erreur lors de la lecture du jeton JWT ou de la validation des données avec Pydantic, nous levons la `HTTPException` que nous avons créée auparavant.

Pour cela, nous mettons à jour le modèle Pydantic `TokenData` avec une nouvelle propriété `scopes`.

En validant les données avec Pydantic, nous pouvons nous assurer que nous avons, par exemple, exactement une `list` de `str` pour les scopes et un `str` pour le `username`.

Au lieu, par exemple, d’un `dict`, ou autre chose, ce qui pourrait casser l’application plus tard et constituer un risque de sécurité.

Nous vérifions également que nous avons un utilisateur avec ce nom d’utilisateur, et sinon, nous levons la même exception que précédemment.

{* ../../docs_src/security/tutorial005_an_py310.py hl[47,117:129] *}

## Vérifier les `scopes` { #verify-the-scopes }

Nous vérifions maintenant que tous les scopes requis, par cette dépendance et tous les dépendants (y compris les *chemins d’accès*), sont inclus dans les scopes fournis dans le jeton reçu, sinon nous levons une `HTTPException`.

Pour cela, nous utilisons `security_scopes.scopes`, qui contient une `list` avec tous ces scopes en `str`.

{* ../../docs_src/security/tutorial005_an_py310.py hl[130:136] *}

## Arbre de dépendances et scopes { #dependency-tree-and-scopes }

Revoyons encore cet arbre de dépendances et les scopes.

Comme la dépendance `get_current_active_user` a une sous-dépendance `get_current_user`, le scope « me » déclaré dans `get_current_active_user` sera inclus dans la liste des scopes requis dans `security_scopes.scopes` passé à `get_current_user`.

Le *chemin d’accès* lui-même déclare également un scope, « items », il sera donc aussi présent dans la liste `security_scopes.scopes` passée à `get_current_user`.

Voici à quoi ressemble la hiérarchie des dépendances et des scopes :

* Le *chemin d’accès* `read_own_items` a :
    * Des scopes requis `["items"]` avec la dépendance :
    * `get_current_active_user` :
        * La fonction de dépendance `get_current_active_user` a :
            * Des scopes requis `["me"]` avec la dépendance :
            * `get_current_user` :
                * La fonction de dépendance `get_current_user` a :
                    * Aucun scope requis par elle-même.
                    * Une dépendance utilisant `oauth2_scheme`.
                    * Un paramètre `security_scopes` de type `SecurityScopes` :
                        * Ce paramètre `security_scopes` a une propriété `scopes` avec une `list` contenant tous les scopes déclarés ci-dessus, donc :
                            * `security_scopes.scopes` contiendra `["me", "items"]` pour le *chemin d’accès* `read_own_items`.
                            * `security_scopes.scopes` contiendra `["me"]` pour le *chemin d’accès* `read_users_me`, car il est déclaré dans la dépendance `get_current_active_user`.
                            * `security_scopes.scopes` contiendra `[]` (rien) pour le *chemin d’accès* `read_system_status`, car il n’a déclaré aucun `Security` avec des `scopes`, et sa dépendance, `get_current_user`, ne déclare pas non plus de `scopes`.

/// tip | Astuce

L’élément important et « magique » ici est que `get_current_user` aura une liste différente de `scopes` à vérifier pour chaque *chemin d’accès*.

Tout dépend des `scopes` déclarés dans chaque *chemin d’accès* et chaque dépendance dans l’arbre de dépendances pour ce *chemin d’accès* spécifique.

///

## Détails supplémentaires sur `SecurityScopes` { #more-details-about-securityscopes }

Vous pouvez utiliser `SecurityScopes` à n’importe quel endroit, et à de multiples endroits, il n’a pas besoin d’être dans la dépendance « root ».

Il aura toujours les scopes de sécurité déclarés dans les dépendances `Security` actuelles et tous les dépendants pour **ce** *chemin d’accès* spécifique et **cet** arbre de dépendances spécifique.

Comme `SecurityScopes` contient tous les scopes déclarés par les dépendants, vous pouvez l’utiliser pour vérifier qu’un jeton possède les scopes requis dans une fonction de dépendance centrale, puis déclarer des exigences de scopes différentes dans différents *chemins d’accès*.

Elles seront vérifiées indépendamment pour chaque *chemin d’accès*.

## Tester { #check-it }

Si vous ouvrez la documentation de l’API, vous pouvez vous authentifier et spécifier quels scopes vous voulez autoriser.

<img src="/img/tutorial/security/image11.png">

Si vous ne sélectionnez aucun scope, vous serez « authenticated », mais lorsque vous essayerez d’accéder à `/users/me/` ou `/users/me/items/`, vous obtiendrez une erreur indiquant que vous n’avez pas suffisamment de permissions. Vous pourrez toujours accéder à `/status/`.

Et si vous sélectionnez le scope `me` mais pas le scope `items`, vous pourrez accéder à `/users/me/` mais pas à `/users/me/items/`.

C’est ce qui arriverait à une application tierce qui tenterait d’accéder à l’un de ces *chemins d’accès* avec un jeton fourni par un utilisateur, selon le nombre de permissions que l’utilisateur a accordées à l’application.

## À propos des intégrations tierces { #about-third-party-integrations }

Dans cet exemple, nous utilisons le flux OAuth2 « password ».

C’est approprié lorsque nous nous connectons à notre propre application, probablement avec notre propre frontend.

Parce que nous pouvons lui faire confiance pour recevoir le `username` et le `password`, puisque nous le contrôlons.

Mais si vous construisez une application OAuth2 à laquelle d’autres se connecteraient (c.-à-d., si vous construisez un fournisseur d’authentification équivalent à Facebook, Google, GitHub, etc.), vous devez utiliser l’un des autres flux.

Le plus courant est le flux implicite.

Le plus sûr est le flux « code », mais il est plus complexe à implémenter car il nécessite plus d’étapes. Comme il est plus complexe, de nombreux fournisseurs finissent par recommander le flux implicite.

/// note | Remarque

Il est courant que chaque fournisseur d’authentification nomme ses flux différemment, pour en faire une partie de sa marque.

Mais au final, ils implémentent le même standard OAuth2.

///

**FastAPI** inclut des utilitaires pour tous ces flux d’authentification OAuth2 dans `fastapi.security.oauth2`.

## `Security` dans les dépendances du décorateur `dependencies` { #security-in-decorator-dependencies }

De la même manière que vous pouvez définir une `list` de `Depends` dans le paramètre `dependencies` du décorateur (comme expliqué dans [Dépendances dans les décorateurs de chemins d’accès](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}), vous pouvez aussi utiliser `Security` avec des `scopes` à cet endroit.
