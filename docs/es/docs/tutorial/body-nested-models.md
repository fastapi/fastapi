# Cuerpo - Modelos Anidados

Con **FastAPI**, puedes definir, validar, documentar y usar modelos anidados de manera arbitraria (gracias a Pydantic).

## Campos de lista

Puedes definir un atributo como un subtipo. Por ejemplo, una `list` en Python:

{* ../../docs_src/body_nested_models/tutorial001_py310.py hl[12] *}

Esto hará que `tags` sea una lista, aunque no declare el tipo de los elementos de la lista.

## Campos de lista con parámetro de tipo

Pero Python tiene una forma específica de declarar listas con tipos internos, o "parámetros de tipo":

### Importar `List` de typing

En Python 3.9 y superior, puedes usar el `list` estándar para declarar estas anotaciones de tipo como veremos a continuación. 💡

Pero en versiones de Python anteriores a 3.9 (desde 3.6 en adelante), primero necesitas importar `List` del módulo `typing` estándar de Python:

{* ../../docs_src/body_nested_models/tutorial002.py hl[1] *}

### Declarar una `list` con un parámetro de tipo

Para declarar tipos que tienen parámetros de tipo (tipos internos), como `list`, `dict`, `tuple`:

* Si estás en una versión de Python inferior a 3.9, importa su versión equivalente del módulo `typing`
* Pasa el/los tipo(s) interno(s) como "parámetros de tipo" usando corchetes: `[` y `]`

En Python 3.9 sería:

```Python
my_list: list[str]
```

En versiones de Python anteriores a 3.9, sería:

```Python
from typing import List

my_list: List[str]
```

Eso es toda la sintaxis estándar de Python para declaraciones de tipo.

Usa esa misma sintaxis estándar para atributos de modelos con tipos internos.

Así, en nuestro ejemplo, podemos hacer que `tags` sea específicamente una "lista de strings":

{* ../../docs_src/body_nested_models/tutorial002_py310.py hl[12] *}

## Tipos de conjunto

Pero luego pensamos en ello, y nos damos cuenta de que los tags no deberían repetirse, probablemente serían strings únicos.

Y Python tiene un tipo de datos especial para conjuntos de elementos únicos, el `set`.

Entonces podemos declarar `tags` como un conjunto de strings:

{* ../../docs_src/body_nested_models/tutorial003_py310.py hl[12] *}

Con esto, incluso si recibes un request con datos duplicados, se convertirá en un conjunto de elementos únicos.

Y siempre que emitas esos datos, incluso si la fuente tenía duplicados, se emitirá como un conjunto de elementos únicos.

Y también se anotará/documentará en consecuencia.

## Modelos Anidados

Cada atributo de un modelo Pydantic tiene un tipo.

Pero ese tipo puede ser en sí mismo otro modelo Pydantic.

Así que, puedes declarar "objetos" JSON anidados profundamente con nombres de atributos específicos, tipos y validaciones.

Todo eso, de manera arbitraria.

### Definir un submodelo

Por ejemplo, podemos definir un modelo `Image`:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[7:9] *}

### Usar el submodelo como tipo

Y luego podemos usarlo como el tipo de un atributo:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[18] *}

Esto significaría que **FastAPI** esperaría un cuerpo similar a:

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

Nuevamente, haciendo solo esa declaración, con **FastAPI** obtienes:

* Soporte de editor (autocompletado, etc.), incluso para modelos anidados
* Conversión de datos
* Validación de datos
* Documentación automática

## Tipos especiales y validación

Además de tipos singulares normales como `str`, `int`, `float`, etc., puedes usar tipos singulares más complejos que heredan de `str`.

Para ver todas las opciones que tienes, revisa el <a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">Overview de Tipos de Pydantic</a>. Verás algunos ejemplos en el siguiente capítulo.

Por ejemplo, como en el modelo `Image` tenemos un campo `url`, podemos declararlo como una instance de `HttpUrl` de Pydantic en lugar de un `str`:

{* ../../docs_src/body_nested_models/tutorial005_py310.py hl[2,8] *}

El string será verificado para ser una URL válida, y documentado en JSON Schema / OpenAPI como tal.

## Atributos con listas de submodelos

También puedes usar modelos Pydantic como subtipos de `list`, `set`, etc.:

{* ../../docs_src/body_nested_models/tutorial006_py310.py hl[18] *}

Esto esperará (convertirá, validará, documentará, etc.) un cuerpo JSON como:

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

/// info | Información

Nota cómo la clave `images` ahora tiene una lista de objetos de imagen.

///

## Modelos anidados profundamente

Puedes definir modelos anidados tan profundamente como desees:

{* ../../docs_src/body_nested_models/tutorial007_py310.py hl[7,12,18,21,25] *}

/// info | Información

Observa cómo `Offer` tiene una lista de `Item`s, que a su vez tienen una lista opcional de `Image`s

///

## Cuerpos de listas puras

Si el valor superior del cuerpo JSON que esperas es un `array` JSON (una `list` en Python), puedes declarar el tipo en el parámetro de la función, al igual que en los modelos Pydantic:

```Python
images: List[Image]
```

o en Python 3.9 y superior:

```Python
images: list[Image]
```

como en:

{* ../../docs_src/body_nested_models/tutorial008_py39.py hl[13] *}

## Soporte de editor en todas partes

Y obtienes soporte de editor en todas partes.

Incluso para elementos dentro de listas:

<img src="/img/tutorial/body-nested-models/image01.png">

No podrías obtener este tipo de soporte de editor si estuvieras trabajando directamente con `dict` en lugar de modelos Pydantic.

Pero tampoco tienes que preocuparte por ellos, los `dicts` entrantes se convierten automáticamente y tu salida se convierte automáticamente a JSON también.

## Cuerpos de `dict`s arbitrarios

También puedes declarar un cuerpo como un `dict` con claves de algún tipo y valores de algún otro tipo.

De esta manera, no tienes que saber de antemano cuáles son los nombres válidos de campo/atributo (como sería el caso con modelos Pydantic).

Esto sería útil si deseas recibir claves que aún no conoces.

---

Otro caso útil es cuando deseas tener claves de otro tipo (por ejemplo, `int`).

Eso es lo que vamos a ver aquí.

En este caso, aceptarías cualquier `dict` siempre que tenga claves `int` con valores `float`:

{* ../../docs_src/body_nested_models/tutorial009_py39.py hl[7] *}

/// tip | Consejo

Ten en cuenta que JSON solo admite `str` como claves.

Pero Pydantic tiene conversión automática de datos.

Esto significa que, aunque tus clientes de API solo pueden enviar strings como claves, mientras esos strings contengan enteros puros, Pydantic los convertirá y validará.

Y el `dict` que recibas como `weights` tendrá realmente claves `int` y valores `float`.

///

## Resumen

Con **FastAPI** tienes la máxima flexibilidad proporcionada por los modelos Pydantic, manteniendo tu código simple, corto y elegante.

Pero con todos los beneficios:

* Soporte de editor (¡autocompletado en todas partes!)
* Conversión de datos (también conocido como parsing/serialización)
* Validación de datos
* Documentación del esquema
* Documentación automática
