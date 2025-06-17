# Variables de Entorno

/// tip | Consejo

Si ya sabes qué son las "variables de entorno" y cómo usarlas, siéntete libre de saltarte esto.

///

Una variable de entorno (también conocida como "**env var**") es una variable que vive **fuera** del código de Python, en el **sistema operativo**, y podría ser leída por tu código de Python (o por otros programas también).

Las variables de entorno pueden ser útiles para manejar **configuraciones** de aplicaciones, como parte de la **instalación** de Python, etc.

## Crear y Usar Variables de Entorno

Puedes **crear** y usar variables de entorno en la **shell (terminal)**, sin necesidad de Python:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Podrías crear una env var MY_NAME con
$ export MY_NAME="Wade Wilson"

// Luego podrías usarla con otros programas, como
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Crea una env var MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Úsala con otros programas, como
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Leer Variables de Entorno en Python

También podrías crear variables de entorno **fuera** de Python, en la terminal (o con cualquier otro método), y luego **leerlas en Python**.

Por ejemplo, podrías tener un archivo `main.py` con:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | Consejo

El segundo argumento de <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> es el valor por defecto a retornar.

Si no se proporciona, es `None` por defecto; aquí proporcionamos `"World"` como el valor por defecto para usar.

///

Luego podrías llamar a ese programa Python:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Aquí todavía no configuramos la env var
$ python main.py

// Como no configuramos la env var, obtenemos el valor por defecto

Hello World from Python

// Pero si creamos una variable de entorno primero
$ export MY_NAME="Wade Wilson"

// Y luego llamamos al programa nuevamente
$ python main.py

// Ahora puede leer la variable de entorno

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Aquí todavía no configuramos la env var
$ python main.py

// Como no configuramos la env var, obtenemos el valor por defecto

Hello World from Python

// Pero si creamos una variable de entorno primero
$ $Env:MY_NAME = "Wade Wilson"

// Y luego llamamos al programa nuevamente
$ python main.py

// Ahora puede leer la variable de entorno

Hello Wade Wilson from Python
```

</div>

////

Dado que las variables de entorno pueden configurarse fuera del código, pero pueden ser leídas por el código, y no tienen que ser almacenadas (committed en `git`) con el resto de los archivos, es común usarlas para configuraciones o **ajustes**.

También puedes crear una variable de entorno solo para una **invocación específica de un programa**, que está disponible solo para ese programa, y solo durante su duración.

Para hacer eso, créala justo antes del programa en sí, en la misma línea:

<div class="termy">

```console
// Crea una env var MY_NAME en línea para esta llamada del programa
$ MY_NAME="Wade Wilson" python main.py

// Ahora puede leer la variable de entorno

Hello Wade Wilson from Python

// La env var ya no existe después
$ python main.py

Hello World from Python
```

</div>

/// tip | Consejo

Puedes leer más al respecto en <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a>.

///

## Tipos y Validación

Estas variables de entorno solo pueden manejar **strings de texto**, ya que son externas a Python y deben ser compatibles con otros programas y el resto del sistema (e incluso con diferentes sistemas operativos, como Linux, Windows, macOS).

Esto significa que **cualquier valor** leído en Python desde una variable de entorno **será un `str`**, y cualquier conversión a un tipo diferente o cualquier validación tiene que hacerse en el código.

Aprenderás más sobre cómo usar variables de entorno para manejar **configuraciones de aplicación** en la [Guía del Usuario Avanzado - Ajustes y Variables de Entorno](./advanced/settings.md){.internal-link target=_blank}.

## Variable de Entorno `PATH`

Hay una variable de entorno **especial** llamada **`PATH`** que es utilizada por los sistemas operativos (Linux, macOS, Windows) para encontrar programas a ejecutar.

El valor de la variable `PATH` es un string largo que consiste en directorios separados por dos puntos `:` en Linux y macOS, y por punto y coma `;` en Windows.

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

Esto significa que el sistema debería buscar programas en los directorios:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

Cuando escribes un **comando** en la terminal, el sistema operativo **busca** el programa en **cada uno de esos directorios** listados en la variable de entorno `PATH`.

Por ejemplo, cuando escribes `python` en la terminal, el sistema operativo busca un programa llamado `python` en el **primer directorio** de esa lista.

Si lo encuentra, entonces lo **utilizará**. De lo contrario, continúa buscando en los **otros directorios**.

### Instalando Python y Actualizando el `PATH`

Cuando instalas Python, se te podría preguntar si deseas actualizar la variable de entorno `PATH`.

//// tab | Linux, macOS

Digamos que instalas Python y termina en un directorio `/opt/custompython/bin`.

Si dices que sí para actualizar la variable de entorno `PATH`, entonces el instalador añadirá `/opt/custompython/bin` a la variable de entorno `PATH`.

Podría verse así:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

De esta manera, cuando escribes `python` en la terminal, el sistema encontrará el programa Python en `/opt/custompython/bin` (el último directorio) y usará ese.

////

//// tab | Windows

Digamos que instalas Python y termina en un directorio `C:\opt\custompython\bin`.

Si dices que sí para actualizar la variable de entorno `PATH`, entonces el instalador añadirá `C:\opt\custompython\bin` a la variable de entorno `PATH`.

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

Esto sería más o menos equivalente a escribir:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

El sistema **encontrará** el programa `python` en `C:\opt\custompython\bin\python` y lo ejecutará.

Esto sería más o menos equivalente a escribir:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

Esta información será útil al aprender sobre [Entornos Virtuales](virtual-environments.md){.internal-link target=_blank}.

## Conclusión

Con esto deberías tener una comprensión básica de qué son las **variables de entorno** y cómo usarlas en Python.

También puedes leer más sobre ellas en la <a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia para Variable de Entorno</a>.

En muchos casos no es muy obvio cómo las variables de entorno serían útiles y aplicables de inmediato. Pero siguen apareciendo en muchos escenarios diferentes cuando estás desarrollando, así que es bueno conocerlas.

Por ejemplo, necesitarás esta información en la siguiente sección, sobre [Entornos Virtuales](virtual-environments.md).
