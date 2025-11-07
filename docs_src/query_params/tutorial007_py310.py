from typing import Annotated, Dict, List, Union

from fastapi import FastAPI, Query
from pydantic import OnErrorOmit

app = FastAPI()


@app.get("/query/mixed-type-params")
def get_mixed_mapping_mixed_type_query_params(
    query: Annotated[int, Query()] = None,
    mapping_query_str_or_int: Annotated[
        Union[Dict[str, OnErrorOmit[str]], Dict[str, int]], Query()
    ] = None,
    mapping_query_int: Annotated[Dict[str, int], Query()] = None,
    sequence_mapping_int: Annotated[Dict[str, List[int]], Query()] = None,
):
    return {
        "query": query,
        "mapping_query_str_or_int": mapping_query_str_or_int,
        "mapping_query_int": mapping_query_int,
        "sequence_mapping_int": sequence_mapping_int,
    }
