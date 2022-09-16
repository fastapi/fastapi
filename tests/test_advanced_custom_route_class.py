import base64
from collections import defaultdict
from typing import Any, Callable

import fastapi
import msgpack
from fastapi import APIRouter, FastAPI, status
from fastapi.routing import APIRoute, get_request_handler
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()


ACCEPT = "accept"
CONTENT_TYPE = "content-type"
JSON = "application/json"
MSGPACK = "application/x-msgpack"


class Base64Bytes(bytes):
    """Defines a Pydantic custom field type for deserializing base64
    string to bytes."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value) -> "Base64Bytes":
        if isinstance(value, str):
            value = base64.b64decode(value)
        return cls(value)


def base64_encode_as_str(data: bytes) -> str:
    """base64-encode binary data as ASCII string"""
    return base64.b64encode(data).decode("ascii")


custom_json_encoder = {
    bytes: base64_encode_as_str,  # Overrides Pydantic default `lambda o: o.decode()`
}


# Override default encoders for raw bytes fields to skip base64-encoding
# when using msgpack to serialize response payloads.
msgpack_encoder_override = defaultdict(
    lambda: str,
    {
        Base64Bytes: lambda x: x,  # Overrides custom_json_encoder's `base64_encode_as_str`
    },
)


class MsgpackRequest(Request):
    """Msgpack request class, used only if the request headers include
    'Content-Type: application/x-msgpack'."""

    media_type = MSGPACK

    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if body:
                # fastapi.tiangolo.com/advanced/custom-request-and-route/#handling-custom-request-body-encodings
                self._body = msgpack.unpackb(body)
        return self._body


class MsgpackResponse(Response):
    """Msgpack response class, used only if the request headers include
    'Accept: application/x-msgpack'."""

    media_type = MSGPACK

    def render(self, content: Any) -> bytes:
        return msgpack.packb(content)


class MultimediaRouteMixin(APIRoute):
    """A route "mixin" that handles 'application/x-msgpack' in addition to
    'application/json'. Its generic design simplifies adding support for more
    media types.

    Credit:
    https://github.com/tiangolo/fastapi/issues/521#issuecomment-646989249"""

    REQUEST_CLASSES = {
        MsgpackRequest.media_type: MsgpackRequest,
    }

    RESPONSE_CLASSES = {
        MsgpackResponse.media_type: MsgpackResponse,
    }

    def _get_multimedia_request_handler(self, mime_type):
        # Use custom response class or fall back on default self.response_class.
        response_class = self.RESPONSE_CLASSES.get(mime_type, self.response_class)
        # Use msgpack override encoder for msgpack responses.
        custom_encoder = msgpack_encoder_override if mime_type == MSGPACK else None

        return get_request_handler(
            dependant=self.dependant,
            body_field=self.body_field,
            status_code=self.status_code,
            response_class=response_class,  # Based on mime_type (see above)
            response_field=self.secure_cloned_response_field,
            response_model_include=self.response_model_include,
            response_model_exclude=self.response_model_exclude,
            response_model_by_alias=self.response_model_by_alias,
            response_model_exclude_unset=self.response_model_exclude_unset,
            response_model_exclude_defaults=self.response_model_exclude_defaults,
            response_model_exclude_none=self.response_model_exclude_none,
            dependency_overrides_provider=self.dependency_overrides_provider,
            custom_encoder=custom_encoder,  # Based on mime_type (see above)
        )

    def get_route_handler(self) -> Callable:
        """Overrides APIRoute.get_route_handler()"""

        async def multimedia_route_handler(request: Request) -> Response:

            content_type_headers = request.headers.get("Content-Type")
            try:
                request_cls = self.REQUEST_CLASSES[content_type_headers]
                request = request_cls(request.scope, request.receive)
            except KeyError:
                pass  # No handler for content_type, process request as-is.

            accept_headers = request.headers.get("Accept")
            route_handler = self._get_multimedia_request_handler(accept_headers)
            return await route_handler(request)

        return multimedia_route_handler


class ModelWithBytes(BaseModel):
    text: str
    raw: Base64Bytes

    class Config:
        json_encoders = custom_json_encoder
        validate_assignment = True


