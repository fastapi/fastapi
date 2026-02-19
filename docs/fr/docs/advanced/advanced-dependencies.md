# Dépendances avancées { #advanced-dependencies }

## Dépendances paramétrées { #parameterized-dependencies }

Toutes les dépendances que nous avons vues étaient des fonctions ou des classes fixes.

Mais il peut y avoir des cas où vous souhaitez pouvoir définir des paramètres sur la dépendance, sans devoir déclarer de nombreuses fonctions ou classes différentes.

Imaginons que nous voulions avoir une dépendance qui vérifie si le paramètre de requête `q` contient un contenu fixe.

Mais nous voulons pouvoir paramétrer ce contenu fixe.

## Une instance « callable » { #a-callable-instance }

En Python, il existe un moyen de rendre une instance de classe « callable ».

Pas la classe elle‑même (qui est déjà un callable), mais une instance de cette classe.

Pour cela, nous déclarons une méthode `__call__` :

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[12] *}

Dans ce cas, ce `__call__` est ce que **FastAPI** utilisera pour détecter des paramètres supplémentaires et des sous‑dépendances, et c’est ce qui sera appelé pour transmettre ensuite une valeur au paramètre dans votre *fonction de chemin d'accès*.

## Paramétrer l'instance { #parameterize-the-instance }

Et maintenant, nous pouvons utiliser `__init__` pour déclarer les paramètres de l’instance, que nous utiliserons pour « paramétrer » la dépendance :

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[9] *}

Dans ce cas, **FastAPI** n’accèdera pas à `__init__` et ne s’en souciera pas ; nous l’utiliserons directement dans notre code.

## Créer une instance { #create-an-instance }

Nous pouvons créer une instance de cette classe avec :

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[18] *}

Et de cette façon, nous pouvons « paramétrer » notre dépendance, qui contient maintenant « bar », en tant qu’attribut `checker.fixed_content`.

## Utiliser l'instance comme dépendance { #use-the-instance-as-a-dependency }

Ensuite, nous pourrions utiliser ce `checker` dans un `Depends(checker)`, au lieu de `Depends(FixedContentQueryChecker)`, car la dépendance est l’instance, `checker`, et non la classe elle‑même.

Et lors de la résolution de la dépendance, **FastAPI** appellera ce `checker` comme ceci :

```Python
checker(q="somequery")
```

... et passera ce que cela renvoie comme valeur de la dépendance à notre *fonction de chemin d'accès*, en tant que paramètre `fixed_content_included` :

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[22] *}

/// tip | Astuce

Tout cela peut sembler artificiel. Et il n’est peut‑être pas encore très clair en quoi c’est utile.

Ces exemples sont volontairement simples, mais ils montrent comment tout cela fonctionne.

Dans les chapitres sur la sécurité, il existe des fonctions utilitaires implémentées de la même manière.

Si vous avez compris tout cela, vous savez déjà comment ces outils utilitaires pour la sécurité fonctionnent en interne.

///

## Dépendances avec `yield`, `HTTPException`, `except` et tâches d'arrière‑plan { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | Alertes

Vous n’avez très probablement pas besoin de ces détails techniques.

Ces détails sont utiles principalement si vous aviez une application FastAPI antérieure à la version 0.121.0 et que vous rencontrez des problèmes avec des dépendances utilisant `yield`.

///

Les dépendances avec `yield` ont évolué au fil du temps pour couvrir différents cas d’utilisation et corriger certains problèmes ; voici un résumé de ce qui a changé.

### Dépendances avec `yield` et `scope` { #dependencies-with-yield-and-scope }

Dans la version 0.121.0, **FastAPI** a ajouté la prise en charge de `Depends(scope="function")` pour les dépendances avec `yield`.

Avec `Depends(scope="function")`, le code d’arrêt après `yield` s’exécute immédiatement après la fin de la *fonction de chemin d'accès*, avant que la réponse ne soit renvoyée au client.

Et lorsque vous utilisez `Depends(scope="request")` (valeur par défaut), le code d’arrêt après `yield` s’exécute après l’envoi de la réponse.

