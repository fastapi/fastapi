from pydantic import BaseModel


def forwardref_method(input: "ForwardRef") -> "ForwardRef":
    return ForwardRef(x=input.x + 1)


class ForwardRef(BaseModel):
    x: int = 0
