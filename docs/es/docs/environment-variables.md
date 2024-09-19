# Variables de Entorno

/// tip

Si ya conoces sobre "variables de entorno" y cómo usarlas, siéntete libre de saltarte esta parte.

///

Una variable de entorno (también conocida como "**env var**") es una variable que existe **por fuera** del código de Python, en el **sistema operativo**, y puede ser leída por tu código Python (o por otros programas también).

Las variables de entorno pueden ser útiles para manejar **configuraciones** de aplicaciones, como parte de la **instalación** de Python, etc.

## Crear y Usar Variables de Entorno

Puedes **crear** y usar variables de entorno en la **shell (terminal)**, sin necesidad de utilizar Python:

////tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Puedes crear una variable de entorno llamada MY_NAME con
$ export MY_NAME="Wade Wilson"

// Luego, podrías usarla con otros programas, como
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Crea un variable de entorno llamada MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Úsala con otros programas, como
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Lee Variables de Entorno en Python

También puedes crear variables de entorno **por fuera** de Python, en la terminal (o por cualquier otro método), y luego **leerlas en Python**.

Por ejemplo, podrías tener un archivo `main.py` con:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip

El segundo argumento de <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> es el valor por defecto que se devuelve.

Si no se proporciona, el valor predeterminado es `None`. En este caso, proporcionamos `"World"` como valor por defecto para usar.

///

Luego, podrías ejecutar ese programa en Python:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Aquí aún no hemos establecido la variable de entorno
$ python main.py

// Como no establecimos la variable de entorno, obtenemos el valor predeterminado

Hello World from Python

// Pero si primero creamos una variable de entorno
$ export MY_NAME="Wade Wilson"

// Y luego ejecutamos el programa nuevamente
$ python main.py

// Ahora puede leer la variable de entorno

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Aquí aún no hemos establecido la variable de entorno
$ python main.py

// Como no establecimos la variable de entorno, obtenemos el valor predeterminado

Hello World from Python

// Pero si primero creamos una variable de entorno
$ $Env:MY_NAME = "Wade Wilson"

// Y luego ejecutamos el programa nuevamente
$ python main.py

// Ahora puede leer la variable de entorno

Hello Wade Wilson from Python
```

</div>

////

Como las variables de entorno se pueden establecer fuera del código, pero pueden ser leídas por el código y no tienen que ser almacenadas (o enviadas a `git`) con el resto de los archivos, es común usarlas para configuraciones o **ajustes**.

También puedes crear una variable de entorno solo para una **invocación específica de un programa**, que estará disponible únicamente para ese programa y solo durante su ejecución.

Para hacer eso, créala justo antes de llamar al programa, en la misma línea:

<div class="termy">

```console
// Crea una variable de entorno MY_NAME en la misma línea para esta ejecución del programa
$ MY_NAME="Wade Wilson" python main.py

// Ahora puede leer la variable de entorno

Hello Wade Wilson from Python

// La variable de entorno ya no existe después
$ python main.py

Hello World from Python
```

</div>

/// tip | Consejo

Puedes leer más sobre esto en <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a>.

///

## Tipos y Validación

Estas variables de entorno solo pueden manejar **cadenas de texto**, ya que son externas a Python y deben ser compatibles con otros programas y el resto del sistema (incluso con diferentes sistemas operativos como Linux, Windows, macOS).

Esto significa que **cualquier valor** leído en Python desde una variable de entorno **será un `str`**, y cualquier conversión a un tipo diferente o validación debe hacerse en el código.

Aprenderás más sobre cómo usar las variables de entorno para manejar **ajustes de aplicación** en la [Guía de Usuario Avanzado - Ajustes y Variables de Entorno](./advanced/settings.md){.internal-link target=_blank}.

## Variable de Entorno `PATH`

Existe una variable de entorno **especial** llamada **`PATH`** que es usada por los sistemas operativos (Linux, macOS, Windows) para encontrar los programas que deben ejecutarse.

El valor de la variable `PATH` es una cadena de texto larga formada por directorios separados por dos puntos `:` en Linux y macOS, y por un punto y coma `;` en Windows.

Por ejemplo, la variable de entorno `PATH` podría verse así:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Esto significa que el sistema debería buscar programas en los directorios:

* `/usr/local/bin`
* `/usr/bin`
* `/bin`
* `/usr/sbin`
* `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

Esto significa que el sistema deberia buscar programas en los directorios:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

Cuando escribes un **comando** en la terminal, el sistema operativo **busca** el programa en **cada uno de los directorios** listados en la variable de entorno `PATH`.

Por ejemplo, cuando escribes `python` en la terminal, el sistema operativo busca un programa llamado `python` en el **primer directorio** de esa lista.

Si lo encuentra, entonces lo **utilizará**. De lo contrario, seguirá buscando en los **otros directorios**.

### Instalando Python y Actualizando el `PATH`

Cuando instalas Python, es posible que te pregunten si deseas actualizar la variable de entorno `PATH`.

//// tab | Linux, macOS

Supongamos que instalas Python y termina en un directorio como `/opt/custompython/bin`.

Si aceptas actualizar la variable de entorno `PATH`, el instalador agregará `/opt/custompython/bin` a la variable de entorno `PATH`.

Podría verse así:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

De esta manera, cuando escribes `python` en la terminal, el sistema encontrará el programa Python en `/opt/custompython/bin` (el último directorio) y usará ese.

////

//// tab | Windows

Supongamos que instalas Python y termina en un directorio como `C:\opt\custompython\bin`.

Si dices que si al actualización de la variable de entorno `PATH`, entonces el instalador agregará `C:\opt\custompython\bin` a la variable de entorno `PATH`.

Podría verse así:

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

De esta manera, cuando escribes `python` en la terminal, el sistema encontrará el programa Python en `C:\opt\custompython\bin` (el último directorio) y usará ese.

////

Entonces, si escribes:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

El sistema **encontrará** el programa `python` en `/opt/custompython/bin` y lo ejecutará.

Esto sería casi igual a escribir:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

El sistema **encontrará** el programa `python` en`C:\opt\custompython\bin\python` y lo ejecutará.

Esto sería casi igual a escribir:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

Esta información será útil cuando aprendas sobre los [Entornos Virtuales](virtual-environments.md){.internal-link target=_blank}.

## Conclusión

Con esto, deberías tener una comprensión básica de lo que son las **variables de entorno** y cómo utilizarlas en Python.

También puedes leer más sobre ellas en <a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia sobre Variables de Entorno</a>.

En muchos casos, no es muy obvio cómo las variables de entorno serían útiles o aplicables de inmediato. Pero aparecen en muchos escenarios diferentes cuando estás desarrollando, por lo que es bueno conocerlas.

Por ejemplo, necesitarás esta información en la siguiente sección sobre [Entornos Virtuales](virtual-environments.md).
