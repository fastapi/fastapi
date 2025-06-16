# Testing

<a href="https://www.starlette.io/testclient/" class="external-link" target="_blank">Starlette</a> rend le test des applications **FastAPI** facile et agréable.

Il est basé sur <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>, qui est lui-même basé sur Request, ce qui le rend très compréhensible et intuitif.

Cela vous permet d'utiliser directement <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> avec **FastAPI**.

## Utiliser `TestClient`

/// info

Pour utiliser `TestClient`, installez d'abord <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a>.

Assurez-vous de créez un [environnement virtuel](../virtual-environments.md){.internal-link target=_blank}, activez-le, puis installez-le, par exemple:

```console
$ pip install httpx
```

///

Importez `TestClient`.

Créez un `TestClient` en y passant votre application **FastAPI**.

Créez des fonctions ayant un nom commençant par `test_` (c'est une convention standard de `pytest`).

Utilisez l'objet `TestClient` comme vous le faites avec `httpx`.

Rédigez des `assert` simples avec les expressions Python standards que vous devez vérifier (encore une fois, un standard `pytest`).

{* ../../docs_src/app_testing/tutorial001.py hl[2,12,15:18] *}

/// tip

Remarquez que les fonctions de test sont des `def` normaux, pas des `async def`.

Et que les appels au client sont également des appels normaux, n'utilisant pas `await`.

Cela vous permet d'utiliser `pytest` directement sans complications.

///

/// note | "Technical Details"

Vous pouvez également utiliser `from starlette.testclient import TestClient`.

**FastAPI** fournit à la fois `starlette.testclient` ainsi que `fastapi.testclient` par commodité pour vous, le développeur. Mais il vient directement de Starlette.

///

/// tip

Si vous souhaitez appeler des fonctions `async` dans vos tests en plus des requêtes à votre application **FastAPI** (comme par exemple des fonctions de base de données asynchrones), jetez un coup d'œil à [Tests Asynchrones](../advanced/async-tests.md){.internal-link target=_blank} dans le tutoriel avancé.

///

## Séparer les tests

Dans une application réelle, il est probable que vous aurez vos tests dans des fichiers distincts.

Et votre application **FastAPI** pourrait aussi être composée de plusieurs fichiers/modules, etc.

### Fichier de l'application **FastAPI**

Disons que vous avez une structure de fichier comme décrite dans [Applications plus grandes](bigger-applications.md){.internal-link target=_blank}:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

Dans le fichier `main.py` vous avez votre app **FastAPI**:


{* ../../docs_src/app_testing/main.py *}

### Fichier de test

Puis, vous pourriez avoir un fichier `test_main.py` avec vos tests. Il pourrait être dans le même paquet Python (le même répertoire avec un fichier `__init__.py`):

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Étant donné que ce fichier est dans le même paquet, vous avez la possibilité d'utiliser un import relatif pour importer l'objet `app` du module `main` (`main.py`):

{* ../../docs_src/app_testing/test_main.py hl[3] *}

...et avoir le code pour les tests comme avant.

## Testing: exemple étendu

Maintenant, nous allons élargir cet exemple et ajouter plus de détails pour voir comment tester des parties différentes.

### Fichier **FastAPI** app étendu

Poursuivons avec la même structure de fichier que précédemment:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Disons que maintenant le fichier `main.py` avec votre application **FastAPI** a d'autres **opérations de chemin**.

Il a une opération `GET` qui pourrait renvoyer une erreur.

Il a une opération `POST` qui pourrait renvoyer plusieurs erreurs.

Les deux *opérations de chemin* demandent un en-tête `X-Token`.

//// tab | Python 3.10+

```Python
{!> ../../docs_src/app_testing/app_b_an_py310/main.py!}
```

////

//// tab | Python 3.9+

```Python
{!> ../../docs_src/app_testing/app_b_an_py39/main.py!}
```

////

//// tab | Python 3.8+

```Python
{!> ../../docs_src/app_testing/app_b_an/main.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip

Preferez utiliser la version `Annotated` si possible.

///

```Python
{!> ../../docs_src/app_testing/app_b_py310/main.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Preferez utiliser la version `Annotated` si possible.

///

```Python
{!> ../../docs_src/app_testing/app_b/main.py!}
```

////

### Fichier de tests étendu

Vous auriez la possibilité de mettre à jour `test_main.py` avec les tests étendus:

{* ../../docs_src/app_testing/app_b/test_main.py *}

Lorsque vous avez besoin du client pour passer des informations dans la requête et que vous ne savez pas comment faire, vous pouvez chercher (Google) comment faire avec `httpx`, ou même avec `requests`, étant donné que le design de HTTPX est basé sur le design de Requests.

Il suffit ensuite de faire la même chose dans vos tests.

Exemple:

* Pour passer un paramètre de *chemin* ou de *requête*, ajoutez-le à l'URL lui-même.
* Pour passez un corps JSON, passez un objet Python (par exemple un `dict`) au paramètre `json`.
* Si vous devez envoyer des données *Form Data* au lieu de JSON, utilisez le paramètre `data` à la place.
* Pour passer des *en-têtes*, utilisez un `dict` dans le paramètre `headers`.
* Pour passer des *cookies*, un `dict` dans le paramètre `cookies`.


Pour plus d'informations sur la façon de passer des données au backend (en utilisant `httpx` ou le `TestClient`), consultez la <a href="https://www.python-httpx.org" class="external-link" target="_blank">documentation de HTTPX</a>.

/// info

Notez que le `TestClient` reçoit des données qui peuvent être converties en JSON, et non des modèles Pydantic.

Si vous avez un modèle Pydantic dans votre test et que vous voulez envoyer ses données à l'application pendant le test, vous pouvez utiliser le `jsonable_encoder` décrit dans [Encodeur JSON compatible](encoder.md){.internal-link target=_blank}.

///

## Le lancer

Ensuite, vous avez juste besoin d'installer `pytest`.

Assurez-vous de créer un [environnement virtuel](../virtual-environments.md){.internal-link target=_blank}, de l'activer, puis de l'installer, par exemple:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

Il détectera automatiquement les fichiers et les tests, les exécutera et vous rapportera les résultats.

Lancez les tests avec:

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
