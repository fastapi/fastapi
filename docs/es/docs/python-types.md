# Introducción a los Tipos de Python

**Python 3.6+** tiene soporte para <abbr title="en español, anotaciones de tipo. En inglés también se conocen como: type annotations">"type hints"</abbr> opcionales.

Estos **type hints** son una nueva sintáxis, desde Python 3.6+, que permite declarar el <abbr title="por ejemplo: str, int, float, bool">tipo</abbr> de una variable.

Usando las declaraciones de tipos para las variables, los editores y otras herramientas pueden proveerte un soporte mejor.

Este es solo un **tutorial corto** sobre los Python type hints. Solo cubre lo mínimo necesario para usarlos con **FastAPI**... Ya que realmente es muy poco lo que necesitas.

Todo **FastAPI** está basado en estos type hints, lo que le da muchas ventajas y beneficios.

Pero, así nunca uses **FastAPI**, también te beneficiarás de aprender un poco sobre type hints.

NOTA: Si eres un experto en Python y ya sabes todo sobre los type hints, puedes saltar al siguiente capítulo.

## Motivación

Comencemos con un ejemplo simple:

```Python
def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
    return full_name


print(get_full_name("john", "doe"))
```

Llamar este programa nos muestra el siguiente <abbr title="en español: salida">output</abbr>:

```
John Doe
```

La función hace lo siguiente:

* Toma un `first_name` y un `last_name`.
* Convierte la primera letra de cada uno en una letra mayúscula con `title()`.
* Las <abbr title="las junta como si fuesen una. Con el contenido de una después de la otra. En inlgés: concatenate.">concatena</abbr> con un espacio en la mitad.

```Python
def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
```

### Edítalo

Es un programa muy simple.

Ahora, imagina que lo estás escribiendo desde cero.

En algún punto habrías comenzado con la definición de la función, tenías los parámetros listos...

Pero, luego tienes que llamar "ese método que convierte la primera letra en una mayúscula".

Era `upper`? O era `uppercase`? `first_uppercase`? `capitalize`?

Luego lo intentas con el viejo amigo de los programadores, el autocompletado del editor.

Escribes el primer parámetro de la función `first_name`, luego un punto (`.`) y luego presionas `Ctrl+Space` para iniciar el autocompletado.

Tristemente, no obtienes nada útil:

<img src="https://fastapi.tiangolo.com/img/python-types/image01.png">

### Añade tipos

Vamos a modificar una única línea de la versión previa.

Vamos a cambiar exactamente este fragmento, los parámetros de la función, de:

```python
first_name, last_name
```

a:

```Python
first_name: str, last_name: str
```

Eso es todo.

Esos son los "type hints":

```Python
def get_full_name(first_name: str, last_name: str):
```

No es lo mismo a declarar valores por defecto, como sería con:

```Python
first_name="john", last_name="doe"
```

Es algo diferente.

Estamos usando los dos puntos (`:`), no un símbolo de igual (`=`).

Añadir los type hints normalmente no cambia lo que sucedería si ellos no estuviesen presentes.

Pero ahora imagina que nuevamente estás creando la función, pero con los type hints.

En el mismo punto intentas iniciar el autocompletado con `Ctrl+Space` y ves:

<img src="https://fastapi.tiangolo.com/img/python-types/image02.png">

Con esto puedes moverte hacia abajo viendo las opciones hasta que encuentras una que te suene:

<img src="https://fastapi.tiangolo.com/img/python-types/image03.png">

## Más motivación

Mira esta función que ya tiene type hints:

```Python
def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + age
    return name_with_age

```

Como el editor conoce el tipo de las variables no solo obtienes autocompletado, si no que también obtienes chequeo de errores:

<img src="https://fastapi.tiangolo.com/img/python-types/image04.png">

Ahora que sabes que tienes que arreglarlo convierte `age` a un string con `str(age)`:

```Python
def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + str(age)
    return name_with_age
```

## Declarando tipos

Acabas de ver el lugar principal para declarar los type hints. Como parámetros de las funciones.

Este es también el lugar principal en que los usarías con  **FastAPI**.

### Tipos simples

Puedes declarar todos los tipos estándar de Python, no solamente  `str`.

Por ejemplo, puedes usar:

* `int`
* `float`
* `bool`
* `bytes`

```Python
def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
```

### Tipos con sub-tipos

Existen algunas estructuras de datos que pueden contener otros valores, como `dict`, `list`, `set` y `tuple`. Los valores internos pueden tener su propio tipo también.

Para declarar esos tipos y sub-tipos puedes usar el módulo estándar de Python `typing`.

Dicho módulo existe específicamente para dar soporte a este tipo de type hints.

#### Listas

Por ejemplo, vamos a definir una variable para que sea una `list` compuesta de `str`.

