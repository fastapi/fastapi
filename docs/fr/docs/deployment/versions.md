# À propos des versions de FastAPI { #about-fastapi-versions }

**FastAPI** est déjà utilisé en production dans de nombreuses applications et de nombreux systèmes. Et la couverture de tests est maintenue à 100 %. Mais son développement avance toujours rapidement.

De nouvelles fonctionnalités sont ajoutées fréquemment, des bogues sont corrigés régulièrement et le code s'améliore continuellement.

C'est pourquoi les versions actuelles sont toujours `0.x.x`, cela reflète que chaque version pourrait potentiellement comporter des changements non rétrocompatibles. Cela suit les conventions de <a href="https://semver.org/" class="external-link" target="_blank">versionnage sémantique</a>.

Vous pouvez créer des applications de production avec **FastAPI** dès maintenant (et vous le faites probablement depuis un certain temps), vous devez juste vous assurer que vous utilisez une version qui fonctionne correctement avec le reste de votre code.

## Épingler votre version de `fastapi` { #pin-your-fastapi-version }

La première chose que vous devez faire est « épingler » la version de **FastAPI** que vous utilisez à la dernière version spécifique dont vous savez qu’elle fonctionne correctement pour votre application.

Par exemple, disons que vous utilisez la version `0.112.0` dans votre application.

Si vous utilisez un fichier `requirements.txt`, vous pouvez spécifier la version avec :

```txt
fastapi[standard]==0.112.0
```

ce qui signifierait que vous utiliseriez exactement la version `0.112.0`.

Ou vous pourriez aussi l'épingler avec :

```txt
fastapi[standard]>=0.112.0,<0.113.0
```

cela signifierait que vous utiliseriez les versions `0.112.0` ou supérieures, mais inférieures à `0.113.0`, par exemple, une version `0.112.2` serait toujours acceptée.

Si vous utilisez un autre outil pour gérer vos installations, comme `uv`, Poetry, Pipenv, ou autres, ils ont tous un moyen que vous pouvez utiliser pour définir des versions spécifiques pour vos paquets.

## Versions disponibles { #available-versions }

Vous pouvez consulter les versions disponibles (par exemple, pour vérifier quelle est la dernière version en date) dans les [Notes de version](../release-notes.md){.internal-link target=_blank}.

## À propos des versions { #about-versions }

Suivant les conventions de versionnage sémantique, toute version inférieure à `1.0.0` peut potentiellement ajouter des changements non rétrocompatibles.

FastAPI suit également la convention selon laquelle tout changement de version « PATCH » concerne des corrections de bogues et des changements rétrocompatibles.

/// tip | Astuce

Le « PATCH » est le dernier chiffre, par exemple, dans `0.2.3`, la version PATCH est `3`.

///

Donc, vous devriez être en mesure d'épingler une version comme suit :

```txt
fastapi>=0.45.0,<0.46.0
```

Les changements non rétrocompatibles et les nouvelles fonctionnalités sont ajoutés dans les versions « MINOR ».

/// tip | Astuce

Le « MINOR » est le numéro au milieu, par exemple, dans `0.2.3`, la version MINOR est `2`.

///

## Mettre à niveau les versions de FastAPI { #upgrading-the-fastapi-versions }

Vous devez ajouter des tests pour votre application.

Avec **FastAPI** c'est très facile (merci à Starlette), consultez les documents : [Tests](../tutorial/testing.md){.internal-link target=_blank}

Après avoir des tests, vous pouvez mettre à niveau la version de **FastAPI** vers une version plus récente et vous assurer que tout votre code fonctionne correctement en exécutant vos tests.

Si tout fonctionne, ou après avoir effectué les changements nécessaires, et que tous vos tests passent, vous pouvez alors épingler votre `fastapi` à cette nouvelle version récente.

## À propos de Starlette { #about-starlette }

Vous ne devez pas épingler la version de `starlette`.

Différentes versions de **FastAPI** utiliseront une version spécifique plus récente de Starlette.

Ainsi, vous pouvez simplement laisser **FastAPI** utiliser la bonne version de Starlette.

## À propos de Pydantic { #about-pydantic }

Pydantic inclut les tests pour **FastAPI** avec ses propres tests, ainsi les nouvelles versions de Pydantic (au-dessus de `1.0.0`) sont toujours compatibles avec FastAPI.

Vous pouvez épingler Pydantic à toute version supérieure à `1.0.0` qui fonctionne pour vous.

Par exemple :

```txt
pydantic>=2.7.0,<3.0.0
```
