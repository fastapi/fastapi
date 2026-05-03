from typing import Annotated

from fastapi import APIRouter, Body, Depends, FastAPI, Query
from pydantic import BaseModel

app = FastAPI()
records_router = APIRouter()


class ClientInfoBase(BaseModel):
    client_id: str


class RetailClientInfo(ClientInfoBase):
    region: str | None = None


class PartnerClientInfo(ClientInfoBase):
    contract_ref: str


class RecordBase(BaseModel):
    title: str


class CaseFileRecord(RecordBase):
    case_number: str


class ContractRecord(RecordBase):
    contract_id: str


def register_record_route(
    router: APIRouter,
    path: str,
    record_schema: type[RecordBase],
    client_schema: type[ClientInfoBase],
):
    @router.post(path)
    def create_record(
        client_info: Annotated[
            ClientInfoBase,
            Query(),
            Depends(client_schema),
        ],
        record: Annotated[
            RecordBase,
            Body(),
            Depends(record_schema),
        ],
    ):
        print(f"processing client #{client_info.client_id} data {record.title!r}")
        return {
            "client_info": client_info.model_dump(),
            "record": record.model_dump(),
        }

    return create_record


register_record_route(
    records_router,
    "/case-files/",
    CaseFileRecord,
    RetailClientInfo,
)
register_record_route(
    records_router,
    "/contracts/",
    ContractRecord,
    PartnerClientInfo,
)
app.include_router(
    records_router,
    prefix="/clients",
)
