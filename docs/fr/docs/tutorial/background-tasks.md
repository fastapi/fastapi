# Tâches d'arrière-plan { #background-tasks }

Vous pouvez définir des tâches d'arrière-plan qui seront exécutées après avoir retourné une réponse.

Ceci est utile pour les opérations qui doivent avoir lieu après une requête, mais où le client n'a pas vraiment à attendre que l'opération soit terminée pour recevoir la réponse.

Cela comprend, par exemple :

* Les notifications par email envoyées après l'exécution d'une action :
    * Étant donné que se connecter à un serveur email et envoyer un email a tendance à être «lent» (plusieurs secondes), vous pouvez retourner la réponse directement et envoyer la notification par email en arrière-plan.
* Traiter des données :
    * Par exemple, disons que vous recevez un fichier qui doit passer par un processus lent, vous pouvez retourner une réponse «Accepted» (HTTP 202) et traiter le fichier en arrière-plan.

## Utiliser `BackgroundTasks` { #using-backgroundtasks }

Pour commencer, importez `BackgroundTasks` et définissez un paramètre dans votre *fonction de chemin* avec `BackgroundTasks` comme type déclaré :

{* ../../docs_src/background_tasks/tutorial001_py39.py hl[1,13] *}

**FastAPI** créera l'objet de type `BackgroundTasks` pour vous et le passera comme paramètre.

## Créer une fonction de tâche { #create-a-task-function }

Créez une fonction à exécuter comme tâche d'arrière-plan.

C'est simplement une fonction standard qui peut recevoir des paramètres.

Elle peut être une fonction asynchrone (`async def`) ou une fonction normale (`def`), **FastAPI** saura la gérer correctement.

Dans cet exemple, la fonction de tâche écrira dans un fichier (afin de simuler un envoi d'email).

Et comme l'opération d'écriture n'utilise ni `async` ni `await`, nous définissons la fonction avec un `def` normal :

{* ../../docs_src/background_tasks/tutorial001_py39.py hl[6:9] *}

## Ajouter la tâche d'arrière-plan { #add-the-background-task }

Dans votre *fonction de chemin*, passez votre fonction de tâche à l'objet de tâches d'arrière-plan grâce à la méthode `.add_task()` :

{* ../../docs_src/background_tasks/tutorial001_py39.py hl[14] *}

`.add_task()` reçoit comme arguments :

* Une fonction de tâche à exécuter en arrière-plan (`write_notification`).
* Toute séquence d'arguments à passer à la fonction de tâche dans l'ordre (`email`).
* Tous les arguments nommés à passer à la fonction de tâche (`message="some notification"`).

## Injection de dépendances { #dependency-injection }

Utiliser `BackgroundTasks` fonctionne aussi avec le système d'injection de dépendances, vous pouvez déclarer un paramètre de type `BackgroundTasks` à plusieurs niveaux : dans une *fonction de chemin*, dans une dépendance (dependable), dans une sous-dépendance, etc.

**FastAPI** sait quoi faire dans chaque cas et comment réutiliser le même objet, afin que toutes les tâches d'arrière-plan soient fusionnées et exécutées ensuite en arrière-plan :


{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13,15,22,25] *}


Dans cet exemple, les messages seront écrits dans le fichier `log.txt` après que la réponse soit envoyée.

S'il y avait un paramètre de requête dans la requête, il sera écrit dans le log via une tâche d'arrière-plan.

Ensuite, une autre tâche d'arrière-plan générée dans la *fonction de chemin* écrira un message utilisant le paramètre de chemin `email`.

## Détails techniques { #technical-details }

La classe `BackgroundTasks` provient directement de <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">`starlette.background`</a>.

Elle est importée/incluse directement dans FastAPI afin que vous puissiez l'importer depuis `fastapi` et éviter d'importer par accident l'alternative `BackgroundTask` (sans le `s` final) depuis `starlette.background`.

En utilisant seulement `BackgroundTasks` (et non `BackgroundTask`), il est possible de l'utiliser en tant que paramètre de *fonction de chemin* et de laisser **FastAPI** gérer le reste pour vous, comme lorsque vous utilisez l'objet `Request` directement.

Il est toujours possible d'utiliser `BackgroundTask` seul dans FastAPI, mais vous devez créer l'objet dans votre code et renvoyer une `Response` Starlette qui l'inclut.

Vous pouvez voir plus de détails dans <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">la documentation officielle de Starlette sur les tâches d'arrière-plan</a>.

## Avertissement { #caveat }

Si vous avez besoin d'effectuer des calculs lourds en arrière-plan et que vous n'avez pas nécessairement besoin qu'ils soient exécutés par le même processus (par exemple, vous n'avez pas besoin de partager la mémoire, les variables, etc.), vous pourriez bénéficier d'utiliser des outils plus importants comme <a href="https://docs.celeryq.dev" class="external-link" target="_blank">Celery</a>.

Ils nécessitent généralement des configurations plus complexes, un gestionnaire de file de messages/jobs, comme RabbitMQ ou Redis, mais ils permettent d'exécuter des tâches d'arrière-plan dans plusieurs processus, et surtout, sur plusieurs serveurs.

Mais si vous avez besoin d'accéder aux variables et objets de la même application **FastAPI**, ou si vous avez besoin d'effectuer de petites tâches d'arrière-plan (comme envoyer une notification par email), vous pouvez simplement utiliser `BackgroundTasks`.

## Résumé { #recap }

Importez et utilisez `BackgroundTasks` avec des paramètres dans les *fonctions de chemin* et les dépendances pour ajouter des tâches d'arrière-plan.
