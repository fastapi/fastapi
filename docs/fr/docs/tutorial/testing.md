# Tester { #testing }

Grâce à <a href="https://www.starlette.dev/testclient/" class="external-link" target="_blank">Starlette</a>, tester des applications **FastAPI** est simple et agréable.

C’est basé sur <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>, dont la conception s’inspire de Requests, ce qui le rend très familier et intuitif.

Avec cela, vous pouvez utiliser <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> directement avec **FastAPI**.

## Utiliser `TestClient` { #using-testclient }

/// info

Pour utiliser `TestClient`, installez d’abord <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a>.

Vous devez créer un [environnement virtuel](../virtual-environments.md){.internal-link target=_blank}, l’activer, puis y installer le paquet, par exemple :

```console
$ pip install httpx
```

///

Importez `TestClient`.

Créez un `TestClient` en lui passant votre application **FastAPI**.

Créez des fonctions dont le nom commence par `test_` (c’est la convention standard de `pytest`).

Utilisez l’objet `TestClient` de la même manière que vous utilisez `httpx`.

Écrivez de simples instructions `assert` avec les expressions Python standard que vous devez vérifier (là encore, standard `pytest`).

{* ../../docs_src/app_testing/tutorial001_py310.py hl[2,12,15:18] *}

/// tip | Astuce

Remarquez que les fonctions de test sont des `def` normales, pas des `async def`.

Et les appels au client sont aussi des appels normaux, sans utiliser `await`.

Cela vous permet d’utiliser `pytest` directement sans complications.

///

/// note | Détails techniques

Vous pouvez aussi utiliser `from starlette.testclient import TestClient`.

**FastAPI** fournit le même `starlette.testclient` sous le nom `fastapi.testclient` uniquement pour votre commodité, en tant que développeur. Mais cela vient directement de Starlette.

///

/// tip | Astuce

Si vous souhaitez appeler des fonctions `async` dans vos tests en dehors de l’envoi de requêtes à votre application FastAPI (par exemple des fonctions de base de données asynchrones), consultez les [Tests asynchrones](../advanced/async-tests.md){.internal-link target=_blank} dans le tutoriel avancé.

///

## Séparer les tests { #separating-tests }

Dans une application réelle, vous auriez probablement vos tests dans un fichier différent.

Et votre application **FastAPI** pourrait aussi être composée de plusieurs fichiers/modules, etc.

### Fichier d’application **FastAPI** { #fastapi-app-file }

Supposons que vous ayez une structure de fichiers comme décrit dans [Applications plus grandes](bigger-applications.md){.internal-link target=_blank} :

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

Dans le fichier `main.py`, vous avez votre application **FastAPI** :


{* ../../docs_src/app_testing/app_a_py310/main.py *}

### Fichier de test { #testing-file }

Vous pourriez alors avoir un fichier `test_main.py` avec vos tests. Il pourrait vivre dans le même package Python (le même répertoire avec un fichier `__init__.py`) :

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Comme ce fichier se trouve dans le même package, vous pouvez utiliser des imports relatifs pour importer l’objet `app` depuis le module `main` (`main.py`) :

{* ../../docs_src/app_testing/app_a_py310/test_main.py hl[3] *}


… et avoir le code des tests comme précédemment.

## Tester : exemple étendu { #testing-extended-example }

Étendons maintenant cet exemple et ajoutons plus de détails pour voir comment tester différentes parties.

### Fichier d’application **FastAPI** étendu { #extended-fastapi-app-file }

Continuons avec la même structure de fichiers qu’auparavant :

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Supposons que désormais le fichier `main.py` avec votre application **FastAPI** contienne d’autres **chemins d’accès**.

Il a une opération `GET` qui pourrait renvoyer une erreur.

Il a une opération `POST` qui pourrait renvoyer plusieurs erreurs.

Les deux chemins d’accès requièrent un en-tête `X-Token`.

{* ../../docs_src/app_testing/app_b_an_py310/main.py *}

### Fichier de test étendu { #extended-testing-file }

Vous pourriez ensuite mettre à jour `test_main.py` avec les tests étendus :

{* ../../docs_src/app_testing/app_b_an_py310/test_main.py *}


Chaque fois que vous avez besoin que le client transmette des informations dans la requête et que vous ne savez pas comment faire, vous pouvez chercher (Google) comment le faire avec `httpx`, ou même comment le faire avec `requests`, puisque la conception de HTTPX est basée sur celle de Requests.

Ensuite, vous faites simplement la même chose dans vos tests.

Par exemple :

* Pour passer un paramètre de chemin ou un paramètre de requête, ajoutez-le directement à l’URL.
* Pour passer un corps JSON, passez un objet Python (par exemple un `dict`) au paramètre `json`.
* Si vous devez envoyer des *Form Data* au lieu de JSON, utilisez le paramètre `data` à la place.
* Pour passer des en-têtes, utilisez un `dict` dans le paramètre `headers`.
* Pour les cookies, un `dict` dans le paramètre `cookies`.

Pour plus d’informations sur la manière de transmettre des données au backend (en utilisant `httpx` ou le `TestClient`), consultez la <a href="https://www.python-httpx.org" class="external-link" target="_blank">documentation HTTPX</a>.

/// info

Notez que le `TestClient` reçoit des données qui peuvent être converties en JSON, pas des modèles Pydantic.

Si vous avez un modèle Pydantic dans votre test et que vous souhaitez envoyer ses données à l’application pendant les tests, vous pouvez utiliser le `jsonable_encoder` décrit dans [Encodeur compatible JSON](encoder.md){.internal-link target=_blank}.

///

## Exécuter { #run-it }

Après cela, vous avez simplement besoin d’installer `pytest`.

Vous devez créer un [environnement virtuel](../virtual-environments.md){.internal-link target=_blank}, l’activer, puis y installer le paquet, par exemple :

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

Il détectera automatiquement les fichiers et les tests, les exécutera et vous communiquera les résultats.

Exécutez les tests avec :

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
