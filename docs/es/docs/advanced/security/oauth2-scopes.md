# Scopes de OAuth2

Puedes usar scopes de OAuth2 directamente con **FastAPI**, están integrados para funcionar de manera fluida.

Esto te permitiría tener un sistema de permisos más detallado, siguiendo el estándar de OAuth2, integrado en tu aplicación OpenAPI (y la documentación de la API).

OAuth2 con scopes es el mecanismo usado por muchos grandes proveedores de autenticación, como Facebook, Google, GitHub, Microsoft, X (Twitter), etc. Lo usan para proporcionar permisos específicos a usuarios y aplicaciones.

Cada vez que te "logueas con" Facebook, Google, GitHub, Microsoft, X (Twitter), esa aplicación está usando OAuth2 con scopes.

En esta sección verás cómo manejar autenticación y autorización con el mismo OAuth2 con scopes en tu aplicación de **FastAPI**.

/// warning | Advertencia

Esta es una sección más o menos avanzada. Si estás comenzando, puedes saltarla.

No necesariamente necesitas scopes de OAuth2, y puedes manejar autenticación y autorización como quieras.

Pero OAuth2 con scopes se puede integrar muy bien en tu API (con OpenAPI) y en la documentación de tu API.

No obstante, tú aún impones esos scopes, o cualquier otro requisito de seguridad/autorización, como necesites, en tu código.

En muchos casos, OAuth2 con scopes puede ser un exceso.

Pero si sabes que lo necesitas, o tienes curiosidad, sigue leyendo.

///

## Scopes de OAuth2 y OpenAPI

La especificación de OAuth2 define "scopes" como una lista de strings separados por espacios.

El contenido de cada uno de estos strings puede tener cualquier formato, pero no debe contener espacios.

Estos scopes representan "permisos".

En OpenAPI (por ejemplo, en la documentación de la API), puedes definir "esquemas de seguridad".

Cuando uno de estos esquemas de seguridad usa OAuth2, también puedes declarar y usar scopes.

Cada "scope" es solo un string (sin espacios).

Normalmente se utilizan para declarar permisos de seguridad específicos, por ejemplo:

* `users:read` o `users:write` son ejemplos comunes.
* `instagram_basic` es usado por Facebook / Instagram.
* `https://www.googleapis.com/auth/drive` es usado por Google.

/// info | Información

En OAuth2 un "scope" es solo un string que declara un permiso específico requerido.

No importa si tiene otros caracteres como `:` o si es una URL.

Esos detalles son específicos de la implementación.

Para OAuth2 son solo strings.

///

## Vista global

Primero, echemos un vistazo rápido a las partes que cambian desde los ejemplos en el **Tutorial - User Guide** principal para [OAuth2 con Password (y hashing), Bearer con tokens JWT](../../tutorial/security/oauth2-jwt.md){.internal-link target=_blank}. Ahora usando scopes de OAuth2:

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,9,13,47,65,106,108:116,122:125,129:135,140,156] *}

Ahora revisemos esos cambios paso a paso.

## Esquema de seguridad OAuth2

El primer cambio es que ahora estamos declarando el esquema de seguridad OAuth2 con dos scopes disponibles, `me` y `items`.

El parámetro `scopes` recibe un `dict` con cada scope como clave y la descripción como valor:

{* ../../docs_src/security/tutorial005_an_py310.py hl[63:66] *}

Como ahora estamos declarando esos scopes, aparecerán en la documentación de la API cuando inicies sesión/autorices.

Y podrás seleccionar cuáles scopes quieres dar de acceso: `me` y `items`.

Este es el mismo mecanismo utilizado cuando das permisos al iniciar sesión con Facebook, Google, GitHub, etc:

<img src="/img/tutorial/security/image11.png">

## Token JWT con scopes

Ahora, modifica la *path operation* del token para devolver los scopes solicitados.

Todavía estamos usando el mismo `OAuth2PasswordRequestForm`. Incluye una propiedad `scopes` con una `list` de `str`, con cada scope que recibió en el request.

Y devolvemos los scopes como parte del token JWT.

/// danger | Peligro

Para simplificar, aquí solo estamos añadiendo los scopes recibidos directamente al token.

Pero en tu aplicación, por seguridad, deberías asegurarte de añadir solo los scopes que el usuario realmente puede tener, o los que has predefinido.

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[156] *}

## Declarar scopes en *path operations* y dependencias

Ahora declaramos que la *path operation* para `/users/me/items/` requiere el scope `items`.

Para esto, importamos y usamos `Security` de `fastapi`.

