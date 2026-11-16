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

{* ../../docs_src/dependencies/tutorial011.py hl[12] *}

Dans ce cas, ce `__call__` est ce que **FastAPI** utilisera pour détecter des paramètres supplémentaires et des sous‑dépendances, et c’est ce qui sera appelé pour transmettre ensuite une valeur au paramètre dans votre *fonction de chemin d'accès*.

## Paramétrer l'instance { #parameterize-the-instance }

Et maintenant, nous pouvons utiliser `__init__` pour déclarer les paramètres de l’instance, que nous utiliserons pour « paramétrer » la dépendance :

{* ../../docs_src/dependencies/tutorial011.py hl[9] *}

Dans ce cas, **FastAPI** n’accèdera pas à `__init__` et ne s’en souciera pas ; nous l’utiliserons directement dans notre code.

## Créer une instance { #create-an-instance }

Nous pouvons créer une instance de cette classe avec :

{* ../../docs_src/dependencies/tutorial011.py hl[18] *}

Et de cette façon, nous pouvons « paramétrer » notre dépendance, qui contient maintenant `"bar"`, en tant qu’attribut `checker.fixed_content`.

## Utiliser l'instance comme dépendance { #use-the-instance-as-a-dependency }

Ensuite, nous pourrions utiliser ce `checker` dans un `Depends(checker)`, au lieu de `Depends(FixedContentQueryChecker)`, car la dépendance est l’instance, `checker`, et non la classe elle‑même.

Et lors de la résolution de la dépendance, **FastAPI** appellera ce `checker` comme ceci :

```Python
checker(q="somequery")
```

... et passera ce que cela renvoie comme valeur de la dépendance à notre *fonction de chemin d'accès*, en tant que paramètre `fixed_content_included` :

{* ../../docs_src/dependencies/tutorial011.py hl[22] *}

/// tip | Astuce

Tout cela peut sembler artificiel. Et il n’est peut‑être pas encore très clair en quoi c’est utile.

Ces exemples sont volontairement simples, mais ils montrent comment tout cela fonctionne.

Dans les chapitres sur la sécurité, il existe des fonctions utilitaires implémentées de la même manière.

Si vous avez compris tout cela, vous savez déjà comment ces outils utilitaires pour la sécurité fonctionnent en interne.

///

## Limiter la concurrence des dépendances { #limit-dependency-concurrency }

Dans certains cas, vous pouvez souhaiter limiter le nombre de requêtes pouvant utiliser une dépendance en même temps.

Par exemple, votre base de données peut disposer d’un nombre limité de connexions. Vous pouvez faire attendre les nouvelles requêtes avant de créer une session, jusqu’à ce qu’une autre requête ait fini d’utiliser sa session.

Vous pouvez le faire avec `max_concurrency` dans `Depends()`.

Mettons à jour l’alias `SessionDep` du [tutoriel sur les bases de données SQL](../tutorial/sql-databases.md) :

```Python
SessionDep = Annotated[Session, Depends(get_session, max_concurrency=5)]
```

Désormais, jusqu’à **cinq requêtes** peuvent avoir une session de base de données ouverte via cette dépendance en même temps.

Si une autre requête a besoin d’une session, elle attend que l’une de ces sessions soit fermée.

Pendant cette attente, elle **n’occupe pas de thread de travail**, ce qui laisse ces threads disponibles pour exécuter d’autres parties du code.

La valeur doit être un entier strictement positif. La valeur par défaut est `None`, ce qui signifie que FastAPI ne limite pas le nombre d’exécutions simultanées de la dépendance.

### Partager la limite entre les routes { #share-the-limit-between-routes }

Toutes les routes de cet exemple utilisent le même alias `SessionDep`, elles partagent donc la limite de cinq sessions.

Pour partager une limite, réutilisez le **même objet `Depends()`**, par exemple dans un alias `Annotated` comme celui-ci.

Si vous écrivez un nouveau `Depends(get_session, max_concurrency=5)` pour chaque route, chacune aura sa propre limite de cinq. Cela reste vrai même si elles utilisent toutes la même fonction `get_session`.

Réutiliser le même `SessionDep` dans une autre application partage également la limite, tant que les deux applications s’exécutent dans la même boucle d’événements. Cela inclut les applications montées.

Par exemple, si deux applications utilisent ce `SessionDep` pour le même pool de connexions à la base de données, elles peuvent avoir à elles deux jusqu’à cinq sessions ouvertes via cette dépendance.

Si les applications utilisent des pools distincts et ont besoin de limites indépendantes, créez un objet `Depends()` distinct pour chaque application.

### Fermer la session avant d’en autoriser une autre { #close-the-session-before-allowing-another-one }

Dans cet exemple, `get_session` utilise `yield`. La session est comptabilisée dans la limite jusqu’à ce que le code d’arrêt ait fini de la fermer.

Le `scope` de la dépendance détermine quand ce code d’arrêt s’exécute :

* Avec `scope="request"`, la valeur par défaut, il s’exécute après l’envoi de la réponse.
* Avec `scope="function"`, il s’exécute après la fin de la *fonction de chemin d'accès*, avant l’envoi de la réponse.

