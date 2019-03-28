from datetime import date, datetime, time, timedelta
from enum import Enum
from typing import List, Tuple, Dict, Union
from uuid import UUID

from pydantic import BaseModel, EmailStr, NameEmail, UrlStr, DSN, Decimal, UUID1, UUID3, \
    UUID4, UUID5, FilePath, DirectoryPath, Path, Json, IPvAnyAddress, StrictStr, \
    ConstrainedStr, constr, ConstrainedInt, conint, PositiveInt, NegativeInt, \
    ConstrainedFloat, confloat, PositiveFloat, NegativeFloat, ConstrainedDecimal, \
    condecimal
from starlette.testclient import TestClient

from fastapi import FastAPI


class MyConstrainedInt(ConstrainedInt):
    gt = 1
    lt = 10


class MyConstrainedFloat(ConstrainedFloat):
    gt: 1.0
    le: 2.0


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
    # my_IPvAnyAddress: IPvAnyAddress
    my_StrictStr: StrictStr
    # my_ConstrainedStr: ConstrainedStr
    my_constr: constr(regex='^text$', min_length=2, max_length=10)
    # my_ConstrainedInt: MyConstrainedInt
    # my_conint: conint(gt=1, lt=6, multiple_of=2)
    # my_PositiveInt: PositiveInt
    # my_NegativeInt: NegativeInt
    my_ConstrainedFloat: MyConstrainedFloat
    # my_confloat: confloat(gt=1.0, lt=6.7)
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
    # my_IPvAnyAddress: IPvAnyAddress  # crash Pydantic if declared this way, no idea how to use
    # my_ConstrainedStr: ConstrainedStr  # crash Pydantic if declared this way, no idea how to use  # crash Pydantic
    my_ConstrainedInt: MyConstrainedInt
    my_conint: conint(gt=1, lt=6, multiple_of=2)
    my_PositiveInt: PositiveInt
    my_NegativeInt: NegativeInt
    my_confloat: confloat(gt=1.0, lt=6.7)
    my_PositiveFloat: PositiveFloat
    my_NegativeFloat: NegativeFloat
    my_condecimal: condecimal(gt=1, le=5, multiple_of=2)


app = FastAPI()


@app.post("/workingtypes")
async def types(tt: Working):
    return tt


@app.post("/failingtypes")
async def types(tt: Failing):
    return tt


def test_openapi():
    with TestClient(app) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        print(response.json())

