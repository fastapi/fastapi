# Types Python avancés { #advanced-python-types }

Voici quelques idées supplémentaires qui peuvent être utiles lorsque vous travaillez avec les types Python.

## Utiliser `Union` ou `Optional` { #using-union-or-optional }

Si votre code ne peut pas utiliser `|` pour une raison quelconque, par exemple si ce n'est pas dans une annotation de type mais dans quelque chose comme `response_model=`, au lieu d'utiliser la barre verticale (`|`) vous pouvez utiliser `Union` de `typing`.

Par exemple, vous pourriez déclarer que quelque chose peut être un `str` ou `None` :

```python
from typing import Union


def say_hi(name: Union[str, None]):
    print(f"Hi {name}!")
```

`typing` propose également un raccourci pour déclarer que quelque chose peut être `None`, avec `Optional`.

Voici un conseil issu de mon point de vue très **subjectif** :

- 🚨 Évitez d'utiliser `Optional[SomeType]`
- À la place ✨ **utilisez `Union[SomeType, None]`** ✨.

Les deux sont équivalents et, en interne, identiques, mais je recommande `Union` plutôt que `Optional` parce que le mot « **optional** » semble impliquer que la valeur est facultative, alors qu'il signifie en réalité « elle peut être `None` », même si elle n'est pas facultative et reste requise.

Je pense que `Union[SomeType, None]` est plus explicite quant à sa signification.

Il ne s'agit que des mots et des noms. Mais ces mots peuvent influencer la manière dont vous et vos coéquipiers pensez au code.

À titre d'exemple, prenons cette fonction :

```python
from typing import Optional


def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

Le paramètre `name` est défini comme `Optional[str]`, mais il **n'est pas facultatif**, vous ne pouvez pas appeler la fonction sans le paramètre :

```Python
say_hi()  # Oh non, cela lève une erreur ! 😱
```

Le paramètre `name` est **toujours requis** (pas *facultatif*) car il n'a pas de valeur par défaut. En revanche, `name` accepte `None` comme valeur :

```Python
say_hi(name=None)  # Ceci fonctionne, None est valide 🎉
```

La bonne nouvelle, c'est que, dans la plupart des cas, vous pourrez simplement utiliser `|` pour définir des unions de types :

```python
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

Ainsi, normalement, vous n'avez pas à vous préoccuper de noms comme `Optional` et `Union`. 😎
