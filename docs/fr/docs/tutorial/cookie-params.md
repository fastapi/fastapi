# Paramètres de cookie { #cookie-parameters }

Vous pouvez définir des paramètres de cookie de la même manière que vous définissez les paramètres `Query` et `Path`.

## Importer `Cookie` { #import-cookie }

Commencez par importer `Cookie` :

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## Déclarer des paramètres `Cookie` { #declare-cookie-parameters }

Déclarez ensuite les paramètres de cookie en utilisant la même structure qu'avec `Path` et `Query`.

Vous pouvez définir la valeur par défaut ainsi que tous les paramètres supplémentaires de validation ou d'annotation :

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | Détails techniques

`Cookie` est une classe « sœur » de `Path` et `Query`. Elle hérite également de la même classe commune `Param`.

Mais rappelez-vous que lorsque vous importez `Query`, `Path`, `Cookie` et d'autres depuis `fastapi`, il s'agit en réalité de fonctions qui renvoient des classes spéciales.

///

/// info

Pour déclarer des cookies, vous devez utiliser `Cookie`, sinon les paramètres seraient interprétés comme des paramètres de requête.

///

/// info

Gardez à l'esprit que, comme **les navigateurs gèrent les cookies** de manière particulière et en coulisses, ils **n'autorisent pas** facilement **JavaScript** à y accéder.

Si vous allez dans l'**interface de la documentation de l'API** à `/docs`, vous pourrez voir la **documentation** des cookies pour vos *chemins d'accès*.

Mais même si vous **renseignez les données** et cliquez sur « Execute », comme l'interface de documentation fonctionne avec **JavaScript**, les cookies ne seront pas envoyés et vous verrez un message **d'erreur** comme si vous n'aviez saisi aucune valeur.

///

## Récapitulatif { #recap }

Déclarez les cookies avec `Cookie`, en utilisant le même schéma commun que `Query` et `Path`.
