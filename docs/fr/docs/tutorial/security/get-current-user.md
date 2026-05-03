# Obtenir l'utilisateur actuel { #get-current-user }

Dans le chapitre précédent, le système de sécurité (basé sur le système d'injection de dépendances) fournissait à la *fonction de chemin d'accès* un `token` en tant que `str` :

{* ../../docs_src/security/tutorial001_an_py310.py hl[12] *}

Mais ce n'est pas encore très utile.

Faisons en sorte qu'il nous fournisse l'utilisateur actuel.

## Créer un modèle d'utilisateur { #create-a-user-model }

Commençons par créer un modèle d'utilisateur Pydantic.

De la même manière que nous utilisons Pydantic pour déclarer des corps de requête, nous pouvons l'utiliser ailleurs :

{* ../../docs_src/security/tutorial002_an_py310.py hl[5,12:6] *}

## Créer une dépendance `get_current_user` { #create-a-get-current-user-dependency }

Créons une dépendance `get_current_user`.

Rappelez-vous que les dépendances peuvent avoir des sous-dépendances ?

`get_current_user` aura une dépendance avec le même `oauth2_scheme` que nous avons créé précédemment.

Comme nous le faisions auparavant directement dans le *chemin d'accès*, notre nouvelle dépendance `get_current_user` recevra un `token` en tant que `str` de la sous-dépendance `oauth2_scheme` :

{* ../../docs_src/security/tutorial002_an_py310.py hl[25] *}

## Récupérer l'utilisateur { #get-the-user }

`get_current_user` utilisera une fonction utilitaire (factice) que nous avons créée, qui prend un token en `str` et retourne notre modèle Pydantic `User` :

{* ../../docs_src/security/tutorial002_an_py310.py hl[19:22,26:27] *}

## Injecter l'utilisateur actuel { #inject-the-current-user }

Nous pouvons donc utiliser le même `Depends` avec notre `get_current_user` dans le *chemin d'accès* :

{* ../../docs_src/security/tutorial002_an_py310.py hl[31] *}

Remarquez que nous déclarons le type de `current_user` comme le modèle Pydantic `User`.

Cela nous aidera dans la fonction avec toute l'autocomplétion et les vérifications de type.

/// tip | Astuce

Vous vous souvenez peut-être que les corps de requête sont également déclarés avec des modèles Pydantic.

Ici, **FastAPI** ne s'y trompera pas car vous utilisez `Depends`.

///

/// check | Vérifications

La manière dont ce système de dépendances est conçu nous permet d'avoir différentes dépendances (différents « dependables ») qui retournent toutes un modèle `User`.

Nous ne sommes pas limités à une seule dépendance pouvant retourner ce type de données.

///

## Autres modèles { #other-models }

Vous pouvez maintenant obtenir l'utilisateur actuel directement dans les *fonctions de chemin d'accès* et gérer les mécanismes de sécurité au niveau de l'**Injection de dépendances**, en utilisant `Depends`.

Et vous pouvez utiliser n'importe quel modèle ou données pour les exigences de sécurité (dans ce cas, un modèle Pydantic `User`).

Mais vous n'êtes pas limité à un modèle, une classe ou un type de données spécifique.

Voulez-vous avoir un `id` et `email` et ne pas avoir de `username` dans votre modèle ? Bien sûr. Vous pouvez utiliser ces mêmes outils.

Voulez-vous simplement avoir un `str` ? Ou juste un `dict` ? Ou directement une instance d'un modèle de classe de base de données ? Tout fonctionne de la même manière.

Vous n'avez en fait pas d'utilisateurs qui se connectent à votre application, mais des robots, bots ou d'autres systèmes, qui n'ont qu'un jeton d'accès ? Là encore, tout fonctionne de la même façon.

Utilisez simplement tout type de modèle, toute sorte de classe, tout type de base de données dont vous avez besoin pour votre application. **FastAPI** vous couvre avec le système d'injection de dépendances.

## Taille du code { #code-size }

Cet exemple peut sembler verbeux. Gardez à l'esprit que nous mélangeons sécurité, modèles de données, fonctions utilitaires et *chemins d'accès* dans le même fichier.

Mais voici le point clé.

La partie sécurité et injection de dépendances est écrite une seule fois.

Et vous pouvez la rendre aussi complexe que vous le souhaitez. Et malgré tout, ne l'écrire qu'une seule fois, en un seul endroit. Avec toute la flexibilité.

Mais vous pouvez avoir des milliers d'endpoints (*chemins d'accès*) utilisant le même système de sécurité.

Et tous (ou seulement une partie d'entre eux, si vous le souhaitez) peuvent profiter de la réutilisation de ces dépendances ou de toute autre dépendance que vous créez.

Et tous ces milliers de *chemins d'accès* peuvent tenir en seulement 3 lignes :

{* ../../docs_src/security/tutorial002_an_py310.py hl[30:32] *}

## Récapitulatif { #recap }

Vous pouvez désormais obtenir l'utilisateur actuel directement dans votre *fonction de chemin d'accès*.

Nous avons déjà fait la moitié du chemin.

Il nous suffit d'ajouter un *chemin d'accès* pour que l'utilisateur/client envoie effectivement le `username` et le `password`.

C'est pour la suite.
