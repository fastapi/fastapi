# WebSockets { #websockets }

Vous pouvez utiliser <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">API WebSockets</a> avec **FastAPI**.

## Installer `websockets` { #install-websockets }

Vous devez créer un [environnement virtuel](../virtual-environments.md){.internal-link target=_blank}, l'activer, et installer `websockets` (une bibliothèque Python qui facilite l'utilisation du protocole « WebSocket ») :

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## Client WebSocket { #websockets-client }

### En production { #in-production }

Dans votre système de production, vous avez probablement un frontend créé avec un framework moderne comme React, Vue.js ou Angular.

Et pour communiquer en utilisant WebSockets avec votre backend, vous utiliseriez probablement les outils fournis par votre frontend.

Ou vous pouvez avoir une application mobile native qui communique directement avec votre backend WebSocket, en code natif.

Ou vous pouvez avoir toute autre façon de communiquer avec l'endpoint WebSocket.

---

Mais pour cet exemple, nous utiliserons un document HTML très simple avec un peu de JavaScript, le tout dans une longue chaîne.

Cela, bien entendu, n'est pas optimal et vous ne l'utiliseriez pas en production.

En production, vous auriez l'une des options ci-dessus.

Mais c'est la façon la plus simple de se concentrer sur la partie serveur des WebSockets et d'avoir un exemple fonctionnel :

{* ../../docs_src/websockets/tutorial001_py310.py hl[2,6:38,41:43] *}

## Créer un `websocket` { #create-a-websocket }

Dans votre application **FastAPI**, créez un `websocket` :

{* ../../docs_src/websockets/tutorial001_py310.py hl[1,46:47] *}

/// note | Détails techniques

Vous pourriez aussi utiliser `from starlette.websockets import WebSocket`.

**FastAPI** fournit le même `WebSocket` directement, simplement pour vous faciliter la vie en tant que développeur. Mais il provient directement de Starlette.

///

## Attendre des messages et envoyer des messages { #await-for-messages-and-send-messages }

Dans votre route WebSocket, vous pouvez `await` des messages et envoyer des messages.

{* ../../docs_src/websockets/tutorial001_py310.py hl[48:52] *}

Vous pouvez recevoir et envoyer des données binaires, texte et JSON.

## Essayer { #try-it }

Si votre fichier s'appelle `main.py`, exécutez votre application avec :

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Ouvrez votre navigateur à l'adresse <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Vous verrez une page simple comme :

<img src="/img/tutorial/websockets/image01.png">

Vous pouvez saisir des messages dans le champ de saisie et les envoyer :

<img src="/img/tutorial/websockets/image02.png">

Et votre application **FastAPI** avec WebSockets vous répondra :

<img src="/img/tutorial/websockets/image03.png">

Vous pouvez envoyer (et recevoir) de nombreux messages :

<img src="/img/tutorial/websockets/image04.png">

Et tous utiliseront la même connexion WebSocket.

## Utiliser `Depends` et autres { #using-depends-and-others }

Dans les endpoints WebSocket, vous pouvez importer depuis `fastapi` et utiliser :

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

Ils fonctionnent de la même manière que pour les autres endpoints/*chemins d'accès* FastAPI :

{* ../../docs_src/websockets/tutorial002_an_py310.py hl[68:69,82] *}

/// info

Comme il s'agit d'un WebSocket, il n'est pas vraiment logique de lever une `HTTPException`, nous levons plutôt une `WebSocketException`.

Vous pouvez utiliser un code de fermeture parmi les <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">codes valides définis dans la spécification</a>.

///

### Essayez les WebSockets avec des dépendances { #try-the-websockets-with-dependencies }

Si votre fichier s'appelle `main.py`, exécutez votre application avec :

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Ouvrez votre navigateur à l'adresse <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Là, vous pouvez définir :

* « Item ID », utilisé dans le chemin.
* « Token » utilisé comme paramètre de requête.

/// tip | Astuce

Notez que le `token` de requête sera géré par une dépendance.

///

Avec cela, vous pouvez connecter le WebSocket puis envoyer et recevoir des messages :

<img src="/img/tutorial/websockets/image05.png">

## Gérer les déconnexions et plusieurs clients { #handling-disconnections-and-multiple-clients }

Lorsqu'une connexion WebSocket est fermée, l'instruction `await websocket.receive_text()` lèvera une exception `WebSocketDisconnect`, que vous pouvez ensuite intercepter et gérer comme dans cet exemple.

{* ../../docs_src/websockets/tutorial003_py310.py hl[79:81] *}

Pour l'essayer :

* Ouvrez l'application dans plusieurs onglets du navigateur.
* Écrivez des messages depuis ceux-ci.
* Puis fermez l'un des onglets.

Cela lèvera l'exception `WebSocketDisconnect`, et tous les autres clients recevront un message comme :

```
Client #1596980209979 left the chat
```

/// tip | Astuce

L'application ci-dessus est un exemple minimal et simple pour montrer comment gérer et diffuser des messages à plusieurs connexions WebSocket.

Mais gardez à l'esprit que, comme tout est géré en mémoire, dans une seule liste, cela ne fonctionnera que tant que le processus s'exécute et uniquement avec un seul processus.

Si vous avez besoin de quelque chose de facile à intégrer avec FastAPI mais plus robuste, pris en charge par Redis, PostgreSQL ou autres, consultez <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a>.

///

## Plus d'informations { #more-info }

Pour en savoir plus sur les options, consultez la documentation de Starlette concernant :

* <a href="https://www.starlette.dev/websockets/" class="external-link" target="_blank">La classe `WebSocket`</a>.
* <a href="https://www.starlette.dev/endpoints/#websocketendpoint" class="external-link" target="_blank">Gestion des WebSocket basée sur des classes</a>.
