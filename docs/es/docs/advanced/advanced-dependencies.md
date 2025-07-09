# Dependencias Avanzadas

## Dependencias con parámetros

Todas las dependencias que hemos visto son una función o clase fija.

Pero podría haber casos en los que quieras poder establecer parámetros en la dependencia, sin tener que declarar muchas funciones o clases diferentes.

Imaginemos que queremos tener una dependencia que revise si el parámetro de query `q` contiene algún contenido fijo.

Pero queremos poder parametrizar ese contenido fijo.

## Una *instance* "callable"

En Python hay una forma de hacer que una instance de una clase sea un "callable".

No la clase en sí (que ya es un callable), sino una instance de esa clase.

Para hacer eso, declaramos un método `__call__`:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[12] *}

En este caso, este `__call__` es lo que **FastAPI** usará para comprobar parámetros adicionales y sub-dependencias, y es lo que llamará para pasar un valor al parámetro en tu *path operation function* más adelante.

## Parametrizar la instance

Y ahora, podemos usar `__init__` para declarar los parámetros de la instance que podemos usar para "parametrizar" la dependencia:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[9] *}

En este caso, **FastAPI** nunca tocará ni se preocupará por `__init__`, lo usaremos directamente en nuestro código.

## Crear una instance

Podríamos crear una instance de esta clase con:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[18] *}

Y de esa manera podemos "parametrizar" nuestra dependencia, que ahora tiene `"bar"` dentro de ella, como el atributo `checker.fixed_content`.

## Usar la instance como una dependencia

Luego, podríamos usar este `checker` en un `Depends(checker)`, en lugar de `Depends(FixedContentQueryChecker)`, porque la dependencia es la instance, `checker`, no la clase en sí.

Y al resolver la dependencia, **FastAPI** llamará a este `checker` así:

```Python
checker(q="somequery")
```

...y pasará lo que eso retorne como el valor de la dependencia en nuestra *path operation function* como el parámetro `fixed_content_included`:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[22] *}

/// tip | Consejo

Todo esto podría parecer complicado. Y puede que no esté muy claro cómo es útil aún.

Estos ejemplos son intencionalmente simples, pero muestran cómo funciona todo.

En los capítulos sobre seguridad, hay funciones utilitarias que se implementan de esta misma manera.

Si entendiste todo esto, ya sabes cómo funcionan por debajo esas herramientas de utilidad para seguridad.

///
