# Historia, Diseño y Futuro

Hace algún tiempo, <a href="https://github.com/tiangolo/fastapi/issues/3#issuecomment-454956920" class="external-link" target="_blank">a **FastAPI** un usuario preguntó</a>:

> ¿Cuál es la historia de este proyecto? Parece haber llegado de la nada a ser asombroso en unas pocas semanas [...]

Aquí te explico.

## Alternativas

Llevo varios años creando APIs con requisitos complejos (Machine Learning, sistemas distribuidos, trabajos asíncronos, bases de datos NoSQL, etc), liderando varios equipos de desarrolladores.

Como parte de eso, necesitaba investigar, probar y utilizar muchas alternativas.

La historia de **FastAPI** es en gran parte la historia de sus predecesores.

Como se dice en la sección. [Alternativas](alternatives.md){.internal-link target=_blank}:

<blockquote markdown="1">

**FastAPI** no existiría si no fuera por el trabajo previo de otros.

Se han creado muchas herramientas antes que han ayudado a inspirar su creación.

Llevo varios años evitando la creación de un nuevo frameworks. Primero intenté resolver todas las funciones cubiertas por **FastAPI** utilizando muchos frameworks, plug-ins y herramientas diferentes.

Pero en algún momento, no hubo otra opción que crear algo que proporcionara todas estas características, tomando las mejores ideas de herramientas anteriores y combinándolas de la mejor manera posible, usando características de lenguaje que ni siquiera estaban disponibles antes (Python 3.6+ <abbr title="tambien conocido en español como: sujerencias de tipo">type hints</abbr>).

</blockquote>

## Investigación

Al utilizar todas las alternativas anteriores tuve la oportunidad de aprender de todas ellas, tomar ideas y combinarlas de la mejor manera que pude encontrar para mí y los equipos de desarrolladores con los que he trabajado.

Por ejemplo, estaba claro que lo ideal sería basarse en <abbr title="tambien conocido en español como: sujerencias de tipos">type hints</abbr> de Python estándar.

Además, el mejor enfoque era utilizar estándares ya existentes.

Entonces, incluso antes de comenzar a codificar **FastAPI**, pasé varios meses estudiando las especificaciones de OpenAPI, JSON Schema, OAuth2, etc. Entendiendo su relación, superposición y diferencias.

## Diseño

Luego dediqué algún tiempo a diseñar la "API" de desarrollador que quería tener como usuario (como desarrollador que usa FastAPI).

Probé varias ideas en los editores de Python más populares: PyCharm, VS Code, editores basados en Jedi.

Según la última <a href="https://www.jetbrains.com/research/python-developers-survey-2018/#development-tools" class="external-link" target="_blank">Encuesta para Desarrolladores de Python</a>, que cubre alrededor del 80% de los usuarios.

Significa que **FastAPI** fue probado específicamente con los editores utilizados por el 80% de los desarrolladores de Python. Y como la mayoría de los demás editores tienden a trabajar de manera similar, todos sus beneficios deberían funcionar para prácticamente todos los editores.

De esa manera podría encontrar las mejores formas de reducir la duplicación de código tanto como sea posible, completarlo en todas partes, verificar tipos y errores, etc.

Todo de una manera que brindó la mejor experiencia de desarrollo para todos los desarrolladores.

## Requisitos

Después de probar varias alternativas, decidí que iba a utilizar <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">**Pydantic**</a> por sus ventajas.

Luego contribuí para que fuera totalmente compatible con el esquema JSON, para soportar diferentes formas de definir declaraciones de restricciones y para mejorar la compatibilidad con el editor (verificaciones de tipos, autocompletado) basado en las pruebas en varios editores.

Durante el desarrollo, también contribuí a <a href="https://www.starlette.io/" class="external-link" target="_blank">**Starlette**</a>, el otro requisito clave.

## Desarrollo

Cuando comencé a crear **FastAPI**, la mayoría de las piezas ya estaban en su lugar, el diseño estaba definido, los requisitos y las herramientas estaban listos y el conocimiento sobre los estándares y especificaciones era claro y actualizado.

## Futuro

En este punto, ya está claro que **FastAPI** con sus ideas está siendo útil para muchas personas.

Se está eligiendo entre alternativas anteriores porque se adapta mejor a muchos casos de uso.

Muchos desarrolladores y equipos ya dependen de **FastAPI** para sus proyectos (incluidos mi equipo y yo).

Pero aún así, quedan muchas mejoras y funciones por venir.

**FastAPI** tiene un gran futuro por delante.

Y [tu ayuda](help-fastapi.md){.internal-link target=_blank} es muy apreciada.
