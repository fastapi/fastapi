# Cuerpo - Múltiples Parámetros

Ahora que hemos visto cómo usar `Path` y `Query`, veamos usos más avanzados de las declaraciones del request body.

## Mezclar `Path`, `Query` y parámetros del cuerpo

Primero, por supuesto, puedes mezclar las declaraciones de parámetros de `Path`, `Query` y del request body libremente y **FastAPI** sabrá qué hacer.

Y también puedes declarar parámetros del cuerpo como opcionales, estableciendo el valor predeterminado a `None`:

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

## Múltiples parámetros del cuerpo

/// note | Nota

Ten en cuenta que, en este caso, el `item` que se tomaría del cuerpo es opcional. Ya que tiene un valor por defecto de `None`.

///

## Múltiples parámetros del cuerpo

En el ejemplo anterior, las *path operations* esperarían un cuerpo JSON con los atributos de un `Item`, como:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

Pero también puedes declarar múltiples parámetros del cuerpo, por ejemplo `item` y `user`:

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}

En este caso, **FastAPI** notará que hay más de un parámetro del cuerpo en la función (hay dos parámetros que son modelos de Pydantic).

Entonces, usará los nombres de los parámetros como claves (nombres de campo) en el cuerpo, y esperará un cuerpo como:

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

/// note | Nota

Ten en cuenta que aunque el `item` se declaró de la misma manera que antes, ahora se espera que esté dentro del cuerpo con una clave `item`.

///

**FastAPI** hará la conversión automática del request, de modo que el parámetro `item` reciba su contenido específico y lo mismo para `user`.

Realizará la validación de los datos compuestos, y los documentará así para el esquema de OpenAPI y la documentación automática.

## Valores singulares en el cuerpo

De la misma manera que hay un `Query` y `Path` para definir datos extra para parámetros de query y path, **FastAPI** proporciona un equivalente `Body`.

Por ejemplo, ampliando el modelo anterior, podrías decidir que deseas tener otra clave `importance` en el mismo cuerpo, además de `item` y `user`.

Si lo declaras tal cual, debido a que es un valor singular, **FastAPI** asumirá que es un parámetro de query.

Pero puedes instruir a **FastAPI** para que lo trate como otra clave del cuerpo usando `Body`:

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}

En este caso, **FastAPI** esperará un cuerpo como:

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

Nuevamente, convertirá los tipos de datos, validará, documentará, etc.

## Múltiples parámetros de cuerpo y query

Por supuesto, también puedes declarar parámetros adicionales de query siempre que lo necesites, además de cualquier parámetro del cuerpo.

Como, por defecto, los valores singulares se interpretan como parámetros de query, no tienes que añadir explícitamente un `Query`, solo puedes hacer:

```Python
q: Union[str, None] = None
```

O en Python 3.10 y superior:

```Python
q: str | None = None
```

Por ejemplo:

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}

/// info | Información

`Body` también tiene todos los mismos parámetros de validación y metadatos extras que `Query`, `Path` y otros que verás luego.

///

## Embeber un solo parámetro de cuerpo

Supongamos que solo tienes un único parámetro de cuerpo `item` de un modelo Pydantic `Item`.

Por defecto, **FastAPI** esperará su cuerpo directamente.

Pero si deseas que espere un JSON con una clave `item` y dentro de ella los contenidos del modelo, como lo hace cuando declaras parámetros de cuerpo extra, puedes usar el parámetro especial `Body` `embed`:

```Python
item: Item = Body(embed=True)
```

como en:

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}

En este caso, **FastAPI** esperará un cuerpo como:

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

en lugar de:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## Resumen

Puedes añadir múltiples parámetros de cuerpo a tu *path operation function*, aunque un request solo puede tener un único cuerpo.

Pero **FastAPI** lo manejará, te dará los datos correctos en tu función, y validará y documentará el esquema correcto en la *path operation*.

También puedes declarar valores singulares para ser recibidos como parte del cuerpo.

Y puedes instruir a **FastAPI** para embeber el cuerpo en una clave incluso cuando solo hay un único parámetro declarado.
