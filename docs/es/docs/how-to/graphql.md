# GraphQL { #graphql }

Como **FastAPI** se basa en el estándar **ASGI**, es muy fácil integrar cualquier paquete de **GraphQL** que también sea compatible con ASGI.

Puedes combinar las *path operations* normales de FastAPI con GraphQL en la misma aplicación.

/// tip | Consejo

**GraphQL** resuelve algunos casos de uso muy específicos.

Tiene **ventajas** y **desventajas** en comparación con las **APIs web** comunes.

Asegúrate de evaluar si los **beneficios** para tu caso de uso compensan los **inconvenientes**. 🤓

///

## Paquetes de GraphQL { #graphql-libraries }

Aquí algunos de los paquetes de **GraphQL** que tienen soporte **ASGI**. Podrías usarlos con **FastAPI**:

* [Strawberry](https://strawberry.rocks/) 🍓
    * Con [documentación para FastAPI](https://strawberry.rocks/docs/integrations/fastapi)
* [Ariadne](https://ariadnegraphql.org/)
    * Con [documentación para FastAPI](https://ariadnegraphql.org/docs/fastapi-integration)
* [Tartiflette](https://tartiflette.io/)
    * Con [Tartiflette ASGI](https://tartiflette.github.io/tartiflette-asgi/) para proporcionar integración con ASGI
* [Graphene](https://graphene-python.org/)
    * Con [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3)

## GraphQL con Strawberry { #graphql-with-strawberry }

Si necesitas o quieres trabajar con **GraphQL**, [**Strawberry**](https://strawberry.rocks/) es el paquete **recomendado** ya que tiene un diseño muy similar al diseño de **FastAPI**, todo basado en **anotaciones de tipos**.

Dependiendo de tu caso de uso, podrías preferir usar un paquete diferente, pero si me preguntas, probablemente te sugeriría probar **Strawberry**.

Aquí tienes una pequeña vista previa de cómo podrías integrar Strawberry con FastAPI:

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

Puedes aprender más sobre Strawberry en la [documentación de Strawberry](https://strawberry.rocks/).

Y también la documentación sobre [Strawberry con FastAPI](https://strawberry.rocks/docs/integrations/fastapi).

## `GraphQLApp` viejo de Starlette { #older-graphqlapp-from-starlette }

Las versiones anteriores de Starlette incluían una clase `GraphQLApp` para integrar con [Graphene](https://graphene-python.org/).

Fue deprecada de Starlette, pero si tienes código que lo usaba, puedes fácilmente **migrar** a [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3), que cubre el mismo caso de uso y tiene una **interfaz casi idéntica**.

/// tip | Consejo

Si necesitas GraphQL, aún te recomendaría revisar [Strawberry](https://strawberry.rocks/), ya que se basa en anotaciones de tipos en lugar de clases y tipos personalizados.

///

## Aprende Más { #learn-more }

Puedes aprender más sobre **GraphQL** en la [documentación oficial de GraphQL](https://graphql.org/).

También puedes leer más sobre cada uno de esos paquetes descritos arriba en sus enlaces.
