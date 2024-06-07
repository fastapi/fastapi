# GraphQL

Como **FastAPI** esta basado en el estándar **ASGI**, es muy facil integrar cualquier librería **GraphQL** que sea compatible con ASGI.

Tu puedes combinar *operaciones regulares de ruta* de la librería de FastAPI con GraphQL en la misma aplicación.

!!! tip
    **GraphQL** resuelve algunos casos de uso específicos.

    Tiene **ventajas** y **desventajas** cuando lo comparas con **APIs web** comunes.

    Asegúrate de evaluar sí los **beneficios** para tu caso de uso compensan las **desventajas.**🤓

## Librerías GraphQL

Aquí hay algunas de las librerías de **GraphQL** que tienen soporte con **ASGI** las cuales podrías usar con **FastAPI**:

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * Con <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">documentación para FastAPI</a>
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * Con <a href="https://ariadnegraphql.org/docs/starlette-integration" class="external-link" target="_blank">documentación para Starlette</a> (Aplica para FastAPI)
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * Con <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> para proveer integración con ASGI
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * Con <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>

## GraphQL con Strawberry

Sí necesitas o quieres trabajar con **GraphQL**, <a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a> es la librería **recomendada** por el diseño mas cercano a **FastAPI**, el cual es completamente basado en **anotaciones de tipo**.

Dependiendo de tus casos de uso, podrías preferir usar una librería diferente, pero sí tu me preguntas, probablemente te recomendaría **Strawberry**.

Aquí hay una pequeña muestra de cómo podrías integrar Strawberry con FastAPI:

```Python hl_lines="3  22  25-26"
{!../../../docs_src/graphql/tutorial001.py!}
```

Puedes aprender mas sobre Strawberry en la <a href="https://strawberry.rocks/" class="external-link" target="_blank">documentación de Strawbeery</a>.

Y también en la documentación sobre <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">Strawberry con FastAPI</a>.

## Clase deprecada `GraphQLApp` en Starlette

Versiones anteriores de Starlette incluyen la clase `GraphQLApp` para integrarlo con <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>.

Esto fue deprecado de Starlette, pero sí aún tienes código que lo usa, puedes facilmente **migrar** a <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>, la cual cubre el mismo caso de uso y tiene una **interfaz casi idéntica.**

!!! tip
    Sí tu necesitas GraphQL, aún te recomendaría revisar <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>, que es basada en anotaciones de tipo en vez de clases y tipos personalizados. 

## Aprende más

Puedes aprender más acerca de **GraphQL** en la <a href="https://graphql.org/" class="external-link" target="_blank">documentación oficial de GraphQL</a>.

También puedes leer más acerca de cada librería descrita anteriormente en sus enlaces.
