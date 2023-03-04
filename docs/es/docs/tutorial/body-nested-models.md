# Cuerpo - Modelos Anidados

Con **FastAPI**, puedes definir, validar, documentar, y usar arbitrariamente modelos profundamente anidados (gracias a Pydantic).

## Campos de lista

Tu puedes definir un atributo para que sea un subtipo. Por ejemplo, una `list` de Python:

=== "Python 3.6 y superior"

    ```Python hl_lines="14"
    {!> ../../../docs_src/body_nested_models/tutorial001.py!}
    ```

=== "Python 3.10 y superior"

    ```Python hl_lines="12"
    {!> ../../../docs_src/body_nested_models/tutorial001_py310.py!}
    ```

Esto hará `tags` una lista, aunque no declara el tipo de los elementos de la lista.

## Campos de lista con tipo de parámetro

Pero Python tiene una forma específica de declarar listas with tipos internos, o "parámetros tipados":

### Importar `List` de `typing`

En Python 3.9 y superior tu puedes usar el estándar `list` para declarar estos tipos de anotaciones como veremos a continuación. 💡

Pero en versiones de Python previas a 3.9 (3.6 y superior), primero necesitas importar `List` desde el módulo estándar de Python `typing`:

```Python hl_lines="1"
{!> ../../../docs_src/body_nested_models/tutorial002.py!}
```

### Declarar una `list` con un parámetro tipado

Para declarar tipos que tienen parámetros tipados (tipos internos), como `list`, `dict`, `tuple`:

* Si estás en una version de Python inferior a 3.9, importa su versión equivalente desde el módulo `typing`
* Pasa el(los) tipo(s) interno(s) como "parámetros tipados" usando corchetes: `[` y `]`

En Python 3.9 sería:

```Python
my_list: list[str]
```

En versiones anteriores a Python 3.9, sería:

```Python
from typing import List

my_list: List[str]
```

Esta es toda la sintaxis estándar de Python para declaraciones tipadas.

Usa esta misma sintaxis estándar para atributos de modelos con tipos internos.

Entonces, en nuestro ejemplo, podemos hacer que `tags` sea especificamente una "lista de cadenas":

=== "Python 3.6 y superior"

    ```Python hl_lines="14"
    {!> ../../../docs_src/body_nested_models/tutorial002.py!}
    ```

=== "Python 3.9 y superior"

    ```Python hl_lines="14"
    {!> ../../../docs_src/body_nested_models/tutorial002_py39.py!}
    ```

=== "Python 3.10 y superior"

    ```Python hl_lines="12"
    {!> ../../../docs_src/body_nested_models/tutorial002_py310.py!}
    ```

## Tipo conjunto

Pero cuando pensamos en ello, y nos damos cuenta que tags no deberían repetirse, probablemente serian cadenas únicas.

Y Python tiene un tipo de dato especial para conjuntos de items únicos, el `set`.

Entonces podemos declarar `tags` como un conjunto de cadenas:

=== "Python 3.6 y superior"

    ```Python hl_lines="1  14"
    {!> ../../../docs_src/body_nested_models/tutorial003.py!}
    ```

=== "Python 3.9 y superior"

    ```Python hl_lines="14"
    {!> ../../../docs_src/body_nested_models/tutorial003_py39.py!}
    ```

=== "Python 3.10 y superior"

    ```Python hl_lines="12"
    {!> ../../../docs_src/body_nested_models/tutorial003_py310.py!}
    ```

Con esto, incluso si recibes una petición con data duplicada, será convertida en un conjunto de items únicos.

Y cada vez que muestres esa data, incluso si la fuente tiene duplicados, será mostrado como un conjunto de items únicos.

Y será anotado / documentado correspondientemente también.

## Modelos anidados

Cada atributo de un modelo Pydantic tiene un tipo.

Peor ese tipo puede él mismo ser otro modelo Pydantic.

Entonces, tu puedes declarar objetos JSON profundamente anidados con nombres de atributo específicos, tipos y validaciones.

Todo eso, anidado arbitrariamente.

### Definir un submodelo

Por ejemplo, podemos definir un modelo `Image`:

=== "Python 3.6 y superior"

    ```Python hl_lines="9-11"
    {!> ../../../docs_src/body_nested_models/tutorial004.py!}
    ```

=== "Python 3.9 y superior"

    ```Python hl_lines="9-11"
    {!> ../../../docs_src/body_nested_models/tutorial004_py39.py!}
    ```

=== "Python 3.10 y superior"

    ```Python hl_lines="7-9"
    {!> ../../../docs_src/body_nested_models/tutorial004_py310.py!}
    ```

### Usar el submodelo como un tipo

Y entonces podemos usarlo como el tipo de un atributo:

=== "Python 3.6 y superior"

    ```Python hl_lines="20"
    {!> ../../../docs_src/body_nested_models/tutorial004.py!}
    ```

=== "Python 3.9 y superior"

    ```Python hl_lines="20"
    {!> ../../../docs_src/body_nested_models/tutorial004_py39.py!}
    ```

=== "Python 3.10 y superior"

    ```Python hl_lines="18"
    {!> ../../../docs_src/body_nested_models/tutorial004_py310.py!}
    ```

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

De nuevo, haciendo solo la declaración, con **FastAPI** obtienes:

* Soporte del editor (completado, etc), incluso para modelos anidados
* Conversión de datos
* Validación de datos
* Documentación automática

## Tipos especiales y validación

