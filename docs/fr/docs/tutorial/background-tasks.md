# Tâches d'arrière-plan { #background-tasks }

Vous pouvez définir des tâches d'arrière-plan à exécuter *après* avoir renvoyé une réponse.

Ceci est utile pour les opérations qui doivent avoir lieu après une requête, mais pour lesquelles le client n'a pas réellement besoin d'attendre que l'opération se termine avant de recevoir la réponse.

Cela comprend, par exemple :

* Les notifications par email envoyées après l'exécution d'une action :
    * Comme se connecter à un serveur email et envoyer un email a tendance à être « lent » (plusieurs secondes), vous pouvez renvoyer la réponse immédiatement et envoyer la notification par email en arrière-plan.
* Le traitement de données :
    * Par exemple, disons que vous recevez un fichier qui doit passer par un traitement lent, vous pouvez renvoyer une réponse « Accepted » (HTTP 202) et traiter le fichier en arrière-plan.

## Utiliser `BackgroundTasks` { #using-backgroundtasks }

Pour commencer, importez `BackgroundTasks` et définissez un paramètre dans votre *fonction de chemin d'accès* avec une déclaration de type `BackgroundTasks` :

{* ../../docs_src/background_tasks/tutorial001_py39.py hl[1,13] *}

**FastAPI** créera l'objet de type `BackgroundTasks` pour vous et le passera comme paramètre.

## Créer une fonction de tâche { #create-a-task-function }

Créez une fonction à exécuter comme tâche d'arrière-plan.

C'est simplement une fonction standard qui peut recevoir des paramètres.

Elle peut être une fonction `async def` ou une fonction `def` normale, **FastAPI** saura la gérer correctement.

Dans ce cas, la fonction de tâche écrira dans un fichier (en simulant l'envoi d'un email).

Et comme l'opération d'écriture n'utilise pas `async` et `await`, nous définissons la fonction avec un `def` normal :

{* ../../docs_src/background_tasks/tutorial001_py39.py hl[6:9] *}

## Ajouter la tâche d'arrière-plan { #add-the-background-task }

À l'intérieur de votre *fonction de chemin d'accès*, passez votre fonction de tâche à l'objet de type *background tasks* avec la méthode `.add_task()` :

{* ../../docs_src/background_tasks/tutorial001_py39.py hl[14] *}

`.add_task()` reçoit comme arguments :

* Une fonction de tâche à exécuter en arrière-plan (`write_notification`).
* N'importe quelle séquence d'arguments qui doit être passée à la fonction de tâche dans l'ordre (`email`).
* N'importe quels arguments nommés qui doivent être passés à la fonction de tâche (`message="some notification"`).

## Injection de dépendances { #dependency-injection }

Utiliser `BackgroundTasks` fonctionne aussi avec le système d'injection de dépendances, vous pouvez déclarer un paramètre de type `BackgroundTasks` à plusieurs niveaux : dans une *fonction de chemin d'accès*, dans une dépendance (dependable), dans une sous-dépendance, etc.

**FastAPI** sait quoi faire dans chaque cas et comment réutiliser le même objet, de sorte que toutes les tâches d'arrière-plan sont fusionnées et exécutées ensuite en arrière-plan :


{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13,15,22,25] *}


Dans cet exemple, les messages seront écrits dans le fichier `log.txt` *après* que la réponse est envoyée.

S'il y avait une query dans la requête, elle sera écrite dans le log via une tâche d'arrière-plan.

Et ensuite une autre tâche d'arrière-plan générée au niveau de la *fonction de chemin d'accès* écrira un message en utilisant le paramètre de chemin `email`.

## Détails techniques { #technical-details }

La classe `BackgroundTasks` provient directement de <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">`starlette.background`</a>.

Elle est importée/incluse directement dans FastAPI afin que vous puissiez l'importer depuis `fastapi` et éviter d'importer accidentellement l'alternative `BackgroundTask` (sans le `s` à la fin) depuis `starlette.background`.

En utilisant uniquement `BackgroundTasks` (et non `BackgroundTask`), il est alors possible de l'utiliser comme paramètre de *fonction de chemin d'accès* et de laisser **FastAPI** gérer le reste pour vous, comme lorsque vous utilisez directement l'objet `Request`.

Il est toujours possible d'utiliser `BackgroundTask` seul dans FastAPI, mais vous devez créer l'objet dans votre code et renvoyer une `Response` Starlette l'incluant.

Vous pouvez voir plus de détails dans <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">la documentation officielle de Starlette sur les Background Tasks</a>.

## Mise en garde { #caveat }

Si vous devez effectuer des calculs lourds en arrière-plan et que vous n'avez pas nécessairement besoin qu'ils soient exécutés par le même process (par exemple, vous n'avez pas besoin de partager la mémoire, les variables, etc.), vous pouvez tirer bénéfice d'utiliser d'autres outils plus importants comme <a href="https://docs.celeryq.dev" class="external-link" target="_blank">Celery</a>.

Ils ont tendance à nécessiter des configurations plus complexes, un gestionnaire de file de messages/tâches, comme RabbitMQ ou Redis, mais ils vous permettent d'exécuter des tâches d'arrière-plan dans plusieurs process, et surtout, sur plusieurs serveurs.

Mais si vous devez accéder à des variables et objets de la même app **FastAPI**, ou si vous devez effectuer de petites tâches d'arrière-plan (comme envoyer une notification par email), vous pouvez simplement utiliser `BackgroundTasks`.

## Résumé { #recap }

Importez et utilisez `BackgroundTasks` avec des paramètres dans les *fonctions de chemin d'accès* et les dépendances pour ajouter des tâches d'arrière-plan.
