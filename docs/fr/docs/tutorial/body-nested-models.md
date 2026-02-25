# Corps - Modèles imbriqués { #body-nested-models }

Avec FastAPI, vous pouvez définir, valider, documenter et utiliser des modèles imbriqués à n'importe quelle profondeur (grâce à Pydantic).

## Déclarer des champs de liste { #list-fields }

Vous pouvez définir un attribut comme étant un sous-type. Par exemple, une `list` Python :

{* ../../docs_src/body_nested_models/tutorial001_py310.py hl[12] *}

Cela fera de `tags` une liste, bien que le type des éléments de la liste ne soit pas déclaré.

## Champs de liste avec paramètre de type { #list-fields-with-type-parameter }

Mais Python a une manière spécifique de déclarer des listes avec des types internes, ou « paramètres de type » :

### Déclarer une `list` avec un paramètre de type { #declare-a-list-with-a-type-parameter }

Pour déclarer des types qui ont des paramètres de type (types internes), comme `list`, `dict`, `tuple`,
passez le(s) type(s) interne(s) comme « paramètres de type » à l'aide de crochets : `[` et `]`

```Python
my_list: list[str]
```

C'est simplement la syntaxe Python standard pour les déclarations de type.

Utilisez cette même syntaxe standard pour les attributs de modèles avec des types internes.

Ainsi, dans notre exemple, nous pouvons faire de `tags` spécifiquement une « liste de chaînes » :

{* ../../docs_src/body_nested_models/tutorial002_py310.py hl[12] *}

## Types set { #set-types }

Mais en y réfléchissant, nous réalisons que les tags ne devraient pas se répéter, ce seraient probablement des chaînes uniques.

Et Python dispose d'un type de données spécial pour les ensembles d'éléments uniques, le `set`.

Nous pouvons alors déclarer `tags` comme un set de chaînes :

{* ../../docs_src/body_nested_models/tutorial003_py310.py hl[12] *}

Avec cela, même si vous recevez une requête contenant des doublons, elle sera convertie en un set d'éléments uniques.

Et chaque fois que vous renverrez ces données, même si la source contenait des doublons, elles seront renvoyées sous la forme d'un set d'éléments uniques.

Elles seront également annotées / documentées en conséquence.

## Modèles imbriqués { #nested-models }

Chaque attribut d'un modèle Pydantic a un type.

Mais ce type peut lui-même être un autre modèle Pydantic.

Ainsi, vous pouvez déclarer des « objets » JSON profondément imbriqués avec des noms d'attributs, des types et des validations spécifiques.

Tout cela, de manière arbitrairement imbriquée.

### Définir un sous-modèle { #define-a-submodel }

Par exemple, nous pouvons définir un modèle `Image` :

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[7:9] *}

### Utiliser le sous-modèle comme type { #use-the-submodel-as-a-type }

Nous pouvons ensuite l'utiliser comme type d'un attribut :

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[18] *}

Cela signifie que FastAPI attendrait un corps similaire à :

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

Là encore, avec cette simple déclaration, avec FastAPI vous obtenez :

- Prise en charge par l'éditeur (autocomplétion, etc.), même pour les modèles imbriqués
- Conversion des données
- Validation des données
- Documentation automatique

## Types spéciaux et validation { #special-types-and-validation }

Outre les types singuliers normaux comme `str`, `int`, `float`, etc. vous pouvez utiliser des types singuliers plus complexes qui héritent de `str`.

Pour voir toutes les options dont vous disposez, consultez <a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">l’aperçu des types de Pydantic</a>. Vous verrez quelques exemples au chapitre suivant.

Par exemple, comme dans le modèle `Image` nous avons un champ `url`, nous pouvons le déclarer comme instance de `HttpUrl` de Pydantic au lieu de `str` :

{* ../../docs_src/body_nested_models/tutorial005_py310.py hl[2,8] *}

La chaîne sera vérifiée comme URL valide et documentée comme telle dans JSON Schema / OpenAPI.

## Attributs avec des listes de sous-modèles { #attributes-with-lists-of-submodels }

Vous pouvez également utiliser des modèles Pydantic comme sous-types de `list`, `set`, etc. :

{* ../../docs_src/body_nested_models/tutorial006_py310.py hl[18] *}

Cela attendra (convertira, validera, documentera, etc.) un corps JSON comme :

```JSON hl_lines="11"
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
```
/// info

Remarquez que la clé `images` contient maintenant une liste d'objets image.

///

## Modèles profondément imbriqués { #deeply-nested-models }

Vous pouvez définir des modèles imbriqués à une profondeur arbitraire :

{* ../../docs_src/body_nested_models/tutorial007_py310.py hl[7,12,18,21,25] *}

/// info

Remarquez que `Offer` a une liste d’`Item`, qui à leur tour ont une liste optionnelle d’`Image`.

///

## Corps de listes pures { #bodies-of-pure-lists }

Si la valeur de premier niveau du corps JSON attendu est un `array` JSON (une `list` Python), vous pouvez déclarer le type dans le paramètre de la fonction, de la même manière que dans les modèles Pydantic :

```Python
images: list[Image]
```

comme :

{* ../../docs_src/body_nested_models/tutorial008_py310.py hl[13] *}

## Bénéficier de la prise en charge de l'éditeur partout { #editor-support-everywhere }

Et vous bénéficiez de la prise en charge de l'éditeur partout.

Même pour les éléments à l'intérieur des listes :

<img src="/img/tutorial/body-nested-models/image01.png">

Vous ne pourriez pas obtenir ce type de prise en charge de l'éditeur si vous travailliez directement avec des `dict` au lieu de modèles Pydantic.

Mais vous n'avez pas à vous en soucier non plus, les `dict` entrants sont convertis automatiquement et votre sortie est également convertie automatiquement en JSON.

## Corps de `dict` arbitraires { #bodies-of-arbitrary-dicts }

Vous pouvez également déclarer un corps comme un `dict` avec des clés d’un certain type et des valeurs d’un autre type.

De cette façon, vous n'avez pas besoin de savoir à l'avance quels sont les noms de champs/attributs valides (comme ce serait le cas avec des modèles Pydantic).

Cela serait utile si vous voulez recevoir des clés que vous ne connaissez pas à l'avance.

---

Un autre cas utile est lorsque vous souhaitez avoir des clés d'un autre type (par exemple `int`).

C'est ce que nous allons voir ici.

Dans ce cas, vous accepteriez n'importe quel `dict` tant qu'il a des clés `int` avec des valeurs `float` :

{* ../../docs_src/body_nested_models/tutorial009_py310.py hl[7] *}

/// tip | Astuce

Gardez à l'esprit que JSON ne prend en charge que des `str` comme clés.

Mais Pydantic dispose d'une conversion automatique des données.

Cela signifie que, même si vos clients d'API ne peuvent envoyer que des chaînes comme clés, tant que ces chaînes contiennent des entiers purs, Pydantic les convertira et les validera.

Et le `dict` que vous recevez dans `weights` aura en réalité des clés `int` et des valeurs `float`.

///

## Récapitulatif { #recap }

Avec FastAPI, vous bénéficiez de la flexibilité maximale fournie par les modèles Pydantic, tout en gardant votre code simple, concis et élégant.

Mais avec tous les avantages :

- Prise en charge par l'éditeur (autocomplétion partout !)
- Conversion des données (a.k.a. parsing / sérialisation)
- Validation des données
- Documentation des schémas
- Documentation automatique
