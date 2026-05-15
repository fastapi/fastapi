# Types de données supplémentaires { #extra-data-types }

Jusqu'à présent, vous avez utilisé des types de données courants, comme :

* `int`
* `float`
* `str`
* `bool`

Mais vous pouvez aussi utiliser des types de données plus complexes.

Et vous bénéficierez toujours des mêmes fonctionnalités que jusqu'à présent :

* Excellente prise en charge dans l'éditeur.
* Conversion des données à partir des requêtes entrantes.
* Conversion des données pour les données de réponse.
* Validation des données.
* Annotations et documentation automatiques.

## Autres types de données { #other-data-types }

Voici quelques types de données supplémentaires que vous pouvez utiliser :

* `UUID` :
    * Un « identifiant universel unique » standard, couramment utilisé comme ID dans de nombreuses bases de données et systèmes.
    * Dans les requêtes et les réponses, il sera représenté sous forme de `str`.
* `datetime.datetime` :
    * Un `datetime.datetime` Python.
    * Dans les requêtes et les réponses, il sera représenté sous forme de `str` au format ISO 8601, par exemple : `2008-09-15T15:53:00+05:00`.
* `datetime.date` :
    * `datetime.date` Python.
    * Dans les requêtes et les réponses, il sera représenté sous forme de `str` au format ISO 8601, par exemple : `2008-09-15`.
* `datetime.time` :
    * Un `datetime.time` Python.
    * Dans les requêtes et les réponses, il sera représenté sous forme de `str` au format ISO 8601, par exemple : `14:23:55.003`.
* `datetime.timedelta` :
    * Un `datetime.timedelta` Python.
    * Dans les requêtes et les réponses, il sera représenté sous forme de `float` de secondes totales.
    * Pydantic permet aussi de le représenter sous la forme d'un « encodage de différence de temps ISO 8601 », [voir la documentation pour plus d'informations](https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers).
* `frozenset` :
    * Dans les requêtes et les réponses, traité de la même manière qu'un `set` :
        * Dans les requêtes, une liste sera lue, les doublons éliminés, puis convertie en `set`.
        * Dans les réponses, le `set` sera converti en `list`.
        * Le schéma généré indiquera que les valeurs du `set` sont uniques (en utilisant `uniqueItems` de JSON Schema).
* `bytes` :
    * `bytes` Python standard.
    * Dans les requêtes et les réponses, traité comme une `str`.
    * Le schéma généré indiquera qu'il s'agit d'une `str` avec le « format » `binary`.
* `Decimal` :
    * `Decimal` Python standard.
    * Dans les requêtes et les réponses, géré de la même manière qu'un `float`.
* Vous pouvez consulter tous les types de données Pydantic valides ici : [Types de données Pydantic](https://docs.pydantic.dev/latest/usage/types/types/).

## Exemple { #example }

Voici un exemple de *chemin d'accès* avec des paramètres utilisant certains des types ci-dessus.

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[1,3,12:16] *}

Notez que les paramètres à l'intérieur de la fonction ont leur type de données naturel et que vous pouvez, par exemple, effectuer des manipulations de dates normales, comme :

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[18:19] *}
