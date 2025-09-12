# OAuth2 con Password (y hashing), Bearer con tokens JWT

Ahora que tenemos todo el flujo de seguridad, hagamos que la aplicación sea realmente segura, usando tokens <abbr title="JSON Web Tokens">JWT</abbr> y hashing de contraseñas seguras.

Este código es algo que puedes usar realmente en tu aplicación, guardar los hashes de las contraseñas en tu base de datos, etc.

Vamos a empezar desde donde lo dejamos en el capítulo anterior e incrementarlo.

## Acerca de JWT

JWT significa "JSON Web Tokens".

Es un estándar para codificar un objeto JSON en un string largo y denso sin espacios. Se ve así:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

No está encriptado, por lo que cualquiera podría recuperar la información de los contenidos.

Pero está firmado. Así que, cuando recibes un token que has emitido, puedes verificar que realmente lo emitiste.

De esta manera, puedes crear un token con una expiración de, digamos, 1 semana. Y luego, cuando el usuario regresa al día siguiente con el token, sabes que el usuario todavía está registrado en tu sistema.

Después de una semana, el token estará expirado y el usuario no estará autorizado y tendrá que iniciar sesión nuevamente para obtener un nuevo token. Y si el usuario (o un tercero) intenta modificar el token para cambiar la expiración, podrás descubrirlo, porque las firmas no coincidirían.

Si quieres jugar con tokens JWT y ver cómo funcionan, revisa <a href="https://jwt.io/" class="external-link" target="_blank">https://jwt.io</a>.

## Instalar `PyJWT`

Necesitamos instalar `PyJWT` para generar y verificar los tokens JWT en Python.

Asegúrate de crear un [entorno virtual](../../virtual-environments.md){.internal-link target=_blank}, activarlo y luego instalar `pyjwt`:

<div class="termy">

```console
$ pip install pyjwt

---> 100%
```

</div>

/// info | Información

Si planeas usar algoritmos de firma digital como RSA o ECDSA, deberías instalar la dependencia del paquete de criptografía `pyjwt[crypto]`.

Puedes leer más al respecto en la <a href="https://pyjwt.readthedocs.io/en/latest/installation.html" class="external-link" target="_blank">documentación de instalación de PyJWT</a>.

///

## Hashing de contraseñas

"Hacer hashing" significa convertir algún contenido (una contraseña en este caso) en una secuencia de bytes (solo un string) que parece un galimatías.

Siempre que pases exactamente el mismo contenido (exactamente la misma contraseña) obtienes exactamente el mismo galimatías.

Pero no puedes convertir del galimatías de nuevo a la contraseña.

### Por qué usar hashing de contraseñas

Si tu base de datos es robada, el ladrón no tendrá las contraseñas en texto claro de tus usuarios, solo los hashes.

Por lo tanto, el ladrón no podrá intentar usar esa contraseña en otro sistema (como muchos usuarios usan la misma contraseña en todas partes, esto sería peligroso).

## Instalar `passlib`

PassLib es un gran paquete de Python para manejar hashes de contraseñas.

Soporta muchos algoritmos de hashing seguros y utilidades para trabajar con ellos.

El algoritmo recomendado es "Bcrypt".

Asegúrate de crear un [entorno virtual](../../virtual-environments.md){.internal-link target=_blank}, activarlo y luego instalar PassLib con Bcrypt:

<div class="termy">

```console
$ pip install "passlib[bcrypt]"

---> 100%
```

</div>

/// tip | Consejo

Con `passlib`, incluso podrías configurarlo para poder leer contraseñas creadas por **Django**, un plug-in de seguridad de **Flask** u otros muchos.

Así, podrías, por ejemplo, compartir los mismos datos de una aplicación de Django en una base de datos con una aplicación de FastAPI. O migrar gradualmente una aplicación de Django usando la misma base de datos.

Y tus usuarios podrían iniciar sesión desde tu aplicación Django o desde tu aplicación **FastAPI**, al mismo tiempo.

///

## Hash y verificación de contraseñas

Importa las herramientas que necesitamos de `passlib`.

Crea un "contexto" de PassLib. Este es el que se usará para hacer el hash y verificar las contraseñas.

/// tip | Consejo

El contexto de PassLib también tiene funcionalidad para usar diferentes algoritmos de hashing, incluidos los antiguos obsoletos solo para permitir verificarlos, etc.

Por ejemplo, podrías usarlo para leer y verificar contraseñas generadas por otro sistema (como Django) pero hacer hash de cualquier contraseña nueva con un algoritmo diferente como Bcrypt.

Y ser compatible con todos ellos al mismo tiempo.

///

Crea una función de utilidad para hacer el hash de una contraseña que venga del usuario.

Y otra utilidad para verificar si una contraseña recibida coincide con el hash almacenado.

Y otra más para autenticar y devolver un usuario.

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,56:57,60:61,70:76] *}

/// note | Nota

Si revisas la nueva (falsa) base de datos `fake_users_db`, verás cómo se ve ahora la contraseña con hash: `"$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"`.

///

## Manejo de tokens JWT

Importa los módulos instalados.

Crea una clave secreta aleatoria que se usará para firmar los tokens JWT.

Para generar una clave secreta segura al azar usa el comando:

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

Y copia el resultado a la variable `SECRET_KEY` (no uses la del ejemplo).

