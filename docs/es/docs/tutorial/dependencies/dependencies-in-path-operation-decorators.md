# Dependencias en decoradores de *path operation*

En algunos casos realmente no necesitas el valor de retorno de una dependencia dentro de tu *path operation function*.

O la dependencia no devuelve un valor.

Pero aún necesitas que sea ejecutada/resuelta.

Para esos casos, en lugar de declarar un parámetro de *path operation function* con `Depends`, puedes añadir una `list` de `dependencies` al decorador de *path operation*.

## Agregar `dependencies` al decorador de *path operation*

El decorador de *path operation* recibe un argumento opcional `dependencies`.

Debe ser una `list` de `Depends()`:

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[19] *}

Estas dependencias serán ejecutadas/resueltas de la misma manera que las dependencias normales. Pero su valor (si devuelven alguno) no será pasado a tu *path operation function*.

/// tip | Consejo

Algunos editores revisan los parámetros de función no usados y los muestran como errores.

Usando estas `dependencies` en el decorador de *path operation* puedes asegurarte de que se ejecutan mientras evitas errores en editores/herramientas.

También puede ayudar a evitar confusiones para nuevos desarrolladores que vean un parámetro no usado en tu código y puedan pensar que es innecesario.

///

/// info | Información

En este ejemplo usamos headers personalizados inventados `X-Key` y `X-Token`.

Pero en casos reales, al implementar seguridad, obtendrías más beneficios usando las [Utilidades de Seguridad integradas (el próximo capítulo)](../security/index.md){.internal-link target=_blank}.

///

## Errores de dependencias y valores de retorno

Puedes usar las mismas *funciones* de dependencia que usas normalmente.

### Requisitos de dependencia

Pueden declarar requisitos de request (como headers) u otras sub-dependencias:

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[8,13] *}

### Lanzar excepciones

Estas dependencias pueden `raise` excepciones, igual que las dependencias normales:

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[10,15] *}

### Valores de retorno

Y pueden devolver valores o no, los valores no serán usados.

Así que, puedes reutilizar una dependencia normal (que devuelve un valor) que ya uses en otro lugar, y aunque el valor no se use, la dependencia será ejecutada:

{* ../../docs_src/dependencies/tutorial006_an_py39.py hl[11,16] *}

## Dependencias para un grupo de *path operations*

Más adelante, cuando leas sobre cómo estructurar aplicaciones más grandes ([Aplicaciones Más Grandes - Múltiples Archivos](../../tutorial/bigger-applications.md){.internal-link target=_blank}), posiblemente con múltiples archivos, aprenderás cómo declarar un único parámetro `dependencies` para un grupo de *path operations*.

## Dependencias Globales

A continuación veremos cómo añadir dependencias a toda la aplicación `FastAPI`, de modo que se apliquen a cada *path operation*.
