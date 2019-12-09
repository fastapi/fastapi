from enum import Enum
from typing import Any, Dict, List, Optional, Union

from fastapi.logger import logger
from pydantic import BaseModel

try:
    from pydantic import AnyUrl, Field
except ImportError:  # pragma: nocover
    # TODO: remove when removing support for Pydantic < 1.0.0
    from pydantic import Schema as Field  # type: ignore
    from pydantic import UrlStr as AnyUrl  # type: ignore

try:
    import email_validator

    assert email_validator  # make autoflake ignore the unused import
    try:
        from pydantic import EmailStr
    except ImportError:  # pragma: nocover
        # TODO: remove when removing support for Pydantic < 1.0.0
        from pydantic.types import EmailStr  # type: ignore
except ImportError:  # pragma: no cover
    logger.info(
        "email-validator not installed, email fields will be treated as str.\n"
        "To install, run: pip install email-validator"
    )

    class EmailStr(str):  # type: ignore
        pass


class Contact(BaseModel):
    name: Optional[str] = None
    url: Optional[AnyUrl] = None
    email: Optional[EmailStr] = None


class License(BaseModel):
    name: str
    url: Optional[AnyUrl] = None


class Info(BaseModel):
    title: str
    description: Optional[str] = None
    termsOfService: Optional[str] = None
    contact: Optional[Contact] = None
    license: Optional[License] = None
    version: str


class ServerVariable(BaseModel):
    enum: Optional[List[str]] = None
    default: str
    description: Optional[str] = None


class Server(BaseModel):
    url: AnyUrl
    description: Optional[str] = None
    variables: Optional[Dict[str, ServerVariable]] = None


class Reference(BaseModel):
    ref: str = Field(..., alias="$ref")


class Discriminator(BaseModel):
    propertyName: str
    mapping: Optional[Dict[str, str]] = None


class XML(BaseModel):
    name: Optional[str] = None
    namespace: Optional[str] = None
    prefix: Optional[str] = None
    attribute: Optional[bool] = None
    wrapped: Optional[bool] = None


class ExternalDocumentation(BaseModel):
    description: Optional[str] = None
    url: AnyUrl


class SchemaBase(BaseModel):
    ref: Optional[str] = Field(None, alias="$ref")
    title: Optional[str] = None
    multipleOf: Optional[float] = None
    maximum: Optional[float] = None
    exclusiveMaximum: Optional[float] = None
    minimum: Optional[float] = None
    exclusiveMinimum: Optional[float] = None
    maxLength: Optional[int] = Field(None, gte=0)
    minLength: Optional[int] = Field(None, gte=0)
    pattern: Optional[str] = None
    maxItems: Optional[int] = Field(None, gte=0)
    minItems: Optional[int] = Field(None, gte=0)
    uniqueItems: Optional[bool] = None
    maxProperties: Optional[int] = Field(None, gte=0)
    minProperties: Optional[int] = Field(None, gte=0)
    required: Optional[List[str]] = None
    enum: Optional[List[str]] = None
    type: Optional[str] = None
    allOf: Optional[List[Any]] = None
    oneOf: Optional[List[Any]] = None
    anyOf: Optional[List[Any]] = None
    not_: Optional[List[Any]] = Field(None, alias="not")
    items: Optional[Any] = None
    properties: Optional[Dict[str, Any]] = None
    additionalProperties: Optional[Union[Dict[str, Any], bool]] = None
    description: Optional[str] = None
    format: Optional[str] = None
    default: Optional[Any] = None
    nullable: Optional[bool] = None
    discriminator: Optional[Discriminator] = None
    readOnly: Optional[bool] = None
    writeOnly: Optional[bool] = None
    xml: Optional[XML] = None
    externalDocs: Optional[ExternalDocumentation] = None
    example: Optional[Any] = None
    deprecated: Optional[bool] = None


class Schema(SchemaBase):
    allOf: Optional[List[SchemaBase]] = None
    oneOf: Optional[List[SchemaBase]] = None
    anyOf: Optional[List[SchemaBase]] = None
    not_: Optional[List[SchemaBase]] = Field(None, alias="not")
    items: Optional[SchemaBase] = None
    properties: Optional[Dict[str, SchemaBase]] = None
    additionalProperties: Optional[Union[Dict[str, Any], bool]] = None


