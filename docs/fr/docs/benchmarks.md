# Test de performance

Les tests de performance de TechEmpower montrent que les applications **FastAPI** tournant sous Uvicorn comme <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">étant l'un des frameworks Python les plus rapides disponibles</a>, seulement inférieur à Starlette et Uvicorn (tous deux utilisés au cœur de FastAPI). (*)

Mais en prêtant attention aux tests de performance et aux comparaisons, il faut tenir compte de ce qu'il suit.

## Tests de performance et rapidité

Lorsque vous vérifiez les tests de performance, il est commun de voir plusieurs outils de différents types comparés comme équivalents.

En particulier, on voit Uvicorn, Starlette et FastAPI comparés (parmi de nombreux autres outils).

Plus le problème résolu par un outil est simple, mieux seront les performances obtenues. Et la plupart des tests de performance ne prennent pas en compte les fonctionnalités additionnelles fournies par les outils.

La hiérarchie est la suivante :

* **Uvicorn** : un serveur ASGI
    * **Starlette** : (utilise Uvicorn) un micro-framework web
        * **FastAPI**: (utilise Starlette) un micro-framework pour API disposant de fonctionnalités additionnelles pour la création d'API, avec la validation des données, etc.

* **Uvicorn** :
    * A les meilleures performances, étant donné qu'il n'a pas beaucoup de code mis-à-part le serveur en lui-même.
    * On n'écrit pas une application avec uniquement Uvicorn. Cela signifie que le code devrait inclure plus ou moins, au minimum, tout le code offert par Starlette (ou **FastAPI**). Et si on fait cela, l'application finale apportera les mêmes complications que si on avait utilisé un framework et que l'on avait minimisé la quantité de code et de bugs.
    * Si on compare Uvicorn, il faut le comparer à d'autre applications de serveurs comme Daphne, Hypercorn, uWSGI, etc.
* **Starlette** :
    * A les seconde meilleures performances après Uvicorn. Starlette utilise en réalité Uvicorn. De ce fait, il ne peut qu’être plus "lent" qu'Uvicorn car il requiert l'exécution de plus de code.
    * Cependant il nous apporte les outils pour construire une application web simple, avec un routage basé sur des chemins, etc.
    * Si on compare Starlette, il faut le comparer à d'autres frameworks web (ou micorframework) comme Sanic, Flask, Django, etc.
* **FastAPI** :
    * Comme Starlette, FastAPI utilise Uvicorn et ne peut donc pas être plus rapide que ce dernier.
    * FastAPI apporte des fonctionnalités supplémentaires à Starlette. Des fonctionnalités qui sont nécessaires presque systématiquement lors de la création d'une API, comme la validation des données, la sérialisation. En utilisant FastAPI, on obtient une documentation automatiquement (qui ne requiert aucune manipulation pour être mise en place).
    * Si on n'utilisait pas FastAPI mais directement Starlette (ou un outil équivalent comme Sanic, Flask, Responder, etc) il faudrait implémenter la validation des données et la sérialisation par nous-même. Le résultat serait donc le même dans les deux cas mais du travail supplémentaire serait à réaliser avec Starlette, surtout en considérant que la validation des données et la sérialisation représentent la plus grande quantité de code à écrire dans une application.
    * De ce fait, en utilisant FastAPI on minimise le temps de développement, les bugs, le nombre de lignes de code, et on obtient les mêmes performances (si ce n'est de meilleurs performances) que l'on aurait pu avoir sans ce framework (en ayant à implémenter de nombreuses fonctionnalités importantes par nous-mêmes).
    * Si on compare FastAPI, il faut le comparer à d'autres frameworks web (ou ensemble d'outils) qui fournissent la validation des données, la sérialisation et la documentation, comme Flask-apispec, NestJS, Molten, etc.
