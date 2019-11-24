from fastapi import FastAPI
from fastapi.routing import APIRoute

app = FastAPI()


@app.get("/items/")
async def read_items():
    return [{"item_id": "Foo"}]


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


use_route_names_as_operation_ids(app)