Vous pouvez en lire davantage dans les documents pour [Dépendances avec `yield` - Sortie anticipée et `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope).

### Dépendances avec `yield` et `StreamingResponse`, Détails techniques { #dependencies-with-yield-and-streamingresponse-technical-details }

Avant FastAPI 0.118.0, si vous utilisiez une dépendance avec `yield`, elle exécutait le code d’arrêt après que la *fonction de chemin d'accès* a retourné, mais juste avant d’envoyer la réponse.

L’objectif était d’éviter de conserver des ressources plus longtemps que nécessaire pendant que la réponse transitait sur le réseau.

Ce changement impliquait aussi que si vous retourniez une `StreamingResponse`, le code d’arrêt de la dépendance avec `yield` aurait déjà été exécuté.

Par exemple, si vous aviez une session de base de données dans une dépendance avec `yield`, la `StreamingResponse` ne pourrait pas utiliser cette session pendant le streaming des données, car la session aurait déjà été fermée dans le code d’arrêt après `yield`.

Ce comportement a été annulé en 0.118.0, afin que le code d’arrêt après `yield` s’exécute après l’envoi de la réponse.

/// info

Comme vous le verrez ci‑dessous, c’est très similaire au comportement avant la version 0.106.0, mais avec plusieurs améliorations et corrections de bogues pour des cas limites.

///

#### Cas d’utilisation avec sortie anticipée du code { #use-cases-with-early-exit-code }

Il existe certains cas d’utilisation avec des conditions spécifiques qui pourraient bénéficier de l’ancien comportement, où le code d’arrêt des dépendances avec `yield` s’exécute avant l’envoi de la réponse.

Par exemple, imaginez que vous ayez du code qui utilise une session de base de données dans une dépendance avec `yield` uniquement pour vérifier un utilisateur, mais que la session de base de données ne soit plus jamais utilisée dans la *fonction de chemin d'accès*, seulement dans la dépendance, et que la réponse mette longtemps à être envoyée, comme une `StreamingResponse` qui envoie les données lentement mais qui, pour une raison quelconque, n’utilise pas la base de données.

Dans ce cas, la session de base de données serait conservée jusqu’à la fin de l’envoi de la réponse, mais si vous ne l’utilisez pas, il ne serait pas nécessaire de la conserver.

Voici à quoi cela pourrait ressembler :

{* ../../docs_src/dependencies/tutorial013_an_py310.py *}

Le code d’arrêt, la fermeture automatique de la `Session` dans :

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[19:21] *}

... serait exécuté après que la réponse a fini d’envoyer les données lentes :

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] hl[31:33] *}

Mais comme `generate_stream()` n’utilise pas la session de base de données, il n’est pas vraiment nécessaire de garder la session ouverte pendant l’envoi de la réponse.

Si vous avez ce cas d’utilisation spécifique avec SQLModel (ou SQLAlchemy), vous pouvez fermer explicitement la session dès que vous n’en avez plus besoin :

{* ../../docs_src/dependencies/tutorial014_an_py310.py ln[24:28] hl[28] *}

De cette manière, la session libérera la connexion à la base de données, afin que d’autres requêtes puissent l’utiliser.

Si vous avez un autre cas d’utilisation qui nécessite une sortie anticipée depuis une dépendance avec `yield`, veuillez créer une <a href="https://github.com/fastapi/fastapi/discussions/new?category=questions" class="external-link" target="_blank">Question de discussion GitHub</a> avec votre cas spécifique et pourquoi vous bénéficieriez d’une fermeture anticipée pour les dépendances avec `yield`.

S’il existe des cas d’utilisation convaincants pour une fermeture anticipée dans les dépendances avec `yield`, j’envisagerai d’ajouter une nouvelle façon d’y opter.

### Dépendances avec `yield` et `except`, Détails techniques { #dependencies-with-yield-and-except-technical-details }

Avant FastAPI 0.110.0, si vous utilisiez une dépendance avec `yield`, puis capturiez une exception avec `except` dans cette dépendance, et que vous ne relanciez pas l’exception, l’exception était automatiquement levée/transmise à tout gestionnaire d’exceptions ou au gestionnaire d’erreur interne du serveur.

Cela a été modifié dans la version 0.110.0 pour corriger une consommation de mémoire non gérée due aux exceptions transmises sans gestionnaire (erreurs internes du serveur), et pour rendre le comportement cohérent avec celui du code Python classique.

### Tâches d'arrière‑plan et dépendances avec `yield`, Détails techniques { #background-tasks-and-dependencies-with-yield-technical-details }

Avant FastAPI 0.106.0, lever des exceptions après `yield` n’était pas possible, le code d’arrêt dans les dépendances avec `yield` s’exécutait après l’envoi de la réponse, donc les [Gestionnaires d'exceptions](../tutorial/handling-errors.md#install-custom-exception-handlers){.internal-link target=_blank} avaient déjà été exécutés.

Cela avait été conçu ainsi principalement pour permettre d’utiliser les mêmes objets « générés par yield » par les dépendances à l’intérieur de tâches d’arrière‑plan, car le code d’arrêt s’exécutait après la fin des tâches d’arrière‑plan.

Cela a été modifié dans FastAPI 0.106.0 afin de ne pas conserver des ressources pendant l’attente de la transmission de la réponse sur le réseau.

/// tip | Astuce

De plus, une tâche d’arrière‑plan est normalement un ensemble de logique indépendant qui devrait être géré séparément, avec ses propres ressources (par ex. sa propre connexion à la base de données).

Ainsi, vous aurez probablement un code plus propre.

///

Si vous comptiez sur ce comportement, vous devez désormais créer les ressources pour les tâches d’arrière‑plan à l’intérieur de la tâche elle‑même, et n’utiliser en interne que des données qui ne dépendent pas des ressources des dépendances avec `yield`.

Par exemple, au lieu d’utiliser la même session de base de données, vous créeriez une nouvelle session de base de données à l’intérieur de la tâche d’arrière‑plan, et vous obtiendriez les objets depuis la base de données en utilisant cette nouvelle session. Puis, au lieu de passer l’objet obtenu depuis la base de données en paramètre à la fonction de tâche d’arrière‑plan, vous passeriez l’identifiant (ID) de cet objet et vous obtiendriez à nouveau l’objet à l’intérieur de la fonction de la tâche d’arrière‑plan.
