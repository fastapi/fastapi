# Simple OAuth2 con Password y Bearer

Ahora vamos a construir a partir del capítulo anterior y agregar las partes faltantes para tener un flujo de seguridad completo.

## Obtener el `username` y `password`

Vamos a usar las utilidades de seguridad de **FastAPI** para obtener el `username` y `password`.

OAuth2 especifica que cuando se utiliza el "password flow" (que estamos usando), el cliente/usuario debe enviar campos `username` y `password` como form data.

Y la especificación dice que los campos deben llamarse así. Por lo que `user-name` o `email` no funcionarían.

Pero no te preocupes, puedes mostrarlo como quieras a tus usuarios finales en el frontend.

Y tus modelos de base de datos pueden usar cualquier otro nombre que desees.

Pero para la *path operation* de inicio de sesión, necesitamos usar estos nombres para ser compatibles con la especificación (y poder, por ejemplo, utilizar el sistema de documentación integrada de la API).

La especificación también establece que el `username` y `password` deben enviarse como form data (por lo que no hay JSON aquí).

### `scope`

La especificación también indica que el cliente puede enviar otro campo del formulario llamado "`scope`".

El nombre del campo del formulario es `scope` (en singular), pero en realidad es un string largo con "scopes" separados por espacios.

Cada "scope" es simplemente un string (sin espacios).

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

## Código para obtener el `username` y `password`

Ahora vamos a usar las utilidades proporcionadas por **FastAPI** para manejar esto.

### `OAuth2PasswordRequestForm`

Primero, importa `OAuth2PasswordRequestForm`, y úsalo como una dependencia con `Depends` en la *path operation* para `/token`:

{* ../../docs_src/security/tutorial003_an_py310.py hl[4,78] *}

`OAuth2PasswordRequestForm` es una dependencia de clase que declara un body de formulario con:

* El `username`.
* El `password`.
* Un campo opcional `scope` como un string grande, compuesto por strings separados por espacios.
* Un `grant_type` opcional.

/// tip | Consejo

La especificación de OAuth2 en realidad *requiere* un campo `grant_type` con un valor fijo de `password`, pero `OAuth2PasswordRequestForm` no lo obliga.

Si necesitas imponerlo, utiliza `OAuth2PasswordRequestFormStrict` en lugar de `OAuth2PasswordRequestForm`.

///

* Un `client_id` opcional (no lo necesitamos para nuestro ejemplo).
* Un `client_secret` opcional (no lo necesitamos para nuestro ejemplo).

/// info | Información

`OAuth2PasswordRequestForm` no es una clase especial para **FastAPI** como lo es `OAuth2PasswordBearer`.

`OAuth2PasswordBearer` hace que **FastAPI** sepa que es un esquema de seguridad. Así que se añade de esa manera a OpenAPI.

Pero `OAuth2PasswordRequestForm` es solo una dependencia de clase que podrías haber escrito tú mismo, o podrías haber declarado parámetros de `Form` directamente.

Pero como es un caso de uso común, se proporciona directamente por **FastAPI**, solo para facilitarlo.

///

### Usa el form data

/// tip | Consejo

La instance de la clase de dependencia `OAuth2PasswordRequestForm` no tendrá un atributo `scope` con el string largo separado por espacios, en su lugar, tendrá un atributo `scopes` con la lista real de strings para cada scope enviado.

No estamos usando `scopes` en este ejemplo, pero la funcionalidad está ahí si la necesitas.

///

Ahora, obtén los datos del usuario desde la base de datos (falsa), usando el `username` del campo del form.

Si no existe tal usuario, devolvemos un error diciendo "Incorrect username or password".

Para el error, usamos la excepción `HTTPException`:

{* ../../docs_src/security/tutorial003_an_py310.py hl[3,79:81] *}

### Revisa el password

En este punto tenemos los datos del usuario de nuestra base de datos, pero no hemos revisado el password.

Primero pongamos esos datos en el modelo `UserInDB` de Pydantic.

Nunca deberías guardar passwords en texto plano, así que, usaremos el sistema de hash de passwords (falso).

Si los passwords no coinciden, devolvemos el mismo error.

#### Hashing de passwords

"Hacer hash" significa: convertir algún contenido (un password en este caso) en una secuencia de bytes (solo un string) que parece un galimatías.

Siempre que pases exactamente el mismo contenido (exactamente el mismo password) obtienes exactamente el mismo galimatías.

Pero no puedes convertir del galimatías al password.

##### Por qué usar hashing de passwords

Si tu base de datos es robada, el ladrón no tendrá los passwords en texto plano de tus usuarios, solo los hashes.

Entonces, el ladrón no podrá intentar usar esos mismos passwords en otro sistema (como muchos usuarios usan el mismo password en todas partes, esto sería peligroso).

