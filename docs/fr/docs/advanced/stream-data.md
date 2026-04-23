# Diffuser des données { #stream-data }

Si vous voulez diffuser des données pouvant être structurées en JSON, vous devez [Diffuser des JSON Lines](../tutorial/stream-json-lines.md).

Mais si vous voulez diffuser des données binaires pures ou des chaînes, voici comment procéder.

/// info

Ajouté dans FastAPI 0.134.0.

///

## Cas d'utilisation { #use-cases }

Vous pouvez l'utiliser si vous souhaitez diffuser des chaînes pures, par exemple directement depuis la sortie d'un service d'**IA LLM**.

Vous pouvez également l'utiliser pour diffuser de gros fichiers binaires, en envoyant chaque bloc de données au fur et à mesure de la lecture, sans tout charger en mémoire d'un coup.

Vous pouvez aussi diffuser de la **vidéo** ou de l'**audio** de cette manière ; cela peut même être généré au fil du traitement et de l'envoi.

## Utiliser une `StreamingResponse` avec `yield` { #a-streamingresponse-with-yield }

Si vous déclarez un `response_class=StreamingResponse` dans votre *fonction de chemin d'accès*, vous pouvez utiliser `yield` pour envoyer chaque bloc de données à son tour.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[1:23] hl[20,23] *}

FastAPI transmettra chaque bloc de données à la `StreamingResponse` tel quel ; il n'essaiera pas de le convertir en JSON ni autre chose similaire.

### Fonctions de chemin d'accès non async { #non-async-path-operation-functions }

Vous pouvez également utiliser des fonctions `def` classiques (sans `async`), et utiliser `yield` de la même manière.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[26:29] hl[27] *}

### Sans annotation { #no-annotation }

Vous n'avez pas vraiment besoin de déclarer l'annotation de type de retour pour diffuser des données binaires.

Comme FastAPI n'essaiera pas de convertir les données en JSON avec Pydantic ni de les sérialiser, dans ce cas l'annotation de type ne sert qu'à votre éditeur et à vos outils ; elle ne sera pas utilisée par FastAPI.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[32:35] hl[33] *}

Cela signifie aussi qu'avec `StreamingResponse` vous avez la liberté — et la responsabilité — de produire et d'encoder les octets de données exactement comme vous avez besoin de les envoyer, indépendamment des annotations de type. 🤓

### Diffuser des bytes { #stream-bytes }

L'un des principaux cas d'usage consiste à diffuser des `bytes` au lieu de chaînes ; vous pouvez bien sûr le faire.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[44:47] hl[47] *}

## Créer une `PNGStreamingResponse` personnalisée { #a-custom-pngstreamingresponse }

Dans les exemples ci-dessus, les octets de données étaient diffusés, mais la réponse n'avait pas d'en-tête `Content-Type`, le client ne savait donc pas quel type de données il recevait.

Vous pouvez créer une sous-classe personnalisée de `StreamingResponse` qui définit l'en-tête `Content-Type` sur le type de données que vous diffusez.

Par exemple, vous pouvez créer une `PNGStreamingResponse` qui définit l'en-tête `Content-Type` à `image/png` en utilisant l'attribut `media_type` :

{* ../../docs_src/stream_data/tutorial002_py310.py ln[6,19:20] hl[20] *}

Vous pouvez ensuite utiliser cette nouvelle classe dans `response_class=PNGStreamingResponse` dans votre *fonction de chemin d'accès* :

{* ../../docs_src/stream_data/tutorial002_py310.py ln[23:27] hl[23] *}

### Simuler un fichier { #simulate-a-file }

Dans cet exemple, nous simulons un fichier avec `io.BytesIO`, qui est un objet de type fichier résidant uniquement en mémoire, mais qui permet d'utiliser la même interface.

Par exemple, nous pouvons itérer dessus pour en consommer le contenu, comme nous le ferions avec un fichier.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[1:27] hl[3,12:13,25] *}

/// note | Détails techniques

Les deux autres variables, `image_base64` et `binary_image`, correspondent à une image encodée en Base64, puis convertie en bytes, afin de la passer à `io.BytesIO`.

C'est uniquement pour que tout tienne dans le même fichier pour cet exemple, et que vous puissiez le copier et l'exécuter tel quel. 🥚

///

En utilisant un bloc `with`, nous nous assurons que l'objet de type fichier est fermé après l'exécution de la fonction génératrice (la fonction avec `yield`). Donc, après la fin de l'envoi de la réponse.

Ce ne serait pas si important dans cet exemple précis, car il s'agit d'un faux fichier en mémoire (avec `io.BytesIO`), mais avec un vrai fichier, il est important de s'assurer qu'il est fermé une fois le travail terminé.

### Gérer les fichiers et async { #files-and-async }

Dans la plupart des cas, les objets de type fichier ne sont pas compatibles avec `async` et `await` par défaut.

Par exemple, ils n'ont pas de `await file.read()`, ni de `async for chunk in file`.

Et dans de nombreux cas, leur lecture serait une opération bloquante (pouvant bloquer la boucle d'événements), car ils sont lus depuis le disque ou le réseau.

/// info

L'exemple ci-dessus est en réalité une exception, car l'objet `io.BytesIO` est déjà en mémoire ; sa lecture ne bloquera donc rien.

Mais dans de nombreux cas, la lecture d'un fichier ou d'un objet de type fichier bloquera.

///

Pour éviter de bloquer la boucle d'événements, vous pouvez simplement déclarer la *fonction de chemin d'accès* avec un `def` classique au lieu de `async def`. Ainsi, FastAPI l'exécutera dans un worker de pool de threads, afin d'éviter de bloquer la boucle principale.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[30:34] hl[31] *}

/// tip | Astuce

Si vous devez appeler du code bloquant depuis une fonction async, ou une fonction async depuis une fonction bloquante, vous pouvez utiliser [Asyncer](https://asyncer.tiangolo.com), une bibliothèque sœur de FastAPI.

///

### `yield from` { #yield-from }

Lorsque vous itérez sur quelque chose, comme un objet de type fichier, et que vous faites un `yield` pour chaque élément, vous pouvez aussi utiliser `yield from` pour émettre chaque élément directement et éviter la boucle `for`.

Ce n'est pas spécifique à FastAPI, c'est simplement Python, mais c'est une astuce utile à connaître. 😎

{* ../../docs_src/stream_data/tutorial002_py310.py ln[37:40] hl[40] *}
