# GraphQL

**FastAPI** cuenta con soporte para GraphQL, usando la librería de `graphene` de Starlette.

Puedes combinar *operaciones de <abbr title="ruta">path</abbr>* normales de FastAPI con GraphQL en la misma aplicación.

## Importar y utilizar `graphene`

GraphQL ha sido implementado mediante Graphene, puedes revisar la <a href="https://docs.graphene-python.org/en/latest/quickstart/" class="external-link" target="_blank"> documentación oficial de Graphene </a> para más detalles.

Importa `graphene` y define la información de GraphQL :

```Python hl_lines="1  6-10"
{!../../../docs_src/graphql/tutorial001.py!}
```

## Agrega `GraphQLApp` de Starlette :

Importa y agrega `GraphQLApp` de Starlette :

```Python hl_lines="3  14"
{!../../../docs_src/graphql/tutorial001.py!}
```

!!! info
    Aquí utilizamos `.add_route`, esta es la forma de añadir una ruta en Starlette (heredado por FastAPI) sin declarar la operación específica (que podría ser `.get()`, `.post()`, etc).

## Pruébalo

Ejecutalo con Uvicorn y abre tu navegador en <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Verás la interfaz web de usuarios de GraphQL :

<img src="https://fastapi.tiangolo.com/img/tutorial/graphql/image01.png">

## Más detalles

Para más detalles sobre:

* Acceso a la información solicitada
* Añadir tareas en segundo plano
* Usar funciones normales o asíncronas

Revisa la <a href="https://www.starlette.io/graphql/" class="external-link" target="_blank"> documentación oficial de GraphQL con  Starlette </a>.