{* ../../docs_src/security/tutorial003_an_py310.py hl[82:85] *}

#### Sobre `**user_dict`

`UserInDB(**user_dict)` significa:

*Pasa las claves y valores de `user_dict` directamente como argumentos clave-valor, equivalente a:*

```Python
UserInDB(
    username = user_dict["username"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    disabled = user_dict["disabled"],
    hashed_password = user_dict["hashed_password"],
)
```

/// info | Información

Para una explicación más completa de `**user_dict` revisa en [la documentación para **Extra Models**](../extra-models.md#about-user_indict){.internal-link target=_blank}.

///

## Devolver el token

El response del endpoint `token` debe ser un objeto JSON.

Debe tener un `token_type`. En nuestro caso, como estamos usando tokens "Bearer", el tipo de token debe ser "`bearer`".

Y debe tener un `access_token`, con un string que contenga nuestro token de acceso.

Para este ejemplo simple, vamos a ser completamente inseguros y devolver el mismo `username` como el token.

/// tip | Consejo

En el próximo capítulo, verás una implementación segura real, con hashing de passwords y tokens <abbr title="JSON Web Tokens">JWT</abbr>.

Pero por ahora, enfoquémonos en los detalles específicos que necesitamos.

///

{* ../../docs_src/security/tutorial003_an_py310.py hl[87] *}

/// tip | Consejo

De acuerdo con la especificación, deberías devolver un JSON con un `access_token` y un `token_type`, igual que en este ejemplo.

Esto es algo que tienes que hacer tú mismo en tu código, y asegurarte de usar esas claves JSON.

Es casi lo único que tienes que recordar hacer correctamente tú mismo, para ser compatible con las especificaciones.

Para el resto, **FastAPI** lo maneja por ti.

///

## Actualizar las dependencias

Ahora vamos a actualizar nuestras dependencias.

Queremos obtener el `current_user` *solo* si este usuario está activo.

Entonces, creamos una dependencia adicional `get_current_active_user` que a su vez utiliza `get_current_user` como dependencia.

Ambas dependencias solo devolverán un error HTTP si el usuario no existe, o si está inactivo.

Así que, en nuestro endpoint, solo obtendremos un usuario si el usuario existe, fue autenticado correctamente, y está activo:

{* ../../docs_src/security/tutorial003_an_py310.py hl[58:66,69:74,94] *}

/// info | Información

El header adicional `WWW-Authenticate` con el valor `Bearer` que estamos devolviendo aquí también es parte de la especificación.

Cualquier código de estado HTTP (error) 401 "UNAUTHORIZED" se supone que también debe devolver un header `WWW-Authenticate`.

En el caso de tokens bearer (nuestro caso), el valor de ese header debe ser `Bearer`.

De hecho, puedes omitir ese header extra y aún funcionaría.

Pero se proporciona aquí para cumplir con las especificaciones.

Además, podría haber herramientas que lo esperen y lo usen (ahora o en el futuro) y eso podría ser útil para ti o tus usuarios, ahora o en el futuro.

Ese es el beneficio de los estándares...

///

## Verlo en acción

Abre la documentación interactiva: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

### Autenticar

Haz clic en el botón "Authorize".

Usa las credenciales:

Usuario: `johndoe`

Contraseña: `secret`

<img src="/img/tutorial/security/image04.png">

Después de autenticarte en el sistema, lo verás así:

<img src="/img/tutorial/security/image05.png">

### Obtener tus propios datos de usuario

Ahora usa la operación `GET` con la path `/users/me`.

Obtendrás los datos de tu usuario, como:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
```

<img src="/img/tutorial/security/image06.png">

Si haces clic en el icono de candado y cierras sesión, y luego intentas la misma operación nuevamente, obtendrás un error HTTP 401 de:

```JSON
{
  "detail": "Not authenticated"
}
```

### Usuario inactivo

Ahora prueba con un usuario inactivo, autentícate con:

Usuario: `alice`

Contraseña: `secret2`

Y trata de usar la operación `GET` con la path `/users/me`.

Obtendrás un error de "Usuario inactivo", como:

```JSON
{
  "detail": "Inactive user"
}
```

## Recapitulación

Ahora tienes las herramientas para implementar un sistema de seguridad completo basado en `username` y `password` para tu API.

Usando estas herramientas, puedes hacer que el sistema de seguridad sea compatible con cualquier base de datos y con cualquier modelo de usuario o de datos.

El único detalle que falta es que en realidad no es "seguro" aún.

En el próximo capítulo verás cómo usar un paquete de hashing de passwords seguro y tokens <abbr title="JSON Web Tokens">JWT</abbr>.