Puedes usar `Security` para declarar dependencias (igual que `Depends`), pero `Security` también recibe un parámetro `scopes` con una lista de scopes (strings).

En este caso, pasamos una función de dependencia `get_current_active_user` a `Security` (de la misma manera que haríamos con `Depends`).

Pero también pasamos una `list` de scopes, en este caso con solo un scope: `items` (podría tener más).

Y la función de dependencia `get_current_active_user` también puede declarar sub-dependencias, no solo con `Depends` sino también con `Security`. Declarando su propia función de sub-dependencia (`get_current_user`), y más requisitos de scope.

En este caso, requiere el scope `me` (podría requerir más de un scope).

/// note | Nota

No necesariamente necesitas añadir diferentes scopes en diferentes lugares.

Lo estamos haciendo aquí para demostrar cómo **FastAPI** maneja scopes declarados en diferentes niveles.

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,140,171] *}

/// info | Información Técnica

`Security` es en realidad una subclase de `Depends`, y tiene solo un parámetro extra que veremos más adelante.

Pero al usar `Security` en lugar de `Depends`, **FastAPI** sabrá que puede declarar scopes de seguridad, usarlos internamente y documentar la API con OpenAPI.

Pero cuando importas `Query`, `Path`, `Depends`, `Security` y otros de `fastapi`, en realidad son funciones que devuelven clases especiales.

///

## Usar `SecurityScopes`

Ahora actualiza la dependencia `get_current_user`.

Esta es la que usan las dependencias anteriores.

Aquí es donde estamos usando el mismo esquema de OAuth2 que creamos antes, declarándolo como una dependencia: `oauth2_scheme`.

Porque esta función de dependencia no tiene ningún requisito de scope en sí, podemos usar `Depends` con `oauth2_scheme`, no tenemos que usar `Security` cuando no necesitamos especificar scopes de seguridad.

También declaramos un parámetro especial de tipo `SecurityScopes`, importado de `fastapi.security`.

Esta clase `SecurityScopes` es similar a `Request` (`Request` se usó para obtener el objeto request directamente).

{* ../../docs_src/security/tutorial005_an_py310.py hl[9,106] *}

## Usar los `scopes`

El parámetro `security_scopes` será del tipo `SecurityScopes`.

Tendrá una propiedad `scopes` con una lista que contiene todos los scopes requeridos por sí mismo y por todas las dependencias que lo usan como sub-dependencia. Eso significa, todos los "dependientes"... esto podría sonar confuso, se explica de nuevo más abajo.

El objeto `security_scopes` (de la clase `SecurityScopes`) también proporciona un atributo `scope_str` con un único string, que contiene esos scopes separados por espacios (lo vamos a usar).

Creamos una `HTTPException` que podemos reutilizar (`raise`) más tarde en varios puntos.

En esta excepción, incluimos los scopes requeridos (si los hay) como un string separado por espacios (usando `scope_str`). Ponemos ese string que contiene los scopes en el header `WWW-Authenticate` (esto es parte de la especificación).

{* ../../docs_src/security/tutorial005_an_py310.py hl[106,108:116] *}

## Verificar el `username` y la forma de los datos

Verificamos que obtenemos un `username`, y extraemos los scopes.

Y luego validamos esos datos con el modelo de Pydantic (capturando la excepción `ValidationError`), y si obtenemos un error leyendo el token JWT o validando los datos con Pydantic, lanzamos la `HTTPException` que creamos antes.

Para eso, actualizamos el modelo de Pydantic `TokenData` con una nueva propiedad `scopes`.

Al validar los datos con Pydantic podemos asegurarnos de que tenemos, por ejemplo, exactamente una `list` de `str` con los scopes y un `str` con el `username`.

En lugar de, por ejemplo, un `dict`, o algo más, ya que podría romper la aplicación en algún punto posterior, haciéndolo un riesgo de seguridad.

También verificamos que tenemos un usuario con ese username, y si no, lanzamos esa misma excepción que creamos antes.

{* ../../docs_src/security/tutorial005_an_py310.py hl[47,117:128] *}

## Verificar los `scopes`

Ahora verificamos que todos los scopes requeridos, por esta dependencia y todos los dependientes (incluyendo *path operations*), estén incluidos en los scopes proporcionados en el token recibido, de lo contrario, lanzamos una `HTTPException`.

Para esto, usamos `security_scopes.scopes`, que contiene una `list` con todos estos scopes como `str`.

{* ../../docs_src/security/tutorial005_an_py310.py hl[129:135] *}

## Árbol de dependencias y scopes

Revisemos de nuevo este árbol de dependencias y los scopes.

