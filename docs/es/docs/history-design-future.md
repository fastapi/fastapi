# Historia, Diseño y Futuro

Hace tiempo, <a href="https://github.com/tiangolo/fastapi/issues/3#issuecomment-454956920" class="external-link" target="_blank">un usuario de **FastAPI** preguntó</a>:

> ¿Cuál es la historia de este proyecto? Parece haber llegado de la nada a increíble en pocas semanas. [...]

Aquí un poco de esa historia.

## Alternativas

Llevo varios años creando APIs con requerimientos complejos (<abbr title="Aprendizaje de Máquinas">Machine Learning</abbr>, sistemas distribuidos, trabajos asíncronos, bases de datos NoSQL, etc), liderando varios equipos de desarrolladores.

Como parte de eso, necesitaba investigar, probar y usar muchas alternativas.

La historia de **FastAPI** es en gran parte la historia de sus predecesores.

Como dije en la sección [Alternativas](alternatives.md){.internal-link target=_blank}:

<blockquote markdown="1">

**FastAPI** no existiría si no fuera por el trabajo previo de otros.

Ha habido muchas herramientas creadas antes, que han ayudado a inspirar su creación.

He estado evitando la creación de un nuevo marco durante varios años. Primero, traté de resolver todas las funciones cubiertas por **FastAPI** utilizando muchos frameworks, complementos y herramientas diferentes.

Pero en algún punto, no había otra opción que crear algo que proporcionara todas estas características, tomando las mejores ideas de herramientas anteriores y combinándolas de la mejor manera posible, usando características del lenguaje que ni siquiera estaban disponibles antes (Python 3.6+ <abbr title="sugerencias de tipo">type hints</abbr>).

</blockquote>

## Investigación

Al usar todas las alternativas anteriores tuve la oportunidad de aprender de todas ellas, tomar ideas y combinarlas de la mejor manera que pude encontrar para mí y los equipos de desarrolladores con los que he trabajado.

Por ejemplo, estaba claro que, idealmente, debería basarse en sugerencias de tipo estándar de Python (type hints).

Además, el mejor enfoque era utilizar estándares ya existentes.

Entonces, incluso antes de comenzar a codificar **FastAPI**, pasé varios meses estudiando las especificaciones de OpenAPI, JSON Schema, OAuth2, etc. Comprendiendo su relación, superposición y diferencias.

## Diseño

Luego pasé un tiempo diseñando la "API" de desarrollador que quería tener como usuario (como desarrollador que usa FastAPI).

Probé varias ideas en los editores de Python más populares: PyCharm, VS Code, editores basados en Jedi.

Por último <a href="https://www.jetbrains.com/research/python-developers-survey-2018/#development-tools" class="external-link" target="_blank">Encuesta de desarrolladores de Python</a>, que cubre alrededor del 80% de los usuarios.

Significa que **FastAPI** se probó específicamente con los editores utilizados por el 80 % de los desarrolladores de Python. Y como la mayoría de los otros editores tienden a funcionar de manera similar, todos sus beneficios deberían funcionar prácticamente en todos los editores.

De esa manera, pude encontrar las mejores formas de reducir la duplicación de código tanto como fuera posible, completamiento en todas partes, verificar tipos y errores, etc.

Todo de una manera que proporcionó la mejor experiencia de desarrollo para todos los desarrolladores.

## Requisitos

Después de probar varias alternativas, decidí que iba a usar <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">**Pydantic**</a> por sus ventajas.

Luego contribuí a él, para hacerlo totalmente compatible con JSON Schema, para admitir diferentes formas de definir declaraciones de restricciones y para mejorar el soporte del editor (comprobaciones de tipo, autocompletado) en función de las pruebas en varios editores.

Durante el desarrollo, también contribuí a <a href="https://www.starlette.io/" class="external-link" target="_blank">**Starlette**</a>, el otro requisito clave.

## Desarrollo

Cuando comencé a crear **FastAPI**, la mayoría de las piezas ya estaban en su lugar, el diseño estaba definido, los requisitos y las herramientas estaban listas, y el conocimiento sobre los estándares y especificaciones estaba claro y fresco.

## Futuro

A estas alturas, ya está claro que **FastAPI** con sus ideas está siendo útil para muchas personas.

Se está eligiendo sobre alternativas anteriores para adaptarse mejor a muchos casos de uso.

Muchos desarrolladores y equipos ya dependen de **FastAPI** para sus proyectos (incluidos mi equipo y yo).

Pero aún así, hay muchas mejoras y características por venir.

**FastAPI** tiene un gran futuro por delante.

Y [tu ayuda](help-fastapi.md){.internal-link target=_blank} es muy apreciad.
