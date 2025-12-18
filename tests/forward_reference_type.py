from pydantic import BaseModel


def forwardref_method(input: "ForwardRefModel") -> "ForwardRefModel":
    return ForwardRefModel(x=input.x + 1)


class ForwardRefModel(BaseModel):
    x: int = 0
