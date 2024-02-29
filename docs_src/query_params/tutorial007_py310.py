from typing import List, Mapping

from fastapi import FastAPI, Query
from fastapi.types import FFQuery

app = FastAPI()


@app.get("/query/mixed-type-params")
def get_mixed_mapping_mixed_type_query_params(
    query: int = Query(),
    mapping_query_str: FFQuery[str, str] = Query({}),
    mapping_query_int: FFQuery[str, int] = Query({}),
    sequence_mapping_queries: FFQuery[str, List[int]] = Query({}),
):
    return {
        "query": query,
        "string_mapping": mapping_query_str,
        "mapping_query_int": mapping_query_int,
        "sequence_mapping_queries": sequence_mapping_queries,
    }
