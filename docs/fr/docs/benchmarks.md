# Tests de performance { #benchmarks }

Les benchmarks indépendants de TechEmpower montrent que les applications **FastAPI** s’exécutant avec Uvicorn sont <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">parmi les frameworks Python les plus rapides disponibles</a>, seulement en dessous de Starlette et Uvicorn eux‑mêmes (tous deux utilisés en interne par FastAPI).

Mais en prêtant attention aux tests de performance et aux comparaisons, vous devez tenir compte de ce qui suit.

## Tests de performance et rapidité { #benchmarks-and-speed }

Lorsque vous vérifiez les tests de performance, il est commun de voir plusieurs outils de différents types comparés comme équivalents.

En particulier, on voit Uvicorn, Starlette et FastAPI comparés (parmi de nombreux autres outils).

Plus le problème résolu par un outil est simple, meilleures seront les performances obtenues. Et la plupart des tests de performance ne prennent pas en compte les fonctionnalités additionnelles fournies par les outils.

La hiérarchie est la suivante :

* **Uvicorn** : un serveur ASGI
    * **Starlette** : (utilise Uvicorn) un microframework web
        * **FastAPI**: (utilise Starlette) un microframework pour API disposant de fonctionnalités additionnelles pour la création d'API, avec la validation des données, etc.

* **Uvicorn** :
    * A les meilleures performances, étant donné qu'il n'a pas beaucoup de code mis à part le serveur en lui‑même.
    * On n'écrit pas une application directement avec Uvicorn. Cela signifie que le code devrait inclure, au minimum, plus ou moins tout le code offert par Starlette (ou **FastAPI**). Et si on fait cela, l'application finale aura la même surcharge que si on avait utilisé un framework, tout en minimisant la quantité de code et les bugs.
    * Si on compare Uvicorn, il faut le comparer à d'autres serveurs d'applications comme Daphne, Hypercorn, uWSGI, etc.
* **Starlette** :
    * A les secondes meilleures performances après Uvicorn. En réalité, Starlette utilise Uvicorn. De ce fait, il ne peut qu’être plus « lent » qu'Uvicorn car il requiert l'exécution de plus de code.
    * Cependant, il apporte les outils pour construire une application web simple, avec un routage basé sur des chemins, etc.
    * Si on compare Starlette, il faut le comparer à d'autres frameworks web (ou microframeworks) comme Sanic, Flask, Django, etc.
* **FastAPI** :
    * Comme Starlette utilise Uvicorn et ne peut donc pas être plus rapide que lui, **FastAPI** utilise Starlette et ne peut donc pas être plus rapide que lui.
    * FastAPI apporte des fonctionnalités supplémentaires à Starlette. Des fonctionnalités dont vous avez presque toujours besoin lors de la création d'une API, comme la validation des données et la sérialisation. En l'utilisant, vous obtenez une documentation automatique « gratuitement » (la documentation automatique n'ajoute même pas de surcharge à l’exécution, elle est générée au démarrage).
    * Si on n'utilisait pas FastAPI mais directement Starlette (ou un autre outil comme Sanic, Flask, Responder, etc.), il faudrait implémenter toute la validation des données et la sérialisation soi‑même. L'application finale aurait donc la même surcharge que si elle avait été construite avec FastAPI. Et dans de nombreux cas, cette validation des données et cette sérialisation représentent la plus grande quantité de code écrite dans les applications.
    * De ce fait, en utilisant FastAPI on minimise le temps de développement, les bugs, le nombre de lignes de code, et on obtient probablement les mêmes performances (voire de meilleures performances) que l'on aurait pu avoir sans ce framework (car il aurait fallu tout implémenter dans votre code).
    * Si on compare FastAPI, il faut le comparer à d'autres frameworks d’application web (ou ensembles d'outils) qui fournissent la validation des données, la sérialisation et la documentation, comme Flask-apispec, NestJS, Molten, etc. Des frameworks avec validation des données, sérialisation et documentation automatiques intégrées.
