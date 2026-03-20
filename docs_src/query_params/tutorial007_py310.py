from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/query/mixed-type-params")
def get_mixed_mapping_mixed_type_query_params(
    query: Annotated[int, Query()] = None,
    mapping_query_str: Annotated[dict[str, str], Query()] = None,
    mapping_query_int: Annotated[dict[str, int], Query()] = None,
    sequence_mapping_int: Annotated[dict[str, list[int]], Query()] = None,
):
    return {
        "query": query,
        "mapping_query_str": mapping_query_str,
        "mapping_query_int": mapping_query_int,
        "sequence_mapping_int": sequence_mapping_int,
    }
