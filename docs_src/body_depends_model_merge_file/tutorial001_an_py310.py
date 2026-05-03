from typing import Annotated, Any

from fastapi import APIRouter, Depends, FastAPI, File, UploadFile
from pydantic import BaseModel

app = FastAPI()
files_router = APIRouter()


class AttachmentBase(BaseModel):
    file: UploadFile


class CommentedAttachment(AttachmentBase):
    comment: str = ""


class NamedAttachment(AttachmentBase):
    name: str = ""


def register_upload_route(
    router: APIRouter,
    path: str,
    schema: type[AttachmentBase],
):
    @router.post(path)
    async def upload(
        attachment: Annotated[
            AttachmentBase,
            File(),
            Depends(schema),
        ],
    ) -> dict[str, Any]:
        return {
            "filename": attachment.file.filename,
            "content_type": attachment.file.content_type,
            "data": attachment.model_dump(exclude={"file"}),
        }

    return upload


register_upload_route(
    files_router,
    "/attachments/commented/",
    CommentedAttachment,
)
register_upload_route(
    files_router,
    "/attachments/named/",
    NamedAttachment,
)
app.include_router(
    files_router,
    prefix="/files",
)
