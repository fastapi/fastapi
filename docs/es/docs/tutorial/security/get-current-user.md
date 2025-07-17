# Obtener Usuario Actual

En el capítulo anterior, el sistema de seguridad (que se basa en el sistema de inyección de dependencias) le estaba dando a la *path operation function* un `token` como un `str`:

{* ../../docs_src/security/tutorial001_an_py39.py hl[12] *}

Pero eso aún no es tan útil. Vamos a hacer que nos dé el usuario actual.

## Crear un modelo de usuario

Primero, vamos a crear un modelo de usuario con Pydantic.

De la misma manera que usamos Pydantic para declarar cuerpos, podemos usarlo en cualquier otra parte:

{* ../../docs_src/security/tutorial002_an_py310.py hl[5,12:6] *}

## Crear una dependencia `get_current_user`

Vamos a crear una dependencia `get_current_user`.

¿Recuerdas que las dependencias pueden tener sub-dependencias?

`get_current_user` tendrá una dependencia con el mismo `oauth2_scheme` que creamos antes.

De la misma manera que estábamos haciendo antes en la *path operation* directamente, nuestra nueva dependencia `get_current_user` recibirá un `token` como un `str` de la sub-dependencia `oauth2_scheme`:

{* ../../docs_src/security/tutorial002_an_py310.py hl[25] *}

## Obtener el usuario

`get_current_user` usará una función de utilidad (falsa) que creamos, que toma un token como un `str` y devuelve nuestro modelo de Pydantic `User`:

{* ../../docs_src/security/tutorial002_an_py310.py hl[19:22,26:27] *}

## Inyectar al usuario actual

Entonces ahora podemos usar el mismo `Depends` con nuestro `get_current_user` en la *path operation*:

{* ../../docs_src/security/tutorial002_an_py310.py hl[31] *}

Ten en cuenta que declaramos el tipo de `current_user` como el modelo de Pydantic `User`.

Esto nos ayudará dentro de la función con todo el autocompletado y chequeo de tipos.

/// tip | Consejo

Tal vez recuerdes que los cuerpos de request también se declaran con modelos de Pydantic.

Aquí **FastAPI** no se confundirá porque estás usando `Depends`.

///

/// check | Revisa

El modo en que este sistema de dependencias está diseñado nos permite tener diferentes dependencias (diferentes "dependables") que todas devuelven un modelo `User`.

No estamos restringidos a tener solo una dependencia que pueda devolver ese tipo de datos.

///

## Otros modelos

Ahora puedes obtener el usuario actual directamente en las *path operation functions* y manejar los mecanismos de seguridad a nivel de **Dependency Injection**, usando `Depends`.

Y puedes usar cualquier modelo o datos para los requisitos de seguridad (en este caso, un modelo de Pydantic `User`).

Pero no estás limitado a usar algún modelo de datos, clase o tipo específico.

¿Quieres tener un `id` y `email` y no tener un `username` en tu modelo? Claro. Puedes usar estas mismas herramientas.

¿Quieres solo tener un `str`? ¿O solo un `dict`? ¿O un instance de clase modelo de base de datos directamente? Todo funciona de la misma manera.

¿En realidad no tienes usuarios que inicien sesión en tu aplicación sino robots, bots u otros sistemas, que solo tienen un token de acceso? Una vez más, todo funciona igual.

Usa cualquier tipo de modelo, cualquier tipo de clase, cualquier tipo de base de datos que necesites para tu aplicación. **FastAPI** te cubre con el sistema de inyección de dependencias.

## Tamaño del código

Este ejemplo podría parecer extenso. Ten en cuenta que estamos mezclando seguridad, modelos de datos, funciones de utilidad y *path operations* en el mismo archivo.

Pero aquí está el punto clave.

El tema de seguridad e inyección de dependencias se escribe una vez.

Y puedes hacerlo tan complejo como desees. Y aún así, tenerlo escrito solo una vez, en un solo lugar. Con toda la flexibilidad.

Pero puedes tener miles de endpoints (*path operations*) usando el mismo sistema de seguridad.

Y todos ellos (o cualquier porción de ellos que quieras) pueden aprovechar la reutilización de estas dependencias o cualquier otra dependencia que crees.

Y todas estas miles de *path operations* pueden ser tan pequeñas como 3 líneas:

{* ../../docs_src/security/tutorial002_an_py310.py hl[30:32] *}

## Resumen

Ahora puedes obtener el usuario actual directamente en tu *path operation function*.

Ya estamos a mitad de camino.

Solo necesitamos agregar una *path operation* para que el usuario/cliente envíe realmente el `username` y `password`.

Eso es lo que viene a continuación.
