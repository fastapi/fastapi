# Réponse - Modifier le code d'état { #response-change-status-code }

Vous avez probablement déjà lu que vous pouvez définir un [Code d'état de la réponse](../tutorial/response-status-code.md){.internal-link target=_blank} par défaut.

Mais dans certains cas, vous devez renvoyer un code d'état différent de celui par défaut.

## Cas d'utilisation { #use-case }

Par exemple, imaginez que vous vouliez renvoyer par défaut un code d'état HTTP « OK » `200`.

Mais si les données n'existent pas, vous voulez les créer et renvoyer un code d'état HTTP « CREATED » `201`.

Mais vous souhaitez toujours pouvoir filtrer et convertir les données que vous renvoyez avec un `response_model`.

Pour ces cas, vous pouvez utiliser un paramètre `Response`.

## Utiliser un paramètre `Response` { #use-a-response-parameter }

Vous pouvez déclarer un paramètre de type `Response` dans votre fonction de chemin d'accès (comme vous pouvez le faire pour les cookies et les en-têtes).

Vous pouvez ensuite définir le `status_code` dans cet objet de réponse *temporaire*.

{* ../../docs_src/response_change_status_code/tutorial001_py310.py hl[1,9,12] *}

Vous pouvez ensuite renvoyer n'importe quel objet nécessaire, comme d'habitude (un `dict`, un modèle de base de données, etc.).

Et si vous avez déclaré un `response_model`, il sera toujours utilisé pour filtrer et convertir l'objet que vous avez renvoyé.

**FastAPI** utilisera cette réponse *temporaire* pour extraire le code d'état (ainsi que les cookies et les en-têtes), et les placera dans la réponse finale qui contient la valeur que vous avez renvoyée, filtrée par tout `response_model`.

Vous pouvez également déclarer le paramètre `Response` dans des dépendances et y définir le code d'état. Mais gardez à l'esprit que la dernière valeur définie prévaut.
