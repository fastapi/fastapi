# GraphQL

Como **FastAPI** está basado en el estándar **ASGI**, es muy fácil integrar cualquier library **GraphQL** que sea compatible con ASGI.

Puedes combinar *operaciones de path* regulares de la library de FastAPI con GraphQL en la misma aplicación.

/// tip | Consejo

**GraphQL** resuelve algunos casos de uso específicos.

Tiene **ventajas** y **desventajas** cuando lo comparas con **APIs web** comunes.

Asegúrate de evaluar si los **beneficios** para tu caso de uso compensan las **desventajas.** 🤓

///

## Librerías GraphQL

Aquí hay algunas de las libraries de **GraphQL** que tienen soporte con **ASGI** las cuales podrías usar con **FastAPI**:

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * Con <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">documentación para FastAPI</a>
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * Con <a href="https://ariadnegraphql.org/docs/fastapi-integration" class="external-link" target="_blank">documentación para FastAPI</a>
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * Con <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> para proveer integración con ASGI
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * Con <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>

## GraphQL con Strawberry

Si necesitas o quieres trabajar con **GraphQL**, <a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a> es la library **recomendada** por el diseño más cercano a **FastAPI**, el cual es completamente basado en **anotaciones de tipo**.

Dependiendo de tus casos de uso, podrías preferir usar una library diferente, pero si me preguntas, probablemente te recomendaría **Strawberry**.

Aquí hay una pequeña muestra de cómo podrías integrar Strawberry con FastAPI:

```Python hl_lines="3  22  25-26"
{!../../../docs_src/graphql/tutorial001.py!}
```

Puedes aprender más sobre Strawberry en la <a href="https://strawberry.rocks/" class="external-link" target="_blank">documentación de Strawberry</a>.

Y también en la documentación sobre <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">Strawberry con FastAPI</a>.

## Clase obsoleta `GraphQLApp` en Starlette

Versiones anteriores de Starlette incluyen la clase `GraphQLApp` para integrarlo con <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>.

Esto fue marcado como obsoleto en Starlette, pero si aún tienes código que lo usa, puedes fácilmente **migrar** a <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>, la cual cubre el mismo caso de uso y tiene una **interfaz casi idéntica.**

/// tip | Consejo

Si necesitas GraphQL, te recomendaría revisar <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>, que es basada en anotaciones de tipo en vez de clases y tipos personalizados.

///

## Aprende más

Puedes aprender más acerca de **GraphQL** en la <a href="https://graphql.org/" class="external-link" target="_blank">documentación oficial de GraphQL</a>.

También puedes leer más acerca de cada library descrita anteriormente en sus enlaces.
