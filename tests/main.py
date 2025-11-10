import http
from typing import Dict, FrozenSet, List, Optional, Union

from fastapi import FastAPI, Path, Query

external_docs = {
    "description": "External API documentation.",
    "url": "https://docs.example.com/api-general",
}

app = FastAPI(openapi_external_docs=external_docs)


@app.api_route("/api_route")
def non_operation():
    return {"message": "Hello World"}


def non_decorated_route():
    return {"message": "Hello World"}


app.add_api_route("/non_decorated_route", non_decorated_route)


@app.get("/text")
def get_text():
    return "Hello World"


@app.get("/path/{item_id}")
def get_id(item_id):
    return item_id


@app.get("/path/str/{item_id}")
def get_str_id(item_id: str):
    return item_id


@app.get("/path/int/{item_id}")
def get_int_id(item_id: int):
    return item_id


@app.get("/path/float/{item_id}")
def get_float_id(item_id: float):
    return item_id


@app.get("/path/bool/{item_id}")
def get_bool_id(item_id: bool):
    return item_id


@app.get("/path/param/{item_id}")
def get_path_param_id(item_id: Optional[str] = Path()):
    return item_id


@app.get("/path/param-minlength/{item_id}")
def get_path_param_min_length(item_id: str = Path(min_length=3)):
    return item_id


@app.get("/path/param-maxlength/{item_id}")
def get_path_param_max_length(item_id: str = Path(max_length=3)):
    return item_id


@app.get("/path/param-min_maxlength/{item_id}")
def get_path_param_min_max_length(item_id: str = Path(max_length=3, min_length=2)):
    return item_id


@app.get("/path/param-gt/{item_id}")
def get_path_param_gt(item_id: float = Path(gt=3)):
    return item_id


@app.get("/path/param-gt0/{item_id}")
def get_path_param_gt0(item_id: float = Path(gt=0)):
    return item_id


@app.get("/path/param-ge/{item_id}")
def get_path_param_ge(item_id: float = Path(ge=3)):
    return item_id


@app.get("/path/param-lt/{item_id}")
def get_path_param_lt(item_id: float = Path(lt=3)):
    return item_id


@app.get("/path/param-lt0/{item_id}")
def get_path_param_lt0(item_id: float = Path(lt=0)):
    return item_id


@app.get("/path/param-le/{item_id}")
def get_path_param_le(item_id: float = Path(le=3)):
    return item_id


@app.get("/path/param-lt-gt/{item_id}")
def get_path_param_lt_gt(item_id: float = Path(lt=3, gt=1)):
    return item_id


@app.get("/path/param-le-ge/{item_id}")
def get_path_param_le_ge(item_id: float = Path(le=3, ge=1)):
    return item_id


@app.get("/path/param-lt-int/{item_id}")
def get_path_param_lt_int(item_id: int = Path(lt=3)):
    return item_id


@app.get("/path/param-gt-int/{item_id}")
def get_path_param_gt_int(item_id: int = Path(gt=3)):
    return item_id


@app.get("/path/param-le-int/{item_id}")
def get_path_param_le_int(item_id: int = Path(le=3)):
    return item_id


@app.get("/path/param-ge-int/{item_id}")
def get_path_param_ge_int(item_id: int = Path(ge=3)):
    return item_id


@app.get("/path/param-lt-gt-int/{item_id}")
def get_path_param_lt_gt_int(item_id: int = Path(lt=3, gt=1)):
    return item_id


@app.get("/path/param-le-ge-int/{item_id}")
def get_path_param_le_ge_int(item_id: int = Path(le=3, ge=1)):
    return item_id


@app.get("/query")
def get_query(query):
    return f"foo bar {query}"


@app.get("/query/optional")
def get_query_optional(query=None):
    if query is None:
        return "foo bar"
    return f"foo bar {query}"


@app.get("/query/int")
def get_query_type(query: int):
    return f"foo bar {query}"


@app.get("/query/int/optional")
def get_query_type_optional(query: Optional[int] = None):
    if query is None:
        return "foo bar"
    return f"foo bar {query}"


@app.get("/query/int/default")
def get_query_type_int_default(query: int = 10):
    return f"foo bar {query}"


@app.get("/query/param")
def get_query_param(query=Query(default=None)):
    if query is None:
        return "foo bar"
    return f"foo bar {query}"


@app.get("/query/param-required")
def get_query_param_required(query=Query()):
    return f"foo bar {query}"


@app.get("/query/param-required/int")
def get_query_param_required_type(query: int = Query()):
    return f"foo bar {query}"


@app.get("/query/mapping-params")
def get_mapping_query_params(queries: Dict[str, str] = Query({})):
    return {"queries": queries}


from pydantic import OnErrorOmit


@app.get("/query/mixed-params")
def get_mixed_mapping_query_params(
    sequence_mapping_queries: Dict[str, List[Union[str, OnErrorOmit[int]]]] = Query({}),
    mapping_query: Dict[str, str] = Query(),
    query: str = Query(),
):
    return {
        "queries": {
            "query": query,
            "mapping_query": mapping_query,
            "sequence_mapping_queries": sequence_mapping_queries,
        }
    }


@app.get("/query/mapping-sequence-params")
def get_sequence_mapping_query_params(
    queries: Dict[str, List[OnErrorOmit[int]]] = Query({}),
):
    return {"queries": queries}


@app.get("/query/mixed-type-params")
def get_mixed_mapping_mixed_type_query_params(
    sequence_mapping_queries: Dict[str, List[OnErrorOmit[int]]] = Query({}),
    mapping_query_str: Dict[str, OnErrorOmit[str]] = Query({}),
    mapping_query_int: Dict[str, OnErrorOmit[int]] = Query({}),
    query: int = Query(),
):
    return {
        "queries": {
            "query": query,
            "mapping_query_str": mapping_query_str,
            "mapping_query_int": mapping_query_int,
            "sequence_mapping_queries": sequence_mapping_queries,
        }
    }


@app.get("/enum-status-code", status_code=http.HTTPStatus.CREATED)
def get_enum_status_code():
    return "foo bar"


@app.get("/query/frozenset")
def get_query_type_frozenset(query: FrozenSet[int] = Query(...)):
    return ",".join(map(str, sorted(query)))


@app.get("/query/list")
def get_query_list(device_ids: List[int] = Query()) -> List[int]:
    return device_ids


@app.get("/query/list-default")
def get_query_list_default(device_ids: List[int] = Query(default=[])) -> List[int]:
    return device_ids
