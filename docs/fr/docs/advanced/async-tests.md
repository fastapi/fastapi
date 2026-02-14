# Tests asynchrones { #async-tests }

Vous avez déjà vu comment tester vos applications **FastAPI** en utilisant le `TestClient` fourni. Jusqu'à présent, vous n'avez vu que comment écrire des tests synchrones, sans utiliser de fonctions `async`.

Pouvoir utiliser des fonctions asynchrones dans vos tests peut être utile, par exemple lorsque vous interrogez votre base de données de manière asynchrone. Imaginez que vous vouliez tester l'envoi de requêtes à votre application FastAPI puis vérifier que votre backend a bien écrit les bonnes données dans la base, tout en utilisant une bibliothèque de base de données asynchrone.

Voyons comment procéder.

## pytest.mark.anyio { #pytest-mark-anyio }

Si nous voulons appeler des fonctions asynchrones dans nos tests, nos fonctions de test doivent être asynchrones. AnyIO fournit un plug-in pratique qui nous permet d'indiquer que certaines fonctions de test doivent être appelées de manière asynchrone.

## HTTPX { #httpx }

Même si votre application **FastAPI** utilise des fonctions `def` normales au lieu de `async def`, c'est toujours une application `async` en interne.

Le `TestClient` fait un peu de magie pour appeler l'application FastAPI asynchrone depuis vos fonctions de test `def` normales, en utilisant pytest standard. Mais cette magie ne fonctionne plus lorsque nous l'utilisons dans des fonctions asynchrones. En exécutant nos tests de manière asynchrone, nous ne pouvons plus utiliser le `TestClient` dans nos fonctions de test.

Le `TestClient` est basé sur <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> et, heureusement, nous pouvons l'utiliser directement pour tester l'API.

## Exemple { #example }

Pour un exemple simple, considérons une structure de fichiers similaire à celle décrite dans [Applications plus grandes](../tutorial/bigger-applications.md){.internal-link target=_blank} et [Tests](../tutorial/testing.md){.internal-link target=_blank} :

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Le fichier `main.py` contiendrait :

{* ../../docs_src/async_tests/app_a_py310/main.py *}

Le fichier `test_main.py` contiendrait les tests pour `main.py`, il pourrait maintenant ressembler à ceci :

{* ../../docs_src/async_tests/app_a_py310/test_main.py *}

## Exécuter { #run-it }

Vous pouvez lancer vos tests comme d'habitude via :

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## En détail { #in-detail }

Le marqueur `@pytest.mark.anyio` indique à pytest que cette fonction de test doit être appelée de manière asynchrone :

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[7] *}

/// tip | Astuce

Notez que la fonction de test est maintenant `async def` au lieu de simplement `def` comme auparavant avec le `TestClient`.

///

Nous pouvons ensuite créer un `AsyncClient` avec l'application et lui envoyer des requêtes asynchrones en utilisant `await`.

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[9:12] *}

C'est l'équivalent de :

```Python
response = client.get('/')
```

... que nous utilisions pour faire nos requêtes avec le `TestClient`.

/// tip | Astuce

Notez que nous utilisons async/await avec le nouveau `AsyncClient` — la requête est asynchrone.

///

/// warning | Alertes

Si votre application s'appuie sur des événements de cycle de vie (lifespan), le `AsyncClient` ne déclenchera pas ces événements. Pour vous assurer qu'ils sont déclenchés, utilisez `LifespanManager` depuis <a href="https://github.com/florimondmanca/asgi-lifespan#usage" class="external-link" target="_blank">florimondmanca/asgi-lifespan</a>.

///

## Autres appels de fonctions asynchrones { #other-asynchronous-function-calls }

Comme la fonction de test est désormais asynchrone, vous pouvez également appeler (et `await`) d'autres fonctions `async` en plus d'envoyer des requêtes à votre application FastAPI dans vos tests, exactement comme vous le feriez ailleurs dans votre code.

/// tip | Astuce

Si vous rencontrez une erreur `RuntimeError: Task attached to a different loop` lors de l'intégration d'appels de fonctions asynchrones dans vos tests (par exemple en utilisant <a href="https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop" class="external-link" target="_blank">MotorClient de MongoDB</a>), n'oubliez pas d'instancier les objets qui ont besoin d'une boucle d'événements uniquement dans des fonctions async, par exemple dans un callback `@app.on_event("startup")`.

///
