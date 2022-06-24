from pydantic import BaseModel


def forwardref_method(input: "ForwardRef") -> "ForwardRef":
    return ForwardRef()


class ForwardRef(BaseModel):
    x: int = 0