Como la dependencia `get_current_active_user` tiene como sub-dependencia a `get_current_user`, el scope `"me"` declarado en `get_current_active_user` se incluirá en la lista de scopes requeridos en el `security_scopes.scopes` pasado a `get_current_user`.

La *path operation* en sí también declara un scope, `"items"`, por lo que esto también estará en la lista de `security_scopes.scopes` pasado a `get_current_user`.

Así es como se ve la jerarquía de dependencias y scopes:

* La *path operation* `read_own_items` tiene:
    * Scopes requeridos `["items"]` con la dependencia:
    * `get_current_active_user`:
        * La función de dependencia `get_current_active_user` tiene:
            * Scopes requeridos `["me"]` con la dependencia:
            * `get_current_user`:
                * La función de dependencia `get_current_user` tiene:
                    * No requiere scopes por sí misma.
                    * Una dependencia usando `oauth2_scheme`.
                    * Un parámetro `security_scopes` de tipo `SecurityScopes`:
                        * Este parámetro `security_scopes` tiene una propiedad `scopes` con una `list` que contiene todos estos scopes declarados arriba, por lo que:
                            * `security_scopes.scopes` contendrá `["me", "items"]` para la *path operation* `read_own_items`.
                            * `security_scopes.scopes` contendrá `["me"]` para la *path operation* `read_users_me`, porque está declarado en la dependencia `get_current_active_user`.
                            * `security_scopes.scopes` contendrá `[]` (nada) para la *path operation* `read_system_status`, porque no declaró ningún `Security` con `scopes`, y su dependencia, `get_current_user`, tampoco declara ningún `scopes`.

/// tip | Consejo

Lo importante y "mágico" aquí es que `get_current_user` tendrá una lista diferente de `scopes` para verificar para cada *path operation*.

Todo depende de los `scopes` declarados en cada *path operation* y cada dependencia en el árbol de dependencias para esa *path operation* específica.

///

## Más detalles sobre `SecurityScopes`

Puedes usar `SecurityScopes` en cualquier punto, y en múltiples lugares, no tiene que ser en la dependencia "raíz".

Siempre tendrá los scopes de seguridad declarados en las dependencias `Security` actuales y todos los dependientes para **esa específica** *path operation* y **ese específico** árbol de dependencias.

Debido a que `SecurityScopes` tendrá todos los scopes declarados por dependientes, puedes usarlo para verificar que un token tiene los scopes requeridos en una función de dependencia central, y luego declarar diferentes requisitos de scope en diferentes *path operations*.

Serán verificados independientemente para cada *path operation*.

## Revisa

Si abres la documentación de la API, puedes autenticarte y especificar qué scopes deseas autorizar.

<img src="/img/tutorial/security/image11.png">

Si no seleccionas ningún scope, estarás "autenticado", pero cuando intentes acceder a `/users/me/` o `/users/me/items/` obtendrás un error diciendo que no tienes suficientes permisos. Aún podrás acceder a `/status/`.

Y si seleccionas el scope `me` pero no el scope `items`, podrás acceder a `/users/me/` pero no a `/users/me/items/`.

Eso es lo que pasaría a una aplicación de terceros que intentara acceder a una de estas *path operations* con un token proporcionado por un usuario, dependiendo de cuántos permisos el usuario otorgó a la aplicación.

## Acerca de las integraciones de terceros

En este ejemplo estamos usando el flujo de OAuth2 "password".

Esto es apropiado cuando estamos iniciando sesión en nuestra propia aplicación, probablemente con nuestro propio frontend.

Porque podemos confiar en ella para recibir el `username` y `password`, ya que la controlamos.

Pero si estás construyendo una aplicación OAuth2 a la que otros se conectarían (es decir, si estás construyendo un proveedor de autenticación equivalente a Facebook, Google, GitHub, etc.) deberías usar uno de los otros flujos.

El más común es el flujo implícito.

El más seguro es el flujo de código, pero es más complejo de implementar ya que requiere más pasos. Como es más complejo, muchos proveedores terminan sugiriendo el flujo implícito.

/// note | Nota

Es común que cada proveedor de autenticación nombre sus flujos de una manera diferente, para hacerlos parte de su marca.

Pero al final, están implementando el mismo estándar OAuth2.

///

**FastAPI** incluye utilidades para todos estos flujos de autenticación OAuth2 en `fastapi.security.oauth2`.

## `Security` en `dependencies` del decorador

De la misma manera que puedes definir una `list` de `Depends` en el parámetro `dependencies` del decorador (como se explica en [Dependencias en decoradores de path operation](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}), también podrías usar `Security` con `scopes` allí.
