# Cuerpo - Múltiples Parámetros

Ahora que ya hemos visto cómo utilizar `Path` y `Query`, vamos a ver usos más avanzados de declaraciones de peticiones con cuerpo.

## Mezclando `Path`, `Query` y parámetros en el cuerpo

Primero, por supuesto que puedes mezclar `Path`, `Query` y declaraciones de parámetros en el cuerpo de una petición libremente y **FastAPI** sabrá qué hacer.

Al igual que también puedes declarar parámetros en el cuerpo opcionales, indicando `None` como valor por defecto:

```Python hl_lines="19-21"
{!../../../docs_src/body_multiple_params/tutorial001.py!}
```

!!! note
Ten en cuenta que en este caso, el campo `item` del cuerpo de la petición, es opcional. Ya que contiene `None` como valor por defecto.

## Múltiples parámetros en el cuerpo

En los ejemplos anteriores, las <abbr title="path operation">operaciones en rutas</abbr> estarían esperando un <abbr title="JSON body">cuerpo JSON</abbr> con atributos de `Item`, como:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

Además podrías declarar múltiples parámetros en el cuerpo, por ejemplo: `item` y `user`:

```Python hl_lines="22"
{!../../../docs_src/body_multiple_params/tutorial002.py!}
```

En este caso, **FastAPI** se dará cuenta de que hay más de un parámetro en el cuerpo dentro de la función (dos parámetros que son modelos de Pydantic).

Entonces, se utilizarán los nombres de los parámetros como <abbr title=keys>claves</abbr> en el cuerpo, y se esperará un cuerpo como este:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

!!! note
Ten en cuenta que aunque `item` fue declarado de la misma forma que anteriormente, ahora se espera que se encuentre dentro del cuerpo con la <abbr title=keys>clave</abbr> `item`.

**FastAPI** hará la conversión automáticamente desde la petición, entonces el parámetro `item` al igual que `user`, recibirán ambos su contenido específico.

Se realizará la validación de los datos compuestos, y será documentado de esa forma en el esquema de OpenAPI y en la documentación automática.

## Valores singulares en el cuerpo

De la misma forma que existem `Query` y `Path` para definir información adicional para la ruta y los parámetros, **FastAPI** proporciona un `Body` equivalente.

Por ejemplo, ampliando el modelo anterior, podrías decidir que te gustaría tener la <abbr title=key>clave</abbr> `importance` en el mismo cuerpo, además de `item` y `user`.

Si lo declaras de esta forma, debido a que es un valor singular, **FastAPI** asumirá que se trata de un <abbr title="query parameter">parámetro en la consulta</abbr>.

También puedes enseñar a **FastAPI** a tratarlo como otra clave del cuerpo usando `Body`:

```Python hl_lines="23"
{!../../../docs_src/body_multiple_params/tutorial003.py!}
```

En este caso, **FastAPI** esperará un cuerpo como este:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

Nuevamente, los tipos de datos serán convertidos, validados, documentados, etc.

## Múltiples parámetros en el cuerpo y consulta

Puedes declarar parámetros adicionales de consulta en cualquier parte que lo necesites, además de los parámetros en el cuerpo.

Ya que los valores singulares son interpretados como parámetros de consulta, no tienes que añadir `Query` de forma explícita, sino que solo tienes que hacer:

```Python
q: Optional[str] = None
```

como en:

```Python hl_lines="27"
{!../../../docs_src/body_multiple_params/tutorial004.py!}
```

!!! info
`Body` al igual que `Query`, `Path` y otros que verás mas adelante, también tiene todas las validaciones adicionales y parámetros de metadatos.

## Incrustar un parámetro en el cuerpo

Digamos que tienes un solo parámetro en el cuerpo `item` del modelo de Pydantic `Item`.

Por defecto, **FastAPI** esperará el cuerpo directamente.

Pero si prefieres utilizar un JSON con una <abbr title=key>clave</abbr> dentro del contenido del modelo, al igual que se hace cuando declaras un parámetro adicional en el cuerpo, puedes usar el parámetro especial `embed` de `Body`:

```Python
item: Item = Body(..., embed=True)
```

como en:

```Python hl_lines="17"
{!../../../docs_src/body_multiple_params/tutorial005.py!}
```

En este caso **FastAPI** esperará un cuerpo como este:

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

En lugar de:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## Recap

Puedes añadir a la <Abrr title="path operation function">función de operación en ruta</abbr> mútiples parámetros en el cuerpo, incluso aunque una petición pueda contener solo un cuerpo.

Sin embargo, **FastAPI** lo procesará, pasará los datos correctos a la función, validará y documentará el esquema correcto en la <Abrr title=path operation function>ruta de la operación</abbr>.

También puedes declarar valores singulares que serán recibidos como parte del cuerpo.

Y puedes pedir a **FastAPI** que incruste el cuerpo en la <Abrr title=key>clave</abbr>, incluso cuando haya un solo parámetro declarado.