De `typing`, importa `List` (con una `L` mayúscula):

```Python
from typing import List
```

Declara la variable con la misma sintáxis de los dos puntos (`:`).

Pon `List` como el tipo.

Como la lista es un tipo que permite tener un "sub-tipo" pones el sub-tipo en corchetes `[]`:

```Python hl_lines="4"
def process_items(items: List[str]):
    for item in items:
        print(item)
```

Esto significa: la variable `items` es una `list` y cada uno de los ítems en esta lista es un `str`.

Con esta declaración tu editor puede proveerte soporte inclusive mientras está procesando ítems de la lista.

Sin tipos el autocompletado en este tipo de estructura es casi imposible de lograr:

<img src="https://fastapi.tiangolo.com/img/python-types/image05.png">

Observa que la variable `item` es unos de los elementos en la lista `items`.

El editor aún sabe que es un `str` y provee soporte para ello.

#### Tuples y Sets

Harías lo mismo para declarar `tuple`s y `set`s:

```Python
from typing import Set, Tuple


def process_items(items_t: Tuple[int, int, str], items_s: Set[bytes]):
    return items_t, items_s
```

Esto significa:

* La variable `items_t` es un `tuple` con 3 ítems, un `int`, otro `int`, y un `str`.
* La variable `items_s` es un `set` y cada uno de sus ítems es de tipo `bytes`.

#### Diccionarios (Dicts)

Para definir un `dict` le pasas 2 sub-tipos separados por comas.

El primer sub-tipo es para los keys del `dict`.

El segundo sub-tipo es para los valores del `dict`:

```Python
from typing import Dict


def process_items(prices: Dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)
```

Esto significa:

* La variable `prices` es un `dict`:
    * Los keys de este `dict` son de tipo `str` (Digamos que son el nombre de cada ítem).
    * Los valores de este `dict` son de tipo `float` (Digamos que son el precio de cada ítem).

**NOTA**: A partir de python 3.9+ ya no es necesario importar desde typing para agregar subtipos.

Solo basta con hacer algo como lo siguiente:
```Python
def process_items(
    items: list[str], prices: dict[str, float],
    items_t: tuple[int, int, str], items_s: set[bytes]
):
```

### Clases como tipos

También puedes declarar una clase como el tipo de una variable.

Digamos que tienes una clase `Person` con la propiedad `name`:

```Python
class Person:
    def __init__(self, name: str):
        self.name = name
```

Entonces puedes declarar una variable que sea de tipo `Person`:

```Python
def get_person_name(one_person: Person):
    return one_person.name
```

Una vez más tendrás todo el soporte del editor:

<img src="https://fastapi.tiangolo.com/img/python-types/image06.png">

## Modelos de Pydantic

<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> es una libreria de Python utilizada para llevar a cabo validación de datos.

Tú declaras la "forma" de los datos mediante clases con atributos.

Cada atributo tiene un tipo.

Luego creas un instancia de esa clase con algunos valores y Pydantic los validará, los convertirá al tipo apropiado (si ese es el caso) y te dará un objeto con todos los datos.

Así obtienes todo el soporte del editor con el objeto resultante.

Tomado de la documentación oficial de Pydantic:

```Python
from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []


external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}
user = User(**external_data)
print(user)
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
# > 123
```


Para aprender más sobre **Pydantic** <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank"> mira su documentación</a>.

Puede que te sea de mucha utilidad debido a que **FastAPI** está completamente basado en Pydantic.

Vas a ver mucho más de esto en práctica en el [Tutorial - Guia de usuario](tutorial/index.md)

## Type hints en **FastAPI**

**FastAPI** aprovecha estos type hints para hacer varias cosas.

Con **FastAPI** declaras los parámetros con type hints y obtienes:

* **Soporte en el editor**.
* **Validación de tipos**.

Además, **FastAPI** usa los mismos tipos declarados para:

* **Definir requerimientos**: desde request path parameters, query parameters, headers, bodies, dependencies, etc.
* **Convertir datos**: desde el request al tipo requerido.
* **Validar datos**: viniendo de cada request:
    * Generando **errores automáticos** devueltos al cliente cuando los datos son inválidos.
* **Documentar** la API usando OpenAPI:
    * Que en su caso es usada por las interfaces de usuario de la documentación automática e interactiva.

Puede que todo esto suene abstracto. Pero no te preocupes, todo puedes verlo en acción en el [Tutorial - Guia de usuario](tutorial/index.md).

Lo importante es que usando el tipado de datos estándar de Python en un único lugar (en vez de añadir más clases, decoradores, etc.) **FastAPI** hará mucho del trabajo por ti.

**Información**
    Si ya pasaste por todo el tutorial y volviste a la sección de los tipos, una buena referencia es <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">la documentación sobre `mypy`</a>.
