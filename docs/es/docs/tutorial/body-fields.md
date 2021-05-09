# Los Campos del Cuerpo (Body - Fields)

De la misma forma que puedes declarar parámetros con `Query`, `Path` y `Body` para realizar validaciones adicionales y de metadatos en la ruta de operacion (_path operation_) de una función, es posible realizar dichas acciones desde los modelos de Pydantic usando `Field`.

## Importa `Field`

Primero, importa Field:

```Python hl_lines="4"
{!../../../docs_src/body_fields/tutorial001.py!}
```

!!! warning
Ten en cuenta que `Field` se importa directamente desde `pydantic`, no desde `fastapi` como sí se hace con (`Query`, `Path`, `Body`, etc).

## Declara los atributos del modelo

Puedes usar `Field` con los atributos de un modelo:

```Python hl_lines="11-14"
{!../../../docs_src/body_fields/tutorial001.py!}
```

`Field` funciona de la misma forma que `Query`, `Path` y `Body`, y además cuenta con los mismos parámetros.

!!! note "Detalles Técnicos"
`Query`, `Path` y otros objetos que verás mas adelante, son en realidad subclases de una clase común llamada `Param`, que a su vez es una subclase de la clase `FieldInfo` de Pydantic.

    De la misma forma, el objeto `Field` devolverá una instancia de `FieldInfo`.

    Igual que otros que verás mas adelante, `Body` también devuelve objetos que son subclase de `FieldInfo`.

    Recuerda que cuando importas `Query`, `Path`, y otros objetos desde `fastapi`, éstos son en realidad funciones que devuelven clases especiales.

!!! tip
Observa cómo el atributo de cada modelo con un tipo, valor por defecto y `Field`, tiene la misma estructura que el parámetro de una función de operación de ruta (_path operation_), con `Field` en lugar de `Path`, `Query` y `Body`.

## Información adicional

Puedes declarar información adicional usando `Field`,` Query`, `Body`, etc. Y ésta será incluida en el esquema JSON generado.

Aprendrás mas sobre cómo añadir información extra más adelante, cuando veas cómo declarar ejemplos.

## Resumen

Puedes usar `Field` de Pydantic para declarar validaciones y metadatos adicionales para los atributos del modelo.

También puedes usar los argumentos de palabras clave (_keyword arguments_) para pasar metadatos de esquema JSON adicionales.
