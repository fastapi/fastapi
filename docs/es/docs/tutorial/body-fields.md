# Body - Campos

De la misma manera que puedes declarar validaciones adicionales y metadatos en los parámetros de las *path operation function* con `Query`, `Path` y `Body`, puedes declarar validaciones y metadatos dentro de los modelos de Pydantic usando `Field` de Pydantic.

## Importar `Field`

Primero, tienes que importarlo:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[4] *}

/// warning | Advertencia

Fíjate que `Field` se importa directamente desde `pydantic`, no desde `fastapi` como el resto (`Query`, `Path`, `Body`, etc).

///

## Declarar atributos del modelo

Después puedes utilizar `Field` con los atributos del modelo:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[11:14] *}

`Field` funciona de la misma manera que `Query`, `Path` y `Body`, tiene todos los mismos parámetros, etc.

/// note | Detalles técnicos

En realidad, `Query`, `Path` y otros que verás a continuación crean objetos de subclases de una clase común `Param`, que es a su vez una subclase de la clase `FieldInfo` de Pydantic.

Y `Field` de Pydantic también regresa una instance de `FieldInfo`.

`Body` también devuelve objetos de una subclase de `FieldInfo` directamente. Y hay otros que verás más adelante que son subclases de la clase `Body`.

Recuerda que cuando importas `Query`, `Path`, y otros desde `fastapi`, en realidad son funciones que devuelven clases especiales.

///

/// tip | Consejo

Observa cómo cada atributo del modelo con un tipo, un valor por defecto y `Field` tiene la misma estructura que un parámetro de una *path operation function*, con `Field` en lugar de `Path`, `Query` y `Body`.

///

## Agregar información extra

Puedes declarar información extra en `Field`, `Query`, `Body`, etc. Y será incluida en el JSON Schema generado.

Aprenderás más sobre cómo agregar información extra más adelante en la documentación, cuando aprendamos a declarar ejemplos.

/// warning | Advertencia

Las claves extra pasadas a `Field` también estarán presentes en el esquema de OpenAPI resultante para tu aplicación.
Como estas claves no necesariamente tienen que ser parte de la especificación de OpenAPI, algunas herramientas de OpenAPI, por ejemplo [el validador de OpenAPI](https://validator.swagger.io/), podrían no funcionar con tu esquema generado.

///

## Resumen

Puedes utilizar `Field` de Pydantic para declarar validaciones adicionales y metadatos para los atributos del modelo.

También puedes usar los argumentos de palabra clave extra para pasar metadatos adicionales del JSON Schema.
