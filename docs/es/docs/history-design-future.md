# Historia, Diseño y Futuro

Hace un tiempo, <a href="https://github.com/tiangolo/fastapi/issues/3#issuecomment-454956920" class="external-link" target="_blank">un usuario de **FastAPI** pregunto</a>:

> Cuál es la historia de este proyecto? Parece ser que vino de ningún lado a increíble en pocas semanas [...]

Aquí esta un breve fragmento de esa historia.

## Alternativas

He creado APIs con requerimientos complejos por algunos años (Machine Learning, sistemas distribuidos, tareas asíncronas, bases de datos NoSQL, etc), dirigiendo varios equipos de desarrolladores.

Como parte de eso, necesite investigarlo, hacer pruebas y usar muchas alternativas.

La historia de **FastAPI** es en gran parte la historia de sus predecesores.

Como mencione en la sección de [Alternativas](alternatives.md){.internal-link target=_blank}:

<blockquote markdown="1">

**FastAPI** no existiría si no fuera por el trabajo que otros hicieron previamente.

Han habido muchas herramientas, anteriormente creadas, que han ayudado a inspirar su creación.

Había estado evitando la creación de nuevos frameworks por algunos años. Primeramente trate de resolver todas las funciones cubiertas por **FastAPI** usando diferentes frameworks, plug-ins, y herramientas.

Pero llego un punto, donde no había otra opción mas que crear algo que pudiera tener todas estas funciones, tomando las mejores ideas de las herramientas previas, y combinarlas de la mejor manera posible, usando funciones del lenguaje que no estaban disponibles anteriormente (Python 3.6+ type hints).

</blockquote>

## Investigación

Al usar todas las herramientas anteriores, tuve la oportunidad de aprender de todas ellas, tomar ideas, y combinarlas de la mejor manera que pude encontrar por mi mismo, y los equipos de desarrolladores con los que he trabajado.

Por ejemplo, fue muy claro que idealmente debería de estar basado en los type hints estándar de Python.

Además, la mejor manera fue usar los estándares existentes.

Así que desde antes que comenzara a escribir una linea de código de **FastAPI**, pasé varios meses estudiando las especificaciones para OpenAPI, JSON Schema, OAuth2, etc. Entendiendo su relación, traslape y diferencias.

## Diseño

Luego estuve un tiempo diseñando la "API" de desarrollo que quería tener como usuario (como desarrollador usando FastAPI)

Probé muchas ideas en los editores de Python más populares: PyCharm, VS Code, y editores basados en Jedi.

Según la última <a href="https://www.jetbrains.com/research/python-developers-survey-2018/#development-tools" class="external-link" target="_blank">encuesta de desarrolladores de Python</a>, que cubre alrededor del 80% de los usuarios.

Eso quiere decir que **FastAPI** fue especialmente examinada con los editores que usan el 80% de los desarrolladores de Python. Y como la mayoría de los editores tienden a trabajar de forma similar, todos los beneficios deberían de funcionar prácticamente en todos los editores.

De esa manera, podía encontrar la mejor forma de reducir el código duplicado tanto como fue posible, tener completación en todos lados, revisión de tipos y errores, etc.

Todo de una manara que produjera la mejor experiencia de desarrollo para todos los desarrolladores.

## Requerimientos

Después de revisar distintas alternativas, decidí que iba a usar <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">**Pydantic**</a> por sus ventajas.

Luego contribuí al proyecto, para hacerlo compatible con JSON Schema, soportar diferentes maneras de definir constraint declarations, y mejorar el soporte de editores (revision de tipos, autocompletación) basado en las pruebas con diferentes editores.

Durante el desarrollo, también contribuí a <a href="https://www.starlette.io/" class="external-link" target="_blank">**Starlette**</a>, el otro requisito clave.

## Desarrollo

Para cuando llegó el día en que comencé a crear propiamente **FastAPI**, todas las piezas ya se encontraban en su lugar, el diseño estaba definido, los requerimientos y herramientas estaban listas, y el conocimiento sobre estándares y especificaciones era claro y freso.

## Futuro

Para este punto, ya esta claro que **FastAPI** incluyendo sus ideas es útil para mucha gente.

Está siendo escogido sobre las alternatives anteriores por cubrir muchos casos de uso de mejor manera.

Muchos desarrolladores y equipos dependen de **FastAPI** para sus proyectos (incluyendo a mi equipo y a mí)

Pero aun, hay muchas mejoras y funciones que están por venir.

**FastAPI** tiene un brillante futuro por delante.

Y [tu ayuda](help-fastapi.md){.internal-link target=_blank} es muy bien recibida.
