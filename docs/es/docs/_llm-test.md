# Archivo de prueba de LLM { #llm-test-file }

Este documento prueba si el <abbr title="Large Language Model – Modelo de lenguaje grande">LLM</abbr>, que traduce la documentación, entiende el `general_prompt` en `scripts/translate.py` y el prompt específico del idioma en `docs/{language code}/llm-prompt.md`. El prompt específico del idioma se agrega al final de `general_prompt`.

Las pruebas añadidas aquí serán vistas por todas las personas que diseñan prompts específicos del idioma.

Úsalo de la siguiente manera:

* Ten un prompt específico del idioma – `docs/{language code}/llm-prompt.md`.
* Haz una traducción fresca de este documento a tu idioma destino (mira, por ejemplo, el comando `translate-page` de `translate.py`). Esto creará la traducción en `docs/{language code}/docs/_llm-test.md`.
* Comprueba si todo está bien en la traducción.
* Si es necesario, mejora tu prompt específico del idioma, el prompt general, o el documento en inglés.
* Luego corrige manualmente los problemas restantes en la traducción para que sea una buena traducción.
* Vuelve a traducir, teniendo la buena traducción en su lugar. El resultado ideal sería que el LLM ya no hiciera cambios a la traducción. Eso significa que el prompt general y tu prompt específico del idioma están tan bien como pueden estar (a veces hará algunos cambios aparentemente aleatorios; la razón es que <a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">los LLMs no son algoritmos deterministas</a>).

Las pruebas:

## Fragmentos de código { #code-snippets }

//// tab | Prueba

Este es un fragmento de código: `foo`. Y este es otro fragmento de código: `bar`. Y otro más: `baz quux`.

////

//// tab | Información

El contenido de los fragmentos de código debe dejarse tal cual.

Consulta la sección `### Content of code snippets` en el prompt general en `scripts/translate.py`.

////

## Comillas { #quotes }

//// tab | Prueba

Ayer, mi amigo escribió: "Si escribes 'incorrectly' correctamente, lo habrás escrito incorrectamente". A lo que respondí: "Correcto, pero 'incorrectly' está incorrecto, no '"incorrectly"'".

/// note | Nota

El LLM probablemente traducirá esto mal. Lo interesante es si mantiene la traducción corregida al volver a traducir.

///

////

//// tab | Información

La persona que diseña el prompt puede elegir si quiere convertir comillas neutras a comillas tipográficas. También está bien dejarlas como están.

Consulta por ejemplo la sección `### Quotes` en `docs/de/llm-prompt.md`.

////

## Comillas en fragmentos de código { #quotes-in-code-snippets }

//// tab | Prueba

`pip install "foo[bar]"`

Ejemplos de literales de string en fragmentos de código: `"this"`, `'that'`.

Un ejemplo difícil de literales de string en fragmentos de código: `f"I like {'oranges' if orange else "apples"}"`

Hardcore: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | Información

... Sin embargo, las comillas dentro de fragmentos de código deben quedarse tal cual.

////

## bloques de código { #code-blocks }

//// tab | Prueba

Un ejemplo de código Bash...

```bash
# Imprime un saludo al universo
echo "Hello universe"
```

...y un ejemplo de código de consola...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

...y otro ejemplo de código de consola...

```console
// Crea un directorio "Code"
$ mkdir code
// Cambia a ese directorio
$ cd code
```

...y un ejemplo de código Python...

```Python
wont_work()  # Esto no va a funcionar 😱
works(foo="bar")  # Esto funciona 🎉
```

...y eso es todo.

////

//// tab | Información

El código en bloques de código no debe modificarse, con la excepción de los comentarios.

Consulta la sección `### Content of code blocks` en el prompt general en `scripts/translate.py`.

////

## Pestañas y cajas coloreadas { #tabs-and-colored-boxes }

//// tab | Prueba

/// info | Información
Algo de texto
///

/// note | Nota
Algo de texto
///

/// note | Detalles técnicos
Algo de texto
///

/// check | Revisa
Algo de texto
///

/// tip | Consejo
Algo de texto
///

/// warning | Advertencia
Algo de texto
///

/// danger | Peligro
Algo de texto
///

////

//// tab | Información

Las pestañas y los bloques `Info`/`Note`/`Warning`/etc. deben tener la traducción de su título añadida después de una barra vertical (`|`).

Consulta las secciones `### Special blocks` y `### Tab blocks` en el prompt general en `scripts/translate.py`.

////

## Enlaces web e internos { #web-and-internal-links }

//// tab | Prueba

El texto del enlace debe traducirse, la dirección del enlace debe permanecer sin cambios:

* [Enlace al encabezado de arriba](#code-snippets)
* [Enlace interno](index.md#installation){.internal-link target=_blank}
* <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">Enlace externo</a>
* <a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">Enlace a un estilo</a>
* <a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">Enlace a un script</a>
* <a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">Enlace a una imagen</a>

El texto del enlace debe traducirse, la dirección del enlace debe apuntar a la traducción:

* <a href="https://fastapi.tiangolo.com/es/" class="external-link" target="_blank">Enlace a FastAPI</a>

////

//// tab | Información

Los enlaces deben traducirse, pero su dirección debe permanecer sin cambios. Una excepción son los enlaces absolutos a páginas de la documentación de FastAPI. En ese caso deben enlazar a la traducción.

Consulta la sección `### Links` en el prompt general en `scripts/translate.py`.

////

## Elementos HTML "abbr" { #html-abbr-elements }

//// tab | Prueba

Aquí algunas cosas envueltas en elementos HTML "abbr" (algunas son inventadas):

### El abbr da una frase completa { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done – Hacer las cosas">GTD</abbr>
* <abbr title="less than – menor que"><code>lt</code></abbr>
* <abbr title="XML Web Token – Token web XML">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface – Interfaz de pasarela de servidor paralela">PSGI</abbr>

### El abbr da una explicación { #the-abbr-gives-an-explanation }

* <abbr title="Un grupo de máquinas configuradas para estar conectadas y trabajar juntas de alguna manera.">clúster</abbr>
* <abbr title="Un método de machine learning que usa redes neuronales artificiales con numerosas capas ocultas entre las capas de entrada y salida, desarrollando así una estructura interna completa">Deep Learning</abbr>

### El abbr da una frase completa y una explicación { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network – Red de Desarrolladores de Mozilla: documentación para desarrolladores, escrita por la gente de Firefox">MDN</abbr>
* <abbr title="Input/Output – Entrada/Salida: lectura o escritura de disco, comunicaciones de red.">I/O</abbr>.

////

//// tab | Información

Los atributos "title" de los elementos "abbr" se traducen siguiendo instrucciones específicas.

Las traducciones pueden añadir sus propios elementos "abbr" que el LLM no debe eliminar. P. ej., para explicar palabras en inglés.

Consulta la sección `### HTML abbr elements` en el prompt general en `scripts/translate.py`.

////

## Encabezados { #headings }

//// tab | Prueba

### Desarrolla una webapp - un tutorial { #develop-a-webapp-a-tutorial }

Hola.

### Anotaciones de tipos y -anotaciones { #type-hints-and-annotations }

Hola de nuevo.

### Superclases y subclases { #super-and-subclasses }

Hola de nuevo.

////

//// tab | Información

La única regla estricta para los encabezados es que el LLM deje la parte del hash dentro de llaves sin cambios, lo que asegura que los enlaces no se rompan.

Consulta la sección `### Headings` en el prompt general en `scripts/translate.py`.

Para instrucciones específicas del idioma, mira p. ej. la sección `### Headings` en `docs/de/llm-prompt.md`.

////

## Términos usados en la documentación { #terms-used-in-the-docs }

//// tab | Prueba

* tú
* tu

* p. ej.
* etc.

* `foo` como un `int`
* `bar` como un `str`
* `baz` como una `list`

* el Tutorial - Guía de usuario
* la Guía de usuario avanzada
* la documentación de SQLModel
* la documentación de la API
* la documentación automática

* Ciencia de datos
* Deep Learning
* Machine Learning
* Inyección de dependencias
* autenticación HTTP Basic
* HTTP Digest
* formato ISO
* el estándar JSON Schema
* el JSON Schema
* la definición del esquema
* Flujo de contraseña
* Móvil

* obsoleto
* diseñado
* inválido
* sobre la marcha
* estándar
* por defecto
* sensible a mayúsculas/minúsculas
* insensible a mayúsculas/minúsculas

* servir la aplicación
* servir la página

* la app
* la aplicación

* la request
* la response
* la response de error

* la path operation
* el decorador de path operation
* la path operation function

* el body
* el request body
* el response body
* el body JSON
* el body del formulario
* el body de archivo
* el cuerpo de la función

* el parámetro
* el parámetro del body
* el parámetro del path
* el parámetro de query
* el parámetro de cookie
* el parámetro de header
* el parámetro del formulario
* el parámetro de la función

* el evento
* el evento de inicio
* el inicio del servidor
* el evento de apagado
* el evento de lifespan

* el manejador
* el manejador de eventos
* el manejador de excepciones
* manejar

* el modelo
* el modelo de Pydantic
* el modelo de datos
* el modelo de base de datos
* el modelo de formulario
* el objeto del modelo

* la clase
* la clase base
* la clase padre
* la subclase
* la clase hija
* la clase hermana
* el método de clase

* el header
* los headers
* el header de autorización
* el header `Authorization`
* el header Forwarded

* el sistema de inyección de dependencias
* la dependencia
* el dependable
* el dependiente

* limitado por I/O
* limitado por CPU
* concurrencia
* paralelismo
* multiprocesamiento

* la variable de entorno
* la variable de entorno
* el `PATH`
* la variable `PATH`

* la autenticación
* el proveedor de autenticación
* la autorización
* el formulario de autorización
* el proveedor de autorización
* el usuario se autentica
* el sistema autentica al usuario

* la CLI
* la interfaz de línea de comandos

* el servidor
* el cliente

* el proveedor en la nube
* el servicio en la nube

* el desarrollo
* las etapas de desarrollo

* el dict
* el diccionario
* la enumeración
* el enum
* el miembro del enum

* el codificador
* el decodificador
* codificar
* decodificar

* la excepción
* lanzar

* la expresión
* el statement

* el frontend
* el backend

* la discusión de GitHub
* el issue de GitHub

* el rendimiento
* la optimización de rendimiento

* el tipo de retorno
* el valor de retorno

* la seguridad
* el esquema de seguridad

* la tarea
* la tarea en segundo plano
* la función de tarea

* la plantilla
* el motor de plantillas

* la anotación de tipos
* la anotación de tipos

* el worker del servidor
* el worker de Uvicorn
* el Gunicorn Worker
* el worker process
* la worker class
* la carga de trabajo

* el despliegue
* desplegar

* el SDK
* el kit de desarrollo de software

* el `APIRouter`
* el `requirements.txt`
* el Bearer Token
* el cambio incompatible
* el bug
* el botón
* el invocable
* el código
* el commit
* el context manager
* la corrutina
* la sesión de base de datos
* el disco
* el dominio
* el motor
* el X falso
* el método HTTP GET
* el ítem
* el paquete
* el lifespan
* el bloqueo
* el middleware
* la aplicación móvil
* el módulo
* el montaje
* la red
* el origen
* el override
* el payload
* el procesador
* la propiedad
* el proxy
* el pull request
* la query
* la RAM
* la máquina remota
* el código de estado
* el string
* la etiqueta
* el framework web
* el comodín
* devolver
* validar

////

//// tab | Información

Esta es una lista no completa y no normativa de términos (mayormente) técnicos vistos en la documentación. Puede ayudar a la persona que diseña el prompt a identificar para qué términos el LLM necesita una mano. Por ejemplo cuando sigue revirtiendo una buena traducción a una traducción subóptima. O cuando tiene problemas conjugando/declinando un término en tu idioma.

Mira p. ej. la sección `### List of English terms and their preferred German translations` en `docs/de/llm-prompt.md`.

////