Aparte de los tipos singulares normales como `str`, `int`, `float`, etc. Tu puedes usar tipos singulares más complejos que heredan de `str`.

Para ver todas las opciones que tienes, visita la documentación para <a href="https://pydantic-docs.helpmanual.io/usage/types/" class="external-link" target="_blank">Tipos exóticos de Pydantic</a>. Verás algunos ejemplos en el siguiente capítulo.

Por ejemplo, como en el modelo `Image` tenemos un campo `url`, podemos declararlo para que sea en vez de un `str`, un `HttpUrl` de Pydantic:

=== "Python 3.6 y superior"

    ```Python hl_lines="4  10"
    {!> ../../../docs_src/body_nested_models/tutorial005.py!}
    ```

=== "Python 3.9 y superior"

    ```Python hl_lines="4  10"
    {!> ../../../docs_src/body_nested_models/tutorial005_py39.py!}
    ```

=== "Python 3.10 y superior"

    ```Python hl_lines="2  8"
    {!> ../../../docs_src/body_nested_models/tutorial005_py310.py!}
    ```

La cadena se verificará que sea una URL valida, y documentada en el Esquema JSON / OpenAPI como tal.

## Atributos con listas de submodelos

También puedes usar modelos Pydantic como subtipos de `list`, `set`, etc:

=== "Python 3.6 y superior"

    ```Python hl_lines="20"
    {!> ../../../docs_src/body_nested_models/tutorial006.py!}
    ```

=== "Python 3.9 y superior"

    ```Python hl_lines="20"
    {!> ../../../docs_src/body_nested_models/tutorial006_py39.py!}
    ```

=== "Python 3.10 y superior"

    ```Python hl_lines="18"
    {!> ../../../docs_src/body_nested_models/tutorial006_py310.py!}
    ```

Esto esperará (convertirá, validará, documentará, etc) un cuerpo JSON como:

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

!!! info
    Nota cómo la clave `images` ahora tiene una lista de objetos `Image`.

## Modelos profundamente anidados

Puedes definir arbitrariamente modelos profundamente anidados:

=== "Python 3.6 y superior"

    ```Python hl_lines="9  14  20  23  27"
    {!> ../../../docs_src/body_nested_models/tutorial007.py!}
    ```

=== "Python 3.9 y superior"

    ```Python hl_lines="9  14  20  23  27"
    {!> ../../../docs_src/body_nested_models/tutorial007_py39.py!}
    ```

=== "Python 3.10 y superior"

    ```Python hl_lines="7  12  18  21  25"
    {!> ../../../docs_src/body_nested_models/tutorial007_py310.py!}
    ```

!!! info
    Nota cómo `Offer` tiene una lista de `Item`s, que a su vez tienen una lista opcional de `Image`s

## Cuerpos de puras listas

Si el valor de nivel superior del cuerpo JSON que esperas es un `array` JSON (una `list` de Python), puedes declarar el tipo en el parámetro de la función, lo mismo que en modelos Pydantic:

```Python
images: List[Image]
```

o en Python 3.9 y superior:

```Python
images: list[Image]
```

como en:

=== "Python 3.6 y superior"

    ```Python hl_lines="15"
    {!> ../../../docs_src/body_nested_models/tutorial008.py!}
    ```

=== "Python 3.9 y superior"

    ```Python hl_lines="13"
    {!> ../../../docs_src/body_nested_models/tutorial008_py39.py!}
    ```

## Soporte para el editor en todas partes

Y obtienes soporte para tu editor en todas partes.

Incluso para items dentro de listas:

<img src="/img/tutorial/body-nested-models/image01.png">

No podrías obtener este tipo de soporte para el editor si estuvieras trabajando directamente con `dict` en lugar de modelos Pydantic.

Pero no te tienes que preocupar acerca de ellos tampoco, los diccionarios que entran son convertidos automaticamente y tu salida es convertida automaticamente a JSON también.

## Cuerpos de `dict`s arbitrarios

También puedes declarar un cuerpo como un `dict` con claves de algún tipo y valores de otro tipo.

Sin tener que saber de antemano cuáles son los nombres válidos de cada campo/atributo  (como seri3a el caso con modelos Pydantic).

Esto sería útil si tu quieres recibir claves que tu no aún no conoces.

---

Otro caso útil es cuando quieres tener claves de otro tipo, p.ej. `int`.

Esto es lo que vamos a ver aquí.

En este caso, tu aceptarías cualquier `dict` mientras tenga claves `int` con valores `float`:

=== "Python 3.6 y superior"

    ```Python hl_lines="9"
    {!> ../../../docs_src/body_nested_models/tutorial009.py!}
    ```

=== "Python 3.9 y superior"

    ```Python hl_lines="7"
    {!> ../../../docs_src/body_nested_models/tutorial009_py39.py!}
    ```

!!! tip
    Recuerda que JSON solo soporta `str` como claves.

    Pero Pydantic tiene conversión automática de datos.

    Esto significa que, incluso aunque los clientes de tu API solo pueden enviar cadenas como claves, mientras estas cadenas contengan puros enteros, Pydantic los convertirá y los validará.

    Y el `dict` que recibes como `weights` de hecho tendrá claves `int` y valores `float`.

## Resumen

Con **FastAPI** tienes la máxima flexibilidad provista por modelos Pydantic, mientras mantienes tu código simple, corto y elegante.

Pero con todos los beneficios:

* Soporte de editor (¡completado en todas partes!)
* Conversión de datos (también conocido como análisis / serialización)
* Validación de datos
* Documentación de esquemas
* Documentación automática
