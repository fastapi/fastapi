import json
from typing import Any, Dict

import pydantic as pyd
import pytest
from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute, RequestHandler
from fastapi.testclient import TestClient
from starlette.routing import Request


class CustomType(pyd.BaseModel):
    _TYPES: dict = {}
    _type: int

    @classmethod
    def from_type(cls, data: Dict[str, Any]):
        cls_type: int = data.get("_type")
        new_cls = cls._TYPES.get(cls_type)
        if new_cls is not None:
            return new_cls(**data.get("fields", {}))
        raise TypeError(f"{cls_type} is not a supported type")


class Payload(CustomType):
    _type: int = 1
    field: str


CustomType._TYPES.update({cls._type: cls for cls in [Payload]})


class CustomRequestHandler(RequestHandler):
    def custom_decoder(self, raw: bytes) -> str:
        data = json.loads(raw.decode())
        return CustomType.from_type(data)

    def get_body_decoder(self, request: Request):
        content_type = request.headers.get("content-type")
        if content_type == "application/x-custom-decoder":
            return self.custom_decoder

        return super().get_body_decoder(request)


class CustomAPIRoute(APIRoute):
    def __init__(
        self, *args, request_handler_class: RequestHandler = None, **kwargs
    ) -> None:
        super().__init__(
            *args,
            request_handler_class=request_handler_class or CustomRequestHandler,
            **kwargs,
        )


app = FastAPI()
router = APIRouter(route_class=CustomAPIRoute)


@router.post("/", response_model=Payload)
def post(payload: Payload):
    return payload


app.include_router(router=router)


client = TestClient(app)


@pytest.mark.parametrize(
    "expected_status,type_id,fields,response_payload",
    [
        (200, 1, {"field": "value"}, {"field": "value"}),
        (400, 2, {"field": "value"}, {"detail": "There was an error parsing the body"}),
    ],
)
def test_custom_decoder(expected_status, type_id, fields, response_payload):
    response = client.post(
        "/",
        json={"_type": type_id, "fields": fields},
        headers={"content-type": "application/x-custom-decoder"},
    )

    assert response.status_code == expected_status
    assert response.json() == response_payload


def test_normal_decoder_in_custom():
    response = client.post(
        "/",
        json={"field": "value"},
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 200
    assert response.json() == {"field": "value"}
