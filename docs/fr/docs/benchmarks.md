# Benchmarks { #benchmarks }

Les benchmarks indépendants de TechEmpower montrent que les applications **FastAPI** exécutées avec Uvicorn sont <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">l’un des frameworks Python les plus rapides disponibles</a>, juste en dessous de Starlette et Uvicorn eux-mêmes (utilisés en interne par FastAPI).

Mais lorsque vous consultez des benchmarks et des comparaisons, vous devez garder ce qui suit à l’esprit.

## Benchmarks et vitesse { #benchmarks-and-speed }

Lorsque vous consultez les benchmarks, il est courant de voir plusieurs outils de types différents comparés comme s’ils étaient équivalents.

En particulier, de voir Uvicorn, Starlette et FastAPI comparés ensemble (parmi de nombreux autres outils).

Plus le problème résolu par l’outil est simple, meilleures seront les performances qu’il obtiendra. Et la plupart des benchmarks ne testent pas les fonctionnalités supplémentaires fournies par l’outil.

La hiérarchie est la suivante :

* **Uvicorn** : un serveur ASGI
    * **Starlette** : (utilise Uvicorn) un microframework web
        * **FastAPI** : (utilise Starlette) un microframework d’API avec plusieurs fonctionnalités supplémentaires pour construire des API, avec la validation des données, etc.

* **Uvicorn** :
    * Aura les meilleures performances, car il n’a pas beaucoup de code supplémentaire en dehors du serveur lui-même.
    * Vous n’écririez pas une application directement en Uvicorn. Cela signifierait que votre code devrait inclure plus ou moins, au minimum, tout le code fourni par Starlette (ou **FastAPI**). Et si vous faisiez cela, votre application finale aurait la même surcharge que si vous aviez utilisé un framework, tout en minimisant le code de votre application et les bugs.
    * Si vous comparez Uvicorn, comparez-le à Daphne, Hypercorn, uWSGI, etc. Des serveurs d’applications.
* **Starlette** :
    * Aura les performances suivantes, après Uvicorn. En fait, Starlette utilise Uvicorn pour s’exécuter. Donc, il ne peut probablement que devenir « plus lent » qu’Uvicorn, en devant exécuter plus de code.
    * Mais il vous fournit les outils pour construire des applications web simples, avec du routage basé sur des chemins, etc.
    * Si vous comparez Starlette, comparez-le à Sanic, Flask, Django, etc. Des frameworks web (ou microframeworks).
* **FastAPI** :
    * De la même manière que Starlette utilise Uvicorn et ne peut pas être plus rapide que lui, **FastAPI** utilise Starlette, donc il ne peut pas être plus rapide que lui.
    * FastAPI fournit plus de fonctionnalités par-dessus Starlette. Des fonctionnalités dont vous avez presque toujours besoin lorsque vous construisez des API, comme la validation des données et la sérialisation. Et en l’utilisant, vous obtenez de la documentation automatique gratuitement (la documentation automatique n’ajoute même pas de surcharge à l’exécution des applications, elle est générée au démarrage).
    * Si vous n’utilisiez pas FastAPI et utilisiez Starlette directement (ou un autre outil, comme Sanic, Flask, Responder, etc.), vous devriez implémenter vous-même toute la validation des données et la sérialisation. Ainsi, votre application finale aurait toujours la même surcharge que si elle avait été construite en utilisant FastAPI. Et dans de nombreux cas, cette validation des données et cette sérialisation représentent la plus grande quantité de code écrite dans les applications.
    * Ainsi, en utilisant FastAPI, vous économisez du temps de développement, des bugs, des lignes de code, et vous obtiendriez probablement les mêmes performances (ou de meilleures) que si vous ne l’utilisiez pas (puisque vous devriez tout implémenter dans votre code).
    * Si vous comparez FastAPI, comparez-le à un framework d’application web (ou à un ensemble d’outils) qui fournit la validation des données, la sérialisation et la documentation, comme Flask-apispec, NestJS, Molten, etc. Des frameworks avec validation automatique intégrée des données, sérialisation et documentation.
