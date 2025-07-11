# À propos des versions de FastAPI

**FastAPI** est déjà utilisé en production dans de nombreuses applications et systèmes. Et la couverture de test est maintenue à 100 %. Mais son développement est toujours aussi rapide.

De nouvelles fonctionnalités sont ajoutées fréquemment, des bogues sont corrigés régulièrement et le code est
amélioré continuellement.

C'est pourquoi les versions actuelles sont toujours `0.x.x`, cela reflète que chaque version peut potentiellement
recevoir des changements non rétrocompatibles. Cela suit les conventions de <a href="https://semver.org/" class="external-link"
target="_blank">versionnage sémantique</a>.

Vous pouvez créer des applications de production avec **FastAPI** dès maintenant (et vous le faites probablement depuis un certain temps), vous devez juste vous assurer que vous utilisez une version qui fonctionne correctement avec le reste de votre code.

## Épinglez votre version de `fastapi`

Tout d'abord il faut "épingler" la version de **FastAPI** que vous utilisez à la dernière version dont vous savez
qu'elle fonctionne correctement pour votre application.

Par exemple, disons que vous utilisez la version `0.45.0` dans votre application.

Si vous utilisez un fichier `requirements.txt`, vous pouvez spécifier la version avec :

```txt
fastapi==0.45.0
```

ce qui signifierait que vous utiliseriez exactement la version `0.45.0`.

Ou vous pourriez aussi l'épingler avec :

```txt
fastapi>=0.45.0,<0.46.0
```

cela signifierait que vous utiliseriez les versions `0.45.0` ou supérieures, mais inférieures à `0.46.0`, par exemple, une version `0.45.2` serait toujours acceptée.

Si vous utilisez un autre outil pour gérer vos installations, comme Poetry, Pipenv, ou autres, ils ont tous un moyen que vous pouvez utiliser pour définir des versions spécifiques pour vos paquets.

## Versions disponibles

Vous pouvez consulter les versions disponibles (par exemple, pour vérifier quelle est la dernière version en date) dans les [Notes de version](../release-notes.md){.internal-link target=_blank}.

## À propos des versions

Suivant les conventions de versionnage sémantique, toute version inférieure à `1.0.0` peut potentiellement ajouter
des changements non rétrocompatibles.

FastAPI suit également la convention que tout changement de version "PATCH" est pour des corrections de bogues et
des changements rétrocompatibles.

/// tip | Astuce

Le "PATCH" est le dernier chiffre, par exemple, dans `0.2.3`, la version PATCH est `3`.

///

Donc, vous devriez être capable d'épingler une version comme suit :

```txt
fastapi>=0.45.0,<0.46.0
```

Les changements non rétrocompatibles et les nouvelles fonctionnalités sont ajoutés dans les versions "MINOR".

/// tip | Astuce

Le "MINOR" est le numéro au milieu, par exemple, dans `0.2.3`, la version MINOR est `2`.

///

## Mise à jour des versions FastAPI

Vous devriez tester votre application.

Avec **FastAPI** c'est très facile (merci à Starlette), consultez la documentation : [Testing](../tutorial/testing.md){.internal-link target=_blank}

Après avoir effectué des tests, vous pouvez mettre à jour la version **FastAPI** vers une version plus récente, et vous assurer que tout votre code fonctionne correctement en exécutant vos tests.

Si tout fonctionne, ou après avoir fait les changements nécessaires, et que tous vos tests passent, vous pouvez
épingler votre version de `fastapi` à cette nouvelle version récente.

## À propos de Starlette

Vous ne devriez pas épingler la version de `starlette`.

Différentes versions de **FastAPI** utiliseront une version spécifique plus récente de Starlette.

Ainsi, vous pouvez simplement laisser **FastAPI** utiliser la bonne version de Starlette.

## À propos de Pydantic

Pydantic inclut des tests pour **FastAPI** avec ses propres tests, ainsi les nouvelles versions de Pydantic (au-dessus
de `1.0.0`) sont toujours compatibles avec **FastAPI**.

Vous pouvez épingler Pydantic à toute version supérieure à `1.0.0` qui fonctionne pour vous et inférieure à `2.0.0`.

Par exemple :

```txt
pydantic>=1.2.0,<2.0.0
```
