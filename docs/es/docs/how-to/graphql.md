# GraphQL

Como **FastAPI** se basa en el estándar **ASGI**, es muy fácil integrar cualquier paquete de **GraphQL** que también sea compatible con ASGI.

Puedes combinar las *path operations* normales de FastAPI con GraphQL en la misma aplicación.

/// tip | Consejo

**GraphQL** resuelve algunos casos de uso muy específicos.

Tiene **ventajas** y **desventajas** en comparación con las **APIs web** comunes.

Asegúrate de evaluar si los **beneficios** para tu caso de uso compensan los **inconvenientes**. 🤓

///

## Paquetes de GraphQL

Aquí algunos de los paquetes de **GraphQL** que tienen soporte **ASGI**. Podrías usarlos con **FastAPI**:

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * Con <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">documentación para FastAPI</a>
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * Con <a href="https://ariadnegraphql.org/docs/fastapi-integration" class="external-link" target="_blank">documentación para FastAPI</a>
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * Con <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> para proporcionar integración con ASGI
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * Con <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>

## GraphQL con Strawberry

Si necesitas o quieres trabajar con **GraphQL**, <a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a> es el paquete **recomendado** ya que tiene un diseño muy similar al diseño de **FastAPI**, todo basado en **anotaciones de tipos**.

Dependiendo de tu caso de uso, podrías preferir usar un paquete diferente, pero si me preguntas, probablemente te sugeriría probar **Strawberry**.

Aquí tienes una pequeña vista previa de cómo podrías integrar Strawberry con FastAPI:

{* ../../docs_src/graphql/tutorial001.py hl[3,22,25:26] *}

Puedes aprender más sobre Strawberry en la <a href="https://strawberry.rocks/" class="external-link" target="_blank">documentación de Strawberry</a>.

Y también la documentación sobre <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">Strawberry con FastAPI</a>.

## `GraphQLApp` viejo de Starlette

Las versiones anteriores de Starlette incluían una clase `GraphQLApp` para integrar con <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>.

Fue deprecada de Starlette, pero si tienes código que lo usaba, puedes fácilmente **migrar** a <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>, que cubre el mismo caso de uso y tiene una **interfaz casi idéntica**.

/// tip | Consejo

Si necesitas GraphQL, aún te recomendaría revisar <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a>, ya que se basa en anotaciones de tipos en lugar de clases y tipos personalizados.

///

## Aprende Más

Puedes aprender más sobre **GraphQL** en la <a href="https://graphql.org/" class="external-link" target="_blank">documentación oficial de GraphQL</a>.

También puedes leer más sobre cada uno de esos paquetes descritos arriba en sus enlaces.
