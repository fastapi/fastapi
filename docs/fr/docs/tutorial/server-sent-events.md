# Événements envoyés par le serveur (SSE) { #server-sent-events-sse }

Vous pouvez diffuser des données vers le client en utilisant les **Server-Sent Events** (SSE).

C'est similaire à [Diffuser des JSON Lines](stream-json-lines.md), mais cela utilise le format `text/event-stream`, pris en charge nativement par les navigateurs via l’API [`EventSource`](https://developer.mozilla.org/en-US/docs/Web/API/EventSource).

/// info | Info

Ajouté dans FastAPI 0.135.0.

///

## Que sont les Server-Sent Events ? { #what-are-server-sent-events }

SSE est un standard pour diffuser des données du serveur au client via HTTP.

Chaque événement est un petit bloc de texte avec des « champs » comme `data`, `event`, `id` et `retry`, séparés par des lignes vides.

Cela ressemble à ceci :

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

Les SSE sont couramment utilisés pour le streaming de chat IA, les notifications en direct, les journaux et l’observabilité, et d’autres cas où le serveur envoie des mises à jour au client.

/// tip | Astuce

Si vous souhaitez diffuser des données binaires, par exemple de la vidéo ou de l’audio, consultez le guide avancé : [Diffuser des données](../advanced/stream-data.md).

///

## Diffuser des SSE avec FastAPI { #stream-sse-with-fastapi }

Pour diffuser des SSE avec FastAPI, utilisez `yield` dans votre *fonction de chemin d'accès* et définissez `response_class=EventSourceResponse`.

Importez `EventSourceResponse` depuis `fastapi.sse` :

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

Chaque élément produit avec `yield` est encodé en JSON et envoyé dans le champ `data:` d’un événement SSE.

Si vous déclarez le type de retour comme `AsyncIterable[Item]`, FastAPI l’utilisera pour **valider**, **documenter** et **sérialiser** les données avec Pydantic.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip | Astuce

Comme Pydantic le sérialisera du côté **Rust**, vous obtiendrez une **performance** bien supérieure que si vous ne déclarez pas de type de retour.

///

### Fonctions de chemin d'accès non async { #non-async-path-operation-functions }

Vous pouvez aussi utiliser des fonctions `def` normales (sans `async`), et utiliser `yield` de la même façon.

FastAPI s’assure qu’elles s’exécutent correctement pour ne pas bloquer la boucle d’événements.

Dans ce cas la fonction n’est pas async, le type de retour approprié serait `Iterable[Item]` :

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### Sans type de retour { #no-return-type }

Vous pouvez aussi omettre le type de retour. FastAPI utilisera le [`jsonable_encoder`](./encoder.md) pour convertir les données et les envoyer.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

Si vous devez définir des champs SSE comme `event`, `id`, `retry` ou `comment`, vous pouvez produire des objets `ServerSentEvent` au lieu de données brutes.

Importez `ServerSentEvent` depuis `fastapi.sse` :

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

Le champ `data` est toujours encodé en JSON. Vous pouvez passer toute valeur sérialisable en JSON, y compris des modèles Pydantic.

## Données brutes { #raw-data }

Si vous devez envoyer des données **sans** encodage JSON, utilisez `raw_data` au lieu de `data`.

C’est utile pour envoyer du texte préformaté, des lignes de log, ou des valeurs <dfn title="Une valeur utilisée pour indiquer une condition ou un état particulier">« sentinelle »</dfn> spéciales comme `[DONE]`.

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note | Remarque

`data` et `raw_data` s’excluent mutuellement. Vous ne pouvez en définir qu’un seul par `ServerSentEvent`.

///

## Reprendre avec `Last-Event-ID` { #resuming-with-last-event-id }

Quand un navigateur se reconnecte après une coupure, il envoie le dernier `id` reçu dans l’en-tête `Last-Event-ID`.

Vous pouvez le lire comme paramètre d’en-tête et l’utiliser pour reprendre le flux là où le client s’était arrêté :

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## SSE avec POST { #sse-with-post }

SSE fonctionne avec **n’importe quelle méthode HTTP**, pas seulement `GET`.

C’est utile pour des protocoles comme [MCP](https://modelcontextprotocol.io) qui diffusent des SSE via `POST` :

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## Détails techniques { #technical-details }

FastAPI met en œuvre certaines bonnes pratiques SSE prêtes à l’emploi.

- Envoyer un commentaire **« keep alive » `ping`** toutes les 15 secondes quand aucun message n’a été émis, pour éviter que certains proxys ne ferment la connexion, comme suggéré dans la [Spécification HTML : Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes).
- Définir l’en-tête `Cache-Control: no-cache` pour **empêcher la mise en cache** du flux.
- Définir un en-tête spécial `X-Accel-Buffering: no` pour **empêcher le buffering** dans certains proxys comme Nginx.

Vous n’avez rien à faire, cela fonctionne prêt à l’emploi. 🤓
