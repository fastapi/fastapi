import json
from datetime import date, datetime, time, timedelta
from enum import Enum
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from typing import Dict, List, Tuple, Union
from uuid import UUID

from fastapi import FastAPI
from pydantic import (
    DSN,
    UUID1,
    UUID3,
    UUID4,
    UUID5,
    BaseModel,
    ConstrainedDecimal,
    Decimal,
    DirectoryPath,
    EmailStr,
    FilePath,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
    Json,
    NameEmail,
    NegativeFloat,
    NegativeInt,
    Path,
    PositiveFloat,
    PositiveInt,
    StrictStr,
    UrlStr,
    condecimal,
    confloat,
    conint,
    constr,
)
from starlette.testclient import TestClient


class Working(BaseModel):
    my_bool: bool
    my_str: str
    my_float: float
    my_int: int
    my_dict: dict
    # my_list: list
    # my_tuple: tuple
    # my_set: set
    my_List_str: List[str]
    # my_tuple_str_int: Tuple[str, int]
    my_dict_str_int: Dict[str, int]
    my_union_str_int: Union[str, int]
    # my_enum: Enum
    my_emailstr: EmailStr
    my_name_email: NameEmail
    my_urlstr: UrlStr
    my_dsn: DSN
    my_bytes: bytes
    my_decimal: Decimal
    my_uuid1: UUID1
    my_uuid3: UUID3
    my_uuid4: UUID4
    my_uuid5: UUID5
    my_uuid: UUID
    my_filepath: FilePath
    my_directorypath: DirectoryPath
    my_path: Path
    my_datetime: datetime
    my_date: date
    my_time: time
    my_timedelta: timedelta
    my_Json: Json
    my_IPvAnyAddress: IPvAnyAddress
    my_ipv4address: IPv4Address
    my_ipv6address: IPv6Address
    my_IPvAnyInterface: IPvAnyInterface
    my_ipv4interface: IPv4Interface
    my_ipv6interface: IPv6Interface
    my_IPvAnyNetwork: IPvAnyNetwork
    my_ipv4network: IPv4Network
    my_ipv6network: IPv6Network
    my_StrictStr: StrictStr
    my_ConstrainedStr: constr(regex="^text$", min_length=2, max_length=10)
    # my_conint: conint(gt=1, lt=6, multiple_of=2)
    # my_PositiveInt: PositiveInt
    # my_NegativeInt: NegativeInt
    # my_PositiveFloat: PositiveFloat
    # my_NegativeFloat: NegativeFloat
    my_ConstrainedDecimal: ConstrainedDecimal
    # my_condecimal: condecimal(gt=1, le=5, multiple_of=2)


class Failing(BaseModel):
    my_list: list
    my_tuple: tuple
    my_set: set
    my_tuple_str_int: Tuple[str, int]
    my_enum: Enum
    my_conint: conint(gt=1, lt=6, multiple_of=2)
    my_PositiveInt: PositiveInt
    my_NegativeInt: NegativeInt
    my_ConstrainedFloat: confloat(gt=1.0, lt=6.7)
    my_PositiveFloat: PositiveFloat
    my_NegativeFloat: NegativeFloat
    my_condecimal: condecimal(gt=1, le=5, multiple_of=2)


app = FastAPI()


@app.post("/workingtypes")
async def workingtypes(tt: Working):
    return tt


@app.post("/failingtypes")
async def failingtypes(tt: Failing):
    return tt


def test_openapi():
    with TestClient(app) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        print(response.json())
        with open("opentestapi.json", "w") as f:
            json.dump(response.json(), f)
