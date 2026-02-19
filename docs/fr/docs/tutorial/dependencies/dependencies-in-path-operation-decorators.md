# Gérer les dépendances dans les décorateurs de chemins d'accès { #dependencies-in-path-operation-decorators }

Dans certains cas, vous n'avez pas vraiment besoin de la valeur de retour d'une dépendance dans votre *fonction de chemin d'accès*.

Ou la dépendance ne retourne aucune valeur.

Mais vous avez quand même besoin qu'elle soit exécutée/résolue.

Dans ces cas, au lieu de déclarer un paramètre de *fonction de chemin d'accès* avec `Depends`, vous pouvez ajouter une `list` de `dependencies` au *décorateur de chemin d'accès*.

## Ajouter `dependencies` au *décorateur de chemin d'accès* { #add-dependencies-to-the-path-operation-decorator }

Le *décorateur de chemin d'accès* accepte un argument optionnel `dependencies`.

Il doit s'agir d'une `list` de `Depends()` :

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[19] *}

Ces dépendances seront exécutées/résolues de la même manière que des dépendances normales. Mais leur valeur (si elles en retournent une) ne sera pas transmise à votre *fonction de chemin d'accès*.

/// tip | Astuce

Certains éditeurs vérifient les paramètres de fonction non utilisés et les signalent comme des erreurs.

En utilisant ces `dependencies` dans le *décorateur de chemin d'accès*, vous pouvez vous assurer qu'elles sont exécutées tout en évitant des erreurs de l'éditeur/des outils.

Cela peut également éviter toute confusion pour les nouveaux développeurs qui voient un paramètre inutilisé dans votre code et pourraient penser qu'il est superflu.

///

/// info | Info

Dans cet exemple, nous utilisons des en-têtes personnalisés fictifs `X-Key` et `X-Token`.

Mais dans des cas réels, lors de l'implémentation de la sécurité, vous tirerez davantage d'avantages en utilisant les [utilitaires de sécurité (chapitre suivant)](../security/index.md){.internal-link target=_blank} intégrés.

///

## Gérer les erreurs et les valeurs de retour des dépendances { #dependencies-errors-and-return-values }

Vous pouvez utiliser les mêmes *fonctions* de dépendance que d'habitude.

### Définir les exigences des dépendances { #dependency-requirements }

Elles peuvent déclarer des exigences pour la requête (comme des en-têtes) ou d'autres sous-dépendances :

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[8,13] *}

### Lever des exceptions { #raise-exceptions }

Ces dépendances peuvent `raise` des exceptions, comme des dépendances normales :

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[10,15] *}

### Gérer les valeurs de retour { #return-values }

Elles peuvent retourner des valeurs ou non, ces valeurs ne seront pas utilisées.

Vous pouvez donc réutiliser une dépendance normale (qui retourne une valeur) que vous utilisez déjà ailleurs ; même si la valeur n'est pas utilisée, la dépendance sera exécutée :

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[11,16] *}

## Définir des dépendances pour un groupe de chemins d'accès { #dependencies-for-a-group-of-path-operations }

Plus tard, en lisant comment structurer des applications plus grandes ([Applications plus grandes - Plusieurs fichiers](../../tutorial/bigger-applications.md){.internal-link target=_blank}), éventuellement avec plusieurs fichiers, vous apprendrez à déclarer un unique paramètre `dependencies` pour un groupe de *chemins d'accès*.

## Définir des dépendances globales { #global-dependencies }

Ensuite, nous verrons comment ajouter des dépendances à l'application `FastAPI` entière, afin qu'elles s'appliquent à chaque *chemin d'accès*.
