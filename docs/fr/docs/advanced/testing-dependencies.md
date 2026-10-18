# Tester des dépendances avec des surcharges { #testing-dependencies-with-overrides }

## Surcharger des dépendances pendant les tests { #overriding-dependencies-during-testing }

Il existe des cas où vous souhaiterez surcharger une dépendance pendant les tests.

Vous ne voulez pas exécuter la dépendance originale (ni ses éventuelles sous‑dépendances).

À la place, vous souhaitez fournir une dépendance différente, utilisée uniquement pendant les tests (éventuellement seulement pour certains tests), et qui fournira une valeur utilisable partout où l’on utilisait celle de la dépendance originale.

### Cas d’usage : service externe { #use-cases-external-service }

Par exemple, vous avez un fournisseur d’authentification externe à appeler.

Vous lui envoyez un token et il renvoie un utilisateur authentifié.

Ce fournisseur peut vous facturer à la requête, et l’appeler peut prendre plus de temps que si vous aviez un utilisateur factice fixe pour les tests.

Vous voudrez probablement tester le fournisseur externe une fois, mais pas nécessairement l’appeler pour chaque test exécuté.

Dans ce cas, vous pouvez surcharger la dépendance qui appelle ce fournisseur et utiliser une dépendance personnalisée qui renvoie un utilisateur factice, uniquement pour vos tests.

### Utiliser l’attribut `app.dependency_overrides` { #use-the-app-dependency-overrides-attribute }

Pour ces cas, votre **FastAPI** application possède un attribut `app.dependency_overrides` ; c’est un simple `dict`.

Pour surcharger une dépendance lors des tests, vous mettez comme clé la dépendance originale (une fonction) et comme valeur votre surcharge de dépendance (une autre fonction).

Ensuite, **FastAPI** appellera cette surcharge au lieu de la dépendance originale.

{* ../../docs_src/dependency_testing/tutorial001_an_py310.py hl[26:27,30] *}

/// tip | Astuce

Vous pouvez définir une surcharge de dépendance pour une dépendance utilisée n’importe où dans votre application **FastAPI**.

La dépendance originale peut être utilisée dans une fonction de chemin d'accès, un décorateur de chemin d'accès (quand vous n’utilisez pas la valeur de retour), un appel à `.include_router()`, etc.

FastAPI pourra toujours la surcharger.

///

Vous pouvez ensuite réinitialiser vos surcharges (les supprimer) en affectant à `app.dependency_overrides` un `dict` vide :

```Python
app.dependency_overrides = {}
```
/// tip | Astuce

Si vous souhaitez surcharger une dépendance uniquement pendant certains tests, vous pouvez définir la surcharge au début du test (dans la fonction de test) et la réinitialiser à la fin (à la fin de la fonction de test).

///