Vous pouvez en lire davantage sur la [sortie anticipée et la portée](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope).

Pour une dépendance sans `yield`, l’appel est comptabilisé dans la limite uniquement jusqu’à la fin de la fonction.

Si vous utilisez une dépendance avec `yield` dans un gestionnaire WebSocket, elle est comptabilisée dans la limite jusqu’à la fin du gestionnaire et du code d’arrêt de la dépendance.

/// note | Remarque

Réutiliser une [valeur de dépendance mise en cache](../tutorial/dependencies/sub-dependencies.md#using-the-same-dependency-multiple-times) ne la comptabilise pas à nouveau dans la limite. Si différentes déclarations partagent cette valeur, seule la déclaration qui appelle la dépendance est comptabilisée dans sa limite.

///

### Choisir une limite pour votre application { #choose-a-limit-for-your-application }

Choisissez une limite adaptée au nombre de connexions à la base de données disponibles pour ces sessions.

Si d’autres parties de votre application utilisent également ces connexions, laissez-leur aussi de la marge. FastAPI ne connaît pas la taille de votre pool de connexions à la base de données.

Chaque processus worker a sa propre limite. Par exemple, deux processus workers utilisant cette dépendance peuvent avoir jusqu’à dix sessions ouvertes à eux deux.

/// note | Détails techniques

Les limites sont également distinctes pour chaque boucle d’événements. Les applications qui s’exécutent dans des boucles d’événements différentes ne partagent pas de limite, même si elles réutilisent le même objet `Depends()`.

///

### Dépendances nécessitant plusieurs ressources { #dependencies-that-need-more-than-one-resource }

FastAPI exécute les sous-dépendances d’une dépendance avant d’appliquer la limite de cette dépendance.

Ainsi, pour limiter les sessions de base de données, placez `max_concurrency` sur `Depends(get_session, ...)`, là où la session est créée.

Une requête peut se bloquer si elle a besoin d’une autre session alors qu’elle en conserve une qui ne sera fermée qu’à la fin de la requête.

Par exemple, imaginez un `Depends(get_session, max_concurrency=1, use_cache=False)` partagé, utilisé deux fois dans la même requête.

Le premier appel crée une session. Le second attend sa fermeture. Mais la première session ne peut pas être fermée avant la fin de la requête, et la requête attend le second appel.

Deux requêtes peuvent aussi se bloquer si l’une conserve une session en attendant une autre ressource, et que l’autre conserve cette ressource en attendant une session.

Si vos requêtes ont besoin de plusieurs ressources, acquérez-les dans le même ordre. FastAPI applique chaque limite séparément, il ne réserve pas à l’avance toutes les ressources dont une requête aura besoin.

## Dépendances avec `yield`, `HTTPException`, `except` et tâches d'arrière‑plan { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | Alertes

Vous n’avez très probablement pas besoin de ces détails techniques.

Ces détails sont utiles principalement si vous aviez une application FastAPI antérieure à la version 0.121.0 et que vous rencontrez des problèmes avec des dépendances utilisant `yield`.

///

Les dépendances avec `yield` ont évolué au fil du temps pour couvrir différents cas d’utilisation et corriger certains problèmes ; voici un résumé de ce qui a changé.

### Dépendances avec `yield` et `scope` { #dependencies-with-yield-and-scope }

Dans la version 0.121.0, FastAPI a ajouté la prise en charge de `Depends(scope="function")` pour les dépendances avec `yield`.

Avec `Depends(scope="function")`, le code d’arrêt après `yield` s’exécute immédiatement après la fin de la *fonction de chemin d'accès*, avant que la réponse ne soit renvoyée au client.

Et lorsque vous utilisez `Depends(scope="request")` (valeur par défaut), le code d’arrêt après `yield` s’exécute après l’envoi de la réponse.

Vous pouvez en lire davantage dans les documents pour [Dépendances avec `yield` - Sortie anticipée et `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope).

### Dépendances avec `yield` et `StreamingResponse`, Détails techniques { #dependencies-with-yield-and-streamingresponse-technical-details }

Avant FastAPI 0.118.0, si vous utilisiez une dépendance avec `yield`, elle exécutait le code d’arrêt après que la *fonction de chemin d'accès* a retourné, mais juste avant d’envoyer la réponse.

L’objectif était d’éviter de conserver des ressources plus longtemps que nécessaire pendant que la réponse transitait sur le réseau.

Ce changement impliquait aussi que si vous retourniez une `StreamingResponse`, le code d’arrêt de la dépendance avec `yield` aurait déjà été exécuté.

Par exemple, si vous aviez une session de base de données dans une dépendance avec `yield`, la `StreamingResponse` ne pourrait pas utiliser cette session pendant le streaming des données, car la session aurait déjà été fermée dans le code d’arrêt après `yield`.

Ce comportement a été annulé en 0.118.0, afin que le code d’arrêt après `yield` s’exécute après l’envoi de la réponse.

/// note | Remarque

Comme vous le verrez ci‑dessous, c’est très similaire au comportement avant la version 0.106.0, mais avec plusieurs améliorations et corrections de bogues pour des cas limites.

///

#### Cas d’utilisation avec sortie anticipée du code { #use-cases-with-early-exit-code }

Il existe certains cas d’utilisation avec des conditions spécifiques qui pourraient bénéficier de l’ancien comportement, où le code d’arrêt des dépendances avec `yield` s’exécute avant l’envoi de la réponse.

Par exemple, imaginez que vous ayez du code qui utilise une session de base de données dans une dépendance avec `yield` uniquement pour vérifier un utilisateur, mais que la session de base de données ne soit plus jamais utilisée dans la *fonction de chemin d'accès*, seulement dans la dépendance, **et** que la réponse mette longtemps à être envoyée, comme une `StreamingResponse` qui envoie les données lentement mais qui, pour une raison quelconque, n’utilise pas la base de données.

Dans ce cas, la session de base de données serait conservée jusqu’à la fin de l’envoi de la réponse, mais si vous ne l’utilisez pas, il ne serait pas nécessaire de la conserver.

Voici à quoi cela pourrait ressembler :

{* ../../docs_src/dependencies/tutorial013.py *}

Le code d’arrêt, la fermeture automatique de la `Session` dans :

{* ../../docs_src/dependencies/tutorial013.py ln[19:21] *}

... serait exécuté après que la réponse a fini d’envoyer les données lentes :

{* ../../docs_src/dependencies/tutorial013.py ln[30:38] hl[31:33] *}

Mais comme `generate_stream()` n’utilise pas la session de base de données, il n’est pas vraiment nécessaire de garder la session ouverte pendant l’envoi de la réponse.

Si vous avez ce cas d’utilisation spécifique avec SQLModel (ou SQLAlchemy), vous pouvez fermer explicitement la session dès que vous n’en avez plus besoin :

{* ../../docs_src/dependencies/tutorial014.py ln[24:28] hl[28] *}

De cette manière, la session libérera la connexion à la base de données, afin que d’autres requêtes puissent l’utiliser.

Si vous avez un autre cas d’utilisation qui nécessite une sortie anticipée depuis une dépendance avec `yield`, veuillez créer une [Question de discussion GitHub](https://github.com/fastapi/fastapi/discussions/new?category=questions) avec votre cas spécifique et pourquoi vous bénéficieriez d’une fermeture anticipée pour les dépendances avec `yield`.

S’il existe des cas d’utilisation convaincants pour une fermeture anticipée dans les dépendances avec `yield`, j’envisagerai d’ajouter une nouvelle façon d’y opter.

### Dépendances avec `yield` et `except`, Détails techniques { #dependencies-with-yield-and-except-technical-details }

Avant FastAPI 0.110.0, si vous utilisiez une dépendance avec `yield`, puis capturiez une exception avec `except` dans cette dépendance, et que vous ne relanciez pas l’exception, l’exception était automatiquement levée/transmise à tout gestionnaire d’exceptions ou au gestionnaire d’erreur interne du serveur.

Cela a été modifié dans la version 0.110.0 pour corriger une consommation de mémoire non gérée due aux exceptions transmises sans gestionnaire (erreurs internes du serveur), et pour rendre le comportement cohérent avec celui du code Python classique.

### Tâches d'arrière‑plan et dépendances avec `yield`, Détails techniques { #background-tasks-and-dependencies-with-yield-technical-details }

Avant FastAPI 0.106.0, lever des exceptions après `yield` n’était pas possible, le code d’arrêt dans les dépendances avec `yield` s’exécutait *après* l’envoi de la réponse, donc les [Gestionnaires d'exceptions](../tutorial/handling-errors.md#install-custom-exception-handlers) avaient déjà été exécutés.

Cela avait été conçu ainsi principalement pour permettre d’utiliser les mêmes objets « générés par yield » par les dépendances à l’intérieur de tâches d’arrière‑plan, car le code d’arrêt s’exécutait après la fin des tâches d’arrière‑plan.

Cela a été modifié dans FastAPI 0.106.0 afin de ne pas conserver des ressources pendant l’attente de la transmission de la réponse sur le réseau.

/// tip | Astuce

De plus, une tâche d’arrière‑plan est normalement un ensemble de logique indépendant qui devrait être géré séparément, avec ses propres ressources (par ex. sa propre connexion à la base de données).

Ainsi, vous aurez probablement un code plus propre.

///

Si vous comptiez sur ce comportement, vous devez désormais créer les ressources pour les tâches d’arrière‑plan à l’intérieur de la tâche elle‑même, et n’utiliser en interne que des données qui ne dépendent pas des ressources des dépendances avec `yield`.

Par exemple, au lieu d’utiliser la même session de base de données, vous créeriez une nouvelle session de base de données à l’intérieur de la tâche d’arrière‑plan, et vous obtiendriez les objets depuis la base de données en utilisant cette nouvelle session. Puis, au lieu de passer l’objet obtenu depuis la base de données en paramètre à la fonction de tâche d’arrière‑plan, vous passeriez l’identifiant (ID) de cet objet et vous obtiendriez à nouveau l’objet à l’intérieur de la fonction de la tâche d’arrière‑plan.