TEXT = "text"
BYTES = b"\x16\r\xd4)\x93>(\x04\x83\xcc\xc5\xd6"


test_dict = {
    "text": TEXT,
    "raw": BYTES,
}

base64_encoded_test_dict = {
    "text": TEXT,
    "raw": base64_encode_as_str(BYTES),
}


router = APIRouter(route_class=MultimediaRouteMixin)


@router.post("")
def post_model_with_bytes(body: ModelWithBytes) -> ModelWithBytes:
    assert body == ModelWithBytes(text=TEXT, raw=BYTES)
    assert body.__config__.json_encoders[bytes] is base64_encode_as_str
    # Verify jsonable_encoder did not mutate body.__config__
    TODO: assert Base64Bytes not in body.__config__.json_encoders
    return body


ENDPOINT_PATH = "/test_multimedia"

app.include_router(router=router, prefix=ENDPOINT_PATH)

client = TestClient(app)


def test_multimedia_route():
    """Test multimedia "middleware" (route mixin) for a simple payload
    that includes raw bytes for two combinations of  'Accept' and
    'Content-Type' HTTP headers."""

    class Saved:
        jsonable_encoder_mutates_config = (
            fastapi.encoders.jsonable_encoder_mutates_config
        )
        catchall_encoder = fastapi.encoders.catchall_encoder

    fastapi.encoders.jsonable_encoder_mutates_config = False
    fastapi.encoders.catchall_encoder = str

    # Test JSON-to-JSON POST
    for headers in (
        {},
        {ACCEPT: JSON},
        {CONTENT_TYPE: JSON},
        {ACCEPT: JSON, CONTENT_TYPE: JSON},
    ):
        resp = client.post(
            ENDPOINT_PATH,
            json=base64_encoded_test_dict,
            headers=headers,
        )
        assert resp.ok
        result = resp.json()
        assert resp.status_code == status.HTTP_200_OK
        assert result == base64_encoded_test_dict

    # Test JSON-to-msgpack POST
    for headers in (
        {ACCEPT: MSGPACK},
        {ACCEPT: MSGPACK, CONTENT_TYPE: JSON},
    ):
        resp = client.post(
            ENDPOINT_PATH,
            headers=headers,
            json=base64_encoded_test_dict,
        )
        assert resp.ok
        assert resp.status_code == status.HTTP_200_OK
        result = msgpack.unpackb(resp.content)
        assert result == test_dict

    # Test msgpack-to-JSON POST
    for headers in (
        {CONTENT_TYPE: MSGPACK},
        {ACCEPT: JSON, CONTENT_TYPE: MSGPACK},
    ):
        resp = client.post(
            ENDPOINT_PATH,
            headers=headers,
            data=msgpack.packb(test_dict),
        )
        assert resp.ok
        result = resp.json()
        assert resp.status_code == status.HTTP_200_OK
        assert result == base64_encoded_test_dict

    # Test msgpack-to-msgpack POST
    for headers in ({ACCEPT: MSGPACK, CONTENT_TYPE: MSGPACK},):
        resp = client.post(
            ENDPOINT_PATH,
            headers=headers,
            data=msgpack.packb(test_dict),
        )
        assert resp.ok
        assert resp.status_code == status.HTTP_200_OK
        result = msgpack.unpackb(resp.content)
        assert result == test_dict

    # Test for error when sending JSON but expecting msgpack
    resp = client.post(
        ENDPOINT_PATH,
        headers={CONTENT_TYPE: MSGPACK},
        json=base64_encoded_test_dict,
    )
    assert not resp.ok
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    # Test for error when sending msgpack but expecting JSON
    resp = client.post(
        ENDPOINT_PATH,
        headers={CONTENT_TYPE: JSON},
        data=msgpack.packb(test_dict),
    )
    assert not resp.ok
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    # Restore pre-test state
    fastapi.encoders.catchall_encoder = Saved.catchall_encoder
    fastapi.encoders.jsonable_encoder_mutates_config = (
        Saved.jsonable_encoder_mutates_config
    )
