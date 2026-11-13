# Tipos avanzados de Python { #advanced-python-types }

Aquí tienes algunas ideas adicionales que podrían ser útiles al trabajar con tipos de Python.

## Usar `Union` u `Optional` { #using-union-or-optional }

Si por alguna razón tu código no puede usar `|`, por ejemplo si no está en una anotación de tipos sino en algo como `response_model=`, en lugar de usar la barra vertical (`|`) puedes usar `Union` de `typing`.

Por ejemplo, podrías declarar que algo podría ser un `str` o `None`:

```python
from typing import Union


def say_hi(name: Union[str, None]):
    print(f"Hi {name}!")
```

`typing` también tiene un atajo para declarar que algo podría ser `None`, con `Optional`.

Aquí va un Consejo desde mi punto de vista muy **subjetivo**:

* 🚨 Evita usar `Optional[SomeType]`
* En su lugar ✨ **usa `Union[SomeType, None]`** ✨.

Ambas son equivalentes y por debajo son lo mismo, pero recomendaría `Union` en lugar de `Optional` porque la palabra "**optional**" parecería implicar que el valor es opcional, y en realidad significa "puede ser `None`", incluso si no es opcional y sigue siendo requerido.

Creo que `Union[SomeType, None]` es más explícito respecto a lo que significa.

Se trata solo de palabras y nombres. Pero esas palabras pueden afectar cómo tú y tu equipo piensan sobre el código.

Como ejemplo, tomemos esta función:

```python
from typing import Optional


def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

El parámetro `name` está definido como `Optional[str]`, pero **no es opcional**, no puedes llamar a la función sin el parámetro:

```Python
say_hi()  # ¡Oh, no, esto lanza un error! 😱
```

El parámetro `name` **sigue siendo requerido** (no es *opcional*) porque no tiene un valor por defecto. Aun así, `name` acepta `None` como valor:

```Python
say_hi(name=None)  # Esto funciona, None es válido 🎉
```

La buena noticia es que, en la mayoría de los casos, podrás simplemente usar `|` para definir uniones de tipos:

```python
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

Así que, normalmente no tienes que preocuparte por nombres como `Optional` y `Union`. 😎
