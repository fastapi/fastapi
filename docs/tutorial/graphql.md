
**FastAPI** has optional support for GraphQL (provided by Starlette directly), using the `graphene` library.

You can combine normal FastAPI path operations with GraphQL on the same application.

## Import and use `graphene`

GraphQL is implemented with Graphene, you can check <a href="https://docs.graphene-python.org/en/latest/quickstart/" target="_blank">Graphene's docs</a> for more details.

Import `graphene` and define your GraphQL data:

```Python hl_lines="1 6 7 8 9 10"
{!./src/graphql/tutorial001.py!}
```

## Add Starlette's `GraphQLApp`

Then import and add Starlette's `GraphQLApp`:

```Python hl_lines="3 14"
{!./src/graphql/tutorial001.py!}
```

!!! info
    Here we are using `.add_route`, that is the way to add a route in Starlette (inherited by FastAPI) without declaring the specific operation (as would be with `.get()`, `.post()`, etc).

## Check it

Run it with Uvicorn and open your browser at <a href="http://127.0.0.1:8000" target="_blank">http://127.0.0.1:8000</a>.

You will see GraphiQL web user interface:

<img src="/img/tutorial/graphql/image01.png">

## Write test for it

```python
# run with pytest
import graphene
from graphene.test import Client
from graphql.execution.executors.asyncio import AsyncioExecutor


class Query(graphene.ObjectType):
    hey = graphene.String(name=graphene.String(default_value="stranger"))
    async_hey = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hey(self, info, name):
        return "hello!"

    async def resolve_async_hey(self, info, name):
        return "async hello!"


my_schema = graphene.Schema(query=Query)


def test_hey(event_loop):
    client = Client(my_schema)
    query = '''
    {
      hey
      asyncHey
    }
    '''
    executed = client.execute(query, executor=AsyncioExecutor())
    assert executed == {'data': {'hey': 'hello!', 'asyncHey': "async hello!"}}
```


## More details

For more details, including:

* Accessing request information
* Adding background tasks
* Using normal or async functions

check the official <a href="https://www.starlette.io/graphql/" target="_blank">Starlette GraphQL docs</a>.