Crea una variable `ALGORITHM` con el algoritmo usado para firmar el token JWT y configúralo a `"HS256"`.

Crea una variable para la expiración del token.

Define un Modelo de Pydantic que se usará en el endpoint de token para el response.

Crea una función de utilidad para generar un nuevo token de acceso.

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,79:87] *}

## Actualizar las dependencias

Actualiza `get_current_user` para recibir el mismo token que antes, pero esta vez, usando tokens JWT.

Decodifica el token recibido, verifícalo y devuelve el usuario actual.

Si el token es inválido, devuelve un error HTTP de inmediato.

{* ../../docs_src/security/tutorial004_an_py310.py hl[90:107] *}

## Actualizar la *path operation* `/token`

Crea un `timedelta` con el tiempo de expiración del token.

Crea un verdadero token de acceso JWT y devuélvelo.

{* ../../docs_src/security/tutorial004_an_py310.py hl[118:133] *}

### Detalles técnicos sobre el "sujeto" `sub` de JWT

La especificación de JWT dice que hay una clave `sub`, con el sujeto del token.

Es opcional usarlo, pero ahí es donde pondrías la identificación del usuario, por lo que lo estamos usando aquí.

JWT podría ser usado para otras cosas aparte de identificar un usuario y permitirle realizar operaciones directamente en tu API.

Por ejemplo, podrías identificar un "coche" o un "artículo de blog".

Luego, podrías agregar permisos sobre esa entidad, como "conducir" (para el coche) o "editar" (para el blog).

Y luego, podrías darle ese token JWT a un usuario (o bot), y ellos podrían usarlo para realizar esas acciones (conducir el coche, o editar el artículo del blog) sin siquiera necesitar tener una cuenta, solo con el token JWT que tu API generó para eso.

Usando estas ideas, JWT puede ser utilizado para escenarios mucho más sofisticados.

En esos casos, varias de esas entidades podrían tener el mismo ID, digamos `foo` (un usuario `foo`, un coche `foo`, y un artículo del blog `foo`).

Entonces, para evitar colisiones de ID, cuando crees el token JWT para el usuario, podrías prefijar el valor de la clave `sub`, por ejemplo, con `username:`. Así, en este ejemplo, el valor de `sub` podría haber sido: `username:johndoe`.

Lo importante a tener en cuenta es que la clave `sub` debería tener un identificador único a lo largo de toda la aplicación, y debería ser un string.

## Revisa

Ejecuta el servidor y ve a la documentación: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Verás la interfaz de usuario como:

<img src="/img/tutorial/security/image07.png">

Autoriza la aplicación de la misma manera que antes.

Usando las credenciales:

Usuario: `johndoe`
Contraseña: `secret`

/// check | Revisa

Observa que en ninguna parte del código está la contraseña en texto claro "`secret`", solo tenemos la versión con hash.

///

<img src="/img/tutorial/security/image08.png">

Llama al endpoint `/users/me/`, obtendrás el response como:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

Si abres las herramientas de desarrollador, podrías ver cómo los datos enviados solo incluyen el token, la contraseña solo se envía en la primera petición para autenticar al usuario y obtener ese token de acceso, pero no después:

<img src="/img/tutorial/security/image10.png">

/// note | Nota

Observa el header `Authorization`, con un valor que comienza con `Bearer `.

///

## Uso avanzado con `scopes`

OAuth2 tiene la noción de "scopes".

Puedes usarlos para agregar un conjunto específico de permisos a un token JWT.

Luego, puedes darle este token directamente a un usuario o a un tercero, para interactuar con tu API con un conjunto de restricciones.

Puedes aprender cómo usarlos y cómo están integrados en **FastAPI** más adelante en la **Guía de Usuario Avanzada**.

## Resumen

Con lo que has visto hasta ahora, puedes configurar una aplicación **FastAPI** segura usando estándares como OAuth2 y JWT.

En casi cualquier framework el manejo de la seguridad se convierte en un tema bastante complejo rápidamente.

Muchos paquetes que lo simplifican tienen que hacer muchos compromisos con el modelo de datos, la base de datos y las funcionalidades disponibles. Y algunos de estos paquetes que simplifican las cosas demasiado en realidad tienen fallos de seguridad en el fondo.

---

**FastAPI** no hace ningún compromiso con ninguna base de datos, modelo de datos o herramienta.

Te da toda la flexibilidad para elegir aquellas que se ajusten mejor a tu proyecto.

Y puedes usar directamente muchos paquetes bien mantenidos y ampliamente usados como `passlib` y `PyJWT`, porque **FastAPI** no requiere mecanismos complejos para integrar paquetes externos.

Pero te proporciona las herramientas para simplificar el proceso tanto como sea posible sin comprometer la flexibilidad, la robustez o la seguridad.

Y puedes usar e implementar protocolos seguros y estándar, como OAuth2 de una manera relativamente simple.

Puedes aprender más en la **Guía de Usuario Avanzada** sobre cómo usar "scopes" de OAuth2, para un sistema de permisos más detallado, siguiendo estos mismos estándares. OAuth2 con scopes es el mecanismo utilizado por muchos grandes proveedores de autenticación, como Facebook, Google, GitHub, Microsoft, X (Twitter), etc. para autorizar aplicaciones de terceros para interactuar con sus APIs en nombre de sus usuarios.
