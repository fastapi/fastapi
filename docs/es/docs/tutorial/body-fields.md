# Los Campos del Cuerpo (Body - Fields)

De la misma forma que puedes declarar parámetros con `Query`, `Path` y `Body` para realizar validaciones adicionales y de metadatos en la <abbr title="path operation">ruta de operacion</abbr> de una función, es posible realizar dichas acciones desde los modelos de Pydantic usando `Field`.

## Importa `Field`

Primero se tiene que importar:

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

    `Body` también devuelve objetos que son subclase de `FieldInfo`. Más adelante verás además otros objetos que son subclase de `Body`.

    Recuerda que cuando importas `Query`, `Path`, y otros objetos desde `fastapi`, éstos son en realidad funciones que devuelven clases especiales.

!!! tip
Observa cómo el atributo de cada modelo con un tipo, valor por defecto y `Field`, tiene la misma estructura que el parámetro de una función de <abbr title="path operation">operación de ruta</abbr>, con `Field` en lugar de `Path`, `Query` y `Body`.

## Información adicional

Puedes declarar información adicional usando `Field`,` Query`, `Body`, etc. Y ésta será incluida en el esquema JSON generado.

Aprendrás mas sobre cómo añadir información extra más adelante, cuando veas cómo declarar ejemplos.

## Resumen

Puedes usar `Field` de Pydantic para declarar validaciones y metadatos adicionales para los atributos del modelo.

También puedes usar los argumentos de <abbr title="keyword arguments">palabras clave</abbr> para pasar metadatos de esquema JSON adicionales.
