from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import (
    Annotated,
    Any,
    BinaryIO,
    TypeVar,
    cast,
)

from annotated_doc import Doc
from pydantic import GetJsonSchemaHandler
from starlette.datastructures import URL as URL  # noqa: F401
from starlette.datastructures import Address as Address  # noqa: F401
from starlette.datastructures import FormData as FormData  # noqa: F401
from starlette.datastructures import Headers as Headers  # noqa: F401
from starlette.datastructures import QueryParams as QueryParams  # noqa: F401
from starlette.datastructures import State as State  # noqa: F401
from starlette.datastructures import UploadFile as StarletteUploadFile
from starlette.exceptions import HTTPException


@dataclass
class ValidationResult:
    is_valid: Annotated[
        bool,
        Doc("Whether the file passed all validation checks."),
    ]
    file_size: Annotated[
        int | None,
        Doc("The size of the file in bytes."),
    ] = None
    content_type: Annotated[
        str | None,
        Doc("The content type of the request, from the headers."),
    ] = None


class UploadFile(StarletteUploadFile):
    """
    A file uploaded in a request.

    Define it as a *path operation function* (or dependency) parameter.

    If you are using a regular `def` function, you can use the `upload_file.file`
    attribute to access the raw standard Python file (blocking, not async), useful and
    needed for non-async code.

    Read more about it in the
    [FastAPI docs for Request Files](https://fastapi.tiangolo.com/tutorial/request-files/).

    ## Example

    ```python
    from typing import Annotated

    from fastapi import FastAPI, File, UploadFile

    app = FastAPI()


    @app.post("/files/")
    async def create_file(file: Annotated[bytes, File()]):
        return {"file_size": len(file)}


    @app.post("/uploadfile/")
    async def create_upload_file(file: UploadFile):
        return {"filename": file.filename}
    ```
    """

    file: Annotated[
        BinaryIO,
        Doc("The standard Python file object (non-async)."),
    ]
    filename: Annotated[str | None, Doc("The original file name.")]
    size: Annotated[int | None, Doc("The size of the file in bytes.")]
    headers: Annotated[Headers, Doc("The headers of the request.")]
    content_type: Annotated[
        str | None, Doc("The content type of the request, from the headers.")
    ]
    max_size: Annotated[
        int | None,
        Doc(
            """
            Maximum allowed file size in bytes. When set, files exceeding this size
            will fail validation with a 413 error.
            """
        ),
    ] = None
    allowed_content_types: Annotated[
        list[str] | None,
        Doc(
            """
            List of allowed MIME types for the uploaded file. When set, files with
            a content type not in this list will fail validation with a 415 error.
            """
        ),
    ] = None

    async def write(
        self,
        data: Annotated[
            bytes,
            Doc(
                """
                The bytes to write to the file.
                """
            ),
        ],
    ) -> None:
        """
        Write some bytes to the file.

        You normally wouldn't use this from a file you read in a request.

        To be awaitable, compatible with async, this is run in threadpool.
        """
        return await super().write(data)

    async def read(
        self,
        size: Annotated[
            int,
            Doc(
                """
                The number of bytes to read from the file.
                """
            ),
        ] = -1,
    ) -> bytes:
        """
        Read some bytes from the file.

        To be awaitable, compatible with async, this is run in threadpool.
        """
        return await super().read(size)

    async def seek(
        self,
        offset: Annotated[
            int,
            Doc(
                """
                The position in bytes to seek to in the file.
                """
            ),
        ],
    ) -> None:
        """
        Move to a position in the file.

        Any next read or write will be done from that position.

        To be awaitable, compatible with async, this is run in threadpool.
        """
        return await super().seek(offset)

    async def close(self) -> None:
        """
        Close the file.

        To be awaitable, compatible with async, this is run in threadpool.
        """
        return await super().close()

    def __init__(
        self,
        file: Annotated[
            BinaryIO,
            Doc("The file-like object to upload."),
        ],
        *,
        size: Annotated[
            int | None,
            Doc("The size of the file in bytes."),
        ] = None,
        filename: Annotated[
            str | None,
            Doc("The original file name."),
        ] = None,
        headers: Annotated[
            Headers | None,
            Doc("The headers of the request."),
        ] = None,
        max_size: Annotated[
            int | None,
            Doc(
                """
                Maximum allowed file size in bytes. When set, the `validate` method
                will raise ``HTTPException`` 413 if the file exceeds this limit.
                """
            ),
        ] = None,
        allowed_content_types: Annotated[
            list[str] | None,
            Doc(
                """
                List of allowed MIME types. When set, the `validate` method will
                raise ``HTTPException`` 415 if the file type is not in this list.
                """
            ),
        ] = None,
    ) -> None:
        super().__init__(file=file, size=size, filename=filename, headers=headers)
        self.max_size = max_size
        self.allowed_content_types = allowed_content_types

    async def validate(
        self,
    ) -> ValidationResult:
        """
        Validate the file against the configured size and content type constraints.

        If validation passes, returns a :class:`ValidationResult` with ``is_valid``
        set to ``True`` and the file's metadata.

        If ``max_size`` is set and the file exceeds it, raises ``HTTPException``
        with status 413.

        If ``allowed_content_types`` is set and the file's content type is not in
        the list, raises ``HTTPException`` with status 415.
        """
        if self.max_size is not None and self.size is not None and self.size > self.max_size:
            raise HTTPException(
                status_code=413,
                detail=f"File size {self.size} exceeds the maximum allowed size of {self.max_size} bytes",
            )
        if self.allowed_content_types is not None and self.content_type not in self.allowed_content_types:
            raise HTTPException(
                status_code=415,
                detail=(
                    f"Content type '{self.content_type}' is not allowed. "
                    f"Must be one of: {self.allowed_content_types}"
                ),
            )
        return ValidationResult(is_valid=True, file_size=self.size, content_type=self.content_type)

    @classmethod
    def _validate(cls, __input_value: Any, _: Any) -> "UploadFile":
        if not isinstance(__input_value, StarletteUploadFile):
            raise ValueError(f"Expected UploadFile, received: {type(__input_value)}")
        return cast(UploadFile, __input_value)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: Mapping[str, Any], handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        return {"type": "string", "contentMediaType": "application/octet-stream"}

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: Callable[[Any], Mapping[str, Any]]
    ) -> Mapping[str, Any]:
        from ._compat.v2 import with_info_plain_validator_function

        return with_info_plain_validator_function(cls._validate)


class DefaultPlaceholder:
    """
    You shouldn't use this class directly.

    It's used internally to recognize when a default value has been overwritten, even
    if the overridden default value was truthy.
    """

    def __init__(self, value: Any):
        self.value = value

    def __bool__(self) -> bool:
        return bool(self.value)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, DefaultPlaceholder) and o.value == self.value


DefaultType = TypeVar("DefaultType")


def Default(value: DefaultType) -> DefaultType:
    """
    You shouldn't use this function directly.

    It's used internally to recognize when a default value has been overwritten, even
    if the overridden default value was truthy.
    """
    return DefaultPlaceholder(value)  # type: ignore


# Sentinel for "parameter not provided" in Param/FieldInfo.
# Typed as None to satisfy ty
_Unset = Default(None)
