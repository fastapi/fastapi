from typing import Any, Callable, Iterable, Type

from starlette.datastructures import UploadFile as StarletteUploadFile


class UploadFile(StarletteUploadFile):
    """An uploaded file included as part of the request data.

    Attributes:
        content_type (str): File content-type.
        file (typing.IO): TextIO or BinaryIO based object.
        filename (str): Filename.
    """

    @classmethod
    def __get_validators__(cls: Type["UploadFile"]) -> Iterable[Callable]:
        yield cls.validate

    @classmethod
    def validate(cls: Type["UploadFile"], v: Any) -> Any:
        """Validates file input.

        Args:
            v (Any): Possible `UploadFile` object to validate.

        Raises:
            ValueError: If object is not an instance of `UploadFile`.

        Returns:
            Any: `UploadFile` object.
        """
        if not isinstance(v, StarletteUploadFile):
            raise ValueError(f"Expected UploadFile, received: {type(v)}")
        return v