class Example(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    value: Optional[Any] = None
    externalValue: Optional[AnyUrl] = None


class ParameterInType(Enum):
    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"


class Encoding(BaseModel):
    contentType: Optional[str] = None
    # Workaround OpenAPI recursive reference, using Any
    headers: Optional[Dict[str, Union[Any, Reference]]] = None
    style: Optional[str] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = None


class MediaType(BaseModel):
    schema_: Optional[Union[Schema, Reference]] = Field(None, alias="schema")
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    encoding: Optional[Dict[str, Encoding]] = None


class ParameterBase(BaseModel):
    description: Optional[str] = None
    required: Optional[bool] = None
    deprecated: Optional[bool] = None
    # Serialization rules for simple scenarios
    style: Optional[str] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = None
    schema_: Optional[Union[Schema, Reference]] = Field(None, alias="schema")
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    # Serialization rules for more complex scenarios
    content: Optional[Dict[str, MediaType]] = None


class Parameter(ParameterBase):
    name: str
    in_: ParameterInType = Field(..., alias="in")


class Header(ParameterBase):
    pass


# Workaround OpenAPI recursive reference
class EncodingWithHeaders(Encoding):
    headers: Optional[Dict[str, Union[Header, Reference]]] = None


class RequestBody(BaseModel):
    description: Optional[str] = None
    content: Dict[str, MediaType]
    required: Optional[bool] = None


class Link(BaseModel):
    operationRef: Optional[str] = None
    operationId: Optional[str] = None
    parameters: Optional[Dict[str, Union[Any, str]]] = None
    requestBody: Optional[Union[Any, str]] = None
    description: Optional[str] = None
    server: Optional[Server] = None


class Response(BaseModel):
    description: str
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    content: Optional[Dict[str, MediaType]] = None
    links: Optional[Dict[str, Union[Link, Reference]]] = None


class Operation(BaseModel):
    tags: Optional[List[str]] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    externalDocs: Optional[ExternalDocumentation] = None
    operationId: Optional[str] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None
    requestBody: Optional[Union[RequestBody, Reference]] = None
    responses: Dict[str, Response]
    # Workaround OpenAPI recursive reference
    callbacks: Optional[Dict[str, Union[Dict[str, Any], Reference]]] = None
    deprecated: Optional[bool] = None
    security: Optional[List[Dict[str, List[str]]]] = None
    servers: Optional[List[Server]] = None


class PathItem(BaseModel):
    ref: Optional[str] = Field(None, alias="$ref")
    summary: Optional[str] = None
    description: Optional[str] = None
    get: Optional[Operation] = None
    put: Optional[Operation] = None
    post: Optional[Operation] = None
    delete: Optional[Operation] = None
    options: Optional[Operation] = None
    head: Optional[Operation] = None
    patch: Optional[Operation] = None
    trace: Optional[Operation] = None
    servers: Optional[List[Server]] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None


# Workaround OpenAPI recursive reference
class OperationWithCallbacks(BaseModel):
    callbacks: Optional[Dict[str, Union[Dict[str, PathItem], Reference]]] = None


class SecuritySchemeType(Enum):
    apiKey = "apiKey"
    http = "http"
    oauth2 = "oauth2"
    openIdConnect = "openIdConnect"


class SecurityBase(BaseModel):
    type_: SecuritySchemeType = Field(..., alias="type")
    description: Optional[str] = None


class APIKeyIn(Enum):
    query = "query"
    header = "header"
    cookie = "cookie"


class APIKey(SecurityBase):
    type_ = Field(SecuritySchemeType.apiKey, alias="type")
    in_: APIKeyIn = Field(..., alias="in")
    name: str


class HTTPBase(SecurityBase):
    type_ = Field(SecuritySchemeType.http, alias="type")
    scheme: str


class HTTPBearer(HTTPBase):
    scheme = "bearer"
    bearerFormat: Optional[str] = None


class OAuthFlow(BaseModel):
    refreshUrl: Optional[str] = None
    scopes: Dict[str, str] = {}


class OAuthFlowImplicit(OAuthFlow):
    authorizationUrl: str


class OAuthFlowPassword(OAuthFlow):
    tokenUrl: str


class OAuthFlowClientCredentials(OAuthFlow):
    tokenUrl: str


class OAuthFlowAuthorizationCode(OAuthFlow):
    authorizationUrl: str
    tokenUrl: str


class OAuthFlows(BaseModel):
    implicit: Optional[OAuthFlowImplicit] = None
    password: Optional[OAuthFlowPassword] = None
    clientCredentials: Optional[OAuthFlowClientCredentials] = None
    authorizationCode: Optional[OAuthFlowAuthorizationCode] = None


class OAuth2(SecurityBase):
    type_ = Field(SecuritySchemeType.oauth2, alias="type")
    flows: OAuthFlows


class OpenIdConnect(SecurityBase):
    type_ = Field(SecuritySchemeType.openIdConnect, alias="type")
    openIdConnectUrl: str


SecurityScheme = Union[APIKey, HTTPBase, OAuth2, OpenIdConnect, HTTPBearer]


class Components(BaseModel):
    schemas: Optional[Dict[str, Union[Schema, Reference]]] = None
    responses: Optional[Dict[str, Union[Response, Reference]]] = None
    parameters: Optional[Dict[str, Union[Parameter, Reference]]] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    requestBodies: Optional[Dict[str, Union[RequestBody, Reference]]] = None
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    securitySchemes: Optional[Dict[str, Union[SecurityScheme, Reference]]] = None
    links: Optional[Dict[str, Union[Link, Reference]]] = None
    callbacks: Optional[Dict[str, Union[Dict[str, PathItem], Reference]]] = None


class Tag(BaseModel):
    name: str
    description: Optional[str] = None
    externalDocs: Optional[ExternalDocumentation] = None


class OpenAPI(BaseModel):
    openapi: str
    info: Info
    servers: Optional[List[Server]] = None
    paths: Dict[str, PathItem]
    components: Optional[Components] = None
    security: Optional[List[Dict[str, List[str]]]] = None
    tags: Optional[List[Tag]] = None
    externalDocs: Optional[ExternalDocumentation] = None
