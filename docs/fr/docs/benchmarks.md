# Tests de performance { #benchmarks }

Des tests de performance indépendants de TechEmpower montrent que les applications **FastAPI** exécutées sous Uvicorn sont <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">parmi les frameworks Python les plus rapides disponibles</a>, seulement derrière Starlette et Uvicorn eux‑mêmes (tous deux utilisés en interne par FastAPI).

Mais lorsque vous examinez les tests de performance et les comparaisons, vous devez garder les points suivants à l'esprit.

## Tests de performance et rapidité { #benchmarks-and-speed }

Lorsque vous vérifiez les tests de performance, il est courant de voir plusieurs outils de types différents comparés comme équivalents.

En particulier, on voit Uvicorn, Starlette et FastAPI comparés ensemble (parmi de nombreux autres outils).

Plus le problème résolu par l’outil est simple, meilleures seront ses performances. Et la plupart des tests de performance ne testent pas les fonctionnalités additionnelles fournies par l’outil.

La hiérarchie est la suivante :

* **Uvicorn** : un serveur ASGI
    * **Starlette** : (utilise Uvicorn) un microframework web
        * **FastAPI** : (utilise Starlette) un microframework d’API avec plusieurs fonctionnalités supplémentaires pour créer des API, notamment la validation des données, etc.

* **Uvicorn** :
    * Aura la meilleure performance, car il n’a pas beaucoup de code supplémentaire en dehors du serveur lui‑même.
    * Vous n’écririez pas une application directement avec Uvicorn. Cela signifierait que votre code devrait inclure, plus ou moins, au minimum, tout le code fourni par Starlette (ou **FastAPI**). Et si vous faisiez cela, votre application finale aurait la même surcharge que si vous aviez utilisé un framework, tout en minimisant le code de votre application et les bugs.
    * Si vous comparez Uvicorn, comparez‑le à Daphne, Hypercorn, uWSGI, etc. Des serveurs d’applications.
* **Starlette** :
    * Aura la deuxième meilleure performance, après Uvicorn. En fait, Starlette utilise Uvicorn pour s’exécuter. Donc, il ne peut probablement être que «plus lent» qu’Uvicorn, puisqu’il doit exécuter plus de code.
    * Mais il fournit les outils pour construire des applications web simples, avec un routage basé sur les chemins, etc.
    * Si vous comparez Starlette, comparez‑le à Sanic, Flask, Django, etc. Des frameworks web (ou microframeworks).
* **FastAPI** :
    * De la même manière que Starlette utilise Uvicorn et ne peut pas être plus rapide que lui, **FastAPI** utilise Starlette, il ne peut donc pas être plus rapide que lui.
    * FastAPI apporte davantage de fonctionnalités au‑dessus de Starlette. Des fonctionnalités dont vous avez presque toujours besoin lors de la création d’API, comme la validation des données et la sérialisation. Et en l’utilisant, vous obtenez gratuitement une documentation automatique (la documentation automatique n’ajoute même pas de surcharge aux applications en cours d’exécution, elle est générée au démarrage).
    * Si vous n’utilisiez pas FastAPI et utilisiez directement Starlette (ou un autre outil, comme Sanic, Flask, Responder, etc.), vous devriez implémenter vous‑même toute la validation et la sérialisation des données. Ainsi, votre application finale aurait tout de même la même surcharge que si elle avait été construite avec FastAPI. Et, dans de nombreux cas, cette validation et cette sérialisation des données représentent la plus grande quantité de code écrite dans les applications.
    * Donc, en utilisant FastAPI, vous gagnez du temps de développement, réduisez les bugs, diminuez le nombre de lignes de code, et vous obtiendrez probablement les mêmes performances (ou de meilleures) que si vous ne l’utilisiez pas (car vous auriez à tout implémenter dans votre code).
    * Si vous comparez FastAPI, comparez‑le à un framework (ou un ensemble d’outils) d’applications web qui fournit la validation des données, la sérialisation et la documentation, comme Flask‑apispec, NestJS, Molten, etc. Des frameworks avec validation des données, sérialisation et documentation automatiques intégrées.
