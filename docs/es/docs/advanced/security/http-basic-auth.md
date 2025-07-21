# HTTP Basic Auth

Para los casos más simples, puedes usar HTTP Basic Auth.

En HTTP Basic Auth, la aplicación espera un header que contiene un nombre de usuario y una contraseña.

Si no lo recibe, devuelve un error HTTP 401 "Unauthorized".

Y devuelve un header `WWW-Authenticate` con un valor de `Basic`, y un parámetro `realm` opcional.

Eso le dice al navegador que muestre el prompt integrado para un nombre de usuario y contraseña.

Luego, cuando escribes ese nombre de usuario y contraseña, el navegador los envía automáticamente en el header.

## Simple HTTP Basic Auth

* Importa `HTTPBasic` y `HTTPBasicCredentials`.
* Crea un "esquema de `security`" usando `HTTPBasic`.
* Usa ese `security` con una dependencia en tu *path operation*.
* Devuelve un objeto de tipo `HTTPBasicCredentials`:
  * Contiene el `username` y `password` enviados.

{* ../../docs_src/security/tutorial006_an_py39.py hl[4,8,12] *}

Cuando intentas abrir la URL por primera vez (o haces clic en el botón "Execute" en la documentación) el navegador te pedirá tu nombre de usuario y contraseña:

<img src="/img/tutorial/security/image12.png">

## Revisa el nombre de usuario

Aquí hay un ejemplo más completo.

Usa una dependencia para comprobar si el nombre de usuario y la contraseña son correctos.

Para esto, usa el módulo estándar de Python <a href="https://docs.python.org/3/library/secrets.html" class="external-link" target="_blank">`secrets`</a> para verificar el nombre de usuario y la contraseña.

`secrets.compare_digest()` necesita tomar `bytes` o un `str` que solo contenga caracteres ASCII (los carácteres en inglés), esto significa que no funcionaría con caracteres como `á`, como en `Sebastián`.

Para manejar eso, primero convertimos el `username` y `password` a `bytes` codificándolos con UTF-8.

Luego podemos usar `secrets.compare_digest()` para asegurar que `credentials.username` es `"stanleyjobson"`, y que `credentials.password` es `"swordfish"`.

{* ../../docs_src/security/tutorial007_an_py39.py hl[1,12:24] *}

Esto sería similar a:

```Python
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # Return some error
    ...
```

Pero al usar `secrets.compare_digest()` será seguro contra un tipo de ataques llamados "timing attacks".

### Timing Attacks

¿Pero qué es un "timing attack"?

Imaginemos que algunos atacantes están tratando de adivinar el nombre de usuario y la contraseña.

Y envían un request con un nombre de usuario `johndoe` y una contraseña `love123`.

Entonces el código de Python en tu aplicación equivaldría a algo como:

```Python
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Pero justo en el momento en que Python compara la primera `j` en `johndoe` con la primera `s` en `stanleyjobson`, devolverá `False`, porque ya sabe que esas dos strings no son iguales, pensando que "no hay necesidad de gastar más computación comparando el resto de las letras". Y tu aplicación dirá "Nombre de usuario o contraseña incorrectos".

Pero luego los atacantes prueban con el nombre de usuario `stanleyjobsox` y contraseña `love123`.

Y el código de tu aplicación hace algo así como:

```Python
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Python tendrá que comparar todo `stanleyjobso` en ambos `stanleyjobsox` y `stanleyjobson` antes de darse cuenta de que ambas strings no son las mismas. Así que tomará algunos microsegundos extra para responder "Nombre de usuario o contraseña incorrectos".

#### El tiempo de respuesta ayuda a los atacantes

En ese punto, al notar que el servidor tardó algunos microsegundos más en enviar el response "Nombre de usuario o contraseña incorrectos", los atacantes sabrán que acertaron en _algo_, algunas de las letras iniciales eran correctas.

Y luego pueden intentar de nuevo sabiendo que probablemente es algo más similar a `stanleyjobsox` que a `johndoe`.

#### Un ataque "profesional"

Por supuesto, los atacantes no intentarían todo esto a mano, escribirían un programa para hacerlo, posiblemente con miles o millones de pruebas por segundo. Y obtendrían solo una letra correcta adicional a la vez.

Pero haciendo eso, en algunos minutos u horas, los atacantes habrían adivinado el nombre de usuario y la contraseña correctos, con la "ayuda" de nuestra aplicación, solo usando el tiempo tomado para responder.

#### Arréglalo con `secrets.compare_digest()`

Pero en nuestro código estamos usando realmente `secrets.compare_digest()`.

En resumen, tomará el mismo tiempo comparar `stanleyjobsox` con `stanleyjobson` que comparar `johndoe` con `stanleyjobson`. Y lo mismo para la contraseña.

De esa manera, usando `secrets.compare_digest()` en el código de tu aplicación, será seguro contra todo este rango de ataques de seguridad.

### Devuelve el error

Después de detectar que las credenciales son incorrectas, regresa un `HTTPException` con un código de estado 401 (el mismo que se devuelve cuando no se proporcionan credenciales) y agrega el header `WWW-Authenticate` para que el navegador muestre el prompt de inicio de sesión nuevamente:

{* ../../docs_src/security/tutorial007_an_py39.py hl[26:30] *}
