# Historia, Diseño y Futuro

Hace algún tiempo, <a href="https://github.com/fastapi/fastapi/issues/3#issuecomment-454956920" class="external-link" target="_blank">un usuario de **FastAPI** preguntó</a>:

> ¿Cuál es la historia de este proyecto? Parece haber surgido de la nada y ser increíble en pocas semanas [...]

Aquí hay un poquito de esa historia.

## Alternativas

He estado creando APIs con requisitos complejos durante varios años (Machine Learning, sistemas distribuidos, trabajos asíncronos, bases de datos NoSQL, etc.), liderando varios equipos de desarrolladores.

Como parte de eso, necesitaba investigar, probar y usar muchas alternativas.

La historia de **FastAPI** es en gran parte la historia de sus predecesores.

Como se dice en la sección [Alternativas](alternatives.md){.internal-link target=_blank}:

<blockquote markdown="1">

**FastAPI** no existiría si no fuera por el trabajo previo de otros.

Ha habido muchas herramientas creadas antes que han ayudado a inspirar su creación.

He estado evitando la creación de un nuevo framework durante varios años. Primero traté de resolver todas las funcionalidades cubiertas por **FastAPI** usando varios frameworks, complementos y herramientas diferentes.

Pero en algún momento, no había otra opción que crear algo que proporcionara todas estas funcionalidades, tomando las mejores ideas de herramientas anteriores y combinándolas de la mejor manera posible, usando funcionalidades del lenguaje que ni siquiera estaban disponibles antes (anotaciones de tipos de Python 3.6+).

</blockquote>

## Investigación

Al usar todas las alternativas anteriores, tuve la oportunidad de aprender de todas ellas, tomar ideas y combinarlas de la mejor manera que pude encontrar para mí y los equipos de desarrolladores con los que he trabajado.

Por ejemplo, estaba claro que idealmente debería estar basado en las anotaciones de tipos estándar de Python.

También, el mejor enfoque era usar estándares ya existentes.

Entonces, antes de siquiera empezar a programar **FastAPI**, pasé varios meses estudiando las especificaciones de OpenAPI, JSON Schema, OAuth2, etc. Entendiendo su relación, superposición y diferencias.

## Diseño

Luego pasé algún tiempo diseñando la "API" de desarrollador que quería tener como usuario (como desarrollador usando FastAPI).

Probé varias ideas en los editores de Python más populares: PyCharm, VS Code, editores basados en Jedi.

Según la última <a href="https://www.jetbrains.com/research/python-developers-survey-2018/#development-tools" class="external-link" target="_blank">Encuesta de Desarrolladores de Python</a>, estos editores cubren alrededor del 80% de los usuarios.

Esto significa que **FastAPI** fue específicamente probado con los editores usados por el 80% de los desarrolladores de Python. Y como la mayoría de los otros editores tienden a funcionar de manera similar, todos sus beneficios deberían funcionar prácticamente para todos los editores.

De esa manera, pude encontrar las mejores maneras de reducir la duplicación de código tanto como fuera posible, para tener autocompletado en todas partes, chequeos de tipos y errores, etc.

Todo de una manera que proporcionara la mejor experiencia de desarrollo para todos los desarrolladores.

## Requisitos

Después de probar varias alternativas, decidí que iba a usar <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">**Pydantic**</a> por sus ventajas.

Luego contribuí a este, para hacerlo totalmente compatible con JSON Schema, para soportar diferentes maneras de definir declaraciones de restricciones, y para mejorar el soporte de los editores (chequeo de tipos, autocompletado) basado en las pruebas en varios editores.

Durante el desarrollo, también contribuí a <a href="https://www.starlette.dev/" class="external-link" target="_blank">**Starlette**</a>, el otro requisito clave.

## Desarrollo

Para cuando comencé a crear el propio **FastAPI**, la mayoría de las piezas ya estaban en su lugar, el diseño estaba definido, los requisitos y herramientas estaban listos, y el conocimiento sobre los estándares y especificaciones estaba claro y fresco.

## Futuro

A este punto, ya está claro que **FastAPI** con sus ideas está siendo útil para muchas personas.

Está siendo elegido sobre alternativas anteriores por adaptarse mejor a muchos casos de uso.

Muchos desarrolladores y equipos ya dependen de **FastAPI** para sus proyectos (incluyéndome a mí y a mi equipo).

Pero aún así, hay muchas mejoras y funcionalidades por venir.

**FastAPI** tiene un gran futuro por delante.

Y [tu ayuda](help-fastapi.md){.internal-link target=_blank} es muy apreciada.
