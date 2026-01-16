# À propos des versions de FastAPI { #about-fastapi-versions }

**FastAPI** est déjà utilisé en production dans de nombreuses applications et systèmes. Et la couverture de test est maintenue à 100 %. Mais son développement avance toujours rapidement.

De nouvelles fonctionnalités sont ajoutées fréquemment, des bogues sont corrigés régulièrement, et le code continue de s’améliorer en continu.

C’est pourquoi les versions actuelles sont toujours `0.x.x`, cela reflète que chaque version peut potentiellement introduire des changements incompatibles. Cela suit les conventions du <a href="https://semver.org/" class="external-link" target="_blank">Semantic Versioning</a>.

Vous pouvez créer des applications de production avec **FastAPI** dès maintenant (et vous le faites probablement depuis un certain temps), vous devez simplement vous assurer que vous utilisez une version qui fonctionne correctement avec le reste de votre code.

## Épinglez votre version de `fastapi` { #pin-your-fastapi-version }

La première chose que vous devez faire est d’« épingler » la version de **FastAPI** que vous utilisez à la version spécifique la plus récente dont vous savez qu’elle fonctionne correctement pour votre application.

Par exemple, disons que vous utilisez la version `0.112.0` dans votre app.

Si vous utilisez un fichier `requirements.txt`, vous pouvez spécifier la version avec :

```txt
fastapi[standard]==0.112.0
```

cela signifierait que vous utiliseriez exactement la version `0.112.0`.

Ou vous pourriez aussi l’épingler avec :

```txt
fastapi[standard]>=0.112.0,<0.113.0
```

cela signifierait que vous utiliseriez les versions `0.112.0` ou supérieures, mais inférieures à `0.113.0`, par exemple, une version `0.112.2` serait toujours acceptée.

Si vous utilisez un autre outil pour gérer vos installations, comme `uv`, Poetry, Pipenv, ou autres, ils ont tous un moyen que vous pouvez utiliser pour définir des versions spécifiques pour vos paquets.

## Versions disponibles { #available-versions }

Vous pouvez consulter les versions disponibles (p. ex. pour vérifier quelle est la dernière version actuelle) dans les [Notes de version](../release-notes.md){.internal-link target=_blank}.

## À propos des versions { #about-versions }

En suivant les conventions du Semantic Versioning, toute version inférieure à `1.0.0` peut potentiellement ajouter des changements incompatibles.

FastAPI suit également la convention selon laquelle tout changement de version « PATCH » concerne des corrections de bogues et des changements compatibles.

/// tip | Astuce

Le « PATCH » est le dernier chiffre, par exemple, dans `0.2.3`, la version PATCH est `3`.

///

Ainsi, vous devriez pouvoir épingler une version comme suit :

```txt
fastapi>=0.45.0,<0.46.0
```

Les changements incompatibles et les nouvelles fonctionnalités sont ajoutés dans les versions « MINOR ».

/// tip | Astuce

Le « MINOR » est le numéro au milieu, par exemple, dans `0.2.3`, la version MINOR est `2`.

///

## Mettre à niveau les versions de FastAPI { #upgrading-the-fastapi-versions }

Vous devez ajouter des tests pour votre app.

Avec **FastAPI**, c’est très facile (grâce à Starlette), consultez la documentation : [Testing](../tutorial/testing.md){.internal-link target=_blank}

Après avoir des tests, vous pouvez alors mettre à niveau la version de **FastAPI** vers une version plus récente, et vous assurer que tout votre code fonctionne correctement en exécutant vos tests.

Si tout fonctionne, ou après avoir effectué les changements nécessaires, et que tous vos tests passent, vous pouvez alors épingler votre `fastapi` à cette nouvelle version récente.

## À propos de Starlette { #about-starlette }

Vous ne devriez pas épingler la version de `starlette`.

Différentes versions de **FastAPI** utiliseront une version spécifique plus récente de Starlette.

Ainsi, vous pouvez simplement laisser **FastAPI** utiliser la bonne version de Starlette.

## À propos de Pydantic { #about-pydantic }

Pydantic inclut les tests pour **FastAPI** avec ses propres tests, ainsi les nouvelles versions de Pydantic (au-dessus de `1.0.0`) sont toujours compatibles avec FastAPI.

Vous pouvez épingler Pydantic à toute version supérieure à `1.0.0` qui fonctionne pour vous.

Par exemple :

```txt
pydantic>=2.7.0,<3.0.0
```
