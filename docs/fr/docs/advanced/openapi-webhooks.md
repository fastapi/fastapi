# Webhooks OpenAPI { #openapi-webhooks }

Il existe des cas où vous voulez informer les utilisateurs de votre API que votre application peut appeler leur application (en envoyant une requête) avec des données, généralement pour notifier un type d'événement.

Cela signifie qu'au lieu du processus habituel où vos utilisateurs envoient des requêtes à votre API, c'est votre API (ou votre application) qui peut envoyer des requêtes vers leur système (vers leur API, leur application).

On appelle généralement cela un webhook.

## Étapes des webhooks { #webhooks-steps }

Le processus consiste généralement à définir dans votre code le message que vous enverrez, c'est-à-dire le corps de la requête.

Vous définissez également, d'une manière ou d'une autre, à quels moments votre application enverra ces requêtes ou événements.

Et vos utilisateurs définissent aussi, d'une manière ou d'une autre (par exemple dans un tableau de bord Web), l'URL à laquelle votre application doit envoyer ces requêtes.

Toute la logique de gestion des URL des webhooks et le code qui envoie effectivement ces requêtes vous incombent. Vous l'implémentez comme vous le souhaitez dans votre propre code.

## Documenter des webhooks avec FastAPI et OpenAPI { #documenting-webhooks-with-fastapi-and-openapi }

Avec FastAPI, en utilisant OpenAPI, vous pouvez définir les noms de ces webhooks, les types d'opérations HTTP que votre application peut envoyer (par exemple `POST`, `PUT`, etc.) et les corps des requêtes que votre application enverra.

Cela peut grandement faciliter la tâche de vos utilisateurs pour implémenter leurs API afin de recevoir vos requêtes de webhook ; ils pourront même peut-être générer automatiquement une partie de leur propre code d'API.

/// info

Les webhooks sont disponibles dans OpenAPI 3.1.0 et versions ultérieures, pris en charge par FastAPI `0.99.0` et versions ultérieures.

///

## Créer une application avec des webhooks { #an-app-with-webhooks }

Lorsque vous créez une application FastAPI, il existe un attribut `webhooks` que vous pouvez utiliser pour définir des webhooks, de la même manière que vous définiriez des chemins d'accès, par exemple avec `@app.webhooks.post()`.

{* ../../docs_src/openapi_webhooks/tutorial001_py310.py hl[9:12,15:20] *}

Les webhooks que vous définissez apparaîtront dans le schéma **OpenAPI** et dans l'interface de **documentation** automatique.

/// info

L'objet `app.webhooks` est en fait simplement un `APIRouter`, le même type que vous utiliseriez pour structurer votre application en plusieurs fichiers.

///

Notez qu'avec les webhooks, vous ne déclarez pas réellement un chemin (comme `/items/`), le texte que vous y passez est simplement un identifiant du webhook (le nom de l'événement). Par exemple, dans `@app.webhooks.post("new-subscription")`, le nom du webhook est `new-subscription`.

C'est parce qu'on s'attend à ce que vos utilisateurs définissent, par un autre moyen (par exemple un tableau de bord Web), le véritable chemin d'URL où ils souhaitent recevoir la requête de webhook.

### Consulter la documentation { #check-the-docs }

Vous pouvez maintenant démarrer votre application et aller sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vous verrez que votre documentation contient les chemins d'accès habituels et désormais aussi des webhooks :

<img src="/img/tutorial/openapi-webhooks/image01.png">
