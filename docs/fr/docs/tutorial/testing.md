# Tester

Grâce à <a href="https://www.starlette.io/testclient/" class="external-link" target="_blank">Starlette</a>, tester des applications **FastAPI** est facile et agréable.

Étant basé sur <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Requests</a>, tester est alors vraiment familier et intuitif.

De plus, vous pouvez utiliser <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> directement avec **FastAPI**.

## Utiliser `TestClient`

Importez `TestClient`.

Créez un object `TestClient` en lui passant votre application **FastAPI**.

Créez des fonctions avec un nom commençant par `test_` (il s'agit d'un standard dans les conventions `pytest`).

Utilisez l'objet `TestClient` de la même manière que vous le feriez avec `requests`.

Écrivez une déclaration simple d'`assert` avec les expressions standard de Python dont vous avez besoin pour faire vos vérifications (de nouveau, il s'agit des standards `pytest`).

```Python hl_lines="2  12  15-18"
{!../../../docs_src/app_testing/tutorial001.py!}
```

!!! info
    Remarquez que les fonctions de tests commencent normalement par `def` et non `async def`.

    Et les appels au client sont des appels normaux n'utilisant pas `await`.

    Cela permet d'utiliser `pytest` directement sans problème.

!!! note "Détails techniques"
    Vous pouvez aussi utiliser `from starlette.testclient import TestClient`.

    **FastAPI** fournit `starlette.testclient` derrière `fastapi.testclient`. `fastapi.testclient` a été créé juste pour votre comodité à vous développeur, mais il vient directement de Starlette.

!!! info
    Si vous voulez appeler les fonctions `async` dans vos tests en dehors de l'envoi de requêtes à votre application FastAPI (par exemple des fonctions asynchrones de base de données), regardez [Async Tests](../advanced/async-tests.md){.internal-link target=_blank} dans le tutoriel avancé.

## La séparation des tests

Dans une vraie application, vous voudrez probablement avoir vos tests dans un fichier différent.

Et votre application **FastAPI** pourrait bien être composée de différents fichiers/modules, etc.

### Le fichier app de **FastAPI**

Disons que vous avez un fichier `main.py` avec votre app **FastAPI** :

```Python
{!../../../docs_src/app_testing/main.py!}
```

### Le fichier de test

Ensuite, vous pourriez avoir un fichier `test_main.py` avec vos tests et importer votre `app` depuis le module `main` (`main.py`):

```Python
{!../../../docs_src/app_testing/test_main.py!}
```

## Tester : exemple étendu

Maintenant, étendons cet exemple en ajoutant plus de détails pour voir comment tester différentes parties.

### Le fichier app étendu de **FastAPI**

Disons que vous avez un fichier `main_b.py` avec votre app **FastAPI**.

Il a une opération `GET` qui pourrait retourner une erreur.

Il a une opération `POST` qui pourrait retourner plusieurs erreurs.

Les deux *opérations de chemin* ont besoin d'un header `X-Token`.

```Python
{!../../../docs_src/app_testing/main_b.py!}
```

### Le fichier de test étendu

Vous pourriez ensuite avoir un fichier `test_main_b.py`, le même qu'avant, avec des tests étendus :

```Python
{!../../../docs_src/app_testing/test_main_b.py!}
```

A chaque fois que vous avez besoin du client pour passer des informations dans la requête et que vous ne savez pas comment, vous pouvez chercher (Google) comment faire cela dans `requests`.

Ensuite, vous faites juste la même chose dans vos tests.

Par exemple :

* Pour passer un paramètre de *chemin* ou *requête*, ajoutez le à l'URL elle-même.
* Pour passer un corps JSON, passer un objet Python (c'est-à-dire un `dict`) au paramètre `json`.
* Si vous avez besoin d'envoyer *Form Data* à la place de JSON, utilisez le paramètre `data` à la place.
* Pour passer des *headers*, utilisez un `dict` dans le paramètre `headers`.
* Pour les *cookies*, un `dict` dans le paramètre `cookies`.

Pour plus d'information sur comment passer les données au backend (en utilisant `requests` ou l'objet `TestClient`) regardez la <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Documentation de Requests</a>.

!!! info
    Notez que l'objet `TestClient` reçoit des données qui peuvent être converties en JSON, non pas des modèles Pydantic.

    Si vous avez un modèle Pydantic dans votre test et que vous voulez envoyer ses données à l'application durant le test, vous pouvez utiliser `jsonable_encoder` décrit dans [JSON Compatible Encoder](encoder.md){.internal-link target=_blank}.

## Lancer les tests

Après tout cela, vous avez juste besoin d'installer `pytest` :

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

Pytest détectera les fichiers et tests automatiquement, les éxecutera et vous renverra les résultats sous la forme d'un rapport.

Lancez les tests avec :

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
