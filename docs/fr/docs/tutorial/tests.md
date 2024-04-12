# Test

Grace à <a href="https://www.starlette.io/testclient/" class="external-link" target="_blank">Starlette</a>, tester l'application **FastAPI** est facile et agréable.

Il repose sur <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>, ce dernier conçu sur la base de Requests, ce qui le rend intuitif et familier pour la plupart d'entre nous.

Ainsi, il vous est possible d'uiliser <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> directement avec **FastAPI**.

## Utiliser `TestClient`
!!! info
Pour utiliser `TestClient`, commencez par installer <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a>.

    ex. `pip install httpx`.

Importez `TestClient`.

Créez un `TestClient` en lui passant votre application **FastAPI**.

Créez des fonctions dont le nom commence par `test_` (c'est une convention standard de `pytest`).

Utilisez l'objet `TestClient` de la même manière que vous le feriez avec `httpx`.

Écrivez des instruction d'assertion `assert` simples avec les expressions Python standard qu'il est necessaire de vérifier (de nouveau, c'est une pratique standard de `pytest`)."

```Python hl_lines="2  12  15-18"
{!../../../docs_src/app_testing/tutorial001.py!}
```

!!! astuce
    il est utile de remarquer que les fonction de test sont normal `def`, et non `async def`

    Et les appel au client sont aussi normaux, pas besoin d'utiliser `await`

    Cela permet d'utiliser `pytest` directement sans complication


!!! note "Details Technique"
    il est aussi possible d'utiliser `from starlette.testclient import TestClient`.

    **FastAPI** fournit la même `starlette.testclient` que `fastapi.testclient` pour une simple question de commodité pour vous, développeur. Mais provient directement de Starlette.


!!! astuce
    Si vous chercher tout de même à utiliser la foncion `async` dans vos test, à l'exeption d’envoyer des requêtes à votre application FastAPI (par exemple, des fonctions de base de données asynchrones), jetez un coup d’œil aux [Tests asynchrones (en)](../advanced/async-tests.md) {.internal-link target=_blank} dans le tutoriel avancé.

## tests séparé

Dans une application réelle, vous auriez probablement vos tests dans un fichier différent.

Et votre application **FastAPI** peut également être composée de plusieurs fichiers/modules, etc.

### fichier app de **FastAPI**

disons que vous ayez une structure de fichier comme décrit dans [application de grande taille (en)](./bigger-applications.md) {.internal-link target=_blank}:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

dans le fichier `main.py` vous avez votre application **FastAPI** :


```Python
{!../../../docs_src/app_testing/main.py!}
```

### fichier de test

Ensuite, vous pourriez avoir un fichier `test_main.py` avec vos tests. Il pourrait se trouver sur le même paquet Python (le même dossier avec un fichier `__init__.py`):

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Comme ce fichier se trouve dans le même package, vous pouvez utiliser des importations relatives pour importer l’objet `app` à partir du module `main` (`main.py`):

```Python
{!../../../docs_src/app_testing/test_main.py!}
```

...et obtenir le code pour les tests comme avant.

## Test: exemple supplémentaire

Allons plus loin dans cet exemple et ajoutons plus de détails pour voir comment tester différentes pièces.

### fichier app étendu de **FastAPI**

Continuons avec la même structure de fichier que tout à l'heure:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Supposons que maintenant le fichier `main.py` avec votre application **FastAPI** a d’autres **opérations sur chemin d'accès**.

Il dispose d’une opération `GET` qui pourrait renvoyer une erreur.

Et dispose d’une opération `POST` qui peut renvoyer plusieurs erreurs.

Les deux *opérations sur chemin d'accès* nécessitent un en-tête `X-Token`.

=== "Python 3.10+"

```Python
{!> ../../../docs_src/app_testing/app_b_an_py310/main.py!}
```

=== "Python 3.9+"

```Python
{!> ../../../docs_src/app_testing/app_b_an_py39/main.py!}
```

=== "Python 3.8+"

```Python
{!> ../../../docs_src/app_testing/app_b_an/main.py!}
```

=== "Python 3.10+ non annoté"

!!! astuce
Favoriser l'utilisation de la version `Annoté` si possible.

```Python
{!> ../../../docs_src/app_testing/app_b_py310/main.py!}
```

=== "Python 3.8+ non annoté"

!!! astuce
Favoriser l'utilisation de la version `Annoté` si possible.

```Python
{!> ../../../docs_src/app_testing/app_b/main.py!}
```

### fichier de test étendu

Vous pouvez mettre à jour `test_main.py` avec les tests étendus :

```Python
{!> ../../../docs_src/app_testing/app_b/test_main.py!}
```
Chaque fois que vous avez besoin que le client transmette des informations dans la requête et que vous ne savez pas comment le faire, vous pouvez rechercher (Google) comment comment si prendre dans `httpx`, ou même comment le faire avec `requests`, car la conception de HTTPX est basée sur la conception de Requests.

il vous suffit de faire la même chose dans vos tests.

ex. :

* Pour passer un paramètre *path* ou *query*, ajoutez-le à l’URL directement.

*  Pour passer une instance JSON, passez un objet Python (ex. un `dict`) au paramètre `json`.

* Si vous avez besoin d’envoyer *Form Data* au lieu de JSON, utilisez le paramètre `data` à la place.

* Pour passer des *headers*, utilisez un `dict` dans le paramètre `headers`.

* Pour les *cookies*, un `dict` dans le paramètre `cookies`.

Pour plus d’informations sur la façon de passer des données au backend (en utilisant `httpx` ou `TestClient`), consultez la <a href="https://www.python-httpx.org" class="external-link" target="_blank">documentation HTTPX</a>.

!!! information
    à otez que le `TestClient` reçoit des données qui peuvent être converties en JSON, et non en modèles Pydantic.

Si vous avez un modèle Pydantic dans votre test et que vous souhaitez envoyer ses données à l’application pendant le test, vous pouvez utiliser le `jsonable_encoder` décrit dans [Encodeur compatible avec JSON](encoder.md){:internal-link target=_blank}.

## exécuter les tests

Maintenant, il vous suffit d'installer `pytest`:

<div class="termy">

```console
$ pip install pytest

---> 100%
```
</div>


Cela détectera automatiquement les fichiers et les tests, les exécutera et vous rapportera les résultats.

Exécutez les tests avec :

<div class="termy">

```console
$ pytest

================ test session starts ================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/user/code/superawesome-cli/app
plugins: forked-1.1.3, xdist-1.31.0, cov-2.8.1
collected 6 items

---> 100%

test_main.py <span style="color: green; white-space: pre;">......                            [100%]</span>

<span style="color: green;">================= 1 passed in 0.03s =================</span>
```

</div>
