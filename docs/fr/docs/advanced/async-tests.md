# Tests Asynchrones

Vous avez déjà vu comment tester vos applications **FastAPI** en utilisant le `TestClient` fourni. Jusqu'à présent, vous avez seulement vu comment écrire des tests synchrones, sans utiliser des fonctions `async`.

Être capable d'utiliser des fonctions asynchrones dans vos tests peut être utile, par exemple, lorsque vous requêtez de manière asynchrone votre base de données. Imaginez que vous vouliez tester l'envoi de requête à votre application FastAPI, puis vérifier que votre backend a bien écrit la bonne donnée dans la base de données, tout en utilisant une librairie de base de données asynchrone.

Voyons comment faire.

## pytest.mark.anyio

Afin de permettre l'appel de fonctions asynchrones dans nos tests, il est essentiel que nos fonctions de tests soient asynchrones. AnyIO propose un plugin soigneusement conçu pour cela, qui nous permet de spécifier que certaines fonctions de test doivent être appelées de manière asynchrone.

## HTTPX

Même si votre application **FastAPI** utilise des fonctions `def` normales plutôt que des `async def`, elle reste une application `async` application en dessous.

`TestClient` utilise de la magie à l'intérieur pour appeler l'application FastAPI dans vos fonctions de test `def` normales, en utilisant un standard pytest. Mais cette magie ne marche plus lorsque vous l'utilisez dans une fonction asynchrone. En lançant nos tests de manière asynchrone, `TestClient` ne peut plus être utilisé dans nos fonctions de tests.

`TestClient` repose <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>, et par chance, on peut l'utiliser directement pour tester l'API.

## Exemple

Prenons un exemple simple, on considère une structure de fichier similaire à celle décrite dans [Applications plus grandes](../tutorial/bigger-applications.md){.internal-link target=_blank} et [Testing](../tutorial/testing.md){.internal-link target=_blank}:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Dans le fichier `main.py` il y aurait:

{* ../../docs_src/async_tests/main.py *}

Le fichier `test_main.py` contiendrait les tests pour `main.py`, et pourrait désormais ressembler à :

{* ../../docs_src/async_tests/test_main.py *}

## Lancez les

Comme d'habitude, vous pouvez lancer vos tests en utilisant :

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## En Détail

Le marqueur `@pytest.mark.anyio` informe pytest que la fonction de test doit être appelée de manière asynchrone:

{* ../../docs_src/async_tests/test_main.py hl[7] *}

/// tip

Notez que la fonction de test est maintenant une `async def` plutôt qu'une simple `def` comme précédemment lorsqu'on utilisait `TestClient`.

///

Puis on crée un `AsyncClient` avec l'application, et on lui envoie des requêtes, en utilisant `await`.

{* ../../docs_src/async_tests/test_main.py hl[9:12] *}

C'est l'équivalent de:

```Python
response = client.get('/')
```

...que l'on utilisait pour faire nos requêtes avec le `TestClient`.

/// tip

Notez que l'on utilise async/await avec le nouvel `AsyncClient` - la requête est asynchrone.

///

/// warning

Dans le cas où votre application dépend des événements de durée de vie, le `AsyncClient` ne déclenchera pas ces événements. Pour vous assurer qu'ils soient déclenchés, utilisez `LifespanManager` de <a href="https://github.com/florimondmanca/asgi-lifespan#usage" class="external-link" target="_blank">florimondmanca/asgi-lifespan</a>.

///

## Autres appels de fonction asynchrone

Comme la fonction de test est maintenant asynchrone, vous pouvez désormais aussi appeler (et `await`) d'autres fonctions `async` en plus d'envoyer des requêtes à votre application FastAPI dans vos tests, exactement de la même manière dont vous les auriez appelées à n'importe quel autre endroit de votre code.

/// tip

Si vous rencontrez une `RuntimeError: Task attached to a different loop` en intégrant des appels de fonctions asynchrones dans vos tests (par exemple en utilisant <a href="https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop" class="external-link" target="_blank">MongoDB's MotorClient</a>), n'oubliez pas d'instancier les objets ayant besoin d'une boucle d'événement seulement dans vos fonctions asynchrones, par exemple une fonction de rappel `'@app.on_event("startup")` callback.

///
