# Paramètres d'en-tête { #header-parameters }

Vous pouvez définir des paramètres `Header` de la même manière que vous définissez des paramètres `Query`, `Path` et `Cookie`.

## Importer `Header` { #import-header }

Commencez par importer `Header` :

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[3] *}

## Déclarer des paramètres `Header` { #declare-header-parameters }

Déclarez ensuite les paramètres d'en-tête en utilisant la même structure qu'avec `Path`, `Query` et `Cookie`.

Vous pouvez définir la valeur par défaut ainsi que tous les paramètres supplémentaires de validation ou d'annotation :

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[9] *}

/// note | Détails techniques

`Header` est une classe « sœur » de `Path`, `Query` et `Cookie`. Elle hérite également de la même classe commune `Param`.

Mais rappelez-vous que lorsque vous importez `Query`, `Path`, `Header` et d'autres depuis `fastapi`, ce sont en réalité des fonctions qui renvoient des classes spéciales.

///

/// info

Pour déclarer des en-têtes, vous devez utiliser `Header`, sinon les paramètres seraient interprétés comme des paramètres de requête.

///

## Conversion automatique { #automatic-conversion }

`Header` offre un peu de fonctionnalité supplémentaire par rapport à `Path`, `Query` et `Cookie`.

La plupart des en-têtes standards sont séparés par un caractère « trait d'union », également appelé « signe moins » (`-`).

Mais une variable comme `user-agent` est invalide en Python.

Ainsi, par défaut, `Header` convertit les caractères des noms de paramètres du tiret bas (`_`) en trait d'union (`-`) pour extraire et documenter les en-têtes.

De plus, les en-têtes HTTP ne sont pas sensibles à la casse, vous pouvez donc les déclarer avec le style Python standard (aussi appelé « snake_case »).

Vous pouvez donc utiliser `user_agent` comme vous le feriez normalement dans du code Python, au lieu d'avoir à mettre des majuscules aux premières lettres comme `User_Agent` ou quelque chose de similaire.

Si, pour une raison quelconque, vous devez désactiver la conversion automatique des traits bas en traits d'union, définissez le paramètre `convert_underscores` de `Header` sur `False` :

{* ../../docs_src/header_params/tutorial002_an_py310.py hl[10] *}

/// warning | Alertes

Avant de définir `convert_underscores` sur `False`, gardez à l'esprit que certains proxies et serveurs HTTP interdisent l'utilisation d'en-têtes contenant des traits bas.

///

## Gérer les en-têtes dupliqués { #duplicate-headers }

Il est possible de recevoir des en-têtes en double. Autrement dit, le même en-tête avec plusieurs valeurs.

Vous pouvez définir ces cas à l'aide d'une liste dans la déclaration de type.

Vous recevrez toutes les valeurs de l'en-tête dupliqué sous forme de `list` Python.

Par exemple, pour déclarer un en-tête `X-Token` qui peut apparaître plusieurs fois, vous pouvez écrire :

{* ../../docs_src/header_params/tutorial003_an_py310.py hl[9] *}

Si vous communiquez avec ce *chemin d'accès* en envoyant deux en-têtes HTTP comme :

```
X-Token: foo
X-Token: bar
```

La réponse ressemblerait à ceci :

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## Récapitulatif { #recap }

Déclarez les en-têtes avec `Header`, en suivant le même modèle que pour `Query`, `Path` et `Cookie`.

Et ne vous souciez pas des traits bas dans vos variables, **FastAPI** s'occupe de les convertir.
