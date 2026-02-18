# Encodeur compatible JSON { #json-compatible-encoder }

Il existe des cas où vous pourriez avoir besoin de convertir un type de données (comme un modèle Pydantic) en quelque chose de compatible avec JSON (comme un `dict`, `list`, etc.).

Par exemple, si vous devez le stocker dans une base de données.

Pour cela, **FastAPI** fournit une fonction `jsonable_encoder()`.

## Utiliser `jsonable_encoder` { #using-the-jsonable-encoder }

Imaginons que vous ayez une base de données `fake_db` qui ne reçoit que des données compatibles JSON.

Par exemple, elle ne reçoit pas d'objets `datetime`, car ceux-ci ne sont pas compatibles avec JSON.

Ainsi, un objet `datetime` doit être converti en une `str` contenant les données au <a href="https://en.wikipedia.org/wiki/ISO_8601" class="external-link" target="_blank">format ISO</a>.

De la même manière, cette base de données n'accepterait pas un modèle Pydantic (un objet avec des attributs), seulement un `dict`.

Vous pouvez utiliser `jsonable_encoder` pour cela.

Elle reçoit un objet, comme un modèle Pydantic, et renvoie une version compatible JSON :

{* ../../docs_src/encoder/tutorial001_py310.py hl[4,21] *}

Dans cet exemple, elle convertirait le modèle Pydantic en `dict`, et le `datetime` en `str`.

Le résultat de son appel est quelque chose qui peut être encodé avec la fonction standard de Python <a href="https://docs.python.org/3/library/json.html#json.dumps" class="external-link" target="_blank">`json.dumps()`</a>.

Elle ne renvoie pas une grande `str` contenant les données au format JSON (sous forme de chaîne). Elle renvoie une structure de données standard de Python (par ex. un `dict`) avec des valeurs et sous-valeurs toutes compatibles avec JSON.

/// note | Remarque

`jsonable_encoder` est en fait utilisée par **FastAPI** en interne pour convertir des données. Mais elle est utile dans de nombreux autres scénarios.

///
