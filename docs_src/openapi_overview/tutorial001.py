from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI(
    title="The title of the API",
    description="""
possibly lengthy description of the api including

newlines and `formating`
    """,
    version="Any string but please use semver (1.0.0-beta)",
)


class CustomError(BaseModel):
    cause: str


class Item(BaseModel):
    id: str = Field(
        title="Short title of the field",
        description="Looooooooonger description what the filed is used for etc.",
        example="what this is",
    )
    q: int = Field(
        0,
        description="""The first parameter defines the default value.
        Also numeric validation are possible here but are
        better placed at the related query""",
        ge=-2,
    )


@app.get(
    "/items/{item_id}",
    # description="This takes precedence over the docstring, but "
    #             "docstring provides more formatting options",
    summary="Short description shown when accordion is closed",
    tags=["Endpoint group1", "Endpoint group 2"],
    name="is only used in the operation id of the swagger spec",
    # Response model is used as 200 response
    response_model=Item,
    responses={
        201: {
            "description": "Custom description of the status code",
            "content": {
                "application/json": {
                    "example": {
                        "my_field_1": "my_value_1",
                        "my_field_2": "my_value_2",
                        "my_field_3": [
                            {"more_json_contents": 0.9842327805523402, "lang": "fra"}
                        ],
                    }
                }
            },
        },
        401: {
            "description": "Access denied",
            "content": {
                "application/json": {
                    "example": {"details": "User X does not have permission Y"}
                }
            },
        },
        500: {"model": CustomError},
    },
)
async def read_items(
    *,
    item_id: int = Path(..., description="The ID of the item to get"),
    q: int = Query(
        ...,
        deprecated=True,
        description="numeric comparators are also rendered in swagger",
        title="used for links and redoc",
        ge=0,
        example=42,
    )
):
    """
    This is rendered in the endpoint documentation if the `description`
    is not set in the endpoint definition. It provides extensive
    formatting option such as:

    * bullet
    * points

    inline `code`

        code blocks

    Python docstring keywords like `Args:` are ignored though.
    """
    return Item(item_id=item_id, q=q)
