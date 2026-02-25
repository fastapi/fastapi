# Utiliser des dataclasses { #using-dataclasses }

FastAPI est construit au‑dessus de **Pydantic**, et je vous ai montré comment utiliser des modèles Pydantic pour déclarer les requêtes et les réponses.

Mais FastAPI prend aussi en charge l'utilisation de <a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a> de la même manière :

{* ../../docs_src/dataclasses_/tutorial001_py310.py hl[1,6:11,18:19] *}

Cela fonctionne grâce à **Pydantic**, qui offre une <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">prise en charge interne des `dataclasses`</a>.

Ainsi, même avec le code ci‑dessus qui n'emploie pas explicitement Pydantic, FastAPI utilise Pydantic pour convertir ces dataclasses standard en la variante de dataclasses de Pydantic.

Et bien sûr, cela prend en charge la même chose :

* validation des données
* sérialisation des données
* documentation des données, etc.

Cela fonctionne de la même manière qu'avec les modèles Pydantic. Et, en réalité, c'est mis en œuvre de la même façon en interne, en utilisant Pydantic.

/// info | Info

Gardez à l'esprit que les dataclasses ne peuvent pas tout ce que peuvent faire les modèles Pydantic.

Vous pourriez donc avoir encore besoin d'utiliser des modèles Pydantic.

Mais si vous avez déjà un ensemble de dataclasses sous la main, c'est une astuce pratique pour les utiliser afin d'alimenter une API Web avec FastAPI. 🤓

///

## Utiliser des dataclasses dans `response_model` { #dataclasses-in-response-model }

Vous pouvez aussi utiliser `dataclasses` dans le paramètre `response_model` :

{* ../../docs_src/dataclasses_/tutorial002_py310.py hl[1,6:12,18] *}

La dataclass sera automatiquement convertie en dataclass Pydantic.

Ainsi, son schéma apparaîtra dans l'interface utilisateur de la documentation de l'API :

<img src="/img/tutorial/dataclasses/image01.png">

## Utiliser des dataclasses dans des structures de données imbriquées { #dataclasses-in-nested-data-structures }

Vous pouvez aussi combiner `dataclasses` avec d'autres annotations de type pour créer des structures de données imbriquées.

Dans certains cas, vous devrez peut‑être encore utiliser la version `dataclasses` de Pydantic. Par exemple, si vous rencontrez des erreurs avec la documentation d'API générée automatiquement.

Dans ce cas, vous pouvez simplement remplacer les `dataclasses` standard par `pydantic.dataclasses`, qui est un remplacement drop‑in :

{* ../../docs_src/dataclasses_/tutorial003_py310.py hl[1,4,7:10,13:16,22:24,27] *}

1. Nous continuons à importer `field` depuis les `dataclasses` standard.

2. `pydantic.dataclasses` est un remplacement drop‑in pour `dataclasses`.

3. La dataclass `Author` inclut une liste de dataclasses `Item`.

4. La dataclass `Author` est utilisée comme paramètre `response_model`.

5. Vous pouvez utiliser d'autres annotations de type standard avec des dataclasses comme corps de la requête.

    Dans ce cas, il s'agit d'une liste de dataclasses `Item`.

6. Ici, nous renvoyons un dictionnaire qui contient `items`, qui est une liste de dataclasses.

    FastAPI est toujours capable de <dfn title="convertir les données dans un format pouvant être transmis">sérialiser</dfn> les données en JSON.

7. Ici, `response_model` utilise une annotation de type correspondant à une liste de dataclasses `Author`.

    Là encore, vous pouvez combiner `dataclasses` avec des annotations de type standard.

8. Notez que cette *fonction de chemin d'accès* utilise un `def` classique au lieu de `async def`.

    Comme toujours, avec FastAPI vous pouvez combiner `def` et `async def` selon vos besoins.

    Si vous avez besoin d'un rappel sur quand utiliser l'un ou l'autre, consultez la section _« In a hurry? »_ dans la documentation à propos de [`async` et `await`](../async.md#in-a-hurry){.internal-link target=_blank}.

9. Cette *fonction de chemin d'accès* ne renvoie pas des dataclasses (même si elle le pourrait), mais une liste de dictionnaires contenant des données internes.

    FastAPI utilisera le paramètre `response_model` (qui inclut des dataclasses) pour convertir la réponse.

Vous pouvez combiner `dataclasses` avec d'autres annotations de type, selon de nombreuses combinaisons, pour former des structures de données complexes.

Reportez‑vous aux annotations dans le code ci‑dessus pour voir plus de détails spécifiques.

## En savoir plus { #learn-more }

Vous pouvez aussi combiner `dataclasses` avec d'autres modèles Pydantic, en hériter, les inclure dans vos propres modèles, etc.

Pour en savoir plus, consultez la <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/" class="external-link" target="_blank">documentation Pydantic sur les dataclasses</a>.

## Version { #version }

C'est disponible depuis FastAPI version `0.67.0`. 🔖
